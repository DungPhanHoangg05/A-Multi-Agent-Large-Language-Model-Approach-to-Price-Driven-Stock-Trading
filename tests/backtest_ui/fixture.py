"""Sinh fixture DOM từ runner/evaluator thật với dữ liệu và HTTP tổng hợp."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json

from fixtures import ROOT, Clock, Provider, Sender, Resources, spec, original, prices
from core.serving_registry import registry_document
from core.serving_runtime.service import Service
from utils.backtest_ui import messages


def fixture() -> dict:
    """Không tiêu thụ API key thật, không dùng dữ liệu tổng hợp làm kết quả khoa học."""
    clock = Clock(); sender = Sender(clock,[original('LONG'),original('SHORT')]*4)
    with TemporaryDirectory() as folder:
        service = Service(ROOT,state_root=Path(folder),clock=clock,sender_factory=lambda _:sender,resources_factory=Resources,provider_factory=Provider)
        identifier = service.create(spec(),'fixture-key','7'*64,background=False)
        service.work(identifier,'fixture-key','7'*64,wait=False)
        with patch('core.serving_runtime.evaluation.prices',side_effect=prices):
            data = service.evaluation(identifier,'7'*64,{})
        from utils.research_i18n import messages as research_messages
        return {'config':{'messages':messages('vi'),'researchMessages':research_messages('vi'),'language':'vi','registry':registry_document(),'runId':identifier},'data':data}


if __name__ == '__main__': print(json.dumps(fixture(),ensure_ascii=False,allow_nan=False))
