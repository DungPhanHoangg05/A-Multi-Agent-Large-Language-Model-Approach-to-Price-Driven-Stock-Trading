"""Kiểm khóa thiết kế, support, quota và thứ tự; không chấp nhận release giả."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from core import unified_protocol as protocol
from core.unified_contracts import digest, json_bytes

ROOT = Path(__file__).resolve().parents[1]


class UnifiedProtocolTests(unittest.TestCase):
    """Preflight được phép BLOCKED; test không biến trạng thái đó thành release."""
    @classmethod
    def setUpClass(cls) -> None:
        cls.design = protocol.read(ROOT, protocol.PROTOCOL)
        cls.manifest = protocol.build(ROOT, cls.design)

    def test_design_digest_and_all_eight_roles_are_locked(self) -> None:
        protocol.validate_protocol(self.design)
        self.assertEqual(digest(self.design), protocol.DESIGN_SHA256)
        self.assertEqual(set(protocol.execution_order(self.design["variants"])), set(protocol.BRANCHES))
        for field, replacement in (("repeats", 1), ("realizations", 2), ("input_profile", "native_common_v1")):
            with self.subTest(field=field):
                wrong = deepcopy(self.design); wrong[field] = replacement
                with self.assertRaises(ValueError):
                    protocol.validate_protocol(wrong)

    def test_api_spend_multiplicity_and_subset_cannot_be_changed(self) -> None:
        for area, field, value in (("authorization", "api", True), ("authorization", "spend_limit_usd", 1),
                                  ("statistics", "joint_family_size", 5), ("cohort", "no_automatic_subset", False),
                                  ("cohort", "split", "EXPAND_UNTIL_PASS"), ("budget", "smoke_executions", 0)):
            with self.subTest(area=area, field=field):
                wrong = deepcopy(self.design); wrong[area][field] = value
                with self.assertRaises(ValueError):
                    protocol.validate_protocol(wrong)

    def test_donor_102_calendar_support_and_bhn_suffix(self) -> None:
        counts = self.manifest["counts"]
        self.assertEqual((counts["planned"], counts["calendar_verified"], counts["scopes"], counts["core4"]), (102, 102, 51, 48))
        bhns = [r for r in self.manifest["points"] if r["symbol"] == "BHN"]
        self.assertEqual(len(bhns), 6)
        self.assertTrue(all(r["raw_decision_index"] - r["suffix_decision_index"] == 673 for r in bhns))
        self.assertEqual(counts["pilot48_overlap"], 16)
        self.assertEqual(counts["cutoff_dates"], 12)

    def test_validation_ceiling_is_insufficient_without_fitting_or_retuning(self) -> None:
        self.assertEqual(self.manifest["alpha_support"]["config"]["min_validation"], 30)
        self.assertEqual(self.manifest["alpha_support"]["compatible_scopes"], 0)
        self.assertFalse(self.manifest["alpha_support"]["numeric_fit_performed"])
        for scope in self.manifest["scopes"]:
            self.assertIn(scope["validation_cycle_ceiling"], (18, 19, 20, 21))
            self.assertIn("ALPHA_VALIDATION_CYCLE_CEILING_BELOW_MINIMUM", scope["blockers"])
            self.assertLess(scope["train_max_exit"], scope["validation_start"])
            self.assertLess(scope["validation_max_exit"], scope["test_start"])

    def test_all_calls_and_shared_repeats_have_explicit_budget(self) -> None:
        budget = self.manifest["budget"]
        self.assertEqual(budget["decision_forecast_slots"], 2448)
        self.assertEqual(budget["new_shared_preparations"], 102)
        self.assertEqual(budget["new_vision_executions"], 204)
        self.assertEqual(budget["nominal_http_upper_bound_including_smoke"], 2662)
        self.assertEqual(budget["http_attempt_cap_including_repairs"], 7986)
        self.assertEqual(budget["retry_additional_reserve"], 5324)
        self.assertEqual(budget["history_collection_calls"], 0)
        for key in ("token_reserve", "duration_hours", "spend_usd"):
            self.assertIsNone(budget[key])

    def test_counterbalance_is_deterministic_and_respects_every_dependency(self) -> None:
        from core.variant_registry import registry_document
        orders = self.manifest["execution_orders"]
        self.assertEqual(len(orders), 306)
        self.assertEqual(len({tuple(protocol.ordered_branches(i)) for i in range(8)}), 8)
        from collections import Counter
        positions = Counter(slot["order"].index("original_fix") for slot in orders)
        self.assertEqual(set(positions), set(range(8)))
        self.assertLessEqual(max(positions.values()) - min(positions.values()), 1)
        for i, slot in enumerate(orders):
            order = slot["order"]
            self.assertEqual(order, protocol.ordered_branches(i))
            self.assertEqual(set(order), set(protocol.BRANCHES))
            for variant in registry_document()["variants"]:
                for dependency in variant["dependencies"]:
                    self.assertLess(order.index(dependency), order.index(variant["id"]))
        with self.assertRaises(ValueError):
            protocol.ordered_branches(-1)

    def test_existing_lexical_runner_is_not_falsely_certified(self) -> None:
        self.assertIn("COUNTERBALANCED_HOSTED_RUNNER_PENDING_U07_U08", self.manifest["blockers"])
        self.assertEqual(self.manifest["status"], "DESIGN_LOCKED_RELEASE_BLOCKED")
        self.assertEqual(self.manifest["counts"]["collection_eligible"], 0)
        self.assertEqual(self.manifest["counts"]["complete_new"], 0)
        self.assertEqual(self.manifest["counts"]["not_started"], 102)
        self.assertFalse(self.manifest["authorization"]["api"])
        self.assertEqual(self.manifest["native_rowwise_causal_gate"], "FAIL")

    def test_missing_quota_is_not_reported_as_zero_or_assumed_expired(self) -> None:
        self.assertEqual(len(self.manifest["quota_ledgers"]), 15)
        self.assertTrue(all(r["status"] in ("MISSING_LOCAL_DO_NOT_ASSUME_ZERO", "PRESENT_DEDUPLICATED_NOT_CLEARED_FOR_NEW_RUN")
                            for r in self.manifest["quota_ledgers"]))
        self.assertFalse(self.manifest["budget"]["current_quota_verified"])
        self.assertFalse(self.manifest["budget"]["live_model_availability_verified"])
        self.assertEqual(self.manifest["quota_history"]["unique_org_request_ids"], 497)
        self.assertEqual(self.manifest["quota_history"]["charged_or_reserved_tokens"], 1140404)
        self.assertFalse(self.manifest["quota_history"]["window_expiry_assumed"])

    def test_frozen_student_files_verified_without_loading_weights(self) -> None:
        self.assertEqual(len(self.manifest["assets"]["student_teacher"]), 2)
        self.assertTrue(all(r["status"] == "BYTES_VERIFIED_NOT_PROVIDER_CERTIFIED"
                            for r in self.manifest["assets"]["student_teacher"]))
        self.assertFalse(self.manifest["market_models_fitted"])
        self.assertEqual(self.manifest["hosted_calls"], 0)

    def test_outcome_poison_cannot_change_selected_cohort_or_order(self) -> None:
        bank = protocol.read(ROOT, protocol.BANK)
        grid = protocol.read(ROOT, protocol.GRID)
        dates = {}
        import csv
        for path in (ROOT / protocol.PRICE).glob("*.csv"):
            with path.open(encoding="utf-8-sig", newline="") as handle:
                dates[path.stem] = [r["date"] for r in csv.DictReader(handle)]
        readiness = protocol.read(ROOT, protocol.READINESS)
        offsets = {s: v["excluded_prefix_rows"] for s, v in readiness["price_views"].items()}
        pilot = protocol.read(ROOT, "docs/plan/week11/free_pilot_inputs.json", True)["units"]
        expected = protocol.cohort(grid, bank, dates, offsets, protocol.causal_config(ROOT), pilot)
        for row in grid:
            row.update(net_return=1e100, actual_direction="UP", action="LONG")
        for row in bank["units"]:
            row.update(net_return=-1e100, actual_direction="DOWN", upstream="POISONED_PREVIOUS_RESPONSE")
        self.assertEqual(protocol.cohort(grid, bank, dates, offsets, protocol.causal_config(ROOT), pilot), expected)

    def test_purge_and_calendar_corruption_fail_before_manifest(self) -> None:
        bank = protocol.read(ROOT, protocol.BANK)
        first = bank["schedule"][0]
        wrong = deepcopy(bank)
        wrong["schedule"][0]["validation"][0] = max(first["train"]) + 3
        with self.assertRaisesRegex(ValueError, "purge"):
            protocol.cohort([], wrong, {first["symbol"]: ["2020-01-01"] * 2000},
                            {first["symbol"]: 0}, protocol.causal_config(ROOT), [])

    def test_resigned_manifest_is_rejected_by_reconstruction(self) -> None:
        recorded = deepcopy(self.manifest)
        recorded["counts"]["collection_eligible"] = 102
        with patch.object(protocol, "read", side_effect=[self.design, recorded]), patch.object(protocol, "build", return_value=self.manifest):
            with self.assertRaisesRegex(ValueError, "tái dựng"):
                protocol.verify(ROOT)

    def test_source_and_donor_mismatch_fail_closed(self) -> None:
        raw = protocol.git_blob
        with patch.object(protocol, "git_blob", side_effect=lambda root, commit, name:
                          raw(root, commit, name) + (b"x" if commit == protocol.DONOR else b"")):
            with self.assertRaisesRegex(ValueError, "Git donor"):
                protocol.build(ROOT, self.design)
        with patch.object(protocol, "git_blob", side_effect=lambda root, commit, name:
                          raw(root, commit, name) + (b"x" if commit == protocol.BASE else b"")):
            with self.assertRaisesRegex(ValueError, "Git U05"):
                protocol.build(ROOT, self.design)

    def test_safe_paths_and_json_native_types(self) -> None:
        for name in ("../secret", "C:/secret", ".env", "outputs/../secret", "core\\secret", "/secret"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                protocol.safe(ROOT, name)
        self.assertEqual(json.loads(json_bytes(self.manifest)), self.manifest)

    def test_cli_isolated_verify_opens_no_heavy_model_or_network_client(self) -> None:
        code = """
import sys,runpy
sys.path.insert(0,sys.argv.pop(1))
sys.argv=['prepare_unified_comparison.py','verify']
runpy.run_path('scripts/prepare_unified_comparison.py',run_name='__main__')
assert not {'torch','groq','httpx','core.bayesian_retriever','core.regime_detector','core.causal_alpha'}.intersection(sys.modules)
"""
        result = subprocess.run([sys.executable, "-I", "-X", "utf8", "-c", code, str(ROOT)], cwd=ROOT,
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "PASS_OFFLINE_PREFLIGHT")

    def test_cli_never_overwrites_sealed_manifest(self) -> None:
        before = (ROOT / protocol.MANIFEST).read_bytes()
        result = subprocess.run([sys.executable, "-I", "-X", "utf8", "scripts/prepare_unified_comparison.py", "build"],
                                cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((ROOT / protocol.MANIFEST).read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
