"""Hồi quy reset riêng forecast hết attempt; bảo toàn upstream và dữ liệu đã hoàn tất."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
from unified_point_restart import test_restart as parent_tests
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock
from core.unified_contracts import digest
from core.unified_execution import StageBook
from core.unified_execution_transport import MockHTTP, Exhausted, wire_state
from core.unified_point_restart.execution import RestartRunner, verify
from core.unified_point_restart.wire import RestartCalls
from core.unified_slot_restart import runtime
from scripts.check_unified_execution import control_response


class SlotTransportTests(parent_tests.RestartTransportTests):
    """Giữ retry/repair, raw, phase cap và UNKNOWN của transport được dùng lại."""


class SlotExecutionTests(parent_tests.parent_tests.execution_tests.HostedExecutionTests):
    """Fixture hai điểm, reset riêng MT sau chuỗi 429/schema lỗi/429."""
    outcome = parent_tests.RestartHostedTests.outcome

    def setup(self, phase: str, records: list[dict], *, all_points: bool = False) -> tuple:
        """Giữ cùng dữ liệu/callback U08 và dùng runner generation-aware."""
        original, upstream, count = super().setup(phase, records, all_points=all_points)
        calls = RestartCalls(original.directory, original.identity, MockHTTP(control_response),
            {i: [] for i in range(1, 6)}, lambda: self.now[0], test_mode=True)
        return RestartRunner(original.directory, original.identity, calls, original.methods), upstream, count

    def test_partial_never_reports_complete_support(self) -> None:
        runner, upstream, _ = self.setup("RESEARCH", self.records[:2])
        runner.calls.sender = MockHTTP(lambda _: httpx.Response(429, headers={"retry-after": "30"}, text="retry after 30 seconds"))
        result = runner.tick(upstream, self.outcome)
        self.assertTrue(result["waiting"])
        self.assertEqual(verify(runner.directory, runner.identity, runner.methods, require_complete=False)["complete_points"], 0)

    def failed_fixture(self) -> tuple:
        """Làm lỗi đúng ba HTTP của slot đích, không ảnh hưởng điểm ở org khác."""
        selected = next(row for row in self.records if row["point"]["id"] == "VCB-2026-09-23")
        runner, upstream, count = self.setup("RESEARCH", [selected, self.records[0]])
        slot = "forecast/" + runner.identity["points"][0]["id"] + "/u0/r2/MT_BICL"
        codes = [429, 200, 429]
        def send(request: httpx.Request) -> httpx.Response:
            if runner.calls.state["rows"][-1]["slot"] == slot:
                code = codes.pop(0)
                if code == 200: return httpx.Response(200, json={"choices": [{"message": {"content": "{}"}}]})
                return httpx.Response(429, headers={"retry-after": "10"}, text="retry after 10 seconds")
            return control_response(request)
        runner.calls.sender = MockHTTP(send)
        for _ in range(10):
            result = runner.tick(upstream, self.outcome)
            if result["blocked"]: break
            self.now[0] = max(result["waiting"].values()) + .01
        self.assertTrue(result["blocked"])
        self.assertEqual(result["complete_points"], 1)
        self.assertEqual(codes, [])
        parent = {"plan": {"retired_http": {}, "generations": {}, "prefix": {"complete_slots": {}}}}
        return runner, upstream, count, slot, parent

    def test_slot_reset_preserves_shared_prepare_all_other_slots_and_raw(self) -> None:
        runner, upstream, count, slot, parent = self.failed_fixture()
        plan = runtime.plan_reset(self.root, runner.identity, slot, parent)
        originals = {p.relative_to(runner.directory).as_posix(): p.read_bytes()
            for folder in ("slots", "http") for p in (runner.directory / folder).glob("*.json")}
        wire_before = (runner.directory / "wire.json").read_bytes()
        backup = runtime.write_backup(self.root, plan)
        self.assertEqual(len(plan["deleted_slots"]), 1)
        self.assertEqual(len(plan["new_retired_http"]), 3)
        self.assertEqual(len(plan["backup_files"]), 5)
        runtime.purge(self.root, plan, backup)
        runtime.purge(self.root, plan, backup)
        self.assertEqual((runner.directory / "wire.json").read_bytes(), wire_before)
        for name, raw in originals.items():
            if name not in plan["deleted_slots"]: self.assertEqual((runner.directory / name).read_bytes(), raw)
        calls = RestartCalls(runner.directory, runner.identity, MockHTTP(control_response),
            {i: [] for i in range(1, 6)}, lambda: self.now[0], test_mode=True,
            retired=plan["retired_http"], generations=plan["generations"])
        restarted = RestartRunner(runner.directory, runner.identity, calls, runner.methods)
        self.finish(restarted, upstream, self.outcome)
        result = verify(runner.directory, runner.identity, runner.methods, retired=plan["retired_http"])
        self.assertEqual((result["complete_points"], result["forecast_slots"]), (2, 48))
        self.assertEqual(result["retired_http_attempts"], 3)
        self.assertEqual(len(count), 2)
        old_rows = [r for r in runner.calls.state["rows"] if r["slot"] == slot]
        new_rows = [r for r in calls.active_rows() if r["slot"] == slot]
        self.assertEqual(len(new_rows), 1)
        self.assertNotEqual(old_rows[0]["attempt"], new_rows[0]["attempt"])
        admission = {"first_slot_restart_http_sequence": len(runner.calls.state["rows"]),
            "parent_admission": {"first_restart_http_sequence": 0,
                "first_model_scoped_http_sequence": 0, "first_provider_scoped_http_sequence": 0,
                "plan": {"retired_http": {}, "generations": {}}}, "plan": plan}
        runtime.verify_admissions(calls.state, admission, 7956)
        with self.assertRaises(ValueError): runtime.verify_admissions(calls.state, admission, len(calls.state["rows"]) - 1)
        for name, raw in originals.items():
            if name not in plan["deleted_slots"]: self.assertEqual((runner.directory / name).read_bytes(), raw)
        with self.assertRaises(ValueError): runtime.purge(self.root, plan, backup)

    def test_completed_or_non_exhausted_slot_rejected(self) -> None:
        runner, _, _, slot, parent = self.failed_fixture()
        with self.assertRaises(ValueError):
            runtime.plan_reset(self.root, runner.identity, slot.replace("r2/MT_BICL", "r0/original_common"), parent)
        parent["plan"]["retired_http"] = {r["id"]: digest(r) for r in runner.calls.state["rows"] if r["slot"] == slot}
        with self.assertRaises(ValueError): runtime.plan_reset(self.root, runner.identity, slot, parent)

    def test_valid_response_cannot_be_discarded(self) -> None:
        runner, _, _, slot, parent = self.failed_fixture()
        state = runner.calls.state
        row = next(r for r in state["rows"] if r["slot"] == slot and r["status"] == 200)
        response = control_response(httpx.Request("POST", "https://synthetic.invalid", json=row["body"]))
        row["response"] = response.content.decode("utf-8")
        save(runner.directory / "http" / (row["id"] + ".json"), row)
        index = load(runner.directory / "wire.json")
        for item in index["rows"]:
            if item["id"] == row["id"]: item["sha256"] = digest(row)
        save(runner.directory / "wire.json", index)
        with self.assertRaisesRegex(ValueError, "hợp lệ"):
            runtime.plan_reset(self.root, runner.identity, slot, parent)

    def test_backup_and_checkpoint_tamper_rejected_before_delete(self) -> None:
        runner, _, _, slot, parent = self.failed_fixture()
        plan = runtime.plan_reset(self.root, runner.identity, slot, parent)
        backup = runtime.write_backup(self.root, plan)
        path = runner.directory / next(iter(plan["deleted_slots"]))
        before = path.read_bytes()
        path.write_bytes(b"changed")
        with self.assertRaises(ValueError): runtime.purge(self.root, plan, backup)
        self.assertTrue(path.exists())
        path.write_bytes(before)
        (self.root / runtime.BACKUP).write_bytes(b"bad zip")
        with self.assertRaises(ValueError): runtime.purge(self.root, plan, backup)
        self.assertEqual(path.read_bytes(), before)

    def test_driver_keeps_manager_lock_through_cold_seal(self) -> None:
        runner, upstream, count = self.setup("RESEARCH", self.records[:1])
        save(runner.directory / "status.json", {"phase": "RESEARCH", "status": "PENDING"})
        methods = runner.methods
        methods.shared = upstream.shared
        def cold(command: list[str], **kwargs: object) -> SimpleNamespace:
            self.assertIn("scripts/unified_slot_restart/run.py", command)
            with self.assertRaises(RuntimeError):
                with PriorRunLock(runner.directory / "manager", digest(runner.identity)):
                    self.fail("Collector phải giữ manager lock")
            with PriorRunLock(runner.directory, digest(runner.identity)):
                result = verify(runner.directory, runner.identity, methods)
            save(runner.directory / "quota_receipt.json", {**result, "quota_policy": runtime.POLICY})
            return SimpleNamespace(returncode=0, stdout="SYNTHETIC_COLD_PASS", stderr="")
        manifest = {"sources": {}, "plan": {"retired_http": {}, "generations": {}}}
        with patch.object(runtime, "require", return_value=({}, {"max_http_attempts": 7956}, manifest)), \
             patch.object(runtime, "run_identity", return_value=runner.identity), \
             patch.object(runtime, "guard_for", return_value=lambda: None), \
             patch.object(runtime, "anchored", return_value={"sources": {}}), \
             patch.object(runtime, "binding", return_value={}), \
             patch.object(runtime, "LiveHTTP", return_value=SimpleNamespace(close=lambda: None)), \
             patch.object(runtime, "attach_diagnostics"), \
             patch.object(runtime, "RestartCalls", return_value=runner.calls), \
             patch.object(runtime, "history", return_value={i: [] for i in range(1, 6)}), \
             patch.object(runtime, "carry_smoke", side_effect=lambda root, rows: rows), \
             patch("core.unified_execution_providers.StudyProviders", return_value=methods), \
             patch.object(runtime, "canonical_outcome", side_effect=lambda root, point: self.outcome(point)), \
             patch.object(runtime, "subprocess", SimpleNamespace(run=cold)), patch("builtins.print"):
            result = runtime.collect(self.root)
        self.assertEqual(result["forecast_slots"], 24)
        self.assertEqual(len(count), 1)


class SlotReleaseTests(parent_tests.RestartReleaseTests):
    """Giữ kiểm trước client ở entrypoint mới."""
    def test_missing_release_rejects_before_any_client(self) -> None:
        with patch.object(runtime, "require", side_effect=ValueError("Thiếu grant")), \
             patch.object(runtime, "LiveHTTP", side_effect=AssertionError("Cấm client")), \
             patch("dotenv.dotenv_values", side_effect=AssertionError("Cấm key")):
            with self.assertRaisesRegex(ValueError, "grant"): runtime.collect(Path("synthetic"))


if __name__ == "__main__":
    unittest.main()
