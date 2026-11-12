"""Fixture synthetic cho scheduler/recovery; không dùng như forecast thị trường."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import threading

import pandas as pd

from core.serving_contracts import ServingRequest
from core.serving_runtime.resources import Resources, VERSION, START, END, default_models, decision_config
from core.unified_contracts import SharedSnapshot, digest
from core.unified_methods import MethodAdapters, validate_prepared, resolve

ROOT = Path(__file__).resolve().parents[2]


def spec(variants=None, mode="analyze", symbol="FPT", repeats=1):
    """Spec thật, input model/option tường minh; resource fixture ghi rõ synthetic."""
    return ServingRequest.create({"version": "variant_serving_v1", "mode": mode, "variant_ids": variants or ["original_fix"],
        "symbols": [symbol], "start_date": "2026-07-02", "end_date": "2026-07-02", "timeframe": "1d", "language": "vi",
        "repeats": repeats, "models": default_models()})


def original(decision="LONG"):
    """Đúng schema legacy; không bịa TP/SL hoặc JSON sửa từ response hỏng."""
    return {"decision": decision, "forecast_horizon": "T+2.5", "confidence": "Cao", "risk_reward_ratio": 1.,
            "evidence_for": "Fixture thuận.", "evidence_against": "Fixture nghịch.", "justification": "Chỉ kiểm hợp đồng."}


class Clock:
    """Tiến thời gian có kiểm soát, không ngủ thật để kiểm quota/retry."""
    def __init__(self):
        self.now = 1000000.
        self.lock = threading.Lock()
    def __call__(self):
        return self.now
    def advance(self, seconds=62.):
        with self.lock:
            self.now += seconds


class FixtureResources(Resources):
    """DI chỉ ở tests, API không nhận flag grant hoặc manifest từ người dùng."""
    def __init__(self, root):
        self.root = root
    def document(self):
        return {"version": VERSION, "bindings": {}, "support": {"symbols": ["FPT", "VNM"], "start_date": START, "end_date": END,
            "calendar": ["2026-07-02", "2026-07-03", "2026-07-06", "2026-07-07"], "synthetic_fixture": True},
            "resources": {k: {"version": "synthetic_fixture_v1", "sha256": "5"*64}
                          for k in ("prices", "news", "calendar", "bank", "regime", "facts", "context", "student")}}
    def verify(self):
        pass
    def points(self, request):
        points = super().points(request)
        for point in points:
            point["quality"] = "SYNTHETIC_FIXTURE"
        return points


class Sender:
    """Raw HTTP fixture có thể 429/timeout/hỏng schema, lưu mọi lần gửi để đối soát."""
    def __init__(self, clock, actions=None):
        self.clock = clock
        self.actions = list(actions or [])
        self.bodies = []
        self.closed = 0
        self.on_send = None
    def send(self, body):
        self.bodies.append(deepcopy(body))
        if self.on_send:
            self.on_send()
        self.clock.advance()
        action = self.actions.pop(0) if self.actions else original()
        if isinstance(action, BaseException):
            raise action
        if type(action) is tuple:
            return action
        if 'response_format' in body:
            if 'fact_ids' in body['response_format']['json_schema']['schema']['properties']:
                from core.mt_bicl_decision import OUTPUT_MARKER
                reply = json.loads(body['messages'][0]['content'].split(OUTPUT_MARKER)[-1])
                reply.update(decision='LONG', confidence='Cao')
            else:
                reply = action
            content = json.dumps(reply, ensure_ascii=False)
        else:
            content = '**Mẫu nến chính:** Kiểm thử synthetic.\n**Xu hướng:** Tăng.\n**Hỗ trợ:** 100.\n**Kháng cự:** 110.\n**Tín hiệu:** LONG.\n**Nhận xét:** Chỉ kiểm đường chạy, không dùng nghiên cứu.'
        return 200, json.dumps({'choices': [{'message': {'content': content}}], 'usage': {'total_tokens': 20}}).encode(), {}
    def close(self):
        self.closed += 1


class Provider:
    """Upstream synthetic; Decision native/common dùng adapter thật, không implement thuật toán thứ hai."""
    instances = []
    def __init__(self, root, points, models, variants):
        self.config = decision_config(models)
        self.adapter = MethodAdapters(self.config)
        self.resolve = resolve
        self.shared_count = 0
        self.outcome_count = 0
        self.payload_hashes = []
        self.instances.append(self)
    def validate_point(self, point):
        pass
    def shared(self, book, point, calls):
        self.shared_count += 1
        payload = {"stock_name": point['symbol'], "as_of_date": point['cutoff'], "time_frame": "1d", "language": "vi", "is_backtest": True,
            **{name+'_report': 'Báo cáo synthetic, không gọi thị trường.' for name in ('indicator','pattern','trend','alpha','sentiment')}}
        return SharedSnapshot.create(point,0,payload,{"source_sha256":"1"*64,"upstream_sha256":digest(payload),"price_end":point['cutoff'],"news_dates":[]}).document()
    def prepare(self, variant, snapshot, deps, repeat):
        from core.serving_runtime.providers import NUMERIC_LOCK
        self.payload_hashes.append(snapshot.sha256)
        with NUMERIC_LOCK:
            return self.adapter.prepare(variant,snapshot,deps,repeat)
    def validate(self, variant, snapshot, prepared, repeat):
        from core.serving_runtime.providers import NUMERIC_LOCK
        with NUMERIC_LOCK:
            validate_prepared(variant,snapshot,prepared,self.config,repeat)
    def outcome(self, point):
        from core.unified_experiment import outcome_from_frame
        self.outcome_count += 1
        frame = pd.DataFrame({'Datetime':pd.bdate_range(point['cutoff'],periods=4), 'Open':[100.,100.,100.,100.],
            'High':[101.,102.,103.,111.], 'Low':[99.]*4, 'Close':[100.,101.,102.,110.], 'Volume':[1000.]*4})
        return outcome_from_frame(point,frame,'1'*64)
