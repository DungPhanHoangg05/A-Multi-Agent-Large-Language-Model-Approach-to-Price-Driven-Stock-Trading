"""Lỗi capture có mã/giai đoạn và lời giải thích an toàn, không phản chiếu key hoặc body provider."""
from __future__ import annotations

from typing import Any,Callable

MESSAGES = {
    'chart.fetch':('Không lấy được nến khung đã chọn từ VCI/KBS.','Could not load the selected timeframe from VCI/KBS.'),
    'chart.validate':('Nến khung chọn có timestamp hoặc OHLCV không hợp lệ.','The selected chart has invalid timestamps or OHLCV.'),
    'prices.daily':('Không lấy được giá ngày của cổ phiếu từ VCI/KBS.','Could not load daily stock prices from VCI/KBS.'),
    'prices.validate':('Giá ngày cổ phiếu có lịch hoặc OHLCV không hợp lệ.','Daily stock timestamps or OHLCV are invalid.'),
    'index.daily':('Không lấy được ngày/Close VNINDEX từ VCI/KBS.','Could not load VNINDEX dates/Close from VCI/KBS.'),
    'index.intraday':('Không lấy được Close VNINDEX intraday khi cần bổ sung phiên đang diễn ra.','Could not load intraday VNINDEX Close for the current session.'),
    'index.validate':('Ngày hoặc Close VNINDEX không hợp lệ, thiếu hoặc vượt cutoff.','VNINDEX dates or Close are invalid, missing or beyond the cutoff.'),
    'news.fetch':('Không lấy hoặc chấm được tin có ngày cho snapshot.','Could not load or score dated news for the snapshot.'),
    'news.validate':('Tin hoặc scorer không khớp hợp đồng point-in-time.','News or its scorer violates the point-in-time contract.'),
    'snapshot.validate':('Snapshot thiếu support, lịch/đơn vị không đồng bộ hoặc dữ liệu chưa đủ.','The snapshot has insufficient support or inconsistent dates/price units.'),
}


class CaptureError(ValueError):
    """Chỉ enum giai đoạn của server đi vào UI/log, không dùng raw exception từ mạng."""
    def __init__(self, stage: str) -> None:
        if stage not in MESSAGES: stage = 'snapshot.validate'
        self.stage = stage
        self.code = 'CAPTURE_'+stage.upper().replace('.','_')
        super().__init__(MESSAGES[stage][0])

    def document(self) -> dict:
        """UI VI/EN nhận cùng code/stage, không cần suy đoán từ HTTP409 chung."""
        vi,en = MESSAGES[self.stage]
        return {'code':self.code,'stage':self.stage,'message':{'vi':vi,'en':en},'retryable':self.stage.endswith(('fetch','daily','intraday'))}


def at(stage: str, function: Callable, *args: Any, **kwargs: Any) -> Any:
    """Định vị biên lỗi; không nuốt thành neutral/CASH hoặc trả dữ liệu frozen thay thế."""
    try:
        return function(*args,**kwargs)
    except CaptureError:
        raise
    except (ValueError,OSError,KeyError,TypeError):
        raise CaptureError(stage) from None
