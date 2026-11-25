"""Kiểm nguồn Groq đã công bố và xuất báo cáo ghép cặp ngoại tuyến."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from core.finalize_serving_resources import FinalizedResources
from core.historical_evaluation_journal import save
from core.unified_contracts import digest
from scripts.compare_luna_with_archived_groq import bicl_archive, component_archive, export_archived
from scripts.fin12_evaluation import execution_outcomes
from scripts.run_provider_evaluation import ROOT, plan


class ArchivedGroqTests(unittest.TestCase):
    """Đọc hiện vật thật và kết quả Luna giả lập, chặn mọi kết nối mạng."""

    def setUp(self) -> None:
        network = patch("socket.socket.connect", side_effect=AssertionError("Báo cáo phải chạy ngoại tuyến"))
        network.start()
        self.addCleanup(network.stop)

    def test_full_archive_cohorts_match_registered_outcomes(self) -> None:
        """Kiểm đủ ba lưới dự báo và hash outcome FIN12 tính lại."""
        study, identity, _ = plan("component", "luna", None)
        result, rows = component_archive(study, identity["points"])
        self.assertEqual(Counter(row["panel"] for row in rows), {"main": 918, "upstream": 54, "factorial": 135})
        self.assertEqual(result["usage"]["observed_total_tokens"], 1_404_064)
        for name in ("bicl", "followup"):
            with self.subTest(study=name):
                study, identity, _ = plan(name, "luna", None)
                result, rows = bicl_archive(study, identity["points"], sample=False)
                keys = {(row["point_id"], row["method"], row["repeat"]) for row in rows}
                self.assertEqual(len(keys), len(rows))
                self.assertEqual(Counter(row["point_id"] for row in rows), {p["id"]: 30 for p in study.points})
                self.assertEqual(len(result["metrics"]), 10)
                if name == "followup":
                    canonical, _, _ = execution_outcomes(study.points, FinalizedResources(ROOT))
                    self.assertEqual(result["outcome_sha256"], digest(canonical))

    def test_report_reads_only_luna_run_and_keeps_archive_cost_unknown(self) -> None:
        """Đối chiếu từng hành động và xuất báo cáo khi thư mục Groq mới không tồn tại."""
        study, identity, _ = plan("bicl", "luna", 1)
        metrics, rows = bicl_archive(study, identity["points"], sample=True)
        luna_rows = deepcopy(rows)
        original = next(row for row in luna_rows if row["method"] == "original_fix")
        original["final_action"] = "LONG" if original["final_action"] == "CASH" else "CASH"
        with TemporaryDirectory() as folder:
            output = Path(folder)
            base = output / "v1" / "bicl" / "sample-1"
            directory = base / "luna"
            save(directory / "predictions.json", luna_rows)
            save(directory / "result.json", {**metrics, "identity": identity, "predictions_sha256": digest(luna_rows),
                                            "usage": {"estimated_cost_usd": 0.001}})
            result = export_archived("bicl", "v1", 1, output=output)
            self.assertFalse(result["api"])
            self.assertFalse((base / "groq").exists())
            self.assertTrue(Path(result["comparison"]).is_file())
            exported = json.loads((base / "luna_vs_archived_groq.json").read_bytes())
            self.assertEqual(result["metrics"], exported["comparison"])
            slot = next(row for row in exported["comparison"] if row["method"] == "original_fix")
            self.assertEqual(slot["groq_cash_to_luna_long"] + slot["groq_long_to_luna_cash"], 1)
            self.assertIsNone(exported["usage"]["groq"]["estimated_cost_usd"])
            save(directory / "predictions.json", [])
            with self.assertRaisesRegex(ValueError, "checksum"):
                export_archived("bicl", "v1", 1, output=output)


if __name__ == "__main__":
    unittest.main()
