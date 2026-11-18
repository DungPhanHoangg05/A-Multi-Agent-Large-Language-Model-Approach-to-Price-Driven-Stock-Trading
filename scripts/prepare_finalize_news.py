"""Tạo/kiểm release FIN05 offline, không ghi đè artifact frozen khác byte."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_news_release import CORPUS, COVERAGE, check_release, coverage, prepare_corpus
from core.unified_contracts import digest, json_bytes
from scripts.verify_original_fix_parity import deny_external_network


def main() -> None:
    """Khóa corpus trước sử dụng; --check không sửa hoặc tự tải nguồn thiếu."""
    deny_external_network()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        result = check_release(ROOT)
    else:
        corpus = prepare_corpus(ROOT)
        result = coverage(ROOT, corpus)
        outputs = [(ROOT / name, json_bytes({"payload": p, "sha256": digest(p)}))
                   for name, p in ((CORPUS, corpus), (COVERAGE, result))]
        if any(path.exists() and path.read_bytes() != raw for path, raw in outputs):
            raise ValueError("Không ghi đè release khác byte; cần version mới")
        for path, raw in outputs:
            if not path.exists():
                with path.open("xb") as handle:
                    handle.write(raw)
    print(json_bytes({key: result[key] for key in (
        "result", "FIN05_complete", "planned_points", "available_points", "unavailable_points",
        "content_pit_proven_articles", "model_forward_calls", "hosted_api_calls")}).decode())


if __name__ == "__main__":
    main()
