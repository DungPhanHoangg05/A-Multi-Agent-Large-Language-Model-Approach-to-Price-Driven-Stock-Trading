"""Kiểm quota được xác nhận, ranh PIT của control và trần payload trước HTTP."""

from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from core.historical_live_smoke import quota_record, anchored_file, history, budget
from core.historical_evaluation_data import HistoricalData
from core.mt_bicl_prompt import canonical_request

ROOT = Path(__file__).resolve().parents[1]


class LiveSmokeTests(unittest.TestCase):
    """Không đọc key hoặc gọi mạng; mọi quota dùng đúng xác nhận người dùng."""

    def test_free_quota_and_distinct_org_refs(self) -> None:
        quota = quota_record()
        self.assertEqual(quota["independent_organizations"], 5)
        self.assertEqual(quota["spend_limit_usd"], 0)
        self.assertFalse(quota["paid_api_allowed"])
        self.assertFalse(quota["split_token_limits"])
        self.assertEqual(len(set(quota["organization_refs"].values())), 5)
        self.assertTrue(all(v == {"rpm": 30, "rpd": 1000, "tpm": 8000, "tpd": 200000} for v in quota["models"].values()))

    def test_unanchored_file_cannot_authorize_smoke(self) -> None:
        with patch("core.historical_live_smoke.subprocess.check_output", return_value=b"wrong"):
            with self.assertRaises(ValueError):
                anchored_file(ROOT, Path("docs/plan/week11/historical_evaluation_validation.json"))

    def test_control_history_never_opens_grid_or_unmatured_labels(self) -> None:
        rows = [{"id": "old", "symbol": "FPT", "date": "2022-06-01", "exit_date": "2022-06-06"},
                {"id": "grid", "symbol": "FPT", "date": "2022-06-02", "exit_date": "2022-06-07"},
                {"id": "equal", "symbol": "FPT", "date": "2022-06-03", "exit_date": "2022-07-01"}]
        label = Mock(return_value={"entry_date": "2022-06-02", "exit_date": "2022-06-06", "r_net": .04, "y": 1})
        module = SimpleNamespace(is_bullish=lambda value: value == "BULLISH")
        data = SimpleNamespace(inputs={"history": rows}, by_day={("FPT", "2022-06-02"): {}},
                               label=label, scope=SimpleNamespace(module=lambda _: module))
        signal = {"trend": "BULLISH", "pattern": "BULLISH", "alpha_consensus": "BULLISH",
                  "indicator_consensus": "BULLISH", "sentiment": "NEUTRAL"}
        with patch("core.historical_live_smoke.signals", return_value=signal):
            result = history(data, SimpleNamespace(get=lambda *a, **k: "BULL"),
                             {"symbol": "FPT", "date": "2022-07-01"}, {})
        self.assertEqual([r["episode_id"] for r in result], ["old"])
        label.assert_called_once()
        self.assertFalse(label.call_args.kwargs["forecast_done"]("anything"))

    def test_oversized_wire_is_blocked_before_http(self) -> None:
        data = HistoricalData(ROOT)
        shared = {"stock_name": "FPT", "as_of_date": "2023-07-03", "time_frame": "1d", "language": "vi", "is_backtest": True,
                  **{name + "_report": "Control." for name in ("indicator", "pattern", "trend", "alpha", "sentiment")}}
        request = canonical_request(shared, "", {"decision": data.protocol["inference"]["config"]})
        request["messages"][0]["content"] = "X" * 100000
        with self.assertRaisesRegex(ValueError, "TPM"):
            budget(request)

    def test_anonymous_reply_schema_roundtrips_real_sdk_without_mutating_contract(self) -> None:
        import json
        import httpx
        from copy import deepcopy
        from langchain_groq import ChatGroq
        from core.historical_evaluation_clients import sdk_schema
        from mt_bicl_support import reply, packet
        data = HistoricalData(ROOT)
        schema = data.scope.module("mt_bicl_contracts").wire_schema()["$defs"]["reply"]
        original = deepcopy(schema)
        expected = reply(packet("FPT-2023-01-06"), anchor=True)
        bodies = []
        def response(request: httpx.Request) -> httpx.Response:
            bodies.append(json.loads(request.content))
            return httpx.Response(200, json={"id": "mock-sdk-schema", "model": "openai/gpt-oss-20b", "created": 1,
                "object": "chat.completion", "choices": [{"index": 0, "finish_reason": "stop", "message": {
                    "role": "assistant", "content": json.dumps(expected)}}]})
        with httpx.Client(transport=httpx.MockTransport(response)) as http:
            llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0, max_tokens=960, max_retries=0,
                           api_key="MOCK_NOT_A_CREDENTIAL", http_client=http)
            result = llm.with_structured_output(sdk_schema(schema), method="json_schema", include_raw=True).invoke("Control SDK.")
        self.assertEqual(result["parsed"], expected)
        self.assertEqual(schema, original)
        self.assertEqual(bodies[0]["response_format"]["json_schema"]["name"], "UtilityICLReply")
        adapted = sdk_schema(schema)
        del adapted["title"]
        self.assertEqual(adapted, schema)

    def test_named_legacy_schema_remains_byte_semantically_identical(self) -> None:
        from core.historical_evaluation_clients import sdk_schema
        from agents.decision_agent import TradeDecisionOutput
        schema = TradeDecisionOutput.model_json_schema()
        self.assertEqual(sdk_schema(schema), schema)


if __name__ == "__main__":
    unittest.main()
