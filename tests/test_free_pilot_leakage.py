"""Hồi quy pilot48: mẫu cố định, PIT, bank transfer, paired và quota/replay."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import time
import unittest
from unittest.mock import Mock, patch

import torch
from threadpoolctl import threadpool_limits

from core.free_pilot_assets import (PilotData, FrozenBank, selected_units, call_order, carry_over,
                                    budget_schedule, PRIMARY, RAW_SOURCE)
from core.free_pilot_runtime import PilotRunner, PilotClients, rendered_request, reserve, protocol_record
from core.historical_evaluation_context import ContextBank
from core.historical_evaluation_graph import GraphProvider, require_factors
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import digest, binding
from core.historical_evaluation_runner import FixtureClients, Regimes
from core.mt_bicl_prompt import canonical_request, COMMON_INSTRUCTION

ROOT = Path(__file__).resolve().parents[1]


class PilotTests(unittest.TestCase):
    """Dữ liệu thật đã khóa, toàn bộ HTTP bị chặn trong fixture kiểm thử."""
    @classmethod
    def setUpClass(cls) -> None:
        torch.set_num_threads(1)
        cls.data = PilotData(ROOT)
        cls.units = cls.data.inputs["grid"]
        with threadpool_limits(limits=1):
            cls.bank = FrozenBank(cls.data)

    def test_calendar_selection_and_no_input_mutation(self) -> None:
        original = load(ROOT / "docs/plan/week11/historical_evaluation_inputs.json")["grid"]
        before = deepcopy(original)
        units = selected_units(original)
        self.assertEqual(original, before)
        self.assertEqual(len(units), 48)
        self.assertEqual(sorted({r["date"] for r in units})[:6],
                         ["2023-07-03", "2023-07-14", "2023-08-01", "2023-08-17", "2023-09-06", "2023-09-22"])
        self.assertEqual(sorted({r["date"] for r in units})[6:],
                         ["2024-07-01", "2024-07-12", "2024-07-30", "2024-08-15", "2024-09-04", "2024-09-20"])
        self.assertEqual([r["org"] for r in units], [i % 5 + 1 for i in range(48)])
        for i in range(48):
            order = call_order(i)
            self.assertEqual(order[:2], ["Original_common", "Fact_Anchor"])
            self.assertEqual(set(order), {*PRIMARY, "Fact_Anchor"})

    def test_transfer_keeps_native_population_and_train_scaler(self) -> None:
        bank = self.bank
        self.assertEqual(len(bank.records), 852)
        self.assertEqual(bank.index.payload["source"], RAW_SOURCE)
        self.assertNotEqual(RAW_SOURCE, self.data.scope.source)
        self.assertTrue(bank.index.payload["transfer_contract"]["no_price_splicing"])
        feature = self.data.features("FPT", "2023-07-03")
        before = deepcopy(feature)
        transformed = bank.index.transform_query("FPT", "2023-07-03", feature)
        self.assertEqual(feature, before)
        self.assertEqual(transformed["index_sha256"], bank.index.identity)
        scaler = bank.index.scaler("FPT", "2023-07-03")
        self.assertLessEqual(scaler["fit_max_exit_date"], "2022-12-30")
        self.assertEqual(max(r["exit_date"] for r in bank.records), "2022-12-30")

    def test_bank_unmature_record_rejected_before_rank(self) -> None:
        bank = FrozenBank.__new__(FrozenBank)
        bank.__dict__.update(self.bank.__dict__)
        bank.records = [*self.bank.records, {"exit_date": "2023-07-03"}]
        with patch("core.historical_evaluation_prior.signals", return_value={}), self.assertRaisesRegex(ValueError, "mature"):
            bank.request("bayesian_v1", {"stock_name": "FPT", "as_of_date": "2023-07-03",
                         "trend_report": "BULLISH", "pattern_report": "BULLISH", "indicator_report": "", "sentiment_report": "", "alpha_report": ""}, "BULL")

    def test_query_outcome_barrier_and_future_price_poison(self) -> None:
        row = self.units[0]
        with self.assertRaises(ValueError):
            self.data.label(row["symbol"], row["date"], as_of="2025-01-01", forecast_done=lambda _: False)
        with self.assertRaises(ValueError):
            self.data.label(row["symbol"], row["date"], as_of=row["exit_date"], forecast_done=lambda _: True)
        frame = self.data.frames[row["symbol"]]
        scope = self.data.scope
        before = scope.features(frame, self.data.events[row["symbol"]], self.data.calendar, row["date"], source=scope.source)
        frame.loc[frame.Datetime > row["date"], ["Open", "High", "Low", "Close"]] = float("nan")
        after = scope.features(frame, self.data.events[row["symbol"]], self.data.calendar, row["date"], source=scope.source)
        self.assertEqual(before, after)

    def test_oversize_prefix_is_rejected_before_serialization(self) -> None:
        shared = {"stock_name": "FPT", "as_of_date": "2023-07-03", "is_backtest": True,
                  "time_frame": "1d", "language": "vi", **{name + "_report": "Báo cáo thử" for name in
                  ("trend", "pattern", "indicator", "alpha", "sentiment")}}
        with self.assertRaises(ValueError):
            canonical_request(shared, "X" * 601, {"decision": self.data.protocol["inference"]["config"]})

    def test_numeric_context_reserves_only_selected_query_and_rejects_query_y(self) -> None:
        context = ContextBank(self.data, lambda _: False)
        episode = context.build("FPT", "2023-08-01")
        withheld = set(context.stream.audit[-1]["withheld_forecast_ids"])
        expected = {r["symbol"] + "-" + r["date"] for r in self.units if r["exit_date"] < "2023-08-01"}
        self.assertEqual(withheld, expected)
        self.assertFalse(withheld.intersection(r["episode_id"] for r in context.stream.closed_records()))
        poisoned = deepcopy(episode)
        poisoned["query"]["y"] = 1
        with self.assertRaises(ValueError):
            context.predict(poisoned)

    def test_paired_request_policy_resume_and_tampered_action(self) -> None:
        class CountClients(FixtureClients):
            def __init__(self) -> None:
                self.calls = []
            def decision(self, org: int, request: dict, attempt: str, branch: str) -> dict:
                self.calls.append(branch)
                return super().decision(org, request, attempt, branch)
        row = self.units[0]
        with TemporaryDirectory() as folder, threadpool_limits(limits=1):
            clients = CountClients()
            runner = PilotRunner.__new__(PilotRunner)
            runner.root, runner.data, runner.smoke = ROOT, self.data, False
            runner.inputs = {"units": self.units, "call_orders": {row["id"]: call_order(0)}}
            runner.book = RunBook(Path(folder), {"fixture": True})
            runner.bank, runner.clients = self.bank, clients
            runner.graph = GraphProvider(self.data, clients, fixture=True)
            runner.context = ContextBank(self.data, runner.forecasts_done)
            runner.regimes = Regimes(self.data, Path(folder))
            runner.require_shared = Mock()
            def validate_fixture(book: RunBook, response: dict, branch: str, *, fixture: bool, request: dict) -> None:
                self.assertFalse(fixture)
                self.assertTrue(response["fixture"])
                self.assertIn(COMMON_INSTRUCTION, request["messages"][0]["content"])
                self.assertLess(len(request["messages"][0]["content"]), 6500)
            with patch("core.free_pilot_runtime.verify_decision", side_effect=validate_fixture):
                outputs = runner.unit(row)
                self.assertTrue(runner.forecasts_done(row["id"]))
                self.assertEqual(set(outputs), {*PRIMARY, "Fact_Anchor"})
                original_calls = list(clients.calls)
                runner.book.verify_only = True
                runner.context = ContextBank(self.data, runner.forecasts_done)
                runner.unit(row)
                self.assertEqual(clients.calls, original_calls)
                slot = runner.book.path(runner.slot(row["id"], "Original_common"))
                doc = load(slot)
                doc["attempts"][-1]["output"]["final_action"] = "LONG"
                doc["attempts"][-1]["output_sha256"] = digest(doc["attempts"][-1]["output"])
                save(slot, doc)
                runner.context = ContextBank(self.data, runner.forecasts_done)
                with self.assertRaises(ValueError):
                    runner.unit(row)


class QuotaAndBoundaryTests(unittest.TestCase):
    """Rào budget/identity phải hoạt động mà không tạo kết nối mạng."""
    def test_carry_includes_both_runs_and_strips_credential_binding(self) -> None:
        rows, proofs = carry_over(ROOT)
        self.assertEqual(len(proofs), 10)
        self.assertEqual(sum(len(r) for r in rows.values()), 160)
        for values in rows.values():
            self.assertEqual(len(values), len({r["id"] for r in values}))
            self.assertTrue(all(r["carry_over"] for r in values))
            self.assertTrue(all("credential_scope" not in r for r in values))
        self.assertTrue(any(r["status"] == "transport_error" for v in rows.values() for r in v))

    def test_tpm_and_hard_deadline_block_before_requests(self) -> None:
        rows = {i: [] for i in range(1, 6)}
        task = {"org": 1, "model": "openai/gpt-oss-20b", "tokens": 8001}
        self.assertEqual(budget_schedule(rows, [task], start=0, latency=10)["status"], "BLOCKED_BUDGET")
        task["tokens"] = 4500
        result = budget_schedule(rows, [task] * 140, start=100000, latency=10)
        self.assertEqual(result["status"], "BLOCKED_BUDGET")

    def test_missing_shared_blocks_decision(self) -> None:
        with TemporaryDirectory() as folder:
            runner = PilotRunner.__new__(PilotRunner)
            runner.inputs = {"units": [{"id": "one"}]}
            runner.book = RunBook(Path(folder), {"fixture": True})
            with self.assertRaisesRegex(ValueError, "seal"):
                runner.require_shared()

    def test_smoke_client_rejects_research_point_without_network(self) -> None:
        client = PilotClients.__new__(PilotClients)
        client.mode, client.deadline = "smoke", time.time() + 60
        with self.assertRaises(ValueError):
            client.stage("pattern", "unused", "FPT-2023-07-03/u0", Mock(), {})

    def test_revoked_full_grant_cannot_authorize_pilot(self) -> None:
        old = load(ROOT / "docs/plan/week11/historical_evaluation_release.json")
        self.assertFalse(old["api"])
        with patch("core.free_pilot_runtime.verify_locked", return_value=({}, {})), \
                patch("core.free_pilot_runtime.anchored", return_value=old), \
                patch.object(PilotClients, "models") as models:
            with self.assertRaises(ValueError):
                PilotClients(Mock(root=ROOT), Mock(), mode="smoke")
            models.assert_not_called()

    def test_deadline_checked_again_at_http_boundary(self) -> None:
        from core.historical_evaluation_data import HistoricalData
        from core.groq_pacing import PilotStop
        data = PilotData.__new__(PilotData)
        data.api_deadline = time.time() - 1
        with patch.object(HistoricalData, "verify_sources"), self.assertRaises(PilotStop):
            data.verify_sources()

    def test_research_grant_requires_unmodified_cold_smoke_slots(self) -> None:
        from core.free_pilot_assets import DIRECTORY
        with TemporaryDirectory() as folder:
            root = Path(folder)
            book = RunBook(root / DIRECTORY, {"fixture": True})
            book.execute("smoke/one", {}, lambda _: {"fixture": True})
            slot = book.path("smoke/one")
            receipt_path = DIRECTORY / "smoke_verified.json"
            save(root / receipt_path, {"status": "SMOKE_COLD_PASS", "run_uuid": book.uuid,
                 "identity": {"fixture": True}, "slots": {slot.name: hashlib.sha256(slot.read_bytes()).hexdigest()}})
            client = PilotClients.__new__(PilotClients)
            client.data, client.book = Mock(root=root), book
            grant = {"smoke_receipt": binding(root, receipt_path)}
            with patch("core.free_pilot_runtime.identity", return_value={"fixture": True}):
                client.require_smoke(grant)
                slot.write_bytes(slot.read_bytes() + b" ")
                with self.assertRaises(ValueError):
                    client.require_smoke(grant)

    def test_source_guard_rejects_revoked_grant_between_http_requests(self) -> None:
        from core.groq_pacing import PilotStop
        client = PilotClients.__new__(PilotClients)
        client.data, client.book, client.mode = Mock(root=ROOT), Mock(uuid="same"), "smoke"
        with patch("core.free_pilot_runtime.verify_locked"), \
                patch("core.free_pilot_runtime.anchored", return_value={"run_uuid": "same", "api": False}), \
                self.assertRaises(PilotStop):
            client.verify_release()

    def test_deleting_carry_does_not_reset_api_quota(self) -> None:
        from core.free_pilot_assets import AUDIT
        with TemporaryDirectory() as folder:
            root = Path(folder)
            save(root / AUDIT, {"quota_carry": {}})
            client = PilotClients.__new__(PilotClients)
            client.data, client.book = Mock(root=root), Mock(directory=root)
            carry = {1: [{"id": "carry", "carry_over": True}]}
            with patch("core.free_pilot_runtime.carry_over", return_value=(carry, {})):
                with self.assertRaisesRegex(ValueError, "Thiếu quota"):
                    client.verify_quota()
                path = root / "usage/org1.json"
                path.parent.mkdir()
                path.write_text(json.dumps({"requests": carry[1]}), encoding="utf-8")
                client.verify_quota()
                path.write_text('{"requests": []}', encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "carry-over"):
                    client.verify_quota()

    def test_unknown_resume_is_not_automatically_replayed(self) -> None:
        with TemporaryDirectory() as folder:
            book = RunBook(Path(folder), {"fixture": True})
            def fail(attempt: str) -> dict:
                raise ConnectionResetError("Kiểm UNKNOWN")
            with self.assertRaises(ConnectionResetError):
                book.execute("one", {}, fail)
            function = Mock(return_value={})
            with self.assertRaisesRegex(ValueError, "reconcile UUID"):
                book.execute("one", {}, function)
            function.assert_not_called()

    def test_bridge_off_and_fixed_call_cap(self) -> None:
        protocol = protocol_record()
        self.assertFalse(protocol["bridge_full_fix_native960"])
        self.assertEqual(protocol["max_http"], 3 * (336 + 96 + 9))
        self.assertFalse(protocol["paid_api_allowed"])


if __name__ == "__main__":
    unittest.main()
