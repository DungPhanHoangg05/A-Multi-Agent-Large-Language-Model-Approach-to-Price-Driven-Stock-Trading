"""Chiếu tiến trình agent từ journal bền vững; không chạy provider hoặc sửa checkpoint."""
from __future__ import annotations

from typing import Any

from core.unified_execution import StageBook


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
    progress['context'] = state(['prepare/forecast/'+point+'/r0/'+variant for variant in request['variant_ids']])
    progress['decision'] = state(['forecast/'+point+'/r'+str(repeat)+'/'+variant
        for repeat in range(request['repeats']) for variant in job['execution_plan']])
    return progress
