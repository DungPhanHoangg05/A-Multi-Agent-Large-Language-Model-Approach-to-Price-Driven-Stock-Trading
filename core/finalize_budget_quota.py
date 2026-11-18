"""Quota FIN09 theo một org Free, đo carry local và ước tính theo model."""
from __future__ import annotations

from collections import Counter
from contextlib import closing
from datetime import datetime, timezone
import math
from pathlib import Path
import sqlite3

from core.groq_pacing import MODEL_LIMITS
from core.unified_protocol import binding, read

ORG = 1
BANK_JOURNAL = "tmp/fin06_bank_hosted_single_org_v1/"
SERVING_LEDGERS = ("outputs/serving_inference/v1/quota.sqlite3", "outputs/serving_live/outputs/serving_inference/v1/quota.sqlite3")
ATTEMPT_CAP = 3


def charge(row: dict) -> int:
    """UNKNOWN/thiếu usage giữ toàn reserve; NOT_SENT đã đối soát không charge."""
    if row["status"] == "NOT_SENT":
        return 0
    usage = row.get("total_tokens")
    value = row["reserved_tokens"] if row["status"] == "UNKNOWN" or usage is None else usage
    if type(value) is not int or value < 0:
        raise ValueError("Usage FIN09 ngoài miền hợp lệ")
    return value


def window(values: list[dict], now: float, seconds: float) -> dict:
    """Chỉ đếm attempt trong cửa sổ; đếm UUID một lần trên mỗi ledger logic."""
    rows = {}
    for row in values:
        timestamp = row["started_at"]
        if now-seconds < timestamp <= now and row["status"] != "NOT_SENT":
            key = row["id"]
            if key in rows and rows[key] != row:
                raise ValueError("Carry khác nội dung cho cùng UUID")
            rows[key] = row
    return {"requests": len(rows), "tokens_charged_or_reserved": sum(charge(r) for r in rows.values()),
            "unknown": sum(r["status"] == "UNKNOWN" for r in rows.values())}


def local_quota(root: Path, carry: list[dict], observed_at: str) -> dict:
    """Đọc ledger chọn org, phân biệt nguồn không nhận diện org/model và quota nhà cung cấp."""
    timestamp = datetime.fromisoformat(observed_at)
    if timestamp.tzinfo is None:
        raise ValueError("Mốc quota cần timezone")
    now = timestamp.timestamp()
    rows = [r for r in carry if r.get("org") == ORG and r.get("model") in MODEL_LIMITS]
    bindings, raw_headers = [], {}
    journal = root / (BANK_JOURNAL + "quota.json")
    if journal.is_file():
        identity = read(root, BANK_JOURNAL + "identity.json", True)
        if identity["org_slot"] != ORG or identity["spend_limit_usd"] != 0:
            raise ValueError("Bank carry thuộc org hoặc phạm vi chi phí khác")
        quota = read(root, BANK_JOURNAL + "quota.json")
        bindings = [binding(root, BANK_JOURNAL + name) for name in ("identity.json", "quota.json")]
        for entry in quota["requests"]:
            rows.append({k: entry.get(k) for k in ("id", "model", "status", "started_at", "reserved_tokens", "total_tokens")})
            if entry.get("rate_limits") and entry["started_at"] <= now:
                raw_headers[entry["model"]] = {k: v for k, v in entry["rate_limits"].items()
                                               if k == "date" or k.startswith("x-ratelimit-")}

    unattributed = []
    checked_stores = []
    for relative in SERVING_LEDGERS:
        path = root / relative
        if not path.is_file():
            continue
        # Đọc metadata quota thuần, không truy cập bảng credential/signing secret.
        with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
            observations = db.execute("SELECT id,started,reserve,used,state FROM attempts WHERE started>? AND started<=?",
                                      (now-86400, now)).fetchall()
        checked_stores.append(relative)
        unattributed.extend({"id": i, "started_at": start, "reserved_tokens": reserve, "total_tokens": used, "status": status}
                            for i, start, reserve, used, status in observations)
    unknown_day = window(unattributed, now, 86400)
    unknown_minute = window(unattributed, now, 61)
    models = {}
    for name, limits in MODEL_LIMITS.items():
        relevant = [r for r in rows if r["model"] == name]
        day_budget, minute_budget = window(relevant, now, 86400), window(relevant, now, 61)
        models[name] = {"assumed_limits": limits, "known_24h": day_budget, "known_61s": minute_budget,
            "local_estimated_day_tokens_remaining": max(0, limits["tpd"]-day_budget["tokens_charged_or_reserved"]
                                                                  -unknown_day["tokens_charged_or_reserved"]),
            "local_estimated_day_requests_remaining": max(0, limits["rpd"]-day_budget["requests"]-unknown_day["requests"]),
            "local_estimated_minute_tokens_remaining": max(0, limits["tpm"]-minute_budget["tokens_charged_or_reserved"]
                                                                     -unknown_minute["tokens_charged_or_reserved"]),
            "provider_remaining_now": None, "last_fin06_headers_historical": raw_headers.get(name)}
    return {"org_slot": ORG, "observed_at_utc": timestamp.astimezone(timezone.utc).isoformat(), "models": models,
            "other_local_stores_without_org_mapping": checked_stores, "unattributed_24h_conservative": unknown_day,
            "bank_quota_sources": bindings, "throughput_scope": "SINGLE_ORG_NO_QUOTA_AGGREGATION",
            "source_scope": "LOCAL_LEDGER_ESTIMATE_NOT_ACCOUNT_BALANCE", "paid_allowed": False, "spend_limit_usd": 0}


def capacity_windows(tokens: int, requests: int, quota: dict) -> int:
    """Số cửa sổ 24h để cấp đủ quota trong kịch bản, kể carry của cửa sổ đầu."""
    if requests == 0:
        return 0
    limits = quota["assumed_limits"]
    future_tokens = max(0, tokens-quota["local_estimated_day_tokens_remaining"])
    future_requests = max(0, requests-quota["local_estimated_day_requests_remaining"])
    return 1 + max(math.ceil(future_tokens/limits["tpd"]), math.ceil(future_requests/limits["rpd"]))


def summarize(rows: list[dict], quota: dict, telemetry: dict) -> dict:
    """Gộp first attempt, reserve retry và thời gian theo model/phase."""
    groups = {}
    for phase in ("RESEARCH", "SMOKE", "TOTAL"):
        slots = rows if phase == "TOTAL" else [row for row in rows if row["phase"] == phase]
        phases = {"logical_slots": len(slots), "states": dict(Counter(r["state"] for r in slots)), "models": {}}
        for model in MODEL_LIMITS:
            planned = [r for r in slots if r["state"] == "NEW" and r["model"] == model]
            budgets = [r["attempt_reserve_tokens"] for r in planned]
            phase_reserve = sum(budgets)
            all_attempts_reserve = sum(r["all_attempts_reserve_tokens"] for r in planned)
            q = quota["models"][model]
            # Telemetry lịch sử cùng role là kịch bản tham khảo, không phải số usage FIN11.
            p50 = sum(telemetry[r["role"]]["p50"] for r in planned) if planned else 0
            p95 = sum(telemetry[r["role"]]["p95"] for r in planned) if planned else 0
            phases["models"][model] = {"new_requests_first_attempt": len(planned), "max_attempts": ATTEMPT_CAP*len(planned),
                "first_attempt_fixture_reserve_tokens": phase_reserve,
                "all_attempts_fixture_reserve_tokens": all_attempts_reserve,
                "admission_upper_bound_all_attempts_tokens": ATTEMPT_CAP*len(planned)*q["assumed_limits"]["tpm"],
                "max_fixture_attempt_tokens": max(budgets, default=0), "historical_usage_p50_scenario": p50,
                "historical_usage_p95_scenario": p95,
                "one_org_24h_windows_p50_scenario": capacity_windows(p50, len(planned), q),
                "one_org_24h_windows_p95_scenario": capacity_windows(p95, len(planned), q),
                "one_org_24h_windows_fixture_reserve": capacity_windows(phase_reserve, len(planned), q),
                "one_org_24h_windows_all_attempts_fixture_reserve": capacity_windows(
                    all_attempts_reserve, ATTEMPT_CAP*len(planned), q)}
        groups[phase] = phases
    return groups
