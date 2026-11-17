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

## Đúng phiên bản của bản PDF hiện hành

Tag nguồn bản thảo là **`thesis-review-20261117-r1`**. Đây là tag cục bộ do
tác giả giữ, chưa được công bố lên remote; cần nhận đúng tagged checkout
từ tác giả nếu remote chưa có tag này. Commit `7a1b77f1` chỉ chứa bản thảo
60 trang trước chỉnh sửa. Mã nguồn thực nghiệm là mốc riêng `384725a6`
trong `docs/plan/week12/final_evidence_snapshot.zip`; không dùng nó làm
định danh phiên bản nguồn LaTeX của PDF hiện hành.

Từ tagged checkout tại gốc repository:

```powershell
git rev-parse 'thesis-review-20261117-r1^{commit}'
py -3.13 thesis/latex/tools/build.py --output-dir tmp/pdfs/reproduce-review --passes 4
Get-FileHash -Algorithm SHA256 thesis/release/thesis.pdf
```

`../release/manifest.json` liên kết tag, các input được recorder của build
đọc, bibliography, tài nguyên hình, công cụ build và SHA-256 PDF phân phối.
Hash văn bản được chuẩn hóa LF để không phụ thuộc chuyển CRLF khi checkout;
hash ảnh/PDF là nguyên byte. Hash PDF dùng để kiểm artifact phân phối.
Không cam kết hash của PDF mới build đồng nhất byte khi timestamp/toolchain
khác; cần đối soát thêm nội dung, bố cục và môi trường đã ghi. Manifest không
chứa hash của chính nó hoặc của source-map, tránh vòng phụ thuộc; source-map
ghi hash manifest. Gói nguồn tự đủ và nghiệm thu từ gói giải nén vẫn thuộc P10.

Đã ghi nhận LuaHBTeX 1.24.0/MiKTeX 25.12, LaTeX2e 2025-11-01 và Biber 2.21.
T76 chuẩn hóa tháng thành số và bỏ trường năm không hợp lệ của model card
không ngày (vẫn ghi rõ undated); không gán năm xuất bản mới. Bản hiện hành sau T80a–T80l có 67 trang A4 dọc/rotation0, không phụ lục,
21 bảng và 8 hình. Giữ12pt/giãn1,5/lề2,5cm ngang và3cm trên dưới; bảng11pt,
nhãn sơ đồ10pt. Không thu nhỏ toàn bảng hoặc xoay trang để ép ngân sách.
T80l build sạch bốn lượt LuaLaTeX/Biber trong bản sao chỉ gồm LaTeX/assets/bib,
không đọc archive/Markdown/mẫu hoặc nguồn ở checkout gốc. Final log không có
underfull/overfull, citation/reference/glyph thiếu hoặc cảnh báo Biber.
MiKTeX vẫn có nhắc chưa kiểm cập nhật ở stdout, exit0; không đổi môi trường.
Đã render đủ 67 trang bằng Poppler 120 dpi và xem từng trang, phóng lớn bảng/hình mới.
Kiểm semantic51 bookmark/51 TOC title links với tiêu đề thật,146 đích nội bộ
hợp lệ và56 liên kết bảng/hình đúng caption. Native headings của report/hyperref
giữ điểm neo cùng tiêu đề; không đặt trang đích cứng theo PDF.
Hash hiện hành và lịch sử60 trang/P8 giữ riêng trong `source-map.json`.
G5 chốt trong phạm vi nội bộ; P10 đóng gói nguồn và build từ gói giải nén vẫn còn mở.
Chưa có phản biện độc lập mới, chưa ký/nộp; chuẩn trường và một số quyền phân phối
chưa xác minh. Suite nghiên cứu không chạy lại vì nguồn/runtime/input đã khóa không đổi.

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
