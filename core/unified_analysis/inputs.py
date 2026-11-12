"""Consumer chỉ đọc gói U08 đã nghiệm thu và kiểm closure nguồn/giá/runtime."""
from __future__ import annotations

import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
from typing import Any
import zipfile

import pandas as pd

from core.unified_contracts import digest
from core.unified_protocol import ordered_branches
from core.unified_analysis.statistics import VARIANTS

PACKAGE = "docs/plan/week12/unified_live_research.zip"
PACKAGE_SHA = "5936bc971bebf1b139a34b93f154ad8e54d0a0e37fdaa6ac4673295f8b60a11c"
PROTOCOL = "docs/plan/week12/unified_comparison_protocol_v2.json"
PREFIX = "outputs/unified_integration/u08_research_r1/"


def decoded(raw: bytes) -> Any:
    """Kiểm envelope gốc trước khi tiêu thụ payload."""
    value = json.loads(raw)
    if isinstance(value, dict) and set(value) == {"payload", "sha256"}:
        if digest(value["payload"]) != value["sha256"]: raise ValueError("Envelope khác checksum")
        return value["payload"]
    return value


def check_files(root: Path, bindings: dict[str, dict[str, Any]]) -> None:
    """Không đổi newline hoặc khôi phục file trong consumer phân tích."""
    for name, expected in bindings.items():
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()): raise ValueError("Binding thoát khỏi workspace")
        raw = path.read_bytes()
        if len(raw) != expected["bytes"] or hashlib.sha256(raw).hexdigest() != expected["sha256"]:
            raise ValueError("Nguồn/input khác snapshot đã khóa: " + name)


def validate_grid(points: list[dict], records: list[dict], outcomes: dict) -> None:
    """Không phân tích subset thành công hoặc một repeat được chọn theo kết quả."""
    expected = {(p["id"], r, v) for p in points for r in range(3) for v in VARIANTS}
    actual = [(r["forecast"]["point_id"], r["forecast"]["repeat"], r["forecast"]["variant"]) for r in records]
    if len(points) != 102 or len({p["id"] for p in points}) != 102 or len(actual) != len(expected) or set(actual) != expected:
        raise ValueError("Thiếu/trùng planned support 102×3×8")
    if set(outcomes) != {p["id"] for p in points}: raise ValueError("Outcome không đủ planned cohort")
    ids = [r["forecast"]["raw"]["source_request_id"] for r in records if r["forecast"]["raw"] is not None]
    if len(ids) != len(set(ids)): raise ValueError("Reuse raw response giữa slot/repeat")
    for record in records:
        if record["forecast"]["realization"] != 0 or record["policy"]["final_action"] not in ("LONG", "CASH"):
            raise ValueError("Realization hoặc action không hợp lệ")


def accept(root: Path) -> dict[str, Any]:
    """Hash closure thay gọi lại LLM/numeric provider; lấy đúng active generation đã seal."""
    raw = (root / PACKAGE).read_bytes()
    if hashlib.sha256(raw).hexdigest() != PACKAGE_SHA: raise ValueError("Gói U08 đã đổi")
    with zipfile.ZipFile(root / PACKAGE) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(manifest["members"]) | {"manifest.json"}:
            raise ValueError("Tập member U08 không khớp manifest")
        for name, binding in manifest["members"].items():
            content = archive.read(name)
            if len(content) != binding["bytes"] or hashlib.sha256(content).hexdigest() != binding["sha256"]:
                raise ValueError("Thành viên U08 đổi byte: " + name)
        sources = json.loads(archive.read("acceptance/u08_acceptance_sources.json"))
        check_files(root, sources)
        parent = decoded(archive.read("docs/plan/week12/unified_comparison_manifest_v2.json"))
        check_files(root, parent["asset_bindings"])
        if parent["runtime"] != {"python": platform.python_version(), "packages": {key: version(key) for key in parent["runtime"]["packages"]}}:
            raise ValueError("Runtime khác Python/107 package đã khóa")
        protocol = json.loads((root / PROTOCOL).read_bytes())
        if digest(protocol) != parent["protocol_sha256"]: raise ValueError("Protocol U06 v2 khác manifest")
        receipt = decoded(archive.read(PREFIX + "receipt.json"))
        if receipt != decoded(archive.read(PREFIX + "quota_receipt.json")) or receipt["status"] != "PASS_U08_RESEARCH":
            raise ValueError("U08 chưa seal đầy đủ")
        proof = json.loads(archive.read("acceptance/u08_acceptance.json"))
        if proof["status"] != "PASS_U08_ACCEPTANCE" or proof["receipt"] != receipt:
            raise ValueError("Thiếu cold acceptance U08")
        identity = decoded(archive.read(PREFIX + "identity.json"))["identity"]
        docs = {}
        for name in names:
            if name.startswith(PREFIX + "slots/"):
                document = decoded(archive.read(name))
                if document["slot"] in docs or document["signature"] != digest(identity): raise ValueError("Slot trùng hoặc khác identity")
                if len(document["attempts"]) != 1 or document["attempts"][0]["status"] != "complete": raise ValueError("Slot chưa complete")
                docs[document["slot"]] = document
        def output(slot: str) -> dict:
            return docs[slot]["attempts"][0]["output"]
        points = identity["points"]
        records, prepared, outcomes = [], {}, {}
        for index, point in enumerate(points):
            outcomes[point["id"]] = output("outcome/" + point["id"])
            for repeat in range(3):
                for variant in ordered_branches(index * 3 + repeat):
                    slot = f"forecast/{point['id']}/u0/r{repeat}/{variant}"
                    records.append(output(slot)); prepared[slot] = output("prepare/" + slot)
        validate_grid(points, records, outcomes)
        if digest(records) != receipt["records_sha256"] or digest(outcomes) != receipt["outcomes_sha256"]:
            raise ValueError("Dataset active không khớp receipt")
        wire = decoded(archive.read(PREFIX + "wire.json"))
        rows = [decoded(archive.read(PREFIX + "http/" + item["id"] + ".json")) for item in wire["rows"]]
        for row, binding in zip(rows, wire["rows"]):
            if digest(row) != binding["sha256"]: raise ValueError("Raw HTTP khác wire index")
        return {"protocol": protocol, "receipt": receipt, "proof": proof, "points": points, "records": records,
            "prepared": prepared, "outcomes": outcomes, "docs": docs, "http": rows,
            "retired": decoded(archive.read("docs/plan/week12/unified_slot_restart_runtime.json"))["plan"]["retired_http"],
            "input_identity": {"u08_package_sha256": PACKAGE_SHA, "records_sha256": receipt["records_sha256"],
                "outcomes_sha256": receipt["outcomes_sha256"], "protocol_sha256": digest(protocol),
                "source_pins": len(sources), "asset_pins": len(parent["asset_bindings"]), "runtime": parent["runtime"]}}


def frames(root: Path, bundle: dict[str, Any]) -> dict[str, pd.DataFrame]:
    """Đọc giá nghìn VND frozen; chỉ account helper chuyển VND, đối soát với label VND."""
    from core.backtest_engine import compute_round_trip_net_return
    result = {}
    for symbol in sorted({p["symbol"] for p in bundle["points"]}):
        path = root / "outputs/unified_integration/u06_assets_v2/prices" / (symbol + ".json")
        frame = pd.DataFrame(json.loads(path.read_bytes()))
        frame["Datetime"] = pd.to_datetime(frame["Datetime"])
        if frame["Datetime"].duplicated().any() or not frame["Datetime"].is_monotonic_increasing:
            raise ValueError("Giá có lịch trùng hoặc không tăng")
        result[symbol] = frame
        for point in (p for p in bundle["points"] if p["symbol"] == symbol):
            outcome = bundle["outcomes"][point["id"]]; target = outcome["target"]
            index = int(pd.DatetimeIndex(frame["Datetime"]).get_indexer([pd.Timestamp(point["cutoff"])])[0])
            if index < 0 or index + 3 >= len(frame): raise ValueError("Không đủ ba phiên thực thi")
            entry, exit_ = float(frame["Open"].iloc[index + 1]) * 1000., float(frame["Close"].iloc[index + 3]) * 1000.
            dates = frame["Datetime"].iloc[index:index+4].dt.strftime("%Y-%m-%d").tolist()
            if (dates != outcome["dates"] or entry != target["entry_open"] or exit_ != target["exit_close"]
                    or hashlib.sha256(path.read_bytes()).hexdigest() != outcome["source_sha256"]
                    or abs(float(compute_round_trip_net_return(entry, exit_)) - target["net_return"]) > 1e-12):
                raise ValueError("Label khác oracle/đơn vị/lịch nguồn giá")
    return result
