# Kế hoạch cuối: cập nhật bài báo và giao diện chọn phiên bản

Ngày audit: **12/11/2026**, nguồn `develop:d16630e9`, donor `fix:9efd23f4`.
Đây là kế hoạch triển khai phần còn lại sau U01–U09, **chưa sửa code, LaTeX,
template, dữ liệu hay kết quả**. Bảng tại mục 6 có cột checklist để theo dõi
ngay trong plan; trạng thái được cập nhật đồng bộ với
[README W12](README.md#công-việc-cuối-cho-bài-báo-và-giao-diện), nơi ghi kết quả kiểm tra.
[Quy trình develop](develop_workflow.md) tiếp tục áp dụng: nhánh tác vụ từ
develop, kiểm tra đúng phạm vi, commit rồi merge develop; không quay lại làm
việc trên fix. Kế hoạch này cụ thể hóa U10 và bổ sung phần ứng dụng sau U10,
không mở lại research U08 hoặc các lượt đã hủy.

## 1. Quyết định về phạm vi và cách trình bày

**Đưa phương pháp mở rộng và kết quả so sánh chính vào thân bài.** Appendix
chứa chi tiết đủ để tái lập và các phân tích bổ sung. Nếu đưa toàn bộ mở rộng
vào appendix thì nội dung chính không giải thích được các phiên bản và kết
luận so sánh mà người đọc cần đánh giá.

Giữ nguyên tiêu đề hiện tại, tác giả, tám section chính theo đúng thứ tự,
các subsection hiện có, công thức kinh tế và sáu appendix A–F. Chèn paragraph
hoặc subsubsection cần thiết trong khung hiện tại; không đổi bài thành một
bài MT-BICL mới, không đổi tên các section hoặc chuyển toàn bộ kết quả gốc
ra phụ lục. Hai entrypoint `main.tex` và `main_submit.tex` dùng chung nội dung;
khác biệt author/CRediT hiện có được giữ.

Phân biệt **hai nghiên cứu có provenance riêng** trong cùng bài:

- **Nghiên cứu gốc**: Full/Base, controls số học, hai panel chín đơn vị về
  upstream và alpha/sentiment/placebo từ revision của fix. Giữ kết quả và
  giới hạn đúng nguồn; Base loại alpha/sentiment không phải `original_common`.
- **Nghiên cứu mở rộng thống nhất U08/U09**: `original_fix`, `original_common`,
  năm mở rộng, `Fact_Anchor` và hai economic controls; 102 điểm, một upstream
  realization, ba Decision repeat. Cùng lịch kiểm định không biến đây thành
  cùng lượt suy luận với nghiên cứu gốc; không trộn response hoặc gộp N.

Ứng dụng tiếp tục là hệ Flask trong **`templates/`** (tên thư mục thực tế),
giữ các màn hình đang dùng và bổ sung lựa chọn phiên bản, kết quả nhiều phiên
bản trên cùng đầu vào, cùng chức năng đọc bằng chứng bài báo. Không tạo một
website riêng. Hoàn tất bài báo trước, sau đó triển khai backend và giao diện.

## 2. Kết quả audit và các việc còn thiếu

| Đối tượng đã đọc | Hiện trạng xác nhận | Hệ quả đối với việc còn lại |
| --- | --- | --- |
| `paper/`, `revision/` | 50 file paper và 28 file revision cùng blob với fix; bài vẫn dùng số liệu nghiên cứu gốc | Chưa thể coi việc chuyển nhánh là đã cập nhật bài bằng U09 |
| `paper/content/01…08`, `appendices.tex` | Đủ tám section và A–F; architecture/algorithm còn mô tả Full/Base và native selector | Bổ sung nhánh common/prior/MT và định nghĩa hai study ngay tại các phần tương ứng |
| `paper/content/tables/` | Sáu bảng chính, bốn bảng appendix, `summary_numbers.tex` lấy từ release cũ | Generator mới và namespace số liệu riêng; không thay macro Full/Base bằng số U09 |
| `scripts/build_revision_manuscript.py` | Generator lịch sử có source archive và hợp đồng không ghi đè artifact | Không dùng như lệnh cập nhật U09 một bước, không ép finalizer cũ nhận bản thảo mới |
| `core/variant_registry.py`, `core/unified_methods.py`, `core/causal_bridge.py` | Tám vai trò có dependency/fallback; common đổi alpha projection và instruction; registry chưa cấp hosted release | UI phải dùng đúng adapter/dependency, không ánh xạ tên phiên bản sang cờ bật/tắt alpha |
| `web_interface.py`, `demo_new.html`, `output.html` | `/api/analyze` nhận mã/khung/ngôn ngữ, chạy graph gốc; không dispatch theo variant; cấu hình/graph dùng chung | Cần request contract, cấu hình đóng băng theo job và orchestration mới trước khi thêm lựa chọn có hiệu lực |
| `backtest.html`, `/api/backtest/start` | Backend từ chối mọi variant khác `original_fix` bằng 409; UI hard-code `full/no_alpha`, hai series và alpha lift | Không thể chỉ thêm dropdown; cần kết quả động theo ID và đường backtest chung có paired protocol |
| `utils/experiment_web.py`, `experiment_io.py`, `experiments.html` | Chỉ đọc replay U04; tìm `identity.json` + `result.json`, lọc một variant | U09 có `results.json`, không có `identity.json`; hiện không run nào trong namespace đủ điều kiện hiện trên trang. Cần adapter đọc U09 và so sánh cạnh nhau |
| Registry/UI quality text | Còn nhãn `WHOLE_SYSTEM_GATE_PENDING_U06_U07` mặc dù hai mốc offline đã hoàn tất | Cập nhật metadata theo capability và phạm vi thực tế, không chuyển thành whole-system PASS |
| Nguồn khóa U09 | Audit lần này khớp **729/729** source bindings, gồm cả bốn template, web entrypoint và registry | Thay UI sẽ làm verifier nguồn hiện hành cũ từ chối: phải có historical checkout/archive và release mới trước khi sửa |
| Reviewer | Response hiện hành tự ghi **0/18 comment được chứng nhận đóng**; matrix có trạng thái/vị trí từ các lượt trước | Đối chiếu cả 87 tiểu mục, không suy rằng test PASS hoặc U09 hoàn tất đã đóng toàn bộ reviewer |

Audit này đọc source và định dạng artifact, chưa khởi động web để kiểm thị giác.
Kiểm responsive, nội dung tràn, chart và tương tác là bước nghiệm thu UI sau
triển khai; chưa có tuyên bố giao diện hiện tại đã PASS các bước đó.

### 2.1. Các giới hạn phải hiện trong bài và phần thông tin nghiên cứu của UI

- Native có parity trên miền hợp lệ U03, không phải tương đương mọi input hay
  đồng nhất response hosted. Native row-wise causal **FAIL**, toàn hệ
  **NOT_CERTIFIED**; alpha causal của common không sửa ngược native.
- U09 có 102 điểm thị trường, 12 ngày/sáu fold, 51 tài khoản mã/fold, ba
  Decision repeat và **một** upstream realization. 2.448 forecast slot không
  phải 2.448 lần chạy full hoặc 2.448 mẫu thị trường độc lập.
- Các tài khoản được cấp vốn riêng; mean account return không phải portfolio
  return. Ba repeat không tăng số quan sát thị trường độc lập.
- Bank có 852 task CORE4; cần hiện effective support/fallback cho OOD5.
  79/102 điểm không có sentiment khả dụng, không diễn giải thành tin trung lập.
- Nhãn donor raw và nhãn query theo oracle khác ở 828/852 task, độ lệch lớn
  nhất khoảng 0,042988489 điểm phần trăm. Giữ nguồn và giải thích mapping;
  không sửa lại dữ liệu đã khóa cho đẹp.
- C2/B gần như luôn fallback: mỗi bản chỉ có ba raw Decision trên 306 slot;
  MT trùng action với Fact_Anchor 302/306 slot. Không diễn giải outcome thành
  giá trị thuần của retriever/student mà bỏ coverage và policy.
- Hiệu quả native→common gồm thay alpha và prompt; common→Fact_Anchor gồm
  thay anchor; Fact_Anchor→MT mới mô tả phần revision. Đây không phải các
  can thiệp cô lập hoàn toàn.

## 3. Nội dung bài báo: giữ khung, sửa đúng vị trí

| Vị trí hiện có | Nội dung cần cập nhật | Nội dung đưa xuống appendix |
| --- | --- | --- |
| Abstract/highlights tại hai `main*.tex` | Thêm phạm vi mở rộng và một kết luận cân bằng từ U09; phân biệt bằng chứng gốc với mở rộng; không tuyên bố profitability/superiority | Không đưa thông số/ledger chi tiết vào abstract |
| 1. Introduction | Giữ động cơ alpha/sentiment; thêm mục tiêu so sánh Bayesian/MT và đóng góp ở mức phương pháp, phần mềm, bằng chứng; không nhận kiến trúc QuantAgent là sáng tạo mới | Danh mục implementation đầy đủ |
| 2. Related works | Bổ sung đoạn Bayesian retrieval, regime context và task/utility-conditioned ICL tại subsection phù hợp; đọc nguồn nghiên cứu gốc trước khi thêm citation | Chi tiết công cụ, không thay nghiên cứu liên quan bằng tên module |
| 3. Problem Formulation | Giữ label/P&L; thêm ký hiệu variant, shared snapshot, prior cutoff, raw proposal/final action. Sửa thuật toán walk-forward thành shared upstream → projection native/common → dependency-ordered Decision → ledger | Pseudocode từng retriever, quy tắc fallback chi tiết |
| 4. System architecture | Giữ Overview và năm agent. Trong Overview nêu registry và nhánh native/common; trong Alpha phân biệt native/causal; trong Decision thêm mô tả ngắn đủ hiểu v1, C2, A, B, MT và Fact_Anchor | Prompt đầy đủ, K/thresholds/resources và schema |
| 5. Experimental Setup | Mỗi subsection giữ tên/thứ tự. Nêu hai study, cùng support nhưng khác response; U09 một upstream/ba Decision; hai baseline, controls và ba bridge; nguồn model/options/bank/selector frozen; quy trình thống kê riêng | 51 selector bindings, model/data/source hashes, exact configuration và toàn attempt ledger |
| 6. Backtest Results | Giữ ba subsection hiện có. Thêm subsubsection so sánh mở rộng trong Nine-Symbol Paired Benchmark; báo cả hai baseline và fallback. Trong Disentangled Ablation giữ panel cũ, giải thích bridge U09 chưa thay được ablation còn thiếu. Thêm sensitivity U09 trong Robustness | Per-symbol/fold/repeat, toàn 20 contrasts, L1/L3, leave-one-out, CORE4 và trace chi tiết |
| 7. Limitations & Future Work | Thêm giới hạn exposed cohort, chỉ Decision repeats, thiếu ablation mới, domain support/fallback, native/common attribution. Giữ sentiment/visual/market execution và public archive còn thiếu | Không giấu giới hạn chính vào appendix |
| 8. Conclusion | Tổng hợp hệ gốc và mở rộng với kết quả âm, baseline cụ thể; chưa đủ chứng minh mở rộng vượt hệ gốc hoặc khả năng giao dịch có lãi | Không thêm kết quả chưa xuất hiện ở Results |
| Availability/acknowledgments/metadata | Trỏ đúng release mới, mô tả khả năng tái lập offline; giữ tác giả/title/ORCID, không bịa DOI/PID hoặc xác nhận quyền chia sẻ | Manifest phần mềm ở appendix E |

**Phân bổ A–F, không thêm appendix mới mặc định:** A thêm prompt chung/prior/
anchor/MT và nói rõ đoạn nào là bản dịch minh họa, đâu là request thật; B thêm
snapshot/forecast/provenance schema; C phân biệt công thức native và causal
adapters; D giữ quy tắc Indicator, chỉ sửa khi có sai lệch có bằng chứng; E thêm
registry/config/dependencies/runtime/restore; F thêm kết quả đầy đủ và sensitivity
U09 cạnh các bảng gốc, ghi study ID rõ ràng.

### 3.1. Cách đọc kết quả chính để không viết quá bằng chứng

Nguồn là [report U09](../../../outputs/unified_integration/u09_analysis_r1/report.md),
`summary.csv`, `contrasts.csv`, `bridge.csv` và `results.json` cùng thư mục.

| Vai trò | Mean account return % | BA % | Bypass /306 |
| --- | ---: | ---: | ---: |
| original_fix — hệ gốc | -0.652699 | 51.844156 | 0 |
| original_common — baseline cùng môi trường mở rộng | -1.024794 | 45.965368 | 0 |
| bayesian_v1 | -0.698188 | 50.095238 | 162 |
| C2 | -1.030117 | 45.748918 | 303 |
| A_tp_pool | -1.019471 | 46.181818 | 282 |
| B_semantic | -1.030117 | 45.748918 | 303 |
| MT_BICL | -1.253483 | 43.168831 | 108 |
| Fact_Anchor — dependency/control | -1.286449 | 42.735931 | 0 |

Bảng chính phải kèm CASH và ALWAYS_LONG theo chu kỳ với đủ phí; không gọi
ALWAYS_LONG là continuous buy-and-hold. V1 so common có Δreturn khoảng
**+0,326606 đpt**, band mô tả **[0,067130; 0,586081]**; so native là
**−0,045489 đpt**, band **[−0,362311; 0,271332]**. Vì vậy kết luận phù hợp là
cải thiện so common trong phân tích này, **chưa có bằng chứng vượt hệ gốc**.
MT so native khoảng −0,600784 đpt. Tất cả vai trò nghiên cứu có mean return âm.

U09 dùng paired circular fold bootstrap 10.000 draw, PCG64 seed20261110,
L2, cùng chỉ số resample cho 20 endpoint/contrast của hai family; band đồng
thời bằng standardized max-deviation. Đọc giá trị từ artifact, không tính lại
trong LaTeX/JavaScript. Giữ quy tắc finite/null, sensitivity L1/L3, không chọn
band đẹp nhất. Sáu fold lịch sử đã exposed chỉ hỗ trợ mô tả/sensitivity, không
nhận calibrated significance/coverage. Không áp seed/phương pháp U09 ngược
vào các bảng nghiên cứu gốc.

### 3.2. Bảng, hình và thuật toán cần xử lý

| Artifact/nhãn hiện tại | Quyết định trong bản cập nhật |
| --- | --- |
| `t01_scope.tex`, `tab:scope` | Thêm panel riêng hoặc bảng kế tiếp cho U08/U09: points, upstream realization, repeats, roles, calls và missing support; không cộng các study thành N mới |
| `t02_classification.tex`, `t03_accounts.tex` | Giữ dữ liệu gốc; bổ sung một bảng chính U09 10 hàng với BA, return, LONG rate, fallback và support. Không ghi đè số Full/Base |
| `t04_repeats.tex` | Giữ hai panel cũ; thêm panel/companion ba Decision repeats trên 102 điểm, ghi một upstream realization |
| `t05_temporal.tex`, `t06_numeric.tex` | Giữ study/estimand gốc; U09 sensitivity nằm trong bảng bổ sung riêng. Numeric selector controls không trở thành LLM retrieval ablation |
| `a01_rules.tex`, `a02_custom.tex` | Giữ quy tắc/công thức native đúng nguồn; thêm phân biệt causal projection nếu cần, không thay công thức archived |
| `a03_symbols.tex`, `a04_execution.tex` | Giữ kết quả gốc; thêm companions U09 theo symbol/fold/repeat. Không gán 12 stress scenarios cũ cho các bản mới chưa chạy |
| `summary_numbers.tex` | Giữ namespace macro gốc; tạo macro U09 có prefix riêng từ cùng nguồn generator để abstract/body/table không lệch nhau |
| `fig:flow` / `figs/final_flow.tex` | Sửa sơ đồ thành shared upstream một lần, hai projection, dependencies và forecast→action; giữ năm agent và biểu diễn đường native |
| `fig:alpha_agent` / `revised_alpha_pipeline.tex` | Thêm nhánh native và causal frozen selector, giữ sentiment là đường riêng; không vẽ tin tức thành thành phần của factor score |
| `fig:decision_agent` / `revised_decision_pipeline.tex` | Thêm prior/fact/MT context, fallback/bypass, policy và raw/final. Tóm tắt ở thân bài, cấu hình chi tiết ở appendix |
| `fig:walkforward` / `revised_walkforward.tex` và `alg:walkforward` | Bổ sung bank exit < cutoff, frozen fits, query không vào context, dependencies/repeats dùng cùng upstream; giữ Open(t+1)→Close(t+3) |
| `fig:calendar` / `final_calendar.png` | Giữ nếu support/dates khớp U09; caption nói rõ dùng chung lịch, khác lượt inference. Không cần tạo ảnh mới chỉ vì sửa văn bản |
| `fig:charts` / `final_pattern.png`, `final_trend.png` | Giữ cặp CMG chọn theo thời gian và provenance gốc. Không chọn lại chart theo outcome; caption không nhận đây là VLM semantic validation |
| Hình kết quả mới | Dùng `return_contrasts.svg/png` U09 làm nguồn cho figure hai baseline trong Results; caption band mô tả. Nếu đổi kích thước/nhãn, render từ cùng dữ liệu trong release mới, giữ nguyên ảnh nguồn |

Các PNG sơ đồ/screenshot legacy không được `\input`/`\includegraphics` trong
bản hiện hành không cần vẽ lại. Dùng LaTeX/TikZ hoặc công cụ plotting xác định
cho sơ đồ/figure khoa học; không dùng ảnh minh họa sinh ngẫu nhiên thay chart
thực nghiệm. Rà label/ref/caption, đơn vị %, đpt, NA và chữ trên hình ở cả hai PDF.

### 3.3. Reviewer: cập nhật bằng chứng, giữ rõ phần chưa đáp ứng

| Comment | Phần có thể cải thiện trong đợt cập nhật | Phần không được tự nhận đã hoàn thành |
| --- | --- | --- |
| R1, R5, R11 | Class-aware metrics, economic oracle, controls, risk/uncertainty và target rõ cho U09 | Lợi nhuận triển khai, suy luận xác nhận từ ít clusters |
| R2, R3 | Phạm vi thời gian/support và ba Decision repeats đủ 102 điểm | Mẫu đại diện/prospective, upstream×Decision factorial đầy đủ, loại contamination |
| R4, R8 | Nêu đúng bundle gốc, mở rộng, dependency bridge, attribution kiến trúc/prompt | Causal component value; retrieval/prior/MT ablations chưa thực thi |
| R6 | Giữ raw/reset/active lineage U08 và giải thích phần mới | Root cause duplicate legacy vẫn chưa biết |
| R7, R14 | Coverage tin tức, input chart và provenance rõ | Financial sentiment labels độc lập, PIT nội dung xác thực, human visual validation |
| R9 | Release/source/archive và hướng dẫn offline mới | Public PID/rights, immutable hosted weights, tái tạo hosted output giống hệt |
| R10, R12, R13 | Phân biệt native/causal, rules, công thức và row-wise gate | Native zero-leakage, fixed/random hosted selector experiment chưa có |
| R15 | Hợp đồng execution, daily/cycle metrics và sensitivity đúng study | Fills/corporate actions xác thực, L5/L10 hoặc sensitivities mới chưa chạy |
| R16 | Rà citation mới, numbering và locator sau render | Danh tính chính xác historical refs [14]/[21]/[22]/[23] khi chưa có nguồn |
| R17, R18 | Giữ cấu trúc/title/tác giả; cập nhật wording và locators | Editor acceptance hoặc thông tin liên hệ chưa được xác thực |

Cập nhật `revision/response_to_reviewers.md` và `reviewer_matrix.csv` theo
từng tiểu mục, gồm nguồn, nội dung sửa, vị trí PDF và giới hạn. Đồng bộ các
trạng thái cũ mâu thuẫn; không dùng một nhãn “addressed” để chứng nhận cả
comment. Kết thúc U10 là **bản thảo khớp bằng chứng và đủ gói bàn giao**, không
đồng nghĩa 18/18 reviewer đã chấp thuận. Việc thu thêm dữ liệu, gán nhãn độc
lập hoặc nghiên cứu prospective là nghiên cứu mới, không tự mở trong đợt này.

## 4. Thiết kế cập nhật ứng dụng hiện tại

### 4.1. Phiên bản và khả năng sử dụng

| Nhãn người dùng | ID backend | Vai trò/điều kiện |
| --- | --- | --- |
| Hệ gốc | `original_fix` | Mặc định, giữ native serving; không ngầm đổi thành common |
| Bayesian v1 | `bayesian_v1` | Bank/regime và common dependency |
| Bayesian v2 — C2 | `C2` | Conditional-quality retrieval, fallback common |
| Bayesian A — TP Pool | `A_tp_pool` | TP-pool retrieval, fallback common |
| Bayesian B — Semantic | `B_semantic` | Semantic retrieval, fallback common |
| MT-BICL | `MT_BICL` | Common + Fact_Anchor + facts/context/student, policy/bypass đúng phiên bản |
| Baseline chung — nâng cao | `original_common` | Đối chứng phương pháp, luôn có trong bảng so sánh nghiên cứu |
| Fact Anchor — nâng cao | `Fact_Anchor` | Dependency/control; tự chạy khi MT cần, cho xem trong chế độ nghiên cứu |

Sáu lựa chọn chính dành cho phân tích; hai vai trò kỹ thuật nằm trong phần
nâng cao và vẫn hiện trong bằng chứng so sánh đầy đủ. CASH/ALWAYS_LONG là
controls của đánh giá, không giả làm agent. Tên hiển thị không thay canonical ID.

Registry cần metadata về khả năng **đọc kết quả / phân tích mới / backtest**,
khung thời gian, miền mã/ngày, resource readiness, model/prompt/config version,
dependency và fallback. Không lấy `hosted_release=False` của research cũ để
chặn mọi ứng dụng tương lai, cũng không bật nó hàng loạt để bỏ qua điều kiện.
Ứng dụng mới có release/capability riêng. Nút chạy chỉ mở khi preflight đủ điều
kiện, nếu thiếu thì nói rõ tài nguyên hay support nào thiếu.

Mục tiêu nghiệm thu là người dùng **chạy được cả sáu bản chính trên miền đầu
vào đã công bố**, không chỉ xem dropdown bị vô hiệu hóa. Research hiện có chỉ
chứng minh đường daily/as-of và assets frozen; không chứng minh mọi mã/ngày
hiện tại hay khung intraday đều được hỗ trợ. F08 đã xây provider as-of và
đóng gói resources phục vụ inference mới. Theo yêu cầu bổ sung ngày 13/11/2026,
F11 mở provider live riêng cho **phiên ngày hoàn tất mới nhất** của chín mã:
chạy từng bản nâng cấp để phân tích thực tế, không chỉ so sánh historical.
Giá/tin/VN-Index được capture và khóa trước forecast. Theo đính chính tiếp theo,
ngay trong chế độ intraday/khung khác cũng chọn được sáu bản: chart/I/P/T theo
khung chọn, ngữ cảnh Alpha/prior/MT vẫn ngày và T+2.5 theo phiên, không giả model
đã được huấn luyện riêng trên nến phút/tuần/tháng.
Không refit ngầm HMM/student/bank;
nếu phải đổi tài nguyên, version hóa bộ mới và giữ kết quả U09 gắn bộ cũ.

### 4.2. Luồng màn hình

1. **Trang phân tích — `demo_new.html`:** theo yêu cầu mới nhất chỉ có nguồn
   Realtime · intraday and other timeframes, duy nhất 1D và sáu lựa chọn phiên bản.
   Chọn mã/bản rồi Phân tích; bỏ form as-of/daily riêng và so sánh. Mọi bản hiện
   cùng overlay từng agent rồi mở cùng bố cục kết quả Original; bản nâng cấp
   bổ sung BICL/context/policy. Original giữ pipeline/ngôn ngữ hiện tại;
   năm bản nâng cấp giữ miền tài nguyên chín mã và báo cáo VI.
2. **Kết quả — `output.html`:** giữ bố cục Original cho decision, lý do,
   báo cáo agent và ảnh của đúng snapshot. Bản nâng cấp thêm panel BICL với
   phương pháp/context/prior, baseline→final, raw/final/LONG/CASH và lý do
   fallback/bypass. Chỉ mở khi phân tích hoàn tất; GET/reload kiểm owner và
   không gọi model. Không tạo P&L/đúng-sai query khi chưa có giá thoát.
3. **Backtest — `backtest.html`:** cấu hình cùng cửa sổ ngày/mã và danh sách
   phiên bản; bảng và series sinh từ IDs. Giữ khả năng đọc kết quả Full/Base
   cũ bằng adapter riêng, không đổi `no_alpha` thành `original_common`.
   Tiến độ phân biệt points, Decision slots và API attempts; có dừng/tiếp tục,
   kết quả partial rõ coverage, không xếp hạng final khi chưa đủ.
4. **Thực nghiệm — `experiments.html`:** danh sách run có loại “Bằng chứng bài
   báo”/“Backtest mới”, nhiều phiên bản cạnh nhau, filter cùng support, baseline
   gốc hoặc common, repeats, bảng metrics, contrast plot, fallback và export.
   U09 là lựa chọn mặc định cho bằng chứng bài báo; mở trang không gọi LLM.
5. **Điều hướng và hình thức:** thống nhất navigation, màu sắc, typography,
   tên phiên bản và VI/EN giữa bốn trang; tận dụng giao diện hiện có. Bảng rộng
   cuộn ngang có cột tên rõ; trạng thái loading/empty/error/partial/completed,
   focus bàn phím và kích thước mobile/desktop đều phải kiểm bằng trình duyệt.

Không dùng màu xanh hoặc badge “tốt nhất” chỉ vì loss nhỏ hơn; hiển thị giá
trị và baseline cụ thể. Metrics không xác định là NA kèm lý do, không thay
bằng 0, kể cả JavaScript hiện dùng `|| 0` ở một số chỗ. Confidence của LLM
không được trình bày như probability đã hiệu chuẩn.

### 4.3. Backend cần có trước khi mở các lựa chọn chạy

- **Hợp đồng request/result:** chọn `variant_ids`, mode, mã/ngày/khung,
  ngôn ngữ, repeat, model/options và version; validate ở server, không chỉ
  ở HTML. Result có `run_id`, snapshot hash, config/resource version,
  requested/executed IDs, raw/final, fallback reason, support và metric unit.
  Kiểu dữ liệu trả JSON phải là Python nguyên bản.
- **Tái sử dụng adapter chung:** một lớp điều phối dùng registry/dependency
  order và các adapter hiện có; không viết thuật toán Bayesian/MT thứ hai
  trong Flask hoặc JavaScript. Đường live phải có provider riêng cho dữ liệu
  hiện tại/as-of, không đọc future labels hoặc chỉ lookup prepared response.
- **Paired execution:** mỗi point có một snapshot bất biến, Indicator→Pattern
  →Trend chạy một lần, deep-copy sang các bản. Tách projection alpha/prompt
  native/common có version. Mỗi dependency chạy một lần trong mỗi repeat;
  không gọi lại graph theo từng phiên bản. Fallback đúng policy, ghi lại
  phương pháp yêu cầu và phương pháp thực thi, không ngầm chuyển sang CASH.
- **Tài nguyên/PIT:** history/news cutoff, prior exit < as-of, selector fit
  chưa nhìn query, teacher/student/HMM version; query đang đánh giá không
  được thêm vào context. Phân biệt no-news hợp lệ với nguồn thiếu/hỏng;
  thiếu resource không được coi là quyết định thành công.
- **Tác vụ nền:** cấu hình/key/model/ngôn ngữ snapshot theo job; tránh một
  người đổi global graph giữa lượt chạy của người khác. Lưu checkpoint/owner
  và ảnh theo run/point, không dùng đường ảnh dùng chung gây lẫn kết quả.
  Retry qua wrapper, quota/backoff, idempotent resume, dừng tại ranh giới an
  toàn; không retry mù một request có kết quả chưa rõ. Job failure/partial
  không xóa slot đã hoàn thành.
- **Cache và export:** key bao gồm input/model/options/prompt/resource/
  language/variant identity; không reuse kết quả của bản khác. Xuất JSON/CSV
  có units/support/provenance, không đưa API key/raw secret vào browser hay
  file export. Render nội dung model như nội dung không tin cậy; lọc HTML,
  chống path traversal và CSV formula injection tại các bề mặt mới.

Các kiểm tra bảo mật trên gắn trực tiếp với endpoint/job/export được sửa,
không phải một dự án thay toàn bộ cơ chế đăng nhập hoặc hạ tầng.

### 4.4. So sánh đúng ở cả dữ liệu cũ và chạy mới

So sánh paired chỉ khi cùng run/input snapshot, mã/ngày, target/cost, model
options, repeat IDs và support. Khác profile native/common là khác biệt
**có chủ đích** phải ghi rõ; khác model/dataset/run không được gọi là paired
chỉ vì cùng tên mã. Có thể xem hai run cạnh nhau để tham khảo nhưng không
tự sinh contrast/statistical band của một thí nghiệm ghép cặp.

Trong bảng U09: giữ metrics mean qua repeat đúng evaluator, N=102, 51 account,
coverage và missingness. Dùng cả BA, accuracy, MCC/F1 nếu có, LONG rate,
return, drawdown, chi phí/turnover và fallback; không dùng accuracy/alpha lift
làm kết luận duy nhất. Hiện daily NAV và cycle return đúng tần suất, không
cộng vốn các account độc lập thành một portfolio. Filter làm thay đổi support
phải báo số mẫu và dùng evaluator cùng hợp đồng; không giữ band full study
cho một subset tùy ý. Mặc định chỉ hiển thị các contrasts đã khóa U09;
phân tích mới ngoài protocol phải có nhãn exploratory.

## 5. Bảo toàn bằng chứng khi sửa paper và UI

Trước thay đổi đầu tiên, F01 chốt source snapshot của paper/revision/app và
cách khôi phục các asset ignored. Giữ nguyên ZIP/receipt/raw U03/U08/U09.
Paper release mới có manifest nối **artifact cũ → số liệu được dùng → bảng/
hình/đoạn mới**, commit nguồn, build environment và hai PDF. Bản thảo cũ vẫn
đọc/verify được bằng source archive của nó.

UI chạm các file đã pin trong 729 bindings. Do đó cần một consumer historical
chạy trên source/runtime đã khóa (checkout hoặc package biệt lập) rồi adapter
ứng dụng đọc output có hash đã kiểm. Không nạp tùy tiện Python từ archive lên
import path web, không sửa expected hash, bỏ guard hoặc ký lại receipt cũ để
đánh dấu bản mới PASS. New app release dùng manifest/version/output namespace
riêng. Các verifier cũ còn đối chiếu worktree phải được gọi trên historical
checkout phù hợp; không hứa lệnh cũ sẽ PASS trên mọi HEAD sau sửa.

Adapter đọc U09 cần nhận dạng `results.json` và receipt/artifact bindings,
không rename file thành `result.json` để qua loader U04. Cache kết quả đã
verify theo identity/hash, không cold-replay toàn study trên mỗi HTTP GET.
CLI, UI và paper dùng cùng dữ liệu/evaluator, không có ba công thức P&L.

Nguồn neo cho kế hoạch:

- [Nghiệm thu U09](unified_analysis_acceptance.json), [runtime U09](unified_analysis_runtime.json), [protocol v2](unified_comparison_protocol_v2.json).
- [Gói U08](unified_live_research.zip): SHA256 `5936bc971bebf1b139a34b93f154ad8e54d0a0e37fdaa6ac4673295f8b60a11c`.
- [Gói kết quả U09](unified_analysis_results.zip): SHA256 `e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9`.
- [Response reviewer hiện hành](../../../revision/response_to_reviewers.md) và [matrix](../../../revision/reviewer_matrix.csv).

## 6. Thứ tự thực hiện và điều kiện hoàn thành

Trạng thái/checklist của các mã F dưới đây cập nhật cùng README W12 trong
cùng commit khi bắt đầu hoặc hoàn tất một bước. F01–F05
hoàn tất U10; F06–F12 là phần ứng dụng bổ sung. Mỗi bước dùng nhánh tác vụ phù
hợp từ develop, không commit trực tiếp develop.

**F01–F05 và U10 đã hoàn tất phạm vi bàn giao nội bộ; F06–F10 đã xong phần tương ứng, F11 đang nghiệm thu.** [Mapping và runbook historical](final_evidence_map.md)
đã chốt hai nghiên cứu, snapshot paper/revision/app và đường khôi phục
nguồn/assets đã khóa. Smoke checkout biệt lập đã khớp nguồn và replay nguyên
byte 15 artifact U09. F02 đã sinh 26 artifact với 798 ô có provenance trong
release/namespace U09 riêng; cold render nguyên byte PASS. Kết quả và hash
ghi tại README W12. F03 đã bổ sung nội dung hai study, build hai PDF 50 trang và kiểm trực quan
100 trang PASS; nguồn/title/tác giả/cấu trúc giữ đúng phạm vi. F04 đã cập nhật
bốn sơ đồ/caption/figure và vị trí bảng, build hai PDF 51/50 trang và kiểm đủ
101 trang PASS. F05 ngày 13/11/2026 đã đồng bộ 87 yêu cầu/18 comment, chốt
PDF 51/50 trang/101 trang render, source/companions/locators và manifest.
0/18 comment được chứng nhận đóng; quyền/PID và evidence còn thiếu giữ rõ.
F06 ngày 13/11/2026 đã chốt [contract/version serving riêng](variant_serving_contract.md),
registry sáu chính/hai nâng cao, API metadata/preflight và job/config/result
identity, 33 test đúng phạm vi PASS. F07 đã có reader U09 kiểm package/member/
receipt, viewer so sánh offline, plot và export; 46 Python + 6 DOM PASS.
Template/CSS/JS đã tách file; browser trực quan chưa kiểm do host không khả dụng
và approval từ chối Edge, giữ trong gate F11. F08 đã có provider/runner mới và
API job có owner, release 188 binding/chín mã/58 phiên 01/07–23/09/2026 (1d/VI),
105 test/compile18 PASS, HTTP fixture và adapter thật trên query mới; chưa smoke
hosted. F09 đã nối form/kết quả với API serving, sáu bản/hai dependency,
so sánh cùng snapshot, raw/final/CASH, context và native/common Alpha;
108 Python + 18 DOM, compile5/JS7 PASS. Browser desktop/mobile chưa kiểm do
host không khả dụng, giữ ở F11. F10 đã có backtest nhiều bản, catalog owner,
filter cùng support, account/classification chung U09, daily NAV/cycle return,
JSON/CSV và adapter Full/No-Alpha riêng; 156 Python + 31 DOM, compile13/JS7
PASS, toàn HTTP fixture. Gate F11 ban đầu có 8 test mới và viện dẫn F10;
sau khi nhận develop `4de6d1aa`, F11 mở thêm dữ liệu phiên ngày mới nhất cho
sáu bản. Mã service/provider/UI đã đổi nên kiểm lại caller/PIT/recovery liên
quan. Mốc ngày trước đính chính có 138 Python + 16 DOM, compile19/JS5 PASS;
đính chính mới mở sáu lựa chọn ngay trong intraday/khung khác và kiểm lại
provider/caller/PIT: **136 Python + 19 DOM, compile14/JS7 PASS**, không coi
gate ngày là chứng nhận code đa khung. Sửa incident tiếp theo: guard 6.500 chỉ
áp dụng backtest, Original realtime giữ prompt gốc; VNINDEX dùng ngày/Close
cho lịch/HMM thay vì chặn vì OHLC không được dùng. **100 Python + 20 DOM,
compile14/JS3 PASS**, 18 leakage/11 native parity. Probe giá thật FPT ngày
13/11: snapshot200/preflight ready/C2 completed, HTTP model fixture và tin tắt;
không phải dự báo thật. [QA sửa realtime](serving_realtime_repair_checks.zip)
khóa kết quả mới, QA trước đó giữ nguyên làm lịch sử. Yêu cầu UI tiếp theo
thu gọn form còn một nguồn Realtime/1D; năm bản nâng cấp dùng cùng overlay và
cửa sổ Original, thêm BICL đọc từ context/policy. **103 Python + 19 DOM, compile12/JS6 PASS**;
[QA giao diện 1D](serving_daily_analysis_checks.zip) khóa mốc đó. Phản hồi UI
tiếp theo sửa BICL trước Decision cuối, format Indicator, khôi phục Alpha
Agent đầy đủ và common riêng, sentiment đúng snapshot/PIT. **39 Python + 21 DOM, compile12/JS3 PASS**,
[QA báo cáo](serving_report_checks.zip); không đổi graph/adapter/prompt/scientific artifacts.
[Receipt F11](serving_integration_acceptance.json) giữ
`OFFLINE_PASS_BROWSER_PENDING`: desktop/mobile chưa kiểm do host không khả dụng
và duyệt tự động từ chối mở Edge. F11 đang làm, chưa merge vì gate browser còn
thiếu theo AGENTS §1.2; F12 chưa bắt đầu.

Ký hiệu: **☑ Hoàn tất**, **☐ Chưa bắt đầu**, **☐ Đang làm**. Chỉ đánh ☑ khi
đạt điều kiện hoàn thành và có kết quả kiểm tra tương ứng trong README W12.

| Mã | Checklist | Công việc, nhánh gợi ý | Phụ thuộc | Đầu ra và điều kiện hoàn thành |
| --- | --- | --- | --- | --- |
| F00 | ☑ Hoàn tất | Audit và lập kế hoạch cuối | U01–U09 | Đã audit paper/reviewer/API/templates và lập plan; chưa sửa paper/UI |
| F01 | ☑ Hoàn tất | Chốt nguồn/evidence và đường historical replay — `docs/final-evidence-map` | Audit này | Snapshot 810 file nguyên byte; mapping hai study; restore 286 asset, 729 source pin và cold replay 15 artifact PASS; không cần resolver mới |
| F02 | ☑ Hoàn tất | Generator bảng/figure/macros U09 — `feat/manuscript-unified-results` | F01 | Release 26 artifact/798 ô có provenance, 10 hàng/20 contrast/3 bridge/support/null; 16 test, compile 6 file và cold render nguyên byte PASS; macro gốc/archive không đổi |
| F03 | ☑ Hoàn tất | Cập nhật nội dung tám section và A–F — `docs/manuscript-extensions` | F02 | Đã cập nhật tám section/A–F và references có nguồn; metadata/24 khối toán cũ giữ nguyên; hai PDF 50 trang và 100 trang render/visual PASS; không trộn nghiên cứu |
| F04 | ☑ Hoàn tất | Cập nhật sơ đồ/caption/layout — `docs/manuscript-figures` | F03 | Bốn sơ đồ khớp shared/projection/dependency/policy và Algorithm 1; figure hai baseline nguyên nguồn; bảng gần diễn giải; hai PDF 51/50 trang, 101 trang render/visual và hình học 38 node/bản PASS |
| F05 | ☑ Hoàn tất | Reviewer, build hai PDF, kiểm và release bài — `docs/manuscript-final-release` | F04 | 87 yêu cầu đồng bộ response/matrix/crosswalk; PDF 51/50 trang, numbering/locators, source68/companions40/manifest và QA145 PASS; U10 bàn giao nội bộ hoàn tất, 0/18 comment được chứng nhận đóng |
| F06 | ☑ Hoàn tất | Chốt UX, capability và API contract — `feat/variant-serving-contract` | F05 | Contract/registry/config serving v1 riêng, sáu chính/hai nâng cao; API metadata/preflight, job identity bất biến và result/partial/UNKNOWN; 33 test, compile 5 file PASS, historical replay giữ F01; runner mới chờ F08 |
| F07 | ☑ Hoàn tất | Đọc U09 và so sánh offline trên web — `feat/research-results-viewer` | F06 | Reader kiểm hash/receipt, U09 mặc định, nhiều bản/hai baseline, plot/export đúng artifact; legacy giữ nguyên; 46 Python + 6 DOM, compile9/JS4 PASS; browser visual chờ F11 do host/approval |
| F08 | ☑ Hoàn tất | Provider và runner chọn bản/paired dùng chung — `feat/variant-serving-runner` | F06, F07 | Release as-of 188 binding/chín mã/58 phiên 1d/VI; sáu bản dùng DAG chung, dependency/fallback, owner/config isolation, quota/retry/UNKNOWN/checkpoint/stop/resume; 105 test/compile18 PASS, HTTP fixture; chưa smoke hosted mới |
| F09 | ☑ Hoàn tất | Nâng form và trang kết quả hiện tại — `feat/variant-analysis-ui` | F08 | Chọn/chạy sáu bản qua API serving, preflight chống response cũ, paired snapshot, raw/final/CASH/coverage/context và hai Alpha; tách template/CSS/JS, giữ realtime legacy, UI VI/EN/CSS mobile; 108 Python + 18 DOM, compile5/JS7 PASS, browser visual chờ F11 |
| F10 | ☑ Hoàn tất | Nâng backtest và trang so sánh — `feat/variant-backtest-ui` | F08, F09 | UI động theo IDs, cùng evaluator U09/nguồn bound, catalog owner và Full/No-Alpha riêng; daily NAV/cycle returns, filter/contrast cùng support, progress/stop/resume/JSON/CSV; 156 Python + 31 DOM, compile13/JS7 PASS, browser visual chờ F11 |
| F11 | ☐ Đang làm | Nghiệm thu realtime và báo cáo Original/BICL — `feat/analysis-report-parity` | F07–F10 | Chỉ Realtime/1D/sáu bản; BICL trước Decision cuối, Indicator chuẩn bảng, Alpha Agent đầy đủ và common riêng, tin snapshot/PIT. **39 Python + 21 DOM, compile12/JS3 PASS**. Browser desktop/mobile còn chờ, chưa hoàn tất/chưa merge; U09 giữ nguyên |
| F12 | ☐ Chưa bắt đầu | Bàn giao ứng dụng và hướng dẫn — `docs/unified-app-handoff` | F11 | Release mới có version/assets/runbook; chỉ làm việc tiếp trên develop; paper/result/UI cùng định danh; không tự push/deploy/submit |

Không gọi hoàn tất F08/F12 nếu mới thêm danh sách nhưng người dùng chưa chạy
được các bản mở rộng trên miền được hỗ trợ. Không gọi hoàn tất khoa học nếu
chỉ sửa trình bày/UI; các nghiên cứu bổ sung còn thiếu vẫn ghi rõ ở Future Work.

### 6.1. Kiểm tra cần chọn khi triển khai

- F02: tests generator/schema/units/null/source lineage, liên hệ
  `tests/unified_analysis/test_analysis.py` và `tests/test_revision_manuscript.py`
  khi caller bị ảnh hưởng; compile chỉ Python đổi. Không refit hoặc inference.
- F03–F05: diff nội dung, refs, số liệu, source hashes; build cả `main` và
  `main_submit`, kiểm undefined reference/citation/overflow, render **mọi trang**
  và kiểm trực quan bảng/hình/cắt trang. Cập nhật locators sau build cuối;
  docs/LaTeX thuần không cần unit/E2E toàn hệ.
- F06–F10: chọn test registry/contracts, `test_unified_experiment.py`, web JSON,
  evaluator và golden native có caller đổi. Thay đường dữ liệu/retrieval phải
  chạy leakage liên quan trong `test_unified_preflight_leakage.py`,
  `test_unified_execution_leakage.py`, `tests/unified_live/test_leakage.py` theo
  đường bị ảnh hưởng; không chỉ kiểm happy path của UI.
- F11: kiểm một upstream/point, dependency once/repeat, common projection,
  native parity, resource thiếu, short=CASH, net target oracle, NA, prompt
  backtest <6.500 ký tự/BRPP ≤600 (Original realtime bỏ trần tổng theo yêu cầu
  người dùng), retry/UNKNOWN/resume/stop và đồng thời hai job khác
  cấu hình. Browser kiểm cả sáu lựa chọn, advanced controls, offline/new run,
  empty/error/partial, export và mobile; fixture/mock trước API thật.
- Bốn gate lịch sử chỉ viện dẫn đúng source/runtime/receipt. Thay code thì
  chạy phần bị ảnh hưởng và ghi giới hạn gate cũ; không tự chạy toàn suite,
  compileall hoặc full research chỉ để đổi trạng thái checklist.

## 7. Số lượt chạy và API còn cần

| Giai đoạn | Chạy full mới | API LLM mới |
| --- | ---: | ---: |
| Audit và plan này | 0 | 0 |
| Cập nhật bài/bảng/hình/reviewer từ U09 | 0 | 0 |
| Đọc U09 và phát triển UI/test bằng fixture/replay | 0 | 0 |
| Kiểm live sau khi runner mới hoàn thiện | Smoke có phạm vi chốt trước | Tính theo dependency closure và request thực tế, không chạy lại 102 điểm mặc định |

Không cần chạy lại full U08 để viết bài hoặc hiển thị kết quả. Nếu chỉ thay
trình bày, không cần tạo lại response. Sau khi đổi serving backend, smoke API
thật chỉ kiểm đường tích hợp mới và tính sẵn budget trên payload/resources
đã hoàn thiện; không lấy grant U08 cũ hoặc quota còn lại làm quyền mở lượt mới.

Với **P điểm**, **R Decision repeat**, tập lựa chọn S và dependency closure
C(S): có **P upstream executions**, tối đa **P × R × |C(S)| Decision slots**;
số request thực tế nhỏ hơn khi fallback/bypass, lớn hơn số success khi retry.
Ví dụ chọn cả sáu bản chính kéo theo common + Fact_Anchor, tối đa tám Decision
slot/point/repeat, upstream vẫn một lần. Chọn riêng MT kéo theo common và
Fact_Anchor, tối đa ba Decision slot. Pattern/Trend thường là hai vision call
trên mỗi upstream ở đường research; các lời gọi phụ của đường live phải được
preflight đếm riêng, không mặc định mọi chế độ chỉ có hai lời gọi upstream.

U08 đã có 2.448 slot, **1.290 active raw Decision responses** và **1.702 HTTP
attempts** toàn ledger, trong đó 15 retired; các số này khác nhau có chủ đích.
Không dùng 2.448 làm số lượt full hoặc forecast fallback làm một API thành công.
Một nghiên cứu mới về ablation, nhiều upstream realization hoặc prospective
cohort cần protocol/budget riêng; không phải điều kiện ngầm để hoàn tất kế
hoạch cập nhật bài và ứng dụng này.
