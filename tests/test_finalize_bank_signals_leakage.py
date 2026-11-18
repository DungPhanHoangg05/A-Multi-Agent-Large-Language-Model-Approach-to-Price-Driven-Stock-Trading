"""Kiểm rào thời gian và body request của producer tín hiệu FIN06."""
from __future__ import annotations

from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np

from causal_profile_support import source_frame
from core.causal_alpha import alpha_values
from core.finalize_bank_resources import CONTRACT
from core.finalize_bank_signals import alpha_signal, point_input, vision_probe
from core.unified_protocol import read


class FinalizeBankSignalsLeakageTests(unittest.TestCase):
    """Không gửi dữ liệu sau cutoff hoặc nhãn vào node thị giác."""

    def test_chart_and_prefix_ignore_future_quotes_and_all_outcome_columns(self) -> None:
        frame = source_frame()
        frame["Volume"] = frame.Volume.round()
        cutoff = frame.Datetime.iloc[599].date().isoformat()
        before, state = point_input("FPT", cutoff, frame)
        poison = frame.copy()
        poison["r_net"] = 99.
        poison.loc[600:, ["Open", "High", "Low", "Close", "Volume"]] = np.nan
        after, changed = point_input("FPT", cutoff, poison)
        self.assertTrue(before.equals(after))
        self.assertEqual(state, changed)
        self.assertEqual(state["kline_data"]["Datetime"][-1], cutoff)
        self.assertEqual(len(state["kline_data"]["Datetime"]), 45)
        self.assertNotIn("r_net", state["kline_data"])

    def test_early_episode_never_uses_later_selector(self) -> None:
        model = {"payload": {"schedule": {"test_start": "2020-10-01", "test_end": "2022-12-27"},
                             "fit_end": "2020-09-30"}}
        with patch("core.finalize_bank_signals.alpha_values", side_effect=AssertionError("Không được tính Alpha")):
            result = alpha_signal(source_frame(), "2020-06-01", model)
            self.assertIsNone(result["value"])
            self.assertEqual(result["reason"], "BEFORE_HISTORICAL_SELECTOR_SUPPORT")
            with self.assertRaises(ValueError):
                alpha_signal(source_frame(), "2020-10-01", model)

    def test_real_nodes_build_vision_requests_without_generating_a_response(self) -> None:
        root = Path(__file__).resolve().parents[1]
        frame = source_frame()
        frame["Volume"] = frame.Volume.round()
        cutoff = frame.Datetime.iloc[599].date().isoformat()
        _, state = point_input("FPT", cutoff, frame)
        config = read(root, CONTRACT, True)["model_options"]["candidate"]
        result = vision_probe(root, state, config)
        self.assertEqual(set(result["requests"]), {"pattern", "trend"})
        for body in result["requests"].values():
            self.assertEqual(body["model"], config["signal_config"]["models"]["graph_llm_model"])
            self.assertEqual(len(body["request_sha256"]), 64)
            self.assertGreaterEqual(body["message_count"], 1)

    def test_vectorized_alpha_projection_matches_real_prefix(self) -> None:
        frame = source_frame()
        cutoff = frame.Datetime.iloc[640].date().isoformat()
        prefix = frame.iloc[:641]
        expected = alpha_values(prefix).iloc[-1]
        frame.loc[641:, ["Open", "High", "Low", "Close"]] *= 10_000.
        batch_row = alpha_values(frame).iloc[640]
        np.testing.assert_allclose(batch_row.to_numpy(), expected.to_numpy(), atol=1e-12, equal_nan=True)
        identifiers = expected.dropna().index[:5]
        model = {"sha256": "fixture", "payload": {
            "schedule": {"test_start": cutoff, "test_end": cutoff}, "fit_end": frame.Datetime.iloc[639].date().isoformat(),
            "threshold": .1, "selected": [{"alpha_id": key, "orientation": 1} for key in identifiers]}}
        actual = alpha_signal(prefix, cutoff, model, factor_row=batch_row.rename(cutoff))
        original = alpha_signal(prefix, cutoff, model)
        self.assertEqual(actual["value"], original["value"])
        np.testing.assert_allclose([x["value"] for x in actual["factors"]],
                                   [x["value"] for x in original["factors"]], atol=1e-12)
        with self.assertRaises(ValueError):
            alpha_signal(prefix, cutoff, model, factor_row=batch_row)


if __name__ == "__main__":
    unittest.main()
