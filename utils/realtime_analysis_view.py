"""Chiếu một phân tích realtime hoàn tất sang bố cục Original, giữ decision/policy và nguồn BICL."""
from __future__ import annotations

from copy import deepcopy
import json

from markupsafe import escape

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


def project(data: dict, language: str, *, articles: list[dict] | None = None) -> dict:
    """Không gọi model/tái tính policy; chỉ một bản, một point, một repeat realtime 1D đã hoàn tất."""
    request = data['identity']['request']
    ids = data['requested_ids']
    if (data['state'] != 'completed' or request['mode'] != 'analyze' or request.get('data_source') != 'live'
            or request.get('chart_timeframe') != '1d' or request['repeats'] != 1 or len(ids) != 1
            or ids[0] not in MAIN_IDS or len(data['snapshots']) != 1):
        raise ValueError('Bố cục phân tích chỉ nhận một kết quả realtime 1D hoàn tất')
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
    sentiment = sentiment_view(payload.get('sentiment_data') or {},articles,row['symbol'],row['as_of_date'])
    chart = data.get('realtime_chart') or payload.get('price_prefix') or {}
    result = {'success':True,'serving_analysis':True,'asset_name':row['symbol'],'timeframe':'1D',
        'data_length':len(chart.get('Datetime',[])), 'technical_indicators':reports['indicator'],
        'pattern_analysis':reports['pattern'],'trend_analysis':reports['trend'],'alpha_analysis':reports['alpha'],
        'pattern_chart':payload.get('pattern_image') or '', 'trend_chart':payload.get('trend_image') or '',
        'sentiment_data':sentiment,'sentiment_analysis':str(escape(payload.get('sentiment_report') or '')),
        'final_decision':reply,'analysis_version':LABELS[variant][int(language=='en')]}
    if variant != 'original_fix':
        common = payload.get('causal_alpha',{}).get('projection') or {}
        result.update(common_alpha_analysis=str(escape(common.get('report') or '')),
            common_alpha_factors=deepcopy(common.get('factors') or []),common_alpha_cutoff=common.get('cutoff'),
            common_alpha_selector=common.get('selector_sha256'))
        trace = detail['context'].get('trace') or {}
        aux = detail['context'].get('aux') or {}
        evidence = trace.get('evidence') or trace.get('retrieval') or {}
        reasons = [value for value in (trace.get('reason'),row.get('fallback_reason'),row.get('bypass_reason'),detail['policy'].get('reason')) if value]
        fallback = row['executed_id'] != variant
        baseline = next((item['final_prediction'] for item in data['rows'] if item['requested_id']=='original_common'),None)
        result['bicl'] = {'method':METHODS[variant][int(language=='en')],
            'status':(('Không áp dụng đề xuất riêng; dùng ' if fallback else 'Đã xử lý bằng ') if language!='en' else
                      ('Separate proposal not applied; using ' if fallback else 'Processed with '))+LABELS[row['executed_id']][int(language=='en')],
            'reason':' · '.join(dict.fromkeys(reasons)), 'raw':row['raw_prediction'], 'final':row['final_prediction'],
            'action':row['final_action'],'cutoff':row['as_of_date'],'captured_at':data['live_input']['captured_at'],
            'baseline':baseline,
            'application_note':(('Support hoặc policy không cho áp dụng đề xuất riêng; quyết định cuối được giữ từ nhánh thực thi ghi dưới đây.' if fallback else
                                 'Ngữ cảnh đã được xử lý theo phương pháp đã chọn; quyết định cuối và lý do bên trên lấy từ phản hồi/policy đã lưu.') if language!='en' else
                                ('Support or policy prevented a separate proposal; the final decision comes from the executed branch below.' if fallback else
                                 'Context was processed by the selected method; the final decision and reasoning above come from the recorded reply and policy.')),
            'prior_count':len(evidence['tasks']) if 'tasks' in evidence else None,
            'tasks':[{'id':task.get('episode_id'),'symbol':task.get('symbol'),'exit_date':task.get('exit_date')} for task in evidence.get('tasks',[])],
            'regime':evidence.get('current_regime') or evidence.get('metadata',{}).get('current_regime'),
            'prefix':trace.get('request',{}).get('prefix'),
            'details':json.dumps({'context':detail['context'],'policy':detail['policy'],'raw_reply':detail['raw_reply']},ensure_ascii=False,indent=2),
            'evidence':json.dumps(evidence or aux,ensure_ascii=False,indent=2)}
    return result
