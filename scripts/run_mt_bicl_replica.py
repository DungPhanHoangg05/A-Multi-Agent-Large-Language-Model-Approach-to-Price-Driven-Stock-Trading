"""Chuẩn bị, pilot, train/resume và cold-verify replica đầy đủ; không gọi LLM."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.mt_bicl_bank import content_hash
from core.mt_bicl_replica_io import NAMESPACE, load_protocol
from core.prior_run_lock import PriorRunLock


def main() -> None:
    """Không tự chuyển bước: mỗi lệnh là một giai đoạn người dùng chủ động chạy."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("check-inputs", "check-lock", "repair-lock", "prepare", "pilot", "train", "evaluate", "verify"))
    args = parser.parse_args()
    protocol = load_protocol(ROOT)
    if args.stage == "repair-lock":
        from core.mt_bicl_replica_lock import repair_pretraining_lock
        result = repair_pretraining_lock(ROOT, protocol)
        print("Replica: " + result["status"], flush=True)
        return
    with PriorRunLock(ROOT / NAMESPACE, content_hash(protocol)):
        if args.stage == "check-lock":
            result = {"status":"LOCK_VERIFIED_NO_FIT"}
        elif args.stage in ("check-inputs", "prepare"):
            from core.mt_bicl_replica_preparation import check_inputs, prepare
            if args.stage == "check-inputs":
                inputs = check_inputs(ROOT)
                result = {"status": "INPUTS_VERIFIED_NO_FIT", "cycles": inputs["membership"]["cycles"], "tasks": inputs["membership"]["tasks"]}
            else:
                result = prepare(ROOT)
        else:
            from core.mt_bicl_replica_training import evaluate_final, pilot, train
            if args.stage == "pilot":
                result = pilot(ROOT)
            elif args.stage == "train":
                result = train(ROOT)
            else:
                result = evaluate_final(ROOT, replay=args.stage == "verify")
    print("Replica: " + result["status"], flush=True)
    if result["status"] in ("NO_ELIGIBLE_CHECKPOINT", "STOP_TEST_FAILURE_NO_RESELECT", "STOP_PAIRED_TINY_GATE"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
