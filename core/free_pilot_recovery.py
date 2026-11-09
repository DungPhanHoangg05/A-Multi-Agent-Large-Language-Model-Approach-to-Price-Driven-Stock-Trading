"""Phục hồi pilot theo bằng chứng durable; retry tạm thời không giới hạn theo slot."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import time
from typing import Any, Iterator
from unittest.mock import patch

from core.bayesian_memory import read_json
from core.historical_evaluation_audit import http_records, serializer, serialized_body
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import digest
from core.prior_run_lock import safe_path, utc_now
from core.prior_stage_journal import encode_output

POLICY = {"version": "pilot_recovery_v3", "max_http_per_slot": None, "max_http_per_attempt": 3,
          "transient_http": [429, 500, 502, 503, 504], "backoff_base_seconds": 30, "backoff_max_seconds": 900,
          "success": "OFFLINE_REPLAY_SAME_ATTEMPT_UUID", "no_dispatch": "NO_LEDGER_ROW_FOR_CURRENT_ATTEMPT",
          "transport": "DURABLE_DIAGNOSTIC_REQUIRED", "quota": "KEEP_CARRY_AND_UNKNOWN_RESERVES",
          "schema_repair": "RETRY_INVALID_SCHEMA_WITH_AUDITED_FORMAT_INSTRUCTION; NO_LOCAL_REPLY_EDITS"}
REPLAY: ContextVar[Any] = ContextVar("pilot_offline_replay", default=None)
REPAIR: ContextVar[Any] = ContextVar("pilot_schema_repair", default=None)
REPAIR_INSTRUCTION = ("\nLƯU Ý ĐỊNH DẠNG JSON: Phản hồi trước không đạt schema. Trả đủ các trường bắt buộc; "
    "các trường chuỗi không được rỗng, kể cả evidence_against. Nếu thiếu bằng chứng, nêu rõ giới hạn; "
    "không bịa thông tin. Chỉ trả JSON đúng schema.")


def repair_request(request: dict) -> tuple[dict, dict]:
    """Thêm chỉ dẫn định dạng cố định; giữ reports/facts/schema/model/options và không sửa reply."""
    from core.mt_bicl_prompt_limits import check_prompt_length
    actual = deepcopy(request)
    actual["messages"][0]["content"] += REPAIR_INSTRUCTION
    check_prompt_length(actual["messages"][0]["content"])
    proof = {"version": "schema_repair_v1", "base_request_sha256": digest(request),
             "repair_request_sha256": digest(actual)}
    return actual, proof


def request_body_hash(request: dict) -> str:
    """Hash body SDK giống runtime đã khóa, gồm schema title/options thực gửi."""
    model = serializer({k: request[k] for k in ("model", "temperature", "max_tokens", "service_tier", "client_options")})
    return digest(serialized_body(model, request["messages"][0]["content"], request["structured"]["schema"]))


def actual_request(request: dict, proof: dict | None) -> dict:
    """Chỉ chấp nhận đúng bản sửa đã định nghĩa, không tin request tự khai trong cache."""
    if proof is None:
        return request
    actual, expected = repair_request(request)
    if proof != expected:
        raise ValueError("Proof schema repair khác request gốc")
    return actual


def valid_decision_reply(book: RunBook, doc: dict, row: dict) -> bool:
    """Phân biệt HTTP200 hợp lệ với JSON sai schema trước khi chọn replay hoặc repair."""
    request = doc["inputs"].get("request")
    if not request or "structured" not in request:
        return True  # Vision vẫn dùng cold validator node, không áp schema Decision.
    raw = checked_http(book, row)
    actual = actual_request(request, row.get("pilot_schema_repair"))
    if request_body_hash(actual) != raw["request_body_sha256"]:
        raise ValueError("Raw Decision khác base/repair request đã khóa")
    matches = [(r, payload) for r, payload in http_records(book, row["checkpoint_attempt_id"], row["branch_id"]) if r["id"] == row["id"]]
    if len(matches) != 1:
        raise ValueError("Không join được raw Decision duy nhất")
    from jsonschema import Draft202012Validator, ValidationError
    try:
        reply = json.loads(matches[0][1]["choices"][0]["message"]["content"])
        Draft202012Validator(request["structured"]["schema"]).validate(reply)
        return True
    except (json.JSONDecodeError, KeyError, IndexError, TypeError, ValidationError):
        return False


@contextmanager
def supervisor_transport_policy() -> Iterator[None]:
    """Thay trần cộng dồn cũ bằng các attempt hữu hạn; supervisor tự phục hồi tiếp."""
    import httpx
    from core import historical_transport_observer as observer
    from core.historical_evaluation_clients import RawHTTP
    original_observer, original_init = observer.observe_transport, RawHTTP.__init__

    @contextmanager
    def observe(root: Path, *, recover_connection_reset: bool = False) -> Iterator[None]:
        # Giữ diagnostic gốc; retry/reset được điều phối bên ngoài theo UUID durable.
        sources = observer.source_bindings(root)
        with original_observer(root, recover_connection_reset=False):
            observed = RawHTTP.handle_request

            def initialize(transport: Any, clients: Any, pacer: Any, inner: Any = None) -> None:
                if inner is None:
                    inner = httpx.HTTPTransport(retries=0, limits=httpx.Limits(max_keepalive_connections=0))
                original_init(transport, clients, pacer, inner)

            def request(transport: Any, message: httpx.Request) -> httpx.Response:
                message.extensions["timeout"] = deepcopy(observer.RECOVERY_POLICY["timeouts"])
                transport.pacer.state["requests"][-1]["historical_transport_policy"] = {
                    "version": POLICY["version"], "max_http_per_slot": None,
                    "max_http_per_attempt": POLICY["max_http_per_attempt"],
                    "timeouts": deepcopy(observer.RECOVERY_POLICY["timeouts"]), "sources": sources}
                if REPAIR.get() is not None:
                    transport.pacer.state["requests"][-1]["pilot_schema_repair"] = deepcopy(REPAIR.get())
                transport.pacer.save()
                return observed(transport, message)

            with patch.object(RawHTTP, "__init__", initialize), patch.object(RawHTTP, "handle_request", request):
                yield

    with patch.object(observer, "observe_transport", observe):
        yield


def slot_rows(book: RunBook, doc: dict) -> list[dict]:
    """Join đủ năm ledger và mọi attempt, không mất lần thử cũ khi khởi động lại."""
    if (doc["signature"] != book.signature or doc["run_uuid"] != book.uuid
            or doc["inputs_sha256"] != digest(doc["inputs"])):
        raise ValueError("Journal khác UUID/source/inputs")
    ids = {a["attempt_id"] for a in doc["attempts"]}
    rows, seen = [], set()
    for org in range(1, 6):
        path = book.directory / "usage" / f"org{org}.json"
        ledger = read_json(path)
        for row in ledger["requests"]:
            if (org, row["id"]) in seen:
                raise ValueError("Ledger trùng request UUID")
            seen.add((org, row["id"]))
            if row.get("checkpoint_attempt_id") not in ids:
                continue
            expected_org = doc["inputs"].get("org", doc["inputs"].get("source", {}).get("org"))
            expected_point = doc["inputs"].get("request", {}).get("point_id") if doc["inputs"].get("request") else None
            expected_point = expected_point or doc["inputs"].get("source", {}).get("point")
            if (row.get("run_signature") != book.signature or row.get("branch_id") != doc["slot"].split("/")[-1]
                    or expected_org != org or expected_point != row.get("point_id")):
                raise ValueError("HTTP khác org/point/branch/source của slot")
            rows.append(row)
    # Mỗi invocation giữ budget riêng; số invocation phục hồi của slot không bị chặn.
    if any(sum(r["checkpoint_attempt_id"] == attempt for r in rows) > POLICY["max_http_per_attempt"] for attempt in ids):
        raise ValueError("Ledger vượt ngân sách HTTP của một attempt")
    return rows


def checked_http(book: RunBook, row: dict) -> dict:
    """Xác minh raw HTTP, request/response audit và UUID trước mọi quyết định phục hồi."""
    proof = row.get("historical_raw")
    if not proof:
        raise ValueError("HTTP thiếu raw durable; không suy đoán để gửi lại")
    path = safe_path(book.directory, proof["path"])
    if hashlib.sha256(path.read_bytes()).hexdigest() != proof["sha256"]:
        raise ValueError("Raw HTTP khác checksum")
    raw = load(path)
    if raw["status"] != row["status"] or any(raw["slot"].get(k) != row.get(k) for k in
            ("checkpoint_attempt_id", "run_signature", "point_id", "branch_id")):
        raise ValueError("Raw HTTP khác status hoặc identity ledger")
    # Dùng chính validator cold của runtime đã khóa, gồm body/canonical hash.
    http_records(book, row["checkpoint_attempt_id"], row["branch_id"])
    return raw


def recovery_action(book: RunBook, doc: dict, *, now: float | None = None) -> dict:
    """Không dùng UUID cũ; chọn attempt cuối và phân biệt replay200/retry/no-dispatch."""
    now = time.time() if now is None else float(now)
    last = doc["attempts"][-1]
    if last["status"] != "unknown":
        raise ValueError("Chỉ phục hồi unknown; không gọi lại slot complete")
    rows = slot_rows(book, doc)
    current = [r for r in rows if r["checkpoint_attempt_id"] == last["attempt_id"]]
    wire_successes = [r for r in rows if r["status"] == 200]
    successes = [r for r in wire_successes if valid_decision_reply(book, doc, r)]
    if any(r["checkpoint_attempt_id"] != last["attempt_id"] for r in successes):
        raise ValueError("Có HTTP200 ở attempt trước; cần audit, không gửi lại")
    for row in rows:
        if isinstance(row["status"], int):
            checked_http(book, row)
    base = {"slot": doc["slot"], "attempt_id": last["attempt_id"], "http_count": len(rows), "resume_at": now}
    if successes:
        if successes[-1]["id"] != wire_successes[-1]["id"]:
            raise ValueError("Có response hợp lệ trước response lỗi; cần audit, không chọn lại kết quả")
        return {**base, "kind": "REPLAY", "reason": "DURABLE_HTTP200_NO_NEW_API"}
    if not current:
        # Wrapper HTTP luôn fsync reserve trước dispatch; không có row nghĩa là chưa dispatch.
        resume = now + 2
        org = doc["inputs"].get("org", doc["inputs"].get("source", {}).get("org"))
        if org in range(1, 6):
            stop = read_json(book.directory / "usage" / f"org{org}.json").get("last_stop", {})
            started = datetime.fromisoformat(last["started_at"]).timestamp()
            if (stop.get("reason") in ("DAILY_QUOTA", "PROVIDER_DAILY_QUOTA", "WAIT_BUDGET_EXCEEDED", "INVOCATION_WAIT_BUDGET_EXCEEDED")
                    and stop.get("at", 0) >= started and stop.get("resume_not_before_utc")):
                resume = max(resume, datetime.fromisoformat(stop["resume_not_before_utc"]).timestamp() + 2)
        return {**base, "kind": "READY" if last.get("authorization") is not None else "RETRY",
                "reason": "PRE_DISPATCH_NO_HTTP", "resume_at": resume}
    delay = min(POLICY["backoff_max_seconds"], POLICY["backoff_base_seconds"] * 2 ** min(10, max(0, len(rows)-1)))
    for row in current:
        if row["status"] == 200:
            base["resume_at"] = max(base["resume_at"], now + delay)
        elif row["status"] in POLICY["transient_http"]:
            raw = checked_http(book, row)
            try:
                retry = float(raw.get("headers", {}).get("retry-after", 0))
            except (TypeError, ValueError):
                retry = 0.
            if not 0 <= retry <= 86400:
                raise ValueError("Retry-after không hợp lệ")
            reset = row.get("retry_until") or 0.
            if type(reset) not in (int, float) or not math.isfinite(reset) or reset < 0:
                raise ValueError("Mốc quota không hợp lệ")
            base["resume_at"] = max(base["resume_at"], now + delay, now + retry, reset + 1 if reset else now)
        elif row["status"] == "transport_error":
            diagnostic = load(safe_path(book.directory, "diagnostics/" + row["id"] + ".json"))
            if (diagnostic["request_record_id"] != row["id"] or diagnostic["run_uuid"] != book.uuid
                    or diagnostic["run_signature"] != book.signature
                    or diagnostic["checkpoint_attempt_id"] != last["attempt_id"]
                    or diagnostic.get("point_id") != row.get("point_id") or diagnostic.get("role") != row.get("role")
                    or diagnostic["provider_outcome"] != "UNKNOWN" or not diagnostic["exception_chain"]):
                raise ValueError("Chẩn đoán transport không khớp UUID")
            from core.historical_transport_observer import source_bindings
            if diagnostic["sources"] != source_bindings(book.directory.parents[2]):
                raise ValueError("Chẩn đoán transport khác source đã khóa")
            base["resume_at"] = max(base["resume_at"], now + delay)
        else:
            raise ValueError("Lỗi chưa có bằng chứng phục hồi an toàn; xem worker log")
    return {**base, "kind": "READY" if last.get("authorization") is not None else "RETRY",
            "reason": "INVALID_DECISION_SCHEMA_REPAIR" if wire_successes else "AUDITED_TRANSIENT_HTTP_OR_TRANSPORT"}


def pending_action(book: RunBook, *, now: float | None = None) -> dict | None:
    """Một worker tuần tự chỉ được có một slot chưa hoàn tất."""
    pending = []
    for path in (book.directory / "slots").glob("*.json"):
        doc = load(path)
        if not book.complete(doc["slot"]):
            pending.append(doc)
    if len(pending) > 1:
        raise ValueError("Nhiều slot unknown; không tự chọn UUID")
    return recovery_action(book, pending[0], now=now) if pending else None


def attempt_document(book: RunBook, attempt: str) -> dict:
    """Lấy đúng parent đang invoke; không suy UUID từ tên mã hoặc phase cũ."""
    matches = [doc for path in (book.directory / "slots").glob("*.json")
               if (doc := load(path))["attempts"][-1]["attempt_id"] == attempt]
    if len(matches) != 1:
        raise ValueError("Attempt Decision không có journal duy nhất")
    slot_rows(book, matches[0])
    return matches[0]


def verify_repaired_decision(book: RunBook, response: dict, branch: str, *, fixture: bool, request: dict | None = None) -> None:
    """Cold verify đúng request gốc hoặc bản sửa có proof; vẫn dùng validator raw của baseline."""
    from core.historical_evaluation_audit import verify_decision
    if fixture or request is None:
        if response.get("schema_repair") is not None:
            raise ValueError("Schema repair cần base request thật")
        return verify_decision(book, response, branch, fixture=fixture, request=request)
    from jsonschema import Draft202012Validator
    Draft202012Validator(request["structured"]["schema"]).validate(response["reply"])
    successes = [(r, payload) for r, payload in http_records(book, response["request_id"], branch) if r["status"] == 200]
    if not successes or successes[-1][0].get("pilot_schema_repair") != response.get("schema_repair"):
        raise ValueError("Response repair không khớp marker durable trong ledger")
    actual = actual_request(request, response.get("schema_repair"))
    verify_decision(book, response, branch, fixture=False, request=actual)


class ReplayModel:
    """Phục hồi vision bằng raw200 đúng payload, không đi qua transport/quota lần nữa."""
    def __init__(self, book: RunBook, doc: dict, config: dict) -> None:
        self.book, self.doc, self.config, self.position = book, doc, config, 0
        role = doc["slot"].split("/")[-1]
        self.success = [(r, p) for r, p in http_records(book, doc["attempts"][-1]["attempt_id"], role) if r["status"] == 200]

    def invoke(self, messages: Any, *args: Any, **kwargs: Any) -> Any:
        from langchain_core.messages import AIMessage
        if self.position >= len(self.success):
            raise ValueError("Replay không có thêm raw200; không gửi API mới")
        row, payload = self.success[self.position]
        config = self.config
        model = serializer({"model": config["signal_config"]["models"]["graph_llm_model"], "temperature": 0.,
                            "max_tokens": 960, "service_tier": "on_demand", "client_options": config["client_options"]["graph"]})
        raw = checked_http(self.book, row)
        if digest(serialized_body(model, messages)) != raw["request_body_sha256"]:
            raise ValueError("Replay vision khác body/PIT/ảnh gốc")
        self.position += 1
        return AIMessage(content=payload["choices"][0]["message"].get("content") or "")


@contextmanager
def replay_durable_success() -> Iterator[None]:
    """Khôi phục output mất sau HTTP200 bằng caller/policy gốc, cùng attempt UUID."""
    from core.free_pilot_runtime import PilotClients
    from core import free_pilot_runtime as runtime
    from core.historical_evaluation_clients import Clients
    original_execute, original_models = RunBook.execute, PilotClients.models
    original_decision, original_stage = PilotClients.decision, PilotClients.stage

    def models(client: Any, org: int) -> tuple:
        replay = REPLAY.get()
        if replay is None:
            return original_models(client, org)
        if replay["model"] is None:
            replay["model"] = ReplayModel(client.book, replay["doc"], client.data.protocol["inference"]["config"])
        return None, replay["model"]

    def decision(client: Any, org: int, request: dict, attempt: str, branch: str) -> dict:
        replay = REPLAY.get()
        if replay is None:
            doc = attempt_document(client.book, attempt)
            if doc["inputs"].get("request") != request:
                raise ValueError("Decision khác base request trong journal")
            previous = [r for r in slot_rows(client.book, doc) if r["status"] == 200]
            needs_repair = any(not valid_decision_reply(client.book, doc, r) for r in previous)
            actual, proof = repair_request(request) if needs_repair else (request, None)
            token = REPAIR.set(proof)
            try:
                response = original_decision(client, org, actual, attempt, branch)
            finally:
                REPAIR.reset(token)
            if proof is not None:
                response["schema_repair"] = proof
            return response
        from langchain_core.messages import AIMessage
        from jsonschema import Draft202012Validator
        import json
        successes = [(r, p) for r, p in http_records(client.book, attempt, branch) if r["status"] == 200]
        if not successes:
            raise ValueError("Không có raw Decision200 để phục hồi")
        row, payload = successes[-1]
        actual = actual_request(request, row.get("pilot_schema_repair"))
        expected = request_body_hash(actual)
        if expected != checked_http(client.book, row)["request_body_sha256"]:
            raise ValueError("Replay Decision khác body gốc")
        content = payload["choices"][0]["message"]["content"]
        reply = json.loads(content)
        Draft202012Validator(request["structured"]["schema"]).validate(reply)
        response = {"reply": reply, "raw_message": encode_output({"messages": [AIMessage(content=content)]})["messages"],
                    "request_id": attempt, "expected_http_body_sha256": expected}
        if row.get("pilot_schema_repair") is not None:
            response["schema_repair"] = deepcopy(row["pilot_schema_repair"])
        return response

    def stage(client: Any, *args: Any, **kwargs: Any) -> dict:
        return (Clients.stage if REPLAY.get() is not None else original_stage)(client, *args, **kwargs)

    def execute(book: RunBook, slot: str, inputs: dict, function: Any, *, validate: Any = None) -> dict:
        path = book.path(slot)
        if book.verify_only or not path.exists():
            return original_execute(book, slot, inputs, function, validate=validate)
        doc = load(path)
        if doc["attempts"][-1]["status"] != "unknown":
            return original_execute(book, slot, inputs, function, validate=validate)
        action = recovery_action(book, doc)
        if action["kind"] != "REPLAY":
            return original_execute(book, slot, inputs, function, validate=validate)
        if doc["inputs"] != inputs:
            raise ValueError("Phục hồi khác inputs đã durable")
        context = {"doc": doc, "model": None}
        token = REPLAY.set(context)
        try:
            output = function(action["attempt_id"])
            if validate:
                previous = book.verify_only
                try:
                    book.verify_only = True
                    validate(output)
                finally:
                    book.verify_only = previous
            if context["model"] is not None and context["model"].position != len(context["model"].success):
                raise ValueError("Replay chưa tiêu thụ đúng raw vision")
        finally:
            REPLAY.reset(token)
        last = doc["attempts"][-1]
        encoded = encode_output(output)
        last.update(status="complete", output=encoded, output_sha256=digest(encoded),
                    offline_recovery={"policy": POLICY["version"], "at": utc_now(), "new_api_calls": 0})
        save(path, doc)
        return deepcopy(output)

    with patch.object(RunBook, "execute", execute), patch.object(PilotClients, "models", models), \
            patch.object(PilotClients, "decision", decision), patch.object(PilotClients, "stage", stage), \
            patch.object(runtime, "verify_decision", verify_repaired_decision):
        yield
