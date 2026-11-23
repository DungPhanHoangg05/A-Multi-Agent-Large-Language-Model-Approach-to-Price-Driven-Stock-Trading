"""Nguồn vendor chín mã, sentiment PIT và nhãn chỉ sau forecast durable."""

from __future__ import annotations

from copy import deepcopy
from datetime import timedelta
import hashlib
import subprocess
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

from agents.alpha_agent import _normalize_sentiment_scores
from core.backtest_engine import compute_round_trip_net_return
from core.execution_prices import corporate_action_barriers
from core.historical_asset_readiness import price_view
from core.historical_evaluation_protocol import INPUTS, PROTOCOL, FIX, MODEL, binding, read
from core.historical_evaluation_scope import AlgorithmScope, SYMBOLS
from core.historical_signals import native_json, snapshot_payload


class FrozenNews:
    """Giữ đồng thời verified count/score và mask downstream; không suy neutral từ missing."""

    def __init__(self, articles: dict[str, list[dict[str, Any]]]) -> None:
        """Chỉ nhận news đã pin, không đọc cache sống hoặc crawler."""
        self.articles = deepcopy(articles)

    def get_sentiment_at(self, symbol: str, cutoff_date: str, llm: Any = None,
                         window_days: int = 90) -> tuple[dict[str, Any], str]:
        """Date-only khả dụng ngày sau; score decay giữ convention donor."""
        if window_days != 90 or symbol not in SYMBOLS:
            raise ValueError("Sentiment ngoài universe/cửa sổ đã khóa")
        cutoff = pd.Timestamp(cutoff_date).normalize() + pd.Timedelta(hours=23, minutes=59, seconds=59)
        rows = []
        for article in self.articles.get(symbol, []):
            if not article.get("date_parsed"):
                continue
            published = pd.Timestamp(article["date_parsed"])
            minimum_available = published.normalize() + timedelta(days=1)
            available = pd.Timestamp(article.get("available_at") or minimum_available)
            if available.tzinfo is not None:
                available = available.tz_convert("Asia/Ho_Chi_Minh").tz_localize(None)
            if available < minimum_available:
                raise ValueError("Availability tin sớm hơn policy date-only")
            if not cutoff - pd.Timedelta(days=90) <= available <= cutoff or published > cutoff:
                continue
            score = article.get("numeric_score")
            if (article.get("scorer") not in ("visobert", "lexicon") or type(score) not in (float, int)
                    or not np.isfinite(score) or not -1 <= score <= 1):
                raise ValueError("Score/scorer tin không hợp lệ")
            rows.append((available, float(score)))
        count = len(rows)
        score = None
        if count >= 3:
            ages = np.asarray([(cutoff - stamp).total_seconds() / 86400 for stamp, _ in rows])
            weights = np.exp(-np.log(2) * ages / 30)
            score = float(np.average([v for _, v in rows], weights=weights))
        data = {"main_sentiment": {"article_count": count if count >= 3 else 0, "avg_score": score},
                "scored_articles": [], "related_sentiment": {}, "related_companies": [],
                "is_unavailable": count < 3, "verified_article_count": count}
        report = ("Sentiment KHÔNG KHẢ DỤNG do thiếu tối thiểu3 score đã xác minh; không coi là trung tính."
                  if count < 3 else f"Sentiment đã xác minh: score={score:.6f}; số bài={count}; peers không khả dụng.")
        return data, report


class HistoricalData:
    """Tách prefix dùng forecast khỏi API nhãn; không ghép giá raw vào chuỗi donor."""

    def __init__(self, root: Path, *, verify: bool = True) -> None:
        """Kiểm input H03 và raw/event H02 trước khi mở dữ liệu."""
        self.root = root.resolve()
        self.protocol = read(root, PROTOCOL, envelope=True)
        self.inputs = read(root, INPUTS, envelope=True)
        self.model_manifest = read(root, MODEL, envelope=True)
        if verify:
            for name in (PROTOCOL, INPUTS, MODEL):
                if (root / name).read_bytes() != subprocess.check_output(["git", "show", "HEAD:" + name.as_posix()], cwd=root):
                    raise ValueError("Input/protocol/model chưa neo Git")
            self.verify_sources()
        self._frames: dict[str, pd.DataFrame] = {}
        self._events: dict[str, list[dict[str, str]]] = {}
        audit = read(root, "outputs/historical_reevaluation/h02_data_r1/execution_audit.json")
        manifest = read(root, FIX / "outputs/revision/r1_prices_v1/manifest.json")
        for record in manifest["symbols"]:
            symbol = record["symbol"]
            frame, _ = price_view((root / FIX / "outputs/revision/r1_prices_v1" / record["path"]).read_bytes())
            frame = frame.rename(columns={"date": "Datetime"})
            frame["Datetime"] = pd.to_datetime(frame["Datetime"])
            self._frames[symbol] = frame
            directory = root / "outputs/historical_reevaluation/h02_data_r1"
            for name in (symbol + ".raw.csv", symbol + ".events.json"):
                if hashlib.sha256((directory / name).read_bytes()).hexdigest() != audit["files"][name]:
                    raise ValueError("Raw/event H02 khác audit đã khóa")
            raw = pd.read_csv(directory / (symbol + ".raw.csv"), parse_dates=["Datetime"])
            raw = raw.loc[raw["Datetime"] >= frame["Datetime"].iloc[0]].copy()
            event_rows = read(root, directory.relative_to(root) / (symbol + ".events.json"))["records"]
            dates = corporate_action_barriers(raw, event_rows)
            self._events[symbol] = [{"exrightDate": day} for day in dates.strftime("%Y-%m-%d")]
        path = self.protocol["effective_mt_bicl"]["calendar"]["source"]
        self.history = pd.read_csv(root / path, parse_dates=["Datetime"])
        self.calendar = pd.DatetimeIndex(self.history["Datetime"])
        self.grid = {r["id"]: r for r in self.inputs["grid"]}
        self.by_day = {(r["symbol"], r["date"]): r for r in self.inputs["grid"]}
        self.news = FrozenNews(read(root, FIX / "outputs/revision/r1_72h_bank_v2/news.json"))
        self.scope = AlgorithmScope(root)

    @property
    def frames(self) -> dict[str, pd.DataFrame]:
        """Caller không sửa được cache giá nguồn qua một nhánh hoặc fixture."""
        return {symbol: frame.copy(deep=True) for symbol, frame in self._frames.items()}

    @property
    def events(self) -> dict[str, list[dict[str, str]]]:
        """Ngày barrier cũng thuộc cache sở hữu riêng."""
        return deepcopy(self._events)

    def verify_sources(self) -> None:
        """Không tự cập nhật checksum khi nguồn đổi, kể cả schema/protocol/model."""
        for entries in (self.protocol["source_bindings"], self.inputs["source_bindings"]):
            for record in entries.values():
                if binding(self.root, record["path"]) != record:
                    raise ValueError("Nguồn khác H03: " + record["path"])
        for directory, entries in self.model_manifest["artifact_trees"].items():
            for name, expected in entries.items():
                actual = binding(self.root, Path(directory) / name)
                if any(actual[k] != expected[k] for k in ("bytes", "sha256")):
                    raise ValueError("Model component khác manifest")

    def prefix(self, symbol: str, cutoff: str) -> pd.DataFrame:
        """Không trả nến entry/exit tương lai vào graph hoặc context query."""
        if symbol not in self._frames:
            raise ValueError("Mã ngoài universe")
        frame = self._frames[symbol]
        prefix = frame.loc[frame["Datetime"] <= pd.Timestamp(cutoff)].copy(deep=True)
        if prefix.empty or prefix["Datetime"].iloc[-1] != pd.Timestamp(cutoff):
            raise ValueError("Không có đúng phiên query")
        return prefix

    def state(self, symbol: str, cutoff: str) -> dict[str, Any]:
        """Graph chỉ thấy45 nến và600 nến Alpha, không nhãn/cột payoff."""
        prefix = self.prefix(symbol, cutoff)
        if len(prefix) < 600:
            raise ValueError("Không đủ600 nến sạch cho Alpha")
        return {"stock_name": symbol, "as_of_date": cutoff, "window_end_date": cutoff,
                "time_frame": "1d", "language": "vi", "is_backtest": True, "messages": [],
                "kline_data": snapshot_payload(prefix.tail(45)), "point_in_time_df": prefix.tail(600).copy(),
                "sentiment_store": self.news, "alpha_norm_method": "zscore_tanh", "alpha_weights": None}

    def features(self, symbol: str, cutoff: str) -> dict[str, Any]:
        """Bốn feature giữ primitive21, barrier lấy từ raw audit chứ không splice giá."""
        return self.scope.features(self._frames[symbol], self._events[symbol], self.calendar, cutoff,
                                   source=self.scope.source)

    def sentiment_audit(self) -> list[dict[str, Any]]:
        """Đối soát đầy đủ hai mask trên1.020 unit, không gọi Alpha/LLM."""
        rows = []
        for unit in self.inputs["grid"]:
            data, _ = self.news.get_sentiment_at(unit["symbol"], unit["date"])
            normalized = _normalize_sentiment_scores(deepcopy(data))
            rows.append({"id": unit["id"], "verified_count": data["verified_article_count"],
                         "verified_score": data["main_sentiment"]["avg_score"],
                         "missing": data["is_unavailable"], "downstream_reliable": bool(normalized["is_reliable"]),
                         "downstream_count": int(normalized["article_count"])})
        return rows

    def label(self, symbol: str, cutoff: str, *, as_of: str,
              forecast_done: Callable[[str], bool]) -> dict[str, Any]:
        """Chỉ đọc Open/Close target sau maturity và mọi forecast của query đã durable."""
        from core.bayesian_memory import iso_date
        cutoff, as_of = iso_date(cutoff), iso_date(as_of)
        if symbol not in self._frames:
            raise ValueError("Mã nhãn ngoài universe đã khóa")
        unit = self.by_day.get((symbol, cutoff))
        if unit is not None and forecast_done(unit["id"]) is not True:
            raise ValueError("Query outcome bị khóa trước forecast durable")
        frame = self._frames[symbol]
        positions = pd.DatetimeIndex(frame["Datetime"])
        index = int(positions.get_indexer([pd.Timestamp(cutoff)])[0])
        if index < 0 or index + 3 >= len(frame):
            raise ValueError("Nhãn thiếu phiên thực thi")
        exit_date = str(positions[index + 3].date())
        entry_date = str(positions[index + 1].date())
        if unit is not None and (entry_date != unit["entry_date"] or exit_date != unit["exit_date"]):
            raise ValueError("Nhãn không khớp lịch H03")
        if exit_date >= as_of:
            raise ValueError("Nhãn chưa đóng nghiêm ngặt trước cutoff")
        net = float(compute_round_trip_net_return(float(frame["Open"].iloc[index + 1]),
                                                 float(frame["Close"].iloc[index + 3])))
        return {"r_net": net, "y": int(net > 0), "entry_date": entry_date,
                "exit_date": exit_date, "quality": "VENDOR_SERIES_LIMITED"}
