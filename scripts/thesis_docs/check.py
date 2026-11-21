"""Kiểm tính toàn vẹn mốc chuyển nguồn và dependency LaTeX cục bộ."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile
from collections import Counter


def lf_sha(path: Path) -> str:
    """Hash nội dung LF để không coi newline checkout Windows là thay đổi văn bản."""
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def main() -> None:
    """Không dùng Markdown để build hoặc tự ghi đè LaTeX đã biên tập."""
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict-cutover-targets', action='store_true')
    parser.add_argument('--strict-current-targets', action='store_true')
    args = parser.parse_args()
    tools = Path(__file__).resolve().parent
    repo = tools.parents[1]
    root = repo / 'thesis'
    latex = root / 'latex'
    archive_home = repo / 'docs/plan/thesis'
    record = json.loads((tools / 'source-map.json').read_text(encoding='utf-8'))
    checked = 0
    archive = record['p8_archive']
    archive_path = archive_home / archive['path']
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != archive['sha256']:
        raise ValueError('Archive P8 khác hash đã khóa.')
    historical: dict[str, bytes] = {}
    with ZipFile(archive_path) as bundle:
        for row in archive['members']:
            content = bundle.read(row['path'])
            if hashlib.sha256(content).hexdigest() != row['sha256']:
                raise ValueError('Member archive khác byte gốc: ' + row['path'])
            historical[row['path']] = content
    for row in record['markdown_archive']:
        content = historical[row['path']]
        if hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest() != row['lf_sha256']:
            raise ValueError('Bản nháp lưu trữ đã đổi: ' + row['path'])
    if args.strict_cutover_targets:
        for row in record['latex_cutover']:
            content = historical[row['path']]
            if hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest() != row['lf_sha256']:
                raise ValueError('Nguồn P8 lưu trữ khác mốc chuyển: ' + row['path'])
    if args.strict_current_targets:
        if 'current_latex' not in record:
            raise ValueError('Chưa khóa hash nguồn LaTeX sau biên tập.')
        for row in record['current_latex']:
            if lf_sha(root / row['path']) != row['lf_sha256']:
                raise ValueError('Nguồn LaTeX khác mốc biên tập: ' + row['path'])
        if lf_sha(root / 'references.bib') != record['current_references_lf_sha256']:
            raise ValueError('Bibliography khác mốc biên tập.')
    for path in root.rglob('*.tex'):
        text = path.read_text(encoding='utf-8')
        for command, target in re.findall(r'\\(input|includegraphics|addbibresource)(?:\[[^\]]*\])?\{([^}]+)\}', text):
            if '#' in target:
                continue
            dependency = root / target
            if command == 'input' and not dependency.suffix:
                dependency = dependency.with_suffix('.tex')
            if not dependency.is_file() or not dependency.resolve().is_relative_to(root.resolve()):
                raise ValueError('Dependency thiếu hoặc ra ngoài cây thesis: ' + target)
            checked += 1
    main_source = (root / 'main.tex').read_text(encoding='utf-8')
    chapter_paths = sorted((latex / 'chapters').glob('*.tex'))
    if len(chapter_paths) != 6:
        raise ValueError('Bản nộp phải có đúng sáu chương.')
    if archive and ((latex / 'appendices').exists() or (root / 'appendices').exists() or r'\appendix' in main_source):
        raise ValueError('Phụ lục còn trong cây bản nộp hoặc main.tex.')
    for path in chapter_paths:
        target = path.relative_to(root).with_suffix('').as_posix()
        if main_source.count(r'\input{' + target + '}') != 1:
            raise ValueError('Nội dung thiếu hoặc ghép lặp: ' + target)
    # So mọi ô đã chọn với cả bảng P8 trong archive và nguồn LaTeX hiện tại.
    table_map = archive_home / 'assets/tables/concise_results.source.json'
    if table_map.exists() and historical:
        projection = json.loads(table_map.read_text(encoding='utf-8'))
        expected_rows = {'tab:component': 10, 'tab:numeric': 4, 'tab:smallpanels': 7,
                         'tab:factorial': 7, 'tab:context': 10, 'tab:vsnative': 5,
                         'tab:vscommon': 5, 'tab:coverage': 8, 'tab:execution': 12}
        if dict(Counter(row['table'] for row in projection['rows'])) != expected_rows:
            raise ValueError('Ánh xạ bảng thiếu/thừa dòng hoặc không đủ family20.')
        source_bytes = historical[projection['source']]
        if hashlib.sha256(source_bytes.replace(b'\r\n', b'\n')).hexdigest() != projection['source_lf_sha256']:
            raise ValueError('Hash bản nháp nguồn bảng không khớp archive.')
        original = historical['latex/chapters/05_experiments.tex'].decode('utf-8')
        tables = re.findall(r'\\begin\{longtable\}.*?\\end\{longtable\}', original, re.S)
        current = (latex / 'chapters/05_experiments.tex').read_text(encoding='utf-8')
        def cells(table: str) -> list[list[str]]:
            """Bỏ khoảng trắng dàn trang, giữ nguyên nội dung từng ô."""
            return [[cell.strip() for cell in line.strip().removesuffix(r'\\').split(' & ')]
                    for line in table.splitlines() if ' & ' in line and line.strip().endswith(r'\\')]
        current_tables = re.findall(r'\\begin\{table\}.*?\\end\{table\}', current, re.S)
        display_names = {
            'Full': 'Our system', 'Base': 'QuantAgent', 'Native': 'Our system',
            'Common': 'Our system (Common)', 'Bayesian v1': 'BICL v1', 'C2': 'BICL v2',
            r'A\_\allowbreak{}tp\_\allowbreak{}pool': 'BICL v3',
            r'B\_\allowbreak{}semantic': 'BICL v4', 'MT-BICL': 'BICL v5',
            'NA': r'\textemdash',
            'upstream': 'Regenerated reports', 'factorial': 'Fixed reports',
            'B': 'QuantAgent', 'AS': 'Our system', 'A': 'Alpha only',
            'S': 'Sentiment only', 'P': 'Past-donor alpha and sentiment',
            'reference': 'Reference', r'pending\_\allowbreak{}t2': 'Pending settlement',
            r'advance\_\allowbreak{}on\_\allowbreak{}demand': 'On-demand advance',
            r'advance\_\allowbreak{}auto': 'Automatic advance',
            r'lower\_\allowbreak{}cost': 'Lower costs', r'higher\_\allowbreak{}cost': 'Higher costs',
            r'sell\_\allowbreak{}charge\_\allowbreak{}10bp': 'Sell charge of 10 bp',
            r'no\_\allowbreak{}fill\_\allowbreak{}proxy': 'Missed fills proxy',
            r'delayed\_\allowbreak{}proxy': 'Delayed fills proxy',
            r'lot100\_\allowbreak{}cap1pct': 'Lot-size and capacity limits',
            'combined': 'Combined assumptions',
            r'all\_\allowbreak{}entries\_\allowbreak{}missed': 'All entries missed',
        }
        # Vẫn kiểm mọi dòng gốc. Bản thảo lược riêng các đối chứng cơ học.
        displayed_count = 0
        for row in projection['rows']:
            if row['original'] not in cells(tables[row['source_table'] - 1]):
                raise ValueError('Dòng nguồn bảng không khớp P8: ' + row['table'])
            selected = [row['original'][i] for i in row['columns']]
            if selected != row['cells']:
                raise ValueError('Ánh xạ cột khác bảng đã lưu: ' + row['table'])
            matches = [table for table in current_tables if r'\label{' + row['table'] + '}' in table]
            if row['table'] == 'tab:numeric':
                if matches:
                    raise ValueError('Bảng selector độc lập chỉ thuộc bản lưu trữ.')
                continue
            if (row['table'] == 'tab:component' and selected[0] not in {'Full', 'Base'}) or (
                row['table'] == 'tab:context' and selected[0] in {'CASH', 'Always-LONG cycles'}
            ):
                if any(c[0] == selected[0] for table in matches for c in cells(table)):
                    raise ValueError('Đối chứng đã lược vẫn xuất hiện trong bản thảo: ' + selected[0])
                continue
            displayed = [display_names.get(cell, cell) for cell in selected]
            if len(matches) != 1 or displayed not in cells(matches[0]):
                raise ValueError('Ô bảng biên tập khác nguồn: ' + row['table'])
            displayed_count += 1
        print(f'PASS: {len(projection["rows"])} dòng gốc P8 và {displayed_count} dòng trình bày khớp nguồn, gồm đủ 20 ô so sánh.')
    print(f'PASS: {len(record["markdown_archive"])} bản nháp lưu trữ; {checked} dependency cục bộ; sáu chương ghép một lần; không phụ lục trong bản nộp. Archive không là input biên dịch.')


if __name__ == '__main__':
    main()
