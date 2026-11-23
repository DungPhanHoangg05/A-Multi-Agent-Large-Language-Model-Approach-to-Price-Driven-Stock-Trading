"""Chiếu tiến trình agent từ journal bền vững; không chạy provider hoặc sửa checkpoint."""
from __future__ import annotations

from typing import Any

from core.unified_execution import StageBook
from core.variant_registry import get_variant


def agent_progress(store: Any, reservation: dict) -> dict[str,str]:
    """Chỉ complete khi slot đã kiểm checksum; file intent hiện hữu là đang thực hiện."""
    job = reservation['job']
    request = job['identity']['request']
    if request['mode'] != 'analyze' or len(reservation['points']) != 1: return {}
    book = StageBook(store.path(job['run_id'])/'journal',job,verify_only=True)
    point = reservation['points'][0]['id']

    def state(slots: list[str]) -> str:
        if all(book.complete(slot) for slot in slots): return 'complete'
        return 'running' if any(book.path(slot).exists() for slot in slots) else 'pending'

    progress = {'loading':state(['render/'+point+'/'+role for role in ('pattern','trend')]),
        **{role:state(['graph/'+point+'/'+node]) for role,node in
           [('indicator','indicator'),('pattern','pattern'),('trend','trend'),('alpha','full')]}}
    # Common/Fact Anchor là tính toán phụ thuộc của BICL, không phải Decision cuối người dùng chọn.
    shared_complete = book.complete('shared/'+point)
    if book.path('graph/'+point+'/full').exists():
        progress['alpha'] = 'complete' if shared_complete else 'running'
    context_variants = [variant for variant in request['variant_ids'] if get_variant(variant).dependencies]
    if context_variants:
        context_slots = ['prepare/forecast/'+point+'/r'+str(repeat)+'/'+variant
            for repeat in range(request['repeats']) for variant in context_variants]
        progress['context'] = state(context_slots)
        if shared_complete and progress['context'] == 'pending': progress['context'] = 'running'
    progress['decision'] = state(['forecast/'+point+'/r'+str(repeat)+'/'+variant
        for repeat in range(request['repeats']) for variant in request['variant_ids']])
    return progress
