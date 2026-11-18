"""Transport đối chứng FIN08, chỉ trả fixture cho runner đang kiểm offline."""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from core.finalize_serving_profile import VERSION
from core.serving_contracts import ServingRequest
from core.serving_runtime.service import Service
from core.unified_contracts import digest


class FixtureClock:
    """Tiến ngày ảo sau mỗi lượt giả lập để kiểm journal mà không chờ quota thật."""
    def __init__(self) -> None:
        self.now = 1_700_000_000.

    def __call__(self) -> float:
        return self.now


class FixtureSender:
    """Giữ raw response ABI, không có kết nối hoặc cơ chế fetch dự phòng."""
    def __init__(self, clock: FixtureClock) -> None:
        self.clock = clock
        self.calls: list[tuple[str, str]] = []

    def send(self, body: dict) -> tuple[int, bytes, dict]:
        """Tạo phản hồi tối thiểu hợp lệ cho vision, Decision và facts."""
        from core.mt_bicl_decision import OUTPUT_MARKER
        self.clock.now += 86401
        prompt = body["messages"][0]["content"]
        if "response_format" in body:
            reply = {"decision": "SHORT", "forecast_horizon": "T+2.5", "confidence": "Thấp", "risk_reward_ratio": 1.,
                     "justification": "Đối chứng offline.", "evidence_for": "Đối chứng offline.",
                     "evidence_against": "Đối chứng offline."}
            schema = body["response_format"]["json_schema"]["schema"]
            if "fact_ids" in schema.get("properties", {}):
                template = json.loads(prompt.rsplit(OUTPUT_MARKER, 1)[-1])
                reply.update({k: template[k] for k in ("version", "fact_ids", "fact_assertions", "context_reason")})
            if len(body["messages"]) > 1:
                reply["display_en"] = {k: "Offline fixture." for k in ("justification", "evidence_for", "evidence_against")}
            content = json.dumps(reply, ensure_ascii=False)
            self.calls.append(("decision", digest(body)))
        else:
            vi = "**Thiên lệch dự báo:** NEUTRAL\n**Hướng xu hướng:** NEUTRAL\nĐối chứng offline."
            en = "**Directional bias:** NEUTRAL\n**Trend direction:** NEUTRAL\nOffline fixture."
            content = (json.dumps({"vi": vi, "en": en}, ensure_ascii=False)
                       if "LIVE UI OUTPUT OVERRIDE" in body["messages"][-1]["content"] else vi)
            self.calls.append(("vision", digest(body)))
        raw = {"choices": [{"message": {"content": content}}], "usage": {"total_tokens": 20}}
        return 200, json.dumps(raw, ensure_ascii=False).encode(), {}

    def close(self) -> None:
        """Transport fixture không giữ socket hoặc client."""


def run(root: Path, spec: ServingRequest, *, preview: bool) -> dict:
    """CLI dùng đúng service/runner; preview cô lập owner và khóa outcome."""
    if spec.document()["version"] != VERSION:
        raise ValueError("CLI finalize cần request finalize_serving_v1")
    with TemporaryDirectory() as temporary:
        if not preview:
            return Service(root, state_root=Path(temporary)).preflight(spec, "")
        clock = FixtureClock()
        sender = FixtureSender(clock)
        service = Service(root, state_root=Path(temporary), clock=clock, sender_factory=lambda _: sender, finalize_fixture=True)
        proof = service.preflight(spec, "offline-fixture")
        if not proof["run_enabled"]:
            return proof
        owner = digest("finalize-cli-offline-preview")
        identifier = service.create(spec, "offline-fixture", owner, background=False)
        service.work(identifier, "offline-fixture", owner, wait=False)
        result = service.result(identifier, owner)
        if result["state"] != "completed":
            raise ValueError("Fixture FIN08 chưa hoàn tất: " + result["state"] + " " + str(result["error"]))
        result["fixture_calls"] = {kind: sum(k == kind for k, _ in sender.calls) for kind in ("vision", "decision")}
        return result
