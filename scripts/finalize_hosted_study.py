"""Thu FIN11 theo key Free do người vận hành chọn và dừng khi hết quota ngày."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from functools import cache, partial
from hashlib import sha256
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_budget_archive import Archive
from core.finalize_budget_quota import ATTEMPT_CAP, ORG, local_quota, window
from core.finalize_budget_study import NAMESPACE, StudyProvider
from core.finalize_study_runner import OfflineStudyRunner, PlannedCalls
from core.groq_pacing import MODEL_LIMITS
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock, utc_now
from core.serving_runtime.quota import Failed, Quota, Stopped, Unknown, Waiting
from core.serving_runtime.resources import default_models
from core.serving_runtime.transport import GroqHTTP
from core.unified_contracts import digest, json_bytes
from core.unified_execution_transport import MockHTTP
from core.unified_preflight_assets import write_new
from core.unified_protocol import binding, git_blob, read
from scripts.finalize_hosted_point_reset import archived_resets
from scripts.finalize_hosted_quota import DailyQuota, HostedWire, quota_for
from scripts.finalize_offline_acceptance import RECEIPT, freeze, verify_record
from scripts.prepare_finalize_api_budget import study

RUN = ROOT/"outputs"/"finalize"/"fin11_v1"
VERSION = "finalize_hosted_study_v3"
SOURCE = "scripts/finalize_hosted_study.py"
TRANSPORT = "core/serving_runtime/transport.py"
QUOTA_SOURCE = "scripts/finalize_hosted_quota.py"
RESET_SOURCE = "scripts/finalize_hosted_point_reset.py"
PREVIOUS = "ef030417"
RELEASE_V2_COMMIT = "c0721b02"
ORG_SLOTS = range(1, 6)
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


class HostedCalls(PlannedCalls):
    """Giữ chuẩn body và U08 reuse FIN10, cấp quota theo org qua các phase."""

    def __init__(self, runner: Any, plans: dict, archive: Archive, sender: GroqHTTP | MockHTTP, clock: Any) -> None:
        self.plans, self.archive = plans, archive
        @cache
        def ledger(model: str, slot: int):
            return quota_for(runner.run_root, account_grant(runner.run_root, runner.grant, slot), model, clock)

        self.transports = {model: HostedWire(runner.directory, digest(runner.identity), sender=sender,
                                            guard=runner.guard_dispatch, clock=clock, total_prompt_guard=True,
                                            org_slot=runner.org_slot, quota_at=partial(ledger, model),
                                            archived_attempts=runner.archived_attempts)
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
                 provider: StudyProvider, archive: Archive, sender: GroqHTTP | MockHTTP, clock=time.time,
                 *, org_slot: int = ORG) -> None:
        if (phase not in PHASES or len(points) != 102 or org_slot not in ORG_SLOTS
                or grant["org_slot"] != ORG or grant["budget_sha256"] != digest(budget)):
            raise ValueError("Scope hosted khác cohort hoặc grant FIN11")
        self.run_root, self.grant, self.org_slot = run_root, grant, org_slot
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
        self.resets = archived_resets(run_root, grant) if phase == "RESEARCH" else []
        self.archived_attempts = Counter()
        for record in self.resets:
            self.archived_attempts.update(record["attempts_by_slot"])
        if any(plans.get(slot, {}).get("state") != "NEW" for slot in self.archived_attempts):
            raise ValueError("Bản lưu point có slot ngoài ngân sách đã khóa")
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
                    except DailyQuota:
                        raise
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
        attempt_counts = Counter(slot for slot, _ in rows) + self.archived_attempts
        if (len(ids) != len(set(ids)) or any(row["slot"] != slot or row["status"] == "UNKNOWN" for slot, row in rows)
                or any(count > ATTEMPT_CAP for count in attempt_counts.values())
                or sum(attempt_counts.values()) > ATTEMPT_CAP*sum(plan["state"] == "NEW" for plan in self.calls.plans.values())):
            raise ValueError("Attempt chưa được đối soát hoặc vượt trần FIN09")
        proof = {"phase": self.identity["phase"], "epoch": self.identity["epoch"], "points": len(self.points),
                 "forecast_slots": len(self.points)*self.repeats*8, "hosted_attempts": len(rows),
                 "tokens_measured": sum(row["usage"] or 0 for _, row in rows), "raw_attempts_sha256": digest([digest(row) for _, row in rows]),
                 "checkpoint_sha256": digest(result), "outcomes_opened": 0, "grant_sha256": digest(self.grant)}
        if self.resets:
            if archived_resets(self.run_root, self.grant) != self.resets:
                raise ValueError("Bản lưu point thay đổi trong khi thu")
            proof["archived_point_attempts"] = [{"point_id": row["point_id"], "manifest_sha256": digest(row),
                                                 "hosted_attempts": row["archived_attempts"],
                                                 "tokens_measured": row["tokens_measured"],
                                                 "unknown_reserve_tokens": row["unknown_reserve_tokens"]} for row in self.resets]
            proof["hosted_attempts_including_archives"] = sum(attempt_counts.values())
        path = self.directory/"receipt.json"
        if path.exists() and load(path) != proof:
            raise ValueError("Receipt phase đã chốt khác raw")
        if not path.exists():
            write_new(path, json_bytes({"payload": proof, "sha256": digest(proof)}))
        return proof


def check_release() -> tuple[dict, Any]:
    """Đối soát FIN10 lịch sử, khóa riêng transport có delta đã kiểm cho FIN11."""
    lock, budget, resources = freeze(ROOT)
    receipt = read(ROOT, RECEIPT, True)
    historical_transport = sha256(git_blob(ROOT, PREVIOUS, TRANSPORT)).hexdigest()
    if historical_transport != receipt["lock"]["code_sha256"][TRANSPORT]:
        raise ValueError("Transport gốc khác FIN10")
    lock["code_sha256"][TRANSPORT] = historical_transport
    verify_record(receipt, lock)
    return {"version": VERSION, "org_slot": ORG, "spend_limit_usd": 0, "budget_sha256": digest(budget),
            "fin10": binding(ROOT, RECEIPT), "runner": binding(ROOT, SOURCE),
            "transport": binding(ROOT, TRANSPORT), "quota_runner": binding(ROOT, QUOTA_SOURCE),
            "point_reset": binding(ROOT, RESET_SOURCE)}, (budget, resources)


def historical_release(release: dict, version: int) -> dict:
    """Khôi phục đúng pin release cũ từ Git để kiểm journal đang dùng."""
    legacy = {key: release[key] for key in ("org_slot", "spend_limit_usd", "budget_sha256", "fin10")}
    legacy["version"] = f"finalize_hosted_study_v{version}"
    sources = {"runner": SOURCE} if version == 1 else {"runner": SOURCE, "transport": TRANSPORT, "quota_runner": QUOTA_SOURCE}
    for field, path in sources.items():
        raw = git_blob(ROOT, PREVIOUS if version == 1 else RELEASE_V2_COMMIT, path)
        legacy[field] = {"path": path, "bytes": len(raw), "sha256": sha256(raw).hexdigest()}
    return legacy


def release_for_grant(grant: dict, release: dict) -> dict:
    """Giữ digest grant gốc của journal; chỉ nhận đúng các bản đã khóa."""
    candidates = (release, historical_release(release, 1), historical_release(release, 2))
    if not any(all(grant.get(key) == value for key, value in version.items()) for version in candidates):
        raise ValueError("Mã nguồn hoặc ngân sách không khớp grant FIN11")
    return {"release": release, "grant_sha256": digest(grant), "operation": "MANUAL_ORG_DAILY_EXIT"}


def verify_operation(root: Path, release: dict, operation: dict) -> None:
    """Đối chiếu khóa vận hành v2/v3 và giữ hai manifest riêng."""
    for name, expected in (("release_v3.json", operation), ("release_v2.json", {**operation, "release": historical_release(release, 2)})):
        path = root/name
        if path.is_file() and load(path) != expected:
            raise ValueError("Release vận hành khác khóa FIN11")


def credential(org_slot: int = ORG) -> str:
    """Chỉ đọc key của org người vận hành đã chọn cho phiên này."""
    from dotenv import dotenv_values
    key = dotenv_values(ROOT/".env").get(f"GROQ_ORG_{org_slot}_API_KEY")
    if not key:
        raise ValueError("Thiếu credential của org đã khóa")
    return key


def account_grant(root: Path, grant: dict, slot: int) -> dict:
    """Đối soát đúng grant của org nguồn mà không cần đọc key cũ."""
    if type(slot) is not int or slot not in ORG_SLOTS:
        raise ValueError("Org nguồn của attempt ngoài phạm vi FIN11")
    if slot == ORG:
        return grant
    account = load(root/"accounts"/f"org-{slot}.json")
    if account["org_slot"] != slot or account["parent_grant_sha256"] != digest(grant):
        raise ValueError("Sổ quota org khác grant FIN11")
    return account


def bind_account(root: Path, grant: dict, slot: int, scope: str, archive: Archive) -> None:
    """Gắn key do tác giả chọn và giữ carry từ nguồn cục bộ của đúng org."""
    path = root/"accounts"/f"org-{slot}.json"
    if slot == ORG or path.exists():
        if account_grant(root, grant, slot)["credential_scope_sha256"] != scope:
            raise ValueError("Credential khác sổ quota đã khóa của org")
        return
    if any(scope == account_grant(root, grant, other)["credential_scope_sha256"]
           for other in ORG_SLOTS if other == ORG or (root/"accounts"/f"org-{other}.json").exists()):
        raise ValueError("Cùng một credential đã gắn vào org khác")
    now = time.time()
    observed = datetime.fromtimestamp(now, timezone.utc).isoformat()
    unknown = local_quota(ROOT, [], observed)["unattributed_24h_conservative"]
    models = {}
    for model, limit in MODEL_LIMITS.items():
        day = window([row for row in archive.carry if row.get("org") == slot and row.get("model") == model], now, 86400)
        models[model] = {"local_estimated_day_tokens_remaining": max(0, limit["tpd"]-day["tokens_charged_or_reserved"]
                                                                       -unknown["tokens_charged_or_reserved"]),
                         "local_estimated_day_requests_remaining": max(0, limit["rpd"]-day["requests"]-unknown["requests"])}
    save(path, {"org_slot": slot, "parent_grant_sha256": digest(grant), "credential_scope_sha256": scope,
                "balance": {"tier": "FREE", "remaining_tokens_24h": None,
                            "source": "OWNER_ATTESTED_GROQ_ALLOWED_MANUAL_ORG"},
                "local_quota": {"observed_at_utc": observed, "models": models}})


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


def run(*, resume_stopped: bool = False, org_slot: int = ORG) -> dict:
    """Smoke hoàn tất và đối soát trước nghiên cứu; giữ checkpoint khi tạm dừng."""
    grant = load(RUN/"grant.json")
    release, (budget, resources) = check_release()
    operation = release_for_grant(grant, release)
    with PriorRunLock(RUN/"worker", digest(grant)):
        verify_operation(RUN, release, operation)
        archived_resets(RUN, grant)
        write_new(RUN/"release_v3.json", json_bytes({"payload": operation, "sha256": digest(operation)}))
        key = credential(org_slot)
        scope = Quota(RUN/"credential.sqlite3").credential_scope(key)
        archive = Archive(ROOT)
        bind_account(RUN, grant, org_slot, scope, archive)
        if resume_stopped:
            (RUN/"stop.request").unlink(missing_ok=True)
        points, variants, _, _ = study(ROOT)
        provider = StudyProvider(resources, points, default_models(), variants)
        sender = GroqHTTP(key)

        def wait(phase: str, point: str, until: float) -> None:
            status("WAITING_QUOTA", phase=phase, point=point, org_slot=org_slot,
                   resume_at=datetime.fromtimestamp(until, timezone.utc).isoformat())
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
                status("RUNNING", phase=phase, org_slot=org_slot)
                runner = HostedStudyRunner(RUN, grant, budget, points, phase, provider, archive, sender, org_slot=org_slot)
                runner.collect(wait, guard_release)
                results[phase] = runner.seal_phase()
            return status("PASS_FIN11", phases=results)
        except DailyQuota as exhausted:
            return status("STOPPED_DAILY_QUOTA", phase=phase, org_slot=org_slot,
                          resume_at=datetime.fromtimestamp(exhausted.until, timezone.utc).isoformat())
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
    parser.add_argument("--org", type=int, choices=ORG_SLOTS, default=ORG, help="Chọn GROQ_ORG_<N>_API_KEY cho phiên thu")
    args = parser.parse_args()
    if args.mode == "authorize":
        if args.balance is None:
            parser.error("Cần --balance")
        result = authorize(args.balance)
    elif args.mode in {"run", "resume"}:
        import torch
        torch.set_num_threads(1)
        result = run(resume_stopped=args.mode == "resume", org_slot=args.org)
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
        if (RUN/"grant.json").is_file():
            grant = load(RUN/"grant.json")
            verify_operation(RUN, release, release_for_grant(grant, release))
        result = {"status": "READY_FOR_ACCOUNT_BALANCE", **release}
    print(json_bytes(result).decode())


if __name__ == "__main__":
    main()
