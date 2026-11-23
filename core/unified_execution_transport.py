"""Ranh HTTP durable U07; chỉ transport mô phỏng, không kế thừa quyền inference cũ."""
from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import re
from typing import Any, Callable
from uuid import uuid4

from core.historical_evaluation_journal import load, save
from core.unified_contracts import digest, json_bytes

LIMITS = {"rpm": 30, "rpd": 1000, "tpm": 8000, "tpd": 200000}
REPAIR = ("\nLƯU Ý ĐỊNH DẠNG JSON: Phản hồi trước không đạt schema. Trả đủ các trường bắt buộc; "
          "không sửa dữ kiện, không bịa bằng chứng. Chỉ trả JSON đúng schema.")


class Deferred(BaseException):
    """Nhường hàng đợi org; không ngủ hoặc để agent đổi thành báo cáo dự phòng."""
    def __init__(self, until: float) -> None:
        self.until = float(until)


class Uncertain(BaseException):
    """Không tự gửi lại request chưa biết kết quả provider."""


class Exhausted(BaseException):
    """Đã dùng hết ba attempt, không biến lỗi thành CASH."""


def wire_state(directory: Path) -> dict[str, Any]:
    """Index nhẹ neo từng raw record bằng hash; replay phát hiện sửa/xóa response độc lập."""
    state = load(directory / "wire.json")
    expanded = []
    for binding in state["rows"]:
        row = load(directory / "http" / (binding["id"] + ".json"))
        if digest(row) != binding["sha256"]:
            raise ValueError("Raw HTTP khác checksum index")
        expanded.append(row)
    return {**state, "rows": expanded}


def body_for(request: dict[str, Any], *, repair: bool = False) -> dict[str, Any]:
    """Dựng ABI SDK bằng hàm chuyển schema thuần, không tạo client hoặc đọc key."""
    from langchain_core.utils.function_calling import convert_to_json_schema
    schema = deepcopy(request["structured"]["schema"])
    schema.setdefault("title", "UtilityICLReply")
    converted = convert_to_json_schema(schema)
    messages = deepcopy(request["messages"])
    if repair:
        messages[0]["content"] += REPAIR
    if (len(messages) != 1 or messages[0]["role"] != "user"
            or type(messages[0]["content"]) is not str or len(messages[0]["content"]) >= 6500):
        raise ValueError("Decision body không đúng projection hoặc vượt budget")
    if request["client_max_retries"] != 0 or request["structured"]["method"] != "json_schema":
        raise ValueError("Không nhận retry SDK hoặc phương thức schema khác")
    return {"model": request["model"], "stream": False, "n": 1,
        "temperature": max(1e-8, request["temperature"]), "stop": None,
        "reasoning_format": None, "reasoning_effort": None,
        "service_tier": request["service_tier"], **deepcopy(request["client_options"]),
        "max_tokens": request["max_tokens"], "messages": messages,
        "response_format": {"type": "json_schema", "json_schema": {"name": converted["title"], "schema": converted}}}


def parsed(body: dict[str, Any], response: dict[str, Any]) -> Any:
    """Giữ nguyên raw reply; schema lỗi phải repair, không vá hoặc suy action cục bộ."""
    from jsonschema import Draft202012Validator
    value = response["choices"][0]["message"]["content"]
    if "response_format" not in body:
        if type(value) is not str or not value.strip():
            raise ValueError("Vision response rỗng")
        return value
    reply = json.loads(value)
    Draft202012Validator(body["response_format"]["json_schema"]["schema"]).validate(reply)
    return reply


def check_usage(row: dict[str, Any]) -> None:
    """Kiểm usage cả khi replay sau crash ngay sau raw fsync, trước lần parse đầu."""
    if row["status"] == 200:
        try:
            usage = json.loads(row["response"]).get("usage", {}).get("total_tokens")
        except (json.JSONDecodeError, AttributeError):
            return
        if usage is not None and (type(usage) is not int or not 0 <= usage <= row["reserved_tokens"]):
            raise Exhausted("Usage vượt reserve; dừng để audit estimator")


def cooldown(row: dict[str, Any], ordinal: int) -> float:
    """Tái dựng backoff từ raw đã fsync kể cả crash trước cập nhật metadata retry."""
    if row["status"] not in (429, 500, 502, 503, 504):
        return 0.
    match = re.search(r"retry after\s+([0-9.]+)\s*s", row["response"], re.I)
    values = [min(900., 5. * 2 ** ordinal), float(row["headers"].get("retry-after", 0)), float(match[1]) if match else 0.]
    if any(not math.isfinite(v) or v < 0 for v in values):
        raise ValueError("Retry-after không hợp lệ")
    return row["completed_at"] + max(values)


class MockHTTP:
    """Adapter mock duy nhất được U07 cho phép; không chứa HTTPTransport thật."""
    def __init__(self, handler: Callable[[Any], Any]) -> None:
        import httpx
        self.transport = httpx.MockTransport(handler)

    def send(self, body: dict[str, Any]) -> tuple[int, bytes, dict[str, str]]:
        """Đi qua httpx.Request/Response thực nhưng không mở socket hoặc dùng credential."""
        import httpx
        response = self.transport.handle_request(httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions",
                                                              content=json_bytes(body)))
        response.read()
        return response.status_code, response.content, dict(response.headers)


class DurableCalls:
    """Một owner retry, raw trước parse, pooled quota cả hai model trên từng org."""
    def __init__(self, directory: Path, signature: str, epoch: str, sender: MockHTTP,
                 history: dict[int, list[dict]], clock: Callable[[], float],
                 hook: Callable[[str], None] = lambda _: None) -> None:
        if type(sender) is not MockHTTP or not epoch.strip() or set(history) != set(range(1, 6)):
            raise ValueError("U07 chỉ mở mock HTTP và năm shard; không có grant live")
        self.directory, self.signature, self.epoch = directory, signature, epoch
        self.sender, self.clock, self.hook = sender, clock, hook
        path = directory / "wire.json"
        carry = []
        for org, rows in history.items():
            seen = {}
            for row in rows:
                if row["id"] in seen and seen[row["id"]] != row:
                    raise ValueError("Carry trùng UUID nhưng khác nội dung")
                seen[row["id"]] = row
            for row in seen.values():
                if (not math.isfinite(row["started_at"]) or type(row["reserved_tokens"]) is not int
                        or row["reserved_tokens"] < 1):
                    raise ValueError("Carry có thời điểm/token không hợp lệ")
                carry.append({**deepcopy(row), "org": org})
        self.identity = {"signature": signature, "epoch": epoch, "history_sha256": digest(carry), "mode": "CONTROL_ONLY"}
        self.state = wire_state(directory) if path.exists() else {"identity": self.identity, "carry": carry, "rows": []}
        if self.state["identity"] != self.identity or self.state["carry"] != carry:
            raise ValueError("Transport đổi epoch/source/carry khi resume")
        self.bindings = [{"id": r["id"], "sha256": digest(r)} for r in self.state["rows"]]

    def refresh(self) -> None:
        """Nạp lại dưới khóa owner của runner, không ghi snapshot cũ khi có worker khác."""
        if (self.directory / "wire.json").exists():
            state = wire_state(self.directory)
            if state["identity"] != self.identity or state["carry"] != self.state["carry"]:
                raise ValueError("Wire đổi identity/carry dưới khóa owner")
            self.state = state
            self.bindings = [{"id": r["id"], "sha256": digest(r)} for r in state["rows"]]

    def persist(self) -> None:
        """Fsync trước dispatch và sau raw response; không lưu credential/request headers."""
        if self.state["rows"]:
            row = self.state["rows"][-1]
            save(self.directory / "http" / (row["id"] + ".json"), row)
            binding = {"id": row["id"], "sha256": digest(row)}
            if len(self.bindings) < len(self.state["rows"]):
                self.bindings.append(binding)
            else:
                self.bindings[-1] = binding
        save(self.directory / "wire.json", {**self.state,
            "rows": self.bindings})

    def ready(self, org: int, tokens: int) -> None:
        """Không nhân quota theo model/key; giữ unknown reserve tới hết cửa sổ đã khóa."""
        if org not in range(1, 6) or type(tokens) is not int or not 0 < tokens <= LIMITS["tpm"]:
            raise ValueError("Org hoặc token admission ngoài protocol")
        now = self.clock()
        rows = [r for r in self.state["carry"] + self.state["rows"] if r["org"] == org]
        daily = [r for r in rows if r["started_at"] > now - 86400]
        minute = [r for r in daily if r["started_at"] > now - 61]
        for subset, count, budget, span, charged in ((daily, "rpd", "tpd", 86400, True), (minute, "rpm", "tpm", 61, False)):
            total = sum((r.get("total_tokens") or r["reserved_tokens"]) if charged else r["reserved_tokens"] for r in subset)
            if len(subset) >= LIMITS[count] or total + tokens > LIMITS[budget]:
                raise Deferred(min(r["started_at"] for r in subset) + span + .01)
        until = max((r.get("retry_until", 0) for r in rows), default=0)
        if until > now:
            raise Deferred(until)
        if rows:
            from core.groq_pacing import reset_seconds
            last = rows[-1]
            headers = last.get("headers", last.get("rate_limits", {}))
            for header, bound in (("x-ratelimit-limit-requests", LIMITS["rpd"]), ("x-ratelimit-limit-tokens", LIMITS["tpm"])):
                if header in headers and (not math.isfinite(float(headers[header])) or float(headers[header]) < bound):
                    raise Exhausted("Provider giảm hạn mức; dừng chờ quota mới")
            for field, required, span in (("requests", 1, 86400), ("tokens", tokens, 61)):
                value = headers.get("x-ratelimit-remaining-" + field)
                if value is not None:
                    value = float(value)
                    if not math.isfinite(value) or value < 0:
                        raise ValueError("Header remaining không hợp lệ")
                    reset = reset_seconds(headers.get("x-ratelimit-reset-" + field, ""))
                    until = last.get("completed_at", last["started_at"]) + (reset if reset is not None else span) + .01
                    if value < required and until > now:
                        raise Deferred(until)

    def call(self, slot: str, org: int, body: dict[str, Any], attempt: str) -> tuple[Any, dict[str, Any]]:
        """Replay raw200 cùng UUID; ba attempts cộng dồn cả transient và schema repair."""
        from core.groq_pacing import request_budget
        from core.research_invocation import ENABLED, invocation_scope
        from agents.decision_agent import _invoke_with_retry
        from jsonschema import ValidationError
        rows = [r for r in self.state["rows"] if r["slot"] == slot]
        repair = False
        for ordinal, row in enumerate(rows):
            check_usage(row)
            if (row["org"] != org or row["attempt"] != attempt or row["base_sha256"] != digest(body)
                    or row["epoch"] != self.epoch):
                raise ValueError("HTTP slot đổi org/attempt/body/epoch")
            if row["status"] == "UNKNOWN":
                raise Uncertain("UNKNOWN cần đối soát UUID " + row["id"])
            actual = deepcopy(body)
            if row["repair"]:
                actual["messages"][0]["content"] += REPAIR
            if row["body"] != actual:
                raise ValueError("Raw HTTP khác base/repair request đã khóa")
            if row["status"] == 200:
                try:
                    reply = parsed(actual, json.loads(row["response"]))
                except (ValueError, KeyError, IndexError, TypeError, ValidationError):
                    repair = "response_format" in body
                    if not repair:
                        raise Exhausted("Vision raw không hợp lệ; không gọi lại ngầm")
                else:
                    if row is not rows[-1]:
                        raise ValueError("Có response hợp lệ trước HTTP khác; không chọn lại kết quả")
                    return reply, row
            elif row["status"] not in (429, 500, 502, 503, 504, "NOT_SENT"):
                raise Exhausted("HTTP không thuộc transient đã khóa")
            elif cooldown(row, ordinal) > self.clock():
                raise Deferred(cooldown(row, ordinal))
        if len(rows) >= 3:
            raise Exhausted("Hết ba HTTP attempts của execution")
        actual = deepcopy(body)
        if repair:
            actual["messages"][0]["content"] += REPAIR
        if "response_format" in actual and len(actual["messages"][0]["content"]) >= 6500:
            raise ValueError("Repair prompt vượt6500 ký tự")
        tokens = request_budget(actual)
        self.ready(org, tokens)
        row = {"id": str(uuid4()), "slot": slot, "attempt": attempt, "org": org, "epoch": self.epoch,
            "sequence": len(self.state["rows"]), "base_sha256": digest(body), "body": actual,
            "repair": repair, "started_at": self.clock(), "reserved_tokens": tokens,
            "status": "UNKNOWN", "response": None, "headers": {}}
        self.state["rows"].append(row)
        self.persist()
        self.hook("intent")
        token = ENABLED.set(True)
        try:
            with invocation_scope("unified_wire"):
                status, raw, headers = _invoke_with_retry(self.sender.send, actual)
        except BaseException:
            # Không biết provider đã nhận hay chưa; giữ nguyên intent/reserve.
            raise Uncertain("Transport chưa biết kết quả UUID " + row["id"]) from None
        finally:
            ENABLED.reset(token)
        row.update(status=status, response=raw.decode("utf-8"), completed_at=self.clock(),
            headers={k: v for k, v in headers.items() if k.startswith("x-ratelimit-") or k in ("retry-after", "x-request-id")})
        self.persist()
        if status in (429, 500, 502, 503, 504):
            row["retry_until"] = cooldown(row, len(rows))
        if status == 200:
            try:
                usage = json.loads(row["response"]).get("usage", {}).get("total_tokens")
                if usage is not None:
                    if type(usage) is not int or not 0 <= usage <= tokens:
                        raise Exhausted("Usage vượt reserve hoặc không hợp lệ")
                    row["total_tokens"] = usage
            except json.JSONDecodeError:
                pass
        self.persist()
        self.hook("raw")
        # Tái đi qua cùng máy trạng thái để parse/repair; không tăng UUID checkpoint.
        return self.call(slot, org, body, attempt)

    def reconcile_not_sent(self, request_id: str, evidence: str) -> None:
        """Đối soát rõ UUID chưa gửi; giữ reserve và trừ attempt cũ, không reset trần3."""
        rows = [r for r in self.state["rows"] if r["id"] == request_id]
        if len(rows) != 1 or rows[0]["status"] != "UNKNOWN" or not evidence.strip():
            raise ValueError("Reconcile cần đúng UNKNOWN UUID và bằng chứng chưa gửi")
        rows[0].update(status="NOT_SENT", reconciliation=evidence)
        save(self.directory / "http" / (rows[0]["id"] + ".json"), rows[0])
        index = next(i for i, row in enumerate(self.state["rows"]) if row["id"] == request_id)
        self.bindings[index] = {"id": request_id, "sha256": digest(rows[0])}
        self.persist()
