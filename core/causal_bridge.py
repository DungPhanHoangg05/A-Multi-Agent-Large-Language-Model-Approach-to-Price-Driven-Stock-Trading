"""Bridge cùng upstream: native nguyên vẹn, mọi nhánh common dùng cùng causal alpha."""
from __future__ import annotations

from copy import deepcopy
import math
from pathlib import Path
from typing import Any

import pandas as pd

from core.bayesian_memory import read_json
from core.causal_alpha import PROFILE, FrozenSelector, frame_document
from core.decision_profiles import NATIVE_PROFILE
from core.unified_contracts import SharedSnapshot, checksum, digest

REPAIRED_NATIVE_PROFILE = "original_fix_causal_serving_v1"


def validate_embedded(document: dict[str, Any]) -> None:
    """Shape/hash projection chỉ là integrity; runner còn tái tính từ selector/giá đã khóa."""
    payload = document["payload"]
    block = payload["causal_alpha"]
    if type(block) is not dict or set(block) != {"projection", "native_shared_sha256"}:
        raise ValueError("Bridge causal sai fields")
    projection = block["projection"]
    keys = {"version", "cutoff", "selector_sha256", "history_sha256", "factors", "report", "scope", "projection_sha256"}
    if (type(projection) is not dict or set(projection) != keys or projection["version"] != PROFILE or projection["cutoff"] != document["point"]["cutoff"]
            or not all(checksum(projection[key]) for key in ("selector_sha256", "history_sha256", "projection_sha256"))
            or projection["projection_sha256"] != digest({k: v for k, v in projection.items() if k != "projection_sha256"})):
        raise ValueError("Projection causal không đúng point/hash")
    rows = projection["factors"]
    row_keys = {"alpha_id", "value", "signal", "available", "orientation"}
    if (type(rows) is not list or len(rows) != 5 or any(type(row) is not dict or set(row) != row_keys for row in rows)
            or any(type(row["alpha_id"]) is not str for row in rows) or len({r["alpha_id"] for r in rows}) != 5):
        raise ValueError("Causal projection cần đúng năm factor khác nhau")
    for row in rows:
        if (set(row) != {"alpha_id", "value", "signal", "available", "orientation"}
                or type(row["value"]) not in (int, float) or not math.isfinite(row["value"]) or abs(row["value"]) > 1
                or row["available"] is not True or type(row["orientation"]) is not int or row["orientation"] not in (-1, 1)
                or row["signal"] not in ("TĂNG", "GIẢM", "TRUNG TÍNH")):
            raise ValueError("Factor causal sai kiểu/availability")
    base = deepcopy(document)
    base["version"] = "shared_snapshot_v1"
    base["payload"].pop("causal_alpha")
    if block["native_shared_sha256"] != digest(base):
        raise ValueError("Causal bridge không bind đúng native parent")


def decision_payload(snapshot: SharedSnapshot, variant: str, *, decision_profile: str | None = None) -> dict[str, Any]:
    """Native sửa phải chọn tường minh; mặc định giữ projection lịch sử nguyên vẹn."""
    if decision_profile is not None and (variant != "original_fix"
            or decision_profile not in (NATIVE_PROFILE, REPAIRED_NATIVE_PROFILE)):
        raise ValueError("Profile bridge không thuộc Native lịch sử hoặc Native causal đã khóa")
    repaired_native = decision_profile == REPAIRED_NATIVE_PROFILE
    shared = snapshot.document()["payload"]
    block = shared.pop("causal_alpha", None)
    if repaired_native and block is None:
        raise ValueError("Native causal cần snapshot đã bind selector và projection causal")
    if block is not None and (variant != "original_fix" or repaired_native):
        shared["alpha_report"] = block["projection"]["report"]
        shared["alpha_factors"] = block["projection"]["factors"]
    return shared


class CausalSources:
    """Nạp một selector đã replay fit mỗi mã/fold; không nạp student/HMM hoặc gọi mạng."""
    def __init__(self, spec: dict[str, Any], root: Path) -> None:
        self.entries: dict[str, Any] = {}
        for key, paths in spec["causal_sources"].items():
            price_path = root / paths["prices"]
            if price_path.suffix == ".csv":
                frame = pd.read_csv(price_path)
            elif price_path.suffix == ".json":
                frame = pd.DataFrame(read_json(price_path))
            else:
                raise ValueError("Nguồn giá causal chỉ nhận CSV/JSON OHLCV đã khóa")
            frame["Datetime"] = pd.to_datetime(frame.Datetime)
            artifact = read_json(root / paths["selector"])
            selector = FrozenSelector(artifact, frame)
            self.entries[key] = (selector, frame, spec["source_hashes"][paths["prices"]])

    def bind(self, snapshot: SharedSnapshot) -> SharedSnapshot:
        """Dựng lại projection từ giá PIT, không tin cờ causal hoặc metadata caller tự ký."""
        doc = snapshot.document()
        point = doc["point"]
        selector, frame, price_sha = self.entries[point["symbol"] + "/" + point["fold"]]
        prefix = frame.loc[frame.Datetime <= pd.Timestamp(point["cutoff"])].copy()
        return bind_snapshot(snapshot, selector, prefix, price_sha)


def bind_snapshot(snapshot: SharedSnapshot, selector: FrozenSelector, prefix: pd.DataFrame, price_sha: str) -> SharedSnapshot:
    """Một primitive bridge dùng chung cho runner, CLI và consumer."""
    doc = snapshot.document()
    point = doc["point"]
    payload = deepcopy(doc["payload"])
    old = payload.pop("causal_alpha", None)
    if (doc["provenance"]["source_sha256"] != price_sha or len(prefix) < 600
            or payload.get("price_prefix") != frame_document(prefix.tail(600))):
        raise ValueError("Native/causal bridge không dùng cùng giá prefix 600 bars đã khóa")
    base = SharedSnapshot.create(point, doc["realization"], payload, doc["provenance"])
    projection = selector.predict(prefix, point["cutoff"])
    block = {"projection": projection, "native_shared_sha256": base.sha256}
    if old is not None and old != block:
        raise ValueError("Projection causal caller cung cấp khác phép tái tính")
    payload["causal_alpha"] = block
    return SharedSnapshot.create(point, doc["realization"], payload, doc["provenance"])


def causal_sources(spec: dict[str, Any], root: Path) -> CausalSources | None:
    """V1 native/common cũ không mở selector hoặc giá nhân quả vô ích."""
    return CausalSources(spec, root) if spec.get("input_profile") == PROFILE else None
