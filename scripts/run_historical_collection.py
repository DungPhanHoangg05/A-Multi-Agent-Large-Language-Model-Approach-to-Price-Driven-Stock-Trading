"""Thu H07 có giám sát: CORE4→OOD5→cold verify, giữ quota Free và toàn bộ checkpoint."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
RUN = Path("outputs/historical_reevaluation/run_r1")
MANAGED = Path("outputs/historical_reevaluation/managed_r1")
PHASES = (("collect_CORE4", "resume", "CORE4"), ("collect_OOD5", "resume", "OOD5"),
          ("verify_CORE4", "verify", "CORE4"), ("verify_OOD5", "verify", "OOD5"))
PINNED = ("scripts/run_historical_collection.py", "scripts/run_historical_evaluation_observed.py",
          "core/historical_transport_observer.py", "docs/plan/week11/historical_evaluation_runtime.json",
          "docs/plan/week11/historical_evaluation_protocol.json", "docs/plan/week11/historical_evaluation_release.json",
          "docs/plan/week11/historical_evaluation_inputs.json", "docs/plan/week11/historical_evaluation_quota.json")


def file_proof(path: Path) -> dict:
    """Băm byte bằng chứng; không mở payoff hoặc đọc credential."""
    with path.open("rb") as handle:
        sha = hashlib.file_digest(handle, "sha256").hexdigest()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha}


def pinned_sources() -> dict:
    """Supervisor chỉ chạy source đã neo Git, không đổi phiên bản giữa các phase."""
    for name in PINNED:
        if (ROOT / name).read_bytes() != subprocess.check_output(["git", "show", "HEAD:" + name], cwd=ROOT):
            raise ValueError("Source supervisor chưa neo Git: " + name)
    return {name: file_proof(ROOT / name) for name in PINNED}


def interruption(directory: Path, identity: dict, *, now: float | None = None) -> dict | None:
    """Đối soát đúng UUID/raw503 hoặc quota chưa dispatch; mọi trường hợp khác dừng."""
    from core.bayesian_memory import read_json
    from core.historical_evaluation_journal import load
    from core.historical_evaluation_protocol import digest
    from core.prior_run_lock import safe_path
    now = time.time() if now is None else now
    pending = []
    for path in (directory / "slots").glob("*.json"):
        doc = load(path)
        if doc["attempts"][-1]["status"] != "complete":
            pending.append(doc)
    if len(pending) != 1:
        return None
    doc = pending[0]; last = doc["attempts"][-1]
    if (doc["signature"] != identity["signature"] or doc["run_uuid"] != identity["run_uuid"]
            or doc["inputs_sha256"] != digest(doc["inputs"]) or last.get("authorization") is not None):
        return None
    attempts = {a["attempt_id"] for a in doc["attempts"]}
    ledger_paths = list((directory / "usage").glob("org*.json"))
    ledgers = [read_json(p) for p in ledger_paths]
    rows = [r for ledger in ledgers for r in ledger["requests"] if r.get("checkpoint_attempt_id") in attempts]
    if len(rows) >= 3 or any(r.get("run_signature") != identity["signature"] or r["status"] == 200 for r in rows):
        return None
    current = [r for r in rows if r.get("checkpoint_attempt_id") == last["attempt_id"]]
    def checked_raw(row: dict) -> dict | None:
        """Mọi quyết định tự tiếp tục đều gắn byte raw với UUID và body đã audit."""
        proof = row.get("historical_raw")
        if not proof:
            return None
        path = safe_path(directory, proof["path"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != proof["sha256"]:
            raise ValueError("Raw503 khác checksum")
        raw = load(path)
        if (raw["status"] != row["status"] or raw["slot"]["checkpoint_attempt_id"] != last["attempt_id"]
                or raw["slot"]["run_signature"] != identity["signature"]
                or raw["request_legacy_body_sha256"] != row["improvement_audit"]["request"]["canonical_body_sha256"]):
            return None
        return raw
    if len(current) == 1 and current[0]["status"] == 503:
        row = current[0]; raw = checked_raw(row)
        if raw is None:
            return None
        try:
            retry = float(raw.get("headers", {}).get("retry-after", 0))
        except (TypeError, ValueError):
            retry = 0.
        if not 0 <= retry <= 86400:
            return None
        return {"attempt_id": last["attempt_id"], "reason": "RAW_HTTP503_AUDITED", "slot": doc["slot"],
                "resume_at": now + max(30. * 2 ** (len(rows) - 1), retry), "http_count": len(rows),
                "raw_sha256": row["historical_raw"]["sha256"]}
    if current and all(r["status"] == 429 for r in current):
        if not all(checked_raw(r) is not None for r in current):
            return None
        reset = max(r.get("retry_until", 0) for r in current)
        if now < reset <= now + 86401:
            return {"attempt_id": last["attempt_id"], "reason": "HTTP429_PROVIDER_WAIT_AUDITED", "slot": doc["slot"],
                    "resume_at": reset + 2., "http_count": len(rows)}
    if current:
        return None
    # Quota dừng trước reserve/HTTP: không suy diễn rằng một transport timeout chưa được xử lý.
    started = datetime.fromisoformat(last["started_at"]).timestamp()
    allowed = {"DAILY_QUOTA", "PROVIDER_DAILY_QUOTA", "WAIT_BUDGET_EXCEEDED", "INVOCATION_WAIT_BUDGET_EXCEEDED"}
    org = doc["inputs"].get("org", doc["inputs"].get("source", {}).get("org"))
    stops = [d.get("last_stop", {}) for p, d in zip(ledger_paths, ledgers) if p.stem == f"org{org}"]
    stops = [s for s in stops if s.get("reason") in allowed and s.get("at", 0) >= started and s.get("resume_not_before_utc")]
    if not stops:
        return None
    stop = max(stops, key=lambda s: s["at"])
    resume = datetime.fromisoformat(stop["resume_not_before_utc"]).timestamp()
    return {"attempt_id": last["attempt_id"], "reason": "PRE_DISPATCH_QUOTA_AUDITED", "slot": doc["slot"],
            "resume_at": max(now + 2., resume + 2.), "http_count": len(rows)}


def phase_result(path: Path, cohort: str, planned: int) -> dict:
    """Exit0 phải kèm summary phase đầy đủ, không coi PARTIAL là hoàn tất."""
    last = ""
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                last = line
    result = json.loads(last)
    if (result.get("status") != "PHASE_COMPLETE" or result.get("cohort") != cohort
            or result.get("completed_units") != planned or result.get("planned_units") != planned):
        raise ValueError("Phase chưa đầy đủ hoặc stdout không đúng schema")
    return result


def sync_plan(state: dict) -> None:
    """Chỉ cập nhật vùng tiến độ máy sở hữu; checklist DONE cần receipt bốn phase PASS."""
    start, end = "<!-- H07_MANAGED_START -->", "<!-- H07_MANAGED_END -->"
    if state["state"] == "COMPLETE":
        from core.historical_evaluation_journal import load
        receipt = load(ROOT / "docs/plan/week11/historical_evaluation_collection.json")
        if (receipt.get("status") != "PASS" or receipt.get("run_uuid") != state["run_uuid"]
                or set(receipt.get("phase_results", {})) != {p[0] for p in PHASES}
                or any(p["result"]["status"] != "PHASE_COMPLETE" for p in receipt["phase_results"].values())):
            raise ValueError("Chưa đủ receipt bốn phase PASS để đánh dấu DONE")
    local = lambda value: datetime.fromisoformat(value).astimezone(timezone(timedelta(hours=7))).strftime("%d/%m/%Y %H:%M:%S UTC+7")
    text = f"Trạng thái máy: **{state['state']}**; phase `{state.get('phase', '-')}`; cập nhật `{local(state['updated_at'])}`."
    if "checkpoint_files" in state:
        text += f" Số file checkpoint: {state['checkpoint_files']} (kể cả lượt đang chạy)."
    if state.get("resume_after_utc") and state["state"] == "WAITING":
        text += f" Chờ quota/backoff đến `{local(state['resume_after_utc'])}`."
    for name in ("docs/plan/plan.md", "docs/plan/week11/README.md", "docs/plan/week11/historical_reevaluation_plan.md"):
        path = ROOT / name; content = path.read_text(encoding="utf-8")
        if content.count(start) != 1 or content.count(end) != 1:
            continue
        before, rest = content.split(start); _, after = rest.split(end)
        content = before + start + "\n" + text + "\n" + end + after
        if state["state"] == "COMPLETE":
            if name.endswith("historical_reevaluation_plan.md"):
                content = content.replace("- [ ] H07 — Chạy đủ ma trận đánh giá.", "- [x] H07 — Chạy đủ ma trận đánh giá và cold verify PASS.")
                a, b = content.index("## H07"), content.index("## H08")
                content = content[:a] + content[a:b].replace("- [ ]", "- [x]") + content[b:]
            if name.endswith("week11/README.md"):
                content = re.sub(r"^(\| H07 \|[^|]+\|)[^|]+\|", r"\1 [x] DONE — đủ ma trận và hai cold verify PASS |", content, flags=re.M)
        path.write_text(content, encoding="utf-8")


def main() -> None:
    """Chạy nền liên tục, chờ quota đúng reset, chỉ kết sổ sau hai cold verify PASS."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("run", "status"))
    args = parser.parse_args()
    from dotenv import load_dotenv
    from core.historical_evaluation_clients import require_release
    from core.historical_evaluation_journal import RunBook, load, save
    from core.historical_evaluation_protocol import CORE4, digest
    from core.prior_run_lock import PriorRunLock, utc_now
    if args.stage == "status":
        print(json.dumps(load(ROOT / MANAGED / "status.json"), ensure_ascii=False))
        return
    sources = pinned_sources()
    assert require_release(ROOT)["mode"] == "RESEARCH"
    quota = load(ROOT / "docs/plan/week11/historical_evaluation_quota.json")
    assert quota["paid_api_allowed"] is False and quota["spend_limit_usd"] == 0
    load_dotenv(ROOT / ".env", override=False)
    keys = [os.environ.get(f"GROQ_ORG_{i}_API_KEY") for i in range(1, 6)]
    if not all(keys) or len(set(keys)) != 5:
        raise ValueError("Cần5 credential đã khóa, không hotswap")
    directory = ROOT / MANAGED; directory.mkdir(parents=True, exist_ok=True)
    bookdir = ROOT / RUN; identity = load(bookdir / "identity.json")
    inputs = load(ROOT / "docs/plan/week11/historical_evaluation_inputs.json")
    planned = {name: sum((u["symbol"] in CORE4) == (name == "CORE4") for u in inputs["grid"])
               for name in ("CORE4", "OOD5")}
    state_path = directory / "status.json"
    state = load(state_path) if state_path.exists() else {"run_uuid": identity["run_uuid"], "sources": sources,
                                                         "phase_results": {}, "started_at": utc_now(), "launches": 0}
    if state["sources"] != sources or state["run_uuid"] != identity["run_uuid"]:
        raise ValueError("Supervisor khác source/run; cần audit trước resume")
    def status(value: str, **fields: object) -> None:
        previous = (state.get("state"), state.get("phase"), state.get("reason"), state.get("checkpoint_files", 0) // 100)
        if value != "WAITING":
            state.pop("resume_after_utc", None); state.pop("reason", None)
        if value != "RUNNING":
            state["child_pid"] = None
        state.update(state=value, updated_at=utc_now(), manager_pid=os.getpid(), **fields)
        state["checkpoint_files"] = sum(1 for _ in (bookdir / "slots").glob("*.json"))
        save(state_path, state)
        if previous != (state.get("state"), state.get("phase"), state.get("reason"), state["checkpoint_files"] // 100):
            try:
                sync_plan(state)
            except (OSError, ValueError) as error:
                state["plan_sync_error"] = type(error).__name__
                save(state_path, state)
    def wait_until(timestamp: float, reason: str) -> None:
        status("WAITING", reason=reason, resume_after_utc=datetime.fromtimestamp(timestamp, timezone.utc).isoformat())
        heartbeat = time.monotonic()
        while time.time() < timestamp:
            time.sleep(max(0., min(30., timestamp - time.time())))
            if time.monotonic() - heartbeat >= 60:
                status("WAITING", reason=reason); heartbeat = time.monotonic()
    with PriorRunLock(directory, digest({"run_uuid": identity["run_uuid"], "supervisor_version": 1})):
        child = None
        try:
            for name, stage, cohort in PHASES:
                if name in state["phase_results"]:
                    proof = state["phase_results"][name]["log"]
                    if file_proof(ROOT / proof["path"]) != proof:
                        raise ValueError("Log phase đã PASS bị thay đổi")
                    continue
                while True:
                    if pinned_sources() != sources:
                        raise ValueError("Source thay đổi giữa các lượt chạy")
                    state["launches"] += 1
                    log = directory / f"{name}_{state['launches']:05d}.log"
                    before_http = ({p.relative_to(ROOT).as_posix(): file_proof(p) for folder in ("http", "usage")
                                    for p in (bookdir / folder).rglob("*") if p.is_file()} if stage == "verify" else None)
                    command = [sys.executable, "-X", "utf8", str(ROOT / "scripts/run_historical_evaluation_observed.py"),
                               stage, "--cohort", cohort, "--recover-connection-reset"]
                    with log.open("w", encoding="utf-8") as handle:
                        child = subprocess.Popen(command, cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT)
                        status("RUNNING", phase=name, child_pid=child.pid, child_log=log.relative_to(ROOT).as_posix())
                        heartbeat = time.monotonic()
                        while child.poll() is None:
                            time.sleep(10.)
                            if time.monotonic() - heartbeat >= 60:
                                status("RUNNING"); heartbeat = time.monotonic()
                        code = child.returncode
                    child = None
                    if code == 0:
                        result = phase_result(log, cohort, planned[cohort])
                        if before_http is not None:
                            after = {p.relative_to(ROOT).as_posix(): file_proof(p) for folder in ("http", "usage")
                                     for p in (bookdir / folder).rglob("*") if p.is_file()}
                            if after != before_http:
                                raise ValueError("Cold verify đã thay đổi HTTP/usage")
                            result["http_usage_unchanged"] = True
                        state["phase_results"][name] = {"result": result, "log": file_proof(log)}
                        status("PHASE_COMPLETE", phase=name)
                        break
                    if stage == "verify":
                        raise ValueError("Cold verify lỗi; không sửa output hoặc tự gửi API")
                    with PriorRunLock(bookdir, identity["signature"]):
                        action = interruption(bookdir, identity)
                    if action is None:
                        raise ValueError("Cần audit lỗi mới hoặc đã hết trần3 HTTP/slot; xem child_log")
                    wait_until(action["resume_at"], action["reason"])
                    with PriorRunLock(bookdir, identity["signature"]):
                        book = RunBook(bookdir, identity["identity"])
                        current = load(book.path(action["slot"]))["attempts"][-1]
                        if current["attempt_id"] == action["attempt_id"] and current["status"] == "unknown" and not current.get("authorization"):
                            book.reconcile(action["attempt_id"], "DELEGATED_H07_SUPERVISOR: " + json.dumps(action, ensure_ascii=False))
            # Bốn phase đều PASS; kiểm số slot theo H03 rồi băm toàn bằng chứng cho H08.
            if pinned_sources() != sources:
                raise ValueError("Source thay đổi trước kết sổ")
            require_release(ROOT)
            with PriorRunLock(bookdir, identity["signature"]):
                protocol = load(ROOT / "docs/plan/week11/historical_evaluation_protocol.json")
                forecast_count = label_count = graph_count = 0
                for path in (bookdir / "slots").glob("*.json"):
                    doc = load(path)
                    assert doc["attempts"][-1]["status"] == "complete"
                    forecast_count += int(doc["slot"].startswith("forecast/"))
                    label_count += int(doc["slot"].startswith("label/"))
                    graph_count += int(doc["slot"].startswith("graph/") and doc["slot"].endswith("/full"))
                assert forecast_count == protocol["budget"]["calls"]["decision"]
                assert label_count == len(inputs["grid"])
                assert graph_count == protocol["budget"]["calls"]["vision"] // 2
                records = {p.relative_to(ROOT).as_posix(): file_proof(p) for folder in ("slots", "http", "usage", "images")
                           for p in sorted((bookdir / folder).rglob("*")) if p.is_file()}
                manifest = bookdir / "collection_manifest.json"
                save(manifest, {"status": "PASS", "run_uuid": identity["run_uuid"], "records": records})
                receipt = {"status": "PASS", "scope": "H07_FULL_MATRIX_COLD_VERIFIED", "run_uuid": identity["run_uuid"],
                           "sources": sources, "phase_results": state["phase_results"], "manifest": file_proof(manifest),
                           "grid_units": len(inputs["grid"]), "forecast_slots": protocol["budget"]["calls"]["decision"],
                           "records_sha256": digest(records), "paid_api_allowed": False, "completed_at": utc_now()}
                save(ROOT / "docs/plan/week11/historical_evaluation_collection.json", receipt)
            status("COMPLETE", receipt="docs/plan/week11/historical_evaluation_collection.json")
        except BaseException as error:
            if child is not None and child.poll() is None:
                child.terminate(); child.wait()
            status("STOPPED", error_type=type(error).__name__, error=str(error), child_pid=None)
            raise


if __name__ == "__main__":
    main()
