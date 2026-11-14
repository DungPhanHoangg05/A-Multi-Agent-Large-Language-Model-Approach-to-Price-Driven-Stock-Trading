# Sổ nguồn và đối chiếu bằng chứng khóa luận

## 1. Thông tin tác giả và yêu cầu trình bày

Thông tin được ghi nhận ngày **14/11/2026** từ yêu cầu và phản hồi trực tiếp
của tác giả trong phiên làm việc này. Bảng dưới phân biệt yêu cầu tác giả đã
chốt với quy định chính thức chưa được cung cấp. Nội dung bìa tiếng Anh nằm
tại [frontmatter.md](frontmatter.md); hồ sơ này dùng để quản lý nguồn.

| Trường | Giá trị | Nguồn và phạm vi xác nhận |
| --- | --- | --- |
| Cơ sở đào tạo | VIETNAM NATIONAL UNIVERSITY, HANOI; UNIVERSITY OF ENGINEERING AND TECHNOLOGY | Hai trang đầu PDF mẫu; tác giả yêu cầu giữ nguyên cơ sở đào tạo. |
| Tác giả | Phan Hoang Dung | Tác giả cung cấp trực tiếp; bìa dùng PHAN HOANG DUNG theo kiểu chữ hoa của mẫu. |
| Mã sinh viên | 23020346 | Tác giả bổ sung trực tiếp; không dùng mã 23020332 trong tên file mẫu. Mẫu không in mã sinh viên trên hai bìa nên bản xem bìa cũng không thêm trường này. |
| Tên đề tài | Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market | Tác giả cung cấp trực tiếp; tên chuẩn khớp [dàn bài](outline.md#a-research-direction). |
| Người hướng dẫn | Dr. Tran Hong Viet | Tác giả cung cấp trực tiếp; thay toàn bộ người hướng dẫn của mẫu. |
| Ngành trên bìa | Artificial Intelligence | Giữ theo mẫu theo yêu cầu chỉ thay tên, đề tài và người hướng dẫn; chưa có hồ sơ ngành/chương trình chính thức riêng. |
| Loại tài liệu | BACHELOR'S GRADUATION THESIS | Giữ theo hai bìa mẫu. |
| Địa điểm/năm trên bìa | HA NOI - 2026 | Giữ theo mẫu theo yêu cầu tác giả; không suy ra hạn nộp hay ngày bảo vệ. |
| Logo | Logo UET gốc, chỉ ở bìa ngoài | Sao chép nguyên byte từ `Latex/images/UET_logo.jpg` vào [tài nguyên khóa luận](assets/figures/UET_logo.jpg). Bìa trong mẫu không có logo. Quyền phát hành lại ngoài phạm vi khóa luận chưa được xác minh. |
| Mẫu trình bày đã chọn | Hai trang đầu [23020332_Tran_Xuan_Bao.pdf](../23020332_Tran_Xuan_Bao.pdf) | Yêu cầu trình bày của tác giả, không phải chứng cứ trường đã phê duyệt toàn bộ mẫu. |
| Hạn nộp/ngày bảo vệ | Chưa xác định | Tác giả xác nhận tạm thời chưa có hạn nộp; không tự đặt ngày. |
| Quy định trích dẫn chính thức | Chưa được cung cấp | Tác giả xác nhận tạm thời chưa có; numeric theo thứ tự xuất hiện chỉ là gợi ý từ `biblatex` trong mẫu, chưa chốt thành quy định. |
| Quy định bố cục chính thức | Chưa được cung cấp | Tác giả xác nhận tạm thời chưa có; A4, cỡ thân bài 12 pt, giãn dòng 1,5, lề và đánh số trang là quan sát từ nguồn mẫu. |
| Biểu mẫu bắt buộc, lời cam đoan, chữ ký, phê duyệt | Chưa xác định | Chưa nhận văn bản chính thức hoặc phê duyệt; không sao chép lời cam đoan/chữ ký của tác giả mẫu. |

### Đối chiếu hai trang bìa

- Giữ A4, Latin Modern, hai dòng tên trường, khung đôi và vị trí logo/tác giả
  theo mẫu; logo rộng `0.25\textwidth`. Khung ngoài cách trái 2 cm, trên
  1,5 cm, phải 1,5 cm, dưới 2 cm; khung trong lùi 0,15 cm.
- Bìa ngoài có logo, bìa trong có Supervisor; cả hai không có số trang.
- Đề tài mới dài hơn đề tài mẫu, nên giữ cỡ `\Large` và chia thành năm dòng
  nhất quán trên hai bìa. Bìa trong giảm khoảng trắng quanh tiêu đề để giữ
  khoảng tách với loại khóa luận/ngành/người hướng dẫn. Đây là điều chỉnh
  dàn dòng cho nội dung mới, không phải tuyên bố đồng nhất từng pixel.
- [Nguồn bìa độc lập](latex/frontmatter/covers.tex) và
  [trình biên dịch bản xem](latex/covers-preview.tex) chỉ phục vụ kiểm yêu cầu
  bìa đã cung cấp sớm; chưa thay thế khung LaTeX toàn văn hay hoàn tất phần đầu.
  [Bản PDF xem bìa](release/covers-preview.pdf) không phải bản khóa luận hoàn chỉnh.
- Markdown vẫn là nguồn nội dung chính. Khi đổi metadata tại
  `frontmatter.md`, phải đồng bộ bản trình bày LaTeX và biên dịch/kiểm lại PDF;
  chưa có chuyển đổi nguồn bản nộp sang LaTeX.

Thông tin còn thiếu chỉ chặn phần hoàn thiện phụ thuộc nó: mã chương trình
chính thức nếu khác ngành trên mẫu, biểu mẫu/câu chữ bắt buộc, kiểu trích dẫn,
giới hạn số trang, quy cách đóng/nộp và hạn nộp. Có thể tiếp tục viết nội dung
kỹ thuật. Hồ sơ yêu cầu đầy đủ theo nghĩa mỗi trường đã có nguồn hoặc ghi rõ
chưa xác định; không có nghĩa các yêu cầu nộp đã được trường xác nhận.

## 2. Phạm vi nghiên cứu và ranh giới luận điểm

[Dàn bài §A](outline.md#a-research-direction) là nơi giữ tên đề tài, RQ1–RQ4,
đóng góp và phạm vi sáu chương đã rà. Không sao chép thêm một bảng trạng thái
ở đây. Đối chiếu dùng cây nguồn
`develop:896353b3e07dc3d7fbae328fb647fd3dd738c15c` làm mốc khảo sát; các file
live dưới đây chỉ xác nhận thành phần đang tồn tại. Kết quả nghiên cứu phải
dùng nguồn/runtime được khóa trong receipt tương ứng, không lấy HEAD live
thay thế.

### Nguồn đối chiếu cho câu hỏi và giới hạn

| ID nguồn | Nguồn | Vai trò trong lần rà này | Giới hạn |
| --- | --- | --- | --- |
| S01 | [Thiết kế thực nghiệm](../paper/content/experimental_setup.tex), [support thành phần](../paper/content/tables/component/scope.tex) | RQ1: Full/Base, đối chứng số, panel upstream/factorial, đơn vị và sự khác biệt hai nghiên cứu. | Bản thảo/bảng dẫn tới bằng chứng; kiểm kê tận ô và khôi phục nguồn đóng băng thuộc bước kiểm kê tiếp theo. |
| S02 | [Kết quả](../paper/content/results.tex), [bảng support ngữ cảnh](../paper/content/tables/historical_context/support.tex) | RQ2: hai họ so sánh với Common/Native, fallback và độ phủ. | Không suy kết quả dùng prior thường xuyên từ tên phương pháp; luôn giữ support và trường hợp fallback. |
| S03 | [Registry](../core/variant_registry.py), [policy](../core/mt_bicl_policy.py), [bridge](../paper/content/tables/historical_context/bridge.tex) | RQ3: tám vai trò, phụ thuộc Common/Fact Anchor/MT-BICL, proposal/final action và điều kiện utility. | Mã live là nguồn giải thích; bridge là mô tả các can thiệp gộp, không cô lập student. |
| S04 | [Receipt phân tích U09](../docs/plan/week12/unified_analysis_acceptance.json), [gói kết quả](../docs/plan/week12/unified_analysis_results.zip) | RQ4: định danh nghiên cứu, 102 điểm/2.448 slot, cold replay 15 artifact và phạm vi audit được ghi nhận. Hash ZIP hiện tại khớp `payload.results_package.sha256`. | Chỉ kiểm hash gói/đọc receipt trong lần này; không chạy lại replay hoặc gate runtime, không tự chứng nhận toàn hệ. |
| S05 | [Hạn chế](../paper/content/limitations.tex), [trạng thái tích hợp](../docs/plan/plan.md) | Giữ các kết luận âm, nhân quả, provenance, ablation chưa chạy và UI chưa nghiệm thu. | F11 vẫn PENDING; trạng thái tài liệu không đóng nghiệm thu ứng dụng. |

Các điểm chặn cách diễn giải đã đối chiếu:

1. Full/Base là so sánh trong nghiên cứu thành phần. Native/Common là cầu
   nối profile trong nghiên cứu ngữ cảnh, thay cả biểu diễn Alpha và chỉ dẫn;
   **Base không phải Common**. Không gộp response hai nghiên cứu thành một mẫu.
2. Nghiên cứu ngữ cảnh có 102 điểm, ba repeat và tám vai trò: 2.448 slot.
   Repeat của Decision giữ nguyên một realization upstream; không tăng số
   quan sát thị trường hoặc đo toàn bộ biến thiên đa agent.
3. C2 và B_semantic chỉ có ba raw Decision mỗi phương pháp; A_tp_pool có 24.
   MT-BICL trùng Fact Anchor ở 302/306 hành động cuối. Những số này được dùng
   để giới hạn câu hỏi quy thuộc cơ chế, không thay cho phân tích kết quả.
4. Mọi return trung bình của tám vai trò nghiên cứu đều âm. Lợi thế Bayesian
   v1 so với Common trong band mô tả không chứng minh vượt Native hay sinh lời.
5. Native row-wise causal vẫn `FAIL`; whole-system causal vẫn
   `NOT_CERTIFIED`. Kiểm cutoff bên ngoài không khắc phục nhân quả từng hàng.
   Khác biệt return bank/query 828/852 bản ghi không phải số nhãn đã đổi.
6. Retrieval-only, statistics-only, no-prior, no-target, no-utility và tách
   student/policy chưa có kết quả trong nghiên cứu ngữ cảnh thống nhất.
   Không dùng panel factorial thành phần để nhận thay các ablation này.

### Định danh nguồn đã dùng trong lần rà

SHA-256 dưới đây là hash toàn file tại thời điểm khảo sát. Đây là danh sách
nguồn tối thiểu cho metadata và phạm vi, chưa phải inventory đầy đủ hai
nghiên cứu. Nguồn mẫu gốc đang nằm ngoài Git; logo cần thiết đã được đưa vào
cây `thesis/` để bản xem không cần đọc `Latex/` khi biên dịch.

| Đường dẫn | SHA-256 |
| --- | --- |
| `23020332_Tran_Xuan_Bao.pdf` | `885413c427959b34e7ed5370fe516d9a4364499bfc8f7589517522d875138b15` |
| `Latex/chapters/00_covers.tex` | `86a51194673f34c242415b6620caeadf229828a070261e5bcf03916c8722fb78` |
| `Latex/preamble.tex` | `6d16f909215eb82924d91cb8cbdeefcfbbb4d24f30648b4534c66f9b136aaf48` |
| `thesis/assets/figures/UET_logo.jpg` | `d71ffc8c4e8d40e1497d54c1fb25621bcd8ef8c0ad0cb73ee0c356980be66229` |
| `core/variant_registry.py` | `30067f05c3b59c8fc3a44bdc3cd55f9adeb3796b21ee2b39c129355781938ae8` |
| `core/mt_bicl_policy.py` | `301525c36c150e21f09a1971101d53d5927cf38c1d2921017c477441e097b488` |
| `paper/content/experimental_setup.tex` | `a6328ee5892106e9e98a2ee40aac81ca8ec7bafa6b35dcc321a87c59a6df1ccc` |
| `paper/content/results.tex` | `c7b61e835ba4b41d4605b65b5531af21444f01cd226260cc42951a073b6380cd` |
| `paper/content/limitations.tex` | `5a88b722c31bdfdaaefe0718e983379e6a7857a728532c7838dfba874044afe4` |
| `docs/plan/week12/unified_analysis_acceptance.json` | `6b435c21c89000775be1f1e1d043b6b3429a0729f37efc16f4bd03be92355456` |
| `docs/plan/week12/unified_analysis_results.zip` | `e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9` |

## 3. Quy ước bổ sung sổ nguồn

Khi bắt đầu kiểm kê và đọc tài liệu, bổ sung nguồn/phiên bản/hash, support,
ánh xạ luận điểm/ô bảng, ghi chú kiểm nguồn gốc và danh mục hình/bảng vào sổ
này. Chưa có bibliography mới, bản thảo sáu chương hoặc kết quả tính lại
trong lần chuẩn bị này. Trạng thái và cách kiểm nằm duy nhất tại
[checklist khóa luận](../docs/plan/week12/README.md#checklist-viết-khóa-luận).
