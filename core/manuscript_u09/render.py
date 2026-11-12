"""Sinh bảng, macro và figure U09; mọi metric lấy từ artifact, không ước lượng lại."""
from __future__ import annotations

import csv
import io
import math
from typing import Any

from core.manuscript_u09.sources import ENDPOINTS, METHODS, PACKAGE, PREFIX, encoded, require

LABELS = dict(zip(METHODS, ("Native", "Common", "Bayes v1", "C2", "A pool", "B semantic",
    "MT-BICL", "Fact anchor", "CASH", "Always-LONG")))
TOKENS = ("Native", "Common", "VOne", "CTwo", "APool", "BSemantic", "MT", "FactAnchor", "Cash", "AlwaysLong")


def number(value: Any, scale: float = 1., digits: int = 3) -> str:
    """Giữ NA, đơn vị phần trăm/đpt và zero đúng rounding; không nhận bool/nonfinite."""
    if value is None:
        return "NA"
    require(type(value) in (int, float) and math.isfinite(value) and math.isfinite(scale), "Ô số không hữu hạn hoặc sai kiểu")
    converted = value * scale
    require(math.isfinite(converted), "Ô số tràn sau đổi đơn vị")
    if abs(converted) < .5 * 10 ** (-digits):
        converted = 0.
    return f"{converted:.{digits}f}"


def escape(value: str) -> str:
    """Escape ID/text nguồn, không escape công thức LaTeX do generator sở hữu."""
    mapping = {"\\": r"\textbackslash{}", "_": r"\_", "&": r"\&", "%": r"\%",
        "$": r"\$", "#": r"\#", "{": r"\{", "}": r"\}", "^": r"\textasciicircum{}", "~": r"\textasciitilde{}"}
    return "".join(mapping.get(c, c) for c in value)


def at(document: Any, pointer: str) -> Any:
    """Đọc JSON pointer cho provenance từng ô, giữ nguyên scalar/null."""
    for part in pointer.strip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        document = document[int(part)] if isinstance(document, list) else document[part]
    return document


def panel(title: str, headers: list[str], rows: list[list[str]]) -> str:
    """Bảng cột cố định, phát hiện sai chiều trước khi ghi nguồn LaTeX."""
    require(bool(rows) and all(len(r) == len(headers) for r in rows), "Số cột bảng không khớp")
    return "\n".join([r"\textbf{" + title + r"}\par\smallskip", r"\begin{tabular}{l" + "r"*(len(headers)-1) + "}",
        r"\hline", " & ".join(headers) + r" \\", r"\hline",
        *[" & ".join(row) + r" \\" for row in rows], r"\hline", r"\end{tabular}\par\medskip"])


def table(label: str, caption: str, panels: list[str], note: str) -> bytes:
    """Float tách namespace U09, không thay label hoặc macro của study gốc."""
    return ("\n".join([r"\begin{table}[p]", r"\centering\small", r"\setlength{\tabcolsep}{3pt}",
        r"\renewcommand{\arraystretch}{1.12}", r"\caption{" + caption + "}", r"\label{tab:u09-" + label + "}",
        *panels, r"\begin{minipage}{\textwidth}\footnotesize " + note + r"\end{minipage}", r"\end{table}", ""])).encode()


def csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    """CSV xác định cho companion; null để trống, không ghi chuỗi nan."""
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


class Cells:
    """Gắn mỗi số render với package/member/pointer, literal, scale và đơn vị."""

    def __init__(self, result: dict[str, Any], facts: dict[str, Any]) -> None:
        """Không giữ state global giữa các lượt build hoặc thread."""
        self.documents = {"results": result, "support": facts}
        self.rows: list[dict[str, Any]] = []

    def value(self, output: str, pointer: str, unit: str, scale: float = 1., digits: int = 3) -> str:
        """Literal được đọc qua pointer, không nhập lại số headline bằng tay."""
        group, path = pointer.lstrip("/").split("/", 1)
        value = at(self.documents[group], path)
        rendered = number(value, scale, digits)
        self.rows.append({"output": output, "source_package": PACKAGE if group == "results" else "DERIVED_SUPPORT",
            "source_member": PREFIX + "results.json" if group == "results" else "support.json",
            "pointer": "/" + path, "value": value, "unit": unit, "scale": scale,
            "digits": digits, "rendered": rendered})
        return rendered


def figures(result: dict[str, Any], cells: Cells) -> dict[str, bytes]:
    """Đổi nhãn figure sang tiếng Anh từ cùng contrasts; không bootstrap hoặc chọn band."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    outputs = {}
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 9, "svg.fonttype": "none",
            "svg.hashsalt": "manuscript_u09_v1", "axes.spines.top": False, "axes.spines.right": False}):
        fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.7), layout="constrained")
        for family, ax in enumerate(axes):
            for y in range(5):
                index = family * 5 + y
                row = result["contrasts"][index]
                point, low, high = (row[k] for k in ("effect_pp", "band95_low_pp", "band95_high_pp"))
                if point is None:
                    ax.text(.5, y, "NA", transform=ax.get_yaxis_transform(), va="center")
                elif low is None:
                    ax.plot(point, y, "o", color="#175c80")
                    ax.annotate("band NA", (point, y), xytext=(5, 5), textcoords="offset points", fontsize=7)
                else:
                    ax.errorbar(point, y, xerr=[[point-low], [high-point]], fmt="o", capsize=3, color="#175c80")
            ax.axvline(0, color="#777777", linewidth=.8)
            ax.set_yticks(range(5), [LABELS[r["method"]] for r in result["contrasts"][family*5:family*5+5]])
            ax.invert_yaxis()
            ax.set_ylim(4.5, -.5)
            ax.set_title("(a) vs Native" if family == 0 else "(b) vs Common")
            ax.set_xlabel("Difference in mean account return (pp)")
            ax.grid(axis="x", alpha=.2)
        fig.suptitle("Extension study: paired return contrasts", fontsize=11)
        fig.supxlabel("Descriptive 95% simultaneous bands; six exposed folds; one upstream realization.", fontsize=8)
        for suffix, metadata in (("svg", {"Date": None, "Creator": "manuscript_u09_v1"}),
                ("png", {"Software": "manuscript_u09_v1"})):
            output = "return_contrasts." + suffix
            stream = io.BytesIO()
            fig.savefig(stream, format=suffix, dpi=180, metadata=metadata)
            outputs[output] = stream.getvalue()
            for index in range(10):
                for field in ("effect_pp", "band95_low_pp", "band95_high_pp"):
                    cells.value(output, f"results/contrasts/{index}/{field}", "percentage_points", digits=6)
        plt.close(fig)
    return outputs


def render(bundle: dict[str, Any]) -> dict[str, bytes]:
    """Sinh toàn bộ namespace U09 từ một bundle đã verify, không ghi file tại đây."""
    result, facts = bundle["result"], bundle["facts"]
    cells = Cells(result, facts)
    outputs: dict[str, bytes] = {}

    def val(output: str, pointer: str, unit: str = "percent", scale: float = 1., digits: int = 3) -> str:
        """Tên ngắn cục bộ cho ô có provenance, tránh state ngoài bundle."""
        return cells.value(output, pointer, unit, scale, digits)

    scope = [("Market points", "points"), ("Symbols", "symbols"), ("Dates", "dates"), ("Folds", "folds"),
        ("Independent-capital accounts per repeat", "accounts"), ("Upstream realizations per point", "upstream_realizations"),
        ("Upstream executions", "upstream_executions"), ("Points without available sentiment", "sentiment_missing")]
    rows = [[name, val("scope.tex", "support/" + key, "count", digits=0)] for name, key in scope]
    rows += [["Decision repeats", val("scope.tex", "results/repeats", "count", digits=0)],
        ["Research forecast slots (eight roles)", val("scope.tex", "results/coverage/complete", "count", digits=0)],
        ["Raw Decision responses", val("scope.tex", "support/raw_decision_responses", "count", digits=0)],
        ["HTTP attempts (including retired)", val("scope.tex", "results/telemetry/http_attempts", "count", digits=0)]]
    outputs["scope.tex"] = table("scope", "Extension study U08/U09: distinct support and execution counts.",
        [panel("Recorded support", ["Quantity", "Count"], rows)],
        "This study shares a test calendar with the original study, not its responses. "
        "Three Decision repeats do not add market observations or upstream realizations. "
        "BHN contributes six points in three recent folds; the other eight symbols contribute twelve each. "
        "Unavailable sentiment is missing input, not neutral news.")

    rows, classification, economics, repeat_rows = [], [], [], []
    for i, method in enumerate(METHODS):
        base = f"results/summary/{i}/"
        rows.append([LABELS[method], val("comparison.tex", base+"mean_account_return_pct"),
            val("comparison.tex", base+"balanced_accuracy_pct", digits=2),
            val("comparison.tex", base+"long_rate", scale=100., digits=2),
            val("comparison.tex", base+"raw_decision_responses", "count", digits=0),
            val("comparison.tex", base+"bypass_forecasts", "count", digits=0),
            val("comparison.tex", base+"n_points", "points_per_repeat", digits=0)])
        classification.append([LABELS[method], val("classification.tex", base+"accuracy", scale=100., digits=2),
            val("classification.tex", base+"balanced_accuracy_pct", digits=2), val("classification.tex", base+"mcc", "ratio"),
            *[val("classification.tex", base+k, scale=100., digits=2) for k in ("f1_positive", "f1_negative", "macro_f1")]])
        economics.append([LABELS[method], *[val("economics.tex", base+k, unit, scale=scale, digits=digits)
            for k, unit, scale, digits in (("mean_daily_mdd_pct", "percent", 1., 3),
                ("mean_cycle_end_mdd_pct", "percent", 1., 3), ("mean_held_session_fraction", "percent", 100., 2),
                ("mean_fee_vnd", "thousand_VND", .001, 3), ("mean_slippage_vnd", "thousand_VND", .001, 3),
                ("mean_turnover_over_initial", "initial_capital_multiple", 1., 3))]])
        selected = [index for index, r in enumerate(result["per_repeat"]) if r["method"] == method]
        selected.sort(key=lambda index: result["per_repeat"][index]["repeat"])
        repeat_rows.append([LABELS[method], *[val("repeats.tex", f"results/per_repeat/{index}/"+field, digits=digits)
            for field, digits in (("mean_account_return_pct", 3), ("balanced_accuracy_pct", 2)) for index in selected],
            val("repeats.tex", base+"repeat_return_sd_ddof1")])
    outputs["comparison.tex"] = table("comparison", "Extension study: ten registered roles and cycle controls.",
        [panel("Paired support: 102 points per repeat", ["Role", "Return (\\%)", "BA (\\%)", "LONG (\\%)", "Raw", "Bypass", "$N$/repeat"], rows)],
        "Return is the equal mean of 51 symbol--fold accounts after averaging three repeats within each account, not a portfolio. "
        "BA is the mean of three per-repeat pooled balanced accuracies. Raw and bypass counts are out of 306 slots per role; "
        "bypass includes registered no-LLM controls. Always-LONG enters at Open(t+1), exits at Close(t+3), with full costs each cycle; "
        "it is not continuous buy-and-hold. Native and Common are different baselines; all eight research roles have negative mean returns.")
    outputs["classification.tex"] = table("classification", "Extension study: class-aware metrics on the same 102 market points.",
        [panel("Mean of per-repeat metrics", ["Role", "Acc. (\\%)", "BA (\\%)", "MCC", "$F1_U$ (\\%)", "$F1_D$ (\\%)", "Macro F1 (\\%)"], classification)],
        "Metrics are averaged after per-repeat evaluation, not pooled as 306 independent market points. "
        "NA is undefined and is not replaced by zero; constant controls have undefined MCC. "
        "Per-class support, missing-class reasons and per-symbol/fold metrics remain in the source companions.")
    outputs["economics.tex"] = table("economics", "Extension study: risk, capital use and transaction costs.",
        [panel("Mean account quantities", ["Role", "EOD MDD (\\%)", "Cycle MDD (\\%)", "Held (\\%)", "Fees (kVND)", "Slip. (kVND)", "Turnover/$C_0$"], economics)],
        "Accounts reset at 50 million VND per symbol/fold/repeat. Held includes observed sessions between queries; "
        "it is not the LONG forecast rate. Fees are 0.25\\% and slippage is 0.10\\% each side. "
        "Daily-close NAV and cycle-end drawdown are distinct. Annualized return/Sharpe/Sortino remain null; "
        "cycle ratios and undefined reasons are supplied by the source companions. Live fills and corporate actions are not certified.")
    outputs["repeats.tex"] = table("repeats", "Extension study: three Decision repeats conditional on one upstream realization.",
        [panel("Return percent and BA percent", ["Role", "$R_1$", "$R_2$", "$R_3$", "$BA_1$", "$BA_2$", "$BA_3$", "$s_R$"], repeat_rows)],
        "Each repeat covers all 102 points and 51 accounts. The return sample SD is read from the recorded ddof=1 summary. "
        "Repeats quantify conditional Decision variability, not upstream variance or extra independent market observations. "
        "The original study's two nine-unit execution panels remain separate.")

    panels = []
    for endpoint in ENDPOINTS:
        for family, baseline in (("system", "original_fix"), ("method", "original_common")):
            selected = [(i, r) for i, r in enumerate(result["contrasts"]) if r["endpoint"] == endpoint and r["family"] == family]
            rows = [[LABELS[r["method"]], *[val("contrasts.tex", f"results/contrasts/{i}/"+k, "percentage_points")
                for k in ("effect_pp", "band95_low_pp", "band95_high_pp")]] for i, r in selected]
            title = ("Return" if endpoint == ENDPOINTS[0] else "BA") + " vs " + LABELS[baseline] + " (pp)"
            panels.append(panel(title, ["Method", "Difference", "Lower", "Upper"], rows))
    outputs["contrasts.tex"] = table("contrasts", "Extension study: all twenty registered endpoint contrasts.", panels,
        "Differences are method minus baseline in percentage points. Bands are the recorded descriptive 95\\% simultaneous "
        "standardized max-deviation bands across all twenty endpoints/contrasts, circular fold block L2, 10,000 draws, "
        "PCG64 seed 20261110. Six exposed temporal clusters do not support calibrated significance or coverage claims. "
        "NA bands remain NA; no new resampling or family selection is performed.")
    rows = [[LABELS[r["method"]] + " vs " + LABELS[r["baseline"]],
        val("bridge.tex", f"results/bridge/{i}/return_difference_pp", "percentage_points"),
        val("bridge.tex", f"results/bridge/{i}/BA_difference_pp", "percentage_points"),
        val("bridge.tex", f"results/bridge/{i}/same_action_forecasts", "count", digits=0)] for i, r in enumerate(result["bridge"])]
    outputs["bridge.tex"] = table("bridge", "Extension study: dependency bridges and action agreement.",
        [panel("Descriptive differences", ["Bridge", "$\\Delta R$ (pp)", "$\\Delta BA$ (pp)", "Same /306"], rows)],
        "Native-to-Common changes both alpha projection and prompt; Common-to-Fact anchor changes the anchor. "
        "MT-BICL versus Fact anchor describes the revision/utility step. These bridges are not fully isolated component interventions.")

    support_rows = []
    for i, row in enumerate(facts["domain_support"]):
        if row["method"] not in METHODS[:8]:
            continue
        base = f"support/domain_support/{i}/"
        support_rows.append([LABELS[row["method"]], row["domain"],
            *[val("support.tex", base+k, "count", digits=0) for k in ("points", "raw_responses", "bypass", "effective_K_defined")],
            val("support.tex", base+"effective_K_min", "count", digits=0), val("support.tex", base+"effective_K_max", "count", digits=0)])
    outputs["support.tex"] = table("support", "Extension study: effective domain support and fallback coverage.",
        [panel("CORE4: 144 slots/role; OOD5: 162 slots/role", ["Role", "Domain", "Points", "Raw", "Bypass", "$K$ recorded", "$K_{min}$", "$K_{max}$"], support_rows)],
        "CORE4 is FPT/MWG/VCB/VNM; OOD5 is BHN/CMG/HVN/MBB/VJC. Counts come from frozen predictions, not new retrieval. "
        "Recorded K means that a numeric effective-K value exists; NA is unrecorded/not applicable, not zero support. "
        "Raw plus bypass covers every slot. Bypass reasons, raw proposals, policy actions and trace hashes remain available in the sources.")

    for endpoint, filename in zip(ENDPOINTS, ("sensitivity_return.tex", "sensitivity_ba.tex")):
        rows = []
        for index, row in enumerate(result["contrasts"]):
            if row["endpoint"] != endpoint:
                continue
            values = []
            for length in (1, 2, 3):
                group = "results/primary_joint_family" if length == 2 else f"results/sensitivity/BLOCK_LENGTH_{length}"
                if at(cells.documents, group+"/ci95") is None:
                    values.append(val(filename, group+"/ci95", "percentage_points"))
                else:
                    low = val(filename, group+f"/ci95/{index}/0", "percentage_points")
                    high = val(filename, group+f"/ci95/{index}/1", "percentage_points")
                    values.append("["+low+", "+high+"]")
            rows.append([LABELS[row["method"]], LABELS[row["baseline"]],
                val(filename, f"results/contrasts/{index}/effect_pp", "percentage_points"), *values])
        outputs[filename] = table(filename.removesuffix(".tex").replace("_", "-"),
            "Extension study: " + ("return" if endpoint == ENDPOINTS[0] else "BA") + " block-length sensitivity (pp).",
            [panel("All predeclared L1/L2/L3 bands", ["Method", "Baseline", "Effect", "L1", "L2 (primary)", "L3"], rows)],
            "All bounds are read from the frozen artifacts, with no re-estimation or choice of the most favorable band. "
            "Leave-one-fold/symbol-out effects and the fixed CORE4 subset are supplied as machine-readable companions. "
            "All sensitivity remains descriptive on an exposed historical cohort.")

    panels = []
    for endpoint in ENDPOINTS:
        for family in ("system", "method"):
            rows = []
            for index, row in enumerate(result["contrasts"]):
                if row["endpoint"] != endpoint or row["family"] != family:
                    continue
                base = "results/sensitivity/CORE4_FIXED_SUBSET/"
                effect = val("sensitivity_core4.tex", base+f"point/{index}", "percentage_points")
                if result["sensitivity"]["CORE4_FIXED_SUBSET"]["ci95"] is None:
                    low = high = val("sensitivity_core4.tex", base+"ci95", "percentage_points")
                else:
                    low = val("sensitivity_core4.tex", base+f"ci95/{index}/0", "percentage_points")
                    high = val("sensitivity_core4.tex", base+f"ci95/{index}/1", "percentage_points")
                rows.append([LABELS[row["method"]], effect, low, high])
            title = ("Return" if endpoint == ENDPOINTS[0] else "BA") + " vs " + ("Native" if family == "system" else "Common")
            panels.append(panel(title + " (pp)", ["Method", "Difference", "Lower", "Upper"], rows))
    outputs["sensitivity_core4.tex"] = table("sensitivity-core4", "Extension study: fixed CORE4 subset sensitivity.", panels,
        "FPT/MWG/VCB/VNM, " + val("sensitivity_core4.tex", "results/sensitivity/CORE4_FIXED_SUBSET/points", "count", digits=0)
        + " points and " + val("sensitivity_core4.tex", "results/sensitivity/CORE4_FIXED_SUBSET/accounts", "count", digits=0)
        + " accounts per repeat. This predeclared subset is nonprimary. Bounds use the recorded L2 joint family; "
        "they are descriptive and cannot establish general superiority or replace the full-cohort result.")

    macros = []
    for token, pointer in (("Points", "support/points"), ("Accounts", "support/accounts"), ("Symbols", "support/symbols"),
            ("Dates", "support/dates"), ("Folds", "support/folds"), ("MissingSentiment", "support/sentiment_missing"),
            ("UpstreamRealizations", "support/upstream_realizations"), ("DecisionRepeats", "results/repeats"),
            ("ForecastSlots", "results/coverage/complete")):
        macros.append(r"\newcommand{\Unified" + token + "}{" + val("summary_numbers.tex", pointer, "count", digits=0) + "}")
    for i, token in enumerate(TOKENS):
        for suffix, field, digits in (("Return", "mean_account_return_pct", 3), ("BA", "balanced_accuracy_pct", 2),
                ("Raw", "raw_decision_responses", 0), ("Bypass", "bypass_forecasts", 0)):
            macros.append(r"\newcommand{\Unified" + token + suffix + "}{" + val("summary_numbers.tex",
                f"results/summary/{i}/" + field, "count" if digits == 0 else "percent", digits=digits) + "}")
    for i, row in enumerate(result["contrasts"]):
        token = TOKENS[METHODS.index(row["method"])] + TOKENS[METHODS.index(row["baseline"])]
        token += "Return" if row["endpoint"] == ENDPOINTS[0] else "BA"
        for suffix, field in (("Effect", "effect_pp"), ("Low", "band95_low_pp"), ("High", "band95_high_pp")):
            macros.append(r"\newcommand{\Unified" + token + suffix + "}{" + val("summary_numbers.tex",
                f"results/contrasts/{i}/" + field, "percentage_points") + "}")
    outputs["summary_numbers.tex"] = ("\n".join(macros) + "\n").encode()
    outputs.update(figures(result, cells))
    outputs["support.json"] = encoded(facts)
    outputs["points.json"] = encoded(bundle["points"])
    outputs["numeric_cells.json"] = encoded(cells.rows)
    outputs["supplement/sensitivity.json"] = encoded(result["sensitivity"])
    sensitivity_rows = []
    for kind in ("LEAVE_ONE_FOLD_OUT", "LEAVE_ONE_SYMBOL_OUT"):
        for group, values in result["sensitivity"][kind].items():
            require(len(values) == 20, "Sensitivity thiếu endpoint")
            for index, row in enumerate(result["contrasts"]):
                sensitivity_rows.append({"analysis": kind, "omitted": group, "family": row["family"],
                    "method": row["method"], "baseline": row["baseline"], "endpoint": row["endpoint"],
                    "effect_pp": values[index]})
    outputs["supplement/leave_one_out.csv"] = csv_bytes(sensitivity_rows)
    for name in ("summary.csv", "contrasts.csv", "bridge.csv", "per_repeat.csv", "classification_by_repeat.csv",
            "classification_by_group.csv", "accounts.csv"):
        outputs["supplement/" + name] = bundle["analysis"][PREFIX + name]
    return outputs
