"""Chạy nguyên CLI H07 đã khóa, bổ sung loại/mã lỗi gốc ra stderr và file riêng."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    """Giữ toàn bộ args, lock, journal, release, payload, quota và retry của CLI gốc."""
    from core.historical_transport_observer import observe_transport
    from scripts.run_historical_evaluation import main as evaluation_main
    recover = "--recover-connection-reset" in sys.argv[1:]
    if recover:
        sys.argv.remove("--recover-connection-reset")
    with observe_transport(ROOT, recover_connection_reset=recover):
        evaluation_main()


if __name__ == "__main__":
    main()
