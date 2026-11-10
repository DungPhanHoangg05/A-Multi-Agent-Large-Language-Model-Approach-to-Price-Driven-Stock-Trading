"""Hồi quy quota org/model, resume journal cũ và rào release trước client."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
from unified_live import test_transport as transport_tests
from unified_live import test_execution as execution_tests
from core.historical_evaluation_journal import load, save
from core.unified_contracts import digest
from core.unified_execution import StageBook
from core.unified_execution_transport import MockHTTP, Deferred, Exhausted, wire_state
from core.unified_experiment import outcome_from_frame
from core.prior_run_lock import PriorRunLock
from core.unified_live.transport import LiveCalls
from core.unified_live.release import NAMESPACES
from core.unified_model_quota.policy import POLICY, ModelCalls, admit, row_model
from core.unified_model_quota import runtime
from scripts.check_unified_execution import control_response

GPT = "openai/gpt-oss-20b"
QWEN = "qwen/qwen3.8-27b"


class ModelTransportTests(transport_tests.LiveTransportTests):
    """Chạy lại các hợp đồng retry/repair/UNKNOWN U08 bằng transport mới."""
    def calls(self, handler: object = None, *, guard: object = None, identity: dict | None = None) -> ModelCalls:
        """Mỗi lần mở lại đều đọc journal thật, không giả lập việc resume."""
        def send(request: httpx.Request) -> httpx.Response:
            self.sent.append(json.loads(request.content))
            return (handler or control_response)(request)
        return ModelCalls(self.root / "run", identity or self.identity, MockHTTP(send), {i: [] for i in range(1, 6)},
                          lambda: self.now[0], guard or (lambda: None), test_mode=True)

    def test_legacy_wire_replays_same_uuid_then_appends_other_model(self) -> None:
        directory = self.root / "run"
        old = LiveCalls(directory, self.identity, MockHTTP(control_response), {i: [] for i in range(1, 6)},
                        lambda: self.now[0], test_mode=True)
        _, first = old.call("forecast/p/v", 1, self.body, "attempt")
        raw_path = directory / "http" / (first["id"] + ".json")
        before = raw_path.read_bytes()
        resumed = self.calls()
        _, replay = resumed.call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(replay["id"], first["id"])
        self.assertEqual(self.sent, [])
        vision = {**deepcopy(self.body), "model": QWEN, "reasoning_effort": "none"}
        del vision["response_format"]
        resumed.call("graph/p/pattern", 1, vision, "vision-attempt")
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(len(resumed.state["rows"]), 2)
        self.assertEqual(raw_path.read_bytes(), before)

    def test_phase_cap_counts_both_models(self) -> None:
        calls = self.calls(identity={**self.identity, "attempt_cap_total": 1})
        vision = {**deepcopy(self.body), "model": QWEN, "reasoning_effort": "none"}
        del vision["response_format"]
        calls.call("graph/p/pattern", 1, vision, "vision-attempt")
        with self.assertRaises(Exhausted):
            calls.call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(len(self.sent), 1)

    def test_admission_replay_detects_same_model_over_budget(self) -> None:
        calls = self.calls()
        calls.call("forecast/p/v", 1, self.body, "attempt")
        self.now[0] += 62
        calls.call("forecast/p/other", 1, self.body, "other-attempt")
        runtime.verify_admissions(calls.state, 0, 30)
        poisoned = deepcopy(calls.state)
        poisoned["rows"][1]["started_at"] = poisoned["rows"][0]["completed_at"] + .1
        poisoned["rows"][1]["reserved_tokens"] = 8000
        with self.assertRaisesRegex(ValueError, "vi phạm quota"):
            runtime.verify_admissions(poisoned, 0, 30)


class BucketTests(unittest.TestCase):
    """Kiểm độc lập đủ RPM/RPD/TPM/TPD và header/cooldown trong từng bucket."""
    def setUp(self) -> None:
        self.now = 2000000000.

    def row(self, model: str, *, org: int = 1, tokens: int = 1, age: float = 1.) -> dict:
        """Carry synthetic giữ định dạng model tường minh như các ledger lịch sử."""
        return {"org": org, "model": model, "started_at": self.now - age,
                "reserved_tokens": tokens, "total_tokens": tokens, "status": 200}

    def test_every_limit_blocks_own_model_but_not_other_model_or_org(self) -> None:
        scenarios = {"rpm": [self.row(QWEN) for _ in range(30)],
                     "rpd": [self.row(QWEN, age=3600) for _ in range(1000)],
                     "tpm": [self.row(QWEN, tokens=7900)],
                     "tpd": [self.row(QWEN, tokens=8000, age=3600) for _ in range(25)]}
        for name, carry in scenarios.items():
            with self.subTest(limit=name):
                state = {"carry": carry, "rows": []}
                before = deepcopy(state)
                with self.assertRaises(Deferred): admit(state, 1, QWEN, 4000, self.now, 7956)
                admit(state, 1, GPT, 4000, self.now, 7956)
                admit(state, 2, QWEN, 4000, self.now, 7956)
                self.assertEqual(state, before)

    def test_combined_daily_usage_above200k_is_valid_when_each_model_has_budget(self) -> None:
        carry = [self.row(model, tokens=8000, age=3600) for model in (GPT, QWEN) for _ in range(24)]
        state = {"carry": carry, "rows": []}
        for model in (GPT, QWEN): admit(state, 1, model, 4000, self.now, 7956)

    def test_active_unknown_reserve_expires_in_own_bucket_only(self) -> None:
        unknown = {**self.row(QWEN, tokens=7900), "status": "UNKNOWN", "total_tokens": None}
        state = {"carry": [unknown], "rows": []}
        with self.assertRaises(Deferred): admit(state, 1, QWEN, 4000, self.now, 7956)
        admit(state, 1, GPT, 4000, self.now, 7956)
        admit(state, 1, QWEN, 4000, self.now + 62, 7956)
        self.assertEqual(state["carry"][0]["status"], "UNKNOWN")

    def test_header_remaining_reset_is_scoped_to_response_model(self) -> None:
        row = self.row(QWEN)
        row.update(completed_at=self.now, headers={"x-ratelimit-remaining-tokens": "1", "x-ratelimit-reset-tokens": "2m"})
        state = {"carry": [row], "rows": []}
        with self.assertRaises(Deferred) as caught: admit(state, 1, QWEN, 4000, self.now, 7956)
        self.assertGreaterEqual(caught.exception.until, self.now + 120)
        admit(state, 1, GPT, 4000, self.now, 7956)

    def test_retry_after_and_lower_limit_are_scoped_to_model(self) -> None:
        row = {**self.row(QWEN), "retry_until": self.now + 30}
        state = {"carry": [row], "rows": []}
        with self.assertRaises(Deferred): admit(state, 1, QWEN, 4000, self.now, 7956)
        admit(state, 1, GPT, 4000, self.now, 7956)
        del row["retry_until"]
        row["headers"] = {"x-ratelimit-limit-tokens": "4000"}
        with self.assertRaises(Exhausted): admit(state, 1, QWEN, 4000, self.now, 7956)
        admit(state, 1, GPT, 4000, self.now, 7956)

    def test_carry_and_current_http_share_same_model_budget(self) -> None:
        carry = [self.row(GPT, tokens=8000, age=3600) for _ in range(24)]
        current = {**self.row(GPT, tokens=6000, age=1800), "body": {"model": GPT}}
        state = {"carry": carry, "rows": [current]}
        with self.assertRaises(Deferred): admit(state, 1, GPT, 4000, self.now, 7956)
        admit(state, 1, QWEN, 4000, self.now, 7956)

    def test_missing_unknown_or_conflicting_model_fails_closed(self) -> None:
        for row in ({}, {"model": "unknown"}, {"model": GPT, "body": {"model": QWEN}}):
            with self.subTest(row=row), self.assertRaises(ValueError): row_model(row)
        with self.assertRaises(ValueError): admit({"carry": [], "rows": []}, 1, "unknown", 100, self.now, 7956)


class PrefixTests(unittest.TestCase):
    """Amendment chỉ nối tiếp, các raw/complete slot đã khóa phải giữ nguyên byte."""
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / NAMESPACES["RESEARCH"]
        self.identity = {"mode": "HOSTED_TEST", "phase": "RESEARCH", "epoch": "TEST", "attempt_cap_total": 7956}
        self.book = StageBook(self.directory, self.identity)
        self.book.execute("forecast/synthetic", {"synthetic": True}, lambda _: {"decision": "SHORT"})
        self.state = {"identity": {"signature": digest(self.identity)}, "carry": [], "rows": []}
        save(self.directory / "wire.json", self.state)
        self.before = runtime.prefix(self.root)

    def test_new_complete_slots_and_http_append_are_allowed(self) -> None:
        self.book.execute("forecast/new", {"synthetic": True}, lambda _: {"decision": "LONG"})
        row = {"id": "new", "org": 1, "body": {"model": GPT}, "status": 200}
        save(self.directory / "http/new.json", row)
        save(self.directory / "wire.json", {**self.state, "rows": [{"id": "new", "sha256": digest(row)}]})
        checked = runtime.check_prefix(self.directory, self.before)
        self.assertEqual(len(checked["rows"]), 1)

    def test_complete_slot_mutation_is_rejected(self) -> None:
        path = self.book.path("forecast/synthetic")
        doc = load(path)
        doc["attempts"][0]["output"]["decision"] = "LONG"
        save(path, doc)
        with self.assertRaisesRegex(ValueError, "Slot complete"):
            runtime.check_prefix(self.directory, self.before)

    def test_carry_and_identity_mutations_are_rejected(self) -> None:
        save(self.directory / "wire.json", {**self.state, "carry": [{"org": 1, "model": GPT}]})
        with self.assertRaisesRegex(ValueError, "carry"):
            runtime.check_prefix(self.directory, self.before)
        save(self.directory / "wire.json", self.state)
        save(self.directory / "identity.json", {"identity": {**self.identity, "epoch": "changed"}})
        with self.assertRaisesRegex(ValueError, "Identity"):
            runtime.check_prefix(self.directory, self.before)

    def test_prefix_raw_cannot_be_replaced_or_removed(self) -> None:
        row = {"id": "old", "org": 1, "body": {"model": GPT}, "status": 200}
        save(self.directory / "http/old.json", row)
        save(self.directory / "wire.json", {**self.state, "rows": [{"id": "old", "sha256": digest(row)}]})
        before = runtime.prefix(self.root)
        save(self.directory / "wire.json", self.state)
        with self.assertRaisesRegex(ValueError, "Prefix raw"):
            runtime.check_prefix(self.directory, before)

    def test_unknown_before_amendment_requires_reconciliation(self) -> None:
        row = {"id": "unknown", "org": 1, "body": {"model": GPT}, "status": "UNKNOWN"}
        save(self.directory / "http/unknown.json", row)
        save(self.directory / "wire.json", {**self.state, "rows": [{"id": "unknown", "sha256": digest(row)}]})
        with self.assertRaisesRegex(ValueError, "UNKNOWN"): runtime.prefix(self.root)

    def test_stopped_entrypoint_preserves_counts_and_never_constructs_client(self) -> None:
        save(self.directory / "status.json", {"status": "PENDING", "forecast_complete": 802})
        (self.directory / "stop.request").write_text("USER", encoding="utf-8")
        with patch.object(runtime, "require", return_value=({}, {}, {})), \
             patch.object(runtime, "run_identity", return_value=self.identity), \
             patch.object(runtime, "LiveHTTP", side_effect=AssertionError("Cấm client")):
            result = runtime.collect(self.root)
        self.assertEqual(result["status"], "STOPPED_BY_OPERATOR")
        self.assertEqual(result["forecast_complete"], 802)

    def test_missing_amendment_fails_before_credentials(self) -> None:
        with patch.object(runtime, "require", side_effect=ValueError("Chưa có amendment")), \
             patch("dotenv.dotenv_values", side_effect=AssertionError("Cấm key")), \
             patch.object(runtime, "LiveHTTP", side_effect=AssertionError("Cấm client")):
            with self.assertRaisesRegex(ValueError, "amendment"): runtime.collect(self.root)

    def test_sealed_entrypoint_reverifies_before_return_without_client(self) -> None:
        save(self.directory / "quota_receipt.json", {"status": "SYNTHETIC_PASS"})
        with patch.object(runtime, "require", return_value=({}, {}, {})), \
             patch.object(runtime, "audit", return_value={"status": "REVERIFIED"}) as checked, \
             patch.object(runtime, "LiveHTTP", side_effect=AssertionError("Cấm client")):
            self.assertEqual(runtime.collect(self.root), {"status": "REVERIFIED"})
        checked.assert_called_once_with(self.root, seal=True)


class ModelHostedTests(execution_tests.HostedExecutionTests):
    """Chạy lại paired/barrier/economic fixture U08 với transport theo model."""
    def setup(self, phase: str, records: list[dict], *, all_points: bool = False) -> tuple:
        """Giữ nguyên fixture runner/phương pháp, thay riêng transport admission."""
        runner, upstream, count = super().setup(phase, records, all_points=all_points)
        runner.calls = ModelCalls(runner.directory, runner.identity, MockHTTP(control_response),
                                  {i: [] for i in range(1, 6)}, lambda: self.now[0], test_mode=True)
        return runner, upstream, count

    def test_manual_driver_finishes24_slots_and_keeps_owner_during_cold_process(self) -> None:
        runner, upstream, count = self.setup("RESEARCH", self.records[:1])
        save(runner.directory / "status.json", {"phase": "RESEARCH", "status": "PENDING"})
        methods = runner.methods
        methods.shared = upstream.shared
        labels = []
        def outcome(root: Path, point: dict) -> dict:
            labels.append(point["id"])
            frame = pd.DataFrame({"Datetime": pd.bdate_range(point["cutoff"], periods=4),
                "Open": [100.]*4, "High": [120.]*4, "Low": [90.]*4,
                "Close": [100., 101., 102., 110.], "Volume": [1000.]*4})
            return outcome_from_frame(point, frame, "1"*64)
        def sleep(seconds: float) -> None:
            self.now[0] += seconds + .01
        def cold(command: list[str], **kwargs: object) -> SimpleNamespace:
            self.assertEqual(command[-2:], ["verify", "--seal"])
            with self.assertRaisesRegex(RuntimeError, "khóa OS"):
                with PriorRunLock(runner.directory / "manager", digest(runner.identity)):
                    self.fail("Manager lock phải thuộc collector đến hết cold seal")
            with PriorRunLock(runner.directory, digest(runner.identity)):
                result = execution_tests.verify(runner.directory, runner.identity, methods)
            save(runner.directory / "quota_receipt.json", {**result, "quota_policy": POLICY})
            return SimpleNamespace(returncode=0, stdout="SYNTHETIC_COLD_PASS", stderr="")
        with patch.object(runtime, "require", return_value=({}, {"max_http_attempts": 7956}, {"sources": {}})), \
             patch.object(runtime, "run_identity", return_value=runner.identity), \
             patch.object(runtime, "guard_for", return_value=lambda: None), \
             patch.object(runtime, "anchored", return_value={}), \
             patch.object(runtime, "binding", return_value={}), \
             patch.object(runtime, "LiveHTTP", return_value=SimpleNamespace(close=lambda: None)), \
             patch.object(runtime, "ModelCalls", return_value=runner.calls), \
             patch.object(runtime, "history", return_value={i: [] for i in range(1, 6)}), \
             patch.object(runtime, "carry_smoke", side_effect=lambda root, rows: rows), \
             patch("core.unified_execution_providers.StudyProviders", return_value=methods), \
             patch.object(runtime, "canonical_outcome", side_effect=outcome), \
             patch.object(runtime.time, "time", side_effect=lambda: self.now[0]), \
             patch.object(runtime.time, "sleep", side_effect=sleep), \
             patch.object(runtime, "subprocess", SimpleNamespace(run=cold)), \
             patch("builtins.print"):
            result = runtime.collect(self.root)
        self.assertEqual(result["status"], "PASS_U08_RESEARCH")
        self.assertEqual(result["forecast_slots"], 24)
        self.assertEqual(result["quota_policy"], POLICY)
        self.assertEqual(len(count), 1)
        self.assertEqual(len(labels), 1)


class AmendmentGrantTests(unittest.TestCase):
    """Kiểm grant mới ràng buộc policy và chế độ manual/Free trước client."""
    def test_manual_scope_policy_spend_and_parent_cap_are_exact(self) -> None:
        parent, parent_grant = {}, {"max_http_attempts": 7956}
        manifest = {"prefix": {}}
        grant = {"version": "unified_model_quota_release_v1", "status": "MODEL_QUOTA_RELEASED",
                 "runtime_sha256": digest(manifest), "policy": POLICY, "authorization": runtime.AUTHORIZATION,
                 "manual_launch_only": True, "api": True, "paid_api_allowed": False, "spend_limit_usd": 0,
                 "namespace": NAMESPACES["RESEARCH"], "max_http_attempts": 7956}
        changes = ({}, {"manual_launch_only": False}, {"paid_api_allowed": True}, {"spend_limit_usd": 1},
                   {"policy": "pooled"}, {"runtime_sha256": "0"*64}, {"max_http_attempts": 9999})
        for change in changes:
            with self.subTest(change=change), \
                 patch.object(runtime, "require_release", return_value=(parent, parent_grant)), \
                 patch.object(runtime, "anchored", side_effect=lambda _, name: manifest if name == runtime.RUNTIME else {**grant, **change}), \
                 patch.object(runtime, "build_runtime", return_value=manifest), \
                 patch.object(runtime, "check_prefix", return_value={}):
                if change:
                    with self.assertRaises(ValueError): runtime.require(Path("synthetic"))
                else:
                    self.assertEqual(runtime.require(Path("synthetic")), (parent, parent_grant, manifest))


if __name__ == "__main__":
    unittest.main()
