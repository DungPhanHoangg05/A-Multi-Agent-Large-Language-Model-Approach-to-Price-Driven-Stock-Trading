"""Một lệnh H07 pilot: tự nạp .env, resume checkpoint và chạy tới cold verify."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    """Worker dùng nguyên CLI đã khóa; manager không tự train hoặc đổi inference runtime."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", choices=("shared", "collect", "verify"), help=argparse.SUPPRESS)
    parser.add_argument("--status", action="store_true", help="Chỉ đọc tiến độ, không gọi API.")
    args = parser.parse_args()
    from core.free_pilot_manager import manage, preflight
    from core.free_pilot_assets import DIRECTORY
    from core.historical_evaluation_journal import load
    if args.status:
        path = ROOT / DIRECTORY / "manager/status.json"
        print(json.dumps(load(path) if path.exists() else {"state": "NOT_STARTED"}, ensure_ascii=False))
        return
    if args.worker:
        from dotenv import load_dotenv
        from core.free_pilot_recovery import replay_durable_success
        from core.free_pilot_runtime import PilotClients
        from unittest.mock import patch
        preflight(ROOT)
        os.chdir(ROOT)
        load_dotenv(ROOT / ".env", override=False)
        script = ROOT / "scripts/run_free_paired_pilot.py"
        sys.argv = [str(script), args.worker]
        original_guard = PilotClients.verify_release
        def guard(client: PilotClients) -> None:
            """Source supervisor bổ sung cũng phải còn nguyên trước từng HTTP."""
            preflight(ROOT)
            original_guard(client)
        with patch.object(PilotClients, "verify_release", guard), replay_durable_success():
            runpy.run_path(str(script), run_name="__main__")
        return
    try:
        manage(ROOT)
    except KeyboardInterrupt:
        print("Đã dừng; checkpoint được giữ. Chạy lại chính lệnh này để tiếp tục.", file=sys.stderr)
        raise SystemExit(130) from None
    except (ValueError, RuntimeError, OSError) as error:
        if str(error) == "Run đang được tiến trình khác giữ khóa OS":
            path = ROOT / DIRECTORY / "manager/status.json"
            print("Đã có supervisor giữ khóa; không tạo tiến trình thu thập trùng.")
            if path.exists():
                print(json.dumps(load(path), ensure_ascii=False))
            return
        print("Dừng và giữ bằng chứng: " + str(error), file=sys.stderr)
        print("Xem manager/status.json và worker log; lệnh tiếp tục vẫn giữ nguyên.", file=sys.stderr)
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
