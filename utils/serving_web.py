"""API serving có owner và preflight thực; không thay endpoint native/experiment cũ."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4
from typing import TYPE_CHECKING

from flask import Blueprint, Response, current_app, jsonify, request
from itsdangerous import URLSafeTimedSerializer, BadSignature
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from core.serving_contracts import ContractError, ServingRequest
from core.serving_registry import CONTRACT_VERSION, registry_document
if TYPE_CHECKING:
    from core.serving_runtime.service import Service

ROOT = Path(__file__).resolve().parents[1]
COOKIE = "qa_serving_owner"

serving = Blueprint("serving", __name__, url_prefix="/api/serving/v1")


@lru_cache(maxsize=1)
def _default_service() -> Service:
    """Khởi tạo private store, không tạo LLM client/provider trước POST start."""
    from core.serving_runtime.service import Service
    return Service(ROOT)


def service() -> Service:
    """App tests/operator có thể inject service; browser không có field thay backend."""
    return current_app.config.get("SERVING_SERVICE") or _default_service()


def key_snapshot() -> str:
    """Lấy key phía server một lần khi start/resume, không đưa vào browser hoặc config JSON."""
    provider = current_app.config.get("SERVING_API_KEY_PROVIDER")
    value = provider() if provider else os.environ.get("GROQ_API_KEY", "")
    return str(value or "").strip()


def owner(create: bool = False) -> tuple[str | None, str | None]:
    """Cookie ký bằng secret bền vững; SHA scope được dùng kiểm quyền mỗi job."""
    from core.unified_contracts import digest
    signer = URLSafeTimedSerializer(service().quota.secret(), salt="serving-owner-v1")
    cookie = request.cookies.get(COOKIE)
    if cookie:
        try:
            identifier = signer.loads(cookie, max_age=90*86400)
            if type(identifier) is str:
                return digest(identifier), None
        except BadSignature:
            pass
    if create:
        identifier = str(uuid4())
        return digest(identifier), signer.dumps(identifier)
    return None, None


def respond(value: dict, cookie: str | None = None, status: int = 200) -> Response:
    """Không cache nội dung job/owner trong proxy dùng chung."""
    response = jsonify(value)
    response.status_code = status
    response.headers["Cache-Control"] = "no-store"
    if cookie:
        response.set_cookie(COOKIE, cookie, httponly=True, secure=request.is_secure, samesite="Strict", max_age=90*86400)
    return response


def mutation_allowed() -> bool:
    """Content-Type JSON và origin cùng host, không bật CORS hoặc nhận form cross-site."""
    origin = request.headers.get("Origin")
    return request.is_json and (not origin or urlsplit(origin).netloc == request.host and urlsplit(origin).scheme == request.scheme)


@serving.get("/registry")
def serving_registry() -> Response:
    """Công bố khả năng ứng dụng riêng, giữ nguyên endpoint registry nghiên cứu."""
    return jsonify(registry_document())


@serving.post("/preflight")
def serving_preflight() -> Response | tuple[Response, int]:
    """Request đúng nhưng chưa sẵn sàng trả 200/blocked; sai cấu trúc trả 400."""
    try:
        if not mutation_allowed():
            return respond({"version": CONTRACT_VERSION, "status": "invalid", "run_enabled": False,
                            "error": ContractError("INVALID_JSON", "request", "Cần JSON từ cùng origin").document()}, status=400)
        spec = ServingRequest.create(request.get_json())
        _, cookie = owner(True)
        return respond(service().preflight(spec, key_snapshot()), cookie)
    except ContractError as error:
        return jsonify({"version": CONTRACT_VERSION, "status": "invalid", "run_enabled": False,
                        "error": error.document()}), 400
    except (BadRequest, UnsupportedMediaType):
        return jsonify({"version": CONTRACT_VERSION, "status": "invalid", "run_enabled": False,
                        "error": ContractError("INVALID_JSON", "request", "Cần body JSON hợp lệ").document()}), 400


@serving.get("/defaults")
def defaults() -> Response:
    """Cấu hình công khai, không trả API key hoặc hmac credential."""
    from core.serving_runtime.resources import default_models
    return respond({"version": CONTRACT_VERSION, "models": default_models(), "registry": registry_document(),
                    "role_execution": {"indicator": "deterministic", "alpha": "deterministic", "sentiment": "frozen_scores",
                                       "pattern": "vision", "trend": "vision", "decision": "structured_llm"}})


@serving.post("/jobs")
def start_job() -> Response:
    """Start nền chỉ sau preflight, snapshot key/model/config riêng của job."""
    if not mutation_allowed():
        return respond({"error": "Cần JSON từ cùng origin"}, status=400)
    try:
        spec = ServingRequest.create(request.get_json())
        scope, cookie = owner(True)
        key = key_snapshot()
        checked = service().preflight(spec, key)
        if not checked["run_enabled"]:
            return respond(checked, cookie, 409)
        identifier = service().create(spec, key, scope)
        return respond({"run_id": identifier, "status": "queued", "status_url": f"/api/serving/v1/jobs/{identifier}"}, cookie, 202)
    except (ContractError, ValueError, BadRequest, UnsupportedMediaType):
        return respond({"error": "Request hoặc resource serving không hợp lệ"}, status=400)


@serving.get("/jobs/<identifier>")
def job_status(identifier: str) -> Response:
    """Read-only journal, không khởi động lại worker hoặc LLM qua GET."""
    try:
        scope, _ = owner()
        if scope is None:
            raise PermissionError()
        return respond(service().result(identifier, scope))
    except (PermissionError, FileNotFoundError, ValueError, KeyError):
        return respond({"error": "Không có job thuộc owner này"}, status=404)


@serving.post("/jobs/<identifier>/<action>")
def control_job(identifier: str, action: str) -> Response:
    """Stop/resume giữ owner/UUID/identity; không nhận key, model hoặc policy mới trong body."""
    if not mutation_allowed() or action not in ("stop", "resume"):
        return respond({"error": "Thao tác không hợp lệ"}, status=400)
    try:
        if request.get_json() != {}:
            raise ValueError("Control body phải rỗng")
        scope, _ = owner()
        if scope is None:
            raise PermissionError()
        service().store.reservation(identifier, scope)
        if action == "stop":
            service().store.control(identifier, True)
        else:
            service().start(identifier, key_snapshot(), scope)
        return respond({"run_id": identifier, "action": action}, status=202)
    except (PermissionError, FileNotFoundError):
        return respond({"error": "Không có job thuộc owner này"}, status=404)
    except (ValueError, KeyError, BadRequest):
        return respond({"error": "Không resume được job với identity/credential hiện tại"}, status=409)
