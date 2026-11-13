"""Job live dùng runner/quota/checkpoint chung, dữ liệu đầu vào được khóa theo owner."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from core.serving_contracts import ServingRequest
from core.serving_runtime.resources import Resources
from core.serving_runtime.service import Service
from core.serving_live.snapshots import Snapshots, VERSION
from core.unified_contracts import checksum, digest, json_bytes


@dataclass(frozen=True)
class LiveRequest:
    """Envelope riêng, không nới schema v1 hoặc cho phép live backtest lấy payoff tương lai."""
    _bytes: bytes

    @classmethod
    def create(cls, value: Any) -> LiveRequest:
        """Model/options/IDs tiếp tục qua validator phục vụ as-of đã có."""
        from core.serving_live.timeframes import TIMEFRAMES
        realtime = type(value) is dict and value.get('version') == 'variant_serving_timeframe_v1'
        fields = {'version','snapshot_id','request'} | ({'chart_timeframe'} if realtime else set())
        if (type(value) is not dict or set(value) != fields
                or value['version'] not in ('variant_serving_live_v1','variant_serving_timeframe_v1') or not checksum(value['snapshot_id'])):
            raise ValueError('Envelope live không hợp lệ')
        request = ServingRequest.create(value['request']).document()
        if request['mode'] not in ('analyze','compare') or request['language'] != 'vi':
            raise ValueError('Live hiện hỗ trợ phân tích/so sánh 1d/VI')
        extra = {}
        if realtime:
            if value['chart_timeframe'] not in TIMEFRAMES or request['mode'] != 'analyze':
                raise ValueError('Khung realtime không hợp lệ hoặc không phải phân tích một bản')
            extra['chart_timeframe'] = value['chart_timeframe']
        return cls(json_bytes({**request,'snapshot_id':value['snapshot_id'],'data_source':'live',**extra}))

    def document(self) -> dict:
        """Bản sao JSON gồm nguồn live và hash input trong identity job."""
        return json.loads(self._bytes)

    @property
    def sha256(self) -> str:
        """Cùng form nhưng snapshot khác luôn có identity khác."""
        return digest(self.document())


class LiveResources:
    """Kiểm toàn bộ frozen weights/bank và snapshot mới, không gọi mạng trong preflight/resume."""
    version = VERSION

    def __init__(self, root: Path, snapshots: Snapshots, identifier: str) -> None:
        self.base, self.snapshots, self.identifier = Resources(root), snapshots, identifier
        self.record = snapshots.read(identifier)
        if self.record.get('index_contract') == 'vnindex_close_v1': self.version = VERSION+'/index_close_v1'
        if 'chart_timeframe' in self.record:
            self.version = 'serving_realtime_timeframe_v1/'+self.record['chart_timeframe']
            if self.record.get('index_contract') == 'vnindex_close_v1': self.version += '/index_close_v1'

    def verify(self) -> None:
        """Không cập nhật expected hash để làm job cũ chạy với dữ liệu mới."""
        self.base.verify()
        if self.snapshots.read(self.identifier) != self.record:
            raise ValueError('Snapshot thay đổi sau preflight')

    def document(self) -> dict:
        """Định danh resource live riêng, giữ nguyên file release F08."""
        document = self.base.document()
        record, identifier = self.record, self.identifier
        document['bindings'] = {**document['bindings'],'live_snapshot/'+identifier:{'sha256':identifier}}
        for name in ('prices','news','calendar'):
            document['resources'][name] = {'version':VERSION+'/'+name,'sha256':digest(record[name if name != 'calendar' else 'index'])}
        document['support'] = {'symbols':[record['symbol']], 'calendar':record['index']['Datetime'],
            'start_date':record['cutoff'],'end_date':record['cutoff'],'timeframes':['1d'],'languages':['vi'],
            'snapshot_id':identifier,'source':'LIVE_CAPTURED_DAILY_CLOSED_SESSION',
            'calendar_policy':record['calendar_policy'],'scientific_status':record['scientific_status']}
        if 'chart_timeframe' in record:
            document['support'].update(chart_timeframe=record['chart_timeframe'],chart_sha256=digest(record['chart']),
                source='REALTIME_CHART_WITH_DAILY_CONTEXT',daily_provisional=record['daily_provisional'])
        return document

    def points(self, request: dict) -> list[dict]:
        """Một point phiên mới nhất đã khóa, tuyệt đối không nhận cutoff khác từ browser."""
        record = self.record
        if (request.get('snapshot_id') != self.identifier or request['symbols'] != [record['symbol']]
                or request['start_date'] != record['cutoff'] or request['end_date'] != record['cutoff']
                or request['mode'] not in ('analyze','compare') or request['timeframe'] != '1d'
                or request['language'] != 'vi' or request.get('chart_timeframe') != record.get('chart_timeframe')):
            raise ValueError('Request không khớp snapshot live')
        return [{'id':record['symbol']+'-'+record['cutoff'],'symbol':record['symbol'],'cutoff':record['cutoff'],
                 'fold':'serving_live_daily','quality':'LIVE_VENDOR_SERIES_EXPLORATORY'}]


class LiveService(Service):
    """Namespace store riêng; dùng lại durable runner, UNKNOWN guard và key snapshot."""
    def __init__(self, root: Path, *, snapshots: Snapshots | None = None, state_root: Path | None = None,
                 **kwargs: Any) -> None:
        super().__init__(root, state_root=state_root or root/'outputs/serving_live', **kwargs)
        self.snapshots = snapshots or Snapshots(self.store.root/'snapshots')

    def resources(self, request: dict | None = None) -> LiveResources:
        """Snapshot ID bắt buộc; không đọc globals về mã/ngày đang được chọn trên UI."""
        if request is None: raise ValueError('Thiếu request live')
        return LiveResources(self.root, self.snapshots, request['snapshot_id'])

    def create(self, spec: LiveRequest, key: str, owner: str, *, background: bool = True) -> str:
        """Chặn dùng snapshot của owner khác kể cả gọi Service trực tiếp ngoài Flask."""
        self.snapshots.read(spec.document()['snapshot_id'], owner)
        return super().create(spec, key, owner, background=background)

    def provider(self, reservation: dict) -> Any:
        """Không fetch dữ liệu lần hai; tạo provider từ snapshot đã nằm trong job identity."""
        from core.serving_live.provider import LiveProvider
        request = reservation['job']['identity']['request']
        record = self.snapshots.read(request['snapshot_id'], reservation['job']['owner_scope_sha256'])
        if 'chart_timeframe' in record:
            from core.serving_live.timeframe_provider import TimeframeProvider
            return TimeframeProvider(self.root,reservation['points'],request['models'],request['variant_ids'],record)
        return LiveProvider(self.root,reservation['points'],request['models'],request['variant_ids'],record)

    def result(self, identifier: str, owner: str) -> dict:
        """GET chỉ đọc journal và metadata capture, không làm mới dữ liệu hoặc chạy model."""
        result = super().result(identifier,owner)
        from core.serving_live.progress import agent_progress
        result['agent_progress'] = agent_progress(self.store,self.store.reservation(identifier,owner))
        request = result['identity']['request']
        record = self.snapshots.read(request['snapshot_id'],owner)
        result['live_input'] = self.snapshots.summary(request['snapshot_id'],record)
        if 'chart' in record: result['realtime_chart'] = record['chart']
        return result
