"""Cold replay số U06 trên toàn102 query; không client/key, không huấn luyện hoặc query payoff."""
from __future__ import annotations

from copy import deepcopy
from contextlib import redirect_stdout
import io
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pandas as pd

from core.unified_contracts import digest
from core.unified_protocol import read
from core.unified_preflight import ASSETS, verify


def replay_numeric(root: Path) -> dict[str, Any]:
    """Tái fit9 nguồn trước test, chiếu102 alpha, tái tạo context/student/utility và mọi request."""
    from core.causal_alpha import FrozenSelector
    from core.causal_bridge import bind_snapshot
    from core.unified_contracts import SharedSnapshot
    from core.unified_preflight_assets import frames
    from core.unified_asset_providers import study_data, FrozenStudyContext, FrozenStudyBank
    from core.historical_evaluation_runner import Regimes
    from core.variant_registry import execution_order, get_variant
    from agents.alpha_agent import create_alpha_agent
    from agents.indicator_agent import create_indicator_agent
    from utils.graph_util import TechnicalTools
    checked = verify(root)
    alpha = read(root, ASSETS + "/frozen_alpha_manifest.json")
    provider = read(root, ASSETS + "/provider_manifest.json")
    sources = frames(root)
    data = study_data(root)
    original_points = read(root, "docs/plan/week12/unified_comparison_manifest.json", True)["points"]
    ids = {row["id"] for row in original_points}
    data.by_day = {key: value for key, value in data.by_day.items() if value["id"] in ids}
    bank = FrozenStudyBank(data, original_points)
    if bank.audit != provider["bank_audit"]:
        raise ValueError("Audit bank/scaler khác producer")
    contexts, selectors = {}, {}
    regimes = Regimes(data, root)
    methods = data.scope.module("unified_methods")
    for i, row in enumerate(provider["points"]):
        saved = read(root, row["path"])
        if digest(saved) != row["sha256"]:
            raise ValueError("Provider control khác manifest")
        point = saved["point"]
        symbol, cutoff, fold = point["symbol"], point["cutoff"], point["fold"]
        frame = sources[symbol]
        artifact = read(root, alpha["causal_sources"][symbol + "/" + fold]["selector"])
        if symbol not in selectors:
            selectors[symbol] = FrozenSelector(artifact, frame)
        elif selectors[symbol].sha256 != artifact["sha256"]:
            raise ValueError("Selector đã thay giữa các fold của cùng mã")
        prefix = frame.loc[frame.Datetime <= pd.Timestamp(cutoff)].copy()
        document = deepcopy(saved["snapshot"])
        embedded = document["payload"].pop("causal_alpha")
        base = SharedSnapshot.create(point, 0, document["payload"], document["provenance"])
        state = data.state(symbol, cutoff)
        with redirect_stdout(io.StringIO()):
            state.update(create_indicator_agent(None, TechnicalTools())(deepcopy(state)))
            state.update(create_alpha_agent(None, True, True, strict_research_mode=True)(deepcopy(state)))
        for field in ("pattern_report", "trend_report"):
            state[field] = document["payload"][field]
        state["alpha_factors"] = deepcopy(state["sentiment_data"]["alpha_results"])
        rebuilt = methods.snapshot_from_graph(point, 0, state, prefix.tail(600), document["provenance"]["source_sha256"], [])
        if rebuilt.document() != base.document():
            raise ValueError("Indicator/native alpha/sentiment không tái lập từ source PIT")
        rebound = bind_snapshot(base, selectors[symbol], prefix, document["provenance"]["source_sha256"])
        if rebound.document() != saved["snapshot"] or embedded != rebound.document()["payload"]["causal_alpha"]:
            raise ValueError("Alpha/native bridge không tái lập từ giá/selector")
        if fold not in contexts:
            contexts[fold] = FrozenStudyContext(data, row["frozen_before"])
        episode = contexts[fold].build(symbol, cutoff)
        variants = contexts[fold].variants(episode)
        if episode != saved["context"] or variants != saved["variants"]:
            raise ValueError("Frozen context/student/utility không khớp producer")
        if regimes.get(cutoff) != saved["regime"]:
            raise ValueError("Query HMM không tái lập")
        outputs = {}
        adapter = methods.MethodAdapters(data.protocol["inference"]["config"], bank_factory=lambda: bank,
            regime=lambda day: regimes.get(day), facts=lambda _: deepcopy(episode["advisor"]["query_facts"]),
            context_factory=lambda: SimpleNamespace(build=lambda *_: deepcopy(episode), variants=lambda _: deepcopy(variants)))
        for variant in execution_order(["original_fix", "original_common", "bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL", "Fact_Anchor"]):
            item = saved["preparations"][variant]
            dependencies = {name: outputs[name] for name in get_variant(variant).dependencies}
            prepared = adapter.prepare(variant, rebound, dependencies, 0)
            if prepared != item["prepared"]:
                raise ValueError("Retrieval/facts/prompt không tái lập từ provider thật")
            methods.validate_prepared(variant, rebound, item["prepared"], data.protocol["inference"]["config"], 0)
            actual = methods.resolve(variant, item["prepared"], item["probe_raw"], dependencies)
            if actual != item["probe_policy"]:
                raise ValueError("Control policy ABI không khớp prepared source")
            outputs[variant] = {"forecast": {"raw": item["probe_raw"]}, "policy": actual}
        print(f"Cold replay {i + 1}/102: {row['point_id']}", flush=True)
    return {"status": "PASS_U06_NUMERIC_COLD_REPLAY", "points": 102, "unique_selectors": 9,
        "scope": "PIT_ASSETS_AND_CONTROL_REQUEST_POLICY_ABI_NOT_HOSTED_PERFORMANCE",
        "manifest_sha256": checked["manifest_sha256"], "inference_http_calls": 0,
        "student_teacher_hmm_training": False, "query_canonical_payoffs_computed": False}
