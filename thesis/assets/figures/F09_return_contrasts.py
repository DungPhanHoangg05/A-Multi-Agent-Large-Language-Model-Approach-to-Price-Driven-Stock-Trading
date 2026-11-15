"""Vẽ contrast đã khóa của U09, không tái lấy mẫu hoặc chạy mô hình."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "docs/plan/week12/unified_analysis_results.zip"
MEMBER = "outputs/unified_integration/u09_analysis_r1/results.json"
PACKAGE_SHA256 = "e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9"
RESULT_SHA256 = "3136ab9bdeab377196236e1a01402646257ec3beb251877702dbc86e1e67e31f"
METHODS = ("bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL")
LABELS = ("Bayesian v1", "C2", "A_tp_pool", "B_semantic", "MT-BICL")


def read_results() -> dict:
    """Kiểm byte gói ngoài/member trước khi đọc số, không sửa bằng chứng."""
    with PACKAGE.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != PACKAGE_SHA256:
            raise ValueError("Gói U09 khác hash đã khóa")
    with zipfile.ZipFile(PACKAGE) as archive:
        raw = archive.read(MEMBER)
    if hashlib.sha256(raw).hexdigest() != RESULT_SHA256:
        raise ValueError("Kết quả U09 khác hash đã khóa")
    return json.loads(raw)


def main() -> None:
    """Xuất PDF/SVG cùng nội dung và PNG xem trước, không sinh draw mới."""
    result = read_results()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "pdf.fonttype": 42, "svg.fonttype": "none"})
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7), sharex=True, sharey=True)
    for ax, baseline, title, color in zip(
        axes, ("original_fix", "original_common"),
        ("A. Against Native (system comparison)", "B. Against Common (method comparison)"),
        ("#245b82", "#9a4f15"),
    ):
        rows = [next(r for r in result["contrasts"] if r["baseline"] == baseline
                     and r["method"] == method
                     and r["endpoint"] == "account_return_percentage_points") for method in METHODS]
        for index, row in enumerate(rows):
            point, low, high = (row[k] for k in ("effect_pp", "band95_low_pp", "band95_high_pp"))
            if row["band_status"] != "DESCRIPTIVE_BANDS" or low is None or high is None:
                raise ValueError("Thiếu band đã lưu, không được tự tạo band")
            ax.errorbar(point, index, xerr=[[point-low], [high-point]], fmt="o",
                        color=color, ecolor=color, capsize=4, markersize=5, linewidth=1.7)
            ax.text(-1.19, index+0.28, f"{point:+.3f} [{low:+.3f}, {high:+.3f}]",
                    fontsize=8, color="#333333")
        ax.axvline(0, color="#777777", linestyle="--", linewidth=1)
        ax.set_title(title, fontsize=10, loc="left", pad=15)
        ax.set_xlim(-1.22, 0.72)
        ax.set_ylim(4.65, -0.6)
        ax.set_yticks(range(5), LABELS)
        ax.tick_params(axis="y", labelleft=True)
        ax.set_xlabel("Mean account-return difference (pp)")
        ax.grid(axis="x", color="#e5e5e5", linewidth=0.6)
        ax.set_axisbelow(True)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
    fig.suptitle("Historical-context study: paired return contrasts", x=0.05, ha="left", fontsize=13)
    fig.text(0.05, 0.025, "102 points | 51 accounts | 3 Decision repeats | Saved bands from the joint 20-cell family\n"
             "Descriptive sensitivity only; six exposed folds. Positive differences favor the extension.", fontsize=9)
    fig.subplots_adjust(left=0.13, right=0.98, top=0.82, bottom=0.23, wspace=0.38)
    target = Path(__file__).with_suffix("")
    fig.savefig(target.with_suffix(".pdf"), metadata={"Title": "F09: paired return contrasts", "CreationDate": None})
    fig.savefig(target.with_suffix(".svg"), metadata={"Date": None})
    fig.savefig(target.with_suffix(".png"), dpi=160)
    plt.close(fig)
    print("Đã xuất F09 từ đúng mười contrast return đã lưu; không tạo phân tích mới.")


if __name__ == "__main__":
    main()
