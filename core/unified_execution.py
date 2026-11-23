"""Điều phối paired U07 theo năm org, checkpoint từng node và barrier đủ24 slots."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from core.historical_evaluation_journal import RunBook, load, save
from core.prior_run_lock import PriorRunLock, utc_now
from core.prior_stage_journal import encode_output, decode_output
from core.unified_contracts import SharedSnapshot, digest
from core.unified_execution_transport import Deferred, Uncertain, Exhausted, DurableCalls, body_for, parsed
from core.unified_protocol import ordered_branches
from core.variant_registry import get_variant


class StageBook(RunBook):
    """Resume cùng UUID; callback chỉ là phép thuần hoặc DurableCalls chống gửi lại UNKNOWN."""
    def __init__(self, *args: Any, hook: Callable[[str], None] = lambda _: None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.hook = hook

    def execute(self, slot: str, inputs: dict[str, Any], function: Any, *, validate: Any = None) -> dict[str, Any]:
        """Không dùng RunBook.reconcile để reset HTTP cap hoặc thay UUID sau crash."""
        path = self.path(slot)
        if path.exists():
            doc = load(path)
            if (doc["signature"] != self.signature or doc["run_uuid"] != self.uuid or doc["slot"] != slot
                    or doc["inputs"] != inputs or doc["inputs_sha256"] != digest(inputs)
                    or len(doc["attempts"]) != 1):
                raise ValueError("Stage khác source/parents/UUID đã durable")
            attempt = doc["attempts"][0]
            if attempt["status"] == "complete":
                return super().execute(slot, inputs, function, validate=validate)
            if attempt["status"] != "unknown" or self.verify_only:
                raise ValueError("Stage chưa hoàn tất")
        else:
            if self.verify_only:
                raise ValueError("Thiếu stage durable")
            attempt = {"attempt_id": str(uuid4()), "started_at": utc_now(), "status": "unknown",
                       "output": None, "output_sha256": None, "authorization": None}
            doc = {"signature": self.signature, "run_uuid": self.uuid, "slot": slot,
                   "inputs": deepcopy(inputs), "inputs_sha256": digest(inputs), "attempts": [attempt]}
            save(path, doc)
        output = function(attempt["attempt_id"])
        if validate:
            validate(output)
        self.hook("before_complete:" + slot)
        encoded = encode_output(output)
        attempt.update(status="complete", output=encoded, output_sha256=digest(encoded), completed_at=utc_now())
        save(path, doc)
        return deepcopy(output)


def raw_record(request: dict[str, Any], row: dict[str, Any], reply: Any) -> dict[str, Any]:
    """Forecast tham chiếu UUID raw HTTP riêng từng repeat, không dùng response cached từ nhánh khác."""
    return {"request_sha256": digest(request), "source_request_id": row["id"],
            "source_sha256": digest(row), "reply": reply}


class PairedStudyRunner:
    """Một vòng cooperative; org bị quota/UNKNOWN không chặn bốn org còn lại."""
    def __init__(self, directory: Path, identity: dict[str, Any], calls: DurableCalls,
                 methods: Any, *, hook: Callable[[str], None] = lambda _: None) -> None:
        if (identity.get("mode") != "CONTROL_ONLY" or identity.get("repeats") != 3
                or identity.get("realizations") != 1 or calls.signature != digest(identity)):
            raise ValueError("U07 khóa control-only, ba repeat và một realization")
        self.directory, self.identity, self.calls, self.methods = directory, deepcopy(identity), calls, methods
        self.hook = hook
        self.points = self.identity["points"]
        if not self.points or len({p["id"] for p in self.points}) != len(self.points):
            raise ValueError("Thiếu hoặc trùng cohort")

    def tick(self, upstream: Any, outcomes: Callable[[dict[str, Any]], dict[str, Any]]) -> dict[str, Any]:
        """Mỗi org xử lý điểm đầu chưa xong; giữ nguyên shard theo global point index."""
        waiting, blocked = {}, {}
        with PriorRunLock(self.directory, digest(self.identity)):
            self.calls.refresh()
            book = StageBook(self.directory, self.identity, hook=self.hook)
            for org in range(1, 6):
                for index in range(org - 1, len(self.points), 5):
                    point = self.points[index]
                    if book.complete("outcome/" + point["id"]):
                        continue
                    try:
                        shared_doc = book.execute("shared/" + point["id"], {"point": point, "org": org},
                            lambda _: upstream.shared(book, deepcopy(point), org))
                        snapshot = SharedSnapshot.create(shared_doc["point"], 0, shared_doc["payload"], shared_doc["provenance"])
                        if snapshot.document()["point"] != point:
                            raise ValueError("Upstream trả sai point")
                        required = []
                        for repeat in range(3):
                            outputs = {}
                            for variant in ordered_branches(index * 3 + repeat):
                                slot = f"forecast/{point['id']}/u0/r{repeat}/{variant}"
                                dependencies = {k: deepcopy(outputs[k]) for k in get_variant(variant).dependencies}
                                parents = {"shared_sha256": snapshot.sha256,
                                           "dependencies": {k: digest(v) for k, v in dependencies.items()}, "org": org}
                                prepared = book.execute("prepare/" + slot, parents,
                                    lambda _: self.methods.prepare(variant, snapshot, deepcopy(dependencies), repeat))
                                self.methods.validate(variant, snapshot, prepared, repeat)
                                def invoke(attempt: str) -> dict[str, Any]:
                                    raw = None
                                    if prepared["request"] is not None:
                                        request = prepared["request"]
                                        reply, row = self.calls.call(slot, org, body_for(request), attempt)
                                        raw = raw_record(request, row, reply)
                                    # Renderer/policy chín mã thuộc namespace của methods.
                                    record = {
                                        "forecast": {"point_id": point["id"], "variant": variant, "repeat": repeat,
                                            "realization": 0, "shared_sha256": snapshot.sha256, "raw": raw,
                                            "dependency_hashes": parents["dependencies"]},
                                        "policy": self.methods.resolve(variant, prepared, raw, dependencies)}
                                    return record
                                def validate(record: dict[str, Any]) -> None:
                                    raw = record["forecast"]["raw"]
                                    if prepared["request"] is None:
                                        if raw is not None:
                                            raise ValueError("Fallback không được có raw API")
                                    else:
                                        matched = [r for r in self.calls.state["rows"] if r["id"] == raw["source_request_id"]]
                                        if len(matched) != 1 or matched[0]["status"] != 200 or matched[0]["slot"] != slot or matched[0]["org"] != org:
                                            raise ValueError("Raw không thuộc forecast/shard đã durable")
                                        row = matched[0]
                                        if (row["base_sha256"] != digest(body_for(prepared["request"]))
                                                or raw != raw_record(prepared["request"], row, parsed(row["body"], json_load(row["response"])))):
                                            raise ValueError("Raw không khớp request/reply")
                                    expected = {"forecast": {"point_id": point["id"], "variant": variant, "repeat": repeat,
                                        "realization": 0, "shared_sha256": snapshot.sha256, "raw": raw,
                                        "dependency_hashes": parents["dependencies"]},
                                        "policy": self.methods.resolve(variant, prepared, raw, dependencies)}
                                    if record != expected:
                                        raise ValueError("Forecast/policy complete không tái lập")
                                output = book.execute(slot, {**parents, "prepared": prepared}, invoke, validate=validate)
                                outputs[variant] = output
                                required.append(slot)
                        if len(required) != 24 or not all(book.complete(s) for s in required):
                            raise ValueError("Chưa đủ24 forecast durable, khóa nhãn query")
                        book.execute("outcome/" + point["id"], {"forecast_slots": required}, lambda _: outcomes(deepcopy(point)))
                    except Deferred as error:
                        waiting[org] = error.until
                        break
                    except (Uncertain, Exhausted) as error:
                        blocked[org] = type(error).__name__
                        break
            done = sum(book.complete("outcome/" + p["id"]) for p in self.points)
            return {"mode": "CONTROL_ONLY", "planned": len(self.points), "complete": done,
                    "waiting": waiting, "blocked": blocked, "api": False,
                    "status": "COMPLETE" if done == len(self.points) else "PENDING"}


def verify_execution(directory: Path, identity: dict[str, Any], methods: Any) -> dict[str, Any]:
    """Đọc và dựng lại policy/raw/parents/barrier; không provider/model/client hoặc ghi file."""
    from core.unified_execution_transport import REPAIR, wire_state, check_usage
    state = wire_state(directory)
    if state["identity"]["signature"] != digest(identity) or state["identity"]["mode"] != "CONTROL_ONLY":
        raise ValueError("Wire khác identity")
    rows = state["rows"]
    if len({r["id"] for r in rows}) != len(rows) or [r["sequence"] for r in rows] != list(range(len(rows))):
        raise ValueError("Wire UUID/order không duy nhất")
    for row in rows:
        check_usage(row)
        if row["epoch"] != state["identity"]["epoch"] or row["org"] not in range(1, 6):
            raise ValueError("Wire đổi epoch/org")
    used, count, allowed_slots = set(), 0, set()
    book = StageBook(directory, identity, verify_only=True)
    for index, point in enumerate(identity["points"]):
        org = 1 + index % 5
        shared = book.execute("shared/" + point["id"], {"point": point, "org": org}, None)
        snapshot = SharedSnapshot.create(shared["point"], 0, shared["payload"], shared["provenance"])
        if snapshot.document()["point"] != point:
            raise ValueError("Shared sai planned point")
        if identity.get("real_graph"):
            for role in ("indicator", "pattern", "trend", "full"):
                slot = f"graph/{point['id']}/{role}"
                stage = load(book.path(slot))
                output = book.execute(slot, stage["inputs"], None)
                if role in ("indicator", "pattern", "trend") and output[role + "_report"] != shared["payload"][role + "_report"]:
                    raise ValueError("Snapshot không nhận report đúng graph stage")
                if role == "full" and any(output[k] != shared["payload"][k] for k in ("alpha_report", "sentiment_report", "sentiment_data")):
                    raise ValueError("Snapshot thay alpha/sentiment native sau graph")
                if role in ("pattern", "trend"):
                    allowed_slots.add(slot)
                    candidates = [r for r in rows if r["slot"] == slot]
                    if not 1 <= len(candidates) <= 3 or any(r["org"] != org or r["attempt"] != stage["attempts"][0]["attempt_id"] for r in candidates):
                        raise ValueError("Vision sai shard/UUID hoặc trần3")
                    image = shared["payload"][role + "_image"]
                    for row in candidates:
                        body = row["body"]
                        options = {k: v for k, v in body.items() if k != "messages"}
                        if options != identity["vision_options"] or row["base_sha256"] != digest(body):
                            raise ValueError("Vision đổi model/options/body")
                        images = [part["image_url"]["url"] for m in body["messages"] if type(m["content"]) is list
                                  for part in m["content"] if part["type"] == "image_url"]
                        if images != ["data:image/png;base64," + image]:
                            raise ValueError("Vision nhận ảnh khác snapshot PIT")
                    if candidates[-1]["status"] != 200:
                        raise ValueError("Graph thiếu raw200")
                    parsed(candidates[-1]["body"], json_load(candidates[-1]["response"]))
        required = []
        previous_completed = load(book.path("shared/" + point["id"]))["attempts"][0]["completed_at"]
        for repeat in range(3):
            outputs = {}
            for variant in ordered_branches(index * 3 + repeat):
                slot = f"forecast/{point['id']}/u0/r{repeat}/{variant}"
                allowed_slots.add(slot)
                dependencies = {k: outputs[k] for k in get_variant(variant).dependencies}
                parents = {"shared_sha256": snapshot.sha256, "dependencies": {k: digest(v) for k, v in dependencies.items()}, "org": org}
                prepared = book.execute("prepare/" + slot, parents, None)
                methods.validate(variant, snapshot, prepared, repeat)
                record = book.execute(slot, {**parents, "prepared": prepared}, None)
                stage = load(book.path(slot))["attempts"][0]
                prep_stage = load(book.path("prepare/" + slot))["attempts"][0]
                if previous_completed > prep_stage["started_at"] or prep_stage["completed_at"] > stage["started_at"]:
                    raise ValueError("Thứ tự thực không khớp counterbalance/DAG đã khóa")
                previous_completed = stage["completed_at"]
                raw = record["forecast"]["raw"]
                if prepared["request"] is not None:
                    candidates = [r for r in rows if r["slot"] == slot]
                    attempt = load(book.path(slot))["attempts"][0]["attempt_id"]
                    if not 1 <= len(candidates) <= 3 or any(r["org"] != org or r["attempt"] != attempt for r in candidates):
                        raise ValueError("Forecast HTTP sai org hoặc attempt cap")
                    base = body_for(prepared["request"])
                    for row in candidates:
                        actual = deepcopy(base)
                        if row["repair"]:
                            actual["messages"][0]["content"] += REPAIR
                        if row["body"] != actual or row["base_sha256"] != digest(base):
                            raise ValueError("Request/schema/model/options đổi trong raw HTTP")
                    row = candidates[-1]
                    reply = parsed(row["body"], json_load(row["response"]))
                    if row["status"] != 200 or raw != raw_record(prepared["request"], row, reply):
                        raise ValueError("Forecast không khớp raw HTTP cuối")
                    if row["id"] in used:
                        raise ValueError("Một response dùng lại giữa nhánh/repeat")
                    used.add(row["id"])
                elif raw is not None or any(r["slot"] == slot for r in rows):
                    raise ValueError("Fallback có HTTP hoặc raw response ngoài registry")
                if methods.resolve is not None:
                    if record["policy"] != methods.resolve(variant, prepared, raw, dependencies):
                        raise ValueError("Policy không tái lập từ raw và dependency")
                    if record["forecast"] != {"point_id": point["id"], "variant": variant, "repeat": repeat,
                            "realization": 0, "shared_sha256": snapshot.sha256, "raw": raw, "dependency_hashes": parents["dependencies"]}:
                        raise ValueError("Forecast metadata khác shared/repeat/dependency")
                outputs[variant] = record
                required.append(slot)
                count += 1
        label = book.execute("outcome/" + point["id"], {"forecast_slots": required}, None)
        started = load(book.path("outcome/" + point["id"]))["attempts"][0]["started_at"]
        if any(load(book.path(slot))["attempts"][0]["completed_at"] > started for slot in required):
            raise ValueError("Nhãn được mở trước barrier durable")
        if label != {"point_id": point["id"], "status": "WITHHELD_CONTROL_NO_QUERY_PAYOFF"}:
            raise ValueError("U07 không được nhận nhãn thị trường control thành kết quả")
    if any(r["slot"] not in allowed_slots for r in rows):
        raise ValueError("Có HTTP ngoài planned graph/forecast")
    return {"status": "PASS_U07_PAIRED_CONTROL_REPLAY", "points": len(identity["points"]),
            "forecast_slots": count, "mock_http_attempts": len(rows), "distinct_decision_responses": len(used),
            "api": False, "native_rowwise_causal_gate": "FAIL", "whole_system_causal_gate": "NOT_CERTIFIED"}


def json_load(raw: str) -> Any:
    """Đọc raw JSON, không gỡ Markdown hoặc sửa reply."""
    import json
    return json.loads(raw)
