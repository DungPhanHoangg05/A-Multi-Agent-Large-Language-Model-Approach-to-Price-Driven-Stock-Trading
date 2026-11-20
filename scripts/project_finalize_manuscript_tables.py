"""Chiếu bảng FIN12 từ artifact đã khóa sang hai bản thảo tự chứa."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'outputs/finalize/fin12_v1'
RECEIPT_SHA = 'd304f01ca78f3eef6666f14a6e39df60dd6dda4af3a8095c1a490ff9ec831c31'
TARGETS = ('paper/content/tables/finalize_results.tex', 'thesis/latex/tables/finalize_results.tex')
METHODS = {
    'original_fix': 'Our system',
    'original_common': 'Our system (Common)',
    'bayesian_v1': 'BICL v1',
    'C2': 'BICL v2',
    'A_tp_pool': 'BICL v3',
    'B_semantic': 'BICL v4',
    'MT_BICL': 'BICL v5',
    'Fact_Anchor': 'Fact Anchor',
}


def read_results() -> dict:
    """Đọc đúng kết quả gốc trước khi chiếu bảng hoặc hình."""
    receipt_bytes = (SOURCE / 'receipt.json').read_bytes()
    if sha256(receipt_bytes).hexdigest() != RECEIPT_SHA:
        raise ValueError('Receipt FIN12 khác bản đã khóa.')
    binding = json.loads(receipt_bytes)['payload']['artifacts']['results.json']
    raw = (SOURCE / 'results.json').read_bytes()
    if binding != {'sha256': sha256(raw).hexdigest(), 'bytes': len(raw)}:
        raise ValueError('Kết quả FIN12 khác checksum trong receipt.')
    return json.loads(raw)


def project(result: dict) -> str:
    """Giữ nguyên miền hỗ trợ và đơn vị của kết quả nguồn."""
    coverage = result['coverage']
    rows = {row['method']: row for row in result['summary']}
    def values(method: str) -> str:
        """Chỉ lấy hai kết quả trên giao đủ tài khoản và số bypass."""
        row = rows[method]
        if row['primary_mean_account_return_pct'] is not None or row['primary_balanced_accuracy_pct'] is not None:
            raise ValueError('Trạng thái chỉ tiêu chính FIN12 khác phạm vi bảng.')
        return (
            f"{row['complete_accounts_mean_account_return_pct']:.4f} & "
            f"{row['complete_accounts_balanced_accuracy_pct']:.4f} & {row['bypass_forecasts']}"
        )
    lines = [r'% Chiếu từ kết quả đã khóa của lần đánh giá bổ sung.', r'\begin{table}[htbp]',
             r'\centering\small', r'\caption{Follow-up BICL evaluation. Mean net return and balanced accuracy (BA) use accounts with both trading cycles. Bypass counts cover all forecast slots per method.}\label{tab:bicl-complete-accounts}',
             r'\begin{tabular}{lrrr}\toprule',
             r'Method & Return (\%) & BA (\%) & Bypasses \\ \midrule']
    lines.extend(f'{name} & {values(method)}' + r' \\' for method, name in METHODS.items())
    lines.extend([r'\bottomrule\end{tabular}', r'\par\smallskip', (
        f"{{\\footnotesize Each repeat includes {coverage['complete_accounts_per_repeat']} of {coverage['planned_accounts_per_repeat']} "
        f"accounts with both cycles, covering {coverage['complete_account_points']} cutoffs shared by all methods. "
        f"Across the full sample, {coverage['available_outcomes']} of {coverage['planned_points']} cutoffs have valid execution labels.\\par}}"
    ), r'\end{table}'])
    return '\n'.join(lines) + '\n'


def project_plot_data(result: dict) -> str:
    """Lấy mẫu số, lợi nhuận và số fallback từ cùng snapshot FIN12."""
    coverage = result['coverage']
    by_method = {row['method']: row for row in result['summary']}
    coverage_rows = ','.join(f'{label}/{coverage[key]}' for label, key in (
        ('Planned cutoffs', 'planned_points'), ('Valid execution labels', 'available_outcomes'),
        ('Cutoffs in complete accounts', 'complete_account_points'),
    ))
    plotted = ('original_fix', 'original_common', 'bayesian_v1', 'C2', 'A_tp_pool', 'B_semantic', 'MT_BICL')
    rows = ','.join(
        f"{METHODS[key]}/{by_method[key]['complete_accounts_mean_account_return_pct']:.6f}/"
        f"{by_method[key]['bypass_forecasts']}" for key in plotted
    )
    return (
        '% Chiếu từ kết quả đã kiểm checksum của lần đánh giá bổ sung.\n'
        f'\\def\\FinCoverageRows{{{coverage_rows}}}\n'
        f'\\def\\FinMethodRows{{{rows}}}\n'
    )


def main() -> None:
    """Cập nhật hoặc đối chiếu bảng và dữ liệu hình ở hai bản thảo."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = read_results()
    projections = dict.fromkeys(TARGETS, project(result))
    projections['thesis/latex/tables/followup_plot_data.tex'] = project_plot_data(result)
    for relative, expected in projections.items():
        path = ROOT / relative
        if args.check:
            if path.read_text(encoding='utf-8') != expected:
                raise ValueError('Tệp khác bản chiếu FIN12: ' + relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding='utf-8', newline='\n')
    print('Bảng và dữ liệu hình khớp bằng chứng FIN12.')


if __name__ == '__main__':
    main()
