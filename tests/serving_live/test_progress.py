"""Tiến trình BICL gồm dependency, Decision cuối chỉ phản ánh bản được chọn; không gọi model."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from support import ROOT,runtime
from core.serving_runtime.service import Service
from core.serving_live.progress import agent_progress
from core.unified_execution import StageBook


class AgentProgress(unittest.TestCase):
    def setUp(self) -> None:
        self.temp=TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        service=Service(ROOT,state_root=Path(self.temp.name),resources_factory=runtime.FixtureResources)
        identifier=service.create(runtime.spec(['C2']),'fixture','a'*64,background=False)
        self.store=service.store; self.reservation=service.store.reservation(identifier,'a'*64)
        self.book=StageBook(service.store.path(identifier)/'journal',self.reservation['job'])
        self.point=self.reservation['points'][0]['id']

    def complete(self,slot: str) -> None:
        self.book.execute(slot,{},lambda _: {})

    def progress(self) -> dict:
        return agent_progress(self.store,self.reservation)

    def test_bicl_before_selected_decision_and_common_alpha_must_finish_projection(self) -> None:
        self.assertEqual(set(self.progress().values()),{'pending'})
        self.complete('graph/'+self.point+'/full')
        self.assertEqual(self.progress()['alpha'],'running')
        self.complete('shared/'+self.point)
        self.assertEqual(self.progress()['alpha'],'complete')
        self.complete('prepare/forecast/'+self.point+'/r0/original_common')
        self.complete('forecast/'+self.point+'/r0/original_common')
        self.assertEqual(self.progress()['context'],'running')
        self.assertEqual(self.progress()['decision'],'pending')
        self.complete('prepare/forecast/'+self.point+'/r0/C2')
        self.assertEqual(self.progress()['context'],'complete')
        slot='forecast/'+self.point+'/r0/C2'
        def interrupted(_: str) -> dict:
            raise RuntimeError('Mô phỏng chưa có kết quả')
        with self.assertRaises(RuntimeError): self.book.execute(slot,{},interrupted)
        self.assertEqual(self.progress()['decision'],'running')
        self.complete(slot)
        self.assertEqual(self.progress()['decision'],'complete')

    def test_policy_bypass_can_complete_target_without_faking_a_model_call(self) -> None:
        self.complete('shared/'+self.point)
        self.complete('prepare/forecast/'+self.point+'/r0/C2')
        self.complete('forecast/'+self.point+'/r0/C2')
        self.assertEqual(self.progress()['context'],'complete')
        self.assertEqual(self.progress()['decision'],'complete')
