"""Giá và lịch xác định cho kiểm thử tính nhân quả của selector."""
from __future__ import annotations

import numpy as np
import pandas as pd


def synthetic_frame(n: int = 96) -> pd.DataFrame:
    """Chuỗi xác định có xu hướng/dao động, không phải OHLCV thực nghiệm."""
    t = np.arange(n, dtype=float)
    close = 100 + .03 * t + 2 * np.sin(t / 4.1) + .7 * np.cos(t / 9)
    return pd.DataFrame({"Datetime": pd.bdate_range("2020-01-01", periods=n),
                         "date": pd.bdate_range("2020-01-01", periods=n).strftime("%Y-%m-%d"),
                         "Open": close - .4 + .2 * np.cos(t / 3), "High": close + 1 + .2 * np.sin(t / 5),
                         "Low": close - 1.1, "Close": close, "Volume": 1000 + 30 * (t % 17) + 40 * np.cos(t / 7)})


def source_frame() -> pd.DataFrame:
    """1300 phiên đủ train/validation/test và 600 nến raw bridge."""
    return synthetic_frame(1300).drop(columns="date")


def schedule(frame: pd.DataFrame) -> dict[str, str]:
    """Hai boundary sát nhau để kiểm purge horizon chứ không chỉ train_end < query."""
    names = ("train_start", "train_end", "validation_start", "validation_end", "test_start", "test_end")
    return dict(zip(names, (str(frame.Datetime.iloc[i].date()) for i in (350, 750, 751, 1000, 1001, 1299))))
