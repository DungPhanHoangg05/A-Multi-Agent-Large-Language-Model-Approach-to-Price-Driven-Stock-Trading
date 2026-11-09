# Kế hoạch so sánh các phương pháp bằng Groq Free

Cập nhật09/11/2026. Thực hiện lại quy trình đầy đủ đã dùng trước đây,
ưu tiên độ tin cậy và khả năng tái lập. Train lại model dưới tên
`MT_BICL_replica_full_r1`; bỏ phương án một seed/dừng sớm.
Người dùng đã hoàn tất fit/pilot/train:đủ3 seed/60 checkpoint, chọn seed42/
step3000. Test `MODEL_GATE_PASS`, cold replay đủ60 checkpoint
`CPU_REPLAY_MATCH`; H02 hoàn tất ở phạm vi audit dữ liệu và model.
H03 đã khóa protocol và dự toán trước inference trên lưới mới.
H04/H05 đã hoàn tất offline; H06 PASS live smoke55 lượt và cold verify.
Ngày09/11/2026, người dùng hủy lượt H07 đầy đủ để chuẩn bị trình bày trong
hai ngày. Phương án hiện hành FREE_PAIRED_PILOT_48 có trạng thái
READY_COLLECTION; smoke9/cold PASS, chưa thu48 điểm hoặc hoàn tất H07.
H01–H06 bên dưới ghi bằng chứng thiết kế cũ; pilot cần khóa protocol/input/
runtime và nghiệm thu phần thay đổi riêng trước API.

## Checklist tổng

- [x] H01 — Khảo sát nguồn và phạm vi đánh giá.
- [x] H02 — Audit dữ liệu và train lại model, nghiệm thu CPU và lưu asset.
- [x] H03 — Khóa protocol, lịch, model và dự toán đánh giá offline.
- [x] H04 — Hoàn thiện adapter và runner, nghiệm thu triển khai offline.
- [x] H05 — Kiểm thử theo phạm vi, PASS84 test và đối soát asset/context.
- [x] H06 — Smoke thiết kế cũ PASS; grant thu thập đầy đủ đã REVOKED ngày09/11.
- [x] H07 cũ — Dừng tiến trình và xóa output thu thập dở theo yêu cầu người dùng.
- [ ] H07 pilot — Audit reuse, khóa48 điểm, nghiệm thu và thu đủ sáu phương pháp.
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
- [x] Kiểm context248 query2021/256 query2022 và membership; scaler731 cycle
  có max exit29/12/2020, mọi model regime fit cutoff≤2020. Adapter9 mã thuộc H04.

### Train lại MT-BICL theo quy trình đầy đủ

- [x] Khóa [protocol replica/source/data/RNG](mt_bicl_replica_full_r1.json) trước fit. Dùng recipe tại Git
  `00b24679f63d491c15cda6be0bc9a2c412651f93`: `protocol_v2.json`,
  `protocol_v2_1.json`, `corpus_manifest_v2.json` trong `docs/plan/week10/`
  và simulator tương ứng. Port có chọn lọc sang code hiện hành, không né guard.
- [x] Hoàn thiện CLI `scripts/run_mt_bicl_replica.py` chuẩn bị/pilot/train/resume/evaluate/verify;
  tests fixture PASS; người dùng đã chạy production prepare/pilot/train. Dùng namespace
  `outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/`, manifest và hash mới;
  giữ nguyên model manifest, receipt và kết quả cũ.
  Có `repair-lock`/`check-lock` cho owner released khác signature trước fit;
  không cho phục hồi kiểu này khi đã có output teacher/pilot/train.
- [x] Dựng bank CORE4 từ raw2018–2022; tách train≤2020, chọn checkpoint2021,
  kiểm cuối2022. Teacher/feature pool/scaler chỉ dùng train; HMM giữ recipe
  prefix và model cuối2020. Bank đã PASS1235/1640 cycle, train731 cycle/48 task;
  context/HMM và byte hash đã được đối soát sau `prepare`.
- [x] Fit teacher Beta–Bernoulli16 grid point, MAP-EM tối đa1.000 vòng,
  convergence<10⁻¹⁰; kiểm oracle độc lập≤10⁻¹² và prior-predictive1.000 draw.
  Hội tụ237 vòng; oracle max error7,106×10⁻¹⁴, không dùng uniform fallback.
- [x] Dựng và seal corpus theo recipe cũ, tách RNG train/pilot/validation/test.
  Validation/test mỗi tập5.000 episode gồm4.500 IID+500 stress;
  validation_swap/test_swap mỗi tập5.000 cặp. Không dùng query-y làm input/loss.
- [x] Chạy GPU preflight100 step và cả hai pilot LEGACY_X_Y_69/PAIRED_37,
  tiny32,500 step/pilot; PAIRED mean KL cuối<0,001. Kiểm gradient query-only
  và resume PASS; PAIRED mean KL4,652×10⁻¹⁰, bỏ weights pilot trước train chính.
- [x] Train đủ ba seed **17,42,73**, mỗi seed **5.000 optimizer step**,
  effective batch128; checkpoint mỗi250 step: **60 checkpoint tổng cộng**.
  Không dừng sớm khi vừa đạt validation; không thay seed hoặc nới gate.
- [x] Khóa student PAIRED_37,2 lớp/hidden128/4 head/FF256/dropout0,
  float32 và AMP/TF32 OFF. Giữ AdamW/lịch warmup250+cosine hiện hành;
  physical batch128/64/32 chọn trước train theo OOM, accumulation giữ batch128.
  Đã kiểm tương thích serving và optimizer/RNG resume bằng fixture CPU.
- [x] Đánh giá đủ60 checkpoint trên synthetic validation/swap và thị trường2021.
  Giữ gate mean KL≤0,02, P95 error≤0,10, swap sign≥0,90 với≥200 cặp có
  |Δq|≥0,05; kiểm constant/context-blind và teacher-too-flat. Thiếu support
  hoặc lỗi kỹ thuật phải ghi rõ, không âm thầm loại để chọn model khác.
- [x] Sau đủ ba seed, chọn checkpoint eligible theo thứ tự:
  macro log loss2021 → macro Brier2021, cả hai làm tròn12 chữ số → step nhỏ hơn
  → seed order17/42/73. Global seed42/step3000; best seed17/73 đều step2500.
- [x] Chỉ sau seal mới chạy synthetic_test/test_swap và diagnostic thị trường2022,
  báo các ablation và đủ đường cong ba seed. Test fail thì không reselect
  hoặc train tiếp dựa trên test. `MODEL_GATE_PASS`; cả ba seed qua gate test.
- [x] Export candidate/teacher, cold replay CPU, kiểm fingerprint và đóng băng
  weights/scaler/regime; chỉ cập nhật readiness sang READY theo phạm vi đã kiểm.
  Gói [model replica đã nghiệm thu](mt_bicl_replica_full_r1_model.json) có weights,
  teacher, scaler và regime được neo Git; đủ60 checkpoint khớp raw logits/metrics.
  Ghi rõ replica tạo năm2026, dữ liệu lịch sử đã exposed và không bảo đảm lợi nhuận.

Train teacher/student dùng dữ liệu local và0 LLM call, có thể bắt đầu sau
khóa protocol replica mà không chờ VNINDEX2026. Chỉ đánh dấu phần model
hoàn tất khi toàn bộ checklist train PASS. Checklist H02 đã hoàn tất;
`PENDING_EXECUTION_DATA` vẫn là giới hạn nghiệm thu kinh tế, adapter9 mã thuộc H04.
Mọi fit/pilot/train production do người dùng chạy theo chỉ đạo; frozen
validation/test và cold replay dùng CPU cùng runtime để so raw logits chính xác.

## H03 — Khóa protocol và ngân sách

- [x] Khóa sáu primary và model replica; CORE4 gồm480 unit, EXTENDED gồm1.020
  unit/9 mã/6 block; giữ102 anchor và eligibility BHN, không chọn theo payoff.
- [x] Khóa recipe từng phương pháp, ablation/control, membership D/C/query,
  train-only scaler, missing support/fallback và prequential memory `exit<t`.
- [x] Khóa LONG Open(t+1)→Close(t+3), SHORT=CASH, phí0,25%/slippage0,10%
  cả hai chiều; labels qua `compute_round_trip_net_return`, fractional shares,
  risk OFF, reset50 triệu/mã/block/repeat. JSON hiệu lực mới có `lot=null`;
  protocol cũ giữ nguyên byte.
- [x] Khóa model Decision `openai/gpt-oss-20b`, vision `qwen/qwen3.8-27b`,
  temperature0, max_tokens960/960 và hai schema response; không dùng cache2048/1024.
- [x] Khóa3 Decision repeat/unit, Original_duplicate,10 ablation/3 retrieval
  control trên102 anchor; panel51 unit thêm realization1/2 và3 repeat/mỗi realization.
- [x] Chốt **H=2.358**, nominal27.846 Decision+6.960 vision=**34.806 calls**.
  Dự toán token/chi phí/thời gian từ telemetry cũ, tách smoke/retry/unknown;
  quota tài khoản và payload960 thực tế kiểm ở H06, không tự chuyển sang trả phí.
- [x] Khóa estimand macro đều mã/block, bootstrap10.000 draw seed20261107,
  family5 contrast với Original và CI đồng thời centered max-deviation,
  quantile linear; BA family riêng, mục tiêu half-width1 đpt return/3 đpt BA.

[Protocol máy](historical_evaluation_protocol.json) và
[lịch/schema/input đã khóa](historical_evaluation_inputs.json) được tạo/kiểm bằng
`scripts/prepare_historical_evaluation.py`. H03 hoàn tất offline;
H04/H05 và các điều kiện live H06 đã được nghiệm thu ở dưới.

## H04 — Hoàn thiện adapter và runner

- [x] Mở universe9 mã và lịch2023–2026 bằng adapter riêng; kiểm parity CORE4/OOD5 mã.
- [x] Dựng context/bank theo recipe từng phương pháp, nhãn engine và PIT;
  query outcome chỉ đọc sau forecast/checkpoint durable, retrieval `exit<query`.
- [x] Kiểm sentiment count/score/mask và coverage toàn lưới; giữ date-only khả dụng
  ngày sau, loại tin không ngày/tương lai; không claim archived content khi chưa có.
- [x] Chạy upstream một lần/unit/realization rồi deep-copy cho các nhánh;
  lưu parent/hash/ảnh, đủ5 factor rows và resolve Original→Fact_Anchor→MT_BICL.
- [x] Hoàn thiện CLI run/resume/verify, ledger/cache riêng, retry/unknown reserve,
  checkpoint mỗi unit và kiểm `previous_exit < next_entry` khi stride3.

CLI: `scripts/run_historical_evaluation.py`. [Runtime H04](historical_evaluation_runtime.json)
khóa source/thư viện mới, giữ nguyên protocol/input/model H02/H03. Fixture cách ly,
không được tính là inference hoặc kết quả nghiên cứu; kiểm triển khai và giới hạn
ghi tại [README W11](README.md#h04--adapter-và-runner-offline).

Trước thu thập cần tạo492 HMM prefix lịch sử bằng CPU; runner dừng trước API
nếu thiếu, không tự fit. Người dùng chạy lệnh sau, có thể chạy lại để tiếp tục:

```powershell
py -3.13 -X utf8 scripts/run_historical_evaluation.py prepare-regimes
```

Lệnh chỉ fit HMM trên prefix VNINDEX đúng ngày, không train teacher/student,
không dùng GPU/LLM. Người dùng đã hoàn tất fit492 prefix; không cần fit lại.
Query HMM2022 và model replica vẫn frozen; H05/H06 đã được nghiệm thu ở dưới.

- [x] Sửa lỗi `prepare-regimes` dùng nhầm guard fit2018–2022: fit/load historical
  dùng namespace riêng tới30/09/2026, giữ nguyên guard model gốc và query/replica.
- [x] Người dùng hoàn tất492 HMM prefix từ31/05/2022 tới17/09/2026;
  H05 đối soát toàn bộ checksum/prefix/PIT, không fit lại model đã lưu.

## H05 — Kiểm thử theo phạm vi

- [x] Chạy tests bị ảnh hưởng:label/cost, suffix/index, PIT/news/query-y poison,
  exit==query, D/C/query rời nhau, scaler/regime, symbol/OOD và model fingerprint.
- [x] Kiểm paired/deep-copy, factor rows/prompt, cache identity, retry/checkpoint/
  resume và metric/bootstrap oracle; chỉ compile Python mới/đổi.
- [x] Ghi kết quả và phạm vi PASS; không chạy full suite/E2E nếu không được yêu cầu.

[Receipt H05](historical_evaluation_validation.json):84 test/13 module PASS,
492 prefix đúng hash/PIT,1.020 context khớp preview,862 frozen forward;
chỉ biên dịch2 Python mới. Chi tiết và giới hạn tại [README W11](README.md#h05--nghiệm-thu-offline).

Lệnh nghiệm thu offline (không train production, không gọi API):

```powershell
py -3.13 -X utf8 scripts/validate_historical_evaluation.py
```

Lệnh kiểm492 prefix và1.020 context, chạy nhóm test đã chọn, biên dịch Python
mới và chỉ ghi receipt PASS khi mọi kiểm tra đạt. Phần paired fixture/cold replay
có thể mất vài phút; log tại `outputs/historical_reevaluation/h04_assets/h05_validation.log`.
Verifier H05 `--verify` áp dụng runtime v2 cũ; runtime v3 dùng verifier H06
ở dưới để kiểm baseline H05 và delta SDK đã nghiệm thu.
Chạy API nghiên cứu thuộc H06/H07 sau release, không nằm trong lệnh H05.

## H06 — Freeze và smoke test

- [x] Neo Git source/runtime/model/data/protocol/IDs; kiểm manifest/hash trước API.
- [x] Smoke đủ sáu primary/Fact_Anchor và control báo cáo dài:BRPP≤600, prompt<6.500,
  giữ distill/cap, utility4.096 draws và factor rows/ảnh; không đổi fallback/model ngầm.
- [x] Kiểm schema/options/quota năm organization, retry wrapper và credential scope;
  chỉ release lượt inference mới khi các gate áp dụng PASS.

[Receipt smoke](historical_evaluation_smoke.json):55 lượt thành công trên5 org
(45 Decision+10 vision),2 response503 được đối soát/reconcile, tổng57 HTTP;
không có429. Cold verify PASS, không phát sinh HTTP mới, không còn slot chờ.
Prompt live tối đa5.954<6.500 ký tự; BRPP600 và báo cáo bão hòa giữ đủ5 factor,
output960, utility4.096 draws; tất cả response thành công kết thúc `stop`.

[Quota](historical_evaluation_quota.json) ghi đúng xác nhận người dùng:5 org
độc lập, mỗi model30 RPM/1.000 RPD/8.000 TPM/200.000 TPD, không tách TPM,
chỉ Free/0 USD. Không coi xác nhận này là bằng chứng Console.
[Plan smoke](historical_evaluation_smoke_plan.json) khóa55 execution/trần300 HTTP;
[grant H07](historical_evaluation_release.json) từng chuyển RESEARCH sau cold verify,
đã được thu hồi ngày09/11/2026 khi người dùng hủy lượt thu đầy đủ.

Smoke dùng bank tín hiệu control cách ly, giá/nhãn/regime quá khứ thật,
không mở payoff query hoặc nhập control vào H07; không là kết quả thị trường.
Runtime v3 chỉ thêm tên schema tại SDK; giữ schema khoa học/H02/H03 và receipt
H05 nguyên byte.10 test wire/guard và5 file Python biên dịch PASS;
chi tiết delta, phạm vi gate và log tại [README W11](README.md#h06--freeze-và-live-smoke-pass).
Verifier hiện hành (offline, không API):

```powershell
py -3.13 -X utf8 scripts/run_historical_smoke.py verify
```

## H07 — Pilot ghép cặp48 điểm bằng API Free

### Trạng thái và phạm vi

Lượt đầy đủ34.806 call đã CANCELLED_BY_USER. Supervisor/child đã dừng;
outputs/historical_reevaluation/run_r1/ và managed_r1/ đã xóa. Trước khi
xóa có186 node upstream complete, một slot unknown và0 forecast grid.
Checkpoint, raw response, ảnh, log và lock của lượt dở không thuộc pilot.
Grant cũ có status=REVOKED, api=false. H02 model, donor archive,
492 HMM prefix và bằng chứng nghiệm thu H05/H06 được giữ.

Ledger quota tối thiểu tại
outputs/historical_reevaluation/quota_history/cancelled_run_r1/ giữ103
request và264.449 token đã tính hoặc reserve, gồm93 HTTP200,7 HTTP503 và3
transport_error. Chỉ giữ thời gian/model/usage/rate-limit và định danh quota,
không giữ report, ảnh, prompt hay kết quả nghiên cứu. Lượt mới phải cộng
quota còn hiệu lực của ledger này và H06; đổi namespace không reset quota.

Pilot có namespace mới outputs/historical_reevaluation/free_pilot_r1/,
UUID/protocol/runtime riêng, hiện READY_COLLECTION. Runner cũ34.806 call và grant
H06 không phát hành pilot. Các phần mở rộng9 mã, ablation/retrieval control,
Original_duplicate và repeats bổ sung nằm ngoài phạm vi buổi trình bày.
Thiết kế đầy đủ H03 được giữ làm tham chiếu.

### Mẫu và đối chứng

Sáu primary là Original_common, bayesian_v1, C2, A_tp_pool, B_semantic,
MT_BICL. Fact_Anchor là dependency bắt buộc của MT-BICL. Mỗi điểm có một
upstream realization và một Decision repeat. CORE4 gồm FPT/MWG/VCB/VNM,
mỗi mã12 ngày chung, tổng48 điểm; mỗi năm có6 ngày.

| Block | Cutoff đã chọn theo lịch |
| --- | --- |
| b2023_h2 | 03/07/2023,14/07/2023,01/08/2023,17/08/2023,06/09/2023,22/09/2023 |
| b2024_h2 | 01/07/2024,12/07/2024,30/07/2024,15/08/2024,04/09/2024,20/09/2024 |

Lấy giao ngày đủ bốn mã trong từng block của input H03, sắp20 ngày tăng
dần, chọn index0,3,7,11,15,19 theo floor(j*19/5), j=0..5. Không dùng
payoff/action để chọn ngày. Manifest pilot phải pin đủ48 ID, entry/exit và
source hash trước inference; kiểm holding spans không chồng lấn.
Dữ liệu2023–2024 đã exposed, scope của pilot là historical exploratory.

Full ở fix và Original_common khác prompt/cap/options. Primary dùng
Original_common cùng scaffold của năm cải tiến; số Full102 điểm trên fix
được dẫn riêng với cohort/options gốc. Bridge Full_fix_native960 mặc định
OFF. Nếu bật, phải khóa trước mọi Decision pilot, chạy đủ48 điểm với
prompt/schema fix và cùng model/960, thêm48 call và family riêng. Bridge
đo cách triển khai Full; không thay Original_common trong năm contrast
primary và không được ghi là tái lập run fix2048/1024.

### Dữ liệu, bank và reuse

- Query giá dùng donor fix đã archive và suffix sạch, cùng prefix tới cutoff
  cho mọi nhánh,45 nến biểu đồ và600 nến Alpha. News cùng snapshot/scorer,
  cửa sổ90 ngày, date-only khả dụng ngày sau và missingness. Entry/exit dùng
  chung; raw supplement chỉ phục vụ audit/barrier, không splice giá.
- Bayesian v1/C2/A/B dùng bank852 episode hiện có tại
  data_manager/regime_memory_store.json, exit04/06/2020–30/12/2022. Khóa
  toàn population cùng schema/manifest/audit/source. Kiểm nhãn qua engine,
  historical signals và PIT trước rank; không dựng bank bằng signal giả.
- Bank Bayesian đóng băng, không append query2023–2024. Giữ K=3, gate,
  shrinkage, tuổi/gap/similarity, renderer và fallback từng phương pháp.
  Báo eligible/stats/examples/fallback mọi query, kể cả prior-off.
- Bank cũ và donor query có provenance riêng. Audit báo chênh nguồn giá,
  normalization và thời điểm tạo signal; không relabel bank theo snapshot
  khác hoặc ghép chuỗi. Estimand là chuyển giao với bank đóng băng, khác
  memory cập nhật đầy đủ của H07 cũ.
- MT dùng replica seed42/step3000, teacher/scaler/HMM frozen đã nghiệm thu.
  Numeric context theo primitive hiện hành trên donor suffix, chỉ cycle
  exit<query, giữ D/C/query và holding spans rời nhau. Context giá không
  cần API lịch sử. Selected query chỉ thành observation sau mọi forecast
  bắt buộc đã durable. Báo rõ MT có numeric context cập nhật còn Bayesian
  có bank signal đóng băng; không quy mọi chênh lệch cho riêng kiến trúc student.
- Audit archive upstream theo input/report/ảnh/factor rows, model/options,
  source/runtime/hash. Thư mục trống hoặc summary không được tính là cache.
  Archive fix được đọc ở commit9efd23f4 đã pin; các nhánh giữ nguyên ref.
  Chỉ nhận raw HTTP thật có provenance; loại fixture/offline_dry_run,
  control smoke H06 và mọi dữ liệu từ lượt H07 đã hủy.
- Archive upstream là dữ liệu cố định cho so sánh có điều kiện trên reports.
  Lưu options gốc, gồm output1024 nếu có; không ghi thành execution960 mới.
  Thiếu provenance/nội dung hoặc khác query data thì không reuse. Nếu tạo
  mới, vision960 một lần/điểm rồi deep-copy tới mọi nhánh.
- Seal48 shared states và strata reused/new trước Decision; báo rõ strata.
  Chạy mới toàn bộ Decision primary trong cùng collection. Action cũ của
  năm phương pháp không được ghép với MT mới thành bảng primary.

### Prompt, model và kinh tế chung

Decision openai/gpt-oss-20b, vision mới qwen/qwen3.8-27b, temperature0,
max_tokens960, reasoning/client options theo H03. Mọi primary dùng cùng
COMMON_INSTRUCTION, distill/cap, năm dòng Alpha và trường kết quả chung;
prefix/projection/schema anchored đổi đúng theo phương pháp. Original
prior OFF, C2/A/B giữ fallback, MT giữ facts guard và utility4.096 draw.
Fact_Anchor bắt buộc. Prompt<6.500, BRPP≤600 ký tự.

LONG Open(t+1)→Close(t+3), SHORT=CASH, phí0,25%/slippage0,10% mỗi chiều,
fractional shares, risk OFF, vốn50 triệu reset mỗi mã/năm/phương pháp.
TP/SL mô tả không thay exit. Nhãn qua compute_round_trip_net_return;
payoff query chỉ mở sau forecast durable. API lỗi không đổi thành CASH.

### Quota và thời gian

| Hạng mục | Execution nominal |
| --- | ---: |
| Sáu primary | 288 |
| Fact_Anchor | 48 |
| Decision tổng | 336 |
| Vision mới tùy cache hợp lệ | 0–96 |
| Research tổng | 336–432 |
| Smoke cách ly một điểm,7 Decision+2 vision | 9 |
| Bridge Full_fix_native960 nếu khóa ON từ đầu | +48 |

Nominal là trần khi mọi nhánh cần LLM; fallback/bypass hợp lệ ghi riêng.
Retry/format repair dùng chung tối đa3 HTTP/slot; trần toàn lượt gồm smoke
là1.323 attempt, hoặc1.467 khi bridge ON. Quota/deadline là rào chắn chặt
hơn các trần này. Smoke tại FPT-2023-06-23 cách ly khỏi48 điểm, giữ raw và
kiểm schema/PIT/payload; không tính vào N.

Phân48 ID sắp theo ngày/mã qua năm org round-robin; mỗi query giữ org cho
mọi nhánh. Cân bằng thứ tự bằng xoay danh sách và giữ dependency
Original→Fact_Anchor→MT; lưu thứ tự actual. Năm key đúng env hiện có.
Mỗi request qua wrapper/quota ledger; unknown giữ reserve,429 chờ reset.
H06 và103 request lượt hủy phải dedup/import vào accounting trước API mới;
quota không được chia lại từ zero theo project hoặc UUID.

Preflight dựng đủ payload để tính ngân sách theo org/model, gồm input ảnh,
output reserve960, quota đã dùng, smoke và retry reserve. ETA dùng telemetry
thật kèm biên thận trọng. Nếu ngân sách không vừa48 giờ thì BLOCKED_BUDGET
trước research, báo phần thiếu; không giảm mẫu/repeat, đổi model/key/cap
hoặc nâng gói sau outcome. Mục tiêu thu trong24 giờ đầu, dành24 giờ sau
cho cold analysis/bảng biểu; chưa bảo đảm deadline khi audit reuse/token
chưa hoàn tất. Chỉ Free, chi tiêu0 USD.

### Công việc cần thực hiện

- [x] P01 — Audit bank852, feature index/scaler/regime, nguồn query/cache
  upstream, quota carry-over, coverage/support48 điểm và feasibility48 giờ.
- [x] P02 — Protocol/input/schema/runtime pilot riêng,48 ID, bridge OFF/ON,
  memory policy, call order, model/options và manifest khóa trước inference.
  Adapter giữ thuật toán từng phiên bản; runner tách full-matrix cũ.
- [x] P03 — Kiểm scoped PIT/query-y poison, full population, disjoint context,
  paired/deep-copy, prompt/factor rows, metric và checkpoint/quota carry-over.
  Chỉ compile Python thay đổi; smoke9 lượt và cold verify trước release.
- [ ] P04 — Seal48 shared states, grant pilot sau P01–P03 PASS, thu đủ
  336 forecast slot và48 bridge nếu đã khóa ON, với bypass hợp lệ,
  source/parent/HTTP/latency. Resume cùng UUID; không chọn lại point hoặc
  dừng theo return.
- [ ] P05 — Cold verify48 point ×sáu primary và Fact_Anchor, mọi slot complete
  hoặc bypass đúng policy, không pending/unknown, nhãn/source khớp. Seal
  manifest trước H08. Thiếu thì PARTIAL và giữ48 là N planned.

Tiến độ09/11: [audit](free_pilot_audit.json), [protocol](free_pilot_protocol.json),
[48 input](free_pilot_inputs.json), [runtime](free_pilot_runtime.json) và
[grant](free_pilot_release.json) đã khóa riêng. Bridge OFF, smoke cố định org5;
48 query vẫn round-robin org1–5. Import đủ160 request H06/lượt hủy,
396.206 token đã tính/reserve. Không cache upstream nào đạt raw HTTP provenance:
48 shared mới/96 vision. Ngân sách gồm530 HTTP nominal+retry reserve20%,
ước lượng khoảng44 giờ, PASS giới hạn48 giờ nhưng chưa đạt mục tiêu24 giờ;
không bảo đảm ETA thực tế. Admission kiểm lại payload48 shared trước Decision.

Bank852 xác minh nhãn native qua engine;828 nhãn khác donor hơn1e-8,
chênh tối đa0,0429885 điểm phần trăm; giữ nguyên cả hai nguồn. Historical
signals dựa vào QA/schema chuẩn hóa đã công bố, thiếu raw signal journal
để chứng nhận lại độc lập. Scaler fit bank≤2022, không fit query.
Preflight không mở payoff48 query: MT đủ support26/48 với selected query
còn bị khóa; support thực tế/bypass được lưu khi chạy đúng lịch prequential.

P03 PASS18 test pilot và38 test hồi quy liên quan; compile đúng bốn file mới.
Người dùng đã chạy smoke:9/9 HTTP200,7 Decision+2 vision,19.611 token;
cold replay PASS,12 slot complete, không còn latest unknown. Agent kiểm lại
không gọi API, source/raw/ảnh/usage/checkpoint khớp; grant PILOT_RELEASED
bind đúng cold receipt và UUID3881b4ba-4609-460a-8137-5fbad4f617db.
P04–P05 còn chờ chạy. Ngân sách còn lại khoảng42,7 giờ gồm retry reserve20%,
PASS thời gian còn lại47,3 giờ; deadline cố định01:56:52 ngày11/11/2026
(UTC+7), không reset khi resume. Người dùng chạy mọi lệnh API; agent chỉ
chuẩn bị code, kiểm ngoại tuyến và đối soát output.

P04 đang PARTIAL:12/48 shared nghiên cứu complete,0 Decision nghiên cứu.
Pattern FPT-2023-08-17 tại org3 dừng HTTP503 do model over capacity;
raw response đã kiểm checksum, slot đã dùng2/3 HTTP, chưa có HTTP200.
Attempt cũ db3f3d2a đã được authorize; attempt cuối là
1066b007-e5d1-433a-93ee-46b2fe8c1bc7. Supervisor tự tìm attempt cuối, không
dùng lại UUID reconcile đã chép trong lệnh cũ; giữ mọi response/reserve/checkpoint.

Chạy tại thư mục gốc repository, giữ năm env key hiện có:

```powershell
py -3.13 -X utf8 scripts/run_free_pilot.py
```

Grant PILOT_RELEASED chỉ mở pilot48. Stage shared seal đủ48 upstream trước
Decision; collect kiểm lại admission với payload thực rồi thu336 forecast slot
gồm fallback/bypass hợp lệ; verify chạy cold và xuất P05_COLD_PASS cùng receipt.
Gửi kết quả P05 để đối soát và chuyển H08. Log console và quota nằm trong
namespace free_pilot_r1, resume cùng UUID, không dùng collector full cũ.
Lệnh trên tự nạp `.env`, tìm phase/attempt hiện tại và chạy shared→collect→verify.
Nếu terminal đóng hoặc tiến trình bị ngắt, chạy lại cùng lệnh; không cần
bootstrap hoặc UUID thủ công. Nếu worker cũ còn giữ OS lock, chờ nó kết thúc;
không khởi chạy API trùng. Lỗi503/429/quota/transport có proof được chờ và
reconcile tự động, giữ trần3 HTTP/slot qua mọi lần khởi động lại. Raw HTTP200
đủ proof được replay bằng chính node/policy cũ và cùng attempt UUID, không
gọi lại API. Lỗi dữ liệu/source, response không thể tái lập, dispatch chưa rõ
hoặc hết trần3 thì dừng có lý do; không giả CASH hoặc nới quota/deadline.

[Manifest supervisor bổ sung](free_pilot_manager.json) khóa source/policy điều
phối, grant và UUID; runtime inference/protocol/asset cũ giữ nguyên byte.
Đã PASS21 test mới và26 hồi quy liên quan; compile đúng bốn Python mới.
Log/tiến độ tại free_pilot_r1/manager/. Khi cold PASS có thêm manager/
collection_receipt.json bind manifest bổ sung và receipt P05; H08 vẫn chờ.

<!-- FREE_PILOT_MANAGER_START -->
Trạng thái **NOT_STARTED**; đã giữ12/48 shared và0/336 forecast nghiên cứu.
<!-- FREE_PILOT_MANAGER_END -->

## H08 — Phân tích pilot

- [ ] Dựng tám account mã/năm mỗi phương pháp. Primary D là mean đều bốn
  mã và hai năm của chênh return so Original_common, đơn vị đpt. Báo return
  tuyệt đối, daily/cycle-end MDD, exposure/turnover/phí/số LONG và cash giữa
  query theo đúng lịch; không gộp thành portfolio return.
- [ ] Pooled accuracy/BA/MCC/F1/confusion matrix trên cùng48 điểm, per-symbol/
  year có n_planned/n_complete/n_defined; undefined=null. Prior-off vẫn trong
  estimand toàn bộ, subgroup chỉ diagnostic. Sharpe/Sortino chu kỳ chỉ báo
  khi xác định, annualized=null; bỏ sqrt(252) mặc định cho mẫu thưa.
- [ ] Khóa trước inference bootstrap circular theo selected-date trong từng
  năm, L=2, mỗi năm giữ6 ngày; cùng index cho bốn mã/mọi nhánh/metric,
  10.000 draw PCG64 seed20261109. Dựng account từng draw, báo point estimate
  và band centered max-deviation95% cho family năm contrast với Original.
  BA là family riêng; cần ít nhất9.500/10.000 joint finite draw để xuất band.
  Giữ số draw mất class, dưới ngưỡng thì band toàn family=null, không sinh bù
  hoặc đổi cách tính sau outcome.
- [ ] Báo12 ngày thực, hai block năm, độ rộng interval, leave-one-date/symbol-out.
  Bootstrap mô tả độ nhạy trên mẫu nhỏ, chưa chứng nhận simultaneous coverage
  hoặc superiority. Một repeat không đo variance giữa các lần LLM. Dữ liệu
  exposed và archive upstream làm kết luận có điều kiện trên reports.
- [ ] Báo coverage/support/bypass, strata nguồn, bank frozen/numeric context,
  raw→facts→veto, inference mới/reuse, token/call/latency thật. Kết quả MT
  cũ−5,313090 đpt và gate replica không phải kết quả pilot mới.
- [ ] So fix bằng bridge nếu khóa ON, hoặc dẫn bảng102 điểm riêng với cohort/
  prompt/options gốc; không trừ hai return khác protocol. Cold consumer
  đối soát raw/label/metric/hash, giữ VENDOR_SERIES_LIMITED, news content PIT
  chưa chứng nhận và PENDING_EXECUTION_DATA.

## H09 — Kết sổ pilot

- [ ] Một bảng sáu primary, per-symbol/year, coverage và uncertainty; bridge
  chỉ xuất khi thu đủ48 điểm theo tùy chọn đã khóa trước.
- [ ] Đóng gói protocol/input/model/manifest/raw/forecast/labels/usage và lệnh
  tái lập offline; README ghi kết quả/trạng thái/giới hạn thật.
- [ ] PILOT_COMPLETE cần P01–P05/H08 và cold verification PASS. H07 đầy đủ
  1.020 điểm vẫn CANCELLED, không đánh dấu full matrix DONE từ pilot48.
  Hết hạn thì bàn giao PARTIAL/BLOCKED và planned/complete thực tế.
