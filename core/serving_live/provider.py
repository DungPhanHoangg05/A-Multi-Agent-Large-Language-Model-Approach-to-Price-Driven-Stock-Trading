"""Provider dùng giá/tin mới nhưng giữ adapter, dependency và upstream một lần."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd

from core.causal_alpha import PROFILE, FrozenSelector, alpha_values, frame_document
from core.causal_bridge import bind_snapshot
from core.historical_evaluation_data import FrozenNews
from core.historical_signals import snapshot_payload
from core.serving_runtime.providers import AsOfProvider
from core.serving_live.context import bind_context
from core.serving_live.snapshots import frame
from core.unified_contracts import digest
from core.unified_methods import snapshot_from_graph
from core.ui_presentation.live import LivePresentation


class LiveSelector:
    """Chuyển top5/threshold đã kiểm sang nguồn mới; không gán replay nguồn live là parity frozen."""
    def __init__(self, artifact: dict, training_frame: pd.DataFrame) -> None:
        frozen = FrozenSelector(artifact,training_frame)
        self.payload = deepcopy(artifact['payload'])
        self.sha256 = digest({'version':'live_frozen_selector_transfer_v1','frozen_selector_sha256':frozen.sha256,
                              'query_source':'LIVE_VENDOR_PREFIX; NO_QUERY_FIT'})

    def predict(self, prefix: pd.DataFrame, cutoff: str) -> dict:
        """Chỉ áp dụng công thức PIT tại query, không fit/chọn threshold hoặc đọc query-y."""
        if (len(prefix) < 600 or str(prefix.Datetime.iloc[-1].date()) != cutoff
                or self.payload['schedule']['test_start'] > cutoff):
            raise ValueError('Query live thiếu prefix hoặc trước thời điểm đóng băng selector')
        values = alpha_values(prefix)
        rows = []
        for selected in self.payload['selected']:
            value = float(values[selected['alpha_id']].iloc[-1]*selected['orientation'])
            if not np.isfinite(value): raise ValueError('Factor live không khả dụng; không fill zero')
            signal = 'TĂNG' if value > self.payload['threshold'] else 'GIẢM' if value < -self.payload['threshold'] else 'TRUNG TÍNH'
            rows.append({'alpha_id':selected['alpha_id'],'value':value,'signal':signal,'available':True,'orientation':selected['orientation']})
        report = 'Alpha causal_common_v1; top5/threshold frozen áp dụng trên giá live; chưa chứng nhận hiệu quả.\n'+'\n'.join(
            f"{row['alpha_id']}: {row['value']:+.6f}; {row['signal']}" for row in rows)
        result = {'version':PROFILE,'cutoff':cutoff,'selector_sha256':self.sha256,'history_sha256':digest(frame_document(prefix)),
            'factors':rows,'report':report,'scope':'LIVE_FROZEN_SELECTION_TRANSFER; EXPLORATORY_NOT_CERTIFIED'}
        return {**result,'projection_sha256':digest(result)}


class LiveProvider(LivePresentation,AsOfProvider):
    """Tái dùng nguyên shared I/P/T/native và MethodAdapters; chỉ thay nguồn query đã seal."""
    def __init__(self, root: Path, points: list[dict], models: dict, variants: list[str], record: dict) -> None:
        super().__init__(root,points,models,variants)
        from core.unified_protocol import read
        symbol, cutoff = record['symbol'], record['cutoff']
        frozen_prices = self.prices[symbol]
        source = self.alpha['causal_sources'][symbol+'/f2026_q3']
        self.selectors[symbol] = LiveSelector(read(root,source['selector']),frozen_prices)
        self.record = deepcopy(record)
        self.prices[symbol] = frame(record['prices'])
        from core.realtime_index import index_frame
        index = index_frame(record['index'])
        previous = self.data.history
        self.data.history = pd.concat([previous,index.loc[index.Datetime > previous.Datetime.iloc[-1]]],ignore_index=True)
        if str(self.data.history.Datetime.iloc[-1].date()) != cutoff:
            raise ValueError('Live query phải sau lịch historical đã đóng băng')
        self.data.calendar = pd.DatetimeIndex(self.data.history.Datetime)
        if self.bank is not None:
            selector_module = self.bank.scope.module('prior_example_selection')
            self.bank.selector = selector_module.PriceExampleSelector(self.bank.index,self.data.calendar)
        self.data.news = FrozenNews({symbol:deepcopy(record['news'])})

        def features(code: str, date: str) -> dict:
            if code != symbol or date != cutoff: raise ValueError('Feature live sai mã/ngày')
            prefix = self.prefix(points[0])
            return self.data.scope.features(prefix,[],self.data.calendar,date,source=self.data.scope.source)

        self.data.features = features
        self.data.state = self.state
        if self.context is not None:
            bind_context(self.context,self.data,symbol,self.prices[symbol],cutoff)

    def state(self, symbol: str, cutoff: str) -> dict:
        """Flag is_backtest là ABI PIT để tránh crawler/LLM ẩn; identity job vẫn data_source=live."""
        prefix = self.prefix({'symbol':symbol,'cutoff':cutoff})
        return {'stock_name':symbol,'as_of_date':cutoff,'window_end_date':cutoff,'time_frame':'1d','language':'vi',
            'is_backtest':True,'messages':[],'kline_data':snapshot_payload(prefix.tail(45)),
            'point_in_time_df':prefix.tail(600).copy(deep=True),'sentiment_store':self.data.news,
            'alpha_norm_method':'zscore_tanh','alpha_weights':None}

    def validate_point(self, point: dict) -> None:
        """Kiểm live selector/facts/news trước vision; không refit hoặc đọc payoff query."""
        self.selectors[point['symbol']].predict(self.prefix(point),point['cutoff'])
        self.data.news.get_sentiment_at(point['symbol'],point['cutoff'])
        self.facts(point)

    def snapshot(self, point: dict, state: dict) -> dict:
        """Native/common dùng đúng một prefix sống; provenance bind toàn bộ capture hash."""
        prefix = self.prefix(point)
        source_sha = digest(frame_document(prefix))
        snapshot = snapshot_from_graph(point,0,state,prefix.tail(600),source_sha,[])
        result = bind_snapshot(snapshot,self.selectors[point['symbol']],prefix,source_sha).document()
        return result

    def prepare(self, variant: str, snapshot: object, dependencies: dict, repeat: int) -> dict:
        """Ghi rõ lịch query dự kiến và bank frozen trong sidecar, không sửa prompt policy."""
        result = super().prepare(variant,snapshot,dependencies,repeat)
        result['trace']['live_input'] = {'captured_at':self.record['captured_at'],
            'calendar_policy':self.record['calendar_policy'],'corporate_actions':self.record['corporate_actions'],
            'context_labels':'FROZEN_BEFORE_2026_07_01; NO_LIVE_QUERY_LABELS'}
        return result

    def outcome(self, point: dict) -> dict:
        """Phân tích mới nhất không có nhãn t+3, không tạo P&L giả."""
        raise ValueError('Live analysis không được đọc outcome query')
