"""Điều phối offline chung, một RunBook và một evaluator cho mọi variant."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
import hashlib
from importlib.metadata import version
from pathlib import Path
import platform
from typing import Any, Callable
from uuid import UUID

from core.historical_evaluation_journal import RunBook, load, save
from core.prior_run_lock import PriorRunLock
from core.unified_contracts import ExperimentSpec, SharedSnapshot, checksum, digest, json_bytes
from core.unified_methods import MethodAdapters, resolve, validate_prepared
from core.variant_registry import execution_order, get_variant

ROOT = Path(__file__).resolve().parents[1]


def runtime_identity() -> dict[str, str]:
    """Chỉ đọc versions cục bộ, không tạo SDK/client hoặc kiểm mạng."""
    return {"python": platform.python_version(), **{name: version(name) for name in
            ("numpy", "pandas", "scipy", "TA-Lib", "langgraph", "langchain-core", "langchain-groq", "torch")}}


def source_identity(root: Path = ROOT) -> dict[str, str]:
    """Khóa toàn runtime Python hiện hành; không gán code mới vào receipt lịch sử."""
    paths = [p for folder in ("agents", "core", "data_manager", "utils") for p in (root / folder).rglob("*.py")]
    paths += [root / "default_config.py", root / "requirements-unified.lock.txt"]
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def outcome_from_frame(point: dict[str, Any], frame: Any, source_sha256: str) -> dict[str, Any]:
    """Chỉ gọi sau barrier; nhãn/P&L dùng oracle target_fields hiện hữu."""
    import pandas as pd
    from utils.target_contract import target_fields
    if not checksum(source_sha256):
        raise ValueError("Outcome thiếu hash nguồn giá")
    dates = pd.DatetimeIndex(frame.Datetime)
    if dates.has_duplicates or not dates.is_monotonic_increasing or dates.hasnans:
        raise ValueError("Lịch outcome không hợp lệ")
    index = int(dates.get_indexer([pd.Timestamp(point["cutoff"])])[0])
    if index < 0 or index + 3 >= len(frame):
        raise ValueError("Không có đủ ba phiên thực thi")
    return {"version": "unified_outcome_record_v1", "point_id": point["id"], "source_sha256": source_sha256,
            "dates": [str(d.date()) for d in dates[index:index + 4]],
            "target": target_fields(frame, index + 1, 3)}


def validate_outcome(point: dict[str, Any], outcome: dict[str, Any]) -> None:
    """Kiểm canonical arithmetic, horizon và quan hệ ngày trước evaluator."""
    from utils.target_contract import validate_target_record
    from core.unified_contracts import day
    if (set(outcome) != {"version", "point_id", "source_sha256", "dates", "target"}
            or outcome["version"] != "unified_outcome_record_v1" or outcome["point_id"] != point["id"]
            or not checksum(outcome["source_sha256"])):
        raise ValueError("Outcome sai identity")
    days = outcome["dates"]
    if type(days) is not list or len(days) != 4 or days[0] != point["cutoff"] or days != sorted(set(day(d) for d in days)):
        raise ValueError("Outcome không có đúng decision và ba phiên tiếp theo")
    target = outcome["target"]
    validate_target_record(target)
    if (target.get("label_contract_version") != "net_cycle_v1" or target["target_horizon_bars"] != 3
            or target["label_fee_each_side"] != .0025 or target["label_slippage_each_side"] != .001):
        raise ValueError("Outcome đổi hợp đồng kinh tế")
    json_bytes(outcome)


class OfflineResponses:
    """Bảng raw response đã khóa; không nhận callable HTTP hoặc tự sinh CASH."""
    def __init__(self, rows: dict[str, Any]) -> None:
        if type(rows) is not dict or any(type(row) is not dict for row in rows.values()):
            raise ValueError("Bảng response offline phải là object JSON")
        self.rows = deepcopy(rows)
        json_bytes(self.rows)
        ids = [row.get("source_request_id") for row in self.rows.values()]
        if any(type(value) is not str for value in ids):
            raise ValueError("Response thiếu UUID nguồn")
        if len(set(ids)) != len(ids):
            raise ValueError("Không dùng cùng response nguồn làm nhiều slot/repeat độc lập")
        self.calls: list[str] = []

    def take(self, slot: str, request: dict[str, Any]) -> dict[str, Any]:
        """Chỉ replay response có đúng request hash và UUID nguồn riêng với UUID RunBook."""
        record = deepcopy(self.rows.get(slot))
        if (type(record) is not dict or set(record) != {"request_sha256", "source_request_id", "reply", "source_sha256"}
                or record["request_sha256"] != digest(request) or not checksum(record["source_sha256"])):
            raise ValueError("Thiếu response offline hoặc request/source không khớp")
        UUID(record["source_request_id"])
        self.calls.append(slot)
        return record


def slot_id(point: str, realization: int, repeat: int, variant: str) -> str:
    """Slot không phụ thuộc UUID hoặc số lần mở lại tiến trình."""
    return f"forecast/{point}/u{realization}/r{repeat}/{variant}"


def make_record(point: dict[str, Any], snapshot: SharedSnapshot, variant: str, repeat: int,
                prepared: dict[str, Any], raw: dict[str, Any] | None, dependencies: dict[str, Any]) -> dict[str, Any]:
    """Lưu raw proposal riêng với action sau policy; parent dependency là hash đầy đủ."""
    if raw is not None:
        if (set(raw) != {"request_sha256", "source_request_id", "reply", "source_sha256"}
                or raw["request_sha256"] != digest(prepared["request"]) or not checksum(raw["source_sha256"])):
            raise ValueError("Raw response không khớp request/source")
        UUID(raw["source_request_id"])
    return {"forecast": {"version": "unified_forecast_record_v1", "point_id": point["id"],
        "variant": variant, "profile": get_variant(variant).profile, "repeat": repeat,
        "realization": snapshot.document()["realization"], "shared_sha256": snapshot.sha256,
        "request_sha256": digest(prepared["request"]) if prepared["request"] is not None else None,
        "raw": raw, "response_sha256": digest(raw) if raw is not None else None,
        "dependency_hashes": {key: digest(value) for key, value in dependencies.items()}},
        "policy": resolve(variant, prepared, raw, dependencies)}


def evaluate(spec: dict[str, Any], records: list[dict[str, Any]], outcomes: dict[str, Any]) -> dict[str, Any]:
    """Evaluator duy nhất; tài khoản reset theo symbol/fold/realization/repeat."""
    from core.backtest_engine import TestPoint, compute_account_metrics
    from utils.target_contract import target_record_fields
    groups: dict[str, list[Any]] = {}
    rows = []
    points = {p["id"]: p for p in spec["points"]}
    order = execution_order(spec["variants"])
    expected_slots = {(point, u, r, variant) for point in points for u in range(spec["realizations"])
                      for r in range(spec["repeats"]) for variant in order}
    actual_slots = [(v["forecast"]["point_id"], v["forecast"]["realization"], v["forecast"]["repeat"], v["forecast"]["variant"]) for v in records]
    if len(actual_slots) != len(expected_slots) or set(actual_slots) != expected_slots:
        raise ValueError("Evaluator thiếu hoặc trùng planned slot/common support")
    request_ids = [v["forecast"]["raw"]["source_request_id"] for v in records if v["forecast"]["raw"] is not None]
    if len(set(request_ids)) != len(request_ids):
        raise ValueError("Response nguồn bị tính nhiều lần trên các slot")
    for record in records:
        forecast, policy = record["forecast"], record["policy"]
        point = points[forecast["point_id"]]
        outcome = outcomes[point["id"]]
        validate_outcome(point, outcome)
        target, dates = outcome["target"], outcome["dates"]
        action = policy["final_action"]
        if action not in ("LONG", "CASH"):
            raise ValueError("Policy không có action kinh tế hợp lệ")
        prediction = "LONG" if action == "LONG" else "SHORT"
        correct = bool((prediction == "LONG") == (target["label_net"] == "UP"))
        key = "/".join((forecast["variant"], point["symbol"], point["fold"], str(forecast["realization"]), str(forecast["repeat"])))
        group = groups.setdefault(key, [])
        group.append(TestPoint(len(group) + 1, point["cutoff"], point["cutoff"], target["decision_close"], target["exit_close"],
            target["label_net"], target["net_return"] * 100., prediction, correct, "N/A", "N/A", prediction,
            correct, "N/A", "N/A", 0., 0., entry_open=target["entry_open"], exit_close=target["exit_close"],
            entry_time=dates[1], exit_time=dates[3], **target_record_fields(target)))
        rows.append({"point_id": point["id"], "symbol": point["symbol"], "fold": point["fold"],
            "cutoff": point["cutoff"], "variant": forecast["variant"], "profile": forecast["profile"],
            "role": get_variant(forecast["variant"]).role, "realization": forecast["realization"], "repeat": forecast["repeat"],
            "raw_proposal": policy["raw_proposal"], "final_action": action, "reason": policy["reason"],
            "bypass": policy["bypass"], "label_net": target["label_net"], "candidate_long_return": target["net_return"],
            "strategy_return": target["net_return"] if action == "LONG" else 0., "quality": point["quality"],
            "shared_sha256": forecast["shared_sha256"], "request_sha256": forecast["request_sha256"],
            "response_sha256": forecast["response_sha256"]})
    accounts = {key: asdict(compute_account_metrics(points)["full"]) for key, points in sorted(groups.items())}
    json_bytes(accounts)
    from core.free_pilot_statistics import classification
    metrics = {}
    for variant in order:
        for u in range(spec["realizations"]):
            for r in range(spec["repeats"]):
                selected = [row for row in rows if (row["variant"], row["realization"], row["repeat"]) == (variant, u, r)]
                p = [int(row["final_action"] == "LONG") for row in selected]
                y = [int(row["label_net"] == "UP") for row in selected]
                metric = classification(p, y, planned=len(points))
                negative = classification([1-v for v in p], [1-v for v in y])["f1_positive"]
                metric.update(f1_negative=negative, macro_f1=(negative + metric["f1_positive"]) / 2
                              if negative is not None and metric["f1_positive"] is not None else None,
                              long_rate=sum(p)/len(p) if p else None)
                metrics[f"{variant}/u{u}/r{r}"] = metric
    planned = len(spec["points"]) * spec["realizations"] * spec["repeats"] * len(order)
    if len(rows) != planned:
        raise ValueError("Thiếu common support, không seal summary từ nhánh thành công riêng")
    return {"version": "unified_result_v1", "mode": spec["mode"], "planned_slots": planned, "complete_slots": len(rows),
        "selected_variants": spec["variants"], "executed_variants": order, "points": len(spec["points"]),
        "account_unit": "SYMBOL_FOLD_REALIZATION_REPEAT", "return_unit": "FRACTION_IN_LEDGER_PERCENT_IN_ACCOUNT",
        "estimand": spec["estimand"], "missing_policy": spec["missing_policy"], "rows": rows, "accounts": accounts,
        "ledgers": {key: [asdict(point) for point in points] for key, points in sorted(groups.items())},
        "classification": metrics,
        "hosted_calls": 0, "native_rowwise_causal_gate": "FAIL",
        "scope": "OFFLINE_CONDITIONAL_ON_LOCKED_SHARED_AND_METHOD_ASSETS; NOT_A_HOSTED_OR_CAUSAL_RELEASE"}


class UnifiedRunner:
    """Một owner journal/lock; phương thức run chỉ tiêu thụ response offline đã khóa."""
    def __init__(self, root: Path, spec: ExperimentSpec, responses: OfflineResponses, *, input_bundle_sha256: str | None = None) -> None:
        self.root = root.resolve()
        self.spec = ExperimentSpec.create(spec.document()).document()
        if type(responses) is not OfflineResponses:
            raise ValueError("U04 chỉ nhận transport offline, chưa cấp HTTP")
        if self.spec["mode"] == "archive_replay" and not checksum(input_bundle_sha256):
            raise ValueError("Replay archive cần hash bundle nguồn tường minh")
        if digest(runtime_identity()) != self.spec["runtime_sha256"]:
            raise ValueError("Runtime khác spec")
        for name, expected in self.spec["source_hashes"].items():
            path = self.root / name
            if not path.resolve().is_relative_to(self.root) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError("Asset/source khác spec: " + name)
        self.responses = responses
        self.identity = {**spec.identity, "implementation": source_identity(), "runtime": runtime_identity(),
                         "offline_responses_sha256": digest(responses.rows), "input_bundle_sha256": input_bundle_sha256}
        self.directory = self.root / self.spec["namespace"]
        if not self.directory.resolve().is_relative_to(self.root):
            raise ValueError("Namespace run thoát khỏi workspace")
        if self.directory.exists() and not (self.directory / "identity.json").exists() and any(self.directory.iterdir()):
            raise ValueError("Không ghi vào thư mục có dữ liệu không thuộc run")

    def forecasts_done(self, point_id: str) -> bool:
        """Callback để ContextBank khóa nhãn query selected cho đến mọi forecast durable."""
        if point_id not in {p["id"] for p in self.spec["points"]} or not (self.directory / "identity.json").exists():
            return False
        book = RunBook(self.directory, self.identity, verify_only=True)
        return all(book.complete(slot_id(point_id, u, r, v)) for u in range(self.spec["realizations"])
                   for r in range(self.spec["repeats"]) for v in execution_order(self.spec["variants"]))

    def run(self, snapshots: Callable[[dict[str, Any], int], SharedSnapshot], methods: MethodAdapters,
            outcomes: Callable[[dict[str, Any]], dict[str, Any]]) -> dict[str, Any]:
        """Một shared/point/realization, mọi repeat dùng deepcopy; label sau mọi forecast durable."""
        order = execution_order(self.spec["variants"])
        records, labels = [], {}
        with PriorRunLock(self.directory, digest(self.identity)):
            book = RunBook(self.directory, self.identity)
            for point in self.spec["points"]:
                for realization in range(self.spec["realizations"]):
                    shared_slot = f"shared/{point['id']}/u{realization}"
                    def produce(_: str) -> dict[str, Any]:
                        return snapshots(deepcopy(point), realization).document()
                    doc = book.execute(shared_slot, {"point": point, "realization": realization}, produce)
                    snapshot = SharedSnapshot.create(doc["point"], doc["realization"], doc["payload"], doc["provenance"])
                    if doc["point"] != point or doc["realization"] != realization:
                        raise ValueError("Shared provider trả sai point/realization")
                    for repeat in range(self.spec["repeats"]):
                        outputs: dict[str, Any] = {}
                        for variant in order:
                            dependencies = {key: deepcopy(outputs[key]) for key in get_variant(variant).dependencies}
                            prep_slot = f"prepare/{point['id']}/u{realization}/r{repeat}/{variant}"
                            parents = {"shared_sha256": snapshot.sha256, "dependencies": {k: digest(v) for k, v in dependencies.items()}}
                            prepared = book.execute(prep_slot, parents,
                                lambda _: methods.prepare(variant, snapshot, deepcopy(dependencies), repeat))
                            validate_prepared(variant, snapshot, prepared, self.spec["decision"], repeat)
                            slot = slot_id(point["id"], realization, repeat, variant)
                            def invoke(_: str) -> dict[str, Any]:
                                raw = self.responses.take(slot, prepared["request"]) if prepared["request"] is not None else None
                                return make_record(point, snapshot, variant, repeat, prepared, raw, dependencies)
                            def validate(actual: dict[str, Any]) -> None:
                                expected = make_record(point, snapshot, variant, repeat, prepared, actual["forecast"]["raw"], dependencies)
                                if actual != expected:
                                    raise ValueError("Forecast/policy không khớp nguồn raw")
                            output = book.execute(slot, {**parents, "prepared": prepared}, invoke, validate=validate)
                            outputs[variant] = output
                            records.append(output)
                required = [slot_id(point["id"], u, r, v) for u in range(self.spec["realizations"])
                            for r in range(self.spec["repeats"]) for v in order]
                if not all(book.complete(slot) for slot in required):
                    raise ValueError("Chưa đủ forecast để mở outcome")
                def check_outcome(actual: dict[str, Any]) -> None:
                    validate_outcome(point, actual)
                    if actual["source_sha256"] not in self.spec["source_hashes"].values():
                        raise ValueError("Outcome không thuộc nguồn asset đã khóa")
                labels[point["id"]] = book.execute("outcome/" + point["id"], {"forecast_slots": required},
                    lambda _: outcomes(deepcopy(point)), validate=check_outcome)
            result = evaluate(self.spec, records, labels)
            save(self.directory / "result.json", result)
        return result


def verify_run(directory: Path, *, root: Path = ROOT) -> dict[str, Any]:
    """Consumer đọc journal đầy đủ, tái tính policy/ledger; không khởi tạo provider/model."""
    directory = directory.resolve()
    identity = load(directory / "identity.json")["identity"]
    spec = ExperimentSpec.create(identity["spec"])
    if directory != root.resolve() / spec.document()["namespace"]:
        raise ValueError("Run không ở namespace đã khóa")
    if identity["implementation"] != source_identity() or identity["runtime"] != runtime_identity() or identity["registry"] != spec.identity["registry"]:
        raise ValueError("Nguồn/runtime/registry đã đổi; cần snapshot frozen riêng")
    for name, expected in spec.document()["source_hashes"].items():
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("Input run đã đổi")
    records, outcomes = [], {}
    doc = spec.document()
    with PriorRunLock(directory, digest(identity)):
        book = RunBook(directory, identity, verify_only=True)
        for point in doc["points"]:
            for u in range(doc["realizations"]):
                state = book.execute(f"shared/{point['id']}/u{u}", {"point": point, "realization": u}, None)
                snapshot = SharedSnapshot.create(state["point"], state["realization"], state["payload"], state["provenance"])
                if state["point"] != point or state["realization"] != u:
                    raise ValueError("Shared journal sai point")
                for r in range(doc["repeats"]):
                    outputs: dict[str, Any] = {}
                    for variant in execution_order(doc["variants"]):
                        dependencies = {k: outputs[k] for k in get_variant(variant).dependencies}
                        parents = {"shared_sha256": snapshot.sha256, "dependencies": {k: digest(v) for k, v in dependencies.items()}}
                        prepared = book.execute(f"prepare/{point['id']}/u{u}/r{r}/{variant}", parents, None)
                        validate_prepared(variant, snapshot, prepared, doc["decision"], r)
                        record = book.execute(slot_id(point["id"], u, r, variant), {**parents, "prepared": prepared}, None)
                        if record != make_record(point, snapshot, variant, r, prepared, record["forecast"]["raw"], dependencies):
                            raise ValueError("Raw/policy trong journal không tái lập")
                        outputs[variant] = record; records.append(record)
            slots = [slot_id(point["id"], u, r, v) for u in range(doc["realizations"])
                     for r in range(doc["repeats"]) for v in execution_order(doc["variants"])]
            outcomes[point["id"]] = book.execute("outcome/" + point["id"], {"forecast_slots": slots}, None)
            if outcomes[point["id"]]["source_sha256"] not in doc["source_hashes"].values():
                raise ValueError("Outcome không thuộc nguồn đã khóa")
        actual = evaluate(doc, records, outcomes)
        if actual != load(directory / "result.json"):
            raise ValueError("Summary không khớp policy/ledger tái tính")
    return actual
