"""CLI H06 prepare/run/verify/reconcile; không tự chạy H07 hoặc nâng gói trả phí."""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))


def main() -> None:
    """Giữ lock toàn smoke; resume giữ UUID, unknown cần reconcile có lý do."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "run", "verify", "reconcile"))
    parser.add_argument("--attempt-id")
    parser.add_argument("--reason")
    args = parser.parse_args()
    import torch
    from threadpoolctl import threadpool_limits
    from core.historical_live_smoke import PLAN, NAMESPACE, prepare, run, anchored_file
    from core.historical_evaluation_journal import RunBook
    from core.historical_evaluation_protocol import binding, digest
    from core.historical_evaluation_clients import RUNTIME
    from core.prior_run_lock import PriorRunLock
    torch.set_num_threads(1)
    with threadpool_limits(limits=1):
        if args.stage == "prepare":
            directory = ROOT / "outputs/historical_reevaluation/h06_prepare"
            directory.mkdir(parents=True, exist_ok=True)
            with (directory / "console.log").open("w", encoding="utf-8") as handle, redirect_stdout(handle):
                result = prepare(ROOT)
            print("H06: preflight đã khóa, chưa gọi API; nominal55 executions, trần300 HTTP, chỉ Free.")
            print("Vision reserve:", result["vision_reserves"], "; Decision reserve:", result["request_reserves"])
            return
        anchored_file(ROOT, PLAN)
        signature = {"scope": "H06_CONTROL_ONLY_NOT_H07", "plan_sha256": binding(ROOT, PLAN)["sha256"],
                     "runtime_sha256": binding(ROOT, RUNTIME)["sha256"]}
        directory = ROOT / NAMESPACE
        if args.stage == "verify" and not (directory / "identity.json").exists():
            raise ValueError("Chưa có smoke để verify")
        with PriorRunLock(directory, digest(signature)):
            if args.stage == "reconcile":
                if not args.attempt_id or not args.reason:
                    raise ValueError("Cần --attempt-id và --reason cụ thể")
                RunBook(directory, signature).reconcile(args.attempt_id, args.reason)
                print("Đã reconcile UUID; chưa gửi HTTP, chạy lại run để tiếp tục.")
                return
            mode = "verify.log" if args.stage == "verify" else "console.log"
            with (directory / mode).open("a", encoding="utf-8") as handle, redirect_stdout(handle):
                result = run(ROOT, verify_only=args.stage == "verify")
            print("H06:", result["status"], "; đã kiểm5 org; control cách ly, chưa release H07.")


if __name__ == "__main__":
    main()
