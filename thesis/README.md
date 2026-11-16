# Khóa luận tốt nghiệp

Thư mục xây dựng khóa luận độc lập cho đề tài **Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market**.

## Nguồn bản nộp chính sau P8

**Mốc chuyển nguồn: 2026-11-16T13:14:55+07:00 (Asia/Saigon).** Từ mốc T72,
[main.tex](latex/main.tex), các file trong `latex/chapters/`,
`latex/appendices/`, `latex/frontmatter/`, [bibliography](references.bib)
và assets dùng chung là nguồn bản nộp chính. Mọi sửa nội dung tiếp theo
thực hiện trong LaTeX; không tự sinh lại từ Markdown. Các file Markdown
chương/phần đầu/phụ lục giữ làm bản nháp đã đối soát tại `e4e31daf`;
[source map](latex/source-map.json) lưu hash LF và ánh xạ mốc chuyển.
Kế hoạch, sổ bằng chứng và README quản lý vẫn tiếp tục cập nhật bằng Markdown.

[PDF ghép P8](release/thesis.pdf) gồm hai bìa, phần đầu, sáu chương,
tài liệu tham khảo và sáu phụ lục. Đây là bản để tiếp tục P9/P10,
chưa là bản đã phản biện, ký, nộp hoặc được trường chấp thuận.
[Hướng dẫn build](latex/README.md) dùng LuaLaTeX/Biber và không cần thư mục
mẫu, PDF mẫu, Pandoc hoặc Markdown. Đã thử trong bản sao chỉ gồm LaTeX,
assets và bibliography; build thiếu file bắt buộc sẽ dừng, không lặng lẽ bỏ chương.

Hạn nộp, giới hạn trang/từ và biểu mẫu chính thức chưa được cung cấp.
Số trang thực tế vượt dự toán viết ban đầu; P9 sẽ rà độ gọn và trình bày,
không bỏ bằng chứng hoặc đổi kết quả chỉ để ép số trang. G4 chưa được coi
là nghiệm thu yêu cầu chính thức khi các mục bắt buộc bên ngoài còn chưa rõ.

## Quy ước ngôn ngữ

- **Trao đổi với người dùng, kế hoạch, checklist và hướng dẫn quản lý:** tiếng Việt.
- **Nội dung khóa luận:** hoàn toàn bằng tiếng Anh, gồm phần đầu, sáu chương, phụ lục, tiêu đề, chú thích hình/bảng, nhãn sơ đồ và diễn giải khoa học. Dàn bài chương mục trong `outline.md` giữ tiếng Anh để làm khung bản thảo.
- **Định danh mã nguồn, tên phương pháp và tên tài liệu gốc:** giữ nguyên. Nếu cần dẫn bằng chứng tiếng Việt, phải có diễn giải tiếng Anh và ghi rõ bản dịch phục vụ trình bày; không sửa danh tính của prompt hoặc dữ liệu thực nghiệm gốc.

## Thứ tự đọc

1. [Dàn bài khóa luận](outline.md): câu hỏi nghiên cứu, sáu chương, phụ lục và ánh xạ tới hệ thống.
2. [Kế hoạch viết chi tiết](plan.md): các task nhỏ, phụ thuộc, đầu ra, tiêu chí nghiệm thu và lộ trình đến gói bàn giao cuối.
3. [Checklist công việc](plan.md#21-một-nguồn-trạng-thái-công-việc): checklist 84 task nằm ngay trong kế hoạch; bằng chứng hoàn thành gộp lưu tại README tuần.
4. [Sổ nguồn và yêu cầu](evidence.md): metadata, kiểm kê hai nghiên cứu, [danh sách đọc theo chủ đề](evidence.md#4-danh-sách-đọc-nguồn-gốc-và-quy-ước-khóa-trích-dẫn), quy ước khóa trích dẫn và giới hạn bằng chứng. Trạng thái đọc/kiểm được ghi theo phạm vi, không suy từ việc có trong bibliography.
5. [Thuật ngữ và ký hiệu](evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt): tên tiếng Anh dùng trong bản thảo, ánh xạ ID, đơn vị và quy tắc diễn đạt thống nhất.
6. [Danh mục hình, bảng và thuật toán](evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn): 23 ID theo kế hoạch, có thông điệp, vị trí, task phụ trách, loại nguồn, provenance và đường xuất dự kiến; chưa phải các sản phẩm đã tạo.
7. [Ví dụ xuyên suốt EX01](evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết): FPT tại cutoff 03/07/2023, quy tắc chọn, nguồn từng bước và ranh giới giữa thông tin dự báo với outcome; giữ kết quả sai, fallback và giới hạn nghiên cứu.
8. [Các chương và sổ ánh xạ](evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm): liên kết tới sáu bản nháp trong `chapters/`, tiêu đề ổn định và ánh xạ luận điểm/ô bảng; sổ chung giữ nguồn và phạm vi tự kiểm, không có checklist hoặc receipt riêng cho từng chương.
9. [Chương 3 — cơ sở lý thuyết](chapters/03_background.md): đã có bản nháp §3.1–§3.7, [F01](assets/diagrams/F01_trade_timeline.pdf)/[F02](assets/diagrams/F02_temporal_partitions.pdf) vector/source TikZ và ví dụ có nguồn hoặc nhãn Illustrative. Nguồn/claim đối soát tại §8 sổ chung; chưa phải bản đã qua rà soát khoa học, citation và bố cục cuối.
10. [Chương 4 — hệ thống đề xuất](chapters/04_proposed_system.md): P3 đã đủ bản nháp §4.1–§4.10, gồm utility/policy, projection, bảng tám vai trò, ba thuật toán và luồng ứng dụng; kèm F03/F04/F05/F05a/F06/F07/F08/F11 có nguồn. [Sổ chung §9](evidence.md#9-nguồn-giải-thích-hệ-thống-đề-xuất) giữ binding và tự kiểm G2 nội bộ. EX01 kết thúc bằng outcome sau barrier; UI/F11 vẫn PENDING. Chưa rà soát toàn văn, phản biện ngoài hoặc dàn trang cuối.

11. [Chương 5 — thực nghiệm và thảo luận](chapters/05_experiments.md): T36–T47; P4/T36–T47 đã đủ bản nháp §5.1–§5.9, F09/F10 và B04/B05/B06/B07/B09. P6 đã đối soát mạch và tự kiểm G3 nội bộ; phụ lục, phản biện và dàn trang cuối còn việc; trạng thái nghiên cứu/ứng dụng không đổi. [Sổ chung §10](evidence.md#10-nguồn-thiết-kế-thực-nghiệm) giữ nguồn/claim. Bảng đã chuyển LaTeX ở P8, giữ Markdown đối chiếu; chưa rà khoa học/ngôn ngữ toàn văn hoặc phản biện ngoài.

12. [Chương 2 — tổng quan tài liệu](chapters/02_related_work.md): T48–T53; P5/T48–T53 đã đủ bản nháp §2.1–§2.7, B08a–b và bibliography 22 nguồn đã kiểm theo phạm vi. P6 đã đối soát mạch và tự kiểm G3 nội bộ; rà soát khoa học/ngôn ngữ và dàn trang cuối còn việc. [Bibliography riêng](references.bib) và [sổ nguồn P5](evidence.md#11-nguồn-tổng-quan-tài-liệu-và-định-vị) giữ phiên bản, đoạn hỗ trợ và giới hạn.

13. [Mở đầu](chapters/01_introduction.md) và [kết luận](chapters/06_conclusion.md): T54–T58; P6 đủ bản nháp Chương 1/6 và đối soát lập luận; G3 tự kiểm nội bộ đạt đúng nguồn T36–T58, chưa review ngoài/dàn trang cuối. [Sổ P6](evidence.md#12-mở-đầu-kết-luận-và-đối-soát-lập-luận) giữ nguồn và phạm vi tự kiểm.

14. [Phần đầu](frontmatter.md): T59–T60; T59–T60 hoàn tất bản nháp phần đầu: abstract/7 keywords, lời cảm ơn và câu chữ cam đoan đã được tác giả xác nhận, 42 chữ viết tắt/26 dòng ký hiệu; chưa ký và chưa có biểu mẫu chính thức. [Sổ P7](evidence.md#13-phần-đầu-và-phụ-lục) giữ nguồn, đối soát và yêu cầu chính thức chưa có.

15. Phụ lục — T61–T66 đã đủ bản nháp: [A: hợp đồng](appendices/A_contracts.md), [B: prompts/responses](appendices/B_prompts.md), [C: cấu hình](appendices/C_configuration.md), [D: bảng mở rộng](appendices/D_results.md), [E: audit](appendices/E_verification.md), [F: tái lập/ứng dụng](appendices/F_reproduction.md). Đã nối tham chiếu trong thân bài và đối soát nguồn/số liệu/phạm vi. [Sổ nguồn appendix](evidence.md#134-phụ-lục-a-hợp-đồng-dữ-liệu-và-thời-gian) giữ locator/hash và QA; đã chuyển LaTeX ở P8, chưa nghiệm thu bản nộp cuối.

16. [Nguồn LaTeX](latex/README.md): T67–T72; Toàn văn đã ghép và chuyển nguồn chính sang LaTeX. [Sổ P8](evidence.md#14-dàn-trang-latex-và-chuyển-nguồn-chính) ghi toolchain, build và phạm vi kiểm.

## Hai trang bìa

[Nội dung bìa tiếng Anh](frontmatter.md) ghi thông tin tác giả, mã sinh viên,
đề tài và người hướng dẫn đã cung cấp. [Bản xem hai trang bìa](release/covers-preview.pdf)
giữ cơ sở đào tạo, logo, khung và kiểu chữ của mẫu; đề tài dài được chia năm
dòng. Mã sinh viên nằm trong hồ sơ, không thêm vào bìa vì mẫu không có trường
này. Hạn nộp và quy định trích dẫn/bố cục chính thức hiện chưa được cung cấp.
Dòng Supervisor trên bìa trong được căn giữa theo trục trang theo đính chính
của tác giả.

Nguồn bản xem gồm [wrapper](latex/covers-preview.tex),
[hai bìa](latex/frontmatter/covers.tex) và logo trong `assets/figures/`.
Wrapper này chỉ dàn trang bản xem bìa riêng. Toàn văn dùng `latex/main.tex`
và nguồn LaTeX chính đã chuyển tại T72; Markdown phần đầu là bản lưu trữ.
Khi đổi metadata được tác giả chấp thuận, sửa nguồn LaTeX và kiểm lại PDF.
Không cần thư mục `Latex/` mẫu để build bản xem hoặc toàn văn.

Từ thư mục gốc kho mã, biên dịch bằng pdfLaTeX hai lượt để định vị khung
TikZ. Thư mục tạm nhận log/aux, chỉ PDF được chép sang thư mục bàn giao:

```powershell
New-Item -ItemType Directory -Force tmp/pdfs/thesis-covers | Out-Null
Push-Location thesis/latex
pdflatex --disable-installer --interaction=nonstopmode --halt-on-error '--output-directory=../../tmp/pdfs/thesis-covers' covers-preview.tex
pdflatex --disable-installer --interaction=nonstopmode --halt-on-error '--output-directory=../../tmp/pdfs/thesis-covers' covers-preview.tex
Pop-Location
Copy-Item tmp/pdfs/thesis-covers/covers-preview.pdf thesis/release/covers-preview.pdf
```

Toolchain bản xem: pdfTeX 3.141592653-2.6-1.40.28, MiKTeX 25.12, LaTeX2e
2025-11-01; font Latin Modern và các package khai báo trong wrapper. Đây là
PDF riêng hai bìa; chưa phải `thesis.pdf` hoàn chỉnh hoặc bản đã nộp. Khi thiếu
package, cài package được báo thiếu trước khi build; môi trường hiện tại đã
được bổ sung `microtype` và `setspace`. MiKTeX còn nhắc kiểm tra cập nhật ở
stderr dù build exit 0; đây không phải lỗi bố cục trong log LaTeX.

Phần phương pháp đề xuất phải giúp giảng viên lần đầu tiếp cận hiểu được toàn bộ hệ thống. Người đọc cần lần theo một quyết định từ đầu vào có thời điểm xác định, các báo cáo agent, ngữ cảnh lịch sử, đề xuất của LLM, hành động sau policy đến kết quả tài khoản mà không phải mở mã nguồn.

## Khung mẫu và bằng chứng

[Nguồn LaTeX mẫu](../Latex/main.tex) và [PDF mẫu](../23020332_Tran_Xuan_Bao.pdf) chỉ cung cấp cấu trúc và cách trình bày. Nội dung nghiên cứu, thông tin tác giả và danh mục tham khảo của mẫu không thuộc khóa luận mới. Khung gồm phần đầu, sáu chương và tài liệu tham khảo; bảng, ký hiệu và phụ lục được điều chỉnh theo hệ thống.

[Kế hoạch dự án](../docs/plan/plan.md), [ghi nhận tích hợp](../docs/plan/week12/README.md), mã nguồn và bằng chứng thực nghiệm đã khóa là nguồn đối chiếu kỹ thuật. [Bài báo hiện tại](../paper/) giúp tìm bằng chứng, không thay thế việc giải thích hệ thống từ những khái niệm ban đầu.

Khảo sát nguồn bắt đầu tại `develop:7a71d4da0dcccded03e46189ce42fea2896f6c80`. Kế hoạch 84 task và việc đổi tên thư mục xuất phát từ `develop:05892c3ec8799a8f3d23ce2eeaaaf0778ea09070` ngày 14/11/2026. Quy ước ngôn ngữ được đính chính theo yêu cầu tiếp theo: tài liệu quản lý bằng tiếng Việt, khóa luận bằng tiếng Anh. Các nghiên cứu lịch sử giữ nguyên mốc mã nguồn/runtime riêng.

## Phạm vi công việc

Đầu ra cuối là khóa luận tiếng Anh hoàn chỉnh, có luận điểm truy vết được, hình/bảng đã kiểm, tài liệu tham khảo, phụ lục, nguồn LaTeX tái lập và PDF đã kiểm trực quan. Kế hoạch bao phủ chuẩn bị, viết, chỉnh sửa, dàn trang và bàn giao. Hoàn thành kế hoạch không đồng nghĩa hoàn thành bản thảo hay tự cho phép thu thực nghiệm mới.

Giữ rõ kết quả âm, thiếu support, vấn đề nguồn dữ liệu và giới hạn nhân quả. Module có trong mã nguồn không chứng minh ablation tương ứng đã chạy; replay offline không phải một lượt gọi mô hình mới.

Các file mẫu có ở máy nhưng chưa được Git theo dõi tại mốc lập kế hoạch. Gói nguồn khóa luận cuối phải tự đủ để biên dịch, không phụ thuộc các file mẫu chưa được theo dõi đó.

## Quy ước làm việc

- Lưu bản thảo tại `thesis/`; quản lý tiến độ tại `docs/plan/`.
- Theo cây thư mục đề xuất trong kế hoạch; chỉ tạo file khi task tương ứng bắt đầu.
- Dùng một sổ đối chiếu bằng chứng chung, không tạo báo cáo riêng cho từng task viết.
- Tuân thủ nhánh tác vụ và Conventional Commits. Task thuần tài liệu kiểm nguồn, liên kết và diff phù hợp, không chạy lại toàn bộ test runtime.
- Ghi rõ thông tin tác giả/người hướng dẫn, quy định cơ sở đào tạo hoặc phản hồi còn thiếu; tiếp tục các phần viết độc lập trong khi chờ thông tin đó.
