"""Failure injection U07 trên raw boundary, cap chung, quota pooled và paired barrier."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx

from core.historical_evaluation_journal import load
from core.unified_contracts import digest
from core.unified_execution import PairedStudyRunner, verify_execution
from core.unified_execution_transport import (DurableCalls, MockHTTP, Deferred, Uncertain, Exhausted,
                                               body_for, wire_state)
from core.unified_methods import resolve, validate_prepared
from core.unified_protocol import ordered_branches
from scripts.check_unified_execution import control_response
from test_unified_experiment import UnifiedFixture


class Crash(BaseException):
    """Mô phỏng tiến trình mất điện, không được helper legacy catch thành fallback."""


class ExecutionRecoveryTests(unittest.TestCase):
    """Hành vi có hệ quả kinh tế: không gửi trùng, không hụt slot hoặc biến lỗi thành CASH."""
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.fx = UnifiedFixture(self.root, repeats=3)
        self.request = self.fx.methods().prepare("original_common", self.fx.snapshot, {}, 0)["request"]
        self.body = body_for(self.request)
        self.now = [2000000000.]
        self.sent = []

    def calls(self, handler: object = None, hook: object = None, history: dict | None = None,
              signature: str = "a"*64) -> DurableCalls:
        def send(request: httpx.Request) -> httpx.Response:
            self.sent.append(json.loads(request.content))
            return (handler or control_response)(request)
        return DurableCalls(self.root / "run", signature, "U07_TEST", MockHTTP(send),
                            history or {i: [] for i in range(1, 6)}, lambda: self.now[0], hook or (lambda _: None))

    def advance(self, function: object) -> object:
        for _ in range(20):
            try:
                return function()
            except Deferred as error:
                self.now[0] = max(self.now[0] + .01, error.until)
        self.fail("Không hội tụ sau deferred")

    def test_pure_body_matches_actual_sdk_serializer(self) -> None:
        from core.historical_evaluation_audit import serializer, serialized_body
        for preparation in self.fx.bundle()["preparations"].values():
            request = preparation["request"]
            if request is not None:
                expected = serialized_body(serializer(request), request["messages"][0]["content"], request["structured"]["schema"])
                self.assertEqual(body_for(request), expected)

    def test_intent_crash_requires_uuid_reconcile_and_preserves_reserve(self) -> None:
        def crash(phase: str) -> None:
            if phase == "intent":
                raise Crash()
        calls = self.calls(hook=crash)
        with self.assertRaises(Crash): calls.call("slot", 1, self.body, "attempt")
        resumed = self.calls()
        with self.assertRaises(Uncertain): resumed.call("slot", 1, self.body, "attempt")
        self.assertEqual(len(self.sent), 0)
        first = resumed.state["rows"][0]
        resumed.reconcile_not_sent(first["id"], "Injection dừng ngay sau fsync, trước sender")
        self.advance(lambda: resumed.call("slot", 1, self.body, "attempt"))
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(len(resumed.state["rows"]), 2)
        self.assertEqual(resumed.state["rows"][0]["reserved_tokens"], first["reserved_tokens"])

    def test_success_before_checkpoint_replays_same_raw_uuid_without_new_send(self) -> None:
        def crash(phase: str) -> None:
            if phase == "raw": raise Crash()
        calls = self.calls(hook=crash)
        with self.assertRaises(Crash): calls.call("slot", 1, self.body, "attempt")
        saved_id = calls.state["rows"][0]["id"]
        reply, row = self.calls().call("slot", 1, self.body, "attempt")
        self.assertEqual(reply["decision"], "SHORT")
        self.assertEqual(row["id"], saved_id)
        self.assertEqual(len(self.sent), 1)

    def test_timeout_after_dispatch_stays_unknown_without_automatic_resend(self) -> None:
        def timeout(request: httpx.Request) -> httpx.Response:
            raise httpx.ReadTimeout("CONTROL_ONLY", request=request)
        with self.assertRaises(Uncertain): self.calls(timeout).call("slot", 1, self.body, "attempt")
        with self.assertRaises(Uncertain): self.calls().call("slot", 1, self.body, "attempt")
        self.assertEqual(len(self.sent), 1)

    def test_schema_repair_and_429_share_cap_across_new_instances(self) -> None:
        sequence = [429, 200, 200]
        def handler(request: httpx.Request) -> httpx.Response:
            status = sequence.pop(0)
            if status == 429:
                return httpx.Response(429, headers={"retry-after": "9"}, text="retry after 17 seconds")
            if len(sequence) == 1:
                return httpx.Response(200, json={"choices": [{"message": {"content": "{}"}}]})
            return control_response(request)
        calls = self.calls(handler)
        with self.assertRaises(Deferred) as caught: calls.call("slot", 1, self.body, "attempt")
        self.assertGreaterEqual(caught.exception.until, self.now[0] + 17)
        self.now[0] = caught.exception.until + 61
        reply, row = self.advance(lambda: self.calls(handler).call("slot", 1, self.body, "attempt"))
        self.assertEqual(reply["decision"], "SHORT")
        self.assertTrue(row["repair"])
        self.assertEqual(len(self.sent), 3)
        self.assertEqual(self.sent[0], self.sent[1])
        self.assertNotEqual(self.sent[1]["messages"], self.sent[2]["messages"])

    def test_three_invalid_schemas_stop_without_fourth_attempt_or_action(self) -> None:
        invalid = lambda _: httpx.Response(200, json={"choices": [{"message": {"content": "{}"}}]})
        with self.assertRaises(Exhausted):
            self.advance(lambda: self.calls(invalid).call("slot", 1, self.body, "attempt"))
        self.assertEqual(len(self.sent), 3)

    def test_org_or_epoch_or_request_drift_is_rejected_on_resume(self) -> None:
        calls = self.calls()
        calls.call("slot", 1, self.body, "attempt")
        with self.assertRaises(ValueError): calls.call("slot", 2, self.body, "attempt")
        with self.assertRaises(ValueError): calls.call("slot", 1, {**self.body, "temperature": .5}, "attempt")
        with self.assertRaises(ValueError):
            DurableCalls(self.root / "run", "a"*64, "OTHER_EPOCH", MockHTTP(control_response),
                         {i: [] for i in range(1, 6)}, lambda: self.now[0])

    def test_pooled_models_daily_carry_and_unknown_survive_resume(self) -> None:
        history = {i: [] for i in range(1, 6)}
        history[1] = [{"id": str(i), "model": "qwen/qwen3.8-27b", "started_at": self.now[0]-100,
                       "reserved_tokens": 8000, "status": "UNKNOWN"} for i in range(25)]
        calls = self.calls(history=history)
        with self.assertRaises(Deferred): calls.call("slot", 1, self.body, "attempt")
        self.assertEqual(len(self.sent), 0)
        calls.call("other-org", 2, self.body, "attempt")
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(len(self.calls(history=history).state["carry"]), 25)

    def test_provider_lower_limit_stops_and_remaining_reset_defers(self) -> None:
        calls = self.calls(lambda r: httpx.Response(200, headers={"x-ratelimit-limit-tokens": "4000"},
                                                   content=control_response(r).content))
        calls.call("slot", 1, self.body, "attempt")
        with self.assertRaises(Exhausted): calls.call("slot2", 1, self.body, "attempt2")

    def test_raw_transient_crash_reconstructs_retry_after_before_new_send(self) -> None:
        def crash(phase: str) -> None:
            if phase == "raw": raise Crash()
        calls = self.calls(lambda _: httpx.Response(503, headers={"retry-after": "90"}, text="CONTROL unavailable"), hook=crash)
        with self.assertRaises(Crash): calls.call("slot", 1, self.body, "attempt")
        with self.assertRaises(Deferred) as caught: self.calls().call("slot", 1, self.body, "attempt")
        self.assertGreaterEqual(caught.exception.until, self.now[0] + 90)
        self.assertEqual(len(self.sent), 1)

    def test_provider_remaining_tokens_obeys_reset_without_model_hotswap(self) -> None:
        calls = self.calls(lambda r: httpx.Response(200, headers={"x-ratelimit-remaining-tokens": "0",
            "x-ratelimit-reset-tokens": "2m"}, content=control_response(r).content))
        calls.call("slot", 1, self.body, "attempt")
        with self.assertRaises(Deferred) as caught: calls.call("slot2", 1, self.body, "attempt2")
        self.assertGreaterEqual(caught.exception.until, self.now[0] + 120)
        self.assertEqual(len(self.sent), 1)

    def test_usage_underestimate_stays_stopped_after_raw_crash_and_resume(self) -> None:
        def response(request: httpx.Request) -> httpx.Response:
            value = control_response(request).json()
            value["usage"]["total_tokens"] = 9000
            return httpx.Response(200, json=value)
        with self.assertRaises(Exhausted): self.calls(response).call("slot", 1, self.body, "attempt")
        with self.assertRaises(Exhausted): self.calls().call("slot", 1, self.body, "attempt")
        self.assertEqual(len(self.sent), 1)

    def test_nonmock_transport_never_opens_legacy_release_or_credentials(self) -> None:
        with self.assertRaises(ValueError):
            DurableCalls(self.root / "run", "a"*64, "U07_TEST", object(),
                         {i: [] for i in range(1, 6)}, lambda: self.now[0])

    def test_process_exit_after_raw_fsync_replays_without_second_dispatch(self) -> None:
        code = '''
import json,sys,os
from pathlib import Path
value=json.loads(sys.stdin.read())
sys.path.insert(0,value['root'])
import httpx
from core.unified_execution_transport import DurableCalls,MockHTTP
def sender(request):
    if value['resume']:
        raise AssertionError('Không được gửi lại sau raw200')
    return httpx.Response(200,json={'choices':[{'message':{'content':json.dumps(value['reply'])}}]})
def hook(phase):
    if phase=='raw' and not value['resume']:
        os._exit(91)
calls=DurableCalls(Path(value['directory']),'a'*64,'U07_TEST',MockHTTP(sender),
    {i:[] for i in range(1,6)},lambda:2000000000.,hook)
reply,row=calls.call('slot',1,value['body'],'attempt')
print(json.dumps({'id':row['id'],'reply':reply}))
'''
        from mt_bicl_support import original
        value = {"root": str(Path(__file__).resolve().parents[1]), "directory": str(self.root / "process"),
                 "body": self.body, "reply": original(), "resume": False}
        first = subprocess.run([sys.executable, "-I", "-X", "utf8", "-c", code], input=json.dumps(value),
                               text=True, capture_output=True, encoding="utf-8", timeout=60)
        self.assertEqual(first.returncode, 91, first.stderr)
        row = wire_state(self.root / "process")["rows"][0]
        value["resume"] = True
        second = subprocess.run([sys.executable, "-I", "-X", "utf8", "-c", code], input=json.dumps(value),
                                text=True, capture_output=True, encoding="utf-8", timeout=60)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(second.stdout)["id"], row["id"])
        self.assertEqual(len(wire_state(self.root / "process")["rows"]), 1)

    def test_vision_stage_crash_before_save_replays_raw_and_never_dispatches_again(self) -> None:
        from core.unified_execution import StageBook
        from core.historical_evaluation_protocol import digest as stage_digest
        identity = {"scope": "GRAPH_PATTERN_CRASH_CONTROL"}
        calls = self.calls(signature=stage_digest(identity))
        fired = []
        def hook(phase: str) -> None:
            if phase.startswith("before_complete:") and not fired:
                fired.append(1)
                raise Crash()
        book = StageBook(self.root / "run", identity, hook=hook)
        def stage(attempt: str) -> dict:
            reply, row = calls.call("graph/pattern", 1, self.body, attempt)
            return {"pattern_report": reply["justification"], "wire_uuid": row["id"]}
        with self.assertRaises(Crash): book.execute("graph/pattern", {"pit": "locked"}, stage)
        output = StageBook(self.root / "run", identity).execute("graph/pattern", {"pit": "locked"}, stage)
        self.assertEqual(output["wire_uuid"], calls.state["rows"][0]["id"])
        self.assertEqual(len(self.sent), 1)

    def test_counterbalance_full_grid_preserves_dependencies_and_native_positions(self) -> None:
        positions = set()
        for i in range(306):
            order = ordered_branches(i)
            positions.add(order.index("original_fix"))
            self.assertLess(order.index("original_common"), order.index("Fact_Anchor"))
            self.assertLess(order.index("Fact_Anchor"), order.index("MT_BICL"))
            self.assertEqual(len(set(order)), 8)
        self.assertEqual(positions, set(range(8)))

    def paired(self, *, calls_hook: object = None, stage_hook: object = None) -> tuple:
        adapter = self.fx.methods()
        methods = SimpleNamespace(prepare=adapter.prepare, resolve=resolve,
            validate=lambda v, s, p, r: validate_prepared(v, s, p, self.fx.spec["decision"], r))
        identity = {"mode": "CONTROL_ONLY", "repeats": 3, "realizations": 1, "points": [self.fx.point]}
        calls = self.calls(hook=calls_hook, signature=digest(identity))
        runner = PairedStudyRunner(self.root / "run", identity, calls, methods, hook=stage_hook or (lambda _: None))
        return runner, methods, identity

    def test_paired_resume_before_forecast_save_keeps_one_shared_and24_slots(self) -> None:
        upstream_count = []
        upstream = SimpleNamespace(shared=lambda *_: (upstream_count.append(1) or self.fx.snapshot.document()))
        fired = []
        def crash(phase: str) -> None:
            if phase.startswith("before_complete:forecast/") and not fired:
                fired.append(1)
                raise Crash()
        runner, methods, identity = self.paired(stage_hook=crash)
        outcome_count = []
        def outcome(point: dict) -> dict:
            book = __import__("core.unified_execution", fromlist=["StageBook"]).StageBook(runner.directory, identity, verify_only=True)
            self.assertTrue(all(book.complete(f"forecast/{point['id']}/u0/r{r}/{v}") for r in range(3) for v in ordered_branches(r)))
            outcome_count.append(1)
            return {"point_id": point["id"], "status": "WITHHELD_CONTROL_NO_QUERY_PAYOFF"}
        with self.assertRaises(Crash): runner.tick(upstream, outcome)
        self.assertEqual(outcome_count, [])
        runner, methods, identity = self.paired()
        for _ in range(50):
            result = runner.tick(upstream, outcome)
            if result["status"] == "COMPLETE": break
            self.now[0] = max(result["waiting"].values()) + .01
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(upstream_count, [1])
        self.assertEqual(outcome_count, [1])
        sends = len(self.sent)
        runner.tick(upstream, outcome)
        self.assertEqual(len(self.sent), sends)
        with patch("httpx.Client", side_effect=AssertionError("Client bị cấm trong verify")), \
             patch("httpx.HTTPTransport", side_effect=AssertionError("Mạng bị cấm")), \
             patch("langchain_groq.ChatGroq", side_effect=AssertionError("SDK bị cấm")):
            result = verify_execution(runner.directory, identity, methods)
        self.assertEqual(result["forecast_slots"], 24)
        rows = wire_state(runner.directory)["rows"]
        self.assertEqual(len({r["id"] for r in rows}), len(rows))


if __name__ == "__main__":
    unittest.main()
