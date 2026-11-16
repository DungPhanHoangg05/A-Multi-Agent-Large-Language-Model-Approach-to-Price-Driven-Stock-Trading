# Kế hoạch chi tiết viết khóa luận

## 1. Mục tiêu và phạm vi hoàn thành

Xây dựng từ đầu một **khóa luận tốt nghiệp hoàn chỉnh bằng tiếng Anh**, giải thích và đánh giá hệ thống hiện tại theo [dàn bài sáu chương](outline.md). Giảng viên chưa biết kho mã phải hiểu toàn bộ phương pháp đề xuất, lần theo được logic của một quyết định và phân biệt kết luận có bằng chứng với giả định hoặc vấn đề còn mở.

**Yêu cầu hiện hành ngày 16/11/2026:** bản nộp khoảng **60–70 trang, không có phụ lục**, gồm phần đầu, sáu chương, tài liệu tham khảo và hình/bảng cần thiết. Bảng phải đọc được trên trang dọc, không xoay cả trang. Giữ nội dung cốt lõi và giải thích đủ phương pháp cho giảng viên lần đầu tiếp cận hệ thống.

**P9 đang triển khai theo yêu cầu tác giả.** Mốc PDF 259 trang được khóa trong sổ bằng chứng §15; trạng thái từng task ở mục 2.1. Không coi dự toán 66 trang là số trang đã đạt trước khi build.

Có **84 task cha** qua mười giai đoạn; P9 bổ sung **12 task con T73a–T73l** để quản lý đợt rút gọn trước lượt rà soát cuối. T01–T72 ghi nhận lịch sử bản đầu tiên; T61–T66 và T71 đã hoàn thành theo phạm vi cũ, không còn là yêu cầu giữ phụ lục trong bản nộp mới. Phụ thuộc là điều kiện sẵn sàng về nội dung, không phải lịch ngày cố định. Chưa có hạn nộp được cung cấp. Theo dõi trạng thái tại mục 2.1.

**Quy ước ngôn ngữ:** trao đổi với người dùng, kế hoạch, checklist và hướng dẫn quản lý dùng **tiếng Việt**. Toàn bộ **nội dung khóa luận** dùng **tiếng Anh**, gồm phần đầu, nội dung chương, tiêu đề, chú thích, nhãn hình/bảng và diễn giải khoa học. Dàn bài chương mục giữ tiếng Anh làm khung bản thảo. Giữ nguyên định danh chương trình, tên tài liệu và bằng chứng trích dẫn; đoạn nguồn không phải tiếng Anh cần được giải thích bằng tiếng Anh trong khóa luận và ghi rõ nếu là bản dịch phục vụ trình bày.

### 1.1. Ngân sách trang cho bản rút gọn

Quy ước lập kế hoạch: **60–70 là tổng số trang vật lý của PDF**, tính cả hai bìa, phần đầu, danh mục, sáu chương và tài liệu tham khảo; không chỉ tính trang đánh số Ả Rập. Đây là cách tính để triển khai yêu cầu người dùng, chưa phải xác nhận quy định chính thức của trường. Mục tiêu làm việc là **66 trang** để còn khoảng điều chỉnh khi build.

| Phần | Mục tiêu | Khoảng phân bổ | Nội dung ưu tiên |
| --- | ---: | ---: | --- |
| Hai bìa và phần đầu | 10 | 9–10 | Thông tin đã xác nhận; abstract, lời cảm ơn/cam đoan, mục lục và danh mục gọn. |
| 1. Introduction | 3 | 3–4 | Bài toán, RQ1–RQ4, phạm vi và đóng góp có giới hạn. |
| 2. Related Work | 5 | 4–5 | Tổng hợp theo nhóm phương pháp; kế thừa và khoảng trống liên quan trực tiếp. |
| 3. Background and Problem Formulation | 7 | 6–7 | Hợp đồng kinh tế/thời gian, ký hiệu và khái niệm cần để đọc Chương 4. |
| 4. Proposed System | 20 | 19–21 | Toàn luồng hệ thống, prior/regime, MT/teacher/student, facts/utility/policy và EX01. |
| 5. Experiments and Discussion | 15 | 14–16 | Thiết kế, hai nghiên cứu, kết quả chính, support/bypass, bất định và hạn chế. |
| 6. Conclusions and Future Work | 3 | 2–3 | Trả lời RQ, kết luận đúng bằng chứng và hướng phát triển. |
| References | 3 | 3–4 | Nguồn thực sự được trích dẫn và attribution cần thiết. |
| **Tổng** | **66** | **60–70** | **Không có Appendix, kể cả phụ lục đổi tên thành chương bổ sung.** |

Khoảng từng phần đã tính hình/bảng/công thức nằm trong phần đó. Có thể chuyển ngân sách giữa các phần nếu vẫn đạt tổng 60–70 và mục 3; không rút mất lời giải thích phương pháp để nhường chỗ cho bảng kiểm nội bộ. Giữ nền trình bày 12 pt, giãn dòng 1,5 và lề hiện hành trong lúc biên tập; ưu tiên bỏ lặp, gộp luận điểm và chọn bảng, không ép trang bằng chữ quá nhỏ hoặc lề hẹp.

### 1.2. Mốc đối chiếu và nguyên tắc cắt gọn

Khảo sát đọc trực tiếp PDF P8: **259 trang, 30 trang có thuộc tính xoay**, phần đầu 19 trang, sáu chương 175 trang, tài liệu tham khảo 3 trang và phụ lục 62 trang. Chương 4 dài 66 trang, Chương 5 dài 63 trang. Chỉ bỏ phụ lục vẫn còn **197 trang**, nên phải biên tập thân bài và danh mục, không chỉ thay cấu hình bảng.

- Mỗi khái niệm định nghĩa đầy đủ một lần; nơi khác dẫn lại và giải thích phần mới. Chương 3 trình bày nền tảng, Chương 4 trình bày cách triển khai, Chương 5 đánh giá bằng chứng.
- Giữ một ví dụ xuyên suốt EX01 và những tình huống bổ sung thực sự cần để giải thích failure/fallback/policy; không chép lại toàn trace ở nhiều mục.
- Ưu tiên bảng trả lời RQ hoặc giải thích cơ chế. Bỏ bảng lặp, bảng chỉ chứa path/hash/UUID và nhật ký kiểm; các nguồn này vẫn nằm trong kho bằng chứng ngoài bản nộp.
- Giữ cả kết quả âm, hai baseline Native/Common, control, độ phủ, bypass, đơn vị phân tích và bất định. Không chọn riêng hàng thuận lợi để giảm trang.
- Giữ phương pháp tự đủ để người đọc hiểu từ bản PDF; kho bằng chứng dùng truy vết sâu, không thay thế công thức, giả định, quy tắc policy hoặc mô tả thiết kế cần thiết.
- Yêu cầu mới ở mục 1 và P9 thay thế dự toán **65–81 trang riêng sáu chương** và yêu cầu phụ lục trong dàn bài cũ. T73a đã đồng bộ `outline.md` và README; mốc trước biên tập và ánh xạ nằm trong sổ bằng chứng §15.

## 2. Quản lý công việc và quy ước file

### 2.1. Một nguồn trạng thái công việc

Theo yêu cầu ngày **14/11/2026**, checklist được đặt trực tiếp trong kế hoạch này và là **nguồn trạng thái duy nhất** cho 84 task cha và 12 task con rút gọn. Đặc tả ở mục 5 giữ công việc, phụ thuộc và điều kiện nghiệm thu. [README tuần](../docs/plan/week12/README.md#checklist-viết-khóa-luận) giữ ghi nhận nguồn, cách kiểm và giới hạn; không duy trì checklist thứ hai hoặc tạo receipt cho từng task. Các ghi nhận DONE dưới P1–P8 là lịch sử bản đầu tiên, không chứng nhận bản rút gọn đã hoàn thành.

Dùng `TODO` (chưa làm), `IN_PROGRESS` (đang làm), `REVIEW` (đang rà soát), `DONE` (hoàn tất) hoặc `BLOCKED` (thiếu điều kiện) khi cần. Mục được đánh dấu hoàn tất phải có đầu ra và đã kiểm điều kiện nghiệm thu. Với mục đang làm hoặc bị chặn, thêm ghi chú ngắn về file hiện tại hoặc thông tin còn thiếu. Ghi nhận hoàn thành theo mẫu `mã task; file/mục; cách kiểm; giới hạn còn lại`, gộp các task liên quan trong một cập nhật tuần. Chỉ ghi đã hoàn tất phản biện bên ngoài khi thực sự nhận và xử lý phản hồi.

Mỗi task hướng tới một phiên làm việc tập trung. Nếu quá lớn, tách thành các task con có hậu tố chữ, giữ mã cha và điều kiện nghiệm thu. **S** là chỉnh sửa/kiểm tra nhỏ, có giới hạn rõ; **M** là một mục nội dung hoặc một nhóm hình/bằng chứng liên quan. Đây là quy mô tham khảo, không phải cam kết số giờ hay ngày hoàn thành.

#### Chuẩn bị — P1

- [x] T01 — DONE: [hồ sơ yêu cầu](evidence.md#1-thông-tin-tác-giả-và-yêu-cầu-trình-bày), metadata có nguồn, [nội dung bìa](frontmatter.md) và bản xem hai bìa. Hạn nộp/quy định chính thức chưa có, đã ghi rõ; chưa hoàn tất các phần đầu phụ thuộc yêu cầu ngoài.
- [x] T02 — DONE: [dàn bài §A.1–A.5](outline.md#a-research-direction), bốn RQ có so sánh/bằng chứng/giới hạn, bốn loại đóng góp và trách nhiệm sáu chương; [nguồn đối chiếu](evidence.md#2-phạm-vi-nghiên-cứu-và-ranh-giới-luận-điểm).
- [x] T03 — DONE: [kiểm kê hai nghiên cứu](evidence.md#3-kiểm-kê-nguồn-hiện-tại-và-hai-nghiên-cứu-đã-khóa), phiên bản/đường dẫn/hash, support và giới hạn; xác nhận ba module có lớp UI cùng logic snapshot nghiên cứu. Đã kiểm 179 file thành phần, 810 nguồn snapshot, 286 asset và U08/U09; không replay hoặc thu thực nghiệm mới.
- [x] T04 — DONE: [danh sách đọc và khóa trích dẫn](evidence.md#4-danh-sách-đọc-nguồn-gốc-và-quy-ước-khóa-trích-dẫn), tại mốc T04 có 59 nguồn/10 nhóm, 3 đã kiểm theo phạm vi, 5 đã đọc một phần, 51 chưa đọc; giữ riêng ứng viên, ghi chú phiên bản/metadata và ưu tiên. Bibliography và trạng thái đọc được cập nhật riêng tại T48–T53.
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

- [x] T36 — DONE: [§5.1](chapters/05_experiments.md#51-studies-and-evidence-scope), bảng phạm vi hai bộ response, đơn vị/tái dùng, mốc khóa và giới hạn receipt. CL117–CL120/ED01–ED09 kiểm số đếm 375/2.448 và thời điểm; không nhận là holdout tiền cứu hoặc ablation đã chạy.
- [x] T37 — DONE: [§5.2/B04a–b](chapters/05_experiments.md#52-data-and-evaluation-support), lịch 12 ngày/sáu fold, độ phủ chín mã, loại trừ BHN, phân vùng và thiếu sentiment. CL121–CL125 kiểm 25 UP/77 DOWN, 51 tài khoản, 79 điểm thiếu tin, 51 binding/chín selector và 828 chênh lệch giá trị return. Bảng nguồn ở Markdown, chưa dàn trang LaTeX.
- [x] T38 — DONE: [§5.3/B04c–e](chapters/05_experiments.md#53-configuration-and-paired-protocol), runtime/model/options, fit offline, ghép cặp/thứ tự và ledger HTTP. CL126–CL130 kiểm nhiệt độ SDK, output token, 40 lệch thứ tự/chín nhóm khác epoch; U08 có 1.290 reply/1.158 bypass/1.702 HTTP, giữ 15 raw retired. Không coi response là quan sát thị trường độc lập hoặc log cũ là kiểm mới.
- [x] T39 — DONE: [§5.4](chapters/05_experiments.md#54-comparators-and-interventions), chín phương pháp chính thành phần, các panel nhỏ, 23 đối chứng factor/12 kịch bản kinh tế; hai baseline/ba bridge ngữ cảnh. CL131–CL136 kiểm support và ID; LONG theo chu kỳ khác giữ liên tục, ablation deferred chưa có kết quả hoặc phân tách nhân quả student.
- [x] T40 — DONE: [§5.5](chapters/05_experiments.md#55-metrics-and-statistical-analysis), công thức/NA, gộp tài khoản và repeat, NAV/MDD/turnover/exposure và quy ước rủi ro riêng. CL137–CL144 kiểm số học, source và metadata tái lấy mẫu; không sinh lại bootstrap. §5.1–§5.5 đủ bản nháp thiết kế.
- [x] T41 — DONE: [§5.6 và B05a–g](chapters/05_experiments.md#56-component-study-results), kết quả chính, confusion/exposure, mã/block, đối chứng số và hai panel lặp. CL145–CL154 truy từng ô tới ED24/25/28/29/32–37; giữ return âm, NA và Full thua Base/placebo trong panel factorial. Đối soát hash/số/đơn vị/support, không chạy lại nghiên cứu.
- [x] T42 — DONE: [§5.7/B06a–c](chapters/05_experiments.md#57-historical-context-results), đủ tám vai trò/hai đối chứng, kết quả, support, raw/bypass và cả ba repeat. CL155–CL158, ED07/16/38/39; giữ return âm, NA và fallback trong tập chính. Phân biệt trung bình 51 tài khoản với SD giữa các repeat; đã đối soát nguồn, ô và liên kết.
- [x] T43 — DONE: [§5.7.4–§5.7.5](chapters/05_experiments.md#574-paired-contrasts-against-both-baselines), B06d đủ 20 contrast, B06e ba bridge và F09 SVG/PDF/PNG/source. CL159–CL162; đúng baseline Native/Common, đơn vị pp và band mô tả đồng thời. Đã kiểm số và render, không sinh lại bootstrap.
- [x] T44 — DONE: [§5.8.1–§5.8.2](chapters/05_experiments.md#581-historical-support-and-recorded-context), B07a–c/F10; CL163–CL168, ED40. Tách bank/gate/reply/action, tuổi và similarity đã lưu, trường thiếu và Brier trên support khác nhau. MT giữ anchor trong 302/306 slot; phân biệt Q10(U) và quantile của thay đổi utility theo chiều hành động. Đã kiểm nguồn, count và render; không suy hiệu ứng nhân quả riêng của student.
- [x] T45 — DONE: [§5.8.3/B07d–g](chapters/05_experiments.md#583-traceable-cases-selected-by-the-declared-rule), năm nhóm/bốn điểm theo §7.7, với 29/47/5/2/52 ứng viên; CT01–CT30/CL169–CL173. Kiểm hash/shared/request/policy và outcome barrier. Có ca đủ context nhưng lỗ, accept nhưng lỗ, veto bỏ lỡ UP và Native sai; CASH bằng 0 khác net return của candidate LONG.
- [x] T46 — DONE: [§5.8.4–§5.8.6](chapters/05_experiments.md#584-sensitivity-to-support-and-dependence-assumptions), B06f/g đủ 20 contrast sensitivity; B05h–j gồm cohort/strata/12 scenario, B07h gồm usage/thời lượng. CL174–CL180/ED41–47; giữ trường thiếu và mẫu số riêng. Band v1−Common tại L1 chứa 0. Chỉ đọc số/trường đã lưu, không replay/fit/API/bootstrap.
- [x] T47 — DONE: [§5.9/B06h/B09](chapters/05_experiments.md#59-unperformed-ablations-and-threats-to-validity), đủ ablation chưa làm, threats và trả lời RQ1–RQ4; CL181–CL187. Giữ Native FAIL/NOT_CERTIFIED, 828/852 return khác số không phải nhãn đổi, return âm và các giới hạn nguồn/mẫu/thực thi/UI. P4 đủ bản nháp; chưa hoàn tất G3 toàn bộ, phản biện ngoài hoặc dàn trang cuối.

#### Nghiên cứu liên quan — P5

- [x] T48 — DONE: [Bibliography 22 nguồn](references.bib) và [sổ §11.1](evidence.md#111-phạm-vi-đọc-metadata-và-luận-điểm-được-hỗ-trợ), metadata/version/đoạn hỗ trợ/hash bản đọc và giới hạn; CL188. Đối chiếu PDF/nguồn gốc, sửa phân biệt edition và tên tác giả; giữ 62 mục discovery riêng, không giả đã đọc toàn bộ. Kiểm BibTeX và links, không chạy nghiên cứu.
- [x] T49 — DONE: [§2.1](chapters/02_related_work.md#21-technical-analysis-and-quantitative-stock-prediction), tín hiệu kỹ thuật/Alpha101 và khác biệt thích nghi một mã, controls/selection versus assessment. CL189–CL192, R01–R03/R17; không suy công thức gốc hay diagnostic thành hiệu quả giao dịch. Kiểm citation, nguồn, liên kết và phạm vi.
- [x] T50 — DONE: [§2.2](chapters/02_related_work.md#22-llms-vlms-and-multi-agent-financial-systems), QuantAgent paper/code attribution, TradingAgents/FinVision và giới hạn chart/sentiment. CL193–CL197, R04–R10; phân biệt kế thừa, thích nghi, bổ sung; pin đối chiếu khác adopted commit. Không tuyên bố vượt trội hoặc HFT cho study daily.
- [x] T51 — DONE: [§§2.3–2.5](chapters/02_related_work.md#23-market-regime-detection), regime/HMM, ICL/Bayes/retrieval, PFN và MT-BICL; CL198–CL204/R11–R16. Nêu đúng giả định và khác biệt teacher16Beta/query-soft-target/student2block4head của triển khai so với bài gốc; không đồng nhất few-shot với multi-task Bayes hoặc synthetic agreement với hiệu quả thị trường.
- [x] T52 — DONE: [§2.6](chapters/02_related_work.md#26-evaluation-of-trading-systems-using-llms), chronological maturity/purging, pairing/ablation, costs, data snooping, dependent resampling/HAC/Holm và tái lập/tiền cứu. CL205–CL209/R17–R22; giữ giả định, không gọi band hiện tại là xác nhận hoặc nói đã chạy phương pháp chưa làm.
- [x] T53 — DONE: [§2.7/B08a–b](chapters/02_related_work.md#27-research-gap-and-position-of-the-thesis), matrix hệ tài chính và cơ chế context/inference, nguồn cho từng hàng/cột và khoảng trống gắn với tích hợp đã triển khai; CL210–CL213. Không tuyên bố đầu tiên/vượt trội hoặc PIT được chứng nhận; giữ kết quả âm, thiếu ablation và Native FAIL. P5 đủ bản nháp, T54 trở đi còn việc.

#### Mở đầu và kết luận — P6

- [x] T54 — DONE: [§§1.1–1.2](chapters/01_introduction.md#11-context-and-motivation): động cơ, thông tin tại cutoff, proposal/fallback/action và sơ đồ input/output; CL214–CL216/§12.1. Giữ hợp đồng kinh tế và giới hạn nhân quả; không kết quả mới.
- [x] T55 — DONE: [§§1.3–1.5](chapters/01_introduction.md#13-objectives-and-research-questions): bốn RQ nguyên văn outline và evidence map, giới hạn, bốn loại đóng góp có attribution và bố cục sáu chương; CL217–CL220/§12.2. Chương 1 đủ bản nháp; không nâng mức bằng chứng.
- [x] T56 — DONE: [§§6.1–6.2](chapters/06_conclusion.md#61-summary-of-the-approach): phương pháp, bốn câu trả lời RQ và đóng góp cùng mức bằng chứng với B09/Chương 5; CL221–CL226/§12.3. Kiểm lại hash nguồn; không kết quả/LLM/fit/resampling mới.
- [x] T57 — DONE: [§§6.3–6.4](chapters/06_conclusion.md#63-limitations): giới hạn material và năm ưu tiên có bằng chứng cần bổ sung; CL227–CL230/§12.4. Repair/ablation/tiền cứu/execution/UI vẫn là công việc tương lai version riêng, không ghi đè lịch sử.
- [x] T58 — DONE: [§12.5](evidence.md#125-đối-soát-toàn-mạch-và-tự-kiểm-g3): đối soát title/RQ/attribution/đóng góp/kinh tế/temporal/policy/limits, chỉnh chuyển đoạn và định nghĩa lặp; CL231–CL232. P6 đủ bản nháp; G3 tự kiểm nội bộ đạt đúng phạm vi, chưa phản biện ngoài hoặc dàn trang cuối.

#### Phần đầu và phụ lục — P7

- [x] T59 — DONE: [Abstract và keywords](frontmatter.md#abstract) tiếng Anh, đủ bài toán/phương pháp/hai thiết kế/kết quả/giới hạn; CL233–CL236/§13.1. Số khớp Chương 5/6, không gain/tiền cứu; giới hạn từ chính thức chưa có, bìa giữ nguyên.
- [x] T60 — DONE: [Phần đầu](frontmatter.md#acknowledgements) đủ metadata/bìa, lời cảm ơn tối giản và cam đoan đã được tác giả xác nhận giữ nguyên; 42 chữ viết tắt, 26 dòng ký hiệu; CL237–CL241/§13.2–13.3. Chữ ký/ngày ký còn để tác giả điền; không suy xác nhận biểu mẫu chính thức hoặc đã nộp.
- [x] T61 — DONE: [Phụ lục A](archive/p8-source.zip) schema/version và hai JSON nguồn, ánh xạ thời gian/nhãn/missingness có liên kết từ §4.2; CL242–CL245/§13.4. Giữ CORE4 khác chín-query-stock, fraction khác %, causal label không là certificate; không nghiên cứu mới.
- [x] T62 — DONE: [Phụ lục B](archive/p8-source.zip) prompt families, bản dịch trình bày có nhãn, BRPP/schema/response projection và UUID/hash/length thật; nối §4.10.1; CL246–CL249/§13.5. Không giả prompt Anh đã chạy, không lộ secrets hoặc biến schema validity thành trading gain.
- [x] T63 — DONE: [Phụ lục C](archive/p8-source.zip) công thức và bảng cấu hình có source theo nghiên cứu/resource, teacher/student/utility và checkpoint thật; nối §5.3.1; CL250–CL253/§13.6. Giữ hai HMM/scaler, seed42-step3000 khác ensemble/pilot; không fit/inference/utility resampling mới.
- [x] T64 — DONE: [Phụ lục D](archive/p8-source.zip) bảng mở rộng component/context theo mã/fold/repeat, đủ sensitivity/omission cells và12 execution scenarios; nối §§5.6–5.7; CL254–CL258/§13.7. Đối soát102/25/77/51, NA/aggregation/repeat means; không chạy ledger hoặc bootstrap mới.
- [x] T65 — DONE: [Phụ lục E](archive/p8-source.zip) ma trận audit, Native counterexamples thật, source/receipt-bound checks và các gate còn thiếu; nối §5.9.2; CL259–CL262/§13.8. Giữ PASS_DETECTION khác causal FAIL, 828 khác changed labels, UI pending và không chạy suite/replay mới.
- [x] T66 — DONE: [Phụ lục F](archive/p8-source.zip) resource identities, lệnh offline có đúng cwd/flags và luồng fixture/live riêng; nối §§4.10.4/5.1.2; CL263–CL266/§13.9. P7 đủ bản nháp; T67 trở đi còn việc, chưa G4/LaTeX/PDF hoặc UI acceptance; không chạy replay/inference mới.

#### Dàn trang — P8

- [x] T67 — DONE: Khung LaTeX sạch đã biên dịch; [nguồn/QA P8](evidence.md#14-dàn-trang-latex-và-chuyển-nguồn-chính). T67 dựng main/preamble/build guide trong thesis/latex, không dùng macro/chủ đề/danh tính mẫu. Hai bìa dùng nguồn đã chốt nguyên nội dung; render hai trang kiểm trực quan, Supervisor căn giữa và không tràn. LuaHBTeX 1.24.0 (MiKTeX 25.12), Latin Modern, report12pt/A4, lề 2,5cm ngang/3cm trên dưới, giãn1,5; bibliography numeric theo thứ tự hiện tại, chưa là chuẩn trường.
- [x] T68 — DONE: Chương 3–4 đã chuyển LaTeX và gắn sơ đồ; [nguồn/QA P8](evidence.md#14-dàn-trang-latex-và-chuyển-nguồn-chính). T68 chuyển 84 heading, 29 bảng/139 dòng, 28 display equations, ba thuật toán và 10 hình vector nguồn sẵn có. Tên/đơn vị/mẫu số được giữ; tự sinh số chương/section/table/figure, ID nguồn như F01/B03 vẫn dùng để đối chiếu. Công thức BA/MCC tách hai dòng để đọc được, không đổi biểu thức; escape ký tự phần trăm trong công thức, xử lý path/hash dài bằng điểm ngắt hợp lệ. TikZ source và PDF đi cùng trong cây thesis.
- [x] T69 — DONE: Chương 5 và bảng/đồ thị đã chuyển LaTeX; [nguồn/QA P8](evidence.md#14-dàn-trang-latex-và-chuyển-nguồn-chính). T69 chuyển đủ 43 heading, 37 bảng/254 dòng, tám display equations và hai đồ thị F09/F10 vector; giữ source notes/footnotes, NA, hai studies/estimators và family20 contrasts. Mỗi hàng đối chiếu toàn bộ token số với AST bản Markdown đã khóa, display equations khớp sau bỏ layout/escape. Bảng rộng dùng landscape/longtable với header lặp; các caption/list entry sinh tự động còn ID B05/B06/F09 giữ để truy vết.
- [x] T70 — DONE: Chương 1/2/6, phần đầu và bibliography đã nối; [nguồn/QA P8](evidence.md#14-dàn-trang-latex-và-chuyển-nguồn-chính). T70 chuyển ba chương còn lại, phần đầu đã xác nhận,42 abbreviations/26 symbol rows, bibliography22 mục, danh mục nội dung/hình/bảng tự sinh. Bìa chỉ xuất hiện hai trang theo nguồn covers, không chép lại bảng metadata/outer/inner từ Markdown; nhãn quản lý Draft/Writing aids không vào PDF. Lời cảm ơn/cam đoan giữ câu chữ tác giả, nhãn unsigned và trường ký/ngày còn trống. Sơ đồ Mermaid bài toán chuyển TikZ có thể sửa, giữ hướng future prices chỉ tới evaluation.
- [x] T71 — DONE: Sáu phụ lục đã chuyển LaTeX và nối tham chiếu; [nguồn/QA P8](evidence.md#14-dàn-trang-latex-và-chuyển-nguồn-chính). T71 chuyển đủ Appendix A–F,32 bảng/479 dòng dữ liệu, năm display equations, các JSON/schema/prompt/command examples. Tất cả token số trong hàng bảng và biểu thức display khớp nguồn Markdown; không bỏ NA, scenario/omission hoặc các kết quả âm. Longtable lặp header, các bảng D nhiều cột dùng landscape; Verbatim tự ngắt chuỗi dài, không thực thi lệnh mẫu. Các link từ thân bài và giữa phụ lục chuyển thành hyperref nội bộ, không có undefined reference/citation hay glyph thiếu trong build mới nhất.
- [x] T72 — DONE: Toàn văn đã ghép và chuyển nguồn chính sang LaTeX; [nguồn/QA P8](evidence.md#14-dàn-trang-latex-và-chuyển-nguồn-chính). T72 ghép đủ hai bìa, phần đầu, sáu chương, bibliography và sáu phụ lục; PDF P8 có 259 trang. Chuyển nguồn lúc 2026-11-16T13:14:55+07:00 (Asia/Saigon), ghi trong README và source-map.json: nội dung tiếp theo sửa trong LaTeX; 13 bản Markdown nội dung giữ làm bản lưu trữ, không duy trì hai nguồn đang sửa. Kế hoạch/sổ bằng chứng vẫn cập nhật bằng Markdown. G4 chưa nghiệm thu yêu cầu chính thức; P9/P10 và UI acceptance còn mở.

#### Rà soát — P9

**Đợt rút gọn trước rà soát cuối — đang triển khai:**

- [x] T73a — DONE: Khóa mốc và ánh xạ biên tập theo ngân sách 66 trang; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73b — DONE: Rút Chương 1–2 còn 3 và 4 trang; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73c — DONE: Rút nền tảng và hợp đồng Chương 3 còn 6 trang; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73d — DONE: Rút tổng quan, hợp đồng và agent foundations Chương 4; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73e — DONE: Rút memory, regime và các prior nhưng giữ điều kiện hỗ trợ; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73f — DONE: Rút facts, task inference, teacher/student và policy MT; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73g — DONE: Gộp điều phối, recovery, ứng dụng và khép ví dụ FPT; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73h — DONE: Rút thiết kế, cấu hình và metrics Chương 5 còn 4 trang; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73i — DONE: Rút kết quả/thảo luận, giữ đủ family và kết quả bất lợi; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73j — DONE: Rút phần đầu còn 10 trang và kết luận còn 2 trang; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [x] T73k — DONE: Bỏ phụ lục khỏi bản nộp, giữ nguyên nguồn lịch sử ngoài build; [đối soát P9](evidence.md#15-rút-gọn-và-đối-soát-p9).
- [ ] T73l — TODO: Chuyển toàn bộ bảng sang bố cục trang dọc và xử lý khoảng trắng/hình/bảng.

**Rà soát bản đã rút gọn:**

- [ ] T73 — Đối soát luận điểm khoa học, phạm vi bằng chứng và nội dung còn đủ sau T73a–T73l.
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

Cây dưới đây mô tả **đầu ra đích sau rút gọn**, không phải trạng thái hiện tại. LaTeX đã là nguồn chính từ T72. T73k đã bỏ cả thư mục Markdown/LaTeX phụ lục khỏi cây bản nộp; nguồn P8 nguyên byte và hash ở archive ngoài đường build.

```text
thesis/
  README.md
  outline.md
  plan.md
  evidence.md                  # sổ nguồn/luận điểm, tài liệu đọc và hình/bảng chung
  frontmatter.md               # bản nháp lịch sử, không dùng build
  chapters/
    01_introduction.md
    02_related_work.md
    03_background.md
    04_proposed_system.md
    05_experiments.md
    06_conclusion.md
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
  release/
    thesis.pdf
    thesis-source.zip
    manifest.json
```

Trước T72, Markdown là nguồn nội dung chính thức; **hiện tại chỉ biên tập bản nộp trong LaTeX**, không sinh lại từ các bản Markdown chương/phần đầu đã lưu trữ. Kế hoạch và sổ bằng chứng vẫn dùng Markdown. T73k phải xử lý minh bạch các bản phụ lục lịch sử, hash và liên kết trước khi xóa nguồn phụ lục; không sửa hash mốc chuyển để che thay đổi. `references.bib` và hình/bảng là nguồn dùng chung. Gói LaTeX phải tìm được tài nguyên bên trong gói, không phụ thuộc mẫu gốc hoặc đường dẫn tuyệt đối trên máy.

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

Có bảng hợp đồng ngắn gọn gồm trường/kiểu đầu vào, điều kiện thời gian, trường đầu ra và bên sử dụng. Mỗi công thức đi kèm diễn giải; dùng EX01 để minh họa nhiều bước thay vì lặp nhiều ví dụ. Thân chương giữ đủ định nghĩa, schema thiết yếu và quy tắc policy để tự đọc hiểu được. Schema đầy đủ, prompt dài, hash/UUID và mã triển khai được dẫn tới nguồn bằng chứng trong repository, **không tạo phụ lục thay thế**. Phần thiết yếu của phụ lục cũ được chuyển theo bảng ở P9.

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
| P7. Phần bổ trợ (lịch sử bản đầu) | T59–T66 | Phần đầu và Phụ lục A–F đã viết | T61–T66 giữ lịch sử; nội dung phụ lục sẽ được chọn lọc rồi bỏ khỏi bản nộp ở P9. |
| P8. Dàn trang | T67–T72 | Dự án LaTeX hoàn chỉnh, tự đủ | Biên dịch đủ nội dung, tham khảo và hình/bảng. |
| P9. Rút gọn và rà soát | T73a–T73l, T73–T80 | Bản 60–70 trang, không phụ lục, toàn trang dọc | Đạt kiểm khoa học, dễ hiểu, tiếng Anh, số liệu, trực quan và phản hồi thực có. |
| P10. Bàn giao | T81–T84 | PDF cuối, gói nguồn và ghi nhận hoàn thành | Tái lập được, có định danh và đã bàn giao; rõ trạng thái nộp bên ngoài. |

**Thứ tự còn lại:** P8 đã có bản đầu → T73a lập ánh xạ → T73b–T73j biên tập theo phụ thuộc → T73k bỏ phụ lục → T73l hoàn thiện bố cục → T73–T80 rà soát → P10 bàn giao. Thông tin cơ sở đào tạo ở T01 chỉ chặn các quyết định thực sự phụ thuộc nó.

## 5. Đặc tả các task

Mã task là định danh quản lý ổn định, không đưa vào thân khóa luận. Phụ thuộc là đầu ra cần có của task trước, không phải yêu cầu xin phép người khác. Mỗi dòng ghi công việc, nơi đặt đầu ra và điều kiện nghiệm thu. **P1–P8 là đặc tả lịch sử đã dùng để tạo bản đầu; yêu cầu viết phụ lục ở T61–T66/T71 đã được thay thế bởi P9**, không thực hiện lại. Nội dung bản nộp tiếp tục dùng tiếng Anh; tiếng Việt trong bảng chỉ dùng quản lý công việc.

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

### P9. Rút gọn xuống 60–70 trang và rà soát bản nộp

#### P9.1. Các task biên tập cần thực hiện

Tất cả task dưới đây còn **TODO**. Đầu ra sẽ nằm trong `latex/chapters/`, `latex/frontmatter/`, cấu trúc build và tài liệu quản lý liên quan; không viết lại các bản Markdown chương đã lưu trữ. Ngân sách ở mục 1.1 là cho bản PDF cuối, không phải số trang bảo đảm trước khi biên dịch.

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T73a / M | T72 | Ghi commit/hash nguồn và PDF trước biên tập; lập bảng ánh xạ mục/hình/bảng theo quyết định giữ, gộp, rút hoặc bỏ khỏi PDF trong sổ bằng chứng chung. Đồng bộ `outline.md` và README với ngân sách mới, không phụ lục. | Mọi mục cốt lõi có nơi đến; phân biệt tài liệu bản nộp với bằng chứng lưu trữ; dự toán tổng 66 trang và khoảng 60–70 thay thế ngân sách cũ. Không tạo receipt riêng cho từng task. |
| T73b / M | T73a | Biên tập Chương 1 còn 3–4 trang và Chương 2 còn 4–5 trang. Gộp động cơ/đóng góp lặp; tổng hợp nghiên cứu theo vấn đề thay vì mô tả dài từng bài; chỉ giữ bảng so sánh giúp định vị đề tài. | Còn đầy đủ RQ1–RQ4, phạm vi, attribution và khoảng trống có nguồn. Không bỏ nguồn cần thiết hoặc cường điệu tính mới để rút văn bản. |
| T73c / M | T73a | Biên tập Chương 3 còn 6–7 trang. Giữ ký hiệu cần dùng, timeline, công thức net return, nền tảng HMM/Beta–Bernoulli/MT/utility và nguyên tắc PIT/paired. Chuyển chi tiết cấu hình sang đúng mục Chương 4–5. | Một định nghĩa chuẩn cho mỗi khái niệm; không lặp nguyên phần triển khai; SHORT=CASH, phí hai chiều, `exit_date < as_of_date` và nhãn zero=DOWN không đổi. |
| T73d / M | T73a, T73c | Biên tập phần tổng quan/dữ liệu/các agent/Native–Common của Chương 4, dự toán khoảng 5 trang trong ngân sách chương. Giữ F03, giải thích Pattern khác Trend và bảng hợp đồng ngắn; gộp cấu trúc lặp của các agent. | Người mới theo được input → báo cáo → Decision, biết thành phần xác định/học offline/gọi LLM; phân biệt Full/Base với Native/Common và giới hạn causality. |
| T73e / M | T73d | Biên tập memory, regime, v1, C2/A/B, dự toán khoảng 5 trang. Giữ điều kiện maturity, fit/fallback regime, similarity/ranking, thống kê population khác top-K, disjoint shrinkage và readiness/bypass. | Có công thức và đầu vào/đầu ra đủ tái hiểu phương pháp; không gọi v1 là Beta posterior, không nhầm B_semantic với embedding hoặc gộp hai nguồn regime. |
| T73f / M | T73d, T73e | Biên tập facts, numerical tasks, teacher/student, training/selection và utility/policy, dự toán khoảng 7 trang. Giữ sơ đồ task/training và policy nếu không trùng thông điệp; gom cấu hình thiết yếu vào bảng nhỏ. | Rõ prior/target/query, nguồn nhãn, frozen resources, teacher mixture, student representation/loss/selection, support và dấu strict Q10/Q90. Phân biệt student với hosted LLM, giữ anchor với chấp nhận thay đổi, xác suất với utility. |
| T73g / M | T73d, T73e, T73f | Biên tập điều phối, prompt/retry/checkpoint, ứng dụng/tái lập và kết thúc EX01, dự toán khoảng 3 trang. Gộp giả mã lặp thành một luồng tổng quát; chuyển phần thiết yếu của A/B/C/F vào đúng vị trí. | Tổng Chương 4 hướng 20 trang và còn trả lời đủ mục 3; paired upstream chạy một lần, outcome barrier, fallback khác failure và giới hạn prompt còn rõ. EX01 giữ cả kết quả lỗ sau phí và trạng thái UI chưa nghiệm thu. |
| T73h / M | T73a, T73g | Rút phần thiết kế/cấu hình/metrics của Chương 5, dự toán khoảng 4 trang. Gộp bảng cohort, partition, coverage và cấu hình quan trọng; giữ khác biệt hai nghiên cứu và tài nguyên huấn luyện/đánh giá. | Rõ 102 points, 51 accounts, 25 UP/77 DOWN, sáu fold, ba Decision repeats; 2.448 slots không phải quan sát độc lập. Mỗi estimator, baseline, uncertainty family và đơn vị được định nghĩa đủ. |
| T73i / M | T73h | Rút kết quả/thảo luận/limitations Chương 5, dự toán khoảng 11 trang. Giữ hai bảng kết quả chính riêng; trình bày gọn đủ family 20 contrast qua bảng hẹp theo baseline/endpoint hoặc hình cộng diễn giải. Gộp support/bypass/action bridge và tình huống điển hình; chọn kết luận sensitivity từ artifact đã có. | Không bỏ adverse outcomes, control, NA hoặc fallback để làm đẹp kết quả. Giữ uncertainty, scope, sample support; giữ 302/306 MT–anchor agreement, kết quả baseline-dependent, Native FAIL/NOT_CERTIFIED và ablation chưa chạy. Bảng chi tiết theo stock/fold/repeat chỉ bỏ khỏi PDF sau khi giữ nguồn truy vết. |
| T73j / M | T73b, T73g, T73i | Rút Chương 6 còn 2–3 trang; phần đầu còn 9–10 trang tính cả hai bìa. Trả lời RQ bằng đoạn ngắn; gộp quy ước đọc và ký hiệu trùng; rút abstract theo kết quả còn giữ. | Hai bìa và câu chữ đã xác nhận không bị thay danh tính; không bịa chữ ký. Abstract/kết luận không thêm kết quả mới; danh mục tự sinh, không bỏ định nghĩa cần để đọc phương pháp. |
| T73k / M | T73g, T73i, T73j | Áp dụng bảng chuyển phụ lục ở P9.2; bỏ `\appendix`, mọi input phụ lục và nguồn phụ lục khỏi cây bản nộp/gói build. Xử lý bản Markdown phụ lục lịch sử qua Git/archive nguyên byte, cập nhật link và kiểm tra source-map nếu cần. | Không còn Appendix trong PDF/TOC/bookmark hoặc tham chiếu treo. Nội dung thiết yếu đã có trong sáu chương. Giữ lịch sử nguồn/hash, không sửa receipt để che việc xóa; gói nộp không chứa phụ lục hay yêu cầu phục hồi phụ lục để build. |
| T73l / M | T73b–T73k | Áp dụng quy tắc bảng dọc P9.3; chuyển/split/gộp bảng, bỏ môi trường xoay, điều chỉnh float, caption và khoảng trắng; phân bổ lại hình chỉ khi cần cho lập luận. | Mọi trang là portrait và rotation=0; không bảng ngang nằm một mình trên trang bị xoay. Không ép fit bằng chữ quá nhỏ; mọi ô/caption đọc được, tổng trang hướng 60–70. Việc xác nhận bản build cuối thuộc T78–T79. |

Các task T73d–T73g chia **20 trang Chương 4**, T73h–T73i chia **15 trang Chương 5**, đã gồm hình/bảng. Đây là phân bổ tham khảo để ưu tiên nội dung; không chèn ngắt trang hoặc kéo dài văn bản để khớp từng số máy móc. Có thể kiểm build cục bộ khi biên tập để phát hiện vượt ngân sách, nhưng chỉ T78–T79 xác nhận PDF cuối.

#### P9.2. Xử lý nội dung phụ lục trước khi xóa

Không chuyển nguyên cả phụ lục lên thân bài. Chỉ giữ phần trực tiếp cần để hiểu phương pháp, diễn giải kết quả hoặc nhận diện hạn chế; chi tiết kiểm toán vẫn được bảo toàn trong kho bằng chứng ngoài bản nộp.

| Phụ lục cũ | Nội dung thiết yếu chuyển vào thân bài | Nội dung bỏ khỏi PDF, giữ nguồn trong repository | Task |
| --- | --- | --- | --- |
| A. Data and Temporal Contracts | Chương 3: timing/nhãn/PIT; Chương 4: schema tối thiểu và missingness/consumer. | JSON đầy đủ, bảng trường lặp, path/hash và bản ghi nguyên văn. | T73c, T73d, T73g, T73k |
| B. Prompts and Responses | Chương 4: cấu trúc request/response, BRPP/facts, validation/fallback và một trích đoạn ngắn nếu thật sự giúp hiểu EX01. | Toàn văn prompt/response, bảng UUID và trace dài. Bản dịch trình bày vẫn phải có nhãn nếu sử dụng. | T73e–T73g, T73k |
| C. Algorithms and Configurations | Chương 4: tham số quyết định thuật toán/teacher/student/policy; Chương 5: cấu hình thực nghiệm và resource selection thực dùng. | Dump cấu hình, inventory và bảng mặc định không liên quan trực tiếp. | T73e–T73h, T73k |
| D. Extended Results | Chương 5: kết quả chính, đủ 20 contrast trong family đã công bố, sensitivity quan trọng và kết quả bất lợi cần cho kết luận. | Các bảng chi tiết lặp theo stock/fold/repeat, toàn ma trận scenario nếu không cần trong lập luận chính. Giữ locator/hash nguồn. | T73i, T73k |
| E. Verification and Audits | Chương 5: bảng ngắn hợp đồng/kiểm chứng/giới hạn, Native row-wise FAIL, scope của Common và các gate chưa đạt. | Nhật ký kiểm thử, receipt và hash dài; không nâng test phát hiện lỗi thành chứng nhận causal. | T73i, T73k |
| F. Reproduction and Application | Chương 4: vận hành/recovery/UI; Chương 5: điều kiện tái lập và giới hạn provenance. | Command log, hướng dẫn khôi phục đầy đủ, liệt kê asset; tiếp tục dẫn tới tài liệu vận hành hiện có. | T73g, T73h, T73k |

#### P9.3. Quy tắc bảng, hình và trang dọc

1. Mỗi bảng phải có mục đích và đoạn dẫn/diễn giải gần bảng. Bỏ bảng trùng thông điệp trước khi chỉnh kích thước.
2. Với bảng nhiều cột: bỏ cột quản lý không cần cho người đọc; chuyển ghi chú chung ra caption/note; tách theo baseline, endpoint hoặc nhóm chỉ số với nhãn/đơn vị rõ. Không tách để che hàng bất lợi hay làm mất cặp so sánh.
3. Dùng bảng có độ rộng theo trang như `tabularx` hoặc cột ngắt dòng. Chỉ dùng `longtable` dọc khi cần qua trang và phải lặp header; bảng ngắn dùng float phù hợp để nằm gần đoạn giải thích.
4. Không dùng `landscape`, `sidewaystable`, `rotatebox` hoặc cấu hình PDF xoay trang. Không lấy `resizebox` thu nhỏ toàn bảng làm cách giải quyết mặc định; cỡ chữ bảng mục tiêu từ 10 pt trở lên và phải đọc được khi in A4.
5. Không cưỡng ép mỗi bảng lên một trang riêng bằng ngắt trang/float page. Nếu bảng hoặc hình toàn trang thực sự cần để đọc, giữ trang dọc và giải thích lý do trong rà soát; không lấp khoảng trắng bằng nội dung dư thừa.
6. F03, phần giải thích MT/training và policy là ưu tiên; hình timeline, chart pair, retrieval, DAG hoặc application chỉ giữ/gộp khi có thông tin riêng. Không phải mọi ID hình cũ đều bắt buộc xuất hiện trong bản rút gọn.
7. Sau khi build: kiểm cả rotation và kích thước trang, overfull box, ô/caption bị cắt, trang trắng, trang chỉ có mẩu bảng, danh mục và liên kết. Render toàn bộ PDF cuối, xem từng trang; kiểm lại các trang ảnh hưởng sau sửa.

#### P9.4. Rà soát và nghiệm thu sau biên tập

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T73 / M | T73l | Đối soát mọi luận điểm chính, đóng góp, kết quả và kết luận với sổ bằng chứng và ánh xạ trước/sau. | Có nguồn và đúng phạm vi; không mất nội dung cốt lõi khi bỏ phụ lục; kết quả âm, thiếu support và thí nghiệm chưa chạy vẫn rõ. |
| T74 / M | T73l | Rà theo góc nhìn người lần đầu đọc bằng mục 3; sửa giải thích Chương 3–4 còn thiếu trong ngân sách trang. | Trả lời được toàn bộ câu hỏi từ PDF, không bắt người đọc mở phụ lục hoặc mã nguồn để hiểu luồng chính; ghi đúng tự kiểm hay phản biện độc lập. |
| T75 / M | T73l | Biên tập ngữ pháp tiếng Anh, thuật ngữ, thì, mạch đoạn, caption và chữ viết tắt trong toàn khóa luận. | Tiếng Anh nhất quán; không acronym chưa giải thích, mã task/nhật ký repo hoặc các đoạn lặp được chèn trở lại làm vượt ngân sách. |
| T76 / M | T73l, T73 | Kiểm bibliography, trích dẫn, nguồn hình, quyền dữ liệu/phần mềm và khai báo cần thiết; cập nhật tham chiếu sau bỏ phụ lục. | Citation đầy đủ/phù hợp; không link/section/table reference treo hoặc mục bibliography mất attribution; quyền còn thiếu được nêu. |
| T77 / M | T73, T75 | Đối soát độc lập công thức, đơn vị, số lượng, phần trăm, quy ước rủi ro và độ chính xác hình/bảng. | Không sai số học/nhãn/support; làm tròn không đổi diễn giải hoặc âm thầm thay số chính xác của nguồn. |
| T78 / M | T74, T75, T76, T77 | Biên dịch sạch; kiểm log, số trang vật lý, danh mục, bookmark, orientation/rotation và trích xuất văn bản; ghi số trang từng phần. | Tổng **60–70 trang**, đủ sáu chương và tham khảo, **không phụ lục, không trang xoay/ngang**; không thiếu citation/reference/asset hoặc cảnh báo chưa được xử lý/kiểm cụ thể. Nếu vượt, quay về task biên tập liên quan thay vì thu nhỏ toàn tài liệu. |
| T79 / M | T78 | Render và xem từng trang, gồm bảng, đồ thị, công thức và thuật toán; sửa bố cục và kiểm lại trang ảnh hưởng. | Không chữ khó đọc, chồng lấn, ô/caption bị cắt, bảng ngắn bị đẩy ra trang riêng vô lý hoặc trang trắng ngoài ý muốn. Lượt rà toàn bộ dùng PDF cuối 60–70 trang; nếu sửa đổi số trang phải kiểm lại T78. |
| T80 / M | T79 | Xử lý phản hồi thực nhận từ tác giả/người hướng dẫn; nếu chưa có, ghi rõ chưa phản biện bên ngoài và làm lượt chỉnh nội bộ. | Mỗi góp ý có xử lý/vị trí; phần đổi được kiểm lại phù hợp; không ghi đã phản biện ngoài khi thiếu bằng chứng. |

### P10. Đóng gói tái lập và bàn giao

| Mã / quy mô | Phụ thuộc | Công việc và đầu ra | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| T81 / M | T80 | Khóa bản thảo cuối, đóng gói nguồn tự đủ, bibliography, hình/bảng và hướng dẫn build. | Không có credential hoặc raw data riêng tư/dư thừa; quyền tài nguyên rõ; không đường dẫn tuyệt đối hoặc phụ thuộc mẫu chưa theo dõi. |
| T82 / M | T81 | Giải nén vào thư mục sạch, build offline khi được hỗ trợ, đối soát PDF với bản đã rà; ghi toolchain/hash trong một manifest. | Build từ gói thành công, nội dung/trang/hình khớp; nếu timestamp khiến PDF khác byte thì ghi rõ, không tuyên bố đồng nhất byte. |
| T83 / S | T82 | Bàn giao `thesis.pdf`, gói nguồn và hướng dẫn tái lập ngắn; liệt kê phê duyệt/nộp bên ngoài còn chờ. | File tồn tại và khớp manifest; bàn giao không đồng nghĩa người hướng dẫn chấp thuận hoặc đã nộp trường. |
| T84 / S | T83 | Chốt checklist bằng commit nguồn, đường dẫn đầu ra và kiểm tra; chỉ ghi nộp/chấp thuận ngoài khi người dùng cung cấp hoặc cho phép sự kiện đó. | Phân biệt hoàn thành nội bộ với đã nộp/được chấp thuận; kế hoạch không tự cho phép gửi email, upload, ký hoặc nộp. |

## 6. Danh mục hình, bảng và thuật toán cần chuẩn bị

Dùng sơ đồ khái niệm để giải thích, công cụ vẽ đồ thị chuẩn cho hình khoa học. Hình/bảng đưa vào khóa luận phải có nhãn tiếng Anh, cỡ chữ đọc được khi in, caption tự đủ, đơn vị phù hợp và nguồn hoặc nhãn minh họa rõ ràng. ID dưới đây là danh mục của bản đầu, **không phải yêu cầu đưa toàn bộ vào bản rút gọn**. T73a ghi quyết định giữ/gộp/bỏ; T73l áp dụng bố cục dọc theo P9.3. ID dùng quản lý; số thứ tự cuối do LaTeX sinh.

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
| F11. Luồng ứng dụng | Đầu vào người dùng → tiến trình → kết quả có thể diễn giải | T35, T73g | Chương 4 nếu cần; không còn Phụ lục F trong bản nộp mới. |
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
| G4. Nguồn hoàn chỉnh | T59–T72, cập nhật cấu trúc T73a–T73l và các mục T01 bắt buộc đã rõ | Bản mới đủ phần đầu, sáu chương và tham khảo; không phụ lục; nguồn LaTeX tự đủ. P8 chỉ chứng minh bản đầu đã ghép. | Giữ danh sách vấn đề; chưa phát hành cuối khi còn danh tính giả định hoặc phần bắt buộc thiếu. |
| G5. Bản dự kiến nộp đã rà | T73a–T73l, T73–T80 | PDF 60–70 trang tính toàn bộ file, portrait/rotation=0, không phụ lục; đạt khoa học, dễ hiểu, tiếng Anh, ghi nguồn, số liệu và trực quan; đúng trạng thái phản biện ngoài. | Mở lại task nội dung/bố cục liên quan nếu vượt trang hoặc mất ý cốt lõi; không chạy lại suite runtime không liên quan. |
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

Khóa luận chỉ **hoàn thành nội bộ** khi mọi phần bắt buộc được viết bằng tiếng Anh; người mới theo được toàn phương pháp; luận điểm và số liệu quan trọng đều truy nguồn được; giữ các giới hạn trọng yếu; trích dẫn, công thức, tham chiếu đúng; PDF cuối có **60–70 trang vật lý, không phụ lục, toàn trang dọc và rotation=0**, đã kiểm từng trang; gói nguồn biên dịch được độc lập với thư mục mẫu. Không đạt yêu cầu bằng cách làm chữ/hình/bảng khó đọc hoặc chuyển toàn bộ phụ lục thành chương bổ sung. Quy định này áp dụng cho sản phẩm khóa luận, không yêu cầu chuyển kế hoạch, checklist hoặc trao đổi quản lý sang tiếng Anh.

Không che chỗ trống nội dung, thông tin bịa, phần bắt buộc thiếu, lỗi số liệu trọng yếu chưa sửa hoặc tài nguyên phát hành chưa kiểm bằng cách đánh dấu task hoàn tất. Việc nộp ra ngoài, người hướng dẫn đồng ý và cơ sở đào tạo chấp thuận là các trạng thái riêng, chỉ ghi khi có bằng chứng thực tế.
