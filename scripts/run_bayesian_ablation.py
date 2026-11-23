"""Tạo đồ thị dùng chung cho đường backtest ghép cặp."""
from __future__ import annotations

from typing import Any

import httpx
from langchain_groq import ChatGroq

from utils.graph_setup import SetGraph
from utils.graph_util import TechnicalTools


def make_builder(plan: dict[str, Any], key: str, client: httpx.Client) -> SetGraph:
    """Dùng client ChatGroq thật; transport chung bắt cả structured và fallback."""
    models = plan["signal_config"]["models"]
    def model(role: str) -> ChatGroq:
        llm = ChatGroq(model=models[f"{role}_llm_model"], temperature=models[f"{role}_llm_temperature"],
            max_tokens=models[f"{role}_llm_max_tokens"], api_key=key, max_retries=0,
            http_client=client, **plan["client_options"][role])
        # LangChain tự đổi 0 thành 1e-8 trong constructor; khôi phục đúng giá trị
        # đã khóa trước mọi request và trước validator nghiên cứu.
        llm.temperature = models[f"{role}_llm_temperature"]
        return llm
    return SetGraph(model("agent"), model("graph"), TechnicalTools())
