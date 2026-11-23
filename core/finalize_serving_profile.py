"""Định danh preview FIN08 dùng chung CLI, serving và reader."""
from __future__ import annotations

from core.variant_registry import get_variant

VERSION = "finalize_serving_v1"
LIVE_CAPTURE = "finalize_live_raw_capture_v1"
RECEIPT = "docs/plan/week12/finalize_context_receipt_v1.json"
RECEIPT_SHA256 = "4dc58e27cd4abfd8194f0d4de4599203f3b41f7563872679bba5e1b951e39c4b"
UNAVAILABLE_OUTCOME = "finalize_outcome_unavailable_v1"
OUTCOME_REASONS = {"PENDING_EXIT", "MISSING_EXECUTION_SESSION", "NO_MATCHED_VOLUME_AT_EXECUTION",
                   "CORPORATE_ACTION_DURING_HOLDING", "OFFLINE_FIXTURE_OUTCOME_LOCKED"}
PENDING = "HOSTED_RELEASE_PENDING_FIN10"
SCIENTIFIC_STATUS = "EXPLORATORY_NOT_CERTIFIED"


def method_profile(variant: str) -> str:
    """Result/requests bản sửa có identity mới dù giữ ID lựa chọn."""
    from core.causal_bridge import REPAIRED_NATIVE_PROFILE
    return REPAIRED_NATIVE_PROFILE if variant == "original_fix" else VERSION + "/" + get_variant(variant).profile
