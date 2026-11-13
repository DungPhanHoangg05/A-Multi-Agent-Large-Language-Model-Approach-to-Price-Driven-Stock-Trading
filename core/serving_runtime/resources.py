"""Resource release as-of: nạp frozen weights, kiểm nguồn và công bố support đóng."""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from typing import Any

from core.unified_contracts import day, digest, json_bytes

MANIFEST = "docs/plan/week12/serving_resources_v1.json"
MANIFEST_SHA256 = "ec0cb010361533716604b5ea2155ea6303358aa68c30bca16ffa0151e64e704c"
VERSION = "serving_asof_q3_2026_v1"
START, END = "2026-07-01", "2026-09-23"
MAX_POINTS = 30


def binding(path: Path) -> dict[str, Any]:
    """Băm byte thực; không thay newline của tài nguyên lịch sử."""
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


@lru_cache(maxsize=2)
def decode_manifest(raw: bytes) -> bytes:
    """Chỉ release đã pin, không nhận manifest hoặc đường dẫn từ browser."""
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError("Resource manifest khác release serving đã khóa")
    value = json.loads(raw)
    if value["version"] != VERSION or value["support"]["start_date"] != START or value["support"]["end_date"] != END:
        raise ValueError("Support khác release serving")
    return json_bytes(value)


class Resources:
    """Không tạo model/client trong preflight; validate dữ liệu trước bất kỳ HTTP nào."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self._manifest = decode_manifest((root / MANIFEST).read_bytes())

    def document(self) -> dict[str, Any]:
        """Bản sao của resource identity và miền đã cấp."""
        result=json.loads(self._manifest)
        result['support']['generation_languages']=['vi']
        result['support']['languages']=['vi','en']
        return result

    def verify(self) -> None:
        """Không tin stat/mtime; thiếu/hỏng nguồn là lỗi resource, không phải fallback."""
        for name, expected in self.document()["bindings"].items():
            path = self.root / name
            if not path.resolve().is_relative_to(self.root) or path.is_symlink() or binding(path) != expected:
                raise ValueError("Tài nguyên serving thiếu hoặc khác release")

    def points(self, request: dict[str, Any]) -> list[dict[str, str]]:
        """Lịch chung bất biến; backtest mỗi ba phiên, không chồng chu kỳ tài khoản."""
        support = self.document()["support"]
        if (request["timeframe"] != "1d" or request["language"] not in ('vi','en')
                or not set(request["symbols"]) <= set(support["symbols"])
                or not START <= day(request["start_date"]) <= day(request["end_date"]) <= END):
            raise ValueError("Mã/ngày/khung/ngôn ngữ ngoài miền serving đã công bố")
        dates = [d for d in support["calendar"] if request["start_date"] <= d <= request["end_date"]]
        if request["mode"] != "backtest" and dates != [request["start_date"]]:
            raise ValueError("Ngày phân tích không phải phiên đã công bố")
        if request["mode"] == "backtest":
            dates = dates[::3]
        points = [{"id": s + "-" + d, "symbol": s, "cutoff": d, "fold": "serving_q3_2026",
                   "quality": "ASOF_FROZEN_VENDOR_EXPLORATORY"} for d in dates for s in request["symbols"]]
        if not 1 <= len(points) <= MAX_POINTS:
            raise ValueError("Job cần từ 1 đến 30 point không chồng chu kỳ")
        return points


def decision_config(models: dict[str, Any]) -> dict[str, Any]:
    """Projection cấu hình về ABI adapter hiện hữu; không nhận SDK retry hoặc key."""
    decision, vision = models["decision"], models["pattern"]
    return {"client_max_retries": 0, "client_options": {
                "agent": {"reasoning_effort": "low", "reasoning_format": "hidden"},
                "graph": {"reasoning_effort": "none", "reasoning_format": "hidden"}},
            "service_tier": "on_demand", "signal_config": {"alpha_weights": None, "language": "vi",
                "norm_method": "zscore_tanh", "time_frame": "1d", "window_size": 45,
                "models": {"agent_llm_model": decision["model"], "agent_llm_temperature": decision["options"]["temperature"],
                    "agent_llm_max_tokens": decision["options"]["max_tokens"], "graph_llm_model": vision["model"],
                    "graph_llm_temperature": vision["options"]["temperature"], "graph_llm_max_tokens": vision["options"]["max_tokens"]}}}


def validate_models(models: dict[str, Any]) -> None:
    """Release khóa hai model đã có ABI/token estimator; không suy model tùy ý đã hỗ trợ."""
    from core.serving_contracts import MODEL_ROLES
    for role in MODEL_ROLES:
        model = models[role]
        expected = "qwen/qwen3.8-27b" if role in ("pattern", "trend") else "openai/gpt-oss-20b"
        if (model["provider"] != "groq" or model["model"] != expected or "seed" in model["options"]
                or model["options"]["max_tokens"] > (1024 if role in ("pattern", "trend") else 2048)):
            raise ValueError("Model/options ngoài release serving")


def default_models() -> dict[str, Any]:
    """Mặc định tường minh cho client mới; đủ sáu role dù upstream numeric không gọi LLM."""
    from core.serving_contracts import MODEL_ROLES
    return {role: {"provider": "groq", "model": "qwen/qwen3.8-27b" if role in ("pattern", "trend") else "openai/gpt-oss-20b",
                   "options": {"temperature": 0, "max_tokens": 960}} for role in MODEL_ROLES}
