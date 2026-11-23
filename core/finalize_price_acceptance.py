"""Nghiệm thu FIN04 theo xác nhận chủ dữ liệu, giữ riêng kết quả PIT độc lập."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from core.finalize_price_audit import ASSETS, COMPAT, DIRECTORY, H02, audit_prices
from core.unified_protocol import binding, read

ACCEPTANCE = DIRECTORY + "finalize_price_acceptance_v1.json"
PROFILE = "finalize_raw_prices_owner_attested_v1"
OWNER_STATEMENT = "Xác nhận chắc chắn đó là giá chính xác. Hãy pass FIN04 và tiếp tục FIN05"


def accepted_prices(root: Path) -> dict[str, Any]:
    """Lập amendment trước query mới; xác nhận của tác giả không thành chứng nhận bên ngoài."""
    audit = read(root, DIRECTORY + "finalize_price_audit.json", True)
    if audit != audit_prices(root):
        raise ValueError("Nguồn giá không còn khớp audit FIN04 đã khóa")
    points = [{**point, "forecast_planned": True, "price_prefix_accepted": True,
               "economic_label_eligible": not point["known_event_dates_inside_holding"],
               "economic_unavailable_reason": ("KNOWN_CORPORATE_ACTION_DURING_HOLDING"
                   if point["known_event_dates_inside_holding"] else None)} for point in audit["points"]]
    # Các cờ độc lập cũ giữ nguyên trong từng point; trường acceptance tách biệt với admission cũ.
    return {
        "version": "finalize_price_acceptance_v1", "result": "PASS_OWNER_ATTESTED",
        "profile": PROFILE, "FIN04_complete": True,
        "owner_confirmation": {"recorded_date": "2026-11-18", "origin": "USER_CONVERSATION",
                               "statement": OWNER_STATEMENT, "scope": "PRICE_ACCURACY_ACCEPTED_BY_OWNER"},
        "independent_price_pit_certified": False,
        "economic_eligibility_status": "KNOWN_EVENT_SCREEN_ONLY_REQUIRE_EXECUTION_VALIDATION",
        "independent_source_gate": audit["price_source_gate"],
        "parents": [binding(root, DIRECTORY + name) for name in (
            "finalize_comparison_contract.json", "finalize_price_audit.json",
            "finalize_price_checks.zip", "finalize_price_primary_sources.zip")],
        "source_bindings": audit["source_bindings"],
        "query_sources": [{"symbol": row["symbol"], "raw_csv": H02 + row["symbol"] + ".raw.csv",
            "event_ledger": H02 + row["symbol"] + ".events.json", "origin": row["locked_origin"],
            "excluded_prefix_rows": row["excluded_prefix_rows"],
            "replaces_donor": ASSETS + row["symbol"] + ".json"} for row in audit["symbols"]],
        "bank_source": COMPAT, "calendar": H02 + "VNINDEX_2018_2026_verified_overlap.csv",
        "recipe": {"price_basis": "UNADJUSTED_EXECUTION_FIELDS", "price_unit": "thousand_VND",
            "volume_unit": "matched_shares", "query_columns": ["Datetime", "Open", "High", "Low", "Close", "Volume"],
            "prefix": "Giữ origin đã khóa; chỉ lấy Datetime <= cutoff, không ghép hoặc scale donor.",
            "availability": "Chấp nhận tái dựng lịch sử theo xác nhận giá của chủ dữ liệu; không tạo available_at giả hoặc nhận là đã chứng minh as-published.",
            "calendar_scope": "Lịch VNINDEX quan sát và đối soát HOSE bổ sung; chưa chứng nhận độc lập mọi ngừng giao dịch 2018–2026.",
            "events_scope": "Ledger vendor đã khóa và năm thông báo VSDC; chưa chứng nhận nội dung lịch sử hoặc tính đầy đủ độc lập.",
            "economic_contract": "Open(t+1) -> Close(t+3); SHORT=CASH; phí 0.25% và slippage 0.10% mỗi chiều; compute_round_trip_net_return.",
            "rights_policy": "Giữ đủ forecast planned; năm chu kỳ quyền giữ economic label NA có lý do, không cộng quyền/đổi P&L hoặc im lặng bỏ point. Dùng cùng mask cho mọi phương pháp và baseline. Các point còn lại chỉ qua sàng lọc quyền đã biết; validator thực thi vẫn phải kiểm quyền/Reference/khối lượng trước nhãn tại FIN12.",
            "rebuild_required": "FIN06 tái tạo selector/đặc trưng/context/tài nguyên chịu ảnh hưởng của raw source theo recipe FIN02 trước query; FIN09 kiểm lại reuse theo request thực.",
            "scientific_scope": "EXPLORATORY_OWNER_ATTESTED_SOURCE; không dùng acceptance này làm bằng chứng PIT nguồn độc lập hoặc toàn hệ Zero-Leakage."},
        "points": points, "planned_forecasts": len(points),
        "economic_eligible_points": sum(p["economic_label_eligible"] for p in points),
        "economic_unavailable_points": sum(not p["economic_label_eligible"] for p in points),
        "dataset_version_changed": True, "resources_rebuilt": False,
        "query_outcomes_computed": False, "hosted_api_calls": 0, "training": False,
    }


def require_accepted_prices(root: Path, *, profile: str) -> dict[str, Any]:
    """Chỉ profile khai báo rõ owner-attested được nhận acceptance; không mở gate độc lập cũ."""
    if profile != PROFILE:
        raise ValueError("Cần profile giá owner-attested đúng version")
    record = read(root, ACCEPTANCE, True)
    if record != accepted_prices(root):
        raise ValueError("Acceptance khác nguồn, recipe hoặc xác nhận đã khóa")
    return record
