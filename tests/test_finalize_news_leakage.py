"""Kiểm future/undated/revision/availability với snapshot tin FIN05."""
from copy import deepcopy
import unittest

from test_finalize_news import NewsFixture


class FinalizeNewsLeakageTests(NewsFixture):
    def test_future_article_content_score_and_id_do_not_change_prefix_snapshot(self) -> None:
        past = [self.row(i) for i in range(3)]
        future = self.row(9, published_at="2026-07-03T09:00:00+07:00", available_at="2026-07-03T10:00:00+07:00")
        expected = self.news(past).snapshot("FPT", "2026-07-02")
        future.update(content="Future poison", numeric_score=float("nan"), article_id="poison")
        self.assertEqual(expected, self.news(past+[future]).snapshot("FPT", "2026-07-02"))

    def test_later_revision_does_not_replace_historical_content(self) -> None:
        old = self.row(1)
        future = self.row(2, source_url_or_archive_id=old["source_url_or_archive_id"],
                          available_at="2026-07-03T10:00:00+07:00")
        self.assertEqual(self.news([old]).snapshot("FPT", "2026-07-02"),
                         self.news([old, future]).snapshot("FPT", "2026-07-02"))
        future["evidence_id"] = None
        self.assertEqual(self.news([]).snapshot("FPT", "2026-07-02"),
                         self.news([future]).snapshot("FPT", "2026-07-02"))

    def test_same_day_after_1530_and_timezone_conversion_are_enforced(self) -> None:
        on_time = self.row(1, available_at="2026-07-02T08:30:00+00:00")
        late = self.row(2, available_at="2026-07-02T08:30:01+00:00")
        news = self.news([on_time, late])
        data, _ = news.get_sentiment_at("FPT", "2026-07-02")
        self.assertEqual(data["verified_article_count"], 1)
        self.assertEqual(news.audit_at("FPT", "2026-07-02")[0]["reason"], "REVISION_AFTER_CUTOFF")

    def test_day_only_is_next_calendar_day_with_proof_and_undated_is_excluded(self) -> None:
        day = self.row(1, published_at="2026-07-02", publication_precision="day",
                       available_at="2026-07-03T00:00:00+07:00")
        unknown = {**day, "published_at": None, "content": "Không ngày", "numeric_score": 999.}
        news = self.news([day, unknown])
        self.assertEqual(news.get_sentiment_at("FPT", "2026-07-02")[0]["verified_article_count"], 0)
        self.assertEqual(news.get_sentiment_at("FPT", "2026-07-03")[0]["verified_article_count"], 1)
        early = self.row(2, published_at="2026-07-02", publication_precision="day", available_at="2026-07-02T10:00:00+07:00")
        with self.assertRaises(ValueError):
            self.news([early]).snapshot("FPT", "2026-07-02")

    def test_missing_proof_never_uses_score_and_naive_or_prepublication_times_fail(self) -> None:
        row = self.row(1)
        unverified = {**row, "evidence_id": None, "numeric_score": 999., "content": "Không được đọc score"}
        data, _ = self.news([unverified]).get_sentiment_at("FPT", "2026-07-02")
        self.assertEqual(data["missing_reason"], "UNVERIFIED_AVAILABILITY")
        self.assertIsNone(data["main_sentiment"]["avg_score"])
        for available in ("2026-06-30T10:00:00", "2026-06-28T10:00:00+07:00"):
            bad = self.row(2, available_at=available)
            with self.assertRaises(ValueError):
                self.news([bad]).snapshot("FPT", "2026-07-02")

    def test_collection_after_cutoff_is_allowed_only_for_earlier_witnessed_content(self) -> None:
        row = self.row(1)
        self.assertEqual(self.news([row]).get_sentiment_at("FPT", "2026-07-02")[0]["verified_article_count"], 1)
        early = deepcopy(row)
        early["collected_at"] = "2026-06-28T09:00:00+07:00"
        with self.assertRaises(ValueError):
            self.news([early]).snapshot("FPT", "2026-07-02")

    def test_archive_observed_after_cutoff_cannot_backdate_availability(self) -> None:
        row = self.row(1, witnessed_at="2026-07-03T10:00:00+07:00")
        with self.assertRaises(ValueError):
            self.news([row]).snapshot("FPT", "2026-07-02")


if __name__ == "__main__":
    unittest.main()
