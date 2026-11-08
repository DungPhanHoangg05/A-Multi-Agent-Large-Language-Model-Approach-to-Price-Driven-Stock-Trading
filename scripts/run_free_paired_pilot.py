"""CLI pilot48; người dùng chạy API, smoke và research có grant riêng."""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    """Giữ lock/UUID chung, giới hạn thread và không tự nâng grant sau smoke."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "smoke", "verify-smoke", "shared", "collect", "verify", "reconcile"))
    parser.add_argument("--attempt-id")
    parser.add_argument("--reason")
    args = parser.parse_args()
    import torch
    from threadpoolctl import threadpool_limits
    from core.free_pilot_runtime import prepare, PilotRunner, identity
    from core.free_pilot_assets import DIRECTORY
    from core.historical_evaluation_journal import RunBook
    from core.historical_transport_observer import observe_transport
    from core.prior_run_lock import PriorRunLock
    torch.set_num_threads(1)
    directory = ROOT / DIRECTORY
    with threadpool_limits(limits=1):
        with PriorRunLock(directory, "free_pilot48_exclusive_v1"):
            if args.stage == "prepare":
                result = prepare(ROOT)
                print(json.dumps({k: result[k] for k in ("status", "carry_requests", "budget", "llm_calls")}, ensure_ascii=False))
                if result["status"] != "PASS":
                    raise SystemExit(2)
                return
            if args.stage == "reconcile":
                if not args.attempt_id or not args.reason:
                    parser.error("Reconcile cần UUID và lý do cụ thể")
                book = RunBook(directory, identity(ROOT))
                book.reconcile(args.attempt_id, args.reason)
                print("Đã reconcile UUID; chưa gửi HTTP.")
                return
            verify = args.stage in ("verify-smoke", "verify")
            runner = PilotRunner(ROOT, smoke=args.stage in ("smoke", "verify-smoke"), verify=verify)
            if verify:
                result = runner.smoke_run() if args.stage == "verify-smoke" else runner.collect()
            else:
                runner.live()
                with (directory / "console.log").open("a", encoding="utf-8") as handle, redirect_stdout(handle):
                    with observe_transport(ROOT, recover_connection_reset=True):
                        result = runner.smoke_run() if args.stage == "smoke" else runner.seal_shared() if args.stage == "shared" else runner.collect()
            print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
