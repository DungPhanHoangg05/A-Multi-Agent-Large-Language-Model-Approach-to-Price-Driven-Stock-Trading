"""Nạp thuật toán đã pin vào namespace riêng; không sửa globals/module nghiên cứu cũ."""

from __future__ import annotations

import builtins
from copy import deepcopy
import hashlib
from pathlib import Path
import re
import subprocess
from types import ModuleType
from typing import Any

import numpy as np
import pandas as pd

from core.historical_evaluation_protocol import read, PROTOCOL

SYMBOLS = ("BHN", "CMG", "FPT", "HVN", "MBB", "MWG", "VCB", "VJC", "VNM")
BASE = "ae5dbc6d"
PORTS = {
    "bayesian_memory", "bayesian_retriever", "prior_evidence_v2", "prior_config",
    "prior_price_similarity", "prior_example_selection", "prior_conditional_statistics",
    "prior_quality_gate", "prior_prompt", "improvement_prior", "price_feature_index",
    "mt_bicl_bank", "mt_bicl_scaler", "mt_bicl_stream", "mt_bicl_tasks", "mt_bicl_features",
    "mt_bicl_contracts", "mt_bicl_protocol", "mt_bicl_utility", "mt_bicl_context",
    "mt_bicl_policy", "mt_bicl_decision",
}


class AlgorithmScope:
    """Mỗi adapter sở hữu bản sao module, import và cache; bytecode phương pháp giữ nguyên.

    Chỉ thay universe, biên lịch đã mở, nguồn vendor và schema ID cục bộ.
    Mọi code được kiểm với H03/Git trước compile; không rewrite source/AST,
    không thay sys.modules hoặc monkeypatch đối tượng đang phục vụ hệ cũ.
    """

    def __init__(self, root: Path, *, symbols: tuple[str, ...] = SYMBOLS,
                 source: dict[str, str] | None = None) -> None:
        """CORE4 chỉ dùng kiểm parity; production dùng đúng universe chín mã."""
        if set(symbols) not in (set(SYMBOLS), {"FPT", "MWG", "VCB", "VNM"}):
            raise ValueError("Universe adapter phải là CORE4 hoặc chín mã đã khóa")
        self.root, self.symbols = root.resolve(), tuple(symbols)
        self.source = source or {"source_library": "vnstock", "primary_source": "VCI",
                                 "price_basis": "VENDOR_SERIES_LIMITED", "price_unit": "thousand_VND"}
        self.modules: dict[str, ModuleType] = {}
        self.provenance: dict[str, str] = {}
        self.pins = read(root, PROTOCOL, envelope=True)["source_bindings"]

    def _import(self, name: str, globals: Any = None, locals: Any = None,
                fromlist: Any = (), level: int = 0) -> Any:
        """Chỉ route các import tuyệt đối thuộc whitelist module thuần."""
        if level == 0 and name.startswith("core.") and name[5:] in PORTS and fromlist:
            return self.module(name[5:])
        return builtins.__import__(name, globals, locals, fromlist, level)

    def module(self, name: str) -> ModuleType:
        """Kiểm source byte, rồi bind dependency vào namespace sở hữu riêng."""
        if name not in PORTS:
            raise ValueError("Module không thuộc whitelist adapter")
        if name in self.modules:
            return self.modules[name]
        relative = f"core/{name}.py"
        raw = (self.root / relative).read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        if relative in self.pins:
            if actual != self.pins[relative]["sha256"]:
                raise ValueError("Source khác pin H03: " + relative)
        else:
            anchored = subprocess.check_output(["git", "show", f"{BASE}:{relative}"], cwd=self.root)
            if raw != anchored and raw.replace(b"\r\n", b"\n") != anchored:
                raise ValueError("Dependency khác mốc Git H03: " + relative)
        self.provenance[relative] = actual
        module = ModuleType("historical_adapter." + name)
        module.__file__ = str(self.root / relative)
        module.__dict__["__builtins__"] = {**vars(builtins), "__import__": self._import}
        self.modules[name] = module
        try:
            exec(compile(raw, module.__file__, "exec"), module.__dict__)
            if "SYMBOLS" in module.__dict__:
                module.SYMBOLS = self.symbols
            if "SOURCE" in module.__dict__ and isinstance(module.SOURCE, dict):
                module.SOURCE = deepcopy(self.source)
            if name == "mt_bicl_bank":
                module.corporate_action_barriers = self.barriers
            elif name == "mt_bicl_stream":
                module._visible_prices = self.visible_prices
                module.extract_pit_price_features = self.features
                module.market_partition = self.partition
                parent = module.MarketStream
                class HistoricalStream(parent):
                    """Mở lịch tới snapshot2026; giữ advance/labels của primitive đã pin."""
                    def _index(self, query: str) -> int:
                        """Không nén lịch hoặc dùng phiên gần nhất."""
                        query = module.day(query)
                        index = int(self.calendar.get_indexer([pd.Timestamp(query)])[0])
                        if index < 0 or query > "2026-09-30" or index + 3 >= len(self.calendar):
                            raise ValueError("Query ngoài lịch H03 hoặc thiếu t+3")
                        return index
                module.MarketStream = HistoricalStream
            elif name == "mt_bicl_contracts":
                schema = deepcopy(module.wire_schema())
                schema["$defs"]["fact_packet"]["properties"]["point_id"]["pattern"] = self.point_pattern()
                # Các định nghĩa dùng chung ID trỏ cùng pattern qua $ref hoặc trường point_id.
                def extend(node: Any) -> None:
                    """Chỉ mở regex universe, giữ mọi trường/enum/hạn mức của schema."""
                    if isinstance(node, dict):
                        for key, value in node.items():
                            if key == "pattern" and isinstance(value, str) and "FPT|MWG|VCB|VNM" in value:
                                node[key] = value.replace("FPT|MWG|VCB|VNM", "|".join(scope_symbols))
                            else:
                                extend(value)
                    elif isinstance(node, list):
                        for value in node:
                            extend(value)
                scope_symbols = self.symbols
                extend(schema)
                module.wire_schema = lambda: deepcopy(schema)
            elif name == "mt_bicl_protocol":
                module.component_seed = self.component_seed
            return module
        except BaseException:
            self.modules.pop(name, None)
            raise

    def point_pattern(self) -> str:
        """ID giữ mã thật, không alias OOD thành mã CORE4."""
        return "^(" + "|".join(self.symbols) + ")-20[0-9]{2}-[0-9]{2}-[0-9]{2}$"

    def component_seed(self, protocol_hash: str, point_id: str, component: str) -> str:
        """Giữ đúng material uint128/CRN; chỉ mở whitelist mã."""
        if not re.fullmatch(r"[0-9a-f]{64}", protocol_hash) or not re.fullmatch(self.point_pattern(), point_id):
            raise ValueError("Hash hoặc ID CRN không hợp lệ")
        self.module("mt_bicl_bank").day(point_id.split("-", 1)[1])
        if component not in ("lambda", "theta") and not (
                component.startswith("magnitude|") and re.fullmatch(self.point_pattern(), component[10:])):
            raise ValueError("Component CRN không hợp lệ")
        material = f"utility-v3|{protocol_hash}|{point_id}|{component}"
        return str(int.from_bytes(hashlib.sha256(material.encode()).digest()[:16], "big"))

    @staticmethod
    def partition(day: str) -> str | None:
        """Giữ partition fit cũ, lịch2023–2026 chỉ là historical đã exposed."""
        if day <= "2020-12-31":
            return "train"
        if day <= "2021-12-31":
            return "checkpoint_selection"
        if day <= "2022-12-31":
            return "validation"
        return "historical_exposed" if day <= "2026-09-30" else None

    @staticmethod
    def barriers(frame: pd.DataFrame, events: list[dict[str, Any]]) -> pd.DatetimeIndex:
        """Dùng ngày quyền/gap từ raw H02; không chế Reference cho chuỗi vendor."""
        from core.execution_prices import validate_raw_frame
        validate_raw_frame(frame)
        if "Reference" in frame:
            from core.execution_prices import corporate_action_barriers
            return corporate_action_barriers(frame, events)
        return pd.DatetimeIndex(pd.to_datetime([r["exrightDate"] for r in events])).unique().sort_values()

    @staticmethod
    def visible_prices(frame: pd.DataFrame, calendar: pd.DatetimeIndex) -> pd.DataFrame:
        """Chỉ chọn OHLCV prefix đã kiểm, không thêm giá Reference giả."""
        from core.execution_prices import validate_raw_frame
        visible = frame.loc[frame["Datetime"] <= calendar[-1]].copy()
        if not visible.empty:
            validate_raw_frame(visible)
            if len(pd.DatetimeIndex(visible["Datetime"]).difference(calendar)):
                raise ValueError("Nguồn giá có phiên ngoài lịch")
        return visible

    def features(self, frame: pd.DataFrame, events: list[dict[str, Any]], calendar: pd.DatetimeIndex,
                 cutoff: str, *, source: dict[str, str]) -> dict[str, Any]:
        """Tái dùng batch primitive21 đã pin với ngày barrier explicit của H02."""
        if source != self.source:
            raise ValueError("Source feature khác profile adapter")
        prefix = calendar[calendar <= pd.Timestamp(cutoff)]
        if len(prefix) < 21 or prefix[-1] != pd.Timestamp(cutoff):
            raise ValueError("Query feature thiếu lịch21 hoặc cutoff")
        visible = self.visible_prices(frame, prefix)
        events = [r for r in events if r["exrightDate"] <= cutoff]
        return self.module("mt_bicl_bank").batch_features(
            visible, events, prefix, np.asarray([len(prefix) - 1], dtype=int))[0][0]
