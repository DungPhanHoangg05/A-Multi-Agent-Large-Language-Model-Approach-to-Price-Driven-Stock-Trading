"""Chạy đối chứng nghiên cứu theo ledger FIN09 và lưu checkpoint theo slot."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Callable

from core.finalize_budget_archive import Archive, fingerprints
from core.finalize_budget_quota import ORG
from core.finalize_budget_study import NAMESPACE, VISION, StudyProvider
from core.finalize_serving_profile import method_profile
from core.historical_evaluation_journal import load
from core.historical_signals import snapshot_payload
from core.prior_run_lock import PriorRunLock
from core.serving_runtime.quota import Quota, Stopped, Unknown
from core.serving_runtime.transport import Calls
from core.unified_contracts import SharedSnapshot, digest
from core.unified_execution import StageBook, raw_record
from core.unified_execution_transport import MockHTTP, body_for, parsed
from core.unified_protocol import ordered_branches
from core.variant_registry import get_variant


class PlannedCalls:
    """Đối chiếu ledger tại ranh giới transport, tái dùng vision với đúng raw U08."""

    def __init__(self, directory: Path, identity: dict, plans: dict, archive: Archive,
                 sender: MockHTTP, clock: Callable[[], float], guard: Callable[[], None],
                 hook: Callable[[str], None]) -> None:
        if type(sender) is not MockHTTP or identity["org_slot"] != ORG:
            raise ValueError("Lượt FIN10 chỉ nhận transport đối chứng và một org")
        self.plans, self.archive = plans, archive
        models = tuple(sorted({row["model"] for row in plans.values()}))
        self.transports = {model: Calls(directory, digest(identity), Quota(directory/"quota"/f"model-{index}.sqlite3", clock),
                                        sender, guard, clock=clock, hook=hook, total_prompt_guard=True)
                           for index, model in enumerate(models)}

    def rows(self, slot: str) -> list[dict]:
        """Đọc attempt durable của đúng model và slot."""
        return self.transports[self.plans[slot]["model"]]._rows(slot)[1]

    def archived_vision(self, slot: str) -> dict:
        """Xác thực UUID, epoch, attempt và HTTP200 khớp ledger đã khóa."""
        row = self.plans[slot]
        old = row["old"]
        if (row["role"] not in VISION or row["phase"] != "RESEARCH" or row["state"] != "REUSE"
                or not old or old != self.archive.candidate(slot) or old["fingerprints"] != row["fingerprints"]
                or old["repair"] or old["status"] != 200 or old["epoch"] != self.archive.identity["epoch"]):
            raise ValueError("Raw U08 chưa đủ bằng chứng reuse vision")
        attempt, _ = self.archive.stage(slot)
        if attempt["attempt_id"] != old["attempt"] or self.rows(slot):
            raise ValueError("Reuse vision khác stage U08 hoặc trùng HTTP mới")
        return self.archive.raw(old["id"], old["sha256"])

    def call(self, slot: str, body: dict, attempt: str) -> tuple[Any, dict]:
        """Chặn drift trước reserve và giữ new/fixture riêng với raw tái dùng."""
        row = self.plans[slot]
        actual = fingerprints(body)
        expected = row["fingerprints"]
        if expected is None or body["model"] != row["model"]:
            raise ValueError("Request xuất hiện ngoài ledger FIN09")
        if row["new_wire_proof"] == "CONTROL_BODY_DEPENDS_ON_NEW_RESPONSES":
            keys = ("options", "schema")
        else:
            keys = tuple(actual)
        if any(actual[key] != expected[key] for key in keys):
            raise ValueError("Wire hoặc model/schema khác ledger FIN09")
        if row["state"] == "REUSE":
            wire = self.archived_vision(slot)
            return parsed(wire["body"], json.loads(wire["response"])), wire
        if row["state"] == "UNKNOWN":
            raise Unknown("Cần đối soát UUID đã khóa trong FIN09")
        if row["state"] != "NEW":
            raise ValueError("Slot bypass không được dispatch")
        return self.transports[row["model"]].call(slot, body, attempt)

    def bypass(self, slot: str, prepared: dict) -> None:
        """MT còn có thể bypass nếu Fact Anchor cùng repeat không đạt điều kiện."""
        row = self.plans[slot]
        anchor = prepared["aux"].get("anchor")
        if (row["state"] != "BYPASS" and not (row["state"] == "NEW" and row["role"] == "MT_BICL"
                and row.get("conditional_support") == "REQUIRES_VALID_SAME_REPEAT_FACT_ANCHOR"
                and anchor is not None and not anchor["policy"]["fact_assertions_valid"])) or self.rows(slot):
            raise ValueError("Bỏ qua request ngoài điều kiện FIN09 hoặc đã có raw")


class OfflineStudyRunner:
    """Giữ một upstream, cùng repeat và thứ tự đã khóa ở cohort FIN02."""

    def __init__(self, directory: Path, release: dict, budget: dict, cohort: list[dict],
                 selected: list[str], phase: str, provider: StudyProvider, archive: Archive,
                 sender: MockHTTP, clock: Callable[[], float], hook: Callable[[str], None] = lambda _: None) -> None:
        self.ordinals = {point["id"]: i for i, point in enumerate(cohort)}
        self.points = [point for point in cohort if point["id"] in selected]
        if (phase not in {"RESEARCH", "SMOKE"} or selected != [point["id"] for point in self.points]
                or not selected or (phase == "SMOKE" and selected != [budget["smoke_point_id"]])
                or budget["namespace"] != NAMESPACE or budget["execution_permitted"] is not False):
            raise ValueError("Lịch hoặc scope đối chứng khác khóa FIN09")
        self.directory, self.provider = directory, provider
        self.read_only = False
        self.repeats = 1 if phase == "SMOKE" else 3
        self.identity = {"namespace": NAMESPACE, "scope": "OFFLINE_FIXTURE", "phase": phase, "points": self.points,
                         "org_slot": ORG, "repeats": self.repeats, "realizations": 1,
                         "release_sha256": digest(release), "budget_sha256": digest(budget)}
        selected_set = set(selected)
        plans = {row["slot"]: row for row in budget["slots"]
                 if row["phase"] == phase and row["slot"].split("/")[1] in selected_set}
        if len(plans) != len(self.points)*(len(VISION)+8*self.repeats):
            raise ValueError("Ledger thiếu slot của lịch đối chứng")
        self.calls = PlannedCalls(directory, self.identity, plans, archive, sender, clock, self.guard_dispatch, hook)

    def guard(self) -> None:
        """Dừng tại biên stage và trước reserve; raw đang nhận vẫn được lưu."""
        if (self.directory/"stop.request").exists():
            raise Stopped()

    def guard_dispatch(self) -> None:
        """Cold replay chỉ được dùng attempt đã durable."""
        self.guard()
        if self.read_only:
            raise ValueError("Cold replay không được reserve hoặc gửi request mới")

    def vision_proofs(self, book: StageBook, point: dict) -> dict:
        """Ghép bằng chứng của từng report với raw đúng slot, kể cả lúc cold replay."""
        identifier = point["id"]
        window = digest(snapshot_payload(self.provider.prefix(point).tail(45)))
        proof = {}
        for role in VISION:
            slot = f"graph/{identifier}/{role}"
            plan = self.calls.plans[slot]
            dep = plan["dependency_receipts"]
            if window != dep["new_price_window_sha256"]:
                raise ValueError("Cửa sổ giá vision khác ledger")
            stage = load(book.path(slot))["attempts"][0]
            if plan["state"] == "REUSE":
                if dep["old_price_window_sha256"] != window:
                    raise ValueError("Cửa sổ giá reuse khác dữ liệu U08")
                wire = self.calls.archived_vision(slot)
            else:
                rows = self.calls.rows(slot)
                if not rows or not 1 <= len(rows) <= 3 or rows[-1]["attempt"] != stage["attempt_id"]:
                    raise ValueError("Thiếu attempt mới của vision")
                wire = rows[-1]
            if stage["status"] != "complete" or wire["status"] != 200 or fingerprints(wire["body"]) != plan["fingerprints"]:
                raise ValueError("Stage vision thiếu raw HTTP200 đúng wire")
            proof[role] = {"state": plan["state"], "raw_id": wire["id"], "raw_sha256": digest(wire),
                           "epoch": wire.get("epoch", "OFFLINE_FIXTURE")}
        return proof

    def tick(self, *, read_only: bool = False) -> dict:
        """Ghi đủ slot hoặc dừng; replay chỉ kiểm lại checkpoint đã hoàn tất."""
        with PriorRunLock(self.directory/"worker", digest(self.identity)):
            self.read_only = read_only
            book = StageBook(self.directory/"journal", self.identity, verify_only=read_only)
            records = {}
            for point in self.points:
                self.guard()
                identifier = point["id"]
                self.provider.validate_point(point)
                doc = book.execute(f"shared/{identifier}", {"point": point},
                                   lambda _: self.provider.shared(book, deepcopy(point), self.calls))
                if doc["point"] != point or doc["realization"] != 0:
                    raise ValueError("Snapshot khác point hoặc realization đã khóa")
                snapshot = SharedSnapshot.create(point, 0, doc["payload"], doc["provenance"])
                vision = self.vision_proofs(book, point)
                slots = self.forecasts(book, point, snapshot)
                records[identifier] = {"shared_sha256": snapshot.sha256, "vision": vision, "forecasts": slots}
            return {"identity_sha256": digest(self.identity), "points": records, "outcomes_opened": 0}

    def forecasts(self, book: StageBook, point: dict, snapshot: SharedSnapshot) -> dict:
        """Tạo request từ snapshot và dependency của đúng repeat, kiểm cold policy."""
        completed = {}
        for repeat in range(self.repeats):
            outputs = {}
            for variant in ordered_branches(self.ordinals[point["id"]]*3+repeat):
                self.guard()
                slot = f"forecast/{point['id']}/u0/r{repeat}/{variant}"
                parents = {k: deepcopy(outputs[k]) for k in get_variant(variant).dependencies}
                hashes = {key: digest(value) for key, value in parents.items()}
                inputs = {"shared_sha256": snapshot.sha256, "dependency_hashes": hashes}
                prepared = book.execute("prepare/"+slot, inputs,
                                        lambda _: self.provider.prepare(variant, snapshot, parents, repeat))
                self.provider.validate_bound(variant, snapshot, parents, repeat, prepared)
                request = prepared["request"]

                def record(attempt: str) -> dict:
                    raw = None
                    if request is None:
                        self.calls.bypass(slot, prepared)
                    else:
                        reply, wire = self.calls.call(slot, body_for(request), attempt)
                        raw = raw_record(request, wire, reply)
                    return {"forecast": {**inputs, "point_id": point["id"], "variant": variant, "repeat": repeat,
                        "realization": 0, "profile": method_profile(variant), "raw": raw,
                        "request_sha256": digest(request) if request is not None else None},
                        "policy": self.provider.resolve_bound(variant, snapshot, parents, repeat, prepared, raw)}

                def validate(value: dict) -> None:
                    attempt = load(book.path(slot))["attempts"][0]["attempt_id"]
                    previous = self.read_only
                    self.read_only = True
                    try:
                        if value != record(attempt):
                            raise ValueError("Checkpoint lệch raw, repeat hoặc policy")
                    finally:
                        self.read_only = previous

                outputs[variant] = book.execute(slot, {**inputs, "prepared": prepared}, record, validate=validate)
                completed[slot] = digest(outputs[variant])
        return completed
