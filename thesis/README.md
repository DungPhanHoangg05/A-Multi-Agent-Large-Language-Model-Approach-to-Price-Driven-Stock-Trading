# Khóa luận tốt nghiệp

Thư mục xây dựng khóa luận độc lập cho đề tài **Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market**.

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
8. [Các chương và sổ ánh xạ](evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm): liên kết tới từng file trong `chapters/`, tiêu đề ổn định và placeholder cho mục chưa viết; sổ chung nhận ánh xạ luận điểm/ô bảng khi viết, không có checklist hoặc receipt riêng cho từng chương.
9. [Chương 3 — cơ sở lý thuyết](chapters/03_background.md): đã có bản nháp §3.1–§3.7, [F01](assets/diagrams/F01_trade_timeline.pdf)/[F02](assets/diagrams/F02_temporal_partitions.pdf) vector/source TikZ và ví dụ có nguồn hoặc nhãn Illustrative. Nguồn/claim đối soát tại §8 sổ chung; chưa phải bản đã qua rà soát khoa học, citation và bố cục cuối.
10. [Chương 4 — hệ thống đề xuất](chapters/04_proposed_system.md): P3 đã đủ bản nháp §4.1–§4.10, gồm utility/policy, projection, bảng tám vai trò, ba thuật toán và luồng ứng dụng; kèm F03/F04/F05/F05a/F06/F07/F08/F11 có nguồn. [Sổ chung §9](evidence.md#9-nguồn-giải-thích-hệ-thống-đề-xuất) giữ binding và tự kiểm G2 nội bộ. EX01 kết thúc bằng outcome sau barrier; UI/F11 vẫn PENDING. Chưa rà soát toàn văn, phản biện ngoài hoặc dàn trang cuối.

11. [Chương 5 — thực nghiệm và thảo luận](chapters/05_experiments.md): T36–T42; Đã có §5.1–§5.7 và B04/B05/B06a–c; §5.8–§5.9 và T43–T47 chưa hoàn tất, P4 còn việc. [Sổ chung §10](evidence.md#10-nguồn-thiết-kế-thực-nghiệm) giữ nguồn/claim. Bảng Markdown chưa chuyển CSV/LaTeX; chưa rà soát toàn văn hoặc phản biện ngoài.

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
Nguồn này chỉ dàn trang bìa, chưa phải khung LaTeX toàn văn; Markdown vẫn
là nguồn nội dung chính. Khi đổi metadata, cập nhật cả bản trình bày LaTeX
và kiểm lại PDF. Không cần thư mục `Latex/` mẫu để build bản xem.

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
