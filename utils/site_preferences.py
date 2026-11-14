"""Ngôn ngữ và theme dùng chung mọi trang; query giữ nguyên job/filter khi đổi tiếng."""
from urllib.parse import urlencode
from flask import request
from utils.i18n import signal_label,confidence_label,localize_timeframe


def install(app, language) -> None:
    """Không đổi schema nghiên cứu; chỉ bổ sung context template/cookie của HTML."""
    @app.context_processor
    def context() -> dict:
        lang=language(); en=lang=='en'
        def locale_url(target: str) -> str:
            values=request.args.to_dict(flat=False); values['lang']=[target]
            return request.path+'?'+urlencode(values,doseq=True)
        def display_confidence(value: str,target: str) -> str:
            return confidence_label(value,target) if target=='en' else {'High':'Cao','Medium':'Trung bình','Low':'Thấp'}.get(value,value)
        return {'locale_url':locale_url,'display_signal':signal_label,'display_confidence':display_confidence,
            'display_timeframe':localize_timeframe,'P':{
            'language':lang,'navigation':'Navigation' if en else 'Điều hướng',
            'dark':'Dark mode' if en else 'Chế độ tối','light':'Light mode' if en else 'Chế độ sáng',
            'preparing':'Translating reports with Groq…' if en else 'Đang dịch báo cáo bằng Groq…',
            'locale_failed':'This section could not be translated. The original report is available below; analysis results are unchanged.' if en else 'Chưa dịch được phần này. Có thể xem báo cáo gốc bên dưới; kết quả phân tích giữ nguyên.',
            'source_report':'Original report (source language)' if en else 'Báo cáo gốc (ngôn ngữ nguồn)',
            'quota_wait':'Waiting for Groq quota until' if en else 'Chờ quota Groq đến',
            'locale_unknown':'Translation outcome is unknown. No request has been resent; check the server journal.' if en else 'Attempt dịch chưa rõ kết quả. Không gửi lại; cần đối soát nhật ký server.'}}
    @app.after_request
    def remember(response):
        if response.mimetype=='text/html': response.set_cookie('qa_lang',language(),max_age=31536000,samesite='Lax')
        return response
