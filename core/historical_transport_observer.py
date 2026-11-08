"""Quan sát lỗi H07; phục hồi reset theo opt-in, giữ body và identity khoa học."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess
import sys
import traceback
from time import sleep
from typing import Any, Iterator
from unittest.mock import patch
from uuid import UUID

import httpx

FILES = ("core/historical_transport_observer.py", "scripts/run_historical_evaluation_observed.py")
RECOVERY_POLICY = {"version": "historical_connection_reset_v1", "max_http_per_slot": 3,
                   "timeouts": {"connect": 30., "read": 120., "write": 60., "pool": 30.},
                   "max_keepalive_connections": 0, "backoff_seconds": [5., 10.]}
ACTIVE_SLOT: ContextVar[Any] = ContextVar("historical_connection_reset_slot", default=None)


def source_bindings(root: Path) -> dict[str, dict[str, Any]]:
    """Observer phải neo Git riêng, không sửa manifest runtime khoa học đã khóa."""
    result = {}
    for name in FILES:
        raw = (root / name).read_bytes()
        if raw != subprocess.check_output(["git", "show", "HEAD:" + name], cwd=root):
            raise ValueError("Observer chưa neo Git: " + name)
        result[name] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return result


def exception_chain(error: BaseException) -> list[dict[str, Any]]:
    """Chỉ lấy loại/mã hệ thống, không lưu message/args có thể chứa key hoặc payload."""
    result, seen = [], set()
    current: BaseException | None = error
    while current is not None and id(current) not in seen and len(result) < 10:
        seen.add(id(current))
        item: dict[str, Any] = {"class": type(current).__module__ + "." + type(current).__name__}
        for field in ("errno", "winerror", "verify_code"):
            value = getattr(current, field, None)
            if type(value) is int:
                item[field] = value
        for field in ("reason", "library"):
            value = getattr(current, field, None)
            if type(value) is str and value.replace("_", "").isalnum():
                item[field] = value
        result.append(item)
        current = current.__cause__ or current.__context__
    return result


def record_error(transport: Any, request: httpx.Request, error: BaseException,
                 sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Ghi chẩn đoán riêng và stderr; không sửa ledger hoặc tự authorize unknown."""
    from core.historical_evaluation_journal import save
    book = transport.clients.book
    row = transport.pacer.state["requests"][-1]
    identifier = str(UUID(row["id"]))
    timeout = request.extensions.get("timeout") or {}
    record = {"version": "historical_transport_diagnostic_v1", "scope": "TRANSPORT_DIAGNOSTIC_NO_BODY_CHANGE",
              "run_uuid": book.uuid, "run_signature": book.signature, "sources": sources,
              "request_record_id": identifier, "checkpoint_attempt_id": row.get("checkpoint_attempt_id"),
              "point_id": row.get("point_id"), "role": row.get("role"),
              "provider_outcome": "UNKNOWN", "exception_chain": exception_chain(error),
              "request_bytes": len(request.content),
              "timeouts": {k: v for k, v in timeout.items() if k in ("connect", "read", "write", "pool")
                           and (v is None or type(v) in (int, float))},
              "frames": [{"file": Path(f.filename).name, "function": f.name, "line": int(f.lineno)}
                         for f in traceback.extract_tb(error.__traceback__)[-8:]]}
    path = book.directory / "diagnostics" / (identifier + ".json")
    save(path, record)
    names = " → ".join(item["class"] for item in record["exception_chain"])
    print(f"Lỗi gốc transport: {names}; ledger={identifier}; chẩn đoán={path}", file=sys.stderr, flush=True)
    return record


def recover_reset(book: Any, slot: str, inputs: dict[str, Any], error: BaseException,
                  recent: dict[str, tuple[Any, dict[str, Any]]]) -> bool:
    """Chỉ reconcile reset vừa chứng kiến trong tiến trình này, giữ reserve và trần3/slot."""
    from core.bayesian_memory import read_json
    from core.historical_evaluation_journal import load
    from core.historical_evaluation_protocol import digest
    identifier = getattr(error, "request_record_id", None)
    observation = recent.pop(identifier, None)
    if observation is None or observation[0] is not book or book.verify_only:
        return False
    record = observation[1]
    chain = record["exception_chain"]
    if (not chain or chain[0]["class"] != "httpx.ReadError" or not any(
            item["class"] == "builtins.ConnectionResetError" and
            (item.get("winerror") == 10054 or item.get("errno") == 10054) for item in chain)):
        return False
    doc = load(book.path(slot))
    last = doc["attempts"][-1]
    if (doc["run_uuid"] != book.uuid or doc["signature"] != book.signature or doc["slot"] != slot
            or doc["inputs"] != inputs or doc["inputs_sha256"] != digest(inputs)
            or last["status"] != "unknown" or last.get("authorization") is not None
            or record["checkpoint_attempt_id"] != last["attempt_id"]
            or record["run_uuid"] != book.uuid or record["run_signature"] != book.signature):
        return False
    attempts = {a["attempt_id"] for a in doc["attempts"]}
    rows = [row for path in (book.directory / "usage").glob("org*.json")
            for row in read_json(path)["requests"] if row.get("checkpoint_attempt_id") in attempts]
    current = [row for row in rows if row["id"] == identifier]
    if (len(current) != 1 or current[0]["status"] != "transport_error" or current[0].get("historical_raw")
            or any(row.get("run_signature") != book.signature or row["status"] == 200 for row in rows)
            or len(rows) >= RECOVERY_POLICY["max_http_per_slot"]):
        return False
    delay = RECOVERY_POLICY["backoff_seconds"][len(rows) - 1]
    book.reconcile(last["attempt_id"], "OPERATOR_OPT_IN historical_connection_reset_v1: WinError10054 vừa ghi nhận; "
                   f"giữ outcome UNKNOWN/reserve, cùng inputs/org/key/model; HTTP tiếp theo {len(rows) + 1}/3.")
    print(f"Phục hồi WinError10054: chờ {delay:g}s, HTTP tiếp theo {len(rows) + 1}/3; "
          "giữ checkpoint và quota reserve.", file=sys.stderr, flush=True)
    sleep(delay)
    return True


@contextmanager
def observe_transport(root: Path, *, recover_connection_reset: bool = False) -> Iterator[None]:
    """Quan sát mặc định; phục hồi reset chỉ khi operator bật policy hữu hạn riêng."""
    from core.historical_evaluation_clients import RawHTTP
    from core.historical_evaluation_journal import RunBook
    from core.groq_pacing import PilotStop, PacedGroqTransport
    sources = source_bindings(root)
    original = RawHTTP.handle_request
    original_init, original_execute = RawHTTP.__init__, RunBook.execute
    original_once = PacedGroqTransport._handle_once
    recent: dict[str, tuple[Any, dict[str, Any]]] = {}

    def initialize(transport: Any, clients: Any, pacer: Any, inner: Any = None) -> None:
        """Mỗi HTTP dùng TCP mới; tắt retry ngầm ở httpx như client gốc."""
        if inner is None:
            inner = httpx.HTTPTransport(retries=0, limits=httpx.Limits(max_keepalive_connections=0))
        original_init(transport, clients, pacer, inner)

    def execute(book: Any, slot: str, inputs: dict[str, Any], function: Any, *, validate: Any = None) -> dict[str, Any]:
        """Dùng lại journal gốc, chỉ retry reset mới có bằng chứng và authorization ghi durable."""
        while True:
            try:
                token = ACTIVE_SLOT.set((book, slot))
                try:
                    return original_execute(book, slot, inputs, function, validate=validate)
                finally:
                    ACTIVE_SLOT.reset(token)
            except PilotStop as error:
                if not recover_reset(book, slot, inputs, error, recent):
                    raise

    def limited_once(transport: Any, request: httpx.Request) -> httpx.Response:
        """Chặn trước reserve thứ4, kể cả khi 429 và reset dùng invocation khác nhau."""
        from core.historical_evaluation_journal import load
        active = ACTIVE_SLOT.get()
        if active is None:
            raise PilotStop("Policy phục hồi cần journal slot đang chạy")
        book, slot = active
        doc = load(book.path(slot))
        attempts = {a["attempt_id"] for a in doc["attempts"]}
        count = sum(row.get("checkpoint_attempt_id") in attempts for row in transport.pacer.state["requests"])
        if count >= RECOVERY_POLICY["max_http_per_slot"]:
            raise PilotStop("Hết trần3 HTTP/slot gồm retry429, reset và attempt cũ; giữ checkpoint")
        return original_once(transport, request)

    def observed(transport: Any, request: httpx.Request) -> httpx.Response:
        """Lỗi ghi log cũng không được che exception transport ban đầu."""
        if recover_connection_reset:
            request.extensions["timeout"] = deepcopy(RECOVERY_POLICY["timeouts"])
            row = transport.pacer.state["requests"][-1]
            row["historical_transport_policy"] = {**deepcopy(RECOVERY_POLICY), "sources": sources}
            transport.pacer.save()
        try:
            return original(transport, request)
        except (httpx.HTTPError, OSError) as error:
            try:
                record = record_error(transport, request, error, sources)
                if recover_connection_reset:
                    recent[record["request_record_id"]] = (transport.clients.book, record)
            except Exception:
                names = " → ".join(item["class"] for item in exception_chain(error))
                print(f"Lỗi gốc transport: {names}; không ghi được file chẩn đoán.", file=sys.stderr, flush=True)
            raise

    with patch.object(RawHTTP, "handle_request", observed):
        if recover_connection_reset:
            with patch.object(RawHTTP, "__init__", initialize), patch.object(RunBook, "execute", execute), \
                    patch.object(PacedGroqTransport, "_handle_once", limited_once):
                yield
        else:
            yield
