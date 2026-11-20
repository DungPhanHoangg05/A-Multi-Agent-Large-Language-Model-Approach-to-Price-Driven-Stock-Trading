"""Biên dịch nguồn LaTeX chính bằng LuaLaTeX/Biber; không đọc hay chuyển Markdown."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


def main() -> None:
    """Ghi log tạm, dừng ngay khi lỗi; bản PDF đích chỉ cập nhật sau build thành công."""
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--engine', choices=('pdflatex', 'xelatex', 'lualatex'), default='pdflatex')
    parser.add_argument('--passes', type=int, default=4, choices=(2, 3, 4))
    parser.add_argument('--skip-bibliography', action='store_true')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[2]
    destination = (args.output_dir or source / 'build').resolve()
    destination.mkdir(parents=True, exist_ok=True)
    engine = shutil.which(args.engine)
    if engine is None:
        raise SystemExit(f'Thiếu {args.engine} trong PATH.')
    command = [engine, '--disable-installer', '-interaction=nonstopmode',
               '-halt-on-error', '-file-line-error', '-recorder',
               '-output-directory=' + str(destination), 'main.tex']
    for step in range(args.passes):
        result = subprocess.run(command, cwd=source, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        (destination / f'pass-{step + 1}.txt').write_bytes(result.stdout)
        if result.returncode:
            print(result.stdout.decode('utf-8', errors='replace')[-6000:])
            raise SystemExit(result.returncode)
        if step == 0 and not args.skip_bibliography and (destination / 'main.bcf').exists():
            executable = shutil.which('biber')
            if executable is None:
                raise SystemExit('Thiếu Biber trong PATH.')
            # Biber/Perl trên Windows có thể không mở được đường dẫn Unicode.
            # Chỉ đưa bản sao bcf/bib vào thư mục tạm ASCII; không sửa bibliography gốc.
            with TemporaryDirectory(prefix='thesis-biber-') as temporary:
                bibroot = Path(temporary)
                shutil.copyfile(destination / 'main.bcf', bibroot / 'main.bcf')
                shutil.copyfile(source / 'references.bib', bibroot / 'references.bib')
                bibliography = subprocess.run([executable, 'main'], cwd=bibroot,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for suffix in ['bbl', 'blg']:
                    if (bibroot / ('main.' + suffix)).exists():
                        shutil.copyfile(bibroot / ('main.' + suffix), destination / ('main.' + suffix))
            (destination / 'biber.txt').write_bytes(bibliography.stdout)
            if bibliography.returncode:
                print(bibliography.stdout.decode('utf-8', errors='replace')[-4000:])
                raise SystemExit(bibliography.returncode)
    final_log = (destination / 'main.log').read_text(encoding='utf-8', errors='replace')
    blockers = ['There were undefined references', 'Missing character:', 'LaTeX Error:']
    if any(item in final_log for item in blockers):
        raise SystemExit('Build còn lỗi tham chiếu/ký tự/LaTeX; xem main.log, chưa cập nhật PDF đích.')
    pdf = destination / 'main.pdf'
    if args.pdf:
        final = args.pdf.resolve()
        final.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pdf, final)
    print('Biên dịch thành công:', pdf)


if __name__ == '__main__':
    main()
