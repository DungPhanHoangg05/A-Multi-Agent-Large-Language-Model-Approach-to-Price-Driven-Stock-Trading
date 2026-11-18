"""Đối soát REST/đơn vị/oracle và gate nguồn FIN04 bằng fixture hoặc byte đã khóa."""
from __future__ import annotations

from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import pandas as pd

from core.backtest_engine import compute_round_trip_net_return
from core.finalize_price_audit import H02, Sources, audit_prices, raw_prices, require_price_gate, session_cycle
from core.unified_contracts import digest, json_bytes
from core.unified_protocol import binding
from test_execution_prices import fixture_frame, raw_records

ROOT = Path(__file__).resolve().parents[1]


class FinalizePriceUnitTests(unittest.TestCase):
    """Không biến checksum hoặc metadata vendor thành chứng nhận as-published."""

    def test_nine_symbol_raw_units_ignore_all_adjusted_fields(self) -> None:
        for symbol in ("FPT", "BHN", "CMG", "HVN", "MBB", "MWG", "VCB", "VJC", "VNM"):
            rows = raw_records()
            for row in rows:
                row.update(ticker=symbol, openPriceAdjusted=1e30, closePriceAdjusted=-1e30)
            frame = raw_prices(rows, symbol)
            self.assertEqual(float(frame.Open.iloc[0]), 100.)
            self.assertEqual(float(frame.Close.iloc[0]), 102.)
            self.assertEqual(float(frame.Volume.iloc[0]), 1000.)
            self.assertNotIn("openPriceAdjusted", frame)
            self.assertEqual(compute_round_trip_net_return(frame.Open.iloc[1],frame.Close.iloc[3]),
                             compute_round_trip_net_return(100_000.,102_000.))
        json_bytes(frame.drop(columns="Datetime").to_dict(orient="list"))

    def test_duplicate_date_mixed_symbol_or_adjusted_only_is_rejected(self) -> None:
        adjusted = raw_records()
        for row in adjusted:
            row.pop("openPrice")
        mixed = raw_records(); mixed[0]["ticker"] = "VNM"
        for rows in (adjusted,mixed,raw_records()+raw_records()[:1]):
            with self.assertRaises(ValueError):
                raw_prices(rows,"FPT")

    def test_calendar_horizon_uses_sessions_and_rejects_gaps_and_duplicates(self) -> None:
        frame = fixture_frame()
        calendar = pd.DatetimeIndex(frame.Datetime)
        self.assertEqual(session_cycle(frame,calendar,"2022-06-09"),
                         {"entry_date":"2022-06-10","exit_date":"2022-06-14"})
        for data,dates,cutoff in ((frame.drop(index=2),calendar,"2022-06-09"),
            (frame,calendar,"2022-06-12"),(frame,calendar,"2022-06-15"),
            (frame,calendar.append(calendar[:1]),"2022-06-09")):
            with self.assertRaises(ValueError):
                session_cycle(data,dates,cutoff)

    def test_rest_pages_reconstruct_without_network_and_reject_resigned_page_drift(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = Sources.__new__(Sources)
            source.root,source.expected,source.bindings = root,{},{}
            for number,row in enumerate(raw_records()[:2]):
                name = H02+f"responses/FPT_prices_{number}.json.gz"
                raw = json_bytes({"successful":True,"code":0,"data":{"number":number,"size":1,
                    "totalPages":2,"totalElements":2,"last":number==1,"content":[row]}})
                url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/FPT/price-history?fromDate=20200101&toDate=20260930&page={number}&size=1000"
                meta = {"url":url,"http_status":200,"response_sha256":hashlib.sha256(raw).hexdigest(),
                        "retrieved_at_utc":"2026-11-08T03:00:00+00:00"}
                for path,data in ((name,gzip.compress(raw,mtime=0)),(name.removesuffix('.gz')+'.meta.json',json_bytes(meta))):
                    (root/path).parent.mkdir(parents=True,exist_ok=True)
                    (root/path).write_bytes(data)
                    source.expected[path] = binding(root,path)
            with patch("requests.sessions.Session.request",side_effect=AssertionError("Không được gọi mạng")):
                rows,receipts = source.pages("FPT","prices")
                self.assertEqual(rows,raw_records()[:2]);self.assertEqual(len(receipts),2)
            path = H02+"responses/FPT_prices_1.json.gz"
            payload = json.loads(gzip.decompress((root/path).read_bytes()))
            payload["data"]["size"] = 2
            changed = json_bytes(payload)
            (root/path).write_bytes(gzip.compress(changed,mtime=0));source.expected[path]=binding(root,path)
            meta_path = path.removesuffix('.gz')+'.meta.json'
            meta = json.loads((root/meta_path).read_bytes());meta["response_sha256"]=hashlib.sha256(changed).hexdigest()
            (root/meta_path).write_bytes(json_bytes(meta));source.expected[meta_path]=binding(root,meta_path)
            with self.assertRaisesRegex(ValueError,"phân trang"):
                source.pages("FPT","prices")


class FinalizePriceCorpusTests(unittest.TestCase):
    """Kiểm corpus thực chỉ bằng hash/quote/bank trưởng thành, không tính outcome query."""
    @classmethod
    def setUpClass(cls) -> None:
        """Đọc một lần để các test không khôi phục hoặc sửa evidence frozen."""
        with patch("requests.sessions.Session.request",side_effect=AssertionError("Không được gọi API")):
            cls.report = audit_prices(ROOT)

    def test_all_102_cycles_and_852_bank_labels_are_audited_but_not_admitted(self) -> None:
        report = self.report
        self.assertEqual(len(report["symbols"]),9)
        self.assertEqual(len(report["points"]),102)
        self.assertEqual(report["calendar"]["query_cycles_verified"],102)
        self.assertEqual(sum(row["episodes"] for row in report["bank_oracle"]),852)
        self.assertEqual(sum(row["oracle_mismatches_above_1e_10"] for row in report["bank_oracle"]),0)
        self.assertTrue(all(not any(row["bank_h02_quote_difference_counts"].values()) for row in report["bank_oracle"]))
        self.assertTrue(all(not p["admitted"] for p in report["points"]))
        self.assertFalse(report["query_outcomes_computed"])
        self.assertFalse(report["dataset_replaced"])
        self.assertEqual(report["admitted_points"],0)
        self.assertEqual(report["price_source_gate"],"BLOCKED_PIT_PROVENANCE")
        self.assertTrue(all(row["blockers"] for row in report["points"]))
        json_bytes(report)

    def test_known_actions_are_reported_without_reselecting_the_locked_cohort(self) -> None:
        report = self.report
        flagged = [p for p in report["points"] if p["known_event_dates_inside_holding"]]
        self.assertEqual(len(flagged),5)
        self.assertTrue(all("KNOWN_CORPORATE_ACTION_DURING_HOLDING" in p["blockers"] for p in flagged))
        self.assertEqual(len({p["id"] for p in report["points"]}),102)

    def test_legacy_newline_drift_is_reported_and_original_bytes_remain_unchanged(self) -> None:
        self.assertEqual(len(self.report["legacy_manifest_deltas"]),8)
        self.assertTrue(all(row["newline_only"] for row in self.report["legacy_manifest_deltas"]))
        for row in self.report["legacy_manifest_deltas"]:
            self.assertEqual(binding(ROOT,row["path"]),row["actual"])
            self.assertEqual(hashlib.sha256((ROOT/row["restorable_from"]).read_bytes()).hexdigest(),row["expected_sha256"])

    def test_resigned_pass_or_changed_denominator_cannot_unlock_source_gate(self) -> None:
        for field,value in (("price_source_gate","PASS"),("admitted_points",102)):
            changed = deepcopy(self.report);changed[field]=value
            with patch("core.finalize_price_audit.audit_prices",return_value=self.report):
                with self.assertRaises(ValueError):require_price_gate(ROOT,changed)
        with patch("core.finalize_price_audit.audit_prices",return_value=self.report):
            with self.assertRaises(ValueError):require_price_gate(ROOT,self.report)
        self.assertNotEqual(digest(changed),digest(self.report))


if __name__ == "__main__":
    unittest.main()
