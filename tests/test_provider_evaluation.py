"""Kiểm routing, schema, pairing, PIT và resume qua HTTP giả lập."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import httpx

from core.evaluation_bicl import bank_records, bind_bank, refresh_bank
from core.evaluation_results import compare
from core.evaluation_transport import DECISION, LUNA, VISION, EvaluationCalls, ProviderHTTP, provider_body, usage_totals
from core.historical_evaluation_journal import load, save
from core.mt_bicl_decision import OUTPUT_MARKER
from core.serving_runtime.quota import Failed, Quota, Unknown
from core.unified_execution import StageBook
from scripts.run_provider_evaluation import ROOT, checkpoint_identity, collect, export, freeze, plan

VISION_REPLY = """**Mô hình:** Dao động trong biên hẹp.
**Độ tin cậy:** Trung bình
**Thiên lệch dự báo:** Trung tính
**Bằng chứng:** Các nến có thân nhỏ và đóng cửa trong cùng vùng giá.
**Nến quan trọng:** Nến cuối thân ngắn.
**Hàm ý giao dịch:** Theo dõi.
**Hướng xu hướng:** Đi ngang
**Mức hỗ trợ:** 28
**Mức kháng cự:** 32
**Độ dốc đường xu hướng:** Đi ngang
**Giá so với hỗ trợ:** Giữ trên hỗ trợ
**Phân tích chi tiết:** Các nến dao động ở giữa hai biên giá.
"""


def mock_reply(body: dict, action: str) -> httpx.Response:
    """Tạo đúng schema, có fact assertions lấy từ chính prompt."""
    content = VISION_REPLY
    if "response_format" in body:
        values = {"decision": action, "forecast_horizon": "T+2.5", "confidence": "Cao", "risk_reward_ratio": 1.,
                  "evidence_for": "Đối chứng.", "evidence_against": "Đối chứng.", "justification": "Đối chứng."}
        schema = body["response_format"]["json_schema"]["schema"]
        if "fact_ids" in schema["properties"]:
            template = json.loads(body["messages"][0]["content"].rsplit(OUTPUT_MARKER, 1)[1])
            values.update({k: template[k] for k in ("version", "fact_ids", "fact_assertions", "context_reason")})
        content = json.dumps(values, ensure_ascii=False)
    return httpx.Response(200, json={"choices": [{"message": {"content": content}}],
                                    "usage": {"prompt_tokens": 16, "completion_tokens": 4, "total_tokens": 20}})


class ProviderEvaluationTests(unittest.TestCase):
    """Không mở socket, kể cả khi runner dựng chart và tài nguyên thật."""

    def setUp(self) -> None:
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)
        network = patch("socket.socket.connect", side_effect=AssertionError("Kiểm thử phải ngoại tuyến"))
        network.start()
        self.addCleanup(network.stop)

    def calls(self, directory: Path, provider: str, book: StageBook, handler, **kwargs) -> EvaluationCalls:
        """Dùng client thực với transport MockTransport, key chỉ là fixture."""
        sender = ProviderHTTP(provider, "fixture", transport=httpx.MockTransport(handler))
        self.addCleanup(sender.close)
        return EvaluationCalls(directory, book.signature, Quota(directory/"quota.sqlite", limits=None),
                               sender, lambda: None, provider=provider, **kwargs)

    def test_full_dry_run_counts_and_same_cohort(self) -> None:
        """Kiểm số lượt từng đợt và tập 852 episode trước mọi dispatch."""
        for name in ("component", "bicl", "followup"):
            _, groq, _ = plan(name, "groq", None)
            _, luna, bank = plan(name, "luna", None)
            self.assertEqual(groq["points"], luna["points"])
            self.assertEqual(len(luna["points"]), 102)
            if name == "component":
                self.assertEqual(luna["calls_by_role"], {"pattern": 120, "trend": 120, "decision": 375})
            elif name == "bicl":
                self.assertEqual(len(bank), 852)
                self.assertEqual(luna["calls_by_role"]["bank_trend"], 852)
            else:
                self.assertEqual(luna["calls_by_role"]["Fact_Anchor"], 306)
                self.assertEqual(luna["calls_by_role"]["MT_BICL"], 189)

    def test_resume_after_raw_and_schema_repair_uses_same_luna(self) -> None:
        """Kiểm 1 raw lỗi, 1 repair thành công, resume không gọi lần thứ ba."""
        body = {"model": DECISION, "max_tokens": 200, "temperature": 1e-8,
                "messages": [{"role": "user", "content": "Mẫu kiểm chứng."}],
                "response_format": {"type": "json_schema", "json_schema": {"name": "Fixture",
                    "schema": {"type": "object", "properties": {"decision": {"type": "string", "enum": ["LONG", "SHORT"]}},
                               "required": ["decision"]}}}}
        requests = []

        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.url.host, "api.openai.com")
            actual = json.loads(request.content)
            self.assertEqual(actual["model"], LUNA)
            self.assertEqual(actual["max_completion_tokens"], 200)
            config = actual["response_format"]["json_schema"]
            self.assertTrue(config["strict"])
            self.assertEqual(config["schema"], {**body["response_format"]["json_schema"]["schema"],
                                                "additionalProperties": False})
            requests.append(actual)
            if len(requests) == 1:
                return httpx.Response(200, json={"choices": [{"message": {"content": "{}"}}]})
            return httpx.Response(200, json={"choices": [{"message": {"content": '{"decision":"LONG"}'}}]})

        def cut(event: str) -> None:
            if event == "raw" and len(requests) == 2:
                raise KeyboardInterrupt

        identity = {"provider": "luna"}
        book = StageBook(self.folder, identity)
        calls = self.calls(self.folder, "luna", book, handler, hook=cut)
        with self.assertRaises(KeyboardInterrupt):
            book.execute("checkpoint", {}, lambda attempt: calls.call("decision", body, attempt)[0])
        book = StageBook(self.folder, identity)
        resumed = self.calls(self.folder, "luna", book, handler)
        self.assertEqual(book.execute("checkpoint", {}, lambda attempt: resumed.call("decision", body, attempt)[0])["decision"], "LONG")
        self.assertEqual(len(requests), 2)
        self.assertTrue(requests[1]["messages"][0]["content"].startswith(body["messages"][0]["content"]))
        self.assertEqual(usage_totals(self.folder, book.signature)["schema_errors"], 1)

    def test_legacy_luna_schema_exhaustion_recovers_in_new_wire_without_resending(self) -> None:
        """Giữ ba raw lỗi 0.8, cùng UUID stage và chỉ gửi thêm qua schema strict."""
        planned = {"provider": "luna"}
        identity = freeze(planned, legacy_schema=True)
        book = StageBook(self.folder, identity)
        slot = "decision/component"
        body = {"model": DECISION, "max_tokens": 200, "messages": [{"role": "user", "content": "Giữ prompt đã khóa."}],
                "response_format": {"type": "json_schema", "json_schema": {"name": "Fixture", "schema": {
                    "type": "object", "properties": {"risk_reward_ratio": {"type": "number", "minimum": 1, "maximum": 5}},
                    "required": ["risk_reward_ratio"]}}}}
        requests = []

        def handler(request: httpx.Request) -> httpx.Response:
            actual = json.loads(request.content)
            requests.append(actual)
            config = actual["response_format"]["json_schema"]
            self.assertEqual(config["schema"]["properties"]["risk_reward_ratio"]["minimum"], 1)
            value = 1.0 if config["strict"] else 0.8
            return httpx.Response(200, json={"choices": [{"message": {"content": json.dumps({"risk_reward_ratio": value})}}]})

        initial = self.calls(self.folder, "luna", book, handler)
        legacy = provider_body("luna", body, strict=False)
        with self.assertRaisesRegex(Failed, "ATTEMPT_CAP_EXHAUSTED"):
            book.execute(slot, {}, lambda attempt: initial.wire.call(slot, legacy, attempt)[0])
        original_path, original_rows = initial.wire._rows(slot)
        original_raw = original_path.read_bytes()
        self.assertEqual(len(requests), 3)
        resumed_identity, upgrade = checkpoint_identity(self.folder, planned)
        self.assertEqual(resumed_identity, identity)
        self.assertEqual(upgrade["new_response_format"], "json_schema_strict")
        resumed = StageBook(self.folder, resumed_identity)
        calls = self.calls(self.folder, "luna", resumed, handler, legacy_schema=True)
        result = resumed.execute(slot, {}, lambda attempt: calls.call(slot, body, attempt)[0])
        self.assertEqual(result, {"risk_reward_ratio": 1.0})
        self.assertEqual(len(requests), 4)
        self.assertTrue(requests[-1]["response_format"]["json_schema"]["strict"])
        self.assertEqual(requests[-1]["messages"], body["messages"])
        self.assertEqual(original_path.read_bytes(), original_raw)
        _, strict_rows = calls.wire._rows(slot + "/strict-schema")
        self.assertEqual(strict_rows[0]["attempt"], original_rows[0]["attempt"])
        self.assertEqual(calls.call(slot, body, strict_rows[0]["attempt"])[0], result)
        self.assertEqual(len(requests), 4)

    def test_strict_wire_retains_unprojected_local_schema_validation(self) -> None:
        """Duy trì kiểm tra trùng fact IDs trong validator gốc và thống kê lỗi."""
        book = StageBook(self.folder, {"provider": "luna"})
        received = []
        body = {"model": DECISION, "max_tokens": 200, "messages": [{"role": "user", "content": "Mẫu"}],
                "response_format": {"type": "json_schema", "json_schema": {"name": "Fixture", "schema": {
                    "type": "object", "properties": {"version": {"const": "v1"}, "facts": {"type": "array",
                        "uniqueItems": True, "items": {"type": "string"}}}, "required": ["version", "facts"]}}}}

        def handler(request: httpx.Request) -> httpx.Response:
            wire = json.loads(request.content)
            received.append(wire)
            schema = wire["response_format"]["json_schema"]["schema"]
            self.assertEqual(schema["properties"]["version"], {"enum": ["v1"], "type": "string"})
            self.assertNotIn("uniqueItems", schema["properties"]["facts"])
            facts = ["a", "a"] if len(received) == 1 else ["a", "b"]
            return httpx.Response(200, json={"choices": [{"message": {"content": json.dumps({"version": "v1", "facts": facts})}}]})

        calls = self.calls(self.folder, "luna", book, handler)
        row = book.execute("point", {}, lambda attempt: calls.call("decision", body, attempt)[0])
        self.assertEqual(row["facts"], ["a", "b"])
        self.assertEqual(len(received), 2)
        self.assertEqual(usage_totals(self.folder, book.signature)["schema_errors"], 1)

    def test_unknown_is_not_resent_automatically(self) -> None:
        """Giữ intent khi mất phản hồi, cho phép resume sau đối soát NOT_SENT."""
        book = StageBook(self.folder, {"provider": "groq"})
        count = 0

        def timeout(_: httpx.Request) -> httpx.Response:
            nonlocal count
            count += 1
            raise httpx.ReadTimeout("offline")

        body = {"model": VISION, "max_tokens": 20, "messages": [{"role": "user", "content": "Mẫu"}]}
        calls = self.calls(self.folder, "groq", book, timeout)
        for _ in range(2):
            with self.assertRaises(Unknown):
                book.execute("point", {}, lambda attempt: {"report": calls.call("vision", body, attempt)[0]})
        self.assertEqual(count, 1)
        _, rows = calls.wire._rows("vision")
        calls.wire.reconcile_not_sent("vision", rows[0]["id"], "Fixture xác nhận request chưa gửi.")
        recovered = self.calls(self.folder, "groq", book, lambda request: mock_reply(json.loads(request.content), "LONG"))
        self.assertIn("Đi ngang", book.execute("point", {}, lambda attempt: {"report": recovered.call("vision", body, attempt)[0]})["report"])

    def test_bank_rejects_exit_at_cutoff_before_render_or_dispatch(self) -> None:
        """Bộ dựng tín hiệu từ chối episode chưa đáo hạn trước mọi gọi model."""
        row = deepcopy(bank_records(ROOT)[0])
        point = {"symbol": "CMG", "cutoff": row["exit_date"]}
        with self.assertRaisesRegex(ValueError, "chưa đáo hạn"):
            refresh_bank(ROOT, None, None, [row], [point])

    def test_rebuilt_bank_preserves_returns_and_updates_signal_dependent_trap(self) -> None:
        """Kiểm 852 chu kỳ, scaler và truy xuất của cả ba nhánh dựa trên giá."""
        study, _, _ = plan("bicl", "luna", None)
        provider = study.provider(None)
        original = provider.bank.base.records
        first = original[0]
        signals = {row["episode_id"]: {key: row["agent_signals"][key] for key in ("pattern", "trend")}
                   for row in original}
        signals[first["episode_id"]]["pattern"] = "BULLISH"
        old_index = provider.bank.index
        bind_bank(provider, self.folder, signals)
        expected = old_index.payload
        expected["provenance"]["bank"]["bank_sha256"] = provider.bank.retriever._bank_sha256
        self.assertEqual(provider.bank.selector.index.payload, expected)
        self.assertNotEqual(provider.bank.index.identity, old_index.identity)
        records = provider.bank.retriever._memory.eligible("2023-07-03", first["symbol"])
        changed = next(row for row in records if row["episode_id"] == first["episode_id"])
        self.assertEqual(changed["agent_signals"]["pattern"], "BULLISH")
        self.assertEqual(changed["outcome"], {**first["outcome"], "was_bull_trap": True})
        self.assertEqual(len(provider.bank.base.records), 852)
        self.assertTrue(all(row["exit_date"] < "2023-07-03" for row in records))
        shared = {"stock_name": "FPT", "as_of_date": "2023-07-03", "time_frame": "1d", "language": "vi",
                  "is_backtest": True, "trend_report": "**Hướng xu hướng:** Tăng",
                  "pattern_report": "**Thiên lệch dự báo:** Trung tính",
                  "indicator_report": "**Đồng thuận chủ đạo:** Tăng", "alpha_report": "Tổng hợp Alpha.",
                  "alpha_factors": [{"signal": "TĂNG"}], "sentiment_report": "Thiếu tin.",
                  "sentiment_data": {"main_sentiment": {"avg_score": None}}}
        regime = provider.regimes.get("2023-07-03")
        for branch in ("C2", "A_tp_pool", "B_semantic"):
            with self.subTest(branch=branch):
                request, trace = provider.bank.request(branch, shared, regime)
                self.assertEqual(request["point_id"], "FPT-2023-07-03")
                self.assertEqual(trace["bank_sha256"], provider.bank.retriever._bank_sha256)

    def test_existing_bank_checkpoint_and_schema_upgrade_keep_identity(self) -> None:
        """Mở checkpoint trước sửa index và giữ receipt schema của lượt đã nâng cấp."""
        planned = {"provider": "luna"}
        previous_binding = freeze(planned, previous_bank_binding=True)
        bicl = self.folder / "binding"
        StageBook(bicl, previous_binding)
        self.assertEqual(checkpoint_identity(bicl, planned), (previous_binding, None))
        before_schema = freeze(planned, legacy_schema=True)
        component = self.folder / "schema"
        StageBook(component, before_schema)
        _, upgrade = checkpoint_identity(component, planned)
        receipt = {**upgrade, "strict_source_sha256": previous_binding["source_sha256"]}
        save(component / "schema_upgrade.json", receipt)
        self.assertEqual(checkpoint_identity(component, planned), (before_schema, receipt))

    def test_transient_retry_honors_provider_delay(self) -> None:
        """429 giữ cùng slot, đợi đủ Retry-After và gửi lại đúng payload."""
        now = [100.]
        requests = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request.content)
            if len(requests) == 1:
                return httpx.Response(429, headers={"Retry-After": "12"}, json={"error": "quota"})
            self.assertGreaterEqual(now[0], 112.)
            return mock_reply(json.loads(request.content), "LONG")

        book = StageBook(self.folder, {"provider": "luna"})
        calls = self.calls(self.folder, "luna", book, handler, clock=lambda: now[0],
                           wait=lambda until: now.__setitem__(0, until))
        body = {"model": VISION, "max_tokens": 20, "messages": [{"role": "user", "content": "Mẫu"}]}
        book.execute("point", {}, lambda attempt: {"report": calls.call("vision", body, attempt)[0]})
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0], requests[1])

    def test_mock_samples_use_real_study_routes(self) -> None:
        """Hai endpoint, ba study thật, ảnh và prompt thành phần giống từng byte."""
        for name in ("component", "bicl", "followup"):
            bodies, results, predictions = {}, {}, {}
            for provider in (("groq", "luna") if name == "component" else ("luna",)):
                with self.subTest(study=name, provider=provider):
                    study, identity, bank = plan(name, provider, 1)
                    identity.update(source_sha256="fixture", runtime={})
                    if name == "followup":
                        # Điểm FIN09 đã xác nhận đủ support cho bước đề xuất sửa hành động.
                        identity["points"] = [next(p for p in study.points if p["id"] == "BHN-2025-10-01")]
                    directory = self.folder/name/provider
                    book = StageBook(directory, identity)
                    actual = bodies[provider] = []

                    def handler(request: httpx.Request) -> httpx.Response:
                        body = json.loads(request.content)
                        assert request.url.host == ("api.openai.com" if provider == "luna" else "api.groq.com")
                        assert body["model"] in ((LUNA,) if provider == "luna" else (VISION, DECISION))
                        actual.append(body)
                        return mock_reply(body, "LONG" if provider == "luna" else "SHORT")

                    calls = self.calls(directory, provider, book, handler)
                    with redirect_stdout(io.StringIO()):
                        results[provider] = collect(directory, identity, study, bank, calls, book)
                    predictions[provider] = load(directory/"predictions.json")
                    self.assertTrue(book.complete("point/" + identity["points"][0]["id"]))
                    self.assertGreater(results[provider]["usage"]["estimated_cost_usd"], 0)
                    if name != "component":
                        self.assertEqual(len([r for r in predictions[provider] if r["method"] == "Fact_Anchor"]), 3)
                        self.assertEqual(len({r.get("shared_sha256") for r in predictions[provider] if r.get("shared_sha256")}), 1)
                    if name == "followup":
                        self.assertEqual(sum(r["llm_response"] for r in predictions[provider] if r["method"] == "MT_BICL"), 3)
            if name == "component":
                self.assertEqual([b["messages"] for b in bodies["groq"]], [b["messages"] for b in bodies["luna"]])
                report = compare(results["groq"], results["luna"], predictions["groq"], predictions["luna"])
                self.assertEqual(sum(r["groq_cash_to_luna_long"] for r in report["comparison"]), 2)
                with redirect_stdout(io.StringIO()):
                    export(self.folder/name)
                self.assertTrue((self.folder/name/"comparison.csv").is_file())


if __name__ == "__main__":
    unittest.main()
