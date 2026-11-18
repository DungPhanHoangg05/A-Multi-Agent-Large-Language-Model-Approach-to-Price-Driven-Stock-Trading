"""Kiểm oracle, biên ngưỡng và rào thời gian của profile OHLCV dùng chung."""
from pathlib import Path
import unittest

import pandas as pd

from core.finalize_deterministic_bank import OUTPUT, summarize
from core.finalize_ohlcv_keys import PATTERN, TREND, key_at, technical_key
from core.unified_protocol import read
from scripts.verify_finalize_ohlcv_bank import oracle

ROOT = Path(__file__).resolve().parents[1]


def window_for(closes: list[float]) -> dict:
    """Tạo nến có hình học hợp lệ cho chuỗi giá đóng độc lập với nhãn."""
    dates = pd.bdate_range("2020-01-01", periods=len(closes)).strftime("%Y-%m-%d").tolist()
    return {"Datetime": dates, "Open": closes.copy(), "Close": closes.copy(),
            "High": [p + 5. for p in closes], "Low": [p - 5. for p in closes], "Volume": [1_000.] * len(dates)}


def signal(window: dict, sessions: list[str] | None = None) -> tuple:
    """So kết quả fixture với oracle khác phép tính trên kho số thật."""
    dates = window["Datetime"] if sessions is None else sessions
    key = technical_key(window, dates[-1], dates)
    actual = key["reason"], key[PATTERN], key[TREND]
    if actual != oracle(window, dates):
        raise AssertionError("Quy tắc sản xuất khác oracle độc lập")
    return actual


class FinalizeOHLCVBankTests(unittest.TestCase):
    """Cửa sổ đồng nhất ở bank/query, khóa khác với báo cáo LLM."""

    def test_engulfing_both_directions_and_exact_half_range(self) -> None:
        bullish = window_for([100.] * 43 + [99., 102.])
        bullish["Open"][-2:] = [101., 98.]
        bullish["Low"][-1], bullish["High"][-1] = 96., 104.
        self.assertEqual(signal(bullish)[1], "BULLISH")
        bullish["High"][-1] = 104.01
        self.assertEqual(signal(bullish)[1], "NEUTRAL")
        bearish = window_for([100.] * 43 + [101., 98.])
        bearish["Open"][-2:] = [99., 102.]
        bearish["High"][-1], bearish["Low"][-1] = 104., 96.
        self.assertEqual(signal(bearish)[1], "BEARISH")

    def test_trend_confirms_both_axes_and_threshold_is_strict(self) -> None:
        self.assertEqual(signal(window_for([100.] * 35 + [110.] * 10))[2], "BULLISH")
        self.assertEqual(signal(window_for([100.] * 35 + [90.] * 10))[2], "BEARISH")
        self.assertEqual(signal(window_for([100.] * 45)), (None, "NEUTRAL", "NEUTRAL"))
        self.assertEqual(signal(window_for([100.] * 35 + [110.] * 9 + [100.5]))[2], "NEUTRAL")
        self.assertEqual(signal(window_for([100.] * 35 + [110.] * 9 + [100.501]))[2], "BULLISH")
        self.assertEqual(signal(window_for([100.] * 35 + [90.] * 9 + [99.5]))[2], "NEUTRAL")
        self.assertEqual(signal(window_for([100.] * 35 + [90.] * 9 + [99.499]))[2], "BEARISH")
        sma_boundary = [100.] * 15 + [66.5] * 20 + [67.] * 10
        self.assertEqual(signal(window_for(sma_boundary))[2], "NEUTRAL")
        sma_boundary[-1] += 0.001
        self.assertEqual(signal(window_for(sma_boundary))[2], "BULLISH")

    def test_missing_bars_or_fields_are_na_with_reason(self) -> None:
        window = window_for([100.] * 45)
        dates = window["Datetime"][:]
        short = {key: values[1:] for key, values in window.items()}
        self.assertEqual(signal(short, dates), ("INSUFFICIENT_WINDOW", None, None))
        window["Datetime"][0] = "2019-12-31"
        self.assertEqual(signal(window, dates), ("SESSION_WINDOW_MISMATCH", None, None))
        window["Datetime"] = dates[:]
        window["Volume"][-1] = float("nan")
        self.assertEqual(signal(window), ("MISSING_OHLCV", None, None))

    def test_future_suffix_and_outcomes_cannot_change_cutoff_output(self) -> None:
        window = window_for([100.] * 35 + [110.] * 10 + [150.] * 5)
        original = pd.DataFrame(window).assign(Datetime=lambda data: pd.to_datetime(data.Datetime))
        calendar = pd.DatetimeIndex(original.Datetime)
        cutoff = window["Datetime"][44]
        expected = key_at(original.iloc[:45], calendar[:45], cutoff)
        changed = original.copy()
        changed.loc[45:, ["Open", "High", "Low", "Close", "Volume"]] = float("inf")
        changed["outcome"] = 1e99
        self.assertEqual(expected, key_at(changed, calendar, cutoff))
        with self.assertRaises(ValueError):
            technical_key(window, cutoff, window["Datetime"][:45])

    def test_artifacts_keep_support_and_queries_have_no_future_labels(self) -> None:
        bank = read(ROOT, OUTPUT + "bank.json", True)
        query = read(ROOT, OUTPUT + "query_keys.json", True)
        support = summarize(bank, query)
        self.assertEqual((support["bank_records"], support["statistics_ready"], support["example_ready"]), (852, 852, 733))
        self.assertEqual((support["query_records"], support["alpha_na"], support["sentiment_na"]), (102, 119, 852))
        for row in query["records"]:
            self.assertTrue({"r_net", "y", "outcome", "exit_close"}.isdisjoint(row))
            self.assertEqual(row["retrieval_key"]["cutoff"], row["cutoff"])
        for row in bank["records"]:
            self.assertEqual(row["example_ready"], row["alpha_consensus"] is not None)


if __name__ == "__main__":
    unittest.main()
