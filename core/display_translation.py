"""Tách báo cáo thành các đoạn bắt buộc; số, mã và cấu trúc Markdown do server giữ."""
from collections import Counter
from dataclasses import dataclass
import re

NUMBERS = re.compile(r'(?<![\w])[-+−–]?\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?%?')
CODES = re.compile(r'`[^`]+`|https?://[^\s)]+|\b(?:LONG|SHORT|CASH|BHN|CMG|FPT|HVN|MBB|MWG|VCB|VJC|VNM|VNINDEX|MACD|RSI|ROC|(?:SMA|EMA|MA)\d+|WQ\d+[A-Za-z0-9_]*|[A-Z]+(?:_[A-Za-z0-9]+)+)\b|%[KDR]\b')
VI_WORDS = re.compile(r'\b(?:phân tích|tín hiệu|công thức|giá trị|diễn giải|nhận xét|tăng|giảm|trung tính|không có|đáng tin|khả dụng)\b',re.I)
MARKER = re.compile(r'⟪K\d+⟫')
PROTECTED = re.compile(CODES.pattern+'|'+NUMBERS.pattern+r'|\*\*|__|[|*]')


class TranslationError(ValueError):
    """Bản dịch thiếu đoạn hoặc thay số/mã; không suy nội dung thay thế."""


def batch_segments(segments: dict) -> list[dict[str,str]]:
    """Gộp đoạn ngắn của nhiều report để không tạo một HTTP request cho mỗi tiêu đề tin."""
    result=[]; batch={}; size=0
    for name,segment in segments.items():
        if batch and (size+len(segment.masked)>1500 or len(batch)>=16):
            result.append(batch); batch={}; size=0
        batch[name]=segment.masked; size+=len(segment.masked)
    if batch: result.append(batch)
    return result


def validate_translation(source: str, translated: str, target: str) -> None:
    """Giữ số/mã/công thức và từ chối bản EN vẫn nguyên câu VI phổ biến."""
    if type(translated) is not str or not translated.strip() or Counter(NUMBERS.findall(source))!=Counter(NUMBERS.findall(translated)) or Counter(CODES.findall(source))!=Counter(CODES.findall(translated)):
        raise TranslationError('Bản dịch đã đổi số, mã hoặc công thức')
    if target=='en' and VI_WORDS.search(translated):
        raise TranslationError('Bản dịch chưa đúng tiếng Anh')


@dataclass
class Segment:
    """Placeholder chỉ thay bằng byte nguồn sau khi kiểm đầy đủ inventory."""
    source: str
    masked: str
    values: list[str]

    def restore(self, translated: str, target: str) -> str:
        """Model không được bỏ, thêm hoặc đổi thứ tự dữ kiện của một đoạn."""
        if type(translated) is not str or MARKER.findall(translated)!=MARKER.findall(self.masked):
            raise TranslationError('Bản dịch thiếu hoặc đổi placeholder')
        result=MARKER.sub(lambda match:self.values[int(match[0][2:-1])],translated.strip())
        validate_translation(self.source,result,target)
        return result


class ReportPlan:
    """Một dòng/đoạn có ID riêng trong schema; model không dựng lại cả báo cáo."""
    def __init__(self, text: str) -> None:
        self.parts: list[tuple[bool,str]]=[]
        self.segments: dict[str,Segment]={}
        fenced=False
        for line in text.splitlines(keepends=True):
            if re.match(r'^\s*(```|~~~)',line):
                fenced=not fenced; self.parts.append((False,line)); continue
            if fenced or not line.strip() or re.fullmatch(r'[\s|:−\-_*]+',line):
                self.parts.append((False,line)); continue
            prefix=re.match(r'^\s*(?:(?:#{1,6}|>|[-+*]|\d+[.)])\s+)?',line)[0]
            content=line[len(prefix):]; raw=content.rstrip(); suffix=content[len(raw):]
            self.parts.append((False,prefix))
            # Không cắt số, công thức hoặc code; chỉ tách ở khoảng trắng giữa các atom.
            atoms=re.findall(PROTECTED.pattern+r'|\s+|[^\s]+',raw)
            current=''
            for atom in atoms:
                if len(current)+len(atom)>1000 and current:
                    self.add(current); current=''
                current+=atom
            if current: self.add(current)
            self.parts.append((False,suffix))

    def add(self, text: str) -> None:
        """Giữ khoảng trắng và các dòng chỉ có số/code tại server, không tốn model call."""
        if not text.strip(): self.parts.append((False,text)); return
        prefix=text[:len(text)-len(text.lstrip())]; raw=text.strip(); suffix=text[len(text.rstrip()):]
        self.parts.append((False,prefix))
        values=[]
        def protect(match: re.Match) -> str:
            values.append(match[0]); return '⟪K'+str(len(values)-1)+'⟫'
        if MARKER.search(raw): raise TranslationError('Nguồn trùng placeholder dịch')
        masked=PROTECTED.sub(protect,raw)
        if not re.search(r'[^\W\d_]',MARKER.sub('',masked),re.UNICODE): self.parts.append((False,raw))
        else:
            identifier='s'+str(len(self.segments))
            self.segments[identifier]=Segment(raw,masked,values); self.parts.append((True,identifier))
        self.parts.append((False,suffix))

    def batches(self) -> list[dict[str,str]]:
        """Giới hạn từng payload và inventory để schema/output nằm trong quota hiện hữu."""
        return batch_segments(self.segments)

    def render(self, translations: dict[str,str], target: str) -> str:
        """Mọi đoạn bắt buộc phải hiện diện trước khi xuất bản bản dịch một report."""
        if set(translations)!=set(self.segments): raise TranslationError('Bản dịch thiếu đoạn nguồn')
        values={name:segment.restore(translations[name],target) for name,segment in self.segments.items()}
        return ''.join(values[value] if dynamic else value for dynamic,value in self.parts)
