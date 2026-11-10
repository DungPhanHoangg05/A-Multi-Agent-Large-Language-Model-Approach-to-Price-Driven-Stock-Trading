"""Rào query-y/PIT tại runner U07 và dispatch độc lập trên assets chín mã U06."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx

from core.historical_evaluation_journal import load, save
from core.unified_contracts import SharedSnapshot, digest
from core.unified_execution import PairedStudyRunner, StageBook, verify_execution
from core.unified_execution_transport import DurableCalls, MockHTTP, wire_state
from core.unified_asset_providers import StudyScope
from core.unified_preflight import ASSETS
from core.unified_protocol import read
from scripts.check_unified_execution import control_response

ROOT = Path(__file__).resolve().parents[1]


class ControlMethods:
    """Tài nguyên prepared U06 phục vụ fault fixture; không giả là replay số hoặc hosted."""
    def __init__(self, records: list[dict]) -> None:
        self.saved = {v["point"]["id"]: v for v in records}
        self.module = StudyScope(ROOT).module("unified_methods")
        self.config = read(ROOT, "docs/plan/week11/historical_evaluation_protocol.json", True)["inference"]["config"]
        self.resolve = self.module.resolve
        self.adapters = {}

    def prepare(self, variant: str, snapshot: SharedSnapshot, deps: dict, repeat: int) -> dict:
        point_id = snapshot.document()["point"]["id"]
        saved = self.saved[point_id]
        if point_id not in self.adapters:
            def bank_request(branch: str, shared: dict, regime: str) -> tuple:
                from core.mt_bicl_prompt import canonical_request
                item = saved["preparations"][branch]["prepared"]
                request = item["request"] or canonical_request(shared, "", {"decision": self.config})
                return deepcopy(request), deepcopy(item["trace"])
            self.adapters[point_id] = self.module.MethodAdapters(self.config,
                bank_factory=lambda: SimpleNamespace(request=bank_request), regime=lambda _: saved["regime"],
                facts=lambda _: deepcopy(saved["context"]["advisor"]["query_facts"]),
                context_factory=lambda: SimpleNamespace(build=lambda *_: deepcopy(saved["context"]), variants=lambda _: deepcopy(saved["variants"])))
        return self.adapters[point_id].prepare(variant, snapshot, deps, repeat)

    def validate(self, variant: str, snapshot: SharedSnapshot, prepared: dict, repeat: int) -> None:
        self.module.validate_prepared(variant, snapshot, prepared, self.config, repeat)


class ExecutionLeakageTests(unittest.TestCase):
    """Tấn công ngay biên state/forecast/outcome, không tính payoff thị trường."""
    @classmethod
    def setUpClass(cls) -> None:
        manifest = read(ROOT, ASSETS + "/provider_manifest.json")
        cls.records = [read(ROOT, row["path"]) for row in manifest["points"]]

    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.now = [2000000000.]

    def runner(self, records: list[dict], handler: object = None) -> tuple:
        points = [row["point"] for row in records]
        identity = {"mode": "CONTROL_ONLY", "repeats": 3, "realizations": 1, "points": points}
        calls = DurableCalls(self.directory, digest(identity), "U07_TEST", MockHTTP(handler or control_response),
                             {i: [] for i in range(1, 6)}, lambda: self.now[0])
        methods = ControlMethods(records)
        mapping = {row["point"]["id"]: row["snapshot"] for row in records}
        counts = {p["id"]: 0 for p in points}
        def shared(book: object, point: dict, org: int) -> dict:
            counts[point["id"]] += 1
            return deepcopy(mapping[point["id"]])
        return PairedStudyRunner(self.directory, identity, calls, methods), SimpleNamespace(shared=shared), counts

    def finish(self, runner: PairedStudyRunner, upstream: object) -> dict:
        for _ in range(200):
            result = runner.tick(upstream, lambda p: {"point_id": p["id"], "status": "WITHHELD_CONTROL_NO_QUERY_PAYOFF"})
            if result["status"] == "COMPLETE": return result
            self.assertFalse(result["blocked"])
            self.now[0] = max(self.now[0] + .01, min(result["waiting"].values()))
        self.fail("Lịch không hội tụ")

    def test_all_nine_symbols_keep_query_label_and_future_price_out_of_snapshot(self) -> None:
        symbols = set()
        for row in self.records:
            doc = deepcopy(row["snapshot"])
            symbols.add(doc["point"]["symbol"])
            for key in ("query_y", "label_net", "entry_open", "exit_close", "target"):
                poisoned = deepcopy(doc["payload"])
                poisoned["sentiment_data"]["nested"] = {key: "FUTURE_QUERY"}
                with self.assertRaises(ValueError): SharedSnapshot.create(doc["point"], 0, poisoned, doc["provenance"])
            poisoned = deepcopy(doc["payload"])
            poisoned["price_prefix"]["Datetime"][-1] = "2099-01-01"
            with self.assertRaises(ValueError): SharedSnapshot.create(doc["point"], 0, poisoned, doc["provenance"])
        self.assertEqual(len(symbols), 9)

    def test_dated_future_and_undated_article_raise_instead_of_entering_state(self) -> None:
        doc = self.records[0]["snapshot"]
        for date in (None, "2099-01-01"):
            payload = deepcopy(doc["payload"])
            payload["sentiment_data"]["scored_articles"] = [{"date_parsed": date}]
            with self.assertRaises(ValueError): SharedSnapshot.create(doc["point"], 0, payload, doc["provenance"])

    def test_unknown_in_one_org_leaves_other_org_running_and_label_closed(self) -> None:
        first = []
        def handler(request: httpx.Request) -> httpx.Response:
            if not first:
                first.append(1)
                raise httpx.ReadTimeout("CONTROL timeout", request=request)
            return control_response(request)
        runner, upstream, counts = self.runner(self.records[:2], handler)
        result = runner.tick(upstream, lambda p: {"point_id": p["id"], "status": "WITHHELD_CONTROL_NO_QUERY_PAYOFF"})
        self.assertEqual(result["blocked"], {1: "Uncertain"})
        for _ in range(40):
            if result["complete"] == 1: break
            self.now[0] = max(result["waiting"].values()) + .01
            result = runner.tick(upstream, lambda p: {"point_id": p["id"], "status": "WITHHELD_CONTROL_NO_QUERY_PAYOFF"})
        self.assertEqual(result["complete"], 1)
        book = StageBook(self.directory, runner.identity, verify_only=True)
        self.assertFalse(book.complete("outcome/" + self.records[0]["point"]["id"]))
        self.assertTrue(book.complete("outcome/" + self.records[1]["point"]["id"]))
        self.assertEqual(set(counts.values()), {1})
        self.assertEqual(len([r for r in runner.calls.state["rows"] if r["org"] == 1]), 1)

    def test_replayed_forecast_tamper_cannot_become_cash_or_pass_cold_verify(self) -> None:
        runner, upstream, _ = self.runner(self.records[:1])
        self.finish(runner, upstream)
        book = StageBook(self.directory, runner.identity, verify_only=True)
        slot = f"forecast/{self.records[0]['point']['id']}/u0/r0/original_common"
        doc = load(book.path(slot))
        doc["attempts"][0]["output"]["policy"]["final_action"] = "LONG"
        from core.historical_evaluation_protocol import digest as old_digest
        doc["attempts"][0]["output_sha256"] = old_digest(doc["attempts"][0]["output"])
        save(book.path(slot), doc)
        with self.assertRaises(ValueError): verify_execution(self.directory, runner.identity, runner.methods)

    def test_complete_run_cold_verify_is_read_only_and_never_constructs_provider(self) -> None:
        runner, upstream, counts = self.runner(self.records[:2])
        self.finish(runner, upstream)
        hashes = {p.relative_to(self.directory).as_posix(): p.read_bytes() for p in self.directory.rglob("*") if p.is_file()}
        with patch("httpx.Client", side_effect=AssertionError("Cấm client")), \
             patch("langchain_groq.ChatGroq", side_effect=AssertionError("Cấm SDK")), \
             patch("core.unified_execution_providers.StudyProviders", side_effect=AssertionError("Cấm provider")):
            result = verify_execution(self.directory, runner.identity, runner.methods)
        self.assertEqual(result["forecast_slots"], 48)
        self.assertEqual(set(counts.values()), {1})
        self.assertEqual(hashes, {p.relative_to(self.directory).as_posix(): p.read_bytes() for p in self.directory.rglob("*") if p.is_file()})
        self.assertEqual(len({r["id"] for r in wire_state(self.directory)["rows"]}), result["mock_http_attempts"])

    def test_carry_duplicates_with_conflicting_token_counts_are_rejected(self) -> None:
        history = {i: [] for i in range(1, 6)}
        row = {"id": "same", "started_at": self.now[0], "reserved_tokens": 1000}
        history[1] = [row, {**row, "reserved_tokens": 2000}]
        with self.assertRaises(ValueError):
            DurableCalls(self.directory, "a"*64, "U07_TEST", MockHTTP(control_response), history, lambda: self.now[0])


if __name__ == "__main__":
    unittest.main()
