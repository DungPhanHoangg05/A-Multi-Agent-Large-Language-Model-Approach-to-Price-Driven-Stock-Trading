"""Freeze H06 và kiểm biên prompt offline; không tự cấp release hoặc gọi API."""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from core.historical_evaluation_audit import verify_runtime
from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_graph import factor_lines, require_factors
from core.historical_evaluation_journal import load, save
from core.historical_evaluation_protocol import binding, digest

FREEZE = Path("docs/plan/week11/historical_evaluation_freeze.json")
H05 = Path("docs/plan/week11/historical_evaluation_validation.json")


def verify_h05(root: Path) -> dict:
    """Dùng lại gate đã PASS nếu mọi byte source/model/input/log vẫn nguyên vẹn."""
    verify_runtime(root)
    if (root / H05).read_bytes() != subprocess.check_output(["git", "show", "HEAD:" + H05.as_posix()], cwd=root):
        raise ValueError("Receipt H05 khác bản neo Git")
    record = load(root / H05)
    if record["status"] != "PASS" or record["api_released"] is not False:
        raise ValueError("H05 chưa PASS offline")
    for entry in [*record["bindings"].values(), record["test_log"], *record["prefix_models"]]:
        actual = binding(root, entry["path"])
        if any(actual[key] != entry[key] for key in ("path", "bytes", "sha256")):
            raise ValueError("Bằng chứng H05 thay đổi: " + entry["path"])
    HistoricalData(root).verify_sources()
    return record


def boundary_probe(config: dict, effective: dict) -> dict:
    """Chỉ stress template bằng fixture, không nhận là longest payload thực hoặc live smoke."""
    from mt_bicl_support import episode, original, reply
    from core.mt_bicl_context import prepare_variants
    from core.mt_bicl_teacher import BetaBernoulliTeacher
    from core.mt_bicl_decision import canonical_request as anchored
    from core.mt_bicl_prompt import canonical_request
    from core.mt_bicl_policy import resolve_anchor
    context = episode()
    packet = context["advisor"]["query_facts"]
    factors = [{"id": i, "name": f"Factor kiểm biên {i}", "value": .123456789, "signal": "TĂNG"} for i in range(1, 6)]
    shared = {"stock_name": context["query"]["symbol"], "as_of_date": context["query"]["as_of_date"],
              "time_frame": "1d", "language": "vi", "is_backtest": True,
              **{name + "_report": "Báo cáo FIXTURE_ONLY. " * 2000 for name in ("trend", "pattern", "indicator", "sentiment")},
              "alpha_report": "\n".join(factor_lines(factors))}
    variants = prepare_variants(context, BetaBernoulliTeacher([(i + 1) / 136 for i in range(16)]), lambda _: .6)
    anchor = resolve_anchor(packet, original("SHORT"), reply(packet, "SHORT", anchor=True),
                            original_source_sha256="1" * 64, anchor_source_sha256="2" * 64,
                            request_id="00000000-0000-4000-8000-000000000001")
    requests = {
        "legacy_no_prior": canonical_request(deepcopy(shared), "", {"decision": config}),
        "legacy_brpp_600": canonical_request(deepcopy(shared), "X" * 600, {"decision": config}),
        "Fact_Anchor": anchored(deepcopy(shared), effective, branch_id="Fact_Anchor", packet=packet),
    }
    selected = variants["branches"]["MT_BICL"]
    if not selected["eligible"]:
        raise ValueError("Fixture kiểm biên MT-BICL thiếu support, không đổi fallback")
    requests["MT_BICL"] = anchored(deepcopy(shared), effective, branch_id="MT_BICL", packet=packet,
                                   projection=selected["projection"], anchor=anchor)
    summaries = {}
    for name, request in requests.items():
        prompt = request["messages"][0]["content"]
        require_factors(prompt, factors)
        if len(prompt) >= 6500 or request["max_tokens"] != 960:
            raise ValueError("Prompt/options kiểm biên vượt hợp đồng")
        summaries[name] = {"chars": len(prompt), "request_sha256": digest(request)}
    try:
        canonical_request(deepcopy(shared), "X" * 601, {"decision": config})
    except ValueError:
        pass
    else:
        raise ValueError("Guard BRPP không chặn601 ký tự")
    return {"scope": "SYNTHETIC_BOUNDARY_ONLY_NOT_LIVE_SMOKE", "requests": summaries,
            "brpp_601_rejected": True, "five_factors_preserved": True, "fixture": True}


def main() -> None:
    """Đóng băng bằng chứng trước API; giữ trạng thái pending cho quota/live smoke."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    import torch
    from threadpoolctl import threadpool_limits
    torch.set_num_threads(1)
    with threadpool_limits(limits=1):
        h05 = verify_h05(ROOT)
        data = HistoricalData(ROOT)
        sources = {**h05["bindings"], H05.as_posix(): binding(ROOT, H05)}
        for name in ("scripts/prepare_historical_smoke.py", "tests/test_historical_smoke_freeze.py",
                     "docs/plan/week11/historical_evaluation_quota_template.json"):
            sources[name] = binding(ROOT, name)
        result = {"version": "historical_h06_freeze_v1", "status": "OFFLINE_FROZEN_NOT_RELEASED",
                  "bindings": sources, "runtime_sources": load(ROOT / "docs/plan/week11/historical_evaluation_runtime.json")["sources"],
                  "prefixes_sha256": digest(h05["prefix_models"]), "grid_units": len(data.inputs["grid"]),
                  "scope_ids_sha256": digest(data.inputs["scopes"]),
                  "boundary_probe": boundary_probe(data.protocol["inference"]["config"], data.protocol["effective_mt_bicl"]),
                  "pending": ["ACCOUNT_QUOTA_AND_ORG_INDEPENDENCE", "LIVE_REGISTRY_AND_LONGEST_PAYLOAD_SMOKE"],
                  "api_released": False, "llm_calls": 0}
        if args.verify:
            if (ROOT / FREEZE).read_bytes() != subprocess.check_output(["git", "show", "HEAD:" + FREEZE.as_posix()], cwd=ROOT):
                raise ValueError("Freeze chưa neo Git")
            if load(ROOT / FREEZE) != result:
                raise ValueError("Freeze khác source/runtime/input hiện tại")
        elif (ROOT / FREEZE).exists() and load(ROOT / FREEZE) != result:
            raise ValueError("Freeze đã tồn tại khác nội dung; cần revision")
        else:
            save(ROOT / FREEZE, result)
        print("H06: OFFLINE_FROZEN; chờ quota/account và live smoke; API vẫn khóa.")


if __name__ == "__main__":
    main()
