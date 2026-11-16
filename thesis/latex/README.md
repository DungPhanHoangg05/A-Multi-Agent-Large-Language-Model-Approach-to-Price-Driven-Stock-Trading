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
py -3.13 -X utf8 thesis/latex/tools/check.py --strict-current-targets
py -3.13 -X utf8 thesis/latex/tools/build.py --output-dir tmp/pdfs/thesis --pdf thesis/release/thesis.pdf
```

`check.py` kiểm archive P8 nguyên byte, hash LF lịch sử, dependency cục bộ,
sáu chương ghép đúng một lần và 68 dòng bảng chiếu từ nguồn cũ (đủ family20).
`--strict-cutover-targets` kiểm nguồn P8 trong archive; các hash mốc T72
không bị sửa để khớp bản mới. `--strict-current-targets` kiểm riêng hash
LaTeX sau biên tập, được khóa lại ở T78; mốc T73l giữ trong `review_history`. Hai bản Markdown Chương 4–5 chỉ đổi
điều hướng tới ZIP; nguyên bản với link cũ vẫn có trong archive.
Build mặc định
chạy bốn lượt LuaLaTeX và Biber; script từ chối cập nhật PDF đích khi còn
reference/citation hoặc ký tự thiếu. Các cờ `--passes`/`--skip-bibliography`
chỉ phục vụ sửa bố cục khi bibliography không đổi, không thay full build.

Đã ghi nhận LuaHBTeX 1.24.0/MiKTeX 25.12, LaTeX2e 2025-11-01 và Biber 2.21.
T76 chuẩn hóa tháng thành số và bỏ trường năm không hợp lệ của model card
không ngày (vẫn ghi rõ undated); không gán năm xuất bản mới. Bản rút gọn
có 60 trang A4 dọc/rotation=0, không phụ lục,
17 bảng chính và 5 hình. Giữ 12 pt/giãn dòng 1,5/lề 2,5cm ngang và 3cm
trên dưới; bảng dùng small 11 pt, nhãn sơ đồ mới 10 pt. Không dùng thu nhỏ
toàn bảng, môi trường xoay hoặc ngắt trang cưỡng ép theo từng bảng.
T78 build trong thư mục sạch với bốn lượt LuaLaTeX/Biber, không đọc mẫu,
Markdown, archive hoặc nguồn ở checkout gốc. Final log không underfull/
overfull box, glyph thiếu, reference/citation treo, glue-splitting note hay
warning Biber. MiKTeX vẫn nhắc chưa kiểm cập nhật ở stdout; exit 0, đây là
nhắc bảo trì môi trường, không phải lỗi bản thảo. Không cập nhật runtime
để xóa lời nhắc. Hash PDF/nguồn và số trang từng phần ở `source-map.json`.
T79–T80 tiếp tục kiểm trực quan và phản hồi; chưa phản biện/nộp bên ngoài.

Notice `licenses/QuantAgent-MIT.txt` giữ nguyên byte notice upstream. Không
suy quyền phân phối data/news/model weights/logo trường từ license phần mềm;
những quyền chưa xác minh được nêu trong Chương 5 và sổ bằng chứng T76.

T73k đã bỏ phụ lục khỏi `main.tex` và xóa hai thư mục phụ lục Markdown/LaTeX
sau khi kiểm byte/hash. `../archive/p8-source.zip` là bằng chứng ngoài gói
bản nộp, không là input của LuaLaTeX/Biber. Chỉ công cụ đối soát lịch sử
cần archive; build không cần Markdown, archive hoặc phụ lục đã xóa.

PDF không phụ thuộc thư mục mẫu để hiển thị. Liên kết tới tài liệu/source
nghiên cứu ngoài các chương vẫn cần repository bằng chứng tương ứng;
chúng không là dependency biên dịch. Gói nguồn bàn giao cuối thuộc P10.
