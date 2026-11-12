"""Đọc archive U09/U08 đã nghiệm thu; không kiểm nguồn hiện hành thay lịch sử F01."""
from __future__ import annotations

from collections import Counter
import csv
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
from typing import Any
import zipfile

DOC = "docs/plan/week12/"
PACKAGE = DOC + "unified_analysis_results.zip"
RESEARCH = DOC + "unified_live_research.zip"
SNAPSHOT = DOC + "final_evidence_snapshot.zip"
ACCEPTANCE = DOC + "unified_analysis_acceptance.json"
PINS = {
    PACKAGE: "e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9",
    RESEARCH: "5936bc971bebf1b139a34b93f154ad8e54d0a0e37fdaa6ac4673295f8b60a11c",
    SNAPSHOT: "80fed8c9a1c265098a394bfc40f13d7f0266c1e05abdb142fba01d873cb8b8b5",
    ACCEPTANCE: "6b435c21c89000775be1f1e1d043b6b3429a0729f37efc16f4bd03be92355456",
}
PREFIX = "outputs/unified_integration/u09_analysis_r1/"
METHODS = ("original_fix", "original_common", "bayesian_v1", "C2", "A_tp_pool",
    "B_semantic", "MT_BICL", "Fact_Anchor", "CASH_EVERY_CYCLE", "ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS")
EXTENSIONS = METHODS[2:7]
ENDPOINTS = ("account_return_percentage_points", "balanced_accuracy_percentage_points")


def require(condition: bool, message: str) -> None:
    """Fail-closed trước khi ghi artifact nếu sai hợp đồng hoặc lineage."""
    if not condition:
        raise ValueError(message)


def encoded(value: Any) -> bytes:
    """JSON UTF-8/LF xác định, giữ null và từ chối NaN/Infinity."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def semantic(value: Any) -> str:
    """Digest envelope đúng quy ước JSON compact của U08/U09."""
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def binding(raw: bytes) -> dict[str, Any]:
    """Length và SHA256 nguyên byte, không đổi newline trong archive."""
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def safe_name(name: str) -> str:
    """Chặn tên archive không portable, traversal, drive và ADS trên Windows."""
    path = PurePosixPath(name)
    require(bool(name) and not path.is_absolute() and path.as_posix() == name
        and ".." not in path.parts and "\\" not in name and ":" not in name
        and "\0" not in name and all(not part.endswith((" ", ".")) for part in path.parts),
        "Đường dẫn artifact không an toàn")
    return name


def decoded(raw: bytes) -> Any:
    """Kiểm dữ liệu hữu hạn, envelope và checksum trước khi dùng payload."""
    def reject(value: str) -> None:
        raise ValueError("JSON nguồn chứa số không hữu hạn")
    value = json.loads(raw, parse_constant=reject)
    if isinstance(value, dict) and set(value) == {"payload", "sha256"}:
        require(semantic(value["payload"]) == value["sha256"], "Envelope nguồn khác checksum")
        return value["payload"]
    return value


def members(archive: zipfile.ZipFile) -> dict[str, bytes]:
    """Kiểm tập member và mọi checksum, không giải nén hoặc thực thi Python từ ZIP."""
    names = archive.namelist()
    require(len(names) == len(set(names)), "Archive có member trùng")
    for name in names:
        safe_name(name)
    manifest = decoded(archive.read("manifest.json"))
    require(set(names) == set(manifest["members"]) | {"manifest.json"}, "Archive thiếu/thừa member")
    output = {}
    for name, expected in manifest["members"].items():
        raw = archive.read(name)
        require(binding(raw) == {k: expected[k] for k in ("bytes", "sha256")}, "Member đổi byte: " + name)
        output[name] = raw
    return output


def validate(result: dict[str, Any]) -> None:
    """Ràng support, mười vai trò, hai baseline và đủ 20 contrast/ba bridge."""
    require((result["status"], result["points"], result["repeats"], result["accounts_per_repeat"])
        == ("PASS_U09_ANALYSIS", 102, 3, 51), "Support U09 sai")
    require(tuple(row["method"] for row in result["summary"]) == METHODS, "Thiếu/trùng/sai thứ tự mười vai trò")
    for row in result["summary"]:
        require((row["n_points"], row["n_forecasts"], row["n_accounts_per_repeat"]) == (102, 306, 51),
            "Mẫu số summary sai")
        require(row["raw_decision_responses"] + row["bypass_forecasts"] == 306, "Raw/bypass không đủ slot")
    identities = [(endpoint, family, method, baseline) for endpoint in ENDPOINTS
        for family, baseline in (("system", "original_fix"), ("method", "original_common")) for method in EXTENSIONS]
    require([(r["endpoint"], r["family"], r["method"], r["baseline"]) for r in result["contrasts"]]
        == identities, "Contrast thiếu/trùng hoặc sai family/endpoint")
    joint = result["primary_joint_family"]
    require((joint["joint_family_size"], joint["draws"], joint["seed"], joint["block_length"])
        == (20, 10000, 20261110, 2), "Thiết kế joint family sai")
    require(len(joint["point"]) == 20 and (joint["ci95"] is None or len(joint["ci95"]) == 20), "Joint family sai chiều")
    for index, row in enumerate(result["contrasts"]):
        require(row["effect_pp"] == joint["point"][index], "Effect khác family đã khóa")
        bounds = joint["ci95"][index] if joint["ci95"] is not None else [None, None]
        require([row["band95_low_pp"], row["band95_high_pp"]] == bounds, "Band khác family đã khóa")
        require((bounds[0] is None) == (bounds[1] is None), "Band thiếu một endpoint")
        if bounds[0] is not None:
            require(bounds[0] <= row["effect_pp"] <= bounds[1], "Band không chứa point estimate")
    require([(r["method"], r["baseline"]) for r in result["bridge"]] ==
        [("original_common", "original_fix"), ("Fact_Anchor", "original_common"), ("MT_BICL", "Fact_Anchor")],
        "Bridge sai dependency")
    require({(r["method"], r["repeat"]) for r in result["per_repeat"]}
        == {(m, r) for m in METHODS for r in range(3)} and len(result["per_repeat"]) == 30, "Repeat thiếu/trùng")
    require(set(result["sensitivity"]) == {"BLOCK_LENGTH_1", "BLOCK_LENGTH_3", "CORE4_FIXED_SUBSET",
        "LEAVE_ONE_FOLD_OUT", "LEAVE_ONE_SYMBOL_OUT"}, "Thiếu sensitivity đã khóa")
    encoded(result)


def support(research: dict[str, bytes], predictions: bytes) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Chỉ đếm support/missingness từ shared slots, không tính lại nhãn hoặc metrics."""
    points = []
    for name, raw in research.items():
        if "/slots/" not in name:
            continue
        slot = decoded(raw)
        if not slot["slot"].startswith("shared/"):
            continue
        attempts = slot["attempts"]
        require(len(attempts) == 1 and attempts[0]["status"] == "complete", "Shared slot chưa complete")
        output = attempts[0]["output"]
        sentiment = output["payload"]["sentiment_data"]
        require(type(sentiment["is_unavailable"]) is bool, "Missing sentiment phải là bool đã ghi")
        points.append({**output["point"], "realization": output["realization"],
            "sentiment_unavailable": sentiment["is_unavailable"], "source_member": name})
    points.sort(key=lambda p: (p["cutoff"], p["symbol"]))
    require(len(points) == len({p["id"] for p in points}) == 102
        and {p["realization"] for p in points} == {0}, "Shared support sai")
    forecasts = list(csv.DictReader(io.StringIO(predictions.decode("utf-8"))))
    point_ids = {p["id"] for p in points}
    expected = {(p, m, str(r)) for p in point_ids for m in METHODS for r in range(3)}
    require(len(forecasts) == len(expected) and {(r["point_id"], r["method"], r["repeat"]) for r in forecasts}
        == expected, "Forecast support không đủ cả controls")
    groups = []
    for method in METHODS:
        for domain, symbols in (("CORE4", {"FPT", "MWG", "VCB", "VNM"}), ("OOD5", {"BHN", "CMG", "HVN", "MBB", "VJC"})):
            selected = [r for r in forecasts if r["method"] == method and r["symbol"] in symbols]
            values = [float(r["effective_K"]) for r in selected if r["effective_K"] != ""]
            require(all(math.isfinite(v) for v in values), "effective K không hữu hạn")
            groups.append({"method": method, "domain": domain, "points": len({r["point_id"] for r in selected}),
                "forecasts": len(selected), "raw_responses": sum(r["llm_response"] == "True" for r in selected),
                "bypass": sum(r["bypass"] == "True" for r in selected),
                "effective_K_defined": len(values), "effective_K_min": min(values) if values else None,
                "effective_K_max": max(values) if values else None,
                "reasons": dict(sorted(Counter(r["reason"] for r in selected).items()))})
    facts = {"points": len(points), "symbols": len({p["symbol"] for p in points}),
        "dates": len({p["cutoff"] for p in points}), "folds": len({p["fold"] for p in points}),
        "accounts": len({(p["symbol"], p["fold"]) for p in points}), "upstream_realizations": 1,
        "upstream_executions": len(points), "sentiment_missing": sum(p["sentiment_unavailable"] for p in points),
        "raw_decision_responses": sum(row["raw_responses"] for row in groups[:16]),
        "by_symbol": dict(sorted(Counter(p["symbol"] for p in points).items())), "domain_support": groups}
    return facts, points


def load(root: Path) -> dict[str, Any]:
    """Chỉ đọc archive đúng pin và receipt; source gate lịch sử được giữ trong F01."""
    for name, expected in PINS.items():
        with (root / name).open("rb") as stream:
            require(hashlib.file_digest(stream, "sha256").hexdigest() == expected, "Nguồn khác pin: " + name)
    acceptance = decoded((root / ACCEPTANCE).read_bytes())
    require(acceptance["status"] == "PASS_U09_ACCEPTANCE", "U09 chưa nghiệm thu")
    with zipfile.ZipFile(root / SNAPSHOT) as archive:
        historical = decoded(archive.read("evidence/f01_restore_smoke.json"))
        require(historical["status"] == "PASS_F01_HISTORICAL_RESTORE"
            and historical["u09_source_bindings"] == 729, "F01 thiếu source gate lịch sử")
    with zipfile.ZipFile(root / PACKAGE) as archive:
        analysis = members(archive)
    with zipfile.ZipFile(root / RESEARCH) as archive:
        research = members(archive)
    result = decoded(analysis[PREFIX + "results.json"])
    receipt = decoded(analysis[PREFIX + "receipt.json"])
    require(receipt["input_identity"] == result["input_identity"], "Identity kết quả khác receipt")
    require(semantic(receipt) == acceptance["analysis_receipt_sha256"], "Receipt khác acceptance")
    require(result["input_identity"]["u08_package_sha256"] == PINS[RESEARCH], "U08 identity sai")
    expected_artifacts = acceptance["cold_replay"]["artifacts"]
    require(receipt["artifacts"] == expected_artifacts and len(expected_artifacts) == 15, "Artifact thiếu/sai receipt")
    for name, expected in expected_artifacts.items():
        require(binding(analysis[PREFIX + name]) == expected, "Artifact sai acceptance: " + name)
    validate(result)
    facts, points = support(research, analysis[PREFIX + "predictions.csv"])
    for row in result["summary"]:
        selected = [r for r in facts["domain_support"] if r["method"] == row["method"]]
        require(sum(r["raw_responses"] for r in selected) == row["raw_decision_responses"]
            and sum(r["bypass"] for r in selected) == row["bypass_forecasts"], "Support raw/bypass khác summary")
    return {"result": result, "facts": facts, "points": points, "analysis": analysis,
        "input_bindings": {n: {"sha256": s, "bytes": (root / n).stat().st_size} for n, s in PINS.items()},
        "historical_source_commit": historical["source_commit"]}
