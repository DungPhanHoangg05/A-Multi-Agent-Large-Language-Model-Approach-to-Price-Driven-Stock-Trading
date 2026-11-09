"""So donor độc lập và native port ở biên request; chặn ngầm đổi profile/PIT."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import Any
import unittest
from unittest.mock import Mock, patch

from agents import decision_agent as decision
from core.backtest_engine import BacktestEngine
from core.decision_profiles import NATIVE_PROFILE, INTEGRATED_PROFILE
from scripts.verify_original_fix_parity import DONOR, REPORTS, client_class, run_graph, archive_replay, extract_donor
from utils.graph_setup import SetGraph
from utils.trading_graph import TradingGraph

ROOT = Path(__file__).resolve().parents[1]


def oracle() -> ModuleType:
    """Nguồn Decision donor không lấy từ implementation đang kiểm."""
    raw = subprocess.check_output(["git", "show", DONOR + ":agents/decision_agent.py"], cwd=ROOT)
    module = ModuleType("u03_frozen_decision")
    exec(compile(raw, "u03_frozen_decision.py", "exec", dont_inherit=True), module.__dict__)
    return module


def state(language: str = "vi", variant: str = "AS") -> dict:
    """Reports đủ dài để phân biệt cap native với cap tích hợp, không có payoff."""
    result = {"stock_name": "FPT", "time_frame": "1 ngày", "language": language, "is_backtest": True,
              **{key: key + "\n" + "Số liệu 123.45; " * 120 for key in REPORTS[:3]}}
    for flag, key in (("A", "alpha_report"), ("S", "sentiment_report")):
        if flag in variant:
            result[key] = key + "\n" + "Tín hiệu α; " * 150
    return result


class OriginalFixRequestTests(unittest.TestCase):
    """Oracle payload/schema/parse và các guard có hệ quả trước lời gọi model."""
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixed = oracle()
        cls.Client = client_class()

    def client(self) -> Any:
        """SDK thật serialize; response/transport dùng double cục bộ."""
        return self.Client(model="openai/gpt-oss-20b", temperature=0., max_tokens=2048,
                           max_retries=3, reasoning_format="hidden")

    def test_all_ablations_both_languages_match_final_wire_schema_and_parse(self) -> None:
        for language in ("vi", "en"):
            for variant in ("B", "A", "S", "AS"):
                before, after = self.client(), self.client()
                value = state(language, variant)
                original = deepcopy(value)
                expected = self.fixed.create_final_trade_decider(before)(value)
                actual = decision.create_final_trade_decider(after, decision_profile=NATIVE_PROFILE)(value)
                with self.subTest(language=language, variant=variant):
                    self.assertEqual(before.requests, after.requests)
                    self.assertEqual(before.schemas, after.schemas)
                    self.assertEqual(expected["final_trade_decision"], actual["final_trade_decision"])
                    self.assertEqual(expected["decision_prompt"], actual["decision_prompt"])
                    self.assertEqual(value, original)

    def test_integrated_caps_have_a_separate_profile_and_stay_below_budget(self) -> None:
        native, common = self.client(), self.client()
        value = state()
        a = decision.create_final_trade_decider(native, decision_profile=NATIVE_PROFILE)(value)
        b = decision.create_final_trade_decider(common, decision_profile=INTEGRATED_PROFILE)(value)
        self.assertNotEqual(a["decision_prompt"], b["decision_prompt"])
        self.assertLess(len(b["decision_prompt"]), 6500)
        # Graph từ Full reports thuộc đường nghiên cứu hiện hành, không nhận nhầm native.
        reports = SetGraph(common, object(), object()).compile_report_decision()
        output = reports.invoke(value)
        self.assertEqual(output["decision_prompt"], b["decision_prompt"])

    def test_native_6499_passes_and_6500_fails_without_model_invoke(self) -> None:
        for length in (6499, 6500):
            client = self.client()
            with patch.object(decision, "_build_compact_prompt_vi", return_value="X" * length):
                node = decision.create_final_trade_decider(client, decision_profile=NATIVE_PROFILE)
                if length == 6500:
                    with self.assertRaisesRegex(ValueError, "ngân sách"):
                        node(state(variant="B"))
                    self.assertEqual(client.requests, [])
                else:
                    self.assertEqual(len(node(state(variant="B"))["decision_prompt"]), length)
                    self.assertEqual(len(client.requests), 1)

    def test_native_rejects_prior_hooks_enabled_or_injected_prefix(self) -> None:
        for hook in ("prior_source_validator", "_prior_preparer", "_before_invoke", "_prior_request"):
            client = self.client()
            with self.subTest(hook=hook), self.assertRaises(ValueError):
                decision.create_final_trade_decider(client, decision_profile=NATIVE_PROFILE, **{hook: lambda *_: None})
            self.assertEqual(client.schemas, [])
        for extra in ({"prior_config": {"enable_bayesian_prior": True}}, {"bayesian_prior_context": "Injected"},
                      {"prior_config": "bad-shape"}):
            client = self.client()
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                decision.create_final_trade_decider(client, decision_profile=NATIVE_PROFILE)({**state(), **extra})
            self.assertEqual(client.requests, [])

    def test_native_off_does_not_open_bank_or_student(self) -> None:
        with (patch("core.bayesian_memory.HistoricalMemory", side_effect=AssertionError("Không được mở bank")),
              patch("core.mt_bicl_adapter.StudentAdapter", side_effect=AssertionError("Không được mở model"))):
            result = decision.create_final_trade_decider(self.client(), decision_profile=NATIVE_PROFILE)(state())
        self.assertIn(json.loads(result["final_trade_decision"])["decision"], ("LONG", "SHORT"))

    def test_archive_cannot_resign_a_changed_manifest_as_donor(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            inventory = root / "docs/plan/week12/fix_develop_source_inventory.zip"
            inventory.parent.mkdir(parents=True)
            inventory.write_bytes((ROOT / "docs/plan/week12/fix_develop_source_inventory.zip").read_bytes())
            manifest = root / "outputs/revision/revision_minimal_v1/manifest.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_bytes(b'{"sha256":"resigned"}')
            with self.assertRaisesRegex(ValueError, "khác Git donor"):
                archive_replay(root)

    def test_cold_oracle_extracts_exact_git_bytes_without_checkout_conversion(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            extract_donor(ROOT, root)
            for name in ("agents/agent_state.py", "agents/decision_agent.py", "core/backtest_engine.py",
                         "default_config.py", "utils/graph_setup.py", "utils/statistical_tests.py"):
                expected = subprocess.check_output(["git", "show", DONOR + ":" + name], cwd=ROOT)
                self.assertEqual((root / name).read_bytes(), expected, name)

    def test_two_invalid_replies_abort_without_synthetic_cash(self) -> None:
        for module in (self.fixed, decision):
            client = self.client()
            client.replies = ['{"decision":"HOLD"}', '{"decision":"HOLD"}']
            kwargs = {"decision_profile": NATIVE_PROFILE} if module is decision else {}
            with self.assertRaises(RuntimeError):
                module.create_final_trade_decider(client, **kwargs)(state())
            self.assertEqual(len(client.requests), 2)
            self.assertEqual(client.requests[0], client.requests[1])

    def test_unknown_profile_stops_engine_and_live_before_client_creation(self) -> None:
        for profile in ("typo", "original_fix", None, 0):
            with patch("langchain_groq.ChatGroq") as llm, self.assertRaises(ValueError):
                BacktestEngine({"decision_profile": profile, "groq_api_key": "fixture"})._init_graphs()
            llm.assert_not_called()
            with patch.object(TradingGraph, "_create_llm") as llm, self.assertRaises(ValueError):
                TradingGraph({"decision_profile": profile})
            llm.assert_not_called()

    def test_legacy_live_and_backtest_entrypoints_select_native(self) -> None:
        with (patch("utils.trading_graph.ChatGroq"), patch("utils.trading_graph.TechnicalTools"),
              patch("utils.trading_graph.SetGraph") as graph):
            live = TradingGraph({"groq_api_key": "fixture"})
            self.assertEqual(graph.call_args.kwargs["decision_profile"], NATIVE_PROFILE)
            live.refresh_llms()
            self.assertEqual(graph.call_args.kwargs["decision_profile"], NATIVE_PROFILE)
        with (patch("langchain_groq.ChatGroq"), patch("utils.graph_util.TechnicalTools"),
              patch("utils.graph_setup.SetGraph") as graph):
            BacktestEngine({"groq_api_key": "fixture"})._init_graphs()
            self.assertEqual(graph.call_args.kwargs["decision_profile"], NATIVE_PROFILE)


class OriginalFixFutureFirewallTests(unittest.TestCase):
    """Poison outcome không được làm đổi request, images, factors hoặc reports query."""
    def test_future_poison_only_changes_evaluation_not_forecast_inputs(self) -> None:
        before, after = run_graph("vi"), run_graph("vi", poison=True)
        for key in ("clients", "stages", "inputs", "reports", "alpha"):
            self.assertEqual(before[key], after[key], key)
        self.assertNotEqual(before["summary"]["test_points"][0]["net_return"],
                            after["summary"]["test_points"][0]["net_return"])
        self.assertEqual(before["stages"], ["indicator", "pattern", "trend", "alpha", "decision", "decision"])
        self.assertEqual(before["inputs"][0]["rows"], 600)
        self.assertEqual(before["alpha"][0]["sentiment_data"]["n_articles_used"], 8)


if __name__ == "__main__":
    unittest.main()
