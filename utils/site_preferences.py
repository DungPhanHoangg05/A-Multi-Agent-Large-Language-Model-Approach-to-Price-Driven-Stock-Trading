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
        from utils.i18n import catalogue
        from utils.analysis_ui import messages
        return {'locale_url':locale_url,'display_signal':signal_label,'display_confidence':display_confidence,
            'catalogue_for':catalogue,'analysis_messages_for':messages,
            'display_timeframe':localize_timeframe,'P':{
            'language':lang,'navigation':'Navigation' if en else 'Điều hướng',
            'dark':'Dark mode' if en else 'Chế độ tối','light':'Light mode' if en else 'Chế độ sáng',
            'preparing':'Loading stored reports…' if en else 'Đang mở báo cáo đã lưu…'}}
    @app.after_request
    def remember(response):
        if response.mimetype=='text/html': response.set_cookie('qa_lang',language(),max_age=31536000,samesite='Lax')
        return response
