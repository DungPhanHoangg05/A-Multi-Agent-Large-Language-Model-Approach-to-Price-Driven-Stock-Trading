"""Đọc đầy đủ tin đã capture cho UI, không sửa sentiment score/normalizer mà agent đã sử dụng."""
from __future__ import annotations

from copy import deepcopy
import math
import pandas as pd

from core.historical_evaluation_data import FrozenNews


def sentiment_view(source: dict, articles: list[dict] | None, symbol: str, cutoff: str) -> dict:
    """Dùng chính eligibility FrozenNews; thiếu nhãn/peers là NA, không dựng phân bố bằng zero."""
    result = deepcopy(source)
    main = result.get('main_sentiment') or {}
    if main.get('avg_score') is None or not main.get('article_count'): return {}
    main['label'] = 'positive' if main['avg_score']>.1 else 'negative' if main['avg_score']<-.1 else 'neutral'
    result['main_sentiment'] = main
    if articles is not None:
        if any(row.get('date_parsed') and pd.Timestamp(row['date_parsed'])>pd.Timestamp(cutoff) for row in articles):
            raise ValueError('Tin hiển thị vượt cutoff của phân tích')
        verified,_ = FrozenNews({symbol:articles}).get_sentiment_at(symbol,cutoff)
        actual = verified['main_sentiment']
        if actual['article_count']!=main['article_count'] or actual['avg_score'] is None or not math.isclose(actual['avg_score'],main['avg_score'],abs_tol=1e-9):
            raise ValueError('Tin hiển thị khác sentiment đã khóa cho agent')
        visible = [row for row in articles if FrozenNews({symbol:[row]}).get_sentiment_at(symbol,cutoff)[0]['verified_article_count']]
        result['scored_articles'] = [{key:row.get(key) for key in ('title','date_parsed','numeric_score','label','scorer','scorer_source')} for row in visible]
        result['model_used'] = ' / '.join(sorted({row.get('scorer_source') or row['scorer'] for row in visible}))
    scored = result.get('scored_articles') or []
    labels = [row.get('label') for row in scored]
    result['distribution_available'] = len(labels)==main['article_count'] and all(value in ('positive','neutral','negative') for value in labels)
    if result['distribution_available']:
        main.update(positive=labels.count('positive'),negative=labels.count('negative'),neutral_count=labels.count('neutral'))
    elif all(key in main for key in ('positive','negative','neutral_count')):
        result['distribution_available'] = sum(main[key] for key in ('positive','negative','neutral_count'))==main['article_count']
    result['relative_available'] = bool(result.get('related_sentiment') or result.get('related_norm'))
    return result
