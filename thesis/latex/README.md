# Biên dịch nguồn khóa luận

Khung mới dùng **LuaLaTeX + Biber**, lớp `report` 12 pt/A4, font Latin Modern,
lề ngang 2,5 cm, trên/dưới 3 cm và giãn dòng 1,5 theo quan sát từ mẫu.
Hai bìa dùng đúng nguồn `frontmatter/covers.tex` đã kiểm trước đó; không đọc
`Latex/` hoặc PDF mẫu. Logo, hình vector và bibliography ở trong cây `thesis/`.
Các nguồn TikZ có thể sửa nằm tại `../assets/diagrams/`; đồ thị có source đi kèm.

Từ thư mục gốc repository:

```powershell
py -3.13 thesis/latex/tools/build.py --output-dir tmp/pdfs/thesis-p8
```

Hoặc từ chính thư mục `thesis/latex/`:

```powershell
py -3.13 tools/build.py
```

Script chỉ biên dịch `.tex`, chạy Biber rồi các lượt LuaLaTeX để ổn định
danh mục/tham chiếu; không tự chuyển Markdown hoặc chạy nghiên cứu. Có thể
chỉ định `--pdf` để chép PDF sau khi build thành công. Cần MiKTeX/TeX Live có
LuaLaTeX, Biber và các package được liệt kê trong `preamble.tex`. Không bật
shell escape hoặc tự tải package trong script. `build/` là thư mục tạm.

Hạn nộp, giới hạn trang/từ, kiểu trích dẫn bắt buộc và biểu mẫu cam đoan
chính thức chưa được cung cấp; numeric theo thứ tự xuất hiện là lựa chọn
biên tập hiện tại. Cam đoan đã được tác giả xác nhận câu chữ nhưng chưa ký.
Khung biên dịch không thay thế review khoa học hoặc nghiệm thu/nộp bên ngoài.
