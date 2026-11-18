"""Đối chứng FIN07 trên 102 điểm, xác minh prior/MT trước khi mở nhãn query."""
from __future__ import annotations

import argparse
from collections import Counter
import math
from pathlib import Path
import sys
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.bayesian_retriever import PREFIX_METRICS
from core.finalize_bank_resources import ASSETS, MODEL
from core.finalize_context import VERSION, FinalizedProviders
from core.finalize_deterministic_bank import OUTPUT
from core.finalize_prior import FIELDS, VARIANTS
from core.historical_evaluation_protocol import PROTOCOL
from core.historical_evaluation_runner import FixtureClients
from core.mt_bicl_oracle import check_posterior, numeric_input
from core.unified_contracts import digest, forecast_only, json_bytes
from core.unified_experiment import runtime_identity
from core.unified_preflight_assets import write_new
from core.unified_protocol import CORE4, binding
from scripts.verify_original_fix_parity import deny_external_network

RECEIPT = "docs/plan/week12/finalize_context_receipt_v1.json"


def require(condition: bool, message: str) -> None:
    """Giữ gate hoạt động cả khi Python bật tối ưu hóa."""
    if not condition:
        raise ValueError(message)


def raw_counts(rows: dict, ids: set[str]) -> list[tuple[int, int]]:
    """Oracle độc lập dùng tập ID giao/hợp, tránh đếm hai lần tín hiệu cùng tăng."""
    bullish_trend = {i for i in ids if rows[i]["retrieval_key"]["trend_ohlcv_rule"] == "BULLISH"}
    bullish_pattern = {i for i in ids if rows[i]["retrieval_key"]["pattern_ohlcv_rule"] == "BULLISH"}
    wins = {i for i in ids if rows[i]["r_net"] > 0}
    losses = ids - wins
    return [(len(wins), len(ids)), *[(len(losses & subset), len(subset)) for subset in
                                   (bullish_pattern | bullish_trend, bullish_trend, bullish_pattern)]]


def verify_prior(provider: FinalizedProviders, point: dict, trace: dict) -> dict:
    """Oracle P/C/B, readiness, xếp hạng/NA và vòng đời strict maturity."""
    from datetime import date
    import numpy as np
    from scipy.stats import beta

    bank = {r["episode_id"]: r for r in provider.rows}
    symbol, cutoff, regime = (point[k] for k in ("symbol", "cutoff", "regime"))
    mature = {i for i, r in bank.items() if r["symbol"] == symbol and r["exit_date"] < cutoff}
    population = {i for i in mature if bank[i]["regime"] == regime and bank[i]["retrieval_key"]["reason"] is None}
    examples = {i for i in population if bank[i]["alpha_consensus"] is not None}
    require(len(mature) == trace["eligible_count"] and sorted(population) == sorted(trace["population_ids"])
            and sorted(examples) == sorted(trace["example_candidate_ids"]), "Oracle phát hiện sai mẫu số/query membership")
    require(trace["query_key"] == point["retrieval_key"] and all(trace["query_signals"][k] == point["retrieval_key"][k]
            for k in FIELDS[:2]), "Khóa truy vấn khác FIN06")
    totals = raw_counts(bank, population)
    for key, (hits, n) in zip(PREFIX_METRICS, totals):
        require(trace["counts"][key] == {"numerator": hits, "denominator": n, "rate": hits / n if n else None},
                "Oracle phát hiện sai mẫu số/tử số Win/Trap/Sai tăng")
    branch = trace["branch"]
    condition = trace["conditional"]
    query = trace["query_signals"]

    def values(row: dict) -> dict:
        return {**row["retrieval_key"], "alpha_consensus": row["alpha_consensus"],
                "indicator_consensus": row["indicator_consensus"]}

    def similarity(identifier: str) -> float:
        prior = values(bank[identifier])
        return len({k for k in FIELDS if prior[k] == query[k]}) / 4

    expected, best, population_count = [], [], len(population)
    metrics_ready = []
    reason = "NO_SAME_SYMBOL_FROZEN_BANK_OOD" if symbol not in CORE4 else "NO_SAME_REGIME_MATURE_BANK" if not population else None
    if point["retrieval_key"]["reason"] is not None and symbol in CORE4:
        reason = "QUERY_OHLCV_KEY_UNAVAILABLE"
    if reason is None and branch == "bayesian_v1":
        expected = sorted(examples, key=lambda i: (-similarity(i), -date.fromisoformat(bank[i]["exit_date"]).toordinal(), i))[:3]
    elif reason is None:
        fields = FIELDS[:2] if branch == "A_tp_pool" else FIELDS
        matches = {i for i in population if tuple(values(bank[i])[k] for k in fields) == tuple(query[k] for k in fields)}
        background = population - matches
        partitions = (("population", population), ("conditional", matches), ("background", background))
        require(list(fields) == condition["fields"], "Sai điều kiện T/P/A/I của phương pháp")
        for name, members in partitions:
            require(sorted(members) == sorted(condition["groups"][name]), "Sai partition thống kê")
            for key, (hits, n) in zip(PREFIX_METRICS, raw_counts(bank, members)):
                require(condition["metrics"][key]["raw_counts"][name] == {
                    "success_count": hits, "support_count": n, "raw_rate": hits/n if n else None}, "Sai raw counts P/C/B")
        for key, (hits, n), (bwin, bsize) in zip(PREFIX_METRICS, raw_counts(bank, matches), raw_counts(bank, background)):
            item = condition["metrics"][key]
            interval = item["credible_interval"]
            if n:
                a = hits + 4 * (bwin + 1) / (bsize + 2)
                b = n + 4 - a
                require(math.isclose(item["posterior_mean"], a/(n+4), abs_tol=1e-12)
                        and math.isclose(float(beta.cdf(interval["lower"], a, b)), .025, abs_tol=1e-10)
                        and math.isclose(float(beta.cdf(interval["upper"], a, b)), .975, abs_tol=1e-10),
                        "Posterior/CrI khác oracle background rời")
                if population_count >= 20 and n >= 5 and interval["upper"] - interval["lower"] <= .75:
                    metrics_ready.append(key)
            else:
                require(interval is None and item["posterior_mean"] is None, "Mẫu số 0 bị đổi thành posterior")
        index = provider.prior.selector.index
        fold = point["fold"]
        scaler = index.scaler(symbol, cutoff, fold_id=fold)
        require(scaler["fit_max_exit_date"] is None or scaler["fit_max_exit_date"] < provider.context.folds[fold],
                "Scaler vượt freeze")
        if point["feature"]["status"] == scaler["status"] == "AVAILABLE":
            features = {r["episode_id"]: r["features"] for r in index.payload["records"]}
            dates = provider.calendar.strftime("%Y-%m-%d").tolist()
            positions = {d: j for j, d in enumerate(dates)}
            scores = {}
            for identifier in examples:
                row, feature = bank[identifier], features[identifier]
                age = (date.fromisoformat(cutoff)-date.fromisoformat(row["as_of_date"])).days
                if age > 730 or feature["status"] != "AVAILABLE":
                    continue
                distance = np.linalg.norm((np.array(point["feature"]["vector"]) - feature["vector"]) / scaler["scale"]) / 2
                score = (similarity(identifier) + 1/(1+distance)) / 2
                if score >= .625:
                    scores[identifier] = float(score * 2**(-age / 365))
            for identifier in sorted(scores, key=lambda i: (-scores[i], -date.fromisoformat(bank[i]["exit_date"]).toordinal(), i)):
                if len(best) == 3:
                    break
                slot = positions[bank[identifier]["as_of_date"]]
                if all(abs(slot - positions[bank[other]["as_of_date"]]) >= 5 for other in best):
                    best.append(identifier)
        require(best == trace["selection"]["selected_ids"], "Ví dụ sai ranking/tuổi/độ đa dạng phiên")
        expected = best if population_count >= 20 else []
        require(trace["gate"]["ready_metric_ids"] == metrics_ready and trace["gate"]["ready_example_ids"] == expected,
                "Cổng thống kê hoặc ví dụ khác oracle")
        reason = None if expected or metrics_ready else "INSUFFICIENT_EVIDENCE"
    require(trace["selected_ids"] == expected and trace["reason"] == reason and trace["fallback"] == (reason is not None),
            "Sai fallback hoặc danh sách ví dụ")
    prefix = trace["request"]["prefix"]
    require(bool(prefix) == (reason is None) and len(prefix) <= 600, "Sai visibility/trần BRPP")
    return {"fallback": reason, "population": population_count, "example_candidates": len(examples), "k": len(expected),
            "examples_selected": expected, "metrics_ready": metrics_ready, "trace_sha256": digest(trace), "prefix_chars": len(prefix)}


def context_proof(provider: FinalizedProviders, point: dict, episode: dict, variants: dict) -> dict:
    """Đối soát input student, facts, freeze và hai phân vị utility bằng oracle riêng."""
    data = numeric_input(episode)
    forecast_only(data["query"])
    require(set(data["query"]) == {"observation_id", "x"}, "Student nhận nhãn query")
    packet = provider.context.facts(point)
    require(episode["advisor"]["query_facts"] == packet and packet["prefix_rows"] == 45, "Sai Fact Anchor/PIT45")
    observations = [r for task in episode["prior"] for r in task["observations"]] + episode["target"]
    freeze = provider.context.folds[point["fold"]]
    reserved = set(provider.points)
    require(all(r["as_of_date"] < r["entry_date"] < r["exit_date"] < freeze and r["episode_id"] not in reserved
                and r["y"] == int(r["r_net"] > 0) for r in observations), "Nhãn context vượt freeze hoặc sai dấu")
    fit = episode["query"]["regime"]
    require(fit["model_training_end_date"] <= "2020-12-31" and fit["feature_end_date"] <= point["cutoff"],
            "HMM MT vượt cutoff")
    context = provider.context.fold_context(point["fold"])
    scan = context.stream.audit[0]
    freeze_logged = scan["as_of_date"]
    require(freeze_logged == freeze and not reserved.intersection(scan["appended_ids"]), "Reserve ID đi qua label engine")
    wire = variants["branches"]["MT_BICL"]["utility"]
    draws = variants["posterior_audits"]["Full"]
    pi = provider.context.student.teacher.pi.tolist()
    oracle = check_posterior(episode, {"wire": wire, "audit": draws}, pi)
    if oracle["supported"]:
        u = sorted(draws["draws"]["U"])
        for q, label in ((.1, "q10"), (.9, "q90")):
            low = math.floor(q*(len(u)-1))
            fraction = q*(len(u)-1)-low
            expected = u[low] * (1-fraction) + u[low+1] * fraction
            require(math.isclose(expected, wire[label + "_U_net_fraction"], abs_tol=1e-12), "Phân vị utility sai oracle")
        require(wire["probability_student"] == context.predict(episode) and math.isclose(wire["posterior_mean_theta"],
                oracle["teacher"]["probability"], abs_tol=1e-12), "Student/teacher bị hoán đổi nguồn")
    return {"K": episode["K"], "m": episode["m"], "membership_sha256": episode["membership_sha256"],
            "facts_sha256": digest(packet), "frozen_before": freeze, "support": wire["reason"],
            "max_observation_exit": max((r["exit_date"] for r in observations), default=None),
            "utility_sha256": digest(wire), "draws_verified": oracle["draws_checked"], "max_error": oracle["max_error"],
            "p_student": wire["probability_student"], "p_teacher": wire["posterior_mean_theta"],
            "q10": wire["q10_U_net_fraction"], "q90": wire["q90_U_net_fraction"]}


def audit(root: Path) -> dict:
    """Đi đúng adapter và resolve trên control schema, tuyệt đối không gọi transport đánh giá."""
    from core.variant_registry import get_variant
    from core.free_pilot_runtime import reserve
    provider = FinalizedProviders(root)
    fixtures = FixtureClients()
    results, counters = [], {branch: Counter() for branch in (*VARIANTS, "MT_BICL")}
    max_chars = max_tokens = 0
    for point in sorted(provider.points.values(), key=lambda p: (p["cutoff"], p["symbol"])):
        identifier = point["id"]
        snapshot = provider.control_snapshot(point)
        adapter, _ = provider.adapters(identifier)
        episode = provider.context.build(point["symbol"], point["cutoff"])
        prepared_mt = provider.context.variants(episode)
        mt = context_proof(provider, point, episode, prepared_mt)
        traces, outputs = {}, {}
        for branch in ("original_common", *VARIANTS, "Fact_Anchor", "MT_BICL"):
            deps = {dep: outputs[dep] for dep in get_variant(branch).dependencies}
            preparation = adapter.prepare(branch, snapshot, deps, 0)
            if point["cutoff"] == provider.context.folds[point["fold"]]:
                adapter.validate(branch, snapshot, deps, 0, preparation)
            request, raw = preparation["request"], None
            if request is not None:
                max_chars = max(max_chars, len(request["messages"][0]["content"]))
                max_tokens = max(max_tokens, reserve(request))
                uuid = str(uuid5(NAMESPACE_URL, "FIN07_OFFLINE_CONTROL|" + identifier + "|" + branch))
                raw = fixtures.decision(1, request, uuid, branch)
                raw["source_request_id"] = uuid
            policy = adapter.resolve(branch, snapshot, deps, 0, preparation, raw)
            outputs[branch] = {"forecast": {"raw": raw, "point_id": identifier, "variant": branch, "repeat": 0,
                                            "realization": 0, "shared_sha256": snapshot.sha256}, "policy": policy}
            if branch in VARIANTS:
                traces[branch] = verify_prior(provider, point, preparation["trace"])
                counters[branch][traces[branch]["fallback"] or "READY"] += 1
                require((raw is None) == bool(traces[branch]["fallback"]), "Fallback prior có response giả")
                if raw is None:
                    require(policy["final_action"] == deps["original_common"]["policy"]["final_action"],
                            "Fallback khác Common cùng repeat")
            if branch == "Fact_Anchor":
                require(policy["wire"]["fact_assertions_valid"], "Fixture hợp lệ bị từ chối Fact Anchor")
            if branch == "MT_BICL":
                require(preparation["aux"]["branch"] == prepared_mt["branches"]["MT_BICL"], "MT dùng nhầm context/weights")
                mt["policy"] = policy["reason"]
                counters[branch][mt["support"]] += 1
        results.append({"id": identifier, "symbol": point["symbol"], "regime": point["regime"], "fold": point["fold"],
                        "prior": traces, "mt": mt})
        if len(results) % 10 == 0 or len(results) == 102:
            print(f"Đã kiểm FIN07 {len(results)}/102", flush=True)
    for name in VARIANTS:
        require(counters[name]["READY"] > 0 and counters[name]["NO_SAME_SYMBOL_FROZEN_BANK_OOD"] == 54,
                "Thiếu chứng cứ ready/fallback cho " + name)
    require(len(results) == 102 and max_chars < 6500 and max_tokens <= 8000, "Sai cohort hoặc prompt budget FIN07")
    sources = (OUTPUT + "manifest.json", ASSETS + "manifest.json", MODEL, PROTOCOL.as_posix(),
               "docs/plan/week12/finalize_news_coverage_v1.json", "core/finalize_context.py", "core/finalize_prior.py",
               "scripts/check_finalize_context.py")
    return {"version": VERSION, "status": "PASS_OFFLINE_FIN07", "scope": "CONTROL_REQUEST_AND_POLICY_NO_MARKET_FORECAST",
            "query_records": len(results), "query_outcomes_computed": False, "hosted_http": 0, "training": False,
            "bank_support": provider_support(provider), "fallback_and_support": {k: dict(v) for k, v in counters.items()},
            "max_prompt_chars": max_chars, "max_control_request_reserve": max_tokens,
            "sources": [binding(root, source) for source in sources], "runtime": runtime_identity(), "points": results}


def provider_support(provider: FinalizedProviders) -> dict:
    """Đếm cohort tĩnh trước gate theo mã và regime."""
    groups: dict[str, Counter] = {}
    for row in provider.rows:
        counts = groups.setdefault(row["symbol"] + "/" + row["regime"], Counter())
        counts.update(statistics=int(row["statistics_ready"]), examples=int(row["example_ready"]))
    return {k: dict(v) for k, v in groups.items()}


def main() -> None:
    """Tái dựng receipt với một thread CPU, giữ cùng float/fingerprint giữa các lần kiểm."""
    deny_external_network()
    import torch
    torch.set_num_threads(1)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit(ROOT)
    artifact = json_bytes({"payload": result, "sha256": digest(result)})
    path = ROOT / RECEIPT
    if args.check:
        require(path.read_bytes() == artifact, "Receipt FIN07 khác byte khi tái lập")
    else:
        write_new(path, artifact)
    print(json_bytes({k: v for k, v in result.items() if k != "points"}).decode())


if __name__ == "__main__":
    main()
