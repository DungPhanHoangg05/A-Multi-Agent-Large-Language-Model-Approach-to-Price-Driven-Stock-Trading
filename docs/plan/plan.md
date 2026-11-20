# Kế hoạch nghiên cứu và triển khai KLTN

Đề tài Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent
LLM Stock Trading in the Vietnamese Stock Market.

## Trạng thái hiện hành

### Kế hoạch finalize hệ thống — cập nhật 20/11/2026

**Mục tiêu bàn giao ngày 20/11/2026 gồm hệ thống đã sửa, bài báo trong
`paper/` và khóa luận trong `thesis/`.** FIN00–FIN13 đã hoàn tất trong
phạm vi ghi dưới đây. Giao diện `finalize_serving_v1` đã qua hồi quy offline
FIN14. Tác giả chuyển sang FIN15 trước và để phần giao diện còn lại làm sau.
Phát hành hosted, chuyển mặc định và FIN16–FIN17 còn mở.
Mục tiêu là bàn giao một bản hệ thống có định danh và miền hỗ trợ rõ ràng,
đạt các kiểm tra nhân quả dữ liệu, kinh tế, ghép cặp và phục hồi áp dụng,
chạy được qua các điểm vào thực tế, có kết quả đánh giá và tài liệu khớp nguồn.
Lợi nhuận âm hoặc chưa đủ bằng chứng vượt đối chứng tiếp tục được báo cáo theo kết quả đo.

Theo yêu cầu hiện hành, **checklist FIN00–FIN17 ngay tại đây là nguồn tiến độ
finalize duy nhất**. README W12 tiếp tục là nguồn bằng chứng U/F đã ghi nhận;
[thesis/plan.md](thesis/plan.md) quản lý các task biên tập/nộp khóa luận.
Các nhận định về đầu mối và trạng thái trong phần lịch sử bên dưới gắn với
mốc được ghi. Task finalize tham chiếu các bằng chứng đó theo đúng phạm vi.

#### Lịch bàn giao 18–20/11/2026

| Mốc đã đối chiếu | Bằng chứng và giới hạn |
| --- | --- |
| FIN01–02 | Manifest inventory và hợp đồng so sánh khớp checksum, cả năm nguồn cha của hợp đồng khớp hash. Giữ 102 điểm, chín mã, ba repeat và tám vai trò gồm sáu phương pháp cùng Common và Fact Anchor. |
| FIN03 | Gói QA Alpha khớp SHA-256 đã khóa. Log ghi 9 test mới và 32 test hồi quy đạt. Phạm vi đã kiểm gồm 85 yếu tố và bridge offline. Các caller thực tế của bản sửa còn thuộc FIN08/14. |
| FIN04 | Kiểm lại validator offline cho kết quả `PASS_OWNER_ATTESTED`. Có 102 forecast dự kiến, 97 điểm qua bộ lọc quyền ban đầu và năm nhãn kinh tế NA. Cờ chứng cứ giá PIT độc lập vẫn là `false`. |
| FIN05 | Validator offline xác nhận 102/102 điểm thiếu tin đủ chứng cứ tại cutoff. Snapshot giữ NA và lý do. Gói QA tin khớp hash. |
| FIN06 | `PASS_OFFLINE_FIN06`. Có 852 chu kỳ đủ khóa thống kê, 733 đủ khóa ví dụ, 119 Alpha NA và 102 khóa query đã kiểm. Phát hành bank offline với 0 HTTP mới. Batch thị giác trước đó thu 2/1.704 slot cùng một chu kỳ, dùng 2.505 và 1.412 token. |
| FIN07 | `PASS_OFFLINE_FIN07`. Oracle kiểm retrieval và ngữ cảnh trên 102 điểm. MT-BICL có 63 đủ support và 39 bypass. Fixture xác nhận C2/A/B lấy ví dụ khi qua gate. Đã kiểm cùng repeat và giữ nhãn query đóng. |
| FIN08 | `PASS_OFFLINE_FIN08`. CLI, as-of, backtest và live nhận profile mới chọn tường minh. Kiểm 522 cặp mã–phiên as-of và replay raw capture đối chứng. Hosted chờ FIN10, default chuyển sau FIN13–FIN14. |
| FIN09 | `PASS_OFFLINE_FIN09_BUDGET`. Đối chiếu 2.662 slot với 1.702 attempt U08. Có 10 vision reuse, 1.165 bypass và 1.487 slot gọi mới kể cả smoke. Dự toán một org Free lấy Decision làm giới hạn. |
| FIN10 | `PASS_OFFLINE_FIN10`. Khóa 162 pin tài nguyên và ledger FIN09. Đạt 153 kiểm thử theo phạm vi. Cold replay 56 slot đối chứng, 0 dispatch mới. FIN11 đã đối soát lại các khóa liên quan. |
| FIN11 | `PASS_FIN11`. Smoke đạt 8 forecast. Nghiên cứu đủ 102 điểm và 2.448 forecast. Đã đối soát 1.511 attempt kể cả smoke và bản lưu. Outcome thị trường chưa được mở. |
| FIN12 | Đánh giá offline từ receipt FIN11. Có 96/102 nhãn thực thi và 45/51 tài khoản đủ hai chu kỳ. Endpoint chính giữ NA. Oracle và cold verify đạt trên phạm vi có dữ liệu. |
| FIN13 | `PASS_FIN13_OWNER_ATTESTED_SCOPE` cho cohort gốc và profile sửa trên nguồn giá tác giả xác nhận. Chứng nhận PIT nguồn độc lập vẫn `NOT_CERTIFIED`. |
| FIN14 | Hồi quy giao diện đạt trên Chromium desktop/mobile với transport đối chứng. Backend ứng dụng vẫn chặn hosted cho `finalize_serving_v1`. Mặc định đang dùng profile hiện hành. |
| FIN15 | Hai bản thảo thống nhất tên QuantAgent, Our system và BICL v1–v5, có bảng phân biệt và sơ đồ tổng thể. Đã đối soát FIN12 và build sạch cả bài báo lẫn khóa luận. |

Bằng chứng đối chiếu gồm [inventory](week12/finalize_inventory.json),
[hợp đồng so sánh](week12/finalize_comparison_contract.json),
[gói QA Alpha](week12/finalize_alpha_checks.zip),
[nghiệm thu giá](week12/finalize_price_acceptance_v1.json),
[độ phủ tin](week12/finalize_news_coverage_v1.json),
[manifest bank OHLCV](../../outputs/finalize/ohlcv_bank_v1/manifest.json) và
[kế hoạch slot thị giác](week12/finalize_bank_collection_plan_v1.json).

**Vì sao đổi cách chuẩn bị bank.** Với mức dùng của cặp đầu tiên, 852 cặp
cần khoảng 3,34 triệu token. Một org theo cấu hình 200.000 token/24 giờ cần
khoảng 17 ngày quota chỉ riêng cho bank. Đây là ngoại suy từ một chu kỳ,
chưa tính retry hay query. Tăng số worker vẫn dùng chung hạn mức đó.

**Quyết định phương pháp cho bản sửa.** Tạo profile riêng cho khóa tìm kiếm
của bank. Từ cửa sổ 45 nến kết thúc tại cutoff, tính hai tín hiệu bằng quy
tắc OHLCV xác định. Ngày đầu phải khóa công thức nhận diện mẫu nến, hướng xu
thế, ngưỡng, cách xử lý thiếu dữ liệu và phiên bản nguồn. Dùng cùng hàm và
cùng ngữ nghĩa ở phía bank và phía query cho v1/C2/A/B, gồm so khớp ví dụ
và các thống kê điều kiện. Các báo cáo Pattern/Trend thị giác thật vẫn đi
qua upstream chung tới Decision. MT-BICL tiếp tục dùng context số, student,
teacher và Fact Anchor theo hợp đồng riêng. Tên trường và phần giải thích
phải cho biết tín hiệu nào do quy tắc sinh, báo cáo nào do model sinh.
Khóa quy tắc từ định nghĩa kỹ thuật và fixture OHLCV trước khi đối chiếu
với tín hiệu đã thu. Hàm sinh khóa chỉ nhận nến đã biết tại ngày quyết định.
FIN07 kiểm cả nhánh đủ support và fallback trên fixture, đồng thời ghi độ
phủ thực tế của từng mã/regime trên bank mới.

Phương án này cần **0 lượt vision mới cho bank**. Giữ nguyên 852 ID, nhãn
kinh tế, 119 Alpha NA và 733 ứng viên có Alpha. Hai phản hồi thật đã thu
thuộc batch thị giác cũ. Lưu nguyên journal để truy vết hoặc tiếp tục batch
đó về sau. Chỉ phát hành profile mới sau khi đã có manifest, verifier và
receipt của chính nó. Độ đúng được kiểm bằng công thức đã khóa, oracle độc
lập và tính nhân quả theo prefix. Báo cáo mức trùng/khác với tín hiệu thị
giác trên dữ liệu có sẵn kèm cỡ mẫu. Một cặp đã thu chưa đủ để kết luận hai
cách tương đương hoặc phương pháp mới cải thiện lợi nhuận.

| Hạn | Công việc theo thứ tự và việc có thể chuẩn bị song song | Điều kiện ra khỏi ngày |
| --- | --- | --- |
| **18/11 · Khóa phương pháp và kiểm tính khả thi** | FIN06/09 khóa amendment máy đọc cho bank và khóa truy xuất query trước khi xem outcome. Dựng hai tín hiệu từ checkpoint/prefix đã pin, tái dùng nhãn, selector, HMM và scaler theo hash. Song song truy chứng cứ nguồn giá gốc, lịch giao dịch và lịch sử sự kiện. Lập dự toán FIN11 cho 102 điểm, gồm quota còn lại, tokens theo model, raw có thể tái dùng, retry và thời gian chờ. | Có manifest 852 ID, số hàng đủ điều kiện thống kê/ví dụ và lý do NA. Verifier tái dựng từng tín hiệu. Chốt khả năng có nguồn PIT độc lập và đủ năng lực gọi query trong thời gian còn lại. Thiếu đầu vào nào ghi rõ blocker và báo ngay trong ngày. |
| **19/11 · Tích hợp, kiểm gate và thu** | FIN07/08 nối profile vào retrieval, MT, CLI, backtest, as-of và realtime với cache version mới. FIN09 chốt số gọi thực sau dry-run. FIN10 chạy kiểm tra bị ảnh hưởng, gồm future poison, economics, paired, token và phục hồi. Khi FIN10 đạt và có quota đã duyệt, FIN11 chỉ thu slot thiếu, cùng upstream và checkpoint. Song song soạn phần phương pháp/giới hạn của cả hai bản thảo. | Cold replay và đường chạy thực nhận đúng profile. Ledger ghi reuse/new/bypass/UNKNOWN cho từng slot. Từng điểm có đủ forecast theo protocol trước khi mở outcome. |
| **20/11 · Đối soát và bàn giao** | FIN12 đối soát số học và support theo hai baseline. FIN13 ký receipt bản sửa theo từng cờ, FIN14 kiểm UI/export rồi mới chuyển default. FIN15 cập nhật bảng/hình và kết luận từ đúng receipt cho cả hai bản thảo, build/render cả hai. FIN16 kiểm khôi phục sạch. FIN17 chốt trạng thái và bàn giao. | Có bản chạy được, manifest/receipt, kết quả tái lập, bản build bài báo và khóa luận. Chỉ đóng toàn bộ khi mọi gate áp dụng đã đạt. Nếu còn thiếu chứng cứ hoặc query chưa đủ, bàn giao phần đã xác minh ngày 20/11 và ghi rõ tiêu chí còn mở. |

**Hai điều kiện có thể làm lỡ hạn dù bank chạy offline**

- **Nguồn giá.** FIN04 cho phép dùng giá theo xác nhận của tác giả. Để đóng cờ
  PIT nguồn độc lập, cần bản lưu giá có bằng chứng khả dụng tại cutoff, lịch
  và chứng cứ sự kiện bao phủ miền công bố. Đối soát phiên bản, coverage,
  timestamp và hash rồi chạy lại validator độc lập trên nguồn đó. Nguồn thay
  đổi phải tái dựng các tài nguyên phụ thuộc và tính lại dự toán reuse. Nếu
  còn thiếu, ghi riêng PASS của phần mềm theo giả định nguồn và giữ
  `NOT_CERTIFIED` cho chứng nhận nguồn tương ứng.
- **Query thật.** Ngân sách 0 lượt mới chỉ áp dụng cho khâu sinh tín hiệu
  bank. FIN09 tách tối đa 204 slot vision upstream, 2.448 slot Decision và
  phần smoke trước reuse/bypass. So ngân sách token thực còn lại từng model
  với thời gian đến hạn. Nếu vượt, ưu tiên khôi phục raw tương thích hoặc
  xin năng lực chạy bổ sung đúng protocol. Nếu vẫn thiếu, giữ nguyên các ô
  pending. Kết quả U09 trong bài báo/khóa luận tiếp tục mang định danh lịch
  sử cho đến khi FIN12 có đủ kết quả của bản sửa.

#### Phạm vi bản cuối và điều kiện kết thúc

- Bao phủ sáu lựa chọn ứng dụng, hai vai trò Common/Fact Anchor và các caller
  CLI, backtest, serving as-of, realtime 1D cùng viewer/export đang được hỗ trợ.
- Khóa profile sửa Alpha của hệ gốc bằng version mới, tái sử dụng
  [causal_common_v1](../../core/causal_alpha.py) và
  [bridge hiện có](../../core/causal_bridge.py). Giữ định danh Native đã tạo
  ra kết quả cũ để truy vết; bản sửa có source/resource/request identity riêng.
- Bộ dữ liệu và tài nguyên của bản cuối phải có bằng chứng đáp ứng phạm vi
  PIT đã công bố. Khi thiếu nguồn gốc cần khôi phục hoặc tái tạo nguồn có lưu
  vết trước nghiệm thu; quy tắc eligibility được khóa trước outcome.
- Mặc định ưu tiên đánh giá sửa đổi trên lịch 102 điểm đã có và tái sử dụng
  các lời gọi còn hợp lệ. Thay đổi nguồn/cohort cần protocol và nhãn phiên bản
  tương ứng. Nghiên cứu xác nhận trên dữ liệu chưa xem là phần tiếp nối khi
  có mục tiêu xác nhận hiệu quả, nằm ngoài điều kiện đóng bản kỹ thuật này.
- Trước khi đóng, các gate áp dụng của bản mới đạt PASS trong miền đã khóa,
  mọi ô/kết quả cần thiết đã hoàn tất, tài liệu và gói khôi phục đã đối soát.
  Vấn đề còn chặn gate phải có bằng chứng xử lý trước khi đánh dấu hoàn thành.
- Receipt Native/U08/U09 và kết quả lịch sử tiếp tục chứng nhận snapshot cũ.
  Báo cáo bản mới ghi riêng trạng thái từng profile, miền, dữ liệu và thời điểm.
  Các giới hạn về kiến thức huấn luyện của LLM và khớp lệnh thực tế được nêu
  đúng phạm vi chứng minh của nghiên cứu.

#### Hợp đồng áp dụng xuyên suốt

LONG vào Open(t+1), ra Close(t+3) theo phiên; SHORT giữ CASH; phí 0,25% và
slippage 0,10% mỗi chiều. Nhãn dùng `compute_round_trip_net_return`.
Giá query ≤ cutoff, tin có thời điểm khả dụng hợp lệ, episode có exit < cutoff.
Orientation/scaler/HMM/student/selector tuân thủ lịch fit đã khóa, nhãn qua
ranh giới split được purge. Upstream Indicator–Pattern–Trend chạy một lần
mỗi point/realization và được deep-copy; outcome query ở sau forecast barrier.
BRPP K=3 ≤600 ký tự, prompt Decision backtest <6.500 ký tự, retry/checkpoint
và đối soát UNKNOWN dùng các primitive hiện có.

#### Checklist thực thi và đầu ra nghiệm thu

Mỗi ô chỉ được đánh dấu khi đã có đầu ra và bằng chứng của chính task.
Các task kỹ thuật tiếp theo dùng workflow theo AGENTS và chỉ đạo Git còn
hiệu lực của người dùng. Lập kế hoạch tự nó chỉ hoàn thành FIN00.

- [x] **FIN00 — Lập kế hoạch finalize.** Đối chiếu plan, registry, causal alpha,
  bridge, audit, serving contract và acceptance U09; khóa thứ tự việc và tiêu
  chí tại đây. Kiểm tài liệu theo ghi nhận cuối mục.
- [x] **FIN01 — Khóa inventory bản làm việc và nguyên nhân các cờ.** Ghi commit,
  runtime, tài nguyên, receipt và đường gọi thực tế của từng phiên bản. Phân
  loại cờ lịch sử, lỗi còn tái hiện và phần thiếu bằng chứng. Đầu ra là bảng
  ảnh hưởng trong checklist này cùng manifest máy đọc dùng lại hạ tầng hiện có.
  Đạt khi mọi FAIL/NOT_CERTIFIED của miền dự kiến có nguồn, task xử lý và tiêu
  chí kiểm lại. Phụ thuộc FIN00, thực hiện offline.
- [x] **FIN02 — Chốt hợp đồng bản cuối và thiết kế so sánh.** Khóa miền mã/ngày,
  source/availability, profile sửa, hai nền đối chứng, các dependency,
  phương pháp/controls, support/fallback, lịch fit/purge, metric và chính sách
  thiếu dữ liệu. Nêu chính xác delta Native sửa/Common; trường hợp request
  tương đương được nhận diện để tái sử dụng. Chốt mọi thay đổi phương pháp
  trước khi xem kết quả mới. Phụ thuộc FIN01.
- [x] **FIN03 — Hoàn thiện Alpha nhân quả và selector.** Tái sử dụng logic hiện
  có để xử lý bfill, chuẩn hóa toàn chuỗi, nhánh volume toàn cửa sổ và sáu
  cửa sổ theo độ dài input. Kiểm đủ 85 yếu tố, warm-up/missing, origin cố định,
  orientation train, lựa chọn validation và đóng băng trước test. Đạt khi
  prefix extension/future poisoning không viết lại quá khứ, giá test không
  tác động fit và caller nhận đúng profile. Phụ thuộc FIN02, chưa cần hosted API.
- [x] **FIN04 — Hoàn thiện nguồn giá, lịch và sự kiện doanh nghiệp.** Đối soát
  giá bank/query, đơn vị, lịch phiên, thời điểm khả dụng và điều chỉnh sự kiện.
  Khôi phục snapshot hoặc tạo nguồn thay thế có định danh/lưu vết khi cần;
  ghi rõ phần thay đổi dataset và tác động đến nhãn/đặc trưng. Đạt khi các
  nguồn trong miền nghiệm thu được validator và oracle chấp nhận, còn các
  giới hạn vendor được mô tả chính xác. Phụ thuộc FIN02.
  **PASS_OWNER_ATTESTED:** tác giả xác nhận giá chính xác và yêu cầu đóng FIN04.
  Acceptance có version/nguồn/recipe; giữ 102 forecast planned và năm nhãn kinh tế
  unavailable do quyền. Chưa chứng nhận PIT nguồn độc lập; raw thay donor cần
  tái tạo tài nguyên chịu ảnh hưởng tại FIN06 trước query mới.
- [x] **FIN05 — Hoàn thiện PIT tin tức.** Đối soát nội dung, nguồn, thời gian
  xuất bản/khả dụng/thu thập, scorer và aggregation. Thu bổ sung hoặc khóa
  nguồn phục vụ bản mới khi thiếu bằng chứng; giữ unavailable có lý do theo
  contract. Đạt khi tin future/undated/sửa sau cutoff được xử lý đúng và cùng
  một snapshot cung cấp báo cáo/hiển thị. Phụ thuộc FIN02; tác động API được
  đưa vào FIN09, dữ liệu cần thu mới được khóa trước sử dụng.
  **PASS_NEWS_PIT_WITH_EXPLICIT_UNAVAILABLE:** profile/snapshot/corpus đã khóa,
  14 test PASS. Cả 102 điểm hiện NA; không đủ chứng cứ nội dung PIT để dùng
  tin legacy. FIN08 nối profile vào ứng dụng; không coi NA là điểm trung tính.
- [x] **FIN06 — Hoàn thiện bank, regime và tài nguyên fit.** Truy nguồn tín
  hiệu/giá/nhãn từng chu kỳ dùng trong bản cuối, xử lý chênh cơ sở giá, kiểm
  strict maturity, train cutoff của HMM/scaler và quy tắc OOD. Nếu cần tái tạo
  bank hoặc refit tài nguyên, có recipe, nhật ký và version mới trước inference
  query. Đạt khi membership/labels/resources được tái dựng và query outcome
  không tác động preparation. Phụ thuộc FIN03–FIN05; nhu cầu API chuẩn bị
  lịch sử được ghi trong FIN09.
  **Nghiệm thu theo lịch ba ngày.** Cấp recipe và namespace mới trước query.
  Kiểm đủ 852 ID, hash cửa sổ, cutoff, hướng tín hiệu và NA từng dòng bằng
  replay. Đối chiếu với oracle trên ca tăng/giảm/đi ngang/thiếu nến, kiểm
  ranh giới ngưỡng và thay đổi hậu tố tương lai. Dùng bản manifest đã kiểm
  để cấp bank cho FIN07. Đã đạt `PASS_OFFLINE_FIN06` với
  [profile OHLCV xác định](#fin06--phát-hành-bank-ohlcv-xác-định). Batch thị
  giác 1.704 slot thuộc recipe trước đây.
- [x] **FIN07 — Kiểm MT-BICL và toàn đường ngữ cảnh.** Kiểm context prior/target,
  fold freeze, reserved IDs, student/teacher, facts, support và thỏa dụng;
  giữ riêng p_student và teacher utility. Kiểm v1/C2/A/B dùng đúng nguồn,
  cổng và mẫu số; kiểm anchor và Q10/Q90 qua các trường hợp chấp nhận/bypass/
  phủ quyết. Đạt khi thay đổi future/query label không đi vào preparation,
  request hoặc policy trước barrier. Kiểm riêng thống kê bẫy tăng/sai hướng,
  tập theo mã/regime, điều kiện T/P và các mẫu số bằng oracle cho profile mới.
  Đối chiếu đúng khóa query/bank, retrieval thực sự hoạt động ở ca đủ support
  và lý do fallback ở ca thiếu support. Phụ thuộc FIN03–FIN06, ưu tiên offline.
  Đã đạt `PASS_OFFLINE_FIN07` theo [receipt](week12/finalize_context_receipt_v1.json).
- [x] **FIN08 — Nối bản sửa vào các điểm vào thực tế.** CLI/backtest/as-of/live
  dùng đúng profile, snapshot, dependency và cache identity mới. Default của
  bản phát hành chuyển sang đường đã sửa sau nghiệm thu; dữ liệu cũ được
  hiển thị đúng profile lịch sử. Trạng thái khoa học của bản mới được dẫn từ
  bằng chứng đã kiểm và đúng miền. Đạt khi không còn caller thuộc bản cuối
  gọi nhầm Alpha cũ, trộn cache hoặc gán receipt cũ cho nguồn mới. Có thể
  nối caller bằng fixture ngay khi schema FIN06 đã khóa. Nghiệm thu tích hợp
  sau FIN07, chuyển default sau FIN13–FIN14. Đã đạt `PASS_OFFLINE_FIN08`
  theo [kết quả kiểm tích hợp](#fin08--nối-profile-finalize-vào-ứng-dụng).
- [x] **FIN09 — Chốt bảng tái sử dụng và ngân sách API.** Đối chiếu từng request
  và dependency với archive, ghi slot dùng lại/chạy mới/bypass và lý do.
  Tính cả gọi chuẩn bị bank, vision, anchor, repeats, smoke, retry và quota
  còn sử dụng; chốt model/options, giới hạn lượt gọi và chi phí/thời gian có
  căn cứ trước thu. Đạt khi số slot/call kiểm được bằng dry-run và mọi lời gọi
  có nhu cầu thực tế. Phụ thuộc FIN01–FIN02; lập dự toán sơ bộ ngay sau FIN02,
  cập nhật theo delta FIN03–FIN08. Với profile bank xác định, dự toán bank
  là 0 HTTP. Khóa riêng ngân sách model cho query, gồm quota còn lại sau các
  lượt đã dùng, token và thời gian cho mỗi model. Kiểm lại ngay sau dry-run
  trước FIN10/11. Đã đạt `PASS_OFFLINE_FIN09_BUDGET` theo
  [kết quả đối chiếu và dự toán](#fin09--chốt-bảng-tái-sử-dụng-và-ngân-sách-api).
- [x] **FIN10 — Nghiệm thu offline trước thu query.** Khóa code/runtime/resource
  và chạy các kiểm tra trực tiếp bị ảnh hưởng, gồm PIT toàn pipeline,
  economics, paired dependency, prompt/schema, retry/checkpoint, owner/cache,
  stop/resume và UNKNOWN. Cold replay bằng fixture kiểm đường mới. Đạt khi
  mọi kiểm tra áp dụng PASS, source pin khớp và blocker chuẩn bị đã được xử lý.
  Phụ thuộc FIN03–FIN09; sửa mới phải kiểm lại phạm vi ảnh hưởng trước thu tiếp.
  Đã đạt `PASS_OFFLINE_FIN10` theo [receipt và replay](#fin10--nghiệm-thu-offline-trước-thu-query).
- [x] **FIN11 — Thực thi thu hồi đáp cần thiết.** Dùng protocol và ngân sách
  FIN09 đã khóa cho các slot thực sự cần gọi. Reuse upstream hợp lệ, checkpoint
  mỗi point, lưu raw/usage/epoch và cùng-repeat dependency. Đạt khi planned =
  complete cho miền đã khóa, mọi attempt được đối soát; thiếu/lỗi giữ nguyên
  trạng thái để xử lý. Phụ thuộc FIN10 và phạm vi thực thi/ngân sách có hiệu
  lực. Task có thể hoàn thành bằng audit 0 call nếu toàn bộ response còn hợp lệ.
  Đã đạt `PASS_FIN11` theo [nghiệm thu lượt thu](#nghiệm-thu-fin11-ngày-20112026).
- [x] **FIN12 — Đánh giá lại bản sửa.** Tính nhãn, tài khoản và metrics bằng
  engine/evaluator đã kiểm; giữ đủ support, raw/final, bypass, NA và kết quả
  âm. So với hai baseline đúng profile, báo epoch và nguồn các phản hồi reuse.
  Kiểm toán độc lập số học và khôi phục artifact phân tích trong tiến trình
  mới. Đạt khi mọi ô có provenance và số liệu khớp oracle. Phụ thuộc FIN11;
  chỉ tái tạo các phân tích bị ảnh hưởng theo protocol đã chốt.
  Đã đạt theo [nghiệm thu FIN12](#fin12--đánh-giá-offline-bản-sửa).
- [x] **FIN13 — Chốt nghiệm thu hệ thống trong miền công bố.** Tổng hợp bằng
  chứng FIN03–FIN12 theo từng profile/caller/input. Bản sửa đạt row-wise
  causal và toàn pipeline PIT trong miền đã khóa; integrity, economics,
  pairing và recovery đạt điều kiện tương ứng. Gate chưa có bằng chứng tiếp
  tục chặn đóng task. Receipt ghi source/runtime/data/model/scope; bản ghi
  Native cũ vẫn dẫn đúng phản ví dụ đã lưu. Lập bảng từng cờ FIN01 với
  profile/caller, phản ví dụ cũ, phép kiểm bản sửa, kết quả và receipt.
  Kiểm cả trường hợp dữ liệu giả sai phải bị từ chối. Chứng nhận PIT nguồn
  độc lập cần bằng chứng giá riêng nêu tại lịch ngày 18/11. Phụ thuộc FIN10
  và FIN12.
  Đạt `PASS_FIN13_OWNER_ATTESTED_SCOPE` sau khi tác giả xác nhận nguồn giá và
  yêu cầu tiếp tục FIN14. [Đối soát FIN13](#fin13--đối-soát-cờ-của-bản-sửa)
  giữ riêng kết luận PIT nguồn độc lập `NOT_CERTIFIED`.
- [ ] **FIN14 — Hồi quy ứng dụng trên phần thay đổi.** Kiểm sáu lựa chọn,
  Common/Fact Anchor, input/preflight, tiến trình, lỗi/partial/UNKNOWN,
  raw/final/context, kết quả cũ/mới, VI/EN, theme và export. Kiểm trực quan
  desktop/mobile cho các màn hình bị ảnh hưởng, ghi nhận quan sát thực.
  Đạt khi UI trình bày đúng nguồn/profile/gate và các thao tác vận hành hoạt
  động. Kế thừa nghiệm thu giao diện 17/11 trong phần không bị ảnh hưởng.
  Phụ thuộc FIN08 và FIN13. [Hồi quy giao diện offline đã đạt](#fin14--hồi-quy-giao-diện-và-export).
  Còn xác minh hosted ứng dụng trước khi chuyển mặc định.
- [x] **FIN15 — Đồng bộ khóa luận, bài báo và tài liệu hệ thống.** Cập nhật
  nguồn tại `thesis/` và `paper/`, hướng dẫn chạy, mô tả phương pháp, bảng/hình,
  limitations và các tài liệu trình bày còn dùng theo đúng release mới.
  Chương kết quả phân biệt study cũ và lần đánh giá
  sửa đổi; số liệu sinh từ nguồn đã khóa. Khóa luận tiếng Anh, quản lý bằng
  tiếng Việt, root README tiếng Anh. Build/render và kiểm phần tài liệu bị
  ảnh hưởng; nối phần bàn giao với P10 của thesis. Tác giả cho tiếp tục
  từ FIN12–FIN13 và kết quả hồi quy offline FIN14. Phần phát hành giao diện
  chuyển sang lượt sau. [Biên tập và build FIN15](#fin15--đồng-bộ-hai-bản-thảo).
- [ ] **FIN16 — Đóng gói và khôi phục bản cuối.** Đóng gói source, runtime lock,
  tài nguyên được phép bàn giao, runbook, manifest, kết quả và receipt theo
  layout hiện có; ghi cách lấy asset local hoặc giới hạn phân phối. Kiểm
  khôi phục trong môi trường sạch, offline replay và các điểm vào sử dụng.
  Đạt khi người nhận tái dựng được phạm vi đã công bố và đối soát đúng hash.
  Phụ thuộc FIN13–FIN15.
- [ ] **FIN17 — Đóng kế hoạch finalize.** Đối chiếu từng deliverable và gate,
  chốt release/default/profile/support, kết quả nghiệm thu và hướng dẫn bàn
  giao. Mọi việc thuộc phạm vi đã hoàn thành hoặc có quyết định phạm vi
  được cập nhật minh bạch trước nghiệm thu. Đạt khi FIN01–FIN16 đều hoàn tất
  và các task bàn giao liên quan được đối soát. Phụ thuộc FIN16.

#### Quy tắc tái sử dụng và gọi API

| Thay đổi đã xác định | Phạm vi thực hiện |
| --- | --- |
| Audit, kiểm toán số học, metadata hoặc policy xác định, với request/schema cũ còn tương thích | Tính và kiểm offline, dùng raw response phù hợp đã lưu |
| Chỉ báo cáo Alpha/prompt của bản Native sửa thay đổi | Gọi lại Decision của bản sửa ở những điểm bị ảnh hưởng; upstream/các nhánh khác cần proof tái sử dụng |
| Bank, retrieval hoặc cách trình bày prior thay đổi | Tái tính preparation rồi gọi các nhánh có request mới, kể cả thay đổi ready/bypass |
| Facts/anchor thay đổi | Kiểm Common → Fact Anchor → MT theo dependency; tái sử dụng ở node có request và contract còn hợp lệ |
| Context/HMM/scaler/teacher/student thay đổi | Tái tính toàn preparation liên quan; xét lại prior/MT, support và policy theo request thực tế |
| Giá/ảnh/tin/báo cáo đầu nguồn thay đổi | Tạo snapshot mới, chạy lại các node và Decision chịu ảnh hưởng theo đồ thị phụ thuộc |
| Điểm mới hoặc nghiên cứu xác nhận mới | Thu các node thuộc protocol mới; upstream chia sẻ và bypass vẫn theo hợp đồng |

Tái sử dụng cần đối chiếu nội dung thực gửi, ảnh, schema, model/options,
profile và dependency cùng nhật ký nguồn. Hash archive thay đổi riêng do
metadata kiểm toán được đánh giá qua verifier, không suy tự động thành request
mới. Thay policy/evaluator chỉ được dùng raw cũ khi contract tương thích và
mọi input cần thiết đã có trước outcome. Ghi serving epoch và giới hạn model
alias khi ghép hồi đáp cũ/mới. Việc dùng chung upstream và phục hồi attempt
đã hoàn tất được tính trong ngân sách, không nhân toàn bộ lưới theo mặc định.

#### Các gate đóng bản cuối

| Gate | Bằng chứng cần có | Task chốt |
| --- | --- | --- |
| Alpha nhân quả | 85 yếu tố, prefix/future poison, train/validation purge và selector freeze, caller đúng profile | FIN03, FIN08, FIN10 |
| PIT toàn pipeline | Nguồn giá/tin/bank, lịch fit, membership và ranh giới outcome được kiểm trên miền công bố | FIN04–FIN07, FIN10, FIN13 |
| Kinh tế và vận hành | Oracle, tài khoản, shared upstream, dependency, prompt, quota/retry/checkpoint/UNKNOWN PASS | FIN10–FIN13 |
| Ứng dụng | Hồi quy caller, UI và dữ liệu kết quả cũ/mới khớp profile và nguồn | FIN14 |
| Bàn giao | Phân tích đối soát, tài liệu khớp release, cold restore và runbook sử dụng được | FIN12, FIN15–FIN17 |

Các gate phần mềm và PIT có phạm vi được mô tả trong receipt. Kết luận vượt
đối chứng cần thiết kế và bằng chứng thống kê tương ứng; đánh giá sau khi dữ
liệu đã exposed giữ phạm vi exploratory. Kiểm định khớp lệnh/thuế/thanh khoản
và portfolio vốn chung có thiết kế riêng khi mở rộng mục tiêu vận hành.

#### Cách kiểm tra và ghi bằng chứng

Áp dụng AGENTS.md mục 1.2. Mỗi task chỉ biên dịch Python thay đổi, chạy test
trực tiếp/caller/hợp đồng liên quan và leakage suite của đường dữ liệu bị đổi.
Tái sử dụng gate cũ cần đối chiếu hash nguồn/runtime/input/log; thay đổi hành
vi cần bằng chứng kiểm lại phần tương ứng. Mốc yêu cầu bốn gate tham chiếu
được đối soát theo phạm vi, chạy hồi quy toàn hệ thống khi người dùng yêu cầu rõ.

Các điểm kiểm có thể tái sử dụng gồm
[test causal alpha](../../tests/test_causal_common_leakage.py),
[test profile](../../tests/test_causal_common_profile.py),
[audit Native](../../core/revision_alpha_contract.py), cùng các suite
sentiment/regime/memory/prior/MT/paired/recovery và serving đang có. Chọn tên
suite cụ thể sau audit caller ở FIN01, bổ sung test khi cần bắt hồi quy mới.
Bằng chứng máy đọc tái sử dụng kho receipt/manifest hiện có; không nhân bản
Markdown theo từng task chỉ để lặp lại checklist này.

**Kiểm FIN00.** Lượt này sửa duy nhất tài liệu kế hoạch, kiểm diff, checklist,
liên kết và hash nguồn được viện dẫn. Không chạy compile/unit/E2E/leakage do
code, runtime, schema và đầu vào thực nghiệm giữ nguyên. Các kết quả PASS
lịch sử được viện dẫn đúng snapshot, chưa có gate runtime mới từ FIN00.

#### FIN01 — Inventory và bảng ảnh hưởng đã khóa ngày 18/11/2026

Nguồn làm việc: `develop:3c674baefc1b1924dbdaea978b78965bce352b53`,
nhánh `docs/finalize-inventory`. [Manifest inventory](week12/finalize_inventory.json)
dùng envelope `payload/sha256`, `digest` và `binding` của hạ tầng unified;
khóa **753 file nguồn/caller/test/UI/runtime**, **18 binding bằng chứng**, tám
vai trò và tám nhóm đường gọi. Đây là inventory trước sửa, không phải receipt
nghiệm thu bản cuối. JSON giữ expected/actual của từng pin lệch và nguồn từng cờ.

| Đường gọi thực tế | Profile/miền đang có | Phần cần xử lý |
| --- | --- | --- |
| `manage_causal_profile.py` → causal Alpha/bridge; `run_unified_experiment.py` → runner/adapters | Fit/verify/predict/bridge và replay offline; Native vẫn nhận Alpha cũ | FIN03/FIN08: profile Native sửa, spec/result identity và caller |
| `unified_live/run.py` → execution/providers | Study U08: tám vai trò, 102 điểm, ba repeat; grant lịch sử | FIN09/FIN10: kiểm request/dependency trước reuse, release mới riêng |
| `/api/analyze` → `WebTradingAnalyzer` → graph; `/api/backtest/start` → engine | Original legacy; backtest extension chuyển serving | FIN08: nối đường sửa, kiểm prompt realtime/backtest đúng hợp đồng |
| `/api/serving/v1` → service/AsOfProvider | Chín mã, 58 phiên 01/07–23/09/2026, 188 binding; tối đa 30 điểm/job | FIN04–FIN08: nguồn/fit/profile mới và preflight |
| `/api/serving/live/v1` → LiveProvider | Capture một lần; chuyển selector frozen; form 1D/sáu lựa chọn | FIN04–FIN08: availability, origin, event ledger, cache và support |
| `/api/research-results`, experiments và export owner | Reader U09 đã verify; legacy/serving namespace riêng | FIN08/FIN14: phân biệt receipt/profile cũ và mới |

Sáu lựa chọn là `original_fix`, `bayesian_v1`, `C2`, `A_tp_pool`,
`B_semantic`, `MT_BICL`; hai vai trò là `original_common`, `Fact_Anchor`.
Native dùng `original_fix_serving_v1`/Alpha native; bốn prior dùng
`common_decision_v1`, Common cùng profile; Anchor/MT dùng
`fact_anchor_v3`/`utility_icl_v3`. Bảy vai trò sau nhận `causal_common_v1`;
dependency/fallback/resource của từng vai trò nằm trong manifest, khớp registry.

| Cờ / phân loại | Nguồn và ảnh hưởng | Task xử lý và tiêu chí kiểm lại |
| --- | --- | --- |
| `ALPHA_NATIVE` — lỗi đã tái hiện | `revision_alpha_contract.rowwise_diagnostics`: bfill, ba normalizer, nhánh volume thay quá khứ; `WINDOW_REPLACEMENTS` ghi sáu window theo độ dài | FIN03/06/08/10: 85 factor prefix/poison, origin và train/purge; mọi caller bản sửa nhận đúng projection |
| `ALPHA_ONLY` — thiếu chứng nhận toàn pipeline | U05 PASS chỉ Alpha PIT; U06/U08/U09 vẫn ghi whole-system NOT_CERTIFIED | FIN04–07/10/13: chứng minh nguồn, fit, maturity và barrier trong miền mới |
| `NEWS_PIT` — thiếu provenance nội dung | Protocol v2: date-only next-day, không chứng nhận content/scorer tồn tại trước cutoff; ảnh hưởng shared sentiment/mọi nhánh | FIN05/09/10: khóa content/source/published/available/collected/scorer và cùng snapshot hiển thị |
| `PRICE_PIT` — thiếu bằng chứng nguồn | U06 và live snapshot: vendor adjustment/event history, bank/query khác nguồn | FIN04/06/10: đơn vị/lịch/availability/events và nhãn oracle đúng source/version |
| `BANK_LINEAGE` — thiếu raw và lệch cơ sở nhãn | U06: bank 852 CORE4 thiếu raw signal journal; 828 nhãn lệch donor, max 0,04298848884252138 đpt | FIN06/09/10: khôi phục hoặc tái tạo có trace, label oracle, exit<cutoff, fit/OOD đúng hợp đồng |
| `MT_LINEAGE` — thiếu bằng chứng dependency bản mới | Context/student/teacher/facts chưa được Alpha-only gate bao phủ | FIN06/07/10: reserved IDs trước label, fold freeze, fit cutoff, support và Q10/Q90/anchor |
| `CALLER_IDENTITY` — đường nguồn còn dùng bản cũ | `causal_bridge.decision_payload` cố ý giữ native khi `original_fix`; profile/registry/cache đang khóa bản cũ | FIN08/10/14: profile và cache mới, không gán receipt cũ cho bản sửa |
| `SOURCE_DELTA` — nguồn hiện hành đã đổi | U08 khớp 703/718, U09 khớp 714/729; cùng 15 đường lệch, không có pin mất local | FIN08/09/10/13: kiểm caller thay đổi và wire request trước reuse; receipt chỉ áp snapshot cũ |
| `OLD_PENDING` — cờ mốc lịch sử | Protocol U06 còn BLOCKED/PENDING_U07_U08; receipt U09 còn U10 PENDING, dù U08/U09/F05 được ghi nhận sau đó | FIN08/13/15: dẫn receipt theo thời điểm/phạm vi, giữ byte cũ; không suy thành causal PASS |
| `UI_ACCEPTANCE` — receipt browser lịch sử, tác giả đã nghiệm thu | Đầu serving contract và kế hoạch xác nhận tác giả nghiệm thu ngày 17/11; acceptance v10/browser pending mô tả mốc trước | FIN14: kế thừa phần UI không đổi; quan sát desktop/mobile cho màn hình chịu thay đổi finalize; không suy xác nhận tác giả thành log browser đã chạy |
| `ARCHIVE_LAYOUT` — đổi chỗ bằng chứng | 30 ZIP cũ đã vào `revision_evidence`; verifier cũ còn đọc đường gốc | FIN10/16: tra index, restore checkout biệt lập theo runbook, kiểm bytes, không sửa expected hash |
| `EXECUTION_LIMITS` — giới hạn nghiên cứu | Cohort exposed, LLM knowledge cutoff, vendor/fill/thuế/thanh khoản và vốn chung chưa được chứng minh | FIN02/12/13/15: exploratory, đúng mẫu số/NA và giới hạn; không tuyên bố profitability/superiority/live fills |

**Kiểm FIN01.** Python **3.13.5/Windows** và **107/107 package** khớp U06;
286/286 asset U06, 188/188 binding serving khớp. Đã đọc/kiểm hash **810 member
snapshot**, **8.063 member U08** (gồm 8.035 file journal) và **15 artifact U09**;
20 gói W12 tại chỗ và 30 ZIP qua `EvidenceArchive` đều nguyên byte. Không
giải nén/ghi đè bằng chứng. Đã chạy riêng phản ví dụ số học nhỏ native, kết quả
`PASS_DETECTION`/Native **FAIL**; đây không phải chạy lại leakage suite hoặc
backtest. FIN01 chỉ thêm inventory/checklist, không đổi code/test/schema/runtime
hoặc đầu vào nghiên cứu nên không compile/unit/E2E/toàn suite theo AGENTS §1.2.
Đối soát JSON/checksum, caller, số liệu, liên kết và `git diff --check`;
**0 API thị trường/LLM, 0 fit/training**, không nâng gate U05/U08/U09/ứng dụng.

#### FIN02 — Hợp đồng bản cuối và so sánh đã khóa ngày 18/11/2026

[Contract máy đọc](week12/finalize_comparison_contract.json) khóa thiết kế
`finalize_anchor102_exploratory_v1`, dựa trên inventory FIN01 và protocol U06 v2.
Trạng thái **METHOD_DESIGN_LOCKED_RESOURCES_AND_EXECUTION_PENDING**: đây là
đặc tả cho FIN03–FIN10, chưa phải spec chạy được hoặc grant thu. Actual resource
hash/recipe/log sẽ được FIN04–FIN07 khóa và FIN10 kiểm trước query. Không đổi
protocol, registry, cấu hình runtime hoặc receipt nghiên cứu cũ.

| Thành phần | Quyết định đã khóa |
| --- | --- |
| Miền đánh giá | Đúng 102 ID/cutoff của U08, chín mã, 51 account symbol–fold/sáu fold; BHN chỉ ba fold cuối/sáu điểm, mỗi mã khác 12 điểm. Một realization upstream, ba Decision repeat. CORE4 chỉ sensitivity đã định trước. Danh sách từng point/hash lịch nằm trong JSON. |
| Miền ứng dụng | 1D, sáu lựa chọn/hai dependency; as-of chín mã/58 phiên 01/07–23/09/2026, tối đa 30 điểm/job, bước ba phiên; chỉ bật binding qua preflight nguồn mới. Live dùng phiên hoàn tất sau 15:30 giờ Việt Nam, capture một lần/owner, không refetch khi resume; thiếu outcome t+3 giữ NA. CLI/backtest/as-of/realtime/viewer/export cùng identity. |
| Native sửa | Giữ selectable ID `original_fix`, cấp Decision profile mới **`original_fix_causal_serving_v1`**. Dùng đúng năm factor, orientation, threshold, giá trị và `alpha_report` từ `causal_common_v1` như Common. Giữ native instruction/schema/distill/cap; không thêm prior/facts/utility hoặc đổi sentiment ngầm. |
| Common và delta | `original_common` giữ `common_decision_v1`, empty prior, cùng causal Alpha/upstream/tin/model/options/repeat. Native sửa và Common khác khuôn prompt/instruction/distill/cap hiện có; so sánh này không quy toàn delta cho Alpha. Native cũ `original_fix_serving_v1`/`native_fix` giữ FAIL và artifact riêng. |
| Phương pháp/dependency | V1/C2/A/B giữ recipe và readiness đã pin; phụ thuộc/fallback Common. Fact Anchor nhận Common cùng repeat và facts; MT nhận Common → Anchor cùng repeat/context/student. Cả tám vai trò dùng cùng Alpha causal trong bản sửa; metadata/result version phân biệt bản cũ. |
| Hai baseline và controls | System family: năm extension trừ Native sửa; method family: năm extension trừ Common. Ba bridge Common–Native sửa, Anchor–Common, MT–Anchor. CASH và ALWAYS_LONG đúng chu kỳ/đủ phí; continuous hold, retrieval ablations và MT ablations chưa thực hiện không được nhận là kết quả. Controls cũ chỉ ở family lịch sử riêng. |
| Nguồn/availability | Ưu tiên phục hồi snapshot as-published có bằng chứng; nguồn thay thế phải chứng minh availability tại cutoff, có version/recipe trước sử dụng. Tải dữ liệu mới không tự chứng minh PIT quá khứ. Giá query≤cutoff, lịch phiên/đơn vị/event ledger đúng source; không splice hoặc ép parity bank/query. |
| Tin tức | Khóa content/source/published/available/collected/revision/scorer/aggregation; date-only chỉ nhận khi có bằng chứng bản nội dung, available từ ngày kế tiếp theo timezone đã khóa. Loại future/undated/bản sửa sau cutoff; nguồn chưa chứng minh giữ unavailable có lý do, không neutral giả. Cùng snapshot cung cấp report/UI. |
| Bank/regime/context | Giữ candidate 852 CORE4, max exit 30/12/2022; phải phục hồi hoặc tái tạo raw signal/nhãn/source có trace. Prior ngoài CORE4 fallback Common đúng registry. Context numeric freeze trước query đầu từng fold, reserved toàn bộ 102 ID trước label, không prequential insertion; HMM/scaler forward-filter, fit IDs/cutoff và source được kiểm. |
| Fit/purge | Giữ `causal_common_v1`: warmup300, normalizer20, train≥60, validation≥30, ≥5 LONG/candidate, thresholds 0,05/0,1/0,2, top5, step3. Orientation train Spearman; selection validation LONG/CASH mean return. Train exit<validation start, validation exit<test start. Một selector/mã dùng qua mọi fold; origin cố định, không fit/test hoặc native fallback. |
| Lịch Alpha cụ thể | Tám mã ngoài BHN: train 14/04/2021–30/09/2022, validation 06/10/2022–27/06/2023, test 03/07/2023–23/09/2026. BHN: train 20/12/2023–26/12/2024, validation 02/01–25/09/2025, test 01/10/2025–23/09/2026. Khóa 51 binding/chín selector; nguồn đổi không tự dịch boundary. |
| Student/teacher/utility | Ưu tiên frozen seed 42/step 3000 sau audit provenance; giữ riêng p_student và posterior teacher. Utility 4.096 draws; MT cần K≥2, query 45 rows/bucket known và ≥5 gains/≥5 non-gains. CASH→LONG chỉ Q10(U)>0, LONG→CASH chỉ −Q90(U)>0; bằng 0 giữ anchor. Rebuild cần recipe/corpus/seed/resource version trước preparation, không tune bằng query/test. |
| Kinh tế | Giữ `compute_round_trip_net_return`, Open(t+1)→Close(t+3), SHORT=CASH, phí 0,25% và slippage 0,10% mỗi chiều. Giá nghìn VND chuyển VND đúng một lần; account độc lập 50 triệu, hai chu kỳ đúng thứ tự, không gộp thành portfolio vốn chung. |
| Metric và thống kê | Giữ nguyên metrics/statistics protocol v2: mean return từng repeat trong account rồi equal mean 51 account; BA pooled 102 mỗi repeat rồi mean 3; raw/final/bypass/support/NA và daily NAV khi đủ. Hai baseline×5 extension×2 endpoint=20 contrast; PCG64 seed 20261110, 10.000 draws, circular fold-block 2/ba starts, 95% simultaneous descriptive band và ≥9.500 joint finite; L1/L3/leave-fold/leave-symbol/CORE4 đã định trước. Không chọn repeat/subgroup hoặc tuyên bố confirmatory trên dữ liệu exposed. |
| Thiếu dữ liệu/lỗi | Thiếu giá/fit/provenance bắt buộc thì chặn preflight; tin NA theo policy đã khóa. Algorithm fallback có lý do và source hash; lỗi API/parse/UNKNOWN/resource integrity không thành CASH. Nếu thiếu action bắt buộc thì primary account return chưa công bố; sensitivity complete intersection/bounds phải ghi nonprimary, không impute CASH. |
| Pairing/recovery | Upstream một lần/point/realization, deep-copy; cùng-repeat DAG; đủ tám vai trò×ba repeat durable trước outcome. BRPP K=3≤600 ký tự, prompt Decision backtest<6.500 ký tự; retry tối đa 3 tổng attempt kể cả repair, checkpoint từng point; UNKNOWN dừng/reserve/đối soát UUID trước resend. |
| Identity/default | Namespace `finalize_resources_v1`, `finalize_anchor102_exploratory_v1`, `finalize_serving_v1`; identity bind code/runtime/resource/snapshot/profile/model-options/request/dependency/repeat/owner. Chuyển default sau FIN13 và hồi quy FIN14, không áp receipt cũ cho bản mới. VI/EN giữ presentation sidecar, canonical policy VI. |

**Tái sử dụng theo request.** FIN09 phải so từng slot với raw U08: bytes
messages/ảnh/schema, model/options/tier, hợp đồng prompt/input, dependency và
nguồn parent cùng repeat. Profile/source hash đổi riêng metadata được đánh giá
bằng verifier và mapping provenance; không tự suy mọi request đều mới hoặc đều
dùng lại được. Native sửa có tối đa 306 Decision cần đối chiếu; Common/prior/
Anchor/MT và upstream chỉ reuse sau proof. Thay bank/facts/context/support hoặc
parent làm đổi request thì vô hiệu hóa đúng node chịu ảnh hưởng. Bypass tính
lại offline, không giả response; không lấy r0 lấp r1/r2. Ghi epoch/model alias
và giới hạn ghép phản hồi cũ/mới; alias không chứng minh cùng weights.

**Dự toán sơ bộ cho FIN09.** 2.448 forecast slot; trần trước reuse/bypass là
2.448 Decision +204 vision +10 smoke = **2.662 execution**, tối đa **7.986
attempt** khi cap 3. Profile bank xác định xử lý **852 chu kỳ với 0 HTTP**.
Số cuộc gọi query còn phụ thuộc số request chứng minh được tái sử dụng.
Chi phí/thời gian/quota còn **chưa xác minh**,
không cam kết lịch thu. Candidate model/options giữ từ runtime U08 để đối chiếu
archive; FIN09 xác minh availability/quota/payload, không tự đổi model hoặc giảm
repeat. **Số API được cấp từ FIN01/FIN02: 0**; ngân sách cuối phải có dry-run
reuse/new/bypass, quota carry, retry/repair/UNKNOWN và release riêng trước thu.

**Thay đổi và kiểm FIN02.** Nếu thay nguồn/recipe/calendar/profile/method/split/
metric đã khóa, phải amendment/version và lý do trước output query mới; sau
output không đổi primary hồi tố. Tất cả nguồn/query đã exposed giữ exploratory.
Nếu FIN03 đổi ngữ nghĩa causal Alpha thì cấp profile mới trước thu; nếu chỉ
tái dùng ngữ nghĩa hiện có thì giữ `causal_common_v1` và pin source mới.
Trong lần rà FIN02 đã bổ sung serving contract vào inventory và phân loại lại
UI theo xác nhận tác giả 17/11, không phủ nhận nghiệm thu vì receipt browser cũ.

Đã kiểm checksum/envelope/parent binding, đúng 102 ID/51 account/ba repeat,
lịch fit/purge, topo dependency/fallback, hai baseline/20 contrast, phép đếm
dự toán, liên kết và diff. `verification_targets` trong JSON ánh xạ các suite
hiện có cho Alpha, giá/tin/bank/regime/MT, paired/recovery và serving; chỉ chọn
nhóm bị ảnh hưởng khi code được sửa, chưa phải kết quả test mới. FIN01–FIN02
chỉ thêm tài liệu/manifest đặc tả chưa được runtime đọc nên không compile,
unit/E2E/leakage suite theo AGENTS §1.2; **0 API, 0 fit/training**. FIN03–FIN17
còn mở, nguồn PIT và gate bản sửa chưa được nhận PASS từ việc chốt thiết kế.

#### FIN03 — Alpha nhân quả, selector và bridge offline ngày 18/11/2026

Nhánh `feat/finalize-causal-alpha-selector`, nền `develop:1e1f22af`.
Tái sử dụng nguyên byte `core/causal_alpha.py`, `core/alpha_compare.py` và
`core/backtest_engine.py`: bfill đã được thay bằng lag giữ NaN, normalizer
expanding theo prefix, volume quan sát theo từng dòng và sáu window cố định
đã có trong `causal_common_v1`. Không đổi công thức, threshold, lịch, cách chọn
hoặc source identity của selector v1; không cần amendment phương pháp FIN02.

[Bridge](../../core/causal_bridge.py) bổ sung lựa chọn keyword
`decision_profile="original_fix_causal_serving_v1"` cho Native. Profile sửa
bắt buộc có projection causal trong snapshot; profile lạ, nhánh sai hoặc thiếu
projection gây `ValueError`. Native sửa nhận đúng toàn bộ payload Common:
cùng năm factor, orientation, threshold, giá trị, báo cáo Alpha và shared
upstream/sentiment. Mặc định và profile Native lịch sử vẫn nhận payload cũ.
Việc dựng snapshot đã bind tiếp tục xác minh selector/giá bằng primitive cũ.

[CLI](../../scripts/manage_causal_profile.py) `bridge` có thêm
`--native-profile original_fix_causal_serving_v1`. Khi chọn, output
`native_causal_bridge_v2` ghi profile/input identity, payload hash, request
Native sửa, request Common và hash request Native lịch sử. Dùng chính factory
Native hiện có để dựng prompt/schema/options, dừng trước invoke thật; không
chạy thêm selector native. Không truyền flag thì output v1 và request lịch sử
giữ nguyên. Đây là caller offline của FIN03; registry/factory ứng dụng vẫn
chưa nhận profile mới, **FIN08** nối CLI/runner/serving/realtime/result identity
và **FIN13–FIN14** mới quyết định chuyển default sau nghiệm thu.

| Phạm vi kiểm | Bằng chứng và kết quả |
| --- | --- |
| 85 handler và sáu window | 1.020 so sánh raw prefix: 85 factor ×12 biên 1/2/19/199/200/229/230/239/240/249/250/300; cùng giá trị và vị trí NaN khi nối dài prefix. Bộ cũ bổ sung prefix sau warm-up tại 380/600/900. PASS. |
| Warm-up/missing/poison | Giữ unavailable trước đủ volume quan sát và normalizer; một Volume thiếu che đúng 300 phiên, phục hồi support sau đó, toàn bộ Volume thiếu không thành proxy/0. Future Volume thiếu/0/rất lớn, giá tương lai bị nhân lớn và nến phẳng không viết lại prefix. Kiểm đủ 85 cột có support thực sau warm-up, không chỉ so toàn NaN. PASS. |
| Train/validation/purge | Nhãn gọi oracle kinh tế; purge strict exit trước boundary. Poison giá test không đổi artifact/fit/orientation; poison validation không đổi train candidates. Sai origin, đổi giá fit, thiếu query hoặc nhận future rows bị từ chối. PASS. |
| Selector đóng băng | Predict không gọi fit; thay giá trong test không chọn lại factor/orientation/threshold. Sửa artifact ngoài object hoặc sửa kết quả cache không làm đổi dự đoán đã đóng băng; thiếu support không fallback Native. PASS. |
| Caller/profile/request | CLI Native sửa và Common cùng payload; schema/model/options Native giữ nguyên, prompt backtest <6.500 ký tự. Poison future và full-file source hash không đổi request sửa; snapshot không bị mutate, JSON giữ kiểu nguyên bản. CLI mặc định giữ bridge v1, không tự bật profile trong app. PASS. |
| Hồi quy caller chung | Runner tám vai trò giữ shared upstream một lần, dependency/fallback, outcome barrier, resume, không nhân bản repeat, evaluator và HTTP fixture viewer/export. Không phải browser hoặc hosted smoke. PASS. |

**Kết quả kiểm đúng phạm vi: 41 test PASS, compile 4 Python PASS.** Gồm:
`test_causal_common_profile` (9), `test_causal_common_leakage` (8),
`test_finalize_alpha_profile` (5), `test_finalize_alpha_leakage` (4) và
`test_unified_experiment` (15). Hai module mới kiểm biên/profile mới; hai module
causal kiểm toán tử/fit/PIT và tương thích bridge; runner chung kiểm các caller
và hợp đồng ghép cặp bị ảnh hưởng. Chỉ biên dịch bridge, CLI và hai file test mới.
Không chạy toàn unit suite, compileall, E2E hoặc các suite sentiment/regime/MT
không đổi; không tuyên bố PASS lại bốn gate toàn hệ từ lượt này.

[Gói QA FIN03](week12/finalize_alpha_checks.zip): **142.277 byte**, SHA256
`30e9514ebfffc8d42013821e7284f6c84b0d8206f4898f5853b4d35a1db52719`.
Gói có 25 member, gồm log nguyên byte, manifest, verifier và nguồn cần đối soát;
manifest pin 20 nguồn trực tiếp, nối inventory/contract FIN01–FIN02, runtime
Python **3.13.5/107 package** và delta expected/actual. Log unittest từ PowerShell
giữ wrapper stderr lịch sử của lệnh; cả hai process exit0 và phần kết thúc
`Ran 9/32 tests ... OK` đã đối soát. Verifier trong tiến trình mới, chế độ `-I`,
đã PASS byte nguồn/runtime/package và 286 asset U06, không chạy lại test/fit/API.

Đối chiếu inventory: **750/753 nguồn cũ nguyên byte**, ba delta là bridge,
CLI và `tests/.gitattributes`; thêm hai file test mới. Thuộc tính LF giữ hash
hai file mới ổn định qua checkout. Đủ **18 binding bằng chứng** và **286 asset
U06** không đổi; không sửa inventory/contract/receipt frozen. Mọi fit/replay
selector trong lần kiểm chỉ dùng fixture synthetic; **0 hosted LLM/market API,
0 training HMM/student/bank**, không đọc outcome thị trường hoặc đánh giá lợi nhuận mới.

FIN03 đạt Alpha PIT và caller bridge/CLI trong miền fixture đã kiểm. Native
lịch sử vẫn **FAIL**, whole-system vẫn **NOT_CERTIFIED**; PIT nguồn và tài nguyên
bản cuối thuộc FIN04–FIN07/FIN10, tích hợp ứng dụng thuộc FIN08. Không dùng kết
quả này để nhận bản sửa đã được phát hành hoặc toàn hệ đã Zero-Leakage.

#### FIN04 — Đối soát nguồn đã có, gate PIT còn chặn ngày 18/11/2026

Nhánh `feat/finalize-price-provenance`, nền `develop:0649b9b3`. Người dùng đã
xác nhận **không có kho snapshot hoặc hồ sơ nguồn bổ sung**. Đã tìm và kiểm
response giá thô/sự kiện H02 cho đủ chín mã, receipt từng trang, giá/query U06,
giá bank và lịch VNINDEX. [Auditor](../../core/finalize_price_audit.py) chỉ đọc
input đã pin từ FIN02/U06; không gọi hàm acquisition hoặc cập nhật dữ liệu cũ.
[Báo cáo máy đọc](week12/finalize_price_audit.json) dùng envelope/checksum hiện có,
giữ 110 binding nguồn, kết quả từng mã, từng point và delta cần xử lý.

**Trạng thái chính xác:** `AUDIT_COMPLETE_SOURCE_GATE_BLOCKED`,
`price_source_gate=BLOCKED_PIT_PROVENANCE`, **0/102 điểm được admission**.
Checksum và các phép đối soát số học PASS không thay chứng cứ dữ liệu đã khả
dụng tại cutoff. Không đánh dấu FIN04 hoàn tất hoặc thay đổi điều kiện FIN02.

| Nội dung | Kết quả đối soát |
| --- | --- |
| REST và đơn vị | Kiểm đủ trang, URL, response SHA/receipt, ticker và schema; dựng lại CSV từ trường Open/High/Low/Close thô, Reference và matched Volume. Chỉ chuyển VND→nghìn VND một lần; không lấy cột Adjusted hoặc scale để ép bằng donor. |
| Lịch/origin | Lịch VNINDEX quan sát có 2.181 phiên 02/01/2018–30/09/2026; đủ query/t+1/t+3 của 102 điểm, cổ phiếu không thiếu phiên trong các chu kỳ đó. BHN giữ origin/suffix đã khóa, 673 dòng đầu chỉ được audit, không tự sửa OHLC hoặc đổi lịch fit. Chưa có chứng cứ lịch sở giao dịch độc lập. |
| Bank/raw H02 | Bốn mã CORE4 có 751 phiên giao nhau/mã; Open/High/Low/Close/Volume khớp hoàn toàn. Đủ 852 episode đáo hạn trước query đầu; t+1/t+3 đúng phiên, không chu kỳ quyền hoặc thiếu matched Volume. Nhãn khớp `compute_round_trip_net_return`, 0 mismatch trên ngưỡng 1e-10; sai số tuyệt đối lớn nhất 2,7755575615628914e-17 theo fraction. Chỉ tính nhãn lịch sử bank, không tính outcome query. |
| Donor/raw H02 | Cả chín chuỗi khác raw: 996–1.681 nến OHLC/mã khác nhau, Volume khác từ 0–166 phiên/mã. JSON giữ số đếm từng cột/từng mã. Nếu dùng raw thay donor, cần version nguồn/dataset và tái tạo tài nguyên/đặc trưng/nhãn chịu ảnh hưởng theo FIN02/FIN06; chưa đổi nguồn hoặc giả định request cũ còn tương đương. |
| Availability | Receipt H02 ghi lượt lấy ngày 08/11/2026; donor ghi lấy lại ngày 01/11/2026 và tự ghi chưa authenticated historical snapshot. Chưa có chứng cứ phiên bản giá đã công khai tại cutoff của study. Không tự gán available_at bằng ngày nến hoặc ngày tải. |
| Sự kiện | Giữ riêng ngày công bố/ngày không hưởng quyền; date-only dùng ngày kế tiếp, undated/future có lý do loại. Nội dung event hiện chỉ có metadata vendor, chưa chứng minh bản công bố tại cutoff. Các ngày quyền dưới đây là cờ cần xác minh, không phải chứng nhận PIT nội dung. |
| Byte nguồn bank legacy | Tám CSV/events tại `data/execution_prices/` khác hash nội bộ manifest do LF/CRLF. Bản byte gốc đúng hash còn nguyên tại compatibility U06 và được loader cũ xác minh/tái dựng từ raw evidence. Auditor dùng bản đã verify này; không đổi hash mong đợi hoặc ghi đè file lịch sử để ép PASS. |

Các chu kỳ có ngày quyền theo metadata công bố trước cutoff:

| Point | Entry t+1 | Exit t+3 | Ngày quyền nằm trong (entry, exit] |
| --- | --- | --- | --- |
| FPT-2023-07-03 | 2023-07-04 | 2023-07-06 | 2023-07-05 |
| VNM-2024-09-20 | 2024-09-23 | 2024-09-25 | 2024-09-24 |
| MBB-2025-01-02 | 2025-01-03 | 2025-01-07 | 2025-01-07 |
| VCB-2025-10-01 | 2025-10-02 | 2025-10-06 | 2025-10-03 |
| VNM-2026-06-24 | 2026-06-25 | 2026-06-29 | 2026-06-26 |

Giữ đủ **102 planned** và lý do từng point. Không loại năm điểm này hồi tố,
không đổi horizon, công thức P&L, phí/slippage hoặc giả định quyền đã được
engine xử lý. Trước phát hành nguồn mới cần xác minh ledger và quyết định
protocol/version phù hợp với cờ quyền; hiện chưa có amendment thay cohort.

**Phần mềm đã kiểm.** [CLI](../../scripts/audit_finalize_prices.py) hỗ trợ
audit, `--check` đối soát lại báo cáo và `--require-pass` làm preflight fail-closed.
`--check` trả exit0 với trạng thái source bị chặn; thêm `--require-pass` trả
exit2/ValueError theo đúng gate thực, không sửa kết quả thành PASS. Validator
prefix cắt giá/timestamp tại cutoff, đòi availability có timezone và không
sớm hơn giờ hoàn tất phiên được caller cung cấp từ lịch đã xác minh. Mốc
15:30 là giờ query theo FIN02, không được dùng để bịa giờ công bố giá hoặc
giờ đóng cửa sở giao dịch. Schema số của prefix không đổi khi future làm đổi
dtype cả cột. Metadata fixture kiểm rào thời gian, không authenticate vendor.

**35 test duy nhất PASS, compile 4 Python PASS:** tám test auditor/REST/corpus,
bốn test leakage/availability/events và 23 test execution-prices/target-contract.
Đã phát hiện test poison future làm dtype Volume trong prefix đổi int→float;
sửa chuẩn hóa kiểu sau khi cắt/validate prefix, kiểm lại nhóm trực tiếp bị ảnh
hưởng. Log FAIL ban đầu và log PASS sau sửa được giữ nguyên. Kiểm lại nhóm
auditor sau thêm rào quyền/khối lượng bank và nhóm primitive kinh tế được dùng.
Không chạy full suite/E2E; reader legacy tại đường byte lệch chưa được cấp lại
gate từ việc dùng bản compatibility đã verify. Không đổi code/runtime cũ hoặc
dependency; chỉ thêm auditor/CLI/test và quy tắc LF cho các file mới.

[Gói QA FIN04](week12/finalize_price_checks.zip): **95.893 byte**, SHA256
`f6945d909febe2a1736fff17ddba11716c027e505168119baec2e8bf6b5346a0`.
Gói có 25 member, log/nguồn/manifest/verifier; ghi rõ
`PASS_AUDITOR_CHECKS_SOURCE_GATE_BLOCKED`, `FIN04_complete=false`. Verifier
tiến trình mới `-I` đối soát byte report, 110 input, nguồn và Python
3.13.5/107 package PASS, không chạy lại test/fit/API. Các bằng chứng FIN01–FIN03,
U06/U08/U09 và dataset cũ giữ nguyên; **0 LLM/market API, 0 training/refit**,
không tính query return hoặc thay default.

**Điều kiện còn chặn FIN04:** cần chứng cứ as-published/availability của giá,
nguồn lịch độc lập và event ledger có provenance trong miền đã khóa; nếu thay
donor bằng raw phải khóa amendment và recipe tài nguyên trước query mới.
Metadata ngày đơn thuần, quote khớp giữa hai lần thu hoặc thu lại dữ liệu hôm
nay chưa đáp ứng điều kiện này. FIN04 tiếp tục mở; chưa mở FIN06/FIN10 bằng
source gate hiện tại. Theo AGENTS §1.2 “Chỉ merge khi mọi kiểm tra áp dụng đều
PASS”, nhánh FIN04 giữ riêng khi gate nguồn của task còn chặn.

**Bổ sung nguồn chính thức theo yêu cầu tự thực hiện.** Đã tự tìm, tải qua
HTTPS và khóa byte **chín tài liệu công khai**: năm thông báo VSDC, hai PDF
HOSE, một response bài lịch HOSE và một bài giải thích ngữ nghĩa giá của
Vnstock. Đây là bằng chứng bổ sung sau audit trên, không ghi đè report/QA đã
đóng băng và chưa được loader thực nghiệm nhận làm input.

| Cờ quyền | Nguồn chính thức | Thời điểm cập nhật hiển thị (UTC+7) | Ngày chốt danh sách | Nội dung quyền |
| --- | --- | --- | --- | --- |
| FPT-2023-07-03 | [VSDC 159649](https://vsdc.vn/vi/ad/159649) | 23/06/2023 09:33:13 | 06/07/2023 | Tiền 1.000 VND/cổ phiếu và cổ phiếu 15% |
| VNM-2024-09-20 | [VSDC 174349](https://vsdc.vn/vi/ad/174349) | 30/08/2024 14:40:30 | 25/09/2024 | Tiền 2.450 VND/cổ phiếu |
| MBB-2025-01-02 | [VSDC 178088](https://vsdc.vn/vi/ad/178088) | 27/12/2024 14:28:25 | 08/01/2025 | Cổ phiếu 15% |
| VCB-2025-10-01 | [VSDC 187574](https://vsdc.vn/vi/ad/187574) | 26/09/2025 10:38:28 | 06/10/2025 | Tiền 450 VND/cổ phiếu |
| VNM-2026-06-24 | [VSDC 197038](https://vsdc.vn/vi/ad/197038) | 17/06/2026 16:09:03 | 29/06/2026 | Tiền 1.850 VND/cổ phiếu |

Cả năm nguồn khớp mã/ngày chốt danh sách và hiển thị thời điểm cập nhật trước
cutoff tương ứng. **Ngày chốt danh sách khác ngày không hưởng quyền**; các
thông báo này không nêu trực tiếp ngày không hưởng quyền, nên chưa cấp xác
minh độc lập cho cột ngày quyền của auditor. Timestamp hiển thị được lưu riêng
với `retrieved_at_utc`; trang đang tồn tại hôm nay không chứng minh nội dung
bất biến tại cutoff hoặc ledger đã đầy đủ. Chưa loại point, sửa P&L, cộng cổ
tức hay áp dụng điều chỉnh quyền vào engine.

Đã kiểm trực quan trang chứa bảng/ngày ký của hai PDF HOSE: Thông báo
2079/TB-SGDHCM ngày 26/12/2024 về lịch 2025 và 2410/TB-SGDHCM ngày
25/12/2025 bổ sung nghỉ 02/01/2026. [Bài lịch 2026 của HOSE](https://www.hsx.vn/vi/tin-tuc/hose-thong-bao-lich-nghi-giao-dich-nam-2026/2437411)
được lấy nguyên JSON từ endpoint công khai của chính trang; `postedDate`
tương ứng 29/04/2026 08:50 UTC (15:50 UTC+7). Danh sách ngày làm việc trừ các ngày nghỉ
đã công bố khớp toàn bộ ngày CSV trong ba miền:

| Miền đối chiếu lịch | Số phiên lịch công bố/CSV | Ngày thiếu/thừa |
| --- | --- | --- |
| Năm 2025 | 249/249 | 0/0 |
| 01/01–30/09/2026 | 182/182 | 0/0 |
| 01/07–23/09/2026 | 58/58 | 0/0 |

Đây là đối chiếu lịch nghỉ đã công bố; chưa kiểm độc lập mọi lần ngừng giao
dịch đột xuất hoặc toàn miền 2018–2026. Bài ngày 29/04/2026 có trước miền Q3,
không được gán hồi tố làm chứng cứ lịch đã biết tại cutoff tháng 1–4/2026.
[Bài Vnstock về dữ liệu lịch sử](https://vnstocks.com/blog/du-lieu-lich-su-va-thong-ke-giao-dich-co-phieu-vnindex)
giúp phân biệt adjusted OHLCV và raw trade history; ví dụ API hiện tại của
bài không chứng nhận schema/phiên bản nguồn `vnstock 4.0.9` đã khóa. Chưa tìm
thấy cam kết không sửa hồi tố hoặc lịch sử phiên bản giá trong tài liệu này.

[Gói nguồn bổ sung](week12/finalize_price_primary_sources.zip): **1.366.117
byte**, SHA256 `03f7ca462e5c2af8e2ecd4be09278d979939adb95c3da1ad49f4459b28f9c1bc`.
Gồm 14 member: chín bản nguồn, report envelope, manifest, recipe thu/đóng gói
và verifier thư viện chuẩn. Report ghi
`PARTIAL_PRIMARY_CORROBORATION_SOURCE_GATE_BLOCKED`, `FIN04_complete=false`,
admission **0/102**; không thay trạng thái audit frozen. Có URL, HTTP metadata,
thời điểm tải và SHA từng nguồn; HTTP Date/hash chỉ xác minh bản thu hiện tại.

Verifier chạy trong process mới `py -3.13 -I` đã PASS checksum gói, sáu parent
và **110 binding input cũ**. Đối soát thêm QA frozen xác nhận nguồn và runtime
Python 3.13.5/107 package không đổi. Lượt bổ sung chỉ tài liệu/bằng chứng,
không đổi code/test/schema/config/runtime hoặc input thực nghiệm nên **không
chạy lại compile/unit/E2E/leakage suite**, theo AGENTS §1.2; 35 test phía trên
là kết quả cũ được viện dẫn, không là lượt chạy mới. Thu tài liệu web công khai
khác với API giá/LLM: **0 market quote API, 0 LLM, 0 fit/training và không tính
query outcome**. Chưa có chứng cứ giá as-published/availability, lịch và ledger
đầy đủ; FIN04 tiếp tục mở trên nhánh riêng, không nới gate để nhận PASS.

#### FIN04 — Amendment xác nhận của chủ dữ liệu, nghiệm thu có phạm vi

Chỉ đạo tiếp theo của tác giả ngày 18/11/2026: **“Xác nhận chắc chắn đó là giá
chính xác. Hãy pass FIN04 và tiếp tục FIN05”**. Theo chỉ đạo này, FIN04 đạt
**`PASS_OWNER_ATTESTED`** cho preparation bản sửa, với profile
`finalize_raw_prices_owner_attested_v1`. Cơ sở là xác nhận của chủ dữ liệu cùng
audit số học/nguồn đã có; **không phải chứng nhận as-published/availability độc
lập**. Các ghi nhận BLOCKED phía trên là kết quả trước amendment và report/QA
frozen tiếp tục giữ nguyên byte. Đây là thay đổi điều kiện chấp nhận nguồn
trước query output mới; không đổi nhãn/kết luận của study lịch sử.

[Acceptance máy đọc](week12/finalize_price_acceptance_v1.json) nối FIN02,
audit, QA và nguồn chính thức bằng hash; giữ nguyên lời xác nhận và 110 binding
input. Khóa chọn H02 **raw OHLCV** theo origin của từng mã đã đối soát; dùng
giá bank tại compatibility đã verify và lịch VNINDEX quan sát. Không lấy
adjusted donor để ép parity, không ghi đè dataset cũ hoặc tạo timestamp
availability từ ngày nến. Lịch nghỉ HOSE và năm thông báo VSDC được viện dẫn
trong gói bổ sung; các giới hạn về toàn lịch 2018–2026, ngừng giao dịch đột
xuất, độ đầy đủ/nội dung lịch sử của ledger vẫn được công bố trong recipe.

Giữ **102 forecast planned**, không đổi universe, repeat, upstream hoặc ngày
query. Năm chu kỳ quyền đã liệt kê giữ **economic label NA** với lý do
`KNOWN_CORPORATE_ACTION_DURING_HOLDING`, dùng chung cho mọi method/baseline.
Không cộng quyền, đổi horizon, phí hoặc oracle để làm chúng hợp lệ. 97 point
còn lại mới qua sàng lọc quyền đã biết; validator thực thi vẫn kiểm quyền,
Reference và khối lượng trước nhãn ở FIN12. Không coi số 97 là kết quả đánh
giá đã hoàn tất. FIN06 tái tạo selector/đặc trưng/context/tài nguyên bị ảnh
hưởng bởi raw source; FIN09 đối chiếu lại request/reuse, FIN10 pin bản thực
trước query. Chưa chạy preparation/refit hoặc tính query outcome tại FIN04.

[Validator acceptance](../../core/finalize_price_acceptance.py) tái dựng audit
và đối soát toàn bộ record; profile phải được caller khai báo rõ, record tự sửa
và ký lại checksum vẫn bị từ chối. [CLI mới](../../scripts/check_finalize_price_acceptance.py)
kiểm offline trả `PASS_OWNER_ATTESTED`, đồng thời giữ
`independent_price_pit_certified=false`. CLI/gate độc lập cũ vẫn phản ánh báo
cáo frozen bị chặn, không được đổi thành PASS độc lập từ lời xác nhận này.
FIN13 và tài liệu bản cuối phải trình bày riêng tính nhân quả đã kiểm bằng
phần mềm với giả định nguồn do tác giả chấp nhận; không tuyên bố toàn pipeline
PIT nguồn đã được xác minh bên ngoài. Xác nhận giá không áp dụng sang tin tức.

**16 test PASS, compile 3 Python PASS:** bốn test acceptance mới và 12 test
auditor/leakage giá. Bao phủ nguồn thực chín mã/102 điểm/852 nhãn bank, record
tự sửa, source drift, profile sai, không mở nhầm gate độc lập, năm cờ quyền và
prefix/availability/future poison đã có. Chỉ compile module, CLI và test mới;
không chạy full suite/E2E hoặc fit/model/API. Kinh tế, paired, retry và code
Alpha/serving cũ giữ nguyên. Ba `.gitattributes` chỉ thêm quy tắc LF cho file mới;
receipt cũ tiếp tục chứng nhận source snapshot cũ, không dùng receipt đó để
nhận các file thuộc tính vừa đổi đã được kiểm lại.

[QA acceptance FIN04](week12/finalize_price_acceptance_checks.zip): **44.412
byte**, SHA256 `c949156bf34f654982a51b52a2d8ce44ab7ca250e29b0701981ef0d11e0bd298`.
Gồm 14 member: source/log/manifest/verifier. Verifier mới `py -3.13 -I` PASS
nguồn/parent/110 input, Python 3.13.5/107 package; không chạy lại test khi đối
soát. **0 hosted/market API, 0 training, 0 query outcome**. FIN04 hoàn tất theo
phạm vi amendment này; FIN05 áp dụng policy tin của FIN02, không nhận sự xác
nhận về giá làm chứng cứ nội dung tin.

#### FIN05 — Khóa corpus và snapshot tin có chứng cứ, giữ unavailable đúng nghĩa

Nhánh `feat/finalize-news-provenance`, nền `develop:52600887`. Áp dụng policy
tin FIN02; không mở rộng xác nhận giá của tác giả sang nội dung/thời gian tin.
[Corpus mới](week12/finalize_news_corpus_v1.json) tái dựng từ đúng ba nguồn
`news.json`, `article_audit.json`, `local_scores.json` đã pin trong U06/FIN02:
**180 bản ghi, 177 bài duy nhất, 154 score duy nhất đã lưu**; news legacy có
155 cặp mã/bài do một bài dùng cho nhiều mã. Kiểm hash nội dung theo quy ước
JSON string của audit cũ và giữ riêng hash byte UTF-8 cho schema mới; không sửa
text, URL, expected hash hoặc bytes corpus lịch sử để ép chúng trùng nhau.

Corpus hiện không có receipt archive đủ để xác minh bản nội dung tại cutoff;
`evidence_registry={}`. Không suy `collected_at` từ mtime, ngày trong URL hoặc
thời gian chạy; không gán `available_at`/`revision_identity` còn thiếu từ
`date_parsed`. Score đã lưu chỉ là chấm hồi tố trên bản text đã biết; pin model
không chứng minh nguồn tin PIT hoặc kiến thức huấn luyện không có tương lai.
Không crawl lại nội dung hiện tại rồi gán thành bản lịch sử.

[Bộ snapshot mới](../../core/finalize_news.py) khóa profile
`finalize_news_pit_v1`, min support 3, cửa sổ 90 ngày và half-life 30 ngày.
Query 1D dùng **15:30 Asia/Ho_Chi_Minh** theo FIN02; đây là version riêng với
FrozenNews lịch sử dùng cuối ngày. Điểm tổng hợp tính bằng trọng số tuổi kể từ
availability; chỉ nhận scorer
`visobert:d7738b85200272f10ba8b048d80236c8c582b581:max256:pos_minus_neg_v1`,
mapping NEG/POS/NEU đã khóa, probabilities hữu hạn/tổng bằng 1 và score bằng
`p_POS-p_NEG`, cùng hash text đầu vào. Sáu hash artifact/model-card được giữ
trong corpus; không tải weights, forward/rescore hoặc suy domain validation mới.

| Hợp đồng tin | Xử lý đã kiểm |
| --- | --- |
| Nội dung/nguồn/revision | Registry chỉ dành cho receipt archive đã được duyệt và khóa; đối chiếu hash file, metadata, content hash và revision. Checksum không tự chứng minh authenticity nguồn; registry synthetic chỉ kiểm phần mềm. Release thực chưa có receipt được duyệt. |
| Công bố/khả dụng/thu thập | Timestamp có timezone. Date-only dùng ngày lịch kế tiếp, chỉ được admission nếu bản nội dung có proof. Availability không sớm hơn sàn công bố hoặc thời điểm chứng kiến bản nội dung. Collection sau cutoff được phép cho archive đã chứng kiến trước đó; không được backdate archive xuất hiện sau cutoff. |
| Future/undated/sửa bài | Loại có lý do trước đọc score/nội dung; revision sau cutoff không thay bản cũ. Theo URL chỉ lấy revision đã biết mới nhất, dedup và từ chối hai bản khác nhau có cùng availability. Revision mới nhất thiếu score giữ NA, không mượn score của bản cũ. |
| Missing | Không có bài hợp lệ, thiếu proof, thiếu score hoặc chưa đủ ba bài đều giữ NA với reason/count riêng; `avg_score=null`, không tạo nhãn neutral hoặc bịa phân bố. Không có peers thì related sentiment không khả dụng. |
| Snapshot dùng chung | `snapshot_values` cấp data/report cho Decision và hiển thị từ cùng payload/hash; consumer phải truyền hash đã pin. Không crawl, chọn lại tin hoặc score lại khi hiển thị; bản sửa rồi tự ký checksum khác hash owner đã giữ bị từ chối. |

[Coverage 102 điểm](week12/finalize_news_coverage_v1.json) có trạng thái
**`PASS_NEWS_PIT_WITH_EXPLICIT_UNAVAILABLE`**, **0 available / 102 unavailable**:
41 `UNVERIFIED_AVAILABILITY`, 61 `NO_ELIGIBLE_NEWS`. Có snapshot identity và
số lượng quarantine theo từng point; audit loại tin ở ngoài payload forecast
nên nội dung/score tương lai không sửa request quá khứ. Không đưa 177 bài
quarantine vào prompt dưới hình thức tin đã biết, không giữ các score legacy
như chứng cứ sentiment tại cutoff. FIN05 PASS cơ chế eligibility, nguồn đã khóa
và biểu diễn thiếu theo FIN02; **không phải chứng nhận rằng có đủ tin thị
trường PIT để sử dụng**. Các fixture có ba bài hợp lệ kiểm được nhánh available,
không chỉ kiểm trường hợp toàn NA của corpus thực.

[Recipe/validator release](../../core/finalize_news_release.py) đối soát lại
ba input, model/recipe và tái dựng toàn corpus/coverage; record tự sửa rồi ký
lại checksum bị từ chối. [CLI](../../scripts/prepare_finalize_news.py) tạo mới
hoặc `--check` offline, từ chối ghi đè artifact khác byte. Chưa sửa caller
FrozenNews/SentimentCache, graph hoặc UI cũ; **FIN08** gắn profile/snapshot mới
vào CLI/backtest/as-of/live và UI. FIN06 dùng nguồn tin mới để tái tạo tài
nguyên bị ảnh hưởng; FIN09 kiểm lại reuse vì report/mask/input đã thay đổi.
Giữ đủ universe/102 point/repeat và cùng missing policy cho mọi phương pháp.

**14 test PASS, compile 5 Python PASS:** bảy test snapshot/scorer/dedup/caller
ownership/release corpus và bảy test leakage về future poison, revision,
cutoff 15:30/múi giờ, date-only/undated, thiếu proof, chronology collection và
archive backdate. Kiểm cả score weighted thực, count 0/1/2/3, bản tin mới nhất
thiếu score và registry/receipt/snapshot bị sửa; đối soát ba nguồn thực cùng
102 snapshot. Chỉ compile hai module, CLI và hai test mới. Không đổi runtime,
dependency hoặc caller cũ nên không chạy full suite/E2E, sentiment legacy
suite hoặc bốn gate toàn hệ. CLI `--check` chạy riêng PASS với mạng bị khóa.

[QA FIN05](week12/finalize_news_checks.zip): **98.991 byte**, SHA256
`a3d302d42c45bc8bbdcf7bcb000f093615fee79fe5bf389accf6364e25292ee3`.
Gói có 17 member: source/log/corpus/coverage/manifest/verifier. Verifier process
mới `py -3.13 -I` đối soát source, parent/input và Python 3.13.5/107 package
PASS, không chạy lại suite/model/API. Ba `.gitattributes` chỉ thêm LF cho file
mới; bằng chứng FIN01–FIN04 và input lịch sử giữ nguyên byte. **0 market/LLM
API, 0 forward/rescore, 0 fit/training, 0 query outcome**. FIN05 hoàn tất trong
phạm vi này; FIN06 là task tiếp theo, chưa có nghiệm thu app hoặc nguồn giá
PIT độc lập từ lượt này.

#### FIN06 — Tái lập nhãn bank, selector giá thô và tài nguyên fit

Nhánh `feat/finalize-bank-resources`, nền `develop:321aba79`. Recipe version
mới được khóa trước khi dựng tài nguyên. Nó nối nguồn giá FIN04 theo xác
nhận chủ dữ liệu, snapshot tin FIN05, lịch train/validation/test FIN02, mã
producer và artifact model đã pin. 102 ID query được reserve từ đầu.
[Recipe FIN06](week12/finalize_bank_recipe_v1.json).

| Phần kiểm | Kết quả |
| --- | --- |
| Membership và nhãn CORE4 | FPT 211, MWG 213, VCB 215, VNM 213. Cả 852 chu kỳ đủ t+1/t+3 trên lịch VNINDEX, exit muộn nhất 30/12/2022. Khi tái dựng, từ chối ID reserve, chu kỳ trùng và exit từ cutoff trở đi trước khi tính nhãn. Oracle giữ Open(t+1), Close(t+3), phí và trượt giá theo hợp đồng. |
| Chênh lệch raw và donor | Kiểm lịch sử cho 852 chu kỳ trước query, có 828 giá trị khác trên 1e-8 điểm phần trăm. Chênh lớn nhất 0,04298848884252138 điểm phần trăm, 0 trường hợp đổi dấu. Bank mới dùng nhãn raw và giữ hash dòng legacy để truy vết. |
| Selector giá thô | Chín artifact `causal_common_raw_execution_v1` giữ lịch FIN02, cadence 3, 85 yếu tố, orientation Spearman từ train, top 5 và ba ngưỡng validation. Trước oracle loại 13 chu kỳ đi qua quyền và 24 chu kỳ có phiên không khớp lệnh. Train còn 73–123 chu kỳ và validation có 46–60 chu kỳ cùng support theo mã. Recipe mới lưu cờ loại và ngày, selector lịch sử vẫn thuộc snapshot cũ. |
| Scaler và regime | Tái dựng index và scaler prior từ giá thô CORE4 đến hết 30/12/2022. Scaler MT tái lập đúng 731 episode fit đến 31/12/2020, khớp cả IDs và tham số của checkpoint đã khóa. HMM prior kiểm hash prefix VNINDEX kết thúc 30/12/2022, chạy forward trên prefix từng query. Năm model prefix MT đã đối soát nguồn và fingerprint đến hết 2020. Pin byte student seed 42, step 3000, và teacher. |
| Đầu vào query | Đủ 102 snapshot giá/tin và regime theo cutoff. Feature giá 21 phiên có 86 available và 16 NA vì cửa sổ đi qua ngày quyền. 54 query thuộc BHN/CMG/HVN/MBB/VJC có fallback `original_common` vì thiếu bank cùng mã. Với 48 query CORE4, thiếu nguồn tín hiệu được báo là blocker riêng. |

[Manifest tài nguyên](../../outputs/finalize/bank_resources_v1/manifest.json)
khóa năm artifact số, gồm bank, index, chế độ thị trường, selector và đầu vào
query. CLI dựng offline bằng `py -3.13 -X utf8 scripts/prepare_finalize_bank.py`
và tái lập byte bằng cùng lệnh thêm `--check`. Cả hai lần đã PASS. Rebuild
đọc đúng recipe đã pin và từ chối ghi đè artifact khác byte. Lượt này fit
selector/scaler bằng dữ liệu trước cutoff, có 0 lượt gọi API, 0 refit
HMM/student và 0 outcome cho 102 query.

**53 test PASS và compile bốn file Python PASS.** Bốn test mới kiểm chặn ID
reserve, maturity, quyền/không khớp trước oracle, parity recipe khi không có
cờ và future poison. 49 test hồi quy kiểm feature index và scaler prior,
bank MT, prefix HMM và Alpha. Fixture synthetic ban đầu dùng Volume lẻ nên
validator từ chối. Đã sửa fixture dùng số cổ phiếu nguyên và lưu log cả hai
lần. Chỉ kiểm đường dữ liệu bị ảnh hưởng, không chạy full suite hoặc E2E.
Verifier `py -3.13 -I` đã đối chiếu 150 binding, Python 3.13.5/107 package và
hai log dựng/tái lập. Gói 15 member, 28.626 byte, SHA256
`955d22f88b0a0cc4cc02f81f8803145b2c91a4451b0a3b8ef63ed05349a47603`.
[QA FIN06](week12/finalize_bank_checks.zip).

**FIN06 còn mở.** Bank số có 852/852 nhãn, bank tín hiệu có **0/852 episode
đủ chứng cứ**. Chưa tìm thấy journal gốc trong thư mục chạy, lịch sử Git hoặc
các gói bằng chứng kế hoạch đã kiểm. Receipt cũ và tín hiệu chuẩn hóa chỉ
được truy vết bằng hash. Mỗi episode còn cần đối soát request/response và
checkpoint theo node, recipe Alpha causal có hiệu lực vào ngày episode, cùng
regime từ model fit đúng prefix. Selector và HMM phục vụ query được fit sau
một số ngày bank nên chưa thể dùng để suy lùi tín hiệu. FIN09 đã có số đếm
852 episode cần giải quyết để lập batch và ngân sách. Số này chưa phải số
HTTP call. Cần khóa và kiểm producer lịch sử trước khi lấy tín hiệu mới.

#### FIN06 — Tạo lại tín hiệu bank theo từng cutoff

Đã tìm bản sao lưu `historical_memory_852_20261004.zip` được ghi ở Phase C
trong các bản sao cục bộ, Git, 237 gói ZIP và Thùng rác Windows. Chỉ còn bốn
snapshot tin gốc có hash khớp. Chưa xác minh được OneDrive trên web vì công
cụ điều khiển trình duyệt dừng khi không xác định được URL. Chuyển sang tạo
lại theo yêu cầu tác giả, bằng version `finalize_bank_signal_rebuild_v2`.
[Hồ sơ sao lưu Phase C](week2/phase_c_memory_generation.md#sao-lưu-và-bảo-toàn-bằng-chứng).

Recipe khóa đầu vào và candidate model trước khi chạy. Mỗi checkpoint trích
OHLCV từ giá thô FIN04, cắt tại ngày quyết định. Cửa sổ Indicator và hai
ảnh thị giác dùng 45 nến. Hash lưu riêng cho prefix, cửa sổ và snapshot tin
FIN05. State producer chỉ nhận metadata episode và prefix. Không chuyển
`r_net` hoặc `y` sang bước tạo tín hiệu. HMM/scaler lịch sử dùng chính công
thức fit theo prefix của runner gốc tại 217 ngày và lưu đủ tham số, source
hash, fit cutoff. Model query cuối năm 2022 chỉ dùng ở đường query đã khóa.

| Hạng mục | Kết quả tái dựng |
| --- | --- |
| Indicator | 852/852 báo cáo và tín hiệu từ node Python của backtest. |
| Regime | 852/852 episode, 217 HMM prefix. Đối soát đúng ngày fit và hash của mỗi model đã lưu. |
| Alpha | 733/852 có đủ năm factor. Bốn selector lịch sử giữ công thức và min support của U06, tính nhãn train/validation bằng oracle giá thô và loại quyền/không khớp trước oracle. Chọn ranh sớm nhất đủ chu kỳ theo lịch U06 kể từ index 686 và bước 3. Mỗi mã giữ selector đó cho các episode sau. 119 episode sớm hơn giữ `BEFORE_HISTORICAL_SELECTOR_SUPPORT`. |
| Tin | 852/852 NA theo FIN05. Chuỗi điểm số cũ không được dùng để điền `NEUTRAL` vào bank mới. |
| Pattern và Trend | Bắt 8 request thật qua renderer và SDK serialization của node. Mỗi mã một chu kỳ có Alpha và mỗi chu kỳ hai node, transport dừng trước HTTP. Tổng 1.704 slot thị giác danh nghĩa nếu giữ đủ 852 episode, chưa gồm retry. Chưa có phản hồi hoặc request body đã khóa cho tất cả slot. |

Lượt đầu tính Alpha riêng từng prefix. Lượt v2 giữ checkpoint của các HMM
đã fit, kiểm lại hash train, và tính 85 toán tử prefix-causal theo lô trên
miền bank đã chốt. Test đối chiếu vector tại cutoff với phép tính trực
tiếp trên prefix kể cả khi giá tương lai bị nhân rất lớn. Chỉ chọn factor
của đúng hàng cutoff; chưa đủ lịch ở ngày nào vẫn giữ NA ngày đó. CLI
`py -3.13 -X utf8 scripts/rebuild_finalize_bank_signals.py --lock-recipe`
khóa recipe, chạy lại không flag để dựng hoặc đối soát checkpoint trong
`tmp/fin06_signal_rebuild_v2/`.

**16 test PASS** và compile ba file Python mới PASS. Hồi quy gồm prefix
Alpha, request thị giác, maturity, quyền/volume và HMM. Lượt chạy trực tiếp
suite cũ vấp checksum ở fixture `data/execution_prices`; lượt kiểm lại trỏ
riêng fixture vào bản compatibility nguyên byte của FIN04. Hai log được
giữ trong gói. Lệnh chạy lại producer đã đối soát và giữ nguyên report.
Verifier process độc lập đã kiểm hash 852 checkpoint, bốn selector và
217 artifact regime. Gói 1.081 member, 3.901.156 byte, SHA256
`612bcb8b22d0627cb0f82adf64758d96b9e1123777154d9e1a4c74d75e9a61aa`.
[Checkpoint tín hiệu tái dựng](week12/finalize_bank_signal_rebuild_v2.zip).

**Điều kiện còn chặn FIN06.** Khóa cách retrieval xử lý 119 Alpha NA và
sentiment NA theo FIN05 trước khi công bố bank mới. Schema tín hiệu legacy
đòi enum nên không dùng trực tiếp cho bank này. FIN09 còn phải khóa request,
quota và ngân sách cho phần Pattern/Trend được chọn. Trang nhà cung cấp
liệt kê model thị giác `qwen/qwen3.8-27b` và 2.048 input token mỗi ảnh,
chưa kiểm quyền model/quota của tài khoản. 0 hosted API, 0 query outcome.
Chưa cấp bank hoặc merge trong lượt này.
[Hướng dẫn vision Groq](https://console.groq.com/docs/vision).

#### FIN06 — Chốt độ phủ bank và bàn giao kế hoạch batch

Quy tắc mới giữ đủ **852 chu kỳ** trong lịch đã khóa. Một chu kỳ chỉ vào
tập thống kê cùng mã/regime khi có cả Pattern và Trend và `exit < cutoff`.
Hai tín hiệu đó cần cho tỷ lệ bẫy tăng và sai hướng. Giữ mẫu số thống kê từ
toàn tập đã đủ điều kiện, kể cả chu kỳ thiếu Alpha. Tập xếp ví dụ cần đủ bốn
tín hiệu T/P/A/I để vẫn so đúng bốn chiều. Vì vậy **733 chu kỳ có thể thành
ví dụ sau khi đủ phản hồi**, còn 119 chu kỳ thiếu Alpha chỉ có thể vào tập
thống kê. Sentiment giữ `null` theo FIN05 và không tham gia điểm kỹ thuật.
Không ép tín hiệu thiếu thành `NEUTRAL` hoặc 0. Quy tắc này là amendment
trước khi thu, có version `finalize_bank_admission_v1`. FIN07 kiểm tích hợp
schema mới, thống kê, similarity và BRPP trước khi dùng trong query.

[Kế hoạch thu máy đọc](week12/finalize_bank_collection_plan_v1.json) khóa
**1.704 slot = 852 chu kỳ × 2 node**, tối đa **5.112 attempt** nếu FIN09 áp
cap 3 cho mỗi slot. Đó là số slot logic, không phải xác nhận chọn account
hay cấp quota. Mỗi slot có ID, node, hash checkpoint và hash cửa sổ ảnh.
Script lập slot của profile cũ đã được dọn. Kế hoạch máy đọc và các hash
checkpoint được giữ để truy vết.
Request body cho toàn bộ batch và mức chi thực còn thuộc FIN09. Handoff
offline có 0 episode sẵn sàng cho thống kê, 0 sẵn sàng làm ví dụ và không
chứa outcome trong slot. Chu kỳ nào thiếu raw/parse tiếp tục chặn admission.

**10 test PASS**, gồm hai test admission/slot và tám test lịch, tín hiệu
và leakage FIN06. Biên dịch ba file Python mới PASS. Lượt này chỉ dựng
handoff offline nên không chạy full suite/E2E. Kiểm hash bank số, gói
checkpoint, byte kế hoạch và tính duy nhất của slot đã PASS. 0 API và 0
outcome query.

Tại mốc handoff này, điều kiện đóng **profile bank thị giác**
vẫn cần kết quả Pattern/Trend có trace và kiểm admission sau thu theo
hợp đồng FIN09. Nhánh chưa merge vào `develop` tại mốc này.
Lịch bàn giao 18–20/11 ở đầu tài liệu dùng một profile bank xác định mới.
Các manifest/slot đã khóa ở đây tiếp tục mô tả đúng batch thị giác.

#### FIN06 — Phát hành bank OHLCV xác định

**`PASS_OFFLINE_FIN06`**. Recipe `finalize_ohlcv_bank_v1` khóa nguồn giá, lịch,
checkpoint, công thức, quy tắc dữ liệu thiếu và phạm vi mẫu cho v1/C2/A/B.
Bank và query dùng chung `key_at` trên đúng 45 phiên VNINDEX kết thúc tại
cutoff. Pattern yêu cầu hai thân nến ngược hướng, thân cuối bao trọn và dài
hơn, đồng thời dài ít nhất nửa biên độ nến cuối. Trend cần cả tỷ lệ SMA10/SMA30
và biến động Close so với 10 phiên trước vượt ngưỡng 0,5% theo cùng hướng.
Trường hợp bằng ngưỡng Trend hoặc hai vế trái hướng trả `NEUTRAL`. Cửa sổ thiếu
phiên hoặc thiếu OHLCV trả NA kèm lý do. Báo cáo thị giác của Decision và hợp
đồng ngữ cảnh MT-BICL được giữ theo thiết kế FIN02.
[Recipe máy đọc](week12/finalize_ohlcv_bank_recipe_v1.json).

Giữ đủ 852 ID và nhãn kinh tế đã khóa. Cả 852 chu kỳ có hai khóa để vào
tập thống kê; 733 chu kỳ đủ T/P/A/I để xếp ví dụ. Có 119 Alpha NA và 852
sentiment NA. Manifest ghi độ phủ cho 16 nhóm mã/regime. Giữ lịch, nguồn
giá, HMM và scaler theo hash FIN04/FIN06. Cờ PIT độc lập cho nguồn giá vẫn
`NOT_CERTIFIED`. 102/102 query có khóa tại cutoff. Chuẩn bị bank và khóa query
dùng 0 HTTP mới, 0 outcome query và 0 lần fit lại.
[Manifest và receipt](../../outputs/finalize/ohlcv_bank_v1/manifest.json),
[bank](../../outputs/finalize/ohlcv_bank_v1/bank.json),
[khóa query](../../outputs/finalize/ohlcv_bank_v1/query_keys.json).

Sau khi khóa recipe và xác minh bản dựng, đối chiếu hai HTTP 200 đã lưu tại
`tmp/fin06_bank_hosted_single_org_v1`. Cả hai liên kết đúng hash wire và
checkpoint của FPT ngày 01/06/2020.

| Khóa | OHLCV | Thị giác | Trùng | Khác |
| --- | --- | --- | ---: | ---: |
| Pattern | `NEUTRAL` | `NEUTRAL` | 1 | 0 |
| Trend | `NEUTRAL` | `NEUTRAL` | 1 | 0 |

Cỡ mẫu là một chu kỳ. Kết quả chỉ ghi nhận mức trùng trên chu kỳ đã lưu.
Giữ nguyên journal gốc, gói checkpoint v2 và kế hoạch 1.704 slot để truy vết.
Đã dọn mã thu API, bộ lập slot cùng test của phương án trước và các bản dựng thử dư thừa.

Chạy lại phép kiểm và so byte với artifact đã phát hành.

```powershell
py -3.13 -X utf8 scripts/prepare_finalize_ohlcv_bank.py --check
py -3.13 -X utf8 -m unittest discover -s tests -p 'test_finalize*bank*leakage.py' -v
```

Lệnh `--check` tái lập đúng byte. Oracle tính độc lập 852 cửa sổ bank và
102 cửa sổ query. Cả 13 test đã đạt, bao phủ
cutoff, ngưỡng, thiếu dữ liệu, thay hậu tố giá/outcome tương lai, nhãn kinh
tế, selector và mô hình regime. Năm file Python mới biên dịch thành công. Full
suite và E2E dành cho gate tích hợp tương ứng vì thay đổi nằm ở producer offline.
FIN07 dùng bank mới để kiểm mẫu số, lấy ví dụ, fallback và nhánh MT-BICL.
FIN08 nối người gọi thực tế vào profile.

#### FIN07 — Retrieval OHLCV và ngữ cảnh MT-BICL

Adapter FIN07 ràng buộc snapshot vào khóa OHLCV, prefix giá, selector Alpha
và snapshot tin của đúng điểm đã khóa. Báo cáo Pattern/Trend thị giác vẫn
đi qua snapshot chung tới Decision. Bốn nhánh prior xếp ví dụ trên T/P từ
OHLCV cùng Alpha/Indicator. Ví dụ yêu cầu đủ bốn hướng. Tập thống kê dùng
toàn bộ chu kỳ cùng mã/regime, có T/P hợp lệ và `exit < cutoff`, kể cả chu
kỳ thiếu Alpha. Sentiment giữ NA theo FIN05.

- v1 dùng tỷ lệ mẫu của toàn tập và chọn tối đa ba ví dụ theo độ khớp T/P/A/I.
- C2 và B dùng C khớp T/P/A/I. A dùng C khớp T/P. Bổ sung background rời
  `P − C` cho hyperprior Beta. Tỷ lệ bẫy tăng có mẫu số là hợp các chu kỳ
  Pattern hoặc Trend tăng. Hai tỷ lệ sai tăng dùng mẫu số theo từng tín hiệu.
  Mẫu số 0 giữ NA. Gate ví dụ dùng giá đã scale, tuổi và khoảng cách phiên.
- Các nhánh chạy qua Common. Fallback lấy đúng action Common cùng point,
  shared, realization và repeat. Trace giữ riêng lý do OOD, thiếu khóa
  OHLCV, thiếu population và thiếu bằng chứng sau gate.

MT-BICL dựng context số từ giá thô FIN04 của từng mã, bắt đầu ở origin đã
khóa. Đóng băng lịch sử trước query đầu của từng fold trong sáu fold. Đưa
toàn bộ 102 ID vào danh sách reserve trước khi tính nhãn. Kiểm riêng tập
centroid, prior quan sát và target quan sát. Ngày công bố sự kiện dùng quy tắc
khả dụng của FIN04. Khi một sự kiện công bố trễ, tính lại feature lịch sử
bị ảnh hưởng theo đúng ngày quan sát. Dùng student seed 42/step 3000 đã pin
cho `p_student`. Teacher và 4.096 draw xác định utility, với hai ngưỡng
chuyển `CASH → LONG` khi `Q10 > 0` và `LONG → CASH` khi `−Q90 > 0`.
Ca thiếu support giữ anchor. Ca assertion của anchor sai dùng Common.

Kiểm đối chứng chạy Common, v1/C2/A/B, Fact Anchor và MT-BICL bằng các
request đầy đủ và phản hồi fixture. Truyền thử báo cáo thị giác trái chiều
để kiểm truy xuất giữ cùng proof. Kiểm poison giá tương lai, chặn nhãn query,
exit bằng cutoff, nội dung replay bị sửa và dependency khác repeat. Đây là
kiểm preparation/policy. Caller CLI/backtest/as-of/live thuộc FIN08.

Lượt đối chứng kiểm đủ **102/102 điểm**. Bốn nhánh prior có 54 điểm OOD
mỗi nhánh. Trong 48 điểm thuộc CORE4, support trước khi gọi Decision là:

| Phương pháp | Có nội dung prior | Có ví dụ | Fallback do thiếu bằng chứng |
| --- | ---: | ---: | ---: |
| v1 | 48 | 48 | 0 |
| C2 | 2 | 0 | 46 |
| A | 8 | 0 | 40 |
| B | 2 | 0 | 46 |

MT-BICL có **63 điểm đủ support**. Trong 39 điểm bypass, 23 thiếu số
quan sát ở ít nhất một dấu và 16 thiếu feature query. Oracle đối chiếu
258.048 draw, gồm các phân vị và xác suất teacher. Ba khoảng có Q10 dương
và 20 khoảng có Q90 âm. Prompt dài nhất 3.802 ký tự với ước tính reserve
3.419 token. Lượt này dùng 0 HTTP, 0 outcome query và 0 refit tài nguyên.
[Receipt FIN07](week12/finalize_context_receipt_v1.json).

Fixture dùng cùng đường lựa chọn trên bank thật, thay regime và vector query
để có đủ support. Cả C2, A và B lấy được ví dụ, khớp oracle và đưa đúng ID
vào prompt. Query thật của fixture tại FPT đầu fold có 19 chu kỳ cùng regime
và rơi vào `LOW_POPULATION_SUPPORT`. Các giá trị dùng riêng cho fixture
được giữ ngoài cohort và receipt của 102 điểm.

```powershell
py -3.13 -X utf8 scripts/check_finalize_context.py --check
py -3.13 -X utf8 -m unittest discover -s tests -p 'test_finalize_context_leakage.py' -v
```

Biên dịch bốn file Python mới và chạy 7 ca FIN07 đều đạt. Các hồi quy được
chọn bao phủ thống kê/xếp ví dụ, contract Unified, chống leakage MT, utility
và Decision. Hai phép kiểm lịch sử trong
suite replica báo lệch byte trên các file trùng `develop` trước FIN07.
H02 tái lập đúng receipt khi đọc bản CSV theo CRLF đã khóa. Pin huấn luyện
gốc dùng `backtest_engine.py` ở `77f4bada`; hai hàm tính nhãn và kiểm chi
phí trùng AST với bản đang dùng. Đối soát riêng 31 pin trong recipe số FIN06
đã đạt. Full suite và E2E toàn hệ dành cho gate tích hợp tương ứng.

#### FIN08 — Nối profile finalize vào ứng dụng

`finalize_serving_v1` là version chọn tường minh. CLI, API as-of, backtest
và live dùng chung runner paired, checkpoint và hợp đồng owner. Identity
bind version, snapshot, nguồn đã pin, runtime, model/options và owner.
Forecast slot bind thêm request, realization, repeat và hash dependency.
Reader/export mang đúng identity của bản ghi. Registry vẫn chọn bản v1
lịch sử mặc định cho đến mốc FIN13–FIN14.

Native `original_fix` của profile mới dùng renderer/schema/cap native với
năm Alpha causal giống Common. Graph chuẩn bị Indicator, Pattern và Trend
một lần cho mỗi điểm. Stage Alpha lấy selector đã fit và tin FIN05. v1/C2/A/B
dùng hai khóa OHLCV từ đúng prefix. MT và Fact Anchor dùng context đã freeze
trước ngày đầu fold Q3, giữ toàn bộ 102 ID nghiên cứu được reserve. Policy
canonical là VI. Bản EN đi trong sidecar của cùng phản hồi.

- CLI dùng `py -3.13 -X utf8 scripts/run_unified_experiment.py finalize request.json`.
  Thêm `--preview` để chạy runner và checkpoint với phản hồi đối chứng trong
  kho tạm. `request.json` có cùng cấu trúc với request API và version
  `finalize_serving_v1`.
- As-of và backtest dùng `/api/serving/v1/preflight` và `/jobs`. Hỗ trợ 1D,
  chín mã, 58 ngày phiên từ 01/07 đến 23/09/2026, tối đa 30 điểm mỗi job.
  Backtest giữ bước ba phiên. Đọc và export qua `/jobs/<id>` và `/jobs/<id>/export`.
- Live yêu cầu `POST /api/serving/live/v1/snapshot` với `symbol` và
  `profile=finalize_serving_v1`. Sau đó dùng snapshot SHA với request lồng
  có cùng version tại `/api/serving/live/v1/preflight`. Capture lấy OHLCV
  thô, Reference, ledger VCI và VNINDEX của phiên đã đóng. Kiểm origin,
  lịch, giá overlap và owner trước admission. Selector chỉ transfer lựa chọn
  đã khóa. Resume dùng đúng capture, tin dùng policy khả dụng FIN05 và
  không có payoff live.

Preflight hosted trả `HOSTED_RELEASE_PENDING_FIN10`. Chế độ fixture thực
thi các slot qua transport đối chứng. Cả payoff của 102 điểm nghiên cứu và
payoff ứng dụng vẫn khóa. Backtest đối chứng xuất
`OFFLINE_FIXTURE_OUTCOME_LOCKED`. Outcome thực được thiết kế chỉ mở sau đủ
slot forecast của point. Rào lịch, quyền và volume giữ NA có lý do trước
khi gọi công thức T+2.5. Chứng cứ FIN07 vẫn thuộc kiểm offline. Profile mới
mang `EXPLORATORY_NOT_CERTIFIED`.

**`PASS_OFFLINE_FIN08`**. Đối soát 162 pin của nguồn và receipt kế thừa.
Đủ 522 prefix của chín mã × 58 phiên với ít nhất 600 nến và khóa OHLCV 45
phiên. Lượt CLI so sáu lựa chọn và hai dependency qua hai repeat hoàn tất
16 slot, dùng một snapshot, hai phản hồi vision fixture và tám phản hồi
Decision fixture. Lượt backtest API kiểm reader/export giữ nguyên identity
và nhãn khóa. Lượt live dùng một phiên bổ sung đối chứng sau lịch FIN04,
kiểm overlap, transfer selector và quyền owner. Replay giữ nguyên kết quả,
identity và số lượt fixture. Đường capture live đã kiểm với
nguồn đối chứng trong lượt này. Số lượt gọi Groq là 0.

Biên dịch 18 file Python thay đổi. Năm ca FIN08 và các hồi quy được chọn
của serving/runtime, contract, live admission và export đều đạt. Giữ byte
evaluator lịch sử để job đã khóa vẫn đọc/xuất theo receipt gốc. Chạy các
gate toàn hệ ở mốc tích hợp tương ứng.

#### FIN09 — Chốt bảng tái sử dụng và ngân sách API

Dry-run giữ nguyên 102 điểm và ba repeat của FIN02. Mỗi điểm dựng Pattern và
Trend đúng một lần từ nguồn FIN04–FIN08 rồi dùng cùng snapshot cho tám vai
trò. Smoke dựng riêng một điểm với một repeat. Điểm smoke theo lịch U08 là
`BHN-2025-10-01`. Bank xác định cần 0 lượt HTTP. Kiểm lại 1.702 attempt U08
theo hash raw, gồm 1.687 active và 15 đã rút. Mỗi slot lưu hash riêng cho
messages, ảnh, schema, model/options và wire, cùng bằng chứng dependency và
đúng repeat. Nếu chưa có báo cáo thị giác thật hoặc kết quả parent, body
Decision đối chứng chỉ để tính token. Quyết định reuse chờ đủ bằng chứng wire
và dependency. MT-BICL còn cần Fact Anchor hợp lệ ở cùng repeat.

Giữ model `qwen/qwen3.8-27b` cho thị giác và `openai/gpt-oss-20b` cho
Decision. Giữ `on_demand`, 960 token đầu ra và temperature theo FIN02.
Ngày 18/11, `GET /models` của org được chọn trả HTTP 200 và liệt kê cả hai
model. Header của lượt metadata chưa xác nhận được số dư hiện tại. Dry-run
chặn mạng và không chạy completion hoặc mở outcome. Hạn mức đang dùng để
lập dự toán cho mỗi model là 30 RPM, 1.000 RPD, 8.000 TPM và 200.000 TPD.
Giữ một org Free, ngân sách 0 USD. Không gộp quota từ các org trong `.env`.
[Giới hạn Groq](https://console.groq.com/docs/rate-limits).
[Chính sách sử dụng Groq](https://console.groq.com/docs/legal/ai-policy).

**`PASS_OFFLINE_FIN09_BUDGET`**. Trong 2.652 slot nghiên cứu, 10 slot vision
ở năm điểm HVN đủ proof để dùng lại, 1.161 slot Decision bypass vì policy
thiếu support, và 1.481 slot dự kiến gọi mới. Sáu trong mười slot smoke dự
kiến gọi mới. Có hai attempt `UNKNOWN` đã rút khỏi archive active. Dry-run
không chuyển chúng thành reuse hay đặt lại UUID cũ. Tổng trần là **4.461
attempt** cho 1.487 slot mới, gồm retry và repair trong cap ba mỗi slot.

| Model | Lượt mới gồm smoke | Trần attempt | Token lượt đầu theo p50–p95 U08 | Reserve fixture lượt đầu | Reserve fixture nếu đủ ba attempt |
| --- | ---: | ---: | ---: | ---: | ---: |
| `qwen/qwen3.8-27b` | 196 | 588 | 482.552–487.452 | 1.036.938 | 3.110.814 |
| `openai/gpt-oss-20b` | 1.291 | 3.873 | 2.516.313–2.607.786 | 4.144.882 | 12.580.332 |

Ảnh chụp ledger lúc 13:11 UTC ngày 18/11 tính hai request FIN06, 3.917 token
đã dùng ở Qwen. Ledger cục bộ còn bốn request với tổng 8.790 token chưa rõ
org/model, nên trừ bảo thủ vào cả hai dự toán. Số dư ước tính cho cửa sổ 24
giờ đầu là **187.293 token / 994 request** ở Qwen và **191.210 token / 996
request** ở GPT. Số dư do Groq xác nhận vẫn chưa có. Theo mức sử dụng U08,
Qwen cần 3 cửa sổ quota 24 giờ và GPT cần 13–14. Theo reserve fixture cho
lượt đầu, hai model lần lượt cần 6 và 21 cửa sổ. Các kịch bản này vượt mốc
20/11 cho toàn batch và chưa tính chờ phát hành hoặc lỗi ngoài dự toán.

Biên dịch năm file Python thay đổi và đạt 52 kiểm thử chọn theo phạm vi
FIN09, gồm đối chiếu body, quota/pacing, PIT và checkpoint/UNKNOWN. Kiểm lại
checksum ledger, từng tham chiếu raw U08, nguồn và runtime bằng
`py -3.13 -X utf8 scripts/prepare_finalize_api_budget.py --check`. Ledger giữ
`execution_permitted=false`. FIN10 khóa đường đối chứng của runner một org.
Lượt gọi FIN11 cần xác nhận hạn mức Free và số dư thực tế.
[Ledger, quota và bằng chứng từng slot](week12/finalize_api_budget_v1.json).

#### FIN10 — Nghiệm thu offline trước thu query

**`PASS_OFFLINE_FIN10`** trên Python 3.13.5. Khóa SHA-256 của ledger FIN09,
2.662 slot, model/options, 278 file nguồn runtime, các điểm vào kiểm thử và
162 pin tài nguyên. Đối soát lại toàn bộ 1.702 raw U08 khi dựng fixture và
khi cold replay. Receipt khóa từng nhóm kiểm thử theo nguồn và hash log.

Runner nghiên cứu đối chứng dùng một org, ledger riêng theo model và namespace
đã khóa. Mỗi point dựng một upstream rồi ghép đúng tám vai trò. Checkpoint
lưu đủ point, repeat, shared snapshot, request và dependency cùng repeat.
Router transport kiểm wire khớp FIN09 cho vision. Với body Decision còn phụ
thuộc báo cáo thật, kiểm schema/options đã khóa và áp trần runtime trên body
thực tế, kể cả repair. Cap ba attempt giữ nguyên qua lần khởi động lại.

- Smoke `BHN-2025-10-01` hoàn tất 8 forecast slot với 6 lượt fixture, trong
  một identity độc lập. Nghiên cứu dùng `FPT-2023-07-03` và `HVN-2025-10-01`
  để kiểm đủ 48 slot qua ba repeat, 29 lượt fixture và 2 raw vision U08 đạt
  proof. Dừng ngay sau khi ghi raw, rồi resume giữ nguyên UUID và tránh gửi lại.
  Thử tháo raw của slot đã complete để xác nhận resume dừng trước dispatch.
- Timeout đối chứng lưu `UNKNOWN` và token reserve. Khởi động lại dừng trước
  khi gửi thêm. Chỉ tiếp tục sau khi đối soát đúng UUID thành `NOT_SENT`, giữ
  attempt cũ trong lịch sử và trong cap. Outcome của query luôn đóng.
- Sửa nến tương lai trong RAM ở điểm FPT, dựng lại graph và giữ nguyên hash
  snapshot cùng 24 request. Cold replay trong tiến trình Python mới tái lập
  56 slot, cùng hash raw/policy và 0 lượt dispatch mới.

Biên dịch ba file Python mới và đạt **153 kiểm thử** về PIT, tài khoản/P&L,
ghép cặp, prompt/token, quota, retry/checkpoint, owner/cache và caller serving
theo phạm vi FIN10. Lượt này dùng hồi quy tích hợp theo phạm vi thay cho chạy
lại toàn bộ unit suite và E2E toàn hệ. Lệnh kiểm khóa và receipt là
`py -3.13 -X utf8 scripts/finalize_offline_acceptance.py check`.
[Receipt nguồn, fixture và kết quả gate](week12/finalize_offline_acceptance_v1.json).

Khoanh phạm vi dữ liệu theo xác nhận FIN04. Chứng nhận PIT độc lập của nhà
cung cấp vẫn chưa có. Có 0 lượt gọi Groq thật và 0 outcome thị trường được mở.
FIN11 cần xác nhận hạn mức Free, số dư thực và giữ carry của một org xuyên
smoke/research trước khi cấp quyền thu. Receipt FIN10 giữ
`execution_permitted=false`.

#### FIN11 — Thu phản hồi trên một org Free

Chủ tài khoản xác nhận hạn mức 200.000 token/ngày cho hai model và cho biết
Groq đã cho phép quy trình dùng nhiều org của các lượt thí nghiệm. Org 1 là
org gốc đã kiểm metadata ở FIN09, ngân sách 0 USD. Mỗi phiên dùng một org do
tác giả chọn trong phạm vi Groq cho phép cho FIN11. Chính sách Groq áp hạn
mức theo tổ chức và có ngoại lệ theo từng trường hợp.
[Giới hạn Groq](https://console.groq.com/docs/rate-limits).
[Chính sách Groq](https://console.groq.com/docs/legal/ai-policy).

Runner `scripts/finalize_hosted_study.py` kiểm lại FIN10 và ledger FIN09 trước
khi tạo grant. Hai phase dùng chung sổ quota của từng org và model nên usage
smoke được tính vào lượt nghiên cứu của đúng org. Smoke có identity riêng và phải đủ tám slot
trước khi mở phase nghiên cứu. Runner giữ request/UUID và cap ba attempt,
tái dùng raw U08 đủ proof, ghi checkpoint mỗi point và giữ outcome thị trường
đóng cho FIN12. Grant, raw và receipt của lượt thu ban đầu giữ nguyên byte.
Release vận hành mới chỉ ghi thêm org nguồn cho attempt mới. Khi replay,
attempt cũ thiếu trường org thuộc org 1. Bản sao smoke hiện có đã replay
offline với 8 slot, 6 raw và 0 dispatch mới. Bản sao điểm FPT đang dở hoàn tất
24 forecast bằng mock ở org khác, giữ nguyên hash 22 raw nghiên cứu đã có.
Biên dịch bốn file Python thay đổi, đạt 8 test FIN11 và 26 test serving runtime.

Chủ org 1 xác nhận chỉ dùng một phần nhỏ quota và còn đủ để bắt đầu. Grant
ghi xác nhận của chủ org, ngân sách 0 USD và carry 24 giờ tính từ ledger cục
bộ. Số dư chính xác trên Console chưa có. Worker chờ khi chạm quota phút.
Nếu quota ngày chặn lượt gọi, worker lưu `STOPPED_DAILY_QUOTA` và thoát. Lỗi
429 theo ngày được lưu với UUID và tính vào cap của slot. `UNKNOWN` vẫn khóa
slot cho đến khi được đối soát. Tác giả chạy lệnh sau từ thư mục gốc để nối
journal hiện có với key ở ô 1. Thay `1` bằng ô org được phép cho phiên kế tiếp.

```powershell
$env:OMP_NUM_THREADS = '1'
$env:MPLBACKEND = 'Agg'
py -3.13 -X utf8 -u scripts/finalize_hosted_study.py resume --org 1
```

Lệnh `py -3.13 -X utf8 scripts/finalize_hosted_study.py status` đọc tiến độ
tại kho cục bộ `outputs/finalize/fin11_v1/`.

Khi thấy `UNKNOWN_NEEDS_RECONCILIATION`, dùng lệnh offline sau để lấy UUID,
slot, org, model và thời điểm gửi theo UTC:

```powershell
py -3.13 -X utf8 scripts/reconcile_finalize_hosted_study.py list
```

Đối chiếu log của đúng project Groq. Nếu có bằng chứng attempt cụ thể chưa
được gửi, lưu nguồn bằng chứng vào một file UTF-8. Lệnh `not-sent` ghi hash
của bằng chứng, giữ UUID, reserve và cap của slot. Sau đó tác giả chạy lại
`resume` để thu tiếp. Khi chỉ có trạng thái `UNKNOWN`, slot chờ đối soát.

```powershell
py -3.13 -X utf8 scripts/reconcile_finalize_hosted_study.py not-sent --request-id <UUID> --evidence <file-bang-chung>
```

Biên dịch hai file Python mới và đạt ba test cho đối soát UUID, bằng chứng,
tính idempotent và việc giữ reserve. Đã thử đối soát trên bản sao checkpoint
FPT.

Tác giả xác nhận Groq trả HTTP 200 cho attempt FPT `10ad1438-158e-46c7-af23-591076dcb755`
và yêu cầu dựng lại toàn bộ điểm do thiếu raw. Lệnh offline `reset-point`
tách wire, stage và ảnh của `FPT-2023-07-03` sang `point_resets/` với manifest
hash. Sổ quota giữ 13 attempt cũ, trong đó có 3.132 token reserve của lượt
thiếu raw. Cap ba attempt tính chung cả bản lưu và lượt mới. Journal cho
`resume` tiếp tục từ FPT với một upstream mới và đủ ba repeat. Miền nghiên
cứu vẫn gồm 102 điểm. Kiểm trên bản sao tái dựng 24 slot với 17 lượt mock.
Đã tách 56 file của FPT trong checkpoint thật và xác minh 117 file còn lại
cùng sổ quota giữ nguyên byte. Trạng thái là `POINT_READY_TO_REPLAY`, điểm
CMG đã hoàn tất. Biên dịch sáu file Python thay đổi và đạt 14 test trong
hai nhóm runner và đối soát. Lượt thao tác này có 0 gọi Groq.

Khi chuyển sang org 2, lượt `MT_BICL` ở repeat đầu của `VJC-2023-07-03`
được tác giả xác nhận HTTP 200 nhưng thiếu raw. Đã ghi `RESPONSE_LOST` cho
đúng UUID, giữ 3.712 token reserve và 95 phản hồi đã nhận. Trạng thái là
`SLOT_READY_TO_REPLAY`. `resume --org 2` tiếp tục tại slot này. Bản sao
checkpoint đã hoàn tất 24 slot của VJC với 9 lượt mock.

Transport FIN11 ghi HTTP status trước khi đọc body và lưu bản sao body
trước khi ghi wire chính. Khi tiếp tục, ưu tiên raw đã lưu, kể cả khi đổi
org. Nếu HTTP 200 đã được ghi mà body bị mất, runner chỉ thử lại đúng slot
trong cap ba attempt và giữ reserve cũ. Nếu chưa có bằng chứng HTTP durable,
slot vẫn chờ đối soát. Biên dịch các file Python thay đổi, đạt 18 test FIN11
và 26 test serving runtime sau khi nguồn ổn định. Đối soát offline lần này
có 0 gọi Groq.

FIN11 v5 dùng quota ngày do Groq báo. Carry và các attempt cũ được lưu để
đối soát. Runner tiếp tục bằng cùng lệnh `resume --org 1` và vẫn điều tiết
theo phút. Khi Groq báo hết quota ngày, runner ghi `STOPPED_DAILY_QUOTA`
và thoát. Nếu Groq không báo thời điểm thử lại, runner bỏ trường
`resume_at` và có thể nhận lệnh `resume` sau khi Console báo có quota.
Đạt 19 kiểm thử FIN11, biên dịch các file Python thay đổi và đối soát grant
cùng các khóa vận hành v2–v4 bằng `check`. Bản sao sổ org 1 tái hiện được
mốc chặn cũ và xác nhận v5 cho phép đặt lượt gọi tại cùng thời điểm. Lượt
kiểm tra có 0 gọi Groq.

##### Nghiệm thu FIN11 ngày 20/11/2026

Runner ghi `PASS_FIN11` lúc 14:11:12 giờ Việt Nam. Smoke `BHN-2025-10-01`
đủ 8 forecast, 6 HTTP 200 và 12.952 token đo được. Research đủ 102 điểm,
2.448 forecast và 204 slot thị giác. Toàn bộ 2.652 slot nghiên cứu khớp
FIN09, gồm 1.481 slot gọi mới, 10 slot thị giác tái dùng U08 và 1.161
slot bypass. Điểm `FPT-2023-07-03` đã được dựng lại và có đủ forecast.
[Receipt smoke](../../outputs/finalize/fin11_v1/smoke/receipt.json).
[Receipt nghiên cứu](../../outputs/finalize/fin11_v1/research/receipt.json).

Journal nghiên cứu hiện hành có 1.492 attempt, gồm 1.481 HTTP 200 có raw,
9 HTTP 429 và 2 `RESPONSE_LOST` đã đối soát. Bản lưu FPT giữ thêm 13 attempt,
trong đó có một lượt thiếu raw đã được tác giả xác nhận HTTP 200. Cả 1.511
attempt kể cả smoke và bản lưu đều khớp từng UUID, model, org và usage với
sổ quota. Có 3.008.327 token đo được và 10.568 token reserve cho ba lượt thiếu
raw. Mỗi slot dùng tối đa hai attempt, kể cả bản lưu, trong cap ba của FIN09.
Journal hiện hành không còn `UNKNOWN`.

Cold replay trên bản sao trong tiến trình mới tái tạo hai receipt, khớp từng
checkpoint và không phát sinh lượt gọi Groq. SHA-256 của tệp receipt nghiên
cứu là `dcf3c28a54343b9506e0834a244cc371bced51b8f478155c9ef004cabddb776b`.
Đã đối soát khóa FIN09, FIN10, grant và release FIN11 v2–v5. Đợt nghiệm thu
chỉ cập nhật kế hoạch và kiểm bằng chứng đã có nên không chạy lại compile,
unit suite, E2E hoặc leakage suite. Outcome thị trường vẫn đóng, sẵn sàng
bàn giao receipt và checkpoint cho FIN12.

#### FIN12 — Đánh giá offline bản sửa

Đã xác minh 2.448 forecast từ receipt FIN11 trước khi mở outcome. Tám
phương pháp dùng chung nhãn và lịch thực thi đã khóa. Hai đối chứng
`CASH_EVERY_CYCLE` và `ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS` dùng cùng
chu kỳ. Artifact giữ từng forecast, profile, raw proposal, hành động cuối,
lý do bypass, hash raw và epoch. Mười phản hồi thị giác tái dùng giữ nguồn U08.
[Kết quả FIN12](../../outputs/finalize/fin12_v1/results.json).
[Receipt FIN12](../../outputs/finalize/fin12_v1/receipt.json).

Có 96/102 nhãn hợp lệ và 45/51 tài khoản đủ hai chu kỳ mỗi repeat. Giữ NA
cho năm điểm có sự kiện quyền trong kỳ nắm giữ và `BHN-2026-07-01` có phiên
thực thi không khớp lệnh. Lợi nhuận tài khoản và BA trên miền chính đã khóa
giữ NA. Phân tích độ nhạy dùng giao 45 tài khoản/90 điểm chung cho mọi
phương pháp. Bảng phân loại trên 96 điểm có nhãn ghi mẫu số riêng.

Trên giao 45 tài khoản, lợi nhuận bình quân của Native sửa là −0,9379%,
Common là −0,5304% và MT-BICL là −1,0600%. Chênh lệch của MT-BICL lần lượt
là −0,1221 và −0,5297 điểm phần trăm so với hai baseline. Cả tám phương pháp
đều có mean return âm trên giao này. Giữ đủ 20 contrast và các sensitivity
L1/L3, bỏ từng fold/mã và CORE4. Bootstrap L2 có 10.000/10.000 draw joint
finite. Band đồng thời giữ NA vì có contrast với độ lệch chuẩn bằng 0.

Oracle Decimal kiểm 96 nhãn và 1.350 tài khoản có thể tính, gồm các dòng
tiền, chi phí và NAV. Oracle theo số đếm fold kiểm cả 20 contrast và
10.000 draw L2. Biên dịch bốn tệp Python thay đổi và đạt 37 kiểm thử chọn
theo phạm vi FIN12, PIT giá và evaluator thống kê dùng lại. Tiến trình mới
tái tạo khớp byte cả chín artifact với `verify`. SHA-256 của receipt là
`d304f01ca78f3eef6666f14a6e39df60dd6dda4af3a8095c1a490ff9ec831c31`.
Chạy `py -3.13 -X utf8 scripts/evaluate_finalize_study.py analyze` để dựng
lại ở môi trường có journal FIN11 và các nguồn đã khóa, hoặc thay
`analyze` bằng `verify` để kiểm artifact đã có. Không gọi Groq trong FIN12.

#### FIN13 — Đối soát cờ của bản sửa

Giữ cohort FIN02 gốc gồm 102 điểm và 2.448 forecast cho nghiệm thu hệ
thống. FIN12 có 96 nhãn thực thi và 45/51 tài khoản đủ hai chu kỳ. Năm
chu kỳ có sự kiện quyền và một chu kỳ thiếu khớp lệnh giữ NA theo hợp đồng
đã khóa. Một cohort thay sáu ngày chỉ tăng độ phủ nhãn và đổi mẫu đánh
giá. Chứng nhận nguồn PIT yêu cầu hồ sơ khả dụng của dữ liệu tại chính
cutoff, nên FIN13 dùng bằng chứng từ cohort gốc.
[Đối soát FIN13 theo source và runtime](week12/finalize_system_gate_v1.json).

| Cờ FIN01 | Kết quả kiểm trên bản sửa và phạm vi áp dụng |
| --- | --- |
| `ALPHA_NATIVE` | **Đã xử lý trên profile sửa.** FIN03 kiểm 85 yếu tố và sáu cửa sổ với prefix/future poison, fit/purge và selector đóng băng. FIN08 xác minh Native sửa và Common nhận cùng năm Alpha causal. FIN11 lưu đúng profile trong 2.448 dự báo. Native lịch sử giữ FAIL cùng phản ví dụ bfill, chuẩn hóa toàn chuỗi và nhánh volume. [FIN03](#fin03--alpha-nhân-quả-selector-và-bridge-offline-ngày-18112026). |
| `ALPHA_ONLY` | **Các cơ chế PIT phần mềm đạt trong miền đã kiểm theo giả định nguồn FIN04.** FIN10 khóa nguồn, tài nguyên và runtime. FIN11 giữ barrier trước outcome. FIN12 đối chiếu nhãn/account/oracle sau barrier. Cờ toàn hệ theo tiêu chí có chứng cứ PIT nguồn độc lập vẫn `NOT_CERTIFIED`. [FIN10](week12/finalize_offline_acceptance_v1.json). |
| `NEWS_PIT` | **Đạt với trạng thái thiếu tin tường minh.** Snapshot chia sẻ với báo cáo/UI. Cả 102 điểm loại tin chưa đủ chứng cứ khả dụng. Profile mới đạt theo policy loại trừ này. [FIN05](week12/finalize_news_coverage_v1.json). |
| `PRICE_PIT` | **Chặn ở nguồn.** Giá thô được tác giả chấp nhận để đánh giá, lịch và sự kiện đã qua audit phạm vi. Chứng nhận độc lập cần bản lưu phiên bản giá đã công bố tại cutoff, lịch phiên và ledger sự kiện có truy vết cho chín mã. [FIN04](week12/finalize_price_acceptance_v1.json). |
| `BANK_LINEAGE` | **Đạt trên bank OHLCV mới.** 852 chu kỳ có nhãn theo oracle, 733 đủ điều kiện làm ví dụ. Giữ dữ liệu mature, recipe tín hiệu, các pin HMM/scaler và fallback Common khi ngoài CORE4. [Manifest FIN06](../../outputs/finalize/ohlcv_bank_v1/manifest.json). |
| `MT_LINEAGE` | **Đạt trong phạm vi đã khóa.** FIN07 kiểm context freeze, reserved IDs, student/teacher, facts, support và Q10/Q90. FIN11 đối chiếu dependency cùng repeat và forecast thật. [Receipt FIN07](week12/finalize_context_receipt_v1.json). |
| `CALLER_IDENTITY` | **Đạt với profile được chọn tường minh.** FIN08 kiểm CLI, API as-of/backtest, capture live đối chứng và reader/export; FIN10 khóa tài nguyên và caller. Gate đổi mặc định chờ FIN13–FIN14. [FIN08](#fin08--nối-profile-finalize-vào-ứng-dụng). |
| `SOURCE_DELTA` | **Đạt trên chuỗi đã khóa của bản sửa.** FIN09/10 kiểm ledger, nguồn và runtime. FIN11/12 đối chiếu release, raw và checkpoint. Mười phản hồi thị giác tái dùng có proof theo đúng U08. [FIN09](week12/finalize_api_budget_v1.json). |
| `OLD_PENDING` | **Mốc lịch sử.** U09 có receipt riêng. Kết luận FIN13 dùng nguồn bản sửa và các receipt đúng epoch. [Receipt U09](week12/unified_analysis_acceptance.json). |
| `UI_ACCEPTANCE` | **Hồi quy offline đã đạt cho giao diện chịu ảnh hưởng.** Đã kiểm bằng Chromium desktop/mobile. Hosted ứng dụng còn chờ phát hành. [FIN14](#fin14--hồi-quy-giao-diện-và-export). |
| `ARCHIVE_LAYOUT` | **Chờ FIN16 cho cold restore toàn gói.** Các pin cần cho lượt phân tích FIN12 đã đọc lại thành công. Kế hoạch đóng gói giữ index và byte bằng chứng gốc. [Index bằng chứng](revision_evidence/index.json). |
| `EXECUTION_LIMITS` | **Giới hạn của nghiên cứu exploratory.** Giữ sáu nhãn NA và mẫu số đúng. Kết quả dựa trên nguồn giá đã chấp nhận và mô hình thực thi T+2.5. [Kết quả FIN12](../../outputs/finalize/fin12_v1/results.json). |

Đã đối soát khóa FIN09/10, raw và checkpoint FIN11 cùng chín artifact FIN12
qua cold verify. Kiểm sai có chủ đích xác nhận validator từ chối cờ PIT
giả, hash giá lệch và forecast sửa hành động rồi tính lại hash cục bộ.
Mốc này chỉ thêm biên bản và kiểm lại bằng chứng theo phạm vi, nên không
chạy lại compileall, unit suite, E2E hoặc leakage suite. Có 0 lượt gọi Groq.
Receipt đối soát ban đầu ghi `BLOCKED_INDEPENDENT_PRICE_PROVENANCE`.

Ngày 20/11/2026, tác giả xác nhận phiên bản giá đang dùng là chính xác về
mọi khía cạnh và yêu cầu hoàn thiện FIN13 để tiếp tục FIN14. Nghiệm thu sử
dụng phạm vi nguồn do tác giả xác nhận cùng 102 điểm FIN02 gốc.
`PASS_FIN13_OWNER_ATTESTED_SCOPE` cho phép tiếp tục hồi quy ứng dụng.
Chứng nhận PIT nguồn giá độc lập vẫn `NOT_CERTIFIED`. Kết luận khoa học
giữ phạm vi exploratory của nguồn và thiết kế đã khóa.
[Receipt chốt FIN13](week12/finalize_system_gate_v2.json).

#### FIN14 — Hồi quy giao diện và export

Hai form Phân tích và Backtest cho chọn tường minh `finalize_serving_v1`.
Phiên bản được khóa cùng request từ preflight đến lúc tạo job. Trang kết quả
hiển thị nguồn, profile, trạng thái PIT và export theo đúng phạm vi owner.
Phân tích dùng đúng capture giá thô và trình đọc của profile sửa. Báo cáo
U09 tiếp tục đọc từ gói kết quả lịch sử riêng.

Ngày 20/11/2026 đã chạy Flask thật trên loopback với nguồn giá và phản hồi
mô hình đối chứng, quan sát tám ảnh Chromium ở 1365×900 và 390×844. Đã kiểm
trực tiếp VI/EN, chế độ sáng/tối, xuất JSON và luồng U09. Phân tích MT-BICL
hiển thị Raw/Final/Context cùng Common và Fact Anchor. Backtest hoàn tất
tám slot ở một cutoff, giữ tám nhãn lợi nhuận NA của fixture. Projection
lỗi, partial và UNKNOWN giữ slot chưa có forecast và khóa resume ở UNKNOWN.
Đã sửa nền panel và header bảng ở chế độ tối, rồi kiểm lại màu và chiều
rộng, không có cuộn ngang toàn trang.

Kết quả kiểm theo phạm vi gồm 47 kiểm thử Node về phân tích, backtest,
viewer nghiên cứu và tùy chọn hiển thị, 5 kiểm thử FIN08 về PIT/serving,
26 kiểm thử runtime ứng dụng về admission/job/checkpoint. Thay đổi chỉ ở
template, CSS và JavaScript của ứng dụng cùng test JS. Không biên dịch
Python hay chạy lại bốn gate toàn hệ. Số lượt Groq thật là 0.

Backend ứng dụng vẫn trả `HOSTED_RELEASE_PENDING_FIN10` cho profile sửa.
Receipt FIN11 bao phủ runner thu dự báo nghiên cứu. FIN14 đã xác minh nút
chạy bị chặn và hiển thị lý do trên web. Phát hành hosted cần nghiệm thu
qua caller ứng dụng trước khi chuyển mặc định.

#### FIN15 — Đồng bộ hai bản thảo

Bài báo giữ tiêu đề và cấu trúc trước FIN15. Abstract nêu khoảng trống
của QuantAgent, giải pháp Alpha Agent và Sentiment Agent, thiết kế so sánh
ghép cặp và kết quả định tính. BICL v1–v5 được trình bày như nghiên cứu
mở rộng. Abstract khóa luận giải thích cách chọn ngữ cảnh trước cutoff,
chính sách sửa hành động, mẫu số FIN12 và giới hạn kết quả. Khóa luận
lấy đóng góp tăng thêm của BICL làm câu hỏi chính, đồng thời truy vết
QuantAgent, Our system, hai đối chứng và từng phiên bản trong bảng phương
pháp. Hai bản phân biệt kết quả thành phần, lượt nghiên cứu ngữ cảnh lịch
sử và lượt chạy lại FIN12. Khóa luận bổ sung năm hình về nguồn bằng chứng,
suy luận regime, lọc lịch sử, độ phủ và kết quả FIN12. Số trích dẫn đặt
sát tác giả, công trình hoặc khái niệm được dẫn.

Bảng FIN12 được chiếu từ kết quả đã đối soát SHA-256 với receipt. Đã
kiểm lại 68 dòng bảng lịch sử khi đổi tên bản trình bày và giữ nguyên
ID của các artifact. Nguồn khóa luận dùng `thesis/main.tex` ở gốc dự án
Overleaf, với đường dẫn nội bộ và hỗ trợ pdfLaTeX/XeLaTeX. Có thể nén
trực tiếp nội dung thư mục nguồn. Kế hoạch và hồ sơ lịch sử để ở
`docs/plan/thesis/`. PDF hiện hành ở `outputs/`. Tiếp tục
[P10](thesis/plan.md#p10-đóng-gói-tái-lập-và-bàn-giao) từ nguồn này.

Đã build sạch hai điểm vào bài báo bằng pdfLaTeX/BibTeX và khóa luận
bằng pdfLaTeX/Biber cùng XeLaTeX/Biber. Đã render để rà bố cục và kiểm
tham chiếu, số liệu, sơ đồ và bảng phiên bản. Hai bản bài báo có 45 và 44
trang. Khóa luận có 70 trang A4 dọc trên cả hai engine. Công việc thay đổi bản thảo
và công cụ build tài liệu. Các gate nghiên cứu và lượt gọi API thật được
giữ theo biên bản trước.

[Bài báo](../../outputs/paper/main-fin15.pdf) ·
[Bản nộp bài báo](../../outputs/paper/main-submit-fin15.pdf) ·
[Khóa luận](../../outputs/thesis/thesis-fin15.pdf) ·
[Thư mục nguồn tự nén cho Overleaf](../../thesis/) ·
[Hướng dẫn Overleaf](thesis/build.md).

### Mốc đã ghi nhận trước kế hoạch finalize

Các trạng thái dưới đây là hồ sơ trước FIN00, dùng để truy vết nguồn và
kế thừa kiểm tra theo phạm vi. Tiến độ công việc finalize cập nhật tại
checklist FIN00–FIN17 ở trên.

**Viết khóa luận, cập nhật ngày 17/11/2026:** thư mục làm việc là `thesis/`.
**P9 bổ sung đã tự rà xong T80a–T80l:** [checklist và đặc tả](thesis/plan.md#p95-bổ-sung-theo-rà-soát-bản-60-trang).
Bản mới 67 trang,21 bảng/8 hình, không phụ lục, A4 dọc/rotation0. Đã thêm bằng chứng
student/regime theo nguồn đã lưu, thu hẹp các kết luận thiếu nguồn, giải thích mẫu/tham số,
nhân quả và cơ chế; thêm DAG/hai biểu đồ, sửa điều hướng và biên tập cuối.
Clean build bốn lượt/Biber trong bản sao độc lập; xem đủ 67 trang render 120 dpi;
51 bookmark/51 TOC title links đúng tiêu đề thật,146 đích nội bộ hợp lệ.
G5 chốt lại trong phạm vi nội bộ, P10/T81–T84 còn mở. Chưa phản biện ngoài/ký/nộp;
chuẩn trường và quyền phân phối chưa rõ vẫn là giới hạn. Không gọi API/fit/inference/
bootstrap/replay hoặc chạy lại suite runtime. Checklist duy nhất ở `thesis/plan.md`.

**UI được tác giả nghiệm thu ngày 17/11/2026:** giao diện hoàn thiện cho khóa luận, có thể cải tiến sau này. Khóa luận và serving contract đã cập nhật; các receipt/browser chưa chạy ở mốc trước giữ làm lịch sử. Không suy nghiệm thu UI thành chứng nhận nhân quả hoặc hiệu quả giao dịch.

**Review bổ sung đã xử lý:** sửa phân biệt phiên bản bản thảo/mã thực nghiệm/nguồn PDF cuối và diễn giải sensitivity; giảm lặp UI, làm rõ giới hạn regime/student. Bản67 trang có tag cục bộ `thesis-review-20261117-r1` và manifest input/PDF; chưa đóng gói P10 hoặc chạy thực nghiệm mới.

**Mốc lịch sử P9/T73a–T73l và T73–T80:** đã rà nội bộ bản biên tập **60 trang**,
toàn A4 dọc/rotation=0, không phụ lục. Giữ12pt/giãn1,5/lề cũ; hai nghiên cứu,
hai baseline, family20, support/bypass/NA/kết quả âm và Native FAIL/NOT_CERTIFIED/
UI PENDING không đổi. LaTeX là nguồn chính; source map/archive P8 giữ lịch sử.
Build sạch bốn lượt LuaLaTeX+Biber không cần Markdown/archive/mẫu PASS;
đã kiểm render60 trang, nguồn và đối soát luận điểm đúng phạm vi. Không chạy
suite nghiên cứu vì code/runtime/input/model/receipt giữ nguyên.
T74–T80 đã rà người đọc, tiếng Anh, citation/quyền, số học, clean build,
mọi trang và phản hồi thực nhận. Kết quả G5 cũ chỉ thuộc lượt tự rà tại mốc đó,
không thay việc xử lý phát hiện mới. P10/T81–T84 còn mở, chưa phản biện ngoài/ký/nộp. Quy định trường và quyền
phân phối tài nguyên chưa rõ tiếp tục được ghi ở sổ bằng chứng. P1–P8 dưới đây là lịch sử.

[Dàn bài tiếng Anh](thesis/outline.md) và [kế hoạch chi tiết bằng tiếng Việt](thesis/plan.md)
bao phủ từ chuẩn bị đến bàn giao PDF/nguồn cuối qua 84 task. Phần phương pháp
phải giải thích toàn hệ thống cho giảng viên lần đầu tiếp cận.
[Checklist viết khóa luận](thesis/plan.md#21-một-nguồn-trạng-thái-công-việc) là nơi duy nhất
cập nhật trạng thái ngay trong kế hoạch theo yêu cầu tác giả. Hồ sơ yêu cầu,
phạm vi nghiên cứu và [kiểm kê hai nghiên cứu](thesis/evidence.md#3-kiểm-kê-nguồn-hiện-tại-và-hai-nghiên-cứu-đã-khóa)
đã có; [danh sách đọc](thesis/evidence.md#4-danh-sách-đọc-nguồn-gốc-và-quy-ước-khóa-trích-dẫn)
phân nhóm nguồn gốc, trạng thái đọc/kiểm và quy ước khóa trích dẫn.
[Thuật ngữ và ký hiệu](thesis/evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt)
thống nhất tên phương pháp, cấp episode/task/query và đơn vị.
[Danh mục hình/bảng/thuật toán](thesis/evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn)
giữ 23 ID có task, vị trí, loại nguồn và provenance; sản phẩm sẽ tạo tại task
phụ trách. [Ví dụ xuyên suốt EX01](thesis/evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết)
chọn FPT tại cutoff 03/07/2023 theo quy tắc không dùng outcome, nối nguồn
đầu vào/lịch sử/proposal/policy và tách kết quả sau cutoff.
[Khung sáu chương](thesis/evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm)
đã đủ bản nháp nội dung tiếng Anh và dùng sổ bằng chứng chung; P7 đã có phần đầu/sáu phụ lục, còn LaTeX, rà soát và bàn giao cuối ở P8–P10.
P2 đã có [bản nháp Chương 3 §3.1–§3.7](thesis/chapters/03_background.md),
từ quan sát/kinh tế đến tín hiệu, HMM, Bayes, MT/utility và PIT/đánh giá,
kèm F01/F02 có source. Chưa rà soát toàn văn cuối hoặc tạo kết quả thực
nghiệm mới. **P3 đã đủ bản nháp [Chương 4 §4.1–§4.10](thesis/chapters/04_proposed_system.md)**:
từ tổng quan/hợp đồng/các agent và Native/Common tới lịch sử/regime, bốn prior,
MT/teacher–student, facts/utility/policy, projection, tám vai trò/ba thuật toán,
ngân sách/phục hồi và ứng dụng. F03/F04/F05/F05a/F06/F07/F08/F11 có nguồn;
EX01 kết thúc bằng outcome sau barrier, giữ net loss và giới hạn causal.
G2 được tự kiểm nội bộ tại sổ bằng chứng; chưa phản biện ngoài/dàn trang cuối.
UI/F11 vẫn PENDING. **P4 và P5 đã đủ bản nháp Chương 5 và Chương 2**, kèm nguồn/bảng/bibliography đã đối soát.
**P6/T54–T58:** P6 đủ bản nháp Chương 1/6 và đối soát lập luận; G3 tự kiểm nội bộ đạt đúng nguồn T36–T58, chưa review ngoài/dàn trang cuối.
**P7/T59–T60:** T59–T60 hoàn tất bản nháp phần đầu: abstract/7 keywords, lời cảm ơn và câu chữ cam đoan đã được tác giả xác nhận, 42 chữ viết tắt/26 dòng ký hiệu; chưa ký và chưa có biểu mẫu chính thức.
**P7/T61–T66:** đã viết Phụ lục A–F và nối tham chiếu trong thân bài; P7 đủ bản nháp, đã được ghép LaTeX ở P8; UI acceptance và yêu cầu chính thức còn mở; không chạy replay/inference mới.
**P8/T67–T72:** Toàn văn đã ghép và chuyển nguồn chính sang LaTeX. Nguồn và QA trong sổ bằng chứng §14; chưa là bản đã duyệt/nộp.
P9/P10 tiếp tục rà soát và đóng gói bàn giao.
Chỉ viết/đối soát nguồn; Native FAIL, whole-system NOT_CERTIFIED và UI/F11 PENDING không đổi.
Bản xem hai
trang bìa có Supervisor căn giữa. Hạn nộp và quy định
trích dẫn/bố cục chính thức chưa được cung cấp. **Trao đổi với người dùng,
kế hoạch, checklist và hướng dẫn quản lý bằng tiếng Việt; toàn bộ nội dung
khóa luận bằng tiếng Anh.** Việc sửa tài liệu này không đổi F11/F12 hoặc phạm vi
nghiệm thu nghiên cứu lịch sử.

Ngày **14/11/2026**, đã nhận khung KLTN và lập [dàn bài Markdown độc lập](thesis/outline.md)
trong `thesis/`: sáu chương, câu hỏi nghiên cứu, phụ lục và ánh xạ mã nguồn/bằng chứng.
Chỉ tham chiếu bố cục mẫu; nội dung xây dựng theo hệ hiện tại. [Ghi nhận phạm vi](week12/README.md#khởi-tạo-dàn-bài-khóa-luận)
tách việc viết KLTN khỏi nghiệm thu UI và thực nghiệm; chưa tạo LaTeX/PDF mới.

Nguồn `paper/` đã được [làm rõ đóng góp và rà liên kết](week12/README.md#làm-rõ-đóng-góp-và-rà-liên-kết-bài-báo):
highlights/abstract mới, bảng indicator, bỏ hình lịch đánh giá cũ; hai PDF vẫn
44 trang/43 references, 42 đích truy cập đã xác nhận và một trang nhà xuất bản
còn yêu cầu xác minh trình duyệt, chi tiết trong báo cáo liên kết hiện hành.

Nguồn bài báo ngày 13/11/2026 đã được [biên tập thành bản độc lập](week12/README.md#biên-tập-bài-báo-độc-lập):
bỏ mã task/giọng phản hồi, caption một câu, toàn bộ bảng/hình `[htb]`, cả hai PDF
44 trang và 43 references; nguồn ở `paper/`, PDF hiện hành ở [outputs/paper](../../outputs/paper/README.md).
Cấu trúc thư mục và cách khôi phục kết quả cũ được ghi tại [checklist dọn dẹp](week12/README.md#sắp-xếp-nguồn-bài-báo-và-kết-quả).
Số liệu, công thức và bằng chứng thực nghiệm giữ nguyên.

Ngày 13/11/2026 đã sửa bố cục và bổ sung references cho nguồn `paper/`:
cả hai PDF 50 trang, 43 tài liệu được dẫn; reference [6] có URL thay thế đã kiểm.
[Checklist và gói bố cục trước](week12/README.md#điều-chỉnh-bố-cục-và-tài-liệu-tham-khảo-của-bài-báo)
ghi phạm vi tài liệu, đối soát số liệu và PDF/ZIP Overleaf mới; bản F05 cùng
crosswalk của nó giữ nguyên làm bằng chứng lịch sử.

**Từ 12/11/2026, `develop` là nhánh tích hợp duy nhất cho toàn bộ công việc:**
hệ gốc, Bayesian/MT-BICL, thực nghiệm, bài báo và phản hồi reviewer.
Task mới tách nhánh từ develop rồi merge trở lại theo AGENTS; `fix` chỉ giữ vai
trò nguồn lịch sử. [Hướng dẫn làm việc chung](week12/develop_workflow.md) xác định
nguồn bài báo, evidence, lệnh kiểm offline và ranh giới tài liệu cũ.
[Checklist W12](week12/README.md#đầu-mối-làm-việc-duy-nhất-trên-develop) là nơi
theo dõi F06–F12 và các yêu cầu khoa học/editorial còn thiếu sau U10; root `plan.md` là lịch sử.

**Kế hoạch thực hiện phần còn lại:** [bài báo và giao diện chọn phiên bản](week12/final_paper_ui_plan.md),
audit ngày 12/11/2026 tại `develop:d16630e9`. Giữ tám section chính và appendix
A–F của bài; đưa phương pháp/kết quả mở rộng chính vào thân bài, chi tiết vào
appendix. F01–F05 cụ thể hóa U10; F06–F12 nâng ứng dụng Flask hiện tại để chọn,
chạy và so sánh phiên bản. [Checklist cuối](week12/README.md#công-việc-cuối-cho-bài-báo-và-giao-diện)
là nơi cập nhật tiến độ. F00–F05 và U10 đã hoàn tất phạm vi bàn giao nội bộ: [mapping và historical restore](week12/final_evidence_map.md)
giữ snapshot 810 nguồn, restore 286 asset và cold replay nguyên byte 15 artifact
U09; [release F02](week12/README.md#f02--generator-và-artifact-bài-báo-u09) có
26 artifact/798 ô có provenance, 16 test và cold render nguyên byte PASS.
[F03](week12/README.md#f03--nội-dung-bản-thảo-hai-nghiên-cứu) đã bổ sung
nội dung tám section/A–F, giữ metadata/cấu trúc và build hai PDF 50 trang,
kiểm trực quan đủ 100 trang PASS. [F04](week12/README.md#f04--sơ-đồ-caption-và-layout-bản-thảo)
đã cập nhật bốn sơ đồ/caption, figure hai baseline và vị trí bảng; hai PDF
51/50 trang, kiểm đủ 101 trang PASS. [F05](week12/README.md#f05--reviewer-locators-và-bàn-giao-bản-thảo-cuối)
ngày 13/11/2026 đã đồng bộ đủ 87 yêu cầu/matrix/response, chốt PDF, source,
companions, locators và manifest; **0/18 comment được chứng nhận đóng**.
F06 ngày 13/11/2026 đã chốt [contract serving riêng](week12/variant_serving_contract.md),
sáu lựa chọn chính/hai nâng cao, preflight và job/config/result identity; 33 test
đúng phạm vi PASS. F07 đã nối reader U09 đã verify với experiments, so sánh
nhiều bản/baseline, chi tiết và export; 46 Python + 6 DOM PASS. UI tách
template/CSS/JS; browser trực quan chờ F11 do host/approval bị chặn. F08 đã có
provider/runner riêng, resource **188 binding/chín mã/58 phiên 01/07–23/09/2026**,
API job owner/preflight/stop/resume, quota/retry/UNKNOWN và paired DAG; **105 test
đúng phạm vi + compile18 PASS**, chỉ HTTP fixture, chưa smoke hosted mới.
F09 đã nối form/kết quả với serving: sáu bản chính/hai dependency, preflight,
so sánh cùng snapshot, raw/final/CASH, context và hai projection Alpha;
**108 Python + 18 DOM, compile5/JS7 PASS**. Template/CSS/JS đã tách file,
giữ đường realtime legacy riêng; UI VI/EN, báo cáo serving vẫn chỉ VI.
Browser desktop/mobile chưa kiểm vì host không khả dụng, giữ trong F11.
F10 đã nối backtest mới và danh mục owner vào experiments, cùng evaluator
account/classification U09, daily NAV/cycle returns, filter/contrast cùng
support và JSON/CSV; Full/No-Alpha legacy có adapter riêng. **156 Python +
31 DOM, compile13/JS7 PASS**, chỉ HTTP fixture; browser visual chờ F11.
**F11 đang làm**: đã nhận develop `4de6d1aa`, sửa prompt Original realtime và
snapshot VNINDEX. Theo yêu cầu mới nhất, form phân tích chạy realtime,
**bỏ hẳn mục Analysis source**, duy nhất **1D**, chọn một trong
sáu bản rồi Phân tích. Đã xóa lựa chọn as-of/daily riêng, so sánh, repeats và
cấu hình serving khỏi form. Original giữ pipeline hiện tại; bản nâng cấp dùng
cùng overlay từng agent rồi mở cùng bố cục kết quả, thêm phần BICL thực tế.
Tiến trình từ checkpoint, decision/policy/context giữ nguyên; không tính lại
hoặc bịa kết quả khi lỗi/UNKNOWN. [Runbook hiện hành](week12/variant_serving_contract.md#form-phân-tích-hiện-hành--realtime-1d).
[Receipt hiện hành](week12/serving_integration_acceptance.json) và
[QA song ngữ hiện hành](week12/serving_bilingual_checks.zip): **135 Python + 24 DOM, compile23/JS2 PASS**.
Đã sửa BICL đứng trước Decision cuối; khôi phục báo cáo Alpha Agent đầy đủ,
hiển thị common Alpha riêng đúng nguồn Decision, format Indicator theo HTML
Original tham chiếu. Tin hiển thị cùng snapshot/cutoff, thiếu metadata là NA.
Sáu layout dùng chung VI/EN và sáng/tối; đổi ngôn ngữ giữ query/job/filter và
cookie. Theo yêu cầu ngày14/11/2026, profile live mới
`live_bilingual_presentation_v1` tạo VI/EN trong cùng invocation Pattern/Trend/
Decision; Indicator/Alpha số học dùng mẫu song ngữ từ kết quả đã tính, không
chạy lại selector. Policy/snapshot canonical vẫn VI; sidecar trình bày riêng,
không sửa artifact nghiên cứu. Hai bản HTML được nhúng sẵn; đổi VI/EN ngay
tại chỗ, không reload/fetch/POST, không gọi dịch hoặc chờ quota Groq. Route
dịch đã ngừng đăng ký. Bản ghi cũ đọc cache hoàn tất đúng owner không cần key;
nếu chưa có tiếng còn lại thì cần phân tích lại một lần. Lượt phân tích đầu
vẫn dùng model và có thể tăng output token, không tăng số call để đổi tiếng.
Theme nhớ lựa chọn hoặc theo hệ điều hành. Các lần sửa dịch trước,21/21 phần
được rà riêng và raw/journal của incident giữ nguyên ở checklist/QA lịch sử.
Các QA cũ giữ nguyên byte làm lịch sử; không chạy toàn suite/cold study hoặc
gọi model/thị trường thật trong lượt sửa UI. Browser host vẫn không khả dụng;
Theo chỉ đạo mới của người dùng ngày14/11/2026, hợp nhất nhánh
`feat/precomputed-bilingual-results` vào `develop`, giữ **UI/F11: PENDING**.
Merge nguồn không phải nghiệm thu browser hoặc hoàn tất F11.
**F12 chưa bắt đầu**, paper/PDF/U09 giữ nguyên. Khung KLTN đã được tiếp nhận;
dàn bài và định hướng viết nằm tại [thesis](../../thesis/README.md).

U06 hoàn tất offline với amendment v2, 102 anchor/ba repeat, 51 selector binding
và student/HMM frozen; U07 đã nghiệm thu paired/recovery offline và nền đã vào
develop. **U08 hoàn tất ngày 12/11/2026**: receipt `PASS_U08_RESEARCH`, đủ
**102 điểm/chín mã, 2.448 forecast, 102 canonical labels**. Cold consumer mới
và gói research đã PASS, giữ 8.035 file journal nguyên byte và đối soát 718
source bindings/runtime đã khóa, 0 inference mới trong lượt nghiệm thu.

[Nghiệm thu và bàn giao U08](week12/README.md#nghiệm-thu-u08) ghi coverage,
raw/usage, reset, nguồn/hash và lệnh kiểm gói. Ledger giữ 1.702 HTTP attempts,
trong đó 15 raw đã nghỉ vẫn tính chi phí và được lưu; không có UNKNOWN active.
[Gói research đã seal](week12/unified_live_research.zip) là đầu vào U09.
**U09 hoàn tất ngày 12/11/2026**: [kết quả và giới hạn](week12/README.md#kết-quả-và-giới-hạn-u09),
[gói bảng/figure](week12/unified_analysis_results.zip) và
[receipt](week12/unified_analysis_acceptance.json) đã PASS. Cold replay15 artifact
nguyên byte,29 test đúng phạm vi, compile8 file; oracle độc lập1.530 account khớp.
Return mean account: native−0,652699%, common−1,024794%, v1−0,698188%,
MT−1,253483%; mọi vai trò research âm. V1 cải thiện so common trong band mô tả,
chưa có bằng chứng vượt native; chỉ sensitivity trên sáu fold đã exposed.
U10 đã xong F01–F05 trong phạm vi bản thảo/bằng chứng nội bộ; reviewer/editor
acceptance, quyền/PID và các nghiên cứu còn thiếu không được suy là hoàn tất. Native row-wise causal vẫn FAIL,
whole-system causal NOT_CERTIFIED;0 API mới hoặc refit trong U09.

Yêu cầu mới: [hợp nhất fix làm hệ gốc và develop làm các mở rộng](week12/fix_develop_integration_plan.md).
Đã hoàn tất phân tích và kế hoạch; [checklist W12](week12/README.md) quản lý U01–U10.
U01 đã khóa inventory/hash hai cây nguồn, imports/callers và bằng chứng;
[kết quả audit](week12/README.md#u01--inventory-nguồn-và-bằng-chứng-đã-khóa) ghi rõ delta nguồn và binding lịch sử.
U02 đã ghép nguồn và PASS kiểm thử đúng phạm vi trên nhánh/worktree riêng;
[checklist chi tiết](week12/README.md#checklist-chi-tiết-u02)
theo dõi contracts/schema/chart, dependencies, evidence và kiểm thử.
U03 đã PASS parity offline trên miền native hợp lệ, replay đủ 204 slot B/AS;
[checklist U03](week12/README.md#checklist-chi-tiết-u03) ghi profile
`original_fix_serving_v1`, delta budget, log và giới hạn nhân quả.
U04 đã có registry tám vai trò, snapshot/records, runner/evaluator và CLI/UI
offline dùng chung; [checklist U04](week12/README.md#checklist-chi-tiết-u04)
ghi 128 test, cold fixture và giới hạn prepared-asset replay.
U05 đã thêm `causal_common_v1`, selector train/validation đã purge và bridge
native/common; [checklist U05](week12/README.md#checklist-chi-tiết-u05) ghi 151 test
và cold replay. Gate này chỉ cho alpha PIT, không nâng native hoặc toàn hệ
thành Zero-Leakage. U07 nghiệm thu phần mềm offline, không nâng gate native/
whole-system causal. Research U08 đã seal với smoke tách biệt; U09 dùng receipt/dataset active
để phân tích paired, giữ nguyên raw đã nghỉ làm bằng chứng chi phí/reset. Trạng thái pilot bên dưới
là bằng chứng giữ nguyên, không phải nghiệm thu hệ thống hợp nhất.

Hệ thống giữ Original và bốn nhóm cải tiến.

| Phiên bản | Vai trò |
| --- | --- |
| Bayesian Prior v1 | Regime retrieval và historical examples |
| Bayesian Prior v2, đại diện C2 | Conditional statistics và readiness |
| Bayesian Prior cải tiến A/B | A_tp_pool và B_semantic |
| MT-BICL | Bucket context, student/teacher, facts, utility và revision policy |

[Kế hoạch hiện hành](week11/historical_reevaluation_plan.md#h07--pilot-ghép-cặp48-điểm-bằng-api-free)
là FREE_PAIRED_PILOT_48 để phục vụ buổi trình bày trong hai ngày. Sáu primary
gồm Original_common, bayesian_v1, C2, A_tp_pool, B_semantic, MT_BICL; giữ
Fact_Anchor dependency. CORE4 ×12 cutoff chung2023–2024 =48 điểm, một repeat,
336 Decision nominal và0–96 vision mới tùy archive hợp lệ; smoke9 lượt riêng.
Bridge fix mặc định OFF, nếu khóa ON trước inference thì thêm48 Decision.
Chỉ Groq Free, chi tiêu0 USD; preflight phải xác minh ngân sách48 giờ.

[Checklist W11](week11/README.md#checklist-đánh-giá-lại) quản lý H01–H09.
H01–H06 của thiết kế cũ đã nghiệm thu dữ liệu, replica đủ ba seed/60 checkpoint,
chọn seed42/step3000, MODEL_GATE_PASS/CPU_REPLAY_MATCH;492 HMM prefix,
84 test offline và55 smoke execution. Các asset/receipt đã hoàn tất được giữ.
Pilot cần audit bank852/reuse upstream, khóa protocol/input/runtime riêng và
kiểm lại phần thay đổi trước release; H03–H06 cũ không tự cấp gate pilot.

Ngày09/11/2026, người dùng hủy H07 đầy đủ34.806 call. Supervisor/child đã
dừng, run_r1/managed_r1 đã xóa; grant thu đầy đủ REVOKED, api=false.
Trước khi xóa có186 node upstream complete và0 forecast grid. Chỉ giữ riêng
ledger tối thiểu103 request/264.449 token đã tính hoặc reserve để cộng quota
còn hiệu lực vào lượt mới. Smoke H06 và model/donor/HMM giữ nguyên.

Pilot đã nghiệm thu P01–P05:48 shared,336 forecast,48 nhãn và cold PASS;
[receipt H07](week11/free_pilot_h07_acceptance.json) khóa evidence trước phân tích.
H08 đã chạy offline và cold consumer PASS; [receipt H08](week11/free_pilot_h08_analysis.json).
Return bình quân tám account: Original−3,690521%; A_tp_pool−2,550858%,
D+1,139663 đpt với band95%[−0,680467;2,959792]; MT−4,414181%, D−0,723660 đpt.
Cả sáu return âm; mọi band D return chứa0, chưa đủ bằng chứng vượt Original.
H09 đã đóng gói và phục hồi cold PASS; trạng thái PILOT_COMPLETE, phạm vi48 điểm.
[Bàn giao và lệnh tái lập](week11/README.md#h09--bàn-giao-pilot48)
cùng [receipt gói bằng chứng](week11/free_pilot_h09_handoff.json) quản lý SHA256.
Không đánh dấu toàn hệ thống hoặc full matrix DONE từ pilot này.
Bayesian dùng bank signal đóng băng2020–2022; MT giữ numeric context của
phương pháp. Query chung dùng donor fix; bank/query khác provenance phải
được audit và báo như giới hạn chuyển giao. Kết luận là historical exploratory
có điều kiện trên shared reports; một repeat không đo variance giữa các lần LLM.
H07 đầy đủ1.020 điểm vẫn CANCELLED. Execution acceptance giữ
PENDING_EXECUTION_DATA và giới hạn vendor series.

## Những phần đã triển khai

- Hệ gốc Indicator/Alpha/Sentiment/Pattern/Trend/Decision cùng backtest.
- Memory Bank và Bayesian Prior có historical signals, provenance, PIT,
  retrieval, feature index, split readiness và BRPP.
- C2, A_tp_pool, B_semantic, các content-mode ablation và retrieval controls.
- MT-BICL có teacher Beta–Bernoulli, student causal, task/scaler/regime,
  bucket context, fact packet, posterior utility4096 draws và policy veto.
- Readiness donor archive, grid, label bridge và kiểm input trước inference.

## Hợp đồng nghiên cứu

LONG vào Open(t+1), ra Close(t+3); SHORT giữ CASH. Phí0,25% và slippage0,10%
cả hai chiều. Nhãn lịch sử dùng compute_round_trip_net_return.
Nến query≤t, tin available≤t và mọi observation phải exit<t.
Upstream một lần/unit/realization, deep-copy tới mọi nhánh.
BRPP≤600 ký tự với K=3, prompt<6.500, API qua retry/checkpoint đã audit.

Model/recipe/prompt/options và IDs được khóa trước inference. Không chọn
winner theo subgroup thuận lợi, không vote/best repeat hoặc đổi model/key
ngầm. Kết quả historical đã exposed mang scope exploratory.
Xác nhận forward có protocol/power/release riêng.

## Tài liệu theo giai đoạn

- [W1](week1/README.md), [W2](week2/README.md), [W3](week3/README.md),
  [W4](week4/README.md), [W5](week5/README.md) quản lý dữ liệu và Bayesian Prior.
- [W6](week6/README.md), [W7](week7/README.md), [W8](week8/README.md),
  [W9](week9/README.md) quản lý cải tiến, development và holdout.
- [W10](week10/README.md) mô tả MT-BICL hiện hành.
- [W11](week11/README.md) quản lý tiến độ áp dụng lại trên dữ liệu chung.
- [W12](week12/README.md) quản lý điều kiện xác nhận và bàn giao.

Mỗi task thực hiện trên nhánh riêng từ develop, kiểm theo phạm vi,
Conventional Commit và hợp nhất sau khi các kiểm tra áp dụng PASS.
