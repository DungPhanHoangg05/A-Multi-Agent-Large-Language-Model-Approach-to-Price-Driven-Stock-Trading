"""Khóa chuyển policy tại prefix hiện có và cold replay đúng từng giai đoạn."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

from core.groq_pacing import MODEL_LIMITS
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock, process_start, utc_now
from core.unified_contracts import digest
from core.unified_execution import StageBook
from core.unified_execution_transport import Deferred
from core.unified_live.execution import HostedRunner, verify
from core.unified_live.manager import canonical_outcome, guard_for, run_identity, verify_phase
from core.unified_live.release import anchored, binding, NAMESPACES, history
from core.unified_live.transport import LiveHTTP, carry_smoke
from core.unified_model_quota import runtime as model_runtime
from core.unified_model_quota.runtime import prefix, check_prefix
from core.unified_model_quota.policy import row_model
from core.unified_provider_quota.policy import POLICY, ProviderCalls, admit

DOC = "docs/plan/week12/"
RUNTIME = DOC + "unified_provider_quota_runtime.json"
CHECKS = DOC + "unified_provider_quota_checks.json"
GRANT = DOC + "unified_provider_quota_release.json"
FOLDERS = ("core/unified_provider_quota", "scripts/unified_provider_quota", "tests/unified_provider_quota")
AUTHORIZATION = "USER_REQUEST_PROVIDER_DRIVEN_QUOTA_MANUAL_LAUNCH_2026_11_11"


def sources(root: Path) -> dict[str, Any]:
    """Khóa các file amendment mới bên cạnh hai thế hệ nguồn U08 trước đó."""
    return {path.relative_to(root).as_posix(): binding(root, path.relative_to(root).as_posix())
            for folder in FOLDERS for path in sorted((root / folder).rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts}


def build_runtime(root: Path, parent: dict[str, Any], before: dict[str, Any]) -> dict[str, Any]:
    """Ghi rõ điểm chuyển policy và quyền gửi dựa vào response thực của provider."""
    pins = sources(root)
    checks = load(root / CHECKS)
    if (checks["status"] != "PASS" or checks["sources"] != pins or checks["failures"] or checks["errors"]
            or checks["skips"] or checks["tests"] != len(set(checks["test_ids"])) or not checks["compiled"]):
        raise ValueError("Scoped checks provider admission chưa PASS")
    return {"version": "unified_provider_quota_runtime_v1", "policy": POLICY,
            "parent_model_runtime_sha256": digest(parent),
            "parent_model_grant_sha256": digest(anchored(root, model_runtime.GRANT)),
            "sources": pins, "checks": binding(root, CHECKS), "prefix": before,
            "first_model_scoped_http_sequence": parent["first_model_scoped_http_sequence"],
            "first_provider_scoped_http_sequence": len(before["http"]),
            "local_count_admission": False, "successful_header_admission": False,
            "provider_retry_after_and_backoff": True, "authorization": AUTHORIZATION,
            "manual_launch_only": True, "scope": "PROVIDER_ADMISSION_ONLY_SAME_RESEARCH_JOURNAL"}


def grant_for(runtime: dict[str, Any], cap: int) -> dict[str, Any]:
    """Grant mới gắn đúng amendment, phase cap và quyền khởi chạy thủ công."""
    return {"version": "unified_provider_quota_release_v1", "status": "PROVIDER_QUOTA_RELEASED",
            "runtime_sha256": digest(runtime), "policy": POLICY, "authorization": AUTHORIZATION,
            "manual_launch_only": True, "api": True, "paid_api_allowed": False, "spend_limit_usd": 0,
            "namespace": NAMESPACES["RESEARCH"], "max_http_attempts": cap}


def prepare(root: Path) -> dict[str, Any]:
    """Chụp prefix khi collector đã dừng, tạo manifest/grant bằng thao tác offline."""
    from scripts.unified_live.run import create
    parent, parent_grant, model = model_runtime.require(root)
    directory = root / NAMESPACES["RESEARCH"]
    run = run_identity(root, "RESEARCH", parent)
    with PriorRunLock(directory / "manager", digest(run)), PriorRunLock(directory, digest(run)):
        runtime = build_runtime(root, model, prefix(root))
        create(root / RUNTIME, runtime)
        create(root / GRANT, grant_for(runtime, parent_grant["max_http_attempts"]))
        status = load(directory / "status.json")
        status.update(status="STOPPED_BY_OPERATOR", quota_policy=POLICY, waiting={}, waiting_models={}, updated_at=utc_now())
        for name in ("next_resume_at", "heartbeat_at"):
            status.pop(name, None)
        save(directory / "status.json", status)
    for name in (RUNTIME, GRANT):
        path = root / name
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    return {"status": "PREPARED_MANUAL_PROVIDER_QUOTA", "prefix_http": len(runtime["prefix"]["http"])}


def require(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Đối soát cả hai release cha và grant mới trước khi đọc key hoặc dựng client."""
    parent, parent_grant, model = model_runtime.require(root)
    runtime, grant = anchored(root, RUNTIME), anchored(root, GRANT)
    anchored(root, CHECKS)
    if runtime != build_runtime(root, model, runtime["prefix"]):
        raise ValueError("Nguồn hoặc policy provider đã đổi")
    if grant != grant_for(runtime, parent_grant["max_http_attempts"]):
        raise ValueError("Grant provider admission sai phạm vi manual/Free")
    check_prefix(root / NAMESPACES["RESEARCH"], runtime["prefix"])
    return parent, parent_grant, runtime


def verify_admissions(state: dict[str, Any], model_first: int, provider_first: int, cap: int) -> None:
    """Tái lập đúng policy trước và sau amendment, không áp lịch cũ cho request mới."""
    if not 0 <= model_first <= provider_first <= len(state["rows"]):
        raise ValueError("Mốc chuyển policy không hợp lệ")
    model_runtime.verify_admissions({**state, "rows": state["rows"][:provider_first]}, model_first, cap)
    for index in range(provider_first, len(state["rows"])):
        row = state["rows"][index]
        prior = {"carry": state["carry"], "rows": state["rows"][:index]}
        try:
            admit(prior, row["org"], row_model(row), row["reserved_tokens"], row["started_at"], cap)
        except Deferred:
            raise ValueError("HTTP mới chưa hết Retry-After/backoff provider") from None


def audit(root: Path, *, seal: bool = False) -> dict[str, Any]:
    """Cold verify prefix và policy, chỉ đọc nhãn của các điểm đã đủ forecast."""
    from core.unified_execution_providers import cold_methods
    parent, grant, runtime = require(root)
    directory = root / NAMESPACES["RESEARCH"]
    run = run_identity(root, "RESEARCH", parent)
    with PriorRunLock(directory, digest(run)):
        state = check_prefix(directory, runtime["prefix"])
        verify_admissions(state, runtime["first_model_scoped_http_sequence"],
                          runtime["first_provider_scoped_http_sequence"], grant["max_http_attempts"])
        result = verify(directory, run, cold_methods(root, parent["config"]), require_complete=seal)
        book = StageBook(directory, run, verify_only=True)
        for point in run["points"]:
            if book.complete("outcome/" + point["id"]):
                saved = load(book.path("outcome/" + point["id"]))["attempts"][0]["output"]
                if saved != canonical_outcome(root, point):
                    raise ValueError("Canonical label không tái lập")
        result.update(quota_policy=POLICY, quota_runtime_sha256=digest(runtime),
                      first_model_scoped_http_sequence=runtime["first_model_scoped_http_sequence"],
                      first_provider_scoped_http_sequence=runtime["first_provider_scoped_http_sequence"])
        ready = []
        for org in range(1, 6):
            for model in MODEL_LIMITS:
                try:
                    admit(state, org, model, 8000, time.time(), grant["max_http_attempts"])
                    admission = "READY"
                except Deferred as error:
                    admission = {"resume_at": error.until}
                ready.append({"org": org, "model": model, "reserve": 8000, "admission": admission})
        if seal:
            result["execution_receipt_sha256"] = digest(verify_phase(root, "RESEARCH", seal=True))
            path = directory / "quota_receipt.json"
            if path.exists() and load(path) != result:
                raise ValueError("Receipt quota đã seal khác journal")
            save(path, result)
        return {**result, "current_admission_probe": ready}


def collect(root: Path) -> dict[str, Any]:
    """Driver thủ công version mới, tái dùng runner/oracle U08 và cùng hai khóa OS."""
    from core.unified_execution_providers import StudyProviders
    parent, parent_grant, runtime = require(root)
    directory = root / NAMESPACES["RESEARCH"]
    if (directory / "quota_receipt.json").exists():
        return audit(root, seal=True)
    run = run_identity(root, "RESEARCH", parent)
    with PriorRunLock(directory / "manager", digest(run)):
        result = load(directory / "status.json")
        result.update(quota_policy=POLICY, pid=os.getpid(), process_start=process_start(os.getpid()))
        if (directory / "stop.request").exists():
            result.update(status="STOPPED_BY_OPERATOR", updated_at=utc_now())
            save(directory / "status.json", result)
            return result
        parent_guard = guard_for(root, "RESEARCH", parent, parent_grant)
        expected_grant = anchored(root, GRANT)
        parent_quota = anchored(root, model_runtime.RUNTIME)
        pins = {**parent_quota["sources"], **runtime["sources"],
                **{name: binding(root, name) for name in (RUNTIME, CHECKS, model_runtime.RUNTIME, model_runtime.CHECKS, model_runtime.GRANT)}}
        def guard() -> None:
            """Kiểm cả grant gốc và amendment trước mọi intent/dispatch."""
            parent_guard()
            if anchored(root, GRANT) != expected_grant or any(binding(root, name) != value for name, value in pins.items()):
                raise ValueError("Nguồn/grant amendment quota đã đổi")
        sender = LiveHTTP(root, "RESEARCH", guard)
        try:
            calls = ProviderCalls(directory, run, sender, carry_smoke(root, history(root)), guard=guard)
            providers = StudyProviders(root, calls)
            runner = HostedRunner(directory, run, calls, providers)
            while True:
                if (directory / "stop.request").exists():
                    result.update(status="STOPPED_BY_OPERATOR", updated_at=utc_now())
                    save(directory / "status.json", result)
                    return result
                calls.waiting_models.clear()
                result = runner.tick(providers, lambda point: canonical_outcome(root, point))
                counts = {"shared_complete": 0, "forecast_complete": 0, "labels_complete": 0}
                for path in (directory / "slots").glob("*.json"):
                    document = load(path)
                    if document["attempts"][0]["status"] == "complete":
                        for key, prefix_name in (("shared_complete", "shared/"), ("forecast_complete", "forecast/"), ("labels_complete", "outcome/")):
                            counts[key] += int(document["slot"].startswith(prefix_name))
                result.update(counts, quota_policy=POLICY, waiting_models=calls.waiting_models,
                              http_attempts=len(calls.state["rows"]), updated_at=utc_now(),
                              pid=os.getpid(), process_start=process_start(os.getpid()))
                if result["blocked"]:
                    result["status"] = "BLOCKED_RECONCILIATION_REQUIRED"
                elif result["status"] != "COMPLETE":
                    result["status"] = "WAITING_QUOTA"
                save(directory / "status.json", result)
                print(json.dumps(result, ensure_ascii=False), flush=True)
                if result["status"] == "COMPLETE":
                    sender.close()
                    # Collector giữ manager lock trong suốt tiến trình cold verifier.
                    break
                if result["blocked"]:
                    return result
                if not result["waiting"]:
                    raise ValueError("Thiếu lý do chờ quota")
                until = min(float(value) for value in result["waiting"].values())
                while time.time() < until and not (directory / "stop.request").exists():
                    result.update(next_resume_at=until, heartbeat_at=utc_now())
                    save(directory / "status.json", result)
                    time.sleep(min(30., max(.01, until - time.time())))
        except Exception as error:
            result.update(status="STOPPED_ERROR", kind=type(error).__name__, reason=str(error)[:1000], updated_at=utc_now())
            save(directory / "status.json", result)
            raise
        finally:
            sender.close()
        command = [sys.executable, "-I", "-X", "utf8", "scripts/unified_provider_quota/run.py", "verify", "--seal"]
        verified = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8")
        (directory / "provider_cold_verify.log").write_text(verified.stdout + verified.stderr, encoding="utf-8")
        if verified.returncode:
            result.update(status="COLD_VERIFY_FAILED", updated_at=utc_now())
            save(directory / "status.json", result)
            raise ValueError("Cold verify quota chưa PASS, journal đã giữ đủ")
        result = load(directory / "quota_receipt.json")
        save(directory / "status.json", {**result, "updated_at": utc_now()})
        return result
