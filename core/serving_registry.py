"""Danh mục ứng dụng riêng; không thay identity của registry nghiên cứu đã khóa."""
from __future__ import annotations

from typing import Any

from core.variant_registry import REGISTRY_VERSION as RESEARCH_REGISTRY_VERSION
from core.variant_registry import execution_order, get_variant

REGISTRY_VERSION = "variant_serving_registry_v1"
CONTRACT_VERSION = "variant_serving_v1"
CONFIG_VERSION = "serving_config_v1"
MAIN_IDS = ("original_fix", "bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL")
ADVANCED_IDS = ("original_common", "Fact_Anchor")
LABELS = {
    "original_fix": ("Hệ gốc", "Original"),
    "bayesian_v1": ("Bayesian v1", "Bayesian v1"),
    "C2": ("Bayesian v2 — C2", "Bayesian v2 — C2"),
    "A_tp_pool": ("Bayesian A — TP Pool", "Bayesian A — TP Pool"),
    "B_semantic": ("Bayesian B — Semantic", "Bayesian B — Semantic"),
    "MT_BICL": ("MT-BICL", "MT-BICL"),
    "original_common": ("Baseline chung", "Common baseline"),
    "Fact_Anchor": ("Fact Anchor", "Fact Anchor"),
}
JOB_STATES = ("queued", "running", "stop_requested", "stopped", "partial", "completed", "failed", "unknown")


def required_resources(identifiers: list[str]) -> list[str]:
    """Tính cả tài nguyên dependency; nguồn giá/tin/lịch luôn cần cho snapshot mới."""
    return sorted({"prices", "news", "calendar"} | {
        resource for identifier in execution_order(identifiers)
        for resource in get_variant(identifier).resources})


def registry_document() -> dict[str, Any]:
    """Metadata không nạp weights, đọc archive, tạo graph hoặc cấp quyền chạy."""
    variants = []
    from core.finalize_serving_profile import SCIENTIFIC_STATUS, VERSION as FINALIZED, method_profile
    for identifier in (*MAIN_IDS, *ADVANCED_IDS):
        method = get_variant(identifier)
        variants.append({
            "id": identifier, "label": dict(zip(("vi", "en"), LABELS[identifier])),
            "group": "main" if identifier in MAIN_IDS else "advanced",
            "profile_version": method.profile, "output_schema": method.schema,
            "retrieval_version": method.retrieval, "dependencies": list(method.dependencies),
            "fallback": method.fallback, "required_resources": required_resources([identifier]),
            "capabilities": {
                "read_results": {"available": True, "reason": "VERIFIED_U09_ARTIFACT_READER",
                                 "scope": "VERIFIED_HISTORICAL_MANIFEST"},
                "analyze": {"available": True, "reason": "CONDITIONAL_SERVER_PREFLIGHT"},
                "compare": {"available": True, "reason": "CONDITIONAL_SERVER_PREFLIGHT"},
                "backtest": {"available": True, "reason": "CONDITIONAL_SERVER_PREFLIGHT"},
            },
        })
    return {
        "version": REGISTRY_VERSION, "contract_version": CONTRACT_VERSION, "config_version": CONFIG_VERSION,
        "default_profile": FINALIZED,
        "model_binding": "JOB_REQUEST_ALL_SIX_AGENT_ROLES",
        "prompt_binding": "SERVER_CONFIG_PROMPT_VERSIONS_INCLUDING_DEPENDENCIES",
        "method_registry_version": RESEARCH_REGISTRY_VERSION, "default": "original_fix",
        "variants": variants, "evaluation_controls": ["CASH", "ALWAYS_LONG"],
        "domain": {
            "candidate_timeframes": ["1d"], "candidate_languages": ["vi","en"], "generation_languages":["vi"],
            "released_symbols": ["BHN", "CMG", "FPT", "HVN", "MBB", "MWG", "VCB", "VJC", "VNM"],
            "released_date_ranges": [{"start_date": "2026-07-01", "end_date": "2026-09-23"}],
            "resource_version": "serving_asof_q3_2026_v1", "max_points": 30, "live_latest_supported": True,
            "live": {"version": "serving_live_daily_v1", "api": "/api/serving/live/v1",
                     "symbol_scope": "LIVE_STOCK_CATALOG; FROZEN_ASOF_SCOPE_UNCHANGED",
                     "timeframes": ["1d"], "languages": ["vi","en"], "generation_languages":["vi"], "modes": ["analyze", "compare"],
                     "session_policy": "LATEST_COMPLETED_DAILY_SESSION_AFTER_15_30_ASIA_HO_CHI_MINH",
                     "snapshot_policy": "CAPTURE_ONCE_PER_OWNER; NO_REFETCH_ON_RESUME",
                     "scientific_status": "EXPLORATORY_NOT_CERTIFIED"},
            "realtime_timeframes": ["5m", "15m", "30m", "1h", "1d", "1w", "1mo"],
            "realtime_versions": list(MAIN_IDS),
            "support_policy": "SERVER_VERIFIED_RESOURCE_MANIFEST_REQUIRED",
            "resource_readiness": "VERIFY_ON_SERVER_PREFLIGHT",
            "historical_support": "EXACT_POINTS_IN_VERIFIED_U09_MANIFEST_ONLY",
            "ood_policy": "DECLARED_METHOD_FALLBACK_ONLY; NOT_RESOURCE_FAILURE",
        },
        "legacy": {"analyze": "/api/analyze", "backtest": "/api/backtest/start",
                   "default_variant": "original_fix", "contract": "legacy_native_unchanged",
                   "research_registry": "/api/experiments/registry"},
        "job_states": list(JOB_STATES),
        "opt_in_profiles": {FINALIZED: {"request_version": FINALIZED, "launch_status": "CONDITIONAL_SERVER_PREFLIGHT",
            "scientific_status": SCIENTIFIC_STATUS, "method_profiles": {v: method_profile(v) for v in (*MAIN_IDS, *ADVANCED_IDS)}}},
        "scientific_limits": {"native_rowwise_causal_gate": "FAIL",
                              "whole_system_causal_gate": "NOT_CERTIFIED"},
    }
