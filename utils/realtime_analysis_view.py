"""Chiếu một phân tích realtime hoàn tất sang bố cục Original, giữ decision/policy và nguồn BICL."""
from __future__ import annotations

import ast
from copy import deepcopy
from functools import lru_cache
from inspect import getsource
from pathlib import Path
import re
from typing import Any

from markupsafe import escape

from core.finalize_serving_profile import VERSION as FINALIZED
from core.serving_registry import LABELS, MAIN_IDS

METHODS = {
    'bayesian_v1': ('Truy xuất tối đa ba chu kỳ đã đóng của cùng mã trong chế độ thị trường hiện tại, đưa prior Bayesian vào Decision.',
                    'Retrieve up to three matured cycles for the same symbol and current market regime; supply Bayesian priors to Decision.'),
    'C2': ('Kiểm tra chất lượng và support của bằng chứng lịch sử trước khi đưa thống kê và ví dụ có điều kiện vào Decision.',
           'Check evidence quality and support before supplying conditional statistics and examples to Decision.'),
    'A_tp_pool': ('Tách các chu kỳ cùng tín hiệu Trend/Pattern khỏi nhóm nền để tính thống kê có điều kiện cho Decision.',
                  'Separate cycles with matching Trend/Pattern signals from the background pool to compute conditional evidence for Decision.'),
    'B_semantic': ('Chọn bằng chứng lịch sử theo độ tương đồng ngữ nghĩa/tín hiệu và kiểm tra support trước khi bổ sung cho Decision.',
                   'Select historical evidence by semantic/signal similarity and check support before supplying it to Decision.'),
    'MT_BICL': ('Tạo Fact Anchor từ dữ kiện tại thời điểm phân tích, kết hợp context đa nhiệm và student đã đóng băng; policy quyết định chấp nhận hay bypass đề xuất sửa.',
                'Build a Fact Anchor from point-in-time facts and combine multi-task context with the frozen student; policy accepts or bypasses the proposed revision.'),
}


@lru_cache(maxsize=None)
def _factor_implementation(alpha_id: str) -> str:
    """Hiển thị biểu thức của handler với cùng cửa sổ cố định như bộ tính causal."""
    from core.alpha_compare import ALPHA_REGISTRY
    from core.causal_alpha import WINDOW_REPLACEMENTS

    entry = ALPHA_REGISTRY.get(alpha_id)
    if entry is None:
        return ''

    class FixedWindows(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call) -> ast.AST:
            window = WINDOW_REPLACEMENTS.get(ast.unparse(node))
            return ast.Constant(window) if window is not None else self.generic_visit(node)

    function = FixedWindows().visit(ast.parse(getsource(entry[0]))).body[0]
    if ast.get_docstring(function) is not None:
        function.body = function.body[1:]
    return ast.unparse(function)


def research_factor_metadata(alpha_id: str, language: str) -> dict:
    """Ghép mô tả song ngữ với cùng biểu thức triển khai dùng cho cả hai bản."""
    from core.alpha_compare import get_alpha_template
    metadata = {**get_alpha_template(alpha_id, language), 'implementation':_factor_implementation(alpha_id)}
    if alpha_id == 'CURRENT_1_FDM':
        return {**metadata, 'formula':'tanh(0.5 × ROC_adj × V / ADV20)',
                'interp':('Động lượng điều chỉnh theo biến động, có trọng số theo khối lượng.' if language == 'vi' else
                          'Volatility-adjusted momentum weighted by volume.')}
    if alpha_id == 'CURRENT_2_SFA':
        return {**metadata, 'type':'OHLCV', 'formula':'tanh(1.5 × tanh(MACD_hist / (0.005 × C + 10⁻⁹)) + 0.5 × ROC_adj)',
                'interp':('Kết hợp histogram MACD với động lượng giá điều chỉnh theo biến động.' if language == 'vi' else
                          'Combines the MACD histogram with volatility-adjusted price momentum.')}
    return metadata


def selector_statistics(symbol: str, cutoff: str, snapshot_id: str | None, selector_hash: str | None) -> dict[str, Any]:
    """Chỉ hiện thống kê fit nếu selector nguồn khớp đúng hash của kết quả live."""
    from core.finalize_bank_resources import ASSETS
    from core.unified_contracts import digest
    from core.unified_protocol import read

    if not snapshot_id or not selector_hash:
        return {}
    try:
        artifact = read(Path(__file__).resolve().parents[1], ASSETS + 'selectors.json')[symbol]
        payload = artifact['payload']
        parent = digest(payload)
        transferred = digest({'version': FINALIZED + '/live_selector_transfer_v1', 'parent': parent,
                              'capture': snapshot_id, 'cutoff': cutoff})
        if parent != artifact['sha256'] or transferred != selector_hash:
            return {}
        ranking = next(row['ranking'] for row in payload['validation_search'] if row['threshold'] == payload['threshold'])
        returns = {row['alpha_id']: row['mean_strategy_return'] for row in ranking}
        factors = {item['alpha_id']: {'train_ic':payload['candidates'][item['alpha_id']]['train_ic'],
                                       'validation_return_pct':100 * returns[item['alpha_id']]}
                   for item in payload['selected']}
        return {'threshold':payload['threshold'], 'factors':factors}
    except (OSError, ValueError, KeyError, TypeError, StopIteration):
        return {}


def can_project(data: dict) -> bool:
    """Bố cục báo cáo nhận một phương pháp, một điểm và một repeat live 1D đã hoàn tất."""
    request = data['identity']['request']
    ids = data['requested_ids']
    timeframe = request.get('chart_timeframe')
    daily = timeframe == '1d' or (timeframe is None and request.get('version') == FINALIZED and request.get('timeframe') == '1d')
    return (data['state'] == 'completed' and request['mode'] == 'analyze' and request.get('data_source') == 'live'
            and daily and request['repeats'] == 1 and len(ids) == 1 and ids[0] in MAIN_IDS and len(data['snapshots']) == 1)


def _saved_prior_statistics(trace: dict, evidence: dict, sent: bool) -> dict | None:
    """Đọc P/C/B và gate đã lưu của prior OHLCV, giữ nguyên cả mẫu số bằng không."""
    archived = evidence.get('statistics') or evidence.get('stats') or {}
    conditional = trace.get('conditional')
    counts = trace.get('counts') or archived.get('metrics')
    if not counts:
        return None
    if archived.get('conditional_count') is not None:
        conditional = archived
    gate = trace.get('gate') or evidence.get('gate') or {}
    ready = gate.get('ready_metric_ids', ())
    metrics = (conditional or {}).get('metrics', {})
    rows = []
    for key, population in counts.items():
        raw_population = population.get('raw_counts', {}).get('population')
        row = {'id':key, 'population':(f"{raw_population['success_count']}/{raw_population['support_count']}"
                                       if raw_population else f"{population['numerator']}/{population['denominator']}"),
               'rate':population.get('rate'), 'in_prompt':sent and (conditional is None or key in ready)}
        if key in metrics:
            metric = metrics[key]
            raw = metric['raw_counts']
            row.update({group:f"{raw[group]['success_count']}/{raw[group]['support_count']}"
                        for group in ('conditional','background')})
            row.update(posterior=metric['posterior_mean'], interval=metric['credible_interval'])
        rows.append(row)
    groups = conditional['groups'] if conditional is not None else {}
    return {'conditional':conditional is not None,
            'population_count':len(trace['population_ids']) if 'population_ids' in trace else archived.get('population_count'),
            'conditional_count':archived.get('conditional_count', len(groups.get('conditional', ()))),
            'background_count':archived.get('background_count', len(groups.get('background', ()))),
            'rows':rows,
            'example_reasons':gate.get('examples_reason_codes', [])}


def _historical_examples(trace: dict, evidence: dict, projection: dict) -> list[dict]:
    """Chỉ hiển thị mã cổ phiếu, ngày và lợi nhuận có trong bằng chứng đã lưu."""
    if 'selected_ids' in trace:
        prefix = (trace.get('request') or {}).get('prefix') or ''
        returns = dict(re.findall(r'^([^\s]+) T/P/A/I=[+0-]+ [WL] ([+-]?[\d.eE+-]+%)$', prefix, re.M))
        records = [{'episode_id':key, 'prompt_return':returns.get(key)} for key in trace['selected_ids']]
    else:
        records = projection.get('exemplars') or evidence.get('tasks') or []
    examples = []
    for record in records:
        identifier = re.fullmatch(r'([A-Z0-9]+)[:-](\d{4}-\d{2}-\d{2})', record.get('episode_id') or '')
        symbol, day = identifier.groups() if identifier else (None, None)
        value = (record.get('outcome') or {}).get('net_return_pct')
        if 'r_net_fraction' in record:
            value = 100 * record['r_net_fraction']
        examples.append({'symbol':record.get('symbol') or symbol, 'date':record.get('as_of_date') or day,
                         'exit_date':record.get('exit_date'),
                         'net_return':f'{value:+.2f}%' if value is not None else record.get('prompt_return')})
    return examples


def project(data: dict, language: str, *, articles: list[dict] | None = None) -> dict:
    """Chiếu báo cáo đã lưu, không gọi model hoặc tính lại policy."""
    if not can_project(data):
        raise ValueError('Bố cục phân tích chỉ nhận một kết quả realtime 1D hoàn tất')
    request = data['identity']['request']
    finalized = request['version'] == FINALIZED
    ids = data['requested_ids']
    variant = ids[0]
    row = next(row for row in data['rows'] if row['requested_id'] == variant and row['repeat'] == 0)
    point = row['point_id']
    payload = data['snapshots'][point]['payload']
    details = data['policy_details']
    detail = details[f'forecast/{point}/r0/{variant}']
    executed = details[f"forecast/{point}/r0/{row['executed_id']}"]
    reply = deepcopy(executed['raw_reply'] or {})
    # Policy có thể giữ anchor/common thay đề xuất raw; UI luôn hiện quyết định cuối đã durable.
    reply['decision'] = row['final_prediction']
    reply.setdefault('forecast_horizon','T+2.5')
    reports = {role:str(escape(payload.get(role+'_report') or '')) for role in ('indicator','pattern','trend','alpha')}
    from utils.analysis_sentiment_view import sentiment_view
    source_sentiment = payload.get('sentiment_data') or {}
    sentiment = (deepcopy(source_sentiment) if finalized else
                 sentiment_view(source_sentiment,articles,row['symbol'],row['as_of_date']))
    if finalized:
        sentiment['model_used'] = sentiment.get('scorer_version')
        scored = sentiment.get('scored_articles') or []
        main = sentiment.get('main_sentiment') or {}
        if main.get('avg_score') is not None:
            score = main['avg_score']
            main['label'] = 'positive' if score > .1 else 'negative' if score < -.1 else 'neutral'
            label_order = ('negative','positive','neutral')
            labels = []
            for article in scored:
                probabilities = article.get('probabilities')
                labels.append(label_order[probabilities.index(max(probabilities))] if probabilities else article.get('label'))
            sentiment['distribution_available'] = (len(labels) == main['article_count'] and
                                                   all(label in label_order for label in labels))
            if sentiment['distribution_available']:
                main.update(positive=labels.count('positive'),negative=labels.count('negative'),neutral_count=labels.count('neutral'))
    chart = data.get('realtime_chart') or payload.get('price_prefix') or {}
    candles = len(chart.get('Datetime',[]))
    result = {'success':True,'serving_analysis':True,'report_language':'vi','asset_name':row['symbol'],'timeframe':'1D',
        'data_length':min(45,candles) if finalized else candles, 'technical_indicators':reports['indicator'],
        'pattern_analysis':reports['pattern'],'trend_analysis':reports['trend'],'alpha_analysis':reports['alpha'],
        'pattern_chart':payload.get('pattern_image') or '', 'trend_chart':payload.get('trend_image') or '',
        'sentiment_data':sentiment,'sentiment_analysis':str(escape(payload.get('sentiment_report') or '')),
        'final_decision':reply,'analysis_version_id':variant,'analysis_version':LABELS[variant][int(language=='en')],
        'run_id':data['run_id'],'execution_profile':request['version'],'analysis_cutoff':row['as_of_date'],
        'analysis_captured_at':(data.get('live_input') or {}).get('captured_at'), 'final_action':row['final_action'],
        'research_profile':finalized,'scientific_status':data.get('scientific_status')}
    result['ui_report_pairs']=deepcopy(data.get('presentations',{}).get(point,{}))
    if executed.get('display_en'):
        result['ui_report_pairs']['decision']={'vi':reply,'en':deepcopy(executed['display_en'])}
    common = payload.get('causal_alpha',{}).get('projection') or {}
    if finalized:
        result['research_alpha_factors'] = deepcopy(common.get('factors') or [])
        result['research_alpha_selector'] = common.get('selector_sha256')
        result['research_alpha_statistics'] = selector_statistics(row['symbol'], row['as_of_date'],
            request.get('snapshot_id'), result['research_alpha_selector'])
        result['research_alpha_counts'] = {signal:sum(factor['signal'] == signal for factor in result['research_alpha_factors'])
                                           for signal in ('TĂNG','GIẢM','TRUNG TÍNH')}
        result['research_news_missing_reason'] = sentiment.get('missing_reason')
        result['research_news_count'] = sentiment.get('verified_article_count')
        result['live_news'] = deepcopy(sentiment.get('live_news'))
    elif variant != 'original_fix':
        result.update(common_alpha_analysis=str(escape(common.get('report') or '')),
            common_alpha_factors=deepcopy(common.get('factors') or []),common_alpha_cutoff=common.get('cutoff'),
            common_alpha_selector=common.get('selector_sha256'))
    if variant != 'original_fix':
        trace = detail['context'].get('trace') or {}
        aux = detail['context'].get('aux') or {}
        evidence = trace.get('evidence') or trace.get('retrieval') or {}
        prefix = (trace.get('request') or {}).get('prefix')
        statistics = _saved_prior_statistics(trace, evidence, row['raw_prediction'] is not None and
                                             bool(prefix or trace.get('retrieval')))
        branch = aux.get('branch') or {}
        mt_projection = branch.get('projection') or {}
        reasons = [value for value in (trace.get('reason'),row.get('fallback_reason'),row.get('bypass_reason'),detail['policy'].get('reason')) if value]
        fallback = row['executed_id'] != variant
        baseline = next((item['final_prediction'] for item in data['rows'] if item['requested_id']=='original_common'),None)
        result['bicl'] = {'method':METHODS[variant][int(language=='en')],
            'status':(('Không áp dụng đề xuất riêng; dùng ' if fallback else 'Đã xử lý bằng ') if language!='en' else
                      ('Separate proposal not applied; using ' if fallback else 'Processed with '))+LABELS[row['executed_id']][int(language=='en')],
            'reason':' · '.join(dict.fromkeys(reasons)), 'raw':row['raw_prediction'], 'final':row['final_prediction'],
            'action':row['final_action'],'cutoff':row['as_of_date'],'captured_at':result['analysis_captured_at'],
            'baseline':baseline,
            'application_note':(('Support hoặc policy không cho áp dụng đề xuất riêng; quyết định cuối được giữ từ nhánh thực thi ghi dưới đây.' if fallback else
                                 'Ngữ cảnh đã được xử lý theo phương pháp đã chọn; quyết định cuối và lý do bên trên lấy từ phản hồi/policy đã lưu.') if language!='en' else
                                ('Support or policy prevented a separate proposal; the final decision comes from the executed branch below.' if fallback else
                                 'Context was processed by the selected method; the final decision and reasoning above come from the recorded reply and policy.')),
            'examples':_historical_examples(trace, evidence, mt_projection),
            'regime':evidence.get('current_regime') or evidence.get('metadata',{}).get('current_regime'),
            'statistics':statistics,
            'groups':[{key:group.get(key) for key in ('n','wins','mean_r_net_fraction')}
                       for group in mt_projection.get('summary', [])],
            'facts':{key:value for key,value in (aux.get('packet') or {}).get('numeric',{}).items()
                     if key in ('close','sma20','macd','signal')}}
    if result.get('bicl'):
        result['ui_bicl_views']={lang:{'method':METHODS[variant][index],
            'status':(('Executed version: ' if index else 'Phiên bản thực thi: ')+LABELS[row['executed_id']][index]),
            'application_note':('Context and policy below come from the recorded analysis.' if index else 'Ngữ cảnh và policy bên dưới lấy từ kết quả phân tích đã lưu.')} for index,lang in enumerate(('vi','en'))}
    return result
