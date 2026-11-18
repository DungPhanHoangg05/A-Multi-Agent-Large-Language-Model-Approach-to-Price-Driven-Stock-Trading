"""Đối chứng FIN08 qua Flask/runner thật, chặn mạng và outcome nghiên cứu."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from flask import Flask
import pandas as pd

from core.finalize_serving_profile import LIVE_CAPTURE, PENDING, VERSION
from core.finalize_serving_resources import FinalizedResources
from core.serving_live.service import LiveService
from core.serving_live.snapshots import Snapshots, ZONE
from core.serving_runtime.resources import default_models
from core.serving_runtime.service import Service
from core.unified_contracts import digest
from scripts.finalize_serving_preview import FixtureClock, FixtureSender
from utils.serving_live_web import live
from utils.serving_web import serving

ROOT = Path(__file__).resolve().parents[1]
KEY = "offline-finalize-fixture"


def request(mode: str, cutoff: str, variants: list[str], *, repeats: int = 1) -> dict:
    """Body tường minh dùng cả CLI và API preview."""
    return {"version": VERSION, "mode": mode, "variant_ids": variants, "symbols": ["FPT"],
            "start_date": cutoff, "end_date": cutoff, "timeframe": "1d", "language": "en",
            "models": default_models(), "repeats": repeats}


class FinalizedServingTests(unittest.TestCase):
    """Chạy normal caller với fixture transport, không thay production provider."""
    def setUp(self) -> None:
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.temp = Path(temporary.name)
        self.clock = FixtureClock()
        self.sender = FixtureSender(self.clock)
        self.app = Flask(__name__)
        self.app.config["SERVING_API_KEY_PROVIDER"] = lambda: KEY
        self.app.register_blueprint(serving)
        self.app.register_blueprint(live)
        self.client = self.app.test_client()

    def service(self, *, fixture: bool, snapshots: Snapshots | None = None) -> Service:
        """Giữ các phương thức thực của service, chỉ đưa transport fixture vào."""
        options = {"clock": self.clock, "sender_factory": lambda _: self.sender, "finalize_fixture": fixture}
        if snapshots is None:
            service = Service(ROOT, state_root=self.temp/"asof", **options)
            self.app.config["SERVING_SERVICE"] = service
        else:
            service = LiveService(ROOT, state_root=self.temp/"live", snapshots=snapshots, **options)
            self.app.config["SERVING_LIVE_SERVICE"] = service
        self.addCleanup(self.join, service)
        return service

    def join(self, service: Service) -> None:
        for worker in list(service.tasks.values()):
            worker.join(timeout=90)
            self.assertFalse(worker.is_alive())

    def test_opt_in_preflight_is_hosted_blocked_and_legacy_default_retained(self) -> None:
        self.service(fixture=False)
        base = "/api/serving/v1"
        value = request("analyze", "2026-07-01", ["original_fix"])
        result = self.client.post(base+"/preflight", json=value).get_json()
        self.assertEqual(result["version"], VERSION)
        self.assertEqual(result["points"][0]["id"], "FPT-2026-07-01")
        self.assertEqual([r["code"] for r in result["blockers"]], [PENDING])
        self.assertEqual(self.client.post(base+"/jobs", json=value).status_code, 409)
        self.assertEqual(self.sender.calls, [])
        catalog = self.client.get(base+"/registry").get_json()
        self.assertEqual(catalog["default"], "original_fix")
        self.assertEqual(catalog["legacy"]["contract"], "legacy_native_unchanged")

    def test_backtest_job_uses_causal_native_shared_checkpoint_and_locked_outcome(self) -> None:
        service = self.service(fixture=True)
        base = "/api/serving/v1"
        value = request("backtest", "2026-07-01", ["original_fix", "bayesian_v1", "MT_BICL"], repeats=2)
        with patch("agents.alpha_agent.create_alpha_agent", side_effect=AssertionError("Alpha legacy")), patch(
                "core.finalize_serving_resources.FinalizedResources.outcome", side_effect=AssertionError("Đọc outcome thật")):
            posted = self.client.post(base+"/jobs", json=value)
            self.assertEqual(posted.status_code, 202, posted.get_json())
            self.join(service)
        path = base+"/jobs/"+posted.get_json()["run_id"]
        result = self.client.get(path).get_json()
        self.assertEqual(result["state"], "completed", result.get("error"))
        self.assertEqual(len(result["snapshots"]), 1)
        self.assertEqual(len(result["rows"]), 10)
        self.assertEqual(sum(k == "vision" for k, _ in self.sender.calls), 2)
        self.assertEqual({r["metric_reason"] for r in result["rows"]}, {"OFFLINE_FIXTURE_OUTCOME_LOCKED"})
        self.assertTrue(all(r["net_return_pct"] is None for r in result["rows"]))
        self.assertEqual(result["identity"]["method_profiles"]["original_fix"], "original_fix_causal_serving_v1")
        view = next(iter(result["snapshots"].values()))
        projection = view["payload"]["causal_alpha"]["projection"]
        self.assertEqual(view["payload"]["alpha_factors"], projection["factors"])
        details = result["policy_details"]
        self.assertTrue(all(details[s]["context"]["trace"]["alpha_projection_sha256"] == projection["projection_sha256"]
                            for s in details if s.endswith("/original_fix")))
        sent = len(self.sender.calls)
        exported = self.client.get(path+"/export").get_json()
        self.assertEqual(exported["provenance"]["identity_sha256"], result["identity_sha256"])
        self.assertEqual(exported["coverage"]["unavailable_outcomes"], result["outcome_unavailable_points"])
        self.assertEqual(exported["evaluation_status"], "UNAVAILABLE_EXECUTION_OUTCOMES")
        self.assertEqual(exported["summary"], [])
        self.assertEqual(len(self.sender.calls), sent)
        self.assertEqual(self.app.test_client().get(path).status_code, 404)
        self.assertNotIn(KEY, json.dumps(result))

    def test_live_capture_compatible_suffix_and_owner_bound_replay(self) -> None:
        resources = FinalizedResources(ROOT)
        market = resources.calendar[["Datetime", "Close"]].copy(deep=True)
        cutoff = "2026-10-01"
        market.loc[len(market)] = [pd.Timestamp(cutoff), float(market.Close.iloc[-1])]
        stock = resources.stock("FPT")
        suffix = stock.iloc[-1:].copy()
        suffix["Datetime"] = pd.Timestamp(cutoff)
        suffix["Reference"] = stock.Close.iloc[-1]
        stock = pd.concat((stock, suffix), ignore_index=True)
        source = stock.rename(columns={"Datetime": "tradingDate", "Open": "openPrice", "High": "highestPrice",
            "Low": "lowestPrice", "Close": "closePrice", "Volume": "totalMatchVolume", "Reference": "referencePrice"})
        source["tradingDate"] = source.tradingDate.dt.strftime("%Y-%m-%d")
        source["ticker"] = "FPT"
        for name in ("openPrice", "highestPrice", "lowestPrice", "closePrice", "referencePrice"):
            source[name] = source[name].mul(1000).round(7)
        seen = []
        def index(symbol: str) -> pd.DataFrame:
            seen.append(symbol)
            return market.copy(deep=True)

        snapshots = Snapshots(self.temp/"capture", prices=index, news=lambda *_: self.fail("Tin legacy"),
                              now=lambda: datetime(2026, 10, 2, 10, tzinfo=ZONE))
        self.service(fixture=True)
        live_service = self.service(fixture=True, snapshots=snapshots)
        base = "/api/serving/live/v1"
        with patch("core.finalize_live_capture.raw_pages", return_value=(source.to_dict("records"), [],
                   {"prices": [{"response_sha256": "1"*64}], "events": [{"response_sha256": "2"*64}]})) as fetch:
            captured = self.client.post(base+"/snapshot", json={"symbol": "FPT", "profile": VERSION})
            self.assertEqual(captured.status_code, 200, captured.get_json())
            capture = captured.get_json()
            fetch.assert_called_once_with("FPT", "2020-01-02", cutoff)
        self.assertEqual(capture["capture_version"], LIVE_CAPTURE)
        value = {"version": "variant_serving_live_v1", "snapshot_id": capture["snapshot_id"],
                 "request": request("compare", cutoff, ["original_fix", "MT_BICL"])}
        posted = self.client.post(base+"/jobs", json=value)
        self.assertEqual(posted.status_code, 202, posted.get_json())
        self.join(live_service)
        path = base+"/jobs/"+posted.get_json()["run_id"]
        result = self.client.get(path+"/export").get_json()
        self.assertEqual(result["state"], "completed", result.get("error"))
        self.assertEqual(seen, ["VNINDEX"])
        self.assertIn(LIVE_CAPTURE, result["identity"]["config"]["provider_version"])
        self.assertEqual(result["outcome_points"], 0)
        self.assertEqual(sum(k == "vision" for k, _ in self.sender.calls), 2)
        payload = result["snapshots"]["FPT-"+cutoff]
        self.assertEqual(payload["payload"]["price_prefix"]["Datetime"][-1], cutoff)
        self.assertEqual(payload["provenance"]["source_sha256"], capture["snapshot_id"])
        self.assertEqual(result["display_language"], "en")
        self.assertTrue(result["presentations"])
        sent = len(self.sender.calls)
        live_service.work(result["run_id"], KEY, result["owner_scope_sha256"], wait=False)
        replay = self.client.get(path+"/export").get_json()
        self.assertEqual(replay, result)
        self.assertEqual(len(self.sender.calls), sent)
        self.assertEqual(seen, ["VNINDEX"])
        self.assertEqual(self.app.test_client().post(base+"/preflight", json=value).status_code, 404)
        legacy_request = deepcopy(value)
        legacy_request["request"]["version"] = "variant_serving_v1"
        self.assertFalse(self.client.post(base+"/preflight", json=legacy_request).get_json()["run_enabled"])
        record = deepcopy(snapshots.read(capture["snapshot_id"]))
        record["prices"]["Reference"] = [int(v) for v in record["prices"]["Reference"]]
        with self.assertRaisesRegex(ValueError, "overlap"):
            FinalizedResources(ROOT, record, digest(record))

    def test_outcome_oracle_on_synthetic_cycle_preserves_costs_and_missing_volume(self) -> None:
        resources = FinalizedResources(ROOT)
        market = pd.DatetimeIndex(resources.calendar.Datetime)
        index = market.get_loc(pd.Timestamp("2026-07-01"))
        dates = market[index:index+4]
        synthetic = pd.DataFrame({"Datetime": dates, "Open": [10.]*4, "Close": [10.,10.,10.,12.],
                                  "High": [13.]*4, "Low": [9.]*4, "Volume": [100]*4, "Reference": [10.]*4})
        point = {"id": "FPT-2026-07-01", "symbol": "FPT", "cutoff": "2026-07-01"}
        label = resources.outcome(point, synthetic)
        from core.unified_experiment import validate_outcome
        validate_outcome(point, label)
        self.assertAlmostEqual(label["target"]["net_return"], 1.2*(1-.001)*(1-.0025)/((1+.001)*(1+.0025))-1)
        synthetic.loc[2, "Volume"] = 0
        self.assertEqual(resources.outcome(point, synthetic)["reason"], "NO_MATCHED_VOLUME_AT_EXECUTION")

    def test_bilingual_wire_checks_total_decision_prompt_before_reserve(self) -> None:
        from core.serving_runtime.quota import Failed
        from core.serving_runtime.transport import Calls
        calls = Calls(self.temp, "fixture", None, self.sender, lambda: None, total_prompt_guard=True)
        body = {"response_format": {}, "messages": [{"role": "user", "content": "a" * 6400},
                                                     {"role": "user", "content": "b" * 100}]}
        with self.assertRaisesRegex(Failed, "PROMPT_BUDGET_EXCEEDED"):
            calls.call("test-budget", body, "fixture")
        self.assertEqual(self.sender.calls, [])


if __name__ == "__main__":
    unittest.main()
