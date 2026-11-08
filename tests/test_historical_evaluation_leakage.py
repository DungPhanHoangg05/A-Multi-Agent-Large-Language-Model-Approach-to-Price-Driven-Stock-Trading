"""Kiểm cutoff history H03, không cho query outcome hoặc cycle chưa đóng vào pool."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

from core.historical_evaluation_protocol import history_before, timeline

ROOT = Path(__file__).resolve().parents[1]


class HistoricalTimelineLeakageTests(unittest.TestCase):
    """Tách ngày quyết định có thể trùng exit và entry giao dịch kế tiếp."""

    @classmethod
    def setUpClass(cls) -> None:
        """Chỉ tạo metadata ngày/ID của lịch thật."""
        cls.inputs = timeline(ROOT)

    def test_exit_equal_query_excluded(self) -> None:
        """Cycle exit đúng ngày query chưa được lấy làm prior."""
        row = self.inputs["history"][40]
        selected = history_before(self.inputs, row["symbol"], row["exit_date"])
        self.assertNotIn(row["id"], {r["id"] for r in selected})
        self.assertTrue(all(r["exit_date"] < row["exit_date"] for r in selected))

    def test_future_and_other_symbol_poison(self) -> None:
        """Thêm history tương lai/khác mã không làm đổi pool hiện tại."""
        query = self.inputs["grid"][0]
        before = history_before(self.inputs, query["symbol"], query["date"])
        poisoned = deepcopy(self.inputs)
        poisoned["history"].extend([
            {"id": "future", "symbol": query["symbol"], "date": "2098-12-20",
             "entry_date": "2098-12-21", "exit_date": "2099-01-01", "y": 1},
            {"id": "other", "symbol": "VNM" if query["symbol"] != "VNM" else "FPT",
             "date": "1999-12-20", "entry_date": "1999-12-21", "exit_date": "2000-01-01", "y": 0}])
        self.assertEqual(before, history_before(poisoned, query["symbol"], query["date"]))

    def test_history_cadence_and_final_cutoff(self) -> None:
        """Giữ600 nến warmup và mọi history cần dùng đóng trước query cuối."""
        for row in self.inputs["history"]:
            self.assertEqual((row["suffix_decision_index"] - 599) % 3, 0)
            last = max(r["date"] for r in self.inputs["grid"] if r["symbol"] == row["symbol"])
            self.assertLess(row["exit_date"], last)
            self.assertLess(row["date"], row["entry_date"])
            self.assertLess(row["entry_date"], row["exit_date"])

    def test_unknown_symbol_rejected(self) -> None:
        """Không mở universe ngầm ngoài chín mã đã đăng ký."""
        with self.assertRaises(ValueError):
            history_before(self.inputs, "UNKNOWN", "2024-01-01")
        for day in ("2024-1-1", "2024-01-01T00:00:00", "2024-01-01Z"):
            with self.assertRaises(ValueError):
                history_before(self.inputs, "FPT", day)

    def test_pool_is_a_deep_copy(self) -> None:
        """Caller sửa metadata prior không được làm biến dạng lịch dùng chung."""
        original = deepcopy(self.inputs)
        selected = history_before(self.inputs, "FPT", "2026-07-01")
        self.assertTrue(selected)
        selected[0]["date"] = "2099-01-01"
        self.assertEqual(self.inputs, original)


if __name__ == "__main__":
    unittest.main()
