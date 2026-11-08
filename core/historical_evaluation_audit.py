"""Đối soát raw HTTP, source runtime và preview offline H04."""

from __future__ import annotations

import base64
from copy import deepcopy
import hashlib
import json
from importlib.metadata import version
from pathlib import Path
from typing import Any

from core.bayesian_memory import read_json
from core.historical_evaluation_clients import RUNTIME
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import binding, read, digest
from core.historical_evaluation_scope import PORTS

NEW_FILES = ("scope", "data", "context", "prior", "journal", "graph", "clients", "runner", "audit")
SERIALIZERS: dict[str, Any] = {}


def serializer(config: dict[str, Any]) -> Any:
    """Chỉ dùng serializer SDK, mọi thử gửi HTTP bị transport chặn tuyệt đối."""
    from langchain_groq import ChatGroq
    import httpx
    key = digest(config)
    if key not in SERIALIZERS:
        def blocked(request: httpx.Request) -> Any:
            raise AssertionError("Verifier offline không được gửi HTTP")
        client = httpx.Client(transport=httpx.MockTransport(blocked))
        SERIALIZERS[key] = ChatGroq(api_key="OFFLINE_SERIALIZER_NOT_A_CREDENTIAL", http_client=client,
            model=config["model"], temperature=config["temperature"], max_tokens=config["max_tokens"],
            max_retries=0, streaming=False, service_tier=config["service_tier"], **config["client_options"])
    return SERIALIZERS[key]


def serialized_body(llm: Any, messages: Any, schema: dict[str, Any] | None = None) -> dict[str, Any]:
    """Cùng ABI với HTTP thật, không dựng tay response_format của Groq."""
    from langchain_core.messages import HumanMessage
    if isinstance(messages, str):
        messages = [HumanMessage(content=messages)]
    converted, params = llm._create_message_dicts(messages, None)
    body = {"messages": converted, **params}
    if schema is not None:
        structured = llm.with_structured_output(schema, method="json_schema", include_raw=True)
        body["response_format"] = structured.steps[0].steps__["raw"].kwargs["response_format"]
    return body


def source_manifest(root: Path) -> dict[str, Any]:
    """Liệt kê toàn dependency runtime mới và các module pure được bind cục bộ."""
    names = {f"core/historical_evaluation_{name}.py" for name in NEW_FILES}
    from core.historical_signals import CODE_FILES
    names.update(CODE_FILES)
    names.update(f"core/{name}.py" for name in PORTS)
    names.update(("scripts/run_historical_evaluation.py", "utils/graph_util.py", "utils/color_style.py",
                  "utils/alpha_selector.py", "agents/alpha_agent.py", "agents/indicator_agent.py",
                  "agents/pattern_agent.py", "agents/trend_agent.py", "core/improvement_transport.py",
                  "core/research_invocation.py", "core/prior_stage_journal.py"))
    return {name: binding(root, name) for name in sorted(names)}


def libraries() -> dict[str, str]:
    """Pin cả thư viện vẽ/TA-Lib/SDK vì chúng ảnh hưởng ảnh và wire payload."""
    return {name: version(name) for name in ("numpy", "pandas", "torch", "scipy", "scikit-learn", "hmmlearn",
        "TA-Lib", "matplotlib", "mplfinance", "langgraph", "langchain-core", "langchain-groq", "httpx", "pydantic", "jsonschema")}


def verify_runtime(root: Path) -> None:
    """Không cấp API nếu code mới đổi nhưng manifest/release vẫn trỏ bản cũ."""
    manifest = read(root, RUNTIME, envelope=True)
    if manifest["sources"] != source_manifest(root) or manifest.get("libraries") != libraries():
        raise ValueError("Runtime H04 khác source manifest đã neo")


def http_records(book: RunBook, attempt: str, role: str) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Join UUID với năm ledger, kiểm byte response đã durable trước parse."""
    result = []
    for path in (book.directory / "usage").glob("org*.json"):
        for row in read_json(path)["requests"]:
            if row.get("checkpoint_attempt_id") != attempt:
                continue
            if row.get("run_signature") != book.signature or row.get("branch_id") != role:
                raise ValueError("HTTP khác run/branch/UUID")
            if row.get("status") == "transport_error":
                continue
            proof = row.get("historical_raw")
            if not proof:
                raise ValueError("HTTP thiếu raw response durable")
            from core.prior_run_lock import safe_path
            raw_path = safe_path(book.directory, proof["path"])
            if hashlib.sha256(raw_path.read_bytes()).hexdigest() != proof["sha256"]:
                raise ValueError("Raw HTTP khác ledger checksum")
            raw = load(raw_path)
            body = base64.b64decode(raw["body_base64"], validate=True)
            payload = json.loads(body)
            audit = row.get("improvement_audit")
            from core.historical_signals import digest as legacy_digest
            if (not audit
                    or audit["response"]["body_sha256"] != hashlib.sha256(body).hexdigest()
                    or audit["response"]["canonical_sha256"] != legacy_digest(payload)):
                raise ValueError("Raw HTTP không khớp request/response audit")
            request_audit = audit["request"]
            if request_audit["canonical_body_sha256"] != raw["request_legacy_body_sha256"]:
                raise ValueError("Request HTTP khác serializer audit legacy")
            result.append((row, payload))
    return result


def verify_decision(book: RunBook, response: dict[str, Any], branch: str, *, fixture: bool,
                    request: dict[str, Any] | None = None) -> None:
    """Parsed reply phải khớp raw provider và AIMessage đã lưu, không chỉ đúng schema."""
    if fixture:
        if response.get("fixture") is not True:
            raise ValueError("Fixture bị trộn với response thật")
        return
    if response.get("fixture"):
        raise ValueError("Không đưa fixture vào research run")
    rows = http_records(book, response["request_id"], branch)
    success = [(row, payload) for row, payload in rows if row["status"] == 200]
    if not success or len(rows) > 3:
        raise ValueError("Decision thiếu HTTP thành công hoặc vượt budget3")
    row, payload = success[-1]
    if request is not None:
        model = serializer({key: request[key] for key in ("model", "temperature", "max_tokens", "service_tier", "client_options")})
        expected = digest(serialized_body(model, request["messages"][0]["content"], request["structured"]["schema"]))
        if expected != response["expected_http_body_sha256"]:
            raise ValueError("Canonical HTTP body không tái dựng từ source hiện tại")
    proof = row["historical_raw"]
    if load(book.directory / proof["path"])["request_body_sha256"] != response["expected_http_body_sha256"]:
        raise ValueError("Decision không đúng canonical HTTP body")
    message = payload["choices"][0]["message"]
    saved = response["raw_message"][-1]["data"]
    if saved["content"] != message.get("content") or json.loads(message["content"]) != response["reply"]:
        raise ValueError("Parsed reply/raw message khác provider response")


def verify_graph(book: RunBook, role: str, slot: str, state: dict[str, Any], output: dict[str, Any],
                 config: dict[str, Any], *, fixture: bool) -> None:
    """Cold replay node từ raw provider, so báo cáo/số; không gọi mạng hoặc tin hash tự khai."""
    from agents.indicator_agent import create_indicator_agent
    from agents.pattern_agent import create_pattern_agent
    from agents.trend_agent import create_trend_agent
    from agents.alpha_agent import create_alpha_agent
    from core.prior_stage_journal import encode_output
    from utils.graph_util import TechnicalTools
    from langchain_core.messages import AIMessage
    if not book.verify_only:
        return
    doc = load(book.path(slot))
    attempt = doc["attempts"][-1]["attempt_id"]
    if fixture and role in ("pattern", "trend"):
        if "FIXTURE_ONLY" not in output[role + "_report"]:
            raise ValueError("Vision fixture không có marker cách ly")
        return
    rows = http_records(book, attempt, role) if not fixture else []
    if role in ("indicator", "full") and rows:
        raise ValueError("Node Python đã phát sinh HTTP ngoài protocol")
    success = [(row, payload) for row, payload in rows if row["status"] == 200]
    class ReplayModel:
        """Chỉ cấp lần lượt response đã lưu khi prompt/body tái dựng khớp."""
        def __init__(self) -> None:
            self.position = 0
        def invoke(self, messages: Any, *args: Any, **kwargs: Any) -> Any:
            if self.position >= len(success):
                raise ValueError("Replay graph cần response không có trong ledger")
            row, payload = success[self.position]
            models = config["signal_config"]["models"]
            model = serializer({"model": models["graph_llm_model"], "temperature": 0., "max_tokens": 960,
                                "service_tier": "on_demand", "client_options": config["client_options"]["graph"]})
            raw = load(book.directory / row["historical_raw"]["path"])
            if digest(serialized_body(model, messages)) != raw["request_body_sha256"]:
                raise ValueError("Graph HTTP body khác source/ảnh/PIT tái dựng")
            self.position += 1
            return AIMessage(content=payload["choices"][0]["message"].get("content") or "")
    replay = ReplayModel()
    nodes = {"indicator": lambda: create_indicator_agent(None, TechnicalTools()),
             "pattern": lambda: create_pattern_agent(None, replay, TechnicalTools()),
             "trend": lambda: create_trend_agent(None, replay, TechnicalTools()),
             "full": lambda: create_alpha_agent(None, True, True, strict_research_mode=True)}
    from core.research_invocation import ENABLED, RECOVERY, invocation_scope
    enabled, recovery = ENABLED.set(True), RECOVERY.set(False)
    try:
        with invocation_scope(role):
            expected = nodes[role]()(deepcopy(state))
    finally:
        ENABLED.reset(enabled); RECOVERY.reset(recovery)
    actual = encode_output({k: v for k, v in output.items() if k != "messages"})
    expected = encode_output({k: v for k, v in expected.items() if k != "messages"})
    if actual != expected or role in ("pattern", "trend") and replay.position != len(success):
        raise ValueError("Output graph không khớp raw/primitive cold replay")


def prepare(root: Path) -> dict[str, Any]:
    """Chỉ audit metadata/prefix/scaler/sentiment và freeze code; không nhãn query/LLM/fit."""
    from core.historical_evaluation_data import HistoricalData
    from core.historical_evaluation_prior import FeaturePopulation
    from core.historical_evaluation_context import ContextBank
    data = HistoricalData(root)
    population = FeaturePopulation(data)
    news = data.sentiment_audit()
    context = ContextBank(data, lambda _: False)
    preview = []
    for unit in sorted(data.inputs["grid"], key=lambda r: (r["date"], r["symbol"])):
        episode = context.build(unit["symbol"], unit["date"])
        preview.append({"id": unit["id"], "status": episode["status"], "K": episode["K"], "m": episode["m"],
                        "context_sha256": digest(episode), "ood": unit["symbol"] not in ("FPT", "MWG", "VCB", "VNM"),
                        "reasons": episode["reasons"]})
    assets = root / "outputs/historical_reevaluation/h04_assets"
    result = {"version": "historical_h04_assets_v1", "status": "OFFLINE_IMPLEMENTATION_AUDITED",
              "preview_scope": "GRID_OUTCOMES_WITHHELD_NOT_FROZEN_H07_CONTEXT",
              "contexts": preview, "sentiment": news, "scalers": population.scalers,
              "history_prefix_models_required": sorted({r["date"] for r in data.inputs["history"]}),
              "llm_calls": 0, "teacher_or_student_fit": False, "api_released": False}
    save(assets / "prepared.json", result)
    profile = runtime_profile(root, data)
    path = root / RUNTIME
    if path.exists() and load(path) != profile:
        raise ValueError("Runtime profile đã khóa khác source; cần revision trước release")
    if not path.exists():
        save(path, profile)
    return result


def runtime_profile(root: Path, data: Any) -> dict[str, Any]:
    """Dựng manifest source/thư viện độc lập với preview; không fit hay truy cập outcome."""
    return {"version": "historical_h04_runtime_v1", "status": "IMPLEMENTED_NOT_RELEASED",
               "sources": source_manifest(root), "libraries": libraries(),
               "schema_sha256": digest(data.scope.module("mt_bicl_contracts").wire_schema()),
               "old_sources_modified": False, "h03_revision": "ae5dbc6d",
               "compatibility_extensions": {
                   "v1_prefix": "EXISTING_ALLOW_SENTIMENT_FLAG_TRUE; FOUR_SIGNAL_TEMPLATE_UNCHANGED; NO_NEUTRAL_REWRITE",
                   "vendor_features": "H02_RAW_BARRIER_DATES_WITH_DONOR_OHLCV_NO_REFERENCE_FABRICATION",
                   "alpha_projection": "FIVE_NUMERIC_NAME_VALUE_SIGNAL_MASK_ROWS_BEFORE_UNCHANGED_DISTILL_CAP",
                   "numeric_phase": "CORE4_WITHHOLDS_OOD_GRID_OUTCOMES_EVEN_AFTER_OOD_PHASE_COMPLETES",
                   "universe": "EXPLICIT_NINE_SYMBOL_SCOPE_NO_MUTATION_OF_ORIGINAL_MODULES"}}


def prepare_regimes(root: Path) -> dict[str, Any]:
    """Lệnh CPU tường minh tạo historical HMM prefix; không fit teacher/student hay refit query."""
    from threadpoolctl import threadpool_limits
    from core.historical_evaluation_data import HistoricalData
    from core.historical_evaluation_runner import Regimes
    from core.regime_detector import MarketRegimeDetector, training_data_hash
    data = HistoricalData(root)
    directory = root / "outputs/historical_reevaluation/h04_assets/legacy_regimes"
    directory.mkdir(parents=True, exist_ok=True)
    dates = sorted({r["date"] for r in data.inputs["history"]})
    for i, cutoff in enumerate(dates):
        prefix = data.history.loc[data.history["Datetime"] <= cutoff].copy()
        path = directory / (cutoff + ".json")
        if path.exists():
            detector = MarketRegimeDetector.load(path, expected_training_hash=training_data_hash(prefix))
        else:
            with threadpool_limits(limits=1):
                detector = MarketRegimeDetector().fit(prefix)
            detector.save(path)
        if detector.metadata["train_end_date"] != cutoff:
            raise ValueError("HMM historical không đúng prefix")
        print(f"Historical regime prefix {i + 1}/{len(dates)} đã durable.", flush=True)
    return {"status": "PREFIX_MODELS_READY", "count": len(dates), "teacher_or_student_fit": False, "llm_calls": 0}
