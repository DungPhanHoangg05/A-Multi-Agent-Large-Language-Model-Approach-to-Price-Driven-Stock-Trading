"""Provider U07 chạy node/renderer thật với mock vision; tài nguyên U06 giữ frozen."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from core.unified_contracts import SharedSnapshot, digest
from core.unified_execution_transport import DurableCalls
from core.unified_preflight import ASSETS
from core.unified_protocol import MANIFEST, read


class StudyProviders:
    """Node upstream độc lập từng stage, một snapshot cho cả tám nhánh và ba repeat."""
    def __init__(self, root: Path, calls: DurableCalls, *, fixture_images: bool = False,
                 cohort: list[dict[str, Any]] | None = None) -> None:
        from core.unified_asset_providers import study_data, FrozenStudyBank
        from core.unified_preflight_assets import frames
        from core.historical_evaluation_graph import GraphProvider
        from core.historical_evaluation_runner import Regimes
        self.root, self.calls = root, calls
        self.data = study_data(root)
        self.original = read(root, MANIFEST, True)["points"] if cohort is None else deepcopy(cohort)
        self.points = [{"id": p["runner_point_id"], "symbol": p["symbol"], "cutoff": p["date"],
                        "fold": p["fold"], "quality": "U07_CONTROL_NOT_MARKET_FORECAST"} for p in self.original]
        ids = {p["id"] for p in self.original}
        self.data.by_day = {k: v for k, v in self.data.by_day.items() if v["id"] in ids}
        self.prices = frames(root)
        self.alpha = read(root, ASSETS + "/frozen_alpha_manifest.json")
        self.bank = FrozenStudyBank(self.data, self.original)
        self.regimes = Regimes(self.data, root)
        self.renderer = GraphProvider(self.data, None, fixture=fixture_images)
        self.module = self.data.scope.module("unified_methods")
        self.contexts: dict[str, Any] = {}
        self.episodes: dict[str, Any] = {}
        self.selectors: dict[str, Any] = {}
        self.resolve = self.module.resolve
        self.adapter = self.module.MethodAdapters(self.data.protocol["inference"]["config"],
            bank_factory=lambda: self.bank, regime=self.regimes.get,
            facts=lambda point: deepcopy(self.episode(point["id"])["advisor"]["query_facts"]),
            context_factory=lambda: SimpleNamespace(build=lambda symbol, cutoff: self.episode(symbol + "-" + cutoff),
                variants=lambda episode: next(iter(self.contexts.values())).variants(episode)))

    def episode(self, point_id: str) -> dict[str, Any]:
        """Fold frozen trước query đầu, tất cả102 ID bị chặn trước oracle lịch sử."""
        from core.unified_asset_providers import FrozenStudyContext
        point = next(p for p in self.points if p["id"] == point_id)
        fold = point["fold"]
        if fold not in self.contexts:
            first = min(p["cutoff"] for p in self.points if p["fold"] == fold)
            self.contexts[fold] = FrozenStudyContext(self.data, first)
        if point_id not in self.episodes:
            self.episodes[point_id] = self.contexts[fold].build(point["symbol"], point["cutoff"])
        return deepcopy(self.episodes[point_id])

    def prepare(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int) -> dict:
        """Gọi đúng adapter chín mã; không truy cập outcome hoặc tạo client."""
        return self.adapter.prepare(variant, snapshot, dependencies, repeat)

    def validate(self, variant: str, snapshot: SharedSnapshot, prepared: dict, repeat: int) -> None:
        """Validator thuần cùng namespace, không nạp bank/student khi replay."""
        self.module.validate_prepared(variant, snapshot, prepared, self.data.protocol["inference"]["config"], repeat)

    def shared(self, book: Any, point: dict[str, Any], org: int) -> dict[str, Any]:
        """Indicator → Pattern → Trend → Alpha/sentiment thực, không compact lại report native."""
        from agents.indicator_agent import create_indicator_agent
        from agents.alpha_agent import create_alpha_agent
        from agents.pattern_agent import create_pattern_agent
        from agents.trend_agent import create_trend_agent
        from core.causal_alpha import FrozenSelector
        from core.causal_bridge import bind_snapshot
        from core.research_invocation import ENABLED, invocation_scope
        from core.prior_stage_journal import encode_output
        from core.historical_signals import snapshot_payload
        from utils.graph_util import TechnicalTools
        import pandas as pd
        state = self.data.state(point["symbol"], point["cutoff"])
        for role in ("pattern", "trend"):
            image = book.execute(f"render/{point['id']}/{role}", {"kline_sha256": digest(state["kline_data"]),
                "renderer_sha256": self.renderer.renderer_hash}, lambda _, role=role: self.renderer.render(role, state["kline_data"]))
            state.update(image)
        config = self.data.protocol["inference"]["config"]
        for role in ("indicator", "pattern", "trend", "full"):
            slot = f"graph/{point['id']}/{role}"
            def invoke(attempt: str) -> dict:
                proxy = VisionProxy(self.calls, slot, org, attempt, config)
                nodes = {"indicator": lambda: create_indicator_agent(None, TechnicalTools()),
                         "pattern": lambda: create_pattern_agent(None, proxy, TechnicalTools()),
                         "trend": lambda: create_trend_agent(None, proxy, TechnicalTools()),
                         "full": lambda: create_alpha_agent(None, True, True, strict_research_mode=True)}
                token = ENABLED.set(True)
                try:
                    with invocation_scope(role), redirect_stdout(io.StringIO()):
                        return nodes[role]()(deepcopy(state))
                finally:
                    ENABLED.reset(token)
            state_input = {k: v for k, v in state.items() if k not in ("point_in_time_df", "sentiment_store")}
            state_input["point_in_time_df"] = snapshot_payload(state["point_in_time_df"])
            state_input["news"] = self.data.news.get_sentiment_at(point["symbol"], point["cutoff"])[0]
            output = book.execute(slot, {"state_sha256": digest(encode_output(state_input)), "org": org}, invoke)
            state.update(output)
        symbol, cutoff = point["symbol"], point["cutoff"]
        state["alpha_factors"] = deepcopy(state["sentiment_data"]["alpha_results"])
        prefix = self.prices[symbol].loc[self.prices[symbol].Datetime <= pd.Timestamp(cutoff)].copy()
        paths = self.alpha["causal_sources"][symbol + "/" + point["fold"]]
        source_sha = hashlib.sha256((self.root / paths["prices"]).read_bytes()).hexdigest()
        base = self.module.snapshot_from_graph(point, 0, state, prefix.tail(600), source_sha, [])
        if symbol not in self.selectors:
            self.selectors[symbol] = FrozenSelector(read(self.root, paths["selector"]), self.prices[symbol])
        return bind_snapshot(base, self.selectors[symbol], prefix, source_sha).document()


class VisionProxy:
    """Đưa message thật từ node qua ABI SDK thuần và raw transport durable."""
    def __init__(self, calls: DurableCalls, slot: str, org: int, attempt: str, config: dict) -> None:
        self.calls, self.slot, self.org, self.attempt, self.config = calls, slot, org, attempt, config

    def invoke(self, messages: Any) -> Any:
        """Không tạo ChatGroq/httpx.Client; không mở fallback model khi lỗi transport."""
        from langchain_groq.chat_models import _convert_message_to_dict
        from langchain_core.messages import AIMessage
        models = self.config["signal_config"]["models"]
        body = {"model": models["graph_llm_model"], "stream": False, "n": 1,
                "temperature": max(1e-8, models["graph_llm_temperature"]), "stop": None,
                "reasoning_format": None, "reasoning_effort": None,
                "service_tier": self.config["service_tier"], **deepcopy(self.config["client_options"]["graph"]),
                "max_tokens": models["graph_llm_max_tokens"], "messages": [_convert_message_to_dict(m) for m in messages]}
        content, _ = self.calls.call(self.slot, self.org, body, self.attempt)
        return AIMessage(content=content)


def cold_methods(root: Path, config: dict) -> Any:
    """Chỉ schema/renderer/policy; verifier không dựng StudyProviders hoặc numeric models."""
    from core.unified_asset_providers import StudyScope
    module = StudyScope(root).module("unified_methods")
    return SimpleNamespace(resolve=module.resolve,
        validate=lambda variant, snapshot, prepared, repeat: module.validate_prepared(variant, snapshot, prepared, config, repeat))
