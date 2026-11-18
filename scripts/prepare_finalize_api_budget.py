"""Tái dựng dry-run FIN09 và kiểm ledger theo 102 point × 3 repeat, 0 completion."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_budget_archive import ARCHIVE, INVENTORY, RETIRED, Archive
from core.finalize_budget_quota import ATTEMPT_CAP, ORG, local_quota, summarize
from core.finalize_budget_study import NAMESPACE, VISION, StudyProvider, point_rows
from core.finalize_serving_profile import RECEIPT
from core.finalize_serving_resources import FinalizedResources
from core.groq_pacing import MODEL_LIMITS, tokenizer_cached
from core.serving_runtime.resources import default_models
from core.unified_contracts import digest, json_bytes
from core.unified_execution import StageBook
from core.unified_experiment import runtime_identity
from core.unified_preflight_assets import write_new
from core.unified_protocol import binding, ordered_branches, read
from scripts.verify_original_fix_parity import deny_external_network

CONTRACT = "docs/plan/week12/finalize_comparison_contract.json"
PREVIOUS_RUNTIME = "docs/plan/week12/unified_live_runtime.json"
LEDGER = "docs/plan/week12/finalize_api_budget_v1.json"
VERSION = "finalize_api_budget_v1"


def require(ok: bool, message: str) -> None:
    """Giữ gate độc lập chế độ tối ưu Python."""
    if not ok:
        raise ValueError(message)


def study(root: Path) -> tuple[list[dict], list[str], str, dict]:
    """Cohort đến từ FIN02 và đúng vai trò/repeat theo runtime lưu trữ."""
    contract = read(root, CONTRACT, True)
    old = read(root, PREVIOUS_RUNTIME, True)
    points = [{k: p[k] for k in ("id", "symbol", "cutoff", "fold")} | {"quality": "FINALIZE_RESEARCH_CONTROL_ONLY"}
              for p in contract["domain"]["primary_points"]]
    archived = [{k: p[k] for k in ("id", "symbol", "cutoff", "fold")} for p in old["points"]]
    require(len(points) == 102 and len({p["id"] for p in points}) == 102
            and [{k: v for k, v in p.items() if k != "quality"} for p in points] == archived,
            "Lịch FIN02 khác U08 hoặc không đủ 102 điểm")
    require(old["repeats"] == 3 and old["realizations"] == 1 and set(old["variants"]) == set(ordered_branches(0))
            and old["config"] == contract["model_options"]["candidate"] and old["smoke_point_id"] in {p["id"] for p in points},
            "Model/options hoặc recipe repeat/smoke khác FIN02")
    return points, old["variants"], old["smoke_point_id"], old["config"]


def recorded_usage(archive: Archive) -> dict:
    """P50/P95 xếp hạng gần nhất, chỉ raw200 active có usage, không dùng label."""
    cohort = {}
    for role in (*VISION, *ordered_branches(0)):
        sample = sorted(archive.telemetry[role])
        require(bool(sample), "Thiếu usage U08 cho " + role)
        cohort[role] = {"n": len(sample), "p50": sample[math.ceil(.50*len(sample))-1],
                        "p95": sample[math.ceil(.95*len(sample))-1], "max": sample[-1]}
    return cohort


def check_rows(rows: list[dict], points: list[dict], smoke_id: str) -> None:
    """Độc lập kiểm membership/slot/repeat/role/state và reserve semantics."""
    expected = set()
    for phase, identifiers, repeats in (("RESEARCH", [p["id"] for p in points], 3), ("SMOKE", [smoke_id], 1)):
        for identifier in identifiers:
            expected.update((phase, f"graph/{identifier}/{role}", role) for role in VISION)
            expected.update((phase, f"forecast/{identifier}/u0/r{repeat}/{role}", role)
                            for repeat in range(repeats) for role in ordered_branches(0))
    seen = {(r["phase"], r["slot"], r["role"]) for r in rows}
    require(seen == expected and len(seen) == len(rows) == 2662, "Ledger thiếu, thừa hoặc trùng slot")
    for row in rows:
        state, body, model = row["state"], row["fingerprints"], row["model"]
        require(state in {"NEW", "REUSE", "BYPASS", "UNKNOWN"} and model in MODEL_LIMITS, "State/model ngoài hợp đồng")
        require((body is None) == (state == "BYPASS"), "Body không khớp bypass")
        if state == "NEW":
            per_attempt = row["attempt_reserve_tokens"]
            require(0 < per_attempt <= MODEL_LIMITS[model]["tpm"]
                    and ATTEMPT_CAP*per_attempt <= row["all_attempts_reserve_tokens"] <= ATTEMPT_CAP*MODEL_LIMITS[model]["tpm"],
                    "Reserve mới khác cap/retry")
        else:
            require(row["attempt_reserve_tokens"] == row["all_attempts_reserve_tokens"] == 0, "Reserve cho slot không dispatch")
        if state == "REUSE":
            require(row["phase"] == "RESEARCH" and row["old"]["status"] == 200 and not row["old"]["repair"]
                    and row["old"]["fingerprints"] == body and row["new_wire_proof"] == "ACTUAL_BODY_BEFORE_TRANSPORT",
                    "Reuse thiếu proof body/HTTP200")


def check_archive(root: Path, result: dict) -> None:
    """Đối soát cả raw U08 theo hash index và ứng viên của từng slot nghiên cứu."""
    old = Archive(root)
    require(result["archive"]["verified_attempts"] == old.receipt["http_attempts"]
            and result["archive"]["archive_unknowns"] == dict(old.archive_unknowns)
            and result["historical_usage_by_role"] == recorded_usage(old), "Provenance hoặc usage U08 khác ledger")
    require(all(r["old"] == (old.candidate(r["slot"]) if r["phase"] == "RESEARCH" else None)
                for r in result["slots"]), "Ledger gán raw sai point/variant/repeat")
    require(all(source == binding(root, source["path"]) for source in result["quota"]["bank_quota_sources"]),
            "Carry FIN06 khác ledger")


def frozen_sources(root: Path) -> list[dict]:
    """Đóng băng toàn đường tạo request; FIN10 còn khóa runtime phát hành riêng."""
    names = (CONTRACT, PREVIOUS_RUNTIME, INVENTORY, RETIRED, RECEIPT, ARCHIVE+"receipt.json", ARCHIVE+"wire.json",
             "core/finalize_context.py", "core/finalize_prior.py", "core/finalize_serving_provider.py",
             "core/serving_runtime/providers.py", "utils/static_util.py", "core/groq_pacing.py",
             "core/unified_execution_transport.py", "core/unified_methods.py", "core/mt_bicl_prompt.py",
             "core/mt_bicl_decision.py", "agents/pattern_agent.py", "agents/trend_agent.py", "agents/decision_agent.py",
             "core/finalize_budget_archive.py", "core/finalize_budget_quota.py", "core/finalize_budget_study.py",
             "scripts/prepare_finalize_api_budget.py")
    return [binding(root, name) for name in names]


def provider_metadata(path: Path) -> dict:
    """Chỉ nhận receipt GET /models đã bỏ secret; không gọi metadata từ dry-run."""
    value = json.loads(path.read_bytes())
    fields = {"endpoint", "http_status", "inference_requests", "metadata_requests", "method", "model_access",
              "observed_at_utc", "org_slot", "rate_limit_headers_present", "status"}
    require(set(value) == fields and value["endpoint"] == "https://api.groq.com/openai/v1/models"
            and value["method"] == "GET" and value["org_slot"] == ORG and value["inference_requests"] == 0
            and value["metadata_requests"] == 1 and value["http_status"] == 200 and value["status"] == "OK"
            and value["model_access"] == dict.fromkeys(MODEL_LIMITS, True)
            and type(value["rate_limit_headers_present"]) is bool
            and datetime.fromisoformat(value["observed_at_utc"]).tzinfo is not None,
            "Metadata model thực chưa đủ cho org dự toán")
    return value


def produce(root: Path, metadata: dict, *, probe: bool = False) -> dict:
    """Dựng all requests offline trên nguồn FIN04/05/06/07 và wire archive U08."""
    require(tokenizer_cached(), "Thiếu tokenizer o200k đã pin")
    points, variants, smoke_id, config = study(root)
    archive = Archive(root)
    usage = recorded_usage(archive)
    quota = local_quota(root, archive.carry, datetime.now(timezone.utc).isoformat())
    resources = FinalizedResources(root)
    resources.verify()
    print(f"Đã kiểm {archive.receipt['http_attempts']} raw U08 và khóa carry org {ORG}", flush=True)
    provider = StudyProvider(resources, points, default_models(), variants)
    require(provider.config == {k: config[k] for k in provider.config}, "Provider chuyển options ngoài scope FIN02")
    rows = []
    with TemporaryDirectory(prefix="fin09-dry-run-") as directory:
        scratch = Path(directory)
        book = StageBook(scratch/"research", {"version": VERSION, "phase": "RESEARCH", "scope": "NO_TRANSPORT"})
        smoke = StageBook(scratch/"smoke", {"version": VERSION, "phase": "SMOKE", "scope": "NO_TRANSPORT"})
        selected = points if not probe else [next(p for p in points if p["id"] == smoke_id)]
        ordinals = {p["id"]: i for i, p in enumerate(points)}
        for i, point in enumerate(selected, start=1):
            rows.extend(point_rows(provider, archive, book, point, phase="RESEARCH", point_index=ordinals[point["id"]], repeats=3))
            if point["id"] == smoke_id:
                rows.extend(point_rows(provider, archive, smoke, point, phase="SMOKE", point_index=ordinals[smoke_id], repeats=1))
            if i == 1 or i % 10 == 0 or i == len(selected):
                print(f"Đã đối chiếu FIN09 {i}/{len(selected)} điểm", flush=True)
    budget = summarize(rows, quota, usage)
    if probe:
        return {"status": "PROBE_ONLY", "budget": budget}
    check_rows(rows, points, smoke_id)
    receipt = read(root, RECEIPT, True)
    prior = {key: value["READY"] for key, value in receipt["fallback_and_support"].items() if key != "MT_BICL"}
    expected = {**prior, "MT_BICL": receipt["fallback_and_support"]["MT_BICL"]["SUPPORTED"]}
    counted = Counter(r["role"] for r in rows if r["phase"] == "RESEARCH" and r["state"] != "BYPASS")
    require(all(counted[name] == count*3 for name, count in expected.items()), "Support fixture khác FIN07")
    return {"version": VERSION, "namespace": NAMESPACE, "status": "PASS_OFFLINE_FIN09_BUDGET",
        "model_options": config, "forecast_realizations": 1, "repeats": 3, "smoke_point_id": smoke_id,
        "attempt_cap_per_slot": ATTEMPT_CAP, "bank_new_executions": 0, "query_outcomes_opened": 0,
        "hosted_completions": 0, "execution_permitted": False,
        "execution_blockers": ["FIN10_RELEASE_PENDING", "ACCOUNT_FREE_LIMITS_AND_REMAINING_UNCONFIRMED"],
        "billing": {"tier_user_attested": "FREE", "paid_allowed": False, "spend_limit_usd": 0},
        "archive": {"verified_attempts": archive.receipt["http_attempts"], "archive_unknowns": dict(archive.archive_unknowns),
                    "archived_epoch": archive.identity["epoch"], "mixed_epoch_allowed_only_with_proof": True,
                    "same_alias_proves_same_weights": False},
        "model_metadata": metadata, "quota": quota, "historical_usage_by_role": usage,
        "budget": budget, "runtime": runtime_identity(), "source_bindings": frozen_sources(root), "slots": rows}


def main() -> None:
    """Check nhanh đối soát receipt/source/ledger; lần build tái tạo đầy đủ body."""
    deny_external_network()
    import torch
    torch.set_num_threads(1)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider-metadata", type=Path, help="Receipt GET /models đã bỏ credential")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--probe", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        result = read(ROOT, LEDGER, True)
        points, _, smoke, config = study(ROOT)
        check_rows(result["slots"], points, smoke)
        require(result["source_bindings"] == frozen_sources(ROOT) and result["model_options"] == config
                and result["runtime"] == runtime_identity() and result["budget"] == summarize(
                    result["slots"], result["quota"], result["historical_usage_by_role"]), "Ledger khác nguồn/summary/runtime")
        check_archive(ROOT, result)
    else:
        if args.provider_metadata is None:
            parser.error("Cần --provider-metadata")
        result = produce(ROOT, provider_metadata(args.provider_metadata), probe=args.probe)
        if not args.probe:
            write_new(ROOT/LEDGER, json_bytes({"payload": result, "sha256": digest(result)}))
    print(json_bytes({k: v for k, v in result.items() if k not in ("slots", "source_bindings")}).decode())


if __name__ == "__main__":
    main()
