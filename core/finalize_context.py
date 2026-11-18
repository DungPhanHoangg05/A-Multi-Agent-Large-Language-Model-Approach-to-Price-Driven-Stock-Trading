"""Provider offline FIN07 cho prior, facts, context và MT-BICL trên nguồn FIN04–06."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import io
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pandas as pd

from core.causal_alpha import FrozenSelector, frame_document, runtime, validated_frame
from core.causal_bridge import bind_snapshot
from core.execution_prices import raw_point_in_time_snapshot
from core.finalize_bank_resources import ASSETS, MODEL, SOURCE
from core.finalize_bank_signals import check_bindings
from core.finalize_deterministic_bank import OUTPUT, RECIPE, make_recipe
from core.finalize_news import FinalizedNews, snapshot_values
from core.finalize_news_release import CORPUS, COVERAGE
from core.finalize_ohlcv_keys import key_at
from core.finalize_price_acceptance import PROFILE, require_accepted_prices
from core.finalize_price_audit import visible_event_dates
from core.finalize_prior import VARIANTS, FinalizedPrior
from core.finalize_raw_selector import VERSION as RAW_SELECTOR
from core.historical_evaluation_context import ContextBank
from core.historical_evaluation_protocol import PROTOCOL
from core.historical_signals import snapshot_payload
from core.mt_bicl_adapter import StudentAdapter
from core.prior_example_selection import PriceExampleSelector
from core.unified_asset_providers import FrozenStudyStream, StudyScope
from core.unified_contracts import SharedSnapshot, digest
from core.unified_protocol import binding, read, safe

VERSION = "finalize_context_v1"


class RawFrozenSelector(FrozenSelector):
    """Tái dùng predictor FIN03, nạp selector raw đã verifier FIN06 khóa trước query."""
    def __init__(self, artifact: dict, reserved: set[str]) -> None:
        payload = artifact["payload"]
        test_start = payload["schedule"]["test_start"]
        dates = payload["train_dates"] + payload["validation_dates"]
        if (digest(payload) != artifact["sha256"] or payload["version"] != RAW_SELECTOR
                or payload["runtime"] != runtime() or payload["fit_end"] >= test_start
                or any(d >= test_start or d in reserved for d in dates)):
            raise ValueError("Raw selector sai nguồn runtime, fit hoặc reservation")
        self._artifact = deepcopy(artifact)
        self._predictions = {}


class FoldStream(FrozenStudyStream):
    """Chỉ cung cấp feature đã pin ở FIN06 và dữ liệu lịch sử đóng tại đầu fold."""
    def __init__(self, stream: Any, first: str, reserved: set[str], ledgers: dict, prices: dict,
                 scope: StudyScope, points: dict) -> None:
        super().__init__(stream, first)
        self.points = points
        by_date = {day: i for i, day in enumerate(self.calendar.strftime("%Y-%m-%d"))}
        # Ledger áp cho eligibility thực thi khi freeze. Nếu công bố muộn, feature
        # lịch sử liên quan phải dựng theo thông tin tại chính ngày quan sát.
        late = {symbol: [(by_date[day], event) for event in ledger
                if event.get("publicDate") and event.get("exrightDate")
                and (day := event["exrightDate"][:10]) in by_date
                and day <= event["publicDate"][:10]] for symbol, ledger in ledgers.items()}
        for row in self._records:
            if row["exit_date"] >= first or row["episode_id"] in reserved:
                raise ValueError("Context frozen chứa ID reserve hoặc nhãn chưa maturity")
            cutoff, symbol = row["as_of_date"], row["symbol"]
            last = row["calendar_index"]
            if any(last - 20 <= i <= last and cutoff <= event["publicDate"][:10]
                   for i, event in late[symbol]):
                known, _ = visible_event_dates(ledgers[symbol], cutoff)
                features = scope.features(prices[symbol], [{"exrightDate": d} for d in known], self.calendar,
                                          cutoff, source=SOURCE)
                reasons = list(dict.fromkeys([*features["reasons"], *row["label_reasons"]]))
                row.update(features=features, reasons=reasons, status="EXCLUDED" if reasons else "AVAILABLE")

    def features(self, symbol: str, cutoff: str) -> dict:
        """Cùng feature PIT nguồn FIN06 cho target query; không nhận mặt hàng nhãn."""
        return deepcopy(self.points[symbol + "-" + cutoff]["feature"])


class FinalizedContext:
    """Tái dùng TaskBuilder, regime, student và utility đã pin; freeze theo fold."""
    def __init__(self, root: Path, data: Any, points: dict[str, dict], ledgers: dict) -> None:
        self.root, self.data, self.points, self.ledgers = root, data, points, ledgers
        self.folds: dict[str, str] = {}
        for point in points.values():
            fold, cutoff = point["fold"], point["cutoff"]
            self.folds[fold] = min(self.folds.get(fold, cutoff), cutoff)
        self._ready: dict[str, ContextBank] = {}
        self._student: StudentAdapter | None = None

    @property
    def student(self) -> StudentAdapter:
        """Nạp model frozen một lần khi thực sự chuẩn bị một context."""
        if self._student is None:
            self._student = StudentAdapter(self.root, manifest=self.root / MODEL)
        return self._student

    def fold_context(self, fold: str) -> ContextBank:
        """Mask cả 102 ID trước engine, độc lập thứ tự query trong fold."""
        if fold not in self._ready:
            first = self.folds[fold]
            events = {s: [{"exrightDate": d} for d in visible_event_dates(ledger, first)[0]]
                      for s, ledger in self.ledgers.items()}
            data = SimpleNamespace(**vars(self.data), events=events)
            context = ContextBank(data, lambda _: False, student=self.student)
            frozen = FoldStream(context.stream, first, set(self.points), self.ledgers, data.frames, data.scope, self.points)
            context.builder.view.source = frozen
            self._ready[fold] = context
        return self._ready[fold]

    def facts(self, point: dict) -> dict:
        """Fact Anchor độc lập khỏi nạp tensor/fit context, dùng facts số từ đúng giá query."""
        planned = self.points[point["id"]]
        if any(planned[k] != point[k] for k in ("symbol", "fold", "cutoff")):
            raise ValueError("Facts thuộc query khác")
        symbol, cutoff = planned["symbol"], planned["cutoff"]
        return self.data.scope.module("mt_bicl_features").make_fact_packet(self.data.frames[symbol], symbol, cutoff)

    def build(self, symbol: str, cutoff: str) -> dict:
        """Giữ prior/target theo nguyên thủy; kiểm cả tập fit centroid trước projection."""
        point = self.points[symbol + "-" + cutoff]
        fold = point["fold"]
        context = self.fold_context(fold)
        result = context.build(symbol, cutoff)
        observations = [r for task in result["prior"] for r in task["observations"]] + result["target"]
        centroid = {identifier for task in result["prior"] for identifier in task["centroid_fit_ids"]}
        expected = result["advisor"]["historical_facts"]
        if (centroid & self.points.keys() or any(r["episode_id"] in self.points or r["exit_date"] >= self.folds[fold]
                for r in observations) or any(p["as_of_date"] >= self.folds[fold] for p in expected.values())):
            raise ValueError("Context trước barrier chứa dữ liệu sau freeze hoặc ID query")
        if result["advisor"]["query_facts"] != self.facts(point):
            raise ValueError("Context và Fact Anchor khác nguồn giá PIT")
        return result

    def variants(self, episode: dict) -> dict:
        """Dùng hai forward frozen cho Full/No_target và teacher riêng cho Q10/Q90."""
        fold = self.points[episode["query"]["episode_id"]]["fold"]
        return self.fold_context(fold).variants(episode)


class FinalizedProviders:
    """Nạp đúng bản FIN06, cấp cùng snapshot cho tám vai trò trước transport."""
    def __init__(self, root: Path) -> None:
        self.root = root
        accepted = require_accepted_prices(root, profile=PROFILE)
        manifest = read(root, OUTPUT + "manifest.json", True)
        if (manifest["status"] != "PASS_OFFLINE_FIN06" or manifest["recipe"] != binding(root, RECIPE)
                or read(root, RECIPE, True) != make_recipe(root)):
            raise ValueError("Bank FIN06 chưa qua nghiệm thu hoặc sai nguồn")
        check_bindings(root, manifest["assets"])
        numeric = read(root, ASSETS + "manifest.json", True)
        check_bindings(root, [numeric["recipe"], *numeric["asset_bindings"]])
        self.rows = read(root, OUTPUT + "bank.json", True)["records"]
        keys = {p["id"]: p for p in read(root, OUTPUT + "query_keys.json", True)["records"]}
        self.points = {}
        for point in read(root, ASSETS + "query_inputs.json"):
            key = keys[point["id"]]
            if any(point[k] != key[k] for k in ("symbol", "fold", "cutoff", "price_prefix_sha256",
                                               "selector_sha256", "news_snapshot_sha256", "prior_fallback")):
                raise ValueError("Query features và khóa OHLCV khác nguồn")
            if point["regime"]["regime_name"] != key["regime"] or point["regime"]["feature_end_date"] > key["cutoff"]:
                raise ValueError("Query regime vượt cutoff hoặc khác FIN06")
            self.points[point["id"]] = {**key, "feature": point["feature"]}
        reserved = read(root, numeric["recipe"]["path"], True)["reserved_ids"]
        if len(self.points) != 102 or set(self.points) != set(keys) or set(keys) != set(reserved):
            raise ValueError("Provider không giữ đúng 102 query reserve")
        self.market = pd.read_csv(safe(root, accepted["calendar"]), parse_dates=["Datetime"])
        self.calendar = pd.DatetimeIndex(self.market.Datetime)
        self.frames, self.ledgers, self.source_hashes = {}, {}, {}
        for source in accepted["query_sources"]:
            symbol, path = source["symbol"], source["raw_csv"]
            frame = pd.read_csv(safe(root, path), parse_dates=["Datetime"])
            self.frames[symbol] = frame.loc[frame.Datetime >= source["origin"]].reset_index(drop=True)
            self.ledgers[symbol] = read(root, source["event_ledger"])["records"]
            self.source_hashes[symbol] = binding(root, path)["sha256"]
        self._selectors: dict[str, FrozenSelector] = {}
        self.selector_docs = read(root, ASSETS + "selectors.json")
        corpus = read(root, CORPUS, True)
        coverage = read(root, COVERAGE, True)
        if digest(corpus) != coverage["corpus_sha256"]:
            raise ValueError("Corpus tin không đúng bản FIN05")
        self.news = FinalizedNews(corpus["records"], evidence=corpus["evidence_registry"], root=root)
        model = read(root, MODEL, True)
        model_regimes = model["preprocessing"]["regime_models"]
        if binding(root, model_regimes["path"]) != model_regimes:
            raise ValueError("HMM MT không khớp custom model manifest")
        if model["training"]["selected_checkpoint"] != read(root, ASSETS + "regimes.json")["student_checkpoint"]:
            raise ValueError("Checkpoint MT khác FIN06")
        self.scope = StudyScope(root, source=SOURCE)
        dates = self.calendar.strftime("%Y-%m-%d").tolist()
        position = {day: i for i, day in enumerate(dates)}
        by_day = {(p["symbol"], p["cutoff"]): {"id": p["id"], "exit_date": dates[position[p["cutoff"]] + 3]}
                  for p in self.points.values()}
        data = SimpleNamespace(root=root, scope=self.scope, history=self.market, calendar=self.calendar,
                               frames=self.frames, model_manifest=model, by_day=by_day)
        self.context = FinalizedContext(root, data, self.points, self.ledgers)
        self.decision = read(root, PROTOCOL.as_posix(), True)["inference"]["config"]
        self.prior = self._prior()

    def _prior(self) -> FinalizedPrior:
        """Chỉ chuyển scaler 2022 đã fit sang cửa sổ từng fold, không gọi fit."""
        from core.price_feature_index import PriceFeatureIndex, _VERIFIED, TRAIN_END
        index = read(self.root, ASSETS + "prior_index.json", True)
        if {r["episode_id"]: (r["symbol"], r["as_of_date"], r["exit_date"]) for r in index["records"]} != {
                r["episode_id"]: (r["symbol"], r["as_of_date"], r["exit_date"]) for r in self.rows}:
            raise ValueError("Price index sai membership bank FIN06")
        scalers = index["scalers"]["oos_2023_2024"]
        bounds = {fold: (first, max(p["cutoff"] for p in self.points.values() if p["fold"] == fold))
                  for fold, first in self.context.folds.items()}
        if any(s["fit_max_exit_date"] > TRAIN_END for s in scalers.values() if s["fit_max_exit_date"] is not None):
            raise ValueError("Scaler prior fit sau cuối 2022")
        bound = {**index, "scalers": {fold: deepcopy(scalers) for fold in bounds},
                 "fold_transfer": {fold: list(span) for fold, span in bounds.items()}}

        class FoldIndex(PriceFeatureIndex):
            """Phạm vi fold được pin bởi 102 query FIN02/06."""
            def scaler(self, symbol: str, as_of_date: str, *, fold_id: str | None = None) -> dict:
                if (fold_id not in bounds or not bounds[fold_id][0] <= as_of_date <= bounds[fold_id][1]
                        or symbol not in scalers):
                    raise ValueError("Scaler khác mã/fold cutoff FIN07")
                return {**deepcopy(scalers[symbol]), "fold_id": fold_id, "index_sha256": self.identity,
                        "scaler_sha256": self._scaler_hashes[(fold_id, symbol)]}

        selector = PriceExampleSelector(FoldIndex(bound, _verified=_VERIFIED), self.calendar)
        return FinalizedPrior(self.rows, self.points, selector, {"decision": self.decision},
                              binding(self.root, OUTPUT + "bank.json")["sha256"], self.calendar)

    def bind(self, snapshot: SharedSnapshot) -> SharedSnapshot:
        """Ràng buộc shared vào đúng prefix, selector và khóa OHLCV đã nghiệm thu."""
        document = snapshot.document()
        point = self.points[document["point"]["id"]]
        symbol, cutoff = point["symbol"], point["cutoff"]
        if any(document["point"][k] != point[k] for k in ("symbol", "cutoff", "fold")):
            raise ValueError("Snapshot khác query finalize")
        frame = self.frames[symbol]
        prefix = validated_frame(raw_point_in_time_snapshot(frame, cutoff))
        if (digest(frame_document(prefix)) != point["price_prefix_sha256"]
                or key_at(prefix, self.calendar, cutoff) != point["retrieval_key"]
                or self.selector_docs[symbol]["sha256"] != point["selector_sha256"]):
            raise ValueError("Snapshot không dùng đúng prefix, khóa OHLCV hoặc selector FIN06")
        if symbol not in self._selectors:
            reserved = {p["cutoff"] for p in self.points.values() if p["symbol"] == symbol}
            self._selectors[symbol] = RawFrozenSelector(self.selector_docs[symbol], reserved)
        return bind_snapshot(snapshot, self._selectors[symbol], prefix, self.source_hashes[symbol])

    def control_snapshot(self, point: dict, *, vision: str = "BULLISH") -> SharedSnapshot:
        """Upstream giả lập riêng hai báo cáo vision, các tín hiệu khác dựng từ giá/tin thật."""
        from agents.indicator_agent import create_indicator_agent
        from utils.graph_util import TechnicalTools
        symbol, cutoff = point["symbol"], point["cutoff"]
        prefix = raw_point_in_time_snapshot(self.frames[symbol], cutoff)
        state = {"stock_name": symbol, "as_of_date": cutoff, "window_end_date": cutoff, "time_frame": "1d",
                 "language": "vi", "is_backtest": True, "messages": [], "kline_data": snapshot_payload(prefix.tail(45))}
        with redirect_stdout(io.StringIO()):
            indicator = create_indicator_agent(None, TechnicalTools())(state)["indicator_report"]
        sentiment, report = snapshot_values(self.news.snapshot(symbol, cutoff), expected_sha256=point["news_snapshot_sha256"])
        payload = {k: state[k] for k in ("stock_name", "as_of_date", "time_frame", "language", "is_backtest")}
        payload.update(pattern_report=f"Đối chứng offline\n**Thiên lệch dự báo:** {vision}",
                       trend_report=f"Đối chứng offline\n**Hướng xu hướng:** {vision}", indicator_report=indicator,
                       alpha_report="Alpha của snapshot đối chứng đang được ràng buộc.", sentiment_data=sentiment,
                       sentiment_report=report, price_prefix=frame_document(prefix.tail(600)))
        planned = {k: point[k] for k in ("id", "symbol", "cutoff", "fold")}
        planned["quality"] = "OFFLINE_CONTROL_ONLY"
        return self.bind(SharedSnapshot.create(planned, 0, payload, {"source_sha256": self.source_hashes[symbol],
            "upstream_sha256": digest(payload), "price_end": cutoff, "news_dates": []}))

    def adapters(self, point_id: str) -> tuple[Any, Any]:
        """Factory point-bound cho FIN07/FIN08, giữ schema chín mã của scope nghiên cứu."""
        from core.variant_registry import get_variant
        module = self.scope.module("unified_methods")
        point = self.points[point_id]
        provider = self

        class BoundMethods(module.MethodAdapters):
            """Khóa provenance trước request và dựng lại trace theo đúng version."""
            def bind_point(self, snapshot: SharedSnapshot) -> SharedSnapshot:
                doc = snapshot.document()
                if doc["point"]["id"] != point_id:
                    raise ValueError("Adapter nhận snapshot thuộc point khác")
                sentiment, report = snapshot_values(provider.news.snapshot(point["symbol"], point["cutoff"]),
                                                    expected_sha256=point["news_snapshot_sha256"])
                if doc["payload"]["sentiment_data"] != sentiment or doc["payload"]["sentiment_report"] != report:
                    raise ValueError("Adapter chưa dùng snapshot tin FIN05")
                return provider.bind(snapshot)

            def prepare(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int) -> dict:
                bound = self.bind_point(snapshot)
                self.verify_dependencies(variant, bound, dependencies, repeat)
                return super().prepare(variant, bound, dependencies, repeat)

            def verify_dependencies(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int) -> None:
                """Fallback/Anchor/MT chỉ dùng forecast durable cùng shared/realization/repeat."""
                if set(dependencies) != set(get_variant(variant).dependencies):
                    raise ValueError("Thiếu dependency theo registry FIN07")
                realization = snapshot.document()["realization"]
                for name, record in dependencies.items():
                    forecast = record["forecast"]
                    expected = {"variant": name, "point_id": point_id, "repeat": repeat,
                                "realization": realization, "shared_sha256": snapshot.sha256}
                    if any(forecast.get(k) != value for k, value in expected.items()):
                        raise ValueError("Dependency khác point/shared hoặc repeat")

            def validate(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int,
                         preparation: dict) -> None:
                if variant in VARIANTS:
                    if preparation != self.prepare(variant, snapshot, dependencies, repeat):
                        raise ValueError("Preparation prior khác nguồn/cổng/prompt FIN07")
                else:
                    bound = self.bind_point(snapshot)
                    self.verify_dependencies(variant, bound, dependencies, repeat)
                    module.validate_prepared(variant, bound, preparation, self.protocol["decision"], repeat)

            def resolve(self, variant: str, snapshot: SharedSnapshot, dependencies: dict, repeat: int,
                        prepared: dict, raw: dict | None) -> dict:
                """Giữ nguyên policy chuẩn sau khi xác minh dependency receipt."""
                self.verify_dependencies(variant, self.bind_point(snapshot), dependencies, repeat)
                return module.resolve(variant, prepared, raw, dependencies)

        return BoundMethods(self.decision, bank_factory=lambda: self.prior,
            regime=lambda cutoff: point["regime"] if cutoff == point["cutoff"] else None,
            facts=self.context.facts, context_factory=lambda: self.context), module
