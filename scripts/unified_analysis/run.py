"""CLI U09 offline; freeze/analyze/verify không đọc key, tạo client hoặc huấn luyện."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main() -> None:
    """Chặn mạng và constructor live trong cả lượt phân tích lẫn cold replay."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("freeze", "analyze", "verify"))
    args = parser.parse_args()
    from scripts.verify_original_fix_parity import deny_external_network
    deny_external_network()
    with ExitStack() as stack:
        for name in ("httpx.Client", "httpx.AsyncClient", "httpx.HTTPTransport", "langchain_groq.ChatGroq",
                     "dotenv.dotenv_values", "core.unified_execution_providers.StudyProviders"):
            stack.enter_context(patch(name, side_effect=AssertionError("U09 cấm key/client/provider: " + name)))
        from core.unified_analysis.runtime import freeze, run, verify
        result = {"freeze": freeze, "analyze": run, "verify": verify}[args.command](ROOT)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
