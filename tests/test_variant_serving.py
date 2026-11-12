"""Kiểm contract ứng dụng mới, identity và tính tương thích của đường nghiên cứu cũ."""
from __future__ import annotations

from copy import deepcopy
import importlib
import json
import unittest
from unittest.mock import patch

from flask import Flask
import numpy as np

from core.serving_contracts import (ContractError, MODEL_ROLES, ServingJob, ServingRequest,
                                    preflight, result_document)
from core.serving_registry import (ADVANCED_IDS, CONTRACT_VERSION, MAIN_IDS, REGISTRY_VERSION,
                                   registry_document, required_resources)
from core.unified_contracts import digest, json_bytes
from core.variant_registry import execution_order, registry_document as historical_registry
from utils.serving_web import serving


def request_fixture(variants: list[str] | None = None, mode: str = "analyze") -> dict:
    """Model giả chỉ dùng identity, không tạo client hoặc gọi mạng."""
    return {"version": CONTRACT_VERSION, "mode": mode, "variant_ids": variants or ["original_fix"],
            "symbols": ["FPT"], "start_date": "2026-11-12", "end_date": "2026-11-12",
            "timeframe": "1d", "language": "vi", "repeats": 1,
            "models": {role: {"provider": "fixture", "model": "fixture-model-v1",
                              "options": {"temperature": 0, "max_tokens": 1024}} for role in MODEL_ROLES}}


def config_fixture(spec: ServingRequest) -> dict:
    """Manifest tổng hợp; object hợp lệ không có nghĩa là được grant inference."""
    variants = spec.document()["variant_ids"]
    return {"version": "serving_config_v1", "registry_version": REGISTRY_VERSION,
            "runner_version": "fixture-v1", "provider_version": "fixture-v1",
            "source_sha256": "1" * 64, "calendar_sha256": "2" * 64, "support_sha256": "3" * 64,
            "credential_scope_sha256": "4" * 64,
            "resources": {name: {"version": "fixture-v1", "sha256": "5" * 64}
                          for name in required_resources(variants)},
            "prompt_versions": {name: "fixture-v1" for name in [*execution_order(variants), *MODEL_ROLES[:-1]]}}


def row_fixture(identifier: str = "original_fix") -> dict:
    """Forecast SHORT phải có hành động CASH và outcome chưa quan sát là null."""
    return {"point_id": "FPT-2026-11-12", "symbol": "FPT", "as_of_date": "2026-11-12", "repeat": 0,
            "requested_id": identifier, "executed_id": identifier, "raw_prediction": "SHORT",
            "final_prediction": "SHORT", "final_action": "CASH", "fallback_reason": None, "bypass_reason": None,
            "support": {"manifest_sha256": "3" * 64, "status": "supported"},
            "net_return_pct": None, "metric_reason": "PENDING_EXIT"}


def progress_fixture(total: int = 1, complete: int = 1) -> dict:
    """Tách point, slot và attempts để không suy số API từ số bản."""
    return {"points_total": 1, "points_complete": int(total == complete),
            "decision_slots_total": total, "decision_slots_complete": complete, "api_attempts": 2}


class ServingContractTests(unittest.TestCase):
    """Mỗi test bảo vệ một hành vi quan sát được của contract."""

    def test_registry_separates_six_main_two_advanced_and_controls(self) -> None:
        old = historical_registry()
        before = digest(old)
        doc = registry_document()
        self.assertEqual(doc["version"], REGISTRY_VERSION)
        self.assertNotEqual(doc["version"], old["version"])
        self.assertEqual([v["id"] for v in doc["variants"] if v["group"] == "main"], list(MAIN_IDS))
        self.assertEqual([v["id"] for v in doc["variants"] if v["group"] == "advanced"], list(ADVANCED_IDS))
        self.assertTrue(set(doc["evaluation_controls"]).isdisjoint(v["id"] for v in doc["variants"]))
        self.assertFalse(any(c["available"] for v in doc["variants"] for c in v["capabilities"].values()))
        self.assertEqual(doc["domain"]["released_symbols"], [])
        self.assertEqual(before, digest(historical_registry()))
        self.assertFalse(old["hosted_release"])
        json_bytes(doc)

    def test_dependency_resources_and_preflight_do_not_grant_run(self) -> None:
        spec = ServingRequest.create(request_fixture(list(MAIN_IDS), "compare"))
        result = preflight(spec)
        self.assertFalse(result["run_enabled"])
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(len(result["execution_plan"]), 8)
        self.assertEqual(len(set(result["execution_plan"])), 8)
        resources = result["blockers"][2]["resources"]
        self.assertEqual(set(resources), {"prices", "news", "calendar", "bank", "regime", "facts", "context", "student"})
        self.assertLess(result["execution_plan"].index("Fact_Anchor"), result["execution_plan"].index("MT_BICL"))
        en = request_fixture(); en["language"] = "en"
        self.assertIn("LANGUAGE_NOT_RELEASED", [b["code"] for b in preflight(ServingRequest.create(en))["blockers"]])

    def test_bad_fields_aliases_dates_modes_and_json_types_are_rejected(self) -> None:
        cases = [("version", "unified_experiment_v2"), ("mode", "hosted"), ("mode", []),
                 ("variant_ids", ["Original_common"]), ("variant_ids", ["CASH"]),
                 ("variant_ids", []), ("variant_ids", ["original_fix", "original_fix"]),
                 ("symbols", ["fpt"]), ("symbols", ["FPT", "FPT"]), ("symbols", "FPT"),
                 ("symbols", ["../FPT"]), ("start_date", "2026-02-30"), ("end_date", "2025-01-01"),
                 ("start_date", None), ("timeframe", "1h"), ("language", "fr"),
                 ("repeats", True), ("repeats", 0), ("repeats", 4), ("repeats", np.int64(1)),
                 ("models", None), ("models", {})]
        for field, value in cases:
            with self.subTest(field=field, value=str(value)), self.assertRaises(ContractError):
                ServingRequest.create({**request_fixture(), field: value})
        for key in ("api_key", "config", "resource_sources", "outcome"):
            with self.subTest(extra=key), self.assertRaises(ContractError):
                ServingRequest.create({**request_fixture(), key: "private-input"})

    def test_mode_cardinality_and_backtest_window_are_explicit(self) -> None:
        for value in (request_fixture(["original_fix", "C2"]), request_fixture(mode="compare"),
                      {**request_fixture(), "end_date": "2026-11-13"},
                      {**request_fixture(), "symbols": ["FPT", "VNM"]}):
            with self.subTest(value=value["mode"]), self.assertRaises(ContractError):
                ServingRequest.create(value)
        good = {**request_fixture(list(MAIN_IDS), "backtest"), "end_date": "2026-11-13", "symbols": ["FPT", "VNM"]}
        self.assertEqual(ServingRequest.create(good).document(), good)

    def test_models_options_are_closed_finite_and_typed(self) -> None:
        for field, bad in (("temperature", True), ("temperature", float("nan")), ("temperature", 2.1),
                           ("max_tokens", 0), ("max_tokens", True), ("seed", -1), ("seed", "42"), ("api_key", "hidden")):
            value = request_fixture()
            value["models"]["decision"]["options"][field] = bad
            with self.subTest(field=field, bad=bad), self.assertRaises(ContractError):
                ServingRequest.create(value)
        value = request_fixture(); value["models"]["decision"]["api_key"] = "hidden"
        with self.assertRaises(ContractError): ServingRequest.create(value)

    def test_request_and_job_are_immutable_and_hash_order_is_canonical(self) -> None:
        value = request_fixture()
        spec = ServingRequest.create(value)
        config = config_fixture(spec)
        job = ServingJob.create(spec, config, "6" * 64, "7" * 64)
        initial = job.document()
        value["language"] = "en"
        config["resources"]["prices"]["sha256"] = "0" * 64
        spec.document()["models"]["decision"]["model"] = "changed"
        job.document()["identity"]["request"]["language"] = "en"
        self.assertEqual(initial, job.document())
        self.assertEqual(spec.sha256, ServingRequest.create(dict(reversed(list(spec.document().items())))).sha256)
        another = ServingJob.create(spec, config_fixture(spec), "6" * 64, "7" * 64).document()
        self.assertEqual(initial["identity_sha256"], another["identity_sha256"])
        self.assertNotEqual(initial["run_id"], another["run_id"])
        other_owner = ServingJob.create(spec, config_fixture(spec), "6" * 64, "8" * 64).document()
        self.assertNotEqual(initial["cache_sha256"], other_owner["cache_sha256"])

    def test_identity_changes_for_every_cache_relevant_dimension(self) -> None:
        spec = ServingRequest.create(request_fixture())
        config = config_fixture(spec)
        baseline = ServingJob.create(spec, config, "6" * 64, "7" * 64).document()["identity_sha256"]
        mutations = [("language", "en"), ("variant_ids", ["original_common"]), ("symbols", ["VNM"]),
                     ("repeats", 2), ("mode", "backtest")]
        for field, value in mutations:
            changed = ServingRequest.create({**request_fixture(), field: value})
            candidate = ServingJob.create(changed, config_fixture(changed), "6" * 64, "7" * 64)
            self.assertNotEqual(baseline, candidate.document()["identity_sha256"], field)
        for role in MODEL_ROLES:
            for field, value in (("model", "other-model"), ("provider", "other-provider"),
                                 ("options", {"temperature": .3, "max_tokens": 1000, "seed": 42})):
                data = request_fixture(); data["models"][role][field] = value
                changed = ServingRequest.create(data)
                self.assertNotEqual(baseline, ServingJob.create(changed, config, "6" * 64, "7" * 64).document()["identity_sha256"])
        for field in ("source_sha256", "calendar_sha256", "support_sha256", "credential_scope_sha256"):
            changed_config = {**config, field: "a" * 64}
            self.assertNotEqual(baseline, ServingJob.create(spec, changed_config, "6" * 64, "7" * 64).document()["identity_sha256"])
        for field in ("runner_version", "provider_version"):
            self.assertNotEqual(baseline, ServingJob.create(spec, {**config, field: "v2"}, "6" * 64, "7" * 64).document()["identity_sha256"])
        for field in ("resources", "prompt_versions"):
            changed_config = deepcopy(config)
            if field == "resources": changed_config[field]["prices"]["sha256"] = "a" * 64
            else: changed_config[field]["original_fix"] = "v2"
            self.assertNotEqual(baseline, ServingJob.create(spec, changed_config, "6" * 64, "7" * 64).document()["identity_sha256"])
        self.assertNotEqual(baseline, ServingJob.create(spec, config, "a" * 64, "7" * 64).document()["identity_sha256"])
        changed_date = ServingRequest.create({**request_fixture(), "start_date": "2026-11-11", "end_date": "2026-11-11"})
        self.assertNotEqual(baseline, ServingJob.create(changed_date, config, "6" * 64, "7" * 64).document()["identity_sha256"])

    def test_config_requires_dependency_resources_hashes_and_server_versions(self) -> None:
        spec = ServingRequest.create(request_fixture(["MT_BICL"]))
        good = config_fixture(spec)
        for mutate in (lambda c: c.update(api_key="hidden"), lambda c: c["resources"].pop("student"),
                       lambda c: c["prompt_versions"].pop("Fact_Anchor"), lambda c: c.update(source_sha256="abc"),
                       lambda c: c.update(registry_version="unified_variant_registry_v2"),
                       lambda c: c["resources"]["facts"].update(path="../secret")):
            bad = deepcopy(good); mutate(bad)
            with self.assertRaises(ContractError): ServingJob.create(spec, bad, "6" * 64, "7" * 64)
        for snapshot, owner in (("prefix", "7" * 64), ("6" * 64, "user-name")):
            with self.assertRaises(ContractError): ServingJob.create(spec, good, snapshot, owner)

    def test_result_has_null_outcome_units_and_never_short_sells(self) -> None:
        spec = ServingRequest.create(request_fixture())
        job = ServingJob.create(spec, config_fixture(spec), "6" * 64, "7" * 64)
        result = result_document(job, "completed", ["original_fix"], progress_fixture(), [row_fixture()])
        self.assertIsNone(result["rows"][0]["net_return_pct"])
        self.assertEqual(result["metric_units"]["net_return_pct"], "PERCENT_PER_CYCLE")
        for field, value in (("final_action", "SHORT"), ("net_return_pct", 1.2), ("metric_reason", None),
                             ("as_of_date", "2026-11-13"), ("repeat", 1), ("raw_prediction", None),
                             ("support", {"manifest_sha256": "0" * 64, "status": "supported"})):
            row = {**row_fixture(), field: value}
            with self.subTest(field=field), self.assertRaises(ContractError):
                result_document(job, "completed", ["original_fix"], progress_fixture(), [row])

    def test_partial_failure_and_unknown_preserve_rows_without_fake_cash(self) -> None:
        spec = ServingRequest.create(request_fixture(["original_fix", "original_common"], "compare"))
        job = ServingJob.create(spec, config_fixture(spec), "6" * 64, "7" * 64)
        error = {"code": "PROVIDER_FAILURE", "message": "Nguồn chưa sẵn sàng", "retryable": True}
        result = result_document(job, "partial", ["original_fix"], progress_fixture(2, 1), [row_fixture()], error)
        self.assertEqual(len(result["rows"]), 1)
        with self.assertRaises(ContractError):
            result_document(job, "completed", ["original_fix"], progress_fixture(2, 1), [row_fixture()])
        with self.assertRaises(ContractError):
            result_document(job, "completed", ["original_fix"], progress_fixture(), [row_fixture()])
        unknown = {"code": "UNKNOWN_ATTEMPT", "message": "Cần đối soát attempt", "retryable": False}
        self.assertEqual(result_document(job, "unknown", ["original_fix"], progress_fixture(2, 1), [row_fixture()], unknown)["state"], "unknown")
        for bad in (None, error, {**unknown, "retryable": True}):
            with self.assertRaises(ContractError):
                result_document(job, "unknown", ["original_fix"], progress_fixture(2, 1), [row_fixture()], bad)

    def test_fallback_requires_declared_chain_and_complete_unique_dependency_slots(self) -> None:
        spec = ServingRequest.create(request_fixture(["MT_BICL"]))
        job = ServingJob.create(spec, config_fixture(spec), "6" * 64, "7" * 64)
        rows = [row_fixture(v) for v in ("original_common", "Fact_Anchor", "MT_BICL")]
        rows[-1].update(executed_id="Fact_Anchor", raw_prediction=None, fallback_reason="NO_ELIGIBLE_CONTEXT")
        result = result_document(job, "completed", ["original_common", "Fact_Anchor"], progress_fixture(3, 3), rows)
        self.assertEqual(result["requested_ids"], ["MT_BICL"])
        for changed in ([rows[0], rows[0], rows[2]], [*rows[:2], {**rows[-1], "executed_id": "original_fix"}],
                        [*rows[:2], {**rows[-1], "fallback_reason": None}]):
            with self.assertRaises(ContractError):
                result_document(job, "completed", ["original_common", "Fact_Anchor"], progress_fixture(3, 3), changed)

    def test_result_rejects_non_native_or_nonfinite_metric(self) -> None:
        spec = ServingRequest.create(request_fixture(mode="backtest"))
        job = ServingJob.create(spec, config_fixture(spec), "6" * 64, "7" * 64)
        for value in (float("inf"), np.float64(1.0), True):
            row = {**row_fixture(), "raw_prediction": "LONG", "final_prediction": "LONG", "final_action": "LONG",
                   "net_return_pct": value, "metric_reason": None}
            with self.assertRaises(ValueError):
                result_document(job, "completed", ["original_fix"], progress_fixture(), [row])
        row = {**row_fixture(), "net_return_pct": 1.2, "metric_reason": None}
        with self.assertRaises(ContractError):
            result_document(job, "completed", ["original_fix"], progress_fixture(), [row])
        row["net_return_pct"] = 0.0
        self.assertEqual(result_document(job, "completed", ["original_fix"], progress_fixture(), [row])["rows"][0]["net_return_pct"], 0.0)


class ServingApiTests(unittest.TestCase):
    """Test HTTP thuần, không cần data provider, weights, API key hoặc network."""

    def setUp(self) -> None:
        app = Flask(__name__)
        app.register_blueprint(serving)
        self.client = app.test_client()

    def test_registry_and_blocked_preflight_are_strict_json_without_side_effects(self) -> None:
        old = digest(historical_registry())
        response = self.client.get("/api/serving/v1/registry")
        self.assertEqual(response.status_code, 200)
        json.loads(response.data)
        response = self.client.post("/api/serving/v1/preflight", json=request_fixture())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()["run_enabled"])
        self.assertNotIn("run_id", response.get_json())
        self.assertEqual(digest(historical_registry()), old)
        self.assertEqual(self.client.post("/api/serving/v1/jobs", json=request_fixture()).status_code, 404)

    def test_malformed_json_and_secret_fields_return_safe_errors(self) -> None:
        responses = [self.client.post("/api/serving/v1/preflight", data="{", content_type="application/json"),
                     self.client.post("/api/serving/v1/preflight", data="not-json"),
                     self.client.post("/api/serving/v1/preflight", json=None)]
        for value in ([], "private-secret", None, {**request_fixture(), "api_key": "private-secret"}):
            responses.append(self.client.post("/api/serving/v1/preflight", data=json.dumps(value), content_type="application/json"))
        for response in responses:
            self.assertEqual(response.status_code, 400)
            self.assertFalse(response.get_json()["run_enabled"])
            self.assertNotIn(b"private-secret", response.data)
            self.assertIn("code", response.get_json()["error"])

    def test_actual_app_registers_new_namespace_and_keeps_old_registry(self) -> None:
        with patch("core.realtime_loader.get_all_symbols_realtime", return_value=[]):
            web = importlib.import_module("web_interface")
        client = web.app.test_client()
        self.assertEqual(client.get("/api/serving/v1/registry").get_json()["version"], REGISTRY_VERSION)
        self.assertEqual(client.get("/api/experiments/registry").get_json(), historical_registry())
        with patch("web_interface.BacktestEngine") as engine:
            self.assertEqual(client.post("/api/backtest/start", json={"variant": "MT_BICL"}).status_code, 409)
            engine.assert_not_called()


if __name__ == "__main__":
    unittest.main()
