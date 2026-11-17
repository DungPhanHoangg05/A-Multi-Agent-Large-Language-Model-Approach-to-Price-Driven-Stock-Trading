# Build và kiểm nguồn Overleaf

Nguồn hiện hành nằm tại `thesis/` ở gốc repository. `main.tex` là điểm vào,
`latexmkrc` chọn LuaLaTeX và `biblatex` dùng Biber. Xem
[hướng dẫn import](../../../../thesis/README.md).

Từ thư mục gốc repository, chạy

```powershell
py -3.13 docs/plan/week12/thesis/tools/build.py
py -3.13 docs/plan/week12/thesis/tools/check.py --strict-cutover-targets --strict-current-targets
```

Build mặc định ghi file tạm vào `tmp/pdfs/thesis/`. Đối số `--source` chọn
thư mục nguồn đã giải nén, `--output-dir` chọn thư mục log/output và `--pdf`
chép PDF sau khi biên dịch thành công.

```powershell
py -3.13 docs/plan/week12/thesis/tools/build.py --source PATH_TO_EXTRACTED_PROJECT --output-dir tmp/pdfs/extracted-thesis --passes 4
```

`check.py` đối soát archive P8, hash nguồn, chữ hoa/thường của dependency
và 68 dòng bảng trong family20. Manifest hiện hành nằm tại
[thesis/manifest.json](../../../../thesis/manifest.json).

PDF và ZIP bàn giao nằm trong [release/](release/). Sau mỗi lần biên tập,
build và xem render của các trang bị ảnh hưởng, rồi cập nhật hash nguồn/PDF
trong source-map và manifest. Hash ZIP được ghi tại source-map bên ngoài ZIP.
Manifest ghi hash các file nguồn và PDF bàn giao.
