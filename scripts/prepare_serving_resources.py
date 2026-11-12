"""Đóng resource manifest phục vụ as-of mới; không gọi LLM, không đổi weights hoặc study."""
from __future__ import annotations

from contextvars import ContextVar
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.serving_runtime.resources import START, END, VERSION, MANIFEST, binding, default_models
from core.unified_contracts import digest, json_bytes

READS: ContextVar[set[str] | None] = ContextVar("serving_resource_reads", default=None)


def audit(event: str, args: tuple[Any, ...]) -> None:
    """Chỉ ghi path input thuộc workspace trong phiên prepare, không quan sát credential/site-packages."""
    records = READS.get()
    if records is None or event != "open" or not args or not isinstance(args[0], (str, bytes)):
        return
    path = Path(args[0].decode() if type(args[0]) is bytes else args[0]).resolve()
    if path.is_relative_to(ROOT) and path.suffix in (".json", ".csv", ".gz", ".pt"):
        if len(args) > 1 and type(args[1]) is str and any(c in args[1] for c in "wax+"):
            return
        records.add(path.relative_to(ROOT).as_posix())


def build() -> dict[str, Any]:
    """Xác minh tài nguyên thật trên miền mới; chỉ snapshot digest, không tạo raw forecast."""
    from core.serving_registry import MAIN_IDS
    from core.serving_runtime.providers import AsOfProvider
    from core.unified_preflight import ASSETS
    from core.unified_protocol import read
    alpha = read(ROOT, ASSETS + "/frozen_alpha_manifest.json")
    symbols = sorted({key.split("/")[0] for key in alpha["causal_sources"]})
    dates = None
    for symbol in symbols:
        source = alpha["causal_sources"][symbol + "/f2026_q3"]
        price = read(ROOT, source["prices"])
        calendar = {d for d in price["Datetime"] if START <= d <= END}
        dates = calendar if dates is None else dates & calendar
    points = [{"id": s + "-" + START, "symbol": s, "cutoff": START, "fold": "serving_q3_2026",
               "quality": "ASOF_FROZEN_VENDOR_EXPLORATORY"} for s in symbols]
    records: set[str] = {ASSETS + "/frozen_alpha_manifest.json"}
    records.update(path for entry in alpha["causal_sources"].values() for path in entry.values())
    token = READS.set(records)
    try:
        provider = AsOfProvider(ROOT, points, default_models(), list(MAIN_IDS))
        for point in points:
            provider.validate_point(point)
            episode = provider.episode(point["symbol"], point["cutoff"])
            provider.context.variants(episode)
            provider.data.features(point["symbol"], point["cutoff"])
            provider.regimes.get(point["cutoff"])
    finally:
        READS.reset(token)
    bindings = {name: binding(ROOT/name) for name in sorted(records) if (ROOT/name).is_file()}
    return {"version": VERSION, "parent": "U06_FROZEN_COMPONENTS_NEW_SERVING_SUPPORT",
        "bindings": bindings, "support": {"symbols": symbols, "start_date": START, "end_date": END,
            "calendar": sorted(dates), "timeframe": "1d", "language": "vi", "max_points": 30,
            "context_frozen_before": START, "backtest_step_sessions": 3, "price_unit": "THOUSAND_VND",
            "live_latest_supported": False},
        "resources": {name: {"version": VERSION + "/" + name, "sha256": digest(bindings)}
                      for name in ("prices", "news", "calendar", "bank", "regime", "facts", "context", "student")},
        "proof": {"new_llm_calls": 0, "hmm_student_bank_training": 0,
            "selector_integrity": "EXACT_REPLAY_LOCKED_TRAIN_VALIDATION_NO_QUERY_FIT",
            "news_policy": "FROZEN_DATED_CORPUS; NO_NEWS_NOT_NEUTRAL; NOT_EXHAUSTIVE_COVERAGE",
            "native_rowwise_causal_gate": "FAIL", "whole_system_causal_gate": "NOT_CERTIFIED"}}


def restore_assets() -> None:
    """Khôi phục đúng byte asset U06 bị ignored; không ghi đè file khác hash hoặc sửa source cũ."""
    import zipfile
    from core.unified_preflight import PACKAGE, ASSET_SHA256, MANIFEST_V2
    from core.unified_protocol import read, git_blob
    raw = (ROOT/PACKAGE).read_bytes()
    if hashlib.sha256(raw).hexdigest() != ASSET_SHA256:
        raise ValueError("Gói assets U06 khác hash đã khóa")
    if (ROOT/MANIFEST_V2).read_bytes() != git_blob(ROOT,"5fd45e2b",MANIFEST_V2):
        raise ValueError("Manifest assets historical khác nguồn đã khóa")
    expected = read(ROOT,MANIFEST_V2,True)["asset_bindings"]
    with zipfile.ZipFile(ROOT/PACKAGE) as archive:
        for name, record in expected.items():
            target = ROOT/name
            if not target.resolve().is_relative_to(ROOT) or target.is_symlink():
                raise ValueError("Asset thoát workspace")
            content = archive.read(name)
            if len(content) != record['bytes'] or hashlib.sha256(content).hexdigest() != record['sha256']:
                raise ValueError("Asset không khớp binding historical")
            if target.exists():
                if target.read_bytes() != content:
                    raise ValueError("Asset hiện có khác hash, không tự ghi đè")
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(content)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chuẩn bị resource serving offline, không LLM")
    parser.add_argument('--restore-assets',action='store_true')
    parser.add_argument('--verify',action='store_true')
    args = parser.parse_args()
    if args.restore_assets:
        restore_assets()
    if args.verify:
        from core.serving_runtime.resources import Resources
        resources = Resources(ROOT)
        resources.verify()
        print(json.dumps({'status':'PASS_SERVING_RESOURCES','version':VERSION,'files':len(resources.document()['bindings'])}))
        sys.exit(0)
    sys.addaudithook(audit)
    result = build()
    raw = json_bytes(result)
    target = ROOT/MANIFEST
    if target.exists() and target.read_bytes() != raw:
        raise ValueError("Release serving đã tồn tại với bytes khác; dùng version mới")
    target.write_bytes(raw)
    print(json.dumps({"path": MANIFEST, "files": len(result["bindings"]), "sha256": hashlib.sha256(raw).hexdigest(),
                      "symbols": result["support"]["symbols"], "dates": len(result["support"]["calendar"])}, ensure_ascii=False))
