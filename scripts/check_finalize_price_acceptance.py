"""Kiểm acceptance FIN04 owner-attested offline, không sửa báo cáo độc lập frozen."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_price_acceptance import PROFILE, require_accepted_prices
from core.unified_contracts import json_bytes
from scripts.verify_original_fix_parity import deny_external_network


def main() -> None:
    """Đối soát byte/recipe/oracle cũ trước cho phép preparation thuộc profile mới."""
    deny_external_network()
    result = require_accepted_prices(ROOT, profile=PROFILE)
    print(json_bytes({key: result[key] for key in (
        "result", "profile", "FIN04_complete", "independent_price_pit_certified",
        "planned_forecasts", "economic_eligible_points", "economic_unavailable_points",
        "resources_rebuilt", "query_outcomes_computed", "hosted_api_calls")}).decode())


if __name__ == "__main__":
    main()
