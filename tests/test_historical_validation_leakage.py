"""Oracle kinh tế độc lập và ranh forecast trước khi primitive đọc target trong fixture."""

from datetime import date, timedelta
import json
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_scope import SYMBOLS


class HistoricalValidationTests(unittest.TestCase):
    """Giá tổng hợp bắc qua cuối tuần; không mở payoff grid nghiên cứu."""

    def fixture(self, symbol: str, exit_close: float = 100.4) -> tuple[HistoricalData, dict]:
        """Tạo query có Close(t) khác giá entry để phát hiện nhãn Close-to-Close sai."""
        data = HistoricalData.__new__(HistoricalData)
        dates = pd.to_datetime(["2025-07-04", "2025-07-07", "2025-07-08", "2025-07-09"])
        data._frames = {symbol: pd.DataFrame({"Datetime": dates, "Open": [500., 100., 101., 102.],
                                            "Close": [500., 101., 102., exit_close]})}
        unit = {"id": symbol + "_FIXTURE_ONLY", "symbol": symbol, "date": "2025-07-04",
                "entry_date": "2025-07-07", "exit_date": "2025-07-09"}
        data.by_day = {(symbol, unit["date"]): unit}
        return data, unit

    def test_nine_symbols_match_scalar_two_sided_cost_oracle(self) -> None:
        for symbol in SYMBOLS:
            data, unit = self.fixture(symbol)
            result = data.label(symbol, unit["date"], as_of="2025-07-10", forecast_done=lambda _: True)
            cash = 50_000_000.
            quantity = cash / (100. * 1.001 * 1.0025)
            final_cash = quantity * 100.4 * .999 * .9975
            self.assertAlmostEqual(result["r_net"], final_cash / cash - 1., places=14)
            self.assertLess(result["r_net"], 0.)
            self.assertEqual(result["y"], 0)
            self.assertEqual(result["entry_date"], unit["entry_date"])
            self.assertEqual(result["exit_date"], unit["exit_date"])
            self.assertIs(type(result["r_net"]), float)
            self.assertIs(type(result["y"]), int)
            json.dumps(result, allow_nan=False)

    def test_unforecast_or_exit_equal_query_never_reaches_target_helper(self) -> None:
        data, unit = self.fixture("CMG")
        with patch("core.historical_evaluation_data.compute_round_trip_net_return", side_effect=AssertionError("Đã đọc target")) as helper:
            for done, cutoff in ((False, "2025-07-10"), (np.bool_(True), "2025-07-10"), (True, unit["exit_date"])):
                with self.assertRaises(ValueError):
                    data.label("CMG", unit["date"], as_of=cutoff, forecast_done=lambda _: done)
            helper.assert_not_called()

    def test_only_t_plus_one_open_and_t_plus_three_close_determine_label(self) -> None:
        data, unit = self.fixture("CMG", 103.)
        expected = data.label("CMG", unit["date"], as_of="2025-07-10", forecast_done=lambda _: True)
        data._frames["CMG"].loc[0, ["Open", "Close"]] = 1e9
        data._frames["CMG"].loc[1, "Close"] = 1e9
        data._frames["CMG"].loc[3, "Open"] = 1e9
        self.assertEqual(expected, data.label("CMG", unit["date"], as_of="2025-07-10", forecast_done=lambda _: True))

    def test_stride_three_previous_exit_strictly_precedes_next_entry(self) -> None:
        dates = pd.bdate_range("2025-07-04", periods=13)
        for query in range(0, 7, 3):
            self.assertLess(dates[query + 3], dates[query + 4])
        data, unit = self.fixture("CMG")
        before = (date.fromisoformat(unit["exit_date"]) - timedelta(days=1)).isoformat()
        with self.assertRaises(ValueError):
            data.label("CMG", unit["date"], as_of=before, forecast_done=lambda _: True)


if __name__ == "__main__":
    unittest.main()
