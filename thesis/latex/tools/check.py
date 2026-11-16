"""Kiểm tính toàn vẹn mốc chuyển nguồn và dependency LaTeX cục bộ."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def lf_sha(path: Path) -> str:
    """Hash nội dung LF để không coi newline checkout Windows là thay đổi văn bản."""
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def main() -> None:
    """Không dùng Markdown để build hoặc tự ghi đè LaTeX đã biên tập."""
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict-cutover-targets', action='store_true')
    args = parser.parse_args()
    latex = Path(__file__).resolve().parents[1]
    root = latex.parent
    record = json.loads((latex / 'source-map.json').read_text(encoding='utf-8'))
    checked = 0
    for row in record['markdown_archive']:
        if lf_sha(root / row['path']) != row['lf_sha256']:
            raise ValueError('Bản nháp lưu trữ đã đổi: ' + row['path'])
    if args.strict_cutover_targets:
        for row in record['latex_cutover']:
            if lf_sha(root / row['path']) != row['lf_sha256']:
                raise ValueError('Nguồn LaTeX khác mốc chuyển: ' + row['path'])
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
    for path in sorted((latex / 'chapters').glob('*.tex')) + sorted((latex / 'appendices').glob('*.tex')):
        target = path.relative_to(latex).with_suffix('').as_posix()
        if main_source.count(r'\input{' + target + '}') != 1:
            raise ValueError('Nội dung thiếu hoặc ghép lặp: ' + target)
    print(f'PASS: {len(record["markdown_archive"])} bản nháp lưu trữ; {checked} dependency cục bộ; 6 chương/6 phụ lục xuất hiện một lần. LaTeX là nguồn bản nộp chính.')


if __name__ == '__main__':
    main()
