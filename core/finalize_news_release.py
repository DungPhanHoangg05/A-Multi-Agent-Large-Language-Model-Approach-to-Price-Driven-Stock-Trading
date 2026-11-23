"""Khóa corpus FIN05 từ byte đã lưu; thiếu bằng chứng nội dung giữ unavailable."""
from __future__ import annotations

from collections import Counter
import hashlib
from pathlib import Path
from typing import Any

from core.finalize_news import AGGREGATION, SCORER, SYMBOLS, FinalizedNews, score_value
from core.unified_contracts import digest
from core.unified_protocol import binding, read

DIRECTORY = "docs/plan/week12/"
CORPUS = DIRECTORY + "finalize_news_corpus_v1.json"
COVERAGE = DIRECTORY + "finalize_news_coverage_v1.json"
BASE = "outputs/historical_reevaluation/inputs/fix/outputs/revision/r1_72h_bank_v2/"


def prepare_corpus(root: Path) -> dict[str, Any]:
    """Đối chiếu inventory/scorer gốc; không suy metadata thu/công bố còn thiếu."""
    contract = read(root, DIRECTORY + "finalize_comparison_contract.json", True)
    pin = contract["sources_and_availability"]["candidate_assets"]
    if binding(root, pin["path"]) != pin:
        raise ValueError("Nguồn candidate tin khác FIN02")
    manifest = read(root, pin["path"], True)
    pins = [manifest["source_bindings"][BASE + name] for name in ("news.json", "article_audit.json", "local_scores.json")]
    if any(binding(root, p["path"]) != p for p in pins):
        raise ValueError("Corpus/scorer cũ khác byte đã pin")
    audit, scores, legacy = (read(root, BASE + name) for name in ("article_audit.json", "local_scores.json", "news.json"))
    if scores["revision"] != SCORER.split(":")[1] or scores["max_length"] != 256 or scores["mapping"] != {"0": "NEG", "1": "POS", "2": "NEU"}:
        raise ValueError("Scorer/model mapping khác recipe FIN05")
    articles = {a["article_id"]: a for a in audit["articles"]}
    records: dict[str, list[dict]] = {s: [] for s in SYMBOLS}
    for item in audit["records"]:
        article = articles[item["article_id"]]
        text = article["text"]
        content_hash = hashlib.sha256(text.encode()).hexdigest()
        # Audit cũ băm JSON string; content_hash mới băm byte UTF-8 văn bản.
        if digest(text) != item["text_hash"]:
            raise ValueError("Text corpus khác hash input scorer")
        score = scores["scores"].get(item["article_id"], {})
        records[item["symbol"]].append({"article_id": item["article_id"], "source_url_or_archive_id": article["url"],
            "content": text, "content_hash": content_hash, "legacy_text_json_hash": item["text_hash"],
            "published_at": article["date_parsed"] if article["date_consistent"] else None,
            "publication_precision": "day", "source_timezone": "Asia/Ho_Chi_Minh",
            "available_at": None, "collected_at": None, "revision_identity": None, "evidence_id": None,
            "numeric_score": score.get("numeric_score"), "probabilities": score.get("probabilities"),
            "scorer_version": SCORER, "score_content_hash": content_hash})
        if score:
            score_value(records[item["symbol"]][-1])
    return {"version": "finalize_news_corpus_v1", "profile": "finalize_news_pit_v1", "records": records,
        "evidence_registry": {}, "source_bindings": pins,
        "parents": [binding(root, DIRECTORY + "finalize_comparison_contract.json")],
        "candidate_records": len(audit["records"]), "unique_articles": len(articles),
        "legacy_scored_records": sum(map(len, legacy.values())), "saved_unique_scores": len(scores["scores"]),
        "scorer_version": SCORER, "model_artifact_hashes": scores["files"],
        "model_card_sha256": scores["model_card_sha256"], "aggregation_version": AGGREGATION,
        "new_source_collection": False, "model_forward_calls": 0, "hosted_api_calls": 0,
        "limits": ["Ngày trong cache không xác nhận bản nội dung đã công khai tại cutoff; không chuyển cờ eligible_source cũ thành archive proof.",
            "Chưa có receipt archive được xác thực trong corpus này; registry rỗng và tin giữ unavailable.",
            "Scorer ViSoBERT đã lưu được chạy hồi tố; pin model/recipe không chứng minh không có kiến thức huấn luyện tương lai.",
            "FIN08 mới nối profile/snapshot này vào CLI, serving và UI; caller lịch sử không bị thay đổi."]}


def coverage(root: Path, corpus: dict[str, Any]) -> dict[str, Any]:
    """Đối soát đủ 102 điểm mà không tạo neutral, suy availability hoặc gọi scorer."""
    contract = read(root, DIRECTORY + "finalize_comparison_contract.json", True)
    news = FinalizedNews(corpus["records"], evidence=corpus["evidence_registry"], root=root)
    points = []
    for point in contract["domain"]["primary_points"]:
        snapshot = news.snapshot(point["symbol"], point["cutoff"])
        data = snapshot["payload"]["sentiment_data"]
        points.append({**point, "snapshot_sha256": snapshot["sha256"],
            "verified_article_count": data["verified_article_count"], "is_unavailable": data["is_unavailable"],
            "missing_reason": data["missing_reason"],
            "quarantine_counts": dict(Counter(r["reason"] for r in news.audit_at(point["symbol"], point["cutoff"])))})
    return {"version": "finalize_news_coverage_v1", "result": "PASS_NEWS_PIT_WITH_EXPLICIT_UNAVAILABLE",
        "FIN05_complete": True, "corpus_sha256": digest(corpus),
        "parents": [binding(root, DIRECTORY + "finalize_comparison_contract.json")],
        "planned_points": len(points), "available_points": sum(not p["is_unavailable"] for p in points),
        "unavailable_points": sum(p["is_unavailable"] for p in points), "points": points,
        "content_pit_proven_articles": len(corpus["evidence_registry"]),
        "query_outcomes_computed": False, "model_forward_calls": 0, "hosted_api_calls": 0}


def check_release(root: Path) -> dict[str, Any]:
    """Tái dựng từ input đã pin, không tin release tự sửa rồi ký lại checksum."""
    corpus = prepare_corpus(root)
    result = coverage(root, corpus)
    if read(root, CORPUS, True) != corpus or read(root, COVERAGE, True) != result:
        raise ValueError("Release tin khác nguồn/recipe/corpus đã khóa")
    return result
