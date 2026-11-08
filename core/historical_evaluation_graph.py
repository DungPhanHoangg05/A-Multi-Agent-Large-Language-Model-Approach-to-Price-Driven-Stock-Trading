"""Shared graph/five-factor rows và ảnh có provenance riêng của run lịch sử."""

from __future__ import annotations

import base64
from contextlib import chdir
from copy import deepcopy
from pathlib import Path
import subprocess
from types import ModuleType
from tempfile import TemporaryDirectory
from typing import Any
import math

from agents.alpha_agent import create_alpha_agent
from agents.indicator_agent import create_indicator_agent
from agents.pattern_agent import create_pattern_agent
from agents.trend_agent import create_trend_agent
from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_journal import RunBook
from core.historical_evaluation_protocol import DONOR, digest
from core.prior_context import REPORT_FIELDS
from core.prior_run_lock import safe_path
from utils.graph_util import TechnicalTools


def factor_lines(factors: list[dict[str, Any]]) -> list[str]:
    """Giữ đủ tên/giá trị/signal/mask; không dùng separator Markdown làm mất bảng."""
    if len(factors) != 5 or len({r["id"] for r in factors}) != 5:
        raise ValueError("Alpha phải có đúng5 factor khác nhau")
    result = []
    for factor in factors:
        for key in ("name", "value", "signal"):
            if key not in factor:
                raise ValueError("Factor thiếu tên/giá trị/signal")
        details = factor.get("details", {})
        try:
            numeric = math.isfinite(float(factor["value"]))
        except (TypeError, ValueError):
            numeric = False
        mask = numeric and details.get("is_reliable", factor.get("is_reliable", True))
        result.append(f"F{factor['id']} {factor['name']}={factor['value']}; {factor['signal']}; mask={int(bool(mask))}")
    return result


def require_factors(prompt: str, factors: list[dict[str, Any]]) -> None:
    """Kiểm prompt cuối, không chỉ kiểm raw report trước distill/cap."""
    if any(line not in prompt for line in factor_lines(factors)):
        raise ValueError("Prompt làm mất tên/giá trị/mask của factor")


class GraphProvider:
    """Mỗi node gọi một lần, lưu intent/output; mọi nhánh nhận deepcopy từ cùng seal."""

    def __init__(self, data: HistoricalData, clients: Any, *, fixture: bool = False) -> None:
        """Client factory phải đã vượt release/transport guard trước khi cấp model."""
        self.data, self.clients, self.fixture = data, clients, fixture
        self.cache: dict[str, tuple[str, dict[str, Any]]] = {}
        raw = subprocess.check_output(["git", "show", f"{DONOR}:utils/static_util.py"], cwd=data.root)
        self.renderer_hash = __import__("hashlib").sha256(raw).hexdigest()
        module = ModuleType("historical_chart_convention")
        module.__file__ = str(data.root / "utils/static_util.py")
        exec(compile(raw, module.__file__, "exec"), module.__dict__)
        self.renderer = module
        if fixture:
            # PNG1x1 chỉ phục vụ test orchestrator, không được ghi vào research namespace.
            pixel = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aNf8AAAAASUVORK5CYII="
            module.generate_kline_image = lambda *args, **kwargs: {"pattern_image": pixel}
            module.generate_trend_image = lambda *args, **kwargs: {"trend_image": pixel}
            self.renderer_hash = digest("FIXTURE_ONLY_PIXEL_NOT_A_MARKET_CHART")

    def render(self, name: str, klines: list[dict[str, Any]]) -> dict[str, Any]:
        """Chạy renderer donor tuần tự trong cwd tạm, giữ file phụ khỏi workspace/run."""
        renderer = {"pattern": self.renderer.generate_kline_image, "trend": self.renderer.generate_trend_image}[name]
        # Donor chưa có write_artifacts; giữ bytecode/ảnh và cô lập ba file phụ của nó.
        with TemporaryDirectory(prefix="historical-chart-") as folder, chdir(folder):
            return renderer(deepcopy(klines))

    def shared(self, book: RunBook, symbol: str, cutoff: str, realization: int, org: int) -> dict[str, Any]:
        """Không có nhãn query trong state, ảnh, hash parent hoặc dữ liệu gửi graph."""
        state = self.data.state(symbol, cutoff)
        point = f"{symbol}-{cutoff}/u{realization}"
        from core.historical_signals import snapshot_payload
        prefix_key = digest({"kline": state["kline_data"], "alpha": snapshot_payload(state["point_in_time_df"]),
                             "news": self.data.news.get_sentiment_at(symbol, cutoff)[0], "org": org})
        if point in self.cache:
            if self.cache[point][0] != prefix_key:
                raise ValueError("Shared cache khác nguồn PIT")
            return deepcopy(self.cache[point][1])
        images = {}
        for name in ("pattern", "trend"):
            path = safe_path(book.directory, f"images/{point}/{name}.png")
            if path.exists() and book.path(f"graph/{point}/indicator").exists():
                raw = path.read_bytes()
            elif book.verify_only:
                raise ValueError("Thiếu ảnh PIT đã lưu")
            else:
                result = self.render(name, state["kline_data"])
                raw = base64.b64decode(result[name + "_image"], validate=True)
                if path.exists() and path.read_bytes() != raw:
                    raise ValueError("Ảnh khác renderer/source/runtime đã seal")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            state[name + "_image"] = base64.b64encode(raw).decode()
            images[name] = {"sha256": __import__("hashlib").sha256(raw).hexdigest(),
                            "renderer_sha256": self.renderer_hash, "path": path.relative_to(book.directory).as_posix()}
        from core.historical_signals import snapshot_payload
        source = {"point": point, "kline": state["kline_data"], "images": images,
                  "alpha_prefix": snapshot_payload(state["point_in_time_df"]),
                  "news": self.data.news.get_sentiment_at(symbol, cutoff)[0],
                  "models": self.data.protocol["inference"]["config"], "org": org}
        for name in ("indicator", "pattern", "trend", "full"):
            parent = {"source": source, "reports": {k: state[k] for k in REPORT_FIELDS if k in state}}
            def invoke(attempt_id: str, name: str = name) -> dict[str, Any]:
                """Không tạo client khi chỉ verify slot hoặc dùng complete output."""
                agent, graph = self.clients.models(org)
                nodes = {"indicator": lambda: create_indicator_agent(agent, TechnicalTools()),
                         "pattern": lambda: create_pattern_agent(agent, graph, TechnicalTools()),
                         "trend": lambda: create_trend_agent(agent, graph, TechnicalTools()),
                         "full": lambda: create_alpha_agent(agent, True, True, strict_research_mode=True)}
                return self.clients.stage(name, attempt_id, point, nodes[name](), deepcopy(state))
            from core.historical_evaluation_audit import verify_graph
            slot = f"graph/{point}/{name}"
            output = book.execute(slot, parent, invoke, validate=lambda actual: verify_graph(
                book, name, slot, state, actual, self.data.protocol["inference"]["config"], fixture=self.fixture))
            state.update(output)
        factors = state["sentiment_data"]["alpha_results"]
        rows = factor_lines(factors)
        compact = "Alpha số PIT (5 factor):\n" + "\n".join(rows) + "\nTỔNG HỢP: " + "/".join(r["signal"] for r in factors)
        shared = {"stock_name": symbol, "as_of_date": cutoff, "time_frame": "1d", "language": "vi", "is_backtest": True,
                  **{key: state[key] for key in REPORT_FIELDS}, "alpha_factors": deepcopy(factors),
                  "sentiment_data": deepcopy(state["sentiment_data"]), "images": images, "source_sha256": digest(source)}
        shared["alpha_report"] = compact
        if any(type(shared[k]) is not str or not shared[k].strip() for k in REPORT_FIELDS):
            raise ValueError("Shared graph thiếu báo cáo")
        self.cache[point] = (prefix_key, deepcopy(shared))
        return deepcopy(shared)
