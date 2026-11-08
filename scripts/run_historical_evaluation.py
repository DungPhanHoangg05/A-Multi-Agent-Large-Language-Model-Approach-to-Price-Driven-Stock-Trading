"""CLI H04 prepare/run/resume/verify/reconcile, API vẫn cần grant H06 đã neo Git."""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    """Giữ lock run trong toàn vòng checkpoint/ledger; fixture tách namespace thật."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "prepare-regimes", "run", "resume", "verify", "reconcile"))
    parser.add_argument("--fixture", action="store_true", help="Chỉ dùng response mô phỏng trong namespace fixture.")
    parser.add_argument("--cohort", choices=("CORE4", "OOD5"), default="CORE4")
    parser.add_argument("--max-units", type=int)
    parser.add_argument("--attempt-id")
    parser.add_argument("--reason")
    args = parser.parse_args()
    import torch
    from threadpoolctl import threadpool_limits
    from core.historical_evaluation_audit import prepare, prepare_regimes
    from core.historical_evaluation_clients import require_release
    from core.historical_evaluation_data import HistoricalData
    from core.historical_evaluation_protocol import digest
    from core.historical_evaluation_runner import HistoricalRunner, runtime_identity
    from core.prior_run_lock import PriorRunLock
    torch.set_num_threads(1)
    with threadpool_limits(limits=1):
        if args.stage in ("prepare", "prepare-regimes"):
            result = prepare(ROOT) if args.stage == "prepare" else prepare_regimes(ROOT)
            print(json.dumps({k: v for k, v in result.items() if k in
                              ("status", "count", "llm_calls", "teacher_or_student_fit", "api_released")}, ensure_ascii=False))
            return
        if args.stage in ("run", "resume") and not args.fixture:
            require_release(ROOT)
        data = HistoricalData(ROOT)
        directory = ROOT / ("outputs/historical_reevaluation/h04_fixture" if args.fixture else data.protocol["namespace"])
        if args.stage == "verify" and not (directory / "identity.json").is_file():
            raise ValueError("Chưa có run để verify; không tạo namespace")
        identity = runtime_identity(data, args.fixture)
        with PriorRunLock(directory, digest(identity)):
            runner = HistoricalRunner(data, fixture=args.fixture, verify_only=args.stage == "verify",
                                      clients=False if args.stage == "reconcile" else None)
            if args.stage == "reconcile":
                if not args.attempt_id or not args.reason:
                    raise ValueError("Reconcile cần --attempt-id và --reason cụ thể")
                runner.book.reconcile(args.attempt_id, args.reason)
                print("Đã lưu audit reconcile UUID; chưa gửi lại HTTP.")
            else:
                log = directory / "console.log"
                if args.stage == "verify":
                    result = runner.run(cohort=args.cohort, max_units=args.max_units)
                else:
                    with log.open("a", encoding="utf-8") as handle, redirect_stdout(handle):
                        result = runner.run(cohort=args.cohort, max_units=args.max_units)
                print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
