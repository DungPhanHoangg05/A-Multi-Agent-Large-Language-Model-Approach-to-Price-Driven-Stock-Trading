"""Chặn mạng khi chuẩn bị tài nguyên và tạo fixture ngoại tuyến cho các test giao diện."""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import socket
from typing import Any


def encode(value: Any) -> bytes:
    """Mã hóa nhất quán, không cho NaN/Infinity đi vào bằng chứng."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def sha(raw: bytes) -> str:
    """Băm đúng byte đã quan sát."""
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    """Digest ngữ nghĩa riêng cho báo cáo U03, không thay digest archive cũ."""
    return sha(encode(value))


def deny_external_network() -> None:
    """Chặn mạng ngoài máy; loopback dành cho socketpair của asyncio Windows."""
    connect, connect_ex = socket.socket.connect, socket.socket.connect_ex
    def guarded(sock: socket.socket, address: Any) -> Any:
        if isinstance(address, tuple) and address[0] in ("127.0.0.1", "localhost", "::1"):
            return connect(sock, address)
        raise AssertionError("U03 không được kết nối mạng ngoài máy")
    def guarded_ex(sock: socket.socket, address: Any) -> Any:
        if isinstance(address, tuple) and address[0] in ("127.0.0.1", "localhost", "::1"):
            return connect_ex(sock, address)
        raise AssertionError("U03 không được kết nối mạng ngoài máy")
    socket.socket.connect, socket.socket.connect_ex = guarded, guarded_ex
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", MPLBACKEND="Agg")
    os.environ.pop("GROQ_API_KEY", None)


def view(value: Any) -> Any:
    """Lưu ảnh bằng hash PNG/pixel và giữ nguyên digest request đầy đủ ở caller."""
    if isinstance(value, str) and value.startswith("data:image/png;base64,"):
        from PIL import Image
        raw = base64.b64decode(value.split(",", 1)[1], validate=True)
        with Image.open(io.BytesIO(raw)) as picture:
            return {"png_sha256": sha(raw), "rgba_sha256": sha(picture.convert("RGBA").tobytes()),
                    "size": list(picture.size)}
    if isinstance(value, dict):
        return {str(k): view(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [view(v) for v in value]
    if hasattr(value, "item"):
        return view(value.item())
    return value


def client_class() -> type:
    """Doubles chỉ thay transport/response; SDK thật vẫn serialize options/schema."""
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_groq import ChatGroq

    class LocalClient:
        """Ghi request thực ở biên model và trả response xác định, không HTTP."""
        def __init__(self, **options: Any) -> None:
            self.options = {k: v for k, v in options.items() if k != "api_key"}
            self.sdk = ChatGroq(**{**options, "api_key": "u03-offline-placeholder"})
            self.requests: list[dict[str, Any]] = []
            self.schemas: list[dict[str, Any]] = []
            self.replies: list[str] = []

        def record(self, prompt: Any, schema: type | None = None) -> None:
            messages = [HumanMessage(content=prompt)] if type(prompt) is str else prompt
            converted, parameters = self.sdk._create_message_dicts(messages, None)
            body = {"messages": converted, **parameters}
            if schema is not None:
                structured = self.sdk.with_structured_output(schema, method="json_schema", include_raw=True)
                body["response_format"] = structured.steps[0].steps__["raw"].kwargs["response_format"]
            self.requests.append({"wire_sha256": digest(body), "wire": view(body), "client_options": self.options})

        def invoke(self, prompt: Any) -> Any:
            self.record(prompt)
            text = str(prompt).lower()
            if self.replies:
                return AIMessage(content=self.replies.pop(0))
            if "trendline slope" in text or "độ dốc" in text:
                content = ("**Trend direction:** Up\n**Support level:** 84.0\n**Resistance level:** 89.0\n"
                    "**Trendline slope:** Rising\n**Price vs support:** Holding above support\n"
                    "**Detailed analysis:** Higher lows support the structure.\n"
                    "**Trend forecast:** Continued upside above support.\n**Confidence:** Medium")
            elif "pattern" in text or "mô hình" in text:
                content = ("**Pattern:** Rising channel\n**Confidence:** Medium\n**Directional bias:** Bullish\n"
                    "**Evidence:** Higher lows and firm closes\n**Key candles:** Bullish continuation\n"
                    "**Trading implication:** Maintain bias above support")
            else:
                content = "Diễn giải fixture xác định từ dữ liệu đã có."
            return AIMessage(content=content)

        def with_structured_output(self, schema: type, method: str, include_raw: bool) -> Any:
            if method != "json_schema" or include_raw is not True:
                raise AssertionError("Schema method/include_raw đã thay đổi")
            self.schemas.append(schema.model_json_schema())
            owner = self
            class Structured:
                def invoke(self, prompt: Any) -> dict[str, Any]:
                    owner.record(prompt, schema)
                    raw = owner.replies.pop(0) if owner.replies else json.dumps({
                        "decision": "LONG" if "### [4]" in str(prompt) else "SHORT", "forecast_horizon": "T+2.5",
                        "confidence": "Cao", "risk_reward_ratio": 1.8, "evidence_for": "Bằng chứng fixture.",
                        "evidence_against": "Chi phí hai chiều.", "justification": "Phản hồi fixture không dùng payoff."}, ensure_ascii=False)
                    try:
                        parsed = schema.model_validate_json(raw)
                    except ValueError as exc:
                        return {"parsed": None, "raw": AIMessage(content=raw), "parsing_error": str(type(exc).__name__)}
                    return {"parsed": parsed, "raw": AIMessage(content=raw), "parsing_error": None}
            return Structured()
    return LocalClient


def market_frame(poison: bool = False) -> Any:
    """603 nến giá tổng hợp; ba nến outcome nằm ngoài prefix 600 nến."""
    import numpy as np
    import pandas as pd
    index = np.arange(603, dtype=float)
    close = 62. + .042 * index + 1.30 * np.sin(index / 11.) + .45 * np.cos(index / 5.)
    opening = close * (1. + .0018 * np.sin(index / 3.))
    frame = pd.DataFrame({"Datetime": pd.bdate_range("2023-01-02", periods=603), "Open": opening,
        "High": np.maximum(opening, close) + .6, "Low": np.minimum(opening, close) - .6,
        "Close": close, "Volume": (1100000 + 220000 * np.sin(index / 13.) + index * 450).astype(float)})
    if poison:
        frame.loc[600:, ["Open", "High", "Low", "Close"]] *= 1.3
        frame.loc[602, "Close"] *= 1.2
        frame.loc[602, "High"] = max(frame.loc[602, "Open"], frame.loc[602, "Close"]) + 1.
    return frame
