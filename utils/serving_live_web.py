"""API phân tích mới nhất qua snapshot riêng; không mở đường live backtest hoặc đổi key trên GET."""
from __future__ import annotations

from functools import lru_cache

from flask import Blueprint, Response, current_app, request
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from core.serving_contracts import ContractError
from core.serving_live.service import LiveRequest, LiveService
from core.serving_live.errors import CaptureError
from utils.serving_web import ROOT, key_snapshot, mutation_allowed, owner, respond

live = Blueprint('serving_live',__name__,url_prefix='/api/serving/live/v1')


@lru_cache(maxsize=1)
def default_service() -> LiveService:
    """Khởi tạo store private, không fetch giá/tin hoặc tạo model cho đến thao tác người dùng."""
    from utils.serving_web import service as asof_service
    backend = LiveService(ROOT)
    # Hai namespace job vẫn dùng chung ledger admission để không nhân đôi TPM/RPM.
    backend.quota = asof_service().quota
    return backend


def service() -> LiveService:
    """Fixture/operator tiêm service riêng; browser không được chọn backend hoặc đường dẫn."""
    return current_app.config.get('SERVING_LIVE_SERVICE') or default_service()


@live.post('/snapshot')
def capture() -> Response:
    """Một thao tác rõ ràng lấy phiên mới nhất rồi trả SHA/ngày cho bước kiểm khả dụng."""
    if not mutation_allowed(): return respond({'error':'Cần JSON cùng origin'},status=400)
    try:
        body = request.get_json()
        if type(body) is not dict or set(body) not in ({'symbol'},{'symbol','timeframe'}): raise ValueError('Body snapshot không hợp lệ')
        scope,cookie = owner(True)
        data = (service().snapshots.capture_timeframe(body['symbol'],body['timeframe'],scope)
                if 'timeframe' in body else service().snapshots.capture(body['symbol'],scope))
        return respond(data,cookie)
    except CaptureError as error:
        current_app.logger.warning('Capture thất bại: code=%s; giai đoạn=%s',error.code,error.stage)
        return respond({'error':str(error),'capture_error':error.document()},status=409)
    except (ValueError,OSError,KeyError,BadRequest,UnsupportedMediaType):
        error = CaptureError('snapshot.validate')
        current_app.logger.warning('Capture thất bại: code=%s; giai đoạn=%s',error.code,error.stage)
        return respond({'error':str(error),'capture_error':error.document()},status=409)
    except Exception:
        return respond({'error':'Nguồn dữ liệu mới nhất tạm không khả dụng; chưa gọi LLM'},status=503)


def checked() -> tuple[LiveRequest,str,str | None]:
    """Kiểm request/owner trước mọi preflight/provider/dispatch."""
    if not mutation_allowed(): raise ValueError('Cần JSON cùng origin')
    spec = LiveRequest.create(request.get_json())
    scope,cookie = owner(True)
    service().snapshots.read(spec.document()['snapshot_id'],scope)
    return spec,scope,cookie


@live.post('/preflight')
@live.post('/jobs')
def start() -> Response:
    """Preflight không tải lại snapshot; start dùng đúng mã/ngày/models/hash đã kiểm."""
    try:
        spec,scope,cookie = checked()
        backend = service(); key = key_snapshot()
        check = backend.preflight(spec,key)
        if request.path.endswith('/preflight'): return respond(check,cookie)
        if not check['run_enabled']: return respond(check,cookie,409)
        identifier = backend.create(spec,key,scope)
        return respond({'run_id':identifier,'status':'queued','source':'live'},cookie,202)
    except (PermissionError,FileNotFoundError):
        return respond({'error':'Không có snapshot thuộc owner này'},status=404)
    except (ValueError,ContractError,KeyError,BadRequest,UnsupportedMediaType):
        return respond({'error':'Request hoặc snapshot live không hợp lệ'},status=400)


@live.get('/jobs/<identifier>')
@live.get('/jobs/<identifier>/export')
def result(identifier: str) -> Response:
    """GET đọc journal; export giữ nguyên nguồn live, không tạo backtest metrics."""
    try:
        scope,_ = owner()
        if scope is None: raise PermissionError('Thiếu owner')
        response = respond(service().result(identifier,scope))
        if request.path.endswith('/export'):
            response.headers['Content-Disposition'] = f'attachment; filename="{identifier}-live.json"'
            response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    except (PermissionError,FileNotFoundError,ValueError,KeyError):
        return respond({'error':'Không có job live thuộc owner này'},status=404)


@live.post('/jobs/<identifier>/<action>')
def control(identifier: str, action: str) -> Response:
    """Stop/resume cùng UUID/input; đổi key hoặc dữ liệu không âm thầm tạo job mới."""
    if not mutation_allowed() or action not in ('stop','resume'):
        return respond({'error':'Thao tác không hợp lệ'},status=400)
    try:
        if request.get_json() != {}: raise ValueError('Body phải rỗng')
        scope,_ = owner()
        if scope is None: raise PermissionError('Thiếu owner')
        backend = service(); backend.store.reservation(identifier,scope)
        if action == 'stop': backend.store.control(identifier,True)
        else: backend.start(identifier,key_snapshot(),scope)
        return respond({'run_id':identifier,'action':action},status=202)
    except (PermissionError,FileNotFoundError):
        return respond({'error':'Không có job live thuộc owner này'},status=404)
    except (ValueError,KeyError,BadRequest):
        return respond({'error':'Không resume được job live với identity/credential hiện tại'},status=409)
