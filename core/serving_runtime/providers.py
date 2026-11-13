"""Provider as-of mới dùng dữ liệu/PIT frozen và adapter phương pháp hiện hữu."""
from __future__ import annotations

import base64
from copy import deepcopy
import hashlib
from pathlib import Path
from types import SimpleNamespace
import threading
from typing import Any

import pandas as pd

from core.unified_contracts import SharedSnapshot, digest
from core.serving_runtime.resources import START, decision_config

NUMERIC_LOCK = threading.RLock()


class AsOfProvider:
    """Mỗi job sở hữu scope, HMM/bank/context/selector riêng; không đọc forecast U09."""

    def __init__(self, root: Path, points: list[dict], models: dict, variants: list[str]) -> None:
        from core.unified_asset_providers import study_data, FrozenStudyBank, FrozenStudyContext
        from core.historical_evaluation_runner import Regimes
        from core.unified_protocol import read
        from core.variant_registry import execution_order
        self.root, self.points, self.models = root, deepcopy(points), deepcopy(models)
        self.data = study_data(root)
        self.config = decision_config(models)
        self.data.protocol["inference"]["config"] = deepcopy(self.config)
        self.alpha = read(root, "outputs/unified_integration/u06_assets_v2/frozen_alpha_manifest.json")
        self.prices = {}
        for symbol in {p["symbol"] for p in points}:
            source = self.alpha["causal_sources"][symbol + "/f2026_q3"]
            frame = pd.DataFrame(read(root, source["prices"]))
            frame["Datetime"] = pd.to_datetime(frame.Datetime)
            self.prices[symbol] = frame
        self.selectors: dict[str, Any] = {}
        self._book = None
        plan = execution_order(variants)
        self.bank = FrozenStudyBank(self.data, [{"symbol": p["symbol"], "date": p["cutoff"], "fold": p["fold"]} for p in points]) if any(v in plan for v in ("bayesian_v1", "C2", "A_tp_pool", "B_semantic")) else None
        self.regimes = Regimes(self.data, root) if self.bank else None
        # Freeze độc lập cửa sổ người dùng; không thêm bất kỳ query serving nào vào context.
        self.context = FrozenStudyContext(self.data, START) if "MT_BICL" in plan else None
        self.episodes: dict[str, dict] = {}
        module = self.data.scope.module("unified_methods")
        self.resolve = module.resolve
        self._validate = module.validate_prepared
        self.adapter = module.MethodAdapters(self.config, bank_factory=lambda: self.bank,
            regime=lambda cutoff: self.regimes.get(cutoff), facts=self.facts,
            context_factory=lambda: SimpleNamespace(build=self.episode, variants=self.context.variants))

    def prefix(self, point: dict[str, str]) -> pd.DataFrame:
        """Forecast chỉ nhận prefix, tuyệt đối không trả entry/exit tương lai."""
        frame = self.prices[point["symbol"]]
        prefix = frame.loc[frame.Datetime <= pd.Timestamp(point["cutoff"])].copy(deep=True)
        if len(prefix) < 600 or str(prefix.Datetime.iloc[-1].date()) != point["cutoff"]:
            raise ValueError("Prefix thiếu 600 bars hoặc không đúng as-of")
        return prefix

    def validate_point(self, point: dict) -> None:
        """Selector chỉ replay integrity trên train/validation đã khóa, không fit query mới."""
        from core.causal_alpha import FrozenSelector
        from core.unified_protocol import read
        symbol = point["symbol"]
        if symbol not in self.selectors:
            source = self.alpha["causal_sources"][symbol + "/f2026_q3"]
            self.selectors[symbol] = FrozenSelector(read(self.root, source["selector"]), self.prices[symbol])
        self.selectors[symbol].predict(self.prefix(point), point["cutoff"])
        self.data.news.get_sentiment_at(symbol, point["cutoff"])
        self.facts(point)

    def facts(self, point: dict) -> dict:
        """Facts query được tính từ giá mới as-of, không lookup prepared episode U09."""
        if self.context is not None:
            return deepcopy(self.episode(point["symbol"], point["cutoff"])["advisor"]["query_facts"])
        return self.data.scope.module("mt_bicl_features").make_fact_packet(self.prefix(point), point["symbol"], point["cutoff"])

    def episode(self, symbol: str, cutoff: str) -> dict:
        """Context/student frozen; truy xuất prior mature trước freeze, query chỉ có x."""
        key = symbol + "-" + cutoff
        if key not in self.episodes:
            self.episodes[key] = self.context.build(symbol, cutoff)
        return deepcopy(self.episodes[key])

    def prepare(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int) -> dict:
        """Khóa đoạn capture stdout của native factory, không chia sẻ preparation giữa job."""
        with NUMERIC_LOCK:
            return self.adapter.prepare(variant, snapshot, deepcopy(dependencies), repeat)

    def validate(self, variant: str, snapshot: SharedSnapshot, prepared: dict, repeat: int) -> None:
        """Dựng lại prompt/schema và kiểm cap trước khi dispatch HTTP."""
        with NUMERIC_LOCK:
            self._validate(variant, snapshot, prepared, self.config, repeat)

    def shared(self, book: Any, point: dict, calls: Any) -> dict:
        """I→P→T chạy một lần; ảnh/outputs có đường run/point, không chdir hoặc file ảnh chung."""
        from agents.indicator_agent import create_indicator_agent
        from agents.pattern_agent import create_pattern_agent
        from agents.trend_agent import create_trend_agent
        from agents.alpha_agent import create_alpha_agent
        from core.causal_alpha import FrozenSelector
        from core.causal_bridge import bind_snapshot
        from core.unified_methods import snapshot_from_graph
        from core.research_invocation import ENABLED, invocation_scope
        from core.historical_signals import snapshot_payload
        from core.prior_stage_journal import encode_output
        from utils.graph_util import TechnicalTools
        from utils import static_util
        state = self.data.state(point["symbol"], point["cutoff"])
        for role in ("pattern", "trend"):
            def render(_: str, role: str = role) -> dict:
                with NUMERIC_LOCK:
                    image = (static_util.generate_kline_image if role == "pattern" else static_util.generate_trend_image)(
                        deepcopy(state["kline_data"]), write_artifacts=False)
                raw = base64.b64decode(image[role + "_image"], validate=True)
                path = book.directory / "images" / point["id"] / (role + ".png")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                return {role + "_image": image[role + "_image"]}
            image = book.execute("render/" + point["id"] + "/" + role, {"kline_sha256": digest(state["kline_data"])}, render)
            raw = base64.b64decode(image[role + "_image"], validate=True)
            path = book.directory / "images" / point["id"] / (role + ".png")
            if path.exists() and path.read_bytes() != raw:
                raise ValueError("Ảnh point khác checkpoint đã khóa")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            state.update(image)
        for role in ("indicator", "pattern", "trend", "full"):
            slot = "graph/" + point["id"] + "/" + role
            def invoke(attempt: str, role: str = role, slot: str = slot) -> dict:
                proxy = VisionProxy(calls, slot, attempt, self.models[role] if role != "full" else self.models["alpha"])
                nodes = {"indicator": lambda: create_indicator_agent(None, TechnicalTools()),
                    "pattern": lambda: create_pattern_agent(None, proxy, TechnicalTools()),
                    "trend": lambda: create_trend_agent(None, proxy, TechnicalTools()),
                    "full": lambda: create_alpha_agent(None, True, True, strict_research_mode=True)}
                token = ENABLED.set(True)
                try:
                    with invocation_scope(role):
                        return nodes[role]()(deepcopy(state))
                finally:
                    ENABLED.reset(token)
            inputs = {k: v for k, v in state.items() if k not in ("point_in_time_df", "sentiment_store")}
            inputs["point_in_time_df"] = snapshot_payload(state["point_in_time_df"])
            output = book.execute(slot, {"state_sha256": digest(encode_output(inputs))}, invoke)
            state.update(output)
        state["alpha_factors"] = deepcopy(state["sentiment_data"]["alpha_results"])
        return self.snapshot(point, state)

    def snapshot(self, point: dict, state: dict) -> dict:
        """Biên đóng snapshot chung; provider live dùng cùng upstream với nguồn riêng đã khóa."""
        from core.causal_bridge import bind_snapshot
        from core.unified_methods import snapshot_from_graph
        source = self.alpha["causal_sources"][point["symbol"] + "/f2026_q3"]
        price_sha = hashlib.sha256((self.root / source["prices"]).read_bytes()).hexdigest()
        prefix = self.prefix(point)
        snapshot = snapshot_from_graph(point, 0, state, prefix.tail(600), price_sha, [])
        symbol = point["symbol"]
        self.validate_point(point)
        return bind_snapshot(snapshot, self.selectors[symbol], prefix, price_sha).document()

    def outcome(self, point: dict) -> dict:
        """Runner chỉ gọi sau đủ forecast point; oracle chung tính nhãn theo giá VND."""
        from core.serving_runtime.runner import slot_id
        if (self._book is None or self._mode != "backtest" or point not in self.points
                or not all(self._book.complete(slot_id(point, repeat, variant))
                           for repeat in range(self._repeats) for variant in self._plan)):
            raise ValueError("Query payoff bị khóa trước đủ forecast durable")
        from core.unified_experiment import outcome_from_frame
        frame = self.data.frames[point["symbol"]]
        frame[["Open", "High", "Low", "Close"]] *= 1000.
        source = self.alpha["causal_sources"][point["symbol"] + "/f2026_q3"]["prices"]
        return outcome_from_frame(point, frame, hashlib.sha256((self.root/source).read_bytes()).hexdigest())

    def bind_book(self, book: Any, plan: list[str], repeats: int, mode: str) -> None:
        """Cấp đường đọc outcome từ journal thực, không nhận cờ forecast_done do agent tự khai."""
        if self._book is not None and self._book.signature != book.signature:
            raise ValueError("Provider không được dùng chung giữa hai job")
        self._book, self._plan, self._repeats, self._mode = book, list(plan), repeats, mode


class VisionProxy:
    """ABI SDK thuần; sender durable duy nhất quản retry/quota/UNKNOWN."""

    def __init__(self, calls: Any, slot: str, attempt: str, model: dict) -> None:
        self.calls, self.slot, self.attempt, self.model = calls, slot, attempt, model

    def invoke(self, messages: Any) -> Any:
        """Không mở client LLM thứ hai hoặc fallback model khi transport lỗi."""
        from langchain_groq.chat_models import _convert_message_to_dict
        from langchain_core.messages import AIMessage
        body = {"model": self.model["model"], "stream": False, "n": 1, "temperature": max(1e-8, self.model["options"]["temperature"]),
                "max_tokens": self.model["options"]["max_tokens"], "service_tier": "on_demand",
                "reasoning_effort": "none", "reasoning_format": "hidden", "stop": None,
                "messages": [_convert_message_to_dict(m) for m in messages]}
        from core.serving_runtime.quota import Failed
        try:
            reply, _ = self.calls.call(self.slot, body, self.attempt)
        except (ValueError, AssertionError, OSError, KeyError):
            raise Failed("INTEGRITY_FAILURE") from None
        return AIMessage(content=reply)
