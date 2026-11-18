"""Poison giá tương lai, availability và sự kiện không được vượt rào PIT FIN04."""
from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from core.finalize_price_audit import session_cycle, validate_prefix_availability, visible_event_dates
from test_execution_prices import fixture_frame


class FinalizePriceLeakageTests(unittest.TestCase):
    """Metadata fixture chỉ kiểm validator thời gian; không chứng nhận vendor lịch sử."""
    def test_future_prices_and_future_metadata_do_not_rewrite_visible_prefix(self) -> None:
        frame = fixture_frame()
        availability = {str(d.date()):str(d.date())+"T15:30:00+07:00" for d in frame.Datetime}
        closed = {str(d.date()):str(d.date())+"T15:00:00+07:00" for d in frame.Datetime}
        expected = validate_prefix_availability(frame,"2022-06-10",availability,session_close_at=closed)
        frame["Volume"] = frame.Volume.astype(object)
        frame.loc[2:,["Open","High","Low","Close","Volume"]] = np.inf
        availability["2022-06-13"] = "not-a-timestamp"
        frame["closePriceAdjusted"] = -1e30
        closed["2022-06-13"] = "not-a-timestamp"
        actual = validate_prefix_availability(frame,"2022-06-10",availability,session_close_at=closed)
        pd.testing.assert_frame_equal(expected,actual)
        self.assertNotIn("closePriceAdjusted",actual)

    def test_missing_future_early_or_naive_availability_is_rejected(self) -> None:
        frame = fixture_frame()
        good = {str(d.date()):str(d.date())+"T15:30:00+07:00" for d in frame.Datetime}
        closed = {str(d.date()):str(d.date())+"T15:00:00+07:00" for d in frame.Datetime}
        for changed in ({}, {**good,"2022-06-10":"2022-06-11T00:00:00+07:00"},
            {**good,"2022-06-10":"2022-06-10T14:59:59+07:00"},
            {**good,"2022-06-10":"2022-06-10T15:30:00"}):
            with self.assertRaises(ValueError):
                validate_prefix_availability(frame,"2022-06-10",changed,session_close_at=closed)
        self.assertEqual(len(validate_prefix_availability(frame,"2022-06-10",closed,session_close_at=closed)),2)
        for bad_calendar in ({},{**closed,"2022-06-10":"2022-06-09T15:00:00+07:00"}):
            with self.assertRaises(ValueError):
                validate_prefix_availability(frame,"2022-06-10",good,session_close_at=bad_calendar)

    def test_future_and_undated_events_have_explicit_reasons_and_cannot_enter_known_barriers(self) -> None:
        known = {"id":"known","publicDate":"2022-06-08T00:00:00","exrightDate":"2022-06-13"}
        future = {"id":"future","publicDate":"2022-06-10T00:00:00","exrightDate":"2022-06-13"}
        undated = {"id":"undated","exrightDate":"2022-06-13"}
        dates,excluded = visible_event_dates([known,future,undated],"2022-06-10")
        self.assertEqual(dates,["2022-06-13"])
        self.assertEqual({e["reason"] for e in excluded},{"PUBLICATION_AFTER_CUTOFF","UNDATED_PUBLICATION"})
        dates_after,_ = visible_event_dates([known,{**future,"exrightDate":"2099-01-01"},undated],"2022-06-10")
        self.assertEqual(dates,dates_after)

    def test_planned_session_dates_do_not_read_future_quote_values(self) -> None:
        frame = fixture_frame();calendar = pd.DatetimeIndex(frame.Datetime)
        expected = session_cycle(frame,calendar,"2022-06-09")
        frame.loc[1:,["Open","High","Low","Close","Volume"]] = np.nan
        self.assertEqual(session_cycle(frame,calendar,"2022-06-09"),expected)


if __name__ == "__main__":
    unittest.main()
