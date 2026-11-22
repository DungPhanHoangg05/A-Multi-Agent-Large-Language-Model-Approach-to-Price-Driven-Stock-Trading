"""Đọc artifact U09 đã khóa; không import mã trong archive hoặc replay evaluator."""
from __future__ import annotations

import csv
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
from typing import Any
import zipfile

from core.unified_contracts import digest, json_bytes

RUN_ID = "u09_analysis_r1"
PACKAGE = "evidence/unified_analysis_results.zip"
PACKAGE_SHA256 = "e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9"
PREFIX = "outputs/unified_integration/" + RUN_ID + "/"
SUPPORT = "outputs/revision/u09_manuscript_assets_v1/artifacts/support.json"
SUPPORT_SHA256 = "cbdb936e5731f56eef0326d74cab5a52c052a34a0d1524ef88fc7cb7bbb3046b"
TABLES = ("predictions", "accounts", "cycles", "daily_nav")
ARTIFACTS = ("results.json", "summary.csv", "contrasts.csv", "bridge.csv", "per_repeat.csv",
             "classification_by_repeat.csv", "classification_by_group.csv", "predictions.csv",
             "accounts.csv", "cycles.csv", "daily_nav.csv", "return_contrasts.png")
NUMBERS = frozenset(("repeat", "realization", "r_net", "strategy_return", "return_pct", "initial_vnd", "final_vnd",
    "daily_mdd_pct", "cycle_end_mdd_pct", "fee_vnd", "slippage_vnd", "turnover_vnd", "turnover_over_initial",
    "long_count", "sessions", "held_sessions", "cash_sessions", "held_session_fraction", "cycle_sharpe",
    "cycle_sortino_lpm2", "annualized_sharpe", "annualized_sortino", "annualized_return", "nav_vnd", "shares",
    "capital_before_vnd", "capital_after_vnd", "numeric_probability", "teacher_probability", "utility_q10", "utility_q90",
    "effective_K", "prior_mean_age_days", "prior_mean_similarity", "prior_regret"))


def _check(raw: bytes, binding: dict[str, Any]) -> None:
    """Đối soát byte thực, không chuẩn hóa newline hoặc ký lại receipt."""
    if len(raw) != binding["bytes"] or hashlib.sha256(raw).hexdigest() != binding["sha256"]:
        raise ValueError("Artifact khác binding đã khóa")


@lru_cache(maxsize=2)
def _verified(raw: bytes) -> tuple[dict[str, bytes], bytes]:
    """Cache theo chính bytes đã kiểm, không tin mtime hoặc nguồn Python tại HEAD mới."""
    if hashlib.sha256(raw).hexdigest() != PACKAGE_SHA256:
        raise ValueError("Gói U09 khác release đã khóa")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        names = archive.namelist()
        if (manifest["version"] != "unified_analysis_results_v1" or manifest["status"] != "PASS_U09_COLD_REPLAY"
                or manifest["namespace"] != PREFIX.rstrip("/") or len(names) != len(set(names))
                or set(names) != set(manifest["members"]) | {"manifest.json"}):
            raise ValueError("Inventory U09 không khớp")
        members = {}
        for name, binding in manifest["members"].items():
            content = archive.read(name)
            _check(content, binding)
            members[name] = content
        envelope = json.loads(members[PREFIX + "receipt.json"])
        receipt = envelope["payload"]
        if digest(receipt) != envelope["sha256"] or receipt["status"] != "PASS_U09_ANALYSIS":
            raise ValueError("Receipt U09 không hợp lệ")
        for name, binding in receipt["artifacts"].items():
            _check(members[PREFIX + name], binding)
        result = json.loads(members[PREFIX + "results.json"])
        if (result["version"] != "unified_analysis_v1" or result["status"] != "PASS_U09_ANALYSIS"
                or result["input_identity"] != receipt["input_identity"] or result["points"] != 102
                or result["repeats"] != 3 or result["accounts_per_repeat"] != 51):
            raise ValueError("Result khác identity/support U09")
        provenance = {"run_id": RUN_ID, "kind": "paper_evidence", "package_sha256": PACKAGE_SHA256,
            "source_commit": manifest["source_commit"], "receipt_sha256": envelope["sha256"],
            "results_sha256": receipt["artifacts"]["results.json"]["sha256"],
            "support_id": digest(result["input_identity"]), "input_identity": result["input_identity"],
            "verification": "PINNED_PACKAGE_AND_MEMBER_RECEIPTS; NOT_CURRENT_SOURCE_REPLAY",
            "artifact_bindings": receipt["artifacts"], "new_api_calls": 0}
        return members, json_bytes(provenance)


@lru_cache(maxsize=16)
def _table(raw: bytes) -> bytes:
    """Projection CSV có kiểu, giữ NA và không tính lại metrics."""
    rows = []
    for original in csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))):
        row = {}
        for key, value in original.items():
            if value == "":
                row[key] = None
            elif key in NUMBERS:
                row[key] = int(value) if key in ("repeat", "realization", "long_count", "sessions", "held_sessions", "cash_sessions") else float(value)
            elif key in ("bypass", "llm_response", "cash_between_queries", "eligible", "fact_assertions_valid"):
                if value not in ("True", "False"):
                    raise ValueError("Giá trị bool CSV không hợp lệ")
                row[key] = value == "True"
            elif key == "undefined_reasons":
                row[key] = json.loads(value)
            else:
                row[key] = value
        rows.append(row)
    return json_bytes(rows)


class ResearchResults:
    """Giữ bytes đã verify trong RAM; consumer chỉ nhận JSON mới hoặc bytes bất biến."""

    def __init__(self, root: Path) -> None:
        raw = (root / PACKAGE).read_bytes()
        self._members, self._provenance = _verified(raw)
        support = (root / SUPPORT).read_bytes()
        if hashlib.sha256(support).hexdigest() != SUPPORT_SHA256:
            raise ValueError("Support companion F02 khác hash đã khóa")
        self._support = support

    def result(self) -> dict[str, Any]:
        """Không chia sẻ reference result có thể bị sửa giữa request."""
        return json.loads(self._members[PREFIX + "results.json"])

    def provenance(self) -> dict[str, Any]:
        """Nêu rõ đọc artifact historical, không chứng nhận source/runtime serving mới."""
        return {**json.loads(self._provenance), "support_companion_sha256": SUPPORT_SHA256}

    def support(self) -> dict[str, Any]:
        """Companion có missingness/support lấy từ release F02 đã khóa."""
        return json.loads(self._support)

    def table(self, name: str) -> list[dict[str, Any]]:
        """Chỉ bảng đã khai báo, không nhận tên đường dẫn từ client."""
        if name not in TABLES:
            raise ValueError("Bảng chi tiết không được hỗ trợ")
        return json.loads(_table(self._members[PREFIX + name + ".csv"]))

    def artifact(self, name: str) -> bytes:
        """Whitelist artifact nguyên byte; không extract file ra filesystem."""
        if name not in ARTIFACTS:
            raise ValueError("Artifact không được hỗ trợ")
        return self._members[PREFIX + name]
