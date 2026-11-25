"""Chạy lại mẫu, ảnh và mẫu prompt đã lưu của nghiên cứu thành phần."""
from __future__ import annotations

from collections import Counter, defaultdict
from contextlib import redirect_stdout
from copy import deepcopy
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
from typing import Any

from agents.decision_agent import TradeDecisionOutput, _distill_report
from agents.pattern_agent import create_pattern_agent
from agents.trend_agent import create_trend_agent
from core.evaluation_transport import DECISION, VISION
from core.historical_signals import snapshot_payload
from core.research_invocation import ENABLED, invocation_scope
from core.serving_runtime.providers import VisionProxy
from core.unified_contracts import digest
from core.unified_protocol import DONOR, git_blob
from utils.graph_util import TechnicalTools

MANIFEST = "outputs/revision/revision_minimal_v1/manifest.json"
NUMERIC = "outputs/revision/r1_72h_bank_v2/numeric/predictions.csv"
HEADINGS = ("### [1] PHÂN TÍCH XU HƯỚNG", "### [2] MÔ HÌNH NẾN", "### [3] CHỈ BÁO KỸ THUẬT")
ARCHIVED_LIMITS = {"trend": 900, "pattern": 900}
MODELS = (("pattern", create_pattern_agent), ("trend", create_trend_agent))


def archive(root: Path, path: str) -> dict:
    """Đọc hiện vật theo commit đã khóa."""
    return json.loads(git_blob(root, DONOR, path))


def decision_prompt(template: str, reports: dict[str, str]) -> str:
    """Chỉ thay hai báo cáo động, giữ nguyên Alpha, sentiment và nhánh placebo."""
    ranges = [template.index(heading + "\n") for heading in HEADINGS]
    if ranges != sorted(ranges):
        raise ValueError("Thứ tự báo cáo khác mẫu thành phần")
    prefix = template[:ranges[0]]
    for heading, role in zip(HEADINGS, ("trend", "pattern")):
        prefix += heading + "\n" + _distill_report(role, reports[role], report_limits=ARCHIVED_LIMITS) + "\n\n"
    return prefix + template[ranges[2]:]


def wire_body(metadata: dict, messages: list[dict], options: dict) -> dict:
    """Giữ model, trần output, nhiệt độ và response format từ lần thu thành phần."""
    return {"model": metadata["ls_model_name"], "temperature": metadata["ls_temperature"],
            "max_tokens": metadata["ls_max_tokens"], "stream": False, "n": 1,
            **deepcopy(options), "messages": messages}


class ArchivedVision:
    """Dùng byte ảnh và hai message đã lưu cho lần phân tích đầu của node."""

    def __init__(self, calls: Any, slot: str, attempt: str, body: dict) -> None:
        self.calls, self.slot, self.attempt, self.body = calls, slot, attempt, body
        self.index = 0

    def invoke(self, messages: Any) -> Any:
        """Giữ lần sửa định dạng do node yêu cầu trong slot riêng."""
        from langchain_core.messages import AIMessage
        index = self.index
        self.index += 1
        if index == 0:
            reply, _ = self.calls.call(self.slot, self.body, self.attempt)
            return AIMessage(content=reply)
        options = {"temperature": self.body["temperature"], "max_tokens": self.body["max_tokens"]}
        return VisionProxy(self.calls, f"{self.slot}/format-{index}", self.attempt,
                           {"model": VISION, "options": options}).invoke(messages)


class ComponentStudy:
    """375 Decision duy nhất, 120 upstream và hai panel theo manifest gốc."""

    def __init__(self, root: Path) -> None:
        self.root = root
        raw = git_blob(root, DONOR, MANIFEST)
        self.source_sha256 = sha256(raw).hexdigest()
        jobs = json.loads(raw)["jobs"]
        if Counter(j["phase"] for j in jobs) != {"main": 204, "upstream": 36, "factorial": 135}:
            raise ValueError("Số lượt Decision khác manifest thành phần")
        self.jobs: dict[str, list[dict]] = defaultdict(list)
        self.points = []
        self.parents = {}
        for job in jobs:
            unit, context = job["unit"], job["context"]
            identifier, realization = unit["id"], context["realization"]
            if identifier not in self.jobs:
                self.points.append({"id": identifier, "symbol": unit["symbol"],
                                    "cutoff": unit["date"], "fold": unit["fold"]})
            self.jobs[identifier].append(job)
            if job["phase"] == "factorial":
                continue
            shard = job["origin_path"].split("/decisions/")[0]
            key = (identifier, realization)
            if self.parents.setdefault(key, shard) != shard:
                raise ValueError("Hai phương pháp dùng hai parent upstream")
        if len(self.points) != 102 or len(self.parents) != 120 or len({j["id"] for j in jobs}) != 375:
            raise ValueError("Cohort, realization hoặc danh tính lượt Decision bị lệch")

    def call_counts(self, points: list[dict]) -> dict[str, int]:
        """Đếm lượt cơ sở theo whitelist, tính upstream dùng chung một lần."""
        selected = {p["id"] for p in points}
        count = sum(identifier in selected for identifier, _ in self.parents)
        return {"pattern": count, "trend": count,
                "decision": sum(len(self.jobs[p["id"]]) for p in points)}

    def request(self, point: dict, realization: int, role: str) -> dict:
        """Kiểm hash và context trước khi tái dùng nội dung vision đã khóa."""
        identifier = point["id"]
        shard = self.parents[identifier, realization]
        node = archive(self.root, f"{shard}/nodes/{identifier}_r{realization}_{role.title()}.json")
        (ref,) = [row for row in node["call_hashes"] if row["path"].endswith(".request.json")]
        raw = git_blob(self.root, DONOR, f"{shard}/{ref['path']}")
        if sha256(raw).hexdigest() != ref["sha256"]:
            raise ValueError("Request upstream thành phần khác hash")
        request = json.loads(raw)
        context = request["context"]
        if (context["unit_id"], context["realization"], context["node"], context["model"]) != (
                identifier, realization, role.title() + " Agent", VISION):
            raise ValueError("Request upstream thành phần khác mã, vai trò hoặc realization")
        (batch,) = request["messages"]
        roles = {"system": "system", "human": "user", "ai": "assistant"}
        messages = [{"role": roles[m["type"]], "content": m["data"]["content"]} for m in batch]
        return wire_body(request["model_metadata"], messages, request["invocation_parameters"])

    def upstream(self, book: Any, point: dict, realization: int, calls: Any, frame: Any) -> dict:
        """Dùng 45 nến PIT để chạy chính bộ kiểm tra đầu ra của Pattern và Trend."""
        prefix = frame.loc[frame.Datetime <= point["cutoff"]].tail(45)
        if len(prefix) != 45 or str(prefix.Datetime.iloc[-1].date()) != point["cutoff"]:
            raise ValueError("Thiếu cửa sổ 45 nến PIT của thành phần")
        state = {"stock_name": point["symbol"], "as_of_date": point["cutoff"],
                 "window_end_date": point["cutoff"], "time_frame": "1d", "language": "vi",
                 "is_backtest": True, "messages": [], "kline_data": snapshot_payload(prefix)}
        reports = {}
        for role, factory in MODELS:
            body = self.request(point, realization, role)
            (image,) = [part["image_url"]["url"] for message in body["messages"]
                        if isinstance(message["content"], list) for part in message["content"]
                        if part["type"] == "image_url"]
            if not image.startswith("data:image/png;base64,"):
                raise ValueError("Ảnh thành phần khác định dạng PNG")
            slot = f"component/{point['id']}/u{realization}/{role}"

            def run(attempt: str) -> dict:
                proxy = ArchivedVision(calls, slot, attempt, body)
                token = ENABLED.set(True)
                try:
                    with invocation_scope(role), redirect_stdout(io.StringIO()):
                        output = factory(None, proxy, TechnicalTools())(
                            deepcopy(state) | {role + "_image": image.split(",", 1)[1]})
                finally:
                    ENABLED.reset(token)
                if not proxy.index or not output[role + "_report"].strip():
                    raise ValueError("Node thành phần thiếu báo cáo vision")
                return {"report": output[role + "_report"]}

            reports[role] = book.execute(slot, {"body_sha256": digest(body), "state_sha256": digest(state)}, run)["report"]
            state[role + "_report"] = reports[role]
        return reports

    def run_point(self, book: Any, point: dict, calls: Any, frame: Any) -> dict:
        """Dùng chung upstream cho mọi nhánh cùng realization, rồi chốt toàn bộ điểm."""
        identifier = point["id"]
        shared = {}
        rows = []
        for job in self.jobs[identifier]:
            context = job["context"]
            realization, repeat, method = (context[key] for key in ("realization", "repeat", "variant"))
            if realization not in shared:
                shared[realization] = book.execute(
                    f"shared/{identifier}/u{realization}", {"point": point, "realization": realization},
                    lambda _: self.upstream(book, point, realization, calls, frame))
            reports = shared[realization]
            prompt = decision_prompt(job["prompt"], deepcopy(reports))
            metadata = job["request_contract"]
            body = wire_body(metadata["model_metadata"], [{"role": "user", "content": prompt}],
                             metadata["invocation_parameters"])
            if body["model"] != DECISION:
                raise ValueError("Decision khác model đã lưu")
            slot = "decision/" + job["id"]

            def run(attempt: str) -> dict:
                reply, wire = calls.call(slot, body, attempt)
                action = TradeDecisionOutput.model_validate(reply, strict=True).decision
                return {"final_action": "CASH" if action == "SHORT" else action, "source_request_id": wire["id"]}

            record = book.execute(slot, {"shared_sha256": digest(reports), "body_sha256": digest(body)}, run)
            row = {**point, **record, "method": method, "repeat": repeat, "panel": job["phase"],
                   "realization": realization, "shared_sha256": digest(reports), "fallback": False}
            rows.append(row)
            if job["phase"] == "main" and any(p["phase"] == "upstream" for p in self.jobs[identifier]):
                rows.append({**row, "panel": "upstream"})
        return {"rows": rows}

    def controls(self, points: list[dict]) -> list[dict]:
        """Giữ dự báo các mô hình số và CASH đã lưu trên đúng mẫu chính."""
        by_id = {p["id"]: p for p in points}
        rows = csv.DictReader(io.StringIO(git_blob(self.root, DONOR, NUMERIC).decode("utf-8")))
        return [{**by_id[row["unit_id"]], "method": row["variant"], "panel": "main", "repeat": 0,
                 "realization": 0, "source_request_id": None, "fallback": False, "label_net": row["label_net"],
                 "final_action": "LONG" if row["prediction"] == "LONG" else "CASH"}
                for row in rows if row["unit_id"] in by_id]
