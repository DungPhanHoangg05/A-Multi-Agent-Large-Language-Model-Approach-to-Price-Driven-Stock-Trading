"""Provider offline chín mã; namespace riêng, bank và context đóng băng trước test."""
from __future__ import annotations

import builtins
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

from core.historical_evaluation_scope import AlgorithmScope, PORTS
from core.unified_contracts import digest
from core.unified_protocol import BASE, CORE4, git_blob

FREEZE = "2022-12-30"
EXTRA = {"mt_bicl_decision", "mt_bicl_prompt", "unified_methods", "free_pilot_assets"}


class StudyScope(AlgorithmScope):
    """Mở schema/renderer trong scope sở hữu riêng; không đổi module gốc hoặc sys.modules."""
    def _import(self, name: str, globals: Any = None, locals: Any = None,
                fromlist: Any = (), level: int = 0) -> Any:
        if level == 0 and name.startswith("core.") and name[5:] in PORTS | EXTRA and fromlist:
            return self.module(name[5:])
        return builtins.__import__(name, globals, locals, fromlist, level)

    def module(self, name: str) -> ModuleType:
        if name not in EXTRA:
            return super().module(name)
        if name not in self.modules:
            relative = "core/" + name + ".py"
            raw = (self.root / relative).read_bytes()
            if raw != git_blob(self.root, BASE, relative):
                raise ValueError("Renderer khác source U05 đã khóa")
            module = ModuleType("unified_study." + name)
            module.__file__ = str(self.root / relative)
            module.__dict__["__builtins__"] = {**vars(builtins), "__import__": self._import}
            self.modules[name] = module
            self.provenance[relative] = __import__("hashlib").sha256(raw).hexdigest()
            try:
                exec(compile(raw, module.__file__, "exec"), module.__dict__)
            except BaseException:
                self.modules.pop(name, None)
                raise
        return self.modules[name]


class FrozenStudyStream:
    """Advance đúng một lần trước test fold; query chỉ đọc x mới, không nhập nhãn test."""
    def __init__(self, source: Any, freeze_before: str) -> None:
        self.source, self.calendar = source, source.calendar
        self.freeze_before = freeze_before
        self._records = source.advance(freeze_before)
        if any(row["exit_date"] >= freeze_before for row in self._records):
            raise ValueError("Context frozen chứa nhãn vượt đầu test fold")

    def features(self, symbol: str, cutoff: str) -> dict[str, Any]:
        return self.source.features(symbol, cutoff)

    def advance(self, cutoff: str) -> list[dict[str, Any]]:
        if cutoff < self.freeze_before:
            raise ValueError("Query nghiên cứu phải sau frozen bank")
        if any(row["exit_date"] >= cutoff for row in self._records):
            raise ValueError("Context chưa trưởng thành trước query")
        return deepcopy(self._records)


class FrozenStudyContext:
    """Tái dùng weights/HMM/scaler và primitive MT thật; không fit hoặc cập nhật theo query."""
    def __init__(self, data: Any, freeze_before: str) -> None:
        from core.historical_evaluation_context import ContextBank
        from core.mt_bicl_adapter import StudentAdapter
        self.data = data
        student = StudentAdapter(data.root, manifest=data.root / "docs/plan/week11/mt_bicl_replica_full_r1_model.json")
        self.context = ContextBank(data, lambda _: False, student=student)
        self.view = FrozenStudyStream(self.context.stream, freeze_before)
        self.context.builder.view.source = self.view

    def build(self, symbol: str, cutoff: str) -> dict[str, Any]:
        result = self.context.build(symbol, cutoff)
        observations = [r for task in result["prior"] for r in task["observations"]] + result["target"]
        if any(r["exit_date"] >= self.view.freeze_before for r in observations):
            raise ValueError("Context query nhập nhãn sau freeze")
        return result

    def variants(self, episode: dict[str, Any]) -> dict[str, Any]:
        return self.context.variants(episode)


class FrozenStudyBank:
    """Bank852 CORE4; OOD có fallback khai báo, scaler2022 được tái dùng chứ không refit."""
    def __init__(self, data: Any, points: list[dict[str, Any]]) -> None:
        from core.unified_preflight_assets import ASSETS, write_new
        from core.unified_protocol import read
        import hashlib
        self.data = data
        self.scope = StudyScope(data.root, symbols=tuple(CORE4))
        # QA W2 đã băm checkout CRLF; giữ schema LF hiện hành và chứng minh đúng biến thể cũ.
        schema_name = "docs/plan/week1/historical_task_record.schema.json"
        raw = (data.root / schema_name).read_bytes()
        legacy = raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        expected = read(data.root, "docs/plan/week2/memory_bank_audit.json")["schema_sha256"]
        if hashlib.sha256(legacy).hexdigest() != expected:
            raise ValueError("Không tái tạo được byte schema CRLF mà QA bank khóa")
        compat_root = data.root / ASSETS / "compatibility"
        write_new(compat_root / schema_name, legacy)
        self.scope.module("bayesian_retriever").ROOT = compat_root
        raw_root = data.root / "data/execution_prices"
        raw_manifest = read(data.root, "data/execution_prices/manifest.json")
        compat_prices = compat_root / "execution_prices"
        write_new(compat_prices / "manifest.json", (raw_root / "manifest.json").read_bytes())
        for files in raw_manifest["files"].values():
            for kind in ("csv", "evidence", "events"):
                expected_file = files[kind]
                blob = (raw_root / expected_file["file"]).read_bytes()
                if hashlib.sha256(blob).hexdigest() != expected_file["sha256"]:
                    if kind == "evidence":
                        raise ValueError("Evidence gzip ngân hàng không khớp manifest")
                    blob = blob.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
                if hashlib.sha256(blob).hexdigest() != expected_file["sha256"]:
                    raise ValueError("Không tái tạo được byte legacy giá/events")
                write_new(compat_prices / expected_file["file"], blob)
        self.scope.module("bayesian_memory").DEFAULT_DATA_DIR = compat_prices
        self.base = self.scope.module("free_pilot_assets").FrozenBank(data)
        self.retriever = self.base.retriever
        module = self.scope.module("price_feature_index")
        raw_payload = self.base.index.payload
        frozen = deepcopy(raw_payload["scalers"]["oos_2023_2024"])
        folds = {}
        for row in points:
            fold = row["fold"]
            if fold not in folds:
                dates = [r["date"] for r in points if r["fold"] == fold]
                folds[fold] = {"query_start": min(dates), "query_end": max(dates)}
        module._FOLDS = deepcopy(folds)
        payload = deepcopy(raw_payload)
        payload["scalers"] = {fold: deepcopy(frozen) for fold in folds}
        payload["transfer_contract"]["query_folds"] = folds
        payload["transfer_contract"]["scaler_transfer"] = "FROZEN_BANK2022_REUSE_NO_QUERY_FIT"
        # Raw bank vẫn giữ nguồn riêng; chỉ biên transform query nhận donor series.
        query_payload = deepcopy(payload)
        query_payload["source"] = deepcopy(self.scope.source)
        guard = module.PriceFeatureIndex(query_payload, _verified=module._VERIFIED)
        class TransferIndex(module.PriceFeatureIndex):
            """Không đổi scaler hoặc bank labels để khớp chuỗi query vendor."""
            def transform_query(self, symbol: str, as_of_date: str, features: dict, *, fold_id: str | None = None) -> dict:
                result = guard.transform_query(symbol, as_of_date, features, fold_id=fold_id)
                result["index_sha256"] = self.identity
                return result
        self.index = TransferIndex(payload, _verified=module._VERIFIED)
        selector_module = self.scope.module("prior_example_selection")
        self.selector = selector_module.PriceExampleSelector(self.index, data.calendar)
        self.audit = {**deepcopy(self.base.audit), "index_identity": self.index.identity,
                      "query_folds": folds, "OOD_policy": "FALLBACK_ORIGINAL_COMMON_NO_SAME_SYMBOL_BANK"}

    def request(self, branch: str, shared: dict[str, Any], regime: str) -> tuple[dict, dict]:
        from core.mt_bicl_prompt import canonical_request
        from core.historical_evaluation_prior import signals
        query = {"symbol": shared["stock_name"], "as_of_date": shared["as_of_date"],
                 "current_regime": regime, "current_signals": signals(shared)}
        if any(row["exit_date"] >= query["as_of_date"] for row in self.base.records):
            raise ValueError("Bank label chưa đóng trước query")
        proof: dict[str, Any] = {"branch": branch, "fallback": False,
                                "bank_sha256": self.retriever._bank_sha256}
        prefix = ""
        if query["symbol"] not in CORE4:
            proof.update(fallback=True, reason="NO_SAME_SYMBOL_FROZEN_BANK_OOD")
            proof["request"] = {"prefix": ""}
            if branch == "bayesian_v1":
                proof["retrieval"] = {"tasks": [], "stats": None}
        elif branch == "bayesian_v1":
            from core.bayesian_retriever import format_compact_prior_prefix
            result = self.retriever.retrieve(**query, mode="bayesian_regime", k=3, seed=42, scope="same_symbol")
            prefix = format_compact_prior_prefix(result["tasks"], result["stats"])
            proof["retrieval"] = result
        elif branch in ("C2", "A_tp_pool", "B_semantic"):
            module = self.scope.module("improvement_prior")
            feature = self.data.features(query["symbol"], query["as_of_date"])
            evidence = module.build_evidence(self.retriever, branch, **query, selector=self.selector, query_features=feature)
            rendered = module.build_request(evidence, branch, self.retriever, selector=self.selector, query_features=feature)
            prefix = rendered["prefix"]
            proof.update(evidence=evidence, request=rendered, fallback=rendered["trace"]["fallback_to_original"])
        else:
            raise ValueError("Nhánh ngoài bank nghiên cứu")
        return canonical_request(deepcopy(shared), prefix, {"decision": self.data.protocol["inference"]["config"]}), proof


def study_data(root: Path) -> Any:
    """Nguồn H02/H03 có hash ở manifest U06; không gọi verifier runtime cũ trên code mới."""
    from core.historical_evaluation_data import HistoricalData
    from core.unified_preflight import RESOURCE_INPUTS
    for name in RESOURCE_INPUTS:
        if (root / name).read_bytes() != git_blob(root, BASE, name):
            raise ValueError("Input/schema/QA lịch sử khác nguồn đã khóa")
    # verify=False chỉ bỏ gate runtime H03 cũ; input thực vẫn phải khớp Git đã khóa.
    for directory in ("outputs/historical_reevaluation/h02_data_r1", "data/execution_prices"):
        for path in sorted((root / directory).rglob("*")):
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                if path.is_symlink() or path.read_bytes() != git_blob(root, BASE, relative):
                    raise ValueError("Nguồn giá/events khác Git U05: " + relative)
    data = HistoricalData(root, verify=False)
    data.scope = StudyScope(root)
    return data
