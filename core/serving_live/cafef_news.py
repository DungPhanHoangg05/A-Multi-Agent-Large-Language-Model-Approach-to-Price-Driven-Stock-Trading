"""Thu, chấm và khóa đúng bài CafeF đã dùng cho một lượt phân tích live."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from functools import lru_cache
import math
import re
from statistics import fmean, pstdev
from typing import Any, Callable
from urllib.parse import urlsplit

from core.finalize_news import VERSION as SNAPSHOT_SCHEMA, ZONE, publication, timestamp
from core.serving_live.cafef_related import ALIASES, MAX_RELATED, live_directory, mentioned, select_related
from core.serving_live.catalog import stock_symbol
from core.unified_contracts import digest

VERSION = 'cafef_live_sentiment_v1'
RELATED_VERSION = 'cafef_live_sentiment_v2'
MAX_ARTICLES = 30
MAX_RELATED_ARTICLES = 10
MIN_RELATIVE_ARTICLES = 2
WINDOW_DAYS = 90
STATUSES = {'AVAILABLE', 'CAFEF_UNAVAILABLE', 'NO_ELIGIBLE_NEWS'}


def publication_fields(raw: str) -> dict[str, str]:
    """Giữ giờ CafeF đã công bố; bài chỉ có ngày khả dụng từ ngày sau."""
    value = raw.strip().replace('-', '/')
    for fmt, precision in (('%d/%m/%Y %H:%M', 'second'), ('%d/%m/%Y', 'day')):
        try:
            parsed = datetime.strptime(value, fmt).replace(tzinfo=ZONE)
        except ValueError:
            continue
        return {'published_at': parsed.isoformat() if precision == 'second' else parsed.date().isoformat(),
                'date_parsed': parsed.date().isoformat(), 'publication_precision': precision,
                'source_timezone': 'Asia/Ho_Chi_Minh'}
    return {}


def _cafef_url(url: str) -> bool:
    """Chỉ nhận URL bài CafeF do crawler lấy từ trang nguồn cố định."""
    value = urlsplit(url)
    return value.scheme == 'https' and value.netloc in ('cafef.vn', 'www.cafef.vn') and value.path.endswith('.chn')


def _collect_news(symbol: str, as_of: datetime, fetch: Callable[[str], Any] | None, limit: int) -> tuple[list[dict], dict]:
    """Chỉ lấy bài liên quan khả dụng trong cửa sổ live, trước khi gọi bộ chấm."""
    from agents.sentiment_agent import CAFEF_BASE_URL, _get, _get_company_keywords, _is_article_relevant
    from agents.sentiment_agent import _parse_listing_page

    if not stock_symbol(symbol) or as_of.tzinfo is None:
        raise ValueError('Mã hoặc giờ cutoff tin CafeF không hợp lệ')
    fetch = fetch or (lambda url: _get(url, retries=1))
    as_of = as_of.astimezone(ZONE)
    lower = as_of - timedelta(days=WINDOW_DAYS)
    keywords = [*_get_company_keywords(symbol), *ALIASES.get(symbol, ())]
    candidates: dict[str, dict] = {}
    fetched = False
    for slug in (symbol.lower(), 'co-phieu-' + symbol.lower()):
        response = fetch(f'{CAFEF_BASE_URL}/{slug}.html')
        if response is None:
            continue
        fetched = True
        for item in _parse_listing_page(response.text, include_time=True):
            url = item['url']
            fields = publication_fields(item['date'])
            if url in candidates or not fields or not _cafef_url(url) or not _is_article_relevant(item, symbol, keywords):
                continue
            _, available = publication(fields)
            if lower <= available <= as_of:
                text = f"{item['title']} {item['snippet']}".strip()[:512]
                candidates[url] = {**fields, 'available_at': available.isoformat(), 'title': item['title'],
                                   'source_url_or_archive_id': url, 'score_input': text, 'score_input_sha256': digest(text)}
        if candidates:
            break
    articles = sorted(candidates.values(), key=lambda item: timestamp(item['available_at']), reverse=True)[:limit]
    status = 'AVAILABLE' if articles else 'NO_ELIGIBLE_NEWS' if fetched else 'CAFEF_UNAVAILABLE'
    return articles, {'version': VERSION, 'as_of_at': as_of.isoformat(), 'status': status}


def _score_articles(articles: list[dict], score: Callable[[str], dict]) -> None:
    """Lưu đầu ra của bộ chấm cho đúng văn bản trong snapshot."""
    fields = ('label', 'numeric_score', 'confidence', 'scorer', 'scorer_backend', 'is_fallback')
    for article in articles:
        scored = score(article['score_input'])
        article.update({key: scored[key] for key in fields})


def capture_news(symbol: str, as_of: datetime, *, fetch: Callable[[str], Any] | None = None,
                 score: Callable[[str], dict] | None = None) -> tuple[list[dict], dict]:
    """Chấm tiêu đề và tóm tắt đã tải của mã chính."""
    from agents.sentiment_agent import _score_text

    articles, meta = _collect_news(symbol, as_of, fetch, MAX_ARTICLES)
    _score_articles(articles, score or _score_text)
    return articles, meta


def capture_live_news(symbol: str, as_of: datetime, *, fetch: Callable[[str], Any] | None = None,
                      score: Callable[[str], dict] | None = None,
                      directory: Callable[[], tuple[dict[str, str], dict[str, dict[int, str]]]] | None = None
                      ) -> tuple[list[dict], dict, dict]:
    """Chấm cả mã chính và mã đối chiếu tại cùng một cutoff, lưu bài gốc theo từng mã."""
    from agents.sentiment_agent import _score_text

    cached_score = lru_cache(maxsize=MAX_ARTICLES + MAX_RELATED * MAX_RELATED_ARTICLES)(score or _score_text)
    articles, meta = capture_news(symbol, as_of, fetch=fetch, score=cached_score)
    related = {}
    if articles:
        secondary = []
        for code, evidence in select_related(symbol, articles, *(directory or live_directory)()):
            rows, peer = _collect_news(code, as_of, fetch, MAX_RELATED_ARTICLES)
            item = {**evidence, 'status': peer['status'], 'articles': rows}
            if len(rows) < MIN_RELATIVE_ARTICLES:
                secondary.append((code, item))
                continue
            related[code] = item
            if len(related) == MAX_RELATED:
                break
        secondary.sort(key=lambda item: -len(item[1]['articles']))
        related.update(secondary[:MAX_RELATED - len(related)])
        for item in related.values():
            _score_articles(item['articles'], cached_score)
    return articles, {**meta, 'version': RELATED_VERSION}, related


def _check_articles(rows: list[dict], status: str, as_of: datetime, limit: int) -> None:
    """Kiểm cùng cutoff, điểm và nguyên văn đã chấm cho từng lô bài."""
    if (status not in STATUSES or bool(rows) != (status == 'AVAILABLE') or len(rows) > limit
            or len({row['source_url_or_archive_id'] for row in rows}) != len(rows)):
        raise ValueError('Trạng thái hoặc danh sách bài CafeF không hợp lệ')
    for row in rows:
        published, floor = publication(row)
        available = timestamp(row['available_at'])
        value, confidence = row['numeric_score'], row['confidence']
        if (not _cafef_url(row['source_url_or_archive_id']) or row['date_parsed'] != published.date().isoformat()
                or available != floor or not as_of - timedelta(days=WINDOW_DAYS) <= available <= as_of
                or not row['score_input'] or len(row['score_input']) > 512 or digest(row['score_input']) != row['score_input_sha256']
                or row['label'] not in ('positive', 'neutral', 'negative')
                or type(confidence) not in (int, float) or not 0 <= confidence <= 1
                or not row['scorer'] or not row['scorer_backend'] or type(row['is_fallback']) is not bool
                or type(value) not in (int, float) or not math.isfinite(value) or not -1 <= value <= 1):
            raise ValueError('Bài CafeF sai nguồn, thời điểm hoặc điểm đã khóa')


def _weighted_score(rows: list[dict], as_of: datetime) -> float | None:
    """Giảm một nửa trọng số của tin sau mỗi 30 ngày."""
    if not rows:
        return None
    weights = [math.exp(-math.log(2) * (as_of - timestamp(row['available_at'])).total_seconds() / (86400 * 30))
               for row in rows]
    return math.fsum(weight * row['numeric_score'] for weight, row in zip(weights, rows)) / math.fsum(weights)


def _visible_articles(rows: list[dict]) -> list[dict]:
    """Dùng timestamp live đã kiểm; giữ văn bản chấm trong snapshot riêng của người chạy."""
    return [{key: value for key, value in row.items() if key not in ('score_input', 'date_parsed')} for row in rows]


def _normalize(rows: list[dict], score: float | None, reliable_count: int) -> dict:
    """Chuẩn hóa quanh trung bình và độ lệch chuẩn của chính lô điểm gốc."""
    scores = [row['numeric_score'] for row in rows]
    stdev = pstdev(scores) if len(scores) >= 3 else None
    value = (score - fmean(scores)) / (stdev + .001) if score is not None and stdev else None
    reason = 'INSUFFICIENT_ARTICLES' if stdev is None else 'ZERO_VARIANCE' if not stdev else None
    return {'z_score': value, 'is_reliable': value is not None and len(scores) >= reliable_count,
            'article_count': len(scores), 'missing_reason': reason}


def _related_metrics(record: dict, rows: list[dict], score: float | None, as_of: datetime) -> dict:
    """Kiểm và tổng hợp đúng bài của các mã đối chiếu đã được khóa ở lúc capture."""
    peers = record['related_news']
    mention_sources = {row['source_url_or_archive_id']: row['score_input'] for row in rows}
    if len(peers) > MAX_RELATED or (peers and not rows):
        raise ValueError('Danh sách công ty đối chiếu CafeF không hợp lệ')
    summaries, norms = {}, {}
    for code, peer in sorted(peers.items()):
        urls = peer['mention_urls']
        industry = peer['industry_code']
        if (code == record['symbol'] or not re.fullmatch('[A-Z]{3}', code) or (not urls and not industry)
                or bool(industry) != (peer['industry_level'] in (2, 3, 4))
                or len(set(urls)) != len(urls)
                or any(url not in mention_sources or not mentioned(code, mention_sources[url]) for url in urls)):
            raise ValueError('Bằng chứng công ty đối chiếu CafeF không hợp lệ')
        articles = peer['articles']
        _check_articles(articles, peer['status'], as_of, MAX_RELATED_ARTICLES)
        avg = _weighted_score(articles, as_of)
        summaries[code] = {'name': peer['name'], 'status': peer['status'], 'article_count': len(articles), 'avg_score': avg,
                           'mention_urls': urls, 'industry_code': industry, 'scored_articles': _visible_articles(articles),
                           'in_relative': len(articles) >= MIN_RELATIVE_ARTICLES}
        norms[code] = _normalize(articles, avg, reliable_count=5)
    # Giữ ngưỡng hai bài của phép so sánh cũ; mã thiếu tin không mặc định điểm 0.
    eligible = [row['avg_score'] for row in summaries.values() if row['in_relative']]
    relative = score - fmean(eligible) if score is not None and eligible else None
    norm = {**_normalize(rows, score, reliable_count=8), 'rel_sentiment': relative, 'relative_peer_count': len(eligible)}
    return {'related_sentiment': summaries, 'related_companies': list(summaries), 'related_norm': norms,
            'sentiment_norm': norm, 'relative_available': relative is not None}


class CapturedNews:
    """Chuẩn hóa snapshot CafeF sang hợp đồng báo cáo sẵn có, không gọi lại mạng hoặc scorer."""
    def __init__(self, record: dict) -> None:
        meta, articles = record['live_news'], record['news']
        as_of = timestamp(meta['as_of_at'])
        with_related = meta['version'] == RELATED_VERSION
        if (meta['version'] not in (VERSION, RELATED_VERSION) or as_of != timestamp(record['captured_at'])
                or with_related != ('related_news' in record)):
            raise ValueError('Snapshot tin CafeF sai phiên bản hoặc cutoff')
        _check_articles(articles, meta['status'], as_of, MAX_ARTICLES)
        self.symbol, self.cutoff = record['symbol'], record['cutoff']
        count = len(articles)
        score = _weighted_score(articles, as_of)
        rows = _visible_articles(articles)
        missing = None if score is not None else meta['status']
        scorers = sorted({row['scorer'] for row in articles})
        self.payload = {'version': SNAPSHOT_SCHEMA, 'symbol': self.symbol, 'cutoff_date': self.cutoff,
            'cutoff_at': meta['as_of_at'], 'window_days': WINDOW_DAYS,
            'sentiment_data': {'main_sentiment': {'article_count': count, 'avg_score': score},
                'scored_articles': rows, 'related_sentiment': {}, 'related_companies': [], 'is_unavailable': score is None,
                'verified_article_count': count, 'missing_reason': missing, 'scorer_version': ' / '.join(scorers),
                'live_news': deepcopy(meta), 'fallback_article_count': sum(row['is_fallback'] for row in rows),
                **(_related_metrics(record, articles, score, as_of) if with_related else {})},
            'sentiment_report': (f'Tâm lý CafeF tại lúc phân tích: score={score:+.6f}; số bài={count}.' if score is not None else
                                 f'Tâm lý CafeF chưa khả dụng; lý do={missing}; số bài={count}.')}

    def snapshot(self, symbol: str, cutoff: str) -> dict:
        """Chỉ mở dữ liệu đã niêm phong cho cặp mã và phiên giá của lượt live."""
        if (symbol, cutoff) != (self.symbol, self.cutoff):
            raise ValueError('Snapshot tin CafeF khác mã hoặc phiên giá đã khóa')
        return {'payload': deepcopy(self.payload), 'sha256': digest(self.payload)}
