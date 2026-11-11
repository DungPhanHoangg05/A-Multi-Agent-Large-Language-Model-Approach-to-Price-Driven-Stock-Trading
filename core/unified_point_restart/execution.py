"""Cold verifier cho tập active, kiểm sequence toàn ledger trước khi bỏ raw đã nghỉ."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any
from core.historical_evaluation_journal import load
from core.unified_contracts import SharedSnapshot, digest
from core.prior_run_lock import PriorRunLock
from core.unified_execution import StageBook, raw_record
from core.unified_execution_transport import wire_state, check_usage, parsed, body_for, Deferred, Uncertain, Exhausted
from core.unified_live.execution import HostedRunner, checked_raw, record_for
from core.unified_protocol import ordered_branches
from core.variant_registry import get_variant


def verify(directory: Path, identity: dict, methods: Any, *, require_complete: bool = True, retired: dict[str, str] | None = None) -> dict[str, Any]:
    """Cold consumer không client/provider: dựng lại metadata, raw, policy và barrier."""
    import json
    from core.unified_experiment import validate_outcome
    state = wire_state(directory)
    if state["identity"]["signature"] != digest(identity) or state["identity"]["mode"] != identity["mode"]:
        raise ValueError("Wire khác identity hosted")
    all_rows = state["rows"]
    retired = retired or {}
    if not set(retired) <= {row["id"] for row in all_rows}:
        raise ValueError("Thiếu raw HTTP đã nghỉ")
    for row in all_rows:
        if row["id"] in retired and digest(row) != retired[row["id"]]:
            raise ValueError("Raw HTTP đã nghỉ khác bằng chứng reset")
    rows = all_rows
    if len({r["id"] for r in rows}) != len(rows) or [r["sequence"] for r in rows] != list(range(len(rows))):
        raise ValueError("Wire trùng UUID hoặc sai thứ tự")
    rows = [row for row in all_rows if row["id"] not in retired]
    book = StageBook(directory, identity, verify_only=True)
    records, outcomes, used, done = [], {}, set(), 0
    allowed = set()
    planned = [p for p in identity["points"] if p["id"] == identity["smoke_point_id"]] if identity["phase"] == "SMOKE" else identity["points"]
    for index, point in enumerate(identity["points"]):
        if point not in planned:
            continue
        if not book.complete("outcome/" + point["id"]):
            if require_complete:
                raise ValueError("Thiếu planned point: " + point["id"])
            continue
        org = 1 + index % 5
        doc = book.execute("shared/" + point["id"], {"point": point, "org": org}, None)
        snapshot = SharedSnapshot.create(doc["point"], 0, doc["payload"], doc["provenance"])
        if doc["point"] != point:
            raise ValueError("Shared sai planned point")
        if identity.get("real_graph", True):
            for role in ("indicator", "pattern", "trend", "full"):
                graph_slot = f"graph/{point['id']}/{role}"
                graph_doc = load(book.path(graph_slot))
                output = book.execute(graph_slot, graph_doc["inputs"], None)
                fields = (role + "_report",) if role != "full" else ("alpha_report", "sentiment_report", "sentiment_data")
                if any(output[k] != doc["payload"][k] for k in fields):
                    raise ValueError("Shared đổi graph report/alpha/sentiment")
                if role in ("pattern", "trend"):
                    allowed.add(graph_slot)
                    candidates = [r for r in rows if r["slot"] == graph_slot]
                    if not 1 <= len(candidates) <= 3 or any(r["org"] != org or r["attempt"] != graph_doc["attempts"][0]["attempt_id"] for r in candidates):
                        raise ValueError("Vision sai shard/attempt cap/UUID")
                    for row in candidates:
                        body = row["body"]
                        if {k: v for k, v in body.items() if k != "messages"} != identity["vision_options"] or row["base_sha256"] != digest(body):
                            raise ValueError("Vision đổi body/model/options")
                        images = [part["image_url"]["url"] for m in body["messages"] if type(m["content"]) is list
                                  for part in m["content"] if part["type"] == "image_url"]
                        if images != ["data:image/png;base64," + doc["payload"][role + "_image"]]:
                            raise ValueError("Ảnh HTTP không khớp snapshot PIT")
                        check_usage(row)
                    if candidates[-1]["status"] != 200:
                        raise ValueError("Vision thiếu raw200")
                    parsed(candidates[-1]["body"], json.loads(candidates[-1]["response"]))
        required = []
        previous = load(book.path("shared/" + point["id"]))["attempts"][0]["completed_at"]
        for repeat in range(identity["repeats"]):
            outputs = {}
            for variant in ordered_branches(index * 3 + repeat):
                slot = f"forecast/{point['id']}/u0/r{repeat}/{variant}"
                allowed.add(slot)
                deps = {k: outputs[k] for k in get_variant(variant).dependencies}
                parents = {"shared_sha256": snapshot.sha256, "dependencies": {k: digest(v) for k, v in deps.items()}, "org": org}
                prepared = book.execute("prepare/" + slot, parents, None)
                methods.validate(variant, snapshot, prepared, repeat)
                record = book.execute(slot, {**parents, "prepared": prepared}, None)
                stamp = load(book.path(slot))["attempts"][0]
                prep_stamp = load(book.path("prepare/" + slot))["attempts"][0]
                if previous > prep_stamp["started_at"] or prep_stamp["completed_at"] > stamp["started_at"]:
                    raise ValueError("Thứ tự thực sai counterbalance/DAG")
                previous = stamp["completed_at"]
                raw = record["forecast"]["raw"]
                if prepared["request"] is not None:
                    checked_raw(rows, slot, org, prepared["request"], raw)
                    if any(r["attempt"] != stamp["attempt_id"] for r in rows if r["slot"] == slot):
                        raise ValueError("HTTP khác UUID checkpoint")
                    if raw["source_request_id"] in used:
                        raise ValueError("Reuse response qua repeat/variant")
                    used.add(raw["source_request_id"])
                elif raw is not None or any(r["slot"] == slot for r in rows):
                    raise ValueError("Bypass không được gửi HTTP")
                if record != record_for(point, snapshot, variant, repeat, prepared, raw, deps, methods):
                    raise ValueError("Metadata/raw/policy khác nguồn")
                outputs[variant] = record
                records.append(record)
                required.append(slot)
        value = book.execute("outcome/" + point["id"], {"forecast_slots": required}, None)
        if previous > load(book.path("outcome/" + point["id"]))["attempts"][0]["started_at"]:
            raise ValueError("Outcome mở trước barrier")
        if identity["phase"] == "SMOKE":
            if value != {"point_id": point["id"], "status": "SMOKE_NO_QUERY_PAYOFF"}:
                raise ValueError("Smoke không được nhập nhãn query")
        else:
            validate_outcome(point, value)
            outcomes[point["id"]] = value
        done += 1
    if require_complete and any(row["slot"] not in allowed for row in rows):
        raise ValueError("HTTP ngoài planned slots")
    if any(row["epoch"] != identity["epoch"] for row in all_rows) or len(all_rows) > identity.get("attempt_cap_total", 7956):
        raise ValueError("HTTP sai epoch hoặc vượt trần phase")
    return {"status": "PASS_U08_" + identity["phase"] if done == len(planned) else "PARTIAL_U08",
        "phase": identity["phase"], "planned_points": len(planned), "complete_points": done,
        "forecast_slots": len(records), "http_attempts": len(all_rows), "active_http_attempts": len(rows), "retired_http_attempts": len(retired), "raw_decision_responses": len(used),
        "records_sha256": digest(records), "outcomes_sha256": digest(outcomes), "api": identity["mode"] == "HOSTED",
        "native_rowwise_causal_gate": "FAIL", "whole_system_causal_gate": "NOT_CERTIFIED"}


class RestartRunner(HostedRunner):
    """Runner active dùng raw của generation hiện hành cho kiểm forecast."""
    def tick(self, upstream: Any, outcome: Any) -> dict[str, Any]:
        """Chỉ mở oracle khi đủ mọi forecast; UNKNOWN không tự retry hoặc bỏ qua điểm."""
        waiting, blocked = {}, {}
        with PriorRunLock(self.directory, digest(self.identity)):
            self.calls.refresh()
            book = StageBook(self.directory, self.identity)
            for org in range(1, 6):
                for index, point in enumerate(self.points):
                    if 1 + index % 5 != org or point not in self.selected or book.complete("outcome/" + point["id"]):
                        continue
                    try:
                        shared_doc = book.execute("shared/" + point["id"], {"point": point, "org": org},
                            lambda _: upstream.shared(book, deepcopy(point), org))
                        snapshot = SharedSnapshot.create(shared_doc["point"], 0, shared_doc["payload"], shared_doc["provenance"])
                        if snapshot.document()["point"] != point:
                            raise ValueError("Shared sai point")
                        required = []
                        for repeat in range(self.identity["repeats"]):
                            outputs = {}
                            for variant in ordered_branches(index * 3 + repeat):
                                slot = f"forecast/{point['id']}/u0/r{repeat}/{variant}"
                                deps = {k: deepcopy(outputs[k]) for k in get_variant(variant).dependencies}
                                parents = {"shared_sha256": snapshot.sha256, "dependencies": {k: digest(v) for k, v in deps.items()}, "org": org}
                                prepared = book.execute("prepare/" + slot, parents,
                                    lambda _: self.methods.prepare(variant, snapshot, deepcopy(deps), repeat))
                                self.methods.validate(variant, snapshot, prepared, repeat)
                                def invoke(attempt: str) -> dict:
                                    """Raw và policy dùng đúng request của slot này, kể cả khi fallback không HTTP."""
                                    raw = None
                                    if prepared["request"] is not None:
                                        request = prepared["request"]
                                        reply, row = self.calls.call(slot, org, body_for(request), attempt)
                                        raw = raw_record(request, row, reply)
                                    return record_for(point, snapshot, variant, repeat, prepared, raw, deps, self.methods)
                                def validate(record: dict) -> None:
                                    """Không tin complete journal nếu raw hoặc parent/policy bị sửa."""
                                    raw = record["forecast"]["raw"]
                                    if prepared["request"] is not None:
                                        checked_raw(self.calls.active_rows(), slot, org, prepared["request"], raw)
                                    elif raw is not None:
                                        raise ValueError("Fallback không được chứa raw API")
                                    if record != record_for(point, snapshot, variant, repeat, prepared, raw, deps, self.methods):
                                        raise ValueError("Forecast/policy không tái lập")
                                outputs[variant] = book.execute(slot, {**parents, "prepared": prepared}, invoke, validate=validate)
                                required.append(slot)
                        if len(required) != 8 * self.identity["repeats"] or not all(book.complete(s) for s in required):
                            raise ValueError("Outcome vẫn khóa vì chưa đủ forecast durable")
                        def label(_: str) -> dict:
                            """Smoke không đọc payoff; research gọi canonical oracle sau barrier này."""
                            if self.identity["phase"] == "SMOKE":
                                return {"point_id": point["id"], "status": "SMOKE_NO_QUERY_PAYOFF"}
                            value = outcome(deepcopy(point))
                            from core.unified_experiment import validate_outcome
                            validate_outcome(point, value)
                            return value
                        book.execute("outcome/" + point["id"], {"forecast_slots": required}, label)
                    except Deferred as error:
                        waiting[org] = error.until
                        break
                    except (Uncertain, Exhausted) as error:
                        blocked[org] = {"kind": type(error).__name__, "point_id": point["id"]}
                        break
            complete = sum(book.complete("outcome/" + p["id"]) for p in self.selected)
            return {"version": "unified_collection_progress_v1", "phase": self.identity["phase"], "api": self.identity["mode"] == "HOSTED",
                "planned_points": len(self.selected), "complete_points": complete, "planned_forecasts": len(self.selected) * 8 * self.identity["repeats"],
                "waiting": waiting, "blocked": blocked, "status": "COMPLETE" if complete == len(self.selected) else "PENDING"}
