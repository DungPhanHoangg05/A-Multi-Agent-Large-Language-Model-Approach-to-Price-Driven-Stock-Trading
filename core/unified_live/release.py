"""Khóa nguồn, cohort và quyền U08 riêng, không sửa receipt U06/U07."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import subprocess
from typing import Any
import zipfile
import json

from core.historical_evaluation_journal import load, save
from core.unified_contracts import digest
from core.unified_protocol import binding, read, MANIFEST, safe, git_blob

DOC = "docs/plan/week12/"
RUNTIME = DOC + "unified_live_runtime.json"
PREFLIGHT = DOC + "unified_live_preflight.json"
CHECKS = DOC + "unified_live_checks.json"
GRANTS = {phase: DOC + "unified_live_" + phase.lower() + "_release.json" for phase in ("SMOKE", "RESEARCH")}
NAMESPACES = {"SMOKE": "outputs/unified_integration/u08_smoke_r1",
              "RESEARCH": "outputs/unified_integration/u08_research_r1"}
U07_SHA = "c77da519973da453bd0581951421528d9567704a6b8ec17f39a9653cbf3a8d21"
LIMITS = {"rpm": 30, "rpd": 1000, "tpm": 8000, "tpd": 200000}


def anchored(root: Path, name: str) -> dict[str, Any]:
    """Mọi quyền phải neo Git, không nhận file tự ghi lại sau khi bắt đầu inference."""
    path = safe(root, name)
    if path.read_bytes() != git_blob(root, "HEAD", name):
        raise ValueError("Nguồn/quyền U08 chưa neo Git: " + name)
    return load(path)


def baseline(root: Path) -> dict[str, Any]:
    """Đối soát672 pin U07 và input/runtime U06; source mới có manifest riêng."""
    from scripts.check_unified_execution import checked_inputs
    package = root / DOC / "unified_execution_checks.zip"
    if hashlib.sha256(package.read_bytes()).hexdigest() != U07_SHA:
        raise ValueError("Gói U07 đã đổi")
    with zipfile.ZipFile(package) as archive:
        sources = json.loads(archive.read("source_bindings.json"))
    for name, expected in sources.items():
        if binding(root, name) != expected:
            raise ValueError("Nguồn U07 đã đổi: " + name)
    return checked_inputs(root)


def history(root: Path) -> dict[int, list[dict[str, Any]]]:
    """Dedup theo org/UUID, giữ nguyên khoản charge/reserve của497 request lịch sử."""
    result: dict[int, dict[str, dict]] = {org: {} for org in range(1, 6)}
    for item in read(root, MANIFEST, True)["quota_ledgers"]:
        org = int(Path(item["path"]).stem.removeprefix("org"))
        for row in read(root, item["path"])["requests"]:
            value = {k: deepcopy(row[k]) for k in ("id", "model", "started_at", "reserved_tokens", "total_tokens",
                     "status", "completed_at", "retry_until", "rate_limits") if k in row}
            previous = result[org].get(row["id"])
            if previous is not None and previous != value:
                raise ValueError("Carry khác nội dung cho cùng UUID")
            result[org][row["id"]] = value
    return {org: list(rows.values()) for org, rows in result.items()}


def freeze_runtime(root: Path) -> dict[str, Any]:
    """Tạo manifest trước inference, khóa code mới và cả107 package cũ."""
    parent = baseline(root)
    names = [p.relative_to(root).as_posix() for folder in ("core/unified_live", "scripts/unified_live", "tests/unified_live")
             for p in sorted((root / folder).rglob("*")) if p.is_file() and "__pycache__" not in p.parts]
    sources = {n: binding(root, n) for n in names}
    checks = load(root / CHECKS)
    if (checks["status"] != "PASS" or checks["sources"] != sources or checks["failures"] or checks["errors"]
            or checks["skips"] or checks["tests"] != len(set(checks["test_ids"])) or not checks["compiled"]):
        raise ValueError("Kiểm thử U08 chưa PASS trên đúng source hiện hành")
    points = [{"id": p["runner_point_id"], "symbol": p["symbol"], "cutoff": p["date"], "fold": p["fold"],
               "quality": "U08_HOSTED_HISTORICAL_EXPLORATORY"} for p in read(root, MANIFEST, True)["points"]]
    return {"version": "unified_live_runtime_v1", "sources": sources, "checks": binding(root, CHECKS),
        "baseline_manifest_sha256": digest(parent), "runtime": parent["runtime"], "points": points,
        "smoke_point_id": min(p["id"] for p in points), "variants": read(root, DOC + "unified_comparison_protocol_v2.json")["variants"],
        "protocol": binding(root, DOC + "unified_comparison_protocol_v2.json"),
        "config": read(root, "docs/plan/week11/historical_evaluation_protocol.json", True)["inference"]["config"],
        "repeats": 3, "realizations": 1, "limits": LIMITS, "attempt_cap": 3,
        "price_transform": "DONOR_THOUSAND_VND_TIMES_1000_ONCE_FOR_CANONICAL_OUTCOME",
        "native_rowwise_causal_gate": "FAIL", "whole_system_causal_gate": "NOT_CERTIFIED",
        "scope": "HISTORICAL_EXPLORATORY_EXPOSED_COHORT"}


def validate_runtime(root: Path) -> dict[str, Any]:
    """Không tạo client hoặc numeric provider; dừng nếu nguồn/runtime đã đổi."""
    runtime = anchored(root, RUNTIME)
    if freeze_runtime(root) != runtime:
        raise ValueError("Nguồn/cohort/runtime khác manifest U08")
    return runtime


def require_release(root: Path, phase: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Release mới theo yêu cầu tiếp tục U08; grant legacy không nằm trong đường cấp quyền."""
    if phase not in GRANTS:
        raise ValueError("Phase U08 không hợp lệ")
    grant = anchored(root, GRANTS[phase])
    runtime = validate_runtime(root)
    preflight = anchored(root, PREFLIGHT)
    if (grant.get("status") != phase + "_RELEASED" or grant.get("api") is not True
            or grant.get("paid_api_allowed") is not False or grant.get("spend_limit_usd") != 0
            or grant.get("runtime_sha256") != digest(runtime) or grant.get("preflight_sha256") != digest(preflight)
            or grant.get("authorization") != "USER_REQUEST_CONTINUE_U08_2026_11_10"
            or grant.get("phase") != phase or grant.get("namespace") != NAMESPACES[phase]
            or grant.get("max_http_attempts") != (30 if phase == "SMOKE" else 7956)
            or preflight["limits"] != LIMITS or preflight["organizations_independent_user_attested"] != 5
            or not preflight["metadata"]["all_required_models_listed"]):
        raise ValueError("Release/quota U08 không khớp hoặc có quyền paid")
    if phase == "RESEARCH":
        receipt = load(root / NAMESPACES["SMOKE"] / "receipt.json")
        expected = identity(runtime, "SMOKE", digest(preflight))
        smoke_identity = load(root / NAMESPACES["SMOKE"] / "identity.json")["identity"]
        if (receipt["status"] != "PASS_U08_SMOKE" or digest(receipt) != grant.get("smoke_receipt_sha256")
                or smoke_identity != expected or receipt.get("identity_sha256") != digest(expected)
                or receipt.get("api") is not True or receipt.get("forecast_slots") != 8
                or receipt.get("complete_points") != 1 or receipt.get("http_attempts", 31) > 30):
            raise ValueError("Research chưa có cold smoke đúng epoch")
    return runtime, grant


def identity(runtime: dict[str, Any], phase: str, preflight_sha256: str) -> dict[str, Any]:
    """Không dùng smoke response hoặc UUID làm repeat của study chính."""
    config = runtime["config"]
    models = config["signal_config"]["models"]
    options = {"model": models["graph_llm_model"], "stream": False, "n": 1,
        "temperature": max(1e-8, models["graph_llm_temperature"]), "stop": None,
        "reasoning_format": None, "reasoning_effort": None, "service_tier": config["service_tier"],
        **config["client_options"]["graph"], "max_tokens": models["graph_llm_max_tokens"]}
    return {"version": "unified_hosted_run_v1", "mode": "HOSTED", "phase": phase,
        "epoch": "U08_" + phase + "_R1", "runtime_sha256": digest(runtime), "preflight_sha256": preflight_sha256,
        "points": runtime["points"], "smoke_point_id": runtime["smoke_point_id"],
        "repeats": 1 if phase == "SMOKE" else 3, "realizations": 1,
        "attempt_cap_total": 30 if phase == "SMOKE" else 7956, "vision_options": options}
