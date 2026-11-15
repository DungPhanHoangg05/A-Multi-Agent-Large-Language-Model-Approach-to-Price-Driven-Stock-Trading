"""Vẽ độ phủ phản hồi và nhánh policy từ số đếm U09 đã lưu."""
from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from F09_return_contrasts import read_results


def main() -> None:
    """Giữ riêng mẫu số 102 điểm và 306 slot, không đo lại hiệu suất."""
    result = read_results()
    summaries = {r["method"]: r for r in result["summary"]}
    methods = ("bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL")
    names = ("Bayesian v1", "C2", "A_tp_pool", "B_semantic", "MT-BICL")
    active = [summaries[m]["raw_decision_responses"] // 3 for m in methods]
    bypass = [summaries[m]["bypass_forecasts"] // 3 for m in methods]
    if any(a+b != 102 for a, b in zip(active, bypass)):
        raise ValueError("Độ phủ không khớp 102 điểm")
    reasons = summaries["MT_BICL"]["policy_reasons"]
    counts = [reasons["BYPASS_QUERY_FEATURE_UNAVAILABLE"]+reasons["BYPASS_UTILITY_UNSUPPORTED"],
              reasons["KEEP_PROPOSED_SAME"], reasons["REJECT_NONPOSITIVE_Q10_DELTA_U"],
              reasons["ACCEPT_POSITIVE_Q10_DELTA_U"]]
    if sum(counts) != 306 or counts[-1] != 4:
        raise ValueError("Số đếm policy không khớp nguồn đã khóa")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "pdf.fonttype": 42, "svg.fonttype": "none"})
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7), gridspec_kw={"width_ratios": [1, 1]})
    left, right = axes
    left.barh(range(5), active, color="#245b82", label="New Decision reply")
    left.barh(range(5), bypass, left=active, color="#d9dfe3", label="Bypass / reuse")
    for i, (a, b) in enumerate(zip(active, bypass)):
        left.text(104, i, f"{a} / {b}", va="center", fontsize=9)
    left.set_yticks(range(5), names)
    left.set_xlim(0, 125)
    left.set_xticks([0, 25, 50, 75, 100])
    left.invert_yaxis()
    left.set_xlabel("Unique points (of 102); label = new / bypass")
    left.set_title("A. Extension response coverage", loc="left", fontsize=11, pad=16)
    left.legend(loc="lower center", bbox_to_anchor=(0.5, -0.37), ncol=1, frameon=False, fontsize=9)
    right.barh(range(4), counts, color=["#a6b0b8", "#245b82", "#b16b31", "#3a7e5d"])
    for i, count in enumerate(counts):
        right.text(count+4, i, str(count), va="center")
    right.set_yticks(range(4), ["Bypass to anchor", "Same proposal / anchor", "Reject proposed change", "Accept proposed change"])
    right.set_xlim(0, 220)
    right.invert_yaxis()
    right.set_xlabel("MT-BICL forecast slots (of 306)")
    right.set_title("B. MT policy: final = anchor in 302/306", loc="left", fontsize=11, pad=16)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="x", color="#e5e5e5", linewidth=0.6)
        ax.set_axisbelow(True)
    fig.suptitle("Historical-context study: coverage and action retention", x=0.04, ha="left", fontsize=13)
    fig.text(0.04, 0.025, "102 market points | 3 Decision repeats | One shared upstream realization per point\n"
             "Response coverage is not incremental accuracy. Bypasses remain in the primary results.", fontsize=9)
    fig.subplots_adjust(left=0.12, right=0.98, top=0.82, bottom=0.32, wspace=0.85)
    target = Path(__file__).with_suffix("")
    fig.savefig(target.with_suffix(".pdf"), metadata={"Title": "F10: context coverage and policy actions", "CreationDate": None})
    fig.savefig(target.with_suffix(".svg"), metadata={"Date": None})
    fig.savefig(target.with_suffix(".png"), dpi=160)
    plt.close(fig)
    print("Đã xuất F10 từ số đếm nguồn; không chạy policy hoặc suy luận mới.")


if __name__ == "__main__":
    main()
