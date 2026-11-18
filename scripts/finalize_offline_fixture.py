"""Đối chứng hai phase nghiên cứu, dừng sau raw và kiểm lại từ tiến trình mới."""
from __future__ import annotations

from contextlib import redirect_stdout
from pathlib import Path
from typing import Any
import io
import json

import httpx

from core.finalize_budget_archive import Archive
from core.finalize_budget_study import StudyProvider
from core.finalize_serving_resources import FinalizedResources
from core.finalize_study_runner import OfflineStudyRunner
from core.historical_evaluation_journal import load
from core.serving_runtime.quota import Stopped, Unknown
from core.serving_runtime.resources import default_models
from core.unified_contracts import digest
from core.unified_execution import StageBook
from core.unified_execution_transport import MockHTTP
from scripts.finalize_serving_preview import FixtureClock, FixtureSender

RESEARCH_SAMPLE = ["FPT-2023-07-03", "HVN-2025-10-01"]


def require(condition: bool, message: str) -> None:
    """Kiểm bằng ngoại lệ kể cả khi dùng Python tối ưu."""
    if not condition:
        raise ValueError(message)


class Fixture:
    """MockTransport thật với đồng hồ ảo và khả năng ngắt tại biên durable."""

    def __init__(self, *, timeout_first: bool = False, forbid_send: bool = False) -> None:
        self.clock = FixtureClock()
        self.sender = FixtureSender(self.clock)
        self.timeout_first, self.forbid_send = timeout_first, forbid_send
        self.attempts = 0
        self.transport = MockHTTP(self.handle)

    def handle(self, request: httpx.Request) -> httpx.Response:
        """Giữ JSON wire ở transport thật; cold replay phải có 0 lượt dispatch."""
        self.attempts += 1
        if self.forbid_send:
            raise AssertionError("Cold replay đã cố dispatch")
        if self.timeout_first and self.attempts == 1:
            raise TimeoutError("Đối chứng mất kết nối trước mock response")
        status, raw, headers = self.sender.send(json.loads(request.content))
        return httpx.Response(status, content=raw, headers=headers)


class Cases:
    """Chỉ dùng provider và tài nguyên đã khóa; outcome thị trường tiếp tục đóng."""

    def __init__(self, resources: FinalizedResources, archive: Archive, release: dict,
                 budget: dict, cohort: list[dict], variants: list[str], workspace: Path) -> None:
        self.resources, self.archive, self.release = resources, archive, release
        self.budget, self.cohort, self.variants, self.workspace = budget, cohort, variants, workspace

    def runner(self, name: str, fixture: Fixture, *, research: list[str] | None = None,
               hook=lambda _: None) -> OfflineStudyRunner:
        """Dùng lại renderer, FIN07 references và Graph đúng kiểu request FIN09."""
        selected = research if research is not None else [self.budget["smoke_point_id"]]
        points = [row for row in self.cohort if row["id"] in selected]
        provider = StudyProvider(self.resources, points, default_models(), self.variants)
        return OfflineStudyRunner(self.workspace/name, self.release, self.budget, self.cohort, selected,
                                  "SMOKE" if research is None else "RESEARCH", provider, self.archive,
                                  fixture.transport, fixture.clock, hook)


def run_tick(runner: OfflineStudyRunner, *, read_only: bool = False) -> dict:
    """Giảm log renderer và giữ ngoại lệ từ đúng stage."""
    with redirect_stdout(io.StringIO()):
        return runner.tick(read_only=read_only)


def expect_stop(runner: OfflineStudyRunner, error: type[BaseException]) -> None:
    """Điều kiện dừng phải xuất hiện trước khi runner báo hoàn tất."""
    try:
        run_tick(runner)
    except error:
        return
    raise ValueError("Fixture không dừng ở biên dự kiến")


def check_counts(result: dict, runner: OfflineStudyRunner, fixture: Fixture) -> dict:
    """Khớp chứng cứ theo slot, số lần gửi và quan hệ smoke/research."""
    forecast_count = sum(len(row["forecasts"]) for row in result["points"].values())
    raw = [row for slot in runner.calls.plans for row in runner.calls.rows(slot)]
    reused = [proof for row in result["points"].values() for proof in row["vision"].values() if proof["state"] == "REUSE"]
    ids = [row["id"] for row in raw] + [row["raw_id"] for row in reused]
    require(len(ids) == len(set(ids)) and forecast_count == len(runner.points)*8*runner.repeats
            and result["outcomes_opened"] == 0 and len(raw) == fixture.attempts,
            "Mất hoặc trùng UUID, slot forecast hay outcome trong fixture")
    book = StageBook(runner.directory/"journal", runner.identity, verify_only=True)
    require(not any(book.path("outcome/"+point["id"]).exists() for point in runner.points), "Fixture đã mở outcome")
    return {"forecasts": forecast_count, "vision_reused": len(reused), "fixture_attempts": fixture.attempts,
            "raw_ids_sha256": digest(ids)}


def stop_case(cases: Cases) -> tuple[dict, dict]:
    """Dừng ngay sau raw, rồi resume bằng runner mới trên đúng checkpoint."""
    fixture = Fixture()
    directory = cases.workspace/"research"
    stop_flag = directory/"stop.request"

    def stop_after_raw(stage: str) -> None:
        if stage == "raw":
            stop_flag.touch()
            raise Stopped()

    initial = cases.runner("research", fixture, research=RESEARCH_SAMPLE, hook=stop_after_raw)
    expect_stop(initial, Stopped)
    before = {slot: rows[0]["id"] for slot in initial.calls.plans if (rows := initial.calls.rows(slot))}
    require(len(before) == fixture.attempts == 1, "Stop phải giữ đúng một raw durable")
    resumed = cases.runner("research", fixture, research=RESEARCH_SAMPLE)
    expect_stop(resumed, Stopped)
    require(fixture.attempts == 1, "Stop flag chưa gỡ nhưng transport đã chạy")
    stop_flag.unlink()
    result = run_tick(resumed)
    require(all(resumed.calls.rows(slot)[0]["id"] == raw_id and len(resumed.calls.rows(slot)) == 1
                for slot, raw_id in before.items()), "Resume gửi lại raw đã lưu")
    counts = check_counts(result, resumed, fixture)
    require(counts["vision_reused"] == 2, "Mẫu research chưa kiểm đúng hai raw reuse HVN")
    slot = next(slot for slot in resumed.calls.plans if slot.startswith("forecast/") and resumed.calls.rows(slot))
    wire = directory/"http"/(digest(slot)+".json")
    detached = wire.with_suffix(".fixture-held")
    wire.rename(detached)
    try:
        expect_stop(resumed, ValueError)
        require(fixture.attempts == counts["fixture_attempts"] and not wire.exists(),
                "Resume tự gửi lại khi raw của checkpoint complete bị thiếu")
    finally:
        detached.rename(wire)
    return result, {**counts, "stop_after_raw_preserves_first_uuid": True,
                    "completed_slot_missing_raw_blocks_dispatch": True}


def unknown_case(cases: Cases) -> dict:
    """Timeout giữ UNKNOWN qua restart; chỉ resume sau đối soát UUID đối chứng."""
    fixture = Fixture(timeout_first=True)
    initial = cases.runner("unknown", fixture)
    expect_stop(initial, Unknown)
    pending = [(slot, rows[0]) for slot in initial.calls.plans if (rows := initial.calls.rows(slot))]
    require(len(pending) == fixture.attempts == 1, "Timeout phải tạo đúng một intent")
    slot, unknown = pending[0]
    require(unknown["status"] == "UNKNOWN" and unknown["reserved_tokens"] > 0,
            "Timeout không giữ đủ reserve UNKNOWN")
    resumed = cases.runner("unknown", fixture)
    expect_stop(resumed, Unknown)
    require(resumed.calls.rows(slot) == [unknown] and fixture.attempts == 1,
            "Restart đã gửi lại hoặc đổi intent UNKNOWN")
    transport = resumed.calls.transports[resumed.calls.plans[slot]["model"]]
    transport.reconcile_not_sent(slot, unknown["id"], "MockTransport xác nhận chưa tạo response trước timeout")
    fixture.clock.now += 86401
    result = run_tick(resumed)
    rows = resumed.calls.rows(slot)
    require([row["status"] for row in rows] == ["NOT_SENT", 200] and rows[0]["id"] == unknown["id"]
            and rows[0]["attempt"] == rows[1]["attempt"], "Đối soát không bảo toàn UUID/attempt")
    return {**check_counts(result, resumed, fixture), "unknown_reserve_preserved": True,
            "manual_uuid_reconciliation": True}


def preparation_hashes(runner: OfflineStudyRunner, point: str) -> dict:
    """Lấy hash preparation chỉ từ journal đối chứng, không đọc outcome."""
    book = StageBook(runner.directory/"journal", runner.identity, verify_only=True)
    records = {}
    for slot in runner.calls.plans:
        if slot.startswith("forecast/"+point+"/"):
            key = "prepare/"+slot
            inputs = load(book.path(key))["inputs"]
            records[slot] = digest(book.execute(key, inputs, None)["request"])
    return records


def poisoned_case(cases: Cases, original: dict) -> dict:
    """Đổi nến tương lai trong bản sao RAM, kiểm lại graph và cả 24 preparation."""
    identifier = RESEARCH_SAMPLE[0]
    fixture = Fixture()
    poisoned = cases.runner("poison", fixture, research=[identifier])
    point = poisoned.points[0]
    frame = poisoned.provider.projection.frames[point["symbol"]]
    future = frame.index[frame["Datetime"] > point["cutoff"]][0]
    frame.loc[future, ["Open", "High", "Low", "Close", "Volume"]] = -1.
    result = run_tick(poisoned)
    reference = cases.runner("research", Fixture(forbid_send=True), research=RESEARCH_SAMPLE)
    preparations = preparation_hashes(poisoned, identifier)
    require(result["points"][identifier]["shared_sha256"] == original["points"][identifier]["shared_sha256"]
            and len(preparations) == 24 and preparations == preparation_hashes(reference, identifier),
            "Giá tương lai đã đổi snapshot hoặc request/dependency của query")
    return {"point_id": identifier, "prepared_slots_equal": len(preparations), "shared_snapshot_equal": True}


def capture(cases: Cases) -> dict:
    """Tách smoke và research, giữ budget trước mọi test fault."""
    fixture = Fixture()
    smoke_runner = cases.runner("smoke", fixture)
    smoke = run_tick(smoke_runner)
    stats = check_counts(smoke, smoke_runner, fixture)
    require(stats["fixture_attempts"] == 6 and stats["vision_reused"] == 0, "Smoke phải có đúng sáu lượt mới")
    print("Smoke đối chứng hoàn tất 8 slot", flush=True)
    research, stop = stop_case(cases)
    print("Research đối chứng hoàn tất 48 slot sau stop/resume", flush=True)
    require(smoke["identity_sha256"] != research["identity_sha256"], "Smoke và research trùng identity")
    unknown = unknown_case(cases)
    print("UNKNOWN đã được kiểm qua restart và đối soát UUID đối chứng", flush=True)
    poison = poisoned_case(cases, research)
    return {"smoke": smoke, "research": research, "smoke_stats": stats, "research_stats": stop,
            "unknown_stats": unknown, "future_poison": poison, "hosted_requests": 0}


def replay(cases: Cases, expected: dict) -> dict:
    """Tiến trình sạch tái dựng request/policy với mock cấm dispatch."""
    fixture = Fixture(forbid_send=True)
    smoke = run_tick(cases.runner("smoke", fixture), read_only=True)
    research = run_tick(cases.runner("research", fixture, research=RESEARCH_SAMPLE), read_only=True)
    require(smoke == expected["smoke"] and research == expected["research"] and fixture.attempts == 0,
            "Cold replay đổi snapshot/policy hoặc có dispatch mới")
    return {"smoke_sha256": digest(smoke), "research_sha256": digest(research), "fixture_dispatches": fixture.attempts}
