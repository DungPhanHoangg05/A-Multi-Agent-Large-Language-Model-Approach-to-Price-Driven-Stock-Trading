"""Kiểm xuất kết quả đầy đủ U09 từ checkpoint đã chốt trong chế độ ngoại tuyến."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from core.historical_evaluation_journal import load
from core.research_results import ResearchResults
from core.unified_analysis.statistics import VARIANTS
from core.unified_execution import StageBook
from scripts.run_provider_evaluation import ROOT, checkpoint_identity, finalize, freeze, plan


class OfflineFinalizationTests(unittest.TestCase):
    """Dùng dự báo đã công bố làm fixture 102 điểm và chặn client/network."""

    def test_full_bicl_finalization_reads_all_locked_protocol_fields(self) -> None:
        """Tái lập BA/P&L, bridge, sensitivity và xuất đúng 3060 dòng."""
        source = ResearchResults(ROOT)
        source_rows = defaultdict(list)
        for row in source.table("predictions"):
            if row["method"] in VARIANTS:
                source_rows[row["point_id"]].append(row)
        study, planned, _ = plan("bicl", "luna", None)
        identity = freeze(planned, previous_finalization=True)
        with TemporaryDirectory() as folder:
            directory = Path(folder)
            book = StageBook(directory, identity)
            for point in planned["points"]:
                rows = source_rows[point["id"]]
                forecasts, prepared = [], {}
                for row in rows:
                    method, repeat = row["method"], row["repeat"]
                    slot = f"forecast/{point['id']}/u0/r{repeat}/{method}"
                    forecasts.append({
                        "forecast": {"point_id": point["id"], "variant": method, "repeat": repeat,
                                     "raw": {"source_request_id": row["source_request_id"]} if row["llm_response"] else None,
                                     "shared_sha256": row["shared_sha256"], "profile": row["profile"]},
                        "policy": {key: row[key] for key in ("raw_proposal", "final_action", "reason", "bypass")},
                    })
                    prepared[slot] = {"trace": {}, "aux": {}}
                book.execute("point/" + point["id"], {"point": point},
                             lambda _: {"records": forecasts, "prepared": prepared})

            resumed, _ = checkpoint_identity(directory, planned)
            self.assertEqual(resumed, identity)
            with patch("socket.socket.connect", side_effect=AssertionError("Finalize phải ngoại tuyến")), patch(
                    "scripts.run_provider_evaluation.ProviderHTTP", side_effect=AssertionError("Finalize không tạo client")), patch.object(
                    study, "provider", side_effect=AssertionError("Finalize không dựng provider")):
                result = finalize(directory, resumed, study)
                self.assertEqual(finalize(directory, resumed, study), result)
            self.assertEqual(len(load(directory / "predictions.json")), 3060)
            self.assertEqual(result["protocol_analysis"]["coverage"]["complete"], 2448)
            self.assertEqual(len(result["protocol_analysis"]["bridge"]), 3)
            self.assertEqual(result["protocol_analysis"]["sensitivity"]["CORE4_FIXED_SUBSET"]["points"], 48)
            self.assertEqual(result["protocol_analysis"]["telemetry"]["new_api_calls"], 0)
            for expected, observed in zip(source.result()["summary"], result["metrics"], strict=True):
                self.assertEqual(expected["method"], observed["method"])
                for key in ("balanced_accuracy_pct", "mean_account_return_pct"):
                    self.assertAlmostEqual(expected[key], observed[key])

    def test_finalization_rejects_unfinished_checkpoint(self) -> None:
        """Thiếu điểm durable thì dừng trước khi phân tích hoặc xuất tệp."""
        study, identity, _ = plan("bicl", "luna", 1)
        with TemporaryDirectory() as folder:
            directory = Path(folder)
            StageBook(directory, identity)
            with self.assertRaisesRegex(ValueError, "Thiếu stage durable"):
                finalize(directory, identity, study)
            self.assertFalse((directory / "result.json").exists())


if __name__ == "__main__":
    unittest.main()
