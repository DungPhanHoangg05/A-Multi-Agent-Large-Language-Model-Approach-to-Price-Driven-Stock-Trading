"""API bản dịch trình bày tách khỏi inference; không sửa JSON nguồn hoặc gọi model qua GET."""
from functools import lru_cache
from flask import Blueprint,Response,current_app,request

from core.serving_locales import LocaleService
from utils.serving_web import ROOT,owner,mutation_allowed,respond,key_snapshot,service as serving_service

locales=Blueprint('display_locales',__name__,url_prefix='/api/display-locales')


@lru_cache(maxsize=1)
def default_service() -> LocaleService:
    """Cùng pool TPM/RPM với analysis/backtest, kho riêng không nằm trong scientific artifacts."""
    return LocaleService(ROOT/'outputs/display_locales/v1',serving_service().quota)


def service() -> LocaleService:
    """Chỉ tests/operator được inject service; browser không chọn model/path."""
    return current_app.config.get('DISPLAY_LOCALE_SERVICE') or default_service()


@locales.post('')
def create() -> Response:
    """Chọn ngôn ngữ là thao tác dịch rõ ràng; không nhận key/model hoặc filesystem path trong body."""
    if not mutation_allowed(): return respond({'error':'INVALID_ORIGIN'},status=400)
    try:
        body=request.get_json()
        if type(body) is not dict or set(body)!={'texts','target'}: raise ValueError('Body không hợp lệ')
        scope,cookie=owner(True)
        result=service().start(body['texts'],body['target'],scope,key_snapshot())
        return respond(result,cookie,200 if result['state']=='completed' else 202)
    except (ValueError,TypeError,KeyError): return respond({'error':'LOCALIZATION_UNAVAILABLE'},status=409)


@locales.get('/<identifier>')
def result(identifier: str) -> Response:
    """Đọc trạng thái và bản dịch đúng owner; tuyệt đối không khởi động worker."""
    try:
        scope,_=owner()
        if scope is None: raise PermissionError('Thiếu owner')
        return respond(service().result(identifier,scope))
    except (ValueError,PermissionError,FileNotFoundError,KeyError): return respond({'error':'NOT_FOUND'},status=404)
