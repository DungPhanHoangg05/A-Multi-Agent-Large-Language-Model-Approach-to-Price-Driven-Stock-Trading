"""Kiểm universe/PIT/label barrier và missing sentiment của adapter H04."""

from copy import deepcopy
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch

import numpy as np
import torch

from core.historical_evaluation_context import ContextBank
from core.historical_evaluation_data import HistoricalData, FrozenNews
from core.historical_evaluation_protocol import CORE4

ROOT = Path(__file__).resolve().parents[1]


class AdapterLeakageTests(unittest.TestCase):
    """Dùng source đã khóa, không fit hoặc gọi provider."""

    @classmethod
    def setUpClass(cls) -> None:
        torch.set_num_threads(1)
        cls.data = HistoricalData(ROOT)

    def test_all_nine_clean_prefix_and_bhn_suffix(self) -> None:
        for symbol, frame in self.data.frames.items():
            cutoff = next(r["date"] for r in self.data.inputs["grid"] if r["symbol"] == symbol)
            prefix = self.data.state(symbol, cutoff)
            self.assertEqual(len(prefix["kline_data"]["Close"]), 45)
            self.assertEqual(len(prefix["point_in_time_df"]), 600)
            self.assertLessEqual(str(prefix["point_in_time_df"]["Datetime"].max().date()), cutoff)
            self.assertFalse({"outcome", "supervised_target", "query_y"}.intersection(prefix))
        self.assertEqual(str(self.data.frames["BHN"]["Datetime"].iloc[0].date()), "2022-09-14")

    def test_future_price_poison_cannot_change_features_or_facts(self) -> None:
        cutoff = "2023-07-03"
        scope = self.data.scope
        frame = self.data.frames["CMG"]
        before = scope.features(frame, self.data.events["CMG"], self.data.calendar, cutoff, source=scope.source)
        facts = scope.module("mt_bicl_features").make_fact_packet(frame, "CMG", cutoff)
        frame.loc[frame["Datetime"] > cutoff, ["Open", "High", "Low", "Close"]] = float("nan")
        self.assertEqual(before, scope.features(frame, self.data.events["CMG"], self.data.calendar, cutoff, source=scope.source))
        self.assertEqual(facts, scope.module("mt_bicl_features").make_fact_packet(frame, "CMG", cutoff))

    def test_frame_and_event_copies_do_not_mutate_cache(self) -> None:
        frame = self.data.frames["CMG"]
        value = float(frame["Close"].iloc[0])
        frame.loc[0, "Close"] = -1
        self.assertEqual(float(self.data.frames["CMG"]["Close"].iloc[0]), value)
        events = self.data.events
        events["CMG"].append({"exrightDate": "2099-01-01"})
        self.assertNotIn({"exrightDate": "2099-01-01"}, self.data.events["CMG"])

    def test_query_label_before_forecast_or_at_exit_is_rejected(self) -> None:
        unit = self.data.inputs["grid"][0]
        with self.assertRaises(ValueError):
            self.data.label(unit["symbol"], unit["date"], as_of="2026-09-30", forecast_done=lambda _: False)
        with self.assertRaises(ValueError):
            self.data.label(unit["symbol"], unit["date"], as_of=unit["exit_date"], forecast_done=lambda _: True)
        value = self.data.label(unit["symbol"], unit["date"], as_of="2026-09-30", forecast_done=lambda _: True)
        self.assertEqual(value["y"], int(value["r_net"] > 0))
        with self.assertRaises(ValueError):
            self.data.label(unit["symbol"], "2023-7-3", as_of="2026-09-30", forecast_done=lambda _: True)

    def test_gated_stream_does_not_compute_unforecast_query_labels(self) -> None:
        bank = ContextBank(self.data, lambda _: False)
        query = "2023-10-02"
        with patch("core.mt_bicl_scaler.fit_scaler", side_effect=AssertionError("Không fit lại")):
            episode = bank.build("CMG", query)
        reserved = set(bank.stream.audit[-1]["withheld_forecast_ids"])
        self.assertTrue(reserved)
        self.assertFalse(reserved.intersection({r["episode_id"] for r in bank.stream.closed_records()}))
        self.assertEqual(episode["query"]["symbol"], "CMG")
        poison = deepcopy(episode)
        poison["query"]["y"] = 1
        with self.assertRaises(ValueError):
            bank.predict(poison)

    def test_extended_wire_keeps_real_ood_id_and_old_validator_unchanged(self) -> None:
        from core.mt_bicl_contracts import validate_fact_packet
        frame = self.data.frames["CMG"]
        packet = self.data.scope.module("mt_bicl_features").make_fact_packet(frame, "CMG", "2023-07-03")
        self.assertEqual(packet["point_id"], "CMG-2023-07-03")
        with self.assertRaises(ValueError):
            validate_fact_packet(packet)

    def test_news_missing_future_unknown_and_same_day_not_used(self) -> None:
        def article(day: str | None, score: float = .5) -> dict:
            return {"date_parsed": day, "numeric_score": score, "scorer": "visobert"}
        news = FrozenNews({"CMG": [article(None), article("2023-07-03"), article("2099-01-01"),
                                   article("2023-07-01"), article("2023-07-01", -.5)]})
        data, report = news.get_sentiment_at("CMG", "2023-07-03")
        self.assertEqual(data["verified_article_count"], 2)
        self.assertTrue(data["is_unavailable"])
        self.assertIsNone(data["main_sentiment"]["avg_score"])
        self.assertEqual(news.get_sentiment_at("CMG", "2023-07-04")[0]["verified_article_count"], 3)

    def test_all_grid_sentiment_masks_keep_two_layers(self) -> None:
        rows = self.data.sentiment_audit()
        self.assertEqual(len(rows), 1020)
        self.assertTrue(all((r["verified_score"] is None) == r["missing"] for r in rows))
        self.assertTrue(all(not r["downstream_reliable"] or r["verified_count"] >= 8 for r in rows))
        self.assertGreater(sum(not r["missing"] for r in rows), sum(r["downstream_reliable"] for r in rows))

    def test_missing_historical_models_stop_before_collection_and_query_never_refits(self) -> None:
        """Không chi API rồi mới phát hiện thiếu492 prefix hoặc tự fit model query."""
        from core.historical_evaluation_runner import Regimes
        with tempfile.TemporaryDirectory() as folder, \
                patch("core.regime_detector.MarketRegimeDetector.fit", side_effect=AssertionError("Không refit")):
            regimes = Regimes(self.data, Path(folder))
            with self.assertRaisesRegex(ValueError, "prepare-regimes"):
                regimes.preflight()
            self.assertIn(regimes.get("2023-07-03"), ("BULL", "BEAR", "CHOPPY", "CONSOLIDATION"))


    def test_core4_context_is_unchanged_after_ood_phase_becomes_durable(self) -> None:
        """Cold replay CORE4 không hấp thụ query-y OOD hoàn tất trong phase sau."""
        from core.historical_evaluation_runner import HistoricalRunner
        from core.historical_evaluation_context import ContextBank
        from core.historical_evaluation_protocol import CORE4
        runner = HistoricalRunner.__new__(HistoricalRunner)
        runner.data, runner.phase, runner.fixture = self.data, None, True
        runner.select_phase("CORE4")
        runner.forecasts_done = lambda identifier: self.data.grid[identifier]["symbol"] in CORE4
        before = ContextBank(self.data, runner.numeric_forecasts_done).build("FPT", "2025-07-01")
        runner.forecasts_done = lambda identifier: True
        after = ContextBank(self.data, runner.numeric_forecasts_done).build("FPT", "2025-07-01")
        self.assertEqual(before, after)
        ood = next(r["id"] for r in self.data.inputs["grid"] if r["symbol"] == "CMG")
        self.assertFalse(runner.numeric_forecasts_done(ood))
        with self.assertRaises(ValueError):
            runner.select_phase("OOD5")
        runner.phase = None
        runner.select_phase("OOD5")
        self.assertTrue(runner.numeric_forecasts_done(ood))

    def test_ood_phase_requires_complete_core4_before_collection(self) -> None:
        """Run thật không được thu OOD sớm rồi thay membership sau khi CORE4 hoàn tất."""
        from core.historical_evaluation_runner import HistoricalRunner
        runner = HistoricalRunner.__new__(HistoricalRunner)
        runner.data, runner.phase, runner.fixture = self.data, None, False
        runner.forecasts_done = lambda identifier: False
        with self.assertRaises(ValueError):
            runner.select_phase("OOD5")
        self.assertIsNone(runner.phase)
        runner.forecasts_done = lambda identifier: True
        runner.select_phase("OOD5")
        self.assertEqual(runner.phase, "OOD5")


if __name__ == "__main__":
    unittest.main()
