"""Dựng hai giao diện từ cùng số liệu đã tính; không chạy lại selector, agent hoặc LLM."""
from copy import deepcopy
import re
from utils.i18n import t,signal_label,get_horizon,confidence_label
from core.serving_runtime.quota import Failed


def indicator_english(data: dict, prices: dict) -> str:
    """Hiện đủ giá trị/cuỗi nến/tín hiệu từ kết quả Indicator đã tính một lần."""
    indicators,classified,summary=data['indicators'],data['classified'],data['summary']
    groups=[('MACD (12,26,9)','macd',[('MACD Line','macd'),('Signal Line','macd_signal'),('Histogram','macd_hist')]),
        ('RSI (14)','rsi',[('RSI','rsi')]),('ROC (10)','roc',[('ROC %','roc')]),
        ('Stochastic (14,3,3)','stoch',[('%K','stoch_k'),('%D','stoch_d')]),('Williams %R (14)','willr',[('%R','willr')])]
    lines=[]
    for title,key,series in groups:
        lines.extend(['### '+title,'| Indicator | Latest value | Last 5 candles |','|---|---|---|'])
        values=indicators.get(key,{})
        for label,name in series:
            from agents.indicator_agent import _lastn
            arr=_lastn(values.get(name,[]),5)
            lines.append(f"| {label} | {arr[-1] if arr else 'NA'} | {arr} |")
        lines.append('Signal: **'+signal_label(classified.get(key,{}).get('signal','TRUNG TÍNH'),'en')+'**\n')
    close=prices.get('Close',[])
    lines.extend(['### Price summary','Latest close: '+str(round(float(close[-1]),4) if close else 'NA'),'Last 5 closes: '+str([round(float(value),4) for value in close[-5:]]),
        'Moving averages: '+'; '.join('MA'+str(window)+'='+str(round(sum(close[-window:])/window,2) if len(close)>=window else 'NA') for window in (5,10,20)),
        '### Signal consensus',f"BULLISH: {summary['n_tang']}/{summary['total']}; BEARISH: {summary['n_giam']}/{summary['total']}; NEUTRAL: {summary['n_trung']}/{summary['total']}",
        '**'+signal_label(summary['consensus'],'en')+'** · Confidence: '+confidence_label(summary['confidence'],'en')])
    return '\n'.join(lines)


def alpha_english(data: dict, symbol: str, timeframe: str, expert: str='') -> str:
    """Giữ value/components/formula nguồn; chỉ chọn metadata EN của đúng alpha đã tuyển."""
    from core.alpha_compare import NEW_ALPHA_TEMPLATES,get_alpha_template
    from agents.alpha_agent import _build_alpha_report
    factors=deepcopy(data.get('alpha_results',[]))
    lookup={meta['name']:key for key,meta in NEW_ALPHA_TEMPLATES.items()}
    for factor in factors:
        identifier=lookup.get(factor['name'])
        if identifier:
            meta=get_alpha_template(identifier,'en')
            original=factor['interpretation']
            suffix=re.search(r'\(IC=[^)]*\)',original)
            factor.update(type=meta['type'],interpretation=meta['interp']+'. '+(suffix[0] if suffix else ''))
            if factor.get('components',{}).get('ic',0)<0: factor['interpretation']+=' '+t('ar_flipped_note','en')
        elif 'Adapted CURRENT_' in factor.get('formula',''):
            # Rank của factor không phải ID công thức CURRENT; không gán nhầm lời giải thích.
            identifier=factor['formula'].removeprefix('Adapted ')
            factor.update(name=identifier,type='Quantitative alpha',
                interpretation=f"Stored value {factor['value']}; signal {signal_label(factor['signal'],'en')}. Historical metrics and components are listed below.")
        else:
            # Các alpha mặc định có metadata i18n sẵn; không thay giá trị nguồn.
            from agents import alpha_agent
            factories=[alpha_agent._alpha1_fdm,alpha_agent._alpha2_sfa,alpha_agent._alpha3_lvr,alpha_agent._alpha4_bfe,alpha_agent._alpha5_ofe]
            index=factor['id']-1; tv=data.get('tech_vars',{})
            local=factories[index](data.get('sentiment_norm',{}),tv,'en') if index==1 else factories[index](tv,'en')
            factor.update(type=local['type'],interpretation=local['interpretation'],name=local['name'])
        factor['horizon']=get_horizon(timeframe,'en')['horizon_short']
    if not factors: raise Failed('INVALID_MODEL_OUTPUT')
    result=_build_alpha_report(factors,data.get('tech_vars',{}),data.get('sentiment_norm',{}),symbol,'en')
    up=sum(f['signal']=='TĂNG' for f in factors); down=sum(f['signal']=='GIẢM' for f in factors)
    consensus='TĂNG' if up>down else 'GIẢM' if down>up else 'TRUNG TÍNH'
    if expert: result+='\n### '+t('alpha_expert_note','en')+'\n'+expert+'\n'
    return result+f"\n**{t('alpha_summary','en')}: {signal_label(consensus,'en')} ({up} BULLISH / {down} BEARISH / {len(factors)-up-down} NEUTRAL)**\n"


def pair_for(role: str, state: dict, output: dict, captured: dict) -> dict:
    """Không ghi bản EN vào state canonical; chỉ tạo sidecar trình bày đã có đủ dữ liệu."""
    field=('alpha' if role=='full' else role)+'_report'; vi=output.get(field,'')
    if role=='indicator':
        en=captured.get('indicator',{}).get('en') or indicator_english(captured['_indicator_data'],state['kline_data'])
    elif role=='full': en=alpha_english(output['sentiment_data'],state['stock_name'],state['time_frame'],captured.get('alpha',{}).get('en',''))
    elif role=='pattern':
        from agents.pattern_agent import _enforce_pattern_markdown_format,_verify_pattern_against_ohlcv
        en=_verify_pattern_against_ohlcv(_enforce_pattern_markdown_format(captured['pattern']['en'],lang='en',kline_data=state['kline_data']),state['kline_data'],lang='en')
    else:
        from agents.trend_agent import _enforce_markdown_format,_verify_trend_against_ohlcv
        en=_verify_trend_against_ohlcv(_enforce_markdown_format(captured['trend']['en'],lang='en',kline_data=state['kline_data']),state['kline_data'],lang='en')
    return {'vi':vi,'en':en}


def sentiment_pair(data: dict) -> dict:
    """Báo cáo số tâm lý từ snapshot; tiêu đề bài báo luôn là trích dẫn nguyên nguồn."""
    main=data.get('main_sentiment') or data
    count=main.get('article_count',0); score=main.get('avg_score',main.get('weighted_score',main.get('average_score')))
    if score is None:
        return {'vi':'Chưa có dữ liệu tâm lý hợp lệ cho phân tích này.',
                'en':'No valid sentiment data is available for this analysis.'}
    return {'vi':f"Tâm lý thị trường: điểm={score}; số bài={count}.",
            'en':f"Market sentiment: score={score}; articles={count}."}
