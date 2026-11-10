"""Kiểm runner hosted trên prepared fixture U06; không inference hoặc nhãn thị trường mới."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
from test_unified_execution_leakage import ControlMethods
from scripts.check_unified_execution import control_response
from core.historical_evaluation_journal import load, save
from core.historical_evaluation_protocol import digest as stage_digest
from core.unified_execution import StageBook
from core.unified_execution_transport import MockHTTP, wire_state
from core.unified_live.transport import LiveCalls, carry_smoke
from core.unified_live.execution import HostedRunner, verify
from core.unified_live.release import NAMESPACES
from core.unified_protocol import read
from core.unified_preflight import ASSETS
from core.unified_experiment import outcome_from_frame


class HostedExecutionTests(unittest.TestCase):
    """Cùng ABI phương pháp thực, response kiểm soát và oracle synthetic tách khỏi giá cohort."""
    @classmethod
    def setUpClass(cls) -> None:
        manifest = read(ROOT, ASSETS + "/provider_manifest.json")
        cls.records = [read(ROOT, row["path"]) for row in manifest["points"]]

    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.now = [2000000000.]

    def setup(self, phase: str, records: list[dict], *, all_points: bool = False) -> tuple:
        """Tạo test identity riêng, không thể được LiveHTTP nhận làm quyền thực."""
        points = [r["point"] for r in (self.records if all_points else records)]
        identity = {"mode": "HOSTED_TEST", "phase": phase, "epoch": "TEST_" + phase, "points": points,
            "smoke_point_id": min(p["id"] for p in points), "repeats": 1 if phase == "SMOKE" else 3,
            "realizations": 1, "real_graph": False, "attempt_cap_total": 30 if phase == "SMOKE" else 7956}
        directory = self.root / NAMESPACES[phase]
        calls = LiveCalls(directory, identity, MockHTTP(control_response), {i: [] for i in range(1, 6)},
                          lambda: self.now[0], test_mode=True)
        methods = ControlMethods(records)
        runner = HostedRunner(directory, identity, calls, methods)
        saved = {r["point"]["id"]: r["snapshot"] for r in records}
        count = []
        def shared(book: object, point: dict, org: int) -> dict:
            count.append((point["id"], org))
            return deepcopy(saved[point["id"]])
        return runner, SimpleNamespace(shared=shared), count

    def finish(self, runner: HostedRunner, upstream: object, outcome: object) -> dict:
        """Đẩy clock quota ảo, không dùng sleep hoặc gọi HTTP thật trong unit test."""
        for _ in range(100):
            result = runner.tick(upstream, outcome)
            self.assertFalse(result["blocked"])
            if result["status"] == "COMPLETE": return result
            self.now[0] = max(self.now[0] + .01, min(result["waiting"].values()))
        self.fail("Lịch không hội tụ")

    def test_smoke_lexicographic_id_keeps_original_global_shard_one_repeat_no_labels(self) -> None:
        first = min(self.records, key=lambda r: r["point"]["id"])
        runner, upstream, count = self.setup("SMOKE", [first], all_points=True)
        with patch("core.unified_live.manager.canonical_outcome", side_effect=AssertionError("Cấm nhãn smoke")):
            self.finish(runner, upstream, lambda _: self.fail("Smoke không được gọi oracle"))
        index = next(i for i, r in enumerate(self.records) if r["point"]["id"] == first["point"]["id"])
        self.assertEqual(count, [(first["point"]["id"], 1 + index % 5)])
        result = verify(runner.directory, runner.identity, runner.methods)
        self.assertEqual(result["status"], "PASS_U08_SMOKE")
        self.assertEqual(result["forecast_slots"], 8)
        self.assertLessEqual(result["http_attempts"], 8)

    def test_research24_slots_one_shared_new_uuids_and_canonical_barrier(self) -> None:
        runner, upstream, count = self.setup("RESEARCH", self.records[:1])
        labels = []
        def outcome(point: dict) -> dict:
            book = StageBook(runner.directory, runner.identity, verify_only=True)
            from core.unified_protocol import ordered_branches
            self.assertTrue(all(book.complete(f"forecast/{point['id']}/u0/r{r}/{v}") for r in range(3) for v in ordered_branches(r)))
            labels.append(point["id"])
            frame = pd.DataFrame({"Datetime": pd.bdate_range(point["cutoff"], periods=4),
                "Open": [100.]*4, "High": [120.]*4, "Low": [90.]*4,
                "Close": [100., 101., 102., 110.], "Volume": [1000.]*4})
            return outcome_from_frame(point, frame, "1"*64)
        self.finish(runner, upstream, outcome)
        self.assertEqual(len(count), 1)
        self.assertEqual(len(labels), 1)
        before = len(runner.calls.state["rows"])
        self.finish(runner, upstream, outcome)
        self.assertEqual(len(runner.calls.state["rows"]), before)
        with patch("httpx.Client", side_effect=AssertionError("Cấm client")), \
             patch("langchain_groq.ChatGroq", side_effect=AssertionError("Cấm SDK")), \
             patch("dotenv.dotenv_values", side_effect=AssertionError("Cấm key")):
            result = verify(runner.directory, runner.identity, runner.methods)
        self.assertEqual(result["forecast_slots"], 24)
        ids = [r["id"] for r in runner.calls.state["rows"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_smoke_cost_is_carried_but_not_responses_or_attempts(self) -> None:
        runner, upstream, _ = self.setup("SMOKE", self.records[:1])
        self.finish(runner, upstream, lambda _: self.fail("Không oracle"))
        carry = carry_smoke(self.root, {i: [] for i in range(1, 6)})
        research = {**runner.identity, "phase": "RESEARCH", "epoch": "TEST_RESEARCH", "repeats": 3}
        calls = LiveCalls(self.root / NAMESPACES["RESEARCH"], research, MockHTTP(control_response), carry,
                          lambda: self.now[0], test_mode=True)
        self.assertEqual(sum(len(v) for v in carry.values()), len(runner.calls.state["rows"]))
        self.assertEqual(calls.state["rows"], [])
        self.assertTrue(all("response" not in row for row in calls.state["carry"]))

    def test_complete_policy_tamper_is_rejected_before_reuse(self) -> None:
        runner, upstream, _ = self.setup("SMOKE", self.records[:1])
        self.finish(runner, upstream, lambda _: self.fail("Không oracle"))
        book = StageBook(runner.directory, runner.identity, verify_only=True)
        slot = f"forecast/{self.records[0]['point']['id']}/u0/r0/original_common"
        document = load(book.path(slot))
        output = document["attempts"][0]["output"]
        output["policy"]["final_action"] = "LONG"
        document["attempts"][0]["output_sha256"] = stage_digest(output)
        save(book.path(slot), document)
        with self.assertRaises(ValueError): verify(runner.directory, runner.identity, runner.methods)

    def test_partial_never_reports_complete_support(self) -> None:
        runner, upstream, _ = self.setup("RESEARCH", self.records[:2])
        runner.tick(upstream, lambda _: self.fail("Chưa đủ24 slot"))
        with self.assertRaises(ValueError): verify(runner.directory, runner.identity, runner.methods)
        result = verify(runner.directory, runner.identity, runner.methods, require_complete=False)
        self.assertEqual(result["status"], "PARTIAL_U08")
        self.assertEqual(result["complete_points"], 0)


if __name__ == "__main__":
    unittest.main()
