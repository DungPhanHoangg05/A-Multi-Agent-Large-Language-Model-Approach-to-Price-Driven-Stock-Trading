"""Fit selector trên giá thô, giữ rào thực thi và lịch FIN02."""
from __future__ import annotations

from functools import partial
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from core.backtest_engine import compute_round_trip_net_return
from core.causal_alpha import CONFIG, alpha_values, frame_document, runtime, validate_schedule, validated_frame
from core.execution_prices import corporate_action_barriers
from core.unified_contracts import digest

VERSION = "causal_common_raw_execution_v1"


def cycle_masks(frame: pd.DataFrame, events: list[dict], schedule: dict[str, str],
                reserved: frozenset[str]) -> tuple[dict[str, np.ndarray], dict[str, dict[str, list[str]]]]:
    """Giữ cadence, loại trước oracle nếu exit chưa đóng, đã reserve, có quyền hoặc thiếu khớp."""
    dates = frame.Datetime.dt.strftime("%Y-%m-%d")
    sessions = frame.Datetime.to_numpy()
    barriers = corporate_action_barriers(frame, events).to_numpy()
    volume = frame.Volume.to_numpy()
    masks, exclusions = {}, {}
    for split, next_split in (("train", "validation"), ("validation", "test")):
        start, end = schedule[split + "_start"], schedule[split + "_end"]
        if start not in set(dates) or end not in set(dates):
            raise ValueError("Ranh giới selector vắng trong lịch giá thô")
        grid = np.flatnonzero(dates.between(start, end))[::CONFIG["cycle_step"]]
        mature = grid[(dates.shift(-3).iloc[grid] < schedule[next_split + "_start"]).to_numpy()]
        reserved_mask = dates.iloc[mature].isin(reserved).to_numpy()
        rights = np.searchsorted(barriers, sessions[mature + 3], side="right") > np.searchsorted(
            barriers, sessions[mature + 1], side="right")
        no_volume = (volume[mature[:, None] + np.arange(1, 4)] <= 0).any(axis=1)
        accepted = mature[~(reserved_mask | rights | no_volume)]
        mask = np.zeros(len(frame), dtype=bool)
        mask[accepted] = True
        masks[split] = mask
        exclusions[split] = {"split_boundary": dates.iloc[np.setdiff1d(grid, mature)].tolist(),
                             "reserved": dates.iloc[mature[reserved_mask]].tolist(),
                             "rights": dates.iloc[mature[rights]].tolist(),
                             "no_volume": dates.iloc[mature[no_volume]].tolist()}
    return masks, exclusions


def fit_raw_selector(frame: pd.DataFrame, events: list[dict], schedule: dict[str, str],
                     reserved: frozenset[str]) -> dict[str, Any]:
    """Dùng công thức Alpha hiện hữu, orientation train và top5/threshold trên validation."""
    validate_schedule(schedule)
    raw = frame.loc[pd.to_datetime(frame.Datetime) < pd.Timestamp(schedule["test_start"])].reset_index(drop=True)
    past = validated_frame(raw)
    masks, exclusions = cycle_masks(raw, events, schedule, reserved)
    eligible_indices = np.flatnonzero(masks["train"] | masks["validation"])
    returns = np.full(len(past), np.nan)
    oracle = np.frompyfunc(partial(compute_round_trip_net_return, fee=CONFIG["fee"], slippage=CONFIG["slippage"]), 2, 1)
    returns[eligible_indices] = oracle(past.Open.to_numpy()[eligible_indices + 1],
                                       past.Close.to_numpy()[eligible_indices + 3]).astype(float)
    factors = alpha_values(past)
    candidates, oriented = {}, {}
    for name in factors:
        values = factors[name].to_numpy()
        train = masks["train"] & np.isfinite(values)
        count = int(train.sum())
        ic = None
        if count >= CONFIG["min_train"] and np.std(values[train]) > 1e-12 and np.std(returns[train]) > 1e-12:
            correlation = float(spearmanr(values[train], returns[train]).statistic)
            if np.isfinite(correlation):
                ic = correlation
        orientation = None if ic is None else (1 if ic >= 0 else -1)
        candidates[name] = {"train_n": count, "train_ic": ic, "orientation": orientation}
        if orientation is not None:
            oriented[name] = values * orientation
    if len(oriented) < CONFIG["top_n"]:
        raise ValueError("Selector giá thô thiếu candidate đủ train support")
    common = masks["validation"] & np.isfinite(np.column_stack(list(oriented.values()))).all(axis=1)
    if common.sum() < CONFIG["min_validation"]:
        raise ValueError("Selector giá thô thiếu validation support sau rào thực thi")
    search = []
    for threshold in CONFIG["thresholds"]:
        ranking = []
        for name, values in oriented.items():
            longs = values[common] > threshold
            if longs.sum() >= CONFIG["min_validation_longs"]:
                ranking.append({"alpha_id": name, "longs": int(longs.sum()),
                                "mean_strategy_return": float(np.where(longs, returns[common], 0.).mean())})
        ranking.sort(key=lambda row: (-row["mean_strategy_return"], row["alpha_id"]))
        if len(ranking) >= CONFIG["top_n"]:
            best = ranking[:CONFIG["top_n"]]
            search.append({"threshold": threshold, "ranking": ranking,
                           "mean_top": float(np.mean([row["mean_strategy_return"] for row in best]))})
    if not search:
        raise ValueError("Selector giá thô thiếu LONG support")
    choice = min(search, key=lambda row: (-row["mean_top"], row["threshold"]))
    dates = past.Datetime.dt.strftime("%Y-%m-%d")
    result = {"version": VERSION, "config": CONFIG.copy(), "schedule": schedule.copy(), "runtime": runtime(),
              "history_origin": dates.iloc[0], "fit_end": dates.iloc[-1],
              "fit_price_sha256": digest(frame_document(past)), "exclusions": exclusions,
              "train_dates": dates[masks["train"]].tolist(), "validation_dates": dates[common].tolist(),
              "threshold": choice["threshold"], "validation_search": search, "candidates": candidates,
              "selected": [{"alpha_id": row["alpha_id"], "orientation": candidates[row["alpha_id"]]["orientation"]}
                           for row in choice["ranking"][:CONFIG["top_n"]]]}
    return {"payload": result, "sha256": digest(result)}
