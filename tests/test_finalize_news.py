"""Kiểm registry archive, scorer, revision và cùng snapshot của Decision/UI."""
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from core.finalize_news import FinalizedNews, SCORER, snapshot_values
from core.finalize_news_release import check_release, prepare_corpus
from core.unified_contracts import digest, json_bytes
from core.unified_protocol import binding, read

ROOT = Path(__file__).resolve().parents[1]


class NewsFixture(unittest.TestCase):
    """Receipt synthetic chỉ mô phỏng registry đã duyệt, không chứng minh tin thị trường."""

    def setUp(self) -> None:
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.evidence: dict = {}

    def row(self, index: int, *, witnessed_at: str | None = None, **changes: object) -> dict:
        """Dựng một bản tin và receipt đã pin để kiểm chronology/content/scorer."""
        text = f"Nội dung nguồn số {index}"
        content_hash = hashlib.sha256(text.encode()).hexdigest()
        row = {"article_id": str(index), "source_url_or_archive_id": f"https://source.example/{index}",
            "content": text, "content_hash": content_hash, "score_content_hash": content_hash,
            "published_at": "2026-06-29T09:00:00+07:00", "publication_precision": "second",
            "source_timezone": "Asia/Ho_Chi_Minh", "available_at": "2026-06-30T10:00:00+07:00",
            "collected_at": "2026-11-18T10:00:00+07:00", "revision_identity": f"revision-{index}",
            "scorer_version": SCORER, "numeric_score": .5, "probabilities": [.1, .6, .3]}
        row.update(changes)
        fields = ("source_url_or_archive_id", "content_hash", "published_at", "publication_precision",
                  "source_timezone", "available_at", "revision_identity")
        proof = {k: row[k] for k in fields}
        proof.update(kind="ARCHIVED_CONTENT", witnessed_at=witnessed_at or row["available_at"])
        raw = json_bytes({"content": row["content"], "metadata": proof})
        identifier = hashlib.sha256(raw).hexdigest()
        name = identifier + ".json"
        (self.root / name).write_bytes(raw)
        proof["archive_binding"] = binding(self.root, name)
        self.evidence[identifier] = proof
        row["evidence_id"] = identifier
        return row

    def news(self, rows: list[dict]) -> FinalizedNews:
        """Mỗi caller sở hữu corpus và registry riêng."""
        return FinalizedNews({"FPT": rows}, evidence=self.evidence, root=self.root)


class FinalizeNewsTests(NewsFixture):
    def test_available_weighted_score_and_same_snapshot_for_decision_display(self) -> None:
        rows = [self.row(1, available_at="2026-06-01T10:00:00+07:00", published_at="2026-05-31T09:00:00+07:00"),
                self.row(2, numeric_score=-.5, probabilities=[.6, .1, .3]), self.row(3)]
        news = self.news(rows)
        snapshot = news.snapshot("FPT", "2026-07-02")
        data, report = snapshot_values(snapshot, expected_sha256=snapshot["sha256"])
        self.assertEqual((data, report), news.get_sentiment_at("FPT", "2026-07-02"))
        w1 = math.exp(-math.log(2) * 31 / 30)
        w2 = math.exp(-math.log(2) * 2 / 30)
        self.assertAlmostEqual(data["main_sentiment"]["avg_score"], .5*w1/(w1+2*w2))
        self.assertEqual(data["verified_article_count"], 3)
        self.assertFalse(data["is_unavailable"])
        self.assertIn("score=", report)
        json.dumps(data, allow_nan=False)

    def test_zero_one_two_articles_are_na_with_reason_and_no_neutral(self) -> None:
        for count in (0, 1, 2):
            data, report = self.news([self.row(i) for i in range(count)]).get_sentiment_at("FPT", "2026-07-02")
            self.assertIsNone(data["main_sentiment"]["avg_score"])
            self.assertEqual(data["main_sentiment"]["article_count"], 0)
            self.assertEqual(data["verified_article_count"], count)
            self.assertNotIn("label", data["main_sentiment"])
            self.assertNotIn("score=", report)

    def test_duplicate_url_revision_is_counted_once_and_latest_missing_score_does_not_reuse_old(self) -> None:
        old = self.row(1)
        new = self.row(2, source_url_or_archive_id=old["source_url_or_archive_id"],
                       available_at="2026-07-01T10:00:00+07:00", numeric_score=None)
        data, _ = self.news([old, deepcopy(old)]).get_sentiment_at("FPT", "2026-07-02")
        self.assertEqual(data["verified_article_count"], 1)
        data, _ = self.news([old, new]).get_sentiment_at("FPT", "2026-07-02")
        self.assertEqual(data["verified_article_count"], 0)
        self.assertEqual(data["missing_reason"], "MISSING_SCORE")
        self.assertEqual((data, self.news([old, new]).get_sentiment_at("FPT", "2026-07-02")[1]),
                         self.news([new, old]).get_sentiment_at("FPT", "2026-07-02"))

    def test_hash_probabilities_scorer_input_and_ambiguous_revision_rejected(self) -> None:
        original = self.row(1)
        for changes in ({"content": "Nội dung bị sửa"}, {"score_content_hash": "0"*64},
                        {"numeric_score": .99}, {"probabilities": [0., 0., 0.]},
                        {"numeric_score": float("nan")}):
            row = {**original, **changes}
            with self.assertRaises(ValueError):
                self.news([row]).snapshot("FPT", "2026-07-02")
        other = self.row(2, source_url_or_archive_id=original["source_url_or_archive_id"])
        with self.assertRaises(ValueError):
            self.news([original, other]).snapshot("FPT", "2026-07-02")

    def test_bad_archive_or_registry_metadata_cannot_be_self_signed(self) -> None:
        row = self.row(1)
        proof = self.evidence[row["evidence_id"]]
        proof["revision_identity"] = "forged"
        with self.assertRaises(ValueError):
            self.news([row])
        proof["revision_identity"] = row["revision_identity"]
        path = self.root / proof["archive_binding"]["path"]
        path.write_bytes(path.read_bytes()+b" ")
        with self.assertRaises(ValueError):
            self.news([row])

    def test_caller_mutation_or_resigned_snapshot_does_not_change_sealed_input(self) -> None:
        rows = [self.row(i) for i in range(3)]
        news = self.news(rows)
        snapshot = news.snapshot("FPT", "2026-07-02")
        rows[0]["content"] = "Sửa corpus ngoài object"
        self.assertEqual(snapshot, news.snapshot("FPT", "2026-07-02"))
        data, _ = snapshot_values(snapshot, expected_sha256=snapshot["sha256"])
        data["scored_articles"].clear()
        self.assertEqual(snapshot, news.snapshot("FPT", "2026-07-02"))
        poisoned = deepcopy(snapshot)
        poisoned["payload"]["sentiment_data"]["main_sentiment"]["avg_score"] = 1.
        poisoned["sha256"] = digest(poisoned["payload"])
        with self.assertRaises(ValueError):
            snapshot_values(poisoned, expected_sha256=snapshot["sha256"])

    def test_real_corpus_stays_quarantined_and_resigned_release_is_rejected(self) -> None:
        corpus = prepare_corpus(ROOT)
        self.assertEqual((corpus["candidate_records"], corpus["unique_articles"], corpus["saved_unique_scores"]), (180, 177, 154))
        self.assertEqual(corpus["evidence_registry"], {})
        result = check_release(ROOT)
        self.assertEqual((result["planned_points"], result["available_points"], result["unavailable_points"]), (102, 0, 102))
        with patch("core.finalize_news_release.read") as reader:
            def altered(root: Path, path: str, *args: object) -> dict:
                value = read(root, path, *args)
                if path.endswith("finalize_news_corpus_v1.json"):
                    value["evidence_registry"]["fake"] = {}
                return value
            reader.side_effect = altered
            with self.assertRaises(ValueError):
                check_release(ROOT)


if __name__ == "__main__":
    unittest.main()
