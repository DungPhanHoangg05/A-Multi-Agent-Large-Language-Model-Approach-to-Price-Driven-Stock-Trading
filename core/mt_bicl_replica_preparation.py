"""Chuẩn bị teacher/corpus/context replica riêng; CLI người dùng mới bắt đầu fit."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pandas as pd
from threadpoolctl import threadpool_limits

from core.execution_prices import load_verified_execution_data
from core.mt_bicl_bank import SYMBOLS, content_hash
from core.mt_bicl_inputs import training_membership
from core.mt_bicl_reference import SequentialBetaOracle
from core.mt_bicl_regimes import RegimeTimeline
from core.mt_bicl_replica_io import file_hash, load_protocol, path_for, read, write
from core.mt_bicl_replica_sampling import BetaTaskSimulator, train_feature_pool
from core.mt_bicl_stream import MarketStream
from core.mt_bicl_tasks import TaskBuilder, validate_episode
from core.mt_bicl_teacher import BetaBernoulliTeacher, fit_hyperprior, prior_predictive_audit, train_task_counts

STREAMS = ("diagnostic", "pilot_tiny", "synthetic_validation", "validation_swap", "synthetic_test", "test_swap")


def check_inputs(root: Path) -> dict[str, Any]:
    """Cold-verify raw/bank/scaler; không fit HMM, teacher hoặc optimizer."""
    from scripts.build_mt_bicl_bank import prepare
    protocol = load_protocol(root)
    bank = prepare(root)
    path = path_for(root, "inputs/dense_bank.json")
    if read(path) != bank:
        raise ValueError("Bank replica khác cold-rebuild")
    membership = training_membership(bank)
    if membership["cycles"] != 731 or membership["tasks"] != 48 or bank["summary"]["minimum_support_status"] != "PASS":
        raise ValueError("Membership/support không tái lập recipe731 cycle/48 task")
    return {"protocol": protocol, "bank": bank, "membership": membership,
            "pool": train_feature_pool(bank, membership), "bank_byte_sha256": file_hash(path)}


def checked_oracle(teacher: BetaBernoulliTeacher, reference: SequentialBetaOracle,
                   data: dict[str, Any], *, pooled: bool = False) -> tuple[dict[str, Any], float]:
    """Đối chiếu p và cả hai log probability với oracle tuần tự độc lập."""
    actual, expected = teacher.predict(data, pooled=pooled), reference.predict(data, pooled=pooled)
    error = max(abs(actual[k] - expected[k]) for k in ("probability", "log_probability_one", "log_probability_zero"))
    if error > 1e-12:
        raise ValueError("Teacher khác oracle độc lập")
    return actual, float(error)


def corpus(simulator: BetaTaskSimulator, teacher: BetaBernoulliTeacher, stream: str) -> dict[str, Any]:
    """Seal toàn tập recipe; không forward student hoặc dùng query-y trong q."""
    if stream not in STREAMS:
        raise ValueError("Không được materialize train hoặc stream ngoài corpus")
    reference = SequentialBetaOracle(teacher.pi.tolist())
    rows, maximum = [], 0.
    for index in range(simulator.manifest["streams"][stream]["ids"]["stop_exclusive"]):
        row = simulator.pair(stream, index) if stream.endswith("_swap") else simulator.episode(stream, index)
        for suffix in (("_a", "_b") if stream.endswith("_swap") else ("",)):
            data = row["input" + suffix]
            row["oracle" + suffix], error = checked_oracle(teacher, reference, data)
            maximum = max(maximum, error)
            row["pooling" + suffix], error = checked_oracle(teacher, reference, data, pooled=True)
            maximum = max(maximum, error)
        if stream.endswith("_swap"):
            delta = row["oracle_b"]["probability"] - row["oracle_a"]["probability"]
            row["eligible"], row["oracle_delta_b_minus_a"] = bool(abs(delta) >= .05), float(delta)
        rows.append(row)
        if (index + 1) % 1000 == 0:
            print(f"Đã kiểm oracle {stream}: {index + 1}", flush=True)
    return {"stream": stream, "episodes": rows, "oracle_max_abs_error": maximum,
            "held_until_selection_seal": stream in ("synthetic_test", "test_swap")}


def contexts(root: Path, bank: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Dựng query2021/2022 với outcome chỉ sidecar sau validate D/C/x PIT."""
    history = pd.read_csv(root / "data/historical/VNINDEX.csv", parse_dates=["Datetime"])
    # Giữ đúng nguồn context lịch sử; MarketStream cắt prefix trước feature/label.
    prices = {s: load_verified_execution_data(root / "data/execution_prices_oos", s) for s in SYMBOLS}
    scalers: dict[str, Any] = {}
    groups: dict[str, list[dict[str, Any]]] = {"checkpoint_selection": [], "validation": []}
    with threadpool_limits(limits=1):
        regimes = RegimeTimeline(history)
        builder = TaskBuilder(bank, MarketStream(bank, prices, pd.DatetimeIndex(history["Datetime"])), regimes)
        source = sorted((r for r in bank["records"] if r["status"] == "AVAILABLE" and r["split"] in groups),
                        key=lambda r: (r["as_of_date"], SYMBOLS.index(r["symbol"])))
        for row in source:
            episode = builder.build(row["symbol"], row["as_of_date"])
            validate_episode(episode)
            if episode["status"] != "AVAILABLE":
                raise ValueError("Query selection/test có feature thiếu")
            scaler = episode.pop("scaler")
            key = content_hash(scaler)
            scalers[key] = scaler
            episode.update(scaler_sha256=key, split=row["split"], supervised_target=deepcopy(row["outcome"]))
            groups[row["split"]].append(episode)
        model_artifacts = regimes.artifacts()
    selection = {"scalers": scalers, "episodes": groups["checkpoint_selection"]}
    test = {"scalers": scalers, "episodes": groups["validation"]}
    for group, year in ((selection, "2021"), (test, "2022")):
        if any(sum(r["query"]["symbol"] == s for r in group["episodes"]) < 40 for s in SYMBOLS):
            raise ValueError("Context thiếu40 query/mã: " + year)
        if any(not r["query"]["as_of_date"].startswith(year) or not r["query"]["exit_date"].startswith(year) for r in group["episodes"]):
            raise ValueError("Context sai partition")
    return selection, test, model_artifacts


def prepare(root: Path) -> dict[str, Any]:
    """Lệnh CPU fit teacher và HMM, chạy bằng người dùng trước pilot GPU."""
    inputs = check_inputs(root)
    protocol, bank = inputs["protocol"], inputs["bank"]
    identity = {"protocol_sha256": content_hash(protocol), "bank_byte_sha256": inputs["bank_byte_sha256"],
                "membership_sha256": content_hash(inputs["membership"]), "feature_pool_sha256": content_hash(inputs["pool"])}
    teacher_path = path_for(root, "teacher/teacher.json")
    if teacher_path.exists():
        fitted = read(teacher_path)
        if fitted["identity"] != identity:
            raise ValueError("Teacher đã có khác identity")
    else:
        tasks = train_task_counts(bank, inputs["membership"])
        fitted = {"identity": identity, **fit_hyperprior(tasks), "task_counts": tasks}
        write(teacher_path, fitted)
    if fitted["converged"] is not True:
        raise ValueError("STOP_TEACHER_NONCONVERGENCE_NO_UNIFORM_FALLBACK")
    teacher = BetaBernoulliTeacher(fitted["pi"])
    write(path_for(root, "teacher/prior_predictive.json"), prior_predictive_audit(fitted["task_counts"], teacher.pi.tolist(),
                                                                              protocol["corpus"]["streams"]["prior_predictive"]["seed"]))
    simulator = BetaTaskSimulator(teacher.pi.tolist(), inputs["pool"], protocol["corpus"])
    files = ["inputs/dense_bank.json", "teacher/teacher.json", "teacher/prior_predictive.json"]
    for stream in STREAMS:
        name = f"corpora/{stream}.json"
        path = path_for(root, name)
        if not path.exists():
            write(path, corpus(simulator, teacher, stream))
        value = read(path)
        if value["stream"] != stream or len(value["episodes"]) != protocol["corpus"]["streams"][stream]["ids"]["stop_exclusive"]:
            raise ValueError("Corpus không đúng stream/mẫu số")
        files.append(name)
    selection, test, models = contexts(root, bank)
    for name, data in (("inputs/selection_2021.json", selection), ("inputs/test_2022.json", test), ("inputs/regime_models.json", models)):
        write(path_for(root, name), data)
        files.append(name)
    result = {"identity": identity, "status": "PREPARED_AWAITING_GPU_PILOT",
              "files": {name: file_hash(path_for(root, name)) for name in files}, "llm_calls": 0,
              "selection_queries": len(selection["episodes"]), "test_queries_held": len(test["episodes"])}
    write(path_for(root, "prepared.json"), result)
    print("Teacher/corpus/context đã seal; chưa chạy student production.", flush=True)
    return result


def load_prepared(root: Path) -> dict[str, Any]:
    """Kiểm mọi byte nhưng chỉ decode validation/2021, không mở test trước selection."""
    protocol = load_protocol(root)
    prepared = read(path_for(root, "prepared.json"))
    if prepared["identity"]["protocol_sha256"] != content_hash(protocol):
        raise ValueError("Prepared khác protocol")
    for name, expected in prepared["files"].items():
        if file_hash(path_for(root, name)) != expected:
            raise ValueError("Prepared input đã đổi: " + name)
    bank = read(path_for(root, "inputs/dense_bank.json"))
    fitted = read(path_for(root, "teacher/teacher.json"))
    pool = train_feature_pool(bank, training_membership(bank))
    context = read(path_for(root, "inputs/selection_2021.json"))
    return {"protocol": protocol, "identity": prepared["identity"], "prepared": prepared,
            "teacher": BetaBernoulliTeacher(fitted["pi"]), "simulator": BetaTaskSimulator(fitted["pi"], pool, protocol["corpus"]),
            "context": context, "selection_rows": context["episodes"],
            "corpora": {s: read(path_for(root, f"corpora/{s}.json"))["episodes"] for s in ("synthetic_validation", "validation_swap")}}
