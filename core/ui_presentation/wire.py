"""Mở rộng phản hồi live trong cùng request; không tạo lời gọi dịch hoặc đổi schema nghiên cứu."""
from copy import deepcopy
import json
import re
from collections import Counter

from core.display_translation import TranslationError, validate_translation
from core.serving_runtime.quota import Failed

DIRECTIVE=('LIVE UI OUTPUT OVERRIDE: make ONE analysis, express it in both languages. '
    'Preserve every numerical fact, formula, ticker and trading action; translate directional labels. '
    'Keep the same report sections in both languages; use concise sentences to fit both reports in the output budget. Return only JSON '
    '{"vi":"complete Vietnamese Markdown report","en":"same complete report in English"}; no second judgement or extra text.')

DECISION_TEXT = ('justification', 'evidence_for', 'evidence_against')
MONTHS = dict(zip(('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'), range(1, 13)))
MONTH = r'Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?'
VI_DATE = re.compile(r'\bngày\s+(?P<day>0?[1-9]|[12]\d|3[01])/(?P<month>0?[1-9]|1[0-2])(?:/(?P<year>\d{4}))?(?![\d/])', re.I)
EN_DATE = re.compile(rf'\b(?:(?P<month>{MONTH})\.?\s+(?P<day>0?[1-9]|[12]\d|3[01])|'
                     rf'(?P<day_first>0?[1-9]|[12]\d|3[01])\s+(?P<month_last>{MONTH})\.?)'
                     r'(?:(?:,\s*|\s+)(?P<year>\d{4}))?\b', re.I)
LITERAL = re.compile(r'(`[^`]+`|https?://[^\s)]+)')


def _matching_display(source: str, english: str) -> str | None:
    """Đối chiếu cách viết ngày và CASH ngoài code/URL, trả nguyên văn bản dịch đã qua kiểm tra."""
    if not isinstance(english, str):
        return None

    def date(match: re.Match) -> str:
        parts = match.groupdict()
        month = parts['month'] or parts.get('month_last')
        number = int(month) if month.isdigit() else MONTHS[month[:3].lower()]
        day = int(parts['day'] or parts.get('day_first'))
        year = '/' + parts['year'] if parts['year'] else ''
        return f'{day}/{number}{year}'

    vi_parts, en_parts = LITERAL.split(source), LITERAL.split(english)
    vi_dates = Counter(date(match) for part in vi_parts[::2] for match in VI_DATE.finditer(part))
    en_dates = Counter(date(match) for part in en_parts[::2] for match in EN_DATE.finditer(part))
    if en_dates and en_dates != vi_dates:
        return None

    try:
        validate_translation(source, english, 'en')
    except TranslationError:
        for index in range(0, len(vi_parts), 2):
            if en_dates:
                vi_parts[index] = VI_DATE.sub(date, vi_parts[index])
        for index in range(0, len(en_parts), 2):
            text = EN_DATE.sub(date, en_parts[index])
            en_parts[index] = re.sub(r'(?<![\w-])cash(?![\w-])', 'CASH', text, flags=re.I) if re.search(r'\bCASH\b', source) else text
        try:
            validate_translation(''.join(vi_parts), ''.join(en_parts), 'en')
        except TranslationError:
            return None
    return english


def report_body(body: dict) -> dict:
    """Giữ nguồn/ảnh/options; chỉ thêm hợp đồng trình bày của profile live mới."""
    result=deepcopy(body)
    for message in result['messages']:
        if message['role']=='system':
            message['content']+='\n'+DIRECTIVE
            break
    result['messages'].append({'role':'user','content':DIRECTIVE})
    return result


def report_reply(value: str) -> dict[str, str | None]:
    """Báo cáo canonical hợp lệ vẫn dùng được khi phần hiển thị EN sai dữ kiện."""
    try:
        raw=value.strip()
        if raw.startswith('```'):
            lines = raw.splitlines()
            if len(lines) < 3 or lines[0].lower() not in ('```','```json') or lines[-1] != '```':
                raise ValueError('Sai khung JSON của báo cáo')
            raw = '\n'.join(lines[1:-1])
        result=json.loads(raw)
        if not isinstance(result, dict) or set(result) - {'vi','en'} or not isinstance(result.get('vi'), str) or not result['vi'].strip():
            raise ValueError('Thiếu báo cáo tiếng Việt')
        return {'vi': result['vi'], 'en': _matching_display(result['vi'], result.get('en'))}
    except (ValueError,TypeError,AttributeError): raise Failed('INVALID_MODEL_OUTPUT') from None


def decision_body(body: dict, *, ground_facts: bool = False) -> dict:
    """Schema wire có thêm bản EN; request canonical và policy vẫn dùng phản hồi VI."""
    result=deepcopy(body)
    schema=result['response_format']['json_schema']['schema']
    node=schema
    if '$ref' in node:
        for name in node['$ref'][2:].split('/'): node=schema[name] if name=='$defs' else node[name]
    node['properties']['display_en']={'type':'object','properties':{key:{'type':'string'} for key in DECISION_TEXT},
        'required':list(DECISION_TEXT),'additionalProperties':False}
    node['required']=[*node['required'],'display_en']
    directive = 'Keep canonical fields in Vietnamese. In the SAME response add display_en: English justification, evidence_for, evidence_against. One decision, same facts. Copy numbers, signs, formulas and LONG/SHORT/CASH exactly; do not add facts. Keep both versions concise.'
    if ground_facts and 'fact_assertions' in node['properties']:
        directive = ('Write Vietnamese and matching English display_en with identical action and numbers. '
                     'Use FACTS in both decision and prose: MACD_ZERO gives the sign; MACD_SIGNAL compares with Signal. '
                     'A possible crossover is not confirmation. Historical utility is not the realized outcome.')
    result['messages'].append({'role':'user','content':directive})
    return result


def decision_reply(value: dict) -> tuple[dict,dict]:
    """Bóc display khỏi dữ liệu đưa vào policy; raw HTTP vẫn giữ đủ phản hồi thực."""
    canonical=deepcopy(value); english=canonical.pop('display_en',None)
    if any(not isinstance(canonical.get(key), str) for key in DECISION_TEXT):
        raise Failed('INVALID_MODEL_OUTPUT')
    display = english if isinstance(english, dict) else {}
    return canonical, {key: _matching_display(canonical[key], display.get(key)) for key in DECISION_TEXT}
