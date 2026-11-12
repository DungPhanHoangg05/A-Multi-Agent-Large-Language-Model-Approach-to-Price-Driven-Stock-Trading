"""Xuất bảng/figure có nguồn, giữ null và các kết quả âm để bàn giao U10."""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

from core.unified_contracts import json_bytes


def write_csv(path: Path, rows: list[dict]) -> None:
    """CSV UTF-8/LF xác định; null để trống, trường lồng giữ JSON nguyên nghĩa."""
    columns = list(dict.fromkeys(k for row in rows for k in row))
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict, list)) else v for k, v in row.items()})
    path.write_bytes(stream.getvalue().encode("utf-8"))


def number(value: Any, digits: int = 3) -> str:
    """Không biến undefined thành số zero trong báo cáo."""
    return "NA" if value is None else f"{value:.{digits}f}"


def report(result: dict, destination: Path) -> None:
    """Sinh nội dung từ JSON, không gõ tay headline hoặc gán band thành superiority."""
    joint = result["primary_joint_family"]
    lines = ["# U09 — Phân tích paired research102", "",
        "Historical exploratory trên cohort đã exposed; sáu fold lịch, ba Decision repeat/một upstream realization.",
        "Return là mean đều 51 tài khoản mã/fold, mỗi tài khoản mean ba repeat; không phải portfolio return.",
        "LONG all-in fractional vào Open(t+1), ra Close(t+3), phí 0,25% và slippage 0,10% mỗi chiều; SHORT=CASH.", "",
        "| Vai trò | Mean account return % | BA % | Accuracy % | MCC | F1 UP | F1 DOWN | LONG /306 | Raw Decision | Bypass |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in result["summary"]:
        lines.append("| " + " | ".join([row["method"], number(row["mean_account_return_pct"]), number(row["balanced_accuracy_pct"]),
            number(row["accuracy"] * 100.) if row["accuracy"] is not None else "NA", number(row["mcc"]),
            number(row["f1_positive"]), number(row["f1_negative"]), str(row["long_forecasts"]),
            str(row["raw_decision_responses"]), str(row["bypass_forecasts"])]) + " |")
    lines += ["", "## Hai family đã đăng ký", "",
        "Effect là method trừ baseline, đơn vị điểm phần trăm. Band đồng thời chung 20 endpoint/contrast; bridge và controls không thêm vào family để chọn kết quả thuận lợi.",
        "", "| Family | Method | Baseline | Endpoint | Effect đpt | Band95% |", "| --- | --- | --- | --- | ---: | --- |"]
    for row in result["contrasts"]:
        band = "NA" if row["band95_low_pp"] is None else f"[{number(row['band95_low_pp'])}; {number(row['band95_high_pp'])}]"
        lines.append(f"| {row['family']} | {row['method']} | {row['baseline']} | {row['endpoint']} | {number(row['effect_pp'])} | {band} |")
    lines += ["", f"Band status: `{joint['status']}`; joint finite {joint['joint_finite_draws']}/10000; undefined {joint['undefined_draws']}.",
        f"Lý do: {', '.join(joint['reasons']) or 'Đủ điều kiện band mô tả'}; cột SD zero: {joint['zero_sd_columns']}.",
        "Không redraw hoặc bỏ cột suy biến. SD ddof1 trên draw joint finite; higher quantile95% của max |draw−estimate|/SD, cùng PCG64 seed20261110, circular fold block L2.",
        "Sáu fold đã exposed chỉ hỗ trợ sensitivity, không chứng nhận coverage/power hoặc p-value xác nhận.", "",
        "## Bridge có dependency", "", "| Method | Baseline | D return đpt | D BA đpt | Trùng action /306 |",
        "| --- | --- | ---: | ---: | ---: |"]
    for row in result["bridge"]:
        lines.append(f"| {row['method']} | {row['baseline']} | {number(row['return_difference_pp'])} | {number(row['BA_difference_pp'])} | {row['same_action_forecasts']} |")
    lines += ["", "Bridge là mô tả. MT so với Fact_Anchor mới tách phần revision/utility khỏi chênh lệch của anchor; không quy toàn bộ D so baseline cho student.",
        "", "## Kinh tế và sensitivity", "",
        "accounts.csv giữ 51×3 account cho từng vai trò/control, reset 50 triệu VND từng mã/fold/repeat; cycles.csv giữ phí/slippage/turnover và quantity fractional.",
        "daily_nav.csv giữ đầy đủ phiên cash/held giữa hai query; EOD MTM MDD và cycle-end MDD tách riêng. Sharpe chu kỳ dùng SD ddof1; Sortino dùng RMS phần âm trên mọi cycle, MAR0; annualized=null.",
        "results.json giữ L1/L3, leave-one-fold-out, leave-one-symbol-out và CORE4 đã định trước. Các draw duplicate fold là bản sao account reset, không nối sáu fold thành tài khoản mới.",
        "BA/confusion được tính riêng từng repeat, mean metrics sau đó; không pool 306 forecast làm 306 mẫu thị trường độc lập. Các metric thiếu class/mẫu số zero giữ null kèm lý do.",
        "", "## Coverage và provenance", "",
        "Đủ 102/102 planned points và 2448/2448 active slots; không có missing-action imputation. BHN chỉ có ba fold sau, không padding thành CASH ở ba fold đầu.",
        "prior_traces.json giữ trace dedup và predictions.csv giữ trace hash, effective K/age/similarity khi có, cùng raw proposal/veto/final. Regret không được ghi trong trace cho null với lý do.",
        "Brier chỉ dùng numeric student/teacher đã ghi và đúng nhãn, trên eligible support; không chuyển confidence LLM thành probability, không gán probability cho fallback.",
        "Retrieval/prior/MT ablation panels và continuous hold chưa thực thi theo protocol; CASH và ALWAYS_LONG là cycle controls cùng 102 query, không gọi continuous buy-and-hold.",
        f"Ledger giữ {result['telemetry']['http_attempts']} HTTP attempts, gồm {result['coverage']['source_raw_http_retired']} raw đã nghỉ sau reset được người dùng yêu cầu; không bỏ chi phí hoặc lấy response cũ vào active dataset.",
        "", "## Giới hạn", "", *["- " + value for value in result["limitations"]],
        "", "Native row-wise causal FAIL; whole-system causal NOT_CERTIFIED. Kết quả có điều kiện trên reports/prices/vendor execution assumptions, không phải kiểm chứng live fills hoặc dự báo chưa exposed.",
        "", "![Hai family return](return_contrasts.svg)", "",
        "Đầu ra JSON/CSV/figure có thể dùng cho U10 sau nghiệm thu; lượt này không sửa bản thảo bài báo.", ""]
    (destination / "report.md").write_bytes("\n".join(lines).encode("utf-8"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "unified_analysis_v1"
    rows = result["contrasts"][:10]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), layout="constrained", sharey=True)
    for index, ax in enumerate(axes):
        selected = rows[index*5:(index+1)*5]
        for y, row in enumerate(selected):
            point = row["effect_pp"]
            if row["band95_low_pp"] is None: ax.plot(point, y, "o", color="#176b87")
            else: ax.errorbar(point, y, xerr=[[point-row["band95_low_pp"]], [row["band95_high_pp"]-point]], fmt="o", capsize=4, color="#176b87")
        ax.axvline(0, color="#777", linewidth=1)
        ax.set_yticks(range(5), [v["method"] for v in selected])
        ax.set_title("So " + selected[0]["baseline"]); ax.grid(axis="x", alpha=.2)
        ax.set_xlabel("D mean account return (điểm phần trăm)")
    axes[0].invert_yaxis()
    fig.suptitle("Research102 — mô tả độ nhạy; band NA nếu family suy biến")
    fig.savefig(destination / "return_contrasts.svg", metadata={"Date": None})
    fig.savefig(destination / "return_contrasts.png", dpi=160, metadata={"Software": "unified_analysis_v1"})
    plt.close(fig)


def write_outputs(destination: Path, result: dict, artifacts: dict) -> None:
    """Mọi artifact xác định theo input/source; không dùng giờ chạy vào nội dung."""
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "results.json").write_bytes(json_bytes(result))
    (destination / "prior_traces.json").write_bytes(json_bytes(artifacts["prior_traces"]))
    for key in ("predictions", "accounts", "daily_nav", "cycles"):
        write_csv(destination / (key + ".csv"), artifacts[key])
    for filename, rows in (("summary.csv", result["summary"]), ("contrasts.csv", result["contrasts"]),
            ("bridge.csv", result["bridge"]), ("classification_by_repeat.csv", result["classification_by_repeat"]),
            ("classification_by_group.csv", result["classification_by_group"]), ("per_repeat.csv", result["per_repeat"])):
        write_csv(destination / filename, rows)
    report(result, destination)
