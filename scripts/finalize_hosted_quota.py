"""Quota theo từng org/model và phân loại giới hạn ngày của FIN11."""
from __future__ import annotations

from datetime import datetime
import json
import math
from pathlib import Path
import re
import time
from typing import Any, Callable

from core.finalize_budget_quota import ATTEMPT_CAP, ORG
from core.groq_pacing import MODEL_LIMITS, reset_seconds
from core.serving_runtime.quota import Failed, Quota, Waiting
from core.serving_runtime.transport import Calls, retry_until
from core.unified_contracts import digest
from scripts.finalize_hosted_response import HostedHTTP, capture_path, recover_response


class DailyQuota(BaseException):
    """Dừng phiên CLI khi Groq báo hết quota ngày."""

    def __init__(self, until: float | None) -> None:
        self.until = until


class HostedQuota(Quota):
    """Cùng DB qua smoke/research của một org và một model."""

    def seed(self, model: str, grant: dict) -> None:
        """Giữ nguyên carry đã khóa khi mở lại DB."""
        limits = MODEL_LIMITS[model]
        observed = datetime.fromisoformat(grant["local_quota"]["observed_at_utc"]).timestamp()
        remaining = grant["balance"]["remaining_tokens_24h"]
        local = grant["local_quota"]["models"][model]
        available = local["local_estimated_day_tokens_remaining"]
        if remaining is not None:
            available = min(available, remaining[model])
        tokens = limits["tpd"]-available
        requests = limits["rpd"]-local["local_estimated_day_requests_remaining"]
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            marker = db.execute("SELECT value FROM metadata WHERE name='fin11_grant'").fetchone()
            signature = digest(grant)
            if marker is not None:
                if marker[0] != signature:
                    raise ValueError("Quota khác grant, không đặt lại carry")
                return
            if db.execute("SELECT 1 FROM attempts LIMIT 1").fetchone() is not None:
                raise ValueError("Quota đã có attempt nhưng thiếu identity của carry")
            count = max(int(tokens > 0), requests)
            db.executemany("INSERT INTO attempts(id,run,started,reserve,used,state,observed) VALUES (?,?,?,0,?,'CARRY',1)",
                           [(f"carry-{i}", "FIN11_CARRY", observed, tokens if i == 0 else 0) for i in range(count)])
            db.execute("INSERT INTO metadata VALUES ('fin11_grant',?)", (signature,))

    def reserve(self, identifier: str, run: str, tokens: int) -> None:
        """Giữ pacing phút và chỉ chặn theo ngày khi có thời hạn từ Groq."""
        if type(tokens) is not int or not 0 < tokens <= self.limits["tpm"]:
            raise Failed("TOKEN_ADMISSION_FAILED")
        now = self.clock()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            headroom = db.execute("SELECT kind,remaining,until FROM headroom WHERE until>?", (now,)).fetchall()
            daily_waits = [until for kind, remaining, until in headroom
                           if kind in ("provider_requests", "daily_retry") and remaining < 1]
            if daily_waits:
                raise DailyQuota(max(daily_waits))
            waits = [until for kind, remaining, until in headroom
                     if kind in ("tokens", "retry") and (tokens if kind == "tokens" else 1) > remaining]
            count, charged, earliest = db.execute(
                "SELECT COUNT(*), COALESCE(SUM(reserve),0), MIN(started) FROM attempts "
                "WHERE state!='CARRY' AND started>?", (now-61,)).fetchone()
            if count >= self.limits["rpm"] or charged+tokens > self.limits["tpm"]:
                waits.append(earliest+61.1)
            if waits:
                raise Waiting(max(waits))
            db.execute("INSERT INTO attempts(id,run,started,reserve,state) VALUES (?,?,?,?,'UNKNOWN')",
                       (identifier, run, now, tokens))
            db.execute("UPDATE headroom SET remaining=remaining-CASE kind WHEN 'tokens' THEN ? ELSE 1 END "
                       "WHERE kind IN ('tokens','provider_requests') AND until>?", (tokens, now))

    def observe(self, identifier: str, headers: dict, observed_at: float) -> None:
        """Chỉ ghi cửa sổ RPD khi header của Groq có thời gian reset."""
        for suffix, limit in (("requests", 1000), ("tokens", 8000)):
            raw = headers.get("x-ratelimit-limit-"+suffix)
            if raw is not None and (not math.isfinite(float(raw)) or float(raw) < limit):
                raise Failed("PROVIDER_LIMIT_BELOW_GRANT")
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            marker = db.execute("SELECT observed FROM attempts WHERE id=?", (identifier,)).fetchone()
            if marker is None:
                raise ValueError("Header không có intent quota")
            if marker[0]:
                return
            for kind in ("tokens", "requests"):
                value = headers.get("x-ratelimit-remaining-"+kind)
                if value is None:
                    continue
                remaining = float(value)
                if not math.isfinite(remaining) or remaining < 0:
                    raise ValueError("Header quota không hữu hạn hoặc âm")
                seconds = reset_seconds(headers.get("x-ratelimit-reset-"+kind, ""))
                if seconds is None and kind == "requests":
                    continue
                # Khóa riêng các số dư RPD đi kèm reset thực, vì sổ cũ từng tự cộng 24 giờ.
                name = "provider_requests" if kind == "requests" else kind
                until = observed_at+(61. if seconds is None else seconds)+.1
                previous = db.execute("SELECT remaining,until FROM headroom WHERE kind=?", (name,)).fetchone()
                if previous and previous[1] > self.clock():
                    remaining, until = min(remaining, previous[0]), max(until, previous[1])
                db.execute("INSERT OR REPLACE INTO headroom VALUES (?,?,?)", (name, remaining, until))
            db.execute("UPDATE attempts SET observed=1 WHERE id=?", (identifier,))

    def record_retry(self, row: dict, until: float | None, *, daily: bool) -> bool:
        """Lưu lần Groq từ chối và thời hạn thực để dùng khi nối lại qua org."""
        identifier, status = row["id"], str(row["status"])
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            previous = db.execute("SELECT state FROM attempts WHERE id=?", (identifier,)).fetchone()
            if previous is None:
                raise ValueError("HTTP chưa được reserve quota durable")
            db.execute("UPDATE attempts SET used=?,retry_until=?,state=? WHERE id=?",
                       (row.get("usage"), until or 0, status, identifier))
            if until is not None and until > self.clock():
                db.execute("INSERT INTO headroom VALUES (?,0,?) ON CONFLICT(kind) DO UPDATE SET until=MAX(until,excluded.until)",
                           ("daily_retry" if daily else "retry", until))
        return previous[0] != status


def quota_for(root: Path, grant: dict, model: str, clock=time.time) -> HostedQuota:
    """Org gốc mở đúng DB cũ; org bổ sung có carry riêng cho mỗi model."""
    index = sorted(MODEL_LIMITS).index(model)
    slot = grant.get("org_slot", ORG)
    path = root/"quota" if slot == ORG else root/"quota"/f"org-{slot}"
    quota = HostedQuota(path/f"model-{index}.sqlite3", clock)
    quota.limits = MODEL_LIMITS[model]
    quota.seed(model, grant)
    return quota


def retry_row(row: dict) -> dict:
    """Bỏ header RPD thiếu reset khi tính backoff chung để tránh mốc giả 24 giờ."""
    headers = row["headers"]
    if reset_seconds(headers.get("x-ratelimit-reset-requests", "")) is not None:
        return row
    return {**row, "headers": {key: value for key, value in headers.items()
                               if key != "x-ratelimit-remaining-requests"}}


def provider_daily_limit(row: dict, ordinal: int) -> DailyQuota | None:
    """Nhận TPD/RPD từ raw 429 đã lưu, kể cả thời lượng Groq ghi trong thông báo."""
    if row["status"] != 429:
        return None
    try:
        error = json.loads(row["response"]).get("error", {})
        message = f"{error.get('message', '')} {error.get('code', '')}"
    except (ValueError, AttributeError):
        message = ""
    headers = row["headers"]
    requests_exhausted = headers.get("x-ratelimit-remaining-requests") == "0"
    if not requests_exhausted and not re.search(r"\b(?:TPD|RPD)\b|per[ _-]+day|daily[ _-]+(?:quota|limit)", message, re.I):
        return None
    match = re.search(r"(?:try again in|retry after)\s+([\d.hms]+)", message, re.I)
    seconds = reset_seconds(match[1].lower().rstrip(".")) if match else None
    normalized = retry_row(row)
    if seconds is None and "retry-after" not in headers and not (
            requests_exhausted and "x-ratelimit-remaining-requests" in normalized["headers"]):
        return DailyQuota(None)
    deadline = retry_until(normalized, ordinal)
    if seconds is not None:
        deadline = max(deadline, row["completed_at"]+seconds+.1)
    return DailyQuota(deadline)


class HostedWire(Calls):
    """Một credential cho HTTP mới, sổ quota theo org nguồn khi replay."""

    def __init__(self, *args, org_slot: int, quota_at: Callable[[int], HostedQuota], guard: Callable[[], None],
                 archived_attempts: dict[str, int] | None = None, **kwargs) -> None:
        self.org_slot, self.quota_at = org_slot, quota_at
        self.archived_attempts = archived_attempts or {}
        self.dispatch_slot: str | None = None

        def check_attempt_cap() -> None:
            guard()
            slot = self.dispatch_slot
            if slot in self.archived_attempts and len(self._rows(slot)[1])+self.archived_attempts[slot] >= ATTEMPT_CAP:
                raise Failed("ATTEMPT_CAP_EXHAUSTED")

        super().__init__(*args, quota=quota_at(org_slot), guard=check_attempt_cap, **kwargs)

    def call(self, slot: str, body: dict, attempt: str) -> tuple[Any, dict]:
        """Giữ cap theo slot qua cả lần cũ đã tách và lần chạy lại."""
        previous = self.dispatch_slot
        self.dispatch_slot = slot
        try:
            return super().call(slot, body, attempt)
        finally:
            self.dispatch_slot = previous

    def account(self, row: dict) -> HostedQuota:
        return self.quota_at(row.get("org_slot", ORG))

    def dispatch(self, row: dict, body: dict) -> tuple[int, bytes, dict]:
        if isinstance(self.sender, HostedHTTP):
            return self.sender.send_durable(self.directory, row, body, self.clock)
        return super().dispatch(row, body)

    def recover_response(self, row: dict) -> dict | None:
        return recover_response(self.directory, row)

    def response_committed(self, row: dict) -> None:
        try:
            capture_path(self.directory, row).unlink(missing_ok=True)
        except OSError:
            # Wire chính đã lưu xong; nếu file tạm bị khóa thì vẫn giữ được raw.
            pass

    def attempt_metadata(self) -> dict:
        return {"org_slot": self.org_slot}

    def wait_for_retry(self, row: dict, ordinal: int, account: HostedQuota, *, last: bool) -> None:
        daily = provider_daily_limit(row, ordinal)
        until = daily.until if daily is not None else retry_until(retry_row(row), ordinal)
        first_seen = account.record_retry(row, until, daily=daily is not None)
        if last and row.get("org_slot", ORG) == self.org_slot:
            if daily is not None and (first_seen if until is None else until > self.clock()):
                raise daily
            if until is not None and until > self.clock():
                raise Waiting(until)
