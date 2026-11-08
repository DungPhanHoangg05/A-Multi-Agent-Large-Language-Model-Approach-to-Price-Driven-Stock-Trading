"""Runner paired/prequential chín mã, checkpoint mọi slot và verify không gọi API."""

from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta
import hashlib
from pathlib import Path
from typing import Any

import pandas as pd

from core.historical_evaluation_clients import Clients, RUNTIME
from core.historical_evaluation_context import ContextBank
from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_graph import GraphProvider, require_factors
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_prior import FeaturePopulation, signals
from core.historical_evaluation_protocol import CORE4, INPUTS, PROTOCOL, digest, read
from core.mt_bicl_prompt import canonical_request
from core.prior_run_lock import PriorRunLock, safe_path
from core.regime_detector import MarketRegimeDetector, training_data_hash


def forecast_slot(unit: str, realization: int, repeat: int, branch: str) -> str:
    """Slot khoa học không đổi theo UUID HTTP hoặc số lần resume."""
    return f"forecast/{unit}/u{realization}/r{repeat}/{branch}"


def branches(data: HistoricalData, unit: dict[str, Any], realization: int, repeat: int) -> list[str]:
    """Original/anchor đứng trước revision; tail được counterbalance đúng H03."""
    names = [name for name in data.protocol["registry_order"] if name != "Original_common"]
    if realization == 0 and unit["anchor"]:
        names.extend(data.protocol["ablations"])
        names.extend(data.protocol["retrieval_controls"])
        names.append("Original_duplicate")
    j = next(i for i, row in enumerate(data.inputs["grid"]) if row["id"] == unit["id"])
    shift = (j + repeat + realization) % len(names)
    return ["Original_common", "Fact_Anchor", *names[shift:], *names[:shift]]


def runtime_identity(data: HistoricalData, fixture: bool) -> dict[str, Any]:
    """Model/data/protocol/source tách khỏi grant H06 để giữ UUID khi nâng smoke→research."""
    from core.historical_evaluation_audit import verify_runtime
    verify_runtime(data.root)
    manifest = read(data.root, RUNTIME, envelope=True)
    for record in manifest["sources"].values():
        from core.historical_evaluation_protocol import binding
        if binding(data.root, record["path"]) != record:
            raise ValueError("Runtime H04 đã đổi: " + record["path"])
    return {"version": "historical_run_v1", "protocol_sha256": hashlib.sha256((data.root / PROTOCOL).read_bytes()).hexdigest(),
            "inputs_sha256": hashlib.sha256((data.root / INPUTS).read_bytes()).hexdigest(),
            "runtime_sha256": hashlib.sha256((data.root / RUNTIME).read_bytes()).hexdigest(),
            "fixture": fixture, "quality": "VENDOR_SERIES_LIMITED"}


class Regimes:
    """Query dùng model2022 frozen; historical dùng prefix artifact đã chuẩn bị riêng."""

    def __init__(self, data: HistoricalData, directory: Path, *, fixture: bool = False) -> None:
        self.data, self.directory, self.fixture = data, directory, fixture
        self.historical_detector = data.scope.module("regime_detector").MarketRegimeDetector
        self.frozen = MarketRegimeDetector.load(data.root / "data_manager/regime_model.json")
        prefix = data.history.loc[data.history["Datetime"] <= self.frozen.metadata["train_end_date"]]
        if training_data_hash(prefix) != self.frozen.metadata["training_data_sha256"]:
            raise ValueError("Query HMM frozen không khớp prefix VNINDEX")
        self.queries: dict[str, str] = {}

    def get(self, cutoff: str, *, historical: bool = False) -> str:
        """Không refit query hoặc dùng model fit sau ngày lịch sử."""
        if self.fixture:
            return "BULL"
        prefix = self.data.history.loc[self.data.history["Datetime"] <= pd.Timestamp(cutoff)].copy()
        if historical:
            path = self.directory / (cutoff + ".json")
            if not path.exists():
                raise ValueError("Thiếu historical regime prefix; chạy CLI prepare-regimes trước API")
            detector = self.historical_detector.load(path, expected_training_hash=training_data_hash(prefix))
            if detector.metadata["train_end_date"] != cutoff:
                raise ValueError("Historical HMM không kết thúc đúng prefix")
        else:
            if cutoff in self.queries:
                return self.queries[cutoff]
            detector = self.frozen
            if detector.metadata["train_end_date"] >= cutoff:
                raise ValueError("Query HMM fit sau cutoff")
        state = detector.classify_regime(prefix, cutoff)
        if state["feature_end_date"] > cutoff:
            raise ValueError("Regime feature vượt cutoff")
        if not historical:
            self.queries[cutoff] = state["regime_name"]
        return state["regime_name"]

    def preflight(self) -> None:
        """Thiếu historical model phải dừng trước cuộc gọi vision đầu tiên."""
        if self.fixture:
            return
        dates = sorted({row["date"] for row in self.data.inputs["history"]})
        missing = [day for day in dates if not (self.directory / (day + ".json")).is_file()]
        if missing:
            raise ValueError(f"Thiếu{len(missing)} historical HMM prefix; chạy prepare-regimes trước API")
        for cutoff in dates:
            prefix = self.data.history.loc[self.data.history["Datetime"] <= cutoff]
            model = self.historical_detector.load(self.directory / (cutoff + ".json"),
                                              expected_training_hash=training_data_hash(prefix))
            if model.metadata["train_end_date"] != cutoff:
                raise ValueError("HMM prefix không đúng cutoff đã khóa")


class HistoricalRunner:
    """Cùng upstream cho mọi branch/repeat; outcome chỉ mở sau toàn forecast của unit."""

    def __init__(self, data: HistoricalData, *, fixture: bool = False, verify_only: bool = False,
                 clients: Any = None, graph: Any = None) -> None:
        """Không tạo live client trong verify hoặc fixture."""
        if not fixture and (graph is not None or clients not in (None, False)):
            raise ValueError("Chỉ fixture mới được inject provider; research phải dùng transport có release guard")
        self.data, self.fixture = data, fixture
        self.phase: str | None = None
        namespace = "outputs/historical_reevaluation/h04_fixture" if fixture else data.protocol["namespace"]
        self.book = RunBook(data.root / namespace, runtime_identity(data, fixture), verify_only=verify_only)
        if clients is None:
            clients = FixtureClients() if fixture else None if verify_only else Clients(data, self.book)
        self.clients = clients
        self.graph = graph or GraphProvider(data, clients, fixture=fixture)
        self.context = ContextBank(data, self.numeric_forecasts_done)
        self.population = FeaturePopulation(data, forecast_done=self.forecasts_done)
        self.regimes = Regimes(data, data.root / "outputs/historical_reevaluation/h04_assets/legacy_regimes", fixture=fixture)
        if not verify_only:
            self.regimes.preflight()
        self.legacy_cache: dict[tuple[str, str], list[dict[str, Any]]] = {}

    def select_phase(self, cohort: str) -> None:
        """Mỗi instance giữ một phase để bank numeric không đổi theo thứ tự cold replay."""
        if cohort not in ("CORE4", "OOD5") or self.phase not in (None, cohort):
            raise ValueError("CORE4/OOD5 phải dùng instance riêng, cùng run identity")
        if self.phase is None and cohort == "OOD5" and not self.fixture:
            if any(not self.forecasts_done(unit["id"]) for unit in self.data.inputs["grid"] if unit["symbol"] in CORE4):
                raise ValueError("Phải hoàn tất forecast CORE4 trước khi thu OOD5")
        self.phase = cohort

    def numeric_forecasts_done(self, identifier: str) -> bool:
        """CORE4 luôn giữ kín grid outcome OOD, kể cả khi OOD đã durable ở phase sau."""
        if self.phase is None:
            raise ValueError("Chưa chọn phase cho context numeric")
        if self.phase == "CORE4" and self.data.grid[identifier]["symbol"] not in CORE4:
            return False
        return self.forecasts_done(identifier)

    def realizations(self, unit: dict[str, Any]) -> list[int]:
        """Panel chỉ thêm hai realization ở đúng51 ID đã khóa."""
        return [0, 1, 2] if unit["id"] in self.data.inputs["panel_ids"] else [0]

    def forecasts_done(self, identifier: str) -> bool:
        """Không tin một cờ bool trong file unit; kiểm toàn bộ slot được protocol yêu cầu."""
        unit = self.data.grid[identifier]
        return all(self.book.complete(forecast_slot(identifier, realization, repeat, branch))
                   for realization in self.realizations(unit) for repeat in range(3)
                   for branch in branches(self.data, unit, realization, repeat))

    def organization(self, symbol: str, cutoff: str) -> int:
        """History trùng query dùng cùng org, không tạo parent/cache khác."""
        unit = self.data.by_day.get((symbol, cutoff))
        rows = self.data.inputs["grid"] if unit else self.data.inputs["history"]
        target = unit["id"] if unit else symbol + ":" + cutoff
        return 1 + next(i for i, row in enumerate(rows) if row["id"] == target) % 5

    def history_records(self, symbol: str, cutoff: str) -> list[dict[str, Any]]:
        """Dựng bank từ raw shared durable của đúng mã; không đọc response/label tương lai."""
        key = (symbol, cutoff)
        if key in self.legacy_cache:
            return deepcopy(self.legacy_cache[key])
        rows = []
        for row in self.data.inputs["history"]:
            if row["symbol"] != symbol or row["exit_date"] >= cutoff:
                continue
            if row["shared_query_unit"] is not None and not self.forecasts_done(row["shared_query_unit"]):
                raise ValueError("History query chưa có đủ forecast durable")
            shared = self.graph.shared(self.book, symbol, row["date"], 0, self.organization(symbol, row["date"]))
            label = self.data.label(symbol, row["date"], as_of=cutoff, forecast_done=self.forecasts_done)
            current = signals(shared)
            bullish = any(self.data.scope.module("bayesian_memory").is_bullish(current[name]) for name in ("trend", "pattern"))
            record = {"episode_id": row["id"], "symbol": symbol, "as_of_date": row["date"],
                      "entry_date": label["entry_date"], "exit_date": label["exit_date"],
                      "regime": self.regimes.get(row["date"], historical=True), "agent_signals": current,
                      "outcome": {"net_return_pct": label["r_net"] * 100., "actual_direction": "UP" if label["y"] else "DOWN",
                                  "result": "WIN_IF_LONG" if label["y"] else "LOSS_IF_LONG",
                                  "was_bull_trap": bool(bullish and not label["y"])}}
            rows.append(record)
        self.legacy_cache[key] = deepcopy(rows)
        return rows

    def unit(self, unit: dict[str, Any]) -> None:
        """Durable mọi branch trước label, không gán lỗi API thành CASH hoặc bypass."""
        identifier, symbol, cutoff = unit["id"], unit["symbol"], unit["date"]
        self.select_phase("CORE4" if symbol in CORE4 else "OOD5")
        episode = self.context.build(symbol, cutoff)
        variants = self.context.variants(episode)
        packet = episode["advisor"]["query_facts"]
        policy = self.data.scope.module("mt_bicl_policy")
        decider = self.data.scope.module("mt_bicl_decision")
        regime = self.regimes.get(cutoff)
        records = self.history_records(symbol, cutoff)
        org = self.organization(symbol, cutoff)
        for realization in self.realizations(unit):
            shared = self.graph.shared(self.book, symbol, cutoff, realization, org)
            for repeat in range(3):
                outputs: dict[str, Any] = {}
                for branch in branches(self.data, unit, realization, repeat):
                    prior = {"branch": branch}
                    anchor = outputs.get("Fact_Anchor", {}).get("anchor")
                    selected = variants["branches"].get(branch)
                    bypass = selected is not None and (not selected["eligible"] or not anchor["policy"]["fact_assertions_valid"])
                    if branch == "Fact_Anchor":
                        request = decider.canonical_request(deepcopy(shared), self.data.protocol["effective_mt_bicl"],
                            branch_id=branch, packet=packet, repeat=repeat)
                    elif selected is not None:
                        request = None if bypass else decider.canonical_request(deepcopy(shared), self.data.protocol["effective_mt_bicl"],
                            branch_id=branch, packet=packet, projection=selected["projection"], anchor=anchor, repeat=repeat)
                    else:
                        request, prior = self.population.request(branch, deepcopy(shared), regime, records, repeat)
                    if request is not None:
                        require_factors(request["messages"][0]["content"], shared["alpha_factors"])
                    parents = {"shared": digest(shared), "episode": digest(episode), "request": request,
                               "prior": prior, "original": digest(outputs["Original_common"]) if "Original_common" in outputs else None,
                               "anchor": digest(anchor) if anchor else None, "org": org}
                    def invoke(attempt: str, branch: str = branch, request: Any = request,
                               selected: Any = selected, bypass: bool = bypass, prior: Any = prior) -> dict[str, Any]:
                        """Deep-copy từng nhánh, giữ proof raw→facts→veto riêng."""
                        if bypass:
                            wire = policy.apply_revision(packet, anchor, selected)
                            return {"llm": None, "policy": wire, "final_action": wire["final_action"]}
                        if prior.get("fallback"):
                            if request != canonical_request(deepcopy(shared), "", {"decision": self.data.protocol["inference"]["config"]}, repeat):
                                raise ValueError("Fallback không đúng Original request")
                            return {"llm": None, "fallback_original_sha256": digest(outputs["Original_common"]),
                                    "final_action": outputs["Original_common"]["final_action"]}
                        response = self.clients.decision(org, deepcopy(request), attempt, branch)
                        if branch == "Fact_Anchor":
                            resolved = policy.resolve_anchor(packet, outputs["Original_common"]["llm"]["reply"], response["reply"],
                                original_source_sha256=digest(outputs["Original_common"]), anchor_source_sha256=digest(response), request_id=attempt)
                            return {"llm": response, "anchor": resolved, "final_action": resolved["policy"]["final_action"]}
                        if selected is not None:
                            wire = policy.apply_revision(packet, anchor, selected, reply=response["reply"], request_id=attempt)
                            return {"llm": response, "policy": wire, "final_action": wire["final_action"]}
                        return {"llm": response, "final_action": policy.action(response["reply"]["decision"])}
                    def validate(output: dict[str, Any], branch: str = branch, selected: Any = selected) -> None:
                        """Cold rebuild policy, không tin action hoặc bypass do file tự khai."""
                        from core.historical_evaluation_audit import verify_decision
                        if output["llm"] is not None:
                            verify_decision(self.book, output["llm"], branch, fixture=self.fixture, request=request)
                        if branch == "Fact_Anchor":
                            expected_anchor = policy.resolve_anchor(packet, outputs["Original_common"]["llm"]["reply"],
                                output["llm"]["reply"], original_source_sha256=digest(outputs["Original_common"]),
                                anchor_source_sha256=digest(output["llm"]), request_id=output["llm"]["request_id"])
                            if expected_anchor != output["anchor"]:
                                raise ValueError("Anchor không bind đúng raw Original/Fact_Anchor")
                            expected = output["anchor"]["policy"]["final_action"]
                        elif selected is not None:
                            response = output["llm"]
                            wire = policy.apply_revision(packet, anchor, selected,
                                reply=response["reply"] if response else None, request_id=response["request_id"] if response else None)
                            if wire != output["policy"]:
                                raise ValueError("Policy cache không tái lập")
                            expected = wire["final_action"]
                        elif output["llm"] is None:
                            if not prior.get("fallback") or output["fallback_original_sha256"] != digest(outputs["Original_common"]):
                                raise ValueError("Fallback giả hoặc sai parent")
                            expected = outputs["Original_common"]["final_action"]
                        else:
                            from jsonschema import Draft202012Validator
                            if list(Draft202012Validator(request["structured"]["schema"]).iter_errors(output["llm"]["reply"])):
                                raise ValueError("Reply cache sai schema")
                            expected = policy.action(output["llm"]["reply"]["decision"])
                        if output["final_action"] != expected:
                            raise ValueError("Final action không khớp policy/raw")
                    outputs[branch] = self.book.execute(forecast_slot(identifier, realization, repeat, branch), parents, invoke, validate=validate)
        if not self.forecasts_done(identifier):
            raise ValueError("Unit chưa đủ toàn bộ forecast durable")
        as_of = (date.fromisoformat(unit["exit_date"]) + timedelta(days=1)).isoformat()
        label = self.data.label(symbol, cutoff, as_of=as_of, forecast_done=self.forecasts_done)
        self.book.execute("label/" + identifier, {"unit": unit, "forecast_complete": True}, lambda _: label,
                          validate=lambda actual: self._same(actual, label))

    @staticmethod
    def _same(actual: Any, expected: Any) -> None:
        """Không dùng hash tự khai để bỏ qua so nhãn engine."""
        if actual != expected:
            raise ValueError("Label cache khác source/engine")

    def run(self, *, cohort: str = "CORE4", max_units: int | None = None) -> dict[str, Any]:
        """Mỗi phase theo union lịch tăng dần; CORE4 trước, rồi OOD5 bằng instance mới."""
        if cohort not in ("CORE4", "OOD5") or max_units is not None and max_units < 1:
            raise ValueError("Cohort/max_units không hợp lệ")
        self.select_phase(cohort)
        symbols = set(CORE4) if cohort == "CORE4" else set(self.data.frames) - set(CORE4)
        grid = [r for r in self.data.inputs["grid"] if r["symbol"] in symbols]
        work = {(r["symbol"], r["date"]) for r in self.data.inputs["history"] if r["symbol"] in symbols}
        work.update((r["symbol"], r["date"]) for r in grid)
        completed = new_units = 0
        previous_exits: dict[tuple[str, str], str] = {}
        for symbol, cutoff in sorted(work, key=lambda pair: (pair[1], pair[0])):
            unit = self.data.by_day.get((symbol, cutoff))
            if unit is None:
                self.graph.shared(self.book, symbol, cutoff, 0, self.organization(symbol, cutoff))
                continue
            account = (unit["symbol"], unit["fold"])
            if account in previous_exits and previous_exits[account] >= unit["entry_date"]:
                raise ValueError("Holding span chồng lấn: previous_exit phải < next_entry")
            previous_exits[account] = unit["exit_date"]
            already = self.forecasts_done(unit["id"])
            self.unit(unit)
            completed += 1
            new_units += int(not already)
            if max_units is not None and (completed if self.book.verify_only else new_units) >= max_units:
                break
        return {"status": "FIXTURE_ONLY" if self.fixture else "PHASE_COMPLETE" if completed == len(grid) else "PARTIAL",
                "cohort": cohort, "completed_units": completed, "planned_units": len(grid),
                "new_units": new_units, "run_uuid": self.book.uuid, "llm_api_used": not self.fixture,
                "economic_acceptance": "PENDING_EXECUTION_DATA"}


class FixtureClients:
    """Responses mô phỏng có nhãn rõ, chỉ được runner đặt ở namespace fixture riêng."""

    def models(self, org: int) -> tuple[Any, Any]:
        """Không nạp key hoặc tạo HTTP client."""
        return None, None

    def stage(self, role: str, attempt: str, point: str, node: Any, state: dict[str, Any]) -> dict[str, Any]:
        """Chỉ Indicator/Alpha chạy số thật; vision mô phỏng kiểm orchestration."""
        if role in ("indicator", "full"):
            return node(deepcopy(state))
        return {role + "_report": "FIXTURE_ONLY — không phải LLM.\n" + (
            "**Thiên lệch dự báo:** BULLISH" if role == "pattern" else "**Hướng xu hướng:** BULLISH")}

    def decision(self, org: int, request: dict[str, Any], attempt: str, branch: str) -> dict[str, Any]:
        """Điền fixture schema từ template hiện hành; không ghi thành inference thật."""
        from agents.decision_agent import TradeDecisionOutput
        reply = {"decision": "SHORT", "forecast_horizon": "T+2.5", "confidence": "Thấp", "risk_reward_ratio": 1.,
                 "evidence_for": "FIXTURE_ONLY", "evidence_against": "Không dùng để phân tích hiệu quả", "justification": "Không gọi LLM."}
        if branch in ("Fact_Anchor", "MT_BICL", "Plain_revision", "No_utility", "No_target", "Stats_only"):
            # Chép assertions từ phần JSON cuối prompt giống điều kiện schema của provider.
            import json
            marker = "Chỉ trả về một JSON hợp lệ, không Markdown hay chữ ngoài JSON:\n"
            template = json.loads(request["messages"][0]["content"].rsplit(marker, 1)[1])
            reply.update({k: template[k] for k in ("version", "fact_ids", "fact_assertions", "context_reason")})
        else:
            TradeDecisionOutput.model_validate(reply, strict=True)
        return {"reply": reply, "raw_message": [], "request_id": attempt, "fixture": True}
