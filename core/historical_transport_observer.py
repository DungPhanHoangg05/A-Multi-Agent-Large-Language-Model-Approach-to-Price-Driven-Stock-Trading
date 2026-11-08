"""Quan sát exception H07 trước wrapper cũ, không đổi wire/retry/run identity."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
from pathlib import Path
import subprocess
import sys
import traceback
from typing import Any, Iterator
from unittest.mock import patch
from uuid import UUID

import httpx

FILES = ("core/historical_transport_observer.py", "scripts/run_historical_evaluation_observed.py")


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
                 sources: dict[str, dict[str, Any]]) -> None:
    """Ghi chẩn đoán riêng và stderr; không sửa ledger hoặc tự authorize unknown."""
    from core.historical_evaluation_journal import save
    book = transport.clients.book
    row = transport.pacer.state["requests"][-1]
    identifier = str(UUID(row["id"]))
    timeout = request.extensions.get("timeout") or {}
    record = {"version": "historical_transport_diagnostic_v1", "scope": "OBSERVER_ONLY_NO_WIRE_RETRY_CHANGE",
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


@contextmanager
def observe_transport(root: Path) -> Iterator[None]:
    """Gọi nguyên hàm gốc một lần, trả nguyên response hoặc ném lại cùng exception."""
    from core.historical_evaluation_clients import RawHTTP
    sources = source_bindings(root)
    original = RawHTTP.handle_request

    def observed(transport: Any, request: httpx.Request) -> httpx.Response:
        """Lỗi ghi log cũng không được che exception transport ban đầu."""
        try:
            return original(transport, request)
        except (httpx.HTTPError, OSError) as error:
            try:
                record_error(transport, request, error, sources)
            except Exception:
                names = " → ".join(item["class"] for item in exception_chain(error))
                print(f"Lỗi gốc transport: {names}; không ghi được file chẩn đoán.", file=sys.stderr, flush=True)
            raise

    with patch.object(RawHTTP, "handle_request", observed):
        yield
