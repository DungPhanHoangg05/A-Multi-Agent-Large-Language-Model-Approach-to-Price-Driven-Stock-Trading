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


def project() -> str:
    """Giữ nguyên miền hỗ trợ và đơn vị của kết quả nguồn."""
    receipt_bytes = (SOURCE / 'receipt.json').read_bytes()
    if sha256(receipt_bytes).hexdigest() != RECEIPT_SHA:
        raise ValueError('Receipt FIN12 khác bản đã khóa.')
    binding = json.loads(receipt_bytes)['payload']['artifacts']['results.json']
    raw = (SOURCE / 'results.json').read_bytes()
    if binding != {'sha256': sha256(raw).hexdigest(), 'bytes': len(raw)}:
        raise ValueError('Kết quả FIN12 khác checksum trong receipt.')
    result = json.loads(raw)
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
    lines = [r'% Chiếu từ results.json đã khóa trong receipt FIN12.', r'\begin{table}[htbp]',
             r'\centering\small', r'\caption{Repaired BICL study. Mean net account return and balanced accuracy (BA) use the common complete-account subset. Bypass counts cover all planned forecasts per method.}\label{tab:fin12-repaired}',
             r'\begin{tabular}{lrrr}\toprule',
             r'Method & Return (\%) & BA (\%) & Bypasses \\ \midrule']
    lines.extend(f'{name} & {values(method)}' + r' \\' for method, name in METHODS.items())
    lines.extend([r'\bottomrule\end{tabular}', r'\par\smallskip', (
        f"{{\\footnotesize {coverage['complete_accounts_per_repeat']}/{coverage['planned_accounts_per_repeat']} complete accounts per repeat, "
        f"{coverage['complete_account_points']} shared cutoffs. {coverage['available_outcomes']}/{coverage['planned_points']} cutoffs have valid labels. "
        f"The full-cohort return and BA are NA.\\\\}}"
    ), r'\end{table}'])
    return '\n'.join(lines) + '\n'


def main() -> None:
    """Cập nhật hoặc đối chiếu hai bản sao dùng khi biên dịch độc lập."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = project()
    for relative in TARGETS:
        path = ROOT / relative
        if args.check:
            if path.read_text(encoding='utf-8') != expected:
                raise ValueError('Bảng khác bản chiếu FIN12: ' + relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding='utf-8', newline='\n')
    print('Hai bảng trình bày khớp bằng chứng FIN12.')


if __name__ == '__main__':
    main()
