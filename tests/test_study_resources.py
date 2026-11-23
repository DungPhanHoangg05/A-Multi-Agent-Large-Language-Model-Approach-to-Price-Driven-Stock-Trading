"""Kiểm cài đặt ngoại tuyến trong checkout mới và bảo toàn đầu vào cục bộ."""
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from scripts.install_study_resources import ROOT, install


class StudyResourcesTests(unittest.TestCase):
    """Dùng đúng gói phân phối để kiểm đường chạy của CLI và ứng dụng."""

    def setUp(self) -> None:
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.package = self.root / "resources/serving_inputs.zip"
        self.package.parent.mkdir()
        shutil.copyfile(ROOT / "resources/serving_inputs.zip", self.package)

    def test_resume_and_preserve_conflicting_files(self) -> None:
        self.assertGreater(install(self.root), 0)
        self.assertEqual(install(self.root), 0)
        manifest = self.root / "docs/plan/week12/serving_resources_v1.json"
        original = manifest.read_bytes()
        manifest.unlink()
        self.assertEqual(install(self.root), 1)
        self.assertEqual(manifest.read_bytes(), original)
        manifest.write_bytes(b"local")
        with self.assertRaises(ValueError):
            install(self.root)
        self.assertEqual(manifest.read_bytes(), b"local")

    def test_damaged_package_creates_no_inputs(self) -> None:
        self.package.write_bytes(b"invalid")
        with self.assertRaises(ValueError):
            install(self.root)
        self.assertFalse((self.root / "docs").exists())
        self.assertFalse((self.root / "outputs").exists())
