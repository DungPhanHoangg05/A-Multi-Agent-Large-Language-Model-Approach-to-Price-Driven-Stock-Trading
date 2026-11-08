"""Hồi quy paired fixture qua đủ primary/anchor/ablation/control và cold resume."""

from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import torch
from threadpoolctl import threadpool_limits

from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_runner import HistoricalRunner, FixtureClients, branches, forecast_slot

ROOT = Path(__file__).resolve().parents[1]


class CountClients(FixtureClients):
    """Chỉ đếm execution mô phỏng, không đại diện API/provider thực."""

    def __init__(self) -> None:
        self.graph_calls: list[tuple[str, str]] = []
        self.decisions: list[str] = []

    def stage(self, role: str, attempt: str, point: str, node: object, state: dict) -> dict:
        self.graph_calls.append((point, role))
        return super().stage(role, attempt, point, node, state)

    def decision(self, org: int, request: dict, attempt: str, branch: str) -> dict:
        self.decisions.append(branch)
        return super().decision(org, request, attempt, branch)


class RunnerTests(unittest.TestCase):
    """Gọi một anchor OOD thật về ngày/giá, mọi response LLM vẫn là fixture cách ly."""

    @classmethod
    def setUpClass(cls) -> None:
        torch.set_num_threads(1)
        cls.data = HistoricalData(ROOT)

    def test_dependency_order_and_exact_matrix_count(self) -> None:
        total = 0
        for unit in self.data.inputs["grid"]:
            realizations = [0, 1, 2] if unit["id"] in self.data.inputs["panel_ids"] else [0]
            for realization in realizations:
                for repeat in range(3):
                    names = branches(self.data, unit, realization, repeat)
                    self.assertEqual(names[:2], ["Original_common", "Fact_Anchor"])
                    self.assertEqual(len(names), len(set(names)))
                    total += len(names)
        self.assertEqual(total, 27846)

    def test_anchor_ood_paired_resume_and_label_barrier(self) -> None:
        clients = CountClients()
        original_book = RunBook
        with tempfile.TemporaryDirectory() as folder, threadpool_limits(limits=1):
            def book(directory: Path, identity: dict, *, verify_only: bool = False) -> RunBook:
                """Quarantine fixture hoàn toàn trong thư mục test tạm."""
                return original_book(Path(folder), identity, verify_only=verify_only)
            with patch("core.historical_evaluation_runner.runtime_identity", return_value={"fixture": True}), \
                    patch("core.historical_evaluation_runner.RunBook", side_effect=book):
                runner = HistoricalRunner(self.data, fixture=True, clients=clients)
                unit = next(r for r in self.data.inputs["grid"] if r["symbol"] == "CMG")
                self.assertFalse(runner.forecasts_done(unit["id"]))
                with redirect_stdout(io.StringIO()):
                    runner.unit(unit)
                self.assertTrue(runner.forecasts_done(unit["id"]))
                self.assertTrue(runner.book.complete("label/" + unit["id"]))
                for point, role in clients.graph_calls:
                    self.assertEqual(clients.graph_calls.count((point, role)), 1)
                count = len(clients.graph_calls), len(clients.decisions)
                with redirect_stdout(io.StringIO()):
                    resumed = HistoricalRunner(self.data, fixture=True, verify_only=True, clients=clients)
                    resumed.unit(unit)
                self.assertEqual(count, (len(clients.graph_calls), len(clients.decisions)))
                # Mọi response đều mang fixture marker, không thể coi là kết quả nghiên cứu.
                for path in (Path(folder) / "slots").glob("*.json"):
                    doc = load(path)
                    if doc["slot"].startswith("forecast/"):
                        output = doc["attempts"][-1]["output"]
                        if output["llm"] is not None:
                            self.assertTrue(output["llm"]["fixture"])
                original_slot = forecast_slot(unit["id"], 0, 0, "Original_common")
                doc = load(runner.book.path(original_slot))
                doc["attempts"][-1]["output"]["final_action"] = "LONG"
                from core.historical_evaluation_protocol import digest
                doc["attempts"][-1]["output_sha256"] = digest(doc["attempts"][-1]["output"])
                save(runner.book.path(original_slot), doc)
                with redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
                    checker = HistoricalRunner(self.data, fixture=True, verify_only=True, clients=clients)
                    checker.unit(unit)


if __name__ == "__main__":
    unittest.main()
