"""Profile alpha nhân quả riêng: toán tử PIT, train/validation purge và selector đóng băng."""
from __future__ import annotations

import ast
from copy import deepcopy
from functools import lru_cache, partial
import hashlib
from importlib.metadata import version
from pathlib import Path
import platform
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from core import alpha_compare as native
from core.unified_contracts import day, digest

PROFILE = "causal_common_v1"
CONFIG = {"warmup": 300, "normalizer_min_periods": 20, "min_train": 60, "min_validation": 30,
          "min_validation_longs": 5, "thresholds": [.05, .1, .2], "top_n": 5, "cycle_step": 3,
          "orientation": "TRAIN_SPEARMAN_ONLY", "selection": "VALIDATION_LONG_CASH_MEAN_RETURN",
          "normalization": "EXPANDING_PREFIX_DDOF1_TANH", "volume": "OBSERVED_ONLY_NO_PROXY",
          "label_contract": "net_cycle_v1", "fee": .0025, "slippage": .001, "horizon": 3}
COLUMNS = ("Datetime", "Open", "High", "Low", "Close", "Volume")
WINDOW_REPLACEMENTS = {"min(250, len(d))": 250, "min(230, max(len(d) - 6, 2))": 230,
                       "min(200, len(d))": 200, "min(200, max(len(d) - 2, 2))": 200,
                       "min(250, len(d) - 1)": 250, "min(240, len(d) - 1)": 240}


def sources() -> dict[str, str]:
    """Pin công thức gốc và bản sửa nhân quả, không sửa nguồn native."""
    return {name: hashlib.sha256(Path(path).read_bytes()).hexdigest() for name, path in
            (("native", native.__file__), ("causal", __file__),
             ("economics", Path(__file__).resolve().parent / "backtest_engine.py"))}


def runtime() -> dict[str, str]:
    """Pin runtime số học của artifact thay vì chỉ giữ tên profile."""
    return {"python": platform.python_version(), **{name: version(name) for name in ("numpy", "pandas", "scipy")}}


def validated_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hóa một lần; volume thiếu vẫn thiếu, giá/ngày sai phải dừng."""
    if not isinstance(frame, pd.DataFrame) or not set(COLUMNS).issubset(frame.columns) or frame.empty:
        raise ValueError("Thiếu nguồn OHLCV cho causal alpha")
    result = frame.loc[:, COLUMNS].copy().reset_index(drop=True)
    dates = pd.DatetimeIndex(pd.to_datetime(result.Datetime))
    if (dates.tz is not None or dates.hasnans or dates.has_duplicates or not dates.is_monotonic_increasing
            or not dates.equals(dates.normalize())):
        raise ValueError("Lịch causal alpha phải tăng, duy nhất và không timezone")
    result["Datetime"] = dates
    for name in COLUMNS[1:]:
        result[name] = pd.to_numeric(result[name], errors="raise").astype(float)
    prices = result.loc[:, COLUMNS[1:5]].to_numpy()
    volume = result.Volume.to_numpy()
    if (not np.isfinite(prices).all() or (prices <= 0).any() or np.isinf(volume).any()
            or (volume[np.isfinite(volume)] < 0).any()
            or (result.High < result[["Open", "Close"]].max(axis=1)).any()
            or (result.Low > result[["Open", "Close"]].min(axis=1)).any()):
        raise ValueError("Giá/volume causal alpha không hợp lệ")
    return result


def frame_document(frame: pd.DataFrame) -> dict[str, Any]:
    """Projection nguồn chính xác, giữ missing bằng null và số chưa làm tròn."""
    values = frame.loc[:, COLUMNS[1:]].astype(object).where(frame.loc[:, COLUMNS[1:]].notna(), None)
    return {"Datetime": frame.Datetime.dt.strftime("%Y-%m-%d").tolist(), **values.to_dict(orient="list")}


def normalize(series: pd.Series, method: str = "zscore_tanh") -> pd.Series:
    """Mỗi dòng chỉ dùng prefix đến chính nó; constant có giá trị 0, missing không fill."""
    if method != "zscore_tanh":
        raise ValueError("Causal v1 chỉ đăng ký expanding zscore_tanh")
    values = series.replace([np.inf, -np.inf], np.nan)
    window = values.expanding(min_periods=CONFIG["normalizer_min_periods"])
    mu, sigma = window.mean(), window.std(ddof=1)
    output = np.tanh((values - mu) / sigma.where(sigma > 1e-12))
    return output.mask((sigma <= 1e-12) & values.notna(), 0.)


def delay(series: pd.Series, period: int = 1) -> pd.Series:
    """Giữ NaN đầu chuỗi, tuyệt đối không bfill từ các dòng sau."""
    if type(period) is not int or period < 0:
        raise ValueError("Delay chỉ nhận lag không âm")
    return series.shift(period)


def features(frame: pd.DataFrame) -> pd.DataFrame:
    """Nhánh volume theo từng dòng; không suy real/proxy bằng toàn cửa sổ."""
    data = frame.copy()
    data["returns"] = data.Close.pct_change(fill_method=None)
    data["log_ret"] = np.log(data.Close / data.Close.shift(1))
    data["vwap"] = (data.High + data.Low + data.Close) / 3.
    data["volume"] = data.Volume
    data["log_vol"] = np.log(data.Volume.where(data.Volume > 0))
    data["adv20"] = data.Volume.rolling(20, min_periods=1).mean()
    data["adv10"] = data.Volume.rolling(10, min_periods=1).mean()
    data["bar_range"] = (data.High - data.Low).where(data.High > data.Low)
    data["close_pos"] = (data.Close - data.Low) / data.bar_range - .5
    data["_has_vol"] = data.Volume.notna()
    return data


@lru_cache(maxsize=1)
def handlers() -> dict[str, Any]:
    """Biên dịch đúng 85 handler trong namespace riêng, sửa sáu cửa sổ phụ thuộc độ dài."""
    tree = ast.parse(Path(native.__file__).read_text(encoding="utf-8-sig"))
    names = {fn.__name__ for fn, _ in native.ALPHA_REGISTRY.values()}
    namespace = dict(native.__dict__)
    namespace.update(normalize_alpha=normalize, delay=delay,
                     _safe_series=lambda s: s.replace([np.inf, -np.inf], np.nan))
    found: set[str] = set()
    class FixedWindows(ast.NodeTransformer):
        """Không đổi công thức khác; gặp thêm len(d) thì fail để audit lại phiên bản."""
        def visit_Call(self, node: ast.Call) -> ast.AST:
            expression = ast.unparse(node)
            if expression in WINDOW_REPLACEMENTS:
                found.add(expression)
                return ast.copy_location(ast.Constant(WINDOW_REPLACEMENTS[expression]), node)
            return self.generic_visit(node)
    definitions = [deepcopy(node) for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    if len(definitions) != len(names) or len(native.ALPHA_REGISTRY) != 85:
        raise ValueError("Registry native đã đổi, cần audit causal v1 lại")
    module = FixedWindows().visit(ast.Module(body=definitions, type_ignores=[]))
    if found != set(WINDOW_REPLACEMENTS) or any(isinstance(n, ast.Call) and ast.unparse(n) == "len(d)" for n in ast.walk(module)):
        raise ValueError("Chưa xử lý hết cửa sổ theo độ dài input")
    exec(compile(ast.fix_missing_locations(module), "causal_alpha_handlers_v1", "exec", dont_inherit=True), namespace)
    return {key: namespace[fn.__name__] for key, (fn, _) in native.ALPHA_REGISTRY.items()}


def alpha_values(frame: pd.DataFrame) -> pd.DataFrame:
    """85 cột vector hóa theo thời gian, warm-up/volume missing có mask chung rõ ràng."""
    frame = validated_frame(frame)
    data = features(frame)
    available = frame.Volume.notna().rolling(CONFIG["warmup"], min_periods=CONFIG["warmup"]).sum() == CONFIG["warmup"]
    output = {}
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        for identifier, handler in handlers().items():
            raw = handler(data).replace([np.inf, -np.inf], np.nan).where(available)
            output[identifier] = normalize(raw).where(available)
    return pd.DataFrame(output, index=frame.index)


def validate_schedule(schedule: dict[str, str]) -> None:
    """Train < validation < test, không nhận ngầm cutoffs theo hiệu ứng quan sát."""
    keys = ("train_start", "train_end", "validation_start", "validation_end", "test_start", "test_end")
    if type(schedule) is not dict or set(schedule) != set(keys):
        raise ValueError("Lịch selector thiếu train/validation/test")
    dates = [day(schedule[key]) for key in keys]
    if not dates[0] < dates[1] < dates[2] < dates[3] < dates[4] <= dates[5]:
        raise ValueError("Lịch train/validation/test chồng lấn hoặc sai thứ tự")


def fit_selector(frame: pd.DataFrame, schedule: dict[str, str]) -> dict[str, Any]:
    """Không chạm giá test: orientation train, chọn threshold/top5 trên validation đã purge."""
    validate_schedule(schedule)
    if not isinstance(frame, pd.DataFrame) or not set(COLUMNS).issubset(frame.columns):
        raise ValueError("Nguồn selector thiếu schema OHLCV")
    # Cắt trước kiểm giá để poison/thiếu giá test không thể tác động fit.
    raw_dates = pd.to_datetime(frame.Datetime)
    past = validated_frame(frame.loc[raw_dates < pd.Timestamp(schedule["test_start"])]).copy()
    dates = past.Datetime.dt.strftime("%Y-%m-%d")
    for key in ("train_start", "train_end", "validation_start", "validation_end"):
        if schedule[key] not in set(dates):
            raise ValueError("Boundary train/validation không thuộc lịch nguồn")
    values = alpha_values(past)
    from core.backtest_engine import compute_round_trip_net_return
    returns = np.full(len(past), np.nan)
    # Ufunc gọi chính oracle scalar, không lặp từng dòng DataFrame hoặc sao chép công thức phí.
    oracle = np.frompyfunc(partial(compute_round_trip_net_return, fee=.0025, slippage=.001), 2, 1)
    returns[:-3] = oracle(past.Open.to_numpy()[1:-2], past.Close.to_numpy()[3:]).astype(float)
    exits = dates.shift(-3)
    masks, purged = {}, {}
    for split, boundary in (("train", "validation_start"), ("validation", "test_start")):
        region = dates.between(schedule[split + "_start"], schedule[split + "_end"])
        start = int(np.flatnonzero(region)[0])
        grid = (np.arange(len(past)) - start) % 3 == 0
        mature = exits.notna() & (exits < schedule[boundary])
        masks[split] = (region & grid & mature).to_numpy(bool)
        purged[split] = dates[region & grid & ~mature].tolist()
    candidates: dict[str, Any] = {}
    eligible = []
    for identifier in values:
        av = values[identifier].to_numpy(float)
        train = masks["train"] & np.isfinite(av) & np.isfinite(returns)
        ic = None
        if train.sum() >= CONFIG["min_train"] and np.std(av[train]) > 1e-12 and np.std(returns[train]) > 1e-12:
            coefficient = float(spearmanr(av[train], returns[train]).statistic)
            ic = coefficient if np.isfinite(coefficient) else None
        candidates[identifier] = {"train_n": int(train.sum()), "train_ic": ic,
                                  "orientation": None if ic is None else (1 if ic >= 0 else -1)}
        if ic is not None:
            eligible.append(identifier)
    if len(eligible) < 5:
        raise ValueError("Không đủ năm candidate có train support, không dùng fallback native")
    common = masks["validation"] & np.isfinite(returns) & np.isfinite(values[eligible].to_numpy()).all(axis=1)
    if int(common.sum()) < CONFIG["min_validation"]:
        raise ValueError("Validation common support sau purge không đủ")
    searches = []
    for threshold in CONFIG["thresholds"]:
        scores = []
        for identifier in eligible:
            oriented = values[identifier].to_numpy()[common] * candidates[identifier]["orientation"]
            longs = oriented > threshold
            mean = float(np.where(longs, returns[common], 0.).mean())
            score = {"alpha_id": identifier, "mean_strategy_return": mean, "longs": int(longs.sum())}
            if score["longs"] >= CONFIG["min_validation_longs"]:
                scores.append(score)
        ranked = sorted(scores, key=lambda row: (-row["mean_strategy_return"], row["alpha_id"]))
        if len(ranked) >= 5:
            top = ranked[:5]
            searches.append({"threshold": threshold, "mean_top5_validation_return": float(np.mean([r["mean_strategy_return"] for r in top])),
                             "ranking": ranked, "selected_ids": [r["alpha_id"] for r in top]})
    if not searches:
        raise ValueError("Không đủ long support cho cấu hình validation đã đăng ký")
    chosen = sorted(searches, key=lambda row: (-row["mean_top5_validation_return"], row["threshold"]))[0]
    payload = {"version": PROFILE, "config": deepcopy(CONFIG), "schedule": deepcopy(schedule), "sources": sources(), "runtime": runtime(),
        "history_origin": dates.iloc[0], "fit_end": dates.iloc[-1], "fit_price_sha256": digest(frame_document(past)),
        "train_dates": dates[masks["train"]].tolist(), "validation_dates": dates[common].tolist(), "purged": purged,
        "candidates": candidates, "validation_search": searches, "threshold": chosen["threshold"],
        "selected": [{"alpha_id": key, "orientation": candidates[key]["orientation"]} for key in chosen["selected_ids"]],
        "scope": "FROZEN_ALPHA_SELECTOR_ONLY_NOT_WHOLE_SYSTEM_CAUSAL_CERTIFICATION"}
    return {"payload": payload, "sha256": digest(payload)}


class FrozenSelector:
    """Tái lập artifact trên train/validation một lần, predict không chọn lại hoặc đọc query-y."""
    def __init__(self, artifact: dict[str, Any], frame: pd.DataFrame) -> None:
        if (type(artifact) is not dict or set(artifact) != {"payload", "sha256"} or type(artifact["payload"]) is not dict
                or type(artifact["payload"].get("schedule")) is not dict or digest(artifact["payload"]) != artifact["sha256"]
                or artifact["payload"].get("version") != PROFILE or artifact["payload"].get("sources") != sources()
                or artifact["payload"].get("runtime") != runtime()
                or artifact != fit_selector(frame, artifact["payload"]["schedule"])):
            raise ValueError("Selector không tái lập từ nguồn train/validation hiện hành")
        self._artifact = deepcopy(artifact)
        self._predictions: dict[str, Any] = {}

    @property
    def sha256(self) -> str:
        """Hash artifact đã xác minh, không phải nhãn tự khai từ snapshot."""
        return self._artifact["sha256"]

    def predict(self, frame: pd.DataFrame, cutoff: str) -> dict[str, Any]:
        """Chỉ nhận prefix đúng nguồn gốc; không cắt/reset origin hoặc nhận dòng sau cutoff."""
        prefix = validated_frame(frame)
        payload = self._artifact["payload"]
        if (prefix.Datetime.dt.strftime("%Y-%m-%d").iloc[-1] != day(cutoff)
                or prefix.Datetime.dt.strftime("%Y-%m-%d").iloc[0] != payload["history_origin"]
                or not payload["schedule"]["test_start"] <= cutoff <= payload["schedule"]["test_end"]):
            raise ValueError("Predict cần đúng prefix origin/cutoff và test window đã khóa")
        fit = prefix.loc[prefix.Datetime < pd.Timestamp(payload["schedule"]["test_start"])]
        if digest(frame_document(fit)) != payload["fit_price_sha256"]:
            raise ValueError("Giá train/validation trong prefix đã đổi")
        history_sha = digest(frame_document(prefix))
        if history_sha in self._predictions:
            return deepcopy(self._predictions[history_sha])
        values = alpha_values(prefix)
        rows = []
        for selected in payload["selected"]:
            value = float(values[selected["alpha_id"]].iloc[-1] * selected["orientation"])
            if not np.isfinite(value):
                raise ValueError("Selected factor không available tại query, không fill zero hoặc đổi ID")
            signal = "TĂNG" if value > payload["threshold"] else "GIẢM" if value < -payload["threshold"] else "TRUNG TÍNH"
            rows.append({"alpha_id": selected["alpha_id"], "value": value, "signal": signal,
                         "available": True, "orientation": selected["orientation"]})
        report = "Alpha causal_common_v1; top5 đóng băng train/validation; LONG/CASH, không bán khống.\n" + "\n".join(
            f"{r['alpha_id']}: {r['value']:+.6f}; {r['signal']}" for r in rows)
        result = {"version": PROFILE, "cutoff": cutoff, "selector_sha256": self.sha256,
                  "history_sha256": history_sha, "factors": rows, "report": report,
                  "scope": "ALPHA_PROFILE_PIT_ONLY; OVERALL_CAUSAL_GATE_PENDING_U06_U07"}
        prediction = {**result, "projection_sha256": digest(result)}
        self._predictions[history_sha] = deepcopy(prediction)
        return prediction
