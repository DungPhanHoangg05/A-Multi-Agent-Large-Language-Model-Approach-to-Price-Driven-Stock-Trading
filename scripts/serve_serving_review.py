"""Mở preview F11 tại loopback với HTTP fixture, không key thật hoặc inference hosted."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import threading
from unittest.mock import patch
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(ROOT/'tests/serving_integration')]


def main() -> None:
    """Không bind mạng ngoài, không reloader và không ghi vào namespace job production."""
    parser = argparse.ArgumentParser(description='Preview F11 bằng HTTP fixture, không API thật')
    parser.add_argument('--port',type=int,default=5051)
    parser.add_argument('--seed',action='store_true',help='Chuẩn bị một backtest MWG/sáu bản với HTTP fixture')
    parser.add_argument('--duration',type=int,default=900,help='Tự dừng preview sau số giây này')
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535: raise ValueError('Port preview ngoài giới hạn')
    if not 30 <= args.duration <= 3600: raise ValueError('Thời lượng preview cần từ 30 đến 3600 giây')
    from review_app import make_app
    from fixtures import spec
    from core.serving_registry import MAIN_IDS
    from utils import serving_web
    # Cookie khác production; chuyển port không được làm mất owner cookie job thật.
    with patch.object(serving_web,'COOKIE','qa_serving_review_owner'):
        state = ROOT/'tmp/serving_review'/str(uuid4()); app,service,owner = make_app(state)
        if args.seed:
            request = spec(list(MAIN_IDS),'backtest',symbol='MWG')
            identifier = service.create(request,'fixture-review-key',owner,background=False)
            service.work(identifier,'fixture-review-key',owner,wait=False)
            result = service.result(identifier,owner)
            if result['state'] != 'completed': raise ValueError('Seed fixture chưa hoàn tất')
            print(f'Backtest fixture: http://127.0.0.1:{args.port}/backtest?run_id={identifier}',flush=True)
        print(f'Preview chỉ loopback: http://127.0.0.1:{args.port}/demo?lang=vi',flush=True)
        print(f'Không gọi Groq/thị trường thật; tự dừng sau {args.duration} giây hoặc Ctrl+C.',flush=True)
        from werkzeug.serving import make_server
        server = make_server('127.0.0.1',args.port,app,threaded=True)
        timer = threading.Timer(args.duration,server.shutdown); timer.daemon = True; timer.start()
        try: server.serve_forever()
        finally: timer.cancel(); server.server_close()


if __name__ == '__main__': main()
