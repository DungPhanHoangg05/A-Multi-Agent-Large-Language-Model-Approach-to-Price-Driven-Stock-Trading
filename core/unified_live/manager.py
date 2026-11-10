"""Điều phối U08 thực, chờ quota có heartbeat và cold seal trước khi công bố thu đủ."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock, utc_now, process_start
from core.unified_contracts import digest, json_bytes
from core.unified_execution import StageBook
from core.unified_live.execution import HostedRunner, verify
from core.unified_live.release import (RUNTIME, PREFLIGHT, CHECKS, NAMESPACES, GRANTS, anchored, require_release,
                                       validate_runtime, identity, history)
from core.unified_live.transport import LiveHTTP, LiveCalls, carry_smoke


def guard_for(root: Path, phase: str, runtime: dict, grant: dict) -> Any:
    """Kiểm grant và source trước mỗi dispatch; không băm lại weights lớn nếu stat giữ nguyên."""
    from core.unified_protocol import safe
    with __import__("zipfile").ZipFile(root / "docs/plan/week12/unified_execution_checks.zip") as archive:
        sources = {**json.loads(archive.read("source_bindings.json")), **runtime["sources"]}
    from core.unified_protocol import binding
    sources.update({name: binding(root, name) for name in (RUNTIME, PREFLIGHT, CHECKS)})
    stats = {name: (safe(root, name).stat().st_mtime_ns, safe(root, name).stat().st_size) for name in sources}
    def guard() -> None:
        """Grant bị sửa/thu hồi hoặc code/input đổi thì dừng trước HTTP, không tự sửa manifest."""
        if anchored(root, GRANTS[phase]) != grant:
            raise ValueError("Release đã đổi; dừng U08")
        for name, expected in sources.items():
            path = safe(root, name)
            stat = path.stat()
            value = (stat.st_mtime_ns, stat.st_size)
            if value != stats[name]:
                if hashlib.sha256(path.read_bytes()).hexdigest() != expected["sha256"]:
                    raise ValueError("Nguồn đang chạy đã đổi: " + name)
                stats[name] = value
    return guard


def canonical_outcome(root: Path, point: dict) -> dict:
    """Chỉ callback sau barrier gọi; đổi nghìn VND đúng một lần và dùng oracle chung."""
    import pandas as pd
    from core.unified_experiment import outcome_from_frame
    from core.unified_protocol import ordered_branches
    directory = root / NAMESPACES["RESEARCH"]
    if not (directory / "identity.json").exists():
        raise ValueError("Query payoff bị khóa trước run/forecast durable")
    run = load(directory / "identity.json")["identity"]
    if run["phase"] != "RESEARCH" or run["repeats"] != 3 or point not in run["points"]:
        raise ValueError("Query payoff ngoài planned research")
    book = StageBook(directory, run, verify_only=True)
    if not all(book.complete(f"forecast/{point['id']}/u0/r{r}/{v}") for r in range(3) for v in ordered_branches(r)):
        raise ValueError("Query payoff vẫn khóa trước đủ24 forecast durable")
    path = root / "outputs/unified_integration/u06_assets_v2/prices" / (point["symbol"] + ".json")
    frame = pd.DataFrame(json.loads(path.read_bytes()))
    frame["Datetime"] = pd.to_datetime(frame["Datetime"])
    columns = ["Open", "High", "Low", "Close"]
    frame[columns] = frame[columns].astype(float) * 1000.
    return outcome_from_frame(point, frame, hashlib.sha256(path.read_bytes()).hexdigest())


def run_identity(root: Path, phase: str, runtime: dict) -> dict:
    """Tách epoch trước khi tạo book hoặc client; không đọc credential."""
    return identity(runtime, phase, digest(anchored(root, PREFLIGHT)))


def status(root: Path, phase: str) -> dict:
    """Chỉ đọc tiến độ, không nạp SDK, model hoặc API key."""
    directory = root / NAMESPACES[phase]
    path = directory / "status.json"
    value = load(path) if path.exists() else {"phase": phase, "status": "NOT_STARTED", "api": False}
    if value.get("pid"):
        value["worker_alive"] = process_start(value["pid"]) == value.get("process_start")
    return value


def verify_phase(root: Path, phase: str, *, seal: bool = False) -> dict:
    """Cold replay không client; nhãn phải khớp lại giá canonical đã pin."""
    from core.unified_execution_providers import cold_methods
    runtime = validate_runtime(root)
    directory = root / NAMESPACES[phase]
    expected = run_identity(root, phase, runtime)
    stored = load(directory / "identity.json")["identity"]
    if expected != stored:
        raise ValueError("Run khác runtime/cohort/epoch")
    methods = cold_methods(root, runtime["config"])
    result = verify(directory, stored, methods)
    book = StageBook(directory, stored, verify_only=True)
    if phase == "RESEARCH":
        for point in runtime["points"]:
            value = load(book.path("outcome/" + point["id"]))["attempts"][0]["output"]
            if value != canonical_outcome(root, point):
                raise ValueError("Outcome không tái lập từ giá canonical")
    bindings = {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for folder in ("slots", "http") for p in sorted((directory / folder).glob("*.json"))}
    result.update(identity_sha256=digest(stored), evidence_sha256=digest(bindings),
                  wire_sha256=hashlib.sha256((directory / "wire.json").read_bytes()).hexdigest(),
                  spend_limit_usd=0, paid_api_allowed=False, economic_price_unit="VND")
    path = directory / "receipt.json"
    if path.exists() and load(path) != result:
        raise ValueError("Receipt đã seal khác journal hiện hành")
    if seal:
        save(path, result)
    return result


def collect(root: Path, phase: str) -> dict:
    """Giữ một owner qua mọi lần chờ; không tạo worker thứ hai hoặc bỏ UNKNOWN."""
    from core.unified_execution_providers import StudyProviders
    runtime, grant = require_release(root, phase)
    directory = root / NAMESPACES[phase]
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ".gitignore").write_text("*\n", encoding="utf-8")
    run = run_identity(root, phase, runtime)
    with PriorRunLock(directory / "manager", digest(run)):
        if (directory / "receipt.json").exists():
            return verify_phase(root, phase)
        initial = history(root)
        if phase == "RESEARCH":
            initial = carry_smoke(root, initial)
        guard = guard_for(root, phase, runtime, grant)
        sender = LiveHTTP(root, phase, guard)
        try:
            calls = LiveCalls(directory, run, sender, initial, guard=guard)
            providers = StudyProviders(root, calls)
            runner = HostedRunner(directory, run, calls, providers)
            while True:
                if (directory / "stop.request").exists():
                    result = {"status": "STOPPED_BY_OPERATOR", "phase": phase, "updated_at": utc_now()}
                    save(directory / "status.json", result)
                    return result
                result = runner.tick(providers, lambda point: canonical_outcome(root, point))
                counts = {"shared_complete": 0, "forecast_complete": 0, "labels_complete": 0}
                for path in (directory / "slots").glob("*.json"):
                    doc = load(path)
                    if doc["attempts"][0]["status"] == "complete":
                        for key, prefix in (("shared_complete", "shared/"), ("forecast_complete", "forecast/"), ("labels_complete", "outcome/")):
                            counts[key] += int(doc["slot"].startswith(prefix))
                result.update(counts, http_attempts=len(calls.state["rows"]), updated_at=utc_now(),
                              pid=__import__("os").getpid(), process_start=process_start(__import__("os").getpid()))
                save(directory / "status.json", result)
                print(json.dumps(result, ensure_ascii=False), flush=True)
                if result["status"] == "COMPLETE":
                    sender.close()
                    # Tiến trình mới không có key/client là cửa nghiệm thu cuối cho phase.
                    command = [sys.executable, "-I", "-X", "utf8", "scripts/unified_live/run.py", "verify", "--phase", phase, "--seal"]
                    verified = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8")
                    (directory / "cold_verify.log").write_text(verified.stdout + verified.stderr, encoding="utf-8")
                    if verified.returncode:
                        raise ValueError("Cold verify U08 chưa PASS; giữ raw và checkpoint")
                    result = load(directory / "receipt.json")
                    save(directory / "status.json", {**result, "updated_at": utc_now()})
                    return result
                if result["blocked"]:
                    result["status"] = "BLOCKED_RECONCILIATION_REQUIRED"
                    save(directory / "status.json", result)
                    return result
                if not result["waiting"]:
                    raise ValueError("Collector không có điểm tiếp theo hoặc lý do chờ")
                until = min(float(v) for v in result["waiting"].values())
                while time.time() < until and not (directory / "stop.request").exists():
                    result.update(next_resume_at=until, heartbeat_at=utc_now())
                    save(directory / "status.json", result)
                    time.sleep(min(30., max(.01, until - time.time())))
        except Exception as error:
            save(directory / "status.json", {"status": "STOPPED_ERROR", "phase": phase,
                "kind": type(error).__name__, "updated_at": utc_now(), "reason": str(error)[:1000]})
            raise
        finally:
            sender.close()
