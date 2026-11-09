"""Nghiệm thu H07 và phân tích H08 offline; chặn mọi kết nối mạng."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def main() -> None:
    """Không gọi collector; verify tái dựng độc lập ở thư mục tạm và so artifact byte."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=('run','verify','accept'))
    args=parser.parse_args()
    import torch
    from threadpoolctl import threadpool_limits
    from core.free_pilot_analysis import accept,run_analysis,ANALYSIS,SOURCES,runtime_versions
    from core.free_pilot_assets import DIRECTORY
    from core.historical_evaluation_journal import load
    from core.historical_evaluation_protocol import binding
    from core.prior_run_lock import PriorRunLock
    torch.set_num_threads(1)
    with patch('socket.socket.connect',side_effect=AssertionError('H08 offline không được gọi mạng')), threadpool_limits(limits=1), \
            PriorRunLock(ROOT/DIRECTORY,'free_pilot48_exclusive_v1'):
        if args.stage=='accept':
            receipt,_,_=accept(ROOT)
            print(json.dumps({k:v for k,v in receipt.items() if k not in ('identity',)},ensure_ascii=False))
        elif args.stage=='run':
            receipt=run_analysis(ROOT)
            print(json.dumps({'status':receipt['status'],'api_calls':0,'output':'outputs/historical_reevaluation/free_pilot_r1/analysis/report.md'}))
        else:
            receipt=load(ROOT/ANALYSIS)
            if receipt['runtime']!=runtime_versions(): raise ValueError('Runtime consumer H08 đổi')
            if receipt['sources']!={name:binding(ROOT,name) for name in SOURCES}: raise ValueError('Source H08 đổi')
            # Thư mục tạm đặt trong workspace để binding luôn có đường dẫn tương đối hợp lệ.
            with TemporaryDirectory(prefix='h08-recheck-',dir=ROOT/DIRECTORY) as folder:
                rebuilt=run_analysis(ROOT,Path(folder))
                if set(rebuilt['artifacts'])!=set(receipt['artifacts']): raise ValueError('Artifacs H08 thiếu/thừa')
                for name,record in receipt['artifacts'].items():
                    expected=hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()
                    actual=hashlib.sha256((Path(folder)/name).read_bytes()).hexdigest()
                    if expected!=record['sha256'] or actual!=expected: raise ValueError('H08 cold khác byte: '+name)
            print('H08_COLD_VERIFY_PASS; API=0; không đổi evidence H07.')


if __name__=='__main__': main()
