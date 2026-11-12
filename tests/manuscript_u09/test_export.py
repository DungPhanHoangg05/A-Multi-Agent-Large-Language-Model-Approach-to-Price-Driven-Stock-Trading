"""Kiểm nguồn khóa, đơn vị/null, lineage và release không ghi đè của generator U09."""
from __future__ import annotations

from copy import deepcopy
import io
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import zipfile

from core.manuscript_u09.sources import (METHODS, PACKAGE, PREFIX, binding, decoded,
    encoded, load, members, safe_name, semantic, validate)
from core.manuscript_u09.render import at, escape, number, panel, render
from core.manuscript_u09.release import INSTALL, RELEASE, SOURCES, build, destination, verify
from core.revision_reproducibility import offline_guard

ROOT = Path(__file__).resolve().parents[2]


class ExportTests(unittest.TestCase):
    """Dùng dữ liệu đã seal; oracle chỉ đối soát field/đơn vị, không ước lượng lại U09."""

    @classmethod
    def setUpClass(cls) -> None:
        """Chỉ load/render một fixture thật, chặn mạng và mọi đường phân tích lại."""
        with offline_guard(), patch("core.unified_analysis.analysis.analyze", side_effect=AssertionError("Cấm ước lượng lại")), \
                patch("dotenv.dotenv_values", side_effect=AssertionError("Cấm đọc key")):
            cls.bundle = load(ROOT)
            cls.outputs = render(cls.bundle)

    def test_locked_package_and_historical_receipt(self) -> None:
        """Hash/receipt/frozen support phải được kiểm trước mọi metric render."""
        self.assertEqual(self.bundle["historical_source_commit"], "384725a66fec074700963fac67c358b28b842092")
        facts = self.bundle["facts"]
        self.assertEqual((facts["points"], facts["accounts"], facts["sentiment_missing"], facts["raw_decision_responses"]),
            (102, 51, 79, 1290))
        with TemporaryDirectory() as folder:
            path = Path(folder)/PACKAGE
            path.parent.mkdir(parents=True)
            path.write_bytes(b"changed")
            with self.assertRaises(ValueError):
                load(Path(folder))

    def test_archive_paths_duplicates_and_members_cannot_bypass_pin(self) -> None:
        """Giữ fail-closed cho tên nguồn không an toàn và tập member khác manifest."""
        for name in ("../escape", "/absolute", "C:/drive", "a\\b", "a/../b", "a/./b", "a:ads", "a."):
            with self.subTest(name=name), self.assertRaises(ValueError):
                safe_name(name)
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr("manifest.json", encoded({"members": {}}))
            archive.writestr("extra", b"bad")
        with zipfile.ZipFile(io.BytesIO(stream.getvalue())) as archive, self.assertRaises(ValueError):
            members(archive)

    def test_envelope_and_nonfinite_sources_are_rejected(self) -> None:
        """Không dùng envelope sai hoặc giá trị nonfinite để tạo số liệu hiển thị."""
        self.assertEqual(decoded(encoded({"payload": {"x": None}, "sha256": semantic({"x": None})})), {"x": None})
        for raw in (b'{"x":NaN}', b'{"x":Infinity}', encoded({"payload": {"x": 2}, "sha256": semantic({"x": 1})})):
            with self.assertRaises(ValueError):
                decoded(raw)

    def test_schema_rejects_support_and_role_changes(self) -> None:
        """Không sinh bảng thành công trên subset, role thiếu hoặc mẫu số bị thay."""
        for key in ("points", "accounts_per_repeat", "repeats"):
            result = deepcopy(self.bundle["result"])
            result[key] -= 1
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(result)
        result = deepcopy(self.bundle["result"])
        result["summary"][-1] = result["summary"][0]
        with self.assertRaises(ValueError):
            validate(result)
        result = deepcopy(self.bundle["result"])
        result["summary"][3]["bypass_forecasts"] = 302
        with self.assertRaises(ValueError):
            validate(result)

    def test_contrasts_keep_family_order_endpoint_and_joint_band(self) -> None:
        """Không tráo baseline hoặc lấy band của endpoint/family khác."""
        for key, value in (("baseline", "original_common"), ("endpoint", "balanced_accuracy_percentage_points"),
                ("effect_pp", 100.), ("band95_low_pp", None)):
            result = deepcopy(self.bundle["result"])
            result["contrasts"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(result)
        result = deepcopy(self.bundle["result"])
        result["contrasts"].pop()
        with self.assertRaises(ValueError):
            validate(result)

    def test_percent_pp_vnd_and_undefined_scaling(self) -> None:
        """BA/return đã là percent; ratio LONG/F1 mới nhân 100 và phí đổi kVND một lần."""
        self.assertEqual(number(51.844155844, digits=2), "51.84")
        self.assertEqual(number(.225490196, scale=100., digits=2), "22.55")
        self.assertEqual(number(111782.302992, scale=.001), "111.782")
        self.assertEqual(number(.3266057766), "0.327")
        self.assertEqual(number(-.0000001), "0.000")
        self.assertEqual(number(None), "NA")
        for value in (True, "0.5", float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                number(value)

    def test_ten_rows_include_both_cycle_controls_and_fallback(self) -> None:
        """Không bỏ control, kết quả âm hoặc fallback gần toàn bộ để làm đẹp bảng."""
        text = self.outputs["comparison.tex"].decode()
        self.assertIn("Native & -0.653 & 51.84 & 22.55 & 306 & 0 & 102", text)
        self.assertIn("C2 & -1.030 & 45.75 & 29.08 & 3 & 303 & 102", text)
        self.assertIn("CASH & 0.000 & 50.00 & 0.00 & 0 & 306 & 102", text)
        self.assertIn("Always-LONG & -3.000 & 50.00 & 100.00 & 0 & 306 & 102", text)
        self.assertIn("not continuous buy-and-hold", text)
        self.assertEqual(len([line for line in text.splitlines() if line.endswith(" & 102 " + chr(92)*2)]), 10)

    def test_macros_are_valid_unique_and_disjoint_from_legacy(self) -> None:
        """Tên macro chỉ gồm chữ, prefix Unified riêng; không định nghĩa lại Full/Base."""
        text = self.outputs["summary_numbers.tex"].decode()
        names = re.findall(r"\\newcommand\{\\([A-Za-z]+)\}", text)
        self.assertEqual(len(names), len(text.splitlines()))
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(all(n.startswith("Unified") for n in names))
        legacy = (ROOT/"paper/generated/summary_numbers.tex").read_text(encoding="utf-8")
        self.assertTrue(set(names).isdisjoint(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}", legacy)))
        self.assertIn(r"\newcommand{\UnifiedVOneCommonReturnEffect}{0.327}", text)
        self.assertIn(r"\newcommand{\UnifiedVOneNativeReturnLow}{-0.362}", text)

    def test_every_numeric_cell_resolves_to_exact_literal_and_unit(self) -> None:
        """Lineage phải trỏ literal thật; phép đổi đơn vị và rounding có thể đối soát độc lập."""
        entries = decoded(self.outputs["numeric_cells.json"])
        self.assertGreater(len(entries), 700)
        for row in entries:
            document = self.bundle["result"] if row["source_package"] == PACKAGE else self.bundle["facts"]
            self.assertEqual(at(document, row["pointer"]), row["value"])
            self.assertEqual(number(row["value"], row["scale"], row["digits"]), row["rendered"])
        native = next(r for r in entries if r["output"] == "comparison.tex" and r["pointer"] == "/summary/0/mean_account_return_pct")
        self.assertEqual((native["unit"], native["scale"], native["rendered"]), ("percent", 1., "-0.653"))

    def test_null_mcc_missing_class_and_annualization_preserved_in_companions(self) -> None:
        """Null/reasons gốc giữ byte trong CSV, không impute hoặc annualize trong generator."""
        self.assertIn("CASH & 75.49 & 50.00 & NA", self.outputs["classification.tex"].decode())
        for name in ("summary.csv", "accounts.csv", "classification_by_group.csv", "per_repeat.csv"):
            self.assertEqual(self.outputs["supplement/"+name], self.bundle["analysis"][PREFIX+name])
        sensitivity = decoded(self.outputs["supplement/sensitivity.json"])
        self.assertEqual(set(sensitivity), set(self.bundle["result"]["sensitivity"]))
        self.assertEqual(len(self.outputs["supplement/leave_one_out.csv"].decode().splitlines()), 301)

    def test_domain_counts_distinguish_unrecorded_k_and_zero(self) -> None:
        """OOD fallback và K thiếu không được diễn giải thành prior trung lập hoặc K=0."""
        groups = self.bundle["facts"]["domain_support"]
        c2 = next(r for r in groups if r["method"] == "C2" and r["domain"] == "OOD5")
        self.assertEqual((c2["points"], c2["forecasts"], c2["raw_responses"], c2["bypass"]), (54, 162, 0, 162))
        native = next(r for r in groups if r["method"] == "original_fix")
        self.assertIsNone(native["effective_K_min"])
        self.assertIn("Native & CORE4 & 48 & 144 & 0 & 0 & NA & NA", self.outputs["support.tex"].decode())

    def test_null_bands_remain_na_in_tables_macros_and_figure(self) -> None:
        """Mô phỏng family suy biến; không tạo band thay thế hoặc bỏ method khỏi figure."""
        bundle = {**self.bundle, "result": deepcopy(self.bundle["result"])}
        result = bundle["result"]
        result["primary_joint_family"]["ci95"] = None
        for row in result["contrasts"]:
            row["band95_low_pp"] = row["band95_high_pp"] = None
        validate(result)
        output = render(bundle)
        self.assertIn("Bayes v1 & -0.045 & NA & NA", output["contrasts.tex"].decode())
        self.assertIn(r"\newcommand{\UnifiedVOneNativeReturnLow}{NA}", output["summary_numbers.tex"].decode())
        self.assertIn("band NA", output["return_contrasts.svg"].decode())

    def test_render_is_byte_deterministic_without_estimating_metrics(self) -> None:
        """So toàn artifact, gồm SVG/PNG, trên hai lượt render từ cùng dữ liệu."""
        with offline_guard(), patch("core.unified_analysis.analysis.analyze", side_effect=AssertionError("Cấm ước lượng lại")):
            rebuilt = render(self.bundle)
        self.assertEqual({n: binding(raw) for n, raw in self.outputs.items()}, {n: binding(raw) for n, raw in rebuilt.items()})

    def test_tex_text_and_columns_are_checked(self) -> None:
        """ID có ký tự LaTeX không được biến thành lệnh hoặc làm lệch cột."""
        self.assertEqual(escape("A_B & 20%"), r"A\_B \& 20\%")
        with self.assertRaises(ValueError):
            panel("fixture", ["a", "b"], [["one"]])

    def test_release_rejects_old_paths_and_existing_namespace_before_loading(self) -> None:
        """Không chạm release cũ hoặc paper đang có dù input mới hợp lệ."""
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("paper", "../escape", "outputs/revision/manuscript_rewrite_v1", "outputs/revision/u09_manuscript_assets_x/nested"):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    destination(root, name)
            installed = root/INSTALL
            installed.mkdir(parents=True)
            sentinel = installed/"original.tex"
            sentinel.write_bytes(b"preserve")
            with patch("core.manuscript_u09.release.load", side_effect=AssertionError("Không được đọc input")), self.assertRaises(ValueError):
                build(root)
            self.assertEqual(sentinel.read_bytes(), b"preserve")
            self.assertFalse((root/RELEASE).exists())

    def test_release_verifier_detects_source_artifact_install_and_extra_tamper(self) -> None:
        """Cold verifier không tin self-digest khi source, output hoặc bản cài khác byte."""
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for name in SOURCES:
                (root/name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT/name, root/name)
            with patch("core.manuscript_u09.release.load", return_value=self.bundle), \
                    patch("core.manuscript_u09.release.commit", return_value="fixture-commit"):
                build(root)
                manifest = decoded((root/RELEASE/"manifest.json").read_bytes())
                self.assertEqual(manifest["figure"]["input"], PREFIX+"results.json")
                self.assertEqual(manifest["figure"]["pointer"], "/contrasts")
                self.assertTrue(verify(root)["byte_identical"])
                with self.assertRaises(ValueError):
                    build(root)
                for path in (root/SOURCES[2], root/RELEASE/"artifacts/comparison.tex", root/INSTALL/"comparison.tex"):
                    original = path.read_bytes()
                    path.write_bytes(b"changed")
                    with self.subTest(path=path), self.assertRaises(ValueError):
                        verify(root)
                    path.write_bytes(original)
                extra = root/RELEASE/"extra.txt"
                extra.write_bytes(b"extra")
                with self.assertRaises(ValueError):
                    verify(root)


if __name__ == "__main__":
    unittest.main()
