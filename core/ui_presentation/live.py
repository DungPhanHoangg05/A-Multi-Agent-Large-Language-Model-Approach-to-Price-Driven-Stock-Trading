"""Hooks trình bày live; forecast canonical đi qua adapter cũ, wire có version riêng."""
from typing import Any
from core.serving_runtime.providers import VisionProxy
from core.ui_presentation.capture import CURRENT
from core.ui_presentation.wire import report_body,report_reply,decision_body,decision_reply


class BilingualVision(VisionProxy):
    """Một Calls/attempt thật; cặp EN được giữ trong sidecar của cùng checkpoint."""
    def __init__(self,calls: Any,slot: str,attempt: str,model: dict,role: str) -> None:
        class PairedCalls:
            """Không tạo sender/client hay reserve riêng cho bản tiếng Anh."""
            def call(self,slot: str,body: dict,attempt: str) -> tuple[Any,dict]:
                """Dùng đúng slot/attempt để giữ retry và raw checkpoint hiện hữu."""
                value,row=calls.call(slot,report_body(body),attempt)
                pair=report_reply(value)
                CURRENT.get()[role]=pair
                return pair['vi'],row
        super().__init__(PairedCalls(),slot,attempt,model)


class LivePresentation:
    """Mixin chỉ dùng ở provider live mới; as-of/research giữ wire cũ."""
    presentation_enabled=True
    def vision_proxy(self,role: str,calls: Any,slot: str,attempt: str,model: dict) -> BilingualVision:
        """Chỉ lớp live này mở hợp đồng phản hồi có hai ngôn ngữ."""
        return BilingualVision(calls,slot,attempt,model,role)
    def wire_body(self,request: dict) -> dict:
        """Tạo wire có bản EN từ bản sao request canonical."""
        from core.unified_execution_transport import body_for
        return decision_body(body_for(request))
    def canonical_reply(self,value: dict) -> dict:
        """Chỉ trả trường canonical cho policy cũ."""
        return decision_reply(value)[0]
    def presentation_reply(self,value: dict) -> dict:
        """Trả bản EN cho sidecar sau khi kiểm cùng dữ kiện."""
        return decision_reply(value)[1]
