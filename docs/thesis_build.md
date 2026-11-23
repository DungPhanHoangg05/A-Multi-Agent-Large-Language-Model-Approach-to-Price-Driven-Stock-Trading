# Biên dịch khóa luận

Nén nội dung [thư mục thesis](../thesis/) sao cho `main.tex` ở gốc ZIP.
Trên Overleaf, chọn `main.tex` làm **Main document** và dùng **pdfLaTeX** hoặc
**XeLaTeX**. Overleaf xử lý Biber khi build.
[Thiết lập tệp chính](https://docs.overleaf.com/getting-started/recompiling-your-project/the-main-document)
· [Chọn trình biên dịch](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler).

Từ gốc kho mã, dùng MiKTeX hoặc TeX Live có Biber và các gói trong `preamble.tex`:

```powershell
py -3.13 scripts/thesis_docs/build.py --engine pdflatex --output-dir tmp/pdfs/thesis-pdftex
py -3.13 scripts/thesis_docs/build.py --engine xelatex --output-dir tmp/pdfs/thesis-xetex
py -3.13 -X utf8 scripts/thesis_docs/check.py --strict-cutover-targets --strict-current-targets
```

Script chạy bốn lượt biên dịch và một lượt Biber. Có thể dùng `--pdf` để
sao chép PDF sau khi build thành công. Bản xem riêng hai bìa dùng
[covers-preview.tex](../thesis/covers-preview.tex) từ thư mục `thesis/`.

Toàn văn dùng A4 dọc, chữ Latin Modern 12 pt, giãn dòng 1,5, hai bìa và
sáu chương. Sơ đồ tổng thể là TikZ và có thể sửa trực tiếp trong
[assets/diagrams](../thesis/assets/diagrams). Bảng FIN12 đã chiếu từ receipt và
được đưa vào nguồn. Biên dịch chỉ cần nội dung trong thư mục `thesis/`.

## Đối soát và truy vết

[PDF FIN15](../outputs/thesis/thesis.pdf) được build bằng pdfLaTeX.
Tag `thesis-review-20261117-r1` và [manifest lịch sử](https://github.com/DungPhanHoangg05/A-Multi-Agent-Large-Language-Model-Approach-to-Price-Driven-Stock-Trading-in-the-Vietnamese-Stock-Ma/blob/0b19e9fc4b285be63bc452068ec6ab261206744d/thesis/release/manifest.json)
giữ đúng bản 67 trang trước FIN15.
`check.py` xác minh archive P8, tính đầy đủ của sáu chương, các đường dẫn
LaTeX, 68 dòng số liệu lưu trữ và 54 dòng còn trình bày, bao gồm 20 ô
so sánh. Gói và bản nháp Markdown phục vụ truy vết, tách khỏi đường biên
dịch.

Notice [QuantAgent MIT](../thesis/latex/licenses/QuantAgent-MIT.txt) giữ theo upstream.
Bản PDF là bản thảo khóa luận.

<a id="ban-truoc-fin15"></a>

## Tra cứu bản trước FIN15

Các chương Markdown gốc nằm trong [gói P8](../evidence/thesis/archive/p8-source.zip).
Để xem bản biên tập, mã vẽ F09/F10, bản xem trước và PDF cũ ở đúng
đường dẫn, mở một checkout riêng từ gốc kho mã.

```powershell
git worktree add --detach ../fin15-history de5d0d13ef6617ed2eaff1e3dd2bdd7f40e3390d
```
