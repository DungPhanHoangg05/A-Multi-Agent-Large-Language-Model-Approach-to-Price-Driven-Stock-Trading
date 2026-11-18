"""Khóa tập bank theo độ phủ tín hiệu trước khi thu Pattern và Trend."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from core.finalize_bank_resources import ASSETS, RECIPE, mature_cycles
from core.finalize_bank_signals import NODES
from core.unified_contracts import digest
from core.unified_protocol import binding, read

ARCHIVE = "docs/plan/week12/finalize_bank_signal_rebuild_v2.zip"
ARCHIVE_HASH = "612bcb8b22d0627cb0f82adf64758d96b9e1123777154d9e1a4c74d75e9a61aa"
POLICY = "finalize_bank_admission_v1"
DIRECTIONS = frozenset({"BULLISH", "BEARISH", "NEUTRAL"})


def classify_signals(signals: dict[str, str | None]) -> tuple[bool, bool]:
    """Chỉ mẫu đã có T/P mới tính thống kê. Xếp ví dụ cần đủ T/P/A/I."""
    fields = {"pattern", "trend", "indicator_consensus", "alpha_consensus", "sentiment"}
    if set(signals) != fields:
        raise ValueError("Tín hiệu bank thiếu trường hoặc có trường ngoài schema")
    for key in fields - {"sentiment"}:
        if signals[key] is not None and signals[key] not in DIRECTIONS:
            raise ValueError("Tín hiệu kỹ thuật ngoài enum đã khóa")
    if signals["sentiment"] not in (None, "POSITIVE", "NEGATIVE", "NEUTRAL"):
        raise ValueError("Tín hiệu tin ngoài enum đã khóa")
    statistics = signals["trend"] is not None and signals["pattern"] is not None
    example = statistics and signals["indicator_consensus"] is not None and signals["alpha_consensus"] is not None
    return statistics, example


def load_payload(raw: bytes) -> dict[str, Any]:
    """Từ chối envelope đã đổi byte nội dung hoặc thiếu version structure."""
    doc = json.loads(raw)
    if set(doc) != {"payload", "sha256"} or digest(doc["payload"]) != doc["sha256"]:
        raise ValueError("Checkpoint bank sai checksum")
    return doc


def collection_plan(root: Path) -> dict[str, Any]:
    """Duyệt 852 checkpoint với nhãn tách biệt, dựng kế hoạch slot label-blind."""
    archive_pin = binding(root, ARCHIVE)
    if archive_pin["sha256"] != ARCHIVE_HASH:
        raise ValueError("Gói checkpoint khác nguồn đã khóa cho admission")
    numeric_pin = binding(root, ASSETS + "bank.json")
    numerical_manifest = read(root, ASSETS + "manifest.json", True)
    if numeric_pin not in numerical_manifest["asset_bindings"]:
        raise ValueError("Bank số không khớp manifest FIN06")
    bank = read(root, ASSETS + "bank.json")["records"]
    expected = {r["episode_id"].replace(":", "-"): r for r in bank}
    reserved = set(read(root, RECIPE, True)["reserved_ids"])
    mature_cycles(bank, reserved, "2022-12-31")
    episodes, slots = [], []
    with ZipFile(root / ARCHIVE) as z:
        report = load_payload(z.read("report.json"))["payload"]
        recipe = load_payload(z.read("recipe.json"))
        if report["recipe_sha256"] != recipe["sha256"] or report["hosted_calls"] != 0:
            raise ValueError("Checkpoint không thuộc recipe offline đã khóa")
        points = report["points"]
        if len(points) != len(expected) or {p["id"] for p in points} != set(expected):
            raise ValueError("Membership checkpoint khác bank FIN06")
        for pointer in points:
            key = pointer["id"]
            doc = load_payload(z.read(f"points/{key}.json"))
            point, parent = doc["payload"], expected[key]
            if (doc["sha256"] != pointer["sha256"] or point["episode_id"] != parent["episode_id"]
                    or point["cutoff"] != parent["as_of_date"] or point["symbol"] != parent["symbol"]
                    or point["parent"]["news_sha256"] != parent["news_snapshot_sha256"]):
                raise ValueError("Checkpoint không khớp episode đã pin")
            if point["sentiment"]["available"] or point["sentiment"]["value"] is not None:
                raise ValueError("Nguồn tin mới cần version và kiểm lại policy FIN05")
            signals = {"pattern": point["vision"]["pattern"]["value"], "trend": point["vision"]["trend"]["value"],
                       "indicator_consensus": point["indicator"]["value"], "alpha_consensus": point["alpha"]["value"],
                       "sentiment": None}
            stats, example = classify_signals(signals)
            if stats or example or signals["indicator_consensus"] is None or any(signals[n] is not None for n in NODES):
                raise ValueError("Admission offline không nhận phản hồi chưa qua FIN09")
            episodes.append({"id": key, "symbol": point["symbol"], "cutoff": point["cutoff"],
                             "alpha_available": signals["alpha_consensus"] is not None,
                             "alpha_reason": point["alpha"].get("reason"), "sentiment_available": False,
                             "statistics_ready": stats, "example_ready": example})
            for node in NODES:
                slots.append({"id": f"bank/{key}/{node}", "node": node, "episode_id": key,
                              "chart_window_sha256": point["parent"]["window_sha256"],
                              "checkpoint_sha256": doc["sha256"], "status": "PENDING_FIN09"})
    counts = Counter(p["symbol"] for p in episodes if p["alpha_available"])
    return {"version": POLICY, "status": "OFFLINE_PREPARATION_PASS_COLLECTION_PENDING",
            "FIN06_complete": False, "bank_release": False, "source_archive": archive_pin, "bank_source": numeric_pin,
            "policy": {"statistics": "Đủ Pattern và Trend, cùng regime/mã và exit < cutoff. Mẫu số lấy toàn population đã admission, không lấy top K.",
                       "examples": "Đủ bốn tín hiệu T/P/A/I. Alpha NA không tham gia similarity hoặc nhận điểm 0. K tối đa 3 như FIN02.",
                       "sentiment": "Giữ null theo FIN05. Không đưa vào thước đo kỹ thuật hoặc thay bằng NEUTRAL.",
                       "scope": "Giữ 852 chu kỳ. Quota FIN09 và raw/parse/regime/index cần qua kiểm trước mở bank.",
                       "integration": "FIN07 kiểm thống kê/similarity/BRPP trên schema này; chưa cấp record cho retriever legacy."},
            "planned_episodes": len(episodes), "alpha_available": sum(counts.values()), "alpha_available_by_symbol": dict(counts),
            "statistics_ready": 0, "examples_ready": 0, "vision_slots_planned": len(slots),
            "attempt_ceiling_if_cap_three": len(slots) * 3, "hosted_calls": 0, "query_outcomes_computed": False,
            "episodes": episodes, "slots": slots}
