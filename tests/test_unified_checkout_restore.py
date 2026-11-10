"""Đảm bảo sửa checkout chỉ đổi newline khớp hash, không sửa nội dung hoặc đường dẫn tùy ý."""
from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.restore_unified_checkout import restore


def binding(raw: bytes) -> dict:
    """Pin byte và hash của fixture tổng hợp, không dùng receipt thị trường."""
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


class CheckoutRestoreTests(unittest.TestCase):
    """Ba hợp đồng vận hành của helper newline độc lập với các kernel nghiên cứu."""
    def test_dry_run_then_exact_restore_both_directions_and_idempotency(self) -> None:
        with TemporaryDirectory() as folder:
            root = Path(folder)
            a, b = b"first\nsecond\n", b"first\r\nsecond\r\n"
            (root / "a.py").write_bytes(b)
            (root / "b.py").write_bytes(a)
            pins = {"a.py": binding(a), "b.py": binding(b)}
            self.assertEqual(restore(root, pins)["newline_changes"], 2)
            self.assertEqual((root / "a.py").read_bytes(), b)
            self.assertEqual(restore(root, pins, write=True)["newline_changes"], 2)
            self.assertEqual((root / "a.py").read_bytes(), a)
            self.assertEqual((root / "b.py").read_bytes(), b)
            self.assertEqual(restore(root, pins, write=True)["newline_changes"], 0)

    def test_meaningful_change_rejects_every_write_before_mutation(self) -> None:
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "a.py").write_bytes(b"safe\r\n")
            (root / "b.py").write_bytes(b"changed\n")
            with self.assertRaises(ValueError):
                restore(root, {"a.py": binding(b"safe\n"), "b.py": binding(b"original\n")}, write=True)
            self.assertEqual((root / "a.py").read_bytes(), b"safe\r\n")

    def test_credentials_and_traversal_are_rejected_before_read(self) -> None:
        with TemporaryDirectory() as folder:
            for name in ("../outside.py", ".env", "secret/.env.local", "C:/outside.py", "a\\b.py"):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    restore(Path(folder), {name: binding(b"secret")}, write=True)


if __name__ == "__main__":
    unittest.main()
