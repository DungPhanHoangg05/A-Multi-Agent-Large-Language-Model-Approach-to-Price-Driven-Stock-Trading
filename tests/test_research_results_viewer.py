"""Đối soát viewer U09 với artifact khóa, filter/export và đường legacy độc lập."""
from __future__ import annotations

from copy import deepcopy
import csv
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import zipfile

from flask import Flask

from core.research_results import (ARTIFACTS, PACKAGE, PACKAGE_SHA256, PREFIX, RUN_ID, SUPPORT,
                                   ResearchResults, _verified)
from core.unified_contracts import json_bytes
from utils.research_view import csv_cell, export_bytes, view
from utils.research_web import research

ROOT = Path(__file__).resolve().parents[1]


class ResearchReaderTests(unittest.TestCase):
    """Dùng gói thực đã seal; không refit hoặc bootstrap để tạo expected mới."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.reader = ResearchResults(ROOT)
        with zipfile.ZipFile(ROOT / PACKAGE) as archive:
            cls.original = json.loads(archive.read(PREFIX + "results.json"))

    def test_verified_package_and_artifacts_match_exact_bytes(self) -> None:
        self.assertEqual(self.reader.result(), self.original)
        with zipfile.ZipFile(ROOT / PACKAGE) as archive:
            for name in ARTIFACTS:
                self.assertEqual(self.reader.artifact(name), archive.read(PREFIX + name), name)
        self.assertEqual(self.reader.support()["sentiment_missing"], 79)
        self.assertEqual(self.reader.provenance()["package_sha256"], PACKAGE_SHA256)

    def test_no_archive_python_or_evaluator_imported_and_cache_is_content_bound(self) -> None:
        before = _verified.cache_info().hits
        with patch("core.unified_experiment.verify_run", side_effect=AssertionError("Không replay evaluator")), \
             patch("core.unified_analysis.analysis.analyze", side_effect=AssertionError("Không bootstrap"), create=True):
            reader = ResearchResults(ROOT)
            data = view(reader, {})
        self.assertGreater(_verified.cache_info().hits, before)
        self.assertEqual(data["summary"], [r for r in self.original["summary"] if r["method"] not in
                         ("CASH_EVERY_CYCLE", "ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS")])
        data["summary"][0]["accuracy"] = 999
        self.assertNotEqual(self.reader.result()["summary"][0]["accuracy"], 999)

    def test_altered_package_or_support_rejected_even_with_same_mtime(self) -> None:
        for field in (PACKAGE, SUPPORT):
            with TemporaryDirectory() as folder:
                root = Path(folder)
                for name in (PACKAGE, SUPPORT):
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes((ROOT/name).read_bytes())
                ResearchResults(root)
                path = root/field
                original_stat = path.stat()
                raw = bytearray(path.read_bytes()); raw[-20] ^= 1; path.write_bytes(raw)
                os.utime(path, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
                with self.assertRaises(ValueError): ResearchResults(root)

    def test_table_numbers_nulls_and_no_hidden_portfolio_aggregation(self) -> None:
        accounts = self.reader.table("accounts")
        self.assertEqual(len(accounts), 1530)
        self.assertEqual(len(self.reader.table("predictions")), 3060)
        self.assertEqual(len(self.reader.table("cycles")), 3060)
        self.assertEqual(len(self.reader.table("daily_nav")), 93330)
        self.assertIs(type(accounts[0]["return_pct"]), float)
        self.assertIsNone(accounts[0]["annualized_sharpe"])
        cash = [r for r in self.reader.table("cycles") if r["action"] == "CASH"]
        self.assertTrue(cash)
        self.assertTrue(all(r["strategy_return"] == 0 for r in cash))
        for name in ("../results", "receipt", "prior_traces"):
            with self.assertRaises(ValueError): self.reader.table(name)
        with self.assertRaises(ValueError): self.reader.artifact("../../secret")

    def test_filters_keep_full_cohort_summary_bands_and_distinguish_repeat_rows(self) -> None:
        full = view(self.reader, {})
        filtered = view(self.reader, {"repeat": "1", "symbol": "BHN", "fold": "f2025_q4"})
        self.assertEqual(filtered["summary"], full["summary"])
        self.assertEqual(filtered["contrasts"], full["contrasts"])
        self.assertEqual(filtered["support"]["points"], 102)
        self.assertTrue(all(r["repeat"] == 1 and r["symbol"] == "BHN" for r in filtered["details"]["rows"]))
        self.assertEqual(len(filtered["per_repeat"]), 8)
        self.assertEqual(len(filtered["classification_by_repeat"]), 8)
        common = view(self.reader, {"methods": "bayesian_v1,MT_BICL", "baseline": "original_common"})
        self.assertEqual(len(common["contrasts"]), 4)
        self.assertTrue(all(r["baseline"] == "original_common" for r in common["contrasts"]))
        self.assertEqual(common["contrasts"], [r for r in self.original["contrasts"] if
                         r["method"] in ("bayesian_v1", "MT_BICL") and r["baseline"] == "original_common"])

    def test_empty_detail_support_not_padded_and_unknown_filters_rejected(self) -> None:
        result = view(self.reader, {"symbol": "BHN", "fold": "b2023_h2"})
        self.assertEqual(result["details"]["rows"], [])
        self.assertEqual(result["details"]["total"], 0)
        self.assertEqual(len(result["summary"]), 8)
        for query in ({"symbol": "XXX"}, {"fold": "bad"}, {"repeat": "3"}, {"repeat": "-1"},
                      {"baseline": "MT_BICL"}, {"methods": "Original_common"}, {"methods": "C2,C2"},
                      {"methods": ""}, {"limit": "201"}, {"offset": "-1"}, {"limit": "1.0"},
                      {"start_date": "2023-01-01"}, {"table": "../results"}):
            with self.subTest(query=query), self.assertRaises(ValueError): view(self.reader, query)

    def test_exports_keep_values_units_identity_and_all_matching_details(self) -> None:
        query = {"methods": "original_fix,bayesian_v1", "repeat": "0", "limit": "2"}
        page = view(self.reader, query)
        result = view(self.reader, query, export=True)
        self.assertEqual(len(page["details"]["rows"]), 2)
        self.assertEqual(len(result["details"]["rows"]), 204)
        raw, _ = export_bytes(result, "json")
        self.assertEqual(json.loads(raw), result)
        raw, _ = export_bytes(result, "csv")
        rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(float(rows[0]["mean_account_return_pct"]), result["summary"][0]["mean_account_return_pct"])
        self.assertEqual(rows[0]["package_sha256"], PACKAGE_SHA256)
        self.assertIn("strategy_return", json.loads(rows[0]["units_json"]))
        raw, _ = export_bytes(result, "csv", "details")
        self.assertEqual(len(list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))), 204)
        for format_name, table_name in (("exe", "summary"), ("csv", "../secret")):
            with self.assertRaises(ValueError): export_bytes(result, format_name, table_name)

    def test_csv_formulas_are_neutralized_without_changing_negative_numbers(self) -> None:
        for value in ("=SUM(A1)", " +cmd", "-cmd", "@call", "\tcmd", "\rdata", "\nline"):
            self.assertTrue(csv_cell(value).startswith("'"))
        self.assertEqual(csv_cell(-.7), -.7)
        result = deepcopy(view(self.reader, {"methods": "original_fix"}))
        result["summary"][0]["method"] = '=HYPERLINK("bad")'
        result["summary"][0]["accuracy"] = None
        raw, _ = export_bytes(result, "csv")
        row = next(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
        self.assertTrue(row["method"].startswith("'="))
        self.assertEqual(row["accuracy"], "")


class ResearchApiTests(unittest.TestCase):
    """HTTP dùng package thật và Flask test client; không có external network."""

    def setUp(self) -> None:
        app = Flask(__name__)
        app.register_blueprint(research)
        self.client = app.test_client()

    def test_catalog_defaults_to_verified_u09_and_json_is_native(self) -> None:
        response = self.client.get("/api/research-results/runs")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["default"], RUN_ID)
        data = self.client.get(f"/api/research-results/{RUN_ID}").get_json()
        json_bytes(data)
        self.assertEqual(len(data["summary"]), 8)
        self.assertEqual(data["coverage"]["complete"], 2448)

    def test_export_and_original_figure_match_verified_projection(self) -> None:
        base = f"/api/research-results/{RUN_ID}"
        result = self.client.get(base + "/export?methods=MT_BICL&repeat=2&format=json").get_json()
        self.assertEqual(len(result["summary"]), 1)
        self.assertEqual(result["details"]["total"], 102)
        response = self.client.get(base + "/export?methods=MT_BICL&format=csv&export_table=details")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        image = self.client.get(base + "/artifacts/return_contrasts.png")
        self.assertEqual(hashlib.sha256(image.data).hexdigest(), "cbe8bc8b1f9f09bd85726273fa84da83581027abf9e74d8149c307dcd67d0b03")

    def test_invalid_filters_duplicate_keys_and_path_escape_do_not_read_files(self) -> None:
        for suffix in ("?methods=bad", "?limit=10&limit=11", "/export?format=exe", "/export?export_table=../secret",
                       "/artifacts/manifest.json", "/artifacts/..%2F..%2Fsecret"):
            with self.subTest(suffix=suffix):
                self.assertIn(self.client.get(f"/api/research-results/{RUN_ID}" + suffix).status_code, (400, 404))
        self.assertEqual(self.client.get("/api/research-results/another-run").status_code, 404)

    def test_missing_package_empty_catalog_and_bad_package_safe_error(self) -> None:
        with TemporaryDirectory() as folder, patch("utils.research_web.ROOT", Path(folder)):
            self.assertEqual(self.client.get("/api/research-results/runs").get_json()["runs"], [])
            self.assertEqual(self.client.get(f"/api/research-results/{RUN_ID}").status_code, 400)
            path = Path(folder)/PACKAGE
            path.parent.mkdir(parents=True)
            path.write_bytes(b"private-secret-bad-archive")
            response = self.client.get("/api/research-results/runs")
            self.assertEqual(response.status_code, 400)
            self.assertNotIn(b"private-secret", response.data)

    def test_real_page_and_language_routes_keep_legacy_selection(self) -> None:
        with patch("core.realtime_loader.get_all_symbols_realtime", return_value=[]):
            web = importlib.import_module("web_interface")
        client = web.app.test_client()
        for language, title in (("vi", "Thực nghiệm giao dịch"), ("en", "Trading experiments")):
            response = client.get("/experiments?lang=" + language)
            self.assertEqual(response.status_code, 200)
            self.assertIn(title, response.get_data(as_text=True))
            self.assertIn(b'value="original_fix" selected', response.data)
            self.assertIn(b'/static/js/experiments/main.js', response.data)
        self.assertEqual(client.get("/api/experiments/registry").get_json()["version"], "unified_variant_registry_v2")
        self.assertEqual(client.get(f"/api/research-results/{RUN_ID}").status_code, 200)


if __name__ == "__main__":
    unittest.main()
