"""Tách admission theo org/model và tái dùng máy retry bền vững của U08."""
from __future__ import annotations

from contextvars import ContextVar
from types import SimpleNamespace
from typing import Any

from core.groq_pacing import MODEL_LIMITS
from core.unified_execution_transport import DurableCalls, Deferred, Exhausted
from core.unified_live.transport import LiveCalls

POLICY = "per_org_model_v1"
MODEL: ContextVar[str] = ContextVar("unified_quota_model", default="")


def row_model(row: dict[str, Any]) -> str:
    """Đọc cả carry lịch sử và raw hosted, từ chối model thiếu hoặc mâu thuẫn."""
    model = row.get("model", row.get("body", {}).get("model"))
    if model not in MODEL_LIMITS or row.get("body", {}).get("model", model) != model:
        raise ValueError("Ledger thiếu model hợp lệ hoặc model mâu thuẫn")
    return model


def admit(state: dict[str, Any], org: int, model: str, tokens: int, now: float,
          attempt_cap: int) -> None:
    """Giữ nguyên cửa sổ, reserve, header và backoff, lọc đúng bucket trước admission."""
    if model not in MODEL_LIMITS:
        raise ValueError("Model ngoài policy quota đã khóa")
    if len(state["rows"]) >= attempt_cap:
        raise Exhausted("Hết trần HTTP của phase U08")
    filtered = {key: [row for row in state[key] if row_model(row) == model]
                for key in ("carry", "rows")}
    view = SimpleNamespace(state=filtered, clock=lambda: now)
    DurableCalls.ready(view, org, tokens)


class ModelCalls(LiveCalls):
    """Giữ identity/UUID/raw U08, thay riêng cách chọn bucket trước HTTP mới."""
    def call(self, slot: str, org: int, body: dict[str, Any], attempt: str) -> tuple[Any, dict[str, Any]]:
        """Scope model theo body thực, kể cả khi máy trạng thái gọi lại để parse/repair."""
        token = MODEL.set(row_model({"body": body}))
        try:
            return super().call(slot, org, body, attempt)
        finally:
            MODEL.reset(token)

    def ready(self, org: int, tokens: int) -> None:
        """Ghi rõ model đang chờ trong telemetry, trần phase vẫn cộng mọi model."""
        model = MODEL.get()
        try:
            admit(self.state, org, model, tokens, self.clock(), self.attempt_cap_total)
        except Deferred as error:
            self.waiting_models[org] = {"model": model, "reserved_tokens": tokens,
                                        "resume_at": error.until}
            raise

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Dùng nguyên kiểm tra identity, carry và kiểu sender của transport U08."""
        super().__init__(*args, **kwargs)
        self.waiting_models: dict[int, dict[str, Any]] = {}
