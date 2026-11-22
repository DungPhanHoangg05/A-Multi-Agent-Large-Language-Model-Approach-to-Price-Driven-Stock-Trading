"""Projection song ngữ chỉ đọc dữ liệu đã lưu; không key, client, queue hoặc lời gọi dịch."""
from copy import deepcopy
from html import unescape
from pathlib import Path
import re
from markupsafe import escape

FIELDS={'indicator':'technical_indicators','pattern':'pattern_analysis','trend':'trend_analysis','alpha':'alpha_analysis','sentiment':'sentiment_analysis'}


def normalized(text: str) -> str:
    """Cùng quy tắc trình bày Indicator cũ, không sửa artifact nguồn."""
    return re.sub(r'^\s*\[END [^\n]*SECTION[^\n]*\]\s*$','',re.sub(r'^\s*===\s*(.*?)\s*===\s*$',lambda m:'### '+re.sub(r'\s*—\s*CHỈ ĐỌC SỐ TRONG SECTION NÀY\s*$','',m[1]),text,flags=re.M),flags=re.M)


def cached_pairs(root: Path, owner: str | None) -> dict:
    """Chỉ nhập cache đã hoàn tất đúng owner từ các phiên bản trước; không khởi động worker."""
    if not owner: return {}
    from core.historical_evaluation_journal import load
    from core.display_translation import validate_translation
    result={}; directory=root/'outputs/display_locales/v1'
    for path in directory.iterdir() if directory.exists() else []:
        if not path.is_dir() or path.is_symlink() or not (path/'source.json').exists(): continue
        source=load(path/'source.json'); status=load(path/'status.json')
        if source.get('owner')!=owner or source.get('target')!='en' or status.get('state')!='completed': continue
        values=load(path/'result.json')
        for name,text in values.items():
            vi=source['texts'][name]; validate_translation(vi,text,'en')
            # Template cũ thêm khoảng trắng cuối div; đó không phải nội dung báo cáo.
            result[vi.rstrip()]=text.rstrip()
    return result


def result_views(result: dict, cache: dict) -> dict:
    """Hai bản dùng chung decision/value/công thức; chỉ thay các đoạn trình bày đã có sẵn."""
    pairs=result.get('ui_report_pairs') or {}; views={}
    for language in ('vi','en'):
        view=deepcopy(result); missing=[]; source_languages={}
        for role,field in FIELDS.items():
            original=unescape(str(result.get(field) or ''))
            text=(normalized(original) if role=='indicator' else original).rstrip()
            existing_en=result.get('report_language')=='en'
            reverse={value:key for key,value in cache.items()}
            stored_pair = pairs.get(role)
            pair=stored_pair or {'vi':reverse.get(text) if existing_en else text,'en':text if existing_en else cache.get(text,cache.get(original))}
            value=pair.get(language)
            if value is None and language == 'en' and stored_pair and stored_pair.get('vi'):
                value = stored_pair['vi']
                source_languages[field] = 'vi'
            if value is None and original:
                missing.append(role)
                value=('Bản ghi cũ chưa có nội dung ở ngôn ngữ này.' if language=='vi' else 'This older record has no stored report in this language.')
            view[field]=str(escape(value or ''))
        decision=deepcopy(result.get('final_decision') or {})
        stored=pairs.get('decision') or {}
        for field in ('justification','evidence_for','evidence_against'):
            source=decision.get(field)
            if isinstance(source,str): source=source.rstrip()
            if language=='en':
                english = (stored.get('en') or {}).get(field)
                if english is None and 'en' in stored and source:
                    english = source
                    source_languages[field] = 'vi'
                decision[field] = english if english is not None else cache.get(source, source if result.get('report_language')=='en' else 'No stored English explanation for this older record.')
            elif stored.get('vi'): decision[field]=stored['vi'].get(field,source)
        view.update(final_decision=decision,report_language=language,missing_presentation=missing,report_source_languages=source_languages)
        if result.get('analysis_version_id'):
            from core.serving_registry import LABELS
            view['analysis_version']=LABELS[result['analysis_version_id']][int(language=='en')]
        if 'ui_bicl_views' in result and result['ui_bicl_views'].get(language): view['bicl'].update(result['ui_bicl_views'][language])
        views[language]=view
    return views
