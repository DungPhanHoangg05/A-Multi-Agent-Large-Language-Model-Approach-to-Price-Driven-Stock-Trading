# Import khóa luận vào Overleaf

1. Zip **nội dung bên trong** thư mục này để `main.tex` nằm ngay ở gốc ZIP.
2. Trên Overleaf, chọn **New project → Existing project (.zip)** và upload ZIP.
3. Trong Settings, chọn **Main document → main.tex** và **Compiler → LuaLaTeX**, rồi bấm **Recompile**.

Overleaf xử lý bibliography Biber theo cấu hình `biblatex`. Dự án có sẵn
`latexmkrc` cho LuaLaTeX và các font Latin Modern của TeX Live.
[Hướng dẫn upload của Overleaf](https://docs.overleaf.com/managing-projects-and-files/uploading-a-project)

## Chỉnh sửa tiếp

Sửa trực tiếp `main.tex`, `preamble.tex`, các file trong `chapters/`,
`frontmatter/` và `references.bib`. Hình dùng trong bản thảo nằm ở
`assets/figures/`. Thêm tài nguyên vào thư mục dự án và dùng đường dẫn
tương đối với chữ hoa/thường khớp tên file.

`manifest.json` ghi phiên bản nguồn và hash của bản bàn giao. Khi tạo bản
bàn giao mới, cập nhật manifest theo nội dung đã chỉnh và PDF vừa biên dịch.

Trong repository đầy đủ, lệnh build cục bộ là

```powershell
py -3.13 docs/plan/week12/thesis/tools/build.py
```

PDF, ZIP và hồ sơ kiểm tra được lưu tại `docs/plan/week12/thesis/release/`
trong repository. Hướng dẫn tại đây dùng cấu trúc nguồn hiện hành cho các
lần chỉnh sửa tiếp theo.
