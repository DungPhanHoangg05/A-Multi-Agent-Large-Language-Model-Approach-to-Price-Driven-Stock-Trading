"""Khóa thiết kế và preflight offline; không cấp quyền thu hoặc mở payoff query."""
from __future__ import annotations

import ast
from collections import Counter
import csv
from importlib.metadata import version
import io
import json
from pathlib import Path, PurePosixPath
import platform
import subprocess
from typing import Any
import zipfile

from core.unified_contracts import day, digest
from core.variant_registry import execution_order, registry_document

DIRECTORY = "docs/plan/week12"
PROTOCOL = DIRECTORY + "/unified_comparison_protocol.json"
MANIFEST = DIRECTORY + "/unified_comparison_manifest.json"
DONOR = "9efd23f4157e0d3ab8069fccab7dccf03439a714"
BASE = "c0a4993fbd3214d32f0580109ad4ecfefd246fcb"
FIX = "outputs/historical_reevaluation/inputs/fix/"
BANK = FIX + "outputs/revision/r1_72h_bank_v2/manifest.json"
PRICE = FIX + "outputs/revision/r1_prices_v1/"
GRID = "outputs/historical_reevaluation/manifests/candidate_grid.json"
READINESS = "outputs/historical_reevaluation/manifests/asset_readiness.json"
PREVIOUS_QA = DIRECTORY + "/causal_common_profile_checks.zip"
PREVIOUS_SHA = "dbb07fa015c62833ef383088eb504a69b7cdebbcee9e9596aa219b279307a08d"
EXTENSIONS = ["bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL"]
BRANCHES = ["original_fix", "original_common", *EXTENSIONS, "Fact_Anchor"]
CORE4 = ["FPT", "MWG", "VCB", "VNM"]
DESIGN_SHA256 = "2d12701324e04f40c5513ca9f1541b9008546b38e9c02c44cd9dee8169548283"


def safe(root: Path, name: str) -> Path:
    """Không đọc credential, đường dẫn thoát repo hoặc symlink."""
    if type(name) is not str:
        raise ValueError("Đường dẫn protocol phải là chuỗi")
    rel = PurePosixPath(name)
    if (not name or rel.is_absolute() or ".." in rel.parts
            or "\\" in name or ":" in name or rel.as_posix() != name
            or any(p.startswith(".env") for p in rel.parts)):
        raise ValueError("Đường dẫn protocol không hợp lệ")
    path = root.joinpath(*rel.parts)
    if (not path.resolve().is_relative_to(root.resolve())
            or any(p.is_symlink() for p in (path, *path.parents))):
        raise ValueError("Nguồn protocol vượt repo hoặc qua symlink")
    return path


def binding(root: Path, name: str) -> dict[str, Any]:
    """Băm đúng byte checkout; nguồn donor còn phải khớp Git blob."""
    import hashlib
    raw = safe(root, name).read_bytes()
    return {"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def read(root: Path, name: str, envelope: bool = False) -> Any:
    """Envelope phải khớp; chưa thay cho việc neo nguồn Git."""
    value = json.loads(safe(root, name).read_bytes())
    if envelope:
        if type(value) is not dict or set(value) != {"payload", "sha256"} or digest(value["payload"]) != value["sha256"]:
            raise ValueError("Envelope protocol sai checksum")
        return value["payload"]
    return value


def git_blob(root: Path, commit: str, name: str) -> bytes:
    """Chỉ đọc blob được chỉ định, không checkout hoặc chạy source archive."""
    return subprocess.check_output(["git", "cat-file", "blob", commit + ":" + name], cwd=root)


def causal_config(root: Path) -> dict[str, Any]:
    """Đọc literal CONFIG bằng AST, không import alpha/model hay fit selector."""
    tree = ast.parse(safe(root, "core/causal_alpha.py").read_text(encoding="utf-8"))
    return ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
                                 and any(isinstance(t, ast.Name) and t.id == "CONFIG" for t in n.targets)))


def validate_protocol(value: dict[str, Any]) -> None:
    """Không nhận các lựa chọn ngoài thiết kế đã khóa trong schema v1."""
    # Pin thiết kế bằng code được review, không tin envelope đã được tự băm lại.
    if digest(value) != DESIGN_SHA256:
        raise ValueError("Thiết kế khác unified_comparison_protocol_v1; cần version/amendment mới")
    if set(execution_order(value["variants"])) != set(BRANCHES):
        raise ValueError("Thiếu baseline, extension hoặc dependency")


def ordered_branches(index: int) -> list[str]:
    """Xoay tail common theo DAG, chèn native lần lượt ở đủ tám vị trí."""
    if type(index) is not int or index < 0:
        raise ValueError("Chỉ số thứ tự không hợp lệ")
    tail = [*EXTENSIONS[:4], "Fact_Anchor", "MT_BICL"]
    shift = (index // 8) % len(tail)
    priority = tail[shift:] + tail[:shift]
    done: list[str] = ["original_common"]
    dependencies = {v["id"]: v["dependencies"] for v in registry_document()["variants"]}
    while len(done) < 7:
        done.append(next(v for v in priority if v not in done and all(d in done for d in dependencies[v])))
    done.insert(index % 8, "original_fix")
    return done


def cohort(grid: list[dict[str, Any]], bank: dict[str, Any], dates: dict[str, list[str]],
           offsets: dict[str, int], minimums: dict[str, int], pilot: list[dict]) -> tuple[list[dict], list[dict]]:
    """Chỉ chọn hai đầu test từ lịch donor; không dùng outcome hoặc coverage tin."""
    scopes, anchors = [], []
    pilot_ids = {r["id"] for r in pilot}
    projected = []
    donor_units = {r["id"]: (r["symbol"], r["fold"], r["date"]) for r in bank["units"]}
    if len(donor_units) != 102 or len(bank["schedule"]) != 51:
        raise ValueError("Donor không đủ 102 anchor/51 scope")
    for scope in bank["schedule"]:
        symbol, fold = scope["symbol"], scope["fold"]
        calendar = dates[symbol][offsets[symbol]:]
        first, last = scope["test"]
        train, validation = scope["train"], scope["validation"]
        if (type(first) is not int or last != first + 57 or first < 599 or last + 3 >= len(calendar)
                or not train or not validation or min(train) < 0
                or train != sorted(set(train)) or validation != sorted(set(validation))
                or max(train) + 3 >= min(validation) or max(validation) + 3 >= first):
            raise ValueError("Lịch donor sai warm-up, purge hoặc horizon")
        # Đây là trần support theo lịch; không giả rằng mọi factor đều có đủ dữ liệu.
        reasons = []
        if len(train) < minimums["min_train"]:
            reasons.append("ALPHA_TRAIN_CYCLE_CEILING_BELOW_MINIMUM")
        if len(validation) < minimums["min_validation"]:
            reasons.append("ALPHA_VALIDATION_CYCLE_CEILING_BELOW_MINIMUM")
        scopes.append({"symbol": symbol, "fold": fold, "train_indices": train,
            "validation_indices": validation, "test_indices": [first, last],
            "train_max_exit": calendar[max(train) + 3], "validation_start": calendar[min(validation)],
            "validation_max_exit": calendar[max(validation) + 3], "test_start": calendar[first],
            "test_end": calendar[last], "train_cycle_ceiling": len(train),
            "validation_cycle_ceiling": len(validation), "blockers": reasons})
        for index in range(first, last + 1, 3):
            row = {"id": f"{symbol}_{fold}_{index}", "symbol": symbol, "fold": fold,
                "suffix_decision_index": index, "raw_decision_index": index + offsets[symbol],
                "date": calendar[index], "entry_date": calendar[index + 1], "exit_date": calendar[index + 3],
                "core4": symbol in CORE4, "anchor": index in (first, last)}
            projected.append(row)
            if row["anchor"]:
                if donor_units.get(row["id"]) != (symbol, fold, row["date"]):
                    raise ValueError("Anchor ID/date khác manifest donor")
                anchors.append({**row, "runner_point_id": symbol + "-" + row["date"],
                    "exposure": ["DONOR_FIX_PREVIOUSLY_EVALUATED"] + (["PILOT48_SELECTED"] if row["id"] in pilot_ids else []),
                    "input_blockers": reasons, "collection_eligible": False})
    # Chỉ so field lịch/ID; field outcome chèn thêm vào grid không tham gia lựa chọn.
    keys = tuple(projected[0])
    if projected != [{k: r[k] for k in keys} for r in grid] or len(projected) != 1020:
        raise ValueError("Grid candidate khác lịch donor")
    anchors.sort(key=lambda r: (r["date"], r["symbol"], r["id"]))
    if len(anchors) != 102 or len({r["runner_point_id"] for r in anchors}) != 102:
        raise ValueError("Cohort trùng hoặc thiếu ID")
    previous: dict[tuple[str, str], str] = {}
    for row in anchors:
        key = row["symbol"], row["fold"]
        if key in previous and previous[key] >= row["entry_date"]:
            raise ValueError("Hai cycle trong tài khoản chồng lấn")
        previous[key] = row["exit_date"]
    return anchors, scopes


def call_budget(protocol: dict[str, Any], count: int) -> dict[str, Any]:
    """Đếm slot và trần attempt; không suy thời gian/quota hiện tại từ hạn mức cũ."""
    if type(count) is not int or count <= 0:
        raise ValueError("Cohort count không hợp lệ")
    repeats, realizations = protocol["repeats"], protocol["realizations"]
    decision = count * repeats * realizations * 8
    vision = count * realizations * 2
    smoke = protocol["budget"]["smoke_executions"]
    cap = protocol["budget"]["max_attempts_per_execution"]
    return {"planned_points": count, "decision_forecast_slots": decision, "new_vision_executions": vision,
        "new_shared_preparations": count * realizations, "smoke_executions": smoke,
        "nominal_http_upper_bound_including_smoke": decision + vision + smoke,
        "http_attempt_cap_including_repairs": cap * (decision + vision + smoke),
        "retry_additional_reserve": (cap - 1) * (decision + vision + smoke),
        "no_llm_controls": count * 2, "hosted_optional_panels": 0,
        "history_collection_calls": 0, "archive_decision_response_reuse": 0,
        "fallback_does_not_remove_forecast_slots": True,
        "live_model_availability_verified": False, "current_quota_verified": False,
        "token_reserve": None, "duration_hours": None, "spend_usd": None,
        "feasibility": "BLOCKED_UNMEASURED_QUOTA_PAYLOAD_AND_CARRY", "api": False}


def build(root: Path, protocol: dict[str, Any]) -> dict[str, Any]:
    """Đối soát local/Git và xuất manifest đầy đủ kể cả gate chưa đạt; không fit."""
    root = root.resolve()
    validate_protocol(protocol)
    sources: dict[str, dict] = {}
    def pin(name: str) -> bytes:
        result = binding(root, name)
        sources[name] = result
        return safe(root, name).read_bytes()
    def doc(name: str, envelope: bool = False) -> Any:
        raw = pin(name)
        if (name in (READINESS, GRID, "data_manager/regime_memory_store.manifest.json")
                or name.startswith("docs/plan/week11/")):
            if raw != git_blob(root, BASE, name):
                raise ValueError("Input/receipt lịch sử khác Git U05: " + name)
        return read(root, name, envelope)
    readiness = doc(READINESS)
    if readiness["donor_commit"] != DONOR:
        raise ValueError("Donor readiness khác mốc khóa")
    archived = readiness["source_archive"]
    if len(archived) != 21 or len({r["source_path"] for r in archived}) != 21:
        raise ValueError("Archive phải đủ 21 source donor")
    for row in archived:
        name = FIX + row["source_path"]
        raw = pin(name)
        if raw != git_blob(root, DONOR, row["source_path"]) or sources[name]["sha256"] != row["sha256"]:
            raise ValueError("Archive khác byte Git donor: " + name)
    bank, grid, prices = doc(BANK), doc(GRID), doc(PRICE + "manifest.json")
    calendars = {}
    for row in prices["symbols"]:
        raw = pin(PRICE + row["path"])
        if sources[PRICE + row["path"]]["sha256"] != row["sha256"]:
            raise ValueError("CSV khác manifest giá donor")
        # Chỉ đọc cột ngày; không tính nhãn/return hoặc chọn theo giá test.
        dates = [day(r["date"]) for r in csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))]
        if dates != sorted(set(dates)) or len(dates) != row["n_rows"]:
            raise ValueError("Lịch CSV không tăng duy nhất")
        calendars[row["symbol"]] = dates
    offsets = {s: v["excluded_prefix_rows"] for s, v in readiness["price_views"].items()}
    pilot = doc("docs/plan/week11/free_pilot_inputs.json", True)
    config = causal_config(root)
    anchors, scopes = cohort(grid, bank, calendars, offsets, config, pilot["units"])
    old_protocol = doc("docs/plan/week11/historical_evaluation_protocol.json", True)
    old_grant = doc("docs/plan/week11/historical_evaluation_release.json", True)
    if old_grant["status"] != "REVOKED" or old_grant["api"] is not False:
        raise ValueError("Grant full cũ phải giữ REVOKED/api=false")
    doc("docs/plan/week11/free_pilot_release.json", True)
    doc("docs/plan/week11/free_pilot_h07_acceptance.json", True)
    handoff = doc("docs/plan/week11/free_pilot_h09_handoff.json")
    bank_manifest = doc("data_manager/regime_memory_store.manifest.json")
    pin("data_manager/regime_memory_store.json")
    if sources["data_manager/regime_memory_store.json"]["sha256"] != bank_manifest["bank_sha256"]:
        raise ValueError("Bank khác manifest frozen")
    pin("data_manager/regime_model.json")
    model = doc("docs/plan/week11/mt_bicl_replica_full_r1_model.json", True)
    assets = []
    for base, members in model["artifact_trees"].items():
        for member, expected in members.items():
            name = base + "/" + member
            if safe(root, name).is_file():
                pin(name)
                if any(sources[name][key] != expected[key] for key in ("sha256", "bytes")):
                    raise ValueError("Frozen student/teacher khác release")
                status = "BYTES_VERIFIED_NOT_PROVIDER_CERTIFIED"
            else:
                status = "MISSING_LOCAL"
            assets.append({"path": name, "expected": expected, "status": status})
    regime = model["preprocessing"]["regime_models"]
    pin(regime["path"])
    if any(sources[regime["path"]][key] != regime[key] for key in ("sha256", "bytes")):
        raise ValueError("HMM prefix khác receipt model")
    # QA cũ chỉ làm mốc delta, không kế thừa kết quả cho source đã sửa.
    if binding(root, PREVIOUS_QA)["sha256"] != PREVIOUS_SHA:
        raise ValueError("QA U05 khác mốc")
    pin(PREVIOUS_QA)
    with zipfile.ZipFile(safe(root, PREVIOUS_QA)) as archive:
        runtime = json.loads(archive.read("runtime.json"))
        previous = json.loads(archive.read("source_bindings.json"))
    changed = []
    for name, expected in previous.items():
        pin(name)
        if sources[name] != expected:
            if name not in (".gitattributes", "README.md"):
                raise ValueError("Source runtime U05 đã đổi ngoài phạm vi protocol: " + name)
            changed.append(name)
    runtime_now = {"python": platform.python_version(),
        "packages": {name: version(name) for name in runtime["packages"]}}
    if runtime_now["python"] != "3.13.5" or runtime_now["packages"] != runtime["packages"]:
        raise ValueError("Runtime đã đổi so U05; cần delta và kiểm tra mới")
    for base in ("agents", "core", "data_manager", "scripts", "tests", "utils"):
        for path in sorted((root / base).rglob("*.py")):
            pin(path.relative_to(root).as_posix())
    for name in (".python-version", "requirements.txt", "requirements-unified.lock.txt", "default_config.py", PROTOCOL):
        pin(name)
    # Nguồn quota tối thiểu phải còn kể cả namespace mới; không suy đã hết hạn theo đồng hồ.
    quota_paths = [f"outputs/historical_reevaluation/{base}/org{i}.json"
                  for base in ("h06_smoke_r1/usage", "quota_history/cancelled_run_r1", "free_pilot_r1/usage")
                  for i in range(1, 6)]
    quota = []
    unique_requests: dict[tuple[int, str], dict] = {}
    for name in quota_paths:
        if safe(root, name).is_file():
            pin(name)
            requests = read(root, name)["requests"]
            org = int(Path(name).stem.removeprefix("org"))
            for row in requests:
                if (type(row["id"]) is not str or not row["id"] or type(row["started_at"]) not in (int, float)
                        or type(row["reserved_tokens"]) is not int or row["reserved_tokens"] < 0
                        or (row.get("total_tokens") is not None and
                            (type(row["total_tokens"]) is not int or row["total_tokens"] < 0))):
                    raise ValueError("Quota ledger thiếu UUID/time/token hợp lệ")
                key = org, row["id"]
                if key in unique_requests and any(unique_requests[key][k] != row[k]
                                                  for k in ("model", "started_at", "reserved_tokens")):
                    raise ValueError("Quota trùng request UUID nhưng khác identity/reserve")
                unique_requests[key] = row
            status = "PRESENT_DEDUPLICATED_NOT_CLEARED_FOR_NEW_RUN"
        else:
            requests = []
            status = "MISSING_LOCAL_DO_NOT_ASSUME_ZERO"
        quota.append({"path": name, "status": status, "request_rows": len(requests)})
    handoff_path = handoff["archive"]["path"]
    if safe(root, handoff_path).is_file():
        pin(handoff_path)
        if any(sources[handoff_path][k] != handoff["archive"][k] for k in ("sha256", "bytes")):
            raise ValueError("Handoff pilot48 khác receipt frozen")
    orders = []
    for i, point in enumerate(anchors):
        for u in range(protocol["realizations"]):
            for repeat in range(protocol["repeats"]):
                index = (i * protocol["realizations"] + u) * protocol["repeats"] + repeat
                orders.append({"point_id": point["runner_point_id"], "realization": u, "repeat": repeat,
                               "order": ordered_branches(index)})
    blockers = ["DONOR_SPLIT_INCOMPATIBLE_WITH_CAUSAL_COMMON_V1", "CAUSAL_SELECTORS_NOT_FITTED_OR_BOUND",
        "UNIFIED_PROVIDER_ASSET_PIT_ACCEPTANCE_PENDING", "COUNTERBALANCED_HOSTED_RUNNER_PENDING_U07_U08",
        "QUERY_NEWS_AVAILABILITY_AND_CONTENT_NOT_CERTIFIED", "BANK_QUERY_PROVENANCE_TRANSFER_AND_OOD_SUPPORT_PENDING",
        "QUOTA_MODEL_AVAILABILITY_AND_CARRY_NOT_RECONCILED", "U07_PAIRED_RECOVERY_NOT_ACCEPTED", "NEW_RELEASE_NOT_GRANTED"]
    return {"version": "unified_comparison_manifest_v1", "protocol_sha256": digest(protocol),
        "base_commit": BASE, "donor_commit": DONOR, "status": "DESIGN_LOCKED_RELEASE_BLOCKED",
        "authorization": protocol["authorization"], "input_profile": protocol["input_profile"],
        "source_bindings": dict(sorted(sources.items())), "runtime": runtime_now,
        "previous_gate_delta": {"bindings": len(previous), "unchanged": len(previous) - len(changed),
            "changed_documentation_attributes_only": changed, "full_previous_suite_rerun": False},
        "calendar_sha256": digest(calendars), "cohort_sha256": digest(anchors), "points": anchors,
        "scopes": scopes, "registry": registry_document(), "execution_orders": orders,
        "counts": {"planned": len(anchors), "calendar_verified": len(anchors), "collection_eligible": 0,
            "complete_new": 0, "failed_new": 0, "not_started": len(anchors), "scopes": len(scopes),
            "cutoff_dates": len({r["date"] for r in anchors}), "core4": sum(r["core4"] for r in anchors),
            "by_symbol": dict(sorted(Counter(r["symbol"] for r in anchors).items())),
            "pilot48_overlap": sum("PILOT48_SELECTED" in r["exposure"] for r in anchors)},
        "exposure": {"all_anchors_previously_evaluated": True, "fresh_test": False,
            "cancelled_full1020": "REVOKED_DO_NOT_RESUME; PREVIOUS_UPSTREAM_EXPOSURE_NOT_FULLY_ENUMERATED",
            "pilot48": "PREVIOUSLY_ANALYZED_NOT_NEW_TEST; NO_RESPONSE_REUSE",
            "handoff": handoff["archive"], "local_handoff_present": safe(root, handoff["archive"]["path"]).is_file(),
            "prospective": "REQUIRES_SEPARATE_FUTURE_FREEZE_UNIVERSE_POWER_AND_N"},
        "alpha_support": {"config": config, "basis": "DONOR_DISJOINT_CYCLE_SCHEDULE_CEILING_NOT_NUMERIC_FIT",
            "numeric_fit_performed": False, "compatible_scopes": sum(not s["blockers"] for s in scopes),
            "remedy": "NEW_VERSIONED_SPLIT_OR_PROFILE_BEFORE_INFERENCE; DO_NOT_LOWER_MINIMUM_OR_SILENTLY_WIDEN"},
        "assets": {"student_teacher": assets, "regime_model_binding": regime,
            "selection": "FROZEN_SEED42_STEP3000_NO_RESELECTION",
            "bank": {"by_symbol": bank_manifest["by_symbol"], "max_exit": bank_manifest["last_exit_date"],
                "status": "FROZEN852_DIFFERENT_SOURCE_NOT_CAUSAL_SIGNAL_CERTIFICATION"},
            "serving_candidate": old_protocol["inference"]["config"],
            "serving_status": "PINNED_HISTORICAL_CANDIDATE_NOT_LIVE_AVAILABILITY_OR_QUOTA_CERTIFICATION"},
        "quota_ledgers": quota,
        "quota_history": {"unique_org_request_ids": len(unique_requests),
            "charged_or_reserved_tokens": sum(r.get("total_tokens") or r["reserved_tokens"] for r in unique_requests.values()),
            "window_expiry_assumed": False, "fresh_provider_quota_verified": False,
            "scope": "FROZEN_REQUEST_HISTORY_DEDUP_BY_ORG_UUID_NOT_AVAILABLE_QUOTA"},
        "budget": call_budget(protocol, len(anchors)), "blockers": blockers,
        "native_rowwise_causal_gate": "FAIL", "whole_system_causal_gate": "PENDING_U06_U07",
        "query_payoffs_computed": False, "hosted_calls": 0, "market_models_fitted": False}


def seal(value: dict[str, Any]) -> dict[str, Any]:
    """Envelope máy, luôn giữ JSON nguyên bản và hữu hạn."""
    return {"payload": value, "sha256": digest(value)}


def verify(root: Path, protocol_path: str = PROTOCOL, manifest_path: str = MANIFEST) -> dict[str, Any]:
    """Tái dựng ở tiến trình mới; checksum tự ký không thể che thay đổi cohort/quyền."""
    protocol = read(root, protocol_path)
    validate_protocol(protocol)
    if protocol_path != PROTOCOL:
        raise ValueError("Protocol v1 phải ở đường dẫn đã khóa")
    recorded = read(root, manifest_path, True)
    if recorded != build(root, protocol):
        raise ValueError("Manifest khác preflight tái dựng; không cấp release")
    return {"status": "PASS_OFFLINE_PREFLIGHT", "release_status": recorded["status"],
        "manifest_sha256": digest(recorded), "counts": recorded["counts"], "budget": recorded["budget"],
        "blockers": recorded["blockers"], "api": False}
