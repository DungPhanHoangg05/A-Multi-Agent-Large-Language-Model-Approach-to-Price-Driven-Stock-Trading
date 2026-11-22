"""Chiếu bảng FIN12 từ artifact đã khóa sang hai bản thảo tự chứa."""
from __future__ import annotations

import argparse
import io
from zipfile import ZipFile
from collections import Counter
import csv
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIN12_ARCHIVE = ROOT / 'evidence/fin12_audit.zip'
RECEIPT_SHA = 'd304f01ca78f3eef6666f14a6e39df60dd6dda4af3a8095c1a490ff9ec831c31'
EVIDENCE = ROOT / 'evidence/manuscript_evidence.json'
BASELINES = ROOT / 'outputs/revision/final_baselines_v1'
HISTORICAL = ROOT / 'outputs/revision/u09_manuscript_assets_v1/artifacts'
COMPONENT_ARCHIVE = ROOT / 'evidence/component_audit.zip'
COMPONENT_SHA = '003e258bb46c16cec256e9e073f4ef7d0f045780183361a9cdb2411d864cf4bf'
BASELINES_SHA = '0a20fbe49049dd61fae2eb8bf3289f65039395e6bcac6745b851a5a00d804226'
COMPONENT = {'AS': 'Our system', 'B': 'QuantAgent', 'logistic_price': 'Logistic-price',
             'constant_down_cash': 'CASH'}
CONTROLS = ('CASH_EVERY_CYCLE', 'ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS')
REFERENCES = {'bayesian_v1': 'original_common', 'C2': 'original_common',
              'A_tp_pool': 'original_common', 'B_semantic': 'original_common', 'MT_BICL': 'Fact_Anchor'}
STATISTICS_METHODS = ('C2', 'A_tp_pool', 'B_semantic')
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


def require(condition: bool, message: str) -> None:
    """Dừng chiếu bảng nếu nguồn và phạm vi không khớp."""
    if not condition:
        raise ValueError(message)


def verified_bytes(path: Path, binding: dict) -> bytes:
    """Đọc tệp theo hash và kích thước đã ghi."""
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == binding['sha256']
            and ('bytes' not in binding or len(raw) == binding['bytes']),
            f'Tệp không khớp hash hoặc kích thước: {path}')
    return raw


def baseline_rows() -> dict:
    """Đọc bảng đối chứng của nghiên cứu thành phần."""
    manifest = json.loads(verified_bytes(BASELINES / 'manifest.json', {'sha256': BASELINES_SHA}))
    bindings = {r['path']: r for r in manifest['outputs']}
    comparison = csv.DictReader(verified_bytes(BASELINES / 'main_comparison.csv',
                                               bindings['main_comparison.csv']).decode().splitlines())
    financial = csv.DictReader(verified_bytes(BASELINES / 'financial.csv',
                                              bindings['financial.csv']).decode().splitlines())
    accounts = {r['variant']: r for r in financial if r['cohort'] == 'all_102'}
    rows = {r['variant']: r for r in comparison if r['variant'] in COMPONENT}
    require(rows.keys() == COMPONENT.keys(), 'Thiếu đối chứng của nghiên cứu thành phần.')
    for method, row in rows.items():
        account = accounts[method]
        require(row['n_valid'] == '102' and row['n_accounts'] == account['n_accounts'] == '51'
                and row['mean_account_net_return_pct'] == account['mean_account_net_return_pct'],
                f'Mẫu số hoặc lợi nhuận đối chứng không khớp: {method}')
        row.update(mdd=account['mean_account_drawdown_pct'], held=account['mean_account_held_session_fraction'])
    return rows


def audit_evidence() -> dict:
    """Đối soát prompt thực gửi, dự báo và bảng nguồn từ các gói bằng chứng FIN15."""
    import sys
    sys.path.insert(0, str(ROOT))
    from core.research_results import ResearchResults
    from core.revision_r4_factorial import actual_text, factor_rows, prompt_parts

    with ZipFile(FIN12_ARCHIVE) as archive:
        def read_json(name: str, expected: dict) -> dict | list:
            """Đối chiếu từng thành viên với receipt trước khi dùng số liệu."""
            raw = archive.read(name)
            require(sha256(raw).hexdigest() == expected['sha256']
                    and len(raw) == expected.get('bytes', len(raw)), f'Sai nguồn FIN12: {name}')
            return json.loads(raw)

        receipt = read_json('receipt.json', {'sha256': RECEIPT_SHA})['payload']
        names = ('results.json', 'predictions.json', 'outcomes.json', 'cycles.json')
        results, predictions, outcomes, cycles = (
            read_json(name, receipt['artifacts'][name]) for name in names
        )
    methods = (*METHODS, *CONTROLS)
    indexed = {(r['point_id'], r['repeat'], r['method']): r for r in predictions}
    require(len(indexed) == len(predictions) and set(indexed) == {
        (p, r, m) for p in outcomes for r in range(3) for m in methods
    }, 'Lưới dự báo thiếu hoặc trùng khóa.')
    labeled = {p for p, r in outcomes.items() if r['target']['label_net'] is not None}
    for (point, _, _), row in indexed.items():
        target = outcomes[point]['target']
        require((row['label_net'], row['r_net']) == (target['label_net'], target['net_return'])
                and point == f"{row['symbol']}-{row['date']}", f'Nhãn hoặc lợi nhuận không khớp: {point}')

    account_groups: dict[tuple, set] = {}
    for row in cycles:
        key = (row['method'], row['repeat'], row['symbol'], row['fold'])
        account_groups.setdefault(key, set()).add(row['point_id'])
        require(row['action'] == indexed[row['point_id'], row['repeat'], row['method']]['final_action'],
                f"Lệnh trong sổ tài khoản không khớp dự báo: {row['point_id']}")
    cohort = {}
    for method in methods:
        for repeat in range(3):
            groups = [points for key, points in account_groups.items() if key[:2] == (method, repeat)]
            points = set().union(*groups)
            require(len(groups) == 45 and all(len(group) == 2 for group in groups)
                    and len(points) == 90 and points <= labeled, f'Mẫu tài khoản không khớp: {method}/{repeat}')
            cohort[method, repeat] = points
    require(all(points == cohort[methods[0], 0] for points in cohort.values()), 'Các phương pháp không cùng mẫu tài khoản.')

    rows = {}
    for summary in results['summary']:
        method = summary['method']
        records = {(p, r): indexed[p, r, method] for p in outcomes for r in range(3)}
        raw = sum(row['llm_response'] for row in records.values())
        fallbacks = sum(row['bypass'] for row in records.values())
        require((raw, fallbacks) == (summary['raw_decision_responses'], summary['bypass_forecasts'])
                and raw + fallbacks == 306, f'Số phản hồi hoặc fallback không khớp: {method}')
        baseline = REFERENCES.get(method)
        changes = [[p, r] for (p, r), row in sorted(records.items())
                   if baseline and row['final_action'] != indexed[p, r, baseline]['final_action']]
        require(all(records[p, r]['llm_response'] and not records[p, r]['bypass'] for p, r in changes),
                f'Fallback đổi hành động đối chứng: {method}')
        require(summary['primary_mean_account_return_pct'] is None
                and summary['primary_balanced_accuracy_pct'] is None, f'Phạm vi chỉ tiêu chính không khớp: {method}')
        rows[method] = {
            'return_pct': summary['complete_accounts_mean_account_return_pct'],
            'ba_pct': summary['complete_accounts_balanced_accuracy_pct'],
            'raw': raw, 'fallback': fallbacks, 'changes': changes, 'reference': baseline,
            'profiles': sorted({r.get('profile', 'deterministic control') for r in records.values()}),
        }
        if method in STATISTICS_METHODS:
            rows[method]['statistics_only_replies'] = sum(
                row['llm_response'] and row['prior_stats_ready'] is True
                and row['prior_examples_ready'] is False and row['effective_K'] == 0
                and row['prior_selected_ids'] == []
                for row in records.values()
            )

    with ZipFile(io.BytesIO(verified_bytes(COMPONENT_ARCHIVE, {'sha256': COMPONENT_SHA}))) as archive:
        audits = json.loads(archive.read('outputs/revision/fusion_prompt_audit_v1/audit.json'))
        original = json.loads(archive.read('outputs/revision/revision_minimal_final_v1/main_predictions.json'))
        dependence = json.loads(archive.read('outputs/revision/final_temporal_v1/primary_dependence.json'))
        prompt_counts = {}
        for request in audits['request_audit']:
            job = request['selected_job_id'] or ''
            if not (job.startswith('main__') and job.endswith('_AS_n0')):
                continue
            raw = archive.read(request['request_path'])
            require(sha256(raw).hexdigest() == request['request_file_sha256'], 'Prompt không khớp hash.')
            doc = json.loads(raw)
            unit_id = doc['context']['unit_id']
            parts = prompt_parts(actual_text(doc))
            require(doc['context']['variant'] == 'AS' and doc['context']['repeat'] == 0
                    and unit_id not in prompt_counts and '**TỔNG HỢP:' in parts['alpha']
                    and ' / ' in parts['alpha'], f'Prompt compact không đúng profile: {unit_id}')
            sentiment = parts['sentiment']
            missing = sentiment.startswith('Sentiment KHÔNG KHẢ DỤNG')
            require(missing or 'score=' in sentiment, f'Trạng thái sentiment không nhận dạng được: {unit_id}')
            prompt_counts[unit_id] = (factor_rows(parts['alpha']), missing)

    baselines = baseline_rows()
    for method, summary in baselines.items():
        points = {r['unit_id']: r for r in original if r['variant'] == method}
        require(set(points) == set(prompt_counts) and {
            f"{r['symbol']}-{r['date']}" for r in points.values()
        } == set(outcomes) and all(r['prediction'] in {'LONG', 'SHORT'} for r in points.values()),
                f'Mẫu điểm hoặc lệnh đối chứng không khớp: {method}')
        counts = Counter((r['label_net'], r['prediction'] == 'LONG') for r in points.values())
        require(tuple(counts[t] for t in (('UP', True), ('UP', False), ('DOWN', False), ('DOWN', True)))
                == tuple(int(summary[k]) for k in ('tp', 'fn', 'tn', 'fp')), f'Ma trận đối chứng không khớp: {method}')

    missing = sum(y for _, y in prompt_counts.values())
    factor_points = sum(x > 0 for x, _ in prompt_counts.values())
    historical_points = json.loads((HISTORICAL / 'points.json').read_bytes())
    historical_missing = sum(r['sentiment_unavailable'] for r in historical_points)
    require(len(historical_points) == len(outcomes) and {r['id'] for r in historical_points} == set(outcomes)
            and historical_missing == json.loads((HISTORICAL / 'support.json').read_bytes())['sentiment_missing'],
            'Mẫu sentiment lịch sử không khớp.')
    interval = next(r['percentile_95'] for r in dependence['cohorts']['all_102']['intervals'] if r['contrast'] == 'AS-B')
    historic_csv = ResearchResults(ROOT).artifact('predictions.csv')
    fpt = {float(r['r_net']) for r in csv.DictReader(historic_csv.decode().splitlines()) if r['point_id'] == 'FPT-2023-07-03'}
    require(len(fpt) == 1 and outcomes['FPT-2023-07-03']['reason'] == 'CORPORATE_ACTION_DURING_HOLDING',
            'Kết quả FPT giữa hai nghiên cứu không khớp.')
    coverage = results['coverage']
    require((len(prompt_counts),factor_points,missing,historical_missing) == (102,0,79,79)
            and (len(outcomes),len(labeled),coverage['complete_account_points'],coverage['forecast_slots'])
            == (102,96,90,2448) and results['primary_joint_family']['ci95'] is None
            and results['sensitivity']['complete_account_intersection']['ci95'] is None,
            'Các mẫu số và trạng thái chỉ tiêu không khớp bằng chứng đã khóa.')
    return {
        'fin12_receipt_sha256': RECEIPT_SHA, 'fin12_artifacts': receipt['artifacts'],
        'component': {'profile': 'main compact AS versus B', 'points': len(prompt_counts),
                      'prompts_with_factor_value_rows': factor_points, 'missing_sentiment': missing,
                      'ba_interval_pp': [100*x for x in interval]},
        'historical': {'missing_sentiment': historical_missing, 'fpt_return_pct': 100*fpt.pop()},
        'followup': {'coverage': {k: v for k, v in coverage.items() if isinstance(v, (int, bool))},
                     'primary_status': results['primary_joint_family']['status'],
                     'band_status': results['sensitivity']['complete_account_intersection']['status'],
                     'band_reasons': results['sensitivity']['complete_account_intersection']['reasons'],
                     'method_rows': rows},
    }


def read_results() -> dict:
    """Đọc bản chiếu đã khóa. Tùy chọn audit đối chiếu lại kho gốc."""
    source_map = json.loads((ROOT / 'scripts/thesis_docs/source-map.json').read_bytes())
    expected = source_map['fin15_outputs']['manuscript_evidence_sha256']
    data = json.loads(verified_bytes(EVIDENCE, {'sha256': expected}))
    require(data['fin12_receipt_sha256'] == RECEIPT_SHA, 'Bản chiếu không khớp receipt FIN12.')
    return data


def project_component(rows: dict) -> str:
    """Tái tạo bảng chính từ nguồn đối chứng được lưu trong Git."""
    out = [r'\begin{table}[!htb]', r'\centering\small', r'\setlength{\tabcolsep}{6pt}',
           r'\renewcommand{\arraystretch}{1.13}',
           r'\caption{Main component-study results at 102 paired cutoffs and 51 accounts per method.}',
           r'\label{tab:classification}', r'\begin{tabular}{@{}lrrrrrr@{}}', r'\toprule',
           r'& \multicolumn{3}{c}{Forecasts} & \multicolumn{3}{c}{Accounts}\\',
           r'\cmidrule(lr){2-4}\cmidrule(lr){5-7}',
           r'Method & Acc. (\%) & BA (\%) & LONGs & Net return (\%) & MDD (\%) & Held (\%)\\', r'\midrule']
    for method, name in COMPONENT.items():
        row = rows[method]
        values = [f"{100*float(row['accuracy']):.2f}", f"{100*float(row['balanced_accuracy']):.2f}",
                  row['predicted_long'], f"{float(row['mean_account_net_return_pct']):.3f}",
                  f"{float(row['mdd']):.2f}", f"{100*float(row['held']):.2f}"]
        out.append(' & '.join([name, *values])+r'\\')
    out.extend([r'\bottomrule', r'\end{tabular}', r'\par\smallskip',
                r'{\footnotesize BA is balanced accuracy. MDD is mean maximum daily-close drawdown.',
                r'Held is the mean share of observed sessions spent invested.\par}', r'\end{table}'])
    return '\n'.join(out)+'\n'


def project(result: dict) -> str:
    """Chiếu số liệu cả hai bản theo mẫu số và hành động đối chứng đã khóa."""
    coverage = result['coverage']
    rows = result['method_rows']
    lines = [r'% Bảng đối chiếu từ lần đánh giá bổ sung.', r'\begin{table}[!htb]',
             r'\centering\small\setlength{\tabcolsep}{3pt}',
             r'\caption{Follow-up BICL results and final-action changes.}\label{tab:bicl-complete-accounts}',
             r'\begin{tabular}{@{}lrrrrrr@{}}\toprule',
             r'& \multicolumn{2}{c}{Complete accounts} & \multicolumn{4}{c}{All 306 slots per method}\\',
             r'\cmidrule(lr){2-3}\cmidrule(lr){4-7}',
             r'Method & Return (\%) & BA (\%) & New replies & Fallbacks & Changes & Stock--dates\\\midrule']
    for method, name in METHODS.items():
        row = rows[method]
        changes = row['changes']
        counts = [str(len(changes)), str(len({p for p, _ in changes}))] if row['reference'] else [r'\textemdash']*2
        values = [f"{row['return_pct']:.4f}", f"{row['ba_pct']:.4f}", str(row['raw']), str(row['fallback']), *counts]
        lines.append(' & '.join([name, *values])+r'\\')
    lines.extend([r'\bottomrule\end{tabular}', r'\par\smallskip',
        r'{\footnotesize Return and balanced accuracy (BA) use '
        f"{coverage['complete_accounts_per_repeat']} accounts ({coverage['complete_account_points']} cutoffs) per repeat. "
        r'Changes compare final actions in the same repeat with Common for v1--v4 and Fact Anchor for v5. '
        r'Stock--dates counts distinct cutoffs with a change. '
        f"CASH returns {rows[CONTROLS[0]]['return_pct']:.4f}\\% and Always-LONG returns "
        f"{rows[CONTROLS[1]]['return_pct']:.4f}\\%; both score 50.00\\% BA on the same complete accounts.",
        statistics_note(rows) + r'\par}',
        r'\end{table}'])
    return '\n'.join(lines)+'\n'


def statistics_note(rows: dict) -> str:
    """Ghi rõ phạm vi của phản hồi có thống kê nhưng không có ví dụ truy xuất."""
    counts = [rows[method]['statistics_only_replies'] for method in STATISTICS_METHODS]
    require(counts == [rows[method]['raw'] for method in STATISTICS_METHODS],
            'Không phải mọi phản hồi v2, v3 và v4 đều chỉ có thống kê.')
    v2, v3, v4 = counts
    return (f'The prompts for all {v2}, {v3} and {v4} new replies in BICL v2, v3 and v4, '
            r'respectively, included historical statistics and zero retrieved examples ($K_{\mathrm{eff}}=0$).')


def project_plot_data(result: dict) -> str:
    """Lấy mẫu số, lợi nhuận và số fallback từ cùng snapshot FIN12."""
    coverage = result['coverage']
    by_method = result['method_rows']
    coverage_rows = ','.join(f'{label}/{coverage[key]}' for label, key in (
        ('Planned cutoffs', 'planned_points'), ('Valid execution labels', 'available_outcomes'),
        ('Cutoffs in complete accounts', 'complete_account_points'),
    ))
    plotted = ('original_fix', 'original_common', 'bayesian_v1', 'C2', 'A_tp_pool', 'B_semantic', 'MT_BICL')
    rows = ','.join(
        f"{METHODS[key]}/{by_method[key]['return_pct']:.6f}/"
        f"{by_method[key]['fallback']}" for key in plotted
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
    parser.add_argument('--audit', action='store_true',
                        help='Đối chiếu các bản ghi nguồn với bảng và dữ liệu hình FIN15')
    args = parser.parse_args()
    evidence = read_results()
    if args.audit:
        require(audit_evidence() == evidence, 'Bản chiếu không khớp bản ghi nguồn.')
    result = evidence['followup']
    projections = dict.fromkeys(TARGETS, project(result))
    projections['paper/content/tables/component/classification.tex'] = project_component(baseline_rows())
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
