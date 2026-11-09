"""Điều phối pilot bằng một lệnh: shared→collect→verify, tự kiểm và phục hồi checkpoint."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from contextlib import contextmanager
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Iterator

from core.free_pilot_assets import DIRECTORY, DOC, GRANT, INPUTS, PROTOCOL, RUNTIME, anchored
from core.free_pilot_recovery import POLICY, pending_action
from core.free_pilot_runtime import identity, verify_locked
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import binding, digest
from core.prior_run_lock import PriorRunLock, utc_now

CONFIG = DOC / "free_pilot_manager.json"
CODE = ("core/free_pilot_manager.py", "core/free_pilot_recovery.py", "scripts/run_free_pilot.py", "tests/test_free_pilot_manager.py")
RUN_LOCK = "free_pilot48_exclusive_v1"
START, END = "<!-- FREE_PILOT_MANAGER_START -->", "<!-- FREE_PILOT_MANAGER_END -->"


def launch_worker(command: list[str], root: Path, handle: Any) -> subprocess.Popen:
    """Khởi chạy worker nền không mở cửa sổ; tách biên này để test không mock lệnh OS lock."""
    return subprocess.Popen(command, cwd=root, stdout=handle, stderr=subprocess.STDOUT,
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


@contextmanager
def run_lock(root: Path, state: dict) -> Iterator[None]:
    """Nếu worker còn sống sau khi đóng terminal, chờ nó nhả lock, không tạo worker trùng."""
    while True:
        lock = PriorRunLock(root / DIRECTORY, RUN_LOCK)
        try:
            lock.__enter__()
            break
        except RuntimeError as error:
            if str(error) != "Run đang được tiến trình khác giữ khóa OS":
                raise
            write_status(root, state, "WAITING_EXISTING_WORKER", reason="Worker cũ còn giữ OS lock; không gửi trùng API")
            print("Worker cũ vẫn chạy; đang chờ checkpoint/OS lock.", flush=True)
            time.sleep(5.)
    try:
        yield
    finally:
        lock.__exit__(None, None, None)


def profile(root: Path) -> dict:
    """Receipt bổ sung cho supervisor, không đổi runtime/identity/checkpoint inference đã khóa."""
    book = load(root / DIRECTORY / "identity.json")
    return {"version": "free_pilot_manager_v3", "run_uuid": book["run_uuid"], "identity": identity(root),
            "policy": POLICY, "phases": ["shared", "collect", "verify"],
            "sources": {name: binding(root, name) for name in CODE},
            "grant": binding(root, GRANT), "campaign": binding(root, DIRECTORY / "campaign.json")}


def preflight(root: Path) -> dict:
    """Kiểm grant/source bổ sung và nguồn inference trước khi đọc key hoặc khởi chạy worker."""
    config = anchored(root, CONFIG)
    if config != profile(root):
        raise ValueError("Supervisor khác source/grant/UUID; không tự thay manifest")
    verify_locked(root)
    grant = anchored(root, GRANT)
    if grant["status"] != "PILOT_RELEASED" or grant.get("api") is not True or grant.get("paid_api_allowed") is not False:
        raise ValueError("Chưa có grant pilot Free sau cold smoke")
    return config


def snapshot(directory: Path) -> dict:
    """Hash chứng cứ; cold verify và phục hồi raw200 không được thay HTTP/quota."""
    return {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for folder in ("http", "usage") for p in (directory / folder).rglob("*") if p.is_file()}


def write_status(root: Path, state: dict, status: str, **fields: Any) -> None:
    """Tiến độ cập nhật tự động; không đánh dấu H08 hoặc toàn H07 DONE."""
    state.update(state=status, updated_at=utc_now(), **fields)
    counters = {"shared_complete": 0, "forecast_complete": 0, "labels_complete": 0}
    for path in (root / DIRECTORY / "slots").glob("*.json"):
        doc = load(path)
        if doc["attempts"][-1]["status"] == "complete":
            counters["shared_complete"] += int(doc["slot"].startswith("shared/") and not doc["slot"].startswith("shared/smoke_"))
            counters["forecast_complete"] += int(doc["slot"].startswith("pilot/"))
            counters["labels_complete"] += int(doc["slot"].startswith("label/"))
    state.update(counters)
    save(root / DIRECTORY / "manager/status.json", state)
    local = datetime.now(timezone(timedelta(hours=7))).strftime("%d/%m/%Y %H:%M:%S UTC+7")
    line = f"Trạng thái **{status}**, phase `{state.get('phase', '-')}`, cập nhật {local}."
    line += f" Shared {counters['shared_complete']}/48; forecast {counters['forecast_complete']}/336; nhãn {counters['labels_complete']}/48."
    if state.get("reason"):
        line += " " + str(state["reason"])
    if state.get("resume_at"):
        line += " Chờ đến " + datetime.fromtimestamp(state["resume_at"], timezone(timedelta(hours=7))).strftime("%H:%M:%S %d/%m/%Y UTC+7") + "."
    for relative in (DOC / "README.md", DOC / "historical_reevaluation_plan.md"):
        path = root / relative
        text = path.read_text(encoding="utf-8")
        if text.count(START) == 1 and text.count(END) == 1:
            before, rest = text.split(START)
            _, after = rest.split(END)
            text = before + START + "\n" + line + "\n" + END + after
            if status == "P05_COLD_PASS":
                if relative.name == "historical_reevaluation_plan.md":
                    text = text.replace("- [ ] P04 —", "- [x] P04 —").replace("- [ ] P05 —", "- [x] P05 —")
                else:
                    text = re.sub(r"^(\| H07 pilot P04 \|[^|]+\|)[^|]+\|", r"\1 [x] PASS:48 shared/336 forecast |", text, flags=re.M)
                    text = re.sub(r"^(\| H07 pilot P05 \|[^|]+\|)[^|]+\|", r"\1 [x] P05_COLD_PASS |", text, flags=re.M)
            path.write_text(text, encoding="utf-8")


def next_phase(book: RunBook, units: list[dict]) -> str:
    """Suy phase từ slot durable, không tin phase cũ hoặc UUID người dùng chép lại."""
    if not book.complete("shared_manifest") or not all(book.complete("shared/" + u["id"]) for u in units):
        return "shared"
    from core.historical_evaluation_protocol import PRIMARY
    if not all(book.complete("pilot/" + u["id"] + "/" + b) for u in units for b in (*PRIMARY, "Fact_Anchor")):
        return "collect"
    if not all(book.complete("label/" + u["id"]) for u in units):
        return "collect"
    return "verify"


def phase_result(path: Path, phase: str, book: RunBook, units: list[dict]) -> dict:
    """Exit0 chưa đủ; kiểm summary và slot/receipt của đúng48 điểm."""
    lines = path.read_text(encoding="utf-8").splitlines()
    result = json.loads(next(line for line in reversed(lines) if line.strip()))
    if result.get("run_uuid") != book.uuid:
        raise ValueError("Worker trả UUID khác run")
    if phase == "shared":
        if result.get("count") != 48 or set(result.get("shared", {})) != {u["id"] for u in units}:
            raise ValueError("Chưa đủ48 shared")
        if next_phase(book, units) == "shared":
            raise ValueError("Summary không khớp shared durable")
    else:
        expected = "P05_COLD_PASS" if phase == "verify" else "P05_PENDING"
        if (result.get("status") != expected or result.get("forecast_slots") != 336
                or result.get("planned_points") != 48 or next_phase(book, units) != "verify"):
            raise ValueError("Forecast/cold chưa đủ48×7 slot")
        if phase == "verify":
            receipt = load(book.directory / "pilot_collection_receipt.json")
            if receipt.get("status") != "P05_COLD_PASS" or receipt.get("run_uuid") != book.uuid:
                raise ValueError("Thiếu receipt cold pilot")
            for folder, key in (("slots", "slots"), ("usage", "usage")):
                for name, sha in receipt[key].items():
                    from core.prior_run_lock import safe_path
                    if hashlib.sha256(safe_path(book.directory, folder + "/" + name).read_bytes()).hexdigest() != sha:
                        raise ValueError("Receipt cold khác bằng chứng hiện tại")
    return result


def wait_until(root: Path, state: dict, timestamp: float, deadline: float) -> None:
    """Chờ theo clock, heartbeat ngắn; không reset deadline khi tắt/mở PowerShell."""
    if timestamp >= deadline:
        raise ValueError("PARTIAL_DEADLINE_48H: thời gian chờ vượt deadline đã khóa")
    while time.time() < timestamp:
        if time.time() >= deadline:
            raise ValueError("PARTIAL_DEADLINE_48H")
        time.sleep(min(5., max(.01, timestamp - time.time())))


def manage(root: Path) -> dict:
    """Chạy đến cold PASS; retry tạm thời liên tục có proof, giữ quota và không tạo CASH."""
    from dotenv import load_dotenv
    config = preflight(root)
    load_dotenv(root / ".env", override=False)
    keys = [os.environ.get(f"GROQ_ORG_{i}_API_KEY") for i in range(1, 6)]
    if not all(keys) or len(set(keys)) != 5:
        raise ValueError("Cần đủ5 credential độc lập trong .env/environment; không hiển thị key")
    directory = root / DIRECTORY
    manager = directory / "manager"
    book = RunBook(directory, identity(root))
    units = load(root / INPUTS)["units"]
    deadline = load(directory / "campaign.json")["deadline_epoch"]
    state_path = manager / "status.json"
    child = None
    # Token khóa OS giữ nguyên qua revision policy; source vẫn được preflight kiểm riêng.
    owner = manager / "run.owner.json"
    from core.bayesian_memory import read_json
    lock_signature = read_json(owner)["run_signature"] if owner.exists() else digest(config)
    with PriorRunLock(manager, lock_signature):
        state = load(state_path) if state_path.exists() else {"run_uuid": book.uuid, "launches": 0}
        if state["run_uuid"] != book.uuid:
            raise ValueError("Trạng thái supervisor khác UUID")
        state["supervisor"] = binding(root, CONFIG)
        no_http_retries = 0
        try:
            while True:
                preflight(root)
                with run_lock(root, state):
                    phase = next_phase(book, units)
                    action = pending_action(book)
                if phase != "verify" and time.time() >= deadline:
                    raise ValueError("PARTIAL_DEADLINE_48H: không tự gia hạn")
                if action is not None and action["kind"] == "RETRY":
                    no_http_retries = no_http_retries + 1 if action["http_count"] == 0 else 0
                    if no_http_retries > 3:
                        raise ValueError("Lỗi trước HTTP lặp lại; xem worker log, chạy lại cùng lệnh sau khi sửa nguyên nhân")
                    write_status(root, state, "WAITING", phase=phase, reason=action["reason"], resume_at=action["resume_at"])
                    print(f"Tự phục hồi {action['slot']}: {action['reason']}; đã ghi {action['http_count']} HTTP, tiếp tục theo quota/backoff.", flush=True)
                    wait_until(root, state, action["resume_at"], deadline)
                    with run_lock(root, state):
                        fresh = pending_action(book)
                        if fresh is None or fresh["attempt_id"] != action["attempt_id"]:
                            continue
                        if fresh["kind"] == "RETRY":
                            book.reconcile(fresh["attempt_id"], "USER_AUTHORIZED_SINGLE_COMMAND: " + json.dumps(action, ensure_ascii=False))
                elif action is not None and action["kind"] == "REPLAY":
                    print("Phục hồi raw HTTP200 tại " + action["slot"] + "; không gọi lại API.", flush=True)
                state["launches"] += 1
                log = manager / f"worker_{state['launches']:04d}_{phase}.log"
                before = snapshot(directory) if phase == "verify" else None
                write_status(root, state, "RUNNING", phase=phase, reason="", resume_at=None, log=log.relative_to(root).as_posix())
                print(f"Đang chạy {phase}; log: {log}", flush=True)
                command = [sys.executable, "-X", "utf8", str(root / "scripts/run_free_pilot.py"), "--worker", phase]
                with log.open("w", encoding="utf-8") as handle:
                    child = launch_worker(command, root, handle)
                    heartbeat = time.monotonic()
                    while child.poll() is None:
                        time.sleep(1.)
                        if time.monotonic() - heartbeat >= 30:
                            write_status(root, state, "RUNNING", phase=phase)
                            print(f"Đang chạy {phase}; checkpoint vẫn được giữ, có thể đang chờ quota.", flush=True)
                            heartbeat = time.monotonic()
                    code = child.returncode
                child = None
                if code == 0:
                    with run_lock(root, state):
                        result = phase_result(log, phase, book, units)
                    if before is not None and snapshot(directory) != before:
                        raise ValueError("Cold verify đã đổi HTTP/quota")
                    if phase == "verify":
                        save(manager / "collection_receipt.json", {"status": "P05_COLD_PASS", "run_uuid": book.uuid,
                             "supervisor": binding(root, CONFIG), "recovery_policy": POLICY,
                             "cold_receipt": binding(root, DIRECTORY / "pilot_collection_receipt.json"),
                             "http_usage_sha256": digest(snapshot(directory)), "H08": "PENDING"})
                        write_status(root, state, "P05_COLD_PASS", phase=phase, reason="H08 còn chờ phân tích", resume_at=None)
                        print("P05_COLD_PASS — hoàn tất thu/cold pilot48; H08 còn chờ.", flush=True)
                        return result
                    continue
                if phase == "verify":
                    raise ValueError("Cold verify thất bại; giữ bằng chứng, xem worker log")
                with run_lock(root, state):
                    failed = pending_action(book)
                if failed is not None and failed["kind"] == "REPLAY":
                    raise ValueError("Raw HTTP200 chưa thể tái lập output hợp lệ; giữ raw, xem worker log")
                if failed is None:
                    raise ValueError("Worker dừng ngoài slot; xem worker log và chạy lại cùng lệnh sau khi sửa nguyên nhân")
        except BaseException as error:
            if child is not None and child.poll() is None:
                child.terminate()
                child.wait()
            write_status(root, state, "STOPPED", reason=str(error), resume_at=None)
            print("Đã giữ checkpoint/quota. Lần sau chạy lại chính lệnh này; chi tiết: " + str(error), file=sys.stderr, flush=True)
            raise
