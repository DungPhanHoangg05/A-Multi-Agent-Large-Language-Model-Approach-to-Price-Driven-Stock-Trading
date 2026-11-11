"""Hồi quy bỏ lịch local, giữ retry provider và nối journal nhiều policy."""
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
from core.unified_execution_transport import MockHTTP, Deferred, Exhausted, Uncertain
from core.unified_experiment import outcome_from_frame
from core.prior_run_lock import PriorRunLock
from core.unified_live.release import NAMESPACES
from core.unified_model_quota.policy import ModelCalls
from core.unified_provider_quota.policy import POLICY, ProviderCalls, admit
from core.unified_provider_quota import runtime
from scripts.check_unified_execution import control_response

GPT = "openai/gpt-oss-20b"
QWEN = "qwen/qwen3.8-27b"


class ProviderTransportTests(transport_tests.LiveTransportTests):
    """Chạy lại máy retry/repair/UNKNOWN U08 qua policy provider response."""
    def calls(self, handler: object = None, *, guard: object = None, identity: dict | None = None) -> ProviderCalls:
        """Tạo lại owner từ journal thật sau mỗi lần resume của fixture."""
        def send(request: httpx.Request) -> httpx.Response:
            self.sent.append(json.loads(request.content))
            return (handler or control_response)(request)
        return ProviderCalls(self.root / "run", identity or self.identity, MockHTTP(send),
                             {i: [] for i in range(1, 6)}, lambda: self.now[0], guard or (lambda: None), test_mode=True)

    def test_success_headers_cannot_schedule_next_request(self) -> None:
        def send(request: httpx.Request) -> httpx.Response:
            response = control_response(request)
            response.headers.update({"x-ratelimit-remaining-requests": "0", "x-ratelimit-remaining-tokens": "0",
                                     "x-ratelimit-reset-requests": "24h", "x-ratelimit-reset-tokens": "24h"})
            return response
        calls = self.calls(send)
        calls.call("forecast/p/first", 1, self.body, "first")
        calls.call("forecast/p/second", 1, self.body, "second")
        self.assertEqual(len(self.sent), 2)

    def test_real429_backoff_is_recorded_and_survives_restart(self) -> None:
        codes = [429, 200]
        def send(request: httpx.Request) -> httpx.Response:
            if codes.pop(0) == 429:
                return httpx.Response(429, headers={"retry-after": "18"}, text="retry after 19 seconds")
            return control_response(request)
        calls = self.calls(send)
        with self.assertRaises(Deferred) as caught: calls.call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(calls.waiting_models[1]["reason"], "PROVIDER_RETRY_AFTER_OR_BACKOFF")
        self.assertEqual(calls.waiting_models[1]["last_http_status"], 429)
        with self.assertRaises(Deferred): self.calls(send).call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(len(self.sent), 1)
        self.now[0] = caught.exception.until + .01
        reply, _ = self.calls(send).call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(reply["decision"], "SHORT")
        self.assertEqual(len(self.sent), 2)

    def test_prior_policy_raw_replays_without_another_http(self) -> None:
        directory = self.root / "run"
        old = ModelCalls(directory, self.identity, MockHTTP(control_response), {i: [] for i in range(1, 6)},
                         lambda: self.now[0], test_mode=True)
        _, row = old.call("forecast/p/v", 1, self.body, "attempt")
        path = directory / "http" / (row["id"] + ".json")
        before = path.read_bytes()
        _, replay = self.calls().call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(replay["id"], row["id"])
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(self.sent, [])


class ProviderAdmissionTests(unittest.TestCase):
    """Chỉ lỗi provider tạo cooldown, lịch sử vẫn được giữ cho kiểm toán."""
    def setUp(self) -> None:
        self.now = 2000000000.

    def row(self, model: str = GPT, *, status: object = 200) -> dict:
        """Raw synthetic đủ dữ kiện để cold tái dựng cooldown ngay sau fsync."""
        return {"org": 1, "body": {"model": model}, "status": status,
                "slot": "forecast/p/v", "started_at": self.now - 1, "completed_at": self.now,
                "reserved_tokens": 8000, "total_tokens": 8000, "headers": {}, "response": ""}

    def test_history_rpm_rpd_tpm_tpd_never_blocks_a_new_request(self) -> None:
        state = {"carry": [{**self.row(), "model": GPT} for _ in range(1000)],
                 "rows": [self.row() for _ in range(1000)]}
        before = deepcopy(state)
        admit(state, 1, GPT, 8000, self.now, 7956)
        self.assertEqual(state, before)

    def test_successful_zero_headers_are_telemetry(self) -> None:
        row = self.row()
        row["headers"] = {"x-ratelimit-remaining-tokens": "0", "x-ratelimit-reset-tokens": "24h"}
        admit({"carry": [], "rows": [row]}, 1, GPT, 8000, self.now, 7956)

    def test_429_and_transient_backoff_are_model_and_org_scoped(self) -> None:
        for code in (429, 500, 502, 503, 504):
            with self.subTest(code=code):
                row = self.row(QWEN, status=code)
                row["headers"] = {"retry-after": "25"}
                state = {"carry": [], "rows": [row]}
                with self.assertRaises(Deferred) as caught: admit(state, 1, QWEN, 1000, self.now, 7956)
                self.assertEqual(caught.exception.until, self.now + 25)
                admit(state, 1, GPT, 1000, self.now, 7956)
                admit(state, 2, QWEN, 1000, self.now, 7956)
                admit(state, 1, QWEN, 1000, caught.exception.until + .01, 7956)

    def test_raw429_before_retry_metadata_reconstructs_provider_delay(self) -> None:
        row = self.row(status=429)
        row["response"] = "retry after 37 seconds"
        with self.assertRaises(Deferred) as caught:
            admit({"carry": [], "rows": [row]}, 1, GPT, 1000, self.now, 7956)
        self.assertEqual(caught.exception.until, self.now + 37)

    def test_later_success_replaces_prior_error_cooldown(self) -> None:
        failed = {**self.row(status=429), "retry_until": self.now + 1000}
        success = {**self.row(), "completed_at": self.now + 1}
        admit({"carry": [], "rows": [failed, success]}, 1, GPT, 1000, self.now + 2, 7956)

    def test_current_unknown_requires_reconcile_but_history_is_retained(self) -> None:
        unknown = self.row(status="UNKNOWN")
        with self.assertRaises(Uncertain): admit({"carry": [], "rows": [unknown]}, 1, GPT, 1000, self.now, 7956)
        admit({"carry": [], "rows": [unknown]}, 2, GPT, 1000, self.now, 7956)
        state = {"carry": [{**unknown, "model": GPT}], "rows": []}
        admit(state, 1, GPT, 1000, self.now, 7956)
        self.assertEqual(state["carry"][0]["status"], "UNKNOWN")

    def test_request_bounds_global_cap_and_bad_provider_delay_fail_closed(self) -> None:
        for org, model, tokens in ((0, GPT, 1000), (1, "other", 1000), (1, GPT, 8001), (1, GPT, True)):
            with self.subTest(values=(org, model, tokens)), self.assertRaises(ValueError):
                admit({"carry": [], "rows": []}, org, model, tokens, self.now, 7956)
        with self.assertRaises(Exhausted): admit({"carry": [], "rows": [self.row()]}, 2, QWEN, 1000, self.now, 1)
        row = {**self.row(status=429), "retry_until": float("nan")}
        with self.assertRaises(ValueError): admit({"carry": [], "rows": [row]}, 1, GPT, 1000, self.now, 7956)

    def test_mixed_policy_cold_verifier_obeys_transition_sequence(self) -> None:
        carry = [{**self.row(), "model": GPT, "started_at": self.now - 3600} for _ in range(25)]
        row = self.row()
        state = {"carry": carry, "rows": [row]}
        runtime.verify_admissions(state, 0, 0, 7956)
        with self.assertRaises(ValueError): runtime.verify_admissions(state, 0, 1, 7956)
        failed = {**self.row(status=429), "started_at": self.now - 2, "completed_at": self.now - 1,
                  "headers": {"retry-after": "30"}}
        with self.assertRaisesRegex(ValueError, "Retry-After"):
            runtime.verify_admissions({"carry": [], "rows": [failed, row]}, 0, 0, 7956)


class ProviderHostedTests(execution_tests.HostedExecutionTests):
    """Paired, barrier và economic fixture chạy với admission mới."""
    def setup(self, phase: str, records: list[dict], *, all_points: bool = False) -> tuple:
        """Dùng cùng dữ liệu/caller U08 và thay riêng transport."""
        runner, upstream, count = super().setup(phase, records, all_points=all_points)
        runner.calls = ProviderCalls(runner.directory, runner.identity, MockHTTP(control_response),
                                     {i: [] for i in range(1, 6)}, lambda: self.now[0], test_mode=True)
        return runner, upstream, count

    def test_partial_never_reports_complete_support(self) -> None:
        runner, upstream, _ = self.setup("RESEARCH", self.records[:2])
        runner.calls.sender = MockHTTP(lambda request: httpx.Response(429, headers={"retry-after": "30"}, text="retry after 30 seconds"))
        result = runner.tick(upstream, lambda _: self.fail("Provider chưa cho đủ24 forecast"))
        self.assertTrue(result["waiting"])
        self.assertEqual(result["complete_points"], 0)
        with self.assertRaises(ValueError): execution_tests.verify(runner.directory, runner.identity, runner.methods)
        partial = execution_tests.verify(runner.directory, runner.identity, runner.methods, require_complete=False)
        self.assertEqual(partial["status"], "PARTIAL_U08")
        self.assertEqual(partial["complete_points"], 0)

    def test_driver_keeps_manager_lock_through_cold_seal(self) -> None:
        runner, upstream, count = self.setup("RESEARCH", self.records[:1])
        save(runner.directory / "status.json", {"phase": "RESEARCH", "status": "PENDING"})
        methods = runner.methods
        methods.shared = upstream.shared
        labels = []
        def outcome(root: Path, point: dict) -> dict:
            labels.append(point["id"])
            frame = pd.DataFrame({"Datetime": pd.bdate_range(point["cutoff"], periods=4), "Open": [100.]*4,
                "High": [120.]*4, "Low": [90.]*4, "Close": [100.,101.,102.,110.], "Volume": [1000.]*4})
            return outcome_from_frame(point, frame, "1"*64)
        def cold(command: list[str], **kwargs: object) -> SimpleNamespace:
            self.assertIn("scripts/unified_provider_quota/run.py", command)
            with self.assertRaises(RuntimeError):
                with PriorRunLock(runner.directory / "manager", digest(runner.identity)):
                    self.fail("Collector phải giữ manager lock")
            with PriorRunLock(runner.directory, digest(runner.identity)):
                result = execution_tests.verify(runner.directory, runner.identity, methods)
            save(runner.directory / "quota_receipt.json", {**result, "quota_policy": POLICY})
            return SimpleNamespace(returncode=0, stdout="SYNTHETIC_COLD_PASS", stderr="")
        with patch.object(runtime, "require", return_value=({}, {"max_http_attempts": 7956}, {"sources": {}})), \
             patch.object(runtime, "run_identity", return_value=runner.identity), \
             patch.object(runtime, "guard_for", return_value=lambda: None), \
             patch.object(runtime, "anchored", return_value={"sources": {}}), \
             patch.object(runtime, "binding", return_value={}), \
             patch.object(runtime, "LiveHTTP", return_value=SimpleNamespace(close=lambda: None)), \
             patch.object(runtime, "ProviderCalls", return_value=runner.calls), \
             patch.object(runtime, "history", return_value={i: [] for i in range(1, 6)}), \
             patch.object(runtime, "carry_smoke", side_effect=lambda root, rows: rows), \
             patch("core.unified_execution_providers.StudyProviders", return_value=methods), \
             patch.object(runtime, "canonical_outcome", side_effect=outcome), \
             patch.object(runtime, "subprocess", SimpleNamespace(run=cold)), \
             patch("builtins.print"):
            result = runtime.collect(self.root)
        self.assertEqual(result["forecast_slots"], 24)
        self.assertEqual(result["quota_policy"], POLICY)
        self.assertEqual(len(labels), 1)
        self.assertEqual(len(count), 1)


class ProviderReleaseTests(unittest.TestCase):
    """Quyền manual/Free và gate trước credential của entrypoint mới."""
    def test_missing_release_rejects_before_any_client(self) -> None:
        with patch.object(runtime, "require", side_effect=ValueError("Thiếu grant")), \
             patch.object(runtime, "LiveHTTP", side_effect=AssertionError("Cấm client")), \
             patch("dotenv.dotenv_values", side_effect=AssertionError("Cấm key")):
            with self.assertRaisesRegex(ValueError, "grant"): runtime.collect(Path("synthetic"))

    def test_grant_cannot_relax_manual_spend_cap_or_parent(self) -> None:
        parent_grant = {"max_http_attempts": 7956}
        manifest = {"prefix": {}}
        grant = runtime.grant_for(manifest, 7956)
        for change in ({}, {"manual_launch_only": False}, {"spend_limit_usd": 1}, {"api": False},
                       {"max_http_attempts": 9999}, {"runtime_sha256": "0"*64}):
            with self.subTest(change=change), \
                 patch.object(runtime.model_runtime, "require", return_value=({}, parent_grant, {})), \
                 patch.object(runtime, "anchored", side_effect=lambda _, name: manifest if name == runtime.RUNTIME else {**grant, **change}), \
                 patch.object(runtime, "build_runtime", return_value=manifest), \
                 patch.object(runtime, "check_prefix", return_value={}):
                if change:
                    with self.assertRaises(ValueError): runtime.require(Path("synthetic"))
                else:
                    self.assertEqual(runtime.require(Path("synthetic")), ({}, parent_grant, manifest))

    def test_stopped_driver_returns_before_reading_credentials(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / NAMESPACES["RESEARCH"]
            identity = {"mode": "HOSTED_TEST", "phase": "RESEARCH", "epoch": "TEST_PROVIDER"}
            save(directory / "status.json", {"status": "STOPPED_BY_OPERATOR", "forecast_complete": 968})
            (directory / "stop.request").write_text("USER", encoding="utf-8")
            with patch.object(runtime, "require", return_value=({}, {}, {})), \
                 patch.object(runtime, "run_identity", return_value=identity), \
                 patch.object(runtime, "LiveHTTP", side_effect=AssertionError("Cấm client")):
                result = runtime.collect(root)
            self.assertEqual(result["status"], "STOPPED_BY_OPERATOR")
            self.assertEqual(result["forecast_complete"], 968)


if __name__ == "__main__":
    unittest.main()
