"""Metric/selection replica gi? nguy?n c?ng th?c v? m?u s? c?a recipe ?? pin."""
from __future__ import annotations
from copy import deepcopy
import math
from typing import Any
import numpy as np
import torch
from core.mt_bicl_bank import SYMBOLS
from core.mt_bicl_evaluation import probabilities, market_input
from core.mt_bicl_replica_student import pack_input, collate_packets, DistilledStudent
from core.mt_bicl_replica_learner import tensor_hash
SEEDS=(17,42,73)
STEPS=tuple(range(250,5001,250))


def mechanism_metrics(logits: list[float], episodes: list[dict[str, Any]]) -> dict[str, Any]:
    """KL Bernoulli oracle||model ổn định; giữ sai số làm tròn nhỏ, không clipping."""
    if not episodes or len(logits) != len(episodes):
        raise ValueError("Sai mẫu số synthetic")
    p, one, zero = probabilities(logits)
    q1 = np.asarray([e["oracle"]["log_probability_one"] for e in episodes], dtype=np.float64)
    q0 = np.asarray([e["oracle"]["log_probability_zero"] for e in episodes], dtype=np.float64)
    q = np.exp(q1)
    if (not np.isfinite([q1, q0]).all() or not np.allclose(q+np.exp(q0), 1, atol=1e-12, rtol=0)
            or not np.allclose(q, [e["oracle"]["probability"] for e in episodes], atol=1e-12, rtol=0)):
        raise ValueError("Oracle log probability không chuẩn hóa")
    kl = q*(q1-one)+np.exp(q0)*(q0-zero)
    error = np.abs(p-q)
    if not np.isfinite(kl).all() or (kl < -1e-12).any():
        raise ValueError("KL không hữu hạn hoặc âm quá sai số làm tròn")
    def summary(slots: np.ndarray) -> dict[str, Any]:
        """Báo support K/m cả cold-start, không bỏ nhóm lỗi lớn."""
        return {"count": int(slots.sum()), "mean_kl_nats": float(kl[slots].mean()),
                "p95_absolute_error": float(np.quantile(error[slots], .95, method="linear"))}
    result = summary(np.ones(len(episodes), dtype=bool))
    for key in ("K", "m"):
        values = np.asarray([e["oracle"][key] for e in episodes])
        result["by_"+key] = {str(int(v)): summary(values == v) for v in np.unique(values)}
    result["gate"] = "PASS" if result["mean_kl_nats"] <= .02 and result["p95_absolute_error"] <= .1 else "FAIL"
    return result


def prior_swap_metrics(a: list[float], b: list[float], pairs: list[dict[str, Any]]) -> dict[str, Any]:
    """Đánh giá đúng toàn bộ tập cặp, mẫu số eligible cố định theo oracle."""
    if len(a) != len(b) or len(a) != len(pairs) or not pairs:
        raise ValueError("Sai mẫu số prior swap")
    delta = probabilities(b)[0]-probabilities(a)[0]
    oracle = np.asarray([r["oracle_b"]["probability"]-r["oracle_a"]["probability"] for r in pairs])
    eligible = np.abs(oracle) >= .05
    if eligible.tolist() != [r["eligible"] for r in pairs]:
        raise ValueError("Không được thay denominator eligible của corpus khóa")
    count = int(eligible.sum())
    agree = int((np.sign(delta[eligible]) == np.sign(oracle[eligible])).sum())
    fraction = agree/count if count else None
    return {"attempt_pairs": len(pairs), "eligible_pairs": count, "agree_pairs": agree,
            "sign_agreement": fraction, "zero_model_delta_eligible": int((delta[eligible] == 0).sum()),
            "gate": "INCONCLUSIVE_BLOCK_DEVELOPMENT" if count < 200 else "PASS" if fraction >= .9 else "FAIL"}


def selection_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Macro đều mã, clip chỉ log loss thị trường; không dùng P&L hoặc synthetic oracle."""
    if not records or len({r["episode_id"] for r in records}) != len(records):
        raise ValueError("Dự báo selection rỗng hoặc trùng ID")
    metrics = {}
    for symbol in SYMBOLS:
        group = [r for r in records if r["symbol"] == symbol]
        if not group:
            raise ValueError("Selection thiếu mã")
        p, y = np.asarray([r["p"] for r in group]), np.asarray([r["y"] for r in group])
        if not np.isfinite(p).all() or ((p < 0) | (p > 1)).any() or not np.isin(y, [0, 1]).all():
            raise ValueError("Xác suất/nhãn selection không hợp lệ")
        clipped = np.clip(p, 1e-6, 1-1e-6)
        metrics[symbol] = {"count": len(group), "log_loss": float(-(y*np.log(clipped)+(1-y)*np.log1p(-clipped)).mean()),
                           "brier": float(((p-y)**2).mean())}
    return {"symbols": metrics, "macro_log_loss": float(np.mean([m["log_loss"] for m in metrics.values()])),
            "macro_brier": float(np.mean([m["brier"] for m in metrics.values()]))}


def ablate(data: dict[str, Any], mode: str) -> dict[str, Any]:
    """Giữ query/membership còn lại, bỏ đúng component; không truy xuất lại context."""
    if mode not in ("full","no_prior","no_target","context_blind"):
        raise ValueError("Ablation không thuộc protocol")
    value = deepcopy(data)
    if mode in ("no_prior","context_blind"):value["prior"] = []
    if mode in ("no_target","context_blind"):value["target"]["observations"] = []
    return value


def predict(model: DistilledStudent, packets: list[dict[str, Any]], physical: int,
            device: torch.device, check: Any=lambda:None) -> list[float]:
    """Inference cố định weights, không nhận nhãn query hoặc gọi optimizer."""
    before = tensor_hash(model)
    model.eval()
    for parameter in model.parameters():parameter.grad = None
    logits = []
    with torch.inference_mode():
        for start in range(0,len(packets),physical):
            check()
            batch = collate_packets(packets[start:start+physical],device)
            z = model(batch["values"],batch["roles"],batch["slots"],batch["padding"])
            logits.extend(z[torch.arange(len(batch["queries"]),device=device),batch["queries"]].cpu().tolist())
    probabilities(logits)
    if tensor_hash(model) != before or any(p.grad is not None for p in model.parameters()):
        raise ValueError("Weights/gradient thay đổi trong frozen inference")
    return logits


def mechanism_report(logits:list[float], rows:list[dict[str,Any]]) -> dict[str,Any]:
    """Giữ cả K/m/joint và IID/stress; gate chính dùng toàn bộ5.000 episode."""
    value = mechanism_metrics(logits,rows)
    for name,group in (("joint",[(r["oracle"]["K"],r["oracle"]["m"]) for r in rows]),
                       ("distribution",["stress" if r["sidecar"]["stress"] else "iid" for r in rows])):
        value["by_"+name] = {}
        for key in sorted(set(group)):
            indices = [i for i,v in enumerate(group) if v == key]
            value["by_"+name][str(key)] = mechanism_metrics([logits[i] for i in indices],[rows[i] for i in indices])
    return value


def swap_report(a:list[float], b:list[float], pairs:list[dict[str,Any]]) -> dict[str,Any]:
    """Dấu, biên độ và Pearson Δp; giữ nguyên eligible từ oracle đã seal."""
    value = prior_swap_metrics(a,b,pairs)
    model = probabilities(b)[0]-probabilities(a)[0]
    oracle = np.asarray([r["oracle_b"]["probability"]-r["oracle_a"]["probability"] for r in pairs])
    mask = np.abs(oracle) >= .05
    value["delta_amplitude_quantiles"] = {"quantiles":[0.,.5,.95,1.],
        "model":np.quantile(np.abs(model[mask]),[0,.5,.95,1],method="linear").tolist() if mask.any() else None,
        "oracle":np.quantile(np.abs(oracle[mask]),[0,.5,.95,1],method="linear").tolist() if mask.any() else None}
    valid = int(mask.sum()) >= 2 and float(model[mask].std()) > 0 and float(oracle[mask].std()) > 0
    value["delta_pearson_correlation"] = float(np.corrcoef(model[mask],oracle[mask])[0,1]) if valid else None
    value["correlation_reason"] = None if valid else "INSUFFICIENT_OR_CONSTANT_DELTA"
    return value


def validation_summary(inputs:dict[str,Any], logits:dict[str,list[float]]) -> dict[str,Any]:
    """Eligibility chỉ từ synthetic validation, sau đó mới dùng2021 để rank."""
    expected = {"full","context_blind","swap_a","swap_b","market_2021"}
    if set(logits) != expected:raise ValueError("Thiếu job checkpoint validation")
    rows,pairs = inputs["corpora"]["synthetic_validation"],inputs["corpora"]["validation_swap"]
    synthetic = mechanism_report(logits["full"],rows)
    swap = swap_report(logits["swap_a"],logits["swap_b"],pairs)
    constant = float(sum(p*g[0] for p,g in zip(inputs["teacher"].pi,
                    [(mu,k) for mu in (.2,.4,.6,.8) for k in (2,8,32,128)])))
    constant_logits = [math.log(constant)-math.log1p(-constant)]*len(rows)
    control = mechanism_report(constant_logits,rows)
    flat = control["gate"] == "PASS" or swap["eligible_pairs"] < 200
    status = "INCONCLUSIVE_TEACHER_TOO_FLAT" if flat else "PASS" if synthetic["gate"] == swap["gate"] == "PASS" else "FAIL"
    if len(logits["market_2021"]) != len(inputs["selection_rows"]):raise ValueError("Sai mẫu số2021")
    records = [{"episode_id":r["query"]["episode_id"],"symbol":r["query"]["symbol"],
                "y":r["supervised_target"]["y"],"p":float(p)}
               for r,p in zip(inputs["selection_rows"],probabilities(logits["market_2021"])[0])]
    if len(records) != len(inputs["selection_rows"]):raise ValueError("Sai mẫu số2021")
    return {"synthetic":synthetic,"prior_swap":swap,"constant_control":control,
            "context_blind_control":mechanism_report(logits["context_blind"],rows),
            "mechanism_status":status,"eligible":status == "PASS",
            "market_2021":selection_metrics(records),"market_2021_records":records}


def selection(records:list[dict[str,Any]]) -> dict[str,Any]:
    """Không fallback market-best; buộc đủ60 report trước selection seal."""
    if {(r["seed"],r["step"]) for r in records} != {(s,t) for s in SEEDS for t in STEPS} or len(records) != 60:
        raise ValueError("Selection cần đủ60 checkpoint/report duy nhất")
    def key(row:dict[str,Any]) -> tuple:
        """Tie-break theo recipe, không P&L/test hoặc checkpoint cuối mặc định."""
        metrics = row["assessment"]["market_2021"]
        return (round(metrics["macro_log_loss"],12),round(metrics["macro_brier"],12),row["step"],SEEDS.index(row["seed"]))
    if any(type(r["assessment"]["eligible"]) is not bool or
           r["assessment"]["eligible"] != (r["assessment"]["mechanism_status"] == "PASS") for r in records):
        raise ValueError("Eligibility không khớp gate cơ chế")
    eligible = [row for row in records if row["assessment"]["eligible"]]
    def descriptor(row:dict[str,Any]) -> dict[str,Any]:
        """Bind weights và report đã đánh giá, không chỉ seed/step tự khai."""
        return {k:row[k] for k in ("seed","step","checkpoint","report")}
    return {"status":"SELECTED" if eligible else "NO_ELIGIBLE_CHECKPOINT",
            "global_candidate_or_none":descriptor(min(eligible,key=key)) if eligible else None,
            "per_seed_candidate_or_none":{str(seed):descriptor(min(group,key=key)) if
                (group := [r for r in eligible if r["seed"] == seed]) else None for seed in SEEDS},
            "eligibility_all_checkpoints":[{"seed":r["seed"],"step":r["step"],"eligible":r["assessment"]["eligible"],
                                            "mechanism_status":r["assessment"]["mechanism_status"]} for r in records],
            "ranking_key":["round(macro_log_loss_2021,12)","round(macro_brier_2021,12)","step","seed_order_17_42_73"]}
