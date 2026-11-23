"""Intent durable theo slot, resume không gọi lại complete/unknown và label barrier."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from core.bayesian_memory import atomic_write_json
from core.historical_evaluation_protocol import digest
from core.prior_run_lock import safe_path, utc_now
from core.prior_stage_journal import encode_output, decode_output


def load(path: Path) -> dict[str, Any]:
    """Kiểm JSON/envelope trước khi tin trạng thái hoặc output."""
    from core.bayesian_memory import read_json
    record = read_json(path)
    if set(record) != {"payload", "sha256"} or digest(record["payload"]) != record["sha256"]:
        raise ValueError("Journal sai envelope")
    return record["payload"]


def save(path: Path, payload: dict[str, Any]) -> None:
    """Ghi atomic/fsync qua primitive đã kiểm trên Windows."""
    atomic_write_json(path, {"payload": payload, "sha256": digest(payload)})


class RunBook:
    """Một slot khoa học độc lập với retry HTTP; UUID và identity không đổi khi resume."""

    def __init__(self, directory: Path, identity: dict[str, Any], *, verify_only: bool = False) -> None:
        """Không tạo file trong verify; identity khác cần namespace riêng."""
        self.directory, self.verify_only = directory.resolve(), verify_only
        self.signature = digest(identity)
        path = safe_path(self.directory, "identity.json")
        if path.exists():
            doc = load(path)
            if doc["identity"] != identity or doc["signature"] != self.signature:
                raise ValueError("Run khác source/protocol/model/fixture identity")
            self.uuid = doc["run_uuid"]
        elif verify_only:
            raise ValueError("Thiếu identity run")
        else:
            self.uuid = str(uuid4())
            save(path, {"identity": identity, "signature": self.signature, "run_uuid": self.uuid})

    def path(self, slot: str) -> Path:
        """Slot không trở thành đường dẫn tùy ý từ unit/branch bên ngoài."""
        return safe_path(self.directory, "slots/" + digest(slot) + ".json")

    def execute(self, slot: str, inputs: dict[str, Any], function: Callable[[str], dict[str, Any]],
                *, validate: Callable[[dict[str, Any]], None] | None = None) -> dict[str, Any]:
        """Lưu UNKNOWN trước call; exception/crash giữ nguyên UUID và không tự replay."""
        path = self.path(slot)
        expected = {"signature": self.signature, "run_uuid": self.uuid, "slot": slot,
                    "inputs_sha256": digest(inputs)}
        if path.exists():
            doc = load(path)
            if any(doc.get(k) != v for k, v in expected.items()) or doc.get("inputs") != inputs:
                raise ValueError("Slot khác nguồn/parent/payload đã durable")
            last = doc["attempts"][-1]
            if last["status"] == "complete":
                if last["output_sha256"] != digest(last["output"]):
                    raise ValueError("Output complete khác hash")
                output = decode_output(last["output"])
                if validate:
                    validate(output)
                return deepcopy(output)
            if last["status"] != "unknown" or last.get("authorization") is None:
                raise ValueError("UNKNOWN cần reconcile UUID: " + last["attempt_id"])
        else:
            if self.verify_only:
                raise ValueError("Chưa có slot durable: " + slot)
            doc = {**expected, "inputs": deepcopy(inputs), "attempts": []}
        if self.verify_only:
            raise ValueError("Slot chưa complete: " + slot)
        attempt = {"attempt_id": str(uuid4()), "started_at": utc_now(), "status": "unknown",
                   "output": None, "output_sha256": None, "authorization": None}
        doc["attempts"].append(attempt)
        save(path, doc)
        output = function(attempt["attempt_id"])
        if validate:
            validate(output)
        encoded = encode_output(output)
        attempt.update(status="complete", output=encoded, output_sha256=digest(encoded))
        save(path, doc)
        return deepcopy(output)

    def complete(self, slot: str) -> bool:
        """Không coi unknown, file lỗi hoặc output thiếu hash là forecast."""
        path = self.path(slot)
        if not path.exists():
            return False
        doc = load(path)
        if doc["signature"] != self.signature or doc["run_uuid"] != self.uuid or doc["slot"] != slot:
            raise ValueError("Slot có identity sai")
        last = doc["attempts"][-1]
        if last["status"] != "complete":
            return False
        if last["output_sha256"] != digest(last["output"]):
            raise ValueError("Output complete sai checksum")
        return True

    def reconcile(self, attempt_id: str, reason: str) -> None:
        """Chỉ authorise UUID unknown cuối đã xác định, giữ lịch sử và lý do."""
        if self.verify_only or not reason.strip() or len(reason) > 1000:
            raise ValueError("Reconcile cần lý do hợp lệ và run ghi được")
        matches = []
        for path in (self.directory / "slots").glob("*.json"):
            doc = load(path)
            if doc["signature"] != self.signature:
                raise ValueError("Slot khác run khi reconcile")
            last = doc["attempts"][-1]
            if last["attempt_id"] == attempt_id:
                if last["status"] != "unknown" or last.get("authorization") is not None:
                    raise ValueError("Không replay complete hoặc UUID đã authorise")
                matches.append((path, doc))
        if len(matches) != 1:
            raise ValueError("UUID unknown không duy nhất trong run")
        path, doc = matches[0]
        doc["attempts"][-1]["authorization"] = {"at": utc_now(), "reason": reason.strip()}
        save(path, doc)
