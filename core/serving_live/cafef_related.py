"""Chọn mã đối chiếu từ tin đã khóa và danh mục ngành hiện tại."""
from __future__ import annotations

from collections import defaultdict
import re

MAX_RELATED = 4
MAX_CANDIDATES = MAX_RELATED * 2
ALIASES = {'CMG': ('Tập đoàn CMC', 'CMC Corp'), 'FRT': ('FPT Retail', 'Long Châu'),
           'FOX': ('FPT Telecom', 'Viễn thông FPT'), 'VCI': ('Vietcap',), 'VNM': ('Vinamilk',),
           'HVN': ('Vietnam Airlines',), 'VJC': ('Vietjet',), 'VCB': ('Vietcombank',),
           'TCB': ('Techcombank',), 'BID': ('BIDV',), 'CTG': ('VietinBank',), 'SAB': ('Sabeco',)}
AMBIGUOUS_CODES = {'USD', 'ETF', 'CEO', 'IPO', 'GDP', 'FDI'}


def mentioned(code: str, text: str) -> bool:
    """Khớp mã viết hoa hoặc tên thương hiệu nhận diện được trong văn bản đã chấm."""
    return bool((code not in AMBIGUOUS_CODES and re.search(rf'\b{code}\b', text)) or any(
        re.search(rf'\b{re.escape(alias)}\b', text, flags=re.IGNORECASE) for alias in ALIASES.get(code, ())))


def live_directory() -> tuple[dict[str, str], dict[str, dict[int, str]]]:
    """Dùng mã đang niêm yết và nhóm ngành ICB qua nguồn thị trường sẵn có."""
    from core.realtime_loader import fetch_dstock_all_symbols

    listed = {row['code']: row['name'] for row in fetch_dstock_all_symbols()}
    industries: dict[str, dict[int, str]] = defaultdict(dict)
    if listed:
        try:
            from vnstock.api.listing import Listing
            groups = Listing(source='VCI').symbols_by_industries()
            for row in groups[['symbol', 'icb_level', 'icb_code']].dropna().to_dict('records'):
                if row['symbol'] in listed:
                    industries[row['symbol']][int(row['icb_level'])] = str(row['icb_code'])
        except Exception as error:
            print(f'[CafeF] Không lấy được phân ngành ICB để đối chiếu: {error}')
    return listed, dict(industries)


def select_related(symbol: str, articles: list[dict], listed: dict[str, str],
                   industries: dict[str, dict[int, str]]) -> list[tuple[str, dict]]:
    """Ưu tiên mã xuất hiện trong nhiều bài đã chấm, rồi bổ sung theo nhóm ngành gần nhất."""
    candidates = {code for code in listed if code != symbol and re.fullmatch('[A-Z]{3}', code)}
    mentions: dict[str, list[str]] = defaultdict(list)
    for row in articles:
        text = row['score_input']
        codes = set(re.findall(r'\b[A-Z]{3}\b', text)) | ALIASES.keys()
        for code in candidates.intersection(codes):
            if mentioned(code, text):
                mentions[code].append(row['source_url_or_archive_id'])
    context = industries.get(symbol, {})
    shared = {code: max((level for level in (2, 3, 4) if context.get(level)
                        and context[level] == industries.get(code, {}).get(level)), default=0)
              for code in candidates}
    ranked = sorted((code for code in candidates if code in mentions or shared[code]),
                    key=lambda code: (-len(mentions.get(code, ())), -shared[code], code))[:MAX_CANDIDATES]
    return [(code, {'name': listed[code], 'mention_urls': mentions.get(code, []),
                    'industry_level': shared[code] or None,
                    'industry_code': context[shared[code]] if shared[code] else None})
            for code in ranked]
