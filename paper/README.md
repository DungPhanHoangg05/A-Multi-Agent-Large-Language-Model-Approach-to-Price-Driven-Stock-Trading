# Nguồn bài báo

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
PDF hiện hành ở [outputs/paper](../outputs/paper/); không cần các thư mục kết quả
thực nghiệm để biên dịch bài báo. Không tạo gói ZIP tự động.

Các bảng trong `content/tables/` là bản đã biên tập cho bài báo; không chạy lại
generator lịch sử để ghi đè chúng. Bằng chứng nguồn cũ và cách khôi phục nằm ở
[kho bằng chứng](../docs/plan/revision_evidence/README.md).
