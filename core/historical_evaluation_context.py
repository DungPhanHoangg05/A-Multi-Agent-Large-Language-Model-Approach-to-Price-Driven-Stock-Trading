"""Context MT-BICL chín mã, scaler/regime frozen và rào forecast trước nhãn."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler

from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_protocol import read
from core.mt_bicl_adapter import StudentAdapter
from core.mt_bicl_bank import content_hash
from core.mt_bicl_oracle import numeric_input
from core.mt_bicl_regimes import RegimeTimeline
from core.regime_detector import FEATURE_COLUMNS, HMM_PARAMETERS, MarketRegimeDetector, training_data_hash


def hydrate(parameters: dict[str, Any]) -> MarketRegimeDetector:
    """Nạp đúng tham số H02 vào primitive hiện hữu, không gọi fit."""
    detector = MarketRegimeDetector()
    detector._metadata = deepcopy(parameters["metadata"])
    detector._model = GaussianHMM(**HMM_PARAMETERS)
    for name, key in (("startprob_", "startprob"), ("transmat_", "transmat"),
                      ("means_", "means"), ("covars_", "covars")):
        setattr(detector._model, name, np.asarray(parameters["model"][key], dtype=float))
    detector._model.n_features = len(FEATURE_COLUMNS)
    detector._scaler = StandardScaler()
    for name, key in (("mean_", "mean"), ("scale_", "scale"), ("var_", "variance")):
        setattr(detector._scaler, name, np.asarray(parameters["scaler"][key], dtype=float))
    detector._scaler.n_features_in_ = len(FEATURE_COLUMNS)
    detector._scaler.n_samples_seen_ = detector.metadata["feature_rows"]
    detector._validate_fitted()
    return detector


class FrozenTimeline(RegimeTimeline):
    """Bổ sung đúng artifact đã fit, thiếu artifact thì dừng thay vì refit ngầm."""

    def __init__(self, data: HistoricalData) -> None:
        """Đối soát model hash theo serialization gốc trước classify."""
        super().__init__(data.history)
        record = data.model_manifest["preprocessing"]["regime_models"]
        actual = read(data.root, record["path"], envelope=True)
        for cutoff, entry in actual.items():
            detector = hydrate(entry["parameters"])
            if training_data_hash(self._prefix(cutoff)) != detector.metadata["training_data_sha256"]:
                raise ValueError("Prefix VNINDEX khác nguồn fit regime H02")
            if content_hash(self._serialize(detector)) != entry["proof"]["model_sha256"]:
                raise ValueError("Regime H02 không khớp fingerprint")
            self._models[cutoff] = detector
            self._proofs[cutoff] = deepcopy(entry["proof"])

    def _model(self, cutoff: str) -> tuple[Any, dict[str, Any]]:
        """Chỉ UNKNOWN khi thiếu499 phiên, không tự huấn luyện model bị thiếu."""
        if len(self._prefix(cutoff)) >= 499 and cutoff not in self._models:
            raise ValueError("Thiếu frozen regime prefix: " + cutoff)
        return super()._model(cutoff)


class ContextBank:
    """Giữ thuật toán task/bucket nguyên byte và lọc query chưa forecast trước label."""

    def __init__(self, data: HistoricalData, forecast_done: Callable[[str], bool], *,
                 student: Any = None) -> None:
        """Không splice bank train cũ; chỉ tái dùng scaler/regime/weights đã nghiệm thu."""
        self.data, self.scope = data, data.scope
        stream_module = self.scope.module("mt_bicl_stream")
        base_stream = stream_module.MarketStream
        symbols = self.scope.symbols

        class GatedStream(base_stream):
            """Reserve ID trước chọn candidates; cycle bị khóa không bao giờ tính payoff."""
            def __init__(self, *args: Any) -> None:
                super().__init__(*args)
                self.reserved: set[str] = set()

            def closed_records(self) -> list[dict[str, Any]]:
                """Không xuất reservation thành observation hoặc nhãn giả."""
                if self._last_query is None:
                    return []
                rows = [deepcopy(row) for key, row in self._rows.items()
                        if key not in self.reserved and row["exit_date"] < self._last_query]
                return sorted(rows, key=lambda r: (r["as_of_date"], symbols.index(r["symbol"])))

            def advance(self, query: str) -> list[dict[str, Any]]:
                """Chặn trước nguyên thủy vector hóa đọc giá entry/exit của query bị khóa."""
                for (symbol, cutoff), unit in data.by_day.items():
                    identifier = symbol + "-" + cutoff
                    if unit["exit_date"] < query and identifier not in self._rows and not forecast_done(unit["id"]):
                        self.reserved.add(identifier)
                        self._rows[identifier] = {}
                withheld = sorted(self.reserved)
                try:
                    rows = super().advance(query)
                    self.audit[-1]["withheld_forecast_ids"] = withheld
                    return rows
                finally:
                    for identifier in self.reserved:
                        self._rows.pop(identifier, None)
                    self.reserved.clear()

        scalers = data.model_manifest["preprocessing"]["scalers"]
        if len(scalers) != 1:
            raise ValueError("Replica phải có đúng một scaler frozen cuối2020")
        scaler = deepcopy(next(iter(scalers.values())))
        bank = {"records": [], "frozen_scaler": scaler}
        self.stream = GatedStream(bank, {s: (data.frames[s], data.events[s]) for s in symbols}, data.calendar)
        tasks = self.scope.module("mt_bicl_tasks")
        parent = tasks.TaskBuilder
        class FrozenBuilder(parent):
            """Inject scaler đã fit thay vì fit bằng chuỗi vendor hồi cứu."""
            def __init__(self, *args: Any) -> None:
                super().__init__(*args)
                self._frozen = deepcopy(scaler)
        features = self.scope.module("mt_bicl_features")
        features.TaskBuilder = FrozenBuilder
        self.builder = features.BucketTaskBuilder(bank, self.stream, FrozenTimeline(data),
                                                {s: data.frames[s] for s in symbols})
        self.student = student or StudentAdapter(data.root, manifest=data.root / "docs/plan/week11/mt_bicl_replica_full_r1_model.json")

    def build(self, symbol: str, cutoff: str) -> dict[str, Any]:
        """Giữ ID/mã thật và OOD trong sidecar, không đưa OOD flag vào tensor student."""
        return self.builder.build(symbol, cutoff)

    def predict(self, episode: dict[str, Any]) -> float:
        """Validator universe mới chạy trước phép chiếu numeric không có query-y."""
        self.scope.module("mt_bicl_contracts").validate_context(episode)
        return self.student.predict_input(numeric_input(episode))

    def variants(self, episode: dict[str, Any]) -> dict[str, Any]:
        """Giữ Full/No_target hai forward và utility4096/CRN của code đã pin."""
        return self.scope.module("mt_bicl_context").prepare_variants(episode, self.student.teacher, self.predict)
