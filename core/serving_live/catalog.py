"""Quy tắc và bộ chuyển giao Alpha cho mã ngoài mẫu nghiên cứu."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from statistics import median

import numpy as np
import pandas as pd

from core.realtime_loader import _STOCK_CODE_RE
from core.unified_contracts import digest

CATALOG = 'LIVE_CATALOG_EXPLORATORY'
ORIGIN = '2018-01-02'
MIN_BARS = 45


def stock_symbol(value: object) -> bool:
    """Giữ đúng định dạng của danh mục live, không dùng mã làm đường dẫn."""
    return isinstance(value, str) and _STOCK_CODE_RE.fullmatch(value) is not None


class CatalogAlpha:
    """Dùng tập factor và hướng phổ biến trong selector đã khóa, không fit bằng giá query."""

    def __init__(self, selectors: dict[str, dict]) -> None:
        self.payloads = {name: item['payload'] for name, item in sorted(selectors.items())}
        if not self.payloads or any(digest(item['payload']) != item['sha256'] for item in selectors.values()):
            raise ValueError('Không xác minh được selector nguồn cho Alpha live')
        votes = Counter((row['alpha_id'], row['orientation'])
                        for payload in self.payloads.values() for row in payload['selected'])
        candidates = {name for name, _ in votes}
        selected = sorted(candidates, key=lambda name: (-(votes[name, 1] + votes[name, -1]), name))[:5]
        if len(selected) != 5:
            raise ValueError('Thiếu factor nguồn cho Alpha live')
        self.selected = {name: 1 if votes[name, 1] >= votes[name, -1] else -1 for name in selected}
        self.threshold = float(median(payload['threshold'] for payload in self.payloads.values()))
        self.sha256 = digest({'version': CATALOG + '/alpha_transfer_v1',
                              'sources': {name: selectors[name]['sha256'] for name in self.payloads},
                              'selected': self.selected, 'threshold': self.threshold})
        self._cached: tuple[str, dict | None] | None = None

    def predict(self, prefix: pd.DataFrame, cutoff: str) -> dict | None:
        """Chỉ dùng giá tại/bên trước cutoff; giữ thiếu Alpha nếu không đủ nến hoặc factor."""
        from core.causal_alpha import PROFILE, alpha_values, frame_document

        if str(prefix.Datetime.iloc[-1].date()) != cutoff or any(
                payload['fit_end'] >= cutoff for payload in self.payloads.values()):
            raise ValueError('Nguồn Alpha không nằm trước cutoff live')
        if len(prefix) < 600:
            return None
        history = digest(frame_document(prefix))
        if self._cached is None or self._cached[0] != history:
            values = alpha_values(prefix)
            rows = []
            for name, orientation in self.selected.items():
                value = float(values[name].iloc[-1] * orientation)
                if not np.isfinite(value):
                    self._cached = (history, None)
                    return None
                signal = 'TĂNG' if value > self.threshold else 'GIẢM' if value < -self.threshold else 'TRUNG TÍNH'
                rows.append({'alpha_id': name, 'value': value, 'signal': signal, 'available': True, 'orientation': orientation})
            report = 'Alpha live dùng bộ factor chuyển giao từ các selector đã khóa.\n' + '\n'.join(
                f"{row['alpha_id']}: {row['value']:+.6f}, {row['signal']}" for row in rows)
            result = {'version': PROFILE, 'cutoff': cutoff, 'selector_sha256': self.sha256, 'history_sha256': history,
                      'factors': rows, 'report': report, 'scope': CATALOG + '/alpha_transfer_v1'}
            self._cached = (history, {**result, 'projection_sha256': digest(result)})
        return deepcopy(self._cached[1])


class CatalogPrior:
    """Tái dùng prior gốc, giữ fallback cùng mã cả khi Alpha chưa đủ dữ liệu."""

    def __init__(self, prior: object) -> None:
        self.prior = prior

    def request(self, branch: str, shared: dict, regime: str) -> tuple[dict, dict]:
        """Không tạo phiếu Alpha hoặc dùng chu kỳ của mã khác thay kho cùng mã."""
        if shared['alpha_factors']:
            return self.prior.request(branch, shared, regime)
        from core.finalize_prior import VARIANTS, statistics
        from core.mt_bicl_prompt import canonical_request

        symbol, cutoff = shared['stock_name'], shared['as_of_date']
        point = self.prior.points[symbol+'-'+cutoff]
        if (branch not in VARIANTS or point['quality'] != CATALOG or point['regime'] != regime
                or any(row['symbol'] == symbol for row in self.prior.rows)):
            raise ValueError('Fallback danh mục không khớp nguồn cùng mã')
        return canonical_request(shared, '', self.prior.decision), {
            'branch': branch, 'fallback': True, 'reason': 'NO_SAME_SYMBOL_FROZEN_BANK_OOD',
            'bank_sha256': self.prior.bank_sha256, 'query_key': deepcopy(point['retrieval_key']),
            'eligible_count': 0, 'population_ids': [], 'selected_ids': [], 'counts': statistics([]),
            'request': {'prefix': ''}}
