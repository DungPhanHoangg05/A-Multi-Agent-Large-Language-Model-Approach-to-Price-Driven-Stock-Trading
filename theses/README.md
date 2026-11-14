# Khóa luận tốt nghiệp

Thư mục xây dựng bản KLTN độc lập cho hệ thống hiện tại. Bắt đầu bằng [dàn bài chi tiết](outline.md), viết bằng tiếng Việt để duyệt nội dung trước khi chuyển sang LaTeX. Tên tiếng Anh của đề tài và các chương được giữ để thuận tiện cho bước chuyển đổi; ngôn ngữ bản nộp cuối chưa được chốt.

## Phạm vi bản đầu

- Tham chiếu **hình thức tổ chức** từ [nguồn mẫu](../Latex/main.tex) và [PDF mẫu](../23020332_Tran_Xuan_Bao.pdf): phần đầu, sáu chương, tài liệu tham khảo.
- Xây dựng lại toàn bộ nội dung theo hệ thống đa agent, Bayesian Prior và MT-BICL trong kho mã hiện tại; không chuyển nội dung nghiên cứu, danh mục tham khảo hoặc thông tin tác giả của bài mẫu sang khóa luận mới.
- Bổ sung danh mục bảng và phụ lục phục vụ phương pháp, kiểm thử và khả năng tái lập. Đây là đề xuất biên soạn, không phải yêu cầu đã xác nhận của cơ sở đào tạo.
- Chỉ lập dàn bài; chưa viết bản thảo đầy đủ, tạo nguồn `.tex`, chạy thực nghiệm hoặc sinh PDF mới.

## Cách đọc dàn bài

1. Đọc định hướng, câu hỏi nghiên cứu và mục lục rút gọn để duyệt mạch lập luận.
2. Đọc từng chương để biết nội dung cần viết, hình/bảng cần chuẩn bị và giới hạn diễn giải.
3. Dùng bảng ánh xạ nguồn cuối tài liệu để tra mã nguồn và bằng chứng khi triển khai bản thảo.

Nội dung mang nhãn **đã có bằng chứng** chỉ có nghĩa là đã có nguồn lưu trong kho; lượt lập dàn bài này không chạy lại hay cấp lại nghiệm thu cho các thí nghiệm đó. Nội dung **cần bổ sung** là công việc tương lai, không được trình bày như một kết quả đã thực hiện.

## Mốc tham chiếu và kiểm tra

- Ngày khảo sát: **14/11/2026**.
- Mốc `develop` trước task: `7a71d4da0dcccded03e46189ce42fea2896f6c80`.
- Nguồn điều phối: [kế hoạch hiện hành](../docs/plan/plan.md), [README tích hợp](../docs/plan/week12/README.md), registry và mã phương pháp được dẫn trong dàn bài. Nguồn [bài báo hiện tại](../paper/) giúp tìm bằng chứng, không quyết định cấu trúc khóa luận.
- Bản mẫu PDF có 62 trang; đã đối chiếu mục lục với `Latex/main.tex` và xem trực quan bìa cùng hai trang mục lục. PDF có biểu mẫu xác nhận cuối tài liệu; chỉ đưa vào bản nộp nếu có yêu cầu tương ứng.
- Kiểm tra của task tài liệu: diff, liên kết nội bộ, công thức kinh tế và các con số phạm vi với nguồn đã lưu; ghi nhận SHA256 các file nguồn tham chiếu và kiểm lại trước bàn giao. Hai tài liệu điều phối được cập nhật để dẫn tới dàn bài mới, không thuộc nhóm nguồn giữ nguyên byte.
- Không chạy compileall, unit test, E2E hay leakage suite vì chỉ thêm Markdown, không đổi code/test/schema/config/runtime hoặc dữ liệu đầu vào, theo AGENTS.md §1.2. Không coi việc lập dàn bài là nghiệm thu lại hệ thống.

Các file mẫu đang có tại máy chưa được Git theo dõi tại thời điểm khảo sát. Liên kết tới mẫu cần các file đó ở repo root; bản dàn bài mới tự chứa cấu trúc cần thiết để tiếp tục viết.
