"""Xuất cùng projection đã đánh giá, giữ NA và chặn công thức CSV."""
from __future__ import annotations

import csv
import io
from typing import Any

from core.unified_contracts import json_bytes
from utils.research_view import csv_cell


def export_bytes(result: dict[str, Any], format_name: str, table: str) -> tuple[bytes, str]:
    """CSV/JSON không tự tính lại metric hoặc ghép nhiều run thành paired contrast."""
    from core.serving_runtime.evaluation import TABLES
    if table not in TABLES: raise ValueError('Bảng export chưa hỗ trợ')
    if format_name == 'json': return json_bytes(result),'application/json'
    if format_name != 'csv': raise ValueError('Chỉ xuất json/csv')
    rows = result.get(table,[])
    meta = {'run_id':result['run_id'],'kind':result['kind'],'status':result['status'],
        'evaluation_status':result['evaluation_status'],'metric_scope':result['metric_scope'],
        'units_json':result['units'],'filters_json':result.get('filters',{}),'provenance_json':result['provenance']}
    columns = list(dict.fromkeys(key for row in rows for key in row)) + [k for k in meta if not any(k in row for row in rows)]
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output,columns,lineterminator='\n'); writer.writeheader()
    for row in rows: writer.writerow({k:csv_cell(v) for k,v in {**row,**meta}.items()})
    return output.getvalue().encode('utf-8-sig'),'text/csv; charset=utf-8'
