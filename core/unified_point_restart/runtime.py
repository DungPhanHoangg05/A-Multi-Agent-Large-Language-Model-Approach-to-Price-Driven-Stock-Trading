"""Sao lưu và reset đúng các điểm lỗi theo yêu cầu người dùng, giữ toàn ledger."""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any
import zipfile

from core.groq_pacing import MODEL_LIMITS
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock, process_start, utc_now, safe_path
from core.unified_contracts import digest
from core.unified_execution import StageBook
from core.unified_execution_transport import Deferred, Exhausted, wire_state
from core.unified_live.manager import canonical_outcome, guard_for, run_identity
from core.unified_live.release import anchored, binding, NAMESPACES, history
from core.unified_live.transport import LiveHTTP, carry_smoke
from core.unified_model_quota import runtime as model_runtime
from core.unified_model_quota.runtime import check_prefix
from core.unified_model_quota.policy import row_model
from core.unified_provider_quota import runtime as provider_runtime
from core.unified_provider_quota.policy import admit
from core.unified_point_restart.wire import RestartCalls, point_id, attach_diagnostics
from core.unified_point_restart.execution import RestartRunner, verify

DOC = "docs/plan/week12/"
RUNTIME = DOC + "unified_point_restart_runtime.json"
CHECKS = DOC + "unified_point_restart_checks.json"
GRANT = DOC + "unified_point_restart_release.json"
BACKUP = DOC + "unified_point_restart_backup.zip"
FOLDERS = ("core/unified_point_restart", "scripts/unified_point_restart", "tests/unified_point_restart")
TARGETS = ("VCB-2026-04-01", "VJC-2025-12-19")
POLICY = "provider_response_point_restart_v1"
AUTHORIZATION = "USER_REQUEST_DELETE_FAILED_POINTS_AND_MANUAL_RERUN_2026_11_11"


def sources(root: Path) -> dict[str, Any]:
    """Khóa source reset riêng, mọi module và receipt cha được kiểm theo chuỗi cũ."""
    return {path.relative_to(root).as_posix(): binding(root, path.relative_to(root).as_posix())
            for folder in FOLDERS for path in sorted((root / folder).rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts}


def plan_reset(root: Path, run: dict[str, Any], targets: tuple[str, ...], protected: set[str]) -> dict[str, Any]:
    """Lập danh sách file chính xác, từ chối xóa điểm đã có label hoặc bằng chứng đã khóa."""
    directory = root / NAMESPACES["RESEARCH"]
    book = StageBook(directory, run, verify_only=True)
    state = wire_state(directory)
    if not targets or len(set(targets)) != len(targets) or not set(targets) <= {p["id"] for p in run["points"]}:
        raise ValueError("Danh sách điểm reset ngoài cohort")
    for target in targets:
        if book.complete("outcome/" + target):
            raise ValueError("Điểm đã hoàn chỉnh không thuộc yêu cầu reset lỗi")
        if not any(row["status"] == "UNKNOWN" and point_id(row["slot"]) == target for row in state["rows"]):
            raise ValueError("Điểm reset phải có UNKNOWN đã đối soát")
    if any(row["status"] == "UNKNOWN" and point_id(row["slot"]) not in targets for row in state["rows"]):
        raise ValueError("Còn UNKNOWN ở điểm khác cần đối soát riêng")
    deleted, complete = {}, {}
    for path in sorted((directory / "slots").glob("*.json")):
        document = load(path)
        if (document["signature"] != digest(run) or document["run_uuid"] != book.uuid
                or book.path(document["slot"]) != path or len(document["attempts"]) != 1):
            raise ValueError("Checkpoint không khớp identity hoặc namespace")
        name = path.relative_to(directory).as_posix()
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        if point_id(document["slot"]) in targets:
            deleted[name] = sha
        elif document["attempts"][0]["status"] == "complete":
            book.execute(document["slot"], document["inputs"], None)
            complete[name] = sha
    if set(deleted) & protected:
        raise ValueError("Reset chạm checkpoint thuộc prefix nghiệm thu cha")
    retired = {row["id"]: digest(row) for row in state["rows"] if point_id(row["slot"]) in targets}
    backup_files = {**deleted, **{f"http/{request_id}.json": hashlib.sha256((directory / "http" / (request_id + ".json")).read_bytes()).hexdigest()
                                  for request_id in retired}}
    backup_files["identity.json"] = hashlib.sha256((directory / "identity.json").read_bytes()).hexdigest()
    prefix = {"identity": binding(root, (directory / "identity.json").relative_to(root).as_posix()),
              "wire_identity_sha256": digest(state["identity"]), "carry_sha256": digest(state["carry"]),
              "http": load(directory / "wire.json")["rows"], "complete_slots": complete}
    return {"targets": list(targets), "generations": {target: 1 for target in targets}, "deleted_slots": deleted,
            "retired_http": retired, "backup_files": backup_files, "prefix": prefix}


def validate_backup(root: Path, plan: dict[str, Any], expected: dict[str, Any]) -> None:
    """Mọi byte cần phục hồi phải có trong ZIP trước khi xóa checkpoint active."""
    if binding(root, BACKUP) != expected:
        raise ValueError("Gói sao lưu khác checksum đã khóa")
    with zipfile.ZipFile(root / BACKUP) as archive:
        if len(archive.namelist()) != len(plan["backup_files"]) or set(archive.namelist()) != set(plan["backup_files"]):
            raise ValueError("Gói sao lưu thiếu hoặc thừa thành viên")
        for name, sha in plan["backup_files"].items():
            if hashlib.sha256(archive.read(name)).hexdigest() != sha:
                raise ValueError("Thành viên sao lưu không đúng byte gốc")


def write_backup(root: Path, plan: dict[str, Any]) -> dict[str, Any]:
    """Tạo ZIP nguyên byte trong bộ nhớ, ghi xong mới cho phép purge."""
    target = root / BACKUP
    if target.exists():
        expected = binding(root, BACKUP)
        validate_backup(root, plan, expected)
        return expected
    directory = root / NAMESPACES["RESEARCH"]
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, sha in plan["backup_files"].items():
            raw = safe_path(directory, name).read_bytes()
            if hashlib.sha256(raw).hexdigest() != sha:
                raise ValueError("Checkpoint đổi trong lúc sao lưu")
            archive.writestr(name, raw)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".zip.tmp")
    temporary.write_bytes(buffer.getvalue())
    os.replace(temporary, target)
    expected = binding(root, BACKUP)
    validate_backup(root, plan, expected)
    return expected


def purge(root: Path, plan: dict[str, Any], backup: dict[str, Any]) -> None:
    """Xóa đúng file slot đã sao lưu, idempotent khi bị ngắt giữa các lần unlink."""
    validate_backup(root, plan, backup)
    directory = root / NAMESPACES["RESEARCH"]
    paths = []
    for name, sha in plan["deleted_slots"].items():
        path = safe_path(directory, name)
        if path.parent != (directory / "slots").resolve():
            raise ValueError("Đường dẫn purge ngoài thư mục slots")
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
                raise ValueError("Checkpoint đã chạy lại hoặc bị sửa, không lặp reset")
            paths.append(path)
    for path in paths:
        path.unlink()


def build_runtime(root: Path, parent: dict[str, Any], plan: dict[str, Any], backup: dict[str, Any]) -> dict[str, Any]:
    """Amendment reset giữ cohort và raw, chỉ nghỉ các execution của hai điểm được yêu cầu."""
    pins = sources(root)
    checks = load(root / CHECKS)
    if (checks["status"] != "PASS" or checks["sources"] != pins or checks["failures"] or checks["errors"]
            or checks["skips"] or checks["tests"] != len(set(checks["test_ids"])) or not checks["compiled"]):
        raise ValueError("Scoped checks point restart chưa PASS")
    return {"version": "unified_point_restart_runtime_v1", "policy": POLICY,
            "parent_provider_runtime_sha256": digest(parent),
            "parent_provider_grant_sha256": digest(anchored(root, provider_runtime.GRANT)),
            "sources": pins, "checks": binding(root, CHECKS), "plan": plan, "backup": backup,
            "first_restart_http_sequence": len(plan["prefix"]["http"]),
            "first_model_scoped_http_sequence": parent["first_model_scoped_http_sequence"],
            "first_provider_scoped_http_sequence": parent["first_provider_scoped_http_sequence"],
            "authorization": AUTHORIZATION, "manual_launch_only": True,
            "provider_evidence": "USER_REPORTED_MATCHING_HTTP200_LOCAL_RESPONSES_MISSING",
            "scope": "USER_REQUESTED_POINT_REPLACEMENT_RETAIN_ALL_HTTP_AND_UNAFFECTED_POINTS"}


def grant_for(runtime: dict[str, Any], cap: int) -> dict[str, Any]:
    """Quyền mới ràng buộc danh sách reset và giới hạn phase hiện có."""
    return {"version": "unified_point_restart_release_v1", "status": "POINT_RESTART_RELEASED",
            "runtime_sha256": digest(runtime), "policy": POLICY, "authorization": AUTHORIZATION,
            "manual_launch_only": True, "api": True, "paid_api_allowed": False, "spend_limit_usd": 0,
            "namespace": NAMESPACES["RESEARCH"], "max_http_attempts": cap}


def prepare(root: Path) -> dict[str, Any]:
    """Khóa hai run lock, sao lưu và xóa checkpoint lỗi bằng quyền người dùng đã cấp."""
    from scripts.unified_live.run import create
    parent, parent_grant, provider = provider_runtime.require(root)
    directory = root / NAMESPACES["RESEARCH"]
    run = run_identity(root, "RESEARCH", parent)
    with PriorRunLock(directory / "manager", digest(run)), PriorRunLock(directory, digest(run)):
        if (root / RUNTIME).exists():
            runtime = load(root / RUNTIME)
            if load(directory / "wire.json")["rows"] != runtime["plan"]["prefix"]["http"]:
                raise ValueError("Đã có HTTP mới sau reset, không lặp prepare")
            if runtime != build_runtime(root, provider, runtime["plan"], runtime["backup"]):
                raise ValueError("Source reset đã đổi")
        else:
            protected = set(provider["prefix"]["complete_slots"]) | set(anchored(root, model_runtime.RUNTIME)["prefix"]["complete_slots"])
            plan = plan_reset(root, run, TARGETS, protected)
            backup = write_backup(root, plan)
            runtime = build_runtime(root, provider, plan, backup)
            create(root / RUNTIME, runtime)
        create(root / GRANT, grant_for(runtime, parent_grant["max_http_attempts"]))
        purge(root, runtime["plan"], runtime["backup"])
        counts = {"shared_complete": 0, "forecast_complete": 0, "labels_complete": 0}
        for path in (directory / "slots").glob("*.json"):
            document = load(path)
            if document["attempts"][0]["status"] == "complete":
                for key, start in (("shared_complete", "shared/"), ("forecast_complete", "forecast/"), ("labels_complete", "outcome/")):
                    counts[key] += int(document["slot"].startswith(start))
        status = load(directory / "status.json")
        status.update(counts, status="STOPPED_BY_OPERATOR", quota_policy=POLICY, blocked={}, waiting={}, waiting_models={},
                      point_generations=runtime["plan"]["generations"], updated_at=utc_now())
        for name in ("next_resume_at", "heartbeat_at"):
            status.pop(name, None)
        save(directory / "status.json", status)
    for name in (RUNTIME, GRANT):
        path = root / name
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    return {"status": "PREPARED_MANUAL_POINT_RESTART", "targets": list(TARGETS),
            "deleted_slots": len(runtime["plan"]["deleted_slots"]), "retired_http": len(runtime["plan"]["retired_http"])}


def require(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Đối soát mọi nguồn cha, prefix và backup trước khi khởi tạo credential/client."""
    parent, parent_grant, provider = provider_runtime.require(root)
    runtime, grant = anchored(root, RUNTIME), anchored(root, GRANT)
    anchored(root, CHECKS)
    if runtime != build_runtime(root, provider, runtime["plan"], runtime["backup"]):
        raise ValueError("Nguồn hoặc danh sách reset đã đổi")
    if grant != grant_for(runtime, parent_grant["max_http_attempts"]):
        raise ValueError("Grant point restart sai phạm vi manual/Free")
    validate_backup(root, runtime["plan"], runtime["backup"])
    state = check_prefix(root / NAMESPACES["RESEARCH"], runtime["plan"]["prefix"])
    for row in state["rows"]:
        if row["id"] in runtime["plan"]["retired_http"] and digest(row) != runtime["plan"]["retired_http"][row["id"]]:
            raise ValueError("Raw HTTP đã nghỉ bị đổi")
    return parent, parent_grant, runtime


def verify_admissions(state: dict[str, Any], runtime: dict[str, Any], cap: int) -> None:
    """Giữ kiểm admission lịch sử, các attempt mới tính cả chi phí generation đã nghỉ."""
    first = runtime["first_restart_http_sequence"]
    provider_runtime.verify_admissions({**state, "rows": state["rows"][:first]},
        runtime["first_model_scoped_http_sequence"], runtime["first_provider_scoped_http_sequence"], cap)
    retired = runtime["plan"]["retired_http"]
    for index in range(first, len(state["rows"])):
        row = state["rows"][index]
        if index >= cap or row.get("point_generation") != runtime["plan"]["generations"].get(point_id(row["slot"]), 0):
            raise ValueError("Trần phase hoặc generation HTTP không hợp lệ")
        visible = [r for r in state["rows"][:index] if not (r["status"] == "UNKNOWN" and r["id"] in retired)]
        try:
            admit({"carry": state["carry"], "rows": visible}, row["org"], row_model(row), row["reserved_tokens"], row["started_at"], cap)
        except Deferred:
            raise ValueError("HTTP generation mới vi phạm cooldown provider") from None


def audit(root: Path, *, seal: bool = False) -> dict[str, Any]:
    """Cold verify dataset active, ledger đầy đủ và gói các execution đã nghỉ."""
    from core.unified_execution_providers import cold_methods
    parent, grant, runtime = require(root)
    directory = root / NAMESPACES["RESEARCH"]
    run = run_identity(root, "RESEARCH", parent)
    with PriorRunLock(directory, digest(run)):
        state = check_prefix(directory, runtime["plan"]["prefix"])
        verify_admissions(state, runtime, grant["max_http_attempts"])
        result = verify(directory, run, cold_methods(root, parent["config"]), require_complete=seal,
                        retired=runtime["plan"]["retired_http"])
        book = StageBook(directory, run, verify_only=True)
        for point in run["points"]:
            if book.complete("outcome/" + point["id"]):
                if load(book.path("outcome/" + point["id"]))["attempts"][0]["output"] != canonical_outcome(root, point):
                    raise ValueError("Canonical label không tái lập")
        result.update(quota_policy=POLICY, quota_runtime_sha256=digest(runtime),
                      point_generations=runtime["plan"]["generations"], reset_backup_sha256=runtime["backup"]["sha256"])
        ready = []
        visible = [r for r in state["rows"] if not (r["status"] == "UNKNOWN" and r["id"] in runtime["plan"]["retired_http"])]
        for org in range(1, 6):
            for model in MODEL_LIMITS:
                try:
                    if len(state["rows"]) >= grant["max_http_attempts"]:
                        raise Exhausted("Hết trần phase")
                    admit({"carry": state["carry"], "rows": visible}, org, model, 8000, time.time(), grant["max_http_attempts"])
                    admission = "READY"
                except Deferred as error:
                    admission = {"resume_at": error.until}
                ready.append({"org": org, "model": model, "reserve": 8000, "admission": admission})
        if seal:
            slots = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((directory / "slots").glob("*.json"))}
            result.update(active_slots_sha256=digest(slots), wire_sha256=hashlib.sha256((directory / "wire.json").read_bytes()).hexdigest())
            for name in ("receipt.json", "quota_receipt.json"):
                path = directory / name
                if path.exists() and load(path) != result:
                    raise ValueError("Receipt đã seal khác dataset active")
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
        provider_quota = anchored(root, provider_runtime.RUNTIME)
        pins = {**parent_quota["sources"], **provider_quota["sources"], **runtime["sources"],
                **{name: binding(root, name) for name in (RUNTIME, CHECKS, BACKUP, model_runtime.RUNTIME, model_runtime.CHECKS, model_runtime.GRANT, provider_runtime.RUNTIME, provider_runtime.CHECKS, provider_runtime.GRANT)}}
        def guard() -> None:
            """Kiểm cả grant gốc và amendment trước mọi intent/dispatch."""
            parent_guard()
            if anchored(root, GRANT) != expected_grant or any(binding(root, name) != value for name, value in pins.items()):
                raise ValueError("Nguồn/grant amendment quota đã đổi")
        sender = LiveHTTP(root, "RESEARCH", guard)
        attach_diagnostics(sender, directory)
        try:
            calls = RestartCalls(directory, run, sender, carry_smoke(root, history(root)), guard=guard,
                                 retired=runtime["plan"]["retired_http"], generations=runtime["plan"]["generations"])
            providers = StudyProviders(root, calls)
            runner = RestartRunner(directory, run, calls, providers)
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
        command = [sys.executable, "-I", "-X", "utf8", "scripts/unified_point_restart/run.py", "verify", "--seal"]
        verified = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8")
        (directory / "point_restart_cold_verify.log").write_text(verified.stdout + verified.stderr, encoding="utf-8")
        if verified.returncode:
            result.update(status="COLD_VERIFY_FAILED", updated_at=utc_now())
            save(directory / "status.json", result)
            raise ValueError("Cold verify quota chưa PASS, journal đã giữ đủ")
        result = load(directory / "quota_receipt.json")
        save(directory / "status.json", {**result, "updated_at": utc_now()})
        return result
