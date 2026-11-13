"""Khóa dữ liệu thị trường trước forecast; resume không tải lại giá hoặc tin mới."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

import pandas as pd

from core.causal_alpha import frame_document, validated_frame
from core.historical_evaluation_data import FrozenNews
from core.historical_evaluation_journal import load, save
from core.historical_evaluation_scope import SYMBOLS
from core.unified_contracts import checksum, digest

VERSION = 'serving_live_daily_v1'
ZONE = ZoneInfo('Asia/Ho_Chi_Minh')


def market_prices(symbol: str) -> pd.DataFrame:
    """VCI/KBS theo loader hiện hữu; cần đủ lịch dài, không dùng cache 200 nến của UI cũ."""
    from core.realtime_loader import fetch_realtime_ohlcv
    frame, error = fetch_realtime_ohlcv(symbol, '1d', lookback_days=3600, tail=3000, use_cache=False)
    if error or frame.empty:
        raise ValueError('Không lấy được nguồn giá ngày mới nhất')
    return frame


def market_news(symbol: str, cutoff: str) -> list[dict]:
    """Tin có ngày mới được chấm; không gọi LLM và không đưa tin undated vào snapshot."""
    from data_manager.sentiment_cache import _crawl_articles_full, _score_articles
    rows = _crawl_articles_full(symbol, max_articles=30, max_pages=2)
    # Ngày-only chỉ coi là khả dụng từ ngày kế tiếp, thống nhất FrozenNews.
    visible = [row for row in rows if row.get('date_parsed') and row['date_parsed'] < cutoff]
    scored = _score_articles(visible)
    names = {'5CD-AI/Vietnamese-Sentiment-visobert':'visobert','viquant-lexicon-v1':'lexicon'}
    for row in scored:
        source = row['scorer']
        if source not in names:
            raise ValueError('Scorer tin live không thuộc backend đã biết')
        # Giữ tên backend gốc trong sidecar; FrozenNews nhận enum đã khóa của research.
        row['scorer_source'] = source
        row['scorer'] = names[source]
    return scored


def clean(frame: pd.DataFrame, maximum: pd.Timestamp) -> pd.DataFrame:
    """Từ chối nến tương lai; loại riêng nến phiên hiện tại chưa hoàn tất trước 15:30 VN."""
    frame = frame.copy(deep=True)
    frame['Datetime'] = pd.to_datetime(frame['Datetime'])
    checked = validated_frame(frame)
    if (checked.Datetime > maximum.normalize()).any():
        raise ValueError('Nguồn thị trường chứa nến tương lai')
    return checked.loc[checked.Datetime >= pd.Timestamp('2018-01-02')].reset_index(drop=True)


class Snapshots:
    """Kho nội bộ theo owner và SHA; chỉ endpoint capture được phép truy cập mạng."""
    def __init__(self, directory: Path, *, prices: Callable = market_prices,
                 news: Callable = market_news, now: Callable | None = None) -> None:
        self.directory = directory
        self.prices, self.news = prices, news
        self.now = now or (lambda: datetime.now(ZONE))

    def path(self, identifier: str) -> Path:
        """ID là SHA đầy đủ, không nhận đường dẫn hoặc alias từ trình duyệt."""
        if not checksum(identifier):
            raise ValueError('Snapshot ID không hợp lệ')
        path = self.directory / (identifier + '.json')
        if path.is_symlink() or not path.resolve().is_relative_to(self.directory.resolve()):
            raise ValueError('Snapshot thoát kho private')
        return path

    def capture(self, symbol: str, owner: str) -> dict:
        """Giá/tin/VNINDEX cùng cutoff; không nhập nhãn hoặc forecast historical đã thực hiện."""
        if symbol not in SYMBOLS or not checksum(owner):
            raise ValueError('Mã hoặc owner ngoài miền live')
        now = self.now().astimezone(ZONE)
        today = pd.Timestamp(now.date())
        stock, index = clean(self.prices(symbol), today), clean(self.prices('VNINDEX'), today)
        closed = today if (now.hour, now.minute) >= (15, 30) else today-pd.Timedelta(days=1)
        index = index.loc[index.Datetime <= closed].copy()
        if len(index) < 600:
            raise ValueError('VNINDEX thiếu 600 phiên đã hoàn tất')
        cutoff = str(index.Datetime.iloc[-1].date())
        if (today-pd.Timestamp(cutoff)).days > 10:
            raise ValueError('Dữ liệu thị trường quá cũ để gọi là mới nhất')
        stock = stock.loc[stock.Datetime <= pd.Timestamp(cutoff)].copy()
        if len(stock) < 600 or str(stock.Datetime.iloc[-1].date()) != cutoff:
            raise ValueError('Cổ phiếu thiếu 600 phiên hoặc chưa đồng bộ phiên VNINDEX')
        if not pd.DatetimeIndex(stock.Datetime).isin(pd.DatetimeIndex(index.Datetime)).all():
            raise ValueError('Giá cổ phiếu có phiên ngoài lịch VNINDEX')
        articles = self.news(symbol, cutoff)
        dated = []
        for row in articles:
            published = row.get('date_parsed')
            if not published:
                continue
            if pd.Timestamp(published) > pd.Timestamp(cutoff):
                raise ValueError('Tin tức vượt cutoff')
            dated.append(row)
        frozen = FrozenNews({symbol: dated})
        frozen.get_sentiment_at(symbol, cutoff)  # Kiểm score/availability trước khi ghi hoặc gọi vision.
        record = {'version':VERSION, 'owner_scope_sha256':owner, 'symbol':symbol, 'cutoff':cutoff,
            'captured_at':now.isoformat(), 'prices':frame_document(stock), 'index':frame_document(index),
            'news':dated, 'calendar_policy':'OBSERVED_VNINDEX; QUERY_T1_T3_WEEKDAY_PLAN_ONLY',
            'price_unit':'thousand_VND', 'source':'VNSTOCK_VCI_KBS_VENDOR_SERIES_LIMITED',
            'corporate_actions':'LIVE_EVENT_LEDGER_UNAVAILABLE; VENDOR_ADJUSTMENT_RISK',
            'scientific_status':'EXPLORATORY_LIVE_INPUT; NOT_CERTIFIED'}
        identifier = digest(record)
        path = self.path(identifier)
        if path.exists():
            if load(path) != record: raise ValueError('Snapshot SHA xung đột')
        else:
            save(path, record)
        return self.summary(identifier, record)

    def read(self, identifier: str, owner: str | None = None) -> dict:
        """Kiểm hash/owner mỗi lần đọc; không tải lại nguồn dù snapshot đã cũ khi resume."""
        record = load(self.path(identifier))
        if digest(record) != identifier or record['version'] != VERSION:
            raise ValueError('Snapshot sống khác hash/version đã khóa')
        if owner is not None and record['owner_scope_sha256'] != owner:
            raise PermissionError('Snapshot không thuộc owner này')
        return record

    @staticmethod
    def summary(identifier: str, record: dict) -> dict:
        """Metadata công khai không có key hoặc đường dẫn máy chủ."""
        return {key:record[key] for key in ('symbol','cutoff','captured_at','source','price_unit','calendar_policy','corporate_actions','scientific_status')} | {
            'snapshot_id':identifier, 'price_rows':len(record['prices']['Datetime']), 'news_articles':len(record['news'])}


def frame(value: dict) -> pd.DataFrame:
    """Mỗi provider sở hữu DataFrame riêng từ bytes snapshot đã kiểm."""
    result = pd.DataFrame(value)
    result['Datetime'] = pd.to_datetime(result.Datetime)
    return validated_frame(result)
