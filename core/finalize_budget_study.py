"""Dry-run request of 102 query khóa trước outcome, dùng renderer/adapter bản sửa."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from core.causal_bridge import REPAIRED_NATIVE_PROFILE, decision_payload
from core.finalize_budget_archive import Archive, fingerprints, match
from core.finalize_budget_quota import ATTEMPT_CAP
from core.finalize_serving_provider import FinalizedProvider
from core.groq_pacing import MODEL_LIMITS, request_budget
from core.historical_evaluation_runner import FixtureClients
from core.historical_signals import snapshot_payload
from core.serving_runtime.providers import VisionProxy
from core.unified_contracts import SharedSnapshot, digest
from core.unified_execution import StageBook, raw_record
from core.unified_execution_transport import REPAIR, body_for, parsed
from core.unified_protocol import ordered_branches
from core.variant_registry import get_variant

VISION = ("pattern", "trend")
MODEL_VISION, MODEL_DECISION = "qwen/qwen3.8-27b", "openai/gpt-oss-20b"
NAMESPACE = "finalize_anchor102_exploratory_v1"


class StudyProvider(FinalizedProvider):
    """Nghiên cứu render VI theo FIN02, sidecar song ngữ dành cho serving."""
    presentation_enabled = False

    def vision_proxy(self, role: str, calls: object, slot: str, attempt: str, model: dict) -> VisionProxy:
        """Cùng request wire đã khóa, transport dưới đây chỉ ghi nhận body."""
        return VisionProxy(calls, slot, attempt, model)


def slot_row(phase: str, slot: str, role: str, body: dict | None, old: dict | None, *,
             conditional: bool, parents_verified: bool, dependencies: dict, bypass_reason: str | None = None) -> dict:
    """Ghi hạch toán trước retry, giữ rõ provenance hoặc lý do phụ thuộc chưa có raw."""
    hashes = fingerprints(body) if body is not None else None
    if phase == "SMOKE" and body is not None:
        state, reason = "NEW", "INDEPENDENT_SMOKE_EPOCH"
    else:
        state, reason = match(hashes, old, parents_verified=parents_verified, conditional=conditional)
    if state == "BYPASS" and bypass_reason:
        reason = bypass_reason
    reserve = repair_reserve = 0
    prompt_chars = None
    if body is not None:
        reserve = request_budget(body)
        repair_reserve = reserve
        if "response_format" in body:
            prompt_chars = sum(len(m["content"]) for m in body["messages"])
            repair = deepcopy(body)
            repair["messages"][0]["content"] += REPAIR
            repair_reserve = request_budget(repair)
            if prompt_chars + len(REPAIR) >= 6500:
                raise ValueError("Decision/repair vượt 6.500 ký tự trong dry-run")
        if max(reserve, repair_reserve) > MODEL_LIMITS[body["model"]]["tpm"]:
            raise ValueError("Request/repair vượt TPM trong dry-run")
    changes = None if not (old and hashes) else [key for key in hashes if old["fingerprints"][key] != hashes[key]]
    return {"phase": phase, "slot": slot, "role": role, "model": body["model"] if body else MODEL_DECISION,
            "state": state, "reason": reason, "new_wire_proof": "NONE_BYPASS" if body is None else
                "CONTROL_BODY_DEPENDS_ON_NEW_RESPONSES" if conditional else "ACTUAL_BODY_BEFORE_TRANSPORT",
            "fingerprints": hashes, "wire_differences": changes, "old": old,
            "dependency_receipts": dependencies, "prompt_chars": prompt_chars,
            "attempt_reserve_tokens": reserve if state == "NEW" else 0,
            "all_attempts_reserve_tokens": reserve + (ATTEMPT_CAP-1)*max(reserve, repair_reserve) if state == "NEW" else 0}


class VisionLedger:
    """Dựng ảnh/report bằng graph thật, nhận raw U08 có proof hoặc fixture đo sizing."""
    def __init__(self, archive: Archive, phase: str, old_price: dict, new_price: dict) -> None:
        self.archive, self.phase = archive, phase
        self.old_price, self.new_price = old_price, new_price
        self.rows: list[dict] = []

    def call(self, slot: str, body: dict, attempt: str) -> tuple[str, dict]:
        """Ghi hai request I/P/T; fixture reply chỉ dùng đo prompt downstream."""
        role = slot.rsplit("/", 1)[-1]
        if role not in VISION or body["model"] != MODEL_VISION or any(r["role"] == role for r in self.rows):
            raise ValueError("Upstream khác đúng một request cho mỗi vai trò thị giác")
        old = self.archive.candidate(slot) if self.phase == "RESEARCH" else None
        parent = self.old_price == self.new_price
        if old and old["fingerprints"]["wire"] == digest(body):
            old_attempt, _ = self.archive.stage(slot)
            parent = parent and old_attempt["attempt_id"] == old["attempt"]
        row = slot_row(self.phase, slot, role, body, old, conditional=False, parents_verified=parent,
                       dependencies={"new_price_window_sha256": digest(self.new_price),
                                     "old_price_window_sha256": digest(self.old_price)})
        self.rows.append(row)
        if row["state"] == "REUSE":
            wire = self.archive.raw(old["id"], old["sha256"])
            return parsed(wire["body"], json.loads(wire["response"])), {}
        if role == "pattern":
            return ("**Mẫu nến chính:** Đối chứng offline.\n**Thiên lệch dự báo:** NEUTRAL\n"
                    "**Giải thích:** Danh mục nến giả lập chỉ dùng kiểm định dạng request."), {}
        return ("**Hướng xu hướng:** Đi ngang\n**Phân tích chi tiết:** Đối chứng định dạng.\n"
                "**Dự báo xu hướng:** Không có dự báo thị trường từ fixture.\n**Độ tin cậy:** Thấp"), {}


def old_snapshot(archive: Archive, point: dict) -> SharedSnapshot:
    """Neo đúng point và realization của hồ sơ cũ, không decode payoff."""
    _, doc = archive.stage("shared/"+point["id"])
    if doc["realization"] != 0 or any(doc["point"][k] != point[k] for k in ("id", "symbol", "cutoff", "fold")):
        raise ValueError("Snapshot U08 không thuộc lịch FIN02")
    return SharedSnapshot.create(doc["point"], 0, doc["payload"], doc["provenance"])


def replay_decision(archive: Archive, slot: str, old: dict, body: dict, new_snapshot: SharedSnapshot,
                    archived_snapshot: SharedSnapshot, variant: str, reused: dict, dependencies: dict) -> tuple[dict | None, str | None]:
    """Chỉ trả raw nếu bản cũ, input projection và mọi parent của repeat khớp."""
    if old["fingerprints"]["wire"] != digest(body) or old["status"] != 200 or old["repair"]:
        return None, None
    profile = REPAIRED_NATIVE_PROFILE if variant == "original_fix" else None
    old_input = decision_payload(archived_snapshot, variant)
    new_input = decision_payload(new_snapshot, variant, decision_profile=profile)
    if old_input != new_input or not dependencies.keys() <= reused.keys():
        return None, None
    attempt, record = archive.stage(slot)
    forecast = record["forecast"]
    if (attempt["attempt_id"] != old["attempt"] or forecast["shared_sha256"] != archived_snapshot.sha256
            or forecast["projection_sha256"] != digest(old_input)
            or forecast["dependency_hashes"] != {k: reused[k] for k in dependencies}):
        return None, None
    _, preparation = archive.stage("prepare/"+slot)
    archived_request = preparation["request"]
    if archived_request is None or body_for(archived_request) != body:
        raise ValueError("Archive forecast khác prepared body đã khóa")
    wire = archive.raw(old["id"], old["sha256"])
    reply = parsed(wire["body"], json.loads(wire["response"]))
    raw = raw_record(archived_request, wire, reply)
    if raw != forecast["raw"] or forecast["request_sha256"] != raw["request_sha256"]:
        raise ValueError("Archive cùng wire nhưng raw/DAG không khớp")
    return raw, digest(record)


def point_rows(provider: StudyProvider, archive: Archive, book: StageBook, point: dict, *,
               phase: str, point_index: int, repeats: int) -> list[dict]:
    """Một upstream, ba repeat, same-repeat dependencies và không gọi outcome."""
    archived = old_snapshot(archive, point)
    prices = archived.document()["payload"]["price_prefix"]
    old_window = {field: values[-45:] for field, values in prices.items()}
    new_window = snapshot_payload(provider.prefix(point).tail(45))
    calls = VisionLedger(archive, phase, old_window, new_window)
    with redirect_stdout(io.StringIO()):
        snapshot_doc = provider.shared(book, point, calls)
    if {row["role"] for row in calls.rows} != set(VISION):
        raise ValueError("Dry-run thiếu request Pattern/Trend")
    vision_proven = all(r["state"] == "REUSE" for r in calls.rows)
    snapshot = SharedSnapshot.create(point, 0, snapshot_doc["payload"], snapshot_doc["provenance"])
    rows = list(calls.rows)
    fixtures = FixtureClients()
    for repeat in range(repeats):
        records, reused = {}, {}
        for variant in ordered_branches(point_index * 3 + repeat):
            slot = f"forecast/{point['id']}/u0/r{repeat}/{variant}"
            parents = {k: records[k] for k in get_variant(variant).dependencies}
            prepared = provider.prepare(variant, snapshot, parents, repeat)
            request = prepared["request"]
            body = body_for(request) if request is not None else None
            if body is not None and body["model"] != MODEL_DECISION:
                raise ValueError("Decision đổi model đã khóa FIN02")
            old = archive.candidate(slot) if phase == "RESEARCH" else None
            raw, archived_forecast_sha = None, None
            if body is not None and old is not None and vision_proven and parents.keys() <= reused.keys():
                raw, archived_forecast_sha = replay_decision(archive, slot, old, body, snapshot, archived, variant, reused, parents)
                if raw is not None:
                    raw["request_sha256"] = digest(request)
            conditional = not vision_proven or not parents.keys() <= reused.keys()
            bypass = prepared["trace"].get("reason")
            if request is None and variant == "MT_BICL":
                bypass = prepared["aux"]["branch"]["reason"]
            row = slot_row(phase, slot, variant, body, old, conditional=conditional,
                parents_verified=archived_forecast_sha is not None,
                dependencies={"shared_control_sha256": snapshot.sha256,
                    "vision_slots": [r["slot"] for r in calls.rows],
                    "same_repeat": {k: {"control_forecast_sha256": digest(v), "archive_forecast_sha256": reused.get(k)}
                                    for k, v in parents.items()}}, bypass_reason=bypass)
            if row["state"] == "REUSE":
                if raw is None or archived_forecast_sha is None:
                    raise ValueError("Thiếu raw đúng scope dù đã nhận REUSE")
                reused[variant] = archived_forecast_sha
            elif request is not None:
                identifier = str(uuid5(NAMESPACE_URL, "FIN09_CONTROL_ONLY|"+phase+"|"+slot))
                raw = fixtures.decision(1, request, identifier, variant)
                raw["source_request_id"] = identifier
            policy = provider.resolve_bound(variant, snapshot, parents, repeat, prepared, raw)
            records[variant] = {"forecast": {"variant": variant, "point_id": point["id"], "repeat": repeat,
                "realization": 0, "shared_sha256": snapshot.sha256, "raw": raw}, "policy": policy}
            row["request_sha256"] = digest(request) if request is not None else None
            if variant == "MT_BICL" and request is not None:
                row["conditional_support"] = "REQUIRES_VALID_SAME_REPEAT_FACT_ANCHOR"
            rows.append(row)
    return rows
