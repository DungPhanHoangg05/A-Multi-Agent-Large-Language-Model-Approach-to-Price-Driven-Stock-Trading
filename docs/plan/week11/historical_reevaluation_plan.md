# Checklist đánh giá lại trên dữ liệu lịch sử

Cập nhật08/11/2026. Thực hiện lại quy trình đầy đủ đã dùng trước đây,
ưu tiên độ tin cậy và khả năng tái lập. Train lại model dưới tên
`MT_BICL_replica_full_r1`; bỏ phương án một seed/dừng sớm.
H02 đã bổ sung dữ liệu, bank và CLI replica; chờ người dùng chạy các bước
fit/pilot/train theo [lệnh bàn giao](README.md#lệnh-chạy-h02). Chưa fit teacher,
chưa chạy GPU hoặc đánh giá model mới.

## Checklist tổng

- [x] H01 — Khảo sát nguồn và phạm vi đánh giá.
- [ ] H02 — Hoàn thiện dữ liệu và train lại model; phần audit đã xong.
- [ ] H03 — Khóa protocol và ngân sách đánh giá.
- [ ] H04 — Hoàn thiện adapter và runner.
- [ ] H05 — Kiểm thử các phần thay đổi.
- [ ] H06 — Freeze và smoke test.
- [ ] H07 — Chạy đủ ma trận đánh giá.
- [ ] H08 — Phân tích và đối soát kết quả.
- [ ] H09 — Kết sổ và bàn giao.

## H01 — Khảo sát nguồn và phạm vi

- [x] Audit donor `fix@9efd23f4157e0d3ab8069fccab7dccf03439a714`.
- [x] Đối soát9 CSV,51 scope,102 anchor và lưới1.020 unit/120 ngày.
- [x] Xác định sáu primary:Original_common, bayesian_v1, C2, A_tp_pool,
  B_semantic, MT_BICL; Fact_Anchor là dependency của MT_BICL.

## H02 — Chuẩn bị dữ liệu và model

### Dữ liệu

- [x] Archive21 blob nguồn, lưu donor commit/blob OID/SHA256.
- [x] Kiểm label bridge1.020 cycle với engine; sai số lớn nhất0.
- [x] Đối soát frozen news155 membership/154 bài và suffix BHN từ14/09/2022.
- [x] Bổ sung VNINDEX tới30/09/2026:2181 phiên,249 phiên overlap khớp đủ OHLCV,
  không thiếu ngày của grid; giữ snapshot/provenance riêng, không sửa prefix cũ.
- [x] Audit raw/đơn vị/quyền/lịch9 mã:18 cycle có rào chắn quyền; BHN giữ suffix673.
  Lưu [audit mới](../../../outputs/historical_reevaluation/h02_data_r1/execution_audit.json);
  vẫn `VENDOR_SERIES_LIMITED`/`PENDING_EXECUTION_DATA`, chưa chứng nhận fill.
- [ ] Kiểm lại dữ liệu context/retrieval, membership và khả năng tái dựng
  scaler/regime từ train; ghi rõ asset nào còn thiếu trong readiness.

### Train lại MT-BICL theo quy trình đầy đủ

- [x] Khóa [protocol replica/source/data/RNG](mt_bicl_replica_full_r1.json) trước fit. Dùng recipe tại Git
  `00b24679f63d491c15cda6be0bc9a2c412651f93`: `protocol_v2.json`,
  `protocol_v2_1.json`, `corpus_manifest_v2.json` trong `docs/plan/week10/`
  và simulator tương ứng. Port có chọn lọc sang code hiện hành, không né guard.
- [x] Hoàn thiện CLI `scripts/run_mt_bicl_replica.py` chuẩn bị/pilot/train/resume/evaluate/verify;
  tests fixture PASS, các giai đoạn production chưa chạy. Dùng namespace
  `outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/`, manifest và hash mới;
  giữ nguyên model manifest, receipt và kết quả cũ.
  Có `repair-lock`/`check-lock` cho owner released khác signature trước fit;
  không cho phục hồi kiểu này khi đã có output teacher/pilot/train.
- [ ] Dựng bank CORE4 từ raw2018–2022; tách train≤2020, chọn checkpoint2021,
  kiểm cuối2022. Teacher/feature pool/scaler chỉ dùng train; HMM giữ recipe
  prefix và model cuối2020. Bank đã PASS1235/1640 cycle, train731 cycle/48 task;
  context/HMM thực chờ lệnh `prepare`, chưa đánh dấu hoàn tất toàn mục.
- [ ] Fit teacher Beta–Bernoulli16 grid point, MAP-EM tối đa1.000 vòng,
  convergence<10⁻¹⁰; kiểm oracle độc lập≤10⁻¹² và prior-predictive1.000 draw.
  Không hội tụ thì dừng, không dùng uniform fallback.
- [ ] Dựng và seal corpus theo recipe cũ, tách RNG train/pilot/validation/test.
  Validation/test mỗi tập5.000 episode gồm4.500 IID+500 stress;
  validation_swap/test_swap mỗi tập5.000 cặp. Không dùng query-y làm input/loss.
- [ ] Chạy GPU preflight100 step và cả hai pilot LEGACY_X_Y_69/PAIRED_37,
  tiny32,500 step/pilot; PAIRED mean KL cuối<0,001. Kiểm gradient query-only
  và resume; bỏ weights preflight/pilot trước train chính.
- [ ] Train đủ ba seed **17,42,73**, mỗi seed **5.000 optimizer step**,
  effective batch128; checkpoint mỗi250 step: **60 checkpoint tổng cộng**.
  Không dừng sớm khi vừa đạt validation; không thay seed hoặc nới gate.
- [x] Khóa student PAIRED_37,2 lớp/hidden128/4 head/FF256/dropout0,
  float32 và AMP/TF32 OFF. Giữ AdamW/lịch warmup250+cosine hiện hành;
  physical batch128/64/32 chọn trước train theo OOM, accumulation giữ batch128.
  Đã kiểm tương thích serving và optimizer/RNG resume bằng fixture CPU.
- [ ] Đánh giá đủ60 checkpoint trên synthetic validation/swap và thị trường2021.
  Giữ gate mean KL≤0,02, P95 error≤0,10, swap sign≥0,90 với≥200 cặp có
  |Δq|≥0,05; kiểm constant/context-blind và teacher-too-flat. Thiếu support
  hoặc lỗi kỹ thuật phải ghi rõ, không âm thầm loại để chọn model khác.
- [ ] Sau đủ ba seed, chọn checkpoint eligible theo thứ tự:
  macro log loss2021 → macro Brier2021, cả hai làm tròn12 chữ số → step nhỏ hơn
  → seed order17/42/73. Lưu best từng seed và global candidate; seal selection.
- [ ] Chỉ sau seal mới chạy synthetic_test/test_swap và diagnostic thị trường2022,
  báo các ablation và đủ đường cong ba seed. Test fail thì không reselect
  hoặc train tiếp dựa trên test; không có candidate đạt gate thì không release.
- [ ] Export candidate/teacher, cold replay CPU, kiểm fingerprint và đóng băng
  weights/scaler/regime; chỉ cập nhật readiness sang READY theo phạm vi đã kiểm.
  Ghi rõ replica tạo năm2026, dữ liệu lịch sử đã exposed và không bảo đảm lợi nhuận.

Train teacher/student dùng dữ liệu local và0 LLM call, có thể bắt đầu sau
khóa protocol replica mà không chờ VNINDEX2026. Chỉ đánh dấu phần model
hoàn tất khi toàn bộ checklist train PASS; toàn H02 còn cần checklist dữ liệu.
Mọi fit/pilot/train production do người dùng chạy theo chỉ đạo; frozen
validation/test và cold replay dùng CPU cùng runtime để so raw logits chính xác.

## H03 — Khóa protocol và ngân sách

- [ ] Khóa sáu primary và model replica; CORE4 gồm480 unit, EXTENDED gồm1.020
  unit/9 mã/6 block; giữ102 anchor và eligibility BHN, không chọn theo payoff.
- [ ] Khóa recipe từng phương pháp, ablation/control, membership D/C/query,
  train-only scaler, missing support/fallback và prequential memory `exit<t`.
- [ ] Khóa LONG Open(t+1)→Close(t+3), SHORT=CASH, phí0,25%/slippage0,10%
  cả hai chiều; labels qua `compute_round_trip_net_return`, fractional shares,
  risk OFF, reset50 triệu/mã/block/repeat. Đồng bộ JSON còn `lot=100`.
- [ ] Khóa model Decision `openai/gpt-oss-20b`, vision `qwen/qwen3.8-27b`,
  temperature0, max_tokens960/960 và schema; đồng bộ JSON còn2048/1024.
- [ ] Khóa3 Decision repeat/unit, Original_duplicate,10 ablation/3 retrieval
  control trên102 anchor; panel51 unit thêm realization1/2 và3 repeat/mỗi realization.
- [ ] Chốt số historical upstream H, token/quota/chi phí/thời gian thực tế;
  đối soát nominal27.846 Decision+2.244 vision+2H = **30.090+2H calls**,
  chưa gồm smoke/control/retry/unknown; không tính CPU/GPU train thành API call.
- [ ] Khóa estimand macro đều mã/block, bootstrap10.000 draw seed20261107,
  family5 contrast với Original và CI đồng thời centered max-deviation,
  quantile linear; BA family riêng, mục tiêu half-width1 đpt return/3 đpt BA.

## H04 — Hoàn thiện adapter và runner

- [ ] Mở universe9 mã và lịch2023–2026 bằng adapter riêng; kiểm parity CORE4/OOD5 mã.
- [ ] Dựng context/bank theo recipe từng phương pháp, nhãn engine và PIT;
  query outcome chỉ đọc sau forecast/checkpoint durable, retrieval `exit<query`.
- [ ] Kiểm sentiment count/score/mask và coverage toàn lưới; giữ date-only khả dụng
  ngày sau, loại tin không ngày/tương lai; không claim archived content khi chưa có.
- [ ] Chạy upstream một lần/unit/realization rồi deep-copy cho các nhánh;
  lưu parent/hash/ảnh, đủ5 factor rows và resolve Original→Fact_Anchor→MT_BICL.
- [ ] Hoàn thiện CLI run/resume/verify, ledger/cache riêng, retry/unknown reserve,
  checkpoint mỗi unit và kiểm `previous_exit < next_entry` khi stride3.

## H05 — Kiểm thử theo phạm vi

- [ ] Chạy tests bị ảnh hưởng:label/cost, suffix/index, PIT/news/query-y poison,
  exit==query, D/C/query rời nhau, scaler/regime, symbol/OOD và model fingerprint.
- [ ] Kiểm paired/deep-copy, factor rows/prompt, cache identity, retry/checkpoint/
  resume và metric/bootstrap oracle; chỉ compile Python mới/đổi.
- [ ] Ghi kết quả và phạm vi PASS; không chạy full suite/E2E nếu không được yêu cầu.

## H06 — Freeze và smoke test

- [ ] Neo Git source/runtime/model/data/protocol/IDs; kiểm manifest/hash trước API.
- [ ] Smoke đủ sáu primary/Fact_Anchor và longest prompts:BRPP≤600, prompt<6.500,
  giữ distill/cap, utility4.096 draws và factor rows/ảnh; không đổi fallback/model ngầm.
- [ ] Kiểm schema/options/quota năm organization, retry wrapper và credential scope;
  chỉ release lượt inference mới khi các gate áp dụng PASS.

## H07 — Chạy đánh giá

- [ ] Thu bank/shared state cần thiết, CORE4 rồi các mã bổ sung, ablation/control
  và panel upstream; đủ repeat/realization đã khóa, không vote hoặc chọn best repeat.
- [ ] Checkpoint/resume cùng identity; xử lý pending/error/unknown có ledger;
  không đổi lỗi thành CASH hoặc dừng khi kết quả vừa dương.
- [ ] Kết sổ đủ ma trận và hash raw/forecast trước mở payoff để phân tích.

## H08 — Phân tích kết quả

- [ ] Dựng lại accounts từ saved actions; báo return/D, MDD daily/cycle-end,
  exposure/turnover/phí, accuracy/BA/MCC/F1/recall và undefined=null.
- [ ] Báo đủ sáu primary, ablation, Fact_Anchor, numeric baselines và student−teacher;
  phân rã raw→facts→veto, support/missingness/OOD, strata, latency và chi phí.
- [ ] Tính CI đồng thời, leave-one-block/symbol-out và từng repeat; giữ kết quả âm,
  LOW_PRECISION và scope exploratory. Chỉ dùng probability đúng event contract.
- [ ] Cold consumer độc lập dựng lại account/metric/report từ raw/forecast/labels
  khớp hash; giữ riêng claim vendor simulation và economic acceptance.

## H09 — Kết sổ

- [ ] Cập nhật checklist tại đây và [README W11](README.md#checklist-đánh-giá-lại).
- [ ] Đóng gói evidence/manifest và hướng dẫn tái lập; giữ receipt/model cũ nguyên byte.
- [ ] Chỉ đánh dấu hoàn thành khi đủ output và kiểm tra của task; thiếu thì giữ
  TODO/BLOCKED với lý do. Lượt cập nhật plan này chỉ kiểm diff/link/recipe/số liệu,
  không chạy lại compile/unit/E2E/leakage vì chỉ đổi Markdown theo AGENTS1.2.
