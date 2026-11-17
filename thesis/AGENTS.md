# Nguồn khóa luận dùng trực tiếp trên Overleaf

- `main.tex` tại gốc `thesis/` là điểm vào duy nhất của bản thảo hiện hành.
- Sửa nội dung tại `chapters/`, `frontmatter/`, `preamble.tex` và `references.bib`.
- Đặt mọi tài nguyên biên dịch trong thư mục này. Viết đường dẫn tương đối từ gốc dự án và khớp chữ hoa/thường với tên file trên Linux.
- Giữ compiler LuaLaTeX, bibliography Biber và cấu hình `latexmkrc` tương thích Overleaf.
- Lưu kế hoạch, bằng chứng, bản nháp và công cụ quản lý tại `docs/plan/week12/thesis/` trong repository.
- Sau mỗi thay đổi, kiểm build từ bản sao sạch hoặc ZIP giải nén, cập nhật manifest và xuất ZIP có `main.tex` ngay ở gốc.
- Đặt PDF xuất và ZIP bàn giao tại `docs/plan/week12/thesis/release/` trong repository.
