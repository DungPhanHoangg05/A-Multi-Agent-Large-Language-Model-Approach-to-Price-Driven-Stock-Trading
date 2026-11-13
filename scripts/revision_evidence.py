"""Liệt kê, kiểm hoặc khôi phục một release lịch sử; không gọi API hay inference."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.revision_evidence_archive import EvidenceArchive, load_index


def main() -> None:
    """Chỉ khôi phục khi người vận hành chọn rõ tên release và thư mục đích."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("list", "verify", "restore"))
    parser.add_argument("release", nargs="?")
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()
    index = load_index(ROOT)
    if args.action == "list":
        print(json.dumps(index["directories"], ensure_ascii=False, indent=2))
        return
    if args.release and args.release not in index["directories"]:
        parser.error("Không tìm thấy release trong chỉ mục")
    with EvidenceArchive(ROOT, index) as archive:
        if args.action == "verify":
            prefix = "outputs/revision/" + args.release + "/" if args.release else ""
            print("Đã kiểm nguyên byte:", archive.verify(prefix), "tệp")
        else:
            if not args.release:
                parser.error("Cần chỉ định release muốn khôi phục")
            print("Đã khôi phục:", archive.restore(args.release, args.destination), "tệp")


if __name__ == "__main__":
    main()
