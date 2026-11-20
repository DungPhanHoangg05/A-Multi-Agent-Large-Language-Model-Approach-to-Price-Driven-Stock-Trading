"""Oracle FIN12 kiểm công thức bằng Decimal và đếm cặp theo fold."""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from math import isclose

import numpy as np
import pandas as pd

from core.unified_analysis.statistics import CONTRASTS, FOLDS, METHODS

FEE = Decimal("0.0025")
SLIP = Decimal("0.001")
VND = Decimal("1000")
CAPITAL = Decimal("50000000")


def decimal(value: float) -> Decimal:
    """Đọc số ở hệ thập phân từ giá nguồn, giữ đơn vị trước phép tính."""
    return Decimal(str(value))


def check_number(observed: float, expected: Decimal | float, name: str) -> None:
    """So sai số nhãn và ledger theo đơn vị thực."""
    if not isclose(observed, float(expected), rel_tol=1e-12, abs_tol=1e-10):
        raise ValueError(f"Oracle FIN12 sai lệch {name}")


def check_outcomes(points: list[dict], outcomes: dict, frames: dict, calendar: pd.DatetimeIndex) -> None:
    """Tính lại nhãn bằng tỷ số tiền bán ròng và giá mua đủ phí, kiểm ngày thực thi."""
    prices = {symbol: frame.set_index("Datetime") for symbol, frame in frames.items()}
    for point in points:
        outcome = outcomes[point["id"]]
        target = outcome["target"]
        if target["net_return"] is None:
            if target["label_net"] is not None:
                raise ValueError("Outcome NA có nhãn giả")
            continue
        index = calendar.get_loc(pd.Timestamp(point["cutoff"]))
        dates = calendar[index:index+4]
        cycle = prices[point["symbol"]].loc[dates]
        entry, exit_ = decimal(cycle.iloc[1].Open)*VND, decimal(cycle.iloc[3].Close)*VND
        net = exit_*(1-SLIP)*(1-FEE)/(entry*(1+SLIP)*(1+FEE))-1
        check_number(target["entry_open"], entry, "giá vào")
        check_number(target["exit_close"], exit_, "giá ra")
        check_number(target["net_return"], net, "nhãn net")
        if (outcome["dates"] != dates.strftime("%Y-%m-%d").tolist()
                or target["label_net"] != ("UP" if net > 0 else "DOWN") or (cycle.iloc[1:].Volume <= 0).any()):
            raise ValueError("Oracle FIN12 không khớp lịch, Volume hoặc dấu nhãn")


def check_account(entries: list[dict], frame: pd.DataFrame, ledger: dict) -> None:
    """Đối chiếu từng dòng tiền, phí, trượt giá, NAV và drawdown trên cả hai chu kỳ."""
    ordered = sorted(entries, key=lambda row: row["date"])
    prices = frame.set_index("Datetime").loc[ordered[0]["date"]:ordered[-1]["exit_date"]]
    dates = prices.index.strftime("%Y-%m-%d").tolist()
    if ledger["dates"] != dates:
        raise ValueError("Ledger FIN12 thiếu phiên NAV")
    nav = dict.fromkeys(dates, CAPITAL)
    cash, end_nav = CAPITAL, [CAPITAL]
    for row, reported in zip(ordered, ledger["cycles"], strict=True):
        first, last = row["entry_date"], row["exit_date"]
        before = cash
        fee = slip = quantity = turnover = Decimal(0)
        if row["action"] == "LONG":
            entry = decimal(prices.loc[first, "Open"])*VND
            exit_ = decimal(prices.loc[last, "Close"])*VND
            quantity = cash/(entry*(1+SLIP)*(1+FEE))
            gross_buy, gross_sell = quantity*entry, quantity*exit_
            fee = (gross_buy*(1+SLIP)+gross_sell*(1-SLIP))*FEE
            slip = (gross_buy+gross_sell)*SLIP
            turnover = gross_buy+gross_sell
            cash = gross_sell*(1-SLIP)*(1-FEE)
            for date in dates[dates.index(first):dates.index(last)]:
                nav[date] = quantity*decimal(prices.loc[date, "Close"])*VND
        nav.update(dict.fromkeys(dates[dates.index(last):], cash))
        end_nav.append(cash)
        for name, value in (("capital_before_vnd", before), ("capital_after_vnd", cash), ("fee_vnd", fee),
                            ("slippage_vnd", slip), ("turnover_vnd", turnover), ("shares", quantity),
                            ("strategy_return", cash/before-1)):
            check_number(reported[name], value, name)
    for index, value in enumerate(nav.values()):
        check_number(ledger["daily_nav_vnd"][index], value, "NAV ngày")
    check_number(ledger["return_pct"], (cash/CAPITAL-1)*100, "lợi nhuận tài khoản")
    for field, series in (("daily_mdd_pct", list(nav.values())), ("cycle_end_mdd_pct", end_nav)):
        peak, maximum = series[0], Decimal(0)
        for value in series:
            peak = max(peak, value)
            maximum = max(maximum, 1-value/peak)
        check_number(ledger[field], maximum*100, field)


def check_contrasts(rows: list[dict], accounts: list[dict], complete_ids: set[str],
                    point_return: np.ndarray, point_ba: np.ndarray, effect: dict) -> dict:
    """Tính lại family từ số đếm fold và ledger, độc lập với tensor chính."""
    by_account = defaultdict(list)
    for account in accounts:
        if account["status"] == "AVAILABLE":
            by_account[(account["fold"], account["symbol"], account["method"])].append(account["return_pct"])
    gains = np.zeros((6, len(METHODS)))
    denom = np.zeros((6, len(METHODS)))
    for (fold, _, method), values in by_account.items():
        if len(values) != 3:
            raise ValueError("Oracle FIN12 thiếu repeat tài khoản")
        cell = (FOLDS.index(fold), METHODS.index(method))
        gains[cell] += sum(values)/3
        denom[cell] += 1
    confusion = np.zeros((6, 3, len(METHODS), 4))
    for row in rows:
        if row["point_id"] in complete_ids:
            label = row["label_net"] == "UP"
            correct = label == (row["final_action"] == "LONG")
            confusion[FOLDS.index(row["fold"]), row["repeat"], METHODS.index(row["method"]),
                      2*int(label)+int(correct)] += 1

    def contrasts(weights: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        returns = (weights@gains)/(weights@denom)
        tallies = (weights@confusion.reshape(6, -1)).reshape(len(weights), 3, len(METHODS), 4)
        fp, tn, fn, tp = np.moveaxis(tallies, -1, 0)
        with np.errstate(divide="ignore", invalid="ignore"):
            ba = 50*(tn/(fp+tn)+tp/(fn+tp)).mean(axis=1)
        left = [METHODS.index(method) for _, method, _ in CONTRASTS]
        right = [METHODS.index(base) for _, _, base in CONTRASTS]
        return returns, ba, np.concatenate((returns[:, left]-returns[:, right], ba[:, left]-ba[:, right]), axis=1)

    returns, ba, point = contrasts(np.ones((1, 6)))
    np.testing.assert_allclose(returns[0], point_return, atol=1e-10, rtol=0)
    np.testing.assert_allclose(ba[0], point_ba, atol=1e-10, rtol=0)
    np.testing.assert_allclose(point[0], effect["point"], atol=1e-10, rtol=0)
    starts = np.random.Generator(np.random.PCG64(20261110)).integers(0, 6, size=(10000, 3))
    weights = np.eye(6)[starts].sum(axis=1)+np.eye(6)[(starts+1)%6].sum(axis=1)
    _, _, draws = contrasts(weights)
    finite = draws[np.isfinite(draws).all(axis=1)]
    if len(finite) != effect["joint_finite_draws"]:
        raise ValueError("Oracle FIN12 sai số draw joint finite")
    if effect["ci95"] is not None:
        sd = finite.std(axis=0, ddof=1)
        critical = np.quantile(np.max(np.abs(finite-point[0])/sd, axis=1), .95, method="higher")
        np.testing.assert_allclose(np.column_stack((point[0]-critical*sd, point[0]+critical*sd)),
                                   effect["ci95"], atol=1e-10, rtol=0)
    return {"status": "PASS", "labels": len({r["point_id"] for r in rows if r["r_net"] is not None}),
            "accounts": sum(len(values) for values in by_account.values()), "contrasts": len(point[0]),
            "bootstrap_draws": len(draws), "joint_finite_draws": len(finite)}
