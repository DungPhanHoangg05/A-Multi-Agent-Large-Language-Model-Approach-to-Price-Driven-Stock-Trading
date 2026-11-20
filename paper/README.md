# Nguồn bài báo

Bài báo so sánh **Our system với QuantAgent** để kiểm tra tác dụng
của alpha OHLCV và sentiment tin tiếng Việt. **BICL v1–v5** là
nghiên cứu mở rộng. Kết quả FIN12 có bảng riêng vì nguồn, forecast và
mẫu số khác lần đánh giá lịch sử. [Tên hệ thống và ID](../README.md#methods-and-profiles)

Mở `main.tex` bằng pdfLaTeX; `main_submit.tex` là bản có dòng và trang phục vụ nộp bài.
Khi đưa lên Overleaf, tải toàn bộ nội dung thư mục này và chọn đúng main document.
Tệp lớp, kiểu bibliography và dữ liệu tài liệu tham khảo đã nằm trong thư mục.

```text
paper/
  main.tex, main_submit.tex   Điểm vào biên dịch
  layout.tex                 Thiết lập bố cục dùng chung
  references.bib             Tài liệu tham khảo
  content/                   Các phần nội dung và phụ lục
    tables/component/        Bảng nghiên cứu thành phần
    tables/historical_context/ Bảng nghiên cứu ngữ cảnh lịch sử
  figures/                   Hình và sơ đồ được bài báo sử dụng
```

Biên dịch tại thư mục này:

```powershell
pdflatex -halt-on-error main.tex
bibtex main
pdflatex -halt-on-error main.tex
pdflatex -halt-on-error main.tex
```

Đổi `main` thành `main_submit` để biên dịch bản nộp.
PDF hiện hành gồm [bản đầy đủ](../outputs/paper/main-fin15.pdf) và
[bản nộp](../outputs/paper/main-submit-fin15.pdf). Nguồn tự đủ để biên dịch.
[PDF và manifest trước FIN15](../outputs/paper/README.md) giữ vai trò bằng chứng lịch sử.

Chạy `py -3.13 -X utf8 scripts/project_finalize_manuscript_tables.py --check`
từ gốc kho mã để so bảng đã chiếu với receipt FIN12. Bằng chứng nguồn cũ
và cách khôi phục nằm ở [kho bằng chứng](../docs/plan/revision_evidence/README.md).
