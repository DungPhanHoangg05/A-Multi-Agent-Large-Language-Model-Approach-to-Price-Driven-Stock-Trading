"""Kiểm biên prompt H06 và checksum bằng chứng trước khi cấp API."""

from pathlib import Path
import unittest
from unittest.mock import patch

import torch
from threadpoolctl import threadpool_limits

from core.historical_evaluation_data import HistoricalData
from scripts.prepare_historical_smoke import boundary_probe, verify_h05

ROOT = Path(__file__).resolve().parents[1]


class SmokeFreezeTests(unittest.TestCase):
    """Chỉ kiểm offline, không mở key hoặc tự tạo release."""

    def test_boundary_preserves_factors_and_hard_limits(self) -> None:
        torch.set_num_threads(1)
        data = HistoricalData(ROOT)
        with threadpool_limits(limits=1):
            result = boundary_probe(data.protocol["inference"]["config"], data.protocol["effective_mt_bicl"])
        self.assertEqual(set(result["requests"]), {"legacy_no_prior", "legacy_brpp_600", "Fact_Anchor", "MT_BICL"})
        self.assertTrue(result["brpp_601_rejected"])
        self.assertTrue(result["five_factors_preserved"])
        self.assertTrue(all(r["chars"] < 6500 for r in result["requests"].values()))

    def test_changed_h05_byte_is_rejected_before_data_loader(self) -> None:
        with patch("scripts.prepare_historical_smoke.verify_runtime"), \
                patch("scripts.prepare_historical_smoke.subprocess.check_output", return_value=b"wrong"), \
                patch("scripts.prepare_historical_smoke.HistoricalData", side_effect=AssertionError("Đã mở data")):
            with self.assertRaisesRegex(ValueError, "neo Git"):
                verify_h05(ROOT)

    def test_changed_model_hash_is_rejected(self) -> None:
        from scripts.prepare_historical_smoke import binding as actual
        def mutated(root: Path, name: str) -> dict:
            """Chỉ làm sai hash model trong phép kiểm, không sửa file thật."""
            result = actual(root, name)
            if "legacy_regimes" in name:
                result["sha256"] = "0" * 64
            return result
        with patch("scripts.prepare_historical_smoke.binding", side_effect=mutated):
            with self.assertRaisesRegex(ValueError, "H05 thay đổi"):
                verify_h05(ROOT)


if __name__ == "__main__":
    unittest.main()
