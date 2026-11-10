"""CLI nghiệm thu U07 control-only; không có lệnh cấp quyền hoặc gọi inference."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.historical_evaluation_journal import load, save
from core.unified_contracts import digest
from core.unified_execution import PairedStudyRunner, verify_execution
from core.unified_execution_transport import MockHTTP, DurableCalls
from core.unified_preflight import MANIFEST_V2
from core.unified_protocol import MANIFEST, read, safe, git_blob


def checked_inputs(root: Path) -> dict:
    """Kiểm660 pin U06, chấp nhận source U07 mới có manifest riêng, không viết lại receipt U06."""
    if safe(root, MANIFEST_V2).read_bytes() != git_blob(root, "ec1ca7ec8a7789a2d18f1cccce328aeccb92ac73", MANIFEST_V2):
        raise ValueError("Manifest U06 khác commit đã nghiệm thu")
    parent = read(root, MANIFEST_V2, True)
    for name, binding in {**parent["source_bindings"], **parent["asset_bindings"]}.items():
        if hashlib.sha256(safe(root, name).read_bytes()).hexdigest() != binding["sha256"]:
            raise ValueError("Nguồn U06 đổi: " + name)
    from importlib.metadata import version
    import platform
    runtime = {"python": platform.python_version(), "packages": {name: version(name) for name in parent["runtime"]["packages"]}}
    if runtime != parent["runtime"]:
        raise ValueError("Runtime khác107 package và Python U06 đã khóa")
    return parent


def control_response(request: Any) -> Any:
    """Trả raw JSON chuẩn Groq có marker CONTROL; không căn cứ vào giá hoặc outcome."""
    import httpx
    body = json.loads(request.content)
    if "response_format" in body:
        prompt = body["messages"][0]["content"]
        reply = {"decision": "SHORT", "forecast_horizon": "T+2.5", "confidence": "Thấp",
            "risk_reward_ratio": 1., "evidence_for": "CONTROL_ONLY", "evidence_against": "Không phải dự báo thị trường",
            "justification": "Kiểm paired/recovery, không gọi LLM."}
        if "fact_assertions" in body["response_format"]["json_schema"]["schema"]["properties"]:
            marker = "Chỉ trả về một JSON hợp lệ, không Markdown hay chữ ngoài JSON:\n"
            template, _ = json.JSONDecoder().raw_decode(prompt.rsplit(marker, 1)[1])
            reply.update({k: deepcopy(template[k]) for k in ("version", "fact_ids", "fact_assertions", "context_reason")})
        content = json.dumps(reply, ensure_ascii=False)
    else:
        content = ("CONTROL_ONLY — không phải nhận định thị trường.\n**Thiên lệch dự báo:** BULLISH\n"
                   "**Hướng xu hướng:** BULLISH\nCó hỗ trợ, động lượng và xác nhận xu hướng trong fixture kiểm soát.")
    return httpx.Response(200, json={"id": "CONTROL_ONLY", "choices": [{"message": {"role": "assistant", "content": content}}],
                                     "usage": {"total_tokens": 500}})


def execute(root: Path, directory: Path, *, fixture_images: bool = False, limit: int | None = None) -> dict:
    """Lịch ảo chỉ dành QA; không biến thời gian mô phỏng thành ước lượng hoàn thành hosted."""
    from core.unified_execution_providers import StudyProviders, cold_methods
    from core.unified_experiment import source_identity, runtime_identity
    parent = checked_inputs(root)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ".gitignore").write_text("*\n", encoding="utf-8")
    original = read(root, MANIFEST, True)
    points = [{"id": p["runner_point_id"], "symbol": p["symbol"], "cutoff": p["date"], "fold": p["fold"],
               "quality": "U07_CONTROL_NOT_MARKET_FORECAST"} for p in original["points"]]
    identity = {"version": "unified_execution_control_v1", "mode": "CONTROL_ONLY", "epoch": "U07_MOCK_NOT_U08",
        "parent_manifest_sha256": digest(parent), "implementation": source_identity(root), "runtime": runtime_identity(),
        "points": points if limit is None else points[:limit], "repeats": 3, "realizations": 1, "fixture_images": fixture_images,
        "real_graph": True}
    identity["entrypoint_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    config = read(root, "docs/plan/week11/historical_evaluation_protocol.json", True)["inference"]["config"]
    models = config["signal_config"]["models"]
    identity["vision_options"] = {"model": models["graph_llm_model"], "stream": False, "n": 1,
        "temperature": max(1e-8, models["graph_llm_temperature"]), "stop": None, "reasoning_format": None,
        "reasoning_effort": None, "service_tier": config["service_tier"], **deepcopy(config["client_options"]["graph"]),
        "max_tokens": models["graph_llm_max_tokens"]}
    history = {i: {} for i in range(1, 6)}
    for item in original["quota_ledgers"]:
        org = int(Path(item["path"]).stem.removeprefix("org"))
        for row in read(root, item["path"])["requests"]:
            quota = {k: deepcopy(row[k]) for k in ("id", "model", "started_at", "reserved_tokens", "total_tokens",
                     "status", "completed_at", "retry_until", "rate_limits") if k in row}
            if row["id"] in history[org] and history[org][row["id"]] != quota:
                raise ValueError("Carry conflict")
            history[org][row["id"]] = quota
    clock_path = directory / "control_clock.json"
    now = [load(clock_path)["now"] if clock_path.exists() else time.time()]
    calls = DurableCalls(directory, digest(identity), identity["epoch"], MockHTTP(control_response),
                         {org: list(rows.values()) for org, rows in history.items()}, lambda: now[0])
    providers = StudyProviders(root, calls, fixture_images=fixture_images)
    runner = PairedStudyRunner(directory, identity, calls, providers)
    for tick in range(10000):
        result = runner.tick(providers, lambda p: {"point_id": p["id"], "status": "WITHHELD_CONTROL_NO_QUERY_PAYOFF"})
        print(json.dumps({**result, "tick": tick}, ensure_ascii=False), flush=True)
        if result["status"] == "COMPLETE":
            save(clock_path, {"now": now[0]})
            save(directory / "acceptance_identity.json", identity)
            verified = verify_execution(directory, identity, cold_methods(root, providers.data.protocol["inference"]["config"]))
            save(directory / "acceptance_result.json", verified)
            return verified
        if result["blocked"] or not result["waiting"]:
            raise ValueError("Run QA dừng có lỗi, giữ journal để đối soát")
        now[0] = max(now[0] + .01, min(result["waiting"].values()))
        save(clock_path, {"now": now[0]})
    raise ValueError("Lịch QA không hội tụ")


def main() -> None:
    """Chỉ namespace mới được chỉ định, verify không khởi tạo transport/provider/client."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("control", "verify"))
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--fixture-images", action="store_true")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if not args.namespace.startswith("outputs/unified_integration/u07_") or len(Path(args.namespace).parts) != 3:
        raise ValueError("U07 cần namespace riêng outputs/unified_integration/u07_*")
    directory = safe(ROOT, args.namespace)
    if args.command == "control":
        result = execute(ROOT, directory, fixture_images=args.fixture_images, limit=args.limit)
    else:
        from core.unified_execution_providers import cold_methods
        from core.unified_experiment import source_identity, runtime_identity
        checked_inputs(ROOT)
        identity = load(directory / "acceptance_identity.json")
        if (identity["implementation"] != source_identity(ROOT) or identity["runtime"] != runtime_identity()
                or identity["entrypoint_sha256"] != hashlib.sha256(Path(__file__).read_bytes()).hexdigest()):
            raise ValueError("Nguồn/runtime khác acceptance")
        config = read(ROOT, "docs/plan/week11/historical_evaluation_protocol.json", True)["inference"]["config"]
        result = verify_execution(directory, identity, cold_methods(ROOT, config))
        if result != load(directory / "acceptance_result.json"):
            raise ValueError("Acceptance summary không tái lập")
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
