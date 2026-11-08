"""Kiểm SDK wire, budget3, raw durable và credential scope bằng MockTransport."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import httpx

from core.groq_pacing import GroqPacer
from core.historical_evaluation_audit import verify_decision
from core.historical_evaluation_clients import Clients
from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_graph import factor_lines
from core.historical_evaluation_journal import RunBook
from core.mt_bicl_prompt import canonical_request

ROOT = Path(__file__).resolve().parents[1]


class MockClock:
    """Thời gian provider giả, không sleep thật trong test429."""
    def __init__(self) -> None:
        self.now = 1790000000.
    def __call__(self) -> float:
        return self.now
    def sleep(self, seconds: float) -> None:
        self.now += seconds


class TransportTests(unittest.TestCase):
    """Mọi HTTP đều chạy trong RAM, không đọc key thật hoặc liên hệ Groq."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = HistoricalData(ROOT)

    def exercise(self, refused: int = 0, *, fail_transport: bool = False, graph: bool = False) -> tuple[dict, str, int]:
        """Dùng serializer ChatGroq thật trên transport mock và ledger tạm."""
        with tempfile.TemporaryDirectory() as folder:
            book = RunBook(Path(folder), {"mock_transport": True})
            calls = []
            reply = {"decision": "SHORT", "forecast_horizon": "T+2.5", "confidence": "Thấp", "risk_reward_ratio": 1.,
                     "evidence_for": "Mock.", "evidence_against": "Mock.", "justification": "Không gọi provider."}
            def respond(request: httpx.Request) -> httpx.Response:
                """Giả lập 429 hoặc response200, không gửi socket."""
                calls.append(json.loads(request.content))
                if fail_transport:
                    raise httpx.ReadTimeout("Timeout mock", request=request)
                if len(calls) <= refused:
                    return httpx.Response(429, headers={"retry-after": "61"},
                        json={"error": {"message": "retry after 61 seconds", "type": "rate_limit_exceeded"}})
                return httpx.Response(200, json={"id": "mock-response", "model": calls[-1]["model"], "created": 1790000000,
                    "object": "chat.completion", "choices": [{"index": 0, "finish_reason": "stop",
                    "message": {"role": "assistant", "content": "Graph mock." if graph else json.dumps(reply)}}],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}})
            clock = MockClock()
            def pacer(path: Path, **kwargs: object) -> GroqPacer:
                return GroqPacer(path, clock=clock, monotonic=clock, sleep=clock.sleep, **kwargs)
            shared = {"stock_name": "CMG", "as_of_date": "2023-07-03", "time_frame": "1d", "is_backtest": True,
                "language": "vi", **{name + "_report": "Báo cáo mock." for name in ("indicator", "pattern", "trend", "sentiment")},
                "alpha_report": "\n".join(factor_lines([{"id": i, "name": f"Factor{i}", "value": .1, "signal": "TĂNG"} for i in range(1, 6)]))}
            request = canonical_request(shared, "", {"decision": self.data.protocol["inference"]["config"]})
            with patch("core.historical_evaluation_clients.require_release", return_value={"mode": "RESEARCH"}), \
                    patch("core.historical_evaluation_audit.verify_runtime"), \
                    patch("core.historical_evaluation_clients.GroqPacer", side_effect=pacer), \
                    patch("core.historical_evaluation_clients.httpx.HTTPTransport", side_effect=lambda **_: httpx.MockTransport(respond)), \
                    patch.dict("os.environ", {"GROQ_ORG_1_API_KEY": "fixture-key-not-a-secret"}):
                clients = Clients(self.data, book)
                if graph:
                    from langchain_core.messages import HumanMessage
                    from agents.decision_agent import _invoke_with_retry
                    from core.historical_evaluation_audit import verify_graph
                    def node(model: object) -> object:
                        """Giữ node test độc lập với parser vision để kiểm body replay."""
                        return lambda state: {"pattern_report": _invoke_with_retry(model.invoke,
                            [HumanMessage(content=state["prompt"])]) .content}
                    state = {"prompt": "Graph mock input."}
                    live = node(clients.models(1)[1])
                    output = book.execute("graph", state, lambda a: clients.stage("pattern", a, "CMG-2023-07-03/u0", live, state))
                    checker = RunBook(Path(folder), {"mock_transport": True}, verify_only=True)
                    with patch("agents.pattern_agent.create_pattern_agent", side_effect=lambda a, model, toolkit: node(model)):
                        verify_graph(checker, "pattern", "graph", state, output,
                                     self.data.protocol["inference"]["config"], fixture=False)
                        with self.assertRaises(ValueError):
                            verify_graph(checker, "pattern", "graph", {"prompt": "Changed."}, output,
                                         self.data.protocol["inference"]["config"], fixture=False)
                elif fail_transport or refused >= 3:
                    with self.assertRaises(BaseException):
                        book.execute("decision", {"request": request}, lambda a: clients.decision(1, request, a, "Original_common"))
                    output = {"stopped": True}
                else:
                    output = book.execute("decision", {"request": request}, lambda a: clients.decision(1, request, a, "Original_common"))
                    verify_decision(book, output, "Original_common", fixture=False, request=request)
                ledger = json.loads((book.directory / "usage/org1.json").read_bytes())
                serialized = json.dumps(ledger)
                self.assertNotIn("fixture-key-not-a-secret", serialized)
                self.assertTrue(all(row.get("credential_scope") for row in ledger["requests"]))
                for pair in clients.cached.values():
                    pair[0].http_client.close()
                return output, serialized, len(calls)

    def test_sdk_canonical_body_and_raw_response(self) -> None:
        output, _, count = self.exercise()
        self.assertEqual(output["reply"]["decision"], "SHORT")
        self.assertEqual(count, 1)

    def test_429_respects_provider_wait_and_shared_three_attempt_budget(self) -> None:
        output, _, count = self.exercise(refused=2)
        self.assertEqual(count, 3)
        self.assertEqual(output["reply"]["decision"], "SHORT")

    def test_three_rejections_stop_and_transport_timeout_is_not_retried(self) -> None:
        self.assertEqual(self.exercise(refused=3)[2], 3)
        self.assertEqual(self.exercise(fail_transport=True)[2], 1)

    def test_graph_cold_replay_rebuilds_wire_and_rejects_changed_prompt(self) -> None:
        output, _, count = self.exercise(graph=True)
        self.assertEqual(output["pattern_report"], "Graph mock.")
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
