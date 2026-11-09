"""Metrics pilot48: tám account, bootstrap circular theo ngày, không annualize mẫu thưa."""

from __future__ import annotations

from typing import Any
import numpy as np
import pandas as pd

SEED = 20261109
DRAWS = 10000
MIN_FINITE = 9500


def classification(prediction: Any, truth: Any, *, planned: int | None = None) -> dict:
    """Pooled confusion, F1 lớp UP/net>0; undefined giữ null thay vì ép zero."""
    p, y = np.asarray(prediction), np.asarray(truth)
    if p.shape != y.shape or p.ndim != 1 or not np.isin(p, [0, 1]).all() or not np.isin(y, [0, 1]).all():
        raise ValueError("Prediction/truth phải là hai vector binary cùng chiều")
    p, y = p.astype(bool), y.astype(bool)
    tp, tn = int(np.sum(p & y)), int(np.sum(~p & ~y))
    fp, fn = int(np.sum(p & ~y)), int(np.sum(~p & y))
    n, positive, negative = len(y), tp + fn, tn + fp
    denominator = float(np.sqrt(float((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))))
    values = {"accuracy": (tp+tn)/n if n else None,
              "balanced_accuracy": .5*(tp/positive+tn/negative) if positive and negative else None,
              "mcc": (tp*tn-fp*fn)/denominator if denominator else None,
              "f1_positive": 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None}
    return {"n_planned": n if planned is None else int(planned), "n_complete": n,
            "n_defined": {k: n if v is not None else 0 for k, v in values.items()},
            "confusion_matrix": [[tn, fp], [fn, tp]], "support_up": positive, "support_down": negative, **values}


def cycle_ratios(returns: Any) -> dict:
    """Sharpe chu kỳ dùng sample SD; Sortino dùng LPM2 toàn chu kỳ, target0, không scale252."""
    r = np.asarray(returns, dtype=float)
    if r.ndim != 1 or not np.isfinite(r).all():
        raise ValueError("Return chu kỳ phải hữu hạn")
    sd = float(np.std(r, ddof=1)) if len(r) > 1 else 0.
    downside = float(np.sqrt(np.mean(np.minimum(r, 0.)**2))) if len(r) else 0.
    mean = float(np.mean(r)) if len(r) else 0.
    return {"cycle_sharpe": mean/sd if sd > 0 else None, "cycle_sortino_lpm2": mean/downside if downside > 0 else None,
            "annualized_sharpe": None, "annualized_sortino": None, "annualized_return": None}


def drawdown(nav: Any) -> float:
    """MDD dương theo NAV, có vốn ban đầu để không bỏ qua drawdown giao dịch đầu."""
    a = np.asarray(nav, dtype=float)
    if a.ndim != 1 or not len(a) or not np.isfinite(a).all() or np.any(a <= 0):
        raise ValueError("NAV phải là vector dương hữu hạn")
    return float(np.max(1. - a / np.maximum.accumulate(a)) * 100.)


def account(cycles: list[dict], frame: pd.DataFrame, *, capital: float = 50_000_000.) -> dict:
    """All-in fractional LONG, EOD mark-to-market, CASH giữa query; phí đúng hàm engine."""
    from core.backtest_engine import compute_round_trip_net_return
    if not cycles or capital <= 0:
        raise ValueError("Account cần cycle và vốn dương")
    cycles = sorted(cycles, key=lambda r: r["date"])
    days = pd.DatetimeIndex(frame["Datetime"])
    if not days.is_monotonic_increasing or not days.is_unique:
        raise ValueError("Lịch giá account phải duy nhất/tăng dần")
    close = frame["Close"].to_numpy(dtype=float)
    opens = frame["Open"].to_numpy(dtype=float)
    first, last = days.get_indexer(pd.to_datetime([cycles[0]["date"], cycles[-1]["exit_date"]]))
    if first < 0 or last < 0:
        raise ValueError("Account thiếu phiên lịch")
    nav = np.full(last-first+1, np.nan); nav[0] = capital
    held = np.zeros(len(nav), dtype=bool)
    cash, previous_exit = float(capital), first
    fees = slippage = turnover = 0.
    records, returns, end_nav = [], [], [cash]
    for row in cycles:
        query, entry, exit_ = days.get_indexer(pd.to_datetime([row["date"], row["entry_date"], row["exit_date"]]))
        if query < first or entry != query+1 or exit_ != query+3 or entry <= previous_exit:
            raise ValueError("Cycle phải T+2.5 và không chồng lấn")
        nav[previous_exit-first:entry-first] = cash
        net = float(compute_round_trip_net_return(opens[entry], close[exit_]))
        if not np.isclose(net, row["r_net"], rtol=0, atol=1e-12):
            raise ValueError("Return account khác nhãn engine")
        if row["action"] not in ("LONG", "CASH"):
            raise ValueError("Không được bán khống hoặc gán invalid thành CASH")
        before, quantity, cost_fee, cost_slip, traded = cash, 0., 0., 0., 0.
        if row["action"] == "LONG":
            entry_vnd, exit_vnd = float(opens[entry]*1000.), float(close[exit_]*1000.)
            buy_notional = cash / 1.0025
            quantity = buy_notional / (entry_vnd*1.001)
            sell_notional = quantity*exit_vnd*.999
            cost_fee = buy_notional*.0025 + sell_notional*.0025
            cost_slip = quantity*entry_vnd*.001 + quantity*exit_vnd*.001
            traded = quantity*(entry_vnd+exit_vnd)
            nav[entry-first:exit_-first+1] = quantity*close[entry:exit_+1]*1000.
            held[entry-first:exit_-first+1] = True
            cash = sell_notional*.9975
            if not np.isclose(cash/before-1., net, rtol=0, atol=1e-12):
                raise ValueError("Ledger tiền khác công thức engine")
        else:
            nav[entry-first:exit_-first+1] = cash
        nav[exit_-first] = cash
        previous_exit = exit_
        fees += cost_fee; slippage += cost_slip; turnover += traded
        period = cash/before-1.
        returns.append(float(period)); end_nav.append(cash)
        records.append({**row, "capital_before_vnd": before, "capital_after_vnd": cash,
                        "shares": float(quantity), "fee_vnd": cost_fee, "slippage_vnd": cost_slip,
                        "turnover_vnd": traded, "strategy_return": float(period)})
    if not np.isfinite(nav).all():
        raise ValueError("NAV có khoảng lịch chưa được hạch toán")
    return {"return_pct": (cash/capital-1.)*100., "initial_vnd": capital, "final_vnd": cash,
            "daily_mdd_pct": drawdown(nav), "cycle_end_mdd_pct": drawdown(end_nav),
            "fee_vnd": fees, "slippage_vnd": slippage, "turnover_vnd": turnover,
            "turnover_over_initial": turnover/capital, "long_count": sum(r["action"]=="LONG" for r in cycles),
            "sessions": len(nav), "held_sessions": int(held.sum()), "cash_sessions": int((~held).sum()),
            "held_session_fraction": float(held.mean()), "cash_between_queries": True,
            "dates": days[first:last+1].strftime("%Y-%m-%d").tolist(), "daily_nav_vnd": nav.tolist(),
            "cycles": records, **cycle_ratios(returns)}


def selected_date_indices() -> np.ndarray:
    """10k draw, hai năm độc lập, ba block circular L2/năm, chung cho mọi mã/method."""
    starts = np.random.Generator(np.random.PCG64(SEED)).integers(0, 6, size=(DRAWS, 2, 3))
    return ((starts[..., None]+np.arange(2)) % 6).reshape(DRAWS, 2, 6)


def estimates(actions: Any, net_returns: Any, truth: Any, indices: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Tái dựng tám account mỗi draw và pooled BA; không gộp account thành portfolio."""
    a, r, y = np.asarray(actions), np.asarray(net_returns, dtype=float), np.asarray(truth)
    if (a.shape != (2, 6, 4, 6) or r.shape != (2, 6, 4) or y.shape != r.shape
            or not np.isin(a, [0, 1]).all() or not np.isin(y, [0, 1]).all()
            or not np.isfinite(r).all() or np.any(r <= -1) or not np.array_equal(y, r>0)):
        raise ValueError("Tensor pilot không đủ2 năm×6 ngày×4 mã×6 method hoặc nhãn lệch engine")
    idx = np.asarray(indices)
    if idx.ndim != 3 or idx.shape[1:] != (2, 6) or not np.issubdtype(idx.dtype, np.integer) or np.any((idx<0)|(idx>5)):
        raise ValueError("Indices bootstrap phải giữ sáu selected date trong từng năm")
    year = np.arange(2)[None, :, None]
    ap = a[year, idx].astype(bool)
    rp, yp = r[year, idx], y[year, idx].astype(bool)
    accounts = np.prod(1.+np.where(ap, rp[..., None], 0.), axis=2)-1.
    macro_return = accounts.mean(axis=(1, 2))*100.
    p = yp.sum(axis=(1, 2, 3))[:, None]
    n = (~yp).sum(axis=(1, 2, 3))[:, None]
    tp = (ap & yp[..., None]).sum(axis=(1, 2, 3))
    tn = (~ap & ~yp[..., None]).sum(axis=(1, 2, 3))
    with np.errstate(divide="ignore", invalid="ignore"):
        ba = .5*(tp/p+tn/n)*100.
    return macro_return[:, 1:]-macro_return[:, :1], ba[:, 1:]-ba[:, :1]


def family_interval(point: Any, draws: Any, *, metric: str) -> dict:
    """Centered max-deviation95% cho đủ năm contrast; không sinh bù draw mất class."""
    p, d = np.asarray(point, dtype=float), np.asarray(draws, dtype=float)
    if p.shape != (5,) or d.shape != (DRAWS, 5):
        raise ValueError("Family phải đủ năm contrast/10.000 draw đã khóa")
    finite = np.isfinite(d).all(axis=1)
    count = int(finite.sum())
    result = {"metric": metric, "point": [float(x) if np.isfinite(x) else None for x in p],
              "draws": DRAWS, "joint_finite_draws": count, "lost_class_or_nonfinite_draws": DRAWS-count,
              "seed": SEED, "block_length": 2, "min_joint_finite": MIN_FINITE,
              "interpretation": "SMALL_SAMPLE_CONDITIONAL_SENSITIVITY_NOT_SUPERIORITY", "ci": None, "half_width": None}
    if count < MIN_FINITE or not np.isfinite(p).all():
        return {**result, "status": "INCONCLUSIVE_UNDEFINED_SUPPORT"}
    width = float(np.quantile(np.max(np.abs(d[finite]-p), axis=1), .95, method="linear"))
    return {**result, "status": "DESCRIPTIVE_ONLY", "half_width": width,
            "ci": [[float(x-width), float(x+width)] for x in p]}


def bootstrap(actions: Any, net_returns: Any, truth: Any) -> dict:
    """Cùng draw indices cho hai family return/BA; tái dựng point trên lịch gốc."""
    original = np.broadcast_to(np.arange(6), (1, 2, 6)).copy()
    point_return, point_ba = estimates(actions, net_returns, truth, original)
    indices = selected_date_indices()
    returned, ba = estimates(actions, net_returns, truth, indices)
    import hashlib
    return {"index_sha256": hashlib.sha256(indices.astype("<i8").tobytes()).hexdigest(),
            "return": family_interval(point_return[0], returned, metric="macro_account_return_pp"),
            "balanced_accuracy": family_interval(point_ba[0], ba, metric="pooled_balanced_accuracy_pp")}
