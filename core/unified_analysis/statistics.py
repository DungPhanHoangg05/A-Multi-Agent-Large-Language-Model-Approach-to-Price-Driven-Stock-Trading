"""Ước lượng paired và max-standardized band đúng protocol U06 v2 đã khóa."""
from __future__ import annotations

import hashlib
from typing import Any

import numpy as np

VARIANTS = ("original_fix", "original_common", "bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL", "Fact_Anchor")
METHODS = (*VARIANTS, "CASH_EVERY_CYCLE", "ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS")
FOLDS = ("b2023_h2", "b2024_h2", "b2025_h1", "f2025_q4", "f2026_q2", "f2026_q3")
EXTENSIONS = VARIANTS[2:7]
CONTRASTS = [(family, method, baseline) for family, baseline in (("system", "original_fix"), ("method", "original_common")) for method in EXTENSIONS]
ENDPOINTS = ("account_return_percentage_points", "balanced_accuracy_percentage_points")


def plain(value: Any) -> Any:
    """Đổi NumPy thành JSON nguyên bản; giữ null cho mọi giá trị không xác định."""
    if isinstance(value, dict): return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [plain(v) for v in value]
    if isinstance(value, np.ndarray): return plain(value.tolist())
    if isinstance(value, np.generic): return plain(value.item())
    if isinstance(value, float) and not np.isfinite(value): return None
    return value


def indices(length: int = 2) -> np.ndarray:
    """PCG64/seed khóa; circular block chung qua mọi mã, method và repeat."""
    if type(length) is not int or length not in (1, 2, 3):
        raise ValueError("Sensitivity chỉ có block length 1, 2 hoặc 3")
    starts = np.random.Generator(np.random.PCG64(20261110)).integers(0, 6, size=(10000, 6 // length))
    return ((starts[..., None] + np.arange(length)) % 6).reshape(10000, 6)


def estimates(actions: np.ndarray, returns: np.ndarray, valid: np.ndarray,
              draws: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Hai cycle/account, mean repeat trước mean account; BA pooled riêng mỗi repeat."""
    a, r, mask = np.asarray(actions), np.asarray(returns, dtype=float), np.asarray(valid)
    if (a.ndim != 5 or a.shape[0] != 6 or a.shape[2:] != (2, 3, len(METHODS))
            or r.shape != a.shape[:3] or mask.shape != r.shape or mask.dtype != bool
            or not np.isin(a, (0, 1)).all() or not np.isfinite(r).all() or np.any(r <= -1)
            or not np.array_equal(mask[:, :, 0], mask[:, :, 1])):
        raise ValueError("Tensor phải đủ sáu fold, hai cycle, ba repeat và 10 method; không thiếu nửa account")
    idx = np.arange(6)[None, :] if draws is None else np.asarray(draws)
    if (idx.ndim != 2 or idx.shape[1] < 1 or not np.issubdtype(idx.dtype, np.integer)
            or np.any((idx < 0) | (idx > 5))):
        raise ValueError("Fold indices ngoài lịch đã khóa")
    support = mask[:, :, 0]
    account_return = np.prod(1. + np.where(a.astype(bool), r[..., None, None], 0.), axis=2) - 1.
    account_mean = account_return.mean(axis=2)
    weights = support[idx]
    denominator = weights.sum(axis=(1, 2))
    if np.any(denominator == 0): raise ValueError("Không có account hoàn chỉnh")
    mean_return = (account_mean[idx] * weights[..., None]).sum(axis=(1, 2)) / denominator[:, None] * 100.
    # Fold được lấy lặp là bản sao account reset độc lập, không compound hai fold.
    ap, yp, mp = a[idx].astype(bool), (r[idx] > 0), mask[idx]
    positive = (yp & mp).sum(axis=(1, 2, 3))
    negative = (~yp & mp).sum(axis=(1, 2, 3))
    tp = (ap & (yp & mp)[..., None, None]).sum(axis=(1, 2, 3))
    tn = (~ap & (~yp & mp)[..., None, None]).sum(axis=(1, 2, 3))
    with np.errstate(divide="ignore", invalid="ignore"):
        ba = (.5 * (tp / positive[:, None, None] + tn / negative[:, None, None])).mean(axis=1) * 100.
    return mean_return, ba


def effects(returned: np.ndarray, ba: np.ndarray) -> np.ndarray:
    """Thứ tự 10 contrast return rồi 10 contrast BA trong cùng một family 20 chiều."""
    left = [METHODS.index(method) for _, method, _ in CONTRASTS]
    right = [METHODS.index(base) for _, _, base in CONTRASTS]
    return np.concatenate((returned[:, left] - returned[:, right], ba[:, left] - ba[:, right]), axis=1)


def bands(point: np.ndarray, draws: np.ndarray) -> dict[str, Any]:
    """Không redraw; chỉ mở cả family khi đủ joint finite và mọi SD khác zero."""
    p, d = np.asarray(point, float), np.asarray(draws, float)
    if p.shape != (20,) or d.shape != (10000, 20): raise ValueError("Phải đủ 20 endpoint/contrast và 10.000 draw")
    finite = np.isfinite(d).all(axis=1)
    n = int(finite.sum())
    sd = np.std(d[finite], axis=0, ddof=1) if n > 1 else np.full(20, np.nan)
    zero = np.flatnonzero(sd == 0.).tolist()
    result = {"joint_family_size": 20, "draws": 10000, "joint_finite_draws": n,
        "undefined_draws": 10000 - n, "minimum_joint_finite": 9500, "point": p,
        "bootstrap_sd_ddof1": sd, "zero_sd_columns": zero, "ci95": None, "critical_value": None,
        "scope": "EXPLORATORY_SENSITIVITY_NO_SUPERIORITY_OR_CONFIRMATORY_P_VALUE"}
    reasons = []
    if n < 9500: reasons.append("INSUFFICIENT_JOINT_FINITE_DRAWS")
    if not np.isfinite(p).all(): reasons.append("UNDEFINED_POINT_ESTIMATE")
    if zero: reasons.append("ZERO_SD_IN_JOINT_FAMILY")
    if not np.isfinite(sd).all(): reasons.append("UNDEFINED_BOOTSTRAP_SD")
    if reasons: return plain({**result, "status": "NULL_SIMULTANEOUS_BANDS", "reasons": reasons})
    maximum = np.max(np.abs(d[finite] - p) / sd, axis=1)
    critical = float(np.quantile(maximum, .95, method="higher"))
    return plain({**result, "status": "DESCRIPTIVE_BANDS", "reasons": [], "critical_value": critical,
        "ci95": np.column_stack((p - critical * sd, p + critical * sd))})


def bootstrap(actions: np.ndarray, returns: np.ndarray, valid: np.ndarray, length: int = 2) -> dict[str, Any]:
    """Tái dựng primary và sensitivity trên cùng indices, không tách family đẹp hơn."""
    sampled = indices(length)
    point = effects(*estimates(actions, returns, valid))[0]
    draws = effects(*estimates(actions, returns, valid, sampled))
    return {"block_length": length, "seed": 20261110, "rng": "PCG64",
        "index_sha256": hashlib.sha256(sampled.astype("<i8").tobytes()).hexdigest(), **bands(point, draws)}
