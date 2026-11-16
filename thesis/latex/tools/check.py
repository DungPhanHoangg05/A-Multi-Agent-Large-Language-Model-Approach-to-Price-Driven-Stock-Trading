"""Kiểm tính toàn vẹn mốc chuyển nguồn và dependency LaTeX cục bộ."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile


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
    latex = Path(__file__).resolve().parents[1]
    root = latex.parent
    record = json.loads((latex / 'source-map.json').read_text(encoding='utf-8'))
    checked = 0
    archive = record.get('p8_archive')
    historical: dict[str, bytes] = {}
    if archive:
        archive_path = root / archive['path']
        if hashlib.sha256(archive_path.read_bytes()).hexdigest() != archive['sha256']:
            raise ValueError('Archive P8 khác hash đã khóa.')
        with ZipFile(archive_path) as bundle:
            for row in archive['members']:
                content = bundle.read(row['path'])
                if hashlib.sha256(content).hexdigest() != row['sha256']:
                    raise ValueError('Member archive khác byte gốc: ' + row['path'])
                historical[row['path']] = content
    for row in record['markdown_archive']:
        content = historical.get(row['path'])
        actual = hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest() if content is not None else lf_sha(root / row['path'])
        if actual != row['lf_sha256']:
            raise ValueError('Bản nháp lưu trữ đã đổi: ' + row['path'])
    if args.strict_cutover_targets:
        for row in record['latex_cutover']:
            content = historical.get(row['path'])
            actual = hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest() if content is not None else lf_sha(root / row['path'])
            if actual != row['lf_sha256']:
                raise ValueError('Nguồn P8 lưu trữ khác mốc chuyển: ' + row['path'])
    for row in record.get('markdown_navigation_updates', []):
        if lf_sha(root / row['path']) != row['lf_sha256']:
            raise ValueError('Bản điều hướng Markdown khác cập nhật đã ghi: ' + row['path'])
    if args.strict_current_targets:
        if 'current_latex' not in record:
            raise ValueError('Chưa khóa hash nguồn LaTeX sau biên tập.')
        for row in record['current_latex']:
            if lf_sha(root / row['path']) != row['lf_sha256']:
                raise ValueError('Nguồn LaTeX khác mốc biên tập: ' + row['path'])
    for path in latex.rglob('*.tex'):
        if 'build' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        for command, target in re.findall(r'\\(input|includegraphics|addbibresource)(?:\[[^\]]*\])?\{([^}]+)\}', text):
            if '#' in target:
                continue
            dependency = latex / target
            if command == 'input' and not dependency.suffix:
                dependency = dependency.with_suffix('.tex')
            if not dependency.is_file() or not dependency.resolve().is_relative_to(root.resolve()):
                raise ValueError('Dependency thiếu hoặc ra ngoài cây thesis: ' + target)
            checked += 1
    main_source = (latex / 'main.tex').read_text(encoding='utf-8')
    chapter_paths = sorted((latex / 'chapters').glob('*.tex'))
    if len(chapter_paths) != 6:
        raise ValueError('Bản nộp phải có đúng sáu chương.')
    if archive and ((latex / 'appendices').exists() or (root / 'appendices').exists() or r'\appendix' in main_source):
        raise ValueError('Phụ lục còn trong cây bản nộp hoặc main.tex.')
    for path in chapter_paths:
        target = path.relative_to(latex).with_suffix('').as_posix()
        if main_source.count(r'\input{' + target + '}') != 1:
            raise ValueError('Nội dung thiếu hoặc ghép lặp: ' + target)
    # So mọi ô đã chọn với cả bảng P8 trong archive và nguồn LaTeX hiện tại.
    table_map = root / 'assets/tables/concise_results.source.json'
    if table_map.exists() and historical:
        projection = json.loads(table_map.read_text(encoding='utf-8'))
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
        for row in projection['rows']:
            if row['original'] not in cells(tables[row['source_table'] - 1]):
                raise ValueError('Dòng nguồn bảng không khớp P8: ' + row['table'])
            selected = [row['original'][i] for i in row['columns']]
            matches = [table for table in current_tables if r'\label{' + row['table'] + '}' in table]
            if selected != row['cells'] or len(matches) != 1 or selected not in cells(matches[0]):
                raise ValueError('Ô bảng biên tập khác nguồn: ' + row['table'])
        print(f'PASS: {len(projection["rows"])} dòng bảng chiếu nguyên ô từ P8, gồm đủ 20 contrast cells.')
    print(f'PASS: {len(record["markdown_archive"])} bản nháp lưu trữ; {checked} dependency cục bộ; sáu chương ghép một lần; không phụ lục trong bản nộp. Archive không là input biên dịch.')


if __name__ == '__main__':
    main()
