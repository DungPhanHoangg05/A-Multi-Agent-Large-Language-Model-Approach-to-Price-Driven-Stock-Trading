"""Kiểm U03 bằng hai tiến trình sạch: Git donor bất biến và cây tích hợp."""
from __future__ import annotations

import argparse
import base64
from contextlib import ExitStack, redirect_stdout, redirect_stderr
from copy import deepcopy
import hashlib
import inspect
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Any
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DONOR = "9efd23f4157e0d3ab8069fccab7dccf03439a714"
BASE = "9eeb201e9133d08ee857eff3abbcffe49291e2af"
REPORTS = tuple(name + "_report" for name in ("indicator", "pattern", "trend", "alpha", "sentiment"))


def encode(value: Any) -> bytes:
    """Mã hóa nhất quán, không cho NaN/Infinity đi vào bằng chứng."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def sha(raw: bytes) -> str:
    """Băm đúng byte đã quan sát."""
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    """Digest ngữ nghĩa riêng cho báo cáo U03, không thay digest archive cũ."""
    return sha(encode(value))


def deny_external_network() -> None:
    """Chặn mạng ngoài máy; loopback dành cho socketpair của asyncio Windows."""
    connect, connect_ex = socket.socket.connect, socket.socket.connect_ex
    def guarded(sock: socket.socket, address: Any) -> Any:
        if isinstance(address, tuple) and address[0] in ("127.0.0.1", "localhost", "::1"):
            return connect(sock, address)
        raise AssertionError("U03 không được kết nối mạng ngoài máy")
    def guarded_ex(sock: socket.socket, address: Any) -> Any:
        if isinstance(address, tuple) and address[0] in ("127.0.0.1", "localhost", "::1"):
            return connect_ex(sock, address)
        raise AssertionError("U03 không được kết nối mạng ngoài máy")
    socket.socket.connect, socket.socket.connect_ex = guarded, guarded_ex
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", MPLBACKEND="Agg")
    os.environ.pop("GROQ_API_KEY", None)


def view(value: Any) -> Any:
    """Lưu ảnh bằng hash PNG/pixel và giữ nguyên digest request đầy đủ ở caller."""
    if isinstance(value, str) and value.startswith("data:image/png;base64,"):
        from PIL import Image
        raw = base64.b64decode(value.split(",", 1)[1], validate=True)
        with Image.open(io.BytesIO(raw)) as picture:
            return {"png_sha256": sha(raw), "rgba_sha256": sha(picture.convert("RGBA").tobytes()),
                    "size": list(picture.size)}
    if isinstance(value, dict):
        return {str(k): view(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [view(v) for v in value]
    if hasattr(value, "item"):
        return view(value.item())
    return value


def without_clocks(value: Any) -> Any:
    """Chỉ bỏ timestamp vận hành và thời gian đo, không bỏ field kinh tế/schema."""
    if isinstance(value, dict):
        return {k: without_clocks(v) for k, v in value.items()
                if k not in ("started_at", "ended_at", "time_full_sec", "time_no_alpha_sec")}
    if isinstance(value, list):
        return [without_clocks(v) for v in value]
    return view(value)


def decision_factory(module: Any, llm: Any) -> Any:
    """Oracle dùng factory thật của donor; port chọn profile native tường minh."""
    kwargs = {"decision_profile": "original_fix_serving_v1"} if "decision_profile" in inspect.signature(module.create_final_trade_decider).parameters else {}
    return module.create_final_trade_decider(llm, **kwargs)


def client_class() -> type:
    """Doubles chỉ thay transport/response; SDK thật vẫn serialize options/schema."""
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_groq import ChatGroq

    class LocalClient:
        """Ghi request thực ở biên model và trả response xác định, không HTTP."""
        def __init__(self, **options: Any) -> None:
            self.options = {k: v for k, v in options.items() if k != "api_key"}
            self.sdk = ChatGroq(**{**options, "api_key": "u03-offline-placeholder"})
            self.requests: list[dict[str, Any]] = []
            self.schemas: list[dict[str, Any]] = []
            self.replies: list[str] = []

        def record(self, prompt: Any, schema: type | None = None) -> None:
            messages = [HumanMessage(content=prompt)] if type(prompt) is str else prompt
            converted, parameters = self.sdk._create_message_dicts(messages, None)
            body = {"messages": converted, **parameters}
            if schema is not None:
                structured = self.sdk.with_structured_output(schema, method="json_schema", include_raw=True)
                body["response_format"] = structured.steps[0].steps__["raw"].kwargs["response_format"]
            self.requests.append({"wire_sha256": digest(body), "wire": view(body), "client_options": self.options})

        def invoke(self, prompt: Any) -> Any:
            self.record(prompt)
            text = str(prompt).lower()
            if self.replies:
                return AIMessage(content=self.replies.pop(0))
            if "trendline slope" in text or "độ dốc" in text:
                content = ("**Trend direction:** Up\n**Support level:** 84.0\n**Resistance level:** 89.0\n"
                    "**Trendline slope:** Rising\n**Price vs support:** Holding above support\n"
                    "**Detailed analysis:** Higher lows support the structure.\n"
                    "**Trend forecast:** Continued upside above support.\n**Confidence:** Medium")
            elif "pattern" in text or "mô hình" in text:
                content = ("**Pattern:** Rising channel\n**Confidence:** Medium\n**Directional bias:** Bullish\n"
                    "**Evidence:** Higher lows and firm closes\n**Key candles:** Bullish continuation\n"
                    "**Trading implication:** Maintain bias above support")
            else:
                content = "Diễn giải fixture xác định từ dữ liệu đã có."
            return AIMessage(content=content)

        def with_structured_output(self, schema: type, method: str, include_raw: bool) -> Any:
            if method != "json_schema" or include_raw is not True:
                raise AssertionError("Schema method/include_raw đã thay đổi")
            self.schemas.append(schema.model_json_schema())
            owner = self
            class Structured:
                def invoke(self, prompt: Any) -> dict[str, Any]:
                    owner.record(prompt, schema)
                    raw = owner.replies.pop(0) if owner.replies else json.dumps({
                        "decision": "LONG" if "### [4]" in str(prompt) else "SHORT", "forecast_horizon": "T+2.5",
                        "confidence": "Cao", "risk_reward_ratio": 1.8, "evidence_for": "Bằng chứng fixture.",
                        "evidence_against": "Chi phí hai chiều.", "justification": "Phản hồi fixture không dùng payoff."}, ensure_ascii=False)
                    try:
                        parsed = schema.model_validate_json(raw)
                    except ValueError as exc:
                        return {"parsed": None, "raw": AIMessage(content=raw), "parsing_error": str(type(exc).__name__)}
                    return {"parsed": parsed, "raw": AIMessage(content=raw), "parsing_error": None}
            return Structured()
    return LocalClient


def market_frame(poison: bool = False) -> Any:
    """603 nến giá tổng hợp; ba nến outcome nằm ngoài prefix 600 nến."""
    import numpy as np
    import pandas as pd
    index = np.arange(603, dtype=float)
    close = 62. + .042 * index + 1.30 * np.sin(index / 11.) + .45 * np.cos(index / 5.)
    opening = close * (1. + .0018 * np.sin(index / 3.))
    frame = pd.DataFrame({"Datetime": pd.bdate_range("2023-01-02", periods=603), "Open": opening,
        "High": np.maximum(opening, close) + .6, "Low": np.minimum(opening, close) - .6,
        "Close": close, "Volume": (1100000 + 220000 * np.sin(index / 13.) + index * 450).astype(float)})
    if poison:
        frame.loc[600:, ["Open", "High", "Low", "Close"]] *= 1.3
        frame.loc[602, "Close"] *= 1.2
        frame.loc[602, "High"] = max(frame.loc[602, "Open"], frame.loc[602, "Close"]) + 1.
    return frame


def write_news(directory: Path, frame: Any) -> None:
    """Tin hợp lệ, future và undated cùng cache để kiểm policy thời gian thật."""
    import pandas as pd
    cutoff = frame.Datetime.iloc[599]
    articles = []
    for index in range(8):
        date = cutoff - pd.Timedelta(days=index * 3 + 1)
        articles.append({"title": f"Tin fixture {index}", "url": f"https://example.invalid/{index}",
            "content": "Nội dung fixture.", "snippet": "Tóm tắt fixture.", "date": date.strftime("%d/%m/%Y"),
            "date_parsed": date.strftime("%Y-%m-%d"), "label": "positive", "confidence": .7,
            "numeric_score": .7, "scorer": "fixture", "is_fallback": False})
    articles.extend([{**articles[0], "date_parsed": (cutoff + pd.Timedelta(days=1)).strftime("%Y-%m-%d")},
                     {**articles[0], "date_parsed": None}])
    (directory / "sentiment_cache_FPT.json").write_bytes(encode({"symbol": "FPT", "scored_articles": articles}))


def run_graph(language: str, poison: bool = False) -> dict[str, Any]:
    """Chạy engine/graph/alpha/sentiment thật; chỉ client và clock được kiểm soát."""
    from dataclasses import asdict
    from unittest.mock import patch
    import langchain_groq
    import core.backtest_engine as engine_module
    import utils.graph_setup as graphs
    import utils.json_util as json_util
    LocalClient = client_class()
    clients: list[Any] = []
    stages: list[str] = []
    inputs, reports, alpha_outputs = [], [], []
    def factory(**options: Any) -> Any:
        client = LocalClient(**options)
        clients.append(client)
        return client
    def traced(name: str, original: Any) -> Any:
        def make(*args: Any, **kwargs: Any) -> Any:
            node = original(*args, **kwargs)
            def invoke(state: dict[str, Any]) -> dict[str, Any]:
                stages.append(name)
                if name == "indicator":
                    data = state["point_in_time_df"]
                    inputs.append({"rows": len(data), "max_date": str(data.Datetime.max()),
                        "prefix_sha256": sha(data.to_json(orient="split", date_format="iso", double_precision=15).encode()),
                        "window": view(state["kline_data"]), "images": {
                            field: view("data:image/png;base64," + state[field]) for field in ("pattern_image", "trend_image")}})
                if name == "decision":
                    reports.append({key: state.get(key) for key in REPORTS})
                result = node(state)
                if name == "alpha":
                    alpha_outputs.append(json_util.to_json_compatible({key: result.get(key) for key in
                        ("alpha_report", "sentiment_report", "sentiment_data", "sentiment_norm")}))
                return result
            return invoke
        return make
    with TemporaryDirectory(prefix="u03-graph-") as directory, ExitStack() as stack:
        previous = Path.cwd()
        stack.callback(os.chdir, previous)
        os.chdir(directory)
        frame = market_frame(poison)
        write_news(Path(directory), frame)
        for name in ("indicator", "pattern", "trend", "alpha"):
            attr = "create_" + name + "_agent"
            stack.enter_context(patch.object(graphs, attr, traced(name, getattr(graphs, attr))))
        stack.enter_context(patch.object(graphs, "create_final_trade_decider", traced("decision", graphs.create_final_trade_decider)))
        stack.enter_context(patch.object(langchain_groq, "ChatGroq", side_effect=factory))
        engine = engine_module.BacktestEngine({"groq_api_key": "u03-offline-placeholder", "language": language,
                                             "use_historical_sentiment": True})
        engine.DELAY_BETWEEN_VARIANTS = engine.DELAY_BETWEEN_TESTS = 0.
        stack.enter_context(patch.object(engine, "_draw_backtest_result", return_value=None))
        summary = engine.run(frame, "FPT", timeframe="1 ngày", n_tests=1, window_size=45, step=3,
                             result_path=str(Path(directory) / "result.json"))
        result = without_clocks(json_util.to_json_compatible(asdict(summary)))
        return {"summary": result, "stages": stages, "inputs": inputs, "reports": reports,
                "alpha": alpha_outputs, "clients": [{"options": c.options, "schemas": c.schemas,
                    "requests": c.requests} for c in clients]}


def decision_matrix() -> list[dict[str, Any]]:
    """So payload cuối, distill/cap, bốn ablation, VI/EN, live/backtest và repair."""
    import agents.decision_agent as decision
    LocalClient = client_class()
    rows = []
    for language in ("vi", "en"):
        for backtest in (False, True):
            for variant in ("B", "A", "S", "AS"):
                for long in (False, True):
                    state = {"stock_name": "FPT", "time_frame": "1 ngày", "language": language, "is_backtest": backtest,
                        **{key: (key + ": " + ("Dữ liệu α 123.45; " * (150 if long else 2))) for key in REPORTS[:3]}}
                    for flag, key in (("A", "alpha_report"), ("S", "sentiment_report")):
                        if flag in variant:
                            state[key] = key + ": " + "Tín hiệu fixture. " * (150 if long else 2)
                    client = LocalClient(model="openai/gpt-oss-20b", temperature=0., max_tokens=2048, max_retries=3,
                                         reasoning_format="hidden")
                    try:
                        result = decision_factory(decision, client)(deepcopy(state))
                        row = {"status": "complete", "normalized": result["final_trade_decision"]}
                    except ValueError as exc:
                        if "ngân sách" not in str(exc):
                            raise
                        row = {"status": "blocked_over_budget"}
                    rows.append({"case": f"{language}/{backtest}/{variant}/{long}", **row,
                                 "schemas": client.schemas, "requests": client.requests})
    state = {"stock_name": "FPT", "time_frame": "1 ngày", "language": "vi", "is_backtest": True,
             **{key: "Báo cáo fixture." for key in REPORTS[:3]}}
    for structured in (True, False):
        client = LocalClient(model="openai/gpt-oss-20b", temperature=0., max_tokens=2048)
        valid = json.dumps({"decision": "LONG", "forecast_horizon": "T+2.5", "confidence": "Cao", "risk_reward_ratio": 1.5,
            "evidence_for": "Fixture", "evidence_against": "Phí", "justification": "Fixture"}, ensure_ascii=False)
        client.replies = ['{"decision":"HOLD"}', valid]
        target = client if structured else type("TextOnly", (), {"invoke": client.invoke})()
        result = decision_factory(decision, target)(state)
        rows.append({"case": f"repair/{structured}", "status": "complete", "normalized": result["final_trade_decision"],
                     "requests": client.requests, "schemas": client.schemas})
    return rows


def entrypoint_probe(summary: dict[str, Any]) -> dict[str, Any]:
    """Kiểm consumer CLI/UI cũ bằng outcome xác định, không chạy web server."""
    from dataclasses import asdict
    from unittest.mock import patch
    import importlib
    import pandas as pd
    from scripts.run_ablation_matrix import _variant_test_points, VARIANTS
    from core.backtest_engine import compute_account_metrics
    import core.realtime_loader as loader
    point = deepcopy(summary["test_points"][0])
    point["variants"] = {name: {"prediction": point["pred_full"] if name != "baseline" else point["pred_no_alpha"],
        "correct": point["correct_full"] if name != "baseline" else point["correct_no_alpha"],
        "confidence": "Cao", "risk_reward_ratio": "1.8"} for name in VARIANTS}
    cli = {name: asdict(compute_account_metrics(_variant_test_points([point], name))["full"]) for name in VARIANTS}
    with patch.object(loader, "get_all_symbols_realtime", return_value=[]):
        web = importlib.import_module("web_interface")
    web._bt_jobs["u03-fixture"] = {"status": "done", "step": "done", "summary": summary,
        "test_points": summary["test_points"], "partial": {}, "error": ""}
    client = web.app.test_client()
    pages = {}
    for language in ("vi", "en"):
        response = client.get("/backtest?lang=" + language)
        if response.status_code != 200:
            raise AssertionError("UI backtest không render được")
        pages[language] = sha(response.data)
    response = client.get("/api/backtest/status/u03-fixture")
    if response.status_code != 200:
        raise AssertionError("UI không đọc được summary")
    missing = client.get("/api/backtest/status/u03-missing")
    if missing.status_code != 404:
        raise AssertionError("UI biến job thiếu thành thành công")
    return {"cli_accounts": cli, "ui_status": response.get_json(), "pages": pages, "missing_status": 404}


def archive_replay(data_root: Path) -> dict[str, Any]:
    """Replay 204 native B/AS chính; parent và byte gắn Git fix, không tự ký lại."""
    from dataclasses import asdict
    from collections import defaultdict
    import pandas as pd
    from importlib.metadata import version
    import agents.decision_agent as decision
    from core.backtest_engine import BacktestEngine, TestPoint, compute_account_metrics
    from core.revision_common_study import FrozenSentiment, point_state, pack_state, restore_state, digest as old_digest
    from core.revision72_run import checked, variant_state
    from core.revision_baselines import load_prices
    from core.revision_minimal_bank import point_path, parent_for, verify_record, raw_prediction
    from utils.target_contract import target_fields
    from utils import static_util

    inventory_path = data_root / "docs/plan/week12/fix_develop_source_inventory.zip"
    if sha(inventory_path.read_bytes()) != "9f05fd92493ca74bbafe9ffb2a7412f99f84aa391d3e3ecaa7aaab8404fb3775":
        raise ValueError("Inventory donor khác mốc U01")
    with zipfile.ZipFile(inventory_path) as bundle:
        inventory = {r["path"]: r["versions"]["fix_frozen"] for r in json.loads(bundle.read("inventory.json"))
                     if "fix_frozen" in r["versions"]}
    bindings = {}
    def bound(name: str | Path) -> Path:
        """Mỗi input phải khớp đúng Git donor trước khi consumer cũ đọc."""
        name = Path(name).as_posix()
        if name not in bindings:
            path = data_root / name
            if name not in inventory or path.is_symlink() or not path.resolve().is_relative_to(data_root):
                raise ValueError("Input replay không có donor an toàn: " + name)
            raw = path.read_bytes()
            expected = inventory[name]
            if len(raw) != expected["bytes"] or sha(raw) != expected["sha256"]:
                raise ValueError("Input replay khác Git donor: " + name)
            bindings[name] = {"bytes": len(raw), "sha256": sha(raw)}
        return data_root / name
    def signed(name: str | Path) -> dict[str, Any]:
        return checked(bound(name))

    run_name = Path("outputs/revision/revision_minimal_v1")
    manifest = signed(run_name / "manifest.json")
    original = signed("outputs/revision/chart_r1_run_v1/run_manifest.json")
    runtime = {name: version(name) for name in original["runtime"] if name != "python"}
    runtime["python"] = sys.version.split()[0]
    if runtime != original["runtime"]:
        raise ValueError("Runtime khác archive native; cần môi trường frozen riêng")
    anchors = {}
    for record in original["sources"]:
        name = record["path"]
        if name not in ("agents/decision_agent.py", "core/backtest_engine.py", "agents/alpha_agent.py",
                        "agents/trend_agent.py", "agents/pattern_agent.py", "agents/indicator_agent.py",
                        "utils/static_util.py", "utils/i18n.py", "data_manager/sentiment_cache.py", "default_config.py"):
            continue
        raw = subprocess.check_output(["git", "show", DONOR + ":" + name], cwd=data_root)
        candidates = {"git_bytes": raw, "crlf_serialization": raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")}
        matches = [kind for kind, candidate in candidates.items() if sha(candidate) == record["sha256"]]
        if not matches:
            raise ValueError("Không neo được source native archive: " + name)
        anchors[name] = {"recorded_sha256": record["sha256"], "git_sha256": sha(raw), "matches": matches}

    protocol = original["protocol"]
    price_path = protocol["price_snapshot"]
    price_manifest = json.loads(bound(Path(price_path) / "manifest.json").read_bytes())
    for record in price_manifest["symbols"]:
        bound(Path(price_path) / record["path"])
    frames, _ = load_prices(data_root / price_path, protocol["price_quality_policy"])
    bank_path = Path("outputs/revision/r1_72h_bank_v2")
    bank = json.loads(bound(bank_path / "manifest.json").read_bytes())
    store = FrozenSentiment(json.loads(bound(bank_path / "news.json").read_bytes()))
    jobs = [job for job in manifest["jobs"] if job["phase"] == "main"]
    if len(jobs) != 204 or len({job["unit"]["id"] for job in jobs}) != 102:
        raise ValueError("Archive main thiếu support đã khóa")
    groups, rows, accounts = {}, [], defaultdict(list)
    LocalClient = client_class()
    client = LocalClient(model=protocol["agent_llm_model"], temperature=0., max_tokens=2048,
                         max_retries=0, reasoning_format="hidden")
    native_node = decision_factory(decision, client)
    request_ids: set[str] = set()
    renders = []
    with TemporaryDirectory(prefix="u03-archive-images-") as directory, ExitStack() as stack:
        previous = Path.cwd()
        stack.callback(os.chdir, previous)
        os.chdir(directory)
        for job in jobs:
            unit = job["unit"]
            key = unit["id"]
            if key not in groups:
                asset = signed(bank_path / f"features/{unit['symbol']}_{unit['decision']}.json")
                donor = signed(bank_path / f"features/{unit['symbol']}_{unit['placebo_donor']}.json")
                initial = point_state(frames[unit["symbol"]], unit["symbol"], unit["decision"], protocol, store)
                shard = Path("outputs/revision/chart_r1_run_v1") / f"shards/org{job['origin_org']}"
                chart = signed(shard / f"charts/{key}.json")
                if chart["asset_hash"] != asset["sha256"]:
                    raise ValueError("Chart/asset parent khác")
                images = {}
                for kind in ("pattern", "trend"):
                    renderer = static_util.generate_kline_image if kind == "pattern" else static_util.generate_trend_image
                    kwargs = {"write_artifacts": False} if "write_artifacts" in inspect.signature(renderer).parameters else {}
                    actual = renderer(initial["kline_data"], **kwargs)[kind + "_image"]
                    if actual != chart[kind + "_image"]:
                        raise AssertionError("Ảnh native khác archive: " + key + "/" + kind)
                    images[kind] = view("data:image/png;base64," + actual)
                initial.update({key: chart[key] for key in ("pattern_image", "trend_image")})
                state, parents = initial, []
                for node in ("Indicator", "Pattern", "Trend"):
                    record = signed(shard / f"nodes/{key}_r0_{node}.json")
                    expected = {"input_hash": old_digest(pack_state(state)), "asset_hash": asset["sha256"],
                                "run_signature": original["sha256"]}
                    if record["parent"] != expected or record["context"]["unit_id"] != key:
                        raise ValueError("Parent/node input replay khác: " + key + "/" + node)
                    for artifact in record["call_hashes"]:
                        path = bound(shard / artifact["path"])
                        if sha(path.read_bytes()) != artifact["sha256"]:
                            raise ValueError("Raw upstream sai checksum")
                    state = {**state, **restore_state(record["state"], initial)}
                    parents.append(record["sha256"])
                if old_digest(pack_state(state)) != job["origin_parent"]["upstream_hash"] or parents != job["origin_parent"]["node_hashes"]:
                    raise ValueError("Shared upstream không khớp Decision parent")
                groups[key] = (state, asset, donor)
                renders.append({"unit_id": key, "images": images, "prefix_rows": len(initial["point_in_time_df"]),
                                "max_date": str(initial["point_in_time_df"].Datetime.max())})
                print(f"U03 archive đã dựng {len(groups)}/102 upstream từ nguồn khóa", flush=True)
            state, asset, donor = groups[key]
            if job["reuse"]:
                record_path = bound(job["reuse"]["path"])
                if sha(record_path.read_bytes()) != job["reuse"]["sha256"]:
                    raise ValueError("Reuse checkpoint đổi byte")
                parent, bank_id, epoch = job["origin_parent"], job["origin_bank_id"], job["origin_epoch"]
            else:
                record_path = bound(point_path(data_root / run_name, job).relative_to(data_root))
                parent, bank_id, epoch = parent_for(manifest, job), manifest["sha256"], manifest["sha256"]
            record = signed(record_path.relative_to(data_root))
            shard_path = record_path.parent.parent
            for artifact in record["call_hashes"]:
                bound((shard_path / artifact["path"]).relative_to(data_root))
            for attempt in record["request_ids"]:
                if attempt in request_ids:
                    raise ValueError("Response bị dùng cho nhiều slots")
                request_ids.add(attempt)
                bound((shard_path / f"calls/{attempt}.request.json").relative_to(data_root))
                bound((shard_path / f"calls/{attempt}.response.json").relative_to(data_root))
                receipt = shard_path / f"calls/{attempt}.response_digest.json"
                if receipt.exists():
                    bound(receipt.relative_to(data_root))
            record = verify_record(record_path, job, parent, bank_id, epoch)
            client.replies = []
            for attempt in record["request_ids"]:
                response = json.loads((shard_path / f"calls/{attempt}.response.json").read_bytes())
                message = response["response"]["generations"][0][0]["message"]
                content = message.get("content")
                if not content and message.get("tool_calls"):
                    content = json.dumps(message["tool_calls"][0]["args"], ensure_ascii=False)
                client.replies.append(content)
            start = len(client.requests)
            output = native_node(variant_state(state, asset, donor, job["context"]["variant"]))
            if output["decision_prompt"] != job["prompt"] or old_digest(output["decision_prompt"]) != job["prompt_hash"]:
                raise AssertionError("Native request khác archive: " + job["id"])
            if json.loads(output["final_trade_decision"])["decision"] != record["prediction"]:
                raise AssertionError("Action replay khác raw response")
            if "state" in record and output["final_trade_decision"] != record["state"]["final_trade_decision"]:
                raise AssertionError("Parse/normalize khác checkpoint")
            actual = client.requests[start:]
            if len(actual) != len(record["request_ids"]) or client.replies:
                raise AssertionError("Replay thừa/thiếu response hoặc format attempts")
            expected_format = job["request_contract"]["invocation_parameters"]["response_format"]
            metadata = job["request_contract"]["model_metadata"]
            for request in actual:
                wire = request["wire"]
                if (wire["response_format"] != expected_format or wire["model"] != metadata["ls_model_name"]
                        or wire["temperature"] != metadata["ls_temperature"] or wire.get("max_tokens") != metadata["ls_max_tokens"]):
                    raise AssertionError("Model/options/schema replay khác archive")
            data = frames[unit["symbol"]].rename(columns={"date": "Datetime"}).copy()
            data["Datetime"] = pd.to_datetime(data["Datetime"])
            fields = target_fields(data, int(unit["decision"]) + 1, 3)
            prediction = record["prediction"]
            correct = bool((prediction == "LONG") == (fields["label_net"] == "UP"))
            point = TestPoint(len(accounts[(unit["symbol"], unit["fold"], job["context"]["variant"])]) + 1,
                str(data.Datetime.iloc[0].date()), unit["date"], fields["decision_close"], fields["exit_close"],
                fields["label_net"], fields["net_return"] * 100, prediction, correct, "Cao", "1.8", prediction,
                correct, "Cao", "1.8", 0., 0., entry_time=str(data.Datetime.iloc[unit["decision"] + 1].date()),
                exit_time=str(data.Datetime.iloc[unit["decision"] + 3].date()), **fields)
            accounts[(unit["symbol"], unit["fold"], job["context"]["variant"])].append(point)
            rows.append({"job_id": job["id"], "unit_id": key, "prediction": prediction,
                         "prompt_hash": job["prompt_hash"], "requests": actual, "target": fields})
    ledger = {"/".join(key): asdict(compute_account_metrics(sorted(points, key=lambda p: p.window_end))["full"])
              for key, points in sorted(accounts.items())}
    if len(ledger) != 102:
        raise AssertionError("Thiếu 51 tài khoản mỗi variant B/AS")
    return {"planned_slots": 204, "complete_slots": len(rows), "upstream_units": len(groups), "image_replays": len(renders) * 2,
            "request_ids": len(request_ids), "rows": rows, "renders": renders, "accounts": ledger,
            "source_anchors": anchors, "runtime": runtime, "bindings": bindings,
            "scope": "CONDITIONAL_ON_ARCHIVED_UPSTREAM_AND_NUMERIC_ASSETS; NO_HOSTED_RESPONSE_REGENERATION"}


def worker(root: Path, output: Path, poison: bool = False, data_root: Path | None = None) -> None:
    """Nạp một cây nguồn duy nhất sau -I; không trộn module donor/integrated."""
    deny_external_network()
    sys.path.insert(0, str(root))
    from unittest.mock import patch
    with patch("dotenv.load_dotenv", return_value=False):
        result = {"graphs": {language: run_graph(language, poison) for language in ("vi", "en")},
                  "matrix": decision_matrix() if not poison else []}
        if not poison:
            result["entrypoints"] = entrypoint_probe(result["graphs"]["vi"]["summary"])
        if data_root is not None:
            result["archive"] = archive_replay(data_root)
    loaded = {}
    for name, module in list(sys.modules.items()):
        if name.split(".")[0] not in ("agents", "core", "utils", "data_manager", "default_config", "web_interface", "scripts"):
            continue
        source = getattr(module, "__file__", None)
        if source and Path(source).suffix == ".py":
            path = Path(source).resolve()
            if not path.is_relative_to(root):
                raise AssertionError("Module dự án lọt từ cây nguồn khác: " + name)
            loaded[path.relative_to(root).as_posix()] = sha(path.read_bytes())
    result["loaded_sources"] = loaded
    with output.open("xb") as handle:
        handle.write(encode(result))


def extract_donor(root: Path, destination: Path) -> None:
    """Đọc blob thô, tránh cả chuyển newline checkout lẫn export của git archive."""
    tree = subprocess.check_output(["git", "ls-tree", "-rz", DONOR, "--", "agents", "core", "utils", "data_manager",
        "default_config.py", "web_interface.py", "scripts/run_ablation_matrix.py", "templates"], cwd=root)
    entries = []
    for row in tree.split(b"\0"):
        if not row:
            continue
        header, name = row.split(b"\t", 1)
        mode, kind, oid = header.split()
        path = destination / name.decode("utf-8")
        if mode != b"100644" or kind != b"blob" or not path.resolve().is_relative_to(destination.resolve()):
            raise ValueError("Cây Git donor chứa đường dẫn hoặc mode không an toàn")
        entries.append((path, oid))
    raw = subprocess.check_output(["git", "cat-file", "--batch"],
        input=b"".join(oid + b"\n" for _, oid in entries), cwd=root)
    stream = io.BytesIO(raw)
    for path, expected_oid in entries:
        oid, kind, size = stream.readline().split()
        if oid != expected_oid or kind != b"blob":
            raise ValueError("Git cat-file trả sai blob donor")
        content = stream.read(int(size))
        if len(content) != int(size) or stream.read(1) != b"\n":
            raise ValueError("Git cat-file trả thiếu byte donor")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    if stream.read():
        raise ValueError("Git cat-file trả byte thừa")


def compare_results(frozen: dict[str, Any], integrated: dict[str, Any]) -> dict[str, Any]:
    """Không bỏ qua payload mismatch hoặc chỉ dùng action để nhận parity."""
    if frozen["graphs"] != integrated["graphs"]:
        for language in frozen["graphs"]:
            for field in frozen["graphs"][language]:
                if frozen["graphs"][language][field] != integrated["graphs"][language][field]:
                    raise AssertionError(f"Graph parity khác {language}/{field}")
    for field in ("entrypoints", "archive"):
        if frozen.get(field) != integrated.get(field):
            raise AssertionError("Cold parity khác " + field)
    for language, graph in integrated["graphs"].items():
        if graph["stages"] != ["indicator", "pattern", "trend", "alpha", "decision", "decision"]:
            raise AssertionError("Upstream/call order không đúng native paired")
        if len(graph["clients"]) != 2 or [len(c["requests"]) for c in graph["clients"]] != [2, 2]:
            raise AssertionError("Số lời gọi text/vision khác protocol fixture")
        if graph["inputs"][0]["rows"] != 600 or graph["alpha"][0]["sentiment_data"]["n_articles_used"] != 8:
            raise AssertionError("Fixture thiếu cutoff/600 bars hoặc policy sentiment")
    matched, blocked = 0, []
    for before, after in zip(frozen["matrix"], integrated["matrix"], strict=True):
        requests = before["requests"]
        oversized = any(len(request["wire"]["messages"][0]["content"]) >= 6500 for request in requests)
        if oversized:
            if after["status"] != "blocked_over_budget" or after["requests"]:
                raise AssertionError("Native quá budget vẫn gọi model")
            blocked.append(before["case"])
        elif before != after:
            raise AssertionError("Golden request/schema/parse khác: " + before["case"])
        else:
            matched += 1
    archive = integrated.get("archive", {})
    return {"status": "PASS", "method": "original_fix", "serving_profile": "original_fix_serving_v1",
            "graph_languages": ["vi", "en"], "golden_matched": matched,
            "legacy_only_over_budget": blocked, "native_over_budget_new_calls": 0,
            "archive": {key: archive.get(key) for key in ("planned_slots", "complete_slots", "upstream_units", "image_replays", "request_ids")},
            "archive_accounts": len(archive.get("accounts", {})),
            "serving_delta": "FAIL_BEFORE_INFERENCE_AT_6500_CHARS; NO_SILENT_RECAP; MODEL_OPTIONS_SCHEMA_UNCHANGED"}


def run(root: Path, destination: Path) -> dict[str, Any]:
    """Chạy cold oracle/port rồi lưu golden và báo cáo mới trong namespace riêng."""
    if destination.exists():
        raise FileExistsError("Không ghi đè bằng chứng U03 đã có")
    if destination.is_relative_to(root) and not destination.is_relative_to(root / "outputs/unified_integration"):
        raise ValueError("Output trong repo phải dùng namespace outputs/unified_integration mới")
    destination.mkdir(parents=True)
    with TemporaryDirectory(prefix="u03-donor-") as directory:
        frozen_root = Path(directory)
        extract_donor(root, frozen_root)
        for name, source in (("frozen", frozen_root), ("integrated", root)):
            with (destination / (name + ".log")).open("wb") as log:
                subprocess.run([sys.executable, "-I", "-X", "utf8", str(Path(__file__).resolve()), "--worker",
                    "--root", str(source), "--data-root", str(root), "--output", str(destination / (name + ".json"))],
                    cwd=source, stdout=log, stderr=subprocess.STDOUT, check=True)
        frozen = json.loads((destination / "frozen.json").read_bytes())
        integrated = json.loads((destination / "integrated.json").read_bytes())
        for name, expected in frozen["loaded_sources"].items():
            raw = subprocess.check_output(["git", "show", DONOR + ":" + name], cwd=root)
            if sha(raw) != expected:
                raise AssertionError("Oracle đã nạp source khác donor Git: " + name)
        report = compare_results(frozen, integrated)
    report.update(donor_commit=DONOR, base_integration=BASE, hosted_calls=0, training_runs=0,
                  scope="DETERMINISTIC_AND_ARCHIVE_PARITY_ON_ADMISSIBLE_INPUTS_NOT_HOSTED_REPRODUCTION")
    (destination / "report.json").write_bytes(encode(report))
    return report


def verify_package(root: Path, package: Path) -> dict[str, Any]:
    """Cold consumer chỉ đối soát bytes/source/runtime và kết quả đã lưu, không tạo client."""
    from importlib.metadata import version
    deny_external_network()
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Gói U03 có thành viên trùng")
        manifest = json.loads(archive.read("manifest.json"))
        if set(names) != {"manifest.json", *manifest["members"]} or manifest["donor_commit"] != DONOR:
            raise ValueError("Gói U03 sai nguồn hoặc tập thành viên")
        for name, expected in manifest["members"].items():
            raw = archive.read(name)
            if len(raw) != expected["bytes"] or sha(raw) != expected["sha256"]:
                raise ValueError("Gói U03 sai hash: " + name)
        for name, expected in json.loads(archive.read("source_bindings.json")).items():
            path = root / name
            if not path.resolve().is_relative_to(root) or sha(path.read_bytes()) != expected["sha256"]:
                raise ValueError("Source U03 khác receipt: " + name)
        runtime = json.loads(archive.read("runtime.json"))
        if runtime["python"] != sys.version.split()[0] or any(version(name) != value for name, value in runtime["packages"].items()):
            raise ValueError("Runtime U03 khác môi trường đã kiểm")
        frozen, integrated = (json.loads(archive.read(name + ".json")) for name in ("frozen", "integrated"))
        for name, expected in integrated.get("archive", {}).get("bindings", {}).items():
            path = root / name
            if (not path.resolve().is_relative_to(root) or path.stat().st_size != expected["bytes"]
                    or sha(path.read_bytes()) != expected["sha256"]):
                raise ValueError("Input archive U03 khác donor đã kiểm: " + name)
        for name, expected in frozen["loaded_sources"].items():
            raw = subprocess.check_output(["git", "show", DONOR + ":" + name], cwd=root)
            if sha(raw) != expected:
                raise ValueError("Nguồn oracle trong gói khác donor Git: " + name)
        report = json.loads(archive.read("report.json"))
        actual = compare_results(frozen, integrated)
        if any(report.get(name) != value for name, value in actual.items()):
            raise ValueError("Báo cáo U03 không khớp golden/cold output")
    return {"status": "PASS", "members": len(names), "hosted_calls": 0, "client_constructions": 0,
            "scope": "HASH_INPUT_SOURCE_RUNTIME_AND_STORED_PARITY_ONLY_NOT_A_NEW_GRAPH_RUN"}


def main() -> None:
    """CLI chỉ kiểm offline; mọi output cần namespace mới."""
    parser = argparse.ArgumentParser(description="Kiểm parity original_fix offline")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path, help="Kiểm gói bằng chứng đã lưu, không chạy lại graph")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--poison", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--data-root", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify_package(args.root.resolve(), args.verify.resolve()), ensure_ascii=False))
    elif args.output is None:
        parser.error("Cần --output mới hoặc --verify gói đã khóa")
    elif args.worker:
        worker(args.root.resolve(), args.output.resolve(), args.poison,
               args.data_root.resolve() if args.data_root else None)
    else:
        print(json.dumps(run(args.root.resolve(), args.output.resolve()), ensure_ascii=False))


if __name__ == "__main__":
    main()
