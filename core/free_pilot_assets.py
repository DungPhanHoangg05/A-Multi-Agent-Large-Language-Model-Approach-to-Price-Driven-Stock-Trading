"""Dữ liệu/protocol riêng cho pilot48; không gọi API hoặc mở payoff query."""

from __future__ import annotations

from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
from typing import Any

import pandas as pd

from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_protocol import CORE4, DONOR, PRIMARY, binding, digest
from core.historical_evaluation_journal import load, save
from core.historical_evaluation_scope import AlgorithmScope

DOC = Path("docs/plan/week11")
DIRECTORY = Path("outputs/historical_reevaluation/free_pilot_r1")
PROTOCOL = DOC / "free_pilot_protocol.json"
INPUTS = DOC / "free_pilot_inputs.json"
RUNTIME = DOC / "free_pilot_runtime.json"
AUDIT = DOC / "free_pilot_audit.json"
GRANT = DOC / "free_pilot_release.json"
BRANCHES = (*PRIMARY, "Fact_Anchor")
CODE = ("core/free_pilot_assets.py", "core/free_pilot_runtime.py", "scripts/run_free_paired_pilot.py")
RAW_SOURCE = {"source_library": "vnstock", "primary_source": "VCI", "price_basis": "UNADJUSTED_EXECUTION", "price_unit": "thousand_VND"}


def selected_units(grid: list[dict]) -> list[dict]:
    """Chọn lịch trước outcome: giao20 ngày/bốn mã, index0/3/7/11/15/19."""
    result = []
    for fold in ("b2023_h2", "b2024_h2"):
        sets = [{r["date"] for r in grid if r["fold"] == fold and r["symbol"] == symbol} for symbol in CORE4]
        days = sorted(set.intersection(*sets))
        if len(days) != 20:
            raise ValueError("Block pilot phải có đúng20 cutoff chung")
        chosen = {days[j * 19 // 5] for j in range(6)}
        result.extend(deepcopy(r) for r in grid if r["fold"] == fold and r["symbol"] in CORE4 and r["date"] in chosen)
    result.sort(key=lambda r: (r["date"], r["symbol"]))
    if len(result) != 48 or len({r["id"] for r in result}) != 48:
        raise ValueError("Pilot phải có đúng48 ID")
    previous = {}
    for i, row in enumerate(result):
        key = row["symbol"], row["date"][:4]
        if key in previous and previous[key] >= row["entry_date"]:
            raise ValueError("Holding spans pilot chồng lấn")
        previous[key] = row["exit_date"]
        row["org"] = i % 5 + 1
    return result


def call_order(index: int) -> list[str]:
    """Xoay tail, luôn Original→Fact_Anchor trước mọi MT revision."""
    tail = [p for p in PRIMARY if p != "Original_common"]
    k = index % len(tail)
    return ["Original_common", "Fact_Anchor", *tail[k:], *tail[:k]]


class PilotData(HistoricalData):
    """Giá donor nguyên vẹn; chỉ48 selected query bị khóa outcome trước forecast."""
    def __init__(self, root: Path, units: list[dict] | None = None) -> None:
        super().__init__(root)
        rows = units if units is not None else selected_units(self.inputs["grid"])
        self.inputs = {**self.inputs, "grid": deepcopy(rows)}
        self.grid = {r["id"]: r for r in rows}
        self.by_day = {(r["symbol"], r["date"]): r for r in rows}
        self.scope = AlgorithmScope(root, symbols=CORE4)

    def verify_sources(self) -> None:
        """Rào deadline tại đúng ranh gửi HTTP, kể cả sau khi đã chờ pacing."""
        super().verify_sources()
        if getattr(self, "api_guard", None) is not None:
            self.api_guard()
        if getattr(self, "api_deadline", None) is not None and time.time() >= self.api_deadline:
            from core.groq_pacing import PilotStop
            raise PilotStop("PARTIAL_DEADLINE_48H; không gửi API sau hạn")


class FrozenBank:
    """Bank852 đã công bố; scaler raw train≤2022, query donor được ghi là transfer."""
    def __init__(self, data: PilotData) -> None:
        from core.bayesian_retriever import BayesianPriorRetriever
        from core.bayesian_memory import DEFAULT_DATA_DIR
        from core.execution_prices import load_verified_execution_data
        from core.price_feature_index import build_price_feature_index, PriceFeatureIndex, _VERIFIED
        self.data = data
        root = data.root
        self.retriever = BayesianPriorRetriever(bank_path=root / "data_manager/regime_memory_store.json",
            manifest_path=root / "data_manager/regime_memory_store.manifest.json", audit_path=root / "docs/plan/week2/memory_bank_audit.json")
        self.records = list(self.retriever._verified_by_id.values())
        if len(self.records) != 852 or max(r["exit_date"] for r in self.records) != "2022-12-30":
            raise ValueError("Bank pilot không phải bản852 đã khóa")
        prices = {s: load_verified_execution_data(DEFAULT_DATA_DIR, s) for s in CORE4}
        projection = [{k: r[k] for k in ("episode_id", "symbol", "as_of_date", "exit_date")} for r in self.records]
        manifest = DEFAULT_DATA_DIR / "manifest.json"
        proof = {"bank": {"bank_sha256": self.retriever._bank_sha256},
                 "prices": {s: {"manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest()} for s in CORE4},
                 "calendar": {"sha256": binding(root, data.protocol["effective_mt_bicl"]["calendar"]["source"])["sha256"]}}
        raw_index = build_price_feature_index(records=projection, prices=prices, calendar=data.calendar,
                                               source=RAW_SOURCE, provenance=proof)
        payload = raw_index.payload
        payload["transfer_contract"] = {"version": "frozen_raw_bank_to_donor_query_v1", "bank_source": RAW_SOURCE,
            "query_source": deepcopy(data.scope.source), "scaler_fit": "BANK_ONLY_EXIT_LE_2022_12_30",
            "no_price_splicing": True}
        query_payload = deepcopy(payload)
        query_payload["source"] = deepcopy(data.scope.source)
        query_guard = PriceFeatureIndex(query_payload, _verified=_VERIFIED)
        class TransferIndex(PriceFeatureIndex):
            """Chỉ đổi biên xác minh nguồn query; không relabel bank hoặc fit lại scaler."""
            def transform_query(self, symbol: str, as_of_date: str, features: dict, *, fold_id: str | None = None) -> dict:
                answer = query_guard.transform_query(symbol, as_of_date, features, fold_id=fold_id)
                answer["index_sha256"] = self.identity
                return answer
        self.index = TransferIndex(payload, _verified=_VERIFIED)
        from core.prior_example_selection import PriceExampleSelector
        self.selector = PriceExampleSelector(self.index, data.calendar)
        self.audit = {"records": 852, "source": proof, "index_identity": self.index.identity,
            "coverage": dict(Counter(r["symbol"] for r in self.records)), "max_exit": max(r["exit_date"] for r in self.records),
            "published_signal_receipt": binding(root, "docs/plan/week2/memory_bank_audit.json"),
            "raw_signal_journals_available": (root / "outputs/historical_memory_run/run_manifest.json").exists(),
            "signal_validation": "PUBLISHED_GIT_QA_AND_NORMALIZED_ENUMS; NO_NEW_RAW_JOURNAL_CERTIFICATION",
            "bank_query_provenance": "DIFFERENT_SOURCES_EXPLICIT_TRANSFER_NOT_RELABELLED",
            "scalers": {s: self.index.scaler(s, "2023-07-03") for s in CORE4}}
        # Chỉ so nhãn lịch sử của bank; không chạm bất kỳ payoff selected query nào.
        differences = []
        for row in self.records:
            label = data.label(row["symbol"], row["as_of_date"], as_of="2023-01-03", forecast_done=lambda _: False)
            differences.append(abs(label["r_net"] * 100. - row["outcome"]["net_return_pct"]))
        self.audit["donor_label_difference"] = {"count_above_1e_8": sum(v > 1e-8 for v in differences),
                                               "max_abs_percentage_points": max(differences)}

    def request(self, branch: str, shared: dict, regime: str) -> tuple[dict, dict]:
        """Giữ selection/gate/shrinkage/renderer nguyên bản; full population852 không bị cắt topK."""
        from core.mt_bicl_prompt import canonical_request
        from core.historical_evaluation_prior import signals
        query = {"symbol": shared["stock_name"], "as_of_date": shared["as_of_date"],
                 "current_regime": regime, "current_signals": signals(shared)}
        if any(r["exit_date"] >= query["as_of_date"] for r in self.records):
            raise ValueError("Bank chưa mature trước query")
        prefix, proof = "", {"branch": branch, "fallback": False, "bank_sha256": self.retriever._bank_sha256}
        if branch == "bayesian_v1":
            from core.bayesian_retriever import format_compact_prior_prefix
            result = self.retriever.retrieve(**query, mode="bayesian_regime", k=3, seed=42, scope="same_symbol")
            prefix = format_compact_prior_prefix(result["tasks"], result["stats"])
            proof["retrieval"] = result
        elif branch in ("C2", "A_tp_pool", "B_semantic"):
            from core.improvement_prior import build_evidence, build_request
            feature = self.data.features(query["symbol"], query["as_of_date"])
            evidence = build_evidence(self.retriever, branch, **query, selector=self.selector, query_features=feature)
            rendered = build_request(evidence, branch, self.retriever, selector=self.selector, query_features=feature)
            prefix = rendered["prefix"]
            proof.update(evidence=evidence, request=rendered, fallback=rendered["trace"]["fallback_to_original"])
        elif branch != "Original_common":
            raise ValueError("Nhánh không thuộc pilot")
        return canonical_request(deepcopy(shared), prefix, {"decision": self.data.protocol["inference"]["config"]}), proof


def carry_over(root: Path) -> tuple[dict[int, list[dict]], dict]:
    """Gộp quota H06/lượt đã hủy theo org+requestID; không reset quota theo UUID mới."""
    fields = {"id", "model", "started_at", "reserved_tokens", "status", "completed_at", "prompt_tokens", "completion_tokens",
              "total_tokens", "rate_limits", "retry_until", "pacing_seconds"}
    result = {i: {} for i in range(1, 6)}; proofs = {}
    for base in ("outputs/historical_reevaluation/h06_smoke_r1/usage", "outputs/historical_reevaluation/quota_history/cancelled_run_r1"):
        for org in range(1, 6):
            path = Path(base) / f"org{org}.json"
            if not (root / path).exists():
                raise ValueError("Thiếu ledger carry-over: " + path.as_posix())
            proofs[path.as_posix()] = binding(root, path)
            doc = json.loads((root / path).read_bytes())
            for old in doc["requests"]:
                row = {k: deepcopy(v) for k, v in old.items() if k in fields}
                identifier = row["id"]
                if identifier in result[org]:
                    present = result[org][identifier]
                    if any(k in present and present[k] != v for k, v in row.items()):
                        raise ValueError("Request quota trùng ID nhưng khác giá trị")
                    present.update(row)
                else:
                    result[org][identifier] = row
                result[org][identifier]["carry_over"] = True
    rows = {org: sorted(values.values(), key=lambda r: (r["started_at"], r["id"])) for org, values in result.items()}
    return rows, proofs


def archive_audit(root: Path, units: list[dict]) -> dict:
    """Archive fix chỉ có callback generations; không giả chúng thành raw HTTP phù hợp."""
    tree = subprocess.check_output(["git", "ls-tree", "-r", DONOR, "outputs/revision/r1_72h_run_v2"], cwd=root)
    names = tree.decode().splitlines()
    candidates = {u["id"]: sum((u["id"] + "_r0_") in line and "/nodes/" in line for line in names) for u in units}
    return {"commit": DONOR, "tree_listing_sha256": hashlib.sha256(tree).hexdigest(), "candidate_nodes": candidates,
            "reused_points": 0, "new_points": 48,
            "reason": "ARCHIVE_CALLBACK_REQUEST_GENERATIONS_NOT_DURABLE_RAW_HTTP_STATUS_BODY; NO_FAKE_CACHE",
            "cancelled_full_run_excluded": True, "h06_control_excluded": True}


def budget_schedule(rows: dict[int, list[dict]], tasks: list[dict], *, start: float, latency: float) -> dict:
    """Mô phỏng đúng quota rolling24h/61s theo hàng đợi đã khóa, gồm reserve retry."""
    from core.groq_pacing import MODEL_LIMITS
    history = {org: deepcopy(values) for org, values in rows.items()}; now = float(start)
    for task in tasks:
        org, model, tokens = task["org"], task["model"], task["tokens"]
        limits = MODEL_LIMITS[model]
        if tokens > limits["tpm"]:
            return {"status": "BLOCKED_BUDGET", "reason": "REQUEST_EXCEEDS_TPM", "tokens": tokens}
        while True:
            daily = [r for r in history[org] if r["model"] == model and r["started_at"] > now - 86400]
            minute = [r for r in daily if r["started_at"] > now - 61]
            if len(daily) >= limits["rpd"] or sum(r.get("total_tokens") or r["reserved_tokens"] for r in daily) + tokens > limits["tpd"]:
                now = min(r["started_at"] for r in daily) + 86400.01
                continue
            if len(minute) >= limits["rpm"] or sum(r["reserved_tokens"] for r in minute) + tokens > limits["tpm"]:
                now = min(r["started_at"] for r in minute) + 61.01
                continue
            break
        history[org].append({"model": model, "started_at": now, "reserved_tokens": tokens})
        now += latency
    return {"status": "PASS" if now - start <= 172800 else "BLOCKED_BUDGET", "finish_utc": datetime.fromtimestamp(now, timezone.utc).isoformat(),
            "hours": (now - start) / 3600., "task_count_including_retry_reserve": len(tasks), "latency_seconds_per_http": latency}


def anchored(root: Path, path: Path) -> dict:
    """Nguồn pilot/quyền API phải khớp byte neo Git trước khi đọc key."""
    raw = (root / path).read_bytes()
    if raw != subprocess.check_output(["git", "show", "HEAD:" + path.as_posix()], cwd=root):
        raise ValueError("Pilot chưa neo Git: " + path.as_posix())
    return load(root / path)


def source_files(root: Path) -> dict:
    """Pin phần baseline và toàn module pilot, không sửa profile/full grant cũ."""
    baseline = load(root / DOC / "historical_evaluation_runtime.json")["sources"]
    return {**baseline, **{name: binding(root, name) for name in CODE},
            **{name: binding(root, name) for name in ("core/bayesian_retriever.py", "core/price_feature_index.py",
                "core/prior_example_selection.py", "core/prior_price_similarity.py", "core/improvement_prior.py")}}
