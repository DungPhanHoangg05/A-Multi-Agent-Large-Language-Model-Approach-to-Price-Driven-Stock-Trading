"""Đối chứng FIN08 qua Flask/runner thật, chặn mạng và outcome nghiên cứu."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from flask import Flask
import pandas as pd

from core.finalize_serving_profile import LIVE_CAPTURE, PENDING, VERSION
from core.finalize_serving_resources import FinalizedResources
from core.serving_live.cafef_news import CapturedNews, capture_live_news, capture_news
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

    def service(self, *, fixture: bool, hosted: bool = False, snapshots: Snapshots | None = None) -> Service:
        """Giữ các phương thức thực của service, chỉ đưa transport fixture vào."""
        options = {"clock": self.clock, "sender_factory": lambda _: self.sender, "finalize_fixture": fixture,
                   "finalize_hosted": hosted}
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

    def test_caller_without_hosted_access_stays_blocked(self) -> None:
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
        self.assertEqual(catalog["default_profile"], VERSION)
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
        self.assertEqual(result["execution_scope"], "OFFLINE_FIXTURE")
        self.assertEqual(len(result["snapshots"]), 1)
        self.assertEqual(len(result["rows"]), 10)
        self.assertEqual(sum(k == "vision" for k, _ in self.sender.calls), 2)
        self.assertEqual({r["metric_reason"] for r in result["rows"]}, {"OFFLINE_FIXTURE_OUTCOME_LOCKED"})
        self.assertTrue(all(r["net_return_pct"] is None for r in result["rows"]))
        self.assertEqual(result["identity"]["method_profiles"]["original_fix"], "original_fix_causal_serving_v1")
        view = next(iter(result["snapshots"].values()))
        self.assertNotIn("live_news", view["payload"]["sentiment_data"])
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

    def test_hosted_backtest_opens_pinned_outcome_after_shared_forecasts(self) -> None:
        service = self.service(fixture=False, hosted=True)
        base = "/api/serving/v1"
        value = request("backtest", "2026-07-02", ["original_fix", "bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL"])
        with patch.dict(self.app.config, {"SERVING_API_KEY_PROVIDER": lambda: ""}):
            blocked = self.client.post(base+"/preflight", json=value).get_json()
            self.assertEqual([row["code"] for row in blocked["blockers"]], ["CREDENTIAL_MISSING"])
        preflight = self.client.post(base+"/preflight", json=value).get_json()
        self.assertTrue(preflight["run_enabled"], preflight)
        self.assertEqual(preflight["execution_scope"], "HOSTED")
        self.assertEqual(self.sender.calls, [])
        posted = self.client.post(base+"/jobs", json=value)
        self.assertEqual(posted.status_code, 202, posted.get_json())
        self.join(service)
        path = base+"/jobs/"+posted.get_json()["run_id"]
        result = self.client.get(path).get_json()
        self.assertEqual(result["state"], "completed", result.get("error"))
        self.assertEqual(result["execution_scope"], "HOSTED")
        self.assertEqual(len(result["snapshots"]), 1)
        self.assertEqual(len(result["rows"]), 8)
        self.assertEqual(result["outcome_points"], 1)
        self.assertEqual(sum(k == "vision" for k, _ in self.sender.calls), 2)
        self.assertTrue(all(row["net_return_pct"] == 0 for row in result["rows"]))
        exported = self.client.get(path+"/export").get_json()
        self.assertEqual(exported["evaluation_status"], "COMPLETE", exported)
        self.assertEqual(exported["provenance"]["execution_scope"], "HOSTED")
        self.assertTrue(all(row["exit_date"] and row["label_net"] is not None for row in exported["predictions"]))

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
            return market.iloc[223:].copy(deep=True)

        snapshots = Snapshots(self.temp/"capture", prices=index, news=lambda *_: self.fail("Tin legacy"),
                              now=lambda: datetime(2026, 10, 2, 10, tzinfo=ZONE))
        self.service(fixture=False, hosted=True)
        live_service = self.service(fixture=False, hosted=True, snapshots=snapshots)
        base = "/api/serving/live/v1"
        def article(identifier: int, when: str, title: str = "FPT công bố kết quả kinh doanh") -> str:
            return (f'<div><h3><a href="/ket-qua-{identifier}.chn">{title}</a></h3>'
                    f'<span class="time">{when}</span></div>')

        listing = "".join([article(123456, "02/10/2026 09:00"), article(123457, "02/10/2026 11:00"),
            article(123458, "02/10/2026"), article(123459, ""), article(123460, "01/10/2026", "HPG tăng sản lượng"),
            article(123461, "01/06/2026 09:00")])
        peer_listing = "".join([article(223456, "02/10/2026 08:00", "CMG công bố doanh thu"),
            article(223457, "01/10/2026 12:00", "CMG ký kết hợp đồng"), article(223458, "02/10/2026 12:00", "CMG sắp tới")])
        news_inputs = []
        news_urls = []

        def news_fetch(url: str) -> SimpleNamespace:
            news_urls.append(url)
            return SimpleNamespace(text=listing if url.endswith("/fpt.html") else peer_listing)

        def news_score(value: str) -> dict:
            news_inputs.append(value)
            return {"label": "positive", "numeric_score": .75 if value.startswith("FPT") else .5,
                    "confidence": .75, "scorer": "test-scorer",
                    "scorer_backend": "fixture", "is_fallback": False}

        def collect(symbol: str, when: datetime) -> tuple[list[dict], dict, dict]:
            return capture_live_news(symbol, when, fetch=news_fetch, score=news_score, directory=lambda: (
                {"FPT": "FPT", "CMG": "CMC"}, {"FPT": {3: "9530"}, "CMG": {3: "9530"}}))

        with patch("core.finalize_live_capture.raw_pages", return_value=(source.to_dict("records"), [],
                   {"prices": [{"response_sha256": "1"*64}], "events": [{"response_sha256": "2"*64}]})) as fetch, patch(
                   "core.finalize_live_capture.capture_live_news", side_effect=collect) as capture_articles:
            captured = self.client.post(base+"/snapshot", json={"symbol": "FPT", "profile": VERSION})
            self.assertEqual(captured.status_code, 200, captured.get_json())
            capture = captured.get_json()
            fetch.assert_called_once_with("FPT", "2020-01-02", cutoff)
            capture_articles.assert_called_once_with("FPT", datetime(2026, 10, 2, 10, tzinfo=ZONE))
        self.assertEqual(capture["capture_version"], LIVE_CAPTURE)
        self.assertEqual(capture["live_news"]["status"], "AVAILABLE")
        value = {"version": "variant_serving_live_v1", "snapshot_id": capture["snapshot_id"],
                 "request": request("compare", cutoff, ["original_fix", "MT_BICL"])}
        with patch("agents.sentiment_agent._get", side_effect=AssertionError("Đọc lại CafeF")), patch(
                "agents.sentiment_agent._score_text", side_effect=AssertionError("Chấm lại tin")), patch.object(
                self.sender, "send", wraps=self.sender.send) as transport:
            checked = self.client.post(base+"/preflight", json=value).get_json()
            self.assertTrue(checked["run_enabled"], checked)
            posted = self.client.post(base+"/jobs", json=value)
            self.assertEqual(posted.status_code, 202, posted.get_json())
            self.join(live_service)
        decision_content = [call.args[0]["messages"][0]["content"] for call in transport.call_args_list
                            if "response_format" in call.args[0]]
        self.assertTrue(any("+0.750000" in prompt for prompt in decision_content))
        self.assertTrue(all(news_inputs[0] not in prompt for prompt in decision_content))
        path = base+"/jobs/"+posted.get_json()["run_id"]
        result = self.client.get(path+"/export").get_json()
        self.assertEqual(result["state"], "completed", result.get("error"))
        self.assertEqual(result["execution_scope"], "HOSTED")
        self.assertEqual(seen, ["VNINDEX"])
        self.assertIn(LIVE_CAPTURE, result["identity"]["config"]["provider_version"])
        self.assertEqual(result["outcome_points"], 0)
        self.assertEqual(sum(k == "vision" for k, _ in self.sender.calls), 2)
        payload = result["snapshots"]["FPT-"+cutoff]
        self.assertEqual(payload["payload"]["price_prefix"]["Datetime"][-1], cutoff)
        self.assertEqual(payload["provenance"]["source_sha256"], capture["snapshot_id"])
        sentiment = payload["payload"]["sentiment_data"]
        self.assertEqual(sentiment["main_sentiment"], {"article_count": 1, "avg_score": .75})
        self.assertEqual(sentiment["live_news"], capture["live_news"])
        rows = sentiment["scored_articles"]
        self.assertEqual([row["published_at"] for row in rows], ["2026-10-02T09:00:00+07:00"])
        self.assertEqual(rows[0]["source_url_or_archive_id"], "https://cafef.vn/ket-qua-123456.chn")
        self.assertNotIn("score_input", rows[0])
        self.assertEqual(sentiment["related_companies"], ["CMG"])
        peer = sentiment["related_sentiment"]["CMG"]
        self.assertEqual(peer["article_count"], 2)
        self.assertEqual(peer["industry_code"], "9530")
        self.assertAlmostEqual(sentiment["sentiment_norm"]["rel_sentiment"], .25)
        self.assertIsNone(sentiment["sentiment_norm"]["z_score"])
        self.assertEqual([item["published_at"] for item in peer["scored_articles"]],
                         ["2026-10-02T08:00:00+07:00", "2026-10-01T12:00:00+07:00"])
        self.assertIn("+0.750000", payload["payload"]["sentiment_report"])
        self.assertEqual(news_urls, ["https://cafef.vn/fpt.html", "https://cafef.vn/cmg.html"])
        self.assertEqual(news_inputs, ["FPT công bố kết quả kinh doanh", "CMG công bố doanh thu", "CMG ký kết hợp đồng"])
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
        self.assertEqual(record["news"][0]["score_input"], news_inputs[0])
        self.assertEqual(record["news"][0]["score_input_sha256"], digest(news_inputs[0]))
        future_news = deepcopy(record)
        future_news["news"][0]["published_at"] = future_news["news"][0]["available_at"] = "2026-10-02T11:00:00+07:00"
        with self.assertRaisesRegex(ValueError, "CafeF"):
            FinalizedResources(ROOT, future_news, digest(future_news))
        peer_future = deepcopy(record)
        peer_row = peer_future["related_news"]["CMG"]["articles"][0]
        peer_row["published_at"] = peer_row["available_at"] = "2026-10-02T11:00:00+07:00"
        with self.assertRaisesRegex(ValueError, "CafeF"):
            CapturedNews(peer_future)
        previous = deepcopy(record)
        previous.pop("related_news")
        previous["live_news"]["version"] = "cafef_live_sentiment_v1"
        old_data = CapturedNews(previous).snapshot("FPT", cutoff)["payload"]["sentiment_data"]
        self.assertNotIn("sentiment_norm", old_data)
        self.assertEqual(old_data["main_sentiment"], sentiment["main_sentiment"])
        record_with_new_text = deepcopy(record)
        record_with_new_text["news"][0]["score_input"] += " sửa sau"
        with self.assertRaisesRegex(ValueError, "CafeF"):
            CapturedNews(record_with_new_text)
        self.assertEqual(record["index"]["Datetime"], market.Datetime.dt.strftime("%Y-%m-%d").tolist())
        self.assertEqual(record["source_receipts"]["index_prefix"], resources.pins[resources.acceptance["calendar"]])
        changed_index = deepcopy(record)
        changed_index["index"]["Close"][-2] += 1
        with self.assertRaisesRegex(ValueError, "overlap"):
            FinalizedResources(ROOT, changed_index, digest(changed_index))
        record["prices"]["Reference"] = [int(v) for v in record["prices"]["Reference"]]
        with self.assertRaisesRegex(ValueError, "overlap"):
            FinalizedResources(ROOT, record, digest(record))

    def test_live_news_distinguishes_unreachable_cafef_from_empty_listing(self) -> None:
        """Lỗi mạng và trang rỗng không sinh điểm trung lập giả."""
        as_of = datetime(2026, 10, 2, 10, tzinfo=ZONE)
        for response, status in ((None, "CAFEF_UNAVAILABLE"), (SimpleNamespace(text="<main></main>"), "NO_ELIGIBLE_NEWS")):
            with self.subTest(status=status):
                rows, metadata = capture_news("FPT", as_of, fetch=lambda _: response,
                                              score=lambda _: self.fail("Không có bài để chấm"))
                record = {"live_news": metadata, "captured_at": as_of.isoformat(), "news": rows,
                          "symbol": "FPT", "cutoff": "2026-10-01"}
                payload = CapturedNews(record).snapshot("FPT", "2026-10-01")["payload"]["sentiment_data"]
                self.assertEqual(payload["missing_reason"], status)
                self.assertIsNone(payload["main_sentiment"]["avg_score"])
                self.assertEqual(payload["scored_articles"], [])

    def test_live_news_normalizes_actual_article_scores_and_checks_mention(self) -> None:
        """Tên thương hiệu có chứng cứ; điểm tương đối dùng mã đủ bài, z-score dùng điểm gốc."""
        def listing(*rows: tuple[int, str, str]) -> SimpleNamespace:
            return SimpleNamespace(text="".join(
                f'<div><h3><a href="/tin-{number}.chn">{title}</a></h3><span class="time">{when}</span></div>'
                for number, title, when in rows))

        responses = {
            "fpt": listing((123456, "FPT hợp tác với FPT Retail", "02/10/2026 09:00"),
                           (123457, "FPT công bố kết quả kinh doanh", "02/09/2026 09:00"),
                           (123458, "FPT chốt phương án cổ tức", "03/08/2026 09:00")),
            "frt": listing((223456, "FRT công bố doanh thu", "02/10/2026 09:00"),
                           (223457, "FRT ký kết hợp đồng", "01/10/2026 12:00")),
            "cmg": listing((323456, "CMG ước tính lợi nhuận", "01/10/2026 12:00")),
        }

        def score(text: str) -> dict:
            value = {"FPT hợp tác với FPT Retail": 1., "FPT công bố kết quả kinh doanh": 0.,
                     "FPT chốt phương án cổ tức": -1.}.get(text, .2)
            return {"label": "neutral", "numeric_score": value, "confidence": 1., "scorer": "fixture",
                    "scorer_backend": "fixture", "is_fallback": False}

        as_of = datetime(2026, 10, 2, 10, tzinfo=ZONE)
        rows, meta, related = capture_live_news("FPT", as_of, score=score,
            fetch=lambda url: responses.get(url.rsplit("/", 1)[-1].removesuffix(".html")),
            directory=lambda: ({"FPT": "FPT", "FRT": "FPT Retail", "CMG": "CMC"},
                               {"FPT": {3: "9530"}, "CMG": {3: "9530"}}))
        record = {"news": rows, "live_news": meta, "related_news": related, "symbol": "FPT",
                  "captured_at": as_of.isoformat(), "cutoff": "2026-10-01"}
        sentiment = CapturedNews(record).snapshot("FPT", "2026-10-01")["payload"]["sentiment_data"]
        norm = sentiment["sentiment_norm"]
        self.assertAlmostEqual(sentiment["main_sentiment"]["avg_score"], 3 / 7)
        self.assertAlmostEqual(norm["z_score"], (3 / 7) / ((2 / 3)**.5 + .001))
        self.assertFalse(norm["is_reliable"])
        self.assertAlmostEqual(norm["rel_sentiment"], 3 / 7 - .2)
        self.assertEqual(norm["relative_peer_count"], 1)
        self.assertFalse(sentiment["related_sentiment"]["CMG"]["in_relative"])
        self.assertEqual(related["FRT"]["mention_urls"], ["https://cafef.vn/tin-123456.chn"])
        related["FRT"]["mention_urls"][0] = "https://cafef.vn/tin-123457.chn"
        with self.assertRaisesRegex(ValueError, "CafeF"):
            CapturedNews(record)

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
