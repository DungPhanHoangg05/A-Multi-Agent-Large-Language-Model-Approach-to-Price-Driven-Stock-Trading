"""Phiên bản tối thiểu của đường prompt native và đường Prior hiện hành."""
from __future__ import annotations

NATIVE_METHOD = "original_fix"
NATIVE_PROFILE = "original_fix_serving_v1"
INTEGRATED_PROFILE = "integrated_default_v1"


def validate_decision_profile(value: str) -> str:
    """Chặn profile không biết trước khi khởi tạo client hoặc biên dịch graph."""
    if type(value) is not str or value not in (NATIVE_PROFILE, INTEGRATED_PROFILE):
        raise ValueError("Decision profile không được hỗ trợ; native chạy mới dùng original_fix_serving_v1")
    return value
