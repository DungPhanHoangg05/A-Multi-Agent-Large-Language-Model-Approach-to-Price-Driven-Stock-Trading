"""Thu phản hồi FIN11 theo grant một org Free và checkpoint riêng từng phase."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import math
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_budget_archive import Archive
from core.finalize_budget_quota import ATTEMPT_CAP, ORG, local_quota
from core.finalize_budget_study import NAMESPACE, StudyProvider
from core.finalize_study_runner import OfflineStudyRunner, PlannedCalls
from core.groq_pacing import MODEL_LIMITS
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock, utc_now
from core.serving_runtime.quota import Failed, Quota, Stopped, Unknown, Waiting
from core.serving_runtime.resources import default_models
from core.serving_runtime.transport import Calls, GroqHTTP
from core.unified_contracts import digest, json_bytes
from core.unified_execution_transport import MockHTTP
from core.unified_preflight_assets import write_new
from core.unified_protocol import binding, read
from scripts.finalize_offline_acceptance import RECEIPT, freeze, verify_record
from scripts.prepare_finalize_api_budget import study

RUN = ROOT/"outputs"/"finalize"/"fin11_v1"
VERSION = "finalize_hosted_study_v1"
SOURCE = "scripts/finalize_hosted_study.py"
PHASES = ("SMOKE", "RESEARCH")


def verify_balance(evidence: dict, now: float) -> float:
    """Giữ riêng xác nhận đủ quota và số dư cụ thể do chủ org đọc trên Console."""
    if (set(evidence) != {"org_slot", "tier", "observed_at", "remaining_tokens_24h", "source"}
            or evidence["org_slot"] != ORG or evidence["tier"] != "FREE"
            or evidence["source"] not in {"OWNER_ATTESTED_GROQ_CONSOLE", "OWNER_ATTESTED_SUFFICIENT"}):
        raise ValueError("Quota cần xác nhận của chủ org Free đã khóa")
    remaining = evidence["remaining_tokens_24h"]
    if evidence["source"] == "OWNER_ATTESTED_SUFFICIENT":
        if remaining is not None:
            raise ValueError("Xác nhận đủ quota không ghi thành số dư đã đo")
    elif (type(remaining) is not dict or set(remaining) != set(MODEL_LIMITS)
          or any(type(value) is not int or not 0 <= value <= MODEL_LIMITS[model]["tpd"]
                 for model, value in remaining.items())):
        raise ValueError("Số dư phải bao phủ quota 24 giờ của hai model")
    observed = datetime.fromisoformat(evidence["observed_at"])
    if observed.tzinfo is None or not 0 <= now-observed.timestamp() < 86400:
        raise ValueError("Cần ảnh chụp quota trong cửa sổ 24 giờ hiện tại, kèm múi giờ")
    return observed.timestamp()


class HostedQuota(Quota):
    """Cùng DB cho smoke/research của một model, giữ carry cạnh quota phát sinh."""

    def seed(self, model: str, grant: dict) -> None:
        """Seed bền vững, dùng giá trị xấu hơn giữa Console và ledger cục bộ."""
        limits = MODEL_LIMITS[model]
        observed = datetime.fromisoformat(grant["local_quota"]["observed_at_utc"]).timestamp()
        remaining = grant["balance"]["remaining_tokens_24h"]
        local = grant["local_quota"]["models"][model]
        available = local["local_estimated_day_tokens_remaining"]
        if remaining is not None:
            available = min(available, remaining[model])
        tokens = limits["tpd"]-available
        requests = limits["rpd"]-grant["local_quota"]["models"][model]["local_estimated_day_requests_remaining"]
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            marker = db.execute("SELECT value FROM metadata WHERE name='fin11_grant'").fetchone()
            signature = digest(grant)
            if marker is not None:
                if marker[0] != signature:
                    raise ValueError("Quota khác grant, không đặt lại carry")
                return
            if db.execute("SELECT 1 FROM attempts LIMIT 1").fetchone() is not None:
                raise ValueError("Quota đã có attempt nhưng thiếu identity của carry")
            count = max(int(tokens > 0), requests)
            db.executemany("INSERT INTO attempts(id,run,started,reserve,used,state,observed) VALUES (?,?,?,0,?,'CARRY',1)",
                           [(f"carry-{i}", "FIN11_CARRY", observed, tokens if i == 0 else 0) for i in range(count)])
            db.execute("INSERT INTO metadata VALUES ('fin11_grant',?)", (signature,))

    def observe(self, identifier: str, headers: dict, observed_at: float) -> None:
        """Dừng khi provider hạ giới hạn đã khóa, kể cả sau khi khởi động lại."""
        for suffix, limit in (("requests", 1000), ("tokens", 8000)):
            raw = headers.get("x-ratelimit-limit-"+suffix)
            if raw is not None and (not math.isfinite(float(raw)) or float(raw) < limit):
                raise Failed("PROVIDER_LIMIT_BELOW_GRANT")
        super().observe(identifier, headers, observed_at)


def quota_for(root: Path, grant: dict, model: str, clock=time.time) -> HostedQuota:
    """Model giữ tên file ổn định xuyên phase và credential scope."""
    index = sorted(MODEL_LIMITS).index(model)
    quota = HostedQuota(root/"quota"/f"model-{index}.sqlite3", clock)
    quota.seed(model, grant)
    return quota


class HostedCalls(PlannedCalls):
    """Giữ chuẩn body và U08 reuse FIN10, cấp quota dùng chung xuyên phase."""

    def __init__(self, runner: Any, plans: dict, archive: Archive, sender: GroqHTTP | MockHTTP, clock: Any) -> None:
        self.plans, self.archive = plans, archive
        self.transports = {model: Calls(runner.directory, digest(runner.identity),
                                        quota_for(runner.run_root, runner.grant, model, clock), sender,
                                        runner.guard_dispatch, clock=clock, total_prompt_guard=True)
                           for model in MODEL_LIMITS}

    def call(self, slot: str, body: dict, attempt: str) -> tuple[Any, dict]:
        """Raw mới có usage đo được; lỗi giữ raw để đối soát tại đúng UUID."""
        reply, raw = super().call(slot, body, attempt)
        if self.plans[slot]["state"] == "NEW" and type(raw.get("usage")) is not int:
            raise Failed("PROVIDER_USAGE_MISSING")
        return reply, raw


class HostedStudyRunner(OfflineStudyRunner):
    """Dùng lại đường graph/DAG được kiểm FIN10, với policy admission hosted riêng."""

    def __init__(self, run_root: Path, grant: dict, budget: dict, points: list[dict], phase: str,
                 provider: StudyProvider, archive: Archive, sender: GroqHTTP | MockHTTP, clock=time.time) -> None:
        if phase not in PHASES or len(points) != 102 or grant["org_slot"] != ORG or grant["budget_sha256"] != digest(budget):
            raise ValueError("Scope hosted khác cohort hoặc grant FIN11")
        self.run_root, self.grant = run_root, grant
        self.directory, self.provider = run_root/phase.lower(), provider
        self.read_only = False
        self.ordinals = {point["id"]: i for i, point in enumerate(points)}
        self.points = points if phase == "RESEARCH" else [point for point in points if point["id"] == budget["smoke_point_id"]]
        self.repeats = 3 if phase == "RESEARCH" else 1
        self.identity = {"namespace": NAMESPACE, "scope": "HOSTED_SINGLE_ORG_FREE", "epoch": f"FIN11_{phase}_V1",
                         "phase": phase, "points": self.points, "org_slot": ORG, "repeats": self.repeats,
                         "realizations": 1, "release_sha256": digest(grant), "budget_sha256": digest(budget)}
        plans = {row["slot"]: row for row in budget["slots"] if row["phase"] == phase}
        if len(plans) != len(self.points)*(2+8*self.repeats) or any(row["state"] == "UNKNOWN" for row in plans.values()):
            raise ValueError("Phase thiếu slot hoặc còn UNKNOWN trong kế hoạch")
        self.calls = HostedCalls(self, plans, archive, sender, clock)

    def guard(self) -> None:
        """Ngừng trước HTTP/stage mới nếu có stop flag toàn lượt thu."""
        if (self.run_root/"stop.request").exists():
            raise Stopped()
        super().guard()

    def vision_proofs(self, book: Any, point: dict) -> dict:
        """Ghi epoch hosted thật cho raw mới; giữ epoch U08 của raw reuse."""
        result = super().vision_proofs(book, point)
        for proof in result.values():
            if proof["state"] == "NEW":
                proof["epoch"] = self.identity["epoch"]
        return result

    def collect(self, wait: Any, release_guard=lambda: None) -> None:
        """Checkpoint sau mỗi point, tiếp tục chính slot dở khi quota mở."""
        points = self.points
        try:
            for point in points:
                self.guard()
                path = self.directory/"points"/(point["id"]+".json")
                if path.exists():
                    done = load(path)
                    if done["identity_sha256"] != digest(self.identity) or list(done["points"]) != [point["id"]]:
                        raise ValueError("Checkpoint point khác grant")
                    continue
                release_guard()
                self.points = [point]
                while True:
                    try:
                        save(path, self.tick())
                        break
                    except Waiting as pending:
                        wait(self.identity["phase"], point["id"], pending.until)
                        release_guard()
        finally:
            self.points = points

    def seal_phase(self) -> dict:
        """Cold verify đủ forecast và raw trước khi đóng smoke/research."""
        result = self.tick(read_only=True)
        if sum(len(point["forecasts"]) for point in result["points"].values()) != len(self.points)*self.repeats*8:
            raise ValueError("Forecast grid chưa đủ")
        for point, value in result["points"].items():
            checkpoint = load(self.directory/"points"/(point+".json"))
            if checkpoint != {**result, "points": {point: value}}:
                raise ValueError("Point checkpoint khác cold replay")
        rows = [(slot, row) for slot in self.calls.plans for row in self.calls.rows(slot)]
        ids = [row["id"] for _, row in rows]
        if (len(ids) != len(set(ids)) or any(row["slot"] != slot or row["status"] == "UNKNOWN" for slot, row in rows)
                or len(rows) > ATTEMPT_CAP*sum(plan["state"] == "NEW" for plan in self.calls.plans.values())):
            raise ValueError("Attempt chưa được đối soát hoặc vượt trần FIN09")
        proof = {"phase": self.identity["phase"], "epoch": self.identity["epoch"], "points": len(self.points),
                 "forecast_slots": len(self.points)*self.repeats*8, "hosted_attempts": len(rows),
                 "tokens_measured": sum(row["usage"] or 0 for _, row in rows), "raw_attempts_sha256": digest([digest(row) for _, row in rows]),
                 "checkpoint_sha256": digest(result), "outcomes_opened": 0, "grant_sha256": digest(self.grant)}
        path = self.directory/"receipt.json"
        if path.exists() and load(path) != proof:
            raise ValueError("Receipt phase đã chốt khác raw")
        if not path.exists():
            write_new(path, json_bytes({"payload": proof, "sha256": digest(proof)}))
        return proof


def check_release() -> tuple[dict, Any]:
    """Giữ FIN10 nguyên byte; nhận delta hosted ở script tách riêng."""
    lock, budget, resources = freeze(ROOT)
    verify_record(read(ROOT, RECEIPT, True), lock)
    return {"version": VERSION, "org_slot": ORG, "spend_limit_usd": 0, "budget_sha256": digest(budget),
            "fin10": binding(ROOT, RECEIPT), "runner": binding(ROOT, SOURCE)}, (budget, resources)


def credential() -> str:
    """Chỉ dùng credential org đã kiểm metadata FIN09 trong tiến trình này."""
    from dotenv import dotenv_values
    key = dotenv_values(ROOT/".env").get(f"GROQ_ORG_{ORG}_API_KEY")
    if not key:
        raise ValueError("Thiếu credential của org đã khóa")
    return key


def authorize(evidence_path: Path) -> dict:
    """Tạo grant duy nhất từ dữ liệu chủ org xác nhận và phạm vi FIN09/10."""
    import json
    release, _ = check_release()
    evidence = json.loads(evidence_path.read_bytes())
    now = time.time()
    verify_balance(evidence, now)
    archive = Archive(ROOT)
    carry = local_quota(ROOT, archive.carry, datetime.fromtimestamp(now, timezone.utc).isoformat())
    scope = Quota(RUN/"credential.sqlite3").credential_scope(credential())
    grant = {**release, "balance": evidence, "local_quota": carry, "credential_scope_sha256": scope}
    write_new(RUN/"grant.json", json_bytes({"payload": grant, "sha256": digest(grant)}))
    return {"status": "GRANTED", "org_slot": ORG, "grant_sha256": digest(grant), "spend_limit_usd": 0}


def status(code: str, **fields: Any) -> dict:
    """Heartbeat chỉ ghi tiến độ, không ghi body/key hoặc lỗi raw ra console."""
    result = {"status": code, "at": utc_now(), **fields}
    save(RUN/"status.json", result)
    return result


def run(*, resume_stopped: bool = False) -> dict:
    """Smoke hoàn tất và đối soát trước nghiên cứu; giữ checkpoint khi tạm dừng."""
    grant = load(RUN/"grant.json")
    release, (budget, resources) = check_release()
    if any(grant[key] != value for key, value in release.items()):
        raise ValueError("Mã nguồn hoặc ngân sách không khớp grant FIN11")
    with PriorRunLock(RUN/"worker", digest(grant)):
        key = credential()
        if Quota(RUN/"credential.sqlite3").credential_scope(key) != grant["credential_scope_sha256"]:
            raise ValueError("Credential thay đổi khi resume")
        if resume_stopped:
            (RUN/"stop.request").unlink(missing_ok=True)
        points, variants, _, _ = study(ROOT)
        archive = Archive(ROOT)
        provider = StudyProvider(resources, points, default_models(), variants)
        sender = GroqHTTP(key)

        def wait(phase: str, point: str, until: float) -> None:
            status("WAITING_QUOTA", phase=phase, point=point, resume_at=datetime.fromtimestamp(until, timezone.utc).isoformat())
            while until > time.time():
                if (RUN/"stop.request").exists():
                    raise Stopped()
                time.sleep(min(45., max(.01, until-time.time())))

        def guard_release() -> None:
            if check_release()[0] != release:
                raise ValueError("Nguồn hoặc runtime thay đổi trong khi thu")

        try:
            results = {}
            for phase in PHASES:
                status("RUNNING", phase=phase)
                runner = HostedStudyRunner(RUN, grant, budget, points, phase, provider, archive, sender)
                runner.collect(wait, guard_release)
                results[phase] = runner.seal_phase()
            return status("PASS_FIN11", phases=results)
        except Stopped:
            return status("STOPPED", phase=phase)
        except Unknown:
            return status("UNKNOWN_NEEDS_RECONCILIATION", phase=phase)
        except Failed as error:
            return status("BLOCKED_PROVIDER", phase=phase, reason=str(error))
        except (ValueError, AssertionError, OSError, KeyError):
            status("BLOCKED_INTEGRITY", phase=phase)
            raise
        finally:
            sender.close()


def main() -> None:
    """CLI cấp grant, thu có độ bền, đọc tiến độ và đặt stop flag."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "authorize", "run", "resume", "status", "stop"))
    parser.add_argument("--balance", type=Path, help="JSON số dư Groq Console đã xác nhận")
    args = parser.parse_args()
    if args.mode == "authorize":
        if args.balance is None:
            parser.error("Cần --balance")
        result = authorize(args.balance)
    elif args.mode in {"run", "resume"}:
        import torch
        torch.set_num_threads(1)
        result = run(resume_stopped=args.mode == "resume")
    elif args.mode == "stop":
        if not (RUN/"grant.json").is_file():
            raise ValueError("Chưa có grant FIN11")
        (RUN/"stop.request").touch()
        result = {"status": "STOP_REQUESTED"}
    elif args.mode == "status":
        result = load(RUN/"status.json") if (RUN/"status.json").is_file() else {
            "status": "GRANTED_NOT_STARTED" if (RUN/"grant.json").is_file() else "READY_FOR_ACCOUNT_BALANCE"}
    else:
        release, _ = check_release()
        result = {"status": "READY_FOR_ACCOUNT_BALANCE", **release}
    print(json_bytes(result).decode())


if __name__ == "__main__":
    main()
