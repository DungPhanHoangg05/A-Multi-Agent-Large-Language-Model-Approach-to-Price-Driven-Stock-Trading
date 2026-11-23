"""Tạo lại các tín hiệu lịch sử có thể tính offline và khóa đầu vào hai node thị giác."""
from __future__ import annotations

from collections import Counter
from contextlib import redirect_stdout
from copy import deepcopy
import io
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import pandas as pd

from core.causal_alpha import CONFIG, alpha_values, frame_document, validated_frame
from core.execution_prices import raw_point_in_time_snapshot, load_verified_execution_data
from core.finalize_bank_resources import ASSETS, CONTRACT, RECIPE, mature_cycles
from core.finalize_news import FinalizedNews, snapshot_values
from core.finalize_news_release import CORPUS, COVERAGE
from core.finalize_price_acceptance import ACCEPTANCE
from core.finalize_price_audit import visible_event_dates
from core.finalize_raw_selector import cycle_masks, fit_raw_selector
from core.historical_runner import PrefixRegimeProvider
from core.historical_signals import report_signal, snapshot_payload
from core.unified_contracts import digest, json_bytes
from core.unified_preflight_assets import schedule, write_new
from core.unified_protocol import CORE4, binding, read

VERSION = "finalize_bank_signal_rebuild_v2"
FIRST_SELECTOR_SESSION = 686
WINDOW = 45
NODES = ("pattern", "trend")


def check_bindings(root: Path, pins: list[dict]) -> None:
    """Đối chiếu byte tại ranh giới trước khi nạp giá hoặc fit local."""
    for pin in pins:
        if binding(root, pin["path"]) != pin:
            raise ValueError("Nguồn tạo lại tín hiệu đã đổi: " + pin["path"])


def rebuild_recipe(root: Path) -> dict[str, Any]:
    """Lưu recipe lịch sử riêng trước khi tạo tín hiệu và kiểm request."""
    contract = read(root, CONTRACT, True)
    numerical = read(root, ASSETS + "manifest.json", True)
    prices = read(root, ACCEPTANCE, True)
    check_bindings(root, [numerical["recipe"], *numerical["asset_bindings"], *prices["source_bindings"].values()])
    paths = (CONTRACT, RECIPE, ACCEPTANCE, CORPUS, COVERAGE, ASSETS + "manifest.json",
             "core/finalize_bank_signals.py", "scripts/rebuild_finalize_bank_signals.py",
             "core/historical_runner.py", "core/historical_signals.py", "core/regime_detector.py",
             "core/causal_alpha.py", "core/finalize_raw_selector.py", "core/alpha_compare.py",
             "core/execution_prices.py", "core/backtest_engine.py", "core/finalize_news.py",
             "agents/indicator_agent.py", "agents/pattern_agent.py", "agents/trend_agent.py",
             "core/historical_evaluation_graph.py", "core/unified_execution_providers.py",
             "utils/graph_util.py", "core/research_invocation.py")
    return {"version": VERSION, "inputs": [binding(root, name) for name in paths],
            "upstream": ["indicator", *NODES], "chart_rows": WINDOW, "language": "vi",
            "historical_selector_first_session": FIRST_SELECTOR_SESSION,
            "historical_selector_policy": "Từ phiên 686 tìm ranh đầu đủ train cycle thực thi theo cadence 3. Dùng lịch U06 và giữ cùng một fit cho các episode sau đó. Episode sớm hơn giữ Alpha NA.",
            "alpha_projection": "Tính chuỗi toán tử prefix-causal một lượt trên miền bank, chỉ lấy hàng tại cutoff mỗi episode.",
            "regime_policy": "HMM theo đúng prefix VNINDEX mỗi ngày quyết định, giữ recipe PrefixRegimeProvider.",
            "sentiment_policy": "Dùng snapshot FIN05. Thiếu chứng cứ là null có mask, không gán neutral.",
            "candidate_vision_config": contract["model_options"]["candidate"],
            "hosted_calls_authorized": False, "signal_release": False}


def historical_selector(frame: pd.DataFrame, events: list[dict], last_day: str) -> dict | None:
    """Fit một lần theo lịch U06, chỉ đọc nến trước mốc áp dụng đầu tiên."""
    if len(frame) <= FIRST_SELECTOR_SESSION:
        return None
    dates = frame.Datetime.dt.strftime("%Y-%m-%d").tolist()
    for first in range(FIRST_SELECTOR_SESSION, min(len(frame) - 57, dates.index(last_day) + 1), CONFIG["cycle_step"]):
        split = schedule(frame, first, first + 57)
        split["test_end"] = last_day
        known_dates, _ = visible_event_dates(events, dates[first - 1])
        known_events = [{"exrightDate": day} for day in known_dates]
        masks, _ = cycle_masks(frame.iloc[:first], known_events, split, frozenset())
        if masks["train"].sum() >= CONFIG["min_train"] and masks["validation"].sum() >= CONFIG["min_validation"]:
            return fit_raw_selector(frame, known_events, split, frozenset())
    return None


def alpha_signal(prefix: pd.DataFrame, cutoff: str, selector: dict | None, *,
                 factor_row: pd.Series | None = None) -> dict[str, Any]:
    """Không dùng selector trước ngày được phép; dữ liệu không đủ giữ trạng thái NA."""
    if selector is None or cutoff < selector["payload"]["schedule"]["test_start"]:
        return {"value": None, "reason": "BEFORE_HISTORICAL_SELECTOR_SUPPORT"}
    fit = selector["payload"]
    if (cutoff > fit["schedule"]["test_end"] or fit["fit_end"] >= cutoff
            or str(prefix.Datetime.iloc[-1].date()) != cutoff):
        raise ValueError("Selector lịch sử vượt phạm vi hoặc prefix khác cutoff")
    if factor_row is not None and factor_row.name != cutoff:
        raise ValueError("Hàng Alpha đã tính khác cutoff episode")
    values = alpha_values(prefix).iloc[-1] if factor_row is None else factor_row
    selected = [float(values[row["alpha_id"]] * row["orientation"]) for row in fit["selected"]]
    if not np.isfinite(selected).all():
        return {"value": None, "reason": "SELECTED_FACTOR_UNAVAILABLE", "selector_sha256": selector["sha256"]}
    threshold = fit["threshold"]
    up, down = sum(x > threshold for x in selected), sum(x < -threshold for x in selected)
    consensus = "BULLISH" if up > down else "BEARISH" if down > up else "NEUTRAL"
    return {"value": consensus, "selector_sha256": selector["sha256"], "fit_end": fit["fit_end"],
            "threshold": threshold, "factors": [row | {"value": v} for row, v in zip(fit["selected"], selected)]}


def point_input(symbol: str, cutoff: str, frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """State upstream chỉ nhận 45 nến và metadata của ngày quyết định."""
    prefix = validated_frame(raw_point_in_time_snapshot(frame, cutoff))
    if len(prefix) < 600:
        raise ValueError("Episode lịch sử thiếu 600 nến warm-up")
    return prefix, {"stock_name": symbol, "as_of_date": cutoff, "window_end_date": cutoff,
                    "time_frame": "1d", "language": "vi", "is_backtest": True, "messages": [],
                    "kline_data": snapshot_payload(prefix.tail(WINDOW))}


class CapturedRequest(BaseException):
    """Dừng tại request thật trước transport, vượt qua handler fallback của agent."""


def vision_probe(root: Path, state: dict, config: dict) -> dict[str, Any]:
    """Dùng chart và node thật để bắt body đầu tiên, không sinh phản hồi giả."""
    from agents.pattern_agent import create_pattern_agent
    from agents.trend_agent import create_trend_agent
    from core.historical_evaluation_graph import GraphProvider
    from core.unified_execution_providers import VisionProxy
    from utils.graph_util import TechnicalTools

    renderer = GraphProvider(SimpleNamespace(root=root), None)
    requests = {}

    class Capture:
        """Chỉ lưu fingerprint của body vừa nhận, không có HTTP client."""
        def call(self, slot: str, org: int, body: dict, attempt: str) -> None:
            requests[slot] = {"request_sha256": digest(body), "model": body["model"],
                              "max_tokens": body["max_tokens"], "message_count": len(body["messages"])}
            raise CapturedRequest()

    with redirect_stdout(io.StringIO()):
        for role, factory in (("pattern", create_pattern_agent), ("trend", create_trend_agent)):
            chart = renderer.render(role, state["kline_data"])
            if not chart.get(role + "_image"):
                raise ValueError("Renderer lịch sử không sinh ảnh " + role)
            proxy = VisionProxy(Capture(), role, 0, "capture-only", config)
            try:
                factory(None, proxy, TechnicalTools())(deepcopy(state) | chart)
            except CapturedRequest:
                pass
            if role not in requests:
                raise ValueError("Node không tạo request thị giác: " + role)
    return {"renderer_sha256": renderer.renderer_hash, "requests": requests}


def build(root: Path, directory: Path, recipe: dict) -> dict[str, Any]:
    """Tính node offline, lưu từng episode theo hash và chặn xuất bank khi còn thiếu."""
    from agents.indicator_agent import create_indicator_agent
    from core.bayesian_memory import atomic_write_json
    from utils.graph_util import TechnicalTools

    if rebuild_recipe(root) != recipe:
        raise ValueError("Recipe tạo lại tín hiệu khác nguồn đã khóa")
    accepted = read(root, ACCEPTANCE, True)
    corpus = read(root, CORPUS, True)
    news = FinalizedNews(corpus["records"], evidence=corpus["evidence_registry"], root=root)
    numeric = read(root, ASSETS + "bank.json")["records"]
    # Tách ngay metadata khỏi nhãn đã dựng. Các node không nhận record r_net hoặc y.
    rows = [{key: row[key] for key in ("episode_id", "symbol", "as_of_date", "exit_date")} for row in numeric]
    reserved = set(read(root, RECIPE, True)["reserved_ids"])
    mature_cycles(rows, reserved, "2022-12-31")
    market = pd.read_csv(root / accepted["calendar"], parse_dates=["Datetime"])
    regimes = PrefixRegimeProvider(directory / "regimes", market.loc[market.Datetime < "2023-01-01"])
    indicator = create_indicator_agent(None, TechnicalTools())
    checkpoints, selectors, probes, regime_cache = [], {}, {}, {}
    for symbol in CORE4:
        frame, events = load_verified_execution_data(root / accepted["bank_source"], symbol)
        episodes = [row for row in rows if row["symbol"] == symbol]
        last_day = max(row["as_of_date"] for row in episodes)
        selectors[symbol] = historical_selector(frame, events, last_day)
        factor_rows = None
        if selectors[symbol] is not None:
            write_new(directory / "selectors" / (symbol + ".json"), json_bytes(selectors[symbol]))
            bank_prefix = validated_frame(raw_point_in_time_snapshot(frame, last_day))
            factor_rows = alpha_values(bank_prefix)
            factor_rows.index = bank_prefix.Datetime.dt.strftime("%Y-%m-%d")
        for row in episodes:
            cutoff = row["as_of_date"]
            identifier = symbol + "-" + cutoff
            prefix, state = point_input(symbol, cutoff, frame)
            news_snapshot = news.snapshot(symbol, cutoff)
            sentiment, _ = snapshot_values(news_snapshot, expected_sha256=news_snapshot["sha256"])
            parent = {"recipe_sha256": digest(recipe), "prefix_sha256": digest(frame_document(prefix)),
                      "window_sha256": digest(state["kline_data"]), "news_sha256": news_snapshot["sha256"]}
            path = directory / "points" / (identifier + ".json")
            if cutoff not in regime_cache:
                regime_cache[cutoff] = regimes.get(cutoff, verify_only=path.exists())
            if path.exists():
                checkpoint = read(directory, "points/" + path.name, True)
                if checkpoint["parent"] != parent or checkpoint["episode_id"] != row["episode_id"]:
                    raise ValueError("Checkpoint khác snapshot lịch sử: " + identifier)
                if checkpoint["regime"] != regime_cache[cutoff]:
                    raise ValueError("Checkpoint khác model HMM lịch sử: " + identifier)
            else:
                with redirect_stdout(io.StringIO()):
                    report = indicator(deepcopy(state))["indicator_report"]
                direction = report_signal(report, ("Đồng thuận chủ đạo", "Dominant consensus"))
                checkpoint = {"episode_id": row["episode_id"], "symbol": symbol, "cutoff": cutoff,
                              "parent": parent, "indicator": {"value": direction, "report": report},
                              "alpha": alpha_signal(prefix, cutoff, selectors[symbol],
                                                    factor_row=None if factor_rows is None else factor_rows.loc[cutoff]),
                              "regime": regime_cache[cutoff], "sentiment": {"value": None,
                                  "reason": sentiment["missing_reason"], "available": not sentiment["is_unavailable"]},
                              "vision": {role: {"value": None, "reason": "PENDING_FIN09_VISION"} for role in NODES}}
                if checkpoint["sentiment"]["available"]:
                    raise ValueError("Recipe signal v1 cần được cập nhật khi đổi support tin")
                atomic_write_json(path, {"payload": checkpoint, "sha256": digest(checkpoint)})
            if checkpoint["alpha"]["value"] is not None and symbol not in probes:
                probes[symbol] = {"point_id": identifier, **vision_probe(root, state, recipe["candidate_vision_config"])}
            checkpoints.append({"id": identifier, "sha256": digest(checkpoint),
                                "alpha_available": checkpoint["alpha"]["value"] is not None,
                                "alpha_pending_reason": checkpoint["alpha"].get("reason")})
        print(f"Đã đối soát tín hiệu offline {symbol}: {len(episodes)} chu kỳ", flush=True)
    ready = sum(c["alpha_available"] for c in checkpoints)
    return {"version": VERSION, "status": "OFFLINE_SIGNALS_REBUILT_VISION_PENDING", "FIN06_complete": False,
            "recipe_sha256": digest(recipe), "indicator_count": len(checkpoints), "regime_count": len(checkpoints),
            "regime_distinct_cutoffs": len({r["as_of_date"] for r in rows}), "alpha_count": ready,
            "alpha_pending": dict(Counter(c["alpha_pending_reason"] for c in checkpoints if not c["alpha_available"])),
            "sentiment_unavailable_count": len(checkpoints), "vision_stage_count_planned": len(checkpoints) * len(NODES),
            "vision_probed": probes, "vision_ready": 0, "hosted_calls": 0, "signal_admitted": 0,
            "query_outcomes_computed": False, "points": checkpoints,
            "selector_sha256": {s: a["sha256"] if a else None for s, a in selectors.items()}}
