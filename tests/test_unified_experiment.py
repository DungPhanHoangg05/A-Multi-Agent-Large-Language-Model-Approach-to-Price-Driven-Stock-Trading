"""Hợp đồng tám vai trò, shared/PIT, raw-policy, durable barrier và CLI/UI offline."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from uuid import NAMESPACE_URL, uuid5

import numpy as np
import pandas as pd

from core.historical_evaluation_journal import load, save
from core.mt_bicl_context import prepare_variants
from core.mt_bicl_teacher import BetaBernoulliTeacher
from core.unified_contracts import ExperimentSpec, SharedSnapshot, digest, json_bytes
from core.unified_experiment import (OfflineResponses, UnifiedRunner, make_record, outcome_from_frame,
                                     runtime_identity, slot_id, verify_run)
from core.unified_methods import MethodAdapters, validate_prepared
from core.variant_registry import execution_order, registry_document, VARIANTS
from mt_bicl_support import episode, original, protocol, reply, shared, unsupported

ROOT = Path(__file__).resolve().parents[1]


class UnifiedFixture:
    """Fixture số tổng hợp; dùng primitive teacher/prompt/policy thật, không frozen weights hoặc API."""
    def __init__(self, root: Path, variants: list[str] | None = None, repeats: int = 1) -> None:
        self.root = root
        self.episode = episode()
        self.facts = self.episode["advisor"]["query_facts"]
        self.prepared = prepare_variants(self.episode, BetaBernoulliTeacher([1/16]*16), lambda e: .6 if e["m"] else .3)
        self.point = {"id": self.facts["point_id"], "symbol": self.facts["point_id"].split("-", 1)[0],
                      "cutoff": self.facts["as_of_date"], "fold": "fixture", "quality": "SYNTHETIC_FIXTURE"}
        self.payload = shared(self.facts)
        self.provenance = {"source_sha256": "1"*64, "upstream_sha256": "2"*64,
                           "price_end": self.point["cutoff"], "news_dates": [self.point["cutoff"]]}
        self.snapshot = SharedSnapshot.create(self.point, 0, self.payload, self.provenance)
        prices = {"Datetime": pd.bdate_range(self.point["cutoff"], periods=4), "Open": [100., 100., 100., 100.],
                  "High": [101., 102., 103., 111.], "Low": [99., 99., 99., 99.], "Close": [100., 101., 102., 110.], "Volume": [1e6]*4}
        self.frame = pd.DataFrame(prices)
        source = root / "synthetic-prices.json"
        source.write_text(self.frame.to_json(date_format="iso"), encoding="utf-8")
        self.source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
        self.spec = {"version": "unified_experiment_v1", "namespace": "outputs/unified_integration/fixture",
            "mode": "fixture", "variants": variants or [v.id for v in VARIANTS], "points": [self.point],
            "repeats": repeats, "realizations": 1, "seed": 42, "decision": protocol()["decision"]["config"],
            "source_hashes": {"synthetic-prices.json": self.source_sha}, "runtime_sha256": digest(runtime_identity()),
            "calendar_sha256": digest([str(d.date()) for d in self.frame.Datetime]),
            "estimand": "SYMBOL_FOLD_ACCOUNT_RETURN_PERCENT", "missing_policy": "FAIL_CLOSED_COMMON_SUPPORT",
            "costs": {"fee": .0025, "slippage": .001, "horizon": 3, "initial_vnd": 50000000}}
        self.spec["resource_sources"] = {name: "synthetic-prices.json" for v in VARIANTS
            if v.id in execution_order(self.spec["variants"]) for name in v.resources}

    def methods(self, counts: dict | None = None) -> MethodAdapters:
        """Factories ghi số lần load; stub bank chỉ kiểm OFF/fallback, active prior có test riêng."""
        counts = counts if counts is not None else {}
        def bank() -> object:
            counts["bank"] = counts.get("bank", 0) + 1
            def request(branch: str, state: dict, regime: str) -> tuple[dict, dict]:
                from core.mt_bicl_prompt import canonical_request
                trace = {"fallback": branch != "bayesian_v1", "retrieval": {"tasks": [], "stats": None},
                         "request": {"prefix": ""}}
                return canonical_request(state, "", {"decision": self.spec["decision"]}), trace
            return SimpleNamespace(request=request)
        def context() -> object:
            counts["student"] = counts.get("student", 0) + 1
            return SimpleNamespace(build=lambda *_: deepcopy(self.episode), variants=lambda _: deepcopy(self.prepared))
        return MethodAdapters(self.spec["decision"], bank_factory=bank, regime=lambda _: "BULL",
                             facts=lambda _: deepcopy(self.facts), context_factory=context)

    def bundle(self) -> dict:
        """Khóa responses xác định từ request trước khi chạy runner, hoàn toàn không đọc outcome."""
        methods = self.methods()
        preparations, responses = {}, {}
        for r in range(self.spec["repeats"]):
            outputs = {}
            for variant in execution_order(self.spec["variants"]):
                dependencies = {k: outputs[k] for k in next(v for v in VARIANTS if v.id == variant).dependencies}
                prepared = methods.prepare(variant, self.snapshot, dependencies, r)
                validate_prepared(variant, self.snapshot, prepared, self.spec["decision"], r)
                slot = slot_id(self.point["id"], 0, r, variant)
                preparations[slot] = prepared
                raw = None
                if prepared["request"] is not None:
                    value = reply(self.facts, "SHORT" if variant == "MT_BICL" else "LONG", anchor=variant == "Fact_Anchor") if variant in ("Fact_Anchor", "MT_BICL") else original()
                    raw = {"request_sha256": digest(prepared["request"]), "source_request_id": str(uuid5(NAMESPACE_URL, slot)),
                           "source_sha256": digest(value), "reply": value}
                    responses[slot] = raw
                outputs[variant] = make_record(self.point, self.snapshot, variant, r, prepared, raw, dependencies)
        return {"spec": self.spec, "snapshots": {self.point["id"]+"/u0": self.snapshot.document()},
                "preparations": preparations, "responses": responses,
                "outcomes": {self.point["id"]: outcome_from_frame(self.point, self.frame, self.source_sha)}}

    def run(self, bundle: dict, counts: dict | None = None) -> dict:
        """Outcome provider kiểm barrier thực, không chỉ dựa vào số callback RAM."""
        counts = counts if counts is not None else {}
        runner = UnifiedRunner(self.root, ExperimentSpec.create(self.spec), OfflineResponses(bundle["responses"]))
        def snapshot(point: dict, u: int) -> SharedSnapshot:
            counts["upstream"] = counts.get("upstream", 0) + 1
            return self.snapshot
        def outcome(point: dict) -> dict:
            from core.historical_evaluation_journal import RunBook
            book = RunBook(runner.directory, runner.identity, verify_only=True)
            self_required = [slot_id(point["id"], 0, r, v) for r in range(self.spec["repeats"]) for v in execution_order(self.spec["variants"])]
            assert all(book.complete(slot) for slot in self_required)
            counts["outcome"] = counts.get("outcome", 0) + 1
            return bundle["outcomes"][point["id"]]
        return runner.run(snapshot, self.methods(counts), outcome)


class UnifiedExperimentTests(unittest.TestCase):
    """Test đường điều phối mới và hợp đồng có hệ quả đến dữ liệu/tài khoản."""
    def test_registry_has_six_research_native_dependency_and_dag(self) -> None:
        doc = registry_document()
        self.assertEqual(doc["default"], "original_fix")
        self.assertEqual(sum(v["role"] == "research" for v in doc["variants"]), 6)
        self.assertEqual(execution_order(["MT_BICL"]), ["original_common", "Fact_Anchor", "MT_BICL"])
        self.assertEqual(execution_order(["original_fix"]), ["original_fix"])
        for bad in (["Original_common"], ["original_fix", "original_fix"], []):
            with self.assertRaises(ValueError): execution_order(bad)
        json_bytes(doc)

    def test_snapshot_immutable_future_and_nested_y_firewall(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix"])
            before = fx.snapshot.sha256
            fx.snapshot.document()["payload"]["trend_report"] = "Mutated"
            self.assertEqual(fx.snapshot.sha256, before)
            for key in ("query_y", "outcome", "entry_open", "label_net"):
                bad = {**fx.payload, "nested": [{key: 1}]}
                with self.assertRaises(ValueError): SharedSnapshot.create(fx.point, 0, bad, fx.provenance)
            for dates in ([None], ["2099-01-01"]):
                with self.assertRaises(ValueError): SharedSnapshot.create(fx.point, 0, fx.payload, {**fx.provenance, "news_dates": dates})
            for published in (None, "2099-01-01"):
                bad = {**fx.payload, "sentiment_data": {"articles": [{"date_parsed": published}]}}
                with self.assertRaises(ValueError): SharedSnapshot.create(fx.point, 0, bad, fx.provenance)
            with self.assertRaises(ValueError): json_bytes({"flag": np.bool_(True)})

    def test_spec_refuses_bad_profile_namespace_costs_and_hosted_before_files(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix"])
            for key, value in (("variants", ["Original_common"]), ("namespace", "outputs/revision/old"),
                               ("mode", "hosted"), ("seed", 43), ("repeats", True), ("costs", {"fee": 0})):
                bad = {**fx.spec, key: value}
                with self.assertRaises(ValueError): ExperimentSpec.create(bad)
            self.assertFalse((fx.root / "outputs").exists())

    def test_native_common_prior_off_loads_no_resources_and_reuses_one_upstream(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix", "original_common"], repeats=2)
            bundle, counts = fx.bundle(), {}
            result = fx.run(bundle, counts)
            self.assertEqual(counts, {"upstream": 1, "outcome": 1})
            self.assertEqual((result["planned_slots"], result["complete_slots"], result["points"]), (4, 4, 1))
            self.assertEqual(len(result["accounts"]), 4)
            self.assertEqual(len({r["shared_sha256"] for r in result["rows"]}), 1)
            for metrics in result["accounts"].values():
                self.assertGreater(metrics["total_return_pct"], 0)
                self.assertIsNone(metrics["sharpe_ratio"])
            self.assertEqual(result, verify_run(fx.root / fx.spec["namespace"], root=fx.root))

    def test_eight_variants_share_evaluator_fallback_raw_policy_and_exact_resume(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory)); bundle, counts = fx.bundle(), {}
            result = fx.run(bundle, counts)
            self.assertEqual(counts, {"upstream": 1, "bank": 1, "student": 1, "outcome": 1})
            self.assertEqual(result["complete_slots"], 8)
            rows = {row["variant"]: row for row in result["rows"]}
            self.assertEqual(rows["C2"]["raw_proposal"], None)
            self.assertEqual(rows["C2"]["reason"], "FALLBACK_ORIGINAL")
            self.assertEqual(rows["MT_BICL"]["raw_proposal"], "SHORT")
            self.assertIn(rows["MT_BICL"]["final_action"], ("CASH", "LONG"))
            again = {}
            self.assertEqual(result, fx.run(bundle, again))
            self.assertEqual(again, {})
            with patch("core.unified_methods.MethodAdapters", side_effect=AssertionError("Không tạo adapter")):
                self.assertEqual(result, verify_run(fx.root / fx.spec["namespace"], root=fx.root))

    def test_failed_decision_keeps_unknown_and_never_opens_outcome_or_fabricates_cash(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix", "original_common"])
            bundle = fx.bundle()
            slot = slot_id(fx.point["id"], 0, 0, "original_common")
            bundle["responses"][slot]["reply"]["decision"] = "HOLD"
            for attempt in range(2):
                counts = {}
                with self.assertRaises(ValueError): fx.run(bundle, counts)
                self.assertNotIn("outcome", counts)
            self.assertFalse((fx.root / fx.spec["namespace"] / "result.json").exists())
            from core.historical_evaluation_journal import RunBook
            identity = load(fx.root / fx.spec["namespace"] / "identity.json")["identity"]
            book = RunBook(fx.root / fx.spec["namespace"], identity, verify_only=True)
            self.assertTrue(book.complete(slot_id(fx.point["id"], 0, 0, "original_fix")))
            self.assertFalse(book.complete(slot))

    def test_tampered_prepared_prompt_summary_or_input_cannot_pass_verify(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix"]); bundle = fx.bundle(); fx.run(bundle)
            path = fx.root / fx.spec["namespace"] / "result.json"
            original_result = load(path)
            changed = deepcopy(original_result); changed["rows"][0]["final_action"] = "CASH"; save(path, changed)
            with self.assertRaises(ValueError): verify_run(path.parent, root=fx.root)
            save(path, original_result)
            prepared = next(iter(bundle["preparations"].values()))
            prepared["request"]["messages"][0]["content"] += " tampered"
            with self.assertRaises(ValueError): validate_prepared("original_fix", fx.snapshot, prepared, fx.spec["decision"], 0)
            (fx.root / "synthetic-prices.json").write_text("changed", encoding="utf-8")
            with self.assertRaises(ValueError): verify_run(path.parent, root=fx.root)

    def test_cli_replay_verify_and_csv_use_identical_records_and_refuse_wrong_hash(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix", "original_common"])
            bundle = fx.bundle(); path = fx.root / "bundle.json"; path.write_bytes(json_bytes(bundle))
            cli = [sys.executable, "-I", "-X", "utf8", str(ROOT / "scripts/run_unified_experiment.py"), "--root", str(fx.root)]
            bad = subprocess.run([*cli, "replay", str(path), "--sha256", "0"*64], capture_output=True)
            self.assertEqual(bad.returncode, 2)
            good = subprocess.run([*cli, "replay", str(path), "--sha256", hashlib.sha256(path.read_bytes()).hexdigest()], capture_output=True, check=True)
            result = json.loads(good.stdout)
            verified = subprocess.run([*cli, "verify", str(fx.root / fx.spec["namespace"])], capture_output=True, check=True)
            self.assertEqual(result, json.loads(verified.stdout))
            csv = fx.root / "table.csv"
            subprocess.run([*cli, "export", str(fx.root / fx.spec["namespace"]), "--format", "csv", "--output", str(csv)], capture_output=True, check=True)
            self.assertEqual(len(csv.read_text(encoding="utf-8-sig").splitlines()), 3)
            refused = subprocess.run([*cli, "export", str(fx.root / fx.spec["namespace"]), "--format", "csv", "--output", str(csv)], capture_output=True)
            self.assertEqual(refused.returncode, 2)

    def test_response_cannot_be_counted_twice_as_independent_repeat(self) -> None:
        with self.assertRaises(ValueError): OfflineResponses({"a": {"source_request_id": "same"}, "b": {"source_request_id": "same"}})

    def test_active_prior_adapters_delegate_real_verified_retriever_selector_and_renderer(self) -> None:
        from core.free_pilot_assets import FrozenBank
        from test_prior_quality_gate import populated_fixture, gate_query
        fx = populated_fixture()
        self.addCleanup(fx.close)
        query = gate_query(fx)
        point = {"id": "FPT-" + query["as_of_date"], "symbol": "FPT", "cutoff": query["as_of_date"],
                 "fold": "fixture", "quality": "SYNTHETIC_FIXTURE"}
        payload = {"stock_name": "FPT", "as_of_date": point["cutoff"], "time_frame": "1d", "language": "vi", "is_backtest": True,
            "trend_report": "Trend direction: Bullish", "pattern_report": "Directional bias: Neutral",
            "indicator_report": "Dominant consensus: Bearish", "alpha_report": "Alpha fixture.", "sentiment_report": "Tin fixture.",
            "alpha_factors": [{"signal": "TRUNG TÍNH"} for _ in range(5)], "sentiment_data": {"main_sentiment": {"avg_score": 0.}}}
        snapshot = SharedSnapshot.create(point, 0, payload, {"source_sha256": "1"*64, "upstream_sha256": "2"*64,
            "price_end": point["cutoff"], "news_dates": []})
        config = protocol()["decision"]["config"]
        bank = object.__new__(FrozenBank)
        bank.retriever, bank.selector = fx.retriever, query["selector"]
        bank.records = [row for row in fx.records if row["exit_date"] < point["cutoff"]]
        bank.data = SimpleNamespace(protocol={"inference": {"config": config}}, features=lambda *_: query["query_features"])
        methods = MethodAdapters(config, bank_factory=lambda: bank, regime=lambda _: "BULL")
        for variant in ("bayesian_v1", "C2", "A_tp_pool", "B_semantic"):
            with self.subTest(variant=variant):
                prepared = methods.prepare(variant, snapshot, {}, 0)
                validate_prepared(variant, snapshot, prepared, config, 0)
                request, trace = bank.request(variant, payload, "BULL")
                self.assertEqual(prepared["trace"], trace)
                self.assertEqual(prepared["request"], None if trace["fallback"] else request)
                if variant == "bayesian_v1":
                    poisoned = deepcopy(prepared)
                    poisoned["trace"]["retrieval"]["tasks"][0]["exit_date"] = point["cutoff"]
                    with self.assertRaises(ValueError): validate_prepared(variant, snapshot, poisoned, config, 0)

    def test_fact_anchor_alone_does_not_load_student_and_mt_bypass_keeps_anchor(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["Fact_Anchor"])
            bundle, counts = fx.bundle(), {}
            result = fx.run(bundle, counts)
            self.assertNotIn("student", counts)
            self.assertNotIn("bank", counts)
            self.assertEqual(result["executed_variants"], ["original_common", "Fact_Anchor"])
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["MT_BICL"])
            fx.prepared["branches"]["MT_BICL"] = unsupported(fx.prepared["branches"]["MT_BICL"])
            bundle = fx.bundle(); result = fx.run(bundle)
            row = next(r for r in result["rows"] if r["variant"] == "MT_BICL")
            self.assertIsNone(row["raw_proposal"])
            self.assertTrue(row["bypass"])
            self.assertEqual(row["final_action"], next(r["final_action"] for r in result["rows"] if r["variant"] == "Fact_Anchor"))

    def test_graph_snapshot_future_poison_is_rejected_before_preparation(self) -> None:
        from core.unified_methods import snapshot_from_graph
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix"])
            prefix = pd.DataFrame({"Datetime": pd.bdate_range(end=fx.point["cutoff"], periods=600),
                "Open": 100., "High": 101., "Low": 99., "Close": 100., "Volume": 1e6})
            result = snapshot_from_graph(fx.point, 0, fx.payload, prefix, fx.source_sha, [])
            self.assertEqual(len(result.document()["payload"]["price_prefix"]["Datetime"]), 600)
            prefix.loc[599, "Datetime"] += pd.Timedelta(days=1)
            with self.assertRaises(ValueError): snapshot_from_graph(fx.point, 0, fx.payload, prefix, fx.source_sha, [])

    def test_context_label_callback_remains_closed_until_every_required_forecast(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["MT_BICL"]); bundle = fx.bundle()
            runner = UnifiedRunner(fx.root, ExperimentSpec.create(fx.spec), OfflineResponses(bundle["responses"]))
            self.assertFalse(runner.forecasts_done(fx.point["id"]))
            self.assertFalse(runner.forecasts_done("unplanned-point"))
            fx.run(bundle)
            self.assertTrue(runner.forecasts_done(fx.point["id"]))

    def test_evaluator_resets_fold_and_keeps_cash_and_undefined_class_metrics(self) -> None:
        from core.unified_experiment import evaluate
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix"])
            point2 = {**fx.point, "cutoff": str((pd.Timestamp(fx.point["cutoff"]) + pd.offsets.BDay(5)).date()), "fold": "next"}
            point2["id"] = point2["symbol"] + "-" + point2["cutoff"]
            records, outcomes = [], {}
            methods = fx.methods()
            for point, decision in ((fx.point, "LONG"), (point2, "SHORT")):
                payload = {**fx.payload, "as_of_date": point["cutoff"]}
                snapshot = SharedSnapshot.create(point, 0, payload, {**fx.provenance, "price_end": point["cutoff"]})
                prepared = methods.prepare("original_fix", snapshot, {}, 0)
                raw = {"request_sha256": digest(prepared["request"]), "source_request_id": str(uuid5(NAMESPACE_URL, point["id"])),
                       "source_sha256": "1"*64, "reply": original(decision)}
                records.append(make_record(point, snapshot, "original_fix", 0, prepared, raw, {}))
                frame = fx.frame.copy(); frame["Datetime"] = pd.bdate_range(point["cutoff"], periods=4)
                outcomes[point["id"]] = outcome_from_frame(point, frame, fx.source_sha)
            result = evaluate({**fx.spec, "points": [fx.point, point2]}, records, outcomes)
            self.assertEqual(len(result["accounts"]), 2)
            self.assertEqual(result["accounts"]["original_fix/FPT/next/0/0"]["final_equity_vnd"], 50000000.)
            self.assertEqual(result["rows"][1]["strategy_return"], 0.)
            self.assertIsNone(result["classification"]["original_fix/u0/r0"]["balanced_accuracy"])
            with self.assertRaises(ValueError): evaluate({**fx.spec, "points": [fx.point, point2]}, [records[0], records[0]], outcomes)

    def test_ui_registry_results_export_and_hosted_selection_gate(self) -> None:
        with TemporaryDirectory() as directory:
            fx = UnifiedFixture(Path(directory), ["original_fix"]); bundle = fx.bundle(); expected = fx.run(bundle)
            with patch("core.realtime_loader.get_all_symbols_realtime", return_value=[]):
                web = importlib.import_module("web_interface")
            with patch("utils.experiment_web.ROOT", fx.root), patch("web_interface.BacktestEngine") as engine:
                client = web.app.test_client()
                self.assertEqual(client.get("/api/experiments/registry").get_json()["default"], "original_fix")
                page = client.get("/experiments")
                self.assertEqual(page.status_code, 200)
                self.assertIn(b'value="original_fix" selected', page.data)
                self.assertEqual(client.get("/api/experiments/fixture").get_json(), expected)
                self.assertEqual(client.get("/api/experiments/fixture/export?format=json").get_json(), expected)
                self.assertEqual(client.get("/api/experiments/fixture/export?format=csv").status_code, 200)
                self.assertEqual(client.get("/api/experiments/missing").status_code, 404)
                self.assertEqual(client.get("/api/experiments/fixture/export?format=exe").status_code, 400)
                self.assertEqual(client.post("/api/experiments/validate", json=fx.spec).status_code, 200)
                self.assertEqual(client.post("/api/backtest/start", json={"variant": "MT_BICL"}).status_code, 409)
                self.assertEqual(client.post("/api/backtest/start", json={"variant": "typo"}).status_code, 400)
                engine.assert_not_called()


if __name__ == "__main__":
    unittest.main()
