"""Đóng gói và phục hồi bằng chứng pilot48; chỉ dùng filesystem và Git local."""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import distributions
import json
from pathlib import Path, PurePosixPath
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PILOT = Path("outputs/historical_reevaluation/free_pilot_r1")
HANDOFF = PILOT / "handoff"
ARCHIVE = HANDOFF / "pilot48_evidence.zip"
RECEIPT = Path("docs/plan/week11/free_pilot_h09_handoff.json")
MANIFEST = "handoff_manifest.json"
DONOR = "9efd23f4157e0d3ab8069fccab7dccf03439a714"
BASE = "ae5dbc6d60e3d1e3dccfa36773b7e2877e4da763"
LOCAL_DIRS = (PILOT, Path("outputs/historical_reevaluation/h04_assets/legacy_regimes"),
              Path("outputs/historical_reevaluation/h06_smoke_r1"),
              Path("outputs/historical_reevaluation/quota_history"),
              Path("outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/inputs"),
              Path("outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/model"))


def encoded(value: object) -> bytes:
    """JSON ổn định, không phụ thuộc newline của checkout."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    """Băm byte gốc, không chuẩn hóa bằng chứng đã khóa."""
    return hashlib.sha256(raw).hexdigest()


def safe_name(name: str) -> str:
    """Từ chối path traversal, đường dẫn Windows và file credential."""
    path = PurePosixPath(name)
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
                *(f"LPT{i}" for i in range(1, 10))}
    if (not name or path.is_absolute() or str(path) != name or "\\" in name or ":" in name
            or any(p == ".." or p.lower() == ".git" or (p.lower().startswith(".env") and p != ".env.example") or p != p.rstrip(" .")
                   or any(c in '<>"|?*' or ord(c) < 32 for c in p)
                   or p.split(".")[0].upper() in reserved for p in path.parts)):
        raise ValueError("Đường dẫn gói không hợp lệ: " + name)
    return name


def git(root: Path, *args: str, data: bytes | None = None) -> bytes:
    """Chỉ gọi Git local, không fetch, push hoặc đọc credential."""
    return subprocess.check_output(["git", "-c", "core.longpaths=true", *args], cwd=root, input=data)


def envelope(path: Path) -> dict:
    """Đối soát checksum của receipt nguồn trước khi tin kết quả PASS."""
    value = json.loads(path.read_bytes())
    digest = sha(json.dumps(value["payload"], ensure_ascii=False, sort_keys=True,
                            separators=(",", ":"), allow_nan=False).encode())
    if set(value) != {"payload", "sha256"} or digest != value["sha256"]:
        raise ValueError("Receipt sai checksum: " + str(path))
    return value["payload"]


def verify_bindings(root: Path, value: object) -> None:
    """Không dùng gate cũ nếu source hoặc artifact đã đổi byte."""
    if isinstance(value, dict):
        if {"path", "bytes", "sha256"} <= value.keys():
            raw = (root / safe_name(value["path"])).read_bytes()
            if len(raw) != value["bytes"] or sha(raw) != value["sha256"]:
                raise ValueError("Binding khác receipt: " + value["path"])
        for item in value.values():
            verify_bindings(root, item)
    elif isinstance(value, list):
        for item in value:
            verify_bindings(root, item)


def git_snapshots(root: Path) -> tuple[bytes, dict[str, str]]:
    """Giữ commit/tree và đúng blob consumer đọc; bỏ lịch sử/blob không liên quan."""
    heads = {"HEAD": git(root, "rev-parse", "HEAD").decode().strip(), "donor": DONOR, "adapter": BASE}
    donor_root = root / "outputs/historical_reevaluation/inputs/fix"
    donor_paths = {p.relative_to(donor_root).as_posix() for p in donor_root.rglob("*") if p.is_file()}
    donor_paths.add("outputs/revision/final_baselines_v1/main_comparison.csv")
    head_paths = {f"docs/plan/week11/free_pilot_{name}.json"
                  for name in ("protocol", "inputs", "runtime", "audit", "manager", "release")}
    head_paths.update(f"docs/plan/week11/{name}.json" for name in
                      ("historical_evaluation_protocol", "historical_evaluation_inputs", "mt_bicl_replica_full_r1_model"))
    objects = set(heads.values())
    for commit in sorted(objects.copy()):
        objects.add(git(root, "rev-parse", commit + "^{tree}").decode().strip())
        for row in git(root, "ls-tree", "-r", "-t", "-z", commit).split(b"\0"):
            if row:
                metadata, name = row.split(b"\t", 1)
                path = safe_name(name.decode("utf-8"))
                _, kind, oid = metadata.decode().split()
                if (kind == "tree" or (commit == heads["HEAD"] and path in head_paths)
                        or (commit == DONOR and path in donor_paths)
                        or (commit == BASE and path.startswith("core/") and path.endswith(".py"))):
                    objects.add(oid)
    packed = git(root, "pack-objects", "--stdout", "--threads=1",
                 data=("\n".join(sorted(objects)) + "\n").encode())
    return packed, heads


def build(root: Path, archive: Path) -> dict:
    """Khóa manifest toàn bộ thành viên; không lấy .env hoặc khóa OS từ máy gốc."""
    h07 = envelope(root / "docs/plan/week11/free_pilot_h07_acceptance.json")
    h08 = envelope(root / "docs/plan/week11/free_pilot_h08_analysis.json")
    if h07["status"] != "PASS" or h08["status"] != "H08_PASS" or h07["run_uuid"] != h08["run_uuid"]:
        raise ValueError("H07/H08 chưa PASS cùng UUID")
    verify_bindings(root, h07)
    verify_bindings(root, h08)
    names = {name.decode("utf-8") for name in git(root, "ls-files", "-z").split(b"\0") if name}
    # Hai nguồn mới vẫn được lấy đúng byte trước commit của task đóng gói.
    names.update(("scripts/package_free_pilot.py", "tests/test_free_pilot_package.py"))
    for folder in LOCAL_DIRS:
        if not (root / folder).is_dir():
            raise ValueError("Thiếu dependency local: " + str(folder))
        names.update(p.relative_to(root).as_posix() for p in (root / folder).rglob("*") if p.is_file())
    excluded = {"run.lock", "run.owner.json", "run.recovery.json"}
    names = {name for name in names if not Path(name).is_relative_to(HANDOFF)
             and name != RECEIPT.as_posix() and Path(name).name not in excluded
             and "__pycache__" not in Path(name).parts}
    files = {}
    for name in sorted(names):
        path = root / safe_name(name)
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
            raise ValueError("Nguồn vượt workspace hoặc là symlink: " + name)
        files[name] = path.read_bytes()
    files["handoff/git.pack"], heads = git_snapshots(root)
    packages = sorted({(d.metadata["Name"], d.version) for d in distributions() if d.metadata["Name"]})
    files["handoff/requirements-installed.txt"] = ("\n".join(f"{n}=={v}" for n, v in packages) + "\n").encode()
    # Chỉ so bí mật trong RAM, không in giá trị hoặc đưa .env vào gói.
    env = root / ".env"
    secrets = []
    if env.exists():
        for line in env.read_text(encoding="utf-8-sig").splitlines():
            key, sep, value = line.partition("=")
            if sep and any(tag in key.upper() for tag in ("KEY", "TOKEN", "SECRET", "PASSWORD")):
                value = value.strip().strip('"\'')
                if len(value) >= 16:
                    secrets.append(value.encode())
    for name, raw in files.items():
        if any(secret in raw for secret in secrets):
            raise ValueError("Nguồn chứa credential đang dùng: " + name)
    manifest = {"status": "PILOT_COMPLETE", "scope": "PILOT48_ONLY_FULL1020_CANCELLED",
                "run_uuid": h07["run_uuid"], "git_snapshots": heads,
                "git_history": "SHALLOW_SPARSE_OBJECTS_FOR_CONSUMER_NOT_FULL_HISTORY", "runtime": h08["runtime"],
                "new_api_calls": 0, "bridge": "OFF_REFERENCE_102_SEPARATE",
                "files": {name: {"bytes": len(raw), "sha256": sha(raw)} for name, raw in sorted(files.items())}}
    archive.parent.mkdir(parents=True, exist_ok=True)
    temp = archive.with_suffix(".tmp")
    with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for name, raw in (*sorted(files.items()), (MANIFEST, encoded(manifest))):
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, raw)
    verify_archive(temp)
    temp.replace(archive)
    return manifest


def verify_archive(archive: Path) -> dict:
    """Kiểm tên, tập thành viên và SHA256 từng file trước khi phục hồi."""
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        if len(names) != len({name.casefold() for name in names}):
            raise ValueError("Gói có tên thành viên trùng")
        for name in names:
            safe_name(name)
        manifest = json.loads(bundle.read(MANIFEST))
        if set(names) != set(manifest["files"]) | {MANIFEST}:
            raise ValueError("Gói thiếu/thừa thành viên")
        for name, expected in manifest["files"].items():
            raw = bundle.read(name)
            if {"bytes": len(raw), "sha256": sha(raw)} != expected:
                raise ValueError("Sai hash thành viên: " + name)
    return manifest


def restore(archive: Path, destination: Path) -> dict:
    """Chỉ giải nén vào thư mục mới/rỗng và dựng Git từ snapshot local đã băm."""
    manifest = verify_archive(archive)
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise ValueError("Thư mục phục hồi phải mới hoặc rỗng")
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        for name in bundle.namelist():
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(bundle.read(name))
    git(destination, "init", "--quiet")
    git(destination, "config", "core.autocrlf", "false")
    git(destination, "config", "core.longpaths", "true")
    git(destination, "index-pack", "--stdin", data=(destination / "handoff/git.pack").read_bytes())
    heads = manifest["git_snapshots"]
    git(destination, "update-ref", "refs/heads/pilot-offline", heads["HEAD"])
    git(destination, "symbolic-ref", "HEAD", "refs/heads/pilot-offline")
    (destination / ".git/shallow").write_text("\n".join(sorted(set(heads.values()))) + "\n", encoding="ascii")
    return manifest


def main() -> None:
    """Lệnh vận hành độc lập; không import collector hoặc mở client API."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("build", "verify", "restore"))
    parser.add_argument("--archive", type=Path, default=ROOT / ARCHIVE)
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()
    if args.stage != "build" and (ROOT / RECEIPT).exists():
        receipt = json.loads((ROOT / RECEIPT).read_bytes())
        if sha(args.archive.read_bytes()) != receipt["archive"]["sha256"]:
            raise ValueError("Gói khác SHA256 của receipt bàn giao")
    if args.stage == "build":
        result = build(ROOT, args.archive)
    elif args.stage == "restore":
        if args.destination is None:
            parser.error("restore cần --destination trỏ tới thư mục mới/rỗng")
        result = restore(args.archive, args.destination.resolve())
    else:
        result = verify_archive(args.archive)
    print(f"H09_{args.stage.upper()}_PASS; {len(result['files'])} file; API=0")


if __name__ == "__main__":
    main()
