# Kế hoạch nghiên cứu và triển khai KLTN

Đề tài Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent
LLM Stock Trading in the Vietnamese Stock Market.

## Trạng thái hiện hành

### Kế hoạch finalize hệ thống — cập nhật 18/11/2026

**Trạng thái hiện tại — FIN00–FIN05 hoàn tất trong phạm vi đã ghi; FIN04 theo
xác nhận chủ dữ liệu (`PASS_OWNER_ATTESTED`), FIN05 theo policy tin có NA rõ
lý do; FIN06–FIN17 chưa thực hiện.** Chứng nhận PIT nguồn giá độc lập vẫn chưa
có; amendment FIN04 bên dưới là cơ sở chấp nhận nguồn cho phần tiếp theo.
Mục tiêu là bàn giao một bản hệ thống có định danh và miền hỗ trợ rõ ràng,
đạt các kiểm tra nhân quả dữ liệu, kinh tế, ghép cặp và phục hồi áp dụng,
chạy được qua các điểm vào thực tế, có kết quả đánh giá và tài liệu khớp nguồn.
Lợi nhuận âm hoặc chưa đủ bằng chứng vượt đối chứng tiếp tục được báo cáo theo kết quả đo.

Theo yêu cầu hiện hành, **checklist FIN00–FIN17 ngay tại đây là nguồn tiến độ
finalize duy nhất**. README W12 tiếp tục là nguồn bằng chứng U/F đã ghi nhận;
[thesis/plan.md](../../thesis/plan.md) quản lý các task biên tập/nộp khóa luận.
Các nhận định về đầu mối và trạng thái trong phần lịch sử bên dưới gắn với
mốc được ghi. Task finalize tham chiếu các bằng chứng đó theo đúng phạm vi.

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
- [ ] **FIN06 — Hoàn thiện bank, regime và tài nguyên fit.** Truy nguồn tín
  hiệu/giá/nhãn từng chu kỳ dùng trong bản cuối, xử lý chênh cơ sở giá, kiểm
  strict maturity, train cutoff của HMM/scaler và quy tắc OOD. Nếu cần tái tạo
  bank hoặc refit tài nguyên, có recipe, nhật ký và version mới trước inference
  query. Đạt khi membership/labels/resources được tái dựng và query outcome
  không tác động preparation. Phụ thuộc FIN03–FIN05; nhu cầu API chuẩn bị
  lịch sử được ghi trong FIN09.
- [ ] **FIN07 — Kiểm MT-BICL và toàn đường ngữ cảnh.** Kiểm context prior/target,
  fold freeze, reserved IDs, student/teacher, facts, support và thỏa dụng;
  giữ riêng p_student và teacher utility. Kiểm v1/C2/A/B dùng đúng nguồn,
  cổng và mẫu số; kiểm anchor và Q10/Q90 qua các trường hợp chấp nhận/bypass/
  phủ quyết. Đạt khi thay đổi future/query label không đi vào preparation,
  request hoặc policy trước barrier. Phụ thuộc FIN03–FIN06, ưu tiên offline.
- [ ] **FIN08 — Nối bản sửa vào các điểm vào thực tế.** CLI/backtest/as-of/live
  dùng đúng profile, snapshot, dependency và cache identity mới. Default của
  bản phát hành chuyển sang đường đã sửa sau nghiệm thu; dữ liệu cũ được
  hiển thị đúng profile lịch sử. Trạng thái khoa học của bản mới được dẫn từ
  bằng chứng đã kiểm và đúng miền. Đạt khi không còn caller thuộc bản cuối
  gọi nhầm Alpha cũ, trộn cache hoặc gán receipt cũ cho nguồn mới. Phụ thuộc
  FIN02, FIN03 và FIN07.
- [ ] **FIN09 — Chốt bảng tái sử dụng và ngân sách API.** Đối chiếu từng request
  và dependency với archive, ghi slot dùng lại/chạy mới/bypass và lý do.
  Tính cả gọi chuẩn bị bank, vision, anchor, repeats, smoke, retry và quota
  còn sử dụng; chốt model/options, giới hạn lượt gọi và chi phí/thời gian có
  căn cứ trước thu. Đạt khi số slot/call kiểm được bằng dry-run và mọi lời gọi
  có nhu cầu thực tế. Phụ thuộc FIN01–FIN02; lập dự toán sơ bộ ngay sau FIN02,
  cập nhật theo delta FIN03–FIN08. Batch gọi model chuẩn bị tài nguyên chỉ mở
  sau khi producer đã qua kiểm offline liên quan và nguồn/recipe/ngân sách
  batch được khóa; sau thu tái kiểm task tài nguyên trước FIN10.
- [ ] **FIN10 — Nghiệm thu offline trước thu query.** Khóa code/runtime/resource
  và chạy các kiểm tra trực tiếp bị ảnh hưởng, gồm PIT toàn pipeline,
  economics, paired dependency, prompt/schema, retry/checkpoint, owner/cache,
  stop/resume và UNKNOWN. Cold replay bằng fixture kiểm đường mới. Đạt khi
  mọi kiểm tra áp dụng PASS, source pin khớp và blocker chuẩn bị đã được xử lý.
  Phụ thuộc FIN03–FIN09; sửa mới phải kiểm lại phạm vi ảnh hưởng trước thu tiếp.
- [ ] **FIN11 — Thực thi thu hồi đáp cần thiết.** Dùng protocol và ngân sách
  FIN09 đã khóa cho các slot thực sự cần gọi. Reuse upstream hợp lệ, checkpoint
  mỗi point, lưu raw/usage/epoch và cùng-repeat dependency. Đạt khi planned =
  complete cho miền đã khóa, mọi attempt được đối soát; thiếu/lỗi giữ nguyên
  trạng thái để xử lý. Phụ thuộc FIN10 và phạm vi thực thi/ngân sách có hiệu
  lực. Task có thể hoàn thành bằng audit 0 call nếu toàn bộ response còn hợp lệ.
- [ ] **FIN12 — Đánh giá lại bản sửa.** Tính nhãn, tài khoản và metrics bằng
  engine/evaluator đã kiểm; giữ đủ support, raw/final, bypass, NA và kết quả
  âm. So với hai baseline đúng profile, báo epoch và nguồn các phản hồi reuse.
  Kiểm toán độc lập số học và khôi phục artifact phân tích trong tiến trình
  mới. Đạt khi mọi ô có provenance và số liệu khớp oracle. Phụ thuộc FIN11;
  chỉ tái tạo các phân tích bị ảnh hưởng theo protocol đã chốt.
- [ ] **FIN13 — Chốt nghiệm thu hệ thống trong miền công bố.** Tổng hợp bằng
  chứng FIN03–FIN12 theo từng profile/caller/input. Bản sửa đạt row-wise
  causal và toàn pipeline PIT trong miền đã khóa; integrity, economics,
  pairing và recovery đạt điều kiện tương ứng. Gate chưa có bằng chứng tiếp
  tục chặn đóng task. Receipt ghi source/runtime/data/model/scope; bản ghi
  Native cũ vẫn dẫn đúng phản ví dụ đã lưu. Phụ thuộc FIN10 và FIN12.
- [ ] **FIN14 — Hồi quy ứng dụng trên phần thay đổi.** Kiểm sáu lựa chọn,
  Common/Fact Anchor, input/preflight, tiến trình, lỗi/partial/UNKNOWN,
  raw/final/context, kết quả cũ/mới, VI/EN, theme và export. Kiểm trực quan
  desktop/mobile cho các màn hình bị ảnh hưởng, ghi nhận quan sát thực.
  Đạt khi UI trình bày đúng nguồn/profile/gate và các thao tác vận hành hoạt
  động. Kế thừa nghiệm thu giao diện 17/11 trong phần không bị ảnh hưởng.
  Phụ thuộc FIN08 và FIN13.
- [ ] **FIN15 — Đồng bộ khóa luận, bài báo và tài liệu hệ thống.** Cập nhật
  nguồn tại `thesis/` và `paper/`, hướng dẫn chạy, mô tả phương pháp, bảng/hình,
  limitations và các tài liệu trình bày còn dùng theo đúng release mới.
  Chương kết quả phân biệt study cũ và lần đánh giá
  sửa đổi; số liệu sinh từ nguồn đã khóa. Khóa luận tiếng Anh, quản lý bằng
  tiếng Việt, root README tiếng Anh. Build/render và kiểm phần tài liệu bị
  ảnh hưởng; nối phần bàn giao với P10 của thesis. Phụ thuộc FIN12–FIN14.
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
attempt** khi cap 3. Đây chưa gồm bank preparation, số call phần này chưa biết
cho tới FIN06; không mặc định bằng 0. Chi phí/thời gian/quota còn **chưa xác minh**,
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

### Mốc đã ghi nhận trước kế hoạch finalize

Các trạng thái dưới đây là hồ sơ trước FIN00, dùng để truy vết nguồn và
kế thừa kiểm tra theo phạm vi. Tiến độ công việc finalize cập nhật tại
checklist FIN00–FIN17 ở trên.

**Viết khóa luận, cập nhật ngày 17/11/2026:** thư mục làm việc là `thesis/`.
**P9 bổ sung đã tự rà xong T80a–T80l:** [checklist và đặc tả](../../thesis/plan.md#p95-bổ-sung-theo-rà-soát-bản-60-trang).
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

[Dàn bài tiếng Anh](../../thesis/outline.md) và [kế hoạch chi tiết bằng tiếng Việt](../../thesis/plan.md)
bao phủ từ chuẩn bị đến bàn giao PDF/nguồn cuối qua 84 task. Phần phương pháp
phải giải thích toàn hệ thống cho giảng viên lần đầu tiếp cận.
[Checklist viết khóa luận](../../thesis/plan.md#21-một-nguồn-trạng-thái-công-việc) là nơi duy nhất
cập nhật trạng thái ngay trong kế hoạch theo yêu cầu tác giả. Hồ sơ yêu cầu,
phạm vi nghiên cứu và [kiểm kê hai nghiên cứu](../../thesis/evidence.md#3-kiểm-kê-nguồn-hiện-tại-và-hai-nghiên-cứu-đã-khóa)
đã có; [danh sách đọc](../../thesis/evidence.md#4-danh-sách-đọc-nguồn-gốc-và-quy-ước-khóa-trích-dẫn)
phân nhóm nguồn gốc, trạng thái đọc/kiểm và quy ước khóa trích dẫn.
[Thuật ngữ và ký hiệu](../../thesis/evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt)
thống nhất tên phương pháp, cấp episode/task/query và đơn vị.
[Danh mục hình/bảng/thuật toán](../../thesis/evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn)
giữ 23 ID có task, vị trí, loại nguồn và provenance; sản phẩm sẽ tạo tại task
phụ trách. [Ví dụ xuyên suốt EX01](../../thesis/evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết)
chọn FPT tại cutoff 03/07/2023 theo quy tắc không dùng outcome, nối nguồn
đầu vào/lịch sử/proposal/policy và tách kết quả sau cutoff.
[Khung sáu chương](../../thesis/evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm)
đã đủ bản nháp nội dung tiếng Anh và dùng sổ bằng chứng chung; P7 đã có phần đầu/sáu phụ lục, còn LaTeX, rà soát và bàn giao cuối ở P8–P10.
P2 đã có [bản nháp Chương 3 §3.1–§3.7](../../thesis/chapters/03_background.md),
từ quan sát/kinh tế đến tín hiệu, HMM, Bayes, MT/utility và PIT/đánh giá,
kèm F01/F02 có source. Chưa rà soát toàn văn cuối hoặc tạo kết quả thực
nghiệm mới. **P3 đã đủ bản nháp [Chương 4 §4.1–§4.10](../../thesis/chapters/04_proposed_system.md)**:
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

Ngày **14/11/2026**, đã nhận khung KLTN và lập [dàn bài Markdown độc lập](../../thesis/outline.md)
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
