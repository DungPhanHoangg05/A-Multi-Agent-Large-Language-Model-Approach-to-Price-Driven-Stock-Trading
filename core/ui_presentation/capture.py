"""Context riêng từng phân tích và proxy cho graph Original; một invoke sinh cả VI/EN."""
from __future__ import annotations
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from typing import Any,Iterator
from langchain_core.messages import AIMessage,HumanMessage
from core.ui_presentation.wire import DIRECTIVE,report_reply,decision_body,decision_reply

CURRENT=ContextVar('ui_bilingual_capture',default=None)


@contextmanager
def capture() -> Iterator[dict[str,Any]]:
    """Không chia sẻ báo cáo giữa thread/job và luôn khôi phục context sau lỗi."""
    reports={}; token=CURRENT.set(reports)
    try: yield reports
    finally: CURRENT.reset(token)


class ReportClient:
    """Delegate nguyên trạng ngoài profile UI; không tạo SDK client hoặc gọi thêm model."""
    def __init__(self,client: Any,role: str) -> None: self.client,self.role=client,role
    def __getattr__(self,name: str) -> Any: return getattr(self.client,name)
    def invoke(self,messages: Any,**kwargs: Any) -> Any:
        """Một phản hồi có cả hai bản; không thay invocation khi context UI tắt."""
        reports=CURRENT.get()
        if reports is None: return self.client.invoke(messages,**kwargs)
        prompt=deepcopy(messages)
        for message in prompt:
            if message.type=='system': message.content+='\n'+DIRECTIVE; break
        client=self.client
        model=str(getattr(client,'model_name','')).lower()
        if 'qwen' in model: client=client.bind(reasoning_effort='none')
        elif 'gpt-oss' in model: client=client.bind(reasoning_effort='low')
        response=client.invoke([*prompt,HumanMessage(content=DIRECTIVE)],**kwargs)
        pair=report_reply(response.content); reports[self.role]=pair
        return AIMessage(content=pair['vi'])


class DecisionClient:
    """Chỉ thay wire trong lượt UI, giữ schema/parse nguyên cho backtest và các caller cũ."""
    def __init__(self,client: Any) -> None: self.client=client
    def __getattr__(self,name: str) -> Any: return getattr(self.client,name)
    def with_structured_output(self,schema: Any,**options: Any) -> Any:
        """Giữ parser canonical riêng với hợp đồng wire song ngữ của UI."""
        normal=self.client.with_structured_output(schema,**options)
        raw_schema=schema.model_json_schema() if hasattr(schema,'model_json_schema') else deepcopy(schema)
        parent=self
        class Structured:
            """Một invocation thực, trả canonical cho parser cũ và lưu display trong context."""
            def invoke(self,prompt: str,**kwargs: Any) -> dict:
                reports=CURRENT.get()
                if reports is None: return normal.invoke(prompt,**kwargs)
                modified=decision_body({'messages':[],'response_format':{'json_schema':{'schema':deepcopy(raw_schema)}}})['response_format']['json_schema']['schema']
                bilingual=parent.client.with_structured_output(modified,**options)
                directive=decision_body({'messages':[],'response_format':{'json_schema':{'schema':deepcopy(raw_schema)}}})['messages'][0]['content']
                result=bilingual.invoke(prompt+'\n'+directive,**kwargs)
                parsed=result['parsed']; parsed=parsed.model_dump() if hasattr(parsed,'model_dump') else parsed
                canonical,english=decision_reply(parsed); reports['decision']={'vi':canonical,'en':english}
                return {**result,'parsed':canonical}
        return Structured()
