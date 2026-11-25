"""Quota conservative chung mọi job/model/key; credential chỉ được giữ trong bộ nhớ."""
from __future__ import annotations

import hashlib
import hmac
from pathlib import Path
import secrets
import sqlite3
import time
import math
from contextlib import contextmanager
from typing import Iterator
from uuid import uuid4

LIMITS = {"rpm": 30, "rpd": 1000, "tpm": 8000, "tpd": 200000}
HEADER_WINDOWS = (("tokens", 61.), ("requests", 86400.))


class Waiting(BaseException):
    """Nhường worker tới hạn retry/quota, không cho agent đổi thành fallback."""
    def __init__(self, until: float) -> None:
        self.until = until


class Unknown(BaseException):
    """Provider có thể đã nhận request; phải đối soát UUID, không retry tự động."""


class Failed(BaseException):
    """Lỗi kỹ thuật kết thúc slot, giữ phần đã complete và raw evidence riêng."""


class Stopped(BaseException):
    """Dừng ở ranh giới an toàn, không xóa checkpoint."""


class Quota:
    """SQLite transaction cấp reserve trước dispatch, không nhân quota theo worker/key/model."""

    def __init__(self, path: Path, clock=time.time, *, limits: dict[str, int] | None = LIMITS) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path, self.clock = path, clock
        self.limits = None if limits is None else dict(limits)
        with self.connect() as db:
            db.executescript("CREATE TABLE IF NOT EXISTS metadata (name TEXT PRIMARY KEY,value TEXT NOT NULL);"
                "CREATE TABLE IF NOT EXISTS credentials (fingerprint TEXT PRIMARY KEY,scope TEXT NOT NULL);"
                "CREATE TABLE IF NOT EXISTS attempts (id TEXT PRIMARY KEY,run TEXT NOT NULL,started REAL NOT NULL,"
                "reserve INTEGER NOT NULL,used INTEGER,retry_until REAL NOT NULL DEFAULT 0,state TEXT NOT NULL,observed INTEGER NOT NULL DEFAULT 0);"
                "CREATE TABLE IF NOT EXISTS headroom (kind TEXT PRIMARY KEY,remaining REAL NOT NULL,until REAL NOT NULL);")
            if 'observed' not in {row[1] for row in db.execute('PRAGMA table_info(attempts)')}:
                db.execute('ALTER TABLE attempts ADD COLUMN observed INTEGER NOT NULL DEFAULT 0')
            db.execute("INSERT OR IGNORE INTO metadata VALUES ('secret',?)", (secrets.token_hex(32),))

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """Khóa transaction dùng được giữa thread/process, timeout hữu hạn."""
        db = sqlite3.connect(self.path, timeout=10)
        try:
            with db:
                yield db
        finally:
            db.close()

    def secret(self) -> str:
        """Secret ký owner cookie nằm trong runtime private, không chứa API key."""
        with self.connect() as db:
            return db.execute("SELECT value FROM metadata WHERE name='secret'").fetchone()[0]

    def credential_scope(self, key: str) -> str:
        """Fingerprint HMAC ở server riêng; browser chỉ thấy digest UUID opaque."""
        if type(key) is not str or not key.strip():
            raise ValueError("Thiếu API key serving")
        fingerprint = hmac.new(bytes.fromhex(self.secret()), key.encode(), hashlib.sha256).hexdigest()
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO credentials VALUES (?,?)", (fingerprint, str(uuid4())))
            scope = db.execute("SELECT scope FROM credentials WHERE fingerprint=?", (fingerprint,)).fetchone()[0]
        return hashlib.sha256(scope.encode()).hexdigest()

    def reserve(self, identifier: str, run: str, tokens: int) -> None:
        """UNKNOWN giữ toàn reserve; response có usage zero vẫn giữ đúng số zero cho quota ngày."""
        limits = self.limits
        if type(tokens) is not int or tokens <= 0 or (limits is not None and tokens > limits["tpm"]):
            raise Failed("TOKEN_ADMISSION_FAILED")
        now = self.clock()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            rows = db.execute("SELECT started,reserve,used,retry_until FROM attempts WHERE started>?", (now-86400,)).fetchall()
            waits = [row[3] for row in rows if row[3] > now]
            for kind, remaining, until in db.execute("SELECT kind,remaining,until FROM headroom WHERE until>?", (now,)):
                if (tokens if kind == "tokens" else 1) > remaining:
                    waits.append(until)
            windows = () if limits is None else ((61, limits["rpm"], limits["tpm"]), (86400, limits["rpd"], limits["tpd"]))
            for span, rpm, tpm in windows:
                selected = [row for row in rows if row[0] > now-span]
                charged = sum(row[1] if span == 61 or row[2] is None else row[2] for row in selected)
                if selected and (len(selected) >= rpm or charged + tokens > tpm):
                    waits.append(min(row[0] for row in selected) + span + .1)
            if waits:
                raise Waiting(max(waits))
            db.execute("INSERT INTO attempts(id,run,started,reserve,state) VALUES (?,?,?,?,?)", (identifier, run, now, tokens, "UNKNOWN"))
            db.execute("UPDATE headroom SET remaining=remaining-CASE kind WHEN 'tokens' THEN ? ELSE 1 END WHERE until>?", (tokens, now))

    def observe(self, identifier: str, headers: dict, observed_at: float) -> None:
        """Header còn quota thấp hơn reserve chặn dispatch tiếp; replay raw không cộng headroom lại."""
        from core.groq_pacing import reset_seconds
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            marker = db.execute("SELECT observed FROM attempts WHERE id=?", (identifier,)).fetchone()
            if marker is None:
                raise ValueError("Header không có intent quota")
            if marker[0]:
                return
            for kind, span in HEADER_WINDOWS:
                value = headers.get("x-ratelimit-remaining-"+kind)
                if value is None:
                    continue
                remaining = float(value)
                if not math.isfinite(remaining) or remaining < 0:
                    raise ValueError("Header quota không hữu hạn hoặc âm")
                seconds = reset_seconds(headers.get("x-ratelimit-reset-"+kind,""))
                until = observed_at+(seconds if seconds is not None else span)+.1
                previous = db.execute("SELECT remaining,until FROM headroom WHERE kind=?",(kind,)).fetchone()
                if previous and previous[1] > self.clock():
                    remaining,until = min(remaining,previous[0]),max(until,previous[1])
                db.execute("INSERT OR REPLACE INTO headroom VALUES (?,?,?)",(kind,remaining,until))
            db.execute("UPDATE attempts SET observed=1 WHERE id=?",(identifier,))

    def repair_millisecond_deadline(self, run: str, row: dict) -> list[str]:
        """Sửa mốc fallback cũ khi raw HTTP cuối xác nhận đơn vị ms và quota còn."""
        from core.groq_pacing import reset_seconds

        if self.limits is not None or row["status"] != 200:
            return []
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            latest = db.execute("SELECT id,run,state,observed FROM attempts ORDER BY started DESC LIMIT 1").fetchone()
            if latest != (row["id"], run, "200", 1):
                return []
            corrected = []
            observed_at = row["completed_at"]
            headers = row["headers"]
            for kind, fallback in HEADER_WINDOWS:
                reset = headers.get("x-ratelimit-reset-" + kind, "")
                seconds = reset_seconds(reset)
                remaining = float(headers.get("x-ratelimit-remaining-" + kind, 0))
                if (not reset.endswith("ms") or seconds is None or seconds >= fallback
                        or not math.isfinite(remaining) or remaining <= 0):
                    continue
                current = db.execute("SELECT until FROM headroom WHERE kind=?", (kind,)).fetchone()
                old_deadline = observed_at + fallback + .1
                if current is not None and math.isclose(current[0], old_deadline, rel_tol=0, abs_tol=1e-5):
                    db.execute("UPDATE headroom SET until=? WHERE kind=?", (observed_at + seconds + .1, kind))
                    corrected.append(kind)
            return corrected

    def finish(self, identifier: str, status: str, usage: int | None, retry_until: float = 0) -> None:
        """Chỉ cập nhật request đã reserve; không xóa request retry hoặc UNKNOWN khỏi chi phí."""
        with self.connect() as db:
            changed = db.execute("UPDATE attempts SET used=?,retry_until=?,state=? WHERE id=?", (usage, retry_until, status, identifier)).rowcount
            if changed != 1:
                raise ValueError("HTTP chưa được reserve quota durable")

    def attempts(self, run: str) -> int:
        """Đếm cả failed/retry/UNKNOWN, độc lập số Decision slot."""
        with self.connect() as db:
            return int(db.execute("SELECT count(*) FROM attempts WHERE run=?", (run,)).fetchone()[0])
