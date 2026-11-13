"""Kiểm khôi phục nguyên byte, hash, traversal và chống ghi đè bằng chứng."""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import hashlib
import json
import unittest

from core.revision_evidence_archive import DIRECTORY, EvidenceArchive, load_index


class EvidenceArchiveTests(unittest.TestCase):
    """Fixture nhỏ độc lập, không đọc model hoặc thay dữ liệu nghiên cứu thật."""

    def fixture(self, root: Path, name: str = "outputs/revision/sample/data.bin") -> dict:
        """Tạo tệp hai mảnh để kiểm digest đầy đủ qua ranh giới mảnh."""
        folder = root / DIRECTORY
        folder.mkdir(parents=True)
        chunks = [b"first\r\n", b"second\x00"]
        raw = b"".join(chunks)
        ids = [hashlib.sha256(chunk).hexdigest() for chunk in chunks]
        part = folder / "part-001.zip"
        with ZipFile(part, "w") as archive:
            for sha, chunk in zip(ids, chunks):
                archive.writestr("blobs/" + sha, chunk)
        index = {"schema": "revision_evidence_archive_v1", "directories": {"sample": {}},
                 "files": {name: {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "chunks": ids}},
                 "blobs": {sha: {"part": part.name, "bytes": len(chunk)} for sha, chunk in zip(ids, chunks)},
                 "parts": {part.name: {"bytes": part.stat().st_size, "sha256": hashlib.sha256(part.read_bytes()).hexdigest()}}}
        self.write_index(folder, index)
        return index

    def write_index(self, folder: Path, index: dict) -> None:
        """Ký digest fixture theo đúng canonical JSON của công cụ đọc."""
        index.pop("sha256", None)
        index["sha256"] = hashlib.sha256(json.dumps(index, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        (folder / "index.json").write_text(json.dumps(index), encoding="utf-8")

    def test_exact_chunks_and_explicit_destination_restore(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root)
            with EvidenceArchive(root) as archive:
                self.assertEqual(archive.verify(), 1)
                self.assertFalse((root / "outputs").exists())
                target = root / "separate"
                self.assertEqual(archive.restore("sample", target), 1)
                self.assertEqual((target / "outputs/revision/sample/data.bin").read_bytes(), b"first\r\nsecond\x00")

    def test_corrupt_archive_is_rejected_before_restore(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root)
            (root / DIRECTORY / "part-001.zip").write_bytes(b"tampered")
            with EvidenceArchive(root) as archive, self.assertRaises(ValueError):
                archive.restore("sample")
            self.assertFalse((root / "outputs").exists())

    def test_changed_destination_is_never_overwritten(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root)
            target = root / "outputs/revision/sample/data.bin"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"current")
            with EvidenceArchive(root) as archive, self.assertRaises(ValueError):
                archive.restore("sample")
            self.assertEqual(target.read_bytes(), b"current")

    def test_signed_traversal_path_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, "../escape.bin")
            with self.assertRaises(ValueError):
                load_index(root)

    def test_missing_release_and_changed_file_digest_are_rejected(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            index = self.fixture(root)
            name = next(iter(index["files"]))
            index["files"][name]["sha256"] = "0" * 64
            self.write_index(root / DIRECTORY, index)
            with EvidenceArchive(root) as archive:
                with self.assertRaises(ValueError):
                    archive.restore("unknown")
                with self.assertRaises(ValueError):
                    archive.restore("sample")
            self.assertFalse((root / "outputs").exists())


if __name__ == "__main__":
    unittest.main()
