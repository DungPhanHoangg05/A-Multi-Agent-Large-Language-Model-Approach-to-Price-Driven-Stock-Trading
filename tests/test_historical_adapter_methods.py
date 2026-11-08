"""Parity CORE4, scaler train-only, prefix/gate và numeric CRN của adapter riêng."""

from copy import deepcopy
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
import torch

from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_graph import factor_lines, require_factors
from core.historical_evaluation_prior import FeaturePopulation
from core.historical_evaluation_protocol import CORE4
from core.historical_evaluation_scope import AlgorithmScope
from core.mt_bicl_bank import SOURCE
from core.mt_bicl_protocol import component_seed, PROTOCOL_SHA256
from core.pit_price_features import extract_pit_price_features

ROOT = Path(__file__).resolve().parents[1]


class MethodAdapterTests(unittest.TestCase):
    """Giữ thuật toán gốc và mở scope tường minh; không thay globals đang dùng."""

    @classmethod
    def setUpClass(cls) -> None:
        torch.set_num_threads(1)
        cls.data = HistoricalData(ROOT)
        cls.population = FeaturePopulation(cls.data)

    def test_feature_parity_core4_on_controlled_reference_fixture(self) -> None:
        scope = AlgorithmScope(ROOT, symbols=CORE4, source=SOURCE)
        for symbol in CORE4:
            frame = self.data.frames[symbol]
            # Reference giả chỉ thuộc fixture đối chiếu, không xuất vào nguồn production.
            frame["Reference"] = frame["Close"].shift().fillna(frame["Close"].iloc[0])
            cutoff = "2023-07-03"
            events = self.data.events[symbol]
            original = extract_pit_price_features(frame, events, self.data.calendar, cutoff, source=SOURCE)
            adapted = scope.features(frame, events, self.data.calendar, cutoff, source=SOURCE)
            self.assertEqual(original["status"], adapted["status"])
            self.assertEqual(original["coverage"], adapted["coverage"])
            np.testing.assert_allclose(original["vector"], adapted["vector"], rtol=0, atol=1e-12)

    def test_crn_byte_parity_core4_and_distinct_extended_ids(self) -> None:
        scope = self.data.scope
        for component in ("lambda", "theta", "magnitude|FPT-2023-01-06"):
            self.assertEqual(component_seed(PROTOCOL_SHA256, "FPT-2023-07-03", component),
                             scope.component_seed(PROTOCOL_SHA256, "FPT-2023-07-03", component))
        self.assertNotEqual(scope.component_seed(PROTOCOL_SHA256, "CMG-2023-07-03", "lambda"),
                            scope.component_seed(PROTOCOL_SHA256, "FPT-2023-07-03", "lambda"))
        with self.assertRaises(ValueError):
            scope.component_seed(PROTOCOL_SHA256, "BAD-2023-07-03", "lambda")

    def test_scope_does_not_mutate_original_universe_or_schema(self) -> None:
        from core.mt_bicl_bank import SYMBOLS
        from core.mt_bicl_contracts import wire_schema
        original = deepcopy(wire_schema())
        self.data.scope.module("mt_bicl_context")
        self.data.scope.module("improvement_prior")
        self.assertEqual(tuple(SYMBOLS), CORE4)
        self.assertEqual(original, wire_schema())
        self.assertEqual(original["$defs"]["reply"], self.data.scope.module("mt_bicl_contracts").wire_schema()["$defs"]["reply"])

    def test_scaler_exact_train_ids_and_no_validation_fit(self) -> None:
        for scope in self.data.inputs["scopes"]:
            symbol, fold = scope["symbol"], scope["fold"]
            scaler = self.population.scalers[fold][symbol]
            days = self.data.frames[symbol]["Datetime"].dt.strftime("%Y-%m-%d").to_numpy()
            allowed = {symbol + ":" + str(days[i]) for i in scope["train"]}
            self.assertTrue(set(scaler["fit_episode_ids"]) <= allowed)
            self.assertLessEqual(scaler["fit_max_exit_date"], scope["train_max_exit"])
            self.assertLess(scaler["fit_max_exit_date"], scope["first_validation_date"])

    def test_task_and_bucket_parity_core4(self) -> None:
        from mt_bicl_tasks_support import setup, FakeDetector
        from core.mt_bicl_features import BucketTaskBuilder
        from core.mt_bicl_stream import MarketStream
        from core.mt_bicl_regimes import RegimeTimeline
        bank, sources, history = setup()
        calendar = pd.DatetimeIndex(history["Datetime"])
        cutoff = str(calendar[995].date())
        original = BucketTaskBuilder(bank, MarketStream(bank, sources, calendar),
            RegimeTimeline(history, detector_factory=FakeDetector), {s: f for s, (f, _) in sources.items()}).build("FPT", cutoff)
        scope = AlgorithmScope(ROOT, symbols=CORE4, source=SOURCE)
        adapted = scope.module("mt_bicl_features").BucketTaskBuilder(bank,
            scope.module("mt_bicl_stream").MarketStream(bank, sources, calendar),
            RegimeTimeline(history, detector_factory=FakeDetector), {s: f for s, (f, _) in sources.items()}).build("FPT", cutoff)
        self.assertEqual(original, adapted)

    def test_all_five_factor_rows_survive_final_prompt(self) -> None:
        from core.mt_bicl_prompt import canonical_request
        factors = [{"id": i, "name": "Factor" + str(i), "value": i * .1, "signal": "TĂNG"} for i in range(1, 6)]
        shared = {"stock_name": "CMG", "as_of_date": "2023-07-03", "time_frame": "1d", "is_backtest": True,
                  "language": "vi", **{name + "_report": "Báo cáo kiểm thử." for name in ("indicator", "pattern", "trend", "sentiment")},
                  "alpha_report": "Alpha số PIT:\n" + "\n".join(factor_lines(factors))}
        request = canonical_request(shared, "", {"decision": self.data.protocol["inference"]["config"]})
        require_factors(request["messages"][0]["content"], factors)
        with self.assertRaises(ValueError):
            require_factors(request["messages"][0]["content"].replace("Factor5", "MẤT"), factors)

    def test_empty_bank_gate_fallback_uses_valid_index_calendar(self) -> None:
        """Calendar hash phải dùng đúng ABI index, không đổi serializer để né guard."""
        factors = [{"id": i, "name": "Factor" + str(i), "value": .1, "signal": "TĂNG"} for i in range(1, 6)]
        shared = {"stock_name": "CMG", "as_of_date": "2023-07-03", "time_frame": "1d", "is_backtest": True,
                  "language": "vi", "alpha_factors": factors, "sentiment_data": {"main_sentiment": {"avg_score": None}},
                  "trend_report": "**Hướng xu hướng:** BULLISH", "pattern_report": "**Thiên lệch dự báo:** BULLISH",
                  "indicator_report": "**Đồng thuận chủ đạo:** BULLISH",
                  "sentiment_report": "Sentiment thiếu tin.", "alpha_report": "\n".join(factor_lines(factors))}
        for branch in ("C2", "A_tp_pool", "B_semantic"):
            request, proof = self.population.request(branch, shared, "BULL", [], 0)
            self.assertTrue(proof["fallback"])
            require_factors(request["messages"][0]["content"], factors)

    def test_utility_projection_parity_and_ood_schema_guards(self) -> None:
        """Giữ raw4096 draws trên CORE4; OOD chỉ mở ID, không bỏ validator numeric/PIT."""
        from mt_bicl_support import episode
        from core.mt_bicl_context import prepare_variants
        from core.mt_bicl_teacher import BetaBernoulliTeacher
        from core.mt_bicl_bank import content_hash
        context = episode()
        teacher = BetaBernoulliTeacher([1. / 16] * 16)
        adapted = self.data.scope.module("mt_bicl_context")
        self.assertEqual(prepare_variants(context, teacher, lambda _: .6), adapted.prepare_variants(context, teacher, lambda _: .6))
        def renamed(value: object) -> object:
            """Chỉ đổi ID/mã của dữ liệu synthetic, scaler vẫn giữ provenance CORE4."""
            if isinstance(value, str):
                return value.replace("FPT", "CMG")
            if isinstance(value, list):
                return [renamed(v) for v in value]
            if isinstance(value, dict):
                return {renamed(k): deepcopy(v) if k == "scaler" else renamed(v) for k, v in value.items()}
            return value
        extended = renamed(context)
        contracts = self.data.scope.module("mt_bicl_contracts")
        extended["membership_sha256"] = contracts.membership_hash(extended)
        variants = adapted.prepare_variants(extended, teacher, lambda _: .6)
        self.assertTrue(variants["branches"]["MT_BICL"]["eligible"])
        self.assertTrue(variants["branches"]["MT_BICL"]["point_id"].startswith("CMG-"))
        poisoned = deepcopy(extended)
        poisoned["advisor"]["query_facts"]["assertions"]["MACD_SIGNAL"] = "BELOW"
        poisoned["membership_sha256"] = contracts.membership_hash(poisoned)
        with self.assertRaises(ValueError):
            contracts.validate_context(poisoned)

    def test_real_donor_renderer_keeps_auxiliary_files_outside_workspace(self) -> None:
        """Dùng renderer thật để bắt lệch chữ ký mà pixel fixture không kiểm được."""
        import base64
        import io
        from PIL import Image
        from core.historical_evaluation_graph import GraphProvider
        names = ("record.csv", "kline_chart.png", "trend_graph.png")
        before = {name: (ROOT / name).read_bytes() if (ROOT / name).exists() else None for name in names}
        graph = GraphProvider(self.data, None)
        state = self.data.state("CMG", "2023-07-03")
        for name in ("pattern", "trend"):
            output = graph.render(name, state["kline_data"])
            image = Image.open(io.BytesIO(base64.b64decode(output[name + "_image"], validate=True)))
            self.assertEqual(image.format, "PNG")
            self.assertGreater(image.width, 1000)
            self.assertGreater(image.height, 500)
            self.assertEqual(Path.cwd(), ROOT)
        after = {name: (ROOT / name).read_bytes() if (ROOT / name).exists() else None for name in names}
        self.assertEqual(before, after)

    def test_v1_keeps_verified_sentiment_without_changing_four_signal_prefix(self) -> None:
        """Mở flag formatter có sẵn, giữ nguyên record tin và byte template T/P/A/I."""
        source = next(r for r in self.data.inputs["history"] if r["symbol"] == "CMG")
        label = self.data.label("CMG", source["date"], as_of="2023-07-03", forecast_done=lambda _: False)
        current = {"trend": "BULLISH", "pattern": "BULLISH", "alpha_consensus": "BULLISH",
                   "indicator_consensus": "BULLISH", "sentiment": "POSITIVE"}
        record = {"episode_id": source["id"], "symbol": "CMG", "as_of_date": source["date"],
            "entry_date": label["entry_date"], "exit_date": label["exit_date"], "regime": "BULL", "agent_signals": current,
            "outcome": {"actual_direction": "UP" if label["y"] else "DOWN", "net_return_pct": label["r_net"] * 100.,
                        "result": "WIN_IF_LONG" if label["y"] else "LOSS_IF_LONG", "was_bull_trap": not bool(label["y"])}}
        factors = [{"id": i, "name": f"Factor{i}", "value": .1, "signal": "TĂNG"} for i in range(1, 6)]
        shared = {"stock_name": "CMG", "as_of_date": "2023-07-03", "time_frame": "1d", "is_backtest": True,
            "language": "vi", "alpha_factors": factors, "sentiment_data": {"main_sentiment": {"avg_score": .5}},
            "trend_report": "**Hướng xu hướng:** BULLISH", "pattern_report": "**Thiên lệch dự báo:** BULLISH",
            "indicator_report": "**Đồng thuận chủ đạo:** BULLISH", "sentiment_report": "Tin tích cực.",
            "alpha_report": "\n".join(factor_lines(factors))}
        request, proof = self.population.request("bayesian_v1", shared, "BULL", [record], 0)
        self.assertEqual(record["agent_signals"]["sentiment"], "POSITIVE")
        old_rows = deepcopy(proof["retrieval"]["tasks"])
        for row in old_rows:
            row["agent_signals"]["sentiment"] = "NEUTRAL"
        old = self.data.scope.module("bayesian_retriever").format_compact_prior_prefix(old_rows, proof["retrieval"]["stats"])
        self.assertIn(old, request["messages"][0]["content"])


if __name__ == "__main__":
    unittest.main()
