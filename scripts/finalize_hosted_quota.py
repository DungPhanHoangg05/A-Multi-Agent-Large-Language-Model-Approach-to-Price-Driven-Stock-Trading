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


class DailyQuota(Waiting):
    """Dừng phiên CLI khi cửa sổ ngày chặn lượt gọi."""


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
        """Giữ transaction hiện hữu; báo riêng khi RPD hoặc TPD đang chặn reserve."""
        try:
            super().reserve(identifier, run, tokens)
        except Waiting as pending:
            now = self.clock()
            with self.connect() as db:
                requests, charged = db.execute(
                    "SELECT COUNT(*), COALESCE(SUM(COALESCE(used,reserve)),0) FROM attempts WHERE started>?",
                    (now-86400,)).fetchone()
                header = db.execute("SELECT 1 FROM headroom WHERE kind='requests' AND remaining<1 AND until>?",
                                    (now,)).fetchone()
            limits = self.limits
            if header or requests >= limits["rpd"] or charged+tokens > limits["tpd"]:
                raise DailyQuota(pending.until) from None
            raise

    def observe(self, identifier: str, headers: dict, observed_at: float) -> None:
        """Dừng khi provider hạ giới hạn đã khóa, kể cả sau khi khởi động lại."""
        for suffix, limit in (("requests", 1000), ("tokens", 8000)):
            raw = headers.get("x-ratelimit-limit-"+suffix)
            if raw is not None and (not math.isfinite(float(raw)) or float(raw) < limit):
                raise Failed("PROVIDER_LIMIT_BELOW_GRANT")
        super().observe(identifier, headers, observed_at)


def quota_for(root: Path, grant: dict, model: str, clock=time.time) -> HostedQuota:
    """Org gốc mở đúng DB cũ; org bổ sung có carry riêng cho mỗi model."""
    index = sorted(MODEL_LIMITS).index(model)
    slot = grant.get("org_slot", ORG)
    path = root/"quota" if slot == ORG else root/"quota"/f"org-{slot}"
    quota = HostedQuota(path/f"model-{index}.sqlite3", clock)
    quota.limits = MODEL_LIMITS[model]
    quota.seed(model, grant)
    return quota


def provider_daily_deadline(row: dict, ordinal: int) -> float | None:
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
    deadline = retry_until(row, ordinal)
    match = re.search(r"(?:try again in|retry after)\s+([\d.hms]+)", message, re.I)
    seconds = reset_seconds(match[1].lower().rstrip(".")) if match else None
    if "retry-after" not in headers and not requests_exhausted and seconds is None:
        deadline = max(deadline, row["completed_at"]+86400)
    elif seconds is not None:
        deadline = max(deadline, row["completed_at"]+seconds+.1)
    return deadline


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

    def attempt_metadata(self) -> dict:
        return {"org_slot": self.org_slot}

    def wait_for_retry(self, row: dict, ordinal: int, account: Quota, *, last: bool) -> None:
        deadline = provider_daily_deadline(row, ordinal)
        same_org = row.get("org_slot", ORG) == self.org_slot
        if not last or deadline is not None:
            until = deadline if deadline is not None else retry_until(row, ordinal)
            account.finish(row["id"], str(row["status"]), row.get("usage"), until)
            if last and same_org and until > self.clock():
                raise DailyQuota(until)
            return
        super().wait_for_retry(row, ordinal, account, last=last)
