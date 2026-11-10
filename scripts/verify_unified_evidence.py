"""Đối soát cây nguồn và byte bằng chứng với inventory U01, không gọi mạng."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = "docs/plan/week12/fix_develop_source_inventory.zip"
INVENTORY_SHA256 = "9f05fd92493ca74bbafe9ffb2a7412f99f84aa391d3e3ecaa7aaab8404fb3775"
FROZEN_CATEGORIES = frozenset(("frozen_evidence", "manuscript_source", "manuscript_asset_or_generated",
    "revision_documentation_or_evidence", "protocol_schema_receipt", "data_or_model_asset"))
# Develop đã thay GitHub Pages bằng Oracle VM; không tự bật lại workflow deploy.
RETIRED_PATHS = frozenset((".github/workflows/deploy.yml",))


def file_hash(path: Path) -> str:
    """Băm tuần tự để không nạp evidence lớn vào RAM."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_rows(root: Path, inventory: list[dict], index: dict[str, tuple[str, str]],
                retired_paths: frozenset[str] = frozenset()) -> dict[str, int]:
    """Chặn mất đường dẫn hoặc thay byte/mode/OID ở mọi artifact đã khóa."""
    checked, retired = 0, 0
    for row in inventory:
        path = row["path"]
        if path not in index:
            if path in retired_paths and row["category"] == "configuration_license_or_other":
                retired += 1
                continue
            raise ValueError("Mất đường dẫn nguồn U01: " + path)
        if row["category"] not in FROZEN_CATEGORIES:
            continue
        source = row["versions"].get("fix_frozen", row["versions"].get("develop"))
        if index[path] != (source["mode"], source["oid"]):
            raise ValueError("Index artifact khác nguồn U01: " + path)
        local = root / path
        if (local.is_symlink() or not local.resolve().is_relative_to(root.resolve()) or not local.is_file()
                or local.stat().st_size != source["bytes"] or file_hash(local) != source["sha256"]):
            raise ValueError("Byte artifact khác nguồn U01: " + path)
        checked += 1
    return {"source_paths_accounted": len(inventory), "source_paths_preserved": len(inventory) - retired,
            "source_paths_retired": retired, "frozen_artifacts_verified": checked}


def verify(root: Path = ROOT) -> dict[str, int]:
    """Neo inventory và cả index lẫn checkout; không nhận receipt tự băm lại."""
    bundle = root / INVENTORY
    if file_hash(bundle) != INVENTORY_SHA256:
        raise ValueError("Inventory U01 khác hash đã khóa")
    with zipfile.ZipFile(bundle) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        for name, expected in manifest["members"].items():
            raw = archive.read(name)
            if len(raw) != expected["bytes"] or hashlib.sha256(raw).hexdigest() != expected["sha256"]:
                raise ValueError("Thành viên inventory khác manifest: " + name)
        inventory = json.loads(archive.read("inventory.json"))
        summary = json.loads(archive.read("summary.json"))
    for row in inventory:
        if row["path"] in RETIRED_PATHS:
            raw = subprocess.check_output(["git", "show", summary["sources"]["fix_frozen"] + ":" + row["path"]], cwd=root)
            if hashlib.sha256(raw).hexdigest() != row["versions"]["fix_frozen"]["sha256"]:
                raise ValueError("Không khôi phục được nguồn workflow đã nghỉ")
    index = {}
    for line in subprocess.check_output(["git", "ls-files", "--stage", "-z"], cwd=root).split(b"\0"):
        if not line:
            continue
        header, path = line.split(b"\t", 1)
        mode, oid, stage = header.decode().split()
        if stage != "0":
            raise ValueError("Index vẫn còn conflict")
        index[path.decode()] = (mode, oid)
    return verify_rows(root, inventory, index, RETIRED_PATHS)


if __name__ == "__main__":
    print("PASS đối soát bằng chứng:", json.dumps(verify(), ensure_ascii=False, sort_keys=True))
