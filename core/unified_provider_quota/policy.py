"""Cho gửi ngay khi không có lỗi provider đang yêu cầu cooldown."""
from __future__ import annotations

import math
from typing import Any

from core.groq_pacing import MODEL_LIMITS
from core.unified_execution_transport import Deferred, Exhausted, Uncertain, cooldown
from core.unified_model_quota.policy import MODEL, ModelCalls, row_model

POLICY = "provider_response_v1"
TRANSIENT = frozenset((429, 500, 502, 503, 504))


def admit(state: dict[str, Any], org: int, model: str, tokens: int, now: float,
          attempt_cap: int) -> None:
    """Chỉ gate theo lỗi thực của đúng org/model, kiểm budget request và trần attempt."""
    if (type(org) is not int or org not in range(1, 6) or model not in MODEL_LIMITS
            or type(tokens) is not int or not 0 < tokens <= MODEL_LIMITS[model]["tpm"]):
        raise ValueError("Org/model hoặc budget request ngoài serving đã khóa")
    if len(state["rows"]) >= attempt_cap:
        raise Exhausted("Hết trần HTTP của phase U08")
    current = [row for row in state["rows"] if row["org"] == org and row_model(row) == model]
    if any(row["status"] == "UNKNOWN" for row in current):
        raise Uncertain("UNKNOWN của org/model cần đối soát trước HTTP mới")
    bucket = [row for row in state["carry"] if row["org"] == org and row_model(row) == model] + current
    if not bucket:
        return
    last = max(bucket, key=lambda row: row.get("completed_at", row["started_at"]))
    if last["status"] not in TRANSIENT:
        return
    stored = float(last.get("retry_until", 0))
    if not math.isfinite(stored) or stored < 0:
        raise ValueError("Cooldown provider không hợp lệ")
    ordinal = max(0, sum(row.get("slot") == last["slot"] for row in current) - 1) if "slot" in last else 0
    response = {**last, "response": last.get("response", ""),
                "headers": last.get("headers", last.get("rate_limits", {})),
                "completed_at": last.get("completed_at", last["started_at"])}
    until = max(stored, cooldown(response, ordinal))
    if until > now:
        raise Deferred(until)


class ProviderCalls(ModelCalls):
    """Giữ raw/retry/repair/UUID U08, admission dựa vào phản hồi provider."""
    def call(self, slot: str, org: int, body: dict[str, Any], attempt: str) -> tuple[Any, dict[str, Any]]:
        """Ghi telemetry cả khi Deferred phát sinh trước ready trong máy retry U08."""
        try:
            return super().call(slot, org, body, attempt)
        except Deferred as error:
            model = body["model"]
            rows = [row for row in self.state["rows"] if row["org"] == org and row_model(row) == model]
            self.waiting_models[org] = {"model": model, "resume_at": error.until,
                "last_http_status": rows[-1]["status"] if rows else None,
                "reason": "PROVIDER_RETRY_AFTER_OR_BACKOFF"}
            raise

    def ready(self, org: int, tokens: int) -> None:
        """Không suy lịch chờ từ bộ đếm hoặc header của response thành công cũ."""
        admit(self.state, org, MODEL.get(), tokens, self.clock(), self.attempt_cap_total)
