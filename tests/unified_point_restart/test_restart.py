"""Hồi quy reset có sao lưu, cách ly generation và giữ đủ chi phí HTTP."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from uuid import uuid4

import httpx
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
from unified_provider_quota import test_policy as parent_tests
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock
from core.unified_contracts import digest
from core.unified_execution import StageBook
from core.unified_execution_transport import MockHTTP, Uncertain, Exhausted, wire_state
from core.unified_experiment import outcome_from_frame
from core.unified_live.release import NAMESPACES
from core.unified_point_restart import runtime
from core.unified_point_restart.execution import RestartRunner, verify
from core.unified_point_restart.wire import RestartCalls, attach_diagnostics
from scripts.check_unified_execution import control_response


class RestartTransportTests(parent_tests.ProviderTransportTests):
    """Giữ nguyên hợp đồng retry/repair, thay tập raw được phép replay."""
    def calls(self, handler: object = None, *, guard: object = None, identity: dict | None = None,
              retired: dict | None = None, generations: dict | None = None) -> RestartCalls:
        """Mỗi resume đọc lại ledger thật; HTTP chỉ qua MockTransport."""
        def send(request: httpx.Request) -> httpx.Response:
            self.sent.append(json.loads(request.content))
            return (handler or control_response)(request)
        return RestartCalls(self.root / "run", identity or self.identity, MockHTTP(send),
            {i: [] for i in range(1, 6)}, lambda: self.now[0], guard or (lambda: None), test_mode=True,
            retired=retired, generations=generations)

    def unknown(self) -> dict:
        """Tạo intent chưa có response như trường hợp người dùng yêu cầu bỏ điểm."""
        def timeout(request: httpx.Request) -> httpx.Response:
            raise httpx.ReadTimeout("CONTROL", request=request)
        with self.assertRaises(Uncertain):
            self.calls(timeout).call("forecast/p/v", 1, self.body, "old")
        return wire_state(self.root / "run")["rows"][0]

    def test_retired_unknown_new_uuid_preserves_original_bytes_and_cost(self) -> None:
        old = self.unknown()
        path = self.root / "run/http" / (old["id"] + ".json")
        before = path.read_bytes()
        calls = self.calls(retired={old["id"]: digest(old)}, generations={"p": 1})
        _, new = calls.call("forecast/p/v", 1, self.body, "new")
        self.assertNotEqual(old["id"], new["id"])
        self.assertEqual(new["point_generation"], 1)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(len(calls.state["rows"]), 2)
        self.assertEqual(calls.active_rows(), [new])
        replay = self.calls(retired={old["id"]: digest(old)}, generations={"p": 1})
        self.assertEqual(replay.call("forecast/p/v", 1, self.body, "new")[1]["id"], new["id"])
        self.assertEqual(len(self.sent), 2)

    def test_retired_success_is_not_selected_for_new_execution(self) -> None:
        old = self.calls().call("forecast/p/v", 1, self.body, "old")[1]
        calls = self.calls(retired={old["id"]: digest(old)}, generations={"p": 1})
        new = calls.call("forecast/p/v", 1, self.body, "new")[1]
        self.assertNotEqual(old["id"], new["id"])
        self.assertEqual(len(self.sent), 2)

    def test_retired_unknown_still_consumes_global_cap(self) -> None:
        old = self.unknown()
        calls = self.calls(retired={old["id"]: digest(old)}, generations={"p": 1})
        calls.attempt_cap_total = 1
        with self.assertRaises(Exhausted): calls.call("forecast/p/v", 1, self.body, "new")
        self.assertEqual(len(self.sent), 1)

    def test_retirement_requires_exact_existing_raw(self) -> None:
        old = self.unknown()
        for retired in ({old["id"]: "0" * 64}, {str(uuid4()): digest(old)}):
            with self.subTest(retired=retired), self.assertRaises(ValueError): self.calls(retired=retired)


class RestartHostedTests(parent_tests.ProviderHostedTests):
    """Chạy paired/barrier và reset toàn điểm trên fixture U06 có hai org."""
    def setup(self, phase: str, records: list[dict], *, all_points: bool = False) -> tuple:
        """Giữ cùng dữ liệu và đổi runner lẫn transport sang generation-aware."""
        original, upstream, count = super().setup(phase, records, all_points=all_points)
        calls = RestartCalls(original.directory, original.identity, MockHTTP(control_response),
            {i: [] for i in range(1, 6)}, lambda: self.now[0], test_mode=True)
        return RestartRunner(original.directory, original.identity, calls, original.methods), upstream, count

    def outcome(self, point: dict) -> dict:
        """Oracle tổng hợp giữ đúng công thức T+2.5, không lấy giá cohort thật."""
        frame = pd.DataFrame({"Datetime": pd.bdate_range(point["cutoff"], periods=4), "Open": [100.] * 4,
            "High": [120.] * 4, "Low": [90.] * 4, "Close": [100., 101., 102., 110.], "Volume": [1000.] * 4})
        return outcome_from_frame(point, frame, "1" * 64)

    def failed_fixture(self) -> tuple:
        """Một điểm lỗi sau bốn HTTP hợp lệ, điểm còn lại hoàn chỉnh."""
        runner, upstream, count = self.setup("RESEARCH", self.records[:2])
        sent = [0]
        def send(request: httpx.Request) -> httpx.Response:
            sent[0] += 1
            if sent[0] == 5: raise httpx.ReadTimeout("CONTROL", request=request)
            return control_response(request)
        runner.calls.sender = MockHTTP(send)
        result = runner.tick(upstream, self.outcome)
        self.assertEqual(result["complete_points"], 1)
        self.assertTrue(result["blocked"])
        return runner, upstream, count

    def reset_fixture(self) -> tuple:
        """Chốt backup trước purge và thu byte mọi file không được phép đổi."""
        runner, upstream, count = self.failed_fixture()
        target = runner.identity["points"][0]["id"]
        plan = runtime.plan_reset(self.root, runner.identity, (target,), set())
        backup = runtime.write_backup(self.root, plan)
        originals = {p.relative_to(runner.directory).as_posix(): p.read_bytes()
            for folder in ("slots", "http") for p in (runner.directory / folder).glob("*.json")}
        originals["wire.json"] = (runner.directory / "wire.json").read_bytes()
        return runner, upstream, count, plan, backup, originals

    def test_reset_reruns_only_failed_point_and_cold_verifies_active_dataset(self) -> None:
        runner, upstream, count, plan, backup, originals = self.reset_fixture()
        self.assertEqual(runtime.write_backup(self.root, plan), backup)
        runtime.purge(self.root, plan, backup)
        runtime.purge(self.root, plan, backup)
        for name, raw in originals.items():
            path = runner.directory / name
            if name in plan["deleted_slots"]: self.assertFalse(path.exists())
            else: self.assertEqual(path.read_bytes(), raw)
        calls = RestartCalls(runner.directory, runner.identity, MockHTTP(control_response),
            {i: [] for i in range(1, 6)}, lambda: self.now[0], test_mode=True,
            retired=plan["retired_http"], generations=plan["generations"])
        restarted = RestartRunner(runner.directory, runner.identity, calls, runner.methods)
        self.finish(restarted, upstream, self.outcome)
        result = verify(runner.directory, runner.identity, runner.methods, retired=plan["retired_http"])
        self.assertEqual((result["complete_points"], result["forecast_slots"]), (2, 48))
        self.assertEqual(result["retired_http_attempts"], 5)
        self.assertEqual(result["http_attempts"], result["active_http_attempts"] + 5)
        self.assertEqual([p for p, _ in count].count(plan["targets"][0]), 2)
        self.assertEqual(len(count), 3)
        for name, raw in originals.items():
            if name.startswith("http/") or (name.startswith("slots/") and name not in plan["deleted_slots"]):
                self.assertEqual((runner.directory / name).read_bytes(), raw)
        with self.assertRaises(ValueError): runtime.purge(self.root, plan, backup)

    def test_purge_rejects_tamper_before_deleting_any_file(self) -> None:
        runner, _, _, plan, backup, originals = self.reset_fixture()
        names = list(plan["deleted_slots"])
        (runner.directory / names[-1]).write_bytes(b"changed")
        with self.assertRaises(ValueError): runtime.purge(self.root, plan, backup)
        self.assertTrue(all((runner.directory / name).exists() for name in names))

    def test_corrupt_backup_rejects_before_deleting_any_file(self) -> None:
        runner, _, _, plan, backup, _ = self.reset_fixture()
        (self.root / runtime.BACKUP).write_bytes(b"bad zip")
        with self.assertRaises(ValueError): runtime.purge(self.root, plan, backup)
        self.assertTrue(all((runner.directory / name).exists() for name in plan["deleted_slots"]))

    def test_purge_rejects_path_escape_and_resumes_partial_purge(self) -> None:
        runner, _, _, plan, backup, _ = self.reset_fixture()
        invalid = deepcopy(plan)
        invalid["deleted_slots"]["../outside.json"] = "0" * 64
        with self.assertRaises(ValueError): runtime.purge(self.root, invalid, backup)
        first = next(iter(plan["deleted_slots"]))
        (runner.directory / first).unlink()
        runtime.purge(self.root, plan, backup)
        self.assertTrue(all(not (runner.directory / name).exists() for name in plan["deleted_slots"]))

    def test_completed_or_protected_point_cannot_be_reset(self) -> None:
        runner, _, _, plan, _, _ = self.reset_fixture()
        with self.assertRaises(ValueError):
            runtime.plan_reset(self.root, runner.identity, (runner.identity["points"][1]["id"],), set())
        with self.assertRaises(ValueError):
            runtime.plan_reset(self.root, runner.identity, tuple(plan["targets"]), set(plan["deleted_slots"]))

    def test_cold_verifier_rejects_missing_or_changed_retirement(self) -> None:
        runner, _, _, plan, _, _ = self.reset_fixture()
        for retired in ({str(uuid4()): "0" * 64}, {next(iter(plan["retired_http"])): "0" * 64}):
            with self.subTest(retired=retired), self.assertRaises(ValueError):
                verify(runner.directory, runner.identity, runner.methods, retired=retired, require_complete=False)

    def test_driver_keeps_manager_lock_through_cold_seal(self) -> None:
        runner, upstream, count = self.setup("RESEARCH", self.records[:1])
        save(runner.directory / "status.json", {"phase": "RESEARCH", "status": "PENDING"})
        methods = runner.methods
        methods.shared = upstream.shared
        def cold(command: list[str], **kwargs: object) -> SimpleNamespace:
            self.assertIn("scripts/unified_point_restart/run.py", command)
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


class RestartReleaseTests(unittest.TestCase):
    """Dừng thủ công và release phải chặn trước credential/client."""
    def test_missing_release_rejects_before_any_client(self) -> None:
        with patch.object(runtime, "require", side_effect=ValueError("Thiếu grant")), \
             patch.object(runtime, "LiveHTTP", side_effect=AssertionError("Cấm client")), \
             patch("dotenv.dotenv_values", side_effect=AssertionError("Cấm key")):
            with self.assertRaisesRegex(ValueError, "grant"): runtime.collect(Path("synthetic"))

    def test_stopped_driver_returns_before_reading_credentials(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / NAMESPACES["RESEARCH"]
            identity = {"mode": "HOSTED_TEST", "phase": "RESEARCH", "epoch": "TEST"}
            save(directory / "status.json", {"status": "STOPPED_BY_OPERATOR", "forecast_complete": 1632})
            (directory / "stop.request").write_text("USER", encoding="utf-8")
            with patch.object(runtime, "require", return_value=({}, {}, {})), \
                 patch.object(runtime, "run_identity", return_value=identity), \
                 patch.object(runtime, "LiveHTTP", side_effect=AssertionError("Cấm client")):
                result = runtime.collect(root)
            self.assertEqual(result["forecast_complete"], 1632)


class DiagnosticTests(unittest.TestCase):
    """Bằng chứng sát transport không chứa key hoặc nội dung ngoại lệ nhạy cảm."""
    def test_http_headers_and_body_durable_without_authorization(self) -> None:
        with TemporaryDirectory() as temporary:
            root, request_id = Path(temporary), str(uuid4())
            with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200,
                    headers={"x-request-id": "provider-id", "authorization": "SECRET"}, text="RAW"))) as client:
                def send(body: dict) -> tuple:
                    response = client.post("https://synthetic.invalid", json=body)
                    return response.status_code, response.content, dict(response.headers)
                sender = SimpleNamespace(send=send, clients={1: client}, intent=lambda: {"id": request_id, "org": 1})
                attach_diagnostics(sender, root)
                self.assertEqual(sender.send({"model": "test"})[0], 200)
            path = root / "diagnostics" / (request_id + ".json")
            record = load(path)
            self.assertEqual(record["response"], "RAW")
            self.assertEqual(record["headers"]["x-request-id"], "provider-id")
            self.assertNotIn("SECRET", path.read_text(encoding="utf-8"))

    def test_timeout_keeps_status_headers_and_type_without_exception_text(self) -> None:
        with TemporaryDirectory() as temporary:
            root, request_id = Path(temporary), str(uuid4())
            client = SimpleNamespace(event_hooks={"response": []})
            def send(body: dict) -> tuple:
                client.event_hooks["response"][0](httpx.Response(200, headers={"x-request-id": "partial"}))
                raise httpx.ReadTimeout("SECRET_FROM_EXCEPTION")
            sender = SimpleNamespace(send=send, clients={1: client}, intent=lambda: {"id": request_id, "org": 1})
            attach_diagnostics(sender, root)
            with self.assertRaises(httpx.ReadTimeout): sender.send({})
            path = root / "diagnostics" / (request_id + ".json")
            record = load(path)
            self.assertEqual(record["server_status"], 200)
            self.assertEqual(record["error_type"], "httpx.ReadTimeout")
            self.assertNotIn("SECRET", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
