"""Fixture causal theo lịch synthetic; không dùng market outcomes hoặc student weights thật."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, uuid5

import pandas as pd

from core.causal_alpha import fit_selector, frame_document
from core.causal_bridge import CausalSources
from core.revision_alpha_contract import synthetic_frame
from core.unified_contracts import SharedSnapshot, digest, json_bytes
from core.unified_experiment import make_record, outcome_from_frame, slot_id
from core.unified_methods import snapshot_from_graph, validate_prepared
from core.variant_registry import VARIANTS, execution_order
from test_unified_experiment import UnifiedFixture
from mt_bicl_support import original, reply


def source_frame() -> pd.DataFrame:
    """1300 phiên đủ train/validation/test và 600 nến raw bridge."""
    return synthetic_frame(1300).drop(columns="date")


def schedule(frame: pd.DataFrame) -> dict[str, str]:
    """Hai boundary sát nhau để kiểm purge horizon chứ không chỉ train_end < query."""
    names = ("train_start", "train_end", "validation_start", "validation_end", "test_start", "test_end")
    return dict(zip(names, (str(frame.Datetime.iloc[i].date()) for i in (350, 750, 751, 1000, 1001, 1299))))


def causal_fixture(root: Path) -> tuple[UnifiedFixture, dict[str, Any], dict[str, Any]]:
    """Nối cả tám vai trò vào cùng nguồn alpha causal; bank/context vẫn là stub ghi rõ fixture."""
    fx = UnifiedFixture(root)
    frame = source_frame()
    frame["Datetime"] = pd.bdate_range(end=pd.Timestamp(fx.point["cutoff"]) + pd.offsets.BDay(3), periods=len(frame))
    artifact = fit_selector(frame, schedule(frame))
    for name, value in (("causal-prices.json", frame_document(frame)), ("causal-selector.json", artifact)):
        (root / name).write_bytes(json_bytes(value))
        fx.spec["source_hashes"][name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
    fx.source_sha = fx.spec["source_hashes"]["causal-prices.json"]
    fx.frame = frame
    prefix = frame.loc[frame.Datetime <= pd.Timestamp(fx.point["cutoff"])].tail(600)
    fx.snapshot = snapshot_from_graph(fx.point, 0, fx.payload, prefix, fx.source_sha, [])
    fx.spec.update(version="unified_experiment_v2", input_profile="causal_common_v1",
        causal_sources={"FPT/fixture": {"prices": "causal-prices.json", "selector": "causal-selector.json"}},
        calendar_sha256=digest(frame.Datetime.dt.strftime("%Y-%m-%d").tolist()))
    bound = CausalSources(fx.spec, root).bind(fx.snapshot)
    return fx, prepared_bundle(fx, bound), artifact


def prepared_bundle(fx: UnifiedFixture, bound: SharedSnapshot) -> dict[str, Any]:
    """Dựng bundle từ một snapshot đã bind, không đưa outcomes vào request/context."""
    methods = fx.methods()
    outputs, preparations, responses = {}, {}, {}
    for variant in execution_order(fx.spec["variants"]):
        dependencies = {key: outputs[key] for key in next(v for v in VARIANTS if v.id == variant).dependencies}
        prepared = methods.prepare(variant, bound, deepcopy(dependencies), 0)
        validate_prepared(variant, bound, prepared, fx.spec["decision"], 0)
        slot = slot_id(fx.point["id"], 0, 0, variant)
        preparations[slot] = prepared
        raw = None
        if prepared["request"] is not None:
            value = reply(fx.facts, "SHORT" if variant == "MT_BICL" else "LONG", anchor=variant == "Fact_Anchor") if variant in ("Fact_Anchor", "MT_BICL") else original()
            raw = {"request_sha256": digest(prepared["request"]), "source_request_id": str(uuid5(NAMESPACE_URL, slot)),
                   "source_sha256": digest({"reply": value, "fixture_response_provenance": fx.source_sha}), "reply": value}
            responses[slot] = raw
        outputs[variant] = make_record(fx.point, bound, variant, 0, prepared, raw, dependencies)
    bundle = {"spec": fx.spec, "snapshots": {fx.point["id"] + "/u0": bound.document()},
        "preparations": preparations, "responses": responses,
        "outcomes": {fx.point["id"]: outcome_from_frame(fx.point, fx.frame, fx.source_sha)}}
    return bundle
