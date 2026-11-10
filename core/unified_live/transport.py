"""Transport U08 có grant và org cố định; tái dùng owner retry/raw đã nghiệm thu U07."""
from __future__ import annotations

from contextvars import ContextVar
from copy import deepcopy
import hashlib
import hmac
import json
from pathlib import Path
import time
from typing import Any, Callable

from core.historical_evaluation_journal import load
from core.unified_contracts import digest, json_bytes
from core.unified_execution_transport import DurableCalls, MockHTTP, wire_state, Exhausted
from core.unified_live.release import require_release, PREFLIGHT, anchored, NAMESPACES

ORG: ContextVar[int | None] = ContextVar("unified_live_org", default=None)
URL = "https://api.groq.com/openai/v1/chat/completions"


class LiveHTTP:
    """Một kết nối mỗi org; không SDK retry, redirect, proxy môi trường hoặc chuyển key."""
    def __init__(self, root: Path, phase: str, guard: Callable[[], None]) -> None:
        import httpx
        from dotenv import dotenv_values
        require_release(root, phase)
        preflight = anchored(root, PREFLIGHT)
        values = dotenv_values(root / ".env")
        clients = {}
        try:
            for org in range(1, 6):
                key = values.get(f"GROQ_ORG_{org}_API_KEY")
                if not key:
                    raise ValueError("Thiếu credential U08 đã khóa")
                actual = hmac.new(key.encode(), b"unified-u06-metadata-v2", hashlib.sha256).hexdigest()
                expected = preflight["metadata"]["rows"][org - 1]["credential_hmac"]
                if not hmac.compare_digest(actual, expected):
                    raise ValueError("Credential khác slot/catalog U08; không hotswap")
                clients[org] = httpx.Client(headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                    transport=httpx.HTTPTransport(retries=0, limits=httpx.Limits(max_keepalive_connections=0)),
                    timeout=httpx.Timeout(120., connect=15., write=60., pool=15.), follow_redirects=False, trust_env=False)
        except BaseException:
            for client in clients.values():
                client.close()
            raise
        self.clients, self.guard = clients, guard
        self.request_id: str | None = None
        self.response_id: str | None = None
        self.response_meta: dict[str, Any] = {}

    def send(self, body: dict[str, Any]) -> tuple[int, bytes, dict[str, str]]:
        """Chỉ endpoint Groq cố định; raw header credential không đi vào journal hoặc log."""
        self.guard()
        org = ORG.get()
        if org not in self.clients:
            raise ValueError("HTTP thiếu shard được điều phối")
        intent = self.intent()
        if intent["id"] != self.request_id or intent["org"] != org or intent["status"] != "UNKNOWN" or intent["body"] != body:
            raise ValueError("HTTP không có đúng intent durable")
        self.response_id, self.response_meta = None, {}
        response = self.clients[org].post(URL, content=json_bytes(body))
        response.read()
        headers = dict(response.headers)
        provider_org = headers.get("x-groq-organization-id")
        self.response_id = self.request_id
        self.response_meta = {"provider_org_sha256": hashlib.sha256(provider_org.encode()).hexdigest() if provider_org else None,
                              "observed_server_date": headers.get("date")}
        return response.status_code, response.content, headers

    def close(self) -> None:
        """Đóng kết nối chính mình, không tác động client của hệ legacy."""
        for client in self.clients.values():
            client.close()


class LiveCalls(DurableCalls):
    """Giữ call/ready U07; identity hosted riêng, carry smoke và kiểm source trước gửi."""
    def __init__(self, directory: Path, identity: dict[str, Any], sender: Any,
                 history: dict[int, list[dict]], clock: Callable[[], float] = time.time,
                 guard: Callable[[], None] = lambda: None, *, test_mode: bool = False,
                 hook: Callable[[str], None] = lambda _: None) -> None:
        if (identity.get("mode") != ("HOSTED_TEST" if test_mode else "HOSTED")
                or (type(sender) is not MockHTTP if test_mode else type(sender) is not LiveHTTP)
                or set(history) != set(range(1, 6))):
            raise ValueError("Transport test/live không khớp identity hoặc năm org")
        self.directory, self.signature, self.epoch = directory, digest(identity), identity["epoch"]
        self.attempt_cap_total = identity.get("attempt_cap_total", 30 if identity["phase"] == "SMOKE" else 7956)
        self.sender, self.clock, self.guard, self.hook = sender, clock, guard, hook
        carry = []
        for org, rows in history.items():
            seen = {}
            for row in rows:
                if row["id"] in seen and seen[row["id"]] != row:
                    raise ValueError("Carry trùng UUID khác nội dung")
                seen[row["id"]] = row
            carry.extend({**deepcopy(row), "org": org} for row in seen.values())
        self.identity = {"signature": self.signature, "epoch": self.epoch,
                         "history_sha256": digest(carry), "mode": identity["mode"]}
        self.state = wire_state(directory) if (directory / "wire.json").exists() else {"identity": self.identity, "carry": carry, "rows": []}
        if self.state["identity"] != self.identity or self.state["carry"] != carry:
            raise ValueError("Resume đổi grant/epoch/carry hoặc đưa smoke vào repeat")
        self.bindings = [{"id": r["id"], "sha256": digest(r)} for r in self.state["rows"]]
        self.fingerprint = self._fingerprint()
        if type(sender) is LiveHTTP:
            sender.intent = lambda: self.state["rows"][-1]

    def ready(self, org: int, tokens: int) -> None:
        """Trần phase cộng dồn mọi retry/repair/UNKNOWN, không phụ thuộc lần mở tiến trình."""
        if len(self.state["rows"]) >= self.attempt_cap_total:
            raise Exhausted("Hết trần HTTP của phase U08")
        super().ready(org, tokens)

    def _fingerprint(self) -> tuple[int, int] | None:
        """Không đọc lại toàn raw HTTP khi chính owner đã fsync index hiện hành."""
        path = self.directory / "wire.json"
        if not path.exists():
            return None
        stat = path.stat()
        return stat.st_mtime_ns, stat.st_size

    def refresh(self) -> None:
        """Chỉ dùng cache trong OS lock; thay owner/index thì kiểm hash toàn bộ lại."""
        if self._fingerprint() != self.fingerprint:
            super().refresh()
            self.fingerprint = self._fingerprint()

    def persist(self) -> None:
        """Gắn org/epoch và metadata provider vào raw trước hash, không ghi key."""
        if self.state["rows"]:
            row = self.state["rows"][-1]
            if type(self.sender) is LiveHTTP:
                if row["status"] == "UNKNOWN":
                    self.sender.request_id = row["id"]
                elif row["id"] == self.sender.response_id:
                    row.update(self.sender.response_meta)
        super().persist()
        self.fingerprint = self._fingerprint()

    def call(self, slot: str, org: int, body: dict[str, Any], attempt: str) -> tuple[Any, dict[str, Any]]:
        """Mọi raw/retry/repair vẫn qua _invoke_with_retry và trần ba bền vững U07."""
        self.guard()
        vision = slot.startswith("graph/") and slot.split("/")[-1] in ("pattern", "trend")
        if not vision and not slot.startswith("forecast/"):
            raise ValueError("HTTP ngoài node vision/Decision đã khóa")
        options = {k: v for k, v in body.items() if k not in ("messages", "response_format")}
        expected = {"model": "qwen/qwen3.8-27b" if vision else "openai/gpt-oss-20b", "stream": False, "n": 1,
            "temperature": 1e-8, "stop": None, "reasoning_format": "hidden", "reasoning_effort": "none" if vision else "low",
            "service_tier": "on_demand", "max_tokens": 960}
        if json_bytes(options) != json_bytes(expected) or (vision == ("response_format" in body)):
            raise ValueError("HTTP đổi model/options/schema ngoài release")
        token = ORG.set(org)
        try:
            reply, row = super().call(slot, org, body, attempt)
            if type(self.sender) is LiveHTTP:
                from email.utils import parsedate_to_datetime
                headers = row["headers"]
                required = ("x-ratelimit-limit-requests", "x-ratelimit-limit-tokens",
                            "x-ratelimit-remaining-requests", "x-ratelimit-remaining-tokens")
                if any(key not in headers for key in required) or not row.get("observed_server_date"):
                    raise Exhausted("Thiếu quota header/date thực, chưa mở forecast hoặc lượt tiếp theo")
                observed = parsedate_to_datetime(row["observed_server_date"]).timestamp()
                if abs(observed - row["completed_at"]) > 180:
                    raise Exhausted("Clock không khớp server, không giả định expiry carry")
                if float(headers["x-ratelimit-limit-requests"]) < 1000 or float(headers["x-ratelimit-limit-tokens"]) < 8000:
                    raise Exhausted("Provider giảm hạn mức, giữ raw để đối soát")
            hashes = {}
            for value in self.state["carry"] + self.state["rows"]:
                observed = value.get("provider_org_sha256")
                if observed:
                    if observed in hashes and hashes[observed] != value["org"]:
                        raise Exhausted("Provider báo hai slot chung org; dừng để đối soát quota")
                    hashes[observed] = value["org"]
            return reply, row
        finally:
            ORG.reset(token)


def carry_smoke(root: Path, initial: dict[int, list[dict]]) -> dict[int, list[dict]]:
    """Research chỉ mang chi phí smoke, tuyệt đối không mang forecast/response smoke."""
    result = deepcopy(initial)
    for row in wire_state(root / NAMESPACES["SMOKE"])["rows"]:
        value = {k: deepcopy(row[k]) for k in ("id", "started_at", "completed_at", "reserved_tokens", "total_tokens",
                 "status", "retry_until", "headers", "provider_org_sha256") if k in row}
        value["model"] = row["body"]["model"]
        result[row["org"]].append(value)
    return result
