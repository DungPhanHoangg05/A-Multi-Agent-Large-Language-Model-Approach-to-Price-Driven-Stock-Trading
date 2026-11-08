"""Reset10054 phục hồi hữu hạn, mỗi HTTP vẫn có reserve/UUID/ledger riêng."""

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import httpx

from core.groq_pacing import GroqPacer, PilotStop
from core.historical_evaluation_clients import RawHTTP, EXPECTED
from core.historical_evaluation_journal import RunBook, load
from core.historical_transport_observer import RECOVERY_POLICY, observe_transport
from core.improvement_transport import ImprovementTransport, SLOT
from core.research_invocation import ENABLED, invocation_scope

ROOT = Path(__file__).resolve().parents[1]
BODY = {"model": "qwen/qwen3.8-27b", "messages": [{"role": "user", "content": "CONTROL"}],
        "temperature": 0., "max_tokens": 960, "stream": False}


class RecoveryTests(unittest.TestCase):
    """Không gọi mạng, sleep thật hoặc đọc credential; clock/HTTP đều fixture."""

    def fixture(self, outcomes: list[str]) -> SimpleNamespace:
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        base = Path(folder.name)
        book = RunBook(base, {"scope": "MOCK_RESET_ONLY"})
        clock = SimpleNamespace(now=1790000000.)
        def advance(seconds: float) -> None:
            clock.now += seconds
        pacer = GroqPacer(base / "usage/org1.json", policy="request_admission_v2",
                         clock=lambda: clock.now, monotonic=lambda: clock.now, sleep=advance)
        pacer.historical_org, pacer.historical_scope = 1, "MOCK_SCOPE"
        clients = SimpleNamespace(book=book, data=SimpleNamespace(root=ROOT, verify_sources=lambda: None),
                                  http_count=0, attempt_cap=100)
        state = SimpleNamespace(book=book, pacer=pacer, calls=[], waits=[], inputs={"point": "fixture"})
        def respond(request: httpx.Request) -> httpx.Response:
            state.calls.append((request.content, dict(request.extensions["timeout"])))
            outcome = outcomes[min(len(state.calls) - 1, len(outcomes) - 1)]
            if outcome == "reset":
                cause = ConnectionResetError(10054, "SECRET_DO_NOT_LOG")
                cause.winerror = 10054
                raise httpx.ReadError("SECRET_DO_NOT_LOG") from cause
            if outcome == "timeout":
                raise httpx.ReadTimeout("SECRET_DO_NOT_LOG")
            if outcome == "mutate_reset":
                state.inputs["changed"] = True
                raise httpx.ReadError("fixture") from ConnectionResetError(10054, "fixture")
            if outcome == "429":
                return httpx.Response(429, headers={"retry-after": "1"}, json={"error": {"message": "retry after 1s"}})
            return httpx.Response(200, json={"choices": [{"message": {"content": "fixture"}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}})
        def run(recover: bool = True) -> dict:
            def wait(seconds: float) -> None:
                state.waits.append(seconds)
                advance(seconds)
            with patch("core.historical_transport_observer.source_bindings", return_value={}), \
                    patch("core.historical_evaluation_audit.verify_runtime"), \
                    patch("core.historical_transport_observer.sleep", side_effect=wait), \
                    observe_transport(ROOT, recover_connection_reset=recover):
                transport = ImprovementTransport(pacer, RawHTTP(clients, pacer, httpx.MockTransport(respond)))
                def invoke(attempt: str) -> dict:
                    enabled = ENABLED.set(True)
                    token = EXPECTED.set({"role": "trend", "images": []})
                    slot = SLOT.set({"run_signature": book.signature, "point_id": "fixture", "branch_id": "trend",
                                     "checkpoint_attempt_id": attempt})
                    try:
                        with invocation_scope("trend") as budget:
                            budget.run_signature, budget.point_id = book.signature, "fixture"
                            budget.branch_id, budget.checkpoint_attempt_id = "trend", attempt
                            request = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions", json=BODY,
                                                    extensions={"timeout": {"read": None}})
                            return transport.handle_request(request).json()
                    finally:
                        EXPECTED.reset(token); SLOT.reset(slot); ENABLED.reset(enabled)
                return book.execute("fixture/trend", state.inputs, invoke)
        state.run = run
        return state

    def test_two_resets_then_success_preserves_body_all_reserves_and_uuid_history(self) -> None:
        state = self.fixture(["reset", "reset", "ok"])
        state.run()
        rows = state.pacer.state["requests"]
        self.assertEqual([r["status"] for r in rows], ["transport_error", "transport_error", 200])
        self.assertEqual(len({body for body, _ in state.calls}), 1)
        self.assertTrue(all(timeout == RECOVERY_POLICY["timeouts"] for _, timeout in state.calls))
        self.assertTrue(all(r["reserved_tokens"] > 0 and r["historical_transport_policy"] for r in rows))
        attempts = load(state.book.path("fixture/trend"))["attempts"]
        self.assertEqual(len(attempts), 3)
        self.assertTrue(all(a["authorization"] for a in attempts[:2]))
        self.assertEqual(attempts[-1]["status"], "complete")
        self.assertEqual(state.waits, [5., 10.])

    def test_three_resets_stop_without_fourth_request_or_authorizing_last(self) -> None:
        state = self.fixture(["reset"])
        with self.assertRaises(PilotStop): state.run()
        self.assertEqual(len(state.calls), 3)
        self.assertIsNone(load(state.book.path("fixture/trend"))["attempts"][-1]["authorization"])

    def test_429_and_reset_share_three_http_cap_across_invocations(self) -> None:
        state = self.fixture(["reset", "429", "429", "ok"])
        with self.assertRaises(PilotStop): state.run()
        self.assertEqual(len(state.calls), 3)
        self.assertEqual(len(state.pacer.state["requests"]), 3)

    def test_timeout_is_not_automatically_replayed(self) -> None:
        state = self.fixture(["timeout", "ok"])
        with self.assertRaises(PilotStop): state.run()
        self.assertEqual(len(state.calls), 1)
        self.assertEqual(state.waits, [])

    def test_existing_unknown_is_not_reconciled_by_new_process_policy(self) -> None:
        state = self.fixture(["reset", "ok"])
        with self.assertRaises(PilotStop): state.run(recover=False)
        with self.assertRaisesRegex(ValueError, "UNKNOWN"): state.run()
        self.assertEqual(len(state.calls), 1)

    def test_old_attempts_count_towards_total_cap_after_manual_reconcile(self) -> None:
        state = self.fixture(["reset"])
        with self.assertRaises(PilotStop): state.run(recover=False)
        attempt = load(state.book.path("fixture/trend"))["attempts"][-1]["attempt_id"]
        state.book.reconcile(attempt, "Operator đã kiểm và cho phép tiếp tục")
        with self.assertRaises(PilotStop): state.run()
        self.assertEqual(len(state.calls), 3)

    def test_changed_inputs_prevent_auto_authorization(self) -> None:
        state = self.fixture(["mutate_reset", "ok"])
        with self.assertRaises(PilotStop): state.run()
        self.assertEqual(len(state.calls), 1)
        self.assertIsNone(load(state.book.path("fixture/trend"))["attempts"][-1]["authorization"])

    def test_fresh_tcp_transport_disables_keepalive_and_hidden_retries(self) -> None:
        with patch("core.historical_transport_observer.source_bindings", return_value={}), \
                patch("core.historical_transport_observer.httpx.HTTPTransport", return_value=Mock()) as factory, \
                observe_transport(ROOT, recover_connection_reset=True):
            RawHTTP(Mock(), Mock())
            self.assertEqual(factory.call_args.kwargs["retries"], 0)
            self.assertEqual(factory.call_args.kwargs["limits"].max_keepalive_connections, 0)


if __name__ == "__main__":
    unittest.main()
