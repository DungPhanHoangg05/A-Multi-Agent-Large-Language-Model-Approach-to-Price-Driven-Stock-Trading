# Kế hoạch đánh giá lại trên dữ liệu lịch sử từ nhánh fix

Cập nhật08/11/2026. Hệ thống gồm Bayesian Prior v1, Bayesian Prior v2 với
đại diện C2, Bayesian Prior cải tiến A/B và MT-BICL.
[Checklist hiện hành](README.md#checklist-đánh-giá-lại) quản lý H01–H09.
H01/H02 đã hoàn tất audit; readiness còn blocker, H03–H09 chưa triển khai.
Theo chỉ đạo08/11/2026, model gốc không tìm thấy: **chuyển sang train replica
MT-BICL nhanh theo mục4.1**, không tiếp tục chờ phục hồi weights cũ.
Lượt cập nhật này chỉ sửa kế hoạch; chưa fit teacher, train hoặc gọi API.

## 1. Phạm vi và registry

Hệ gốc Original là đối chứng chung. Mọi phương pháp giữ trong report kể cả
khi kết quả âm hoặc không đạt nomination. Mỗi phiên bản có namespace và
hash source/model/input/prompt riêng; cùng dữ liệu và ngân sách inference.

| Nhóm phiên bản | Primary | Thành phần được giữ |
| --- | --- | --- |
| Bayesian Prior v1 | `bayesian_v1` | Memory Bank, regime retrieval, agent signals và BRPP |
| Bayesian Prior v2 | `C2` | Conditional statistics, shrinkage, split readiness và ranking |
| Bayesian Prior cải tiến A/B | `A_tp_pool`, `B_semantic` | Partition T/P và renderer tương ứng |
| MT-BICL | `MT_BICL` | Replica `MT_BICL_replica_fast_r1` sau nghiệm thu; frozen student/teacher, bucket context, facts, posterior utility và veto |

Primary có **6 nhánh**, gồm Original và5 cải tiến. Fact_Anchor là dependency
bắt buộc của MT-BICL trên toàn lưới. Các cấu hình nội bộ khác của Bayesian
Prior vẫn phục vụ kiểm thử hợp đồng; chúng không thêm phiên bản primary.

MT-BICL dùng các module `core/mt_bicl_*.py`, schema
`mt_bicl.schema.json`, cấu hình `mt_bicl_protocol.json` và model manifest
`mt_bicl_model.json` trong thư mục tuần này. Các thành phần teacher/student,
task/scaler/regime và shared prompt thuộc một phương pháp MT-BICL hiện hành.

## 2. Nguồn fix đã kiểm tra

Nguồn donor là `9efd23f4157e0d3ab8069fccab7dccf03439a714`. Import chọn
lọc bằng Git blob vào `outputs/historical_reevaluation/inputs/fix/`, giữ
donor commit, blob OID, SHA256 và byte count. Archive hiện có21 blob nguồn.

| Nguồn trong fix | Hợp đồng cần tái dùng |
| --- | --- |
| `scripts/freeze_revision_prices.py`, `r1_prices_v1/manifest.json` | Snapshot giá, hashes, thời điểm tải và adjustment |
| `core/revision_baselines.py` | Kiểm OHLC, suffix BHN, nhãn net và purge |
| `core/revision_common_study.py` | Shared state, prefix query và frozen sentiment |
| `core/revision72_data.py` | Sáu khối lịch sử, lịch102 unit và news availability |
| `core/revision_r2_panel.py` | Kiểm ngày thật, warmup và label maturity |
| `core/revision_minimal_bank.py` | Parent/hash và điều kiện cache reuse |
| `sentiment_inventory_v1/summary.json`, `sentiment_coverage_v1/summary.json` | Scorer provenance và coverage |
| `chart_convention_v1/report.json`, `r4_final_v1/manifest.json` | Convention ảnh và đủ factor rows trong prompt |
| `final_temporal_v1/contamination.json` | Exposure lịch sử và scope exploratory |
| `utils/target_contract.py`, `core/revision_execution_final.py` | Entry/exit, label net và ledger |

Các đường output rút gọn trong bảng nằm dưới `outputs/revision/`.
Các tên A/B của factorial fix phải có mapping độc lập với A_tp_pool/B_semantic.

### Giá và lịch

Snapshot VCI/vnstock tải01/11/2026 có9 mã BHN, CMG, FPT, HVN, MBB, MWG,
VCB, VJC, VNM, mỗi mã1.681 dòng từ02/01/2020 tới30/09/2026. Đã kiểm9/9
CSV từ Git khớp manifest. Snapshot là chuỗi vendor tải hồi cứu; adjustment
và ledger quyền/cổ tức chưa được chứng nhận đầy đủ.

BHN có OHLC mâu thuẫn ngày13/09/2022. Giữ raw, dùng suffix từ14/09/2022,
bỏ673 dòng prefix theo policy fix. BHN thiếu600 nến sạch ở ba khối đầu.
Eligibility dựa input/warmup, không dựa lợi nhuận.

| Khối | Train tới | Test start | Số mã |
| --- | --- | --- | ---: |
| b2023_h2 | 31/03/2023 | 03/07/2023 | 8 |
| b2024_h2 | 31/03/2024 | 01/07/2024 | 8 |
| b2025_h1 | 30/09/2024 | 02/01/2025 | 8 |
| f2025_q4 | 30/06/2025 | 01/10/2025 | 9 |
| f2026_q2 | 31/12/2025 | 01/04/2026 | 9 |
| f2026_q3 | 31/03/2026 | 01/07/2026 | 9 |

Validation nằm sau train và mọi label phải exit trước test. Tên khối h2
là ID donor; các cutoff thực của hai khối này nằm trong quý III.

### Tin và LLM

Cache legacy có180 record/177 identity;155 record qua kiểm nguồn/ngày.
Scorer lịch sử của180 record đều unknown. Fix chấm lại154 identity bằng
ViSoBERT revision `d7738b85200272f10ba8b048d80236c8c582b581`,
mapping0 NEG/1 POS/2 NEU, tạo155 membership bài–mã.
Date-only khả dụng từ ngày sau, cửa sổ90 ngày, tối thiểu3 bài.

Trên102 cutoff có23 đủ ngưỡng bài và79 missing; downstream normalizer chỉ
đánh dấu9 reliable. H04 phải đối soát count/score/mask qua cả hai lớp.
Archived publication content chưa được chứng nhận PIT đầy đủ.

Indicator/Alpha backtest tính bằng Python, Pattern/Trend dùng vision.
Fix có sửa convention ảnh và lỗi nén làm mất factor rows. Mỗi prompt cần
kiểm đủ tên, giá trị và mask của5 factor rows, cùng ảnh và parent state.

Toàn bộ thời điểm giá/nhãn đều trước inference của fix. Dữ liệu lịch sử
đã exposed và served-weight revision chưa được xác minh; kết quả historical
mới được phân loại exploratory. Cohort forward cần release riêng.

## 3. Cohort và dữ liệu chung

Giữ102 anchor donor để kiểm mapping. Mở rộng mỗi scope thành20 cutoff,
`decision_i=first_decision+3*i`, i=0..19. Audit đã đối soát **51 scope,
1.020 unit và120 ngày cutoff**,51/51 endpoint khớp donor, đủ target t+3.

- **CORE4 primary** gồm FPT/MWG/VCB/VNM,6 khối,480 unit. Macro đều bốn mã
  trong block, rồi đều sáu block.
- **EXTENDED secondary** gồm1.020 unit của9 mã eligible. Báo riêng540 unit
  của năm mã bổ sung và mask BHN. Hai cohort có giao nhau.
- Lỗi API/code là pending/error. Thiếu support prior/utility giữ ID và dùng
  fallback đúng recipe đã khóa. Kết quả chỉ COMPLETE khi đủ toàn bộ G.

Stride3 có thể cho exit trước trùng ngày decision sau; vị thế sau vào Open
phiên kế tiếp. Ledger kiểm `previous_exit < next_entry`; retrieval kiểm
`exit_date < query_date`. Adapter cần test boundary này vì audit decision
span của fix chặt hơn khi chạm ngày.

Mọi query thấy nến≤t, tin available≤t và observation exit<t. D/C/query rời
nhau, chronological, không lặp observation ở nhiều task. Lưu membership IDs,
max exit, scaler/model hashes, K/m, OOD và fallback reason.
Query outcome chỉ đọc sau forecast/checkpoint durable.

Availability pool mở rộng theo logical cutoff t cho mọi phương pháp.
Outcome của test trước chỉ vào memory query sau khi exit<t; dữ liệu fit
teacher/scaler/regime dừng ở train, selection replica không dùng outcome
lưới2023–2026. Teacher/student đóng băng sau nghiệm thu replica. HMM giữ
recipe KLTN và prefix decoding; regime SMA/volatility/liquidity của fix là
strata mô tả riêng. Schema và input encoding của MT-BICL giữ bốn feature,
K≤3, m≤8; adapter chín mã cần parity trên bốn mã và kiểm OOD trên năm mã mới.

Labels sinh bằng `compute_round_trip_net_return`, đối chiếu độc lập
`target_fields` của fix. LONG vào Open(t+1), đóng Close(t+3), SHORT giữ CASH;
phí0,25% và slippage0,10% cả hai chiều, fractional shares và risk OFF.

## 4. Asset và data readiness

[Readiness máy](../../../outputs/historical_reevaluation/manifests/asset_readiness.json)
được tạo/cold-verify bằng `scripts/prepare_historical_assets.py`.
Gói model MT-BICL có candidate tensor và teacher pi pin hash; nạp qua
`core.mt_bicl_adapter.StudentAdapter`. Model gốc hiện thiếu cả hai component.
Theo chỉ đạo mới, dựng gói replica riêng theo mục4.1; không yêu cầu hash mới
trùng hash model gốc và không dùng teacher thay student khi kiểm thất bại.

H02 cần nghiệm thu gói replica mới, VNINDEX2026 và dữ liệu context/retrieval.
Các source/data guards còn hard-code bốn mã cần adapter universe tường minh
trong H04. Model/scaler chỉ dùng dữ liệu được recipe cho phép trước test.

Snapshot vendor đang mang `VENDOR_SERIES_LIMITED`; economic acceptance giữ
`PENDING_EXECUTION_DATA`. Kiểm quyền/chia tách/cổ tức, đơn vị giá/volume,
lịch và từng holding span trên9 mã. Đối chiếu theo ngày với execution source
hiện có; mọi splice hoặc dataset revision phải có provenance và dùng đồng
bộ mọi phương pháp. Không sửa nhãn riêng một nhánh để thay kết quả.

Kết quả đã lưu của MT-BICL có D=−5,313090 đpt so Original và
NOT_NOMINATED trên development60 điểm. Đây là kết quả cũ của phương pháp,
không là kết quả lưới1.020 điểm. Dữ liệu raw/report cũ thiếu một phần; kết
luận của lượt áp dụng lại phải có receipt và cold replay mới.

### 4.1. Train lại replica theo đường nhanh

**Quyết định08/11:**không chờ thêm model gốc. Triển khai một lượt
`MT_BICL_replica_fast_r1`, giữ sáu primary; cột `MT_BICL` phải ghi rõ model
ID/hash replica trong registry và report. Đây là replica rút gọn lịch train/
selection, không là khôi phục nguyên byte hoặc tái lập đủ ba seed của run cũ.
Kết quả NOT_NOMINATED cũ giữ nguyên như reference, không gán cho weights mới.

**Đường găng bắt đầu từ dữ liệu local:**bank raw CORE4 giai đoạn2018–2022,
VNINDEX đang có, primitive engine/features/scaler/teacher/student hiện hành.
Teacher và feature pool chỉ dùng cycle hợp lệ có exit≤31/12/2020; không đưa
năm2022 hoặc outcome2023–2026 vào fit/selection để bù support. Không cần
historical agent signals, vision/Decision API, VNINDEX2026 hoặc universe
chín mã để train teacher/student. Dữ liệu2026 và bằng chứng execution tiếp
tục là dependency riêng cho đánh giá toàn lưới; không trì hoãn train vì chúng.
R1 chỉ materialize train view trước; bank/query outcome2021–2022 dành cho
diagnostic được mở sau selection seal, không chạy builder mặc định mở toàn
bank2022 rồi gọi đó là train-only.

| Thứ tự | Việc cần làm ngay khi triển khai | Điều kiện chuyển bước |
| --- | --- | --- |
| R0 Khóa recipe | Protocol replica máy, source/data/membership/RNG hashes, profile và rule dừng dưới đây; neo Git trước fit/optimizer | Đủ train support; oracle/packing/leakage và checkpoint/resume theo phạm vi PASS |
| R1 Chuẩn bị CPU | Dựng bank/scaler train-only; fit teacher; tạo/cache corpora và q oracle đúng recipe | Teacher hội tụ, oracle độc lập sai số≤10⁻¹²; seal input/corpus trước student |
| R2 Preflight | Đo trainer thật trên GPU hiện có, batch128; tiny-fit PAIRED_37 duy nhất, gradient query-only và resume check | Tiny32 đạt mean KL<0,001 ở checkpoint250 hoặc500; weights preflight/pilot bỏ đi |
| R3 Train nhanh | Seed42 duy nhất, tối đa5.000 step, kiểm checkpoint mỗi250 step | Dừng ngay checkpoint đầu tiên đạt toàn gate validation; không tìm checkpoint tốt nhất theo lợi nhuận |
| R4 Freeze/verify | Seal selection trước test; export candidate/teacher và kiểm test cố định/cold CPU replay | Test và integrity PASS mới khóa manifest replica, weights/scaler/teacher frozen |

**Profile đã chọn để giảm thời gian:**

- Giữ `DistilledStudent`:2 lớp, hidden128,4 head, FF256, dropout0,
  paired tối đa37 token và bốn feature. Float32, AMP/TF32 OFF, không ensemble.
- AdamW lr3e−4, betas0,9/0,999, eps10⁻⁸, weight decay0,01, clip1.
  Effective batch128; preflight chọn physical128, chỉ xuống64/32 nếu OOM,
  accumulation2/4 giữ effective batch. Khóa lựa chọn trước train chính.
- Giữ `scheduled_lr` hiện có:250 step warmup, cosine theo horizon5.000 về
  3e−5. Không nén scheduler theo thời điểm early stop. Seed42, train episode
  ID=`(step−1)*128+i`; tối đa640.000 episode, sinh theo batch và cache q.
- Chỉ distill synthetic từ teacher posterior D/C; loss tại query duy nhất.
  Không dùng latent thật hoặc query-y làm target, không trộn BCE thị trường.
  Không chạy lại pilot LEGACY_X_Y, ba seed hoặc hyperparameter search.
- Checkpoint gồm model/optimizer/step, RNG và input identity; resume đúng
  UUID/hash, không sinh lại stream mới. Cache tensor/corpus/q, tránh parse
  JSON hoặc tính lại teacher trong mỗi epoch; mọi tối ưu phải giữ parity.
  Giữ utility4.096 draws và mọi hợp đồng inference khi áp dụng replica.

**Corpus và rule dừng khóa trước optimizer:**dùng recipe simulator cũ tại
`00b24679f63d491c15cda6be0bc9a2c412651f93`, file
`core/mt_bicl_v2_simulator.py` (SHA256
`e1156d4ead4f4696616b54f4a5db3719de80627198313b9104de1e4270781727`)
và `docs/plan/week10/corpus_manifest_v2.json` (SHA256
`28292984f0a320533dd288a197f97d0536272750534d87103b92e0a37154489f`).
Đọc bằng Git pin để port có chọn lọc sang replica; không phục hồi nguyên
runner cũ hoặc monkey-patch né guard. Hiện có primitives fit/optimizer,
nhưng chưa có CLI trainer/simulator replica hoàn chỉnh; R0 phải bổ sung.

Giữ cấu trúc K=0..3, m=0..8, mỗi prior2..8 observation, sampling feature
train-only và mixture4.500 IID+500 stress. Validation/test mỗi tập5.000
episode; validation_swap/test_swap mỗi tập5.000 cặp A/B, giữ cấu trúc/x/C/
query và chỉ thay nhãn prior theo swap recipe. Khóa stream seed/component domain riêng theo manifest
replica, tách train/preflight/pilot/validation/test và domain RNG của run
lịch sử; không redraw để tăng support. Feature pool cũ kỳ vọng731 cycle/
48 task nhưng phải tái tính và kiểm membership/hash từ raw; không giả đủ
731 bằng cách điền bù hoặc hard-code nhãn.

Tại step250,500,…,5.000, candidate eligible khi technical PASS, mean
KL(oracle||student)≤0,02 nat, P95 |p_student−q|≤0,10 trên5.000 validation,
và swap sign agreement≥0,90 trên ít nhất200 cặp có |Δq|≥0,05.
Zero student delta tính disagree khi oracle khác0. Constant/context-blind
controls và teacher-too-flat check giữ nguyên: constant đạt cả KL/P95
hoặc swap thiếu support thì INCONCLUSIVE, không release. Báo riêng IID,
stress, K/m và controls; không thay aggregate gate sau xem kết quả.

Chọn **checkpoint eligible đầu tiên theo step**, dừng optimizer, seal
selection rồi mới forward synthetic_test/test_swap. Test áp dụng cùng gate
và kiểm độc lập; fail thì STOP, không quay lại train/reselect bằng test.
Không có candidate tới5.000 thì `NO_ELIGIBLE_CHECKPOINT`; không tăng seed,
step hoặc nới threshold trong cùng revision. Năm2021/2022 chỉ diagnostic
sau seal, không xếp hạng checkpoint; payoff lưới2023–2026 vẫn chưa mở.
Rule một seed/first-pass khác recipe lịch sử ba seed/đủ60 checkpoint;
report phải nêu giới hạn này và không claim ổn định qua seed. Reuse
validation nhiều checkpoint được công khai; test riêng giữ sau selection.
Seed42 được chọn trong bối cảnh đã biết lịch sử run cũ; test synthetic mới
chỉ kiểm gate cơ chế của replica, không xóa exposure hoặc tạo xác nhận
thị trường độc lập.

Teacher giữ16 grid point, MAP-EM tối đa1.000 vòng, convergence<10⁻¹⁰,
Dirichlet alpha2 và oracle tuần tự độc lập; không hội tụ thì dừng, không
uniform fallback. HMM/scaler tái dựng đúng recipe train≤2020 và kiểm hash;
không thay bằng artifact HMM fit cuối2022. Ngày tạo replica thực tế là2026;
data cutoff quá khứ không chứng minh model đã tồn tại trước test lịch sử.
Toàn bộ đánh giá tiếp tục exploratory/exposed.

**Artifact/release:**ghi riêng tại
`outputs/bayesian_benchmark/mt_bicl/replicas/fast_r1/`, gồm inputs, teacher,
corpora, training/checkpoints, model và verification. Khi triển khai tạo
`docs/plan/week11/mt_bicl_replica_fast_r1.json` và manifest model replica
riêng, neo Git trước consumer; giữ nguyên manifest/hash gốc và readiness
audit cũ. Loader phải bind đúng release/manifest mới, không dùng đường dẫn
manifest tùy ý để né source guard. Candidate/teacher mới có SHA riêng;
H03 map primary MT_BICL sang gói mới sau R4, các ablation dùng cùng gói.

**Ưu tiên thời gian:**R0→R4 chạy tuần tự và checkpoint durable; không chờ
H03 inference budget toàn lưới mới chuẩn bị teacher/student. Khóa protocol
replica và kiểm theo phạm vi trước fit là gate kỹ thuật, không yêu cầu tìm
lại model gốc hoặc xin lại lựa chọn train replica đã được chỉ đạo. Đo wall
time gồm sinh corpus/oracle, train, validation, I/O và cold verify sau
preflight; công bố ETA từ trainer thật, không hứa số phút từ benchmark
proxy cũ. Tối đa5.000 step là trần công việc, không phải cam kết thời gian.
Training teacher/student cần0 LLM API call. Quỹ research30.090+2H ở mục5
không cộng nhầm CPU/GPU train thành API usage.

**Phạm vi lượt cập nhật08/11:**chỉ Markdown; chưa tạo protocol/model
manifest replica hoặc đổi các cờ `training_allowed=false` trong JSON hiện
có. Chỉ đạo mới được ghi thành kế hoạch R0–R4; triển khai phải dùng release
replica đúng phạm vi thay vì bật quyền toàn bộ protocol cũ. Đã đối soát
recipe/source/hash, arithmetic và liên kết; không chạy compile/unit/E2E/
leakage suite vì không đổi code/test/runtime/schema/input theo AGENTS1.2.

## 5. Inference và repeats

Đề xuất Decision `openai/gpt-oss-20b`, vision `qwen/qwen3.8-27b`,
temperature cấu hình0 và max_tokens960 cho cả hai. Lưu metadata thực, gồm
trường hợp SDK chuyển temperature thành1e-8. Đây là common contract mới.

Preflight kiểm schema, longest prompts, quota ITPM/OTPM/RPM/RPD/TPD và năm
organization `GROQ_ORG_1_API_KEY`…`GROQ_ORG_5_API_KEY`.
Log scope HMAC; API qua `_invoke_with_retry`, reserve đúng output budget,
backoff theo provider, checkpoint durable. Đổi options cần revision mới
đồng bộ panel; không đổi model/key ngầm.

Upstream chạy một lần/unit/realization, deep-copy sang mọi nhánh. Giữ
`_distill_report`, `_cap_report`, BRPP≤600 ký tự với K=3, prompt<6.500.
Reuse chỉ khi source/prefix/news/renderer/model/options/schema/payload và
parent hashes cùng contract. Cache2048/1024 của donor không được mặc định
coi tương đương contract960.

Chạy3 Decision executions mỗi unit trên upstream realization0, báo cả ba
và mean metric; không vote hoặc chọn best. Original chạy trước, Fact_Anchor
sau để resolve a0/proof, rồi MT-BICL revision. Các nhánh khác counterbalance.

Panel upstream chọn1 unit/scope bằng metadata/hash,51 unit. Thêm
realization1/2 và3 Decision repeats trên mỗi realization; mọi nhánh vẫn dùng
cùng upstream trong realization. Không đếm repeats thành N thị trường.

| Hạng mục nominal trước bypass/reuse | Công thức | Calls |
| --- | --- | ---: |
| Primary và Fact_Anchor | 1.020×7×3 | 21.420 |
| Ablation102 anchor | 102×10×3 | 3.060 |
| random/recent/similarity | 102×3×3 | 918 |
| Original_duplicate độc lập | 102×3 | 306 |
| Upstream panel bổ sung | 51×2×7×3 | 2.142 |
| Tổng Decision | Tổng năm dòng trên | 27.846 |
| Vision query/panel | 2×(1.020+51×2) | 2.244 |
| Vision historical bank | 2×H | Chốt H trong H03 |

Tổng nominal **30.090+2H research calls**, chưa gồm smoke/control/retry/
rejected/unknown. H là số historical upstream duy nhất còn cần dựng.
H03 phải chốt H, token/cost/RAM/quota và tính khả thi trước release.

Mười ablation LLM gồm stats/examples của C2/A/B và Plain_revision,
No_utility, No_target, Stats_only của MT-BICL. Fact_Anchor đã có trên toàn
lưới. Utility-only, student/teacher numeric và CASH/always-LONG chạy offline.
MT-BICL giữ utility4096 draws và common random streams; No_target phải
recompute posterior/student theo membership đã bỏ C.

## 6. Đo hiệu quả và uncertainty

Tài khoản reset50 triệu/mã/block/nhánh/repeat. Primary mỗi repeat tính
`D_j=mean_6_blocks(mean_4_symbols(R_j-R_Original))`, đơn vị đpt, rồi lấy
mean ba repeat. EXTENDED macro đều block rồi đều mã eligible trong block.
Không nối equity qua khoảng trống giữa sáu block.

Báo return/D, MDD/ΔMDD daily MTM và cycle-end riêng, LONG rate, exposure,
turnover, phí, số trade, confusion, accuracy, BA, MCC, macro-F1 và recall
hai lớp. Undefined giữ null. Strata gồm mã/block/regime/quý/K/m/missingness/
sentiment support, facts/utility support, OOD, latency và API cost.

Probability Brier/log loss/calibration chỉ cho đầu ra số có event contract
net-return-positive; confidence văn bản không là xác suất.
Đối chứng numeric gồm train-majority, momentum, logistic/factor cùng cutoff,
CASH/always-LONG cycles và continuous hold có ledger riêng.
Exposure-matched random chỉ fit trên train/calibration trước test.

Báo MT-BICL−Fact_Anchor/Plain/No_utility/No_target/Stats/Utility và phân rã
raw→facts→veto, cùng student−teacher gap. Bayesian full−stats/examples và
retrieval controls dùng cùng evidence. Giữ mọi contrast bất lợi.

Bootstrap10.000 draw seed20261107 trên whole time block, giữ toàn bộ mã,
method/repeat cùng block. Cùng draw indices cho mọi contrast.
Family primary gồm **5 contrast cải tiến−Original trên CORE4**.
Với draw b, `T_b=max_j(abs(D*_jb-D_j))`; CI đồng thời dùng
`D_j +/- quantile_0.95(T)`, quantile linear. BA có family riêng.
H03 khóa oracle cho ties, constant/null contrast và support thiếu.

Sáu block còn phụ thuộc thị trường; intervals historical là sensitivity có
điều kiện. Báo leave-one-block/symbol-out và từng repeat.
Mục tiêu precision đề xuất là half-width1 đpt cho D và3 đpt cho BA; mẫu cố
định chưa đạt thì LOW_PRECISION, không thêm mẫu chỉ để đổi dấu CI.
Candidate historical mang scope exploratory. Xác nhận độc lập cần cohort
forward/power/cluster plan và release khóa trước response đầu.

## 7. Checklist triển khai

| Bước | Đầu ra và điều kiện hoàn tất |
| --- | --- |
| H01 | Audit donor/source, registry và kế hoạch bốn nhóm hiện hành |
| H02 | Audit đã DONE; mở tiếp R0–R4 train replica nhanh, VNINDEX/context và blocker execution; chưa ghi READY khi thiếu gói nghiệm thu |
| H03 | Protocol máy, IDs/folds, inference/options, repeats, families và budget H; bind manifest replica R4 |
| H04 | Adapter/harness sáu primary, shared graph/history và symbol/OOD |
| H05 | Tests trực tiếp, PIT/leakage, economics/paired/retry/checkpoint và oracle |
| H06 | Freeze bank/runtime và smoke longest prompts/toàn registry |
| H07 | Collect CORE4, extension, ablation/retrieval và repeats đúng ma trận |
| H08 | Cold analysis/accounts/uncertainty/strata/cost |
| H09 | Receipt, README và bằng chứng với phạm vi kết luận đúng |

Namespace dữ liệu mới là `outputs/historical_reevaluation/`.
Model/runtime MT-BICL dùng `outputs/bayesian_benchmark/mt_bicl/`.
Cấu hình hiện hành ở trạng thái SPEC_ONLY; API evaluation chưa release.
Kế hoạch train replica đã được chỉ đạo; gate R0–R4 và release riêng cần
được triển khai trước chạy. H03 phải đồng bộ fractional shares của plan
với `economic_contract.lot=100` và max_tokens960 với2048/1024 còn lưu trong
JSON hiện hành; không để khác biệt này đi vào common inference contract.

Kiểm H05 bao gồm future/query-y poison, exit==query, suffix index, symbol/
OOD, strict net label, full factor rows, cache contract, unknown retries,
immutable model fingerprint và bootstrap oracle. Compile đúng file Python
thay đổi; các gate nguồn cũ chỉ được viện dẫn khi hash/phạm vi còn phù hợp.
