"""Chuyển query MT-BICL sang prefix mới; labels/context và weights vẫn frozen."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

import pandas as pd


class LiveStream:
    """Chỉ x của query mới; advance không sinh nhãn mới hoặc đọc entry/exit query."""
    def __init__(self, frozen: Any, calendar: pd.DatetimeIndex, features: Any, cutoff: str) -> None:
        self.frozen, self.calendar, self.query_features, self.cutoff = frozen, calendar, features, cutoff
        self.freeze_before = frozen.freeze_before

    def advance(self, cutoff: str) -> list[dict]:
        """Giữ đúng tập cycle đã mature trước freeze của nghiên cứu."""
        return self.frozen.advance(cutoff)

    def features(self, symbol: str, cutoff: str) -> dict:
        """Không splice chuỗi vendor live vào lịch sử đã dùng để sinh labels."""
        return self.query_features(symbol,cutoff) if cutoff == self.cutoff else self.frozen.features(symbol,cutoff)


def bind_context(context: Any, data: Any, symbol: str, prefix: pd.DataFrame, cutoff: str) -> None:
    """Mở lịch query bằng phiên đã quan sát; t+1/t+3 chỉ là lịch kế hoạch, không payoff."""
    bucket = context.context.builder
    # TaskBuilder cần metadata entry/exit để kiểm khoảng; đây không phải lịch khớp lệnh.
    # Không có giá cho ba ngày kế hoạch, không đưa chúng vào features/HMM hoặc oracle.
    observed = pd.DatetimeIndex(data.history.Datetime)
    planned = pd.bdate_range(pd.Timestamp(cutoff)+pd.Timedelta(days=1), periods=3)
    calendar = observed.union(planned)
    stream = LiveStream(context.view,calendar,data.features,cutoff)
    context.view = stream
    bucket.view.source = stream
    bucket.view.calendar = calendar
    historical_packet = bucket.view.packet
    make_packet = data.scope.module('mt_bicl_features').make_fact_packet
    def packet(code: str, date: str) -> dict:
        """Facts prior giữ nguồn cùng labels frozen; chỉ facts query nhận chuỗi vendor live."""
        if code == symbol and date == cutoff:
            return make_packet(prefix,code,date)
        return historical_packet(code,date)
    bucket.view.packet = packet
    builder = bucket.builder
    builder.calendar = calendar
    builder._days = calendar.strftime('%Y-%m-%d').tolist()
    builder._positions = {day:index for index,day in enumerate(builder._days)}
    # FrozenTimeline đã xác minh mọi model trên nguồn cũ trước khi nhận x live.
    builder.regimes._history = data.history[['Datetime','Close']].copy(deep=True)
    builder.regimes.calendar = calendar
