"""DAG serving paired, checkpoint mỗi node/slot và outcome sau forecast barrier."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import threading
from typing import Any

from core.historical_evaluation_journal import load
from core.prior_run_lock import PriorRunLock
from core.serving_contracts import result_document
from core.unified_contracts import SharedSnapshot, digest
from core.unified_execution import StageBook, raw_record
from core.unified_execution_transport import body_for
from core.variant_registry import get_variant
from core.serving_runtime.quota import Stopped

ERRORS = {
    "RESOURCE_UNAVAILABLE": "Tài nguyên serving chưa sẵn sàng",
    "INTEGRITY_FAILURE": "Nguồn hoặc checkpoint khác identity đã khóa",
    "PROVIDER_FAILURE": "Provider trả lỗi; giữ nguyên slot đã hoàn tất",
    "UNKNOWN_ATTEMPT": "Attempt chưa rõ kết quả; cần đối soát UUID trước khi gửi lại",
    "QUOTA_EXCEEDED": "Đang chờ quota hoặc thời hạn retry của provider",
    "INVALID_MODEL_OUTPUT": "Phản hồi model không đạt hợp đồng",
    "INTERNAL_ERROR": "Không hoàn tất tác vụ; checkpoint đã được giữ",
}


def safe_error(code: str, retryable: bool = False) -> dict:
    """Chỉ thông báo định trước, không đưa raw credential/error body ra browser."""
    return {"code": code, "message": ERRORS[code], "retryable": retryable}


def slot_id(point: dict, repeat: int, variant: str) -> str:
    """Một slot duy nhất cho mỗi point/repeat/dependency."""
    return f"forecast/{point['id']}/r{repeat}/{variant}"


class Runner:
    """Provider và transport được inject; tests không cần gọi HTTP hoặc dùng stub forecast cache."""

    def __init__(self, store: Any, reservation: dict, calls: Any, provider: Any, *, read_only: bool = False) -> None:
        self.store, self.reservation, self.calls, self.provider = store, reservation, calls, provider
        self.job = store.job(reservation)
        self.doc = self.job.document()
        self.run_id = self.doc["run_id"]
        self.directory = store.path(self.run_id)
        self.book = StageBook(self.directory/"journal", self.doc, verify_only=read_only)
        self.plan = self.doc["execution_plan"]
        self.request = self.doc["identity"]["request"]
        if provider is not None and hasattr(provider, "bind_book"):
            provider.bind_book(self.book, self.plan, self.request["repeats"], self.request["mode"])

    def guard_stop(self) -> None:
        """Chỉ dừng trước stage/HTTP mới, không hủy một request có thể đã gửi."""
        if self.store.control(self.run_id)["stop_requested"]:
            raise Stopped()

    def tick(self) -> None:
        """Không mở outcome nếu thiếu bất kỳ forecast/dependency/repeat durable nào."""
        for point in self.reservation["points"]:
            self.guard_stop()
            snapshot_doc = self.book.execute("shared/"+point["id"], {"point": point},
                lambda _: self.provider.shared(self.book, deepcopy(point), self.calls))
            snapshot = SharedSnapshot.create(snapshot_doc["point"], 0, snapshot_doc["payload"], snapshot_doc["provenance"])
            if snapshot_doc["point"] != point:
                raise ValueError("Shared snapshot khác planned point")
            required = []
            for repeat in range(self.request["repeats"]):
                records = {}
                for variant in self.plan:
                    self.guard_stop()
                    slot = slot_id(point, repeat, variant)
                    deps = {k: deepcopy(records[k]) for k in get_variant(variant).dependencies}
                    parents = {"snapshot": snapshot.sha256, "dependencies": {k: digest(v) for k, v in deps.items()}}
                    prepared = self.book.execute("prepare/"+slot, parents,
                        lambda _: self.provider.prepare(variant, snapshot, deepcopy(deps), repeat))
                    self.provider.validate(variant, snapshot, prepared, repeat)
                    def execute(attempt: str) -> dict:
                        raw = None
                        if prepared["request"] is not None:
                            reply, wire = self.calls.call(slot, body_for(prepared["request"]), attempt)
                            raw = raw_record(prepared["request"], wire, reply)
                        return {"forecast": {"variant": variant, "raw": raw},
                                "policy": self.provider.resolve(variant, prepared, raw, deepcopy(deps))}
                    def validate(record: dict) -> None:
                        raw = record["forecast"]["raw"]
                        if (prepared["request"] is None) != (raw is None):
                            raise ValueError("Raw không đúng request/bypass")
                        if raw is not None:
                            actual_reply, wire = self.calls.call(slot, body_for(prepared["request"]),
                                load(self.book.path(slot))["attempts"][0]["attempt_id"])
                            if raw != raw_record(prepared["request"], wire, actual_reply):
                                raise ValueError("Raw/UUID không khớp wire đã durable")
                        if record["policy"] != self.provider.resolve(variant, prepared, raw, deepcopy(deps)):
                            raise ValueError("Policy không tái lập từ raw/dependency")
                    records[variant] = self.book.execute(slot, {**parents, "prepared": prepared}, execute, validate=validate)
                    required.append(slot)
            if not all(self.book.complete(slot) for slot in required):
                raise ValueError("Outcome bị khóa trước forecast barrier")
            if self.request["mode"] == "backtest":
                self.guard_stop()
                self.book.execute("outcome/"+point["id"], {"slots": required}, lambda _: self.provider.outcome(deepcopy(point)))

    def public(self, status: dict) -> dict:
        """Kết quả partial chỉ chứa slot complete; dữ liệu model để ngoài main rows cho UI nâng cao."""
        from core.prior_stage_journal import decode_output
        rows, executed, details, snapshots = [], set(), {}, {}
        points_complete = 0
        for point in self.reservation["points"]:
            point_rows = []
            shared_slot = "shared/"+point["id"]
            if self.book.complete(shared_slot):
                shared = self.book.execute(shared_slot, {"point": point}, None)
                snapshots[point["id"]] = {"sha256": digest(shared), "payload": shared["payload"], "provenance": shared["provenance"]}
            outcome = None
            outcome_slot = "outcome/"+point["id"]
            if self.book.complete(outcome_slot):
                outcome = decode_output(load(self.book.path(outcome_slot))["attempts"][0]["output"])
            for repeat in range(self.request["repeats"]):
                effective = {}
                for variant in self.plan:
                    slot = slot_id(point, repeat, variant)
                    if not self.book.complete(slot):
                        continue
                    record = decode_output(load(self.book.path(slot))["attempts"][0]["output"])
                    policy, raw = record["policy"], record["forecast"]["raw"]
                    if raw is not None:
                        wire = load(self.directory/"http"/(digest(slot)+".json"))
                        candidates = [row for row in wire["rows"] if row["id"] == raw["source_request_id"]]
                        if (wire["run_id"] != self.run_id or wire["slot"] != slot or len(candidates) != 1
                                or digest(candidates[0]) != raw["source_sha256"]):
                            raise ValueError("Raw response/checksum khác slot đã complete")
                    actual = variant
                    if policy["reason"] in ("FALLBACK_ORIGINAL", "ANCHOR_INVALID_USE_ORIGINAL"):
                        actual = effective["original_common"]
                    elif variant == "MT_BICL" and policy["bypass"]:
                        actual = effective["Fact_Anchor"]
                    effective[variant] = actual
                    executed.add(actual)
                    row = {"point_id": point["id"], "symbol": point["symbol"], "as_of_date": point["cutoff"], "repeat": repeat,
                        "requested_id": variant, "executed_id": actual, "raw_prediction": policy["raw_proposal"],
                        "final_prediction": "LONG" if policy["final_action"] == "LONG" else "SHORT", "final_action": policy["final_action"],
                        "fallback_reason": policy["reason"] if actual != variant else None,
                        "bypass_reason": policy["reason"] if policy["bypass"] else None,
                        "support": {"manifest_sha256": self.doc["identity"]["config"]["support_sha256"],
                                    "status": "declared_fallback" if actual != variant else "supported"},
                        "net_return_pct": (float(outcome["target"]["net_return"]) * 100 if policy["final_action"] == "LONG" else 0.) if outcome else None,
                        "metric_reason": None if outcome else "NOT_EVALUATED"}
                    point_rows.append(row)
                    preparation = decode_output(load(self.book.path("prepare/"+slot))["attempts"][0]["output"])
                    details[slot] = {"policy": policy, "raw_reply": raw["reply"] if raw else None,
                                     "context": {"trace": preparation.get("trace"), "aux": preparation.get("aux")},
                                     "shared_sha256": snapshots[point["id"]]["sha256"]}
            rows.extend(point_rows)
            points_complete += int(len(point_rows) == len(self.plan)*self.request["repeats"])
        progress = {"points_total": len(self.reservation["points"]), "points_complete": points_complete,
                    "decision_slots_total": len(self.reservation["points"])*len(self.plan)*self.request["repeats"],
                    "decision_slots_complete": len(rows), "api_attempts": self.calls.quota.attempts(self.run_id)}
        result = result_document(self.job, status["state"], sorted(executed), progress, rows, status["error"])
        result.update(retry_at=status.get("retry_at"), snapshots=snapshots, policy_details=details,
                      outcome_points=sum(self.book.complete("outcome/"+p["id"]) for p in self.reservation["points"]),
                      input_snapshot_scope="SEALED_RESOURCE_AND_POINT_MANIFEST; SHARED_REPORT_HASHES_PER_POINT")
        return result
