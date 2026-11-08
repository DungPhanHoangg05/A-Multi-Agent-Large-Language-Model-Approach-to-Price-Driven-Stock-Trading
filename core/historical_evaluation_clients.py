"""Client Groq có release guard, quota riêng từng org và raw HTTP durable hữu hạn."""

from __future__ import annotations

import base64
from contextvars import ContextVar
from copy import deepcopy
import hashlib
import hmac
import json
import os
from pathlib import Path
import subprocess
from typing import Any

import httpx
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from agents.decision_agent import _invoke_with_retry
from core.groq_pacing import GroqPacer
from core.historical_evaluation_journal import RunBook, save, load
from core.historical_evaluation_protocol import PROTOCOL, digest, read
from core.improvement_transport import ImprovementTransport, SLOT
from core.research_invocation import CURRENT, ENABLED, RECOVERY, invocation_scope

EXPECTED: ContextVar[Any] = ContextVar("historical_expected_http", default=None)
RUNTIME = Path("docs/plan/week11/historical_evaluation_runtime.json")
RELEASE = Path("docs/plan/week11/historical_evaluation_release.json")


def require_release(root: Path) -> dict[str, Any]:
    """H04 không tự cấp quyền; H06 phải neo grant/check receipt vào Git."""
    if not (root / RELEASE).is_file():
        raise ValueError("Chưa có release H06; không đọc key hoặc gọi API")
    raw = (root / RELEASE).read_bytes()
    if raw != subprocess.check_output(["git", "show", "HEAD:" + RELEASE.as_posix()], cwd=root):
        raise ValueError("Release chưa neo Git")
    release = read(root, RELEASE, envelope=True)
    from core.historical_evaluation_audit import verify_runtime
    verify_runtime(root)
    if (release.get("status") != "RELEASED" or release.get("mode") not in ("SMOKE", "RESEARCH")
            or release.get("api") is not True or release.get("quota_verified") is not True
            or release.get("protocol_sha256") != hashlib.sha256((root / PROTOCOL).read_bytes()).hexdigest()
            or release.get("runtime_sha256") != hashlib.sha256((root / RUNTIME).read_bytes()).hexdigest()
            or not release.get("receipts")):
        raise ValueError("Release/check/quota không khớp protocol/runtime")
    for name, sha in release["receipts"].items():
        from core.prior_run_lock import safe_path
        path = safe_path(root, name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != sha or load(path).get("status") != "PASS":
            raise ValueError("Receipt release chưa PASS hoặc sai hash")
    return release


class RawHTTP(httpx.BaseTransport):
    """Ranh HTTP kiểm payload và lưu body response trước khi SDK/parser nhận kết quả."""

    def __init__(self, clients: Clients, pacer: GroqPacer, inner: httpx.BaseTransport | None = None) -> None:
        self.clients, self.pacer = clients, pacer
        self.inner = inner or httpx.HTTPTransport(retries=0)

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        """Không lưu header credential hoặc tự gửi lại lỗi transport/timeout."""
        body = json.loads(request.content)
        expected, budget = EXPECTED.get(), CURRENT.get()
        if expected is None or budget is None or expected["role"] not in ("pattern", "trend", "decision"):
            raise ValueError("HTTP ngoài slot đã đăng ký")
        output = body.get("max_completion_tokens", body.get("max_tokens"))
        if output != 960 or body.get("temperature") not in (0., 1e-8) or body.get("stream") is not False:
            raise ValueError("HTTP khác output960/temperature/stream đã khóa")
        target = "qwen/qwen3.8-27b" if expected["role"] != "decision" else "openai/gpt-oss-20b"
        if body.get("model") != target:
            raise ValueError("HTTP đổi model ngầm")
        if expected.get("body_sha256") is not None and digest(body) != expected["body_sha256"]:
            raise ValueError("Body SDK khác canonical request đã dựng offline")
        for message in body["messages"]:
            if isinstance(message.get("content"), list):
                for part in message["content"]:
                    if part["type"] == "image_url":
                        url = part["image_url"]["url"]
                        if not url.startswith("data:image/png;base64,"):
                            raise ValueError("Ảnh HTTP không phải snapshot PNG nội bộ")
                        sha = hashlib.sha256(base64.b64decode(url.split(",", 1)[1], validate=True)).hexdigest()
                        if sha not in expected["images"]:
                            raise ValueError("Ảnh HTTP khác parent PIT")
        self.clients.data.verify_sources()
        from core.historical_evaluation_audit import verify_runtime
        verify_runtime(self.clients.data.root)
        if self.clients.http_count >= self.clients.attempt_cap:
            raise ValueError("Hết trần HTTP attempt đã khóa")
        self.clients.http_count += 1
        row = self.pacer.state["requests"][-1]
        row.update(organization=self.pacer.historical_org, credential_scope=self.pacer.historical_scope)
        self.pacer.save()
        response = self.inner.handle_request(request)
        response.read()
        path = self.clients.book.directory / "http" / (row["id"] + ".json")
        save(path, {"version": "historical_raw_http_v1", "slot": deepcopy(SLOT.get()),
                    "request_body_sha256": digest(body), "status": response.status_code,
                    "request_legacy_body_sha256": __import__("core.historical_signals", fromlist=["digest"]).digest(body),
                    "body_base64": base64.b64encode(response.content).decode(),
                    "headers": {k: v for k, v in response.headers.items()
                                if k.startswith("x-ratelimit-") or k in ("retry-after", "x-request-id")}})
        row["historical_raw"] = {"path": path.relative_to(self.clients.book.directory).as_posix(),
                                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        self.pacer.save()
        return response

    def close(self) -> None:
        """Đóng connection của chính transport này."""
        self.inner.close()


class Clients:
    """Không tạo client/key trước release, không xoay key khi org bị quota."""

    def __init__(self, data: Any, book: RunBook) -> None:
        """Resume cộng cả reserve unknown trong năm ledger riêng của run."""
        release = require_release(data.root)
        self.data, self.book, self.cached = data, book, {}
        self.http_count = 0
        for path in (book.directory / "usage").glob("org*.json"):
            from core.bayesian_memory import read_json
            self.http_count += len(read_json(path)["requests"])
        limits = data.protocol["budget"]
        self.attempt_cap = (limits["smoke_control_execution_reserve"] * 3
                            if release["mode"] == "SMOKE" else limits["max_total_http_attempts"])

    def models(self, org: int) -> tuple[Any, Any]:
        """Mỗi org giữ client/ledger riêng, max_retries SDK luôn bằng0."""
        if org not in range(1, 6):
            raise ValueError("Org ngoài năm shard đã khóa")
        if org not in self.cached:
            key = os.environ.get(f"GROQ_ORG_{org}_API_KEY")
            if not key:
                raise ValueError(f"Thiếu credential organization{org}")
            path = self.book.directory / "usage" / f"org{org}.json"
            pacer = GroqPacer(path, policy="request_admission_v2")
            scope = hmac.new(self.book.uuid.encode(), key.encode(), hashlib.sha256).hexdigest()
            pacer.historical_org, pacer.historical_scope = org, scope
            scopes = {r.get("credential_scope") for r in pacer.state["requests"] if r.get("credential_scope")}
            if scopes and scopes != {scope}:
                raise ValueError("Credential khác shard đã bắt đầu; không hotswap key")
            raw = RawHTTP(self, pacer)
            transport = ImprovementTransport(pacer, raw)
            class ScopedTransport(httpx.BaseTransport):
                """Cưỡng chế trần3 cả format repair khi helper legacy bật recovery."""
                def handle_request(self, request: httpx.Request) -> httpx.Response:
                    budget = CURRENT.get()
                    if budget is None:
                        raise ValueError("HTTP thiếu invocation budget")
                    if budget.attempts >= 3:
                        raise ValueError("Vượt3 HTTP/slot")
                    # Cho phép chờ đúng provider reset, trần3 vẫn do transport kiểm độc lập.
                    budget.recovery_enabled = True
                    result = transport.handle_request(request)
                    pacer.state["requests"][-1].update(organization=org, credential_scope=scope)
                    pacer.save()
                    return result
                def close(self) -> None:
                    transport.close()
            http = httpx.Client(transport=ScopedTransport(), timeout=120)
            config = self.data.protocol["inference"]["config"]
            pairs = []
            for role in ("agent", "graph"):
                models = config["signal_config"]["models"]
                pairs.append(ChatGroq(model=models[f"{role}_llm_model"], temperature=0., max_tokens=960,
                    max_retries=0, streaming=False, service_tier="on_demand", api_key=key, http_client=http,
                    **config["client_options"][role]))
            self.cached[org] = tuple(pairs)
        return self.cached[org]

    def stage(self, role: str, attempt: str, point: str, node: Any, state: dict[str, Any]) -> dict[str, Any]:
        """Node lồng dùng cùng ngân sách; mọi helper API đi qua retry wrapper cũ."""
        images = [hashlib.sha256(base64.b64decode(state[k])).hexdigest()
                  for k in ("pattern_image", "trend_image") if state.get(k)]
        tokens = (ENABLED.set(True), RECOVERY.set(False),
                  EXPECTED.set({"role": role, "images": images}))
        slot = SLOT.set({"run_signature": self.book.signature, "point_id": point,
                         "checkpoint_attempt_id": attempt, "branch_id": role})
        try:
            with invocation_scope(role) as budget:
                budget.checkpoint_attempt_id, budget.point_id = attempt, point
                budget.run_signature, budget.branch_id = self.book.signature, role
                return node(state)
        finally:
            SLOT.reset(slot)
            ENABLED.reset(tokens[0]); RECOVERY.reset(tokens[1]); EXPECTED.reset(tokens[2])

    def decision(self, org: int, request: dict[str, Any], attempt: str, branch: str) -> dict[str, Any]:
        """Lưu raw message bên cạnh parsed reply, sửa format nằm trong cùng trần3."""
        llm = self.models(org)[0]
        schema = request["structured"]["schema"]
        structured = llm.with_structured_output(schema, method="json_schema", include_raw=True)
        prompt = request["messages"][0]["content"]
        messages, params = llm._create_message_dicts([HumanMessage(content=prompt)], None)
        raw_chain = structured.steps[0].steps__["raw"]
        expected = digest({"messages": messages, **params, "response_format": raw_chain.kwargs["response_format"]})
        def invoke(state: Any) -> dict[str, Any]:
            """Không catch transport/PIT thành response hoặc CASH."""
            from core.prior_stage_journal import encode_output
            from jsonschema import Draft202012Validator
            last = None
            for _ in range(2):
                result = _invoke_with_retry(structured.invoke, prompt)
                if result.get("parsing_error") is None and isinstance(result.get("parsed"), dict):
                    reply = result["parsed"]
                    errors = list(Draft202012Validator(schema).iter_errors(reply))
                    if not errors:
                        return {"reply": deepcopy(reply), "raw_message": encode_output({"messages": [result["raw"]]})["messages"],
                                "request_id": attempt, "expected_http_body_sha256": expected}
                    last = errors[0]
            raise ValueError("Decision không đúng schema sau format repair") from last
        token = EXPECTED.set({"role": "decision", "images": [], "body_sha256": expected})
        try:
            # stage() phục vụ graph; Decision giữ expected HTTP contract riêng.
            enable, recovery = ENABLED.set(True), RECOVERY.set(False)
            slot = SLOT.set({"run_signature": self.book.signature, "point_id": request["point_id"],
                             "checkpoint_attempt_id": attempt, "branch_id": branch})
            try:
                with invocation_scope("decision") as budget:
                    budget.checkpoint_attempt_id, budget.point_id = attempt, request["point_id"]
                    budget.run_signature, budget.branch_id = self.book.signature, branch
                    return invoke(None)
            finally:
                SLOT.reset(slot); ENABLED.reset(enable); RECOVERY.reset(recovery)
        finally:
            EXPECTED.reset(token)
