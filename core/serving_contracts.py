"""Hợp đồng serving bất biến cho preflight, cấu hình và kết quả; không thực thi inference."""
from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any
from uuid import UUID, uuid4

from core.serving_registry import CONFIG_VERSION, CONTRACT_VERSION, JOB_STATES, REGISTRY_VERSION, required_resources
from core.unified_contracts import checksum, day, digest, json_bytes
from core.variant_registry import execution_order, get_variant

MODEL_ROLES = ("indicator", "pattern", "trend", "alpha", "sentiment", "decision")
COSTS = {"fee": .0025, "slippage": .001, "horizon": 3, "initial_vnd": 50000000}


class ContractError(ValueError):
    """Lỗi có mã ổn định; thông báo không chép lại giá trị đầu vào hay secret."""

    def __init__(self, code: str, field: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.field = field

    def document(self) -> dict[str, Any]:
        """Envelope dùng chung cho API và trạng thái lỗi job."""
        return {"code": self.code, "field": self.field, "message": str(self), "retryable": False}


def _require(condition: bool, field: str, message: str) -> None:
    """Giữ lỗi validation có cấu trúc, không trả traceback ra browser."""
    if not condition:
        raise ContractError("INVALID_REQUEST", field, message)


def _object(value: Any, fields: set[str], field: str) -> None:
    """Schema đóng để API key và field chưa được version hóa không đi vào identity."""
    _require(type(value) is dict and set(value) == fields, field, "Object thiếu hoặc thừa field")


def _token(value: Any) -> bool:
    """Tên version/model/provider dùng token không có whitespace hoặc HTML."""
    return type(value) is str and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,159}", value) is not None


@dataclass(frozen=True)
class ServingRequest:
    """Request mới không tự nhận alias, không đọc globals và không chứa credentials."""
    _bytes: bytes

    @classmethod
    def create(cls, value: Any) -> ServingRequest:
        """Validate trước mọi I/O; model/options của đủ sáu agent được snapshot tường minh."""
        _object(value, {"version", "mode", "variant_ids", "symbols", "start_date", "end_date",
                        "timeframe", "language", "repeats", "models"}, "request")
        try:
            json_bytes(value)
        except ValueError as error:
            raise ContractError("INVALID_REQUEST", "request", "Chỉ nhận JSON nguyên bản hữu hạn") from error
        _require(value["version"] == CONTRACT_VERSION, "version", "Version contract không được hỗ trợ")
        _require(value["mode"] in ("analyze", "compare", "backtest"), "mode", "Mode không được hỗ trợ")
        try:
            execution_order(value["variant_ids"])
        except (ValueError, TypeError) as error:
            raise ContractError("INVALID_REQUEST", "variant_ids", "Variant rỗng, trùng hoặc không được hỗ trợ") from error
        symbols = value["symbols"]
        _require(type(symbols) is list and 1 <= len(symbols) <= 32 and all(
            type(s) is str and re.fullmatch(r"[A-Z][A-Z0-9]{0,11}", s) for s in symbols),
            "symbols", "Cần danh sách mã canonical viết hoa")
        _require(len(set(symbols)) == len(symbols), "symbols", "Mã không được trùng")
        for field in ("start_date", "end_date"):
            try:
                day(value[field])
            except (ValueError, TypeError) as error:
                raise ContractError("INVALID_REQUEST", field, "Ngày phải có dạng YYYY-MM-DD") from error
        _require(value["start_date"] <= value["end_date"], "end_date", "Cửa sổ ngày bị đảo")
        _require(value["timeframe"] == "1d", "timeframe", "Contract mới chỉ khai báo khung ngày 1d")
        _require(value["language"] in ("vi", "en"), "language", "Ngôn ngữ phải là vi hoặc en")
        _require(type(value["repeats"]) is int and 1 <= value["repeats"] <= 3,
                 "repeats", "Repeat phải là số nguyên từ 1 đến 3")
        if value["mode"] != "backtest":
            _require(len(symbols) == 1 and value["start_date"] == value["end_date"],
                     "symbols", "Phân tích/so sánh dùng một mã và một ngày as-of")
            _require(len(value["variant_ids"]) == 1 if value["mode"] == "analyze" else len(value["variant_ids"]) >= 2,
                     "variant_ids", "Phân tích chọn một bản; so sánh chọn ít nhất hai bản")
        _object(value["models"], set(MODEL_ROLES), "models")
        for role, model in value["models"].items():
            _object(model, {"provider", "model", "options"}, "models." + role)
            _require(_token(model["provider"]) and _token(model["model"]), "models." + role, "Thiếu model/provider hợp lệ")
            options = model["options"]
            _require(type(options) is dict and {"temperature", "max_tokens"} <= set(options)
                     <= {"temperature", "max_tokens", "seed"}, "models." + role, "Options không được hỗ trợ")
            _require(type(options["temperature"]) in (float, int) and 0 <= options["temperature"] <= 2
                     and type(options["max_tokens"]) is int and 1 <= options["max_tokens"] <= 8192,
                     "models." + role, "Temperature hoặc token budget không hợp lệ")
            _require("seed" not in options or type(options["seed"]) is int and 0 <= options["seed"] <= 2**32 - 1,
                     "models." + role, "Seed không hợp lệ")
        return cls(json_bytes(value))

    def document(self) -> dict[str, Any]:
        """Consumer nhận bản sao; thay đổi globals/form sau đó không đổi request đã seal."""
        return json.loads(self._bytes)

    @property
    def sha256(self) -> str:
        """Hash gồm mã/ngày/khung/ngôn ngữ/mode/repeat/model/options/variant."""
        return digest(self.document())


def preflight(spec: ServingRequest) -> dict[str, Any]:
    """Caller thuần chỉ kiểm cấu trúc; grant phải qua Service kiểm resource/owner/key phía server."""
    request = spec.document()
    blockers = [{"code": "SERVER_PREFLIGHT_REQUIRED", "message": "Cần kiểm resource/support/model/credential tại server",
                 "resources": required_resources(request["variant_ids"])}]
    if request["language"] != "vi":
        blockers.append({"code": "LANGUAGE_NOT_RELEASED", "message": "Projection mới chưa nghiệm thu tiếng Anh"})
    return {"version": CONTRACT_VERSION, "registry_version": REGISTRY_VERSION, "status": "blocked",
            "run_enabled": False, "request_sha256": spec.sha256,
            "requested_ids": request["variant_ids"], "execution_plan": execution_order(request["variant_ids"]),
            "blockers": blockers}


@dataclass(frozen=True)
class ServingJob:
    """Định danh job đã bind snapshot/resources; tạo object không phải cấp phép thực thi."""
    _bytes: bytes

    @classmethod
    def create(cls, spec: ServingRequest, config: dict[str, Any], snapshot_sha256: str,
               owner_scope_sha256: str, *, run_id: str | None = None) -> ServingJob:
        """Config do server dựng; không nhận API key, path, grant hoặc credentials từ request."""
        _object(config, {"version", "registry_version", "runner_version", "provider_version", "source_sha256",
                         "calendar_sha256", "support_sha256", "credential_scope_sha256", "resources", "prompt_versions"}, "config")
        json_bytes(config)
        _require(config["version"] == CONFIG_VERSION and config["registry_version"] == REGISTRY_VERSION,
                 "config.version", "Version config/registry không khớp")
        _require(_token(config["runner_version"]) and _token(config["provider_version"]),
                 "config", "Thiếu version runner/provider")
        for field in ("source_sha256", "calendar_sha256", "support_sha256", "credential_scope_sha256"):
            _require(checksum(config[field]), "config." + field, "Cần SHA256 đầy đủ")
        request = spec.document()
        plan = execution_order(request["variant_ids"])
        _object(config["resources"], set(required_resources(request["variant_ids"])), "config.resources")
        for resource in config["resources"].values():
            _object(resource, {"version", "sha256"}, "config.resources")
            _require(_token(resource["version"]) and checksum(resource["sha256"]),
                     "config.resources", "Tài nguyên thiếu version/hash")
        _object(config["prompt_versions"], set(plan) | set(MODEL_ROLES[:-1]), "config.prompt_versions")
        _require(all(_token(v) for v in config["prompt_versions"].values()),
                 "config.prompt_versions", "Thiếu version prompt/projection")
        _require(checksum(snapshot_sha256) and checksum(owner_scope_sha256), "snapshot", "Thiếu snapshot/owner scope hash")
        identity = {"version": CONTRACT_VERSION, "registry_version": REGISTRY_VERSION,
                    "request": request, "config": config, "snapshot_sha256": snapshot_sha256,
                    "costs": dict(COSTS), "target": "OPEN_T1_CLOSE_T3_NET; SHORT_IS_CASH",
                    "method_profiles": {v: get_variant(v).profile for v in plan}}
        identifier = str(uuid4()) if run_id is None else run_id
        _require(type(identifier) is str and str(UUID(identifier)) == identifier, "run_id", "Run ID phải là UUID canonical")
        doc = {"run_id": identifier, "owner_scope_sha256": owner_scope_sha256,
               "config_sha256": digest(config), "identity_sha256": digest(identity),
               "cache_sha256": digest({"identity": identity, "owner_scope_sha256": owner_scope_sha256}),
               "identity": identity, "requested_ids": request["variant_ids"], "execution_plan": plan}
        return cls(json_bytes(doc))

    def document(self) -> dict[str, Any]:
        """Config public không chứa raw secret; F08 giữ credential thật ở kho server riêng."""
        return json.loads(self._bytes)


def result_document(job: ServingJob, state: str, executed_ids: list[str], progress: dict[str, Any],
                    rows: list[dict[str, Any]], error: dict[str, Any] | None = None) -> dict[str, Any]:
    """Envelope kết quả/partial có units/support; lỗi kỹ thuật không bị biến thành CASH."""
    doc = job.document()
    _require(state in JOB_STATES, "state", "Trạng thái job không hợp lệ")
    _require(type(executed_ids) is list and all(type(v) is str for v in executed_ids)
             and len(set(executed_ids)) == len(executed_ids) and set(executed_ids) <= set(doc["execution_plan"]),
             "executed_ids", "Executed IDs phải thuộc execution plan")
    _object(progress, {"points_total", "points_complete", "decision_slots_total", "decision_slots_complete", "api_attempts"}, "progress")
    _require(all(type(v) is int and v >= 0 for v in progress.values())
             and progress["points_complete"] <= progress["points_total"]
             and progress["decision_slots_complete"] <= progress["decision_slots_total"], "progress", "Tiến độ không hợp lệ")
    _require(type(rows) is list, "rows", "Rows phải là danh sách")
    seen = set()
    request = doc["identity"]["request"]
    _require(progress["decision_slots_total"] == progress["points_total"] * len(doc["execution_plan"]) * request["repeats"],
             "progress", "Tổng slot phải tính cả dependency và repeat")
    point_slots: dict[str, set[tuple[int, str]]] = {}
    for row in rows:
        _object(row, {"point_id", "symbol", "as_of_date", "repeat", "requested_id", "executed_id", "raw_prediction",
                      "final_prediction", "final_action", "fallback_reason", "bypass_reason", "support", "net_return_pct", "metric_reason"}, "rows")
        _require(row["requested_id"] in doc["execution_plan"] and row["executed_id"] in executed_ids,
                 "rows", "Row không khớp variant đã thực thi")
        allowed = {row["requested_id"]}
        method = get_variant(row["requested_id"])
        while method.fallback:
            allowed.add(method.fallback)
            method = get_variant(method.fallback)
        _require(row["executed_id"] in allowed, "rows", "Không được fallback sang phương pháp ngoài policy")
        _require(row["symbol"] in request["symbols"] and type(row["repeat"]) is int
                 and 0 <= row["repeat"] < request["repeats"], "rows", "Row ngoài support request")
        try:
            cutoff = day(row["as_of_date"])
        except (ValueError, TypeError) as exc:
            raise ContractError("INVALID_REQUEST", "rows", "Ngày row không hợp lệ") from exc
        _require(request["start_date"] <= cutoff <= request["end_date"]
                 and row["point_id"] == row["symbol"] + "-" + cutoff, "rows", "Row ngoài cửa sổ as-of")
        key = (row["point_id"], row["repeat"], row["requested_id"])
        _require(key not in seen, "rows", "Slot kết quả bị trùng")
        seen.add(key)
        point_slots.setdefault(row["point_id"], set()).add((row["repeat"], row["requested_id"]))
        _require(row["raw_prediction"] in (None, "LONG", "SHORT") and row["final_prediction"] in ("LONG", "SHORT")
                 and row["final_action"] == ("LONG" if row["final_prediction"] == "LONG" else "CASH"),
                 "rows", "Prediction/action không đúng hợp đồng kinh tế")
        for field in ("fallback_reason", "bypass_reason"):
            _require(row[field] is None or type(row[field]) is str and 0 < len(row[field]) <= 200,
                     "rows", "Lý do fallback/bypass phải là mã ngắn")
        _require(row["executed_id"] == row["requested_id"] or row["fallback_reason"] is not None,
                 "rows", "Fallback phải có lý do")
        _require(row["raw_prediction"] is not None or row["fallback_reason"] is not None or row["bypass_reason"] is not None,
                 "rows", "Thiếu raw phải ghi fallback/bypass")
        _object(row["support"], {"manifest_sha256", "status"}, "rows.support")
        _require(row["support"]["manifest_sha256"] == doc["identity"]["config"]["support_sha256"]
                 and row["support"]["status"] in ("supported", "declared_fallback"), "rows", "Support không khớp manifest job")
        _require(row["net_return_pct"] is None or type(row["net_return_pct"]) in (float, int),
                 "rows", "Metric không xác định phải là null")
        _require(request["mode"] == "backtest" or row["net_return_pct"] is None,
                 "rows", "Phân tích mới chưa có outcome; không nhận P&L tương lai")
        _require(row["final_action"] != "CASH" or row["net_return_pct"] is None or row["net_return_pct"] == 0,
                 "rows", "Giữ cash không phát sinh P&L giao dịch")
        _require(row["metric_reason"] in ("PENDING_EXIT", "NOT_EVALUATED", "MISSING_OUTCOME")
                 if row["net_return_pct"] is None else row["metric_reason"] is None,
                 "rows", "Metric NA cần lý do; metric có giá trị không dùng lý do NA")
    _require(len(rows) == progress["decision_slots_complete"], "progress", "Rows không khớp số slot hoàn tất")
    slots_per_point = len(doc["execution_plan"]) * request["repeats"]
    _require(len(point_slots) <= progress["points_total"] and progress["points_complete"] == sum(
        len(slots) == slots_per_point for slots in point_slots.values()), "progress", "Coverage point không khớp slot đã hoàn tất")
    if state == "completed":
        _require(progress["points_total"] > 0 and progress["decision_slots_total"] > 0 and
                 progress["points_complete"] == progress["points_total"] and
                 progress["decision_slots_complete"] == progress["decision_slots_total"] and error is None,
                 "state", "Chưa đủ coverage để completed")
    if error is not None:
        _object(error, {"code", "message", "retryable"}, "error")
        _require(error["code"] in ("RESOURCE_UNAVAILABLE", "SUPPORT_MISMATCH", "PROVIDER_FAILURE", "QUOTA_EXCEEDED",
                                  "UNKNOWN_ATTEMPT", "INVALID_MODEL_OUTPUT", "INTEGRITY_FAILURE", "INTERNAL_ERROR")
                 and type(error["message"]) is str and 0 < len(error["message"]) <= 200
                 and type(error["retryable"]) is bool, "error", "Lỗi cần mã và thông báo an toàn")
    _require(state not in ("failed", "unknown") or error is not None, "error", "Job lỗi phải có mã lỗi")
    _require(state != "unknown" or error["code"] == "UNKNOWN_ATTEMPT" and not error["retryable"],
             "error", "UNKNOWN cần đối soát, không tự retry")
    result = {"version": CONTRACT_VERSION, **doc, "state": state, "executed_ids": executed_ids,
              "progress": progress, "rows": rows, "error": error,
              "metric_units": {"net_return_pct": "PERCENT_PER_CYCLE"},
              "support_sha256": doc["identity"]["config"]["support_sha256"]}
    return json.loads(json_bytes(result))
