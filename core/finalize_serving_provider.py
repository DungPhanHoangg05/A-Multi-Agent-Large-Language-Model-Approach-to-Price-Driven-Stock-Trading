"""Adapter serving bản sửa; tái dùng graph paired, FIN07 và policy thực thi."""
from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace
from typing import Any

import pandas as pd

from core.causal_alpha import frame_document
from core.causal_bridge import REPAIRED_NATIVE_PROFILE, bind_snapshot, decision_payload
from core.execution_prices import raw_point_in_time_snapshot
from core.finalize_bank_resources import HMM, SOURCE
from core.finalize_context import FinalizedProviders, RawFrozenSelector
from core.finalize_news import snapshot_values
from core.finalize_ohlcv_keys import key_at
from core.finalize_price_audit import visible_event_dates
from core.finalize_serving_profile import VERSION
from core.finalize_serving_resources import FinalizedResources
from core.historical_signals import snapshot_payload
from core.pit_price_features import extract_pit_price_features
from core.regime_detector import MarketRegimeDetector, training_data_hash
from core.serving_runtime.providers import AsOfProvider, NUMERIC_LOCK
from core.serving_runtime.resources import START, decision_config
from core.serving_live.catalog import MIN_BARS, CatalogAlpha, CatalogPrior
from core.ui_presentation.live import LivePresentation
from core.unified_contracts import REPORTS, SharedSnapshot, digest
from core.variant_registry import execution_order


class ServingProjection(FinalizedProviders):
    """Mở điểm as-of/live từ prefix giá, giữ bank/fit/102 reservation FIN07."""
    def __init__(self, resources: FinalizedResources, points: list[dict], models: dict) -> None:
        super().__init__(resources.root)
        self.decision = decision_config(models)
        self.catalog = resources.catalog
        archived_fit = self.market.loc[self.market.Datetime <= pd.Timestamp("2022-12-30")]
        self.hmm = MarketRegimeDetector.load(resources.root/HMM, expected_training_hash=training_data_hash(archived_fit))
        ledger = self.ledgers
        live = resources.live
        if live is not None:
            if 'live_news' in live:
                self.news = resources.live_news
            symbol, cutoff = live["symbol"], live["cutoff"]
            self.frames[symbol] = resources.live_frame.copy(deep=True)
            self.market = resources.live_market.copy(deep=True)
            self.calendar = pd.DatetimeIndex(self.market.Datetime)
            self.source_hashes[symbol] = resources.snapshot_id
            ledger = {**ledger, symbol: live["events"]}
            # Transfer chỉ mở cửa sổ query. Origin, giá fit, top5, orientation,
            # ngưỡng và lựa chọn của selector FIN06 đều qua kiểm hash gốc.
            if self.catalog:
                from core.unified_asset_providers import StudyScope
                self.scope = StudyScope(self.root, source=SOURCE)
                self.scope.symbols = (*self.scope.symbols, symbol)
                self.context.data.scope = self.scope
                self.context.ledgers = ledger
                transfer = CatalogAlpha(self.selector_docs)
            else:
                artifact = self.selector_docs[symbol]
                reserved = {p["cutoff"] for p in self.points.values() if p["symbol"] == symbol}
                transfer = RawFrozenSelector(artifact, reserved)
                transfer._artifact["payload"]["schedule"]["test_end"] = max(cutoff, artifact["payload"]["schedule"]["test_end"])
                transfer._artifact["sha256"] = digest({"version": VERSION + "/live_selector_transfer_v1",
                    "parent": artifact["sha256"], "capture": resources.snapshot_id, "cutoff": cutoff})
            self._selectors[symbol] = transfer
            context_data = self.context.data
            # Chỉ TaskBuilder cần metadata dự kiến t+1/t+3; HMM/khóa T/P
            # tiếp tục dùng lịch quan sát. Không sinh nến hay outcome live.
            planned = pd.bdate_range(pd.Timestamp(cutoff) + pd.Timedelta(days=1), periods=3)
            context_data.calendar = self.calendar.union(planned)
            context_data.history = self.market
            self.context.folds["finalize_live_daily"] = START

        for point in points:
            self.add_point(point, ledger, live is not None)
        self.prior = self._prior()
        if self.catalog:
            self.prior = CatalogPrior(self.prior)

    def add_point(self, point: dict, ledgers: dict, live: bool) -> None:
        """Dùng cùng key_at, price_feature, HMM đã pin và khóa hash tin của điểm."""
        symbol, cutoff, identifier = (point[name] for name in ("symbol", "cutoff", "id"))
        raw = self.frames[symbol]
        prefix = raw_point_in_time_snapshot(raw, cutoff)
        features = prefix.merge(raw[["Datetime", "Reference"]], on="Datetime", validate="one_to_one")
        visible, _ = visible_event_dates(ledgers[symbol], cutoff)
        feature = extract_pit_price_features(features, [{"exrightDate": day} for day in visible],
                                             self.calendar, cutoff, source=SOURCE)
        regime = self.hmm.classify_regime(self.market.loc[self.market.Datetime <= cutoff].copy(), cutoff)
        key = key_at(prefix, self.calendar, cutoff)
        if (len(prefix) < (MIN_BARS if self.catalog else 600) or regime["feature_end_date"] > cutoff
                or (not self.catalog and key["reason"] is not None)):
            raise ValueError("Preparation FIN08 thiếu prefix hoặc regime tại cutoff")
        projection = {**point, "regime": regime["regime_name"], "feature": feature,
            "retrieval_key": key, "price_prefix_sha256": digest(frame_document(prefix)),
            "selector_sha256": self._selectors[symbol].sha256 if self.catalog else self.selector_docs[symbol]["sha256"],
            "news_snapshot_sha256": self.news.snapshot(symbol, cutoff)["sha256"]}
        if not live and identifier in self.points:
            existing = self.points[identifier]
            if any(existing.get(k) != v for k, v in projection.items() if k != "quality"):
                raise ValueError("Binding serving lệch projection đã kiểm FIN07")
        self.points[identifier] = projection
        calendar = self.context.data.calendar
        planned_exit = str(calendar[calendar.get_loc(pd.Timestamp(cutoff)) + 3].date())
        self.context.data.by_day[(symbol, cutoff)] = {"id": identifier, "exit_date": planned_exit}

    def bind(self, snapshot: SharedSnapshot) -> SharedSnapshot:
        """Giữ xác minh nguồn và bỏ Alpha có lý do khi mã live mới thiếu lịch sử."""
        if not self.catalog:
            return super().bind(snapshot)
        doc = snapshot.document()
        point = self.points[doc['point']['id']]
        symbol, cutoff = point['symbol'], point['cutoff']
        prefix = raw_point_in_time_snapshot(self.frames[symbol], cutoff)
        source = self.source_hashes[symbol]
        selector = self._selectors[symbol]
        if (any(doc['point'][k] != point[k] for k in ('symbol', 'cutoff', 'fold'))
                or doc['provenance']['source_sha256'] != source
                or digest(frame_document(prefix)) != point['price_prefix_sha256']
                or doc['payload']['price_prefix'] != frame_document(prefix.tail(600))
                or selector.sha256 != point['selector_sha256']):
            raise ValueError('Snapshot danh mục live khác nguồn đã khóa')
        if selector.predict(prefix, cutoff) is None:
            if 'causal_alpha' in doc['payload']:
                raise ValueError('Snapshot chứa Alpha không khả dụng')
            return snapshot
        return bind_snapshot(snapshot, selector, prefix, source)


class FinalizedProvider(LivePresentation, AsOfProvider):
    """Chỉ đổi nguồn/projection trên shared runner, giữ upstream và checkpoint hiện hữu."""
    def __init__(self, resources: FinalizedResources, points: list[dict], models: dict, variants: list[str], *, preview: bool = True) -> None:
        self.resources, self.models, self.points = resources, deepcopy(models), deepcopy(points)
        self.projection = ServingProjection(resources, points, models)
        self.config = self.projection.decision
        self.data = SimpleNamespace(state=self.state)
        self._book = None
        self._requested = execution_order(variants)
        self.preview = preview
        self._adapters: dict[str, Any] = {}
        self._alpha: dict[str, dict] = {}

    def prefix(self, point: dict) -> pd.DataFrame:
        """Đúng origin, ngày đóng và chỉ OHLCV đã biết trước Decision."""
        return raw_point_in_time_snapshot(self.projection.frames[point["symbol"]], point["cutoff"])

    def state(self, symbol: str, cutoff: str) -> dict:
        """State upstream một lần, không gọi crawler/Alpha legacy hoặc target oracle."""
        prefix = self.prefix({"symbol": symbol, "cutoff": cutoff})
        return {"stock_name": symbol, "as_of_date": cutoff, "window_end_date": cutoff, "time_frame": "1d",
                "language": "vi", "is_backtest": True, "messages": [], "kline_data": snapshot_payload(prefix.tail(45)),
                "point_in_time_df": prefix.tail(600), "sentiment_store": self.projection.news}

    def alpha(self, point: dict) -> dict:
        """Chỉ áp dụng selector đã fit, không chạy create_alpha_agent."""
        key, symbol, cutoff = (point[name] for name in ("id", "symbol", "cutoff"))
        if key not in self._alpha:
            projection = self.projection
            if symbol not in projection._selectors:
                reserved = {p["cutoff"] for p in projection.points.values() if p["symbol"] == symbol}
                projection._selectors[symbol] = RawFrozenSelector(projection.selector_docs[symbol], reserved)
            self._alpha[key] = projection._selectors[symbol].predict(self.prefix(point), cutoff) or {
                'factors': [], 'report': 'Chưa đủ dữ liệu để tính bộ Alpha chuyển giao. Tín hiệu Alpha không khả dụng.'}
        return deepcopy(self._alpha[key])

    def validate_point(self, point: dict) -> None:
        """Xác nhận Alpha/NA/facts và nguồn context trước vision ở cả chế độ live."""
        with NUMERIC_LOCK:
            self.alpha(point)
            self.projection.news.snapshot(point["symbol"], point["cutoff"])
            if "MT_BICL" in self._requested:
                self.projection.context.build(point["symbol"], point["cutoff"])
            elif "Fact_Anchor" in self._requested:
                self.projection.context.facts(point)

    def alpha_stage(self, state: dict) -> dict:
        """Cấp chung năm factor và report tin đã khóa cho Native lẫn các extension."""
        symbol, cutoff = state["stock_name"], state["as_of_date"]
        point = self.projection.points[symbol+"-"+cutoff]
        alpha = self.alpha(point)
        data, report = snapshot_values(self.projection.news.snapshot(symbol, cutoff), expected_sha256=point["news_snapshot_sha256"])
        return {"alpha_factors": alpha["factors"], "alpha_report": alpha["report"],
                "sentiment_data": data, "sentiment_report": report}

    def report_pair(self, role: str, state: dict, output: dict, display: dict) -> dict:
        """Hiển thị VI/EN dùng cùng năm giá trị, chạy ngoài prompt canonical."""
        if role != "full":
            return super().report_pair(role, state, output, display)
        from utils.i18n import signal_label
        lines = [f"{r['alpha_id']}: {r['value']:+.6f}; {signal_label(r['signal'], 'en')}" for r in output["alpha_factors"]]
        intro = 'Causal alpha from the frozen five-factor selector.'
        if self.resources.catalog:
            intro = ('Live alpha uses factors transferred from the frozen selectors.' if lines else
                     'Insufficient data for transferred alpha. Alpha signals are unavailable.')
        return {"vi": output["alpha_report"], "en": "\n".join([intro, *lines])}

    def snapshot(self, point: dict, state: dict) -> dict:
        """Seal snapshot đã ràng buộc giá/source và projection trước mọi branch."""
        from core.unified_methods import snapshot_from_graph
        prefix = self.prefix(point)
        source = self.projection.source_hashes[point["symbol"]]
        if self.resources.catalog and len(prefix) < 600:
            from utils.json_util import to_json_compatible
            keys = (*REPORTS, 'stock_name', 'as_of_date', 'time_frame', 'language', 'is_backtest',
                    'pattern_image', 'trend_image', 'alpha_factors', 'sentiment_data')
            payload = to_json_compatible({**{key: state[key] for key in keys if key in state},
                                          'price_prefix': frame_document(prefix)})
            original = SharedSnapshot.create(point, 0, payload, {'source_sha256': source,
                'upstream_sha256': digest(payload), 'price_end': point['cutoff'], 'news_dates': []})
        else:
            original = snapshot_from_graph(point, 0, state, prefix.tail(600), source, [])
        return self.projection.bind(original).document()

    def adapter(self, snapshot: SharedSnapshot) -> Any:
        """Cache adapter theo point trong job, không chia sẻ giữa owner/run."""
        identifier = snapshot.document()["point"]["id"]
        if identifier not in self._adapters:
            self._adapters[identifier], _ = self.projection.adapters(identifier)
        return self._adapters[identifier]

    def prepare(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int) -> dict:
        """Native giữ renderer gốc, nhưng đọc chính projection causal như Common."""
        with NUMERIC_LOCK:
            adapter = self.adapter(snapshot)
            if variant != "original_fix":
                return adapter.prepare(variant, snapshot, dependencies, repeat)
            from core.unified_methods import native_request
            bound = adapter.bind_point(snapshot)
            adapter.verify_dependencies(variant, bound, dependencies, repeat)
            alpha = bound.document()['payload'].get('causal_alpha')
            shared = decision_payload(bound, variant, decision_profile=REPAIRED_NATIVE_PROFILE if alpha else None)
            request = native_request(shared, {"decision": self.config}, repeat)
            return {"request": request, "trace": {"fallback": False, "decision_profile": REPAIRED_NATIVE_PROFILE,
                    "alpha_projection_sha256": alpha['projection']['projection_sha256'] if alpha else None}, "aux": {}}

    def validate_bound(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int, prepared: dict) -> None:
        """Cold replay tái kiểm đúng bộ dependency/canonical request của profile mới."""
        with NUMERIC_LOCK:
            if variant != "original_fix":
                self.adapter(snapshot).validate(variant, snapshot, dependencies, repeat, prepared)
            elif self.prepare(variant, snapshot, dependencies, repeat) != prepared:
                raise ValueError("Native causal khác preparation sealed")

    def wire_body(self, request: dict) -> dict:
        """Nhắc đối chiếu facts trên wire live của các nhánh anchored."""
        from core.ui_presentation.wire import decision_body
        from core.unified_execution_transport import body_for
        if self.resources.live is None:
            return super().wire_body(request)
        return decision_body(body_for(request), ground_facts=True)

    def resolve_bound(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int,
                      prepared: dict, raw: dict | None) -> dict:
        """Giữ action/raw/policy và kiểm same-repeat proof trước resolve."""
        with NUMERIC_LOCK:
            return self.adapter(snapshot).resolve(variant, snapshot, dependencies, repeat, prepared, raw)

    def outcome(self, point: dict) -> dict:
        """Chỉ tính giá trị kinh tế sau đủ tất cả forecast/dependency durable."""
        from core.serving_runtime.runner import slot_id
        if (self.resources.live is not None or self._book is None or self._mode != "backtest" or point not in self.points
                or not all(self._book.complete(slot_id(point, repeat, variant))
                           for repeat in range(self._repeats) for variant in self._plan)):
            raise ValueError("Outcome bị khóa trước forecast barrier")
        if self.preview:
            return self.resources.unavailable(point, "OFFLINE_FIXTURE_OUTCOME_LOCKED")
        return self.resources.outcome(point, self.projection.frames[point["symbol"]])
