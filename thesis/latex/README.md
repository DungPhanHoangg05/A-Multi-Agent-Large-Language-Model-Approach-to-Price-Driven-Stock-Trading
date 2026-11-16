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

## Nguồn chính và kiểm mốc chuyển

Từ thời điểm ghi trong `source-map.json` (T72), `.tex` là nguồn bản nộp
chính; Markdown là bản lưu trữ, không nằm trong đường build. Pandoc 3.9
chỉ được dùng để chuyển một lần và không cần cài để biên dịch lại.
Không tự chuyển ngược hoặc tạo lại các file đã biên tập từ bản nháp cũ.

Từ thư mục gốc repository:

```powershell
py -3.13 -X utf8 thesis/latex/tools/check.py --strict-cutover-targets
py -3.13 -X utf8 thesis/latex/tools/build.py --output-dir tmp/pdfs/thesis --pdf thesis/release/thesis.pdf
```

`check.py` kiểm hash LF của bản nháp lưu trữ, dependency nội bộ và việc ghép
mỗi chương/phụ lục đúng một lần. Cờ strict so thêm LaTeX với mốc chuyển;
sau sửa LaTeX được phép ở P9, bỏ cờ này hoặc ghi baseline mới đúng phạm vi,
không cập nhật hash bản nháp để che thay đổi ngoài ý định. Build mặc định
chạy bốn lượt LuaLaTeX và Biber; script từ chối cập nhật PDF đích khi còn
reference/citation hoặc ký tự thiếu. Các cờ `--passes`/`--skip-bibliography`
chỉ phục vụ sửa bố cục khi bibliography không đổi, không thay full build.

Đã ghi nhận LuaHBTeX 1.24.0/MiKTeX 25.12, LaTeX2e 2025-11-01 và Biber 2.21.
Hai warning metadata bibliography gốc (`month=March`, `year=n.d.`) không
làm thiếu citation hoặc đổi numeric order; không sửa metadata nguồn chỉ
để xóa warning. Các ghi chú nội bộ longtable về glue splitting được lưu
trong log và đã kiểm bằng render/bounds; không có overfull box hoặc mất
ký tự trong bản P8 đã ghép. P9 tiếp tục rà khoảng trắng và bố cục toàn văn.

PDF không phụ thuộc thư mục mẫu để hiển thị. Liên kết tới tài liệu/source
nghiên cứu ngoài các chương vẫn cần repository bằng chứng tương ứng;
chúng không là dependency biên dịch. Gói nguồn bàn giao cuối thuộc P10.
