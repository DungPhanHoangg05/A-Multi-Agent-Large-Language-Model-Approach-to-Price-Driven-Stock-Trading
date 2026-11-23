"""I/P/T từ khung được chọn, Alpha/prior/MT từ ngày: cùng thời điểm capture và mục tiêu T+2.5."""
from __future__ import annotations

from copy import deepcopy

from core.serving_live.provider import LiveProvider
from core.historical_signals import snapshot_payload


class TimeframeProvider(LiveProvider):
    """Không thay nhãn daily bằng ba nến intraday, không huấn luyện lại model trên query."""
    def state(self, symbol: str, cutoff: str) -> dict:
        """Báo cáo kỹ thuật và ảnh nhận đúng nến/timestamp khung người dùng chọn."""
        state = super().state(symbol,cutoff)
        state.update(kline_data=deepcopy(self.record['chart']),time_frame=self.record['chart_timeframe'],
                     chart_timeframe=self.record['chart_timeframe'])
        return state

    def role_state(self, role: str, state: dict) -> dict:
        """Native Alpha tiếp tục nhận 600 nến ngày và horizon ba phiên, không phải ba bar."""
        result = deepcopy(state)
        if role == 'full':
            prefix = self.prefix(self.points[0])
            result.update(kline_data=snapshot_payload(prefix.tail(45)),time_frame='1d')
        return result

    def snapshot(self, point: dict, state: dict) -> dict:
        """Adapter Decision giữ ABI ngày; reports đã chứa tín hiệu khung chọn và nguồn chart riêng."""
        projected = deepcopy(state)
        projected['time_frame'] = '1d'
        return super().snapshot(point,projected)

    def prepare(self, variant: str, snapshot: object, dependencies: dict, repeat: int) -> dict:
        """Sidecar nêu rõ chart timeframe, daily context và nến ngày provisional nếu có."""
        result = super().prepare(variant,snapshot,dependencies,repeat)
        result['trace']['live_input'].update(chart_timeframe=self.record['chart_timeframe'],
            context_timeframe='1d',daily_provisional=self.record['daily_provisional'],target='OPEN_T1_CLOSE_T3_NET')
        return result
