"""Đối chiếu raw U08 cùng logical slot; giữ riêng raw đã retire và UNKNOWN."""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from uuid import UUID

from core.historical_evaluation_journal import load
from core.unified_contracts import digest
from core.unified_execution import StageBook
from core.unified_protocol import binding, read

ARCHIVE = "outputs/unified_integration/u08_research_r1/"
INVENTORY = "docs/plan/week12/finalize_inventory.json"
RETIRED = "docs/plan/week12/unified_slot_restart_runtime.json"


def fingerprints(body: dict) -> dict[str, str]:
    """So riêng wire, nội dung văn bản, ảnh, schema và model/options/tier."""
    messages = deepcopy(body["messages"])
    images = []
    for message in messages:
        if isinstance(message["content"], list):
            for part in message["content"]:
                if part["type"] == "image_url":
                    images.append(part["image_url"])
                    part["image_url"] = None
    return {"wire": digest(body), "messages": digest(messages), "images": digest(images),
            "schema": digest(body.get("response_format")),
            "options": digest({k: v for k, v in body.items() if k not in ("messages", "response_format")})}


def match(current: dict | None, old: dict | None, *, parents_verified: bool,
          conditional: bool = False) -> tuple[str, str]:
    """Quyết định reuse trước thu; fixture không thể chuyển một slot thành REUSE."""
    if current is None:
        return "BYPASS", "POLICY_NO_REQUEST"
    if old is None:
        return "NEW", "ARCHIVE_NO_RAW_SAME_SLOT"
    if old["fingerprints"]["wire"] != current["wire"]:
        return "NEW", "FIXTURE_BODY_ONLY" if conditional else "WIRE_BYTES_CHANGED"
    if old["status"] == "UNKNOWN" and parents_verified and not conditional:
        return "UNKNOWN", "EXACT_ARCHIVE_ATTEMPT_UNRESOLVED"
    if conditional or not parents_verified:
        return "NEW", "PARENT_PROVENANCE_UNVERIFIED"
    if old["status"] != 200 or old["repair"]:
        return "NEW", "NO_UNREPAIRED_HTTP200"
    return "REUSE", "EXACT_WIRE_AND_PARENT_PROOF"


class Archive:
    """Chỉ đọc U08; verify wire index, attempt hashes, receipt và subset slot active."""
    def __init__(self, root: Path) -> None:
        self.directory = root / ARCHIVE
        self.receipt = load(self.directory / "receipt.json")
        index = read(root, INVENTORY, True)["receipt_index"]["U08"]
        if (self.receipt != index["receipt"] or self.receipt["status"] != "PASS_U08_RESEARCH"
                or binding(root, ARCHIVE + "wire.json")["sha256"] != self.receipt["wire_sha256"]):
            raise ValueError("Archive U08 khác receipt đã kiểm FIN01")
        self.identity = load(self.directory/"identity.json")["identity"]
        self.book = StageBook(self.directory, self.identity, verify_only=True)
        self.retired = read(root, RETIRED, True)["plan"]["retired_http"]
        wire = load(self.directory/"wire.json")
        if wire["identity"]["signature"] != digest(self.identity):
            raise ValueError("Wire và journal U08 khác identity")
        self.active: dict[str, list[dict]] = defaultdict(list)
        self.telemetry: dict[str, list[int]] = defaultdict(list)
        self.carry: list[dict] = list(wire["carry"])
        self.status: Counter = Counter()
        self.archive_unknowns: Counter = Counter()
        seen = set()
        for sequence, ref in enumerate(wire["rows"]):
            row = self.raw(ref["id"], ref["sha256"])
            if row["sequence"] != sequence or row["id"] in seen:
                raise ValueError("Wire U08 sai thứ tự hoặc trùng UUID")
            seen.add(row["id"])
            model, status, slot = row["body"]["model"], row["status"], row["slot"]
            retired = row["id"] in self.retired
            self.status[("retired" if retired else "active", str(status))] += 1
            if status == "UNKNOWN":
                self.archive_unknowns["retired" if retired else "active"] += 1
            self.carry.append({"id": row["id"], "model": model, "org": row["org"], "status": status,
                               "started_at": row["started_at"], "reserved_tokens": row["reserved_tokens"],
                               "total_tokens": row.get("total_tokens")})
            if retired:
                if self.retired[row["id"]] != ref["sha256"]:
                    raise ValueError("Raw retire khác hash đã khóa")
                continue
            if status == 200 and type(row.get("total_tokens")) is int:
                self.telemetry[slot.rsplit("/", 1)[-1]].append(row["total_tokens"])
            self.active[slot].append({"id": row["id"], "sha256": ref["sha256"], "status": status,
                                      "attempt": row["attempt"], "repair": row["repair"], "epoch": row["epoch"],
                                      "fingerprints": fingerprints(row["body"])})
        if (not self.retired.keys() <= seen or len(seen) != self.receipt["http_attempts"]
                or sum(len(rows) for rows in self.active.values()) != self.receipt["active_http_attempts"]):
            raise ValueError("Phạm vi archive U08 khác receipt")

    def raw(self, identifier: str, expected_sha256: str) -> dict:
        """Đọc đúng UUID/hash, không sao chép request thật ra ledger FIN09."""
        if str(UUID(identifier)) != identifier:
            raise ValueError("Raw UUID không canonical")
        row = load(self.directory/"http"/(identifier+".json"))
        if digest(row) != expected_sha256 or row["id"] != identifier:
            raise ValueError("Raw U08 khác wire index")
        return row

    def candidate(self, slot: str) -> dict | None:
        """Chỉ xét attempt cuối active của đúng role, point, realization và repeat."""
        rows = self.active.get(slot, ())
        return rows[-1] if rows else None

    def stage(self, slot: str) -> tuple[dict, dict]:
        """Cold read chart/forecast/preparation; không đọc journal outcome."""
        if slot.split("/", 1)[0] not in {"graph", "shared", "forecast", "prepare"}:
            raise ValueError("Slot ngoài phạm vi request FIN09")
        record = load(self.book.path(slot))
        value = self.book.execute(slot, record["inputs"], None)
        return record["attempts"][0], value
