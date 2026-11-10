"""Khóa amendment riêng và nối collector thủ công vào journal U08 hiện hữu."""
from __future__ import annotations

import hashlib
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
from core.unified_execution_transport import Deferred, wire_state
from core.unified_live.execution import HostedRunner, verify
from core.unified_live.manager import canonical_outcome, guard_for, run_identity, verify_phase
from core.unified_live.release import anchored, binding, require_release, NAMESPACES
from core.unified_live.transport import LiveHTTP, carry_smoke
from core.unified_live.release import history
from core.unified_model_quota.policy import POLICY, ModelCalls, admit, row_model

DOC = "docs/plan/week12/"
RUNTIME = DOC + "unified_model_quota_runtime.json"
CHECKS = DOC + "unified_model_quota_checks.json"
GRANT = DOC + "unified_model_quota_release.json"
FOLDERS = ("core/unified_model_quota", "scripts/unified_model_quota", "tests/unified_model_quota")
AUTHORIZATION = "USER_REQUEST_SEPARATE_MODEL_QUOTAS_MANUAL_LAUNCH_2026_11_10"


def sources(root: Path) -> dict[str, Any]:
    """Khóa riêng source amendment, nối tiếp các pin nguồn U06/U07/U08."""
    return {path.relative_to(root).as_posix(): binding(root, path.relative_to(root).as_posix())
            for folder in FOLDERS for path in sorted((root / folder).rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts}


def prefix(root: Path) -> dict[str, Any]:
    """Chụp prefix raw và mọi slot complete trước khi sửa policy, giữ nguyên byte."""
    directory = root / NAMESPACES["RESEARCH"]
    state = wire_state(directory)
    if any(row["status"] == "UNKNOWN" for row in state["rows"]):
        raise ValueError("Phải đối soát UNKNOWN trước amendment quota")
    identity = load(directory / "identity.json")["identity"]
    book = StageBook(directory, identity, verify_only=True)
    complete = {}
    for path in sorted((directory / "slots").glob("*.json")):
        document = load(path)
        if document["attempts"][0]["status"] == "complete":
            book.execute(document["slot"], document["inputs"], None)
            complete[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"identity": binding(root, (directory / "identity.json").relative_to(root).as_posix()),
            "wire_identity_sha256": digest(state["identity"]), "carry_sha256": digest(state["carry"]),
            "http": load(directory / "wire.json")["rows"], "complete_slots": complete}


def check_prefix(directory: Path, value: dict[str, Any]) -> dict[str, Any]:
    """Resume được append HTTP mới, mọi raw/complete slot thuộc prefix phải khớp."""
    if hashlib.sha256((directory / "identity.json").read_bytes()).hexdigest() != value["identity"]["sha256"]:
        raise ValueError("Identity nghiên cứu đã đổi")
    index = load(directory / "wire.json")
    if index["rows"][:len(value["http"])] != value["http"]:
        raise ValueError("Prefix raw trước amendment đã đổi")
    state = wire_state(directory)
    if digest(state["identity"]) != value["wire_identity_sha256"] or digest(state["carry"]) != value["carry_sha256"]:
        raise ValueError("Wire identity hoặc carry trước amendment đã đổi")
    for name, expected in value["complete_slots"].items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Slot complete trước amendment đã đổi")
    for row in state["carry"] + state["rows"]:
        row_model(row)
    return state


def build_runtime(root: Path, parent: dict[str, Any], grant: dict[str, Any], before: dict[str, Any]) -> dict[str, Any]:
    """Cohort, serving và run UUID được neo vào manifest U08 đã nghiệm thu."""
    pins = sources(root)
    checks = load(root / CHECKS)
    if (checks["status"] != "PASS" or checks["sources"] != pins or checks["failures"] or checks["errors"]
            or checks["skips"] or checks["tests"] != len(set(checks["test_ids"])) or not checks["compiled"]):
        raise ValueError("Scoped checks chưa PASS trên source amendment")
    return {"version": "unified_model_quota_runtime_v1", "policy": POLICY,
            "limits_by_model": MODEL_LIMITS, "parent_runtime_sha256": digest(parent),
            "parent_grant_sha256": digest(grant), "sources": pins, "checks": binding(root, CHECKS),
            "prefix": before, "first_model_scoped_http_sequence": len(before["http"]),
            "authorization": AUTHORIZATION, "manual_launch_only": True,
            "scope": "ADMISSION_ONLY_PRESERVE_RUN_UUID_FORECASTS_AND_RETRY_CAP"}


def prepare(root: Path) -> dict[str, Any]:
    """Tạo manifest/grant mới bằng thao tác offline dưới cả hai khóa của run."""
    from scripts.unified_live.run import create
    parent, parent_grant = require_release(root, "RESEARCH")
    directory = root / NAMESPACES["RESEARCH"]
    run = run_identity(root, "RESEARCH", parent)
    with PriorRunLock(directory / "manager", digest(run)), PriorRunLock(directory, digest(run)):
        runtime = build_runtime(root, parent, parent_grant, prefix(root))
        create(root / RUNTIME, runtime)
        grant = {"version": "unified_model_quota_release_v1", "status": "MODEL_QUOTA_RELEASED",
                 "runtime_sha256": digest(runtime), "policy": POLICY, "authorization": AUTHORIZATION,
                 "manual_launch_only": True, "api": True, "paid_api_allowed": False, "spend_limit_usd": 0,
                 "namespace": NAMESPACES["RESEARCH"], "max_http_attempts": parent_grant["max_http_attempts"]}
        create(root / GRANT, grant)
    # Artifact mới dùng LF để byte làm việc khớp Git trên Windows.
    for name in (RUNTIME, GRANT):
        path = root / name
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    return {"status": "PREPARED_MANUAL_MODEL_QUOTA", "prefix_http": len(runtime["prefix"]["http"])}


def require(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Kiểm grant amendment và nguồn trước khi cho đọc credential hoặc tạo client."""
    parent, parent_grant = require_release(root, "RESEARCH")
    runtime, grant = anchored(root, RUNTIME), anchored(root, GRANT)
    anchored(root, CHECKS)
    if runtime != build_runtime(root, parent, parent_grant, runtime["prefix"]):
        raise ValueError("Nguồn hoặc phạm vi amendment quota đã đổi")
    expected = {"version": "unified_model_quota_release_v1", "status": "MODEL_QUOTA_RELEASED",
                "runtime_sha256": digest(runtime), "policy": POLICY, "authorization": AUTHORIZATION,
                "manual_launch_only": True, "api": True, "paid_api_allowed": False, "spend_limit_usd": 0,
                "namespace": NAMESPACES["RESEARCH"], "max_http_attempts": parent_grant["max_http_attempts"]}
    if grant != expected:
        raise ValueError("Grant quota theo model không đúng phạm vi thủ công/Free")
    check_prefix(root / NAMESPACES["RESEARCH"], runtime["prefix"])
    return parent, parent_grant, runtime


def verify_admissions(state: dict[str, Any], first: int, cap: int) -> None:
    """Cold kiểm từng HTTP mới từ lịch sử đã biết ở đúng thời điểm dispatch."""
    for index in range(first, len(state["rows"])):
        row = state["rows"][index]
        prior = {"carry": state["carry"], "rows": state["rows"][:index]}
        try:
            admit(prior, row["org"], row_model(row), row["reserved_tokens"], row["started_at"], cap)
        except Deferred:
            raise ValueError("HTTP sau amendment vi phạm quota org/model") from None


def audit(root: Path, *, seal: bool = False) -> dict[str, Any]:
    """Cold verify phần đã thu, chỉ đọc payoff của những điểm đã đủ forecast durable."""
    from core.unified_execution_providers import cold_methods
    parent, grant, runtime = require(root)
    directory = root / NAMESPACES["RESEARCH"]
    run = run_identity(root, "RESEARCH", parent)
    with PriorRunLock(directory, digest(run)):
        state = check_prefix(directory, runtime["prefix"])
        verify_admissions(state, runtime["first_model_scoped_http_sequence"], grant["max_http_attempts"])
        result = verify(directory, run, cold_methods(root, parent["config"]), require_complete=seal)
        book = StageBook(directory, run, verify_only=True)
        for point in run["points"]:
            if book.complete("outcome/" + point["id"]):
                saved = load(book.path("outcome/" + point["id"]))["attempts"][0]["output"]
                if saved != canonical_outcome(root, point):
                    raise ValueError("Canonical label không tái lập")
        result.update(quota_policy=POLICY, quota_runtime_sha256=digest(runtime),
                      first_model_scoped_http_sequence=runtime["first_model_scoped_http_sequence"])
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
            base = verify_phase(root, "RESEARCH", seal=True)
            result["execution_receipt_sha256"] = digest(base)
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
        pins = {**runtime["sources"], **{name: binding(root, name) for name in (RUNTIME, CHECKS)}}
        def guard() -> None:
            """Kiểm cả grant gốc và amendment trước mọi intent/dispatch."""
            parent_guard()
            if anchored(root, GRANT) != expected_grant or any(binding(root, name) != value for name, value in pins.items()):
                raise ValueError("Nguồn/grant amendment quota đã đổi")
        sender = LiveHTTP(root, "RESEARCH", guard)
        try:
            calls = ModelCalls(directory, run, sender, carry_smoke(root, history(root)), guard=guard)
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
        command = [sys.executable, "-I", "-X", "utf8", "scripts/unified_model_quota/run.py", "verify", "--seal"]
        verified = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8")
        (directory / "quota_cold_verify.log").write_text(verified.stdout + verified.stderr, encoding="utf-8")
        if verified.returncode:
            result.update(status="COLD_VERIFY_FAILED", updated_at=utc_now())
            save(directory / "status.json", result)
            raise ValueError("Cold verify quota chưa PASS, journal đã giữ đủ")
        result = load(directory / "quota_receipt.json")
        save(directory / "status.json", {**result, "updated_at": utc_now()})
        return result
