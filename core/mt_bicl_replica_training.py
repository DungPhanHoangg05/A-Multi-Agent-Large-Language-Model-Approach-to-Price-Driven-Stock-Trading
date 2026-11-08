"""Pilot/train ba seed, selection60 checkpoint và cold inference replica; không LLM."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import time
from typing import Any
from uuid import uuid4

import torch

from core.mt_bicl_bank import content_hash
from core.mt_bicl_evaluation import market_input, probabilities
from core.mt_bicl_replica_io import (configure, file_hash, load_checkpoint, path_for, read,
    restore_rng, rng_state, save_checkpoint, tree_hash, write)
from core.mt_bicl_replica_learner import evaluate, gradient_audit, make_optimizer, optimizer_step, scheduled_lr, tensor_hash
from core.mt_bicl_replica_metrics import (SEEDS, STEPS, ablate, mechanism_report, predict,
    selection, selection_metrics, swap_report, validation_summary)
from core.mt_bicl_replica_preparation import load_prepared
from core.mt_bicl_replica_student import CASES, LEGACY, PAIRED, DistilledStudent, pack_input


def identity(inputs: dict[str, Any], root: Path) -> str:
    """Bind toàn prepared receipt, không chỉ source hoặc teacher pi tự khai."""
    return content_hash({**inputs["identity"], "prepared_sha256": file_hash(path_for(root, "prepared.json"))})


def batch(inputs: dict[str, Any], step: int, seed: int, *, preflight: bool = False) -> list[dict[str, Any]]:
    """Synthetic-only random-access; không đọc latent/query-y để tính teacher q."""
    if seed not in SEEDS or type(step) is not int or not 1 <= step <= (100 if preflight else 5000):
        raise ValueError("Seed/step ngoài recipe")
    rows = []
    for index in range((step - 1) * 128, step * 128):
        data = inputs["simulator"].episode("preflight" if preflight else "train", index, model_seed=seed)["input"]
        rows.append(pack_input(data, teacher_q=inputs["teacher"].predict(data)["probability"]))
    return rows


def gpu_identity() -> dict[str, Any]:
    """Lưu GPU production để resume không đổi thiết bị ngầm."""
    value = torch.cuda.get_device_properties(0)
    return {"name": value.name, "capability": list(torch.cuda.get_device_capability(0)),
            "total_memory": int(value.total_memory), "cuda": torch.version.cuda}


def snapshot(model: DistilledStudent, optimizer: torch.optim.Optimizer, *, seed: int, step: int,
             binding: str, uuid: str, physical: int) -> dict[str, Any]:
    """Checkpoint đầy đủ trajectory và RNG, không chỉ weights."""
    return {"model": model.state_dict(), "optimizer": optimizer.state_dict(), "rng": rng_state(),
            "seed": seed, "step": step, "identity": binding, "run_uuid": uuid, "physical_batch": physical,
            "model_tensor_sha256": tensor_hash(model)}


def restore(model: DistilledStudent, optimizer: torch.optim.Optimizer, payload: dict[str, Any],
            *, binding: str, uuid: str, seed: int, physical: int) -> int:
    """Không phục hồi checkpoint khác source/seed/run/batch dù shape giống nhau."""
    if (payload["identity"] != binding or payload["run_uuid"] != uuid or payload["seed"] != seed
            or payload["physical_batch"] != physical):
        raise ValueError("Checkpoint khác identity/run/seed/batch")
    model.load_state_dict(payload["model"], strict=True)
    if tensor_hash(model) != payload["model_tensor_sha256"]:
        raise ValueError("Checkpoint model khác fingerprint")
    optimizer.load_state_dict(payload["optimizer"])
    restore_rng(payload["rng"])
    return int(payload["step"])


def pilot(root: Path) -> dict[str, Any]:
    """Người dùng chạy GPU preflight100 và hai tiny-fit500; kiểm replay step500."""
    inputs = load_prepared(root)
    binding = identity(inputs, root)
    device = configure(17, cuda=True)
    report_path = path_for(root, "pilot/report.json")
    state_path = path_for(root, "pilot/state.json")
    state = read(state_path) if state_path.exists() else {"identity": binding, "run_uuid": str(uuid4()), "gpu": gpu_identity(), "cases": {}}
    if state["identity"] != binding or state["gpu"] != gpu_identity():
        raise ValueError("Pilot khác identity/GPU")
    write(state_path, state, mutable=True)
    if report_path.exists():
        result = read(report_path)
        if result["identity"] != binding or result["state_sha256"] != file_hash(state_path):
            raise ValueError("Pilot report khác state")
        for row in state["cases"].values():
            for record in row["checkpoints"].values():
                load_checkpoint(path_for(root, record["file"]), record)
        return result
    if "physical_batch" not in state:
        for physical in (128, 64, 32):
            model, optimizer = None, None
            try:
                configure(17, cuda=True)
                model = DistilledStudent().to(device)
                optimizer = make_optimizer(model)
                start = time.perf_counter()
                for step in range(1, 101):
                    optimizer_step(model, optimizer, batch(inputs, step, 17, preflight=True), physical, device)
                torch.cuda.synchronize()
                state.update(physical_batch=physical, preflight_steps=100, preflight_wall_seconds=time.perf_counter() - start)
                write(state_path, state, mutable=True)
                del model, optimizer
                break
            except torch.cuda.OutOfMemoryError:
                if physical == 32:
                    raise
                del model, optimizer
                torch.cuda.empty_cache()
    physical = state["physical_batch"]
    tiny_rows = read(path_for(root, "corpora/pilot_tiny.json"))["episodes"]
    diagnostics = read(path_for(root, "corpora/diagnostic.json"))["episodes"]
    reports = {}
    for case in CASES:
        configure(17, cuda=True)
        model = DistilledStudent(case).to(device)
        optimizer = make_optimizer(model)
        packets = [pack_input(r["input"], teacher_q=r["oracle"]["probability"], packing=case) for r in tiny_rows]
        diagnostic = [pack_input(r["input"], teacher_q=r["oracle"]["probability"], packing=case) for r in diagnostics]
        progress = state["cases"].setdefault(case, {"checkpoints": {}, "initial": evaluate(model, packets, physical, device)})
        step = 0
        if progress["checkpoints"]:
            last = max(map(int, progress["checkpoints"]))
            pointer = progress["checkpoints"][str(last)]
            step = restore(model, optimizer, load_checkpoint(path_for(root, pointer["file"]), pointer), binding=binding,
                           uuid=state["run_uuid"], seed=17, physical=physical)
        audit = gradient_audit(model, packets, device)
        for current in range(step + 1, 501):
            optimizer_step(model, optimizer, packets * 4, physical, device)
            if current in (250, 499, 500):
                name = f"pilot/{case}-{current}.pt"
                pointer = save_checkpoint(path_for(root, name), snapshot(model, optimizer, seed=17, step=current,
                    binding=binding, uuid=state["run_uuid"], physical=physical))
                pointer["file"] = name
                progress["checkpoints"][str(current)] = pointer
                if current in (250, 500):
                    progress[str(current)] = evaluate(model, packets, physical, device)
                write(state_path, state, mutable=True)
        # Replay thật một optimizer step từ499, rồi so đầy đủ model/optimizer/RNG tại500.
        at499 = progress["checkpoints"]["499"]
        restore(model, optimizer, load_checkpoint(path_for(root, at499["file"]), at499), binding=binding,
                uuid=state["run_uuid"], seed=17, physical=physical)
        optimizer_step(model, optimizer, packets * 4, physical, device)
        replay = snapshot(model, optimizer, seed=17, step=500, binding=binding, uuid=state["run_uuid"], physical=physical)
        if tree_hash(replay) != progress["checkpoints"]["500"]["payload_sha256"]:
            raise ValueError("Pilot optimizer/RNG replay không khớp")
        reports[case] = {"tiny": progress["500"], "diagnostic": evaluate(model, diagnostic, physical, device),
                         "gradient_audit": audit, "optimizer_replay": "PASS"}
    status = "PASS" if reports[PAIRED]["tiny"]["mean_kl_nat"] < .001 else "STOP_PAIRED_TINY_GATE"
    result = {"identity": binding, "state_sha256": file_hash(state_path), "physical_batch": physical,
              "gpu": state["gpu"], "status": status, "cases": reports, "production_weights_discarded": True}
    write(report_path, result)
    if status != "PASS":
        raise ValueError(status)
    return result


def validation_jobs(inputs: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Cache packet CPU; không mở synthetic test/market2022 trước selection seal."""
    if "jobs" not in inputs:
        rows, pairs = inputs["corpora"]["synthetic_validation"], inputs["corpora"]["validation_swap"]
        inputs["jobs"] = {"full": [pack_input(r["input"]) for r in rows],
            "context_blind": [pack_input(ablate(r["input"], "context_blind")) for r in rows],
            "swap_a": [pack_input(r["input_a"]) for r in pairs], "swap_b": [pack_input(r["input_b"]) for r in pairs],
            "market_2021": [pack_input(market_input(r, inputs["context"])) for r in inputs["selection_rows"]]}
    return inputs["jobs"]


def checkpoint_assessment(payload: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    """Frozen inference CPU cố định ở cả thu và cold replay; không tiêu thụ RNG train."""
    before = rng_state()
    try:
        model = DistilledStudent()
        model.load_state_dict(payload["model"], strict=True)
        logits = {name: predict(model, packets, 128, torch.device("cpu")) for name, packets in validation_jobs(inputs).items()}
        return {"logits": logits, "assessment": validation_summary(inputs, logits), "model_tensor_sha256": tensor_hash(model)}
    finally:
        restore_rng(before)


def verified_records(root: Path, inputs: dict[str, Any], state: dict[str, Any], *, replay: bool = False) -> list[dict[str, Any]]:
    """Mỗi assessment bind đúng checkpoint; cold replay tính lại raw logits/metric."""
    records = []
    for row in state["checkpoints"]:
        payload = load_checkpoint(path_for(root, row["file"]), row)
        report = read(path_for(root, row["report"]["file"]))
        if file_hash(path_for(root, row["report"]["file"])) != row["report"]["sha256"]:
            raise ValueError("Assessment khác receipt")
        if report["checkpoint_sha256"] != row["sha256"] or report["identity"] != state["identity"]:
            raise ValueError("Assessment khác checkpoint/identity")
        if replay and report["result"] != checkpoint_assessment(payload, inputs):
            raise ValueError("Raw validation logits/metric không khớp cold CPU replay")
        records.append({"seed": row["seed"], "step": row["step"], "checkpoint": {k:v for k,v in row.items() if k != "report"},
                        "report": row["report"], "assessment": report["result"]["assessment"]})
    return records


def train(root: Path) -> dict[str, Any]:
    """Ba seed đủ5.000 step; checkpoint/resume durable, không metric early stop."""
    inputs = load_prepared(root)
    binding = identity(inputs, root)
    pilot_report = pilot(root)
    if pilot_report["status"] != "PASS":
        raise ValueError("Chưa PASS pilot")
    physical = pilot_report["physical_batch"]
    binding = content_hash({"prepared_identity": binding, "pilot_sha256": file_hash(path_for(root, "pilot/report.json"))})
    path = path_for(root, "training/state.json")
    state = read(path) if path.exists() else {"identity": binding, "run_uuid": str(uuid4()), "gpu": pilot_report["gpu"],
                                            "physical_batch": physical, "checkpoints": [], "started_at": datetime.now(timezone.utc).isoformat()}
    if state["identity"] != binding or state["physical_batch"] != physical or state["gpu"] != gpu_identity():
        raise ValueError("Train khác identity/GPU/batch")
    write(path, state, mutable=True)

    def assess(row: dict[str, Any]) -> None:
        """Nếu crash sau checkpoint durable, hoàn tất assessment trước train tiếp."""
        payload = load_checkpoint(path_for(root, row["file"]), row)
        name = row["file"].removesuffix(".pt") + ".assessment.json"
        result = {"identity": binding, "checkpoint_sha256": row["sha256"], "result": checkpoint_assessment(payload, inputs)}
        write(path_for(root, name), result)
        row["report"] = {"file": name, "sha256": file_hash(path_for(root, name))}
        write(path, state, mutable=True)

    for row in state["checkpoints"]:
        if "report" not in row:
            assess(row)
    verified_records(root, inputs, state)
    for seed in SEEDS:
        device = configure(seed, cuda=True)
        model, optimizer = DistilledStudent().to(device), None
        optimizer = make_optimizer(model)
        completed = [r for r in state["checkpoints"] if r["seed"] == seed]
        step = 0
        if completed:
            last = max(completed, key=lambda r: r["step"])
            step = restore(model, optimizer, load_checkpoint(path_for(root, last["file"]), last), binding=binding,
                           uuid=state["run_uuid"], seed=seed, physical=physical)
        for current in range(step + 1, 5001):
            for group in optimizer.param_groups:
                group["lr"] = scheduled_lr(current)
            optimizer_step(model, optimizer, batch(inputs, current, seed), physical, device)
            if current % 250 == 0:
                name = f"training/seed{seed}/checkpoint-{current:05d}.pt"
                payload = snapshot(model, optimizer, seed=seed, step=current, binding=binding, uuid=state["run_uuid"], physical=physical)
                row = {"file": name, "seed": seed, "step": current, **save_checkpoint(path_for(root, name), payload)}
                state["checkpoints"].append(row)
                write(path, state, mutable=True)
                assess(row)
                print(f"Seed{seed}: {current}/5000; checkpoint+assessment durable.", flush=True)
        del model, optimizer
        torch.cuda.empty_cache()
    result = {"identity": binding, "state_sha256": file_hash(path), **selection(verified_records(root, inputs, state))}
    write(path_for(root, "training/selection.json"), result)
    return result


def open_test(root: Path, inputs: dict[str, Any], seal: dict[str, Any]) -> dict[str, Any]:
    """Kiểm selection durable và đủ60 checkpoint trước decode test/2022."""
    if read(path_for(root, "training/selection.json")) != seal or seal["status"] != "SELECTED":
        raise ValueError("Test chỉ mở sau immutable selection seal SELECTED")
    state = read(path_for(root, "training/state.json"))
    if seal["identity"] != state["identity"] or seal["state_sha256"] != file_hash(path_for(root, "training/state.json")):
        raise ValueError("Selection khác state")
    expected = selection(verified_records(root, inputs, state))
    if any(seal[k] != v for k,v in expected.items()):
        raise ValueError("Selection khác derive60 checkpoint")
    return {"synthetic_test": read(path_for(root, "corpora/synthetic_test.json"))["episodes"],
            "test_swap": read(path_for(root, "corpora/test_swap.json"))["episodes"],
            "market": read(path_for(root, "inputs/test_2022.json"))}


def evaluate_final(root: Path, *, replay: bool = False) -> dict[str, Any]:
    """CPU frozen inference và ablation; test fail không reselect/teacher fallback."""
    inputs = load_prepared(root)
    torch.set_num_threads(1)
    seal = read(path_for(root, "training/selection.json"))
    tests = open_test(root, inputs, seal)
    corpus, pairs, market = tests["synthetic_test"], tests["test_swap"], tests["market"]
    stages = {}
    for seed in SEEDS:
        candidate = seal["per_seed_candidate_or_none"][str(seed)]
        if candidate is None:
            stages[str(seed)] = {"status": "NOT_RUN_NO_ELIGIBLE_CHECKPOINT"}
            continue
        payload = load_checkpoint(path_for(root, candidate["checkpoint"]["file"]), candidate["checkpoint"])
        model = DistilledStudent()
        model.load_state_dict(payload["model"], strict=True)
        logits = {"swap_a": predict(model, [pack_input(r["input_a"]) for r in pairs], 128, torch.device("cpu")),
                  "swap_b": predict(model, [pack_input(r["input_b"]) for r in pairs], 128, torch.device("cpu"))}
        diagnostics = {}
        for mode in ("full", "no_prior", "no_target", "context_blind"):
            logits[mode] = predict(model, [pack_input(ablate(r["input"], mode)) for r in corpus], 128, torch.device("cpu"))
            mz = predict(model, [pack_input(market_input(r, market, mode if mode != "context_blind" else "full")
                                    if mode != "context_blind" else ablate(market_input(r, market), mode)) for r in market["episodes"]], 128, torch.device("cpu"))
            diagnostics[mode] = selection_metrics([{"episode_id":r["query"]["episode_id"],"symbol":r["query"]["symbol"],
                "y":r["supervised_target"]["y"],"p":float(p)} for r,p in zip(market["episodes"],probabilities(mz)[0])])
            logits["market_2022_"+mode] = mz
        teacher_controls = {}
        for mode in ("full", "no_prior", "no_target", "pooling"):
            data = [market_input(r, market, "full" if mode == "pooling" else mode) for r in market["episodes"]]
            values = [inputs["teacher"].predict(r, pooled=mode == "pooling")["probability"] for r in data]
            teacher_controls[mode] = selection_metrics([{"episode_id":r["query"]["episode_id"],"symbol":r["query"]["symbol"],
                "y":r["supervised_target"]["y"],"p":float(p)} for r,p in zip(market["episodes"],values)])
        constant = float(sum(p*mu for p,mu in zip(inputs["teacher"].pi, [.2]*4+[.4]*4+[.6]*4+[.8]*4)))
        import math
        control = mechanism_report([math.log(constant)-math.log1p(-constant)]*len(corpus), corpus)
        synthetic, swap = mechanism_report(logits["full"], corpus), swap_report(logits["swap_a"], logits["swap_b"], pairs)
        gate = "PASS" if synthetic["gate"] == swap["gate"] == "PASS" and control["gate"] != "PASS" else "FAIL_OR_INCONCLUSIVE"
        stage = {"candidate":candidate,"logits":logits,"synthetic":synthetic,"prior_swap":swap,"constant_control":control,
                 "market_2022":diagnostics,"teacher_market_2022":teacher_controls,"status":gate,"model_tensor_sha256":tensor_hash(model)}
        write(path_for(root, f"evaluation/seed{seed}.json"), stage)
        stages[str(seed)] = stage
    selected = seal["global_candidate_or_none"]
    passed = stages[str(selected["seed"])]["status"] == "PASS"
    report = {"selection_sha256":file_hash(path_for(root,"training/selection.json")),"status":"MODEL_GATE_PASS" if passed else "STOP_TEST_FAILURE_NO_RESELECT",
              "stages":{s:content_hash(v) for s,v in stages.items()},"historical_evaluation_released":False,"llm_calls":0}
    write(path_for(root,"evaluation/report.json"),report)
    if replay:
        state = read(path_for(root,"training/state.json"))
        verified_records(root,inputs,state,replay=True)
        write(path_for(root,"evaluation/cold_verification.json"),{"status":"CPU_REPLAY_MATCH","checkpoints":60,
              "report_sha256":file_hash(path_for(root,"evaluation/report.json")),"optimizer_retrained":False})
    if passed:
        payload = load_checkpoint(path_for(root,selected["checkpoint"]["file"]),selected["checkpoint"])
        weights = {"version":"mt_bicl_replica_full_r1_candidate","seed":selected["seed"],"step":selected["step"],
                   "model":payload["model"],"model_tensor_sha256":payload["model_tensor_sha256"],"selection_sha256":report["selection_sha256"]}
        save_checkpoint(path_for(root,"model/candidate.pt"),weights)
        write(path_for(root,"model/teacher.json"),read(path_for(root,"teacher/teacher.json")))
        model_path = path_for(root,"model")
        manifest = {"version":"mt_bicl_model_assets","status":"FROZEN_AWAITING_COLD_VERIFY" if not replay else "COLD_VERIFIED",
                    "inference_released":False,"artifact_trees":{model_path.relative_to(root).as_posix():{
                    n:{"sha256":file_hash(model_path/n),"bytes":(model_path/n).stat().st_size} for n in ("candidate.pt","teacher.json")}}}
        if path_for(root,"model/manifest.json").exists() and read(path_for(root,"model/manifest.json"))["status"] == "COLD_VERIFIED":
            manifest["status"] = "COLD_VERIFIED"
        write(path_for(root,"model/manifest.json"),manifest,mutable=True)
    return report
