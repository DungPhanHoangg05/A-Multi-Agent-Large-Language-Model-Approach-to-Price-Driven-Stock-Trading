"""HTTP loopback và spy provider thật cho nghiệm thu, không gọi Groq/thị trường."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from http.cookiejar import CookieJar
import json
from pathlib import Path
import sys
import threading
from typing import Any
from urllib.error import HTTPError
from urllib.request import build_opener, HTTPCookieProcessor, Request

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT),str(ROOT/'tests/serving_runtime')]
from support import Clock, Sender, Provider, FixtureResources, spec, original
from core.serving_runtime.providers import AsOfProvider
from core.unified_contracts import digest


class Client:
    """CookieJar riêng cho mỗi owner, HTTP thật chỉ đến cổng loopback của test."""
    def __init__(self, base: str) -> None:
        self.base = base; self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
    def call(self, path: str, body: dict | None = None, *, origin: str | None = None) -> tuple[int,dict,bytes,dict]:
        headers = {'Content-Type':'application/json'} if body is not None else {}
        if origin is not None: headers['Origin'] = origin
        request = Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        try: response = self.opener.open(request,timeout=60)
        except HTTPError as error: response = error
        with response:
            raw = response.read(); content_type = response.headers.get('Content-Type','')
            value = json.loads(raw) if 'application/json' in content_type else {}
            return response.status,value,raw,dict(response.headers)


class TracedProvider(AsOfProvider):
    """Chạy nguyên provider; spy kiểm một snapshot, dependency và cap ở ranh giới prepare."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args,**kwargs)
        self.prepares: Counter = Counter(); self.shared_count = 0; self.outcomes_count = 0
        self.parents: set[str] = set(); self.prefix_lengths: list[int] = []; self.prompt_lengths: list[int] = []
    def shared(self, *args: Any) -> dict:
        self.shared_count += 1
        return super().shared(*args)
    def prepare(self, variant: str, snapshot: Any, dependencies: dict, repeat: int) -> dict:
        before = snapshot.document(); parent = digest(before)
        self.parents.add(parent); self.prepares[(before['point']['id'],repeat,variant)] += 1
        prepared = super().prepare(variant,snapshot,dependencies,repeat)
        if snapshot.document() != before: raise AssertionError('Adapter đã sửa snapshot dùng chung')
        if prepared['request'] is not None:
            self.prompt_lengths.append(len(prepared['request']['messages'][0]['content']))
        prefix = prepared['trace'].get('request',{}).get('prefix','')
        if variant == 'bayesian_v1' and not prepared['trace']['fallback']:
            from core.bayesian_retriever import format_compact_prior_prefix
            retrieval = prepared['trace']['retrieval']; prefix = format_compact_prior_prefix(retrieval['tasks'],retrieval['stats'])
        if variant in ('bayesian_v1','C2','A_tp_pool','B_semantic'):
            self.prefix_lengths.append(len(prefix))
        return prepared
    def outcome(self, point: dict) -> dict:
        self.outcomes_count += 1
        return super().outcome(point)
