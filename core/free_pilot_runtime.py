"""Runner pilot48 tách full-run: shared seal trước Decision, quota carry-over và cold replay."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from typing import Any

from core.free_pilot_assets import (DOC, DIRECTORY, PROTOCOL, INPUTS, RUNTIME, AUDIT, GRANT,
    PilotData, FrozenBank, call_order, carry_over, archive_audit, budget_schedule, anchored, source_files)
from core.historical_evaluation_clients import Clients
from core.historical_evaluation_context import ContextBank
from core.historical_evaluation_graph import GraphProvider, require_factors
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import binding, digest, PRIMARY
from core.historical_evaluation_audit import verify_decision
from core.groq_pacing import MODEL_LIMITS, request_budget, PilotStop
from core.prior_run_lock import utc_now

SMOKE = {"id": "smoke_FPT_2023_06_23", "symbol": "FPT", "date": "2023-06-23", "org": 5}


def rendered_request(data: PilotData, shared: dict, branch: str, packet: dict,
                     variant: dict | None = None, anchor: dict | None = None) -> dict:
    """Reports/distill/cap/factor rows giống nhau; anchored bổ sung đúng COMMON_INSTRUCTION."""
    from core.mt_bicl_prompt import COMMON_INSTRUCTION
    from core.mt_bicl_prompt_limits import check_prompt_length
    module = data.scope.module("mt_bicl_decision")
    if branch not in ("Fact_Anchor", "MT_BICL"):
        raise ValueError("Renderer anchored chỉ có hai nhánh pilot")
    request = module.canonical_request(deepcopy(shared), data.protocol["effective_mt_bicl"], branch_id=branch,
        packet=packet, projection=variant["projection"] if variant else None, anchor=anchor)
    request["messages"][0]["content"] = COMMON_INSTRUCTION + "\n" + request["messages"][0]["content"]
    check_prompt_length(request["messages"][0]["content"])
    require_factors(request["messages"][0]["content"], shared["alpha_factors"])
    return request


def reserve(request: dict) -> int:
    """Băm/đếm body SDK thực, không đánh đồng ký tự và token."""
    from core.historical_evaluation_audit import serializer, serialized_body
    model = serializer({k: request[k] for k in ("model", "temperature", "max_tokens", "service_tier", "client_options")})
    return request_budget(serialized_body(model, request["messages"][0]["content"], request["structured"]["schema"]))


def protocol_record() -> dict:
    """Lock estimand/lịch/call cap mới, bridge OFF và48h không tự reset khi resume."""
    return {"version": "free_paired_pilot_48_v1", "status": "LOCKED_OFFLINE", "primary": list(PRIMARY),
        "dependency": "Fact_Anchor", "bridge_full_fix_native960": False, "repeat": 1,
        "bayesian_memory": "FROZEN_852_EXIT_LE_2022_12_30", "mt_memory": "NUMERIC_PIT_SELECTED_QUERY_GATED",
        "query_source": "DONOR_FIX_VALID_SUFFIX", "scope": "HISTORICAL_EXPLORATORY_CONDITIONAL_ON_SHARED_REPORTS",
        "nominal": {"decision": 336, "new_vision": 96, "smoke": 9}, "max_http": 1323,
        "retry_reserve_fraction": .20, "collection_deadline_hours": 48, "target_collection_hours": 24,
        "paid_api_allowed": False, "spend_limit_usd": 0,
        "bootstrap": {"type": "CIRCULAR_SELECTED_DATE_WITHIN_YEAR", "block_length": 2, "draws": 10000,
            "rng": "PCG64", "seed": 20261109, "min_joint_finite": 9500, "family": "FIVE_CONTRASTS_CENTERED_MAX_DEVIATION_95"},
        "economics": {"entry": "Open(t+1)", "exit": "Close(t+3)", "short": "CASH", "fee": .0025,
            "slippage": .001, "fractional": True, "reset_vnd": 50000000, "reset_by": "SYMBOL_YEAR_METHOD"}}


def prepare(root: Path) -> dict:
    """P01/P02 offline; không gọi mạng, không đọc payoff48 query hoặc train teacher/student."""
    from tempfile import TemporaryDirectory
    from core.historical_live_smoke import ProbeClients
    from core.bayesian_memory import atomic_write_json
    from core.mt_bicl_prompt import canonical_request
    from core.historical_evaluation_runner import Regimes
    from core.historical_transport_observer import RECOVERY_POLICY
    if (root / PROTOCOL).exists():
        verify_locked(root)
        return anchored(root, AUDIT)
    data = PilotData(root); units = data.inputs["grid"]; bank = FrozenBank(data)
    carry, carry_proofs = carry_over(root)
    for values in carry.values():
        if any(r["model"] not in MODEL_LIMITS or r.get("total_tokens", 0) > r["reserved_tokens"] for r in values):
            raise ValueError("Carry-over sai model hoặc thiếu reserve")
    context = ContextBank(data, lambda _: False)
    coverage = []
    for row in units:
        episode = context.build(row["symbol"], row["date"])
        variants = context.variants(episode)
        coverage.append({"id": row["id"], "status": episode["status"], "K": episode["K"], "m": episode["m"],
                         "MT_eligible": variants["branches"]["MT_BICL"]["eligible"], "context_sha256": digest(episode),
                         "query_feature": data.features(row["symbol"], row["date"])["status"]})
    # Probe report là control tạm, không được nhập vào shared/forecast production.
    with TemporaryDirectory() as directory:
        probe = ProbeClients(data.protocol["inference"]["config"])
        shared = GraphProvider(data, probe).shared(RunBook(Path(directory), {"probe": True}), SMOKE["symbol"], SMOKE["date"], 0, SMOKE["org"])
    saturated = deepcopy(shared)
    for field in ("indicator_report", "pattern_report", "trend_report", "sentiment_report"):
        saturated[field] = "Báo cáo kiểm ngân sách, chưa phải forecast. " * 2000
    request = canonical_request(saturated, "X" * 600, {"decision": data.protocol["inference"]["config"]})
    from core.historical_evaluation_runner import FixtureClients
    from uuid import uuid4
    smoke_context = ContextBank(data, lambda _: False)
    smoke_episode = smoke_context.build(SMOKE["symbol"], SMOKE["date"])
    smoke_variant = smoke_context.variants(smoke_episode)["branches"]["MT_BICL"]
    packet = smoke_episode["advisor"]["query_facts"]
    policy = data.scope.module("mt_bicl_policy")
    anchor_request = rendered_request(data, saturated, "Fact_Anchor", packet)
    fake = FixtureClients()
    original_reply = fake.decision(5, request, str(uuid4()), "Original_common")["reply"]
    anchor_reply = fake.decision(5, anchor_request, str(uuid4()), "Fact_Anchor")["reply"]
    control_anchor = policy.resolve_anchor(packet, original_reply, anchor_reply,
        original_source_sha256=digest(original_reply), anchor_source_sha256=digest(anchor_reply), request_id=str(uuid4()))
    if not smoke_variant["eligible"]:
        raise ValueError("Smoke đã khóa không đủ MT support; không tự chọn lại điểm")
    controls = {b: bank.request(b, deepcopy(shared), Regimes(data, root).get(SMOKE["date"]))[0]
                for b in PRIMARY if b != "MT_BICL"}
    controls.update(BRPP_600=request, Fact_Anchor=anchor_request,
                    MT_BICL=rendered_request(data, saturated, "MT_BICL", packet, smoke_variant, control_anchor))
    payload_reserves = {b: reserve(r) for b, r in controls.items()}
    decision_reserve = max(4500, *payload_reserves.values())
    vision = probe.reserves
    if len(vision) != 2 or max(vision + [decision_reserve]) > 8000:
        raise ValueError("Payload vượt quota TPM, không tự hạ cap")
    tasks = [{"org": SMOKE["org"], "model": "qwen/qwen3.8-27b", "tokens": v} for v in vision]
    tasks += [{"org": SMOKE["org"], "model": "openai/gpt-oss-20b", "tokens": decision_reserve} for _ in range(7)]
    tasks += [{"org": u["org"], "model": "qwen/qwen3.8-27b", "tokens": v} for u in units for v in vision]
    tasks += [{"org": u["org"], "model": "openai/gpt-oss-20b", "tokens": decision_reserve} for u in units for _ in range(7)]
    # Reserve20% là ngân sách đã khóa; trần3/slot vẫn do transport kiểm, không cấp vô hạn token.
    import math
    retry_tasks = []
    for org in range(1, 6):
        for model in MODEL_LIMITS:
            group = [t for t in tasks if t["org"] == org and t["model"] == model]
            retry_tasks.extend(deepcopy(group[:math.ceil(len(group) * .2)]))
    telemetry = []
    for org in range(1, 6):
        old = json.loads((root / f"outputs/historical_reevaluation/h06_smoke_r1/usage/org{org}.json").read_bytes())
        telemetry.extend(float(r["latency_seconds"]) for r in old["requests"] if r["status"] == 200)
    latency = max(10., sorted(telemetry)[int(.95 * (len(telemetry) - 1))] * 1.5)
    budget = budget_schedule(carry, [*tasks, *retry_tasks], start=time.time(), latency=latency)
    audit = {"status": budget["status"], "scope": "P01_OFFLINE_NO_QUERY_PAYOFF", "bank": bank.audit,
        "cache": archive_audit(root, units), "coverage": coverage, "quota_carry": carry_proofs,
        "carry_requests": sum(len(v) for v in carry.values()),
        "carry_charged_or_reserved": sum(r.get("total_tokens") or r["reserved_tokens"] for v in carry.values() for r in v),
        "budget": budget, "decision_planning_reserve": decision_reserve, "vision_reserves": vision,
        "payload_controls": payload_reserves, "control_forecasts_imported": False,
        "budget_method": "SATURATED_REPORT_CONTROL_MIN4500_PER_DECISION_PLUS20PCT_RETRY; ACTUAL_ADMISSION_RECHECKED",
        "collection_deadline_guaranteed": False, "llm_calls": 0, "teacher_student_fit": False}
    save(root / AUDIT, audit)
    if audit["status"] != "PASS":
        return audit
    protocol = protocol_record()
    inputs = {"status": "LOCKED", "units": units, "smoke": SMOKE,
              "source_inputs": binding(root, DOC / "historical_evaluation_inputs.json"),
              "call_orders": {u["id"]: call_order(i) for i, u in enumerate(units)}}
    runtime = {"status": "PASS", "sources": source_files(root), "bank": binding(root, "data_manager/regime_memory_store.json"),
               "bank_manifest": binding(root, "data_manager/regime_memory_store.manifest.json"),
               "bank_audit": binding(root, "docs/plan/week2/memory_bank_audit.json"), "index_identity": bank.index.identity,
               "baseline_runtime": binding(root, DOC / "historical_evaluation_runtime.json"), "transport_policy": RECOVERY_POLICY}
    for path, value in ((PROTOCOL, protocol), (INPUTS, inputs), (RUNTIME, runtime)):
        if (root / path).exists() and load(root / path) != value:
            raise ValueError("Pilot đã khóa khác nguồn; cần revision, không ghi đè")
        save(root / path, value)
    identity = {"scope": "FREE_PAIRED_PILOT_48", "protocol": binding(root, PROTOCOL)["sha256"],
                "inputs": binding(root, INPUTS)["sha256"], "runtime": binding(root, RUNTIME)["sha256"]}
    book = RunBook(root / DIRECTORY, identity)
    campaign_path = book.directory / "campaign.json"
    if not campaign_path.exists():
        save(campaign_path, {"run_uuid": book.uuid, "created_at": utc_now(), "deadline_epoch": time.time() + 172800})
    campaign = load(campaign_path)
    if campaign["run_uuid"] != book.uuid:
        raise ValueError("Campaign khác UUID, không reset quota/deadline")
    for org, values in carry.items():
        path = book.directory / "usage" / f"org{org}.json"
        if not path.exists():
            atomic_write_json(path, {"version": 1, "limits": MODEL_LIMITS, "requests": values})
    save(book.directory / "bank_index.json", bank.index.payload)
    grant = {"status": "SMOKE_READY", "api": True, "paid_api_allowed": False, "run_uuid": book.uuid,
             "protocol_sha256": identity["protocol"], "runtime_sha256": identity["runtime"],
             "audit_sha256": binding(root, AUDIT)["sha256"], "campaign_sha256": binding(root, campaign_path.relative_to(root))["sha256"]}
    if (root / GRANT).exists() and load(root / GRANT) != grant:
        raise ValueError("Grant pilot đã có nội dung khác")
    save(root / GRANT, grant)
    return audit


def verify_locked(root: Path) -> tuple[dict, dict]:
    """Kiểm Git/hash source/model/data pilot riêng, không dùng grant full đã revoked."""
    protocol, inputs, runtime = (anchored(root, p) for p in (PROTOCOL, INPUTS, RUNTIME))
    if runtime["sources"] != source_files(root):
        raise ValueError("Runtime pilot đổi source")
    if anchored(root, AUDIT)["status"] != "PASS":
        raise ValueError("P01 chưa PASS")
    for entry in (runtime["bank"], runtime["bank_manifest"], runtime["bank_audit"], runtime["baseline_runtime"]):
        if binding(root, entry["path"]) != entry:
            raise ValueError("Asset pilot đổi byte")
    return protocol, inputs


class PilotClients(Clients):
    """Tái dùng SDK/transport gốc, grant riêng và accounting gồm mọi carry-over."""
    def __init__(self, data: PilotData, book: RunBook, *, mode: str) -> None:
        protocol, _ = verify_locked(data.root)
        grant = anchored(data.root, GRANT)
        if (grant.get("api") is not True or grant.get("paid_api_allowed") is not False or grant["run_uuid"] != book.uuid
                or grant["protocol_sha256"] != binding(data.root, PROTOCOL)["sha256"]
                or grant["runtime_sha256"] != binding(data.root, RUNTIME)["sha256"]
                or grant["audit_sha256"] != binding(data.root, AUDIT)["sha256"]
                or grant["campaign_sha256"] != binding(data.root, DIRECTORY / "campaign.json")["sha256"]
                or grant["status"] not in (("SMOKE_READY",) if mode == "smoke" else ("PILOT_RELEASED",))):
            raise ValueError("Pilot chưa có grant đúng giai đoạn/UUID")
        self.data, self.book, self.cached, self.mode = data, book, {}, mode
        self.http_count = sum(not r.get("carry_over", False) for path in (book.directory / "usage").glob("org*.json")
                              for r in json.loads(path.read_bytes())["requests"])
        self.attempt_cap = 27 if mode == "smoke" else protocol["max_http"]
        self.deadline = load(book.directory / "campaign.json")["deadline_epoch"]
        self.data.api_deadline = self.deadline
        self.data.api_guard = self.verify_release
        self.verify_quota()
        if mode != "smoke":
            self.require_smoke(grant)

    def verify_quota(self) -> None:
        """Không cho xóa ledger hoặc carry-over để lấy quota mới theo namespace."""
        carry, proofs = carry_over(self.data.root)
        if proofs != load(self.data.root / AUDIT)["quota_carry"]:
            raise ValueError("Nguồn quota carry-over đổi so P01")
        for org, expected in carry.items():
            path = self.book.directory / "usage" / f"org{org}.json"
            if not path.is_file():
                raise ValueError("Thiếu quota ledger, không được khởi tạo quota từ zero")
            rows = json.loads(path.read_bytes())["requests"]
            by_id = {r["id"]: r for r in rows}
            if len(by_id) != len(rows) or any(by_id.get(r["id"]) != r for r in expected):
                raise ValueError("Quota ledger thiếu/đổi carry-over hoặc trùng ID")

    def require_smoke(self, grant: dict) -> None:
        """Grant nghiên cứu phải bind cold smoke đúng UUID/runtime, không dùng H06 cũ."""
        path = DIRECTORY / "smoke_verified.json"
        if grant.get("smoke_receipt") != binding(self.data.root, path):
            raise ValueError("Grant chưa bind cold smoke pilot")
        receipt = load(self.data.root / path)
        if (receipt["status"] != "SMOKE_COLD_PASS" or receipt["run_uuid"] != self.book.uuid
                or receipt["identity"] != identity(self.data.root)):
            raise ValueError("Smoke không khớp runtime/UUID pilot")
        for name, expected in receipt["slots"].items():
            from core.prior_run_lock import safe_path
            if hashlib.sha256(safe_path(self.book.directory, "slots/" + name).read_bytes()).hexdigest() != expected:
                raise ValueError("Slot smoke đổi sau cold verify")

    def verify_release(self) -> None:
        """Kiểm lại source/grant ngay trước mỗi HTTP, kể cả sau thời gian chờ quota."""
        verify_locked(self.data.root)
        grant = anchored(self.data.root, GRANT)
        if (grant["run_uuid"] != self.book.uuid or grant.get("api") is not True
                or self.book.signature != digest(identity(self.data.root))
                or grant.get("paid_api_allowed") is not False
                or grant["status"] != ("SMOKE_READY" if self.mode == "smoke" else "PILOT_RELEASED")
                or grant["campaign_sha256"] != binding(self.data.root, DIRECTORY / "campaign.json")["sha256"]
                or grant["audit_sha256"] != binding(self.data.root, AUDIT)["sha256"]):
            raise PilotStop("Grant đã thu hồi/đổi nguồn; chưa gửi HTTP")
        if self.mode != "smoke":
            self.require_smoke(grant)
        self.verify_quota()

    def stage(self, role: str, attempt: str, point: str, node: Any, state: dict) -> dict:
        if self.mode == "smoke" and point != "FPT-2023-06-23/u0":
            raise ValueError("Grant smoke không cho phép upstream nghiên cứu")
        if time.time() >= self.deadline:
            raise PilotStop("PARTIAL_DEADLINE_48H; giữ raw/checkpoint, không tạo CASH")
        return super().stage(role, attempt, point, node, state)

    def decision(self, org: int, request: dict, attempt: str, branch: str) -> dict:
        if branch not in (*PRIMARY, "Fact_Anchor"):
            raise ValueError("Nhánh ngoài pilot")
        if time.time() >= self.deadline or reserve(request) > load(self.data.root / AUDIT)["decision_planning_reserve"]:
            raise PilotStop("PARTIAL_DEADLINE_OR_BUDGET; không gửi request")
        if self.mode == "smoke" and request["point_id"] != "FPT-2023-06-23":
            raise ValueError("Grant smoke không cho phép query nghiên cứu")
        return super().decision(org, request, attempt, branch)


def identity(root: Path) -> dict:
    """Identity không chứa grant để giữ UUID khi chuyển smoke sang nghiên cứu."""
    return {"scope": "FREE_PAIRED_PILOT_48", **{name: binding(root, path)["sha256"]
            for name, path in (("protocol", PROTOCOL), ("inputs", INPUTS), ("runtime", RUNTIME))}}


class PilotRunner:
    """Runner48: cùng shared seal, anchor trước revision và label sau mọi forecast."""
    def __init__(self, root: Path, *, smoke: bool = False, verify: bool = False) -> None:
        from core.historical_evaluation_runner import Regimes
        verify_locked(root)
        self.root, self.smoke = root, smoke
        self.inputs = load(root / INPUTS)
        self.data = PilotData(root, self.inputs["units"])
        self.book = RunBook(root / DIRECTORY, identity(root), verify_only=verify)
        self.bank = FrozenBank(self.data)
        if self.bank.index.identity != load(root / RUNTIME)["index_identity"]:
            raise ValueError("Index bank/scaler khác bản khóa")
        self.context = ContextBank(self.data, self.forecasts_done)
        self.regimes = Regimes(self.data, root / "outputs/historical_reevaluation/h04_assets/legacy_regimes")
        self.clients = None
        self.graph = GraphProvider(self.data, None)

    def live(self) -> None:
        """Chỉ mở client khi thực sự cần thu thập, không mở trong cold verify."""
        if self.book.verify_only:
            raise ValueError("Cold verify cấm API")
        self.clients = PilotClients(self.data, self.book, mode="smoke" if self.smoke else "pilot")
        self.graph.clients = self.clients

    def slot(self, identifier: str, branch: str) -> str:
        """Tách slot smoke khỏi336 forecast nghiên cứu."""
        return ("smoke/" if self.smoke else "pilot/") + identifier + "/" + branch

    def forecasts_done(self, identifier: str) -> bool:
        """Chỉ giải khóa numeric query sau cả bảy forecast durable, không nhìn action."""
        return all(self.book.complete("pilot/" + identifier + "/" + b) for b in (*PRIMARY, "Fact_Anchor"))

    def shared(self, row: dict) -> dict:
        """Hash toàn state để mọi nhánh dùng đúng parent, raw/ảnh vẫn giữ trong graph journal."""
        value = self.graph.shared(self.book, row["symbol"], row["date"], 0, row["org"])
        return self.book.execute("shared/" + row["id"], {"unit": row, "shared_sha256": digest(value)}, lambda _: value,
                                 validate=lambda actual: self.same(actual, value))

    @staticmethod
    def same(actual: Any, expected: Any) -> None:
        """Cold replay so nội dung chứ không tin hash tự khai."""
        if actual != expected:
            raise ValueError("Nội dung cache không tái lập từ nguồn khóa")

    def seal_shared(self) -> dict:
        """Hoàn tất toàn bộ48 upstream trước bất kỳ Decision nghiên cứu nào."""
        seals = {row["id"]: digest(self.shared(row)) for row in self.inputs["units"]}
        payload = {"run_uuid": self.book.uuid, "count": 48, "reused": 0, "new": 48, "shared": seals}
        return self.book.execute("shared_manifest", {"inputs": digest(self.inputs)}, lambda _: payload,
                                 validate=lambda actual: self.same(actual, payload))

    def require_shared(self) -> None:
        """Thiếu dù một shared state thì chưa được thu Decision."""
        if not self.book.complete("shared_manifest") or any(not self.book.complete("shared/" + u["id"]) for u in self.inputs["units"]):
            raise ValueError("Chưa seal đủ48 shared; chạy stage shared trước collect")

    def unit(self, row: dict) -> dict:
        """Giữ query-y kín; tái lập policy từ raw response ở cả resume và cold replay."""
        from core.mt_bicl_prompt import canonical_request
        if not self.smoke:
            self.require_shared()
        shared = self.shared(row)
        episode = self.context.build(row["symbol"], row["date"])
        packet = episode["advisor"]["query_facts"]
        selected = self.context.variants(episode)["branches"]["MT_BICL"]
        policy = self.data.scope.module("mt_bicl_policy")
        regime = self.regimes.get(row["date"])
        order = call_order(0) if self.smoke else self.inputs["call_orders"][row["id"]]
        outputs = {}
        for branch in order:
            anchor = outputs.get("Fact_Anchor", {}).get("anchor")
            bypass = branch == "MT_BICL" and (not selected["eligible"] or not anchor["policy"]["fact_assertions_valid"])
            prior = {"branch": branch, "fallback": False}
            if branch == "Fact_Anchor":
                request = rendered_request(self.data, deepcopy(shared), branch, packet)
            elif branch == "MT_BICL":
                request = None if bypass else rendered_request(self.data, deepcopy(shared), branch, packet, selected, anchor)
            else:
                request, prior = self.bank.request(branch, deepcopy(shared), regime)
            if request is not None:
                require_factors(request["messages"][0]["content"], shared["alpha_factors"])
            parents = {"shared": digest(shared), "episode": digest(episode), "request": request, "prior": prior,
                       "original": digest(outputs["Original_common"]) if "Original_common" in outputs else None,
                       "anchor": digest(anchor) if anchor else None, "org": row["org"], "smoke": self.smoke}

            def invoke(attempt: str) -> dict:
                """Fallback/bypass đúng thuật toán không được giả là response LLM."""
                if bypass:
                    wire = policy.apply_revision(packet, anchor, selected)
                    return {"llm": None, "policy": wire, "final_action": wire["final_action"]}
                if prior["fallback"] and not self.smoke:
                    original_request = canonical_request(deepcopy(shared), "", {"decision": self.data.protocol["inference"]["config"]})
                    self.same(request, original_request)
                    return {"llm": None, "fallback_original_sha256": digest(outputs["Original_common"]),
                            "final_action": outputs["Original_common"]["final_action"]}
                response = self.clients.decision(row["org"], deepcopy(request), attempt, branch)
                if branch == "Fact_Anchor":
                    resolved = policy.resolve_anchor(packet, outputs["Original_common"]["llm"]["reply"], response["reply"],
                        original_source_sha256=digest(outputs["Original_common"]), anchor_source_sha256=digest(response), request_id=attempt)
                    return {"llm": response, "anchor": resolved, "final_action": resolved["policy"]["final_action"]}
                if branch == "MT_BICL":
                    wire = policy.apply_revision(packet, anchor, selected, reply=response["reply"], request_id=attempt)
                    return {"llm": response, "policy": wire, "final_action": wire["final_action"]}
                # Smoke fallback là probe wire cách ly; không thay action của fallback bằng action probe.
                action = outputs["Original_common"]["final_action"] if prior["fallback"] else policy.action(response["reply"]["decision"])
                return {"llm": response, "final_action": action, "smoke_fallback_probe": bool(prior["fallback"])}

            def validate(output: dict) -> None:
                """Không chấp nhận action/policy nếu không khớp request và raw HTTP thật."""
                response = output["llm"]
                if response is not None:
                    verify_decision(self.book, response, branch, fixture=False, request=request)
                if branch == "Fact_Anchor":
                    if response is None:
                        raise ValueError("Anchor thiếu raw")
                    expected_anchor = policy.resolve_anchor(packet, outputs["Original_common"]["llm"]["reply"], response["reply"],
                        original_source_sha256=digest(outputs["Original_common"]), anchor_source_sha256=digest(response), request_id=response["request_id"])
                    self.same(output["anchor"], expected_anchor)
                    expected = expected_anchor["policy"]["final_action"]
                elif branch == "MT_BICL":
                    wire = policy.apply_revision(packet, anchor, selected, reply=response["reply"] if response else None,
                                                 request_id=response["request_id"] if response else None)
                    self.same(output["policy"], wire)
                    expected = wire["final_action"]
                elif prior["fallback"]:
                    if response is None:
                        self.same(output["fallback_original_sha256"], digest(outputs["Original_common"]))
                    elif not self.smoke or output.get("smoke_fallback_probe") is not True:
                        raise ValueError("Fallback không được gọi lại LLM nghiên cứu")
                    expected = outputs["Original_common"]["final_action"]
                else:
                    if response is None:
                        raise ValueError("Thiếu response ngoài bypass/fallback")
                    expected = policy.action(response["reply"]["decision"])
                self.same(output["final_action"], expected)
            outputs[branch] = self.book.execute(self.slot(row["id"], branch), parents, invoke, validate=validate)
        if self.smoke:
            if any(o["llm"] is None for o in outputs.values()):
                raise ValueError("Smoke chưa exercise đủ7 Decision; giữ raw để audit, không release pilot")
        else:
            from datetime import date, timedelta
            if not self.forecasts_done(row["id"]):
                raise ValueError("Chưa đủ forecast để mở payoff")
            as_of = (date.fromisoformat(row["exit_date"]) + timedelta(days=1)).isoformat()
            label = self.data.label(row["symbol"], row["date"], as_of=as_of, forecast_done=self.forecasts_done)
            self.book.execute("label/" + row["id"], {"unit": row, "forecast_complete": True}, lambda _: label,
                              validate=lambda actual: self.same(actual, label))
        return outputs

    def smoke_run(self) -> dict:
        """Một điểm smoke cách ly; cold PASS vẫn chưa tự cấp grant nghiên cứu."""
        self.unit(self.inputs["smoke"])
        result = {"status": "SMOKE_COLD_PASS" if self.book.verify_only else "SMOKE_COLLECTED",
                  "run_uuid": self.book.uuid, "point": SMOKE["id"], "decision_slots": 7, "vision_slots": 2, "research_granted": False}
        if self.book.verify_only:
            smoke_slots = [p for p in (self.book.directory / "slots").glob("*.json") if
                load(p)["slot"].startswith(("smoke/", "graph/FPT-2023-06-23/u0/")) or load(p)["slot"] == "shared/" + SMOKE["id"]]
            save(self.book.directory / "smoke_verified.json", {**result, "identity": identity(self.root),
                 "slots": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in smoke_slots}})
        return result


    def collect(self) -> dict:
        """Không chọn lại48 point theo kết quả; cold replay giữ nguyên lịch prequential."""
        self.require_shared()
        self.seal_shared()
        if not self.book.verify_only:
            self.admit_decisions()
        for row in self.inputs["units"]:
            self.unit(row)
            print("Đã kiểm/thu: " + row["id"], flush=True)
        result = {"status": "P05_PENDING" if not self.book.verify_only else "P05_COLD_PASS",
                "run_uuid": self.book.uuid, "planned_points": 48, "forecast_slots": 336, "bridge": False}
        if self.book.verify_only:
            slots = {}
            for path in (self.book.directory / "slots").glob("*.json"):
                record = load(path)
                if record["attempts"][-1]["status"] != "complete":
                    raise ValueError("Còn slot pending/unknown, không seal P05")
                slots[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            save(self.book.directory / "pilot_collection_receipt.json", {**result, "identity": identity(self.root),
                 "slots": slots, "usage": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in (self.book.directory / "usage").glob("org*.json")}, "H08": "PENDING"})
        return result


    def admit_decisions(self) -> dict:
        """Dựng payload thực từ48 shared trước research; chặn budget/deadline trước action đầu."""
        from core.historical_evaluation_runner import FixtureClients
        from uuid import uuid4
        import math
        control = ContextBank(self.data, self.forecasts_done)
        bound = load(self.root / AUDIT)["decision_planning_reserve"]
        tasks, payloads = [], {}
        for row in self.inputs["units"]:
            shared = self.shared(row)
            episode = control.build(row["symbol"], row["date"])
            packet = episode["advisor"]["query_facts"]
            variant = control.variants(episode)["branches"]["MT_BICL"]
            requests = {b: self.bank.request(b, deepcopy(shared), self.regimes.get(row["date"]))[0]
                        for b in PRIMARY if b != "MT_BICL"}
            requests["Fact_Anchor"] = rendered_request(self.data, shared, "Fact_Anchor", packet)
            fake = FixtureClients()
            for action in ("LONG", "SHORT"):
                original = fake.decision(row["org"], requests["Original_common"], str(uuid4()), "Original_common")["reply"]
                reply = fake.decision(row["org"], requests["Fact_Anchor"], str(uuid4()), "Fact_Anchor")["reply"]
                reply["decision"] = action
                anchor = self.data.scope.module("mt_bicl_policy").resolve_anchor(packet, original, reply,
                    original_source_sha256=digest(original), anchor_source_sha256=digest(reply), request_id=str(uuid4()))
                if variant["eligible"]:
                    requests["MT_BICL_" + action] = rendered_request(self.data, shared, "MT_BICL", packet, variant, anchor)
            values = {b: reserve(r) for b, r in requests.items()}
            if max(values.values()) > bound:
                raise PilotStop("BLOCKED_BUDGET: payload thực vượt reserve đã khóa; chưa gọi Decision")
            payloads[row["id"]] = values
            tasks.extend({"org": row["org"], "model": "openai/gpt-oss-20b", "tokens": bound}
                         for b in (*PRIMARY, "Fact_Anchor") if not self.book.complete(self.slot(row["id"], b)))
        retry = []
        for org in range(1, 6):
            group = [t for t in tasks if t["org"] == org]
            retry.extend(deepcopy(group[:math.ceil(.2 * len(group))]))
        usage = {i: json.loads((self.book.directory / "usage" / f"org{i}.json").read_bytes())["requests"] for i in range(1, 6)}
        audit = load(self.root / AUDIT)
        budget = budget_schedule(usage, [*tasks, *retry], start=time.time(), latency=audit["budget"]["latency_seconds_per_http"])
        deadline = load(self.book.directory / "campaign.json")["deadline_epoch"]
        finish = datetime.fromisoformat(budget["finish_utc"]).timestamp() if "finish_utc" in budget else float("inf")
        result = {"status": "PASS" if budget["status"] == "PASS" and finish <= deadline else "BLOCKED_BUDGET",
                  "budget": budget, "actual_shared_payload_reserves": payloads, "run_uuid": self.book.uuid}
        save(self.book.directory / "decision_admission.json", result)
        if result["status"] != "PASS":
            raise PilotStop("BLOCKED_BUDGET: ngân sách còn lại không vừa deadline48h, giữ nguyên48 điểm")
        return result


def promote(root: Path) -> dict:
    """Tạo candidate grant sau cold smoke; vẫn phải neo Git trước khi API nghiên cứu mở."""
    runner = PilotRunner(root, smoke=True, verify=True)
    runner.smoke_run()
    grant = anchored(root, GRANT)
    if grant["status"] != "SMOKE_READY":
        raise ValueError("Chỉ nâng grant SMOKE_READY sau nghiệm thu")
    grant.update(status="PILOT_RELEASED", smoke_receipt=binding(root, DIRECTORY / "smoke_verified.json"))
    save(root / GRANT, grant)
    return {"status": "CANDIDATE_NOT_GIT_ANCHORED", "run_uuid": runner.book.uuid}
