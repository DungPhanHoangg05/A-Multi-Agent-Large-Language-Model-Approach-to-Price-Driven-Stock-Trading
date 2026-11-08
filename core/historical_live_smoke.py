"""Smoke H06 cách ly: bank tín hiệu kiểm soát, numeric PIT thật, không là kết quả H07."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
from typing import Any

from core.historical_evaluation_audit import verify_decision, serialized_body, serializer
from core.historical_evaluation_clients import Clients, RELEASE, RUNTIME, require_release
from core.historical_evaluation_context import ContextBank
from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_graph import GraphProvider, require_factors
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_prior import FeaturePopulation, signals
from core.historical_evaluation_protocol import PROTOCOL, digest, binding, CORE4
from core.historical_evaluation_runner import Regimes
from core.groq_pacing import MODEL_LIMITS, request_budget

DOC = Path("docs/plan/week11")
PLAN = DOC / "historical_evaluation_smoke_plan.json"
QUOTA = DOC / "historical_evaluation_quota.json"
RESULT = DOC / "historical_evaluation_smoke.json"
NAMESPACE = "outputs/historical_reevaluation/h06_smoke_r1"
CODE = ("core/historical_live_smoke.py", "scripts/run_historical_smoke.py", "tests/test_historical_live_smoke.py")
LEGACY = ("bayesian_v1", "C2", "A_tp_pool", "B_semantic")
BEFORE_RUNTIME = DOC / "historical_evaluation_runtime_pre_schema_title.json"
AMENDMENT = DOC / "historical_evaluation_transport_amendment.json"


def verified_baseline(root: Path) -> dict:
    """H05 v2 giữ nguyên; v3 chỉ nhận hai delta SDK đã kiểm hồi quy, không mượn gate cho code khác."""
    from core.historical_evaluation_audit import verify_runtime
    verify_runtime(root)
    h05 = anchored_file(root, DOC / "historical_evaluation_validation.json")
    before, after = load(root / BEFORE_RUNTIME), load(root / RUNTIME)
    changed = {name for name in before["sources"] if before["sources"][name] != after["sources"].get(name)}
    if (set(before["sources"]) != set(after["sources"]) or before["libraries"] != after["libraries"]
            or changed != {"core/historical_evaluation_clients.py", "core/historical_evaluation_audit.py"}
            or before["schema_sha256"] != after["schema_sha256"]):
        raise ValueError("Delta runtime vượt sửa tên schema SDK đã khai báo")
    for entry in [*h05["bindings"].values(), h05["test_log"], *h05["prefix_models"]]:
        path = BEFORE_RUNTIME if entry["path"] == RUNTIME.as_posix() else Path(entry["path"])
        actual = binding(root, path)
        if any(actual[key] != entry[key] for key in ("bytes", "sha256")):
            raise ValueError("Bằng chứng baseline H05 thay đổi: " + entry["path"])
    HistoricalData(root).verify_sources()
    return h05


def anchored_file(root: Path, name: Path) -> dict:
    """Mọi quyền API/plan phải đã neo Git; không nhận receipt tự sửa và băm lại."""
    if (root / name).read_bytes() != subprocess.check_output(["git", "show", "HEAD:" + name.as_posix()], cwd=root):
        raise ValueError("File chưa neo Git: " + name.as_posix())
    return load(root / name)


def quota_record() -> dict:
    """Ghi đúng xác nhận người dùng: không giả là org ID hoặc telemetry Console."""
    return {"status": "PASS", "scope": "USER_ATTESTED_FREE_ACCOUNTS", "evidence": "USER_EXPLICIT_CONFIRMATION",
            "independent_organizations": 5, "split_token_limits": False, "paid_api_allowed": False,
            "spend_limit_usd": 0, "models": deepcopy(MODEL_LIMITS),
            "organization_refs": {str(i): f"GROQ_ORG_{i}_API_KEY" for i in range(1, 6)},
            "provider_organization_ids": None}


def budget(request: dict) -> int:
    """Dựng body SDK thật trước API, kiểm reserve chứ không coi ký tự là token."""
    llm = serializer({key: request[key] for key in ("model", "temperature", "max_tokens", "service_tier", "client_options")})
    reserve = request_budget(serialized_body(llm, request["messages"][0]["content"], request["structured"]["schema"]))
    if reserve > 8000:
        raise ValueError(f"Payload cần reserve {reserve}>8.000 TPM; không gửi API")
    return reserve


class ProbeClients:
    """Chạy node thật trên ảnh thật, nhưng chặn mạng và chỉ thu payload để tính reserve."""
    def __init__(self, config: dict) -> None:
        self.config, self.reserves = config, []

    def models(self, org: int) -> tuple:
        return None, self

    def invoke(self, messages: Any, *args: Any, **kwargs: Any) -> Any:
        from langchain_core.messages import AIMessage
        config = self.config
        model = serializer({"model": config["signal_config"]["models"]["graph_llm_model"], "temperature": 0.,
                            "max_tokens": 960, "service_tier": "on_demand", "client_options": config["client_options"]["graph"]})
        reserve = request_budget(serialized_body(model, messages))
        if reserve > 8000:
            raise ValueError(f"Vision reserve {reserve}>8.000 TPM; không gửi API")
        self.reserves.append(reserve)
        return AIMessage(content="CONTROL_ONLY — không phải nhận định thị trường.\n**Thiên lệch dự báo:** BULLISH\n"
                         "**Hướng xu hướng:** BULLISH\nCó hỗ trợ, động lượng và xác nhận xu hướng trong fixture kiểm soát.")

    def stage(self, role: str, attempt: str, point: str, node: Any, state: dict) -> dict:
        from core.research_invocation import ENABLED, RECOVERY, invocation_scope
        enabled, recovery = ENABLED.set(True), RECOVERY.set(False)
        try:
            with invocation_scope(role):
                return node(deepcopy(state))
        finally:
            ENABLED.reset(enabled); RECOVERY.reset(recovery)


def history(data: HistoricalData, regimes: Regimes, unit: dict, shared: dict) -> list[dict]:
    """Tín hiệu bank được lặp từ query để kiểm support; giá/nhãn/regime quá khứ vẫn thật/PIT.

    Đây là control bank có nhãn rõ, không được import vào bank H07 hay báo hiệu quả thị trường.
    Không đọc bất kỳ payoff grid nào khi chưa có forecast.
    """
    current, rows = signals(shared), []
    bullish = any(data.scope.module("bayesian_memory").is_bullish(current[key]) for key in ("trend", "pattern"))
    for row in data.inputs["history"]:
        if (row["symbol"] != unit["symbol"] or row["exit_date"] >= unit["date"]
                or (row["symbol"], row["date"]) in data.by_day):
            continue
        label = data.label(row["symbol"], row["date"], as_of=unit["date"], forecast_done=lambda _: False)
        rows.append({"episode_id": row["id"], "symbol": row["symbol"], "as_of_date": row["date"],
                     "entry_date": label["entry_date"], "exit_date": label["exit_date"],
                     "regime": regimes.get(row["date"], historical=True), "agent_signals": deepcopy(current),
                     "outcome": {"net_return_pct": label["r_net"] * 100., "actual_direction": "UP" if label["y"] else "DOWN",
                                 "result": "WIN_IF_LONG" if label["y"] else "LOSS_IF_LONG", "was_bull_trap": bool(bullish and not label["y"])}})
    return rows


def requests(data: HistoricalData, unit: dict, shared: dict, episode: dict, variants: dict,
             population: FeaturePopulation, regimes: Regimes, anchor: dict | None = None) -> dict:
    from core.mt_bicl_prompt import canonical_request
    decider = data.scope.module("mt_bicl_decision")
    packet = episode["advisor"]["query_facts"]
    result = {"Original_common": canonical_request(deepcopy(shared), "", {"decision": data.protocol["inference"]["config"]}),
              "Fact_Anchor": decider.canonical_request(deepcopy(shared), data.protocol["effective_mt_bicl"], branch_id="Fact_Anchor", packet=packet)}
    records = history(data, regimes, unit, shared)
    for branch in LEGACY:
        request, proof = population.request(branch, deepcopy(shared), regimes.get(unit["date"]), records, 0)
        if proof.get("fallback"):
            raise ValueError("Control không kích hoạt prior " + branch + "; không đổi fallback")
        result[branch] = request
    saturated = deepcopy(shared)
    for field in ("indicator_report", "pattern_report", "trend_report", "sentiment_report"):
        saturated[field] = "Báo cáo CONTROL_ONLY. " * 2000
    result["BRPP_600_CONTROL"] = canonical_request(saturated, "X" * 600, {"decision": data.protocol["inference"]["config"]})
    if anchor is not None:
        projection = variants["branches"]["MT_BICL"]["projection"]
        for branch, reports in (("MT_BICL", shared), ("MT_MAX_CONTROL", saturated)):
            result[branch] = decider.canonical_request(deepcopy(reports), data.protocol["effective_mt_bicl"],
                branch_id="MT_BICL", packet=packet, projection=projection, anchor=anchor)
    for request in result.values():
        require_factors(request["messages"][0]["content"], shared["alpha_factors"])
        budget(request)
    return result


def prepare(root: Path) -> dict:
    """Khóa quota, chọn control đủ support trước API và cấp đúng grant SMOKE hữu hạn."""
    import tempfile
    verified_baseline(root)
    freeze = anchored_file(root, DOC / "historical_evaluation_freeze.json")
    for entry in freeze["bindings"].values():
        path = BEFORE_RUNTIME if entry["path"] == RUNTIME.as_posix() else Path(entry["path"])
        actual = binding(root, path)
        if any(actual[key] != entry[key] for key in ("bytes", "sha256")):
            raise ValueError("Freeze H06 đã đổi")
    data = HistoricalData(root)
    context, population = ContextBank(data, lambda _: False), FeaturePopulation(data)
    regimes = Regimes(data, root / "outputs/historical_reevaluation/h04_assets/legacy_regimes")
    regimes.preflight()
    config = data.protocol["inference"]["config"]
    candidates = [u for u in data.inputs["grid"] if u["symbol"] in CORE4 and u["anchor"]]
    # Ưu tiên prefix trưởng thành dài nhất, không dùng payoff query hoặc kết quả LLM để chọn control.
    candidates.sort(key=lambda u: (u["date"], u["symbol"]), reverse=True)
    selected = None
    for unit in candidates:
        episode = context.build(unit["symbol"], unit["date"])
        if episode["status"] != "AVAILABLE":
            continue
        NoActionableContext = data.scope.module("mt_bicl_context").NoActionableContext
        try:
            variants = context.variants(episode)
        except NoActionableContext:
            continue
        if not variants["branches"]["MT_BICL"]["eligible"]:
            continue
        selected = unit, episode, variants
        break
    if selected is None:
        raise ValueError("Không có control MT-BICL đủ support")
    unit, episode, variants = selected
    probe = ProbeClients(config)
    with tempfile.TemporaryDirectory() as folder:
        shared = GraphProvider(data, probe).shared(RunBook(Path(folder), {"scope": "OFFLINE_CONTROL_PROBE"}), unit["symbol"], unit["date"], 0, 1)
    # Chỉ anchor fixture ở preflight; live smoke bắt buộc dùng raw Original/Fact_Anchor thật.
    from mt_bicl_support import original, reply
    from uuid import UUID
    packet = episode["advisor"]["query_facts"]
    anchor = data.scope.module("mt_bicl_policy").resolve_anchor(packet, original("SHORT"), reply(packet, "SHORT", anchor=True),
        original_source_sha256="1" * 64, anchor_source_sha256="2" * 64, request_id=str(UUID(int=1)))
    rendered = requests(data, unit, shared, episode, variants, population, regimes, anchor)
    result = {"status": "PASS", "scope": "SMOKE_PREFLIGHT_ONLY_CONTROL_BANK_NO_RESEARCH_FORECASTS", "unit": unit,
              "control_bank_policy": "PAST_NON_GRID_LABELS_REAL_QUERY_SIGNALS_REPLICATED_EXPLICIT_FIXTURE",
              "bindings": {name: binding(root, name) for name in (*CODE, (DOC / "historical_evaluation_freeze.json").as_posix(),
                            BEFORE_RUNTIME.as_posix(), RUNTIME.as_posix())},
              "h05_sha256": binding(root, DOC / "historical_evaluation_validation.json")["sha256"],
              "quota_sha256": digest(quota_record()), "vision_reserves": probe.reserves,
              "request_chars": {k: len(v["messages"][0]["content"]) for k, v in rendered.items()},
              "request_reserves": {k: budget(v) for k, v in rendered.items()},
              "nominal_executions": 55, "max_http_attempts": 300, "organizations": 5}
    for name, value in ((QUOTA, quota_record()), (PLAN, result)):
        if (root / name).exists() and load(root / name) != value:
            raise ValueError("Plan/quota khác bản đã khóa; cần revision")
        save(root / name, value)
    grant = {"status": "RELEASED", "mode": "SMOKE", "api": True, "quota_verified": True,
             "quota_evidence": "USER_ATTESTATION_FREE_0_USD", "protocol_sha256": binding(root, PROTOCOL)["sha256"],
             "runtime_sha256": binding(root, RUNTIME)["sha256"], "receipts": {
                 name.as_posix(): binding(root, name)["sha256"] for name in (DOC / "historical_evaluation_validation.json", QUOTA, PLAN)}}
    if (root / RELEASE).exists() and load(root / RELEASE) != grant:
        raise ValueError("Release đã có nội dung khác; không ghi đè")
    save(root / RELEASE, grant)
    return result


def run(root: Path, *, verify_only: bool = False) -> dict:
    """Mỗi org một upstream thật; checkpoint trước HTTP, dừng lỗi/unknown, tuyệt đối không mở query-y."""
    plan = anchored_file(root, PLAN)
    quota = anchored_file(root, QUOTA)
    if quota != quota_record() or digest(quota) != plan["quota_sha256"]:
        raise ValueError("Quota khác xác nhận đã khóa")
    for entry in plan["bindings"].values():
        if binding(root, entry["path"]) != entry:
            raise ValueError("Source/plan smoke đã đổi")
    verified_baseline(root)
    if not verify_only and require_release(root)["mode"] != "SMOKE":
        raise ValueError("Smoke chỉ dùng grant SMOKE")
    data = HistoricalData(root)
    identity = {"scope": "H06_CONTROL_ONLY_NOT_H07", "plan_sha256": binding(root, PLAN)["sha256"],
                "runtime_sha256": binding(root, RUNTIME)["sha256"]}
    book = RunBook(root / NAMESPACE, identity, verify_only=verify_only)
    clients = None if verify_only else Clients(data, book)
    if not verify_only:
        from dotenv import load_dotenv
        import os
        load_dotenv(root / ".env", override=False)
        keys = [os.environ.get(f"GROQ_ORG_{i}_API_KEY") for i in range(1, 6)]
        if any(not k for k in keys) or len(set(keys)) != 5:
            raise ValueError("Cần5 key khác nhau theo mapping người dùng đã xác nhận")
    context, population = ContextBank(data, lambda _: False), FeaturePopulation(data)
    regimes = Regimes(data, root / "outputs/historical_reevaluation/h04_assets/legacy_regimes")
    unit = plan["unit"]
    episode = context.build(unit["symbol"], unit["date"])
    variants = context.variants(episode)
    if not variants["branches"]["MT_BICL"]["eligible"]:
        raise ValueError("MT-BICL mất support; không gửi API")
    graph = GraphProvider(data, clients)
    shared_by_org, batches, outputs, anchors = {}, {}, {}, {}
    for org in range(1, 6):
        shared = graph.shared(book, unit["symbol"], unit["date"], org - 1, org)
        shared_by_org[org] = shared
        batches[org] = requests(data, unit, shared, episode, variants, population, regimes)
        outputs[org] = {}
        print(f"Đã lưu upstream thật org{org}.", flush=True)
    # Round-robin giữa org độc lập, không xoay key khi một org hết quota.
    for branch in ("Original_common", "Fact_Anchor", *LEGACY, "MT_BICL", "BRPP_600_CONTROL", "MT_MAX_CONTROL"):
        for org in range(1, 6):
            anchor = anchors.get(org)
            if branch in ("MT_BICL", "MT_MAX_CONTROL"):
                if anchor is None or not anchor["policy"]["fact_assertions_valid"]:
                    raise ValueError("Live Fact_Anchor sai facts; không giả anchor hoặc đổi fallback")
                batches[org] = requests(data, unit, shared_by_org[org], episode, variants, population, regimes, anchor)
            request = batches[org][branch]
            response = book.execute(f"org{org}/{branch}", {"org": org, "request": request, "scope": identity["scope"]},
                lambda attempt: clients.decision(org, deepcopy(request), attempt, branch),
                validate=lambda actual: verify_decision(book, actual, branch, fixture=False, request=request))
            outputs[org][branch] = response
            if branch == "Fact_Anchor":
                anchors[org] = data.scope.module("mt_bicl_policy").resolve_anchor(episode["advisor"]["query_facts"],
                    outputs[org]["Original_common"]["reply"], response["reply"],
                    original_source_sha256=digest(outputs[org]["Original_common"]), anchor_source_sha256=digest(response),
                    request_id=response["request_id"])
            if branch in ("MT_BICL", "MT_MAX_CONTROL"):
                data.scope.module("mt_bicl_policy").apply_revision(episode["advisor"]["query_facts"], anchor,
                    variants["branches"]["MT_BICL"], reply=response["reply"], request_id=response["request_id"])
            print(f"Đã smoke {branch} ở org{org}.", flush=True)
    completed = list(range(1, 6))
    records = {}
    for directory in ("slots", "http", "usage", "images"):
        for path in sorted((book.directory / directory).rglob("*")):
            if path.is_file():
                records[path.relative_to(root).as_posix()] = binding(root, path.relative_to(root))
    result = {"status": "PASS", "scope": identity["scope"], "run_uuid": book.uuid,
              "organizations": completed, "nominal_executions": 55, "plan_sha256": binding(root, PLAN)["sha256"],
              "records_sha256": digest(records), "control_bank_not_research": True, "query_payoff_opened": False,
              "paid_api_allowed": False, "api_research_released": False}
    if verify_only:
        if load(root / RESULT) != result:
            raise ValueError("Smoke receipt khác cold replay")
    else:
        save(root / RESULT, result)
    return result
