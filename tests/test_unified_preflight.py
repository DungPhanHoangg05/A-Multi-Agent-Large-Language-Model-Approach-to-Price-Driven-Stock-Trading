"""Kiểm split/assets/quota v2 và biên read-only; không thu forecast thị trường."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any
import unittest
from unittest.mock import patch

import pandas as pd

from core import unified_preflight as preflight
from core.unified_protocol import read, MANIFEST
from core.unified_preflight_assets import ASSETS, schedule

ROOT = Path(__file__).resolve().parents[1]


class PreflightTests(unittest.TestCase):
    """Nguồn thật đã chuẩn bị; kết quả chỉ là support và ABI của control offline."""
    @classmethod
    def setUpClass(cls) -> None:
        cls.alpha = read(ROOT, ASSETS + "/frozen_alpha_manifest.json")
        cls.providers = read(ROOT, ASSETS + "/provider_manifest.json")
        cls.parent = read(ROOT, MANIFEST, True)

    def test_102_ids_and_all_51_scope_bindings_are_preserved(self) -> None:
        self.assertEqual(len(self.alpha["causal_sources"]), 51)
        self.assertEqual({r["point_id"] for r in self.providers["points"]}, {r["runner_point_id"] for r in self.parent["points"]})
        self.assertEqual(self.alpha["unique_fitted_selectors"], 9)
        self.assertEqual(self.alpha["query_count"], 102)

    def test_holdout_is_frozen_before_first_anchor_for_every_symbol(self) -> None:
        grouped: dict[str, set[str]] = {}
        for row in self.alpha["scopes"]:
            symbol = row["symbol"]
            grouped.setdefault(symbol, set()).add(row["selector_sha256"])
            artifact = read(ROOT, self.alpha["causal_sources"][symbol + "/" + row["fold"]]["selector"])["payload"]
            earliest = min(p["date"] for p in self.parent["points"] if p["symbol"] == symbol)
            self.assertEqual(artifact["schedule"]["test_start"], earliest)
            self.assertLess(artifact["fit_end"], earliest)
            self.assertTrue(all(d < earliest for d in artifact["train_dates"] + artifact["validation_dates"]))
            self.assertEqual(artifact["config"]["min_train"], 60)
            self.assertEqual(artifact["config"]["min_validation"], 30)
            self.assertGreaterEqual(len(artifact["train_dates"]), 60)
            self.assertGreaterEqual(len(artifact["validation_dates"]), 30)
        self.assertTrue(all(len(values) == 1 for values in grouped.values()))

    def test_split_indices_embargo_and_horizon(self) -> None:
        frame = pd.DataFrame({"Datetime": pd.bdate_range("2018-01-02", periods=1800)})
        value = schedule(frame, 872, 929)
        days = frame.Datetime.dt.strftime("%Y-%m-%d").tolist()
        self.assertEqual(value["train_start"], days[319])
        self.assertEqual(value["train_end"], days[685])
        self.assertEqual(value["validation_start"], days[689])
        self.assertEqual(value["validation_end"], days[868])
        with self.assertRaises(ValueError):
            schedule(frame, 600, 657)

    def test_every_probe_has_eight_roles_and_native_bridge_unchanged(self) -> None:
        from core.variant_registry import VARIANTS
        for row in self.providers["points"]:
            record = read(ROOT, row["path"])
            self.assertTrue(record["native_request_unchanged"])
            self.assertEqual(set(record["preparations"]), {v.id for v in VARIANTS})
            self.assertIn("CONTROL", record["scope"])
            self.assertNotIn("outcome", record)
            self.assertNotIn("query_y", record["context"]["query"])

    def test_ood_bank_fallback_is_explicit_and_has_no_fake_raw_response(self) -> None:
        for row in self.providers["points"]:
            if row["point_id"].split("-", 1)[0] in ("FPT", "MWG", "VCB", "VNM"):
                continue
            record = read(ROOT, row["path"])
            for variant in ("bayesian_v1", "C2", "A_tp_pool", "B_semantic"):
                prepared = record["preparations"][variant]
                self.assertTrue(prepared["prepared"]["trace"]["fallback"])
                self.assertEqual(prepared["prepared"]["trace"]["reason"], "NO_SAME_SYMBOL_FROZEN_BANK_OOD")
                self.assertIsNone(prepared["probe_raw"])
                self.assertEqual(prepared["probe_policy"]["reason"], "FALLBACK_ORIGINAL")

    def test_mt_support_masks_and_fallbacks_are_not_relabelled_as_active(self) -> None:
        self.assertEqual(sum(row["mt_eligible"] for row in self.providers["points"]), 66)
        for row in self.providers["points"]:
            record = read(ROOT, row["path"])
            item = record["preparations"]["MT_BICL"]
            self.assertEqual(row["mt_eligible"], row["mt_reason"] == "SUPPORTED")
            if not row["mt_eligible"]:
                self.assertIsNone(item["prepared"]["request"])
                self.assertIsNone(item["probe_raw"])
                self.assertTrue(item["probe_policy"]["bypass"])

    def test_news_missing_and_next_day_masks_are_preserved(self) -> None:
        news = read(ROOT, ASSETS + "/news_manifest.json")
        self.assertFalse(news["content_pit_certified"])
        self.assertEqual(len(news["points"]), 102)
        self.assertEqual(sum(row["unavailable"] for row in news["points"]), 79)
        for row in news["points"]:
            cutoff = pd.Timestamp(row["point_id"].split("-", 1)[1])
            self.assertEqual(row["unavailable"], len(row["visible_articles"]) < 3)
            if row["unavailable"]:
                self.assertIsNone(row["mean_score"])
            for article in row["visible_articles"]:
                self.assertGreaterEqual(pd.Timestamp(article["available_at"]).normalize(), pd.Timestamp(article["published"]).normalize() + pd.Timedelta(days=1))
                self.assertLessEqual(pd.Timestamp(article["available_at"]).normalize(), cutoff)

    def test_current_quota_is_attested_and_model_catalog_is_get_only(self) -> None:
        attest = read(ROOT, ASSETS + "/quota_attestation.json")
        meta = read(ROOT, ASSETS + "/provider_metadata.json")
        self.assertEqual(attest["organizations_independent"], 5)
        self.assertFalse(attest["provider_org_ids_verified"])
        self.assertEqual(meta["metadata_requests"], 5)
        self.assertEqual(meta["inference_requests"], 0)
        self.assertEqual(meta["method"], "GET")
        self.assertTrue(meta["all_required_models_listed"])
        self.assertEqual(len({r["credential_hmac"] for r in meta["rows"]}), 5)

    def test_quota_combines_models_in_one_org_and_keeps_unknown_reserve(self) -> None:
        limits = {"rpm": 30, "rpd": 1000, "tpm": 8000, "tpd": 200000}
        history = {1: [{"started_at": 0., "reserved_tokens": 8000, "status": "unknown", "model": "A"}]}
        result = preflight.pooled_schedule(history, [{"org": 1, "tokens": 1, "model": "B"}], 0., limits, 0.)
        self.assertGreater(result["hours_with_latency_scenario"] * 3600, 61.)
        with self.assertRaises(ValueError):
            preflight.pooled_schedule(history, [{"org": 1, "tokens": 8001}], 0., limits)

    def test_independent_org_queues_can_progress_without_switching_keys(self) -> None:
        limits = {"rpm": 30, "rpd": 1000, "tpm": 8000, "tpd": 200000}
        history = {1: [], 2: []}
        tasks = [{"org": 1, "tokens": 8000}, {"org": 2, "tokens": 8000}]
        result = preflight.pooled_schedule(history, tasks, 0., limits, 5.)
        self.assertEqual(result["hours_with_latency_scenario"] * 3600, 5.)
        self.assertEqual(result["reserved_tokens"], 16000)

    def test_package_is_pinned_and_all_members_match_final_assets(self) -> None:
        import zipfile
        self.assertEqual(hashlib.sha256((ROOT / preflight.PACKAGE).read_bytes()).hexdigest(), preflight.ASSET_SHA256)
        with zipfile.ZipFile(ROOT / preflight.PACKAGE) as archive:
            manifest = json.loads(archive.read("assets_manifest.json"))
            self.assertEqual(len(archive.namelist()), 287)
            for name, expected in manifest["members"].items():
                raw = archive.read(name)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), expected["sha256"])
                self.assertEqual(raw, (ROOT / name).read_bytes())

    def test_design_mutation_cannot_be_hidden_by_resigning_manifest(self) -> None:
        original = preflight.read
        def altered(root: Path, name: str, *args: Any, **kwargs: Any) -> Any:
            value = original(root, name, *args, **kwargs)
            if name == preflight.PROTOCOL_V2:
                value["repeats"] = 1
            return value
        with patch.object(preflight, "read", side_effect=altered), self.assertRaises(ValueError):
            preflight.validate_design(ROOT)

    def test_default_verify_does_not_import_model_client_or_read_keys(self) -> None:
        code = """
import runpy,sys
sys.path.insert(0,sys.argv.pop(1))
sys.argv=['prepare_unified_comparison_v2.py','verify']
runpy.run_path('scripts/prepare_unified_comparison_v2.py',run_name='__main__')
assert not {'torch','httpx','groq','dotenv','core.causal_alpha','core.unified_asset_providers'}.intersection(sys.modules)
"""
        result = subprocess.run([sys.executable, "-I", "-X", "utf8", "-c", code, str(ROOT)], cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf8"))
        self.assertFalse(json.loads(result.stdout)["api"])

    def test_metadata_audit_sends_only_five_gets_and_never_serializes_keys(self) -> None:
        import io
        from types import SimpleNamespace
        from scripts.audit_unified_provider import audit, NoRedirect
        values = {f"GROQ_ORG_{i}_API_KEY": "test-only-secret-" + str(i) for i in range(1, 6)}
        body = json.dumps({"data": [{"id": m, "active": True, "context_window": 131072, "owned_by": "test"}
                                    for m in ("openai/gpt-oss-20b", "qwen/qwen3.8-27b")]})
        requests = []
        def opened(request: Any, timeout: int) -> Any:
            requests.append(request)
            response = io.StringIO(body)
            response.status = 200
            response.headers = {"Date": "Mon, 09 Nov 2026 18:50:44 GMT"}
            return response
        with patch("dotenv.dotenv_values", return_value=values), patch("scripts.audit_unified_provider.build_opener", return_value=SimpleNamespace(open=opened)):
            result = audit(Path("unused-test-only"))
        self.assertEqual(len(requests), 5)
        self.assertTrue(all(r.get_method() == "GET" and r.full_url == "https://api.groq.com/openai/v1/models" and r.data is None for r in requests))
        serialized = json.dumps(result)
        self.assertTrue(all(key not in serialized for key in values.values()))
        self.assertEqual(result["inference_requests"], 0)
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.example"))

    def test_fresh_recipe_exports_prices_and_loads_through_causal_sources(self) -> None:
        from tempfile import TemporaryDirectory, gettempdir
        from core import unified_preflight_assets as assets
        from core.causal_bridge import CausalSources
        from core.unified_protocol import BANK
        frame = assets.frames(ROOT)["FPT"]
        bank = read(ROOT, BANK)
        scope = next(row for row in bank["schedule"] if row["symbol"] == "FPT")
        with TemporaryDirectory(prefix="u06-price-export-test-") as folder:
            root = Path(folder).resolve()
            self.assertTrue(root.is_relative_to(Path(gettempdir()).resolve()))
            with patch.object(assets, "frames", return_value={"FPT": frame}), patch.object(assets, "read", return_value={"schedule": [scope]}):
                result = assets.frozen_alpha_assets(root)
            sources = result["causal_sources"]
            source_hashes = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                             for entry in sources.values() for name in entry.values()}
            reader = CausalSources({"causal_sources": sources, "source_hashes": source_hashes}, root)
            selector, exported, _ = reader.entries["FPT/" + scope["fold"]]
            cutoff = result["scopes"][0]["queries"][0]["point_id"].split("-", 1)[1]
            actual = selector.predict(exported.loc[exported.Datetime <= cutoff], cutoff)
            expected = read(root, result["scopes"][0]["queries"][0]["projection"])
            self.assertEqual(actual, expected)
            self.assertEqual(result["query_count"], 2)


if __name__ == "__main__":
    unittest.main()
