"""Hồi quy released owner khác signature trước fit; không làm yếu khóa run đã train."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

from core.mt_bicl_bank import content_hash
from core.mt_bicl_replica_io import NAMESPACE, PROTOCOL, path_for, read
from core.mt_bicl_replica_lock import previous_protocol, repair_pretraining_lock
from core.prior_run_lock import PriorRunLock, host_boot, lock_handle

ROOT = Path(__file__).resolve().parents[1]


class ReplicaLockTests(unittest.TestCase):
    """Mọi ca dùng thư mục tạm; không gọi prepare/fit hoặc optimizer."""

    def setUp(self) -> None:
        """Dựng đúng triệu chứng: owner released của source revision cũ."""
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.directory = self.root / NAMESPACE
        self.directory.mkdir(parents=True)
        (self.directory / "run.lock").write_bytes(b"0")
        self.protocol = {"version":"replica", "model":{"layers":2}, "source_sha256":{"script":"new"}}
        self.owner = {"host_id":host_boot()[0],"boot_id":host_boot()[1],"pid":99999999,
            "process_start_time":"old-time","owner_uuid":str(uuid4()),"acquired_at":"2026-11-08T03:52:09Z",
            "run_signature":"a"*64,"owner_state":"released","released_at":"2026-11-08T03:54:23Z"}
        self.owner_path = self.directory / "run.owner.json"
        self.original = (json.dumps(self.owner,ensure_ascii=False,indent=2)+"\r\n").encode()
        self.owner_path.write_bytes(self.original)

    def repair(self) -> dict:
        """Chỉ tiêm liveness và Git lookup, giữ OS lock thật trong test."""
        with patch("core.mt_bicl_replica_lock.process_start",return_value=None), \
             patch("core.mt_bicl_replica_lock.previous_protocol",return_value="commit"):
            return repair_pretraining_lock(self.root,self.protocol)

    def test_reproduce_error_then_archive_exact_bytes_and_reacquire(self) -> None:
        """Guard cũ từ chối signature mới; recovery prefit giữ byte và lock inode."""
        with self.assertRaises(ValueError):
            with PriorRunLock(self.directory,content_hash(self.protocol)):
                pass
        result = self.repair()
        self.assertEqual(result["status"],"PREFIT_OWNER_ARCHIVED")
        self.assertEqual((self.root/result["archive"]).read_bytes(),self.original)
        self.assertFalse(self.owner_path.exists())
        self.assertEqual((self.directory/"run.lock").read_bytes(),b"0")
        receipt = read(path_for(self.root,f"lock_history/{self.owner['owner_uuid']}.migration.json"))
        self.assertEqual(receipt["owner_byte_sha256"],hashlib.sha256(self.original).hexdigest())
        with PriorRunLock(self.directory,content_hash(self.protocol)):
            pass
        current = json.loads(self.owner_path.read_bytes())
        self.assertEqual(current["run_signature"],content_hash(self.protocol))
        self.assertEqual(current["owner_state"],"released")

    def test_busy_os_lock_does_not_modify_owner(self) -> None:
        """Không lấy metadata released làm lý do phá một handle đang sống."""
        with (self.directory/"run.lock").open("r+b") as handle:
            lock_handle(handle)
            with self.assertRaises(RuntimeError):
                self.repair()
        self.assertEqual(self.owner_path.read_bytes(),self.original)
        self.assertFalse((self.directory/"lock_history").exists())

    def test_live_owner_other_host_active_and_unknown_liveness_stop(self) -> None:
        """Không archive owner chưa xác minh đầy đủ dù OS lock đang rảnh."""
        for delta in ({"host_id":"other-host"},{"owner_state":"active","released_at":None},
                      {"owner_uuid":None},{"released_at":None}):
            raw=json.dumps({**self.owner,**delta}).encode()
            self.owner_path.write_bytes(raw)
            with self.assertRaises((ValueError,TypeError,AttributeError)):
                self.repair()
            self.assertEqual(self.owner_path.read_bytes(),raw)
        self.owner_path.write_bytes(self.original)
        with patch("core.mt_bicl_replica_lock.process_start",return_value=self.owner["process_start_time"]):
            with self.assertRaises(RuntimeError):repair_pretraining_lock(self.root,self.protocol)
        with patch("core.mt_bicl_replica_lock.process_start",side_effect=RuntimeError("Không xác minh")):
            with self.assertRaises(RuntimeError):repair_pretraining_lock(self.root,self.protocol)
        self.assertEqual(self.owner_path.read_bytes(),self.original)

    def test_any_fit_train_output_or_directory_blocks_rebind(self) -> None:
        """Teacher/corpus/prepared/pilot/checkpoint không được mất identity hoặc reseal."""
        for name in ("teacher","corpora","pilot","training","model","prepared.json","inputs/context.json"):
            path=self.directory/name
            if "." in path.name:
                path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b"evidence")
            else:
                path.mkdir()
            with self.assertRaises(ValueError):self.repair()
            self.assertEqual(self.owner_path.read_bytes(),self.original)
            if path.is_dir():path.rmdir()
            else:path.unlink()

    def test_unrecognized_protocol_signature_preserves_owner(self) -> None:
        """Không tự gán signature mới khi không có Git provenance của owner cũ."""
        with patch("core.mt_bicl_replica_lock.process_start",return_value=None), \
             patch("core.mt_bicl_replica_lock.previous_protocol",side_effect=ValueError("Unknown")):
            with self.assertRaises(ValueError):repair_pretraining_lock(self.root,self.protocol)
        self.assertEqual(self.owner_path.read_bytes(),self.original)

    def test_pending_migration_receipt_can_resume_without_resealing(self) -> None:
        """Crash trước rename không buộc xóa receipt hoặc sửa timestamp cũ."""
        original_rename=Path.rename
        def fail_owner(path:Path,target:Path) -> Path:
            if path == self.owner_path:raise OSError("Fixture crash trước rename")
            return original_rename(path,target)
        with patch.object(Path,"rename",fail_owner):
            with self.assertRaises(OSError):self.repair()
        receipt=path_for(self.root,f"lock_history/{self.owner['owner_uuid']}.migration.json")
        before=receipt.read_bytes()
        self.assertEqual(self.repair()["status"],"PREFIT_OWNER_ARCHIVED")
        self.assertEqual(receipt.read_bytes(),before)

    def test_git_lookup_accepts_only_source_delta(self) -> None:
        """Đúng signature lỗi thực tế có trong Git; đổi dữ liệu/recipe phải revision riêng."""
        current=json.loads((ROOT/PROTOCOL).read_bytes())
        old=json.loads(subprocess.check_output(["git","show","66691b6a:"+PROTOCOL.as_posix()],cwd=ROOT))
        self.assertTrue(previous_protocol(ROOT,content_hash(old),current))
        changed=deepcopy(current);changed["training"]["model_seeds"]=[42]
        with self.assertRaises(ValueError):previous_protocol(ROOT,content_hash(old),changed)
        with self.assertRaises(ValueError):previous_protocol(ROOT,"0"*64,current)


if __name__ == "__main__":
    unittest.main()
