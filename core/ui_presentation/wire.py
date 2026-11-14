"""Mở rộng phản hồi live trong cùng request; không tạo lời gọi dịch hoặc đổi schema nghiên cứu."""
from copy import deepcopy
import json

from core.display_translation import validate_translation
from core.serving_runtime.quota import Failed

DIRECTIVE=('LIVE UI OUTPUT OVERRIDE: make ONE analysis, express it in both languages. '
    'Preserve every numerical fact, formula, ticker and trading action; translate directional labels. '
    'Keep the same report sections in both languages; use concise sentences to fit both reports in the output budget. Return only JSON '
    '{"vi":"complete Vietnamese Markdown report","en":"same complete report in English"}; no second judgement or extra text.')


def report_body(body: dict) -> dict:
    """Giữ nguồn/ảnh/options; chỉ thêm hợp đồng trình bày của profile live mới."""
    result=deepcopy(body)
    for message in result['messages']:
        if message['role']=='system':
            message['content']+='\n'+DIRECTIVE
            break
    result['messages'].append({'role':'user','content':DIRECTIVE})
    return result


def report_reply(value: str) -> dict[str,str]:
    """Một phản hồi phải có đủ hai bản; không gọi model bổ sung nếu thiếu."""
    try:
        raw=value.strip()
        if raw.startswith('```'): raw=raw.split('\n',1)[1].rsplit('```',1)[0]
        result=json.loads(raw)
        if set(result)!={'vi','en'}: raise ValueError('Thiếu hai ngôn ngữ')
        validate_translation(result['vi'],result['en'],'en')
        return result
    except (ValueError,TypeError,KeyError): raise Failed('INVALID_MODEL_OUTPUT') from None


def decision_body(body: dict) -> dict:
    """Schema wire có thêm bản EN; request canonical và policy vẫn dùng phản hồi VI."""
    result=deepcopy(body)
    schema=result['response_format']['json_schema']['schema']
    node=schema
    if '$ref' in node:
        for name in node['$ref'][2:].split('/'): node=schema[name] if name=='$defs' else node[name]
    node['properties']['display_en']={'type':'object','properties':{key:{'type':'string'} for key in ('justification','evidence_for','evidence_against')},
        'required':['justification','evidence_for','evidence_against'],'additionalProperties':False}
    node['required']=[*node['required'],'display_en']
    result['messages'].append({'role':'user','content':'Keep canonical fields in Vietnamese. In the SAME response add display_en: English justification, evidence_for, evidence_against. One decision, same facts. Copy numbers, signs, formulas and LONG/SHORT/CASH exactly; do not add facts. Keep both versions concise.'})
    return result


def decision_reply(value: dict) -> tuple[dict,dict]:
    """Bóc display khỏi dữ liệu đưa vào policy; raw HTTP vẫn giữ đủ phản hồi thực."""
    canonical=deepcopy(value); english=canonical.pop('display_en',None)
    try:
        if set(english)!= {'justification','evidence_for','evidence_against'}: raise ValueError('Thiếu bản EN')
        for key in english: validate_translation(canonical[key],english[key],'en')
    except (ValueError,TypeError,KeyError): raise Failed('INVALID_MODEL_OUTPUT') from None
    return canonical,english
