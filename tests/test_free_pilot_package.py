"""Kiểm gói bàn giao: chặn traversal, thiếu/thừa file, tamper và overwrite."""

import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import zipfile

SOURCE = Path(__file__).resolve().parents[1] / "scripts/package_free_pilot.py"
SPEC = importlib.util.spec_from_file_location("package_free_pilot", SOURCE)
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)


class PilotPackageTests(unittest.TestCase):
    """Không cần dữ liệu nghiên cứu hoặc gọi API để kiểm hợp đồng archive."""

    def fixture(self, path: Path, *, raw: bytes = b"proof", extra: bool = False) -> None:
        """Khóa hash của proof gốc để phát hiện sửa nội dung."""
        manifest = {"files": {"proof.txt": {"bytes": 5, "sha256": PACKAGE.sha(b"proof")}}}
        with zipfile.ZipFile(path, "w") as bundle:
            bundle.writestr("proof.txt", raw)
            bundle.writestr(PACKAGE.MANIFEST, json.dumps(manifest))
            if extra:
                bundle.writestr("extra.txt", b"extra")

    def test_reject_unsafe_names(self) -> None:
        """Tên Windows, credential và đường dẫn vượt root đều bị chặn."""
        for name in ("../outside", "/abs", "C:/abs", "a\\b", ".env", "a/.env.prod", ".git/config", "a//b",
                     "a/NUL.txt", "a/dir.", "a/file ", ".GIT/config", "a/*", "a/file?"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                PACKAGE.safe_name(name)
        self.assertEqual(PACKAGE.safe_name("data/evidence.json"), "data/evidence.json")
        self.assertEqual(PACKAGE.safe_name("deploy/oracle/.env.example"), "deploy/oracle/.env.example")

    def test_byte_hash_and_exact_membership(self) -> None:
        """Phát hiện tamper cùng kích thước và file thừa ngoài manifest."""
        with TemporaryDirectory() as folder:
            path = Path(folder) / "proof.zip"
            self.fixture(path)
            self.assertEqual(len(PACKAGE.verify_archive(path)["files"]), 1)
            self.fixture(path, raw=b"other")
            with self.assertRaisesRegex(ValueError, "Sai hash"):
                PACKAGE.verify_archive(path)
            self.fixture(path, extra=True)
            with self.assertRaisesRegex(ValueError, "thiếu/thừa"):
                PACKAGE.verify_archive(path)

    def test_missing_duplicate_and_windows_case_collision(self) -> None:
        """Không nhận gói thiếu file hoặc đè tên khi giải nén trên Windows."""
        with TemporaryDirectory() as folder:
            path = Path(folder) / "proof.zip"
            self.fixture(path)
            with zipfile.ZipFile(path) as bundle:
                manifest = bundle.read(PACKAGE.MANIFEST)
            with zipfile.ZipFile(path, "w") as bundle:
                bundle.writestr(PACKAGE.MANIFEST, manifest)
            with self.assertRaisesRegex(ValueError, "thiếu/thừa"):
                PACKAGE.verify_archive(path)
            self.fixture(path)
            with zipfile.ZipFile(path, "a") as bundle:
                bundle.writestr("PROOF.txt", b"other")
            with self.assertRaisesRegex(ValueError, "trùng"):
                PACKAGE.verify_archive(path)

    def test_restore_never_overwrites_nonempty_folder(self) -> None:
        """Giữ nguyên file của người dùng khi chọn nhầm thư mục phục hồi."""
        with TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "proof.zip"
            self.fixture(path)
            destination = root / "existing"
            destination.mkdir()
            (destination / "keep.txt").write_text("giữ nguyên", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mới hoặc rỗng"):
                PACKAGE.restore(path, destination)
            self.assertEqual((destination / "keep.txt").read_text(encoding="utf-8"), "giữ nguyên")


if __name__ == "__main__":
    unittest.main()
