"""Oracle scalar độc lập cho bootstrap paired/max-deviation và null support."""

from __future__ import annotations

import json
import math
import statistics
import unittest

import numpy as np

from core.historical_evaluation_statistics import primary_interval


def values_from_blocks(blocks: list[list[float]]) -> list:
    """Nhân mỗi block thành bốn mã và ba repeat để tạo input đủ support."""
    return [[[list(row) for _ in range(3)] for _ in range(4)] for row in blocks]


class HistoricalStatisticsTests(unittest.TestCase):
    """Các family giữ cùng draw indices và không loại contrast bất lợi/null."""

    def test_centered_scalar_oracle_and_shared_draws(self) -> None:
        """Tính trực tiếp từng draw rồi nội suy quantile bằng scalar độc lập."""
        blocks = [[float(b - 2), float(2 * b + 100), float(-b), 7., 0.] for b in range(6)]
        actual = primary_interval(values_from_blocks(blocks))
        point = [statistics.mean(row[j] for row in blocks) for j in range(5)]
        indices = np.random.Generator(np.random.PCG64(20261107)).integers(0, 6, size=(10000, 6))
        maxima = sorted(max(abs(statistics.mean(blocks[int(b)][j] for b in draw) - point[j])
                            for j in range(5)) for draw in indices)
        index = .95 * (len(maxima) - 1)
        lower = math.floor(index)
        width = maxima[lower] + (index - lower) * (maxima[lower + 1] - maxima[lower])
        self.assertEqual(actual["point"], point)
        self.assertAlmostEqual(actual["half_width"], width, places=12)
        self.assertEqual(len(actual["ci"]), 5)
        json.dumps(actual, allow_nan=False)

    def test_constant_and_null_contrasts(self) -> None:
        """Family constant có width0; thiếu support không được giảm family xuống4."""
        values = values_from_blocks([[100., -3., 0., 7., 2.]] * 6)
        actual = primary_interval(values)
        self.assertEqual(actual["half_width"], 0.)
        self.assertTrue(all(low == high for low, high in actual["ci"]))
        values[2][1][0][4] = None
        missing = primary_interval(values)
        self.assertEqual(missing["status"], "INCONCLUSIVE_UNDEFINED_SUPPORT")
        self.assertIsNone(missing["ci"])
        self.assertEqual(missing["draws"], 0)

    def test_ba_family_separate_precision_same_draws(self) -> None:
        """BA dùng ngưỡng3 đpt, return1 đpt; giữ cùng width và point."""
        values = values_from_blocks([[float(b)] * 5 for b in (-3, -2, -1, 1, 2, 3)])
        returns = primary_interval(values)
        ba = primary_interval(values, metric="balanced_accuracy")
        self.assertEqual(returns["status"], "LOW_PRECISION")
        self.assertEqual(ba["status"], "PASS")
        self.assertEqual(returns["half_width"], ba["half_width"])

    def test_reject_incomplete_nonfinite_or_boolean_input(self) -> None:
        """Không đếm repeat như block và không biến NaN/boolean thành metric."""
        with self.assertRaises(ValueError):
            primary_interval(np.zeros((5, 4, 3, 5)).tolist())
        for poison in (float("nan"), float("inf"), True):
            values = values_from_blocks([[0.] * 5 for _ in range(6)])
            values[0][0][0][0] = poison
            with self.assertRaises(ValueError):
                primary_interval(values)


if __name__ == "__main__":
    unittest.main()
