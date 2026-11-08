# W11 — Đánh giá lại các cải tiến trên dữ liệu lịch sử chung

Cập nhật08/11/2026. Original và bốn nhóm cải tiến là Bayesian Prior v1,
Bayesian Prior v2/C2, Bayesian Prior A/B và MT-BICL.
[Kế hoạch tổng](../plan.md) · [Đặc tả đánh giá](historical_reevaluation_plan.md)

## Phạm vi hiện hành

Primary6 nhánh gồm Original_common, bayesian_v1, C2, A_tp_pool, B_semantic,
MT_BICL. Fact_Anchor là dependency bắt buộc của MT-BICL.
CORE4 gồm480 unit; EXTENDED gồm1.020 unit trên9 mã eligible,120 ngày cutoff,
6 time blocks. Các ablation/retrieval/repeats có lịch riêng trong kế hoạch.

Donor fix được đọc theo commit
`9efd23f4157e0d3ab8069fccab7dccf03439a714`.
Archive21 blob nguồn,9 CSV khớp hash và label bridge1.020 cycle.
Data/vendor quality và economic acceptance được báo riêng.
H02 hoàn tất audit VNINDEX2026, raw/quyền9 mã và bank train, cùng nghiệm thu model.
Model gốc không tìm thấy; áp dụng [checklist replica đầy đủ](historical_reevaluation_plan.md#h02--chuẩn-bị-dữ-liệu-và-model).
Người dùng đã hoàn tất fit/pilot/train:đủ60 checkpoint, chọn seed42/step3000.
Test `MODEL_GATE_PASS`, cold replay đủ60 checkpoint `CPU_REPLAY_MATCH`.
Tiếp theo H03 khóa protocol và ngân sách; H03–H09 tiếp tục theo checklist.

## Checklist đánh giá lại

| Bước | Công việc | Trạng thái |
| --- | --- | --- |
| H01 | Audit donor, dữ liệu/PIT/exposure và kế hoạch bốn nhóm | [x] DONE |
| H02 | Dữ liệu, train replica ba seed và asset readiness | [x] DONE — MODEL_GATE_PASS / CPU_REPLAY_MATCH; execution acceptance vẫn PENDING_EXECUTION_DATA |
| H03 | Protocol máy, registry, inference, families và budget chính xác | [ ] TODO |
| H04 | Adapter/harness trên dữ liệu chung và universe chín mã | [ ] TODO |
| H05 | Kiểm theo phạm vi, PIT/paired/economics/checkpoint | [ ] TODO |
| H06 | Freeze bank/runtime và smoke toàn registry | [ ] TODO |
| H07 | Collect primary, extension, ablation/retrieval và repeats | [ ] TODO |
| H08 | Cold analysis và uncertainty/multiplicity/strata/cost | [ ] TODO |
| H09 | Kết sổ bằng chứng, trạng thái và giới hạn | [ ] TODO |

## Kết quả các phương pháp đã ghi nhận

| Phương pháp | Kết quả |
| --- | --- |
| Bayesian Prior v1 | Pilot FPT20 có return−7,91%, Original−5,67%; accuracy50% so55% |
| Bayesian Prior v2/C2 | Development D+1,742822 đpt, chỉ2/4 mã tăng; NOT_PROMOTED |
| A_tp_pool | Holdout64 điểm D+2,025325 đpt, CI95%[0,135027;4,211864];3/4 mã tăng |
| B_semantic | Development D khoảng+1,455 đpt; không được chọn |
| MT-BICL | Development60 điểm D−5,313090 đpt, accuracy45% so65%; NOT_NOMINATED |

Các vòng dùng cohort/response riêng và Original ghép cặp trong từng vòng.
Kết quả đã lưu không phải kết quả áp dụng lại trên lưới1.020 unit.

## Kiểm tra và bàn giao

MT-BICL được tổ chức theo các module không đánh số phiên bản trong
`core/mt_bicl_*.py`; namespace `outputs/bayesian_benchmark/mt_bicl/`.
Student/teacher và dữ liệu dùng chung tiếp tục thuộc phương pháp hiện hành.
Các hợp đồng kinh tế/PIT/paired/prompt và quyền release vẫn được kiểm riêng.

Phạm vi kiểm của đợt hợp nhất gồm utility/oracle, prompt/facts/policy,
student frozen/query poison, bank/scaler/task/stream leakage, readiness
và hồi quy paired/prompt/token/callers. Biên dịch đúng các Python thay đổi.
Kết quả kiểm PASS gồm159 test riêng biệt trong16 module liên quan;106 test
MT-BICL được chạy lại PASS sau thay đổi nhãn schema cuối. Đã biên dịch36
Python thay đổi; thêm17 lượt kiểm loader/readiness PASS sau khi khóa manifest
mặc định với Git. Raw utility draw SHA đối soát với mốc trước dọn là
`e98d2e0d2dc10f0efe21cd2185f05316d81b62d9aa70f0ba8d2c8c36192b9a90`.
Các log nằm tại `outputs/bayesian_benchmark/mt_bicl/validation.log` và
`validation_mt_bicl.log`. Không chạy lại toàn suite/E2E theo AGENTS1.2.

Đã kiểm diff rỗng cho agents, engine, loader, Bayesian Prior, dữ liệu,
data_manager, utils và cấu hình gốc so mốc bắt đầu. Source/receipt donor và
lưới1.020 unit giữ nguyên byte. Phần dọn ledger đã loại519 request của
thí nghiệm bị bỏ; các nhóm request còn lại được giữ và tên nhánh MT-BICL
được đồng bộ. Readiness mới đã tạo và cold-verify PASS, registry6 nhánh có1 READY và5
BLOCKED_ASSET; model package0/2 component, VNINDEX2026 còn thiếu.
Label bridge1.020 cycle PASS; kinh tế giữ PENDING_EXECUTION_DATA.
Receipt tại `outputs/historical_reevaluation/manifests/asset_readiness.json`.

## Kế hoạch train replica08/11/2026

Theo chỉ đạo mới, dùng quy trình đầy đủ đã thực hiện trước đây:
`MT_BICL_replica_full_r1`, ba seed17/42/73 ×5.000 step, effective batch128,
checkpoint mỗi250 step. Đánh giá đủ60 checkpoint trước selection; không
dừng ở checkpoint đầu tiên vừa đạt gate. Chọn theo macro log loss/Brier2021,
rồi step và seed order; test chỉ mở sau seal, fail thì không reselect.

Các task chuẩn bị/teacher/pilot/train/test/cold replay có checkbox tại
[checklist H02](historical_reevaluation_plan.md#h02--chuẩn-bị-dữ-liệu-và-model).
Lượt viết lại plan trước triển khai chỉ sửa Markdown, chưa fit/train hoặc
thay model/protocol JSON, receipt hay dữ liệu; khi đó chỉ kiểm diff/link/
recipe/hash/số liệu theo AGENTS1.2. PASS ở mục trước thuộc đợt hợp nhất;
kết quả triển khai H02 mới được ghi riêng ngay bên dưới.

## H02 — chuẩn bị và bàn giao08/11/2026

- [x] Tải snapshot VNINDEX2025–2026 riêng,249 phiên overlap khớp đủ OHLCV với
  bản cũ; xuất lịch2018–2026 gồm2181 phiên, phủ đủ decision/entry/exit của grid.
- [x] Lưu HTTP responses/raw/events của9 mã; audit18 cycle có rào chắn quyền,
  giữ raw BHN lỗi và suffix673; không thay donor hoặc chứng nhận fill.
- [x] Dựng bank1235/1640 cycle hợp lệ, train731 cycle/48 task, support PASS;
  cold-check input, feature/label/scaler qua nguồn đã khóa, không fit HMM/teacher.
- [x] Port simulator/student69+37/metrics theo recipe Git pin, CLI từng stage,
  checkpoint đầy đủ optimizer/RNG, OS lock, selection đủ60 và test sau seal.
- [x] Khóa protocol/source/runtime/data trước fit; model manifest/release cũ nguyên byte.
- [x] Người dùng chạy `prepare` để fit teacher/HMM, tạo corpus/context và seal.
- [x] Người dùng chạy `pilot` rồi `train`; đủ3 seed/60 checkpoint, không early stop.
- [x] Sau train, chạy `evaluate` và `verify`, kiểm model/test/cold CPU replay mới.

Evidence mới ở `outputs/historical_reevaluation/h02_data_r1/`, gồm raw HTTP,
manifest acquisition và `execution_audit.json`. Manifest acquisition ghi
coverage của supplement2025–2026; dùng `execution_audit.json` để đọc coverage
trên lịch đầy đủ2018–2026 và suffix BHN. Raw/vendor khác nhau trên phần lớn
ngày; economic acceptance vẫn `PENDING_EXECUTION_DATA`, không splice giá cổ
phiếu hoặc sửa nhãn riêng phương pháp. Receipt readiness trước đó là bằng
chứng audit cũ, không bị ghi đè hay coi là nghiệm thu gói replica mới.

Protocol máy [mt_bicl_replica_full_r1.json](mt_bicl_replica_full_r1.json) bind
recipe tại `00b24679`, source/runtime/raw train và raw OOS dùng cho context.
Pipeline mới dùng CPU cho mọi frozen validation/test/cold replay để so raw
logits cùng runtime; GPU chỉ dùng preflight/pilot/train. Phải đo ETA gồm
sample/teacher, CPU validation và I/O, không lấy proxy GPU làm ETA toàn lượt.
Prepared receipt bind mọi corpus/teacher/context; test chỉ được decode bởi
student sau selection seal; train/inference LLM historical vẫn tách quyền.

Kiểm theo phạm vi: **63 test riêng biệt PASS** gồm16 mới,8 bank leakage,
13 task leakage,3 adapter leakage và23 economic account; **10 Python mới
biên dịch PASS**. Có fixture CPU kiểm loss query-only, hai packing, serving
parity, optimizer/RNG replay và checkpoint orphan; đây không phải production
training. Không full suite/compileall/E2E; không fit teacher/HMM, không chạy
GPU hoặc LLM. Source/protocol đã neo Git trước lệnh bàn giao.

## Lệnh chạy H02

Chạy trong thư mục repo bằng PowerShell. `prepare` bắt đầu fit CPU; `pilot`
bắt đầu GPU. Theo chỉ đạo, các bước này để người dùng chạy. Mỗi stage có
guard riêng; lỗi hoặc gate FAIL thì dừng, không tự chuyển sang stage kế.

Lỗi owner khác signature ở đầu `prepare` đã xác định là metadata của lần
`check-inputs` trước khi sửa source OOM. Owner cũ đã released, chưa có fit/
train. Bổ sung recovery riêng cho replica: lấy OS lock, kiểm cùng host,
owner đã kết thúc, signature cũ có Git provenance và recipe/data/runtime
không đổi; chỉ cho phép namespace có input bank và metadata preflight.
Lưu nguyên byte owner tại `lock_history/` cùng receipt migration trước khi
chuyển owner cũ ra khỏi đường dẫn active. Không xóa `run.lock`, không nới
`PriorRunLock` dùng chung hoặc thay UUID/state/checkpoint nghiên cứu.

Khi cần kiểm lại lỗi này trước fit, các lệnh dưới đây không chạy training:

```powershell
py -3.13 -X utf8 scripts/run_mt_bicl_replica.py repair-lock
if ($LASTEXITCODE -ne 0) { throw "Chưa phục hồi được khóa; không xóa state hoặc chạy train." }
py -3.13 -X utf8 scripts/run_mt_bicl_replica.py check-lock
if ($LASTEXITCODE -ne 0) { throw "Khóa chưa PASS; giữ metadata để kiểm tra." }
```

Kiểm riêng bản sửa:14 test PASS (7 recovery mới,6 hồi quy OS lock và1 source
pin),3 Python mới/đổi biên dịch PASS. Bao phủ khóa sống/host khác/liveness
unknown, artifact fit/train, signature không rõ, archive nguyên byte và
resume sau crash trước rename. Chỉ source pins CLI/lock đổi; recipe/model/
data/runtime giữ nguyên, không full suite/E2E hoặc fit/GPU/LLM.
Đã chạy recovery local: `PREFIT_OWNER_ARCHIVED`, sau đó `check-lock` trả
`LOCK_VERIFIED_NO_FIT`; owner mới released và bind đúng protocol hiện tại.
Không chạy `prepare` hoặc tự bắt đầu training trong lượt sửa này.

```powershell
$env:CUBLAS_WORKSPACE_CONFIG = ":4096:8"
foreach ($replicaStage in @("prepare", "pilot", "train")) {
    py -3.13 -X utf8 scripts/run_mt_bicl_replica.py $replicaStage
    if ($LASTEXITCODE -ne 0) { throw "H02 dừng tại $replicaStage; giữ checkpoint và log để kiểm tra." }
}
```

Nếu bị ngắt khi train, đặt lại biến môi trường rồi chạy lại lệnh stage
`train`; giữ nguyên namespace, UUID và checkpoint, không xóa state.

```powershell
$env:CUBLAS_WORKSPACE_CONFIG = ":4096:8"
py -3.13 -X utf8 scripts/run_mt_bicl_replica.py train
```

Sau khi `train` trả `SELECTED`, bước nghiệm thu CPU, không optimizer:

```powershell
py -3.13 -X utf8 scripts/run_mt_bicl_replica.py evaluate
if ($LASTEXITCODE -ne 0) { throw "Model không qua test; không reselect." }
py -3.13 -X utf8 scripts/run_mt_bicl_replica.py verify
if ($LASTEXITCODE -ne 0) { throw "Cold replay chưa PASS; không release model." }
```

Output riêng: `outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/`.
`MODEL_GATE_PASS` không cấp quyền chạy lưới H07; H03–H06 vẫn cần hoàn tất.

## H02 — kết quả train và nghiệm thu replica08/11/2026

Người dùng đã chạy `prepare`/`pilot`/`train` đầy đủ. Đã đối soát12 input,
60 checkpoint và60 assessment theo byte hash. Teacher hội tụ237 vòng,
max delta9,827×10⁻¹¹; oracle toàn bộ corpus max error7,106×10⁻¹⁴.
Pilot69/37 đều optimizer replay PASS; PAIRED tiny KL4,652×10⁻¹⁰.
Context có248 query2021/256 query2022; scaler fit731 cycle với max exit
29/12/2020, mọi model regime có fit cutoff≤31/12/2020.

Selection đã seal sau đủ60 checkpoint:global **seed42/step3000**; best
seed17 và73 đều step2500. `evaluate` CPU trả `MODEL_GATE_PASS`, giữ đủ
kết quả từng seed và ablation. Gate test cố định5.000 episode, swap5.000 cặp:

| Seed | Step chọn | Mean KL | P95 absolute error | Swap sign agreement | Eligible pairs | Gate |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 17 | 2500 | 0,002497287 | 0,067003671 | 98,243115% | 2106 | PASS |
| 42 | 3000 | 0,002774316 | 0,066780334 | 98,385565% | 2106 | PASS |
| 73 | 2500 | 0,003114808 | 0,069906050 | 98,338082% | 2106 | PASS |

Diagnostic2022 của candidate:macro log loss0,6813400072/Brier0,2441134978;
teacher tương ứng0,6775858521/0,2422396245. Student kém teacher lần lượt
+0,0037541551/+0,0018738733; không che kết quả bất lợi hoặc đổi checkpoint.
Gate cơ chế không chứng minh lợi nhuận; kết quả lịch sử giữ scope exploratory.

Cold replay CPU đã PASS: toàn bộ 60 checkpoint khớp raw logits/metrics;
các test stage của ba seed khớp receipt, không chạy optimizer. Adapter CPU
nạp đúng weights, fingerprint `c60ae9695dde6f308ff30b0f4de7e40539ea5e8353cc7b1e0acb3d57a11f471c`,
model ở chế độ frozen.

[Manifest model replica](mt_bicl_replica_full_r1_model.json) khóa candidate,
teacher, scaler train-only, regime và hash các receipt. Weights/teacher,
regime và receipt nghiệm thu được lưu Git, giữ nguyên byte khi checkout.
Toàn bộ checkpoint optimizer/RNG và corpus vẫn giữ nguyên tại namespace local;
đóng gói bằng chứng đầy đủ thuộc H09. Manifest gốc và protocol train không đổi.

H02 hoàn tất ở phạm vi audit dữ liệu và model; data quality vẫn
`VENDOR_SERIES_LIMITED`, economic acceptance vẫn `PENDING_EXECUTION_DATA`.
Chưa release inference trên lưới mới. H03 tiếp theo khóa sáu primary, model binding,
IDs/folds, hợp đồng kinh tế, options API, repeat/family thống kê và ngân sách.

Kiểm lần này: frozen `evaluate`/`verify`, loader/fingerprint và đối soát hash
43 file nguồn/27 file dữ liệu PASS; diff và liên kết đã kiểm. Không sửa
code/test/runtime, không train/refit; không chạy lại compile/unit/E2E/leakage suite
theo AGENTS1.2. Kết quả test fixture trước đây vẫn là bằng chứng lịch sử, không ghi
là đã chạy lại.
