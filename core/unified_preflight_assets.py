"""Chuẩn bị assets U06 có version; giữ query test ngoài mọi phép fit."""
from __future__ import annotations

from copy import deepcopy
import io
import json
from pathlib import Path
from typing import Any

import pandas as pd

from core.causal_alpha import FrozenSelector, fit_selector, frame_document, validated_frame
from core.unified_contracts import digest, json_bytes
from core.unified_protocol import BANK, PRICE, READINESS, read

ASSETS = "outputs/unified_integration/u06_assets_v2"
PROTOCOL_V2 = "docs/plan/week12/unified_comparison_protocol_v2.json"


def schedule(frame: pd.DataFrame, first: int, last: int) -> dict[str, str]:
    """Train từ index319; validation60 cycle/180 phiên, embargo đủ ba phiên."""
    if type(first) is not int or type(last) is not int or last != first + 57 or first < 686:
        raise ValueError("Không đủ lịch cho split causal đã đăng ký")
    days = frame.Datetime.dt.strftime("%Y-%m-%d").tolist()
    indices = (319, first - 187, first - 183, first - 4, first, last)
    return dict(zip(("train_start", "train_end", "validation_start", "validation_end", "test_start", "test_end"),
                    (days[i] for i in indices)))


def frames(root: Path) -> dict[str, pd.DataFrame]:
    """Giữ nguyên float64 và suffix donor; chỉ đổi tên date thành Datetime."""
    metadata = read(root, PRICE + "manifest.json")
    offsets = read(root, READINESS)["price_views"]
    result = {}
    for row in metadata["symbols"]:
        symbol = row["symbol"]
        frame = pd.read_csv(root / PRICE / row["path"])
        frame = frame.iloc[offsets[symbol]["excluded_prefix_rows"]:].reset_index(drop=True)
        frame = frame.rename(columns={"date": "Datetime"})
        result[symbol] = validated_frame(frame)
    return result


def write_new(path: Path, raw: bytes) -> None:
    """Resume chỉ nhận byte trùng; không sửa artifact đã tạo hoặc receipt cũ."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != raw:
            raise ValueError("Artifact U06 đã tồn tại nhưng khác byte: " + path.name)
    else:
        with path.open("xb") as handle:
            handle.write(raw)


def frozen_alpha_assets(root: Path) -> dict[str, Any]:
    """Khóa trước anchor đầu từng mã; mọi fold dùng chung fit để không đọc nhãn test cũ."""
    data = frames(root)
    scopes = read(root, BANK)["schedule"]
    fits: dict[str, Any] = {}
    bindings, summaries = {}, []
    for symbol, frame in data.items():
        write_new(root / ASSETS / "prices" / (symbol + ".json"), json_bytes(frame_document(frame)))
    for scope in scopes:
        symbol, fold = scope["symbol"], scope["fold"]
        frame = data[symbol]
        if symbol not in fits:
            matching = [s for s in scopes if s["symbol"] == symbol]
            earliest = min(s["test"][0] for s in matching)
            latest = max(s["test"][1] for s in matching)
            split = schedule(frame, earliest, earliest + 57)
            split["test_end"] = str(frame.Datetime.iloc[latest].date())
            fits[symbol] = fit_selector(frame, split)
        artifact = fits[symbol]
        path = ASSETS + "/frozen_selectors/" + symbol + "_" + fold + ".json"
        write_new(root / path, json_bytes(artifact))
        selector = FrozenSelector(artifact, frame)
        queries = []
        for index in scope["test"]:
            cutoff = str(frame.Datetime.iloc[index].date())
            projection = selector.predict(frame.iloc[:index + 1].copy(), cutoff)
            projection_path = ASSETS + "/frozen_alpha/" + symbol + "-" + cutoff + ".json"
            write_new(root / projection_path, json_bytes(projection))
            queries.append({"point_id": symbol + "-" + cutoff, "projection": projection_path,
                            "projection_sha256": projection["projection_sha256"]})
        bindings[symbol + "/" + fold] = {"prices": ASSETS + "/prices/" + symbol + ".json", "selector": path}
        summaries.append({"symbol": symbol, "fold": fold, "schedule": artifact["payload"]["schedule"],
            "selector_sha256": artifact["sha256"], "train_cycles": len(artifact["payload"]["train_dates"]),
            "validation_common_cycles": len(artifact["payload"]["validation_dates"]), "queries": queries})
        print(f"Đã xác minh selector holdout {len(summaries)}/51: {symbol}/{fold}", flush=True)
    result = {"version": "unified_frozen_alpha_assets_v2", "causal_sources": bindings, "scopes": summaries,
        "selector_bindings": len(summaries), "unique_fitted_selectors": len(fits), "query_count": sum(len(s["queries"]) for s in summaries),
        "numeric_selector_fit": True, "student_teacher_hmm_fit": False, "query_outcomes_computed": False,
        "memory_rule": "FIT_BEFORE_EARLIEST_TEST_PER_SYMBOL_AND_REUSE_ACROSS_ALL_FOLDS"}
    write_new(root / ASSETS / "frozen_alpha_manifest.json", json_bytes(result))
    return result


def provider_assets(root: Path) -> dict[str, Any]:
    """Kiểm tất cả102 nguồn/nhánh trên control không LLM; không seal thành forecast thị trường."""
    from contextlib import redirect_stdout
    import hashlib
    from types import SimpleNamespace
    from uuid import uuid5, NAMESPACE_URL
    from agents.alpha_agent import create_alpha_agent
    from agents.indicator_agent import create_indicator_agent
    from utils.graph_util import TechnicalTools
    from core.causal_bridge import bind_snapshot
    from core.historical_evaluation_runner import Regimes, FixtureClients
    from core.unified_asset_providers import study_data, FrozenStudyContext, FrozenStudyBank
    from core.unified_protocol import MANIFEST, execution_order
    from core.free_pilot_runtime import reserve
    data = study_data(root)
    points = read(root, MANIFEST, True)["points"]
    ids = {row["id"] for row in points}
    data.by_day = {key: row for key, row in data.by_day.items() if row["id"] in ids}
    bank = FrozenStudyBank(data, points)
    regimes = Regimes(data, root)
    contexts: dict[str, Any] = {}
    alpha = read(root, ASSETS + "/frozen_alpha_manifest.json")
    selectors: dict[str, Any] = {}
    canonical_prices = frames(root)
    methods_module = data.scope.module("unified_methods")
    fixture = FixtureClients()
    records, max_reserve, max_chars = [], 0, 0
    for i, point in enumerate(points):
        symbol, cutoff, fold = point["symbol"], point["date"], point["fold"]
        first = min(row["date"] for row in points if row["fold"] == fold)
        if fold not in contexts:
            contexts[fold] = FrozenStudyContext(data, first)
        context = contexts[fold]
        episode = context.build(symbol, cutoff)
        variants = context.variants(episode)
        selected = [row for task in episode["prior"] for row in task["observations"]] + episode["target"]
        if any(row["episode_id"] in {p["runner_point_id"] for p in points} or row["exit_date"] >= first for row in selected):
            raise ValueError("Context đọc nhãn cohort hoặc vượt frozen fold")
        packet = episode["advisor"]["query_facts"]
        prefix = canonical_prices[symbol].loc[canonical_prices[symbol].Datetime <= pd.Timestamp(cutoff)].copy()
        state = data.state(symbol, cutoff)
        with redirect_stdout(io.StringIO()):
            state.update(create_indicator_agent(None, TechnicalTools())(deepcopy(state)))
            state.update(create_alpha_agent(None, True, True, strict_research_mode=True)(deepcopy(state)))
        state.update(pattern_report="CONTROL_ONLY: không phải dự báo LLM.\n**Thiên lệch dự báo:** BULLISH",
                     trend_report="CONTROL_ONLY: không phải dự báo LLM.\n**Hướng xu hướng:** BULLISH")
        state["alpha_factors"] = deepcopy(state["sentiment_data"]["alpha_results"])
        runner_point = {"id": point["runner_point_id"], "symbol": symbol, "cutoff": cutoff,
                        "fold": fold, "quality": "PREFLIGHT_CONTROL_NOT_MARKET_FORECAST"}
        paths = alpha["causal_sources"][symbol + "/" + fold]
        price_sha = hashlib.sha256((root / paths["prices"]).read_bytes()).hexdigest()
        base = methods_module.snapshot_from_graph(runner_point, 0, state, prefix.tail(600), price_sha, [])
        artifact = read(root, paths["selector"])
        if artifact["sha256"] not in selectors:
            selectors[artifact["sha256"]] = FrozenSelector(artifact, canonical_prices[symbol])
        snapshot = bind_snapshot(base, selectors[artifact["sha256"]], prefix, price_sha)
        frozen_projection = read(root, ASSETS + "/frozen_alpha/" + point["runner_point_id"] + ".json")
        if snapshot.document()["payload"]["causal_alpha"]["projection"] != frozen_projection:
            raise ValueError("Projection khác selector/giá đã khóa")
        adapter = methods_module.MethodAdapters(data.protocol["inference"]["config"], bank_factory=lambda: bank,
            regime=lambda day: regimes.get(day), facts=lambda _: deepcopy(packet),
            context_factory=lambda: SimpleNamespace(build=lambda *_: deepcopy(episode), variants=lambda _: deepcopy(variants)))
        outputs, preparation_records = {}, {}
        for variant in execution_order(read(root, PROTOCOL_V2)["variants"]):
            deps = {key: outputs[key] for key in __import__("core.variant_registry", fromlist=["get_variant"]).get_variant(variant).dependencies}
            prepared = adapter.prepare(variant, snapshot, deps, 0)
            methods_module.validate_prepared(variant, snapshot, prepared, adapter.protocol["decision"], 0)
            request = prepared["request"]
            raw = None
            tokens = 0
            if request is not None:
                tokens = reserve(request)
                max_reserve = max(max_reserve, tokens)
                max_chars = max(max_chars, len(request["messages"][0]["content"]))
                identifier = str(uuid5(NAMESPACE_URL, "U06_CONTROL_ONLY|" + point["id"] + "|" + variant))
                raw = fixture.decision(1, request, identifier, variant)
                raw["source_request_id"] = identifier
            policy = methods_module.resolve(variant, prepared, raw, deps)
            outputs[variant] = {"forecast": {"raw": raw}, "policy": policy}
            preparation_records[variant] = {"prepared": prepared, "probe_raw": raw,
                "probe_policy": policy, "reserve_tokens": tokens,
                "scope": "CONTROL_REQUEST_ABI_ONLY_NOT_FORECAST_OR_EFFECT_ESTIMATE"}
        if max_reserve > 8000:
            raise ValueError("Control payload vượt 8.000 TPM; không hạ cap ngầm")
        original = adapter.prepare("original_fix", base, {}, 0)["request"]
        if original != preparation_records["original_fix"]["prepared"]["request"]:
            raise ValueError("Bridge làm đổi native request")
        record = {"point": runner_point, "snapshot": snapshot.document(), "context": episode,
            "variants": variants, "preparations": preparation_records,
            "regime": regimes.get(cutoff), "native_request_unchanged": True,
            "scope": "OFFLINE_PREFLIGHT_CONTROL_ONLY_NO_MARKET_FORECAST_OR_QUERY_OUTCOME"}
        path = ASSETS + "/providers/" + point["runner_point_id"] + ".json"
        write_new(root / path, json_bytes(record))
        records.append({"point_id": point["runner_point_id"], "path": path, "sha256": digest(record),
            "K": episode["K"], "m": episode["m"], "mt_eligible": variants["branches"]["MT_BICL"]["eligible"],
            "mt_reason": variants["branches"]["MT_BICL"]["reason"],
            "frozen_before": first, "selected_max_exit": max((r["exit_date"] for r in selected), default=None),
            "prior_fallbacks": {v: preparation_records[v]["prepared"]["trace"]["fallback"]
                                for v in ("bayesian_v1", "C2", "A_tp_pool", "B_semantic")}})
        print(f"Đã kiểm provider {i + 1}/102: {point['runner_point_id']}", flush=True)
    result = {"version": "unified_provider_assets_v2", "points": records,
        "bank_audit": bank.audit, "scope_sources": data.scope.provenance, "bank_scope_sources": bank.scope.provenance,
        "max_control_prompt_chars": max_chars, "max_control_request_reserve": max_reserve,
        "query_labels_computed": False, "teacher_student_hmm_training": False,
        "inference_http_calls": 0, "control_only": True}
    write_new(root / ASSETS / "provider_manifest.json", json_bytes(result))
    return result


def vision_probe(root: Path) -> dict[str, Any]:
    """Dựng hai body vision từ graph/ảnh thật, transport mock; không forecast hoặc gọi API."""
    from contextlib import redirect_stdout
    from tempfile import TemporaryDirectory
    from core.historical_evaluation_audit import serializer, serialized_body
    from core.historical_evaluation_graph import GraphProvider
    from core.historical_evaluation_journal import RunBook
    from core.historical_live_smoke import ProbeClients
    from core.unified_asset_providers import study_data
    from core.groq_pacing import request_budget
    data = study_data(root)
    bodies = []
    class Probe(ProbeClients):
        """Quan sát đúng body SDK; phản hồi có marker control từ primitive đã kiểm."""
        def invoke(self, messages: Any, *args: Any, **kwargs: Any) -> Any:
            config = self.config
            llm = serializer({"model": config["signal_config"]["models"]["graph_llm_model"], "temperature": 0.,
                "max_tokens": 960, "service_tier": "on_demand", "client_options": config["client_options"]["graph"]})
            bodies.append(serialized_body(llm, messages))
            return super().invoke(messages, *args, **kwargs)
    probe = Probe(data.protocol["inference"]["config"])
    with TemporaryDirectory(prefix="unified-vision-control-") as folder, redirect_stdout(io.StringIO()):
        book = RunBook(Path(folder), {"scope": "U06_VISION_BODY_CONTROL_NO_FORECAST"})
        GraphProvider(data, probe).shared(book, "CMG", "2023-07-03", 0, 1)
    if len(bodies) != 2 or len(probe.reserves) != 2:
        raise ValueError("Call graph không có đúng hai vision request")
    result = {"version": "unified_vision_probe_v2", "scope": "SDK_BODY_PROBE_NO_INFERENCE",
        "bodies": bodies, "reserves": [request_budget(body) for body in bodies],
        "sdk_body_sha256": [digest(body) for body in bodies], "metadata_only": True,
        "inference_http_calls": 0, "images": "REAL_DONOR_RENDERER_ON_PINNED_PREFIX"}
    write_new(root / ASSETS / "vision_probe.json", json_bytes(result))
    return result


def news_assets(root: Path) -> dict[str, Any]:
    """Đối soát availability/tối thiểu3 bài với từng snapshot; không chứng nhận nội dung PIT."""
    from core.unified_asset_providers import study_data
    data = study_data(root)
    providers = read(root, ASSETS + "/provider_manifest.json")
    records = []
    for row in providers["points"]:
        point = row["point_id"]
        symbol, cutoff = point.split("-", 1)
        expected, _ = data.news.get_sentiment_at(symbol, cutoff)
        actual = read(root, row["path"])["snapshot"]["payload"]["sentiment_data"]
        for key in ("main_sentiment", "verified_article_count", "is_unavailable"):
            if actual[key] != expected[key]:
                raise ValueError("Sentiment snapshot khác nguồn scores/PIT")
        end = pd.Timestamp(cutoff) + pd.Timedelta(hours=23, minutes=59, seconds=59)
        visible = []
        for article in data.news.articles.get(symbol, []):
            if not article.get("date_parsed"):
                continue
            published = pd.Timestamp(article["date_parsed"])
            minimum = published.normalize() + pd.Timedelta(days=1)
            available = pd.Timestamp(article.get("available_at") or minimum)
            if available.tzinfo is not None:
                available = available.tz_convert("Asia/Ho_Chi_Minh").tz_localize(None)
            if available < minimum:
                raise ValueError("Tin khả dụng trước policy date-only")
            if end - pd.Timedelta(days=90) <= available <= end and published <= end:
                visible.append({"article_sha256": digest(article), "published": published.isoformat(),
                    "available_at": available.isoformat(), "scorer": article["scorer"]})
        if len(visible) != expected["verified_article_count"]:
            raise ValueError("Count availability không khớp sentiment source")
        records.append({"point_id": point, "visible_articles": visible,
                        "unavailable": expected["is_unavailable"], "mean_score": expected["main_sentiment"]["avg_score"]})
    result = {"version": "unified_news_availability_v2", "points": records,
              "date_only_policy": "NEXT_CALENDAR_DAY", "undated": "EXCLUDED",
              "minimum_scored_articles": 3, "content_pit_certified": False}
    write_new(root / ASSETS / "news_manifest.json", json_bytes(result))
    return result
