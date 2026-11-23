"""Đối chiếu số, mã và công thức giữa hai bản ngôn ngữ của báo cáo."""
from collections import Counter
import re

NUMBERS = re.compile(r'(?<![\w])[-+−–]?\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?%?')
CODES = re.compile(r'`[^`]+`|https?://[^\s)]+|\b(?:LONG|SHORT|CASH|BHN|CMG|FPT|HVN|MBB|MWG|VCB|VJC|VNM|VNINDEX|MACD|RSI|ROC|(?:SMA|EMA|MA)\d+|WQ\d+[A-Za-z0-9_]*|[A-Z]+(?:_[A-Za-z0-9]+)+)\b|%[KDR]\b')
VI_WORDS = re.compile(r'\b(?:phân tích|tín hiệu|công thức|giá trị|diễn giải|nhận xét|tăng|giảm|trung tính|không có|đáng tin|khả dụng)\b',re.I)
PROTECTED = re.compile(CODES.pattern+'|'+NUMBERS.pattern+r'|\*\*|__|[|*]')


class TranslationError(ValueError):
    """Bản dịch thiếu đoạn hoặc thay số/mã; không suy nội dung thay thế."""


def validate_translation(source: str, translated: str, target: str) -> None:
    """Giữ số/mã/công thức và từ chối bản EN vẫn nguyên câu VI phổ biến."""
    if type(translated) is not str or not translated.strip() or Counter(NUMBERS.findall(source))!=Counter(NUMBERS.findall(translated)) or Counter(CODES.findall(source))!=Counter(CODES.findall(translated)):
        raise TranslationError('Bản dịch đã đổi số, mã hoặc công thức')
    if target=='en' and VI_WORDS.search(translated):
        raise TranslationError('Bản dịch chưa đúng tiếng Anh')
