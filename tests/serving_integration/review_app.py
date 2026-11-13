"""App review loopback: UI/backend thật, Groq fixture, mọi mutation legacy bị chặn."""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any
from unittest.mock import patch

from fixtures import ROOT, Clock, Sender


def make_app(state_root: Path) -> tuple[Any,Any,str]:
    """Không lấy key thật, không tải vnstock; store review tách khỏi job của người dùng."""
    from flask import jsonify,request
    from itsdangerous import URLSafeTimedSerializer
    from core.serving_runtime.service import Service
    from core.unified_contracts import digest
    from utils import serving_web
    with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
        web = importlib.import_module('web_interface')
    app = web.app; clock = Clock()
    service = Service(ROOT,state_root=state_root,clock=clock,sender_factory=lambda _:Sender(clock))
    app.config.update(SERVING_SERVICE=service,SERVING_API_KEY_PROVIDER=lambda:'fixture-review-key',
                      SERVING_LEGACY_ROOT=state_root,TESTING=False)
    owner_id = 'f11-loopback-review-owner'
    cookie = URLSafeTimedSerializer(service.quota.secret(),salt='serving-owner-v1').dumps(owner_id)

    @app.before_request
    def fixture_boundary() -> Any:
        """Chỉ API serving/research đọc; legacy không được chạy hoặc thay key/model thật."""
        if request.path == '/api/groq-status':
            return jsonify({'valid':True,'fixture':True,'message':'HTTP fixture; không kết nối Groq'})
        if request.path == '/api/assets': return jsonify({'assets':[],'total':0,'fixture':True})
        if request.path.startswith('/api/') and not request.path.startswith(('/api/serving/v1/','/api/research-results/','/api/experiments/')):
            return jsonify({'error':'Preview fixture chặn API legacy/thị trường/cấu hình','fixture':True}),409
        return None

    @app.after_request
    def fixture_notice(response: Any) -> Any:
        """Cookie review riêng và banner cố định để không nhầm HTTP fixture thành mô hình thật."""
        response.set_cookie(serving_web.COOKIE,cookie,httponly=True,samesite='Strict')
        response.headers['X-Serving-Review'] = 'F11_HTTP_FIXTURE_ONLY_NO_HOSTED_CALLS'
        if response.mimetype == 'text/html':
            raw = response.get_data(as_text=True).replace('<title>','<title>FIXTURE · ',1)
            notice = '<aside style="margin:1rem;padding:.8rem;background:#fff1dc;color:#293344;overflow-wrap:anywhere">F11 REVIEW · HTTP FIXTURE · Dữ liệu historical frozen, không gọi Groq/thị trường thật. Không dùng để ra quyết định giao dịch.</aside>'
            response.set_data(raw.replace('</body>',notice+'</body>',1))
        return response
    return app,service,digest(owner_id)
