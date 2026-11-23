"""Bank upstream đã durable và scaler train-only cho Bayesian v1/C2/A/B chín mã."""

from __future__ import annotations

from copy import deepcopy
from types import FunctionType
from functools import partial
from typing import Any

import numpy as np
import pandas as pd

from core.historical_evaluation_data import HistoricalData
from core.historical_signals import digest, report_signal
from core.mt_bicl_prompt import canonical_request


def signals(shared: dict[str, Any]) -> dict[str, str]:
    """Parse đúng trường kết luận, Alpha/Sentiment lấy mask/số đã đóng băng."""
    result = {"trend": report_signal(shared["trend_report"], ("Hướng xu hướng", "Trend direction")),
              "pattern": report_signal(shared["pattern_report"], ("Thiên lệch dự báo", "Directional bias")),
              "indicator_consensus": report_signal(shared["indicator_report"], ("Đồng thuận chủ đạo", "Dominant consensus"))}
    factors = shared["alpha_factors"]
    directions = [r["signal"] for r in factors]
    if any(v not in ("TĂNG", "GIẢM", "TRUNG TÍNH") for v in directions):
        raise ValueError("Alpha không có đúng signal enum")
    up, down = directions.count("TĂNG"), directions.count("GIẢM")
    result["alpha_consensus"] = "BULLISH" if up > down else "BEARISH" if down > up else "NEUTRAL"
    score = shared["sentiment_data"]["main_sentiment"].get("avg_score")
    result["sentiment"] = "NEUTRAL" if score is None or score == 0 else "POSITIVE" if score > 0 else "NEGATIVE"
    return result


class FeaturePopulation:
    """Tính feature không nhãn một lần; mỗi index truy vấn chứa đúng bank đã maturity."""

    def __init__(self, data: HistoricalData, *, forecast_done: Any = lambda _: False) -> None:
        """Scaler chỉ fit ID train donor, không dùng validation/test hoặc LLM signal."""
        self.data, self.scope = data, data.scope
        self.forecast_done = forecast_done
        self.validated: set[str] = set()
        self.rows: dict[str, dict[str, Any]] = {}
        self.folds: dict[str, dict[str, Any]] = {}
        for symbol in self.scope.symbols:
            history = [r for r in data.inputs["history"] if r["symbol"] == symbol]
            indices = data.calendar.get_indexer(pd.to_datetime([r["date"] for r in history]))
            features, _ = self.scope.module("mt_bicl_bank").batch_features(
                data.frames[symbol], data.events[symbol], data.calendar, indices)
            for row, feature in zip(history, features):
                self.rows[row["id"]] = {"episode_id": row["id"], "symbol": symbol, "as_of_date": row["date"],
                                        "exit_date": row["exit_date"], "features": feature}
        self.scalers: dict[str, dict[str, Any]] = {}
        index_module = self.scope.module("price_feature_index")
        for scope in data.inputs["scopes"]:
            symbol, fold = scope["symbol"], scope["fold"]
            dates = data.frames[symbol]["Datetime"].dt.strftime("%Y-%m-%d").to_numpy()
            units = [r for r in data.inputs["grid"] if r["symbol"] == symbol and r["fold"] == fold]
            self.folds[fold] = {"query_start": min(r["date"] for r in units),
                                "query_end": max(r["date"] for r in units)}
            ids = {symbol + ":" + str(dates[i]) for i in scope["train"]}
            rows = [r for key, r in self.rows.items() if key in ids]
            if len(rows) != len(ids):
                raise ValueError("Scaler thiếu train IDs trong lịch history đã khóa")
            rows.sort(key=lambda r: (r["as_of_date"], r["episode_id"]))
            fit = {"fit_cutoff": scope["train_max_exit"], "fit_inclusive": True,
                   "freeze_date": scope["first_validation_date"]}
            scaler = index_module._fit(rows, symbol, fit)
            if scaler["fit_max_exit_date"] is not None and scaler["fit_max_exit_date"] >= scope["first_validation_date"]:
                raise ValueError("Scaler vượt biên train/validation")
            self.scalers.setdefault(fold, {})[symbol] = scaler
        index_module._FOLDS = deepcopy(self.folds)

    def index(self, records: list[dict[str, Any]]) -> Any:
        """Producer chỉ cấp index có membership trùng bank đã xác minh, không index tương lai."""
        module = self.scope.module("price_feature_index")
        payload = {"records": [deepcopy(self.rows[r["episode_id"]]) for r in records],
            "scalers": self.scalers, "source": self.scope.source,
            "provenance": {"bank": {"bank_sha256": digest(records)},
                           "calendar": {"path": self.data.protocol["effective_mt_bicl"]["calendar"]["source"]}},
            "train_material": {"calendar_sha256": module._hash(
                self.data.calendar[self.data.calendar <= pd.Timestamp("2022-12-30")].strftime("%Y-%m-%d").tolist())}}
        return module.PriceFeatureIndex(payload, _verified=module._VERIFIED)

    def retriever(self, records: list[dict[str, Any]], cutoff: str) -> Any:
        """Caller cấp record đã đối soát raw/journal/nhãn; không dùng manifest W1 giả cho OOD."""
        module = self.scope.module("bayesian_retriever")
        by_id = {r["episode_id"]: deepcopy(r) for r in records}
        if len(by_id) != len(records) or any(key not in self.rows for key in by_id):
            raise ValueError("Bank có ID lạ hoặc trùng")
        for row in records:
            if row["exit_date"] >= cutoff:
                raise ValueError("Bank đưa nhãn chưa đóng vào query")
            module.normalize_signals(row["agent_signals"])
            if row["symbol"] not in self.scope.symbols or row["regime"] not in module.REGIMES:
                raise ValueError("Bank sai mã/regime")
            fingerprint = digest(row)
            if fingerprint not in self.validated:
                label = self.data.label(row["symbol"], row["as_of_date"], as_of=cutoff,
                                        forecast_done=self.forecast_done)
                bullish = any(module.is_bullish(row["agent_signals"][key]) for key in ("trend", "pattern"))
                expected = {"net_return_pct": label["r_net"] * 100., "actual_direction": "UP" if label["y"] else "DOWN",
                            "result": "WIN_IF_LONG" if label["y"] else "LOSS_IF_LONG",
                            "was_bull_trap": bool(bullish and not label["y"])}
                if row["outcome"] != expected or row["entry_date"] != label["entry_date"] or row["exit_date"] != label["exit_date"]:
                    raise ValueError("Bank label khác engine/source/PIT")
                self.validated.add(fingerprint)
        memory = self.scope.module("bayesian_memory").HistoricalMemory()
        memory._records = deepcopy(records)
        retriever = module.BayesianPriorRetriever.__new__(module.BayesianPriorRetriever)
        retriever._memory, retriever._verified_by_id = memory, by_id
        retriever._bank_sha256, retriever._price_index_identities = digest(records), set()
        return retriever

    def request(self, branch: str, shared: dict[str, Any], regime: str,
                records: list[dict[str, Any]], repeat: int) -> tuple[dict[str, Any], dict[str, Any]]:
        """Tái dùng selection/gate/prefix của phương pháp gốc trong scope chín mã."""
        prefix, proof = "", {"branch": branch, "fallback": False}
        if branch not in ("Original_common", "Original_duplicate"):
            retriever = self.retriever(records, shared["as_of_date"])
            query = {"symbol": shared["stock_name"], "as_of_date": shared["as_of_date"],
                     "current_regime": regime, "current_signals": signals(shared)}
            if branch in ("bayesian_v1", "random", "recent", "similarity"):
                mode = "bayesian_regime" if branch == "bayesian_v1" else branch
                result = retriever.retrieve(**query, mode=mode, k=3, seed=42, scope="same_symbol")
                source = self.scope.module("bayesian_retriever")
                # Template v1 chỉ hiện T/P/A/I; mở đúng flag đã có để không giả sentiment=NEUTRAL.
                formatter = source.format_compact_prior_prefix
                bound = FunctionType(formatter.__code__, {**formatter.__globals__,
                    "_prefix_task_line": partial(source._prefix_task_line, allow_sentiment=True)},
                    formatter.__name__, formatter.__defaults__)
                prefix = bound(result["tasks"], result["stats"])
                proof["retrieval"] = result
                proof["input_compatibility"] = "V1_FOUR_SIGNAL_TEMPLATE_ACCEPTS_VERIFIED_NEWS_NO_SENTIMENT_REWRITE"
            else:
                module = self.scope.module("improvement_prior")
                base = module.PROFILES[branch][0]
                index = self.index(records)
                selector = self.scope.module("prior_example_selection").PriceExampleSelector(index, self.data.calendar)
                feature = self.data.features(query["symbol"], query["as_of_date"])
                evidence = module.build_evidence(retriever, base, **query, selector=selector, query_features=feature)
                request = module.build_request(evidence, branch, retriever, selector=selector, query_features=feature)
                prefix = request["prefix"]
                proof.update(evidence=evidence, request=request, fallback=request["trace"]["fallback_to_original"])
        config = self.data.protocol["inference"]["config"]
        return canonical_request(deepcopy(shared), prefix, {"decision": config}, repeat), proof
