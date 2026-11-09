"""Adapter mỏng gọi prompt/retrieval/policy hiện hữu; nạp bank/student theo nhu cầu."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import io
from typing import Any, Callable

from core.unified_contracts import SharedSnapshot, digest, json_bytes, forecast_only


def snapshot_from_graph(point: dict[str, Any], realization: int, shared: dict[str, Any], prefix: Any,
                        source_sha256: str, news_dates: list[str]) -> SharedSnapshot:
    """Adapter upstream hiện hữu: giữ raw reports/ảnh/factors và prefix, không nhận outcome."""
    import pandas as pd
    from core.unified_contracts import REPORTS
    from utils.json_util import to_json_compatible
    forecast_only(shared)
    dates = pd.DatetimeIndex(prefix.Datetime)
    if (len(prefix) != 600 or dates.tz is not None or dates.hasnans or dates.has_duplicates
            or not dates.is_monotonic_increasing or not dates.equals(dates.normalize())
            or str(dates[-1].date()) != point["cutoff"]):
        raise ValueError("Upstream phải có đúng prefix PIT 600 bars")
    columns = ("Open", "High", "Low", "Close", "Volume")
    import numpy as np
    matrix = prefix[list(columns)].to_numpy(dtype=float)
    if not np.isfinite(matrix).all() or (matrix[:, :4] <= 0).any() or (matrix[:, 4] < 0).any():
        raise ValueError("Prefix có giá/volume không hợp lệ")
    payload = {key: shared[key] for key in (*REPORTS, "stock_name", "as_of_date", "time_frame", "language", "is_backtest")}
    for key in ("pattern_image", "trend_image", "alpha_factors", "sentiment_data"):
        if key in shared:
            payload[key] = shared[key]
    payload["price_prefix"] = {"Datetime": dates.strftime("%Y-%m-%d").tolist(),
                               **{key: prefix[key].astype(float).tolist() for key in columns}}
    payload = to_json_compatible(payload)
    return SharedSnapshot.create(point, realization, payload, {"source_sha256": source_sha256,
        "upstream_sha256": digest(payload), "price_end": point["cutoff"], "news_dates": news_dates})


def envelope(shared: dict[str, Any], protocol: dict[str, Any], repeat: int) -> dict[str, Any]:
    """Envelope giống common SDK contract, không dựng common prompt cho native."""
    from agents.decision_agent import TradeDecisionOutput
    config = protocol["decision"]
    models = config["signal_config"]["models"]
    return {"point_id": shared["stock_name"] + "-" + shared["as_of_date"], "repeat_index": repeat,
            "model": models["agent_llm_model"], "temperature": models["agent_llm_temperature"],
            "max_tokens": models["agent_llm_max_tokens"], "client_max_retries": config["client_max_retries"],
            "client_options": deepcopy(config["client_options"]["agent"]), "service_tier": config["service_tier"],
            "structured": {"schema": TradeDecisionOutput.model_json_schema(), "method": "json_schema", "include_raw": True}}


def native_request(shared: dict[str, Any], protocol: dict[str, Any], repeat: int) -> dict[str, Any]:
    """Dừng tại invoke của factory native, giữ đúng distill/cap và guard U03."""
    from agents.decision_agent import create_final_trade_decider
    from core.decision_profiles import NATIVE_PROFILE
    class Captured(BaseException):
        """Thoát trước model, không kích hoạt retry hoặc parse response giả."""
    prompts: list[str] = []
    class Capture:
        """Client chỉ quan sát ranh giới invoke, không có HTTP."""
        def invoke(self, prompt: str) -> None:
            prompts.append(prompt)
            raise Captured()
    with redirect_stdout(io.StringIO()):
        try:
            create_final_trade_decider(Capture(), decision_profile=NATIVE_PROFILE)(deepcopy(shared))
        except Captured:
            pass
    if len(prompts) != 1:
        raise ValueError("Không lấy được đúng một prompt native")
    # Envelope serving chung; nội dung native chỉ lấy từ factory gốc.
    request = envelope(shared, protocol, repeat)
    request["messages"] = [{"role": "user", "content": prompts[0]}]
    return request


class MethodAdapters:
    """Factory tài nguyên được caller khóa nguồn; adapter không giữ RunBook hoặc outcomes."""
    def __init__(self, decision: dict[str, Any], *, bank_factory: Callable[[], Any] | None = None,
                 regime: Callable[[str], str] | None = None,
                 facts: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
                 context_factory: Callable[[], Any] | None = None) -> None:
        self.protocol = {"decision": deepcopy(decision)}
        self.bank_factory, self.regime, self.facts = bank_factory, regime, facts
        self.context_factory = context_factory
        self._bank: Any = None
        self._context: Any = None
        self._episodes: dict[str, Any] = {}

    def prepare(self, variant: str, snapshot: SharedSnapshot, dependencies: dict[str, Any], repeat: int) -> dict[str, Any]:
        """Tạo projection/request, không mutate shared và không gọi LLM."""
        from core.mt_bicl_prompt import canonical_request, COMMON_INSTRUCTION
        shared = snapshot.document()["payload"]
        request, trace, aux = None, {"fallback": False}, {}
        if variant == "original_fix":
            request = native_request(shared, self.protocol, repeat)
        elif variant == "original_common":
            request = canonical_request(shared, "", self.protocol, repeat)
        elif variant in ("bayesian_v1", "C2", "A_tp_pool", "B_semantic"):
            if self.bank_factory is None or self.regime is None:
                raise ValueError("Thiếu factory bank/regime đã xác minh")
            if self._bank is None:
                self._bank = self.bank_factory()
            request, trace = self._bank.request(variant, deepcopy(shared), self.regime(shared["as_of_date"]))
            request = deepcopy(request)
            request["repeat_index"] = repeat
            if type(trace.get("fallback")) is not bool:
                raise ValueError("Trace prior thiếu fallback bool")
            if trace["fallback"]:
                original = canonical_request(shared, "", self.protocol, repeat)
                if request != original:
                    raise ValueError("Fallback phải khớp đúng request Original_common")
                request = None
        elif variant in ("Fact_Anchor", "MT_BICL"):
            from core.mt_bicl_contracts import validate_fact_packet, validate_context, validate_branch
            from core.mt_bicl_decision import canonical_request as anchored_request
            if self.facts is None:
                raise ValueError("Thiếu nguồn facts PIT")
            packet = deepcopy(self.facts(deepcopy(snapshot.document()["point"])))
            validate_fact_packet(packet)
            if packet["point_id"] != shared["stock_name"] + "-" + shared["as_of_date"]:
                raise ValueError("Facts khác query")
            aux["packet"] = packet
            anchor, branch = None, None
            if variant == "MT_BICL":
                if self.context_factory is None:
                    raise ValueError("Thiếu context/student đã khóa")
                key = packet["point_id"]
                if key not in self._episodes:
                    if self._context is None:
                        self._context = self.context_factory()
                    episode = self._context.build(shared["stock_name"], shared["as_of_date"])
                    validate_context(episode)
                    if episode["advisor"]["query_facts"] != packet:
                        raise ValueError("Context và fact packet không cùng nguồn")
                    self._episodes[key] = deepcopy(self._context.variants(episode)["branches"]["MT_BICL"])
                branch = deepcopy(self._episodes[key])
                validate_branch(branch)
                anchor = dependencies["Fact_Anchor"]["policy"]["anchor"]
                aux.update(branch=branch, anchor=anchor)
            if branch is None or (branch["eligible"] and anchor["policy"]["fact_assertions_valid"]):
                request = anchored_request(shared, {"decision": {"config": self.protocol["decision"]}},
                    branch_id=variant, packet=packet, projection=branch["projection"] if branch else None,
                    anchor=anchor, repeat=repeat)
                request["messages"][0]["content"] = COMMON_INSTRUCTION + "\n" + request["messages"][0]["content"]
        else:
            raise ValueError("Không có adapter cho variant")
        if request is not None:
            content = request["messages"][0]["content"]
            if type(content) is not str or len(content) >= 6500:
                raise ValueError("Prompt cuối vượt ngân sách trước transport")
            template = envelope(shared, self.protocol, repeat)
            if any(request.get(k) != v for k, v in template.items() if k not in ("messages", "structured")):
                raise ValueError("Adapter thay model/options chung ngoài spec")
        result = {"request": request, "trace": trace, "aux": aux}
        json_bytes(result)
        return result


def validate_prepared(variant: str, snapshot: SharedSnapshot, prepared: dict[str, Any],
                      decision: dict[str, Any], repeat: int) -> None:
    """Dựng lại prompt/schema từ trace đã khóa; không tải bank/student trong cold consumer."""
    from core.mt_bicl_prompt import canonical_request, COMMON_INSTRUCTION
    from core.mt_bicl_decision import canonical_request as anchored_request
    if set(prepared) != {"request", "trace", "aux"}:
        raise ValueError("Preparation sai fields")
    shared, protocol = snapshot.document()["payload"], {"decision": decision}
    if variant == "original_fix":
        expected = native_request(shared, protocol, repeat)
    elif variant == "original_common":
        expected = canonical_request(shared, "", protocol, repeat)
    elif variant in ("Fact_Anchor", "MT_BICL"):
        from core.mt_bicl_contracts import validate_fact_packet, validate_branch
        aux = prepared["aux"]
        validate_fact_packet(aux["packet"])
        branch, anchor = aux.get("branch"), aux.get("anchor")
        if variant == "MT_BICL":
            validate_branch(branch)
        if branch is not None and (not branch["eligible"] or not anchor["policy"]["fact_assertions_valid"]):
            expected = None
        else:
            expected = anchored_request(shared, {"decision": {"config": decision}}, branch_id=variant,
                packet=aux["packet"], projection=branch["projection"] if branch else None, anchor=anchor, repeat=repeat)
            expected["messages"][0]["content"] = COMMON_INSTRUCTION + "\n" + expected["messages"][0]["content"]
    else:
        trace = prepared["trace"]
        if variant == "bayesian_v1":
            from core.bayesian_retriever import format_compact_prior_prefix
            retrieval = trace["retrieval"]
            if any(task["exit_date"] >= shared["as_of_date"] for task in retrieval["tasks"]):
                raise ValueError("Historical prior chưa mature trước query")
            prefix = format_compact_prior_prefix(retrieval["tasks"], retrieval["stats"])
        else:
            prefix = trace["request"]["prefix"]
        if type(trace["fallback"]) is not bool or (trace["fallback"] and prefix):
            raise ValueError("Fallback không đúng prefix OFF")
        expected = None if trace["fallback"] else canonical_request(shared, prefix, protocol, repeat)
    if prepared["request"] != expected:
        raise ValueError("Prepared request không khớp prompt/options/schema đã khóa")
    if expected is not None and len(expected["messages"][0]["content"]) >= 6500:
        raise ValueError("Prepared request vượt ngân sách")


def resolve(variant: str, prepared: dict[str, Any], raw: dict[str, Any] | None,
            dependencies: dict[str, Any]) -> dict[str, Any]:
    """Phân biệt raw proposal, fallback và final policy; lỗi kỹ thuật luôn raise."""
    from agents.decision_agent import TradeDecisionOutput
    from core.mt_bicl_policy import resolve_anchor, apply_revision, action
    from core.mt_bicl_contracts import validate_wire
    if (prepared["request"] is None) != (raw is None):
        raise ValueError("Response không khớp request/bypass")
    reply = raw["reply"] if raw else None
    anchor = None
    if variant == "Fact_Anchor":
        validate_wire(reply, "reply")
        anchor = resolve_anchor(prepared["aux"]["packet"], dependencies["original_common"]["forecast"]["raw"]["reply"], reply,
            original_source_sha256=digest(dependencies["original_common"]), anchor_source_sha256=digest(raw),
            request_id=raw["source_request_id"])
        wire = anchor["policy"]
    elif variant == "MT_BICL":
        if prepared["aux"]["anchor"] != dependencies["Fact_Anchor"]["policy"]["anchor"]:
            raise ValueError("MT không dùng đúng Fact_Anchor durable của cùng repeat")
        wire = apply_revision(prepared["aux"]["packet"], prepared["aux"]["anchor"], prepared["aux"]["branch"],
                              reply=reply, request_id=raw["source_request_id"] if raw else None)
    elif prepared["trace"]["fallback"]:
        if raw is not None or "original_common" not in dependencies:
            raise ValueError("Fallback thiếu Original_common durable")
        wire = {"final_action": dependencies["original_common"]["policy"]["final_action"],
                "reason": "FALLBACK_ORIGINAL", "bypass": True}
    else:
        TradeDecisionOutput.model_validate(reply, strict=True)
        wire = {"final_action": action(reply["decision"]), "reason": "RAW_DECISION", "bypass": False}
    return {"version": "unified_policy_record_v1", "raw_proposal": reply["decision"] if reply else None,
            "final_action": wire["final_action"], "reason": wire["reason"], "bypass": wire["bypass"],
            "wire": wire, "anchor": anchor}
