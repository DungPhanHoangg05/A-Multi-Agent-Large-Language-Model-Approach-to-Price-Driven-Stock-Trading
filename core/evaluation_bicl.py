"""BICL lịch sử và follow-up dùng chung DAG, giữ tài nguyên và guard của từng đợt."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
from hashlib import sha256
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import Any

from agents.indicator_agent import create_indicator_agent
from core.bayesian_memory import atomic_write_json, is_bullish
from core.evaluation_component import MODELS
from core.evaluation_transport import VISION
from core.finalize_bank_resources import CONTRACT, mature_cycles
from core.finalize_bank_signals import point_input
from core.finalize_serving_profile import method_profile
from core.finalize_serving_provider import FinalizedProvider
from core.finalize_serving_resources import FinalizedResources
from core.historical_signals import report_signal
from core.research_invocation import ENABLED, invocation_scope
from core.serving_runtime.providers import VisionProxy
from core.serving_runtime.resources import default_models
from core.unified_contracts import SharedSnapshot, digest
from core.unified_execution import raw_record
from core.unified_execution_providers import StudyProviders
from core.unified_execution_transport import body_for
from core.unified_protocol import CORE4, MANIFEST, git_blob, ordered_branches, read
from core.unified_preflight_assets import ASSETS
from core.variant_registry import get_variant
from utils.graph_util import TechnicalTools

HISTORY = "a034c8bb39f77fb47c9387937c590b762e7711f6"
LOCKED_BUDGET = "docs/plan/week12/finalize_api_budget_v1.json"
BANK = "data_manager/regime_memory_store.json"
BANK_MANIFEST = "data_manager/regime_memory_store.manifest.json"
BANK_AUDIT = "docs/plan/week2/memory_bank_audit.json"
BANK_RELEASE = "f743b94684dc7dbfc5e7eb04e6aaeb0a1930917b"
BANK_FIELDS = {"pattern": ("Thiên lệch dự báo", "Directional bias"),
               "trend": ("Hướng xu hướng", "Trend direction")}
VARIANTS = tuple(ordered_branches(0))


def archived_payload(root: Path, path: str) -> dict:
    """Đọc đúng envelope U08 hoặc FIN09 đã lưu tại commit nguồn."""
    envelope = json.loads(git_blob(root, HISTORY, path))
    if envelope["sha256"] != digest(envelope["payload"]):
        raise ValueError("Envelope lịch sử lệch checksum")
    return envelope["payload"]


def initial_points(cohort: list[dict]) -> list[dict]:
    """Ánh xạ ID của manifest U05 sang schema point dùng trong U08."""
    return [{"id": p["runner_point_id"], "symbol": p["symbol"], "cutoff": p["date"],
             "fold": p["fold"], "quality": "U07_CONTROL_NOT_MARKET_FORECAST"} for p in cohort]


class FormatVision(VisionProxy):
    """Cấp slot bền vững cho lượt sửa định dạng thị giác của cùng node."""

    def __init__(self, calls: Any, slot: str, attempt: str, model: dict) -> None:
        super().__init__(calls, slot, attempt, model)
        self.index = 0
        self.original = slot

    def invoke(self, messages: Any) -> Any:
        """Tiếp tục đúng thứ tự request khi node được tái chạy sau checkpoint."""
        self.slot = self.original if self.index == 0 else f"{self.original}/format-{self.index}"
        self.index += 1
        return super().invoke(messages)


class FollowupProvider(FinalizedProvider):
    """Giữ đúng chế độ nghiên cứu FIN11 và dùng OHLCV cho khóa truy xuất."""

    presentation_enabled = False

    def vision_proxy(self, role: str, calls: Any, slot: str, attempt: str, model: dict) -> FormatVision:
        """Gọi vision theo cùng ABI FIN11, lưu cả lượt sửa định dạng."""
        return FormatVision(calls, slot, attempt, model)


class InitialVision:
    """Thích nghi chữ ký U08 với client một cấu hình và sửa định dạng cục bộ."""

    def __init__(self, calls: Any) -> None:
        self.calls = calls
        self.indexes: dict[tuple[str, str], int] = {}

    def call(self, slot: str, org: int, body: dict, attempt: str) -> tuple[Any, dict]:
        """Tiến điểm gọi sau khi raw đã hợp lệ, giữ thứ tự qua lần retry."""
        key = (slot, attempt)
        index = self.indexes.get(key, 0)
        current = slot if index == 0 else f"{slot}/format-{index}"
        result = self.calls.call(current, body, attempt)
        self.indexes[key] = index + 1
        return result


def bank_records(root: Path) -> list[dict]:
    """Giữ đủ 852 episode và đối chiếu bytes với manifest lịch sử."""
    raw = (root / BANK).read_bytes()
    rows = json.loads(raw)
    if len(rows) != 852 or sha256(raw).hexdigest() != read(root, BANK_MANIFEST)["bank_sha256"]:
        raise ValueError("Bank lịch sử không khớp manifest 852 chu kỳ")
    return rows


def refresh_bank(root: Path, book: Any, calls: Any, rows: list[dict], points: list[dict]) -> dict[str, dict]:
    """Chỉ gửi OHLCV đã cắt theo episode, giữ nhãn và các nguồn số tách biệt."""
    from core.execution_prices import load_verified_execution_data
    if not rows:
        return {}
    reserved = {p["symbol"] + "-" + p["cutoff"] for p in points}
    mature_cycles(rows, reserved, min(p["cutoff"] for p in points))
    pricing = root / ASSETS / "compatibility/execution_prices"
    frames = {symbol: load_verified_execution_data(pricing, symbol)[0] for symbol in {r["symbol"] for r in rows}}
    options = read(root, BANK_MANIFEST)["models"]
    model = {"model": options["graph_llm_model"], "options": {"temperature": options["graph_llm_temperature"],
                                                              "max_tokens": options["graph_llm_max_tokens"]}}
    if model["model"] != VISION:
        raise ValueError("Model vision khác cấu hình kho lịch sử")
    source = "utils/static_util.py"
    raw_renderer = git_blob(root, BANK_RELEASE, source)
    renderer = ModuleType("evaluation_historical_chart")
    renderer.__file__ = str(root / source)
    exec(compile(raw_renderer, renderer.__file__, "exec"), renderer.__dict__)
    renderer_sha = sha256(raw_renderer).hexdigest()
    indicator = create_indicator_agent(None, TechnicalTools())
    signals = {}
    for index, row in enumerate(rows, 1):
        cutoff = row["as_of_date"]
        _, state = point_input(row["symbol"], cutoff, frames[row["symbol"]])
        identifier = row["episode_id"].replace(":", "-")

        def episode(_: str) -> dict:
            with redirect_stdout(io.StringIO()):
                state.update(indicator(deepcopy(state)))
            outputs = {}
            for role, factory in MODELS:
                render = renderer.generate_kline_image if role == "pattern" else renderer.generate_trend_image
                slot = f"bank/{identifier}/{role}"
                image = book.execute("render/" + slot, {"window_sha256": digest(state["kline_data"]), "renderer_sha256": renderer_sha},
                                     lambda _: render(deepcopy(state["kline_data"]), write_artifacts=False))

                def run(attempt: str) -> dict:
                    proxy = FormatVision(calls, slot, attempt, model)
                    token = ENABLED.set(True)
                    try:
                        with invocation_scope(role), redirect_stdout(io.StringIO()):
                            result = factory(None, proxy, TechnicalTools())(deepcopy(state) | image)
                    finally:
                        ENABLED.reset(token)
                    report = result[role + "_report"]
                    if not proxy.index:
                        raise ValueError("Episode thiếu lượt vision")
                    return {"report": report, "signal": report_signal(report, BANK_FIELDS[role])}

                result = book.execute(slot, {"state_sha256": digest({k: v for k, v in state.items() if k != "messages"}),
                                             "image_sha256": digest(image)}, run)
                state[role + "_report"] = result["report"]
                outputs[role] = result["signal"]
            return outputs

        signals[row["episode_id"]] = book.execute("bank/" + identifier,
            {"symbol": row["symbol"], "cutoff": cutoff, "window_sha256": digest(state["kline_data"])}, episode)
        if index % 25 == 0 or index == len(rows):
            print(f"Tín hiệu kho lịch sử {index}/{len(rows)}", flush=True)
    return signals


def bind_bank(provider: StudyProviders, directory: Path, signals: dict[str, dict]) -> None:
    """Xác minh bank Luna và ràng buộc lại chỉ mục mà không fit scaler."""
    bank = provider.bank
    original = bank.base.records
    if set(signals) != {row["episode_id"] for row in original}:
        raise ValueError("Chưa đủ 852 cặp tín hiệu Luna đã kiểm tra")
    rows = []
    for row in original:
        vision = signals[row["episode_id"]]
        if set(vision) != set(BANK_FIELDS):
            raise ValueError("Kho Luna đổi tín hiệu ngoài Pattern/Trend")
        outcome = {**row["outcome"], "was_bull_trap": (
            row["outcome"]["actual_direction"] == "DOWN" and any(is_bullish(value) for value in vision.values()))}
        rows.append({**row, "agent_signals": {**row["agent_signals"], **vision}, "outcome": outcome})
    path = directory / "bank" / "records.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = read(provider.root, BANK_MANIFEST)
    audit = read(provider.root, BANK_AUDIT)
    economics = {key: manifest[key] for key in ("format_version", "completed", "remaining", "by_symbol", "by_regime", "by_year")}
    factory = bank.scope.module("bayesian_retriever").BayesianPriorRetriever
    with TemporaryDirectory(dir=path.parent) as folder:
        candidate = Path(folder) / path.name
        atomic_write_json(candidate, rows)
        binding = {"bank_sha256": sha256(candidate.read_bytes()).hexdigest(), "run_signature": digest(signals)}
        manifest_doc = {**economics, **binding, "parent_bank_sha256": manifest["bank_sha256"]}
        audit_doc = {**economics, **binding, "status": "PASS", "schema_sha256": audit["schema_sha256"]}
        manifest_path, audit_path = candidate.with_name("manifest.json"), candidate.with_name("validation.json")
        atomic_write_json(manifest_path, manifest_doc)
        atomic_write_json(audit_path, audit_doc)
        retriever = factory(bank_path=candidate, manifest_path=manifest_path, audit_path=audit_path)
    payload = bank.index.payload
    bank_provenance = payload["provenance"]["bank"]
    if bank_provenance["bank_sha256"] != manifest["bank_sha256"]:
        raise ValueError("Index giá không thuộc kho gốc đã khóa")
    bank_provenance["bank_sha256"] = retriever._bank_sha256
    index_module = bank.scope.module("price_feature_index")
    # Giữ lớp TransferIndex để query vẫn dùng chuỗi donor và scaler đã khóa.
    index = type(bank.index)(payload, _verified=index_module._VERIFIED)
    bank.scope.module("prior_price_similarity")._bind_index(retriever, index)
    selector = type(bank.selector)(index, bank.data.calendar)
    atomic_write_json(path, rows)
    atomic_write_json(path.with_name("manifest.json"), manifest_doc)
    atomic_write_json(path.with_name("validation.json"), audit_doc)
    bank.retriever, bank.index, bank.selector = retriever, index, selector
    bank.base.retriever, bank.base.records = retriever, rows
    bank.audit["index_identity"] = index.identity


class BiclStudy:
    """Tạo cùng grid tám phương pháp, chỉ mở outcome ngoài vòng thu sau barrier."""

    def __init__(self, root: Path, study: str) -> None:
        self.root, self.study = root, study
        self.followup = study == "followup"
        if self.followup:
            self.contract = read(root, CONTRACT, True)
            self.points = [{**p, "quality": "FINALIZE_RESEARCH_CONTROL_ONLY"} for p in self.contract["domain"]["primary_points"]]
            self.source_sha256 = digest(self.contract)
        else:
            manifest = archived_payload(root, MANIFEST)
            self.cohort = manifest["points"]
            self.points = initial_points(self.cohort)
            self.source_sha256 = digest(manifest)
        if len(self.points) != 102 or len({p["id"] for p in self.points}) != 102:
            raise ValueError("BICL cần đủ 102 điểm đã dự trữ")
        self.ordinals = {p["id"]: index for index, p in enumerate(self.points)}

    def call_counts(self, points: list[dict]) -> dict[str, int]:
        """Giữ trần cho prior/MT có điều kiện, không suy HTTP từ số forecasts."""
        result = {"pattern": len(points), "trend": len(points)}
        if self.followup:
            chosen = {p["id"] for p in points}
            ledger = archived_payload(self.root, LOCKED_BUDGET)
            from collections import Counter
            roles = Counter(row["role"] for row in ledger["slots"] if row["phase"] == "RESEARCH"
                            and row["slot"].split("/")[1] in chosen and row["state"] != "BYPASS")
            return result | {method: roles[method] for method in VARIANTS}
        supported = sum(p["symbol"] in CORE4 for p in points) * 3
        return result | {method: supported if method in ("bayesian_v1", "C2", "A_tp_pool", "B_semantic") else len(points)*3
                         for method in VARIANTS}

    def provider(self, calls: Any) -> Any:
        """Chỉ dựng tài nguyên của đợt hiện tại, không fit lại Alpha/HMM/teacher/student."""
        if self.followup:
            resources = FinalizedResources(self.root)
            resources.verify()
            return FollowupProvider(resources, self.points, default_models(), list(VARIANTS), preview=False)
        return StudyProviders(self.root, InitialVision(calls), cohort=self.cohort)

    def run_point(self, book: Any, provider: Any, point: dict, calls: Any) -> dict:
        """Ghép mọi biến thể/repeat với snapshot và đúng dependency của lần đó."""
        identifier = point["id"]
        ordinal = self.ordinals[identifier]

        def shared(_: str) -> dict:
            with redirect_stdout(io.StringIO()):
                if self.followup:
                    provider.validate_point(point)
                    return provider.shared(book, deepcopy(point), calls)
                provider.calls.indexes.clear()
                return provider.shared(book, deepcopy(point), 1)

        doc = book.execute("shared/" + identifier, {"point": point}, shared)
        if doc["point"] != point or doc["realization"] != 0:
            raise ValueError("Snapshot sai point hoặc realization")
        snapshot = SharedSnapshot.create(point, 0, doc["payload"], doc["provenance"])
        records, prepared_by_slot = [], {}
        for repeat in range(3):
            outputs: dict[str, dict] = {}
            for variant in ordered_branches(ordinal*3+repeat):
                slot = f"forecast/{identifier}/u0/r{repeat}/{variant}"
                deps = {key: deepcopy(outputs[key]) for key in get_variant(variant).dependencies}
                inputs = {"shared_sha256": snapshot.sha256, "dependency_hashes": {key: digest(v) for key, v in deps.items()}}
                prepared = book.execute("prepare/" + slot, inputs,
                                        lambda _: provider.prepare(variant, snapshot, deps, repeat))
                prepared_by_slot[slot] = prepared
                if self.followup:
                    provider.validate_bound(variant, snapshot, deps, repeat, prepared)
                else:
                    provider.validate(variant, snapshot, prepared, repeat)

                def record(attempt: str) -> dict:
                    request = prepared["request"]
                    raw = None
                    if request is not None:
                        reply, wire = calls.call(slot, body_for(request), attempt)
                        raw = raw_record(request, wire, reply)
                    if self.followup:
                        policy = provider.resolve_bound(variant, snapshot, deps, repeat, prepared, raw)
                    else:
                        policy = provider.resolve(variant, prepared, raw, deps)
                    return {"forecast": {**inputs, "point_id": identifier, "variant": variant, "repeat": repeat,
                            "realization": 0, "profile": method_profile(variant) if self.followup else get_variant(variant).profile,
                            "request_sha256": digest(request) if request is not None else None, "raw": raw},
                            "policy": policy}

                result = book.execute(slot, {**inputs, "prepared": prepared}, record)
                records.append(result)
                outputs[variant] = result
        return {"records": records, "prepared": prepared_by_slot}
