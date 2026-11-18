"""Lưu phản hồi HTTP của FIN11 trước khi cập nhật journal wire chính."""
from __future__ import annotations

from pathlib import Path
from typing import Callable
from uuid import UUID

from core.historical_evaluation_journal import load, save
from core.serving_runtime.transport import GroqHTTP, response_headers, response_record
from core.unified_contracts import digest, json_bytes


def capture_path(directory: Path, row: dict) -> Path:
    """Khóa đường dẫn bản lưu theo UUID HTTP, độc lập với slot và key."""
    identifier = str(UUID(row["id"]))
    if identifier != row["id"]:
        raise ValueError("UUID bản lưu HTTP không hợp lệ")
    return directory/"received"/(identifier+".json")


def capture_identity(row: dict) -> dict:
    """Định danh bản lưu gắn đúng intent và nội dung gửi."""
    return {"id": row["id"], "slot": row["slot"], "attempt": row["attempt"],
            "org_slot": row["org_slot"], "wire_sha256": digest(row["body"])}


class HostedHTTP(GroqHTTP):
    """Giữ HTTP status trước khi đọc body và giữ body trước khi đóng response."""

    def send_durable(self, directory: Path, row: dict, body: dict, clock: Callable[[], float]) -> tuple[int, bytes, dict]:
        path = capture_path(directory, row)
        with self.client.stream("POST", "https://api.groq.com/openai/v1/chat/completions", content=json_bytes(body)) as response:
            status, headers = response.status_code, response_headers(dict(response.headers))
            received = {"identity": capture_identity(row), "status": status, "headers": headers,
                        "at": clock(), "response": None}
            save(path, received)
            raw = response.read()
            save(path, {**received, "at": clock(), "response": raw.decode("utf-8", errors="replace")})
        return status, raw, headers


def recover_response(directory: Path, row: dict) -> dict | None:
    """Khôi phục body đã nhận; HTTP 200 thiếu body vẫn tính là một attempt."""
    path = capture_path(directory, row)
    if not path.is_file():
        return None
    received = load(path)
    if received["identity"] != capture_identity(row):
        raise ValueError("Bản lưu phản hồi HTTP khác intent")
    if received["response"] is not None:
        return response_record(row, received["status"], received["response"].encode("utf-8"), received["headers"], received["at"])
    if received["status"] == 200:
        return {**row, "status": "RESPONSE_LOST", "provider_http_status": 200, "headers": received["headers"],
                "completed_at": received["at"], "reconciliation_source": "DURABLE_HTTP_HEADERS"}
    return None
