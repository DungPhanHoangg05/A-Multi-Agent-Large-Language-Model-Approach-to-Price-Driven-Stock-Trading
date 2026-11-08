"""Oracle CI đồng thời cho năm contrast CORE4; chưa đọc kết quả giao dịch mới."""

from __future__ import annotations

from typing import Any
import numpy as np


def primary_interval(values: Any, *, metric: str = "return") -> dict[str, Any]:
    """Nhận block×mã×repeat×contrast, đơn vị đpt; null giữ nguyên cả family."""
    if metric not in ("return", "balanced_accuracy"):
        raise ValueError("Chỉ nhận family return hoặc balanced accuracy riêng")
    array = np.asarray(values, dtype=object)
    if array.shape != (6, 4, 3, 5):
        raise ValueError("Family primary phải đủ6 block/4 mã/3 repeat/5 contrast")
    if any(x is not None and (type(x) not in (int, float) or not np.isfinite(x)) for x in array.flat):
        raise ValueError("Contrast phải là số hữu hạn Python gốc hoặc null")
    if any(x is None for x in array.flat):
        return {"status": "INCONCLUSIVE_UNDEFINED_SUPPORT", "point": None, "ci": None, "draws": 0}
    blocks = np.asarray(array, dtype=float).mean(axis=(1, 2))
    point = blocks.mean(axis=0)
    indices = np.random.Generator(np.random.PCG64(20261107)).integers(0, 6, size=(10000, 6))
    replicate = blocks[indices].mean(axis=1)
    maximum = np.max(np.abs(replicate - point), axis=1)
    width = float(np.quantile(maximum, .95, method="linear"))
    return {"status": "PASS" if width <= (1. if metric == "return" else 3.) else "LOW_PRECISION",
            "metric": metric,
            "point": [float(v) for v in point],
            "ci": [[float(v - width), float(v + width)] for v in point],
            "half_width": width, "draws": 10000, "seed": 20261107,
            "interpretation": "HISTORICAL_DEPENDENT_BLOCK_SENSITIVITY"}
