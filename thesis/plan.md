# Kế hoạch chi tiết viết khóa luận

## 1. Mục tiêu và phạm vi hoàn thành

Xây dựng từ đầu một **khóa luận tốt nghiệp hoàn chỉnh bằng tiếng Anh**, giải thích và đánh giá hệ thống hiện tại theo [dàn bài sáu chương](outline.md). Giảng viên chưa biết kho mã phải hiểu toàn bộ phương pháp đề xuất, lần theo được logic của một quyết định và phân biệt kết luận có bằng chứng với giả định hoặc vấn đề còn mở.

Đầu ra gồm bản thảo, phần đầu, tài liệu tham khảo, Phụ lục A–F, hình/bảng có nguồn, dự án LaTeX tự đủ, PDF đã kiểm trực quan và gói bàn giao tái lập. Việc lập kế hoạch chưa hoàn thành bất kỳ task viết nào dưới đây.

Có **84 task nhỏ**, chia thành mười giai đoạn. Phụ thuộc thể hiện điều kiện sẵn sàng về nội dung, không phải lịch ngày cố định. Chưa có hạn nộp được cung cấp. Theo dõi trạng thái từng task tại mục 2.1; thông tin ngoài còn thiếu ở T01 không chặn các phần viết độc lập.

**Quy ước ngôn ngữ:** trao đổi với người dùng, kế hoạch, checklist và hướng dẫn quản lý dùng **tiếng Việt**. Toàn bộ **nội dung khóa luận** dùng **tiếng Anh**, gồm phần đầu, nội dung chương, phụ lục, tiêu đề, chú thích, nhãn hình/bảng và diễn giải khoa học. Dàn bài chương mục giữ tiếng Anh làm khung bản thảo. Giữ nguyên định danh chương trình, tên tài liệu và bằng chứng trích dẫn; đoạn nguồn không phải tiếng Anh cần được giải thích bằng tiếng Anh trong khóa luận và ghi rõ nếu là bản dịch phục vụ trình bày.

## 2. Quản lý công việc và quy ước file

### 2.1. Một nguồn trạng thái công việc

Theo yêu cầu ngày **14/11/2026**, checklist được đặt trực tiếp trong kế hoạch này và là **nguồn trạng thái duy nhất** cho 84 task viết khóa luận. Đặc tả ở mục 5 giữ công việc, phụ thuộc và điều kiện nghiệm thu. [README tuần](../docs/plan/week12/README.md#checklist-viết-khóa-luận) giữ ghi nhận nguồn, cách kiểm và giới hạn; không duy trì checklist thứ hai hoặc tạo receipt cho từng task.

Dùng `TODO` (chưa làm), `IN_PROGRESS` (đang làm), `REVIEW` (đang rà soát), `DONE` (hoàn tất) hoặc `BLOCKED` (thiếu điều kiện) khi cần. Mục được đánh dấu hoàn tất phải có đầu ra và đã kiểm điều kiện nghiệm thu. Với mục đang làm hoặc bị chặn, thêm ghi chú ngắn về file hiện tại hoặc thông tin còn thiếu. Ghi nhận hoàn thành theo mẫu `mã task; file/mục; cách kiểm; giới hạn còn lại`, gộp các task liên quan trong một cập nhật tuần. Chỉ ghi đã hoàn tất phản biện bên ngoài khi thực sự nhận và xử lý phản hồi.

Mỗi task hướng tới một phiên làm việc tập trung. Nếu quá lớn, tách thành các task con có hậu tố chữ, giữ mã cha và điều kiện nghiệm thu. **S** là chỉnh sửa/kiểm tra nhỏ, có giới hạn rõ; **M** là một mục nội dung hoặc một nhóm hình/bằng chứng liên quan. Đây là quy mô tham khảo, không phải cam kết số giờ hay ngày hoàn thành.

#### Chuẩn bị — P1

- [x] T01 — DONE: [hồ sơ yêu cầu](evidence.md#1-thông-tin-tác-giả-và-yêu-cầu-trình-bày), metadata có nguồn, [nội dung bìa](frontmatter.md) và bản xem hai bìa. Hạn nộp/quy định chính thức chưa có, đã ghi rõ; chưa hoàn tất các phần đầu phụ thuộc yêu cầu ngoài.
- [x] T02 — DONE: [dàn bài §A.1–A.5](outline.md#a-research-direction), bốn RQ có so sánh/bằng chứng/giới hạn, bốn loại đóng góp và trách nhiệm sáu chương; [nguồn đối chiếu](evidence.md#2-phạm-vi-nghiên-cứu-và-ranh-giới-luận-điểm).
- [x] T03 — DONE: [kiểm kê hai nghiên cứu](evidence.md#3-kiểm-kê-nguồn-hiện-tại-và-hai-nghiên-cứu-đã-khóa), phiên bản/đường dẫn/hash, support và giới hạn; xác nhận ba module có lớp UI cùng logic snapshot nghiên cứu. Đã kiểm 179 file thành phần, 810 nguồn snapshot, 286 asset và U08/U09; không replay hoặc thu thực nghiệm mới.
- [x] T04 — DONE: [danh sách đọc và khóa trích dẫn](evidence.md#4-danh-sách-đọc-nguồn-gốc-và-quy-ước-khóa-trích-dẫn), 59 nguồn/10 nhóm, 3 đã kiểm theo phạm vi, 5 đã đọc một phần, 51 chưa đọc; giữ riêng ứng viên, ghi chú phiên bản/metadata và ưu tiên. Chưa hoàn tất T48 hoặc bibliography cuối.
- [x] T05 — DONE: [thuật ngữ và ký hiệu](evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt), tên phương pháp/ID, episode/task/query, probability/confidence/utility, support/K và fraction/%/pp/bp; đối chiếu code/schema và đơn vị. Không đổi logic nghiên cứu hoặc đánh dấu phần lý thuyết/phần đầu đã viết xong.
- [x] T06 — DONE: [danh mục có nguồn](evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn), 11 hình/3 thuật toán/9 bảng; từng ID có thông điệp, vị trí, task phụ trách, loại nguồn và đường xuất dự kiến. Đã đối soát nguồn liên quan; chưa tạo sản phẩm hoặc hoàn tất các task vẽ/viết và nghiệm thu UI.
- [x] T07 — DONE: [EX01 và quy tắc chọn tình huống](evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết), FPT cutoff 03/07/2023, u0/r0; nối inputs/context/proposals/policy/outcome bằng nguồn đã khóa. Chọn không dùng outcome, giữ kết quả net âm, hai nguồn regime và fallback; chưa thực hiện các task viết/vẽ hoặc chọn nhóm ca T45.
- [x] T08 — DONE: [khung sáu chương và sổ chung](evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm), tiêu đề khớp dàn bài, mỗi mục ghi rõ nội dung chưa viết; dùng tiếp `evidence.md` với quy ước nối luận điểm/ô bảng tới nguồn. Chưa viết chương, tạo kết quả/hình/bảng hoặc hoàn tất task P2 trở đi.

#### Cơ sở lý thuyết — P2

- [x] T09 — DONE: [§3.1](chapters/03_background.md#31-observations-and-time-indexing), OHLCV/phiên quan sát/cutoff, [e−W,e), t=e−1, entry e và exit e+L−1; 45/600 nến, warm-up và thiếu dữ liệu. [F01](assets/diagrams/F01_trade_timeline.pdf) có nguồn TikZ, đã build/render/kiểm; EX01 và CL001–CL006 có binding trong sổ chung. Chưa hoàn tất T10–T15 hoặc Chương 3.
- [x] T10 — DONE: [§3.2](chapters/03_background.md#32-economic-contract-and-prediction-target), công thức đủ hai chiều phí/slippage, nhãn >0 và zero=DOWN, proposal/action/payoff riêng; ví dụ Illustrative LONG/CASH kiểm bằng oracle. CL007–CL008 có nguồn, không đổi nhãn hoặc kết quả đã khóa.
- [x] T11 — DONE: [§3.3](chapters/03_background.md#33-technical-alpha-and-sentiment-signals), năm chỉ báo trước heuristic; alpha/normalization/IC/selection và sentiment/availability/missingness riêng. CL009–CL011 có nguồn; không gọi vote, IC hoặc confidence là xác suất đã hiệu chuẩn.
- [x] T12 — DONE: [§3.4](chapters/03_background.md#34-hidden-markov-models-for-market-regimes), state/emission/transition, VN-Index features, fit/scaler/mapping/fallback và endpoint posterior. CL012–CL013 tách filtering/smoothing, cutoff model thực dùng và hai nguồn regime EX01; không refit hoặc chứng nhận causal toàn hệ.
- [x] T13 — DONE: [§3.5](chapters/03_background.md#35-bayesian-summaries-of-historical-evidence), Beta–Bernoulli, disjoint background shrinkage, mẫu số/K, credible interval/readiness và hai ví dụ Illustrative. CL014–CL016 kiểm counts/quantiles; không gọi posterior là calibrated query probability hoặc return interval.
- [x] T14 — DONE: [§3.6](chapters/03_background.md#36-multi-task-context-and-utility), prior/target/query, teacher/student/LLM và sign probability/utility riêng; ví dụ Illustrative 80% nhưng U=−0.4%, hai dấu strict Q10/Q90 và anchor. CL017–CL020 có nguồn; không suy lợi ích student riêng từ pipeline gộp.
- [x] T15 — DONE: [§3.7](chapters/03_background.md#37-temporal-validity-and-evaluation-principles), giá/tin/episode/resource/query boundaries, purge/reserved IDs, paired protocol/dependence và metric/support/NA. F02 có TikZ/PDF/PNG đã kiểm; CL021–CL025 có nguồn. P2 có bản nháp Chương 3, chưa hoàn tất phương pháp P3/G2 hoặc rà soát cuối.

#### Hệ thống đề xuất — P3

- [x] T16 — DONE: [§4.1](chapters/04_proposed_system.md#41-system-overview-and-one-decision-walkthrough), mục đích/luồng toàn hệ và mở EX01 trước outcome. F03 có TikZ/PDF/PNG đã kiểm, tách offline/numerical/hosted/policy/evaluation và thứ tự chạy thật; CL026–CL028 có nguồn, chưa nhận hoàn tất các mục phương pháp còn lại.
- [x] T17 — DONE: [§4.2](chapters/04_proposed_system.md#42-input-preparation-and-shared-state), nguồn/cửa sổ/missingness, B02 hợp đồng, state/shared/context riêng và hash EX01. CL029–CL032 có nguồn; bảng hiện nằm trong Markdown, chưa xuất bảng LaTeX hoặc chứng nhận dữ liệu/causal toàn hệ.
- [x] T18 — DONE: [Indicator/Decision §4.3](chapters/04_proposed_system.md#43-the-base-multi-agent-pipeline), priorities/vote/missingness, distillation/caps, base schema và LONG/CASH; CL033–CL037 có nguồn. EX01 count lines bị cap khỏi Indicator prompt fragment, đã ghi rõ thay vì giả toàn summary tới LLM; không sửa runtime/forecast frozen.
- [x] T19 — DONE: [§4.3.2–§4.3.3](chapters/04_proposed_system.md#432-pattern), hai PNG FPT nguyên byte từ U08 và F04 có chú giải ngoài ảnh, PDF/PNG/source đã kiểm. CL038–CL042 giữ Pattern warning/low confidence và Trend widening trái geometry Close-fit; dịch report có nhãn, không coi kiểm format/heuristic là grounding hoặc forecast đúng.
- [x] T20 — DONE: [§4.3.4](chapters/04_proposed_system.md#434-alpha), candidate adaptations, công thức thực thi/normalization/IC/ranking/report và Native/Common riêng. CL043–CL047 khớp source và EX01 selector/projection đã khóa; giữ Native row-wise FAIL, in-sample diagnostics và symmetric Sharpe khác CASH. Không refit, sửa runtime hoặc nhận công thức thích nghi bằng bản gốc.
- [x] T21 — DONE: [§4.3.5](chapters/04_proposed_system.md#435-sentiment), live/component-cache/context FrozenNews riêng, scorer/availability/decay và min3/reliable8. CL048–CL050 giữ EX01 unavailable/null khác zero/neutral; không crawl, chạy scorer hoặc sửa nghiên cứu đã khóa.
- [x] T22 — DONE: [§4.4 và B03 phần foundation](chapters/04_proposed_system.md#44-native-and-common-foundations), delta field/selector/instruction/caps; Native/Common khác Full/Base. CL051–CL054 đối chiếu envelope EX01 và paired code; không nhận bridge là ablation một nguyên nhân hoặc bảng prior đã hoàn tất.
- [x] T23 — DONE: [§4.5.1–§4.5.3](chapters/04_proposed_system.md#451-a-completed-signal-episode), schema/oracle/bull trap, saved JSON và timeline strict maturity; bank852 CORE4 khác context số/fold freeze/reserved102. CL055–CL058 nối manifest/U08, giữ transfer giá bank/query; regime tích hợp viết ở T24.
- [x] T24 — DONE: [§4.5.4](chapters/04_proposed_system.md#454-regime-fitting-and-query-time-assignment), fit/scaler/mapping/quality fallback và query frozen; F05a phân biệt model2022/2020 và scaler4feature MT. CL059–CL063 nối artifact/EX01, giữ CONSOLIDATION khác BULL; không refit hoặc nâng gate toàn hệ.
- [x] T25 — DONE: [§4.6](chapters/04_proposed_system.md#46-bayesian-prior-v1), lọc eligibility trước tổng hợp outcome, score/tie-break, population khác top3, BRPP có chú giải và F05. CL064–CL069 khớp EX01 cùng FB01 no-bank; prefix369/request4556chars, fallback dùng Common cùng repeat; không gán v1 empirical rate là Beta posterior hoặc chạy forecast mới.
- [x] T26 — DONE: [§4.7.1](chapters/04_proposed_system.md#471-c2-disjoint-shrinkage-and-separate-readiness), P/C/B rời nhau, masks/counts, shrinkage/CrI và gate stats/examples riêng. CL070–CL073 khớp EX01 P19/C1/B18; retrieved3 khác visible0, posterior audit không là nội dung prompt đã chạy.
- [x] T27 — DONE: [§4.7.2/B03 phần bốn prior](chapters/04_proposed_system.md#472-alternative-conditional-and-presentation-profiles), AconditionT/P, Bpresentation giữ C2evidence, selector/gate/prefix/fallback rõ. CL074–CL077 kiểm EX01 A14/5, C2/B identical và ba bypass; semantic không embedding, bảng nguồn Markdown chưa xuất CSV/TeX.
- [x] T28 — DONE: [§4.8 mở đầu và §4.8.2](chapters/04_proposed_system.md#482-task-construction), vector/scaler/bucket/63sessiontask/ranking/foldfreeze; F06 và bảng EX01 K3/14rows/queryunlabeled. CL078–CL082 nối fullmembership/hosted preparation, không tạo context hoặc fit mới.
- [x] T29 — DONE: [§4.8.3](chapters/04_proposed_system.md#483-teacher-and-student), teacher/grid/counts, simulator, paired37/271873params/queryloss, optimizer và selection thực dùng. CL083–CL088 nối recipe/10receipts/60assessment/export; seed42-step3000 và psaved EX01, không train/loadweights/forward hoặc gọi resource cũ là release toàn hệ.
- [x] T30 — DONE: [§4.8.1](chapters/04_proposed_system.md#481-fact-packet-and-fact-anchor), facts45bars/3assertions, Commondependency/schema/proof/a0 và invalidanchor branch có nhãn Illustrative. CL089–CL092 nối EX013916chars/NO_NUMERIC_VETO, giữ giới hạn validenum khác prosegrounding; utilitypolicy đầy đủ chờ T31.
- [x] T31 — DONE: [§4.8.4/§4.8.6–§4.8.7](chapters/04_proposed_system.md#484-utility), teacher sign/ bootstrap magnitude, support, strict Q10/Q90 và trace riêng; F07 có nguồn/PDF/PNG đã kiểm. CL093–CL097 nối EX01 giữ LONG; bốn ví dụ chấp nhận/từ chối có nhãn Illustrative, không thêm thực nghiệm.
- [x] T32 — DONE: [§4.8.5](chapters/04_proposed_system.md#485-context-projection), toàn membership khác exemplar, bảng input/schema từng họ, bản dịch prefix EX01 có chú giải. CL098–CL101 kiểm 14→4, 437/4586 ký tự, source card và full-precision policy; không giả prompt C2/A/B đã gửi hoặc can thiệp chưa đo.
- [x] T33 — DONE: [§4.9](chapters/04_proposed_system.md#49-variant-orchestration-and-complete-algorithms), B03 tám vai trò, F08 DAG và A01–A03 có nguồn; cùng u0, dependencies đúng repeat, counterbalance và barrier24. CL102–CL105 kiểm timestamps/parents/UUID của EX01; pseudocode không phải runner mới hoặc replay.
- [x] T34 — DONE: [§4.10.1–§4.10.3](chapters/04_proposed_system.md#4101-prompt-admission-and-bounded-repair), caps/final guard, retry owner, schema repair, lifecycle/UNKNOWN và amendment quota/restart thực tế. CL106–CL110 kiểm source, OP01–OP04, năm raw HTTP EX01 và arithmetic cooldown; không chạy lại crash/recovery hoặc suite.
- [x] T35 — DONE: [§4.10.4–§4.10.5](chapters/04_proposed_system.md#4104-application-workflow-and-interpretation), luồng Realtime1D/F11 schematic và EX01 từ input→raw/policy→outcome sau barrier. CL111–CL116 có binding ứng dụng riêng, receipt UI vẫn PENDING, net loss −0.2647317124% không giấu; P3 đủ bản nháp §4.1–§4.10, G2 tự kiểm nội bộ, chưa phản biện/dàn trang cuối.

#### Thực nghiệm — P4

- [x] T36 — DONE: [§5.1](chapters/05_experiments.md#51-studies-and-evidence-scope), bảng phạm vi hai response collection, units/reuse, queue freeze và receipts/giới hạn. CL117–CL120 có ED01–ED09; kiểm accounting375/2448, timestamps và nguồn khóa, không nhận holdout tiền cứu hoặc ablation chưa chạy.
- [ ] T37 — Mô tả dữ liệu, phân vùng, loại trừ và độ phủ.
- [ ] T38 — Mô tả cấu hình đã khóa và thực thi ghép cặp.
- [ ] T39 — Đặc tả đối chứng và can thiệp thực tế.
- [ ] T40 — Đặc tả chỉ số, cách tổng hợp và quy ước thống kê.
- [ ] T41 — Trình bày kết quả nghiên cứu thành phần.
- [ ] T42 — Trình bày kết quả nghiên cứu ngữ cảnh lịch sử.
- [ ] T43 — Trình bày band chênh lệch và các so sánh bridge.
- [ ] T44 — Phân tích support, fallback và cơ chế policy.
- [ ] T45 — Viết tình huống có truy vết, gồm thiếu support và quyết định sai.
- [ ] T46 — Báo cáo phân tích độ bền và tài nguyên đã thực hiện.
- [ ] T47 — Thảo luận giới hạn, ablation chưa làm và trả lời RQ.

#### Nghiên cứu liên quan — P5

- [ ] T48 — Kiểm nguồn gốc và metadata tài liệu tham khảo.
- [ ] T49 — Tổng quan phân tích kỹ thuật và dự báo định lượng.
- [ ] T50 — Tổng quan LLM/VLM đa agent và phần kế thừa.
- [ ] T51 — Tổng quan regime, ngữ cảnh Bayes và MT-BICL.
- [ ] T52 — Tổng quan phương pháp đánh giá và tái lập.
- [ ] T53 — Tổng hợp bảng so sánh và khoảng trống nghiên cứu.

#### Mở đầu và kết luận — P6

- [ ] T54 — Viết động cơ và phát biểu bài toán.
- [ ] T55 — Viết RQ, giới hạn, đóng góp và bố cục.
- [ ] T56 — Tóm tắt phương pháp và trả lời từng RQ.
- [ ] T57 — Viết hạn chế và hướng phát triển theo ưu tiên.
- [ ] T58 — Đối soát mạch lập luận và thuật ngữ toàn khóa luận.

#### Phần đầu và phụ lục — P7

- [ ] T59 — Viết abstract và keywords.
- [ ] T60 — Hoàn thiện bìa, lời cảm ơn, cam đoan và danh mục.
- [ ] T61 — Viết Phụ lục A: hợp đồng dữ liệu và thời gian.
- [ ] T62 — Viết Phụ lục B: prompt và response.
- [ ] T63 — Viết Phụ lục C: thuật toán và cấu hình.
- [ ] T64 — Viết Phụ lục D: kết quả mở rộng.
- [ ] T65 — Viết Phụ lục E: kiểm tra và audit.
- [ ] T66 — Viết Phụ lục F: tái lập và ứng dụng.

#### Dàn trang — P8

- [ ] T67 — Tạo và biên dịch khung LaTeX sạch.
- [ ] T68 — Chuyển cơ sở lý thuyết và phương pháp đề xuất.
- [ ] T69 — Chuyển kết quả thực nghiệm và hình/bảng khoa học.
- [ ] T70 — Chuyển các chương còn lại, phần đầu và bibliography.
- [ ] T71 — Chuyển phụ lục và các tham chiếu bổ trợ.
- [ ] T72 — Ghép toàn văn, xác định LaTeX là nguồn bản nộp.

#### Rà soát — P9

- [ ] T73 — Đối soát luận điểm khoa học và phạm vi bằng chứng.
- [ ] T74 — Rà khả năng đọc hiểu của người lần đầu tiếp cận.
- [ ] T75 — Biên tập tiếng Anh trong toàn bộ khóa luận.
- [ ] T76 — Kiểm trích dẫn, ghi nguồn, quyền và khai báo cần thiết.
- [ ] T77 — Đối soát công thức, đơn vị, số lượng và cách hiển thị số.
- [ ] T78 — Build sạch, kiểm tham chiếu, số trang và cấu trúc.
- [ ] T79 — Kiểm từng trang render và sửa lỗi bố cục.
- [ ] T80 — Xử lý phản hồi đã nhận và chỉnh sửa cuối.

#### Bàn giao — P10

- [ ] T81 — Khóa và đóng gói nguồn bản thảo tự đủ.
- [ ] T82 — Build từ bản giải nén sạch và xác minh đầu ra.
- [ ] T83 — Bàn giao PDF, nguồn và hướng dẫn tái lập.
- [ ] T84 — Chốt hoàn thành nội bộ và ghi đúng trạng thái bên ngoài.

### 2.2. Cấu trúc đầu ra đề xuất

Ở giai đoạn lập kế hoạch chỉ cần `README.md`, `outline.md` và tài liệu này. Tạo các đầu ra dưới đây khi bắt đầu task tương ứng; đây là đường dẫn dự kiến, không phải xác nhận file đã tồn tại.

```text
thesis/
  README.md
  outline.md
  plan.md
  evidence.md                  # sổ nguồn/luận điểm, tài liệu đọc và hình/bảng chung
  frontmatter.md               # nội dung phần đầu và thông tin bìa
  chapters/
    01_introduction.md
    02_related_work.md
    03_background.md
    04_proposed_system.md
    05_experiments.md
    06_conclusion.md
  appendices/
    A_contracts.md
    B_prompts.md
    C_configuration.md
    D_results.md
    E_verification.md
    F_reproduction.md
  references.bib
  assets/
    diagrams/                  # nguồn sơ đồ có thể sửa và hình xuất
    tables/                    # bảng dẫn xuất có nguồn đối chiếu
    figures/                   # đồ thị và ảnh ứng dụng có nguồn
  latex/
    main.tex
    preamble.tex
    frontmatter/
    chapters/
    appendices/
  release/
    thesis.pdf
    thesis-source.zip
    manifest.json
```

Trong giai đoạn viết, Markdown là nguồn nội dung chính thức. Tại T72, ghi nhận thời điểm chuyển đổi và lấy LaTeX làm nguồn bản nộp; giữ Markdown như bản thảo đã rà soát. Không âm thầm duy trì hai bản đang sửa nhưng khác nhau. `references.bib` và hình/bảng là nguồn dùng chung. Gói LaTeX phải tìm được các tài nguyên bên trong gói, không phụ thuộc mẫu gốc hoặc đường dẫn tuyệt đối trên máy.

Sổ bằng chứng gồm: nguồn/phiên bản/hash và vai trò; ánh xạ luận điểm hoặc ô bảng; ghi chú đọc/trích dẫn; danh mục hình/bảng; thông tin còn thiếu và vấn đề bằng chứng chưa giải quyết. Dẫn tới các artifact đã khóa thay vì sao chép archive lớn vào thư mục khóa luận. Checklist nằm tại mục 2.1 của kế hoạch này; lịch sử hoàn thành gộp và bằng chứng kiểm tra nằm tại `docs/plan/`.

### 2.3. Chính sách thay đổi và kiểm tra

- Tạo nhánh `docs/<chủ-đề-kỹ-thuật>` từ `develop` đã cập nhật; commit và merge sau khi các kiểm tra áp dụng đạt. Commit mô tả nội dung, không chứa mã tiến độ tuần/ngày.
- Sửa Markdown/nội dung: kiểm liên kết, công thức, thuật ngữ, số liệu nguồn và diff; không cần chạy lại compileall, unit, E2E hoặc leakage chỉ vì viết tài liệu.
- Sửa LaTeX: biên dịch tài liệu bị ảnh hưởng, kiểm trích dẫn/tham chiếu, bố cục và PDF cuối; đọc và áp dụng kỹ năng PDF khi thực sự bắt đầu công việc PDF.
- Sửa bộ sinh bảng/đồ thị: kiểm đúng phạm vi với giá trị đã khóa; chỉ biên dịch các file Python thay đổi nếu có. Không biến task viết thành tái cấu trúc runtime ngoài yêu cầu.
- Giữ nguyên dữ liệu, journal, model, receipt và bằng chứng âm đã khóa. Tính toán mới phải có đầu ra dẫn xuất riêng và nguồn rõ ràng, không ghi đè bằng chứng lịch sử.
- Không tự gọi mô hình, thu dữ liệu thị trường, huấn luyện lại hoặc chạy ablation còn thiếu để lấp chỗ trống bản thảo. Ghi rõ thiếu bằng chứng, thu hẹp kết luận hoặc đề xuất task nghiên cứu riêng.

## 3. Yêu cầu giúp người đọc mới hiểu phương pháp

Giả định người đọc có kiến thức học máy bậc đại học nhưng chưa biết kho mã, chữ viết tắt hoặc quy ước giao dịch của hệ thống. Chương phương pháp phải giải thích **toàn bộ hệ thống**, không chỉ phần prior prefix mới hoặc danh sách module Python.

### 3.1. Thứ tự giải thích bắt buộc

1. Mô tả quyết định thực tế bằng một đoạn ngắn: quan sát gì, chọn gì và khi nào biết kết quả.
2. Đưa sơ đồ luồng dữ liệu tổng quan, phân biệt huấn luyện, suy luận, policy và đánh giá.
3. Theo một ví dụ mã cổ phiếu/ngày xuyên suốt, dùng tên bản ghi dễ hiểu trước công thức hoặc ID triển khai.
4. Giới thiệu các agent cơ sở và thông tin mỗi agent đóng góp, bao gồm các phần tính số không gọi LLM.
5. Giải thích Native/Common khác nhau thế nào và vì sao bổ sung ngữ cảnh lịch sử.
6. Đi từ episode đã kết thúc tới truy xuất theo regime, rồi thống kê điều kiện và các prior thay thế.
7. Giới thiệu lần lượt facts, prior/target tasks, teacher/student và utility trước khi trình bày policy MT-BICL đầy đủ.
8. Giải thích điều phối, fallback hợp lệ, lỗi kỹ thuật và phục hồi, rồi đưa giả mã toàn trình.
9. Quay lại ví dụ ban đầu để phân biệt raw proposal, final action và kết quả kinh tế xuất hiện sau đó.

### 3.2. Nội dung phải giải thích cho từng thành phần

Với mỗi thành phần chính, trả lời: **Vì sao cần? Đầu vào là gì? Tại thời điểm đó đã biết những gì? Phép tính hoặc suy luận nào diễn ra? Đầu ra là gì? Thành phần nào dùng đầu ra? Thiếu bằng chứng hoặc lỗi lời gọi thì xử lý thế nào? Phần nào kế thừa, phần nào thay đổi?**

Có bảng hợp đồng ngắn gọn gồm trường/kiểu đầu vào, điều kiện thời gian, trường đầu ra và bên sử dụng. Mỗi công thức đi kèm diễn giải và ví dụ ngắn. Schema đầy đủ, prompt dài và mã triển khai đặt ở phụ lục; thân chương vẫn giữ đủ định nghĩa và quy tắc policy để tự đọc hiểu được.

### 3.3. Câu hỏi kiểm tra mức độ dễ hiểu

Sau Chương 3–4, người đọc phải trả lời được các câu sau mà không mở mã nguồn:

- Vì sao SHORT là CASH trong nghiên cứu này, và khi nào quan sát được giá vào/thoát LONG?
- Mỗi agent được nhìn dữ liệu nào tại cutoff; phần nào xác định, phần nào học offline, phần nào gọi mô hình lúc suy luận?
- Pattern và Trend khác nhau thế nào dù đều nhận biểu đồ?
- Alpha khác sentiment và phát biểu confidence của LLM ra sao?
- Native/Common thay đổi gì, và vì sao Base là một đối chứng khác?
- Khi nào episode đủ điều kiện; regime, similarity, support và `K` khác nhau thế nào?
- Prior tasks, target observations và query trong MT-BICL là gì?
- Teacher/student học hoặc ước lượng gì; tài nguyên nào giữ cố định khi đánh giá?
- Vì sao xác suất nhãn dương cao chưa chắc đem lại utility dương?
- Fact Anchor đóng góp gì, và khi nào policy từ chối đề xuất khác của LLM?
- Vì sao tám vai trò dự báo có thể tạo ít hơn tám lời gọi Decision mới trong một repeat?
- Hành động cuối được chuyển thành lợi nhuận tài khoản thế nào mà không đưa outcome của query ngược vào context?
- Ràng buộc nào đã được kiểm, và vì sao vẫn chưa chứng nhận nhân quả toàn hệ?

T74 dùng bộ câu hỏi này để rà soát nội bộ. Có thể ghi là tự kiểm nội bộ; không ghi là đã được giảng viên phản biện độc lập nếu chưa thực sự diễn ra.

## 4. Các giai đoạn và mốc hoàn thành

| Giai đoạn | Task | Đầu ra chính | Điều kiện kết thúc |
| --- | --- | --- | --- |
| P1. Chuẩn bị | T01–T08 | Yêu cầu, nguồn/bằng chứng, ký hiệu và khung bản thảo | Rõ phạm vi, nguồn truy cập được và yêu cầu bên ngoài còn thiếu. |
| P2. Cơ sở lý thuyết | T09–T15 | Chương 3 | Định nghĩa nhất quán các khái niệm và hợp đồng cần cho phương pháp. |
| P3. Phương pháp đề xuất | T16–T35 | Chương 4, sơ đồ giải thích và thuật toán | Ví dụ xuyên suốt và mô tả thành phần bao phủ toàn hệ thống. |
| P4. Thực nghiệm | T36–T47 | Chương 5 và hình/bảng kết quả | Mỗi số liệu/diễn giải có nguồn và đúng phạm vi nghiên cứu. |
| P5. Nghiên cứu liên quan | T48–T53 | Chương 2 và tài liệu tham khảo | Kiểm nguồn gốc, ghi nhận kế thừa và khoảng trống nghiên cứu. |
| P6. Mạch lập luận | T54–T58 | Chương 1 và 6 | Câu hỏi, đóng góp, phát hiện và giới hạn thống nhất. |
| P7. Phần bổ trợ | T59–T66 | Phần đầu và Phụ lục A–F | Nội dung đầy đủ, được tham chiếu từ thân khóa luận. |
| P8. Dàn trang | T67–T72 | Dự án LaTeX hoàn chỉnh, tự đủ | Biên dịch đủ nội dung, tham khảo và hình/bảng. |
| P9. Rà soát | T73–T80 | Bản dự kiến nộp đã kiểm | Đạt kiểm khoa học, tiếng Anh, trực quan và xử lý phản hồi thực có. |
| P10. Bàn giao | T81–T84 | PDF cuối, gói nguồn và ghi nhận hoàn thành | Tái lập được, có định danh và đã bàn giao; rõ trạng thái nộp bên ngoài. |

**Thứ tự làm:** phần thiết yếu P1 → P2 → P3 → P4 → P6 → P7 → P8 → P9 → P10. Đọc nguồn P5 có thể bắt đầu ngay sau T04 và phục vụ P2/P3; chốt khoảng trống nghiên cứu sau khi hiểu phương pháp thực tế. Thông tin cơ sở đào tạo ở T01 chỉ chặn các quyết định phần đầu/bố cục phụ thuộc nó, không chặn viết kỹ thuật.

## 5. Đặc tả các task

Mã task là định danh quản lý ổn định, không đưa vào thân khóa luận. Phụ thuộc là đầu ra cần có của task trước, không phải yêu cầu xin phép người khác. Mỗi dòng ghi công việc, nơi đặt đầu ra và điều kiện nghiệm thu cụ thể. Các mục/chương/phụ lục được yêu cầu viết dưới đây đều phải được soạn **bằng tiếng Anh**; tiếng Việt trong bảng chỉ dùng để quản lý công việc.

### P1. Chuẩn bị và quản lý nguồn

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T01 / S | — | Ghi cơ sở đào tạo, tác giả/mã sinh viên, ngành, người hướng dẫn, biểu mẫu, quy định trích dẫn/bố cục và hạn nộp thực tế vào phần thông tin của `evidence.md`. Phân biệt quy định đã xác nhận với gợi ý từ mẫu. | Mỗi trường có nguồn hoặc ghi rõ chưa xác định; không bịa danh tính, ngày hoặc phê duyệt. Thông tin ngoài còn thiếu chỉ chặn phần hoàn thiện phụ thuộc nó. |
| T02 / S | — | Rà tên đề tài, RQ1–RQ4, đóng góp và phạm vi sáu chương theo dàn bài và hệ hiện tại. | Mỗi RQ có kiểu so sánh/bằng chứng dự kiến; tách phần kế thừa với nhận định thực nghiệm. |
| T03 / M | T02 | Kiểm kê nguồn hiện tại và hai nghiên cứu thành phần/ngữ cảnh đã khóa trong `evidence.md`: phiên bản, đường dẫn, hash, support và giới hạn. | Mỗi kết quả định lượng dự kiến có artifact truy cập được hoặc ghi rõ thiếu; phân biệt source/runtime lịch sử với mã live. |
| T04 / M | T02 | Lập danh sách đọc nguồn gốc và quy ước khóa trích dẫn; coi bibliography hiện có là danh sách ứng viên. | Nguồn được nhóm theo chủ đề và đánh dấu chưa đọc/đã đọc/đã kiểm; có trong `paper/` chưa đồng nghĩa đã xác minh. |
| T05 / S | T02 | Định nghĩa thuật ngữ tiếng Anh, ký hiệu, ánh xạ tên gọi và quy ước diễn đạt trong `evidence.md`. | Rõ Native/Common/Base, episode/task/query, probability/confidence/utility, phần trăm và điểm phần trăm. |
| T06 / S | T03, T05 | Lập danh mục hình/bảng/thuật toán theo mục 6, kèm thông điệp và nguồn. | Mỗi mục có task phụ trách, chương sử dụng và loại nguồn: đo được, dẫn xuất hoặc minh họa. |
| T07 / M | T03, T05 | Chọn ví dụ xuyên suốt có truy vết và quy tắc chọn trường hợp. Nếu thiếu ví dụ lưu phù hợp, dùng ví dụ giả định có nhãn rõ. | Ghi cutoff, đầu vào hợp lệ, ID nguồn và giới hạn; số minh họa không bị hiểu là kết quả thực nghiệm. |
| T08 / S | T02 | Tạo sáu file bản thảo với tiêu đề từ dàn bài và sổ bằng chứng chung. | Có tiêu đề ổn định; chỗ trống chỉ rõ nội dung còn thiếu, không tạo cảm giác đã có nội dung/kết quả. |

### P2. Cơ sở lý thuyết và mô hình bài toán

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T09 / M | T05, T08 | Viết §3.1: OHLCV, phiên giao dịch, cutoff, cửa sổ, warm-up và ánh xạ chỉ số engine; tạo hình thời gian. | Người đọc xác định được nến cuối nhìn thấy, điểm vào/thoát, không nhầm ngày lịch với phiên quan sát. |
| T10 / M | T03, T09 | Viết §3.2 với công thức kinh tế chính xác, quy tắc nhãn khi return bằng 0 và phép tính LONG/CASH đơn giản. | Công thức/ví dụ khớp hàm chuẩn, đủ hai chiều chi phí; không mô tả CASH là lợi nhuận bán khống. |
| T11 / M | T04, T05, T09 | Viết §3.3 giới thiệu năm chỉ báo, biến đổi/lựa chọn alpha và thông tin sentiment riêng. | Định nghĩa đi trước quy tắc triển khai; thống kê xếp hạng và confidence không được gọi là dự báo đã hiệu chuẩn. |
| T12 / M | T04, T05 | Viết §3.4 về trạng thái/phát xạ/chuyển trạng thái HMM, đặc trưng VN-Index và suy luận tại cuối prefix. | Rõ fit, scaler, diễn giải trạng thái và cutoff; không ngầm sử dụng làm trơn với quan sát tương lai. |
| T13 / M | T04, T05 | Viết §3.5: cập nhật Beta–Bernoulli, counts điều kiện/background, shrinkage và ví dụ posterior có nhãn minh họa. | Định nghĩa ký hiệu/mẫu số; support toàn tập khác `K` hiển thị; diễn giải khoảng đúng giới hạn. |
| T14 / M | T04, T05, T13 | Viết §3.6: tasks, target observations, query, vai trò teacher/student và xác suất so với utility lợi nhuận. | Phân biệt đa tác vụ với đa agent; ví dụ số cho thấy xác suất nhãn và lợi ích kỳ vọng khác nhau. |
| T15 / M | T03, T09, T10 | Viết §3.7: PIT, điều kiện episode đã kết thúc, purge, so sánh ghép cặp, tính phụ thuộc và đơn vị đánh giá. | Nhất quán bất đẳng thức thời gian giá/tin/episode; loại nhãn query; phân biệt cutoff bên ngoài với nhân quả từng hàng. |

### P3. Giải thích toàn bộ hệ thống đề xuất từ nền tảng

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T16 / M | T06, T07, T09, T10 | Viết §4.1 bằng tiếng Anh dễ hiểu; tạo kiến trúc tổng quan và mở đầu ví dụ xuyên suốt. | Sơ đồ tách fit offline, suy luận, policy và đánh giá; nêu mục đích mỗi thành phần trước chi tiết kỹ thuật. |
| T17 / M | T03, T15, T16 | Viết §4.2: nguồn, cửa sổ, snapshot, dữ liệu thiếu và bảng hợp đồng đầu vào/đầu ra. | Mỗi đầu vào có ranh giới thời gian và bên sử dụng; outcome query không vào đường dự báo. |
| T18 / M | T11, T17 | Giải thích Indicator và Decision cơ sở ở §4.3: vote, rút gọn báo cáo, đầu ra có cấu trúc và ánh xạ hành động. | Phân biệt Indicator xác định với suy luận Decision; giải thích thiếu/lỗi mà không đồng nhất confidence với xác suất. |
| T19 / M | T11, T17 | Viết các mục Pattern/Trend, cặp biểu đồ đầu vào có chú thích và ví dụ báo cáo. | Người mới phân biệt dựng biểu đồ, diễn giải VLM và kiểm nhất quán số học; ảnh thực có nguồn. |
| T20 / M | T03, T11, T17 | Viết xử lý Alpha: xây ứng viên, chuẩn hóa, định hướng IC, xếp hạng và báo cáo được chọn. | Nêu tính không nhân quả lịch sử của native và selection trong mẫu; không khẳng định công thức thích nghi tương đương bản gốc. |
| T21 / M | T03, T11, T17 | Viết đầu vào/tổng hợp sentiment, nguồn gốc, thời điểm khả dụng, missingness và cách nối vào báo cáo. | Phân biệt đầu vào live với nghiên cứu đã khóa, dùng ngưỡng đúng profile; thiếu dữ liệu không thành bằng chứng trung tính tự tạo. |
| T22 / M | T18, T20, T21 | Viết §4.4 và bảng phân biệt Native/Common/Base, chỉ rõ upstream giữ nguyên và trường alpha/prompt thay đổi. | Người đọc xác định được can thiệp và vì sao so sánh đó không cô lập một nguyên nhân duy nhất. |
| T23 / M | T10, T15, T17 | Viết cấu trúc episode/bank lịch sử ở §4.5, kèm bản ghi ví dụ và timeline đủ điều kiện. | Giải thích trường dữ liệu, nguồn nhãn và kiểm hợp lệ; signal bank khác ngữ cảnh tác vụ số. |
| T24 / M | T12, T17, T23 | Viết tích hợp fit/suy luận regime ở §4.5 và sơ đồ huấn luyện so với query. | Gán trạng thái, metadata, fallback chất lượng fit và định danh scaler/model khớp đường đã đánh giá. |
| T25 / M | T22, T23, T24 | Viết §4.6: tập hợp lệ, điểm truy xuất/tie-break, ví dụ được chọn và prefix Bayesian v1 có chú giải. | Ví dụ lọc trước khi tổng hợp outcome; nêu rõ `K<=3`, fallback và ID nguồn. |
| T26 / M | T13, T22, T23 | Viết C2 ở §4.7: các tập rời nhau, shrinkage, khoảng và readiness riêng cho thống kê/ví dụ. | Từ diễn giải có thể dựng lại counts; biết khi nào thống kê hoặc ví dụ không khả dụng. |
| T27 / M | T25, T26 | Viết A_tp_pool và B_semantic; hoàn thiện bảng bốn prior. | Rõ khác biệt matching, biểu diễn, support, fallback; không suy có embedding retrieval từ tên phương pháp. |
| T28 / M | T14, T15, T23 | Viết tạo MT task/context ở §4.8, dùng sơ đồ prior tasks, target observations và query. | Định nghĩa membership theo bucket, vector, scaler và điều kiện thời gian; outcome query không thành observation của context. |
| T29 / M | T03, T14, T28 | Viết huấn luyện/suy luận teacher/student: kiến trúc thực dùng, mục tiêu, recipe, lựa chọn và checkpoint đã khóa. | Mỗi chi tiết kiến trúc/huấn luyện truy về triển khai hoặc lock đã đánh giá; không thay bằng model giả định. |
| T30 / M | T17, T22, T28 | Viết facts và Fact Anchor, ví dụ assertion và nhánh anchor không hợp lệ. | Rõ phụ thuộc Common, kiểm hợp lệ, hành động anchor và nguồn; không ngầm có veto kinh tế ở bước này. |
| T31 / M | T13, T28, T29, T30 | Viết ước lượng utility và policy sửa quyết định; tạo cây hành động và ví dụ chấp nhận/từ chối. | Đúng phân vị CASH→LONG/LONG→CASH; phân biệt raw proposal, final action, bypass hợp lệ và lỗi kỹ thuật. |
| T32 / M | T18, T25, T26, T27, T29, T31 | Viết phép chiếu context vào prompt; chú giải trường mỗi họ Decision nhận được. | Rõ thống kê toàn membership so với ví dụ hiển thị; kiểm trần ký tự và schema theo builder thực dùng. |
| T33 / M | T22, T27, T31, T32 | Viết §4.9: DAG tám vai trò và ba thuật toán toàn trình cho context, phương pháp/policy, đánh giá ghép cặp. | Phụ thuộc chạy đúng thứ tự, dùng lại upstream, fallback không tạo call giả, chỉ nối outcome khi dự báo đã lưu bền vững. |
| T34 / M | T17, T32, T33 | Viết kiểm soát vận hành ở §4.10: prompt budget, retry, sửa schema, checkpoint theo giai đoạn, resume và UNKNOWN. | Mô tả vòng đời điểm thành công, thiếu support và bị ngắt; lỗi kỹ thuật không âm thầm thành CASH. |
| T35 / M | T16, T33, T34 | Viết luồng ứng dụng và kết thúc ví dụ từ đầu vào tới hành động rồi outcome. Chỉ thêm ảnh UI có phiên bản khi đã có và đã kiểm. | Hiểu hệ thống dù không có ảnh UI; trạng thái nghiệm thu ứng dụng đúng thực tế, không ngụ ý triển khai có lãi. |

### P4. Thiết kế thực nghiệm, kết quả và thảo luận

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T36 / M | T03, T15, T22, T33 | Viết §5.1 và bảng phạm vi tách bằng chứng nghiên cứu thành phần/ngữ cảnh lịch sử. | Không trộn tên nghiên cứu, cohort, responses, mốc khóa và giới hạn dữ liệu đã quan sát. |
| T37 / M | T03, T17, T23, T36 | Viết §5.2 và bảng dữ liệu/phân vùng/độ phủ, loại trừ, bank và sentiment. | Số lượng, ngày, support theo mã, warm-up và missingness khớp artifact đã lưu. |
| T38 / M | T03, T29, T33, T34, T36 | Viết §5.3: model/runtime, các bước fit, repeats, lịch chạy và thống kê request. | Phân biệt 102 điểm, 51 tài khoản, ba repeat, 2.448 slot, response và HTTP attempt; dùng cấu hình nghiên cứu đã khóa. |
| T39 / M | T22, T27, T33, T36 | Viết §5.4: họ đối chứng, bridge contrasts, đối chứng số và can thiệp thành phần đã hoàn tất. | Mỗi contrast có hai bên và support chung; không lẫn Base/Common hoặc always-LONG/continuous hold. |
| T40 / M | T10, T15, T36, T38, T39 | Viết §5.5 với công thức, thứ tự lấy trung bình, mẫu số, chi phí/exposure và tái lấy mẫu ghép cặp. | Giữ estimator và quy ước chỉ số rủi ro riêng mỗi nghiên cứu; band mô tả không thành ý nghĩa thống kê xác nhận. |
| T41 / M | T03, T37, T39, T40 | Viết §5.6 và dựng lại bảng so sánh chính của nghiên cứu thành phần từ số liệu hiện có. | Mỗi ô có nguồn; diễn giải đúng chiều, độ lớn, đơn vị và support, kể cả kết quả bất lợi. |
| T42 / M | T03, T37, T39, T40 | Viết §5.7 và bảng ngữ cảnh lịch sử cho mọi vai trò cùng đối chứng kinh tế. | Giữ đủ kết quả/support/fallback; bình quân return tài khoản và BA khớp nguồn. |
| T43 / M | T40, T42 | Dựng đồ thị contrast Native/Common và diễn giải, kèm band mô tả đồng thời và bridge. | Đúng họ/chỉ số/đơn vị đã phân tích; không chọn riêng họ đẹp hoặc ghép equity curve từ tài khoản độc lập. |
| T44 / M | T25, T26, T27, T31, T42 | Viết phân tích cơ chế: độ phủ, tuổi/similarity nếu đã lưu, fallback, trùng anchor và can thiệp policy. | Phân biệt chỉ số có ghi với không có; không suy tác động nhân quả riêng của student từ chênh lệch tổng. |
| T45 / M | T07, T35, T41, T42, T44 | Viết nhóm tình huống có truy vết: đủ context, thiếu support, bất đồng/veto và quyết định sai. | Theo quy tắc chọn đã nêu; tách facts/proposals/actions/outcomes và có dự báo sai. |
| T46 / M | T03, T34, T40, T41, T42 | Viết phân tích độ bền và tài nguyên từ các panel/sensitivity đã chạy và usage đã ghi. | Đúng định nghĩa chi phí, độ trễ, usage thiếu; giữ support riêng và giả định thực thi. |
| T47 / M | T36, T41, T43, T44, T45, T46 | Hoàn thiện §5.9 và bảng trả lời RQ; liệt kê ablation chưa làm, nguy cơ ảnh hưởng tính hợp lệ. | Kết luận bị giới hạn rõ bởi native causal FAIL, provenance, return âm, mẫu phụ thuộc và dữ liệu đã exposed. |

### P5. Tổng quan tài liệu và định vị nghiên cứu

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T48 / M | T04 | Đọc/kiểm nguồn gốc, ghi ánh xạ luận điểm–trích dẫn và điền `references.bib`. | Kiểm metadata và đoạn hỗ trợ; không dùng nguồn chưa đọc/chưa xác minh như bằng chứng đã chắc chắn. |
| T49 / M | T11, T48 | Viết §2.1 về phân tích kỹ thuật, alpha và đối chứng định lượng. | Giải thích điểm giống/khác liên quan tới triển khai; tránh chỉ liệt kê phương pháp không có căn cứ. |
| T50 / M | T16, T22, T48 | Viết §2.2 về LLM/VLM đa agent, đặc biệt phần kế thừa QuantAgent. | Rõ phần dùng lại, thích nghi và bổ sung; nhận định tính mới có phạm vi bảo vệ được. |
| T51 / M | T12, T13, T14, T29, T48 | Viết §§2.3–2.5 về regime, ngữ cảnh Bayes và MT-BICL/student–teacher. | Giải thích liên hệ và khác biệt triển khai; không đồng nhất mọi retrieval/few-shot với học Bayes đa tác vụ. |
| T52 / M | T15, T40, T48 | Viết §2.6 về backtest, tính phụ thuộc, ablation, tái lập và kiểm định tiền cứu. | Nguồn hỗ trợ lý do/giới hạn của thiết kế thực tế, không tạo bảo đảm mà thiết kế chưa có. |
| T53 / M | T27, T31, T47, T49, T50, T51, T52 | Viết §2.7 và bảng so sánh/khoảng trống nghiên cứu. | Mọi so sánh có nguồn; khoảng trống gắn với đóng góp đã triển khai, không tuyên bố vượt trội thiếu bằng chứng. |

### P6. Mở đầu, kết luận và tính nhất quán lập luận

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T54 / M | T02, T10, T47, T53 | Viết §§1.1–1.2: động cơ và phát biểu bài toán cho người đọc kỹ thuật nói chung. | Hiểu nhiệm vụ, thông tin sẵn có và mục tiêu đánh giá trước thuật ngữ chuyên sâu. |
| T55 / M | T02, T47, T53, T54 | Viết §§1.3–1.5: RQ, thách thức, giới hạn, đóng góp và bố cục. | Mỗi đóng góp dẫn tới chương/bằng chứng thực có; nêu đúng phần kế thừa và nghiên cứu chưa chạy. |
| T56 / M | T47, T55 | Viết §§6.1–6.2, trả lời tường minh từng câu hỏi nghiên cứu. | Khớp Chương 5; không đưa kết quả mới hoặc kết luận mạnh hơn. |
| T57 / M | T47, T56 | Viết §§6.3–6.4: hạn chế và hướng phát triển theo ưu tiên. | Hướng phát triển xử lý thiếu bằng chứng cụ thể; sửa nhân quả, ablation và tiền cứu vẫn là công việc tương lai riêng. |
| T58 / S | T53, T55, T56, T57 | Đọc chuỗi mở đầu–phương pháp–kết quả–kết luận, sửa chuyển đoạn và định nghĩa lặp. | Tên đề tài, RQ, đóng góp, thuật ngữ và kết luận khớp, không đổi phạm vi thiếu giải thích. |

### P7. Phần đầu và phụ lục

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T59 / M | T47, T55, T56 | Viết abstract và keywords trong `frontmatter.md`, theo giới hạn độ dài đã xác nhận nếu có. | Bài toán, phương pháp, thiết kế, kết quả và giới hạn khớp khóa luận; không bịa lợi ích hoặc kết luận tiền cứu. |
| T60 / M | T01, T05, T58 | Hoàn thiện thông tin bìa, lời cảm ơn, cam đoan, chữ viết tắt và ký hiệu trong `frontmatter.md`. | Thông tin cá nhân/câu chữ bắt buộc đã xác nhận; không sao chép danh tính mẫu, bịa chữ ký hoặc xác nhận chưa nhận. |
| T61 / M | T10, T15, T17, T23 | Viết Phụ lục A: schema gọn, ánh xạ thời gian, nhãn và quy ước thiếu dữ liệu. | Ví dụ/trường schema đúng phiên bản mô tả; tham chiếu từ thân bài tới đúng chi tiết. |
| T62 / M | T18, T25, T27, T30, T32 | Viết Phụ lục B: prompt đại diện, BRPP, schema và response mẫu. | Bỏ bí mật, giữ ID request; bản dịch tiếng Anh ghi rõ phục vụ trình bày, không giả là prompt tiếng Anh đã chạy. |
| T63 / M | T20, T24, T25, T26, T29, T31, T38 | Viết Phụ lục C: công thức, cấu hình, siêu tham số và thiết lập huấn luyện/suy luận. | Mỗi tham số số có nguồn, đúng nghiên cứu/profile; không lấy mặc định thay giá trị quan sát. |
| T64 / M | T41, T42, T43, T44, T46 | Viết Phụ lục D: bảng mở rộng theo mã/fold/repeat và sensitivity. | Tổng/mẫu số khớp bảng chính; tách các nghiên cứu và chỉ số không khả dụng. |
| T65 / M | T03, T15, T34, T47 | Viết Phụ lục E về phạm vi kiểm thử/audit và phản ví dụ giữ lại. | Nêu đúng kiểm tra đã chạy trên nguồn nào; không suy chứng nhận toàn hệ từ test đúng phạm vi. |
| T66 / M | T03, T35, T38, T65 | Viết Phụ lục F: tái lập offline, điều kiện tài nguyên và luồng ứng dụng. | Lệnh trỏ tới artifact đã biết, đúng thư mục chạy; phân biệt replay chỉ số, inference mới và UI còn chờ kiểm. |

### P8. Triển khai LaTeX và ghép tài liệu

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T67 / M | T01, T08 | Dựng khung LaTeX sạch tối thiểu theo quy ước mẫu cần dùng; chỉ để chỗ trống tiếng Anh ở thông tin chưa rõ. Ghi engine/toolchain. | Biên dịch được; bỏ chủ đề/macro/thông tin cá nhân mẫu; liệt kê quy định còn chờ xác nhận. |
| T68 / M | T09, T10, T11, T12, T13, T14, T15, T35, T67 | Chuyển Chương 3–4, công thức và thuật toán sang LaTeX; gắn sơ đồ có thể sửa. | Công thức và ví dụ khớp bản đã rà; mọi ký hiệu, hình/bảng và tham chiếu thuật toán hợp lệ. |
| T69 / M | T47, T64, T67 | Chuyển Chương 5 và bảng/đồ thị, giữ độ chính xác và chú thích nguồn. | Đối chiếu mọi số với nguồn; nhãn hàng/cột, đơn vị phần trăm và ghi chú support đúng sau dàn trang. |
| T70 / M | T53, T58, T59, T60, T67 | Chuyển Chương 1, 2, 6 và phần đầu; nối bibliography và các danh mục tự sinh. | Hiển thị đủ nội dung tiếng Anh; tài liệu tham khảo thống nhất thứ tự/kiểu, không lỗi citation. |
| T71 / M | T61, T62, T63, T64, T65, T66, T67 | Chuyển Phụ lục A–F, nối tham chiếu qua lại và hình/bảng. | Phụ lục rõ, đọc được, có dẫn tới; schema/prompt dài không lấn thân bài hoặc tràn trang. |
| T72 / S | T68, T69, T70, T71 | Ghép toàn văn, ghi thời điểm chuyển nguồn chính thức từ Markdown sang LaTeX trong README. | Có một nguồn bản nộp chính; nội dung xuất hiện đúng một lần, đường dẫn hoạt động không cần thư mục mẫu. |

### P9. Rà khoa học, ngôn ngữ, mức độ dễ hiểu và trực quan

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T73 / M | T72 | Đối soát mọi luận điểm chính, đóng góp, kết quả và kết luận với sổ bằng chứng. | Có nguồn và đúng phạm vi; kết quả âm, thiếu support và thí nghiệm chưa chạy vẫn rõ. |
| T74 / M | T72 | Rà theo góc nhìn người lần đầu đọc bằng mục 3; bổ sung giải thích Chương 3–4 còn thiếu. | Trả lời được toàn bộ câu hỏi từ văn bản; ghi đúng rà nội bộ hay độc lập, không bịa phản hồi người đọc. |
| T75 / M | T72 | Biên tập ngữ pháp tiếng Anh, thuật ngữ, thì, mạch đoạn, caption và chữ viết tắt trong toàn khóa luận. | Tiếng Anh học thuật nhất quán; không còn diễn giải chưa dịch, acronym chưa giải thích, mã task hoặc nhật ký repo trong thân bài. |
| T76 / M | T72, T73 | Kiểm bibliography, trích dẫn, nguồn hình, quyền dữ liệu/phần mềm và khai báo hỗ trợ nếu được yêu cầu. | Citation đầy đủ/phù hợp, nội dung kế thừa ghi nguồn, quyền còn thiếu ảnh hưởng phát hành được nêu; không hứa công khai khi chưa có quyền. |
| T77 / M | T73, T75 | Đối soát độc lập công thức, đơn vị, số lượng, phần trăm, quy ước rủi ro và độ chính xác hình/bảng. | Không sai số học/nhãn/support; làm tròn không đổi diễn giải hoặc âm thầm thay số chính xác của nguồn. |
| T78 / M | T74, T75, T76, T77 | Biên dịch sạch; kiểm log, tham chiếu, số trang, danh mục, bookmark và trích xuất văn bản. | Không thiếu citation/reference/asset, công thức bị cắt hoặc lỗi build chưa giải quyết; cảnh báo đã sửa hoặc kiểm cụ thể. |
| T79 / M | T78 | Render và xem từng trang, gồm bảng, đồ thị, thuật toán, phụ lục; sửa bố cục và kiểm lại trang ảnh hưởng. | Không chữ khó đọc, chồng lấn, lỗi font, hình bị cắt hoặc trang trắng ngoài ý muốn; lượt rà toàn bộ dùng bản build cuối. |
| T80 / M | T79 | Xử lý phản hồi thực nhận từ tác giả/người hướng dẫn; nếu chưa có, ghi rõ chưa phản biện bên ngoài và làm lượt chỉnh nội bộ. | Mỗi góp ý có xử lý/vị trí; phần đổi được kiểm lại phù hợp; không ghi đã phản biện ngoài khi thiếu bằng chứng. |

### P10. Đóng gói tái lập và bàn giao

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T81 / M | T80 | Khóa bản thảo cuối, đóng gói nguồn tự đủ, bibliography, hình/bảng và hướng dẫn build. | Không có credential hoặc raw data riêng tư/dư thừa; quyền tài nguyên rõ; không đường dẫn tuyệt đối hoặc phụ thuộc mẫu chưa theo dõi. |
| T82 / M | T81 | Giải nén vào thư mục sạch, build offline khi được hỗ trợ, đối soát PDF với bản đã rà; ghi toolchain/hash trong một manifest. | Build từ gói thành công, nội dung/trang/hình khớp; nếu timestamp khiến PDF khác byte thì ghi rõ, không tuyên bố đồng nhất byte. |
| T83 / S | T82 | Bàn giao `thesis.pdf`, gói nguồn và hướng dẫn tái lập ngắn; liệt kê phê duyệt/nộp bên ngoài còn chờ. | File tồn tại và khớp manifest; bàn giao không đồng nghĩa người hướng dẫn chấp thuận hoặc đã nộp trường. |
| T84 / S | T83 | Chốt checklist bằng commit nguồn, đường dẫn đầu ra và kiểm tra; chỉ ghi nộp/chấp thuận ngoài khi người dùng cung cấp hoặc cho phép sự kiện đó. | Phân biệt hoàn thành nội bộ với đã nộp/được chấp thuận; kế hoạch không tự cho phép gửi email, upload, ký hoặc nộp. |

## 6. Danh mục hình, bảng và thuật toán cần chuẩn bị

Dùng sơ đồ khái niệm để giải thích, công cụ vẽ đồ thị chuẩn cho hình khoa học. Hình/bảng đưa vào khóa luận phải có nhãn tiếng Anh, cỡ chữ đọc được khi in, caption tự đủ, đơn vị phù hợp và nguồn hoặc nhãn minh họa rõ ràng. ID dưới đây dùng quản lý; số thứ tự cuối do LaTeX sinh.

[Danh mục chi tiết có nguồn](evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn)
mở đủ 23 ID cha bên dưới, gồm thông điệp, vị trí, task phụ trách, loại nguồn
đo được/dẫn xuất/minh họa và đường xuất dự kiến. Trạng thái có nguồn không
đồng nghĩa sản phẩm đã được soạn hoặc kiểm trực quan.

| Hạng mục | Thông điệp chính | Task phụ trách | Vị trí / bằng chứng |
| --- | --- | --- | --- |
| F01. Timeline giao dịch | Thấy gì tại `t`, vào `t+1`, thoát `t+3` | T09–T10 | Chương 3; engine/target contract. |
| F02. Phân vùng thời gian | Train/validation/test và ranh giới maturity/purge | T15, T37 | Chương 3/5; protocol và bản ghi chia tập. |
| F03. Tổng quan hệ thống | Toàn đường chạy, tách huấn luyện/suy luận/policy/đánh giá | T16 | Chương 4; graph, registry, adapters. |
| F04. Biểu đồ đầu vào | Bằng chứng khác nhau của Pattern và Trend | T19 | Chương 4; cặp ảnh lưu hoặc minh họa có nhãn. |
| F05. Episode và truy xuất | Memory hợp lệ → matching/ranking → prefix/fallback | T23–T25 | Chương 4; bank/retriever. |
| F06. Tác vụ MT và huấn luyện | Prior/target/query, teacher, student và suy luận đã khóa | T28–T29 | Chương 4; lock task/model đã đánh giá. |
| F07. Cây policy | Facts, support, anchor, proposal, utility veto và hành động cuối | T30–T31 | Chương 4; trace policy. |
| F08. DAG phụ thuộc | Upstream chung và phụ thuộc theo repeat | T33 | Chương 4; registry/protocol. |
| F09. So sánh chênh lệch | Ước lượng chênh lệch và band mô tả | T43 | Chương 5; artifact phân tích đã khóa. |
| F10. Độ phủ và đổi hành động | Support context thực dùng, fallback/policy | T44 | Chương 5; traces và support. |
| F11. Luồng ứng dụng | Đầu vào người dùng → tiến trình → kết quả có thể diễn giải | T35 | Chương 4/Phụ lục F; ảnh có phiên bản đã kiểm nếu có. |
| A01–A03. Thuật toán | Context PIT; chạy phương pháp/policy; dự báo/đánh giá ghép cặp | T33 | Chương 4; đủ đầu vào/đầu ra và xử lý lỗi/fallback. |
| B01. Ký hiệu | Ký hiệu và đơn vị xuyên suốt | T05, T60 | Phần đầu/Chương 3. |
| B02. Hợp đồng thành phần | Mục đích, đầu vào, thời gian và đầu ra | T17–T22 | Chương 4. |
| B03. So sánh phương pháp | Native/Common và các ngữ cảnh lịch sử | T22, T27, T33 | Chương 4. |
| B04. Dữ liệu/cấu hình | Cohort, phân vùng, bank, missingness, model/runtime | T37–T38 | Chương 5. |
| B05–B06. Kết quả chính | Tách nghiên cứu thành phần và ngữ cảnh | T41–T42 | Chương 5; số chính xác đã khóa. |
| B07. Cơ chế/tình huống | Context, raw proposal, policy và outcome | T44–T45 | Chương 5. |
| B08. So sánh nghiên cứu | Giống/khác có nguồn và khoảng trống | T53 | Chương 2; nguồn gốc đã kiểm. |
| B09. Bảng trả lời RQ | Câu trả lời có bằng chứng và bất định còn lại | T47, T56 | Chương 5/6. |

Không gọi mô hình lại chỉ để có ví dụ đẹp hơn. Dịch chú giải, không đổi danh tính khoa học của đầu vào đã đo. Prompt lưu bằng tiếng Việt phải ghi rõ bản tiếng Anh là bản dịch phục vụ trình bày.

## 7. Các mốc rà soát

Các mốc này quản lý việc viết, không phải bốn gate runtime của hệ thống và không nghiệm thu lại nghiên cứu lịch sử.

| Mốc | Công việc cần có | Điều kiện đạt | Khi chưa đạt |
| --- | --- | --- | --- |
| G1. Sẵn sàng viết có nguồn | T02–T08; ghi vấn đề T01 | Truy cập nguồn được hoặc nêu thiếu; thuật ngữ, phạm vi và ví dụ thống nhất. | Viết phần độc lập; không bịa bằng chứng hoặc thông tin cá nhân. |
| G2. Giải thích phương pháp | T09–T35 | Đủ bản Chương 3/4; hợp đồng, sơ đồ, ví dụ và thuật toán policy khớp. | Bổ sung khái niệm hoặc tách mục quá lớn trước khi kết luận về phương pháp. |
| G3. Lập luận có bằng chứng | T36–T58 | Kết quả, tổng quan, RQ và kết luận khớp; nhận định trong phạm vi nguồn. | Sửa diễn giải/thu hẹp kết luận; nêu nghiên cứu mới tùy chọn riêng. |
| G4. Nguồn hoàn chỉnh | T59–T72 và các mục T01 bắt buộc đã rõ | Đủ phần đầu, chương, tham khảo, phụ lục và biên dịch được. | Giữ danh sách vấn đề; chưa phát hành cuối khi còn danh tính giả định hoặc phần bắt buộc thiếu. |
| G5. Bản dự kiến nộp đã rà | T73–T80 | Đạt khoa học, dễ hiểu, tiếng Anh, ghi nguồn, số liệu và trực quan; đúng trạng thái phản biện ngoài. | Mở lại task và kiểm phụ thuộc bị ảnh hưởng; không chạy lại suite runtime không liên quan. |
| G6. Hoàn thành nội bộ | T81–T84 | Bàn giao PDF/nguồn tự đủ, build sạch và có manifest. | Nêu chính xác còn thiếu gì; đã nộp/chấp thuận cần bằng chứng thực tế riêng. |

## 8. Vướng mắc thường gặp và cách giữ phạm vi

| Vấn đề | Xử lý trong phạm vi viết | Không được suy diễn |
| --- | --- | --- |
| Thiếu tác giả, người hướng dẫn, hạn nộp hoặc bố cục chính thức | Ghi T01, hỏi thông tin cụ thể khi cần, tiếp tục viết kỹ thuật. | Metadata mẫu không phải danh tính người dùng hoặc quy định của trường. |
| Thiếu artifact đã khóa hoặc hash khác | Theo hướng dẫn phục hồi hiện có; giữ expected/actual identity và thu hẹp nhận định thiếu nguồn. | Artifact live cùng tên không phải nguồn tương đương. |
| Ablation có code nhưng chưa chạy | Mô tả khả năng và đưa câu hỏi nhân quả sang hướng phát triển. | Có mã nguồn chưa có nghĩa có kết quả. |
| Kết quả âm hoặc chưa rõ | Báo đúng support và bất định mô tả. | Hoàn thành khóa luận không đòi hỏi chiến lược phải sinh lời. |
| Native vẫn lỗi nhân quả từng hàng | Giải thích lỗi, phạm vi common projection và ảnh hưởng diễn giải. | Qua kiểm cutoff chưa chứng nhận toàn hệ. |
| Chưa nghiệm thu UI/browser | Giải thích kiến trúc, chỉ dùng hình đã kiểm và nêu giới hạn. | Mốc tài liệu không đóng F11 hoặc nghiệm thu ứng dụng. |
| Chưa có phản hồi bên ngoài | Hoàn tất kiểm nội bộ, ghi rõ chưa nhận phản biện ngoài. | Tự kiểm không phải giảng viên chấp thuận. |
| Có kết quả mới khi đang viết | Đánh phiên bản sổ bằng chứng, đánh giá chương/nhận định ảnh hưởng trước khi đưa vào. | Receipt cũ không tự chứng nhận code hoặc dữ liệu mới. |

## 9. Định nghĩa hoàn thành cuối cùng

Khóa luận chỉ **hoàn thành nội bộ** khi mọi phần bắt buộc được viết bằng tiếng Anh; người mới theo được toàn phương pháp; luận điểm và số liệu quan trọng đều truy nguồn được; giữ các giới hạn trọng yếu; trích dẫn, công thức, tham chiếu đúng; PDF cuối đã kiểm từng trang; gói nguồn biên dịch được độc lập với thư mục mẫu. Quy định này áp dụng cho sản phẩm khóa luận, không yêu cầu chuyển kế hoạch, checklist hoặc trao đổi quản lý sang tiếng Anh.

Không che chỗ trống nội dung, thông tin bịa, phần bắt buộc thiếu, lỗi số liệu trọng yếu chưa sửa hoặc tài nguyên phát hành chưa kiểm bằng cách đánh dấu task hoàn tất. Việc nộp ra ngoài, người hướng dẫn đồng ý và cơ sở đào tạo chấp thuận là các trạng thái riêng, chỉ ghi khi có bằng chứng thực tế.
