"""Kho checkpoint private theo UUID/owner; không đặt key vào JSON hoặc source control."""
from __future__ import annotations

from pathlib import Path
from contextlib import closing
import threading
import sqlite3
from uuid import UUID

from core.historical_evaluation_journal import load, save
from core.serving_contracts import ServingJob
from core.unified_contracts import digest, json_bytes


class Store:
    """Control và status riêng, tránh worker ghi đè yêu cầu dừng từ HTTP thread."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve() / "outputs/serving_inference/v1"
        if not self.root.resolve().is_relative_to(root.resolve()):
            raise ValueError("Namespace private serving thoát workspace")
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root/".gitignore").write_text("*\n", encoding="utf-8")
        self.mutex = threading.RLock()
        with closing(sqlite3.connect(self.root/"controls.sqlite3")) as db, db:
            db.execute("CREATE TABLE IF NOT EXISTS controls (id TEXT PRIMARY KEY,stop INTEGER NOT NULL,generation INTEGER NOT NULL)")

    def path(self, run_id: str) -> Path:
        """Không nhận ID chứa đường dẫn hoặc symlink thoát namespace."""
        if type(run_id) is not str or str(UUID(run_id)) != run_id:
            raise ValueError("Run ID không hợp lệ")
        path = self.root / run_id
        if not path.resolve().is_relative_to(self.root) or path.is_symlink():
            raise ValueError("Run ID thoát namespace")
        return path

    def create(self, job: ServingJob, points: list[dict], source: dict) -> None:
        """Ghi reservation trước worker; identity/config/request không chứa credential."""
        doc = job.document()
        path = self.path(doc["run_id"])
        with self.mutex:
            if path.exists():
                raise ValueError("Không ghi đè UUID job đã tồn tại")
            path.mkdir()
            save(path/"reservation.json", {"job": doc, "points": points, "source": source})
            from core.unified_execution import StageBook
            StageBook(path/"journal", doc)
            with closing(sqlite3.connect(self.root/"controls.sqlite3")) as db, db:
                db.execute("INSERT INTO controls VALUES (?,0,0)", (doc["run_id"],))
            save(path/"status.json", {"state": "queued", "error": None, "retry_at": None})

    def reservation(self, run_id: str, owner: str) -> dict:
        """Owner không lấy từ query; sai owner không tiết lộ nội dung job."""
        doc = load(self.path(run_id)/"reservation.json")
        job = doc["job"]
        if job["owner_scope_sha256"] != owner:
            raise PermissionError("Không có job thuộc owner này")
        if job["identity_sha256"] != digest(job["identity"]) or job["config_sha256"] != digest(job["identity"]["config"]):
            raise ValueError("Job identity sai checksum")
        return doc

    def job(self, reservation: dict) -> ServingJob:
        """Phục hồi UUID cũ, không tạo identity hoặc cache key mới khi resume."""
        return ServingJob(json_bytes(reservation["job"]))

    def control(self, run_id: str, stop: bool | None = None, *, expected_generation: int | None = None) -> dict:
        """Đọc/ghi stop riêng dưới mutex; không sửa slot đã hoàn tất."""
        self.path(run_id)
        with closing(sqlite3.connect(self.root/"controls.sqlite3", timeout=10)) as db, db:
            if stop is not None:
                sql = "UPDATE controls SET stop=?,generation=generation+1 WHERE id=?"
                args = (int(stop), run_id)
                if expected_generation is not None:
                    sql += " AND generation=?"
                    args += (expected_generation,)
                db.execute(sql, args)
            row = db.execute("SELECT stop,generation FROM controls WHERE id=?", (run_id,)).fetchone()
            if row is None:
                raise ValueError("Thiếu control của job")
            return {"stop_requested": bool(row[0]), "generation": int(row[1])}

    def status(self, run_id: str, state: str | None = None, error: dict | None = None, retry_at: float | None = None) -> dict:
        """Trạng thái lỗi dùng mã/thông báo an toàn, không serialize exception SDK."""
        with self.mutex:
            path = self.path(run_id)/"status.json"
            if state is not None:
                save(path, {"state": state, "error": error, "retry_at": retry_at})
            return load(path)
