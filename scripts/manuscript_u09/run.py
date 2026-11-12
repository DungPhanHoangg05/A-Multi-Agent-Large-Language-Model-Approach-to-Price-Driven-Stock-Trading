"""Sinh/kiểm artifact bài báo U09 offline; không sửa bản thảo hoặc release lịch sử."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main() -> None:
    """Chặn network trước khi import generator, chỉ đọc dữ liệu cục bộ đã nghiệm thu."""
    from core.revision_reproducibility import offline_guard
    from core.manuscript_u09.sources import encoded
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--release", default="outputs/revision/u09_manuscript_assets_v1")
    parser.add_argument("--artifact-only", action="store_true")
    args = parser.parse_args()
    with offline_guard():
        from core.manuscript_u09.release import build, verify
        result = build(ROOT, args.release, artifact_only=args.artifact_only) if args.command == "build" else verify(ROOT, args.release)
    print("Kết quả artifact bài báo U09: " + encoded(result).decode().strip())


if __name__ == "__main__":
    main()
