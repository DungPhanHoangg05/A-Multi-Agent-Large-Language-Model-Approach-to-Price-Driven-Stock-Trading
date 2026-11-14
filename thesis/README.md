# Khóa luận tốt nghiệp

Thư mục xây dựng khóa luận độc lập cho đề tài **Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market**.

## Quy ước ngôn ngữ

- **Trao đổi với người dùng, kế hoạch, checklist và hướng dẫn quản lý:** tiếng Việt.
- **Nội dung khóa luận:** hoàn toàn bằng tiếng Anh, gồm phần đầu, sáu chương, phụ lục, tiêu đề, chú thích hình/bảng, nhãn sơ đồ và diễn giải khoa học. Dàn bài chương mục trong `outline.md` giữ tiếng Anh để làm khung bản thảo.
- **Định danh mã nguồn, tên phương pháp và tên tài liệu gốc:** giữ nguyên. Nếu cần dẫn bằng chứng tiếng Việt, phải có diễn giải tiếng Anh và ghi rõ bản dịch phục vụ trình bày; không sửa danh tính của prompt hoặc dữ liệu thực nghiệm gốc.

## Thứ tự đọc

1. [Dàn bài khóa luận](outline.md): câu hỏi nghiên cứu, sáu chương, phụ lục và ánh xạ tới hệ thống.
2. [Kế hoạch viết chi tiết](plan.md): các task nhỏ, phụ thuộc, đầu ra, tiêu chí nghiệm thu và lộ trình đến gói bàn giao cuối.
3. [Checklist công việc](../docs/plan/week12/README.md#checklist-viết-khóa-luận): nơi duy nhất cập nhật trạng thái và bằng chứng hoàn thành; kế hoạch chỉ định nghĩa task, không lặp lại trạng thái.

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
