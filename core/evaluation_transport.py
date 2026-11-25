"""Transport và hạch toán dành riêng cho thực nghiệm so sánh nhà cung cấp."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Callable

import httpx
from jsonschema import Draft202012Validator, ValidationError

from core.groq_pacing import request_budget
from core.historical_evaluation_journal import load
from core.serving_runtime.quota import Failed, Waiting
from core.serving_runtime.transport import Calls
from core.unified_contracts import digest, json_bytes
from core.unified_execution_transport import parsed

VISION = "qwen/qwen3.8-27b"
DECISION = "openai/gpt-oss-20b"
LUNA = "gpt-6-luna"
ENDPOINTS = {
    "groq": ("GROQ_API_KEY", "https://api.groq.com/openai/v1/chat/completions"),
    "luna": ("OPENAI_API_KEY", "https://api.openai.com/v1/chat/completions"),
}
RATES = {
    VISION: {"input": .80, "cached": .80, "cache_write": .80, "output": 4.00},
    DECISION: {"input": .075, "cached": .037, "cache_write": .075, "output": .30},
    LUNA: {"input": .10, "cached": .01, "cache_write": .125, "output": .50},
}


def openai_schema(schema: dict) -> dict:
    """Chuẩn hóa schema cho OpenAI; validator cục bộ vẫn dùng đầy đủ ràng buộc."""
    local_keywords = {"uniqueItems", "minLength", "maxLength", "const"}
    result = {key: deepcopy(value) for key, value in schema.items() if key not in local_keywords}
    if "const" in schema:
        result["enum"] = [deepcopy(schema["const"])]
    if "enum" in result and all(isinstance(value, str) for value in result["enum"]):
        result.setdefault("type", "string")
    if "properties" in schema:
        result["type"] = "object"
        result["additionalProperties"] = False
    for key in ("properties", "$defs", "definitions"):
        if key in schema:
            result[key] = {name: openai_schema(value) for name, value in schema[key].items()}
    if "items" in schema:
        result["items"] = openai_schema(schema["items"])
    if "anyOf" in schema:
        result["anyOf"] = [openai_schema(value) for value in schema["anyOf"]]
    return result


def provider_body(provider: str, body: dict, *, strict: bool = True) -> dict:
    """Đổi tham số giao thức và model, giữ nguyên messages và validator gốc."""
    if provider not in ENDPOINTS or body["model"] not in (VISION, DECISION):
        raise ValueError("Request nằm ngoài cấu hình so sánh")
    result = deepcopy(body)
    if provider == "luna":
        result.update(model=LUNA, max_completion_tokens=result.pop("max_tokens"),
                      reasoning_effort="none", service_tier="default", store=False)
        result.pop("reasoning_format", None)
        result.pop("stop", None)
        if "response_format" in result:
            config = result["response_format"]["json_schema"]
            config["strict"] = strict
            if strict:
                config["schema"] = openai_schema(config["schema"])
    return result


def token_budget(body: dict) -> int:
    """Dùng estimator chung và dự phòng thêm cho cách tính ảnh của Luna."""
    if body["model"] != LUNA:
        return request_budget(body)
    vision = "response_format" not in body
    projection = {**body, "model": VISION if vision else DECISION}
    return request_budget(projection) + (8192 if vision else 2048)


class ProviderHTTP:
    """Client một endpoint, một model family, không có retry ngoài journal."""

    def __init__(self, provider: str, key: str, *, transport: httpx.BaseTransport | None = None) -> None:
        if not key.strip():
            raise ValueError("Thiếu biến môi trường " + ENDPOINTS[provider][0])
        self.provider, (_, self.url) = provider, ENDPOINTS[provider]
        self.client = httpx.Client(
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            transport=transport if transport is not None else httpx.HTTPTransport(retries=0),
            timeout=httpx.Timeout(120, connect=15), follow_redirects=False, trust_env=False,
        )

    def send(self, body: dict) -> tuple[int, bytes, dict[str, str]]:
        """Chỉ chuyển body đã được khóa theo đúng nhà cung cấp."""
        allowed = (LUNA,) if self.provider == "luna" else (VISION, DECISION)
        if body["model"] not in allowed:
            raise ValueError("Model của request khác cấu hình endpoint")
        result = self.client.post(self.url, content=json_bytes(body))
        return result.status_code, result.content, dict(result.headers)

    def close(self) -> None:
        """Đóng client do thực nghiệm tạo."""
        self.client.close()


class EvaluationCalls:
    """Chuyển request chuẩn hóa trước khi journal ghi body thực tế."""

    def __init__(self, *args: Any, provider: str, wait: Callable[[float], None] | None = None,
                 legacy_schema: bool = False, **kwargs: Any) -> None:
        self.wire = Calls(*args, total_prompt_guard=True, token_budget=token_budget, **kwargs)
        self.provider = provider
        self.wait = wait
        self.legacy_schema = legacy_schema

    def call(self, slot: str, body: dict, attempt: str) -> tuple[Any, dict]:
        """Phát lại raw cũ hoặc chuyển slot hết lượt lỗi schema sang wire strict."""
        actual = provider_body(self.provider, body)
        if self.provider != "luna" or "response_format" not in actual:
            return self._call(slot, actual, attempt)
        if self.legacy_schema:
            _, rows = self.wire._rows(slot)
            legacy = provider_body(self.provider, body, strict=False)
            if rows and rows[0]["base_sha256"] == digest(legacy):
                try:
                    return self._call(slot, legacy, attempt)
                except Failed as error:
                    if str(error) != "ATTEMPT_CAP_EXHAUSTED" or not all(row["status"] == 200 for row in rows):
                        raise
                    slot += "/strict-schema"
        schema = body["response_format"]["json_schema"]["schema"]
        return self._call(slot, actual, attempt, validate_reply=Draft202012Validator(schema).validate)

    def _call(self, slot: str, body: dict, attempt: str, *,
              validate_reply: Callable[[Any], None] | None = None) -> tuple[Any, dict]:
        """Dùng chung retry và đầu mối chờ quota hiện có."""
        while True:
            try:
                return self.wire.call(slot, body, attempt, validate_reply=validate_reply)
            except Waiting as delay:
                if self.wait is None:
                    raise
                self.wait(delay.until)

def usage_totals(directory: Path, run_id: str) -> dict:
    """Cộng usage kể cả response lỗi schema và giữ số lượt thiếu usage."""
    grouped: dict[str, Counter] = {}
    for path in sorted((directory / "http").glob("*.json")):
        doc = load(path)
        if doc["run_id"] != run_id:
            raise ValueError("Nhật ký HTTP khác thực nghiệm")
        for row in doc["rows"]:
            model = row["body"]["model"]
            totals = grouped.setdefault(model, Counter())
            totals["attempts"] += 1
            totals["unknown"] += row["status"] == "UNKNOWN"
            totals["http_errors"] += isinstance(row["status"], int) and row["status"] != 200
            totals["schema_errors"] += 0
            if row["response"] is None:
                totals["usage_missing"] += row["status"] != "NOT_SENT"
                continue
            try:
                response = json.loads(row["response"])
            except (TypeError, ValueError):
                response = {}
            if row["status"] == 200 and "response_format" in row["body"]:
                try:
                    parsed(row["body"], response)
                except (KeyError, IndexError, TypeError, ValueError, ValidationError):
                    totals["schema_errors"] += 1
                else:
                    totals["schema_errors"] += bool(row.get("schema_error"))
            usage = response.get("usage") or {}
            prompt, output = usage.get("prompt_tokens"), usage.get("completion_tokens")
            if not all(type(value) is int and value >= 0 for value in (prompt, output)):
                totals["usage_missing"] += 1
                continue
            details = usage.get("prompt_tokens_details") or {}
            cached, writes = details.get("cached_tokens", 0), details.get("cache_write_tokens", 0)
            if not all(type(value) is int and value >= 0 for value in (cached, writes)) or cached + writes > prompt:
                raise ValueError("Usage cache không khớp số token đầu vào")
            rate = RATES[model]
            totals.update(prompt_tokens=prompt, completion_tokens=output, cached_tokens=cached, cache_write_tokens=writes)
            totals["estimated_cost_usd"] += ((prompt-cached-writes)*rate["input"] + cached*rate["cached"]
                                               + writes*rate["cache_write"] + output*rate["output"])/1_000_000
    combined = Counter()
    for totals in grouped.values():
        combined.update(totals)
    fields = ("attempts", "unknown", "http_errors", "schema_errors", "usage_missing", "prompt_tokens",
              "completion_tokens", "cached_tokens", "cache_write_tokens", "estimated_cost_usd")
    return {**{key: combined[key] for key in fields}, "by_model": {k: dict(v) for k, v in grouped.items()},
            "rates_usd_per_million": {k: RATES[k] for k in grouped}}
