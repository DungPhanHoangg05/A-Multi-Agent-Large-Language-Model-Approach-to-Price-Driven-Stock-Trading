"""Kiểm lịch, workload, chống tự reseal và ngân sách H03; không API hoặc fit."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from core import historical_evaluation_protocol as protocol

ROOT = Path(__file__).resolve().parents[1]


class HistoricalProtocolTests(unittest.TestCase):
    """Dùng chính lịch donor đã audit để bắt lệch ngày/suffix/purge."""

    @classmethod
    def setUpClass(cls) -> None:
        """Chỉ dựng metadata; không đọc outcome hoặc tạo graph/model."""
        cls.inputs = protocol.timeline(ROOT)

    def test_fixed_cohort_and_bhn_eligibility(self) -> None:
        """Giữ20 cycle/scope, CORE4 và BHN chỉ ba fold cuối."""
        rows = self.inputs["grid"]
        self.assertEqual((len(rows), sum(r["core4"] for r in rows), sum(r["anchor"] for r in rows)), (1020, 480, 102))
        self.assertEqual({r["fold"] for r in rows if r["symbol"] == "BHN"},
                         {"f2025_q4", "f2026_q2", "f2026_q3"})
        self.assertTrue(all(r["raw_decision_index"] - r["suffix_decision_index"] == 673
                            for r in rows if r["symbol"] == "BHN"))

    def test_panel_one_per_scope_without_payoff(self) -> None:
        """Panel phủ51 scope, không lấy18 ID panel donor làm lịch mới."""
        selected = [r for r in self.inputs["grid"] if r["id"] in self.inputs["panel_ids"]]
        self.assertEqual(len(selected), 51)
        self.assertEqual(len({(r["symbol"], r["fold"]) for r in selected}), 51)
        self.assertFalse(any("y" in r or "net_return" in r for r in self.inputs["grid"] + self.inputs["history"]))

    def test_mutated_query_date_rejected(self) -> None:
        """Grid tự đổi ngày không khớp index donor dù ID vẫn giữ nguyên."""
        original_read = protocol.read
        def changed(root: Path, name: str | Path, **kwargs: bool) -> object:
            """Chỉ thay dữ liệu grid đầu vào cho kiểm âm."""
            value = original_read(root, name, **kwargs)
            if Path(name) == protocol.GRID:
                value[0]["date"] = "2099-01-01"
            return value
        with patch.object(protocol, "read", side_effect=changed):
            with self.assertRaises(ValueError):
                protocol.timeline(ROOT)

    def test_purge_boundary_rejected(self) -> None:
        """Nhãn validation chạm test không được chấp nhận."""
        original_read = protocol.read
        def changed(root: Path, name: str | Path, **kwargs: bool) -> object:
            """Cài validation có exit==first test để kiểm biên chặt."""
            value = original_read(root, name, **kwargs)
            if Path(name) == protocol.DONOR_BANK:
                value["schedule"][0]["validation"][-1] = value["schedule"][0]["test"][0] - 3
            return value
        with patch.object(protocol, "read", side_effect=changed):
            with self.assertRaises(ValueError):
                protocol.timeline(ROOT)

    def test_exact_workload_and_no_training_calls(self) -> None:
        """Đếm độc lập các loại execution, tách lịch sử và query dùng chung."""
        calls = protocol.research_calls(self.inputs)
        self.assertEqual(calls["decision"], 21420 + 3060 + 918 + 306 + 2142)
        self.assertEqual(calls["query_panel_vision"], 2244)
        self.assertEqual(calls["research_total"], 30090 + 2 * calls["historical_upstream_H"])
        shared = [r for r in self.inputs["history"] if r["shared_query_unit"] is not None]
        self.assertEqual(calls["history_population"], calls["historical_upstream_H"] + len(shared))
        self.assertTrue(all(r["shared_query_unit"] in {q["id"] for q in self.inputs["grid"]} for r in shared))

    def test_resealed_mutation_cannot_replace_frozen_contract(self) -> None:
        """Checksum mới không cho phép đổi authorization/options/count đã seal."""
        expected = {"authorization": {"api": False}, "max_tokens": 960, "calls": 30090}
        with tempfile.TemporaryDirectory() as directory:
            root, name = Path(directory), Path("protocol.json")
            for field, value in (("authorization", {"api": True}), ("max_tokens", 2048), ("calls", 1)):
                changed = {**expected, field: value}
                (root / name).write_bytes(protocol.encode({"payload": changed, "sha256": protocol.digest(changed)}))
                with self.assertRaises(ValueError):
                    protocol.save_once(root, name, expected, verify=True)

    def test_paths_and_missing_frozen_file(self) -> None:
        """Không đọc ngoài repo/credential và verify không tự tạo file thiếu."""
        for name in ("../outside.json", ".env", ".env.local"):
            with self.assertRaises(ValueError):
                protocol.safe(ROOT, name)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                protocol.save_once(Path(directory), Path("missing.json"), {}, verify=True)
            self.assertFalse((Path(directory) / "missing.json").exists())

    def test_empty_archive_cannot_bypass_donor_verification(self) -> None:
        """Xóa danh sách nguồn trong receipt không được bỏ qua đối soát Git."""
        with patch.object(protocol, "read", return_value={"donor_commit": protocol.DONOR, "source_archive": []}):
            with self.assertRaises(ValueError):
                protocol.frozen_sources(ROOT)

    def test_budget_uses_history_reference_and_reserves(self) -> None:
        """Không coi latency cũ là số đo960 mới, không bỏ retry/unknown khỏi trần."""
        inputs = deepcopy(self.inputs)
        inputs["telemetry"] = {"models": {model: {"fields": {
            "prompt_tokens": {"mean": 2000.}, "completion_tokens": {"mean": 200.},
            "latency_seconds": {"mean": 2.}}} for model in protocol.MODELS}}
        budget = protocol.budget(inputs)
        nominal = budget["calls"]["research_total"]
        self.assertEqual(budget["max_total_http_attempts"], (nominal + 100) * 3 + budget["unknown_attempt_reserve"])
        self.assertGreater(budget["all_attempts_planning_usd"], budget["planning_usd"])
        self.assertFalse(budget["organization_independence_verified"])
        self.assertFalse(budget["deadline_guaranteed"])
        json.dumps(budget, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
