# Biên dịch khóa luận

Điểm vào toàn văn là [thesis/main.tex](../main.tex). Có thể tạo dự án
Overleaf từ [gói nguồn khóa luận](../../output/overleaf/thesis-fin15-overleaf.zip).
Chọn `main.tex` làm **Main document** và dùng **pdfLaTeX** hoặc **XeLaTeX**.
Gói chứa nguồn, hình và bibliography của bản thảo. Overleaf xử lý Biber khi build.
[Thiết lập tệp chính](https://docs.overleaf.com/getting-started/recompiling-your-project/the-main-document)
· [Chọn trình biên dịch](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler).

Từ gốc kho mã, dùng MiKTeX hoặc TeX Live có Biber và các gói trong `preamble.tex`:

```powershell
py -3.13 thesis/latex/tools/build.py --engine pdflatex --output-dir tmp/pdfs/thesis-pdftex
py -3.13 thesis/latex/tools/build.py --engine xelatex --output-dir tmp/pdfs/thesis-xetex
py -3.13 -X utf8 thesis/latex/tools/check.py --strict-cutover-targets --strict-current-targets
```

Script chạy bốn lượt biên dịch và một lượt Biber. Có thể dùng `--pdf` để
sao chép PDF sau khi build thành công. Bản xem riêng hai bìa dùng
[covers-preview.tex](../covers-preview.tex) từ thư mục `thesis/`.

Toàn văn dùng A4 dọc, chữ Latin Modern 12 pt, giãn dòng 1,5, hai bìa và
sáu chương. Sơ đồ tổng thể là TikZ và có thể sửa trực tiếp trong
[assets/diagrams](../assets/diagrams/). Bảng FIN12 đã chiếu từ receipt và
được đưa vào nguồn. Biên dịch chỉ cần nội dung trong thư mục `thesis/`.

## Đối soát và truy vết

[PDF FIN15](../../output/pdf/thesis-fin15.pdf) được build bằng pdfLaTeX.
Tag `thesis-review-20261117-r1` và [manifest lịch sử](../release/manifest.json)
giữ đúng bản 67 trang trước FIN15.
`check.py` xác minh archive P8, tính đầy đủ của sáu chương, các đường dẫn
LaTeX và 68 dòng số liệu lịch sử, bao gồm 20 ô so sánh. Gói và bản nháp
Markdown lưu trữ phục vụ truy vết, tách khỏi đường biên dịch.

Notice [QuantAgent MIT](licenses/QuantAgent-MIT.txt) giữ theo upstream.
Bản PDF là bản thảo khóa luận. Thông tin phản biện, chữ ký và nộp nằm ở
[P10](../plan.md#p10-đóng-gói-tái-lập-và-bàn-giao).
