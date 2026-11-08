# Checklist đánh giá lại trên dữ liệu lịch sử

Cập nhật08/11/2026. Thực hiện lại quy trình đầy đủ đã dùng trước đây,
ưu tiên độ tin cậy và khả năng tái lập. Train lại model dưới tên
`MT_BICL_replica_full_r1`; bỏ phương án một seed/dừng sớm.
Người dùng đã hoàn tất fit/pilot/train:đủ3 seed/60 checkpoint, chọn seed42/
step3000. Test `MODEL_GATE_PASS`, cold replay đủ60 checkpoint
`CPU_REPLAY_MATCH`; H02 hoàn tất ở phạm vi audit dữ liệu và model.
H03 đã khóa protocol và dự toán trước inference trên lưới mới.
H04/H05 đã hoàn tất offline; H06 PASS live smoke55 lượt và cold verify.
H07 đã bắt đầu thu bank; tạm dừng vì transport_error, đã reconcile để người dùng tiếp tục.

## Checklist tổng

- [x] H01 — Khảo sát nguồn và phạm vi đánh giá.
- [x] H02 — Audit dữ liệu và train lại model, nghiệm thu CPU và lưu asset.
- [x] H03 — Khóa protocol, lịch, model và dự toán đánh giá offline.
- [x] H04 — Hoàn thiện adapter và runner, nghiệm thu triển khai offline.
- [x] H05 — Kiểm thử theo phạm vi, PASS84 test và đối soát asset/context.
- [x] H06 — Freeze, live smoke55 lượt và cold verify PASS; release H07 Free/0 USD.
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
[grant H07](historical_evaluation_release.json) đã chuyển RESEARCH sau cold verify.

Smoke dùng bank tín hiệu control cách ly, giá/nhãn/regime quá khứ thật,
không mở payoff query hoặc nhập control vào H07; không là kết quả thị trường.
Runtime v3 chỉ thêm tên schema tại SDK; giữ schema khoa học/H02/H03 và receipt
H05 nguyên byte.10 test wire/guard và5 file Python biên dịch PASS;
chi tiết delta, phạm vi gate và log tại [README W11](README.md#h06--freeze-và-live-smoke-pass).
Verifier hiện hành (offline, không API):

```powershell
py -3.13 -X utf8 scripts/run_historical_smoke.py verify
```

## H07 — Chạy đánh giá

Trạng thái IN_PROGRESS: đã bắt đầu thu bank tại `run_r1`;5 checkpoint node
complete,2 HTTP200 và1 transport_error, chưa có forecast grid. Pattern của
`MWG-2022-05-31/u0` org2 gián đoạn kết nối, không có raw response/output;
không xác định được provider đã xử lý request hay chưa. Đã đối soát và
reconcile UUID `4f84363c-c92f-4ff6-a567-74be59962424`, giữ nguyên attempt cũ,
quota reserve, key/model/payload và5 checkpoint complete. Chờ người dùng
chạy lại khối lệnh dưới; không cần train/fit lại, chưa hoàn tất H07.

- [ ] Thu bank/shared state cần thiết, CORE4 rồi các mã bổ sung, ablation/control
  và panel upstream; đủ repeat/realization đã khóa, không vote hoặc chọn best repeat.
- [ ] Checkpoint/resume cùng identity; xử lý pending/error/unknown có ledger;
  không đổi lỗi thành CASH hoặc dừng khi kết quả vừa dương.
- [ ] Kết sổ đủ ma trận và hash raw/forecast trước mở payoff để phân tích.

Lệnh H07, chạy CORE4 trước rồi mới OOD5; cùng lệnh có thể tiếp tục các slot
đã hoàn tất. Dừng nếu lỗi, giữ nguyên checkpoint và xử lý UUID unknown theo log:

```powershell
foreach ($cohort in @("CORE4", "OOD5")) {
    py -3.13 -X utf8 -m dotenv -f .env run -- py -3.13 -X utf8 scripts/run_historical_evaluation.py run --cohort $cohort
    if ($LASTEXITCODE -ne 0) { throw "Dừng tại $cohort; giữ checkpoint và log." }
}
```

Theo dõi log trong PowerShell thứ hai sau khi lệnh chạy đã tạo file:

```powershell
Get-Content outputs/historical_reevaluation/run_r1/console.log -Tail 30 -Wait
```

Không chạy hai tiến trình thu thập cùng lúc. Nếu dừng, gửi traceback/UUID để
đối soát trước khi tiếp tục; không xóa checkpoint hoặc tự reconcile unknown.
Sau khi hai cohort hoàn tất, kiểm cold replay/kết sổ trước khi đánh dấu H07 DONE.

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
  TODO/BLOCKED với lý do. Kiểm theo phạm vi thay đổi tại AGENTS1.2;
  ghi kết quả và giới hạn vào README tuần, không tự động chạy lại toàn suite.
