"""Registry thống nhất; tên archive cũ chỉ là alias được khai báo tường minh."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Variant:
    """Nhận diện phương pháp, projection và dependency; không phải grant inference."""
    id: str
    profile: str
    schema: str
    dependencies: tuple[str, ...] = ()
    resources: tuple[str, ...] = ()
    retrieval: str | None = None
    fallback: str | None = None
    role: str = "research"
    alpha: bool = True
    sentiment: bool = True


VARIANTS = (
    Variant("original_fix", "original_fix_serving_v1", "TradeDecisionOutput", role="native"),
    Variant("original_common", "common_decision_v1", "TradeDecisionOutput"),
    Variant("bayesian_v1", "common_decision_v1", "TradeDecisionOutput", ("original_common",),
            ("bank", "regime"), "bayesian_regime_k3", "original_common"),
    Variant("C2", "common_decision_v1", "TradeDecisionOutput", ("original_common",),
            ("bank", "regime"), "conditional_quality_v3", "original_common"),
    Variant("A_tp_pool", "common_decision_v1", "TradeDecisionOutput", ("original_common",),
            ("bank", "regime"), "tp_pool_v1", "original_common"),
    Variant("B_semantic", "common_decision_v1", "TradeDecisionOutput", ("original_common",),
            ("bank", "regime"), "semantic_v1", "original_common"),
    Variant("Fact_Anchor", "fact_anchor_v3", "utility_icl_reply_v3", ("original_common",),
            ("facts",), fallback="original_common", role="dependency"),
    Variant("MT_BICL", "utility_icl_v3", "utility_icl_reply_v3", ("original_common", "Fact_Anchor"),
            ("facts", "context", "student"), fallback="Fact_Anchor"),
)
REGISTRY_VERSION = "unified_variant_registry_v2"


def get_variant(identifier: str) -> Variant:
    """Không tự sửa hoa/thường hoặc nhận alias archive như một profile mới."""
    for variant in VARIANTS:
        if type(identifier) is str and identifier == variant.id:
            return variant
    raise ValueError("Variant không được hỗ trợ: " + str(identifier))


def execution_order(identifiers: list[str]) -> list[str]:
    """Thứ tự topo xác định; dependencies chỉ chạy một lần trong mỗi repeat."""
    if (type(identifiers) is not list or not identifiers or any(type(v) is not str for v in identifiers)
            or len(set(identifiers)) != len(identifiers)):
        raise ValueError("Danh sách variant rỗng hoặc trùng")
    result: list[str] = []
    def add(identifier: str) -> None:
        variant = get_variant(identifier)
        for dependency in variant.dependencies:
            add(dependency)
        if identifier not in result:
            result.append(identifier)
    for identifier in identifiers:
        add(identifier)
    return result


def registry_document() -> dict:
    """Danh mục CLI/UI không import bank, model hoặc client."""
    return {"version": REGISTRY_VERSION, "default": "original_fix", "hosted_release": False,
            "variants": [{**asdict(v), "dependencies": list(v.dependencies), "resources": list(v.resources)} for v in VARIANTS],
            "archive_aliases": {"Original_common": "original_common"},
            "input_profiles": {"native_common_v1": "HISTORICAL_EXPLORATORY",
                "causal_common_v1": "FROZEN_PURGED_ALPHA_ONLY; WHOLE_SYSTEM_GATE_PENDING_U06_U07"},
            "native_rowwise_causal_gate": "FAIL", "quality": "HISTORICAL_EXPLORATORY_CONDITIONAL"}
