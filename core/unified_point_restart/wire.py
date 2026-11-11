"""Wire cho generation mới của điểm reset, giữ nguyên raw HTTP generation cũ."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import time
from typing import Any
from uuid import UUID, uuid4

from core.historical_evaluation_journal import save
from core.unified_contracts import digest
from core.unified_execution_transport import (DurableCalls, Deferred, Uncertain, Exhausted,
    REPAIR, check_usage, parsed, cooldown)
from core.unified_model_quota.policy import MODEL
from core.unified_provider_quota.policy import ProviderCalls, admit


def point_id(slot: str) -> str:
    """Mọi namespace stage U08 đặt ID điểm ngay sau loại stage."""
    parts = slot.removeprefix("prepare/").split("/")
    if len(parts) < 2 or parts[0] not in ("shared", "forecast", "graph", "render", "outcome"):
        raise ValueError("Slot ngoài namespace nghiên cứu U08")
    return parts[1]


class RestartWire(DurableCalls):
    """Chèn dưới LiveCalls trong MRO để tái dùng guard/options/header của U08."""

    def call(self, slot: str, org: int, body: dict[str, Any], attempt: str) -> tuple[Any, dict[str, Any]]:
        """Replay raw200 cùng UUID; ba attempts cộng dồn cả transient và schema repair."""
        from core.groq_pacing import request_budget
        from core.research_invocation import ENABLED, invocation_scope
        from agents.decision_agent import _invoke_with_retry
        from jsonschema import ValidationError
        rows = [r for r in self.state["rows"] if r["slot"] == slot and not self.retired(r)]
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
        row["point_generation"] = self.generations.get(point_id(slot), 0)
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


class RestartCalls(ProviderCalls, RestartWire):
    """Dùng UUID execution mới sau reset và tính mọi HTTP cũ vào phase cap."""
    def __init__(self, *args: Any, retired: dict[str, str] | None = None,
                 generations: dict[str, int] | None = None, **kwargs: Any) -> None:
        """Đối soát mọi ID nghỉ trước khi cho phép nó rời tập execution active."""
        super().__init__(*args, **kwargs)
        self.retirements = dict(retired or {})
        self.generations = dict(generations or {})
        found = {row["id"] for row in self.state["rows"] if self.retired(row)}
        if found != set(self.retirements):
            raise ValueError("Thiếu raw HTTP thuộc generation đã nghỉ")

    def retired(self, row: dict[str, Any]) -> bool:
        """ID nghỉ phải khớp toàn bộ raw đã khóa, gồm body, UUID, status và thời gian."""
        expected = self.retirements.get(row["id"])
        if expected is None:
            return False
        if digest(row) != expected:
            raise ValueError("Raw HTTP đã nghỉ bị đổi")
        return True

    def ready(self, org: int, tokens: int) -> None:
        """Chỉ bỏ UNKNOWN của generation nghỉ khỏi gate, mọi error provider khác vẫn hiệu lực."""
        if len(self.state["rows"]) >= self.attempt_cap_total:
            raise Exhausted("Hết trần HTTP của phase U08")
        visible = [row for row in self.state["rows"] if not (row["status"] == "UNKNOWN" and self.retired(row))]
        admit({"carry": self.state["carry"], "rows": visible}, org, MODEL.get(), tokens,
              self.clock(), self.attempt_cap_total)

    def active_rows(self) -> list[dict[str, Any]]:
        """Verifier của forecast chỉ dùng raw thuộc generation active."""
        return [row for row in self.state["rows"] if not self.retired(row)]


def attach_diagnostics(sender: Any, directory: Path) -> None:
    """Lưu response hoặc loại ngoại lệ trước khi wrapper U08 che chi tiết lỗi mạng."""
    original = sender.send
    active: dict[str, Any] = {}
    def persist() -> None:
        """Chỉ UUID local làm tên file, không ghi request/header chứa credential."""
        UUID(active["request_id"])
        save(directory / "diagnostics" / (active["request_id"] + ".json"), active)
    def headers(response: Any) -> None:
        """Capture request ID và HTTP status ngay khi có headers, trước lúc đọc body."""
        active.update(server_status=response.status_code, headers={k: v for k, v in response.headers.items()
            if k.startswith("x-ratelimit-") or k in ("retry-after", "x-request-id", "date")})
        persist()
    for client in sender.clients.values():
        client.event_hooks["response"].append(headers)
    def send(body: dict[str, Any]) -> tuple[int, bytes, dict[str, str]]:
        """Giữ nguyên lời gọi HTTP, bổ sung bằng chứng durable ở sát transport."""
        active.clear()
        intent = sender.intent()
        active.update(request_id=intent["id"], org=intent["org"], body_sha256=digest(body),
                      started_at=time.time(), status="SENDING")
        persist()
        try:
            result = original(body)
        except BaseException as error:
            active.update(status="TRANSPORT_EXCEPTION", error_type=type(error).__module__ + "." + type(error).__name__,
                          completed_at=time.time())
            persist()
            raise
        active.update(status="RESPONSE_DURABLE", server_status=result[0], response=result[1].decode("utf-8"),
                      headers={k: v for k, v in result[2].items()
                          if k.startswith("x-ratelimit-") or k in ("retry-after", "x-request-id", "date")},
                      completed_at=time.time())
        persist()
        return result
    sender.send = send
