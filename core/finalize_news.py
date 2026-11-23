"""Snapshot tin FIN05: kiểm bản nội dung, giờ khả dụng và scorer trước tổng hợp."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, time, timedelta
import hashlib
import json
import math
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from core.unified_contracts import digest, json_bytes
from core.unified_protocol import binding

VERSION = "finalize_news_pit_v1"
AGGREGATION = "available_decay30_min3_cutoff1530_v1"
SCORER = "visobert:d7738b85200272f10ba8b048d80236c8c582b581:max256:pos_minus_neg_v1"
ZONE = ZoneInfo("Asia/Ho_Chi_Minh")
SYMBOLS = ("BHN", "CMG", "FPT", "HVN", "MBB", "MWG", "VCB", "VJC", "VNM")


def timestamp(value: str) -> datetime:
    """Đòi timezone rõ ràng; không suy giờ công bố từ ngày thu hoặc ngày trong URL."""
    if type(value) is not str:
        raise ValueError("Thời điểm tin phải là chuỗi có múi giờ")
    stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("Thời điểm tin thiếu múi giờ")
    return stamp.astimezone(ZONE)


def publication(row: dict[str, Any]) -> tuple[datetime, datetime]:
    """Trả thời điểm công bố và sàn availability theo độ chính xác nguồn."""
    value = row["published_at"]
    if type(value) is not str or not value:
        raise ValueError("Ngày công bố tin phải là chuỗi hợp lệ")
    if row.get("publication_precision") == "day":
        if row.get("source_timezone") != "Asia/Ho_Chi_Minh" or len(value) != 10:
            raise ValueError("Tin date-only thiếu timezone nguồn hoặc ngày không chuẩn")
        stamp = datetime.combine(datetime.strptime(value, "%Y-%m-%d").date(), time(), ZONE)
        return stamp, stamp + timedelta(days=1)
    if row.get("publication_precision") != "second":
        raise ValueError("Độ chính xác thời gian tin không hợp lệ")
    stamp = timestamp(value)
    return stamp, stamp


def score_value(row: dict[str, Any]) -> float | None:
    """Khóa ViSoBERT/recipe; score dùng đúng nội dung và bằng p_POS trừ p_NEG."""
    if row.get("scorer_version") != SCORER or row.get("numeric_score") is None:
        return None
    value, probs = row["numeric_score"], row.get("probabilities")
    if (type(value) not in (int, float) or not math.isfinite(value) or not -1 <= value <= 1
            or type(probs) is not list or len(probs) != 3
            or any(type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1 for p in probs)
            or not math.isclose(math.fsum(probs), 1., abs_tol=1e-5)
            or not math.isclose(value, probs[1]-probs[0], abs_tol=1e-7)
            or row.get("score_content_hash") != row["content_hash"]):
        raise ValueError("Score/probabilities không khớp recipe hoặc bản nội dung")
    return float(value)


class FinalizedNews:
    """Kho sở hữu riêng; registry là ranh giới tin cậy đã duyệt và được khóa trước sử dụng.

    Hash không tự chứng nhận bản công bố. Caller chỉ đăng ký receipt archive đã
    xác minh nguồn; fixture registry kiểm phần mềm, không xác thực tin thị trường.
    Release FIN05 thực giữ registry rỗng vì corpus cũ thiếu chứng cứ nội dung PIT.
    """

    def __init__(self, records: dict[str, list[dict[str, Any]]], *, evidence: dict[str, dict], root: Path) -> None:
        """Chỉ đọc file evidence đã pin; không crawl, score lại hoặc gọi model."""
        self._records, self._evidence = deepcopy(records), deepcopy(evidence)
        if set(records) - set(SYMBOLS):
            raise ValueError("Corpus tin có mã ngoài miền đã khóa")
        for identifier, proof in self._evidence.items():
            pin = proof["archive_binding"]
            if pin["sha256"] != identifier or binding(root, pin["path"]) != pin:
                raise ValueError("Evidence tin khác byte archive đã đăng ký")
            receipt = json.loads((root / pin["path"]).read_bytes())
            if (receipt.get("metadata") != {k: v for k, v in proof.items() if k != "archive_binding"}
                    or hashlib.sha256(receipt["content"].encode()).hexdigest() != proof["content_hash"]):
                raise ValueError("Registry tin khác nội dung/metadata receipt archive")

    def _select(self, symbol: str, cutoff_date: str) -> tuple[datetime, list[dict], list[dict]]:
        """Cắt thời gian trước đọc nội dung/score; chỉ giữ revision mới nhất đã biết."""
        if symbol not in SYMBOLS or type(cutoff_date) is not str or len(cutoff_date) != 10:
            raise ValueError("Mã/ngày tin ngoài miền đã khóa")
        query = datetime.combine(datetime.strptime(cutoff_date, "%Y-%m-%d").date(), time(15, 30), ZONE)
        selected: dict[str, dict] = {}
        excluded = []

        def reject(row: dict, reason: str) -> None:
            """Chỉ ghi ID/lý do vào audit riêng, không đưa nội dung bị loại vào forecast."""
            excluded.append({"article_id": str(row.get("article_id", "")), "reason": reason})

        for row in self._records.get(symbol, []):
            if not row.get("published_at"):
                reject(row, "UNDATED_PUBLICATION")
                continue
            published, floor = publication(row)
            if published > query:
                reject(row, "PUBLICATION_AFTER_CUTOFF")
                continue
            declared_available = timestamp(row["available_at"]) if row.get("available_at") else None
            if declared_available is not None and declared_available < floor:
                raise ValueError("Availability tin sớm hơn sàn công bố/date-only")
            if floor > query or (declared_available is not None and declared_available > query):
                reject(row, "REVISION_AFTER_CUTOFF")
                continue
            proof = self._evidence.get(row.get("evidence_id"))
            if proof is None:
                reject(row, "UNVERIFIED_AVAILABILITY")
                continue
            available = timestamp(row.get("available_at"))
            if available < query - timedelta(days=90):
                reject(row, "OUTSIDE_NEWS_WINDOW")
                continue
            # available_at là thời điểm bảo thủ bản nội dung đã được chứng kiến,
            # khác collected_at của lần tải bản archive về sau.
            witnessed, collected = timestamp(proof.get("witnessed_at")), timestamp(row.get("collected_at"))
            fields = ("content_hash", "source_url_or_archive_id", "published_at", "publication_precision",
                      "source_timezone", "available_at", "revision_identity")
            if (proof.get("kind") != "ARCHIVED_CONTENT" or any(row.get(k) != proof.get(k) for k in fields)
                    or any(type(row.get(k)) is not str or not row[k].strip() for k in fields)
                    or available < max(floor, witnessed)
                    or collected < witnessed or collected < published
                    or type(row.get("content")) is not str or not row["content"].strip()
                    or hashlib.sha256(row["content"].encode()).hexdigest() != row["content_hash"]):
                raise ValueError("Nội dung/revision hoặc chronology tin không khớp evidence")
            key = row["source_url_or_archive_id"]
            previous = selected.get(key)
            if previous and timestamp(previous["available_at"]) == available:
                if previous != row:
                    raise ValueError("Hai revision tin khác nhau có cùng thời điểm khả dụng")
                reject(row, "DUPLICATE_ARTICLE")
                continue
            if previous and timestamp(previous["available_at"]) > available:
                reject(row, "SUPERSEDED_REVISION")
                continue
            if previous:
                reject(previous, "SUPERSEDED_REVISION")
            selected[key] = deepcopy(row)
        rows = []
        for row in sorted(selected.values(), key=lambda r: (r["available_at"], r["source_url_or_archive_id"])):
            if score_value(row) is None:
                reject(row, "MISSING_SCORE")
            else:
                rows.append(row)
        return query, rows, excluded

    def snapshot(self, symbol: str, cutoff_date: str) -> dict[str, Any]:
        """Một payload/hash duy nhất cấp dữ liệu, báo cáo và hiển thị cùng bản tin."""
        query, rows, excluded = self._select(symbol, cutoff_date)
        count = len(rows)
        score = None
        reason = None
        if count >= 3:
            weights = [math.exp(-math.log(2) * (query-timestamp(r["available_at"])).total_seconds()/86400/30) for r in rows]
            score = float(math.fsum(w*r["numeric_score"] for w, r in zip(weights, rows))/math.fsum(weights))
        else:
            reasons = {item["reason"] for item in excluded}
            reason = ("INSUFFICIENT_ELIGIBLE_NEWS" if count else "UNVERIFIED_AVAILABILITY"
                      if "UNVERIFIED_AVAILABILITY" in reasons else "MISSING_SCORE"
                      if "MISSING_SCORE" in reasons else "NO_ELIGIBLE_NEWS")
        data = {"main_sentiment": {"article_count": count if score is not None else 0, "avg_score": score},
                "scored_articles": rows, "related_sentiment": {}, "related_companies": [],
                "is_unavailable": score is None, "is_reliable": score is not None,
                "verified_article_count": count, "missing_reason": reason,
                "scorer_version": SCORER, "aggregation_version": AGGREGATION}
        report = (f"Sentiment KHÔNG KHẢ DỤNG; lý do={reason}; số bài hợp lệ={count}; không gán điểm trung tính."
                  if score is None else f"Sentiment đã xác minh: score={score:.6f}; số bài={count}; peers không khả dụng.")
        payload = {"version": VERSION, "symbol": symbol, "cutoff_date": cutoff_date,
                   "cutoff_at": query.isoformat(), "window_days": 90,
                   "sentiment_data": data, "sentiment_report": report}
        return {"payload": payload, "sha256": digest(payload)}

    def audit_at(self, symbol: str, cutoff_date: str) -> list[dict]:
        """Các lý do quarantine ở ngoài snapshot/prompt; nội dung future không tác động forecast."""
        return self._select(symbol, cutoff_date)[2]

    def get_sentiment_at(self, symbol: str, cutoff_date: str, llm: Any = None,
                         window_days: int = 90) -> tuple[dict[str, Any], str]:
        """Giao diện caller tương thích; không sử dụng llm hoặc trả neutral thay NA."""
        if window_days != 90:
            raise ValueError("Cửa sổ tin khác recipe đã khóa")
        snapshot = self.snapshot(symbol, cutoff_date)
        return snapshot_values(snapshot, expected_sha256=snapshot["sha256"])


def snapshot_values(snapshot: dict[str, Any], *, expected_sha256: str) -> tuple[dict[str, Any], str]:
    """Consumer Decision/UI đọc cùng payload đã seal; không chọn lại tin hoặc score lại."""
    if (set(snapshot) != {"payload", "sha256"} or snapshot["sha256"] != expected_sha256
            or digest(snapshot["payload"]) != snapshot["sha256"]
            or snapshot["payload"]["version"] != VERSION):
        raise ValueError("Snapshot tin khác hash/version đã khóa")
    payload = snapshot["payload"]
    # Ép hợp đồng JSON nguyên bản ngay tại biên, không giấu NaN hoặc scalar NumPy.
    json_bytes(payload)
    return deepcopy(payload["sentiment_data"]), payload["sentiment_report"]
