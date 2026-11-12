"""Endpoint metadata/preflight mới; không tạo job hoặc mở tài nguyên inference."""
from __future__ import annotations

from flask import Blueprint, Response, jsonify, request
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from core.serving_contracts import ContractError, ServingRequest, preflight
from core.serving_registry import CONTRACT_VERSION, registry_document

serving = Blueprint("serving", __name__, url_prefix="/api/serving/v1")


@serving.get("/registry")
def serving_registry() -> Response:
    """Công bố khả năng ứng dụng riêng, giữ nguyên endpoint registry nghiên cứu."""
    return jsonify(registry_document())


@serving.post("/preflight")
def serving_preflight() -> Response | tuple[Response, int]:
    """Request đúng nhưng chưa sẵn sàng trả 200/blocked; sai cấu trúc trả 400."""
    try:
        spec = ServingRequest.create(request.get_json())
        return jsonify(preflight(spec))
    except ContractError as error:
        return jsonify({"version": CONTRACT_VERSION, "status": "invalid", "run_enabled": False,
                        "error": error.document()}), 400
    except (BadRequest, UnsupportedMediaType):
        return jsonify({"version": CONTRACT_VERSION, "status": "invalid", "run_enabled": False,
                        "error": ContractError("INVALID_JSON", "request", "Cần body JSON hợp lệ").document()}), 400
