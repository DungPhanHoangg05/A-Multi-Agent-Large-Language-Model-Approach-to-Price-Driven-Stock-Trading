"""Transport serving riêng: intent/raw durable, wrapper chung và retry có trạng thái."""
from __future__ import annotations

from copy import deepcopy
import json
import math
import re
from email.utils import parsedate_to_datetime
from pathlib import Path
import time
from typing import Any, Callable
from uuid import uuid4

from core.historical_evaluation_journal import load, save
from core.unified_contracts import digest, json_bytes
from core.unified_execution_transport import parsed, REPAIR
from core.serving_runtime.quota import Quota, Waiting, Unknown, Failed


def response_headers(headers: dict) -> dict:
    """Giữ các header quota đủ để đối soát và tính retry."""
    return {str(k).lower(): str(v) for k, v in headers.items()
            if str(k).lower().startswith("x-ratelimit-") or str(k).lower() == "retry-after"}


def response_record(row: dict, status: int, raw: bytes, headers: dict, completed: float) -> dict:
    """Chuẩn hóa raw theo cùng ABI khi nhận trực tiếp hoặc phục hồi từ bản lưu."""
    response = raw.decode("utf-8", errors="replace")
    try:
        usage = json.loads(response).get("usage", {}).get("total_tokens")
    except (ValueError, AttributeError):
        usage = None
    invalid = usage is not None and (type(usage) is not int or usage < 0)
    return {**row, "status": int(status), "response": response, "completed_at": completed,
            "headers": response_headers(headers), "usage_invalid": invalid, "usage": None if invalid else usage}


def retry_until(row: dict, ordinal: int) -> float:
    """Backoff và retry-after kể cả HTTP-date; không cắt thời hạn Groq yêu cầu chờ dài."""
    from core.groq_pacing import reset_seconds
    at = row["completed_at"]
    deadlines = [at + min(900., 5.*2**ordinal)] if row["status"] in (429, 500, 502, 503, 504) else [0.]
    match = (re.search(r"(?:retry after|try again in)\s*([0-9]+(?:\.[0-9]+)?)\s*s", row["response"], re.I)
             if row["status"] in (429,500,502,503,504) else None)
    if match:
        deadlines.append(at + float(match[1]) + 1.)
    headers = row["headers"]
    if "retry-after" in headers:
        value = headers["retry-after"]
        try:
            delay = float(value)
            if not math.isfinite(delay) or delay < 0:
                raise ValueError("Retry-after không hợp lệ")
            deadlines.append(at+delay)
        except ValueError:
            deadlines.append(parsedate_to_datetime(value).timestamp())
    for kind, span in (("tokens", 61.), ("requests", 86400.)):
        value = headers.get("x-ratelimit-remaining-"+kind)
        if value is not None and float(value) <= 0:
            seconds = reset_seconds(headers.get("x-ratelimit-reset-"+kind, ""))
            deadlines.append(at+(seconds if seconds is not None else span)+.1)
    return max(deadlines)


class GroqHTTP:
    """Client riêng từng job; không SDK retry, proxy môi trường, redirect hoặc đổi key."""

    def __init__(self, key: str) -> None:
        import httpx
        self.client = httpx.Client(headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            transport=httpx.HTTPTransport(retries=0), timeout=httpx.Timeout(120, connect=15),
            follow_redirects=False, trust_env=False)

    def send(self, body: dict[str, Any]) -> tuple[int, bytes, dict[str, str]]:
        """Endpoint cố định; không trả request headers hoặc credential cho journal/browser."""
        response = self.client.post("https://api.groq.com/openai/v1/chat/completions", content=json_bytes(body))
        response.read()
        return response.status_code, response.content, dict(response.headers)

    def close(self) -> None:
        """Không đóng client legacy hoặc client của job khác."""
        self.client.close()


class Calls:
    """Một slot giữ cùng attempt/body và tối đa ba HTTP, kể cả qua restart."""

    def __init__(self, directory: Path, run_id: str, quota: Quota, sender: Any,
                 guard: Callable[[], None], *, clock=time.time, hook=lambda _: None,
                 total_prompt_guard: bool = False, token_budget: Callable[[dict], int] | None = None) -> None:
        self.directory, self.run_id, self.quota, self.sender = directory, run_id, quota, sender
        self.guard, self.clock, self.hook = guard, clock, hook
        self.total_prompt_guard = total_prompt_guard
        self.token_budget = token_budget

    def _rows(self, slot: str) -> tuple[Path, list[dict]]:
        """Không nhận đường dẫn tùy ý; một file envelope riêng cho mỗi slot."""
        path = self.directory / "http" / (digest(slot) + ".json")
        if not path.exists():
            return path, []
        doc = load(path)
        if doc["run_id"] != self.run_id or doc["slot"] != slot:
            raise ValueError("Wire khác run/slot")
        return path, doc["rows"]

    def account(self, row: dict) -> Quota:
        """Lấy sổ quota của attempt khi phát lại raw."""
        return self.quota

    def attempt_metadata(self) -> dict:
        """Thông tin bổ sung được lưu cùng intent trước khi gửi."""
        return {}

    def dispatch(self, row: dict, body: dict) -> tuple[int, bytes, dict]:
        """Gửi qua client đã chọn cho attempt."""
        return self.sender.send(body)

    def recover_response(self, row: dict) -> dict | None:
        """Chỉ transport có bản sao HTTP durable mới phục hồi được response."""
        return None

    def response_committed(self, row: dict) -> None:
        """Báo cho transport rằng wire chính đã giữ raw."""

    def wait_for_retry(self, row: dict, ordinal: int, account: Quota, *, last: bool) -> None:
        """Ghi thời hạn retry trước khi trả quyền điều phối cho worker."""
        until = retry_until(row, ordinal)
        account.finish(row["id"], str(row["status"]), row.get("usage"), until)
        if until > self.clock():
            raise Waiting(until)

    def call(self, slot: str, body: dict, attempt: str, *,
             validate_reply: Callable[[Any], None] | None = None) -> tuple[Any, dict]:
        """Replay raw đã fsync; ngoại lệ BaseException thoát agent, không suy báo cáo/CASH."""
        from core.groq_pacing import PilotStop, request_budget
        from agents.decision_agent import _invoke_with_retry
        from core.research_invocation import ENABLED, invocation_scope
        from jsonschema import ValidationError
        path, rows = self._rows(slot)
        repair = False
        for ordinal, row in enumerate(rows):
            if row["attempt"] != attempt or row["base_sha256"] != digest(body):
                raise Failed("INTEGRITY_FAILURE")
            actual = deepcopy(body)
            if row["repair"]:
                actual["messages"][0]["content"] += REPAIR
            if actual != row["body"]:
                raise Failed("INTEGRITY_FAILURE")
            if row["status"] == "UNKNOWN":
                recovered = self.recover_response(row)
                if recovered is None:
                    raise Unknown("UNKNOWN_ATTEMPT")
                rows[ordinal] = row = recovered
                save(path, {"run_id": self.run_id, "slot": slot, "rows": rows})
                self.response_committed(row)
            account = self.account(row)
            if row["status"] == "RESPONSE_LOST":
                if row.get("provider_http_status") != 200 or row["response"] is not None:
                    raise Failed("INTEGRITY_FAILURE")
                if row["headers"]:
                    account.observe(row["id"], row["headers"], row["completed_at"])
                repair = repair or row["repair"]
                continue
            if row["status"] != "NOT_SENT":
                account.observe(row["id"], row["headers"], row["completed_at"])
            if row["status"] == 200:
                if row.get("usage_invalid"):
                    raise Failed("INVALID_USAGE")
                if row.get("usage") is not None and row["usage"] > row["reserved_tokens"]:
                    raise Failed("TOKEN_ESTIMATE_UNDERRUN")
                try:
                    reply = parsed(row["body"], json.loads(row["response"]))
                    if validate_reply is not None:
                        validate_reply(reply)
                except (ValueError, KeyError, TypeError, IndexError, ValidationError):
                    if "response_format" not in body:
                        raise Failed("INVALID_MODEL_OUTPUT") from None
                    if validate_reply is not None and not row.get("schema_error"):
                        row["schema_error"] = True
                        save(path, {"run_id": self.run_id, "slot": slot, "rows": rows})
                    repair = True
                else:
                    if ordinal != len(rows)-1:
                        raise ValueError("Không chọn lại response sau slot đã thành công")
                    account.finish(row["id"], "200", row.get("usage"), retry_until(row, ordinal))
                    return reply, row
            elif row["status"] in (429, 500, 502, 503, 504):
                self.wait_for_retry(row, ordinal, account, last=ordinal == len(rows)-1)
            elif row["status"] != "NOT_SENT":
                raise Failed("PROVIDER_FAILURE")
        if len(rows) >= 3:
            raise Failed("ATTEMPT_CAP_EXHAUSTED")
        self.guard()
        actual = deepcopy(body)
        if repair:
            actual["messages"][0]["content"] += REPAIR
        if "response_format" in actual:
            messages = actual["messages"] if self.total_prompt_guard else actual["messages"][:1]
            if sum(len(message["content"]) for message in messages) >= 6500:
                raise Failed("PROMPT_BUDGET_EXCEEDED")
        identifier = str(uuid4())
        tokens = (self.token_budget or request_budget)(actual)
        self.quota.reserve(identifier, self.run_id, tokens)
        row = {**self.attempt_metadata(), "id": identifier, "attempt": attempt, "slot": slot, "base_sha256": digest(body), "body": actual,
               "repair": repair, "started_at": self.clock(), "reserved_tokens": tokens, "status": "UNKNOWN",
               "response": None, "headers": {}, "usage": None}
        rows.append(row)
        save(path, {"run_id": self.run_id, "slot": slot, "rows": rows})
        self.hook("intent")
        enabled = ENABLED.set(True)
        try:
            with invocation_scope("serving_wire"):
                status, raw, headers = _invoke_with_retry(self.dispatch, row, deepcopy(actual))
            recorded = response_record(row, status, raw, headers, self.clock())
        except (Exception, PilotStop):
            recorded = self.recover_response(row)
            if recorded is None:
                raise Unknown("UNKNOWN_ATTEMPT") from None
        except BaseException:
            raise Unknown("UNKNOWN_ATTEMPT") from None
        finally:
            ENABLED.reset(enabled)
        # Raw phải durable trước parse/policy, kể cả crash ngay sau response.
        rows[-1] = recorded
        save(path, {"run_id": self.run_id, "slot": slot, "rows": rows})
        self.response_committed(recorded)
        self.hook("raw")
        if validate_reply is not None:
            return self.call(slot, body, attempt, validate_reply=validate_reply)
        return self.call(slot, body, attempt)

    def reconcile_not_sent(self, slot: str, request_id: str, evidence: str) -> None:
        """Chỉ operator local sau đối soát; không có endpoint browser tự reset UNKNOWN/cap."""
        path, rows = self._rows(slot)
        if not rows or rows[-1]["id"] != request_id or rows[-1]["status"] != "UNKNOWN" or not evidence.strip():
            raise ValueError("Reconcile không đúng UNKNOWN cuối hoặc thiếu bằng chứng")
        rows[-1].update(status="NOT_SENT", reconciliation_sha256=digest(evidence))
        save(path, {"run_id": self.run_id, "slot": slot, "rows": rows})
