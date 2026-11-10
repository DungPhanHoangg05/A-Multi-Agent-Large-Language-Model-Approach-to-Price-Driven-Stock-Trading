"""Đọc catalog model Groq bằng GET; không inference, không ghi key hoặc mở grant."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import hmac
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.unified_contracts import json_bytes


class NoRedirect(HTTPRedirectHandler):
    """Không gửi Authorization qua redirect tới host khác."""
    def redirect_request(self, req: Request, fp: object, code: int, msg: str,
                         headers: object, newurl: str) -> None:
        return None


def audit(credential_file: Path) -> dict:
    """Chỉ sử dụng năm slot đã khai báo; thông báo lỗi không chứa header hoặc credential."""
    from dotenv import dotenv_values
    values = dotenv_values(credential_file)
    endpoint = "https://api.groq.com/openai/v1/models"
    models = ("openai/gpt-oss-20b", "qwen/qwen3.8-27b")
    rows = []
    for org in range(1, 6):
        name = f"GROQ_ORG_{org}_API_KEY"
        key = values.get(name)
        if not key:
            raise ValueError("Thiếu credential slot đã khai báo")
        request = Request(endpoint, method="GET", headers={"Authorization": "Bearer " + key,
                          "Accept": "application/json", "User-Agent": "unified-offline-preflight/2"})
        try:
            with build_opener(NoRedirect()).open(request, timeout=30) as response:
                data = json.load(response)
                available = {m["id"]: m for m in data["data"]}
                observed_headers = {k.lower(): v for k, v in response.headers.items()
                                    if k.lower() == "date" or k.lower().startswith("x-ratelimit-")}
                provider_org = response.headers.get("x-groq-organization-id")
                rows.append({"organization_slot": org, "credential_reference": name,
                    "credential_hmac": hmac.new(key.encode(), b"unified-u06-metadata-v2", hashlib.sha256).hexdigest(),
                    "provider_org_sha256": hashlib.sha256(provider_org.encode()).hexdigest() if provider_org else None,
                    "status": int(response.status), "model_catalog": {model: {k: available.get(model, {}).get(k)
                        for k in ("id", "active", "context_window", "owned_by")} for model in models},
                    "rate_headers": observed_headers})
        except HTTPError as error:
            raise ValueError(f"GET catalog bị từ chối tại slot {org}, HTTP {error.code}") from None
        except (URLError, TimeoutError, KeyError, json.JSONDecodeError):
            raise ValueError(f"Không xác minh được catalog tại slot {org}") from None
    return {"version": "unified_provider_metadata_v2", "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": endpoint, "method": "GET", "metadata_requests": 5, "inference_requests": 0,
        "authorization_changed": False, "rows": rows,
        "all_required_models_listed": all(row["model_catalog"][m]["id"] == m for row in rows for m in models),
        "provider_org_identity_available": all(row["provider_org_sha256"] is not None for row in rows),
        "limits_source": "FRESH_PUBLIC_DOCS_PLUS_EXPLICIT_CURRENT_ACCOUNT_ATTESTATION_REQUIRED"}


def main() -> None:
    """Tạo receipt mới; không đọc key trong các lệnh preflight offline khác."""
    parser = argparse.ArgumentParser(description="Kiểm metadata Groq, không inference")
    parser.add_argument("--credential-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError("Receipt đã tồn tại; không gọi lại metadata hoặc ghi đè")
        if args.output.resolve().is_relative_to(ROOT) and not args.output.resolve().is_relative_to(ROOT / "outputs/unified_integration"):
            raise ValueError("Receipt mới phải ở namespace tích hợp")
        result = audit(args.credential_file)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as handle:
            handle.write(json_bytes(result) + b"\n")
        print(json_bytes({"status": "PASS_METADATA_GET_ONLY", "metadata_requests": 5,
                          "inference_requests": 0, "all_required_models_listed": result["all_required_models_listed"]}).decode())
    except (ValueError, OSError) as error:
        parser.exit(2, "Không thể kiểm metadata: " + str(error) + "\n")


if __name__ == "__main__":
    main()
