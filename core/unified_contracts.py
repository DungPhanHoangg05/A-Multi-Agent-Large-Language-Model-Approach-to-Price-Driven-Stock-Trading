"""Spec và shared snapshot bất biến; outcome ở kho riêng sau forecast barrier."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
import json
import math
from pathlib import PurePosixPath
import re
from typing import Any

from core.variant_registry import execution_order, get_variant, registry_document

VERSION = "unified_experiment_v1"
REPORTS = tuple(name + "_report" for name in ("indicator", "pattern", "trend", "alpha", "sentiment"))
FORBIDDEN = frozenset(("outcome", "evaluation", "supervised_target", "query_y", "actual_direction",
    "actual_pct_change", "entry_open", "exit_close", "net_return", "net_return_pct", "label_net", "label_gross",
    "target", "future", "final_trade_decision", "decision_prompt", "prior_config", "bayesian_prior_context",
    "strategy_return", "label_contract_version", "entry_date", "exit_date", "gross_return", "r_net", "y"))


def json_bytes(value: Any) -> bytes:
    """Chỉ nhận kiểu JSON nguyên bản, hữu hạn; không ép kiểu NumPy âm thầm."""
    def check(item: Any) -> None:
        if type(item) is dict:
            if any(type(key) is not str for key in item):
                raise ValueError("Khóa JSON phải là str")
            for child in item.values():
                check(child)
        elif type(item) is list:
            for child in item:
                check(child)
        elif item is not None and type(item) not in (str, int, float, bool):
            raise ValueError("Không chấp nhận kiểu ngoài JSON nguyên bản")
    check(value)
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (ValueError, TypeError) as error:
        raise ValueError("JSON phải hữu hạn và serialize được") from error


def digest(value: Any) -> str:
    """Hash ngữ nghĩa của hợp đồng mới, không thay digest receipt cũ."""
    return hashlib.sha256(json_bytes(value)).hexdigest()


def checksum(value: Any) -> bool:
    """Nhận diện SHA256 đầy đủ, không chấp nhận prefix."""
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def day(value: str) -> str:
    """Chỉ ngày ISO, không đoán timezone hay giờ availability."""
    if type(value) is not str or date.fromisoformat(value).isoformat() != value:
        raise ValueError("Ngày phải có dạng YYYY-MM-DD")
    return value


def forecast_only(value: Any) -> None:
    """Rào query-y đệ quy trên shared payload, không áp lên historical prior tasks."""
    if type(value) is dict:
        if FORBIDDEN.intersection(value):
            raise ValueError("Shared snapshot chứa outcome/prior/Decision query")
        for child in value.values():
            forecast_only(child)
    elif type(value) is list:
        for child in value:
            forecast_only(child)


@dataclass(frozen=True)
class SharedSnapshot:
    """Bytes bất biến; mỗi consumer chỉ nhận bản JSON mới, không chia sẻ reference."""
    _bytes: bytes

    @classmethod
    def create(cls, point: dict[str, Any], realization: int, payload: dict[str, Any],
               provenance: dict[str, Any]) -> SharedSnapshot:
        """Chỉ seal nguồn forecast đúng point/cutoff, có hash cha và availability."""
        if type(payload) is not dict or type(provenance) is not dict:
            raise ValueError("Payload/provenance snapshot phải là object")
        forecast_only(payload)
        allowed = {*REPORTS, "stock_name", "as_of_date", "is_backtest", "time_frame", "language",
                   "pattern_image", "trend_image", "alpha_factors", "sentiment_data", "price_prefix", "causal_alpha"}
        if set(payload) - allowed:
            raise ValueError("Snapshot có field ngoài projection forecast đã khóa")
        def news_availability(value: Any) -> None:
            """Kiểm cả raw article nếu caller giữ trong sentiment_data, không chỉ tin metadata."""
            if type(value) is dict:
                if "date_parsed" in value:
                    published = value["date_parsed"]
                    if type(published) is not str or day(published[:10]) > point["cutoff"]:
                        raise ValueError("Tin future hoặc undated không được vào snapshot")
                for child in value.values():
                    news_availability(child)
            elif type(value) is list:
                for child in value:
                    news_availability(child)
        news_availability(payload.get("sentiment_data"))
        if (payload.get("stock_name") != point["symbol"] or payload.get("as_of_date") != point["cutoff"]
                or payload.get("is_backtest") is not True or payload.get("time_frame") != "1d"
                or payload.get("language") != "vi" or any(type(payload.get(k)) is not str or not payload[k].strip() for k in REPORTS)):
            raise ValueError("Snapshot không khớp point hoặc projection common VI/1d")
        if type(realization) is not int or realization < 0:
            raise ValueError("Realization không hợp lệ")
        if "price_prefix" in payload:
            prices = payload["price_prefix"]
            if (type(prices) is not dict or set(prices) != {"Datetime", "Open", "High", "Low", "Close", "Volume"}
                    or any(type(v) is not list for v in prices.values())
                    or len({len(v) for v in prices.values()}) != 1 or not 1 <= len(prices["Datetime"]) <= 600
                    or prices["Datetime"] != sorted(set(day(d) for d in prices["Datetime"]))
                    or prices["Datetime"][-1] != point["cutoff"]):
                raise ValueError("Price prefix không đúng PIT/600 bars")
            for column in ("Open", "High", "Low", "Close", "Volume"):
                if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 or
                       (column != "Volume" and v == 0) for v in prices[column]):
                    raise ValueError("Price prefix chứa giá/volume không hợp lệ")
        if (set(provenance) != {"source_sha256", "upstream_sha256", "price_end", "news_dates"}
                or not all(checksum(provenance[k]) for k in ("source_sha256", "upstream_sha256"))
                or day(provenance["price_end"]) != point["cutoff"]
                or type(provenance["news_dates"]) is not list
                or any(day(d) > point["cutoff"] for d in provenance["news_dates"])):
            raise ValueError("Nguồn/availability snapshot không hợp lệ")
        doc = {"version": "shared_snapshot_causal_v1" if "causal_alpha" in payload else "shared_snapshot_v1", "point": point, "realization": realization,
               "payload": payload, "provenance": provenance}
        if "causal_alpha" in payload:
            from core.causal_bridge import validate_embedded
            validate_embedded(doc)
        return cls(json_bytes(doc))

    def document(self) -> dict[str, Any]:
        """Không cho caller mutate bản đã seal."""
        return json.loads(self._bytes)

    @property
    def sha256(self) -> str:
        """Hash toàn snapshot, gồm provenance và realization."""
        return hashlib.sha256(self._bytes).hexdigest()


@dataclass(frozen=True)
class ExperimentSpec:
    """Spec có version và identity đầy đủ; U04 chỉ mở fixture/archive offline."""
    _bytes: bytes

    @classmethod
    def create(cls, value: dict[str, Any]) -> ExperimentSpec:
        """Kiểm trước khi mở tài nguyên hoặc tạo RunBook."""
        expected = {"version", "namespace", "mode", "variants", "points", "repeats", "realizations", "seed",
                    "decision", "source_hashes", "resource_sources", "runtime_sha256", "calendar_sha256", "estimand", "missing_policy", "costs"}
        if type(value) is dict and value.get("version") == "unified_experiment_v2":
            expected |= {"input_profile", "causal_sources"}
        if type(value) is not dict or set(value) != expected or value["version"] not in (VERSION, "unified_experiment_v2"):
            raise ValueError("ExperimentSpec sai version/fields")
        execution_order(value["variants"])
        namespace = PurePosixPath(value["namespace"])
        if (len(namespace.parts) != 3 or namespace.parts[:2] != ("outputs", "unified_integration")
                or re.fullmatch(r"[A-Za-z0-9_-]{1,100}", namespace.name) is None
                or namespace.as_posix() != value["namespace"]):
            raise ValueError("Run cần namespace outputs/unified_integration mới")
        if value["mode"] not in ("fixture", "archive_replay"):
            raise ValueError("U04 chưa cấp hosted release")
        if any(type(value[k]) is not int or not 1 <= value[k] <= 4 for k in ("repeats", "realizations")) or type(value["seed"]) is not int:
            raise ValueError("Repeat/realization/seed không hợp lệ")
        if value["seed"] != 42:
            raise ValueError("Adapter hiện hành khóa seed42; seed khác cần phiên bản phương pháp riêng")
        if value["missing_policy"] != "FAIL_CLOSED_COMMON_SUPPORT" or value["estimand"] != "SYMBOL_FOLD_ACCOUNT_RETURN_PERCENT":
            raise ValueError("Estimand/missing support chưa được hỗ trợ")
        if value["costs"] != {"fee": .0025, "slippage": .001, "horizon": 3, "initial_vnd": 50000000}:
            raise ValueError("Không được đổi hợp đồng kinh tế primary")
        if (not checksum(value["runtime_sha256"]) or not checksum(value["calendar_sha256"])
                or type(value["source_hashes"]) is not dict or not value["source_hashes"]
                or any(not checksum(v) for v in value["source_hashes"].values())):
            raise ValueError("Thiếu source/runtime/calendar identity")
        required_resources = {resource for variant in execution_order(value["variants"]) for resource in get_variant(variant).resources}
        if (type(value["resource_sources"]) is not dict or set(value["resource_sources"]) != required_resources
                or any(type(path) is not str or path not in value["source_hashes"] for path in value["resource_sources"].values())):
            raise ValueError("Resource bank/regime/facts/context/student thiếu nguồn hash tương ứng")
        points = value["points"]
        if type(points) is not list or not points:
            raise ValueError("Thiếu cohort đã khai báo")
        seen: set[str] = set()
        last: dict[tuple[str, str], str] = {}
        previous = ""
        for point in points:
            if (type(point) is not dict or set(point) != {"id", "symbol", "cutoff", "fold", "quality"}
                    or any(type(v) is not str or not v for v in point.values()) or point["id"] in seen
                    or point["id"] != point["symbol"] + "-" + day(point["cutoff"])):
                raise ValueError("Point ID/cohort không hợp lệ hoặc trùng")
            if re.fullmatch(r"[A-Z0-9]{1,12}", point["symbol"]) is None or re.fullmatch(r"[A-Za-z0-9_-]{1,80}", point["fold"]) is None:
                raise ValueError("Mã/fold không hợp lệ")
            key = (point["symbol"], point["fold"])
            if key in last and point["cutoff"] <= last[key]:
                raise ValueError("Point trong tài khoản phải theo thời gian")
            if point["cutoff"] < previous:
                raise ValueError("Cohort prequential phải theo lịch chung qua mọi mã")
            previous = point["cutoff"]
            seen.add(point["id"]); last[key] = point["cutoff"]
        # Dựng request rỗng ở adapter sẽ kiểm cấu trúc model/options đầy đủ.
        if type(value["decision"]) is not dict or not value["decision"]:
            raise ValueError("Thiếu serving config Decision")
        if value["version"] == "unified_experiment_v2":
            groups = {point["symbol"] + "/" + point["fold"] for point in points}
            bindings = value["causal_sources"]
            if (value["input_profile"] != "causal_common_v1" or type(bindings) is not dict or set(bindings) != groups
                    or any(type(entry) is not dict or set(entry) != {"prices", "selector"}
                           or any(type(path) is not str or path not in value["source_hashes"] for path in entry.values())
                           for entry in bindings.values())):
                raise ValueError("Causal family cần selector và giá đã hash cho mọi mã/fold")
        return cls(json_bytes(value))

    def document(self) -> dict[str, Any]:
        """Bản sao để caller không sửa spec đang chạy."""
        return json.loads(self._bytes)

    @property
    def identity(self) -> dict[str, Any]:
        """Registry là một phần identity, không chỉ tên run."""
        return {"spec": self.document(), "registry": registry_document()}
