"""Kiểm checkpoint/unknown/release và raw response binding mà không gọi API."""

from pathlib import Path
import tempfile
import unittest

from core.historical_evaluation_clients import require_release
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import digest


class JournalTests(unittest.TestCase):
    """Không replay complete, không tự nối unknown, không cấp quyền bằng CLI flag."""

    def test_complete_resume_and_deep_copy(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            book = RunBook(root, {"fixture": True})
            calls = []
            def invoke(identifier: str) -> dict:
                """Ghi một lượt mô phỏng để kiểm resume."""
                calls.append(identifier)
                return {"reply": {"decision": "LONG"}}
            first = book.execute("slot", {"source": "a"}, invoke)
            first["reply"]["decision"] = "SHORT"
            second = RunBook(root, {"fixture": True}, verify_only=True)
            self.assertEqual(second.uuid, book.uuid)
            self.assertEqual(second.execute("slot", {"source": "a"}, invoke)["reply"]["decision"], "LONG")
            self.assertEqual(len(calls), 1)
            with self.assertRaises(ValueError):
                second.execute("slot", {"source": "changed"}, invoke)

    def test_crash_keeps_unknown_uuid_and_requires_specific_reconcile(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            book = RunBook(Path(folder), {"fixture": True})
            calls = []
            def broken(identifier: str) -> dict:
                """Mô phỏng response không rõ sau dispatch."""
                calls.append(identifier)
                raise RuntimeError("Mất kết nối fixture")
            with self.assertRaises(RuntimeError):
                book.execute("slot", {}, broken)
            with self.assertRaises(ValueError):
                book.execute("slot", {}, broken)
            self.assertEqual(len(calls), 1)
            unknown = load(book.path("slot"))["attempts"][-1]["attempt_id"]
            with self.assertRaises(ValueError):
                book.reconcile("WRONG_UUID", "Không được replay")
            book.reconcile(unknown, "Đã đối soát raw/ledger fixture")
            book.execute("slot", {}, lambda _: {"ok": True})
            with self.assertRaises(ValueError):
                book.reconcile(unknown, "Không dùng UUID cũ")
            self.assertEqual(len(load(book.path("slot"))["attempts"]), 2)

    def test_missing_verify_does_not_create_identity(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with self.assertRaises(ValueError):
                RunBook(root, {}, verify_only=True)
            self.assertFalse((root / "identity.json").exists())

    def test_mutated_complete_output_and_identity_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            book = RunBook(Path(folder), {"fixture": True})
            book.execute("slot", {}, lambda _: {"ok": True})
            doc = load(book.path("slot"))
            doc["attempts"][-1]["output"]["ok"] = False
            save(book.path("slot"), doc)
            with self.assertRaises(ValueError):
                book.complete("slot")
            with self.assertRaises(ValueError):
                RunBook(Path(folder), {"fixture": False})

    def test_release_missing_stops_before_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "Chưa có release H06"):
                require_release(Path(folder))


if __name__ == "__main__":
    unittest.main()
