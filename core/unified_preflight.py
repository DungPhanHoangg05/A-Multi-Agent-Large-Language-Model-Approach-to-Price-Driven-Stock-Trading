"""Nghiệm thu U06 offline: split/assets/quota có nguồn, không mở inference release."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from email.utils import parsedate_to_datetime
import hashlib
from importlib.metadata import version
import json
import math
from pathlib import Path
from typing import Any
import zipfile

from core.unified_contracts import digest, json_bytes
from core.unified_protocol import (BASE, MANIFEST, PROTOCOL, binding, build as legacy_build,
                                   git_blob, ordered_branches, read, safe, seal)

ASSETS = "outputs/unified_integration/u06_assets_v2"
PROTOCOL_V2 = "docs/plan/week12/unified_comparison_protocol_v2.json"
MANIFEST_V2 = "docs/plan/week12/unified_comparison_manifest_v2.json"
PACKAGE = "docs/plan/week12/unified_comparison_assets_v2.zip"
PARENT = "1c19513d908a083425436572e565e957fba752f1"
DESIGN_SHA256 = "02e620df1399835c0bec8bd0a99684384ba8ba43160319e32fec4240a3820cb3"
ASSET_SHA256 = "d5c4f1bc31c1a95d9e685a9cc13d1f86ce2d3cc0105b9023561fd5f567e2d8c4"
RESOURCE_INPUTS = ("docs/plan/week1/historical_task_record.schema.json",
    "docs/plan/week11/historical_evaluation_inputs.json", "docs/plan/week11/mt_bicl.schema.json",
    "docs/plan/week2/memory_bank_audit.json")


def validate_design(root: Path) -> dict[str, Any]:
    """Giữ v1 nguyên byte; v2 chỉ nhận thiết kế đã khai báo trước inference."""
    value = read(root, PROTOCOL_V2)
    if digest(value) != DESIGN_SHA256:
        raise ValueError("Thiết kế v2 khác hash đã khóa; cần amendment có version")
    for name in (PROTOCOL, MANIFEST, "docs/plan/week12/unified_comparison_checks.zip"):
        if safe(root, name).read_bytes() != git_blob(root, PARENT, name):
            raise ValueError("Bằng chứng U06 v1 bị đổi")
    if value["authorization"]["api"] or value["authorization"]["paid_api_allowed"]:
        raise ValueError("U06 không được mở quyền inference hoặc paid API")
    return value


def selected_paths(root: Path) -> list[str]:
    """Chỉ gói assets cuối; prototype có ledger riêng, không nhập vào provider hoặc forecast."""
    alpha = read(root, ASSETS + "/frozen_alpha_manifest.json")
    providers = read(root, ASSETS + "/provider_manifest.json")
    names = {ASSETS + "/" + n for n in ("frozen_alpha_manifest.json", "provider_manifest.json",
        "provider_metadata.json", "quota_attestation.json", "vision_probe.json", "news_manifest.json",
        "protocol_before_input_support_audit.json", "protocol_before_cross_fold_firewall.json")}
    for row in alpha["causal_sources"].values():
        names.update(row.values())
    for scope in alpha["scopes"]:
        names.update(row["projection"] for row in scope["queries"])
    names.update(row["path"] for row in providers["points"])
    names.update(p.relative_to(root).as_posix() for p in (root / ASSETS / "compatibility").rglob("*") if p.is_file())
    if any(not name.startswith(ASSETS + "/") for name in names):
        raise ValueError("Assets ra ngoài namespace mới")
    return sorted(names)


def package_assets(root: Path) -> dict[str, Any]:
    """Đóng gói nguyên byte nguồn mới để checkout khác có thể restore trước verify."""
    paths = selected_paths(root)
    members = {name: binding(root, name) for name in paths}
    manifest = {"version": "unified_comparison_assets_v2", "members": members,
                "scope": "NUMERIC_AND_CONTROL_ASSETS_ONLY_NOT_HOSTED_FORECASTS", "api": False}
    import io
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in [*paths, "assets_manifest.json"]:
            raw = json_bytes(manifest) if name == "assets_manifest.json" else safe(root, name).read_bytes()
            entry = zipfile.ZipInfo(name, (2026, 11, 10, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, raw)
    from core.unified_preflight_assets import write_new
    write_new(root / PACKAGE, output.getvalue())
    return {**binding(root, PACKAGE), "members": len(members) + 1}


def restore_assets(root: Path) -> dict[str, Any]:
    """Restore chỉ nhận đúng prefix/version/hash; không overwrite byte khác hoặc source cũ."""
    from core.unified_preflight_assets import write_new
    if binding(root, PACKAGE)["sha256"] != ASSET_SHA256:
        raise ValueError("Gói assets khác hash pin trong code v2")
    with zipfile.ZipFile(safe(root, PACKAGE)) as archive:
        manifest = json.loads(archive.read("assets_manifest.json"))
        if manifest["version"] != "unified_comparison_assets_v2" or manifest["api"] is not False:
            raise ValueError("Sai phiên bản gói assets")
        if len(archive.namelist()) != len(set(archive.namelist())) or set(archive.namelist()) != set(manifest["members"]) | {"assets_manifest.json"}:
            raise ValueError("Gói assets có thành viên thừa/trùng")
        for name, expected in manifest["members"].items():
            if not name.startswith(ASSETS + "/"):
                raise ValueError("Gói assets chứa đường dẫn ngoài namespace")
            path = safe(root, name)
            raw = archive.read(name)
            if len(raw) != expected["bytes"] or hashlib.sha256(raw).hexdigest() != expected["sha256"]:
                raise ValueError("Thành viên gói assets khác hash")
            write_new(path, raw)
    return {"status": "RESTORED_EXACT_ASSETS", "members": len(manifest["members"]), "api": False}


def pooled_schedule(history: dict[int, list[dict]], tasks: list[dict], start: float,
                    limits: dict[str, int], latency: float = 5.) -> dict[str, Any]:
    """Lập lịch bảo thủ gộp cả hai model mỗi org; không nhân quota theo key/model."""
    if not math.isfinite(start) or latency < 0 or any(limits[k] < 1 for k in ("rpm", "rpd", "tpm", "tpd")):
        raise ValueError("Quota hoặc thời điểm lập lịch không hợp lệ")
    rows = deepcopy(history)
    clocks = {org: start for org in rows}
    for task in tasks:
        org, tokens = task["org"], task["tokens"]
        now = clocks[org]
        if type(tokens) is not int or not 0 < tokens <= limits["tpm"] or tokens > limits["tpd"]:
            raise ValueError("Một request vượt quota admission")
        while True:
            daily = [row for row in rows[org] if row["started_at"] > now - 86400]
            minute = [row for row in daily if row["started_at"] > now - 61]
            charged = sum(row.get("total_tokens") or row["reserved_tokens"] for row in daily)
            if len(daily) + 1 > limits["rpd"] or charged + tokens > limits["tpd"]:
                now = min(row["started_at"] for row in daily) + 86400.01
                continue
            if len(minute) + 1 > limits["rpm"] or sum(row["reserved_tokens"] for row in minute) + tokens > limits["tpm"]:
                now = min(row["started_at"] for row in minute) + 61.01
                continue
            break
        rows[org].append({"started_at": now, "reserved_tokens": tokens})
        clocks[org] = now + latency
    return {"executions": len(tasks), "reserved_tokens": sum(row["tokens"] for row in tasks),
        "hours_with_latency_scenario": (max(clocks.values()) - start) / 3600., "assumed_latency_seconds": latency,
        "scope": "DETERMINISTIC_QUOTA_SCENARIO_NOT_COMPLETION_GUARANTEE"}


def budget(root: Path, baseline: dict, providers: dict) -> dict[str, Any]:
    """Khóa scenario đầy đủ3 repeats, carry và trần attempt; hạn mức là attestation hiện tại."""
    attest = read(root, ASSETS + "/quota_attestation.json")
    metadata = read(root, ASSETS + "/provider_metadata.json")
    if (attest["organizations_independent"] != 5 or attest["plan"] != "FREE" or attest["split_limits"]
            or attest["paid_api_allowed"] or attest["inference_release"] or metadata["inference_requests"] != 0
            or not metadata["all_required_models_listed"] or len({r["credential_hmac"] for r in metadata["rows"]}) != 5
            or any(model["active"] is not True for row in metadata["rows"] for model in row["model_catalog"].values())):
        raise ValueError("Thiếu xác nhận quota/catalog hoặc có quyền thu ngầm")
    limits = {k: attest["limits"]["openai/gpt-oss-20b"][k] for k in ("rpm", "rpd", "tpm", "tpd")}
    history: dict[int, dict[str, dict]] = {i: {} for i in range(1, 6)}
    for item in baseline["quota_ledgers"]:
        org = int(Path(item["path"]).stem.removeprefix("org"))
        for row in read(root, item["path"])["requests"]:
            history[org][row["id"]] = row
    rows = {org: list(values.values()) for org, values in history.items()}
    start = parsedate_to_datetime(metadata["rows"][-1]["rate_headers"]["date"]).timestamp()
    vision = read(root, ASSETS + "/vision_probe.json")["reserves"]
    decision = max(4500, providers["max_control_request_reserve"])
    if len(vision) != 2 or max([decision, *vision]) > limits["tpm"]:
        raise ValueError("Payload thực vượt quota TPM đã xác nhận")
    tasks = [{"org": 1, "tokens": value} for value in [*vision, *([decision] * 8)]]
    for i, _ in enumerate(baseline["points"]):
        org = 1 + i % 5
        tasks.extend({"org": org, "tokens": value} for value in [*vision, *([decision] * 24)])
    nominal = pooled_schedule(rows, tasks, start, limits)
    worst_tasks = [{"org": row["org"], "tokens": limits["tpm"]} for row in tasks for _ in range(3)]
    worst = pooled_schedule(rows, worst_tasks, start, limits)
    return {**baseline["budget"], "current_quota_verified": True,
        "quota_evidence_grade": "CURRENT_USER_ATTESTATION_PLUS_AUTHENTICATED_CATALOG_NOT_PROVIDER_ORG_IDS",
        "live_model_availability_verified": True, "metadata_get_requests": 5, "inference_http_calls": 0,
        "decision_reserve_tokens_measured_control": decision, "vision_reserve_tokens_measured": vision,
        "per_request_hard_admission_token_cap": 8000, "token_reserve": worst["reserved_tokens"],
        "spend_usd": 0, "duration_hours": None, "feasibility": "PASS_PACED_FREE_SCENARIO_NO_DEADLINE_PROMISE",
        "nominal_scenario": nominal, "all_attempts_max_admission_scenario": worst,
        "quota_pooling": "BOTH_MODELS_SHARE_ORG_TPM_TPD_RPM_RPD_CONSERVATIVE",
        "dispatch": "FIVE_INDEPENDENT_ORG_QUEUES; POINTS_IN_FIXED_CALENDAR_PRIORITY_WITHIN_QUEUE; SAME_POINT_DAG_SERIAL",
        "quota_history": baseline["quota_history"], "as_of_server_date": metadata["rows"][-1]["rate_headers"]["date"],
        "other_concurrent_usage": "NOT_ASSUMED_ABSENT; RECONCILE_HEADERS_BEFORE_EACH_ADMISSION_IN_U08",
        "release_revalidation_required": True, "api": False}


def build(root: Path) -> dict[str, Any]:
    """Một manifest đủ nguồn U06; execution vẫn chờ U07/U08 và không nhận causal toàn hệ."""
    root = root.resolve()
    protocol = validate_design(root)
    baseline = legacy_build(root, read(root, PROTOCOL))
    alpha = read(root, ASSETS + "/frozen_alpha_manifest.json")
    providers = read(root, ASSETS + "/provider_manifest.json")
    planned = {p["runner_point_id"] for p in baseline["points"]}
    if (len(alpha["causal_sources"]) != 51 or len(providers["points"]) != 102
            or {row["point_id"] for row in providers["points"]} != planned
            or any(s["train_cycles"] < 60 or s["validation_common_cycles"] < 30 for s in alpha["scopes"])):
        raise ValueError("Không đủ nguồn cho toàn bộ planned cohort")
    for scope in alpha["scopes"]:
        p = scope["schedule"]
        if not p["train_end"] < p["validation_start"] < p["validation_end"] < p["test_start"]:
            raise ValueError("Split overlap")
    sources = deepcopy(baseline["source_bindings"])
    for name in (PROTOCOL_V2, MANIFEST, "docs/plan/week12/unified_comparison_checks.zip", "outputs/unified_integration/.gitignore", *RESOURCE_INPUTS):
        sources[name] = binding(root, name)
    for directory in ("outputs/historical_reevaluation/h02_data_r1", "data/execution_prices"):
        for path in sorted((root / directory).rglob("*")):
            if path.is_file():
                name = path.relative_to(root).as_posix()
                if path.read_bytes() != git_blob(root, BASE, name):
                    raise ValueError("Nguồn raw/events ngoài Git đã khóa")
                sources[name] = binding(root, name)
    artifacts = {name: binding(root, name) for name in selected_paths(root)}
    package = binding(root, PACKAGE)
    if package["sha256"] != ASSET_SHA256:
        raise ValueError("Asset package khác hash v2 đã khóa")
    with zipfile.ZipFile(root / PACKAGE) as archive:
        member_manifest = json.loads(archive.read("assets_manifest.json"))
        if member_manifest["members"] != artifacts:
            raise ValueError("Asset package khác nguồn đã chuẩn bị")
        if len(archive.namelist()) != len(artifacts) + 1:
            raise ValueError("Asset package thiếu/thừa member")
        for name, expected in artifacts.items():
            raw = archive.read(name)
            if hashlib.sha256(raw).hexdigest() != expected["sha256"] or len(raw) != expected["bytes"]:
                raise ValueError("Asset package member khác checksum")
    previous = read(root, MANIFEST, True)["source_bindings"]
    changed = [name for name, expected in previous.items() if binding(root, name) != expected]
    if set(changed) - {".gitattributes", "README.md", "tests/test_unified_protocol.py"}:
        raise ValueError("Nguồn nền U06 v1 đổi ngoài phạm vi amendment")
    return {"version": "unified_comparison_manifest_v2", "status": "U06_COMPLETE_OFFLINE_INPUTS_READY",
        "base_commit": PARENT, "donor_commit": baseline["donor_commit"], "protocol_sha256": digest(protocol),
        "parent_manifest": binding(root, MANIFEST), "authorization": protocol["authorization"],
        "source_bindings": dict(sorted(sources.items())), "asset_bindings": artifacts,
        "asset_package": {**package, "members": len(artifacts) + 1}, "runtime": baseline["runtime"],
        "cohort_calendar_sha256": baseline["calendar_sha256"], "cohort_ids": sorted(planned),
        "counts": {**baseline["counts"], "input_eligible": 102, "collection_eligible": 0,
                   "selectors": 51, "unique_symbol_selectors": 9, "query_projections": 102, "provider_controls": 102},
        "alpha_support": alpha, "provider_support": providers, "budget": budget(root, baseline, providers),
        "resource_contract_profile": protocol["resources"]["contract_profile"],
        "execution_orders": baseline["execution_orders"], "estimand_and_inference": protocol["statistics"],
        "exposure": {**baseline["exposure"], "prototype_expanding_alpha_computed_prior_fold_query_labels": True,
            "prototype_assets_used_in_final_study": False,
            "design_selected_using_test_payoffs": False}, "previous_gate_delta": {"previous_bindings": len(previous),
            "unchanged": len(previous) - len(changed), "changed": changed},
        "native_rowwise_causal_gate": "FAIL", "whole_system_causal_gate": "NOT_CERTIFIED_HISTORICAL_EXPLORATORY",
        "execution_release": "PENDING_U07_PAIRED_RECOVERY_AND_NEW_U08_GRANT",
        "remaining_execution_gates": ["U07_NINE_SYMBOL_SCOPE_AND_PAIRED_RECOVERY_ACCEPTANCE",
            "U08_FRESH_QUOTA_HEADERS_AND_TRANSPORT_SMOKE", "U08_NEW_EXPLICIT_RELEASE"],
        "quality_limits": ["EXPOSED_HISTORICAL_COHORT", "NEWS_CONTENT_PIT_NOT_CERTIFIED",
            "NATIVE_ROWWISE_CAUSAL_FAIL", "BANK_QUERY_SOURCE_TRANSFER", "VENDOR_SERIES_LIMITED_NO_FILL_CERTIFICATION",
            "QUOTA_ORG_IDS_USER_ATTESTED_NOT_PROVIDER_VERIFIED", "CONTROL_REQUESTS_ARE_NOT_HOSTED_FORECASTS"],
        "inference_http_calls": 0, "metadata_get_calls": 5, "numeric_selector_fit": True,
        "student_teacher_hmm_training": False, "final_assets_cohort_query_canonical_outcomes_computed": False}


def verify(root: Path) -> dict[str, Any]:
    """Cold verify hash và tái dựng preflight thuần; không model/client/network hoặc credential."""
    recorded = read(root, MANIFEST_V2, True)
    expected = build(root)
    if recorded != expected:
        raise ValueError("Manifest v2 khác nguồn/preflight tái dựng")
    return {"status": "PASS_U06_OFFLINE_PREFLIGHT", "manifest_sha256": digest(recorded),
        "input_eligible": recorded["counts"]["input_eligible"], "selectors": 51,
        "source_bindings": len(recorded["source_bindings"]), "asset_members": recorded["asset_package"]["members"],
        "execution_release": recorded["execution_release"], "api": False}
