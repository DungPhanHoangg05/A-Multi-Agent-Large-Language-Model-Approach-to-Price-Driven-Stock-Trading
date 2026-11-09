# W11 — So sánh các phương pháp bằng Groq Free

Cập nhật09/11/2026. Hệ thống gồm Original và bốn nhóm cải tiến Bayesian
Prior v1, Bayesian Prior v2/C2, Bayesian Prior A/B và MT-BICL.
[Kế hoạch tổng](../plan.md) · [Kế hoạch pilot](historical_reevaluation_plan.md#h07--pilot-ghép-cặp48-điểm-bằng-api-free)

## Phạm vi hiện hành

FREE_PAIRED_PILOT_48 có sáu primary Original_common, bayesian_v1, C2,
A_tp_pool, B_semantic, MT_BICL và dependency Fact_Anchor. CORE4 gồm
FPT/MWG/VCB/VNM,12 cutoff chung2023–2024, một upstream và một Decision
repeat/điểm;336 Decision nominal,0–96 vision mới tùy archive hợp lệ,
smoke9 execution cách ly. Bridge Full_fix_native960 mặc định OFF, thêm48
Decision nếu được khóa ON trước inference. Quota năm org Free, chi tiêu0 USD.

Bayesian dùng bank852 episode đóng băng2020–2022; MT giữ numeric context
theo phương pháp và replica seed42/step3000 đã nghiệm thu. Query donor fix,
prompt/model/options/kinh tế chung phải khóa trước API. Reuse upstream là
đánh giá có điều kiện trên reports đã lưu, phải có provenance; Decision
primary đều chạy mới. Lịch48 điểm, quota carry-over và phân tích mẫu nhỏ
được đặc tả trong plan. Hiện READY_COLLECTION, smoke9/cold PASS và grant
pilot đã phát hành;48 điểm nghiên cứu còn chờ người dùng chạy.

## Checklist đánh giá lại

| Bước | Công việc | Trạng thái |
| --- | --- | --- |
| H01 | Audit donor và phạm vi các phương pháp | [x] DONE của thiết kế đầy đủ |
| H02 | Dữ liệu và replica ba seed/60 checkpoint | [x] MODEL_GATE_PASS / CPU_REPLAY_MATCH; giữ asset |
| H03 | Protocol/lịch/dự toán34.806 call | [x] Bằng chứng thiết kế cũ; pilot cần protocol riêng |
| H04 | Adapter/runner9 mã | [x] Bằng chứng thiết kế cũ; pilot cần adapter/runner riêng |
| H05 | 84 test offline,492 prefix,1.020 context | [x] Bằng chứng cũ; kiểm delta pilot trước release |
| H06 | Smoke55 execution và cold verify | [x] Bằng chứng cũ; grant full collection đã REVOKED |
| H07 cũ | Dừng và xóa lượt thu dở | [x] CANCELLED_BY_USER ngày09/11 |
| H07 pilot P01 | Audit bank/cache/quota và feasibility48 giờ | [x] PASS |
| H07 pilot P02 | Khóa48 ID/protocol/runtime/bridge option | [x] PASS |
| H07 pilot P03 | Scoped checks, smoke9 execution và cold verify | [x] PASS |
| H07 pilot P04 | Thu48 điểm/sáu primary/Fact_Anchor | [ ] PARTIAL:12/48 shared;0 forecast nghiên cứu |
| H07 pilot P05 | Cold verify và seal pilot | [ ] TODO |
| H08 | Phân tích paired/uncertainty/coverage | [ ] TODO |
| H09 | Bảng so sánh/evidence và bàn giao | [ ] TODO |

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
Chưa release inference trên lưới mới. Kết quả khóa protocol H03 được ghi bên dưới.

Kiểm lần này: frozen `evaluate`/`verify`, loader/fingerprint và đối soát hash
43 file nguồn/27 file dữ liệu PASS; diff và liên kết đã kiểm. Không sửa
code/test/runtime, không train/refit; không chạy lại compile/unit/E2E/leakage suite
theo AGENTS1.2. Kết quả test fixture trước đây vẫn là bằng chứng lịch sử, không ghi
là đã chạy lại.

## H03 — khóa protocol và dự toán offline

- [x] Tạo [protocol máy](historical_evaluation_protocol.json), gồm registry sáu primary,
  Fact_Anchor dependency, model replica và cấu hình MT-BICL hiệu lực riêng.
- [x] Khóa [input/lịch/schema](historical_evaluation_inputs.json):1.020 unit,
  51 scope,102 anchor và panel51 ID chọn bằng hash trước response.
- [x] Khóa recipe, scaler train-only, PIT/membership, fallback và bootstrap oracle.
- [x] Khóa ma trận calls, dự toán token/latency/chi phí và trần attempt/reserve.
- [x] Kiểm thử theo phạm vi, compile Python mới và đối soát protocol/input/Git.

Protocol cũ, manifest model và dữ liệu H02 giữ nguyên byte. Cấu hình mới là
960/960 token, temperature0, fractional shares (`lot=null`), risk OFF,
reset50 triệu/mã/block/nhánh/realization/repeat. Hai schema response được chụp
từ `TradeDecisionOutput` và reply MT-BICL; alias Original/A_reference không
tạo thêm execution ngoài Original_common/A_tp_pool.

Legacy scaler fit feature trên train IDs của từng scope, freeze trước validation;
MT-BICL giữ scaler/regime cuối2020 của replica. Legacy query HMM giữ artifact
fit tới30/12/2022, historical metadata dùng prefix tại ngày lịch sử.
Giữ bank giá donor riêng, không splice với chuỗi dùng train replica.
Tin date-only khả dụng ngày sau, lookback90 ngày, tối thiểu3 bài, peers rỗng;
provenance/scorer đã khóa nhưng không chứng nhận archived content PIT.

History LLM gồm2.998 cycle theo suffix sạch, warmup600 và stride3. Trong đó640
cycle trùng query được dùng chung đúng upstream realization0 của run mới;
**H=2.358** cycle cần thêm. Thu theo union lịch tăng dần; chỉ cấp history có
`exit<query`, không chèn query ngoài cadence vào legacy bank. MT-BICL giữ
stream numeric theo calendar riêng. Cache donor2048/1024 không được tính là reuse.

| Hạng mục | Nominal executions/calls |
| --- | ---: |
| Sáu primary + Fact_Anchor, ba Decision repeat | 21.420 |
| Mười ablation trên102 anchor, ba repeat | 3.060 |
| Ba retrieval control trên102 anchor, ba repeat | 918 |
| Original_duplicate trên102 anchor, ba repeat | 306 |
| Panel51 unit, thêm hai upstream realization và ba repeat/bảy nhánh | 2.142 |
| Tổng Decision | 27.846 |
| Vision query/panel | 2.244 |
| Vision history bổ sung,2H | 4.716 |
| Tổng research nominal trước bypass/reuse | **34.806** |

Panel là diagnostic upstream, không tham gia tài khoản primary hoặc tăng N thị
trường. Primary chỉ dùng realization0; báo đủ ba repeat và mean, không vote/best.
CI return và BA là hai family riêng, mỗi family năm contrast CORE4; resample
toàn sáu block bằng cùng draw indices. Giữ ties/constant; bất kỳ support null
làm cả family INCONCLUSIVE, không loại contrast hoặc điền0.

Dự toán dùng4.511 response Decision và1.284 response vision thành công trong
ledger cũ; chỉ lưu aggregate, không lưu key/scope/request ID. Giá niêm yết quy
đổi khoảng **20,69 USD** cho research nominal theo usage tham chiếu; dự toán
6500 input+960 output token/call là **84,51 USD**, chưa gồm reserve.
Trần cả attempt/reserve là106.459 HTTP attempt, quy đổi khoảng271,99 USD theo
cùng giả định token. Đây là dự toán, không là invoice hoặc quyền chi tiền.
Giá tham chiếu kiểm08/11/2026 từ
[GPT-OSS20B](https://console.groq.com/docs/model/openai/gpt-oss-20b) và
[Qwen3.8-27B](https://console.groq.com/docs/model/qwen/qwen3.8-27b).

[Quota công bố](https://console.groq.com/docs/rate-limits) tham chiếu30 RPM,
1.000 RPD,8.000 TPM và200.000 TPD/org. Nếu có năm org độc lập và cộng chung
quota token hai model, usage tham chiếu tương đương **68 ngày năng lực token**;
không phải cam kết lịch chạy hoặc phép đo payload960. Trần dự toán token cao
hơn nhiều; cần đối soát ITPM/OTPM/TPD, spend limit, tổ chức độc lập và longest
payload tại H06. Không hứa72 giờ, tự nâng gói trả phí hoặc giảm mẫu/repeat.
Ảnh dự trù khoảng3,40 GiB, RAM dự trù2 GiB; đo tài nguyên mới thuộc H06.

Kiểm H03:18 test PASS trong `test_historical_evaluation_protocol.py`,
`test_historical_evaluation_leakage.py`, `test_historical_evaluation_statistics.py`;
bao phủ lịch/suffix/purge, future/exit==query, deep-copy, reseal, workload/reserve
và oracle scalar độc lập cho CI. Sáu Python mới biên dịch PASS.
Producer offline và verifier tái dựng byte/ngữ nghĩa/Git PASS; không chạy lại
unit toàn hệ thống/E2E hoặc các gate model H02 vì source/runtime cũ không đổi.

Kiểm lại offline, không gọi API:

```powershell
py -3.13 -X utf8 scripts/prepare_historical_evaluation.py --verify
```

Verifier cần các archive/input H02 và ledger tham chiếu local; H09 đóng gói
chúng cùng bằng chứng tái lập. Trạng thái `LOCKED_OFFLINE_NOT_RELEASED`:
API/training/teacher-fit/confirmation đều OFF. H04 đã triển khai bên dưới, tiếp theo H05/H06;
economic acceptance vẫn `PENDING_EXECUTION_DATA`.

## H04 — adapter và runner offline

- [x] Adapter9 mã/lịch2023–2026, ID OOD thật và parity CORE4.
- [x] Context, bank, train-only scaler, frozen student/teacher/regime và nhãn engine PIT.
- [x] Sentiment toàn lưới, date-only ngày sau, tách count/score/mask.
- [x] Shared upstream một lần/unit/realization, deep-copy, ảnh/parent hash và năm factor.
- [x] CLI run/resume/verify/reconcile, ledger riêng, unknown reserve và checkpoint.

Các module `core/historical_evaluation_{scope,data,context,prior,graph,journal,
clients,runner,audit}.py` và [CLI](../../../scripts/run_historical_evaluation.py)
tách đường chạy mới khỏi hệ thống cũ. Adapter nạp bytecode nguồn đã pin vào
namespace riêng, mở universe/vendor calendar tại phạm vi này; không sửa
global hoặc validator của module gốc. Giữ ID thật của OOD, scaler731 cycle
và candidate seed42/step3000. Giá donor không splice với giá train replica;
rào chắn quyền lấy ngày từ raw/event H02 đã hash, không tạo cột Reference giả.

Context stream chặn query chưa đủ forecast durable trước khi tính nhãn;
retrieval bắt buộc `exit<query`. Kiểm dữ liệu tương lai và ID/ngày không hợp lệ
đều dừng bằng lỗi. Unit chỉ mở nhãn qua engine sau toàn bộ forecast cần thiết;
giữ `previous_exit<next_entry` trong mỗi tài khoản. Original và Fact_Anchor
được resolve trước các revision. Mọi repeat/nhánh dùng cùng upstream và ảnh
trong realization, nhận bản sao độc lập.
Cold replay CORE4 luôn giữ kín outcome grid OOD của pha sau, kể cả khi file
OOD đã durable; mỗi instance chỉ chạy một pha để membership không đổi khi resume.
Run thật chỉ cho bắt đầu OOD5 sau khi toàn bộ forecast CORE4 đã durable.

Hai tương thích được ghi rõ trong [runtime H04](historical_evaluation_runtime.json):
Alpha xuất đủ năm dòng tên/giá trị/signal/mask trước distill/cap cũ, tránh
separator Markdown làm mất bảng; formatter v1 dùng flag `allow_sentiment=True`
có sẵn, giữ template T/P/A/I và score tin thật, không ghi lại sentiment thành
NEUTRAL. Renderer donor giữ nguyên bytecode, chạy tuần tự trong cwd tạm để
cô lập file phụ; PNG thật có hash và provenance trong namespace run.

[Audit metadata](../../../outputs/historical_reevaluation/h04_assets/prepared.json)
đã kiểm1.020 context preview,51 scaler scope và540 unit OOD. Có862 preview
AVAILABLE/158 UNAVAILABLE khi chủ động giữ kín outcome của toàn bộ grid;
đây không phải context đóng băng của H07. Coverage tin là213/1.020 unit đủ
ít nhất3 score xác minh,88 unit đạt reliability downstream ít nhất8 bài;
count/missing mask của hai tầng giữ riêng (anchor tương ứng23/102 và9/102).
Không chứng nhận archived content
PIT, fill thực hoặc lợi nhuận từ các số này.

Retry dùng wrapper hiện hành, SDK/HTTP không retry ngầm; trần3 HTTP/slot
bao gồm429 và sửa format. Unknown/crash cần reconcile đúng UUID trước replay,
không tự chuyển lỗi thành CASH. Raw HTTP lưu trước parse, tách ledger năm org,
khóa credential scope, giữ reserve unknown và trần attempt theo H03.
Cold verifier dựng lại body bằng serializer SDK bị chặn mạng, replay node từ
raw response, dựng lại policy và nhãn; checksum tự khai không đủ để qua gate.

Kiểm triển khai H04:32 test riêng biệt PASS trong năm module
`test_historical_adapter_{journal,leakage,methods,runner,transport}.py`.
Bao phủ PIT/query-y, clean suffix, bản sao dữ liệu, hai tầng sentiment,
membership/scaler, parity task/bucket/utility4.096 draws, ID OOD, prompt năm
factor, renderer thật, ma trận27.846 Decision, paired/checkpoint/unknown và
raw HTTP/body/retry. Wire tests dùng mock HTTP trong RAM; fixture vision/Decision
có marker cách ly, không dùng credential hoặc provider. Đã biên dịch15 Python
mới, kiểm runtime/source và verifier H03 PASS; không chạy toàn suite/E2E hay
train/refit/đánh giá lại model H02 theo phạm vi AGENTS1.2.

Lệnh audit không fit/gọi LLM:

```powershell
py -3.13 -X utf8 scripts/run_historical_evaluation.py prepare
py -3.13 -X utf8 scripts/run_historical_evaluation.py run --fixture --cohort OOD5 --max-units 1
py -3.13 -X utf8 scripts/run_historical_evaluation.py verify --fixture --cohort OOD5 --max-units 1
```

`run/resume` dùng checkpoint complete, không gọi lại slot đã hoàn tất;
`--max-units` giới hạn số unit mới, còn `verify` giới hạn số unit được kiểm.
Lệnh thật thiếu release H06 đã được kiểm là dừng trước đọc key/HTTP.
H04 hoàn tất triển khai offline; H05 được nghiệm thu ở mục dưới, H06 chưa release.

Trước thu thập cần492 model HMM historical prefix, tách khỏi query HMM2022
và HMM/scaler train replica. Chưa fit các model mới trong H04; runner preflight
dừng trước vision nếu thiếu. Theo chỉ đạo người dùng tự chạy khi cần train,
lệnh CPU được bàn giao tại [checklist H04](historical_reevaluation_plan.md#h04--hoàn-thiện-adapter-và-runner):

```powershell
py -3.13 -X utf8 scripts/run_historical_evaluation.py prepare-regimes
```

Lệnh lưu từng prefix, kiểm lại model đã có khi chạy tiếp; không train
teacher/student, không GPU/LLM. H05 kiểm nghiệm thu theo phạm vi, H06 khóa
receipt/runtime/Git, kiểm longest payload và quota năm org trước API.

Sửa lỗi `prepare-regimes`: lệnh cũ gọi trực tiếp primitive chỉ cho fit2018–2022,
nên dừng khi prefix đầu tiên sang2023. Adapter nay nạp cùng bytecode HMM đã pin
vào namespace historical riêng, mở biên fit/validation tới30/09/2026 cho cả
producer và loader/preflight của runner. Giữ nguyên tham số, scaler/calibration,
checksum/schema artifact; model query2022 và model/scaler MT-BICL không đổi.
Runtime H04 được nâng lên `historical_h04_runtime_v2` trước release; bản v1
vẫn được giữ nguyên tại Git `cb9cf9c0`. Không có research run cần migrate.

Đã kiểm lại51 prefix local tới29/12/2022: đúng training hash và giữ nguyên byte.
Chạy lại `prepare-regimes` dùng tiếp51 file này, chỉ fit441 prefix còn thiếu.
Chưa chạy phần fit production còn lại; không cần xóa thư mục hoặc train replica.

Kiểm sửa lỗi:17 test PASS gồm6 test mới trong
`test_historical_regime_prefix_leakage.py` và11 test adapter leakage hiện hành.
Đã numerical fit fixture synthetic qua2023 và2026, so byte artifact legacy,
kiểm save/load, guard2022 gốc, future poison/cutoff, resume không refit/ghi đè,
hash sai và runner load/preflight. Bốn Python thay đổi biên dịch PASS; source/
model/protocol/input H02/H03 giữ nguyên byte. Đây là kiểm theo đường sửa lỗi;
không chạy lại32 test H04, full suite/E2E hoặc492 model production.

## H05 — nghiệm thu offline

- [x] Người dùng hoàn tất492 HMM prefix; đối soát toàn bộ hash, cutoff và classification.
- [x] Dựng lại1.020 context và kiểm D/C/query/PIT/schema, khớp byte-ngữ nghĩa preview H04.
- [x] Forward862 context AVAILABLE bằng student frozen, kiểm fingerprint sau forward.
- [x] PASS84 test thuộc13 module đã chọn; không skip, error hoặc failure.
- [x] Biên dịch2 Python mới; kiểm source/runtime/model/data giữ nguyên sau nghiệm thu.

[Receipt máy H05](historical_evaluation_validation.json) khóa source/test/helper,
protocol/input/model/runtime/preview,492 checksum model prefix và checksum log.
Prefix từ31/05/2022 tới17/09/2026:480 HMM và12 MULTI_FACTOR theo calibration
của recipe, không bỏ model fallback hoặc chọn lại theo kết quả. Query HMM2022,
student/teacher/scaler replica và runtime H04 v2 giữ nguyên byte.

Nhóm kiểm được chọn theo đúng đường H04/H03 sử dụng, gồm năm module
`test_historical_adapter_*`, `test_historical_regime_prefix_leakage`, ba module
`test_historical_evaluation_{protocol,leakage,statistics}`, cùng
`test_mt_bicl_{adapter_leakage,features_leakage,utility}` và
`test_historical_validation_leakage`. Chúng bao phủ label/cost bằng oracle cash
hai chiều trên fixture9 mã, lịch/suffix và exit==query, future/query-y poison,
membership/scaler/regime, OOD/model fingerprint, paired/deep-copy, năm factor,
prompt/utility4.096 draws, journal/unknown/retry/resume/raw HTTP và bootstrap
scalar10.000 draw. Kiểm32 test H04 được chạy lại trong nhóm84 test này;
không chạy unit toàn hệ thống/E2E hoặc lặp lại60 checkpoint/model gate H02.

Audit context giữ kín outcome của toàn grid;862 AVAILABLE/158 UNAVAILABLE
khớp preview H04. Đây là kiểm hợp đồng/frozen forward, chưa phải context
prequential cuối cùng H07 hoặc kết quả hiệu quả thị trường. Các model HMM
production đã được người dùng fit; lượt H05 không refit chúng hoặc teacher/student.
Test numerical fit chỉ dùng fixture tổng hợp trong thư mục tạm; HTTP/vision/Decision
dùng mock/fixture cách ly. Tổng API thật0; economic acceptance vẫn PENDING_EXECUTION_DATA.

Chạy nghiệm thu đầy đủ:

```powershell
py -3.13 -X utf8 scripts/validate_historical_evaluation.py
```

Lệnh kiểm asset/context, chạy84 test và biên dịch đúng hai Python mới.
Phần paired fixture/cold replay có thể mất vài phút; xem log tại
`outputs/historical_reevaluation/h04_assets/h05_validation.log`.
Thời gian chạy không tham gia checksum log. Chỉ ghi PASS sau toàn bộ gate;
source/asset đổi hoặc test lỗi phải dừng, không ghi đè receipt khác.

Kiểm nhanh bằng chứng đã neo Git, không chạy lại tests:

```powershell
py -3.13 -X utf8 scripts/validate_historical_evaluation.py --verify
```

Verifier cần model prefix và log local đúng checksum; H09 sẽ đóng gói cùng
bằng chứng tái lập. H06 tiếp tục freeze/smoke/longest payload/quota năm org;
H05 không cấp quyền chạy research API hay tự đổi ngân sách/model.

## H06 — freeze và live smoke PASS

- [x] Neo [freeze](historical_evaluation_freeze.json), source/runtime/model/data/protocol/IDs; đối soát H05 và492 prefix.
- [x] Live smoke sáu primary/Fact_Anchor, ảnh thật và control báo cáo bão hòa/BRPP600 trên5 org.
- [x] Schema/options/credential scope/quota, output960, đủ5 factor và utility4.096 draws.
- [x] Cold verify PASS không API; neo [receipt smoke](historical_evaluation_smoke.json), release H07 chỉ Free/0 USD.

Kết quả:55 HTTP200 (45 Decision+10 vision), tất cả `finish_reason=stop`,
completion tối đa319 token. Hai HTTP503 `over capacity` tại pattern/trend org5
đã đối soát raw response và reconcile đúng UUID, giữ nguyên org/key/model/payload;
57 HTTP tổng, không429, không còn slot chờ. Mỗi org1–4 có11 lượt, org5 có13;
5 credential scope khác nhau trong ledger. Cold verify dựng lại graph, prompt,
raw/parsed reply, utility/policy và record hash; vẫn57 HTTP sau kiểm.
Log/raw/ảnh/checkpoint tại `outputs/historical_reevaluation/h06_smoke_r1/`.
Hash log cold verify được ghi trong [grant](historical_evaluation_release.json).

Prompt live tối đa5.954<6.500 ký tự, MT control tối đa5.301; reserve vision
5.471/5.110, Decision tối đa3.856<8.000 TPM/request. Giữ distill/cap, BRPP600,
max_tokens960 và model/options H03. Đây là control báo cáo bão hòa cùng payload
ảnh thực; không khẳng định đã quan sát mọi payload tương lai của lưới H07.

[Quota đã khóa](historical_evaluation_quota.json) là USER_ATTESTATION:
5 key thuộc5 org độc lập, cả hai model30 RPM/1.000 RPD/8.000 TPM/200.000 TPD,
không tách ITPM/OTPM, chỉ Free/0 USD. Header live xác nhận trần1.000 request/
8.000 token; không giả là provider org ID hoặc bằng chứng Console đầy đủ.
[Plan smoke](historical_evaluation_smoke_plan.json) khóa55 execution/trần300 HTTP;
pacer/ledger riêng từng org, không xoay key khi hết quota.

Preflight phát hiện schema reply MT-BICL vô danh không được SDK chấp nhận.
[Amendment transport](historical_evaluation_transport_amendment.json) chỉ thêm
`title=UtilityICLReply` tại adapter SDK; schema khoa học, fields/enum và Original
giữ nguyên. Runtime v3 thay đúng hai file clients/audit, thư viện không đổi.
[Runtime v2 nguyên byte](historical_evaluation_runtime_pre_schema_title.json) và
receipt H05 được giữ làm baseline.10 test PASS gồm6 test trong
`test_historical_live_smoke` và4 test `test_historical_adapter_transport`;
5 file Python mới/đổi biên dịch PASS. Không chạy lại84 test hoặc full suite/E2E:
H05 được đối soát hash cho phần không đổi, delta wire có hồi quy mới.
Lượt kết sổ chỉ sửa tài liệu/grant/receipt, kiểm diff/hash/liên kết, không chạy lại suite.
Lệnh freeze/H05 v2 ở mục trước là lịch sử; verifier hiện hành kiểm baseline và delta:

```powershell
py -3.13 -X utf8 scripts/run_historical_smoke.py verify
```

Smoke cách ly ở namespace riêng; upstream thật một lần/org rồi deepcopy tới
các nhánh. Historical agent signals là fixture lặp từ query để kiểm support;
giá/nhãn/regime quá khứ thật, chỉ lấy cycle non-grid exit<query. Đây không là
archival PIT tín hiệu LLM hoặc kết quả H07; không import bank/control response
vào research, không mở payoff query. Original→Fact_Anchor→MT dùng raw reply thật;
không giả facts, sửa fallback hoặc đổi lỗi thành CASH.

[Grant](historical_evaluation_release.json) từng RESEARCH, hiện REVOKED; bằng chứng protocol/runtime,
H05/quota/plan/amendment/smoke PASS. Thiết kế CORE4→OOD5 đã hủy; thay bằng
[kế hoạch pilot](historical_reevaluation_plan.md#h07--pilot-ghép-cặp48-điểm-bằng-api-free).
Collection full đã hủy và output đã xóa; pilot cần grant/runtime riêng.
Economic acceptance vẫn PENDING_EXECUTION_DATA; H06 không thay đổi giới hạn vendor series.

## H07 — chuyển sang pilot Free ngày09/11/2026

Theo chỉ đạo người dùng, đã dừng supervisor và child thu thập; không còn
tiến trình run_historical_collection hoặc run_historical_evaluation của H07.
Đã xóa outputs/historical_reevaluation/run_r1/ và managed_r1/, gồm398 và12
file tại thời điểm dọn. Các log kiểm vận hành từng nằm trong run_r1 cũng
được xóa cùng lượt dở. Không có forecast grid nào được giữ làm kết quả.

Chỉ giữ quota tối thiểu tại outputs/historical_reevaluation/quota_history/
cancelled_run_r1/,103 request với264.449 token đã tính/reserve;93 HTTP200,
7 HTTP503,3 transport_error. Không giữ prompt/report/ảnh/nhãn ở ledger này.
P01 phải cộng lịch sử quota này và H06 vào accounting thực, kể cả unknown.

Grant full collection đã thu hồi bằng status=REVOKED, api=false; H06 smoke
vẫn là bằng chứng lịch sử. Protocol full/input/schema/runtime/H02 model,
donor và HMM prefix giữ byte cũ. Pilot đã có collector, protocol/input/runtime
và grant PILOT_RELEASED riêng; smoke/cold PASS, collection chờ người dùng chạy.

Plan chốt48 điểm theo lịch, Bayesian bank frozen, shared reports chung và
Decision mới. Có điều kiện audit bank/cache/token trước cam kết48 giờ;
nếu không đủ phải ghi BLOCKED_BUDGET hoặc PARTIAL, không chọn lại mẫu theo
outcome. Giữ scope historical exploratory và giới hạn provenance bank/query.

Đợt cập nhật sửa Markdown, trạng thái grant và ignore cho ledger quota local;
không đổi Python, thuật toán, model, query input hoặc runtime. QA theo AGENTS1.2 gồm lịch/ID/call
math, liên kết/diff, hash asset, quota projection và guard từ chối grant
REVOKED trước API. Không chạy compile/unit/E2E toàn hệ thống; gate cũ
không được ghi là gate pilot mới. QA PASS cho48 ID/ngày/holding spans,
call math336/432/1.323 attempt, toàn bộ link/fragment/fence của ba Markdown,
projection quota103 request/264.449 token và absence hai thư mục đã xóa.
Chín file bank/model/protocol/input/runtime/receipt đối soát với1213c076
giữ nguyên byte. Consumer require_release trên grant đã commit từ chối đúng
lỗi REVOKED, socket mock xác nhận0 kết nối. Diff check PASS, main/fix giữ ref.

### Pilot48 — sẵn sàng thu thập do người dùng chạy

- [x] P01: bank852/native labels/scaler≤2022;12 ngày/48 ID cố định; audit nguồn
  query/cache và carry160 request/396.206 token. Reuse0, vision mới96.
- [x] P02: collector riêng, protocol/input/runtime/grant PILOT_RELEASED;
  bridge OFF, smoke org5,48 query round-robin. Grant full vẫn REVOKED.
- [x] P03: offline PASS18 test pilot và38 test hồi quy; live smoke9/cold PASS.
- [ ] P04/P05: seal48 shared, release riêng,336 forecast và cold receipt.

Lệnh chạy và giới hạn nguồn được cập nhật trong
[plan H07](historical_reevaluation_plan.md#h07--pilot-ghép-cặp48-điểm-bằng-api-free).
Từ đây người dùng chạy API; agent không tự thu thập. Preflight khoảng44 giờ
gồm retry reserve20%, chưa bảo đảm48 giờ hoặc mục tiêu thu24 giờ.

QA theo AGENTS1.2: compile bốn Python mới;18 test pilot kiểm PIT/query-y,
bank transfer/full population, paired/cold policy, prompt, carry/deadline/
grant/checkpoint.38 hồi quy thuộc price_feature_index_leakage,
prior_price_similarity_leakage, historical_adapter_transport,
historical_reset_recovery, historical_adapter_journal và backtest_token_budget:
bao phủ primitive giá/PIT, SDK wire, retry/checkpoint và prompt được tái dùng.
Không chạy full suite, E2E hay train lại; chưa ghi smoke hoặc H07 DONE.
Logs local trong free_pilot_r1: offline_tests.log PASS50 (12 pilot ban đầu+
38 hồi quy); pilot_tests.log PASS15; grant_tests.log PASS11, tám test trùng,
tổng18 pilot riêng biệt. Source runtime được khóa trong free_pilot_runtime.json.
SHA256 ba log lần lượt81011394c0c0a6b3ceeb94f8bf7281945bb3c7a828ea82318ac24266fa03def3,
f311fadc4441ef3a8aad7264410565e3ca25f0633bc6f97a45f39c7896260cb1,
3c0437bc102e43503ea127f0dbca6453afddddee21b0581117ce0a492cd1f243.

Khắc phục khởi động smoke: CLI chưa tự nạp `.env`; kiểm tra cục bộ xác nhận
cả năm credential có giá trị, không xuất key. Ledger vẫn0 request pilot,
slot graph/FPT-2023-06-23/u0/indicator có attempt unknown
80890094-073d-436b-9253-6e7aec50d066 trước tạo client. Người dùng reconcile
đúng UUID này với lý do chưa gửi HTTP, rồi chạy bootstrap dotenv trong plan.
Giữ nguyên UUID run, checkpoint, runtime và quota. QA thay đổi thuần hướng dẫn:
bootstrap `--help` PASS với socket chặn mạng; đối soát hash source/runtime;
không chạy lại compile, unit hoặc E2E vì không đổi code/config/dữ liệu khoa học.

Nghiệm thu smoke và release:9/9 HTTP200 ở org5,7 Decision+2 vision,
19.611 token;12 slot complete,0 latest unknown. Cold replay offline được
kiểm lại với socket chặn mạng; evidence/checkpoint/usage/ảnh giữ byte.
Source/runtime và các gate scoped trên giữ nguyên; không chạy lại unit/compile/E2E.
Grant bind smoke_verified.json SHA256
1d2e895c3845ac963741556f4bf0be7841692022db3b02d163358b83682d6e24,
UUID3881b4ba-4609-460a-8137-5fbad4f617db. Log release_verify.log SHA256
9a93d04f75573cbe46aa68b86605d029f533e3ce00d53d454d962e8c8442fcf4.
Ngân sách còn lại PASS khoảng42,7 giờ; deadline01:56:52 ngày11/11/2026 UTC+7
giữ nguyên. Người dùng chạy shared→collect→verify theo plan; P04/P05/H08 chưa DONE.

Mốc chuyển sang supervisor:12 shared nghiên cứu complete;0 forecast, một
latest unknown ở Pattern FPT-2023-08-17/org3. Hai raw HTTP503 đều khớp
checksum, chưa có HTTP200; supervisor v2 tiếp tục retry lỗi tạm thời. UUID db3f3d2a đã
authorize, UUID cuối1066b007-e5d1-433a-93ee-46b2fe8c1bc7 được tự nhận diện.

### Một lệnh chạy và tiếp tục pilot

Chạy `py -3.13 -X utf8 scripts/run_free_pilot.py` ở thư mục gốc repo. Lệnh tự
nạp `.env`, chọn shared→collect→verify từ checkpoint thực, kiểm và reconcile
attempt cuối, chờ503/429/quota có proof. Nếu bị ngắt, dùng lại cùng lệnh;
không chép UUID cũ. Raw200 đủ proof được replay cùng UUID/node/policy, không
gửi API mới. Theo yêu cầu người dùng, v2 bỏ trần cộng dồn HTTP/slot, tăng
backoff tối đa900 giây rồi tiếp tục retry lỗi tạm thời. Giữ toàn bộ carry/
reserve, quota Free, ngân sách toàn lượt và deadline48h. Dispatch chưa rõ/
lỗi source vẫn được báo rõ, không giả output. Không tự gia hạn48h.
Worker cũ còn chạy thì chờ OS lock; supervisor đang chạy thì không tạo bản trùng.

Manifest bổ sung free_pilot_manager.json pin source điều phối, policy và
base grant/identity. Protocol, runtime inference, model, smoke và checkpoint
được giữ nguyên. Worker dùng CLI đã khóa; wrapper chỉ thêm rào source bổ sung
và phục hồi có proof. manager/collection_receipt.json khi hoàn tất bind
manifest này với receipt P05, không tự làm H08 hoặc đánh dấu pilot tổng DONE.

QA supervisor v1 tham chiếu: PASS21 test mới,26 hồi quy liên quan (supervisor cũ, reset recovery,
journal và SDK transport). Có test end-to-end fixture shared→503→resume→collect→
verify và chạy lại sau complete; kiểm replay vision/Decision raw200 giữ UUID/
HTTP/quota, source/schema/payload tamper, attempt cũ, quota reset và trần3.
Compile đúng bốn Python mới; không chạy full unit/E2E/leakage suite vì không
đổi primitive dữ liệu/PIT/retrieval/kinh tế. Gate56 trước đó giữ phạm vi inference
cũ; không ghi là đã chạy lại. Không gọi API thật hoặc tự chạy collector.
Log local manager_tests.log PASS37 (15 test mới ban đầu+22 hồi quy),
manager_final_tests.log PASS22 (18 test mới+4 SDK), manager_release_tests.log
PASS20 và manager_orphan_test.log PASS1 kiểm worker cũ còn giữ OS lock.
SHA256 ba log đầu tương ứng:
8e2318a2ae8f756b74042490f29208f0e182195b15f9e6ad4c5c0c1b71731ad1,
f74b465ed9610b80ccc85d71908b88f65cb29673d34142885784e255b3661178,
d67c5158b7efcd48a723bdc8ae7a5c3e899b6a93f0ffc1c6c80b4a6b46af2fea.

Delta v2 theo chỉ đạo bỏ trần slot: policy/source bổ sung được khóa lại,
giữ UUID/checkpoint/cold smoke/runtime inference. Worker thay guard cộng dồn
của observer cũ bằng attempt hữu hạn nối tiếp tự động; timeout hữu hạn,
TCP mới/SDK không retry ngầm và mọi reserve/raw/audit vẫn giữ. Manager dùng
lại token khóa OS qua revision, không xóa owner hoặc lịch sử quota.
PASS50 kiểm tra liên quan:22 test manager/recovery,8 reset cũ,5 journal,
4 SDK transport và11 quota/boundary. Có wire test gửi được HTTP thứ5 sau
bốn reset, body/timeouts/ledger không đổi; retry sau7 lỗi vẫn tiếp tục và
backoff dừng tăng ở900s. Compile bốn Python thay đổi, không chạy full suite/
E2E toàn hệ thống hoặc train vì không đổi dữ liệu, retrieval, prompt hay kinh tế.
Log manager_unbounded_tests.log PASS35, SHA256
a26e4806ce6d2a552ddd5cde3cf27804f1f724c30d94ec503c04891b1de8c101;
manager_unbounded_contract_tests.log PASS15. Agent không gọi API thật.

<!-- FREE_PILOT_MANAGER_START -->
Trạng thái **NOT_STARTED**; đã giữ12/48 shared và0/336 forecast nghiên cứu.
<!-- FREE_PILOT_MANAGER_END -->
