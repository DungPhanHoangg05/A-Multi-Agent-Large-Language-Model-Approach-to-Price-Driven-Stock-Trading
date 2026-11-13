# Contract ứng dụng chọn phiên bản

Contract `variant_serving_v1`, registry `variant_serving_registry_v1`, config
`serving_config_v1`. Đây là giao diện riêng của ứng dụng Flask hiện hành;
`unified_variant_registry_v2` và `unified_experiment_v1/v2` tiếp tục nhận diện
phương pháp và replay nghiên cứu. Không đổi expected hash/receipt lịch sử.

**F08 đã có backend inference as-of riêng**: resource
`serving_asof_q3_2026_v1`, runner `serving_runner_v1`. Các ghi chú “chưa mở”
ở mốc F06/F07 bên dưới là lịch sử; trạng thái hiện hành là grant có điều kiện
qua server preflight và miền cụ thể trong mục tiếp theo. Không mở lại grant
nghiên cứu U08, không dùng API key từ body request.

## Chạy serving as-of từ F08

Miền công bố: **1d/VI**, BHN/CMG/FPT/HVN/MBB/MWG/VCB/VJC/VNM, **58 phiên
01/07–23/09/2026** trong calendar đã pin. Đây là dữ liệu vendor historical
frozen; **chưa hỗ trợ giá/tin mới nhất hiện tại, intraday hoặc EN**. Query mới
được dựng từ giá as-of và chạy upstream/Decision mới, không lookup forecast
hay prepared response U09. Bank CORE4/OOD fallback và MT eligible/bypass giữ
đúng policy; “chạy được” không có nghĩa mọi nhánh luôn đủ support để gọi LLM.
Thiếu/hỏng resource là lỗi, không được chuyển thành fallback thành công.

Resource manifest [serving_resources_v1.json](serving_resources_v1.json) khóa
**188 input binding**, tham chiếu nguyên byte các component đã có; không nhân
bản weights hoặc thay manifest/receipt cũ. Source và runtime SDK/scientific
được bind riêng cho mỗi job. Cần checkout Git với nguồn historical còn truy
cập được và các dependencies/runtime đã cài theo dự án, Python 3.13.5. Chuẩn bị:

```powershell
py -3.13 -X utf8 scripts/prepare_serving_resources.py --restore-assets --verify
```

Lệnh khôi phục asset ignored từ gói U06 đúng SHA/member binding; không ghi đè
file hiện có khác hash. Không fit HMM/student/bank, không gọi thị trường/LLM.
Selector được kiểm integrity bằng replay đúng train/validation cũ, không chọn
lại trên query; native Alpha giữ hành vi tính/selection của profile gốc trên
prefix. Nếu tokenizer o200k chưa cache, preflight báo TOKENIZER_NOT_READY;
có thể chuẩn bị cache bằng `py -3.13 -c "import tiktoken; tiktoken.get_encoding('o200k_base')"`
(chỉ tải tokenizer khi thiếu, không inference).

Chạy app hiện hành; API key lấy từ cấu hình server hiện có hoặc `GROQ_API_KEY`.
`GET /api/serving/v1/defaults` trả đủ model/options đã mở cho client. Pattern/
Trend dùng `qwen/qwen3.8-27b`, Decision dùng `openai/gpt-oss-20b`; Indicator,
Alpha và sentiment là numeric/frozen-score, không gọi LLM riêng dù request
snapshot đủ sáu role. Provider thực tế có thể trả lỗi/quota; chỉ kiểm HTTP
fixture trong F08, chưa chứng nhận smoke hosted mới hoặc độ chính xác khoa học.

| Endpoint mới | Kết quả | Hành vi |
| --- | --- | --- |
| `GET /api/serving/v1/defaults` | 200 | Model/options, registry, role execution; không key |
| `POST /api/serving/v1/preflight` | 200 ready/blocked | Kiểm resource/hash, calendar, language, model/tokenizer/key; không inference |
| `POST /api/serving/v1/jobs` | 202 / 409 | Snapshot riêng rồi start nền / bị preflight chặn |
| `GET /api/serving/v1/jobs/<run_id>` | 200 / 404 | Chỉ đọc checkpoint thuộc owner, không khởi động LLM |
| `POST /api/serving/v1/jobs/<run_id>/stop` | 202 | Body `{}`, dừng tại ranh giới an toàn |
| `POST /api/serving/v1/jobs/<run_id>/resume` | 202 / 409 | Body `{}`, giữ UUID/config/model/key binding/slot |

POST cần JSON cùng origin. Cookie owner ký, HttpOnly/SameSite Strict, được
giữ qua preflight/start và các lần poll/control. Sai owner trả 404. Đổi key
server không hotswap job cũ; muốn resume phải khớp credential scope đã bind.
API key không nằm trong config/status/checkpoint public; HMAC fingerprint ở
kho private chỉ ánh xạ sang UUID opaque, browser chỉ nhận digest của scope.

Ví dụ PowerShell dùng model/options do server trả; **POST jobs thực sự gọi
Groq** khi preflight ready. Ví dụ không tự gửi nếu thiếu key/resource/support:

```powershell
$servingBase = 'http://127.0.0.1:5000/api/serving/v1'
$servingDefaults = Invoke-RestMethod "$servingBase/defaults"
$servingSpec = @{
  version = 'variant_serving_v1'; mode = 'compare'
  variant_ids = @('original_fix', 'bayesian_v1', 'C2', 'A_tp_pool', 'B_semantic', 'MT_BICL')
  symbols = @('FPT'); start_date = '2026-07-02'; end_date = '2026-07-02'
  timeframe = '1d'; language = 'vi'; repeats = 1; models = $servingDefaults.models
}
$servingBody = [Text.Encoding]::UTF8.GetBytes(($servingSpec | ConvertTo-Json -Depth 12))
$servingCheck = Invoke-RestMethod -Uri "$servingBase/preflight" -Method Post -ContentType 'application/json' -Body $servingBody -SessionVariable servingSession
if ($servingCheck.run_enabled) {
  $servingRun = Invoke-RestMethod -Uri "$servingBase/jobs" -Method Post -ContentType 'application/json' -Body $servingBody -WebSession $servingSession
  Invoke-RestMethod -Uri "$servingBase/jobs/$($servingRun.run_id)" -WebSession $servingSession
}
```

Backtest chọn tối đa 30 point/job, lấy mỗi ba phiên từ đầu cửa sổ từng mã để
không chồng vòng vốn; repeat 1–3. Cùng point có một I→P→T/Alpha/sentiment,
deep-copy sang các nhánh; dependency chạy một lần/repeat. Chọn cả sáu bản
tối đa tám Decision slot/repeat và hai vision request/point trước retry.
Preflight trả upper bound attempt; fallback/bypass không được tính là API call.

State private tại `outputs/serving_inference/v1/`, tự ignored. Một job có
input-resource manifest hash bất biến và shared-report hash riêng từng point;
ảnh đặt theo run/point, không dùng cwd/ảnh chung. Journal/raw fsync trước
dispatch/parse; SQLite quota chung mọi serving job/key/model, không chia quota
theo từng model hoặc hotswap key để né giới hạn. Reserve UNKNOWN, usage thực,
headroom/reset headers, 429/5xx và backoff đều bền qua resume; chờ bằng các nhịp
ngắn có thể stop. Ledger không biết traffic legacy/bên ngoài trước khi thấy
header provider, nên không bảo đảm quota còn lại của tài khoản trên server.

Timeout/response mơ hồ giữ UNKNOWN, `retryable:false`; resume không gửi lại
UNKNOWN. Operator local phải đối soát request UUID và bằng chứng trước khi
dùng `Calls.reconcile_not_sent`; không có endpoint browser tự reset hoặc xóa
attempt cap. Complete raw sau crash được replay cùng UUID, không gọi lại LLM.
Source/runtime/resource đổi thì dừng; không ký lại identity cũ để chạy tiếp.

Outcome chỉ mở sau đủ forecast durable của đúng point/repeat/dependency và chỉ
ở mode backtest; provider tự kiểm journal barrier. Analyze/compare luôn giữ
P&L null/NOT_EVALUATED. LONG dùng oracle kinh tế chung, SHORT=CASH có P&L 0.
Partial/failed/unknown giữ rows đã xong, tiến độ tách point/slot/API attempts;
không dựng slot thiếu thành CASH. Kết quả/chi tiết có raw/final, policy reason,
requested/effective IDs, snapshot/provenance. F09 đã nối form/kết quả;
F10 đã nối backtest/experiments. F08 không sửa template hoặc endpoint native legacy.

## Form và kết quả từ F09

Mở `/` hoặc `/demo`, chọn nguồn **As-of** và một mã/ngày trong miền công bố.
Mặc định Hệ gốc; “Phân tích” chạy bản trong dropdown, “So sánh phiên bản” chạy
các checkbox đã chọn (ít nhất hai, mặc định Hệ gốc + Bayesian v1). Các dependency
tự chạy và hiện trong phần nâng cao. Chọn nguồn realtime legacy để dùng form
mã/khung cũ với Hệ gốc; luồng này không nhận các bản mở rộng.

Giao diện VI/EN không đổi ngôn ngữ report đã có. Provider mới hiện chỉ hỗ trợ
VI; chọn report EN sẽ bị chặn thay vì tự đổi sang VI. Repeat và options của
Decision/Pattern/Trend nằm trong cấu hình nâng cao; tên model lấy từ server.
Đổi input hoặc lưu key làm hết hiệu lực preflight cũ. Chỉ grant mới tương ứng
mới bật nút; server vẫn preflight lại khi tạo job. Start có gọi Groq thực nếu
đủ tài nguyên/key; mở trang hoặc đọc kết quả không gọi inference.

Kết quả mở `/output?serving_run=<UUID>`, giữ cookie owner để reload/stop/resume;
link job gần nhất trên form chỉ lưu UUID, không lưu key hoặc raw response.
Các card tách raw/final/action/effective ID/reason, dependency thu gọn. Chart,
ảnh và reports lấy từ một snapshot; Alpha native/common ghi rõ hai projection.
Chi tiết thêm `policy_details[slot].context = {trace, aux}` từ prepare durable,
không tính lại context qua GET. P&L analyze/compare luôn “Chưa có kết quả”;
không dùng giá thoát tương lai hoặc xếp hạng khi partial. UNKNOWN cần operator
đối soát, UI không tự resume/resend. Nếu POST start mất phản hồi, không tự gửi
lại; dùng link gần nhất nếu có hoặc kiểm nhật ký server trước khi tạo job khác.

UI serving mới dùng text DOM cho nội dung model và PNG base64 cho ảnh; không
đọc ảnh/sessionStorage legacy. CSS/JS/partial tách theo chức năng, có layout
mobile/focus; browser desktop/mobile chưa kiểm do host không khả dụng, giữ ở F11.

## Backtest và so sánh từ F10

Mở `/backtest`, chọn nhiều mã, cửa sổ query, phiên bản và repeat; model/options
nằm trong cấu hình nâng cao. Default Hệ gốc + Bayesian v1, FPT 02–07/07/2026.
Preflight cho biết point, Decision slot và trần API attempts trước start.
Giới hạn vẫn ≤30 point/job, step ba phiên, 1d/VI; không tự đổi dữ liệu sang latest.
`/backtest?run_id=<UUID>` đọc job cũ với cookie owner, có stop/resume. Link
“Full/No-Alpha cũ” dùng `/backtest?source=legacy`, giữ endpoint/native engine cũ.

`GET /api/serving/v1/jobs` trả catalog **backtest thuộc owner**, không dùng UUID
để vượt quyền. `GET jobs/<UUID>/evaluation` đọc checkpoint, kiểm forecast/outcome
barrier rồi mới mở giá bound để đánh giá; không chạy lại upstream/retrieval/LLM.
Source evaluator/runtime và manifest giá phải khớp job. Metrics dùng helper account
và classification U09, không sửa oracle Open(t+1)→Close(t+3), SHORT=CASH và phí.
Summary/classification là mean từng repeat; return là mean account mã/repeat độc
lập, không phải portfolio. Daily NAV EOD và return cuối chu kỳ có units riêng,
Sharpe/Sortino không annualize. Undefined giữ null, không chuyển sang zero.

Summary/NAV/contrast chỉ có khi **toàn job đủ common support và outcome**;
partial vẫn xem được các forecast đã hoàn tất và coverage, không xếp hạng.
Query filter đóng: `methods`, `baseline` (native/common đã chạy hoặc `none`),
`symbol`, `repeat`, `start_date`, `end_date`. Các filter tính lại metric trên
cùng subset; không nhận run/config/owner mới hoặc filter trùng. Contrast chỉ có
point estimate cùng job/input/model/options/repeat, không có CI/p-value mới.
Biểu đồ chọn một mã/repeat, không cộng NAV các account độc lập.

`GET jobs/<UUID>/export` nhận cùng filter, thêm `format=json|csv` và `table`:
`predictions|summary|accounts|daily_nav|cycles|contrasts|per_repeat`. JSON/CSV đi
qua cùng evaluator, giữ provenance/units, attachment/nosniff/no-store và chặn
công thức CSV. GET không tự resume, sửa resource pin hoặc xóa cap UNKNOWN.

`/experiments` giữ U09 mặc định và thêm kind `serving_backtest`; có thể mở thẳng
`/experiments?kind=serving_backtest&run_id=<UUID>`. Hai run không được ghép thành
paired contrast. Kind `legacy_backtest` dùng adapter riêng cho file tên hợp lệ
`backtest_result/backtest_<SYMBOL>_<YYYYMMDD>_<HHMM[SS]>.json`; API đọc tại
`/api/serving/v1/legacy-backtests[/<ID>[/export]]`. Đây là file local từ ứng dụng
cũ, không có owner lịch sử; không trộn vào catalog job private hoặc U09.
Vai trò là `legacy_full`/`legacy_no_alpha`, không alias common; số liệu nguồn
ghi `LEGACY_DECLARED_NOT_RECERTIFIED`. Thiếu/lỗi giữ NA, không suy thành CASH.
Không chứng nhận lại economics của file cũ qua adapter. Browser desktop/mobile
vẫn chờ F11 do host không khả dụng; kiểm offline dùng HTTP fixture.

## Nghiệm thu F11 và preview fixture

[Receipt tích hợp](serving_integration_acceptance.json) và
[gói QA](serving_integration_checks.zip) đang có trạng thái
`OFFLINE_PASS_BROWSER_PENDING`, **không phải F11 hoàn tất**. Tám test mới kiểm
HTTP hai job/provider thật đồng thời, restart trên store bền vững, support522
và rào chắn preview. Gate F10 156 Python + 31 DOM được viện dẫn sau đối soát
nguồn/log/runtime107, không chạy lại vì ứng dụng không đổi.

```powershell
py -3.13 -X utf8 scripts/check_serving_acceptance.py
py -3.13 -X utf8 scripts/check_serving_acceptance.py --run
py -3.13 -X utf8 scripts/serve_serving_review.py --port 5051 --seed --duration 900
```

Lệnh đầu chỉ đối soát receipt/member/source/runtime/evidence. `--run` chạy lại
đúng suite F11 tám test và biên dịch tám Python mới rồi ghi QA/receipt, không
gọi hosted LLM/thị trường. Không có cờ tự đánh PASS browser. Nếu ứng dụng hoặc
runtime khác F10, script từ chối viện dẫn; phải chọn lại test đúng phần đổi.

Preview chỉ bind `127.0.0.1`, in URL form và UUID seed backtest sáu bản.
HTTP Groq dùng fixture, provider/resource/UI vẫn thật; native Alpha vẫn tính/
selection. Key cố định fixture, cookie `qa_serving_review_owner` và store dưới
`tmp/serving_review/<UUID>` riêng, API legacy/thị trường/đổi key-model bị chặn.
Banner **HTTP FIXTURE** giữ rõ nguồn mô phỏng; không dùng kết quả để ra quyết
định giao dịch. Dừng bằng Ctrl+C hoặc tự thoát sau 900 giây; không reloader.

Phần còn thiếu bắt buộc: browser desktop/mobile kiểm sáu lựa chọn, nâng cao,
offline/new run, empty/error/partial/completed, stop/resume, exports, VI/EN,
layout và keyboard/focus. Host không khả dụng và duyệt tự động từ chối mở Edge;
HTTP200/DOM test không thay nghiệm thu trực quan. Khi có browser khả dụng, ghi
bằng chứng quan sát thật và kiểm phần ảnh hưởng trước khi chốt F11/merge hoặc
mở F12. Live smoke chỉ thực hiện nếu phạm vi triển khai cần; chưa gọi API thật
trong lượt nghiệm thu offline này. Giữ U09, causal FAIL/NOT_CERTIFIED nguyên vẹn.

## Lựa chọn và miền sử dụng

Nguồn tên/nhóm/dependency/fallback duy nhất cho ứng dụng là
[`core/serving_registry.py`](../../../core/serving_registry.py).
Thứ tự phương pháp vẫn lấy từ registry nghiên cứu, không cài lại thuật toán.

| Nhóm | ID canonical | Nhãn VI | Dependency | Fallback phương pháp |
| --- | --- | --- | --- | --- |
| Chính, mặc định | `original_fix` | Hệ gốc | — | — |
| Chính | `bayesian_v1` | Bayesian v1 | common | common |
| Chính | `C2` | Bayesian v2 — C2 | common | common |
| Chính | `A_tp_pool` | Bayesian A — TP Pool | common | common |
| Chính | `B_semantic` | Bayesian B — Semantic | common | common |
| Chính | `MT_BICL` | MT-BICL | common, Fact_Anchor | Fact_Anchor |
| Nâng cao | `original_common` | Baseline chung | — | — |
| Nâng cao | `Fact_Anchor` | Fact Anchor | common | common |

`common` trong bảng là `original_common`. Không nhận alias `Original_common`,
không đổi `no_alpha` thành common. CASH/ALWAYS_LONG chỉ là control đánh giá.
Phần nâng cao thu gọn; vẫn hiển thị hai vai trò này trong bảng nghiên cứu đầy đủ.
Label VI/EN không thay ID. Form phân tích mặc định native; so sánh chọn từ hai
bản, dùng cùng một mã/ngày/snapshot. Backtest cho chọn nhiều mã/ngày và bản.
Chi tiết bốn màn hình, accessibility, bảng metrics và navigation giữ theo
[thiết kế §4](final_paper_ui_plan.md#4-thiết-kế-cập-nhật-ứng-dụng-hiện-tại).

Ba khả năng đọc kết quả, phân tích mới và backtest được công bố riêng; có
thêm `compare` cho phân tích cùng snapshot. Tại F06 mọi khả năng trong API
mới đều chưa mở: adapter U09 thuộc F07, provider/runner thuộc F08. Khả năng
native tại endpoint cũ vẫn giữ hành vi hiện hữu, không được suy thành grant
cho namespace mới.

**Từ F07**, `read_results` có adapter `VERIFIED_U09_ARTIFACT_READER` và
`available:true`; ba khả năng chạy mới vẫn chưa mở. `/experiments` dùng
`/api/research-results/runs` và `/<run_id>`/`/export`/`/artifacts/<name>` dưới
namespace `/api/research-results`. Reader kiểm package/member/receipt đã khóa,
không gọi evaluator historical trên source serving mới. Filter method/baseline
chỉ ẩn hàng của full cohort; symbol/fold chỉ lọc chi tiết, repeat còn chọn hàng
metrics từng repeat đã seal. Xem [kết quả/giới hạn F07](README.md#f07--viewer-u09-và-so-sánh-offline).

Miền ứng viên ban đầu của runner mới là **1d/VI**. Chưa có mã/ngày nào được
cấp cho inference mới ở F06. EN được nhận về cấu trúc để snapshot ngôn ngữ,
nhưng preflight báo `LANGUAGE_NOT_RELEASED`. Khung intraday bị từ chối.
U09 chỉ có các point trong manifest lịch sử đã verify; không suy thành mọi
ngày của chín mã. Bank CORE4/OOD fallback, HMM/student và selector phải có
support/availability version hóa do server kiểm ở F08; không refit ngầm.
Thiếu resource/provider không phải OOD hợp lệ và không được giả làm bypass.

## HTTP và request

| Endpoint | Kết quả | Tác dụng |
| --- | --- | --- |
| `GET /api/serving/v1/registry` | 200, danh mục/version/domain/capabilities | Chỉ metadata, không đọc archive/model |
| `POST /api/serving/v1/preflight` | 200 `blocked`, `run_enabled:false` nếu cấu trúc đúng | Hash request, topo plan và blocker, không tạo job |
| Như trên, request sai | 400 `invalid`, error có code/field/message/retryable | Không echo dữ liệu lỗi/secret |

F06 chưa có endpoint start/resume/stop/export mới. Không gửi request mới sang
`/api/analyze` để giả lập dispatch. Các endpoint native và experiments cũ
không đổi schema. `hosted_release:false` cũ cũng không là công tắc cấp quyền
cho ứng dụng mới. Preflight F06 luôn fail closed; chuỗi hash hợp lệ không
phải bằng chứng tài nguyên sẵn sàng.

Body đóng, mọi field bắt buộc; ví dụ dưới là phân tích native. `models` có đủ
`indicator`, `pattern`, `trend`, `alpha`, `sentiment`, `decision`, mỗi role
chứa `provider`, `model`, `options`. Giá trị model bên dưới chỉ minh họa cấu trúc.

```json
{
  "version": "variant_serving_v1",
  "mode": "analyze",
  "variant_ids": ["original_fix"],
  "symbols": ["FPT"],
  "start_date": "2026-11-12",
  "end_date": "2026-11-12",
  "timeframe": "1d",
  "language": "vi",
  "repeats": 1,
  "models": {
    "indicator": {"provider":"fixture","model":"fixture-v1","options":{"temperature":0,"max_tokens":1024}},
    "pattern": {"provider":"fixture","model":"fixture-v1","options":{"temperature":0,"max_tokens":1024}},
    "trend": {"provider":"fixture","model":"fixture-v1","options":{"temperature":0,"max_tokens":1024}},
    "alpha": {"provider":"fixture","model":"fixture-v1","options":{"temperature":0,"max_tokens":1024}},
    "sentiment": {"provider":"fixture","model":"fixture-v1","options":{"temperature":0,"max_tokens":1024}},
    "decision": {"provider":"fixture","model":"fixture-v1","options":{"temperature":0,"max_tokens":1024}}
  }
}
```

`mode` là `analyze`/`compare`/`backtest`. Analyze chọn đúng một variant;
compare chọn ít nhất hai. Hai mode này dùng một mã, start=end là ngày as-of.
Backtest dùng cửa sổ start≤end, 1–32 mã canonical không trùng. Repeat là int
1–3, không nhận bool. Options đóng: temperature hữu hạn [0,2], max_tokens int
[1,8192], seed tùy chọn int [0,2³²−1]. Đây là trần cấu trúc, không thay quota,
prompt <6.500 ký tự/BRPP ≤600 và token guard thực tế ở runner. Server F08
phải kiểm allowlist/provider/model/quota trước grant; không tin model từ client
là đã có quyền chạy. Field dư, secret, NumPy, NaN/Infinity bị từ chối.

`INVALID_JSON` áp dụng JSON hỏng/thiếu content type; `INVALID_REQUEST` áp dụng
schema/version/miền cấu trúc sai. Request đúng nhưng không đủ khả năng dùng
trả blocker `RUNNER_NOT_RELEASED`, `SUPPORT_NOT_PUBLISHED`,
`RESOURCES_NOT_READY` (kèm tên resource), có thể `LANGUAGE_NOT_RELEASED`.
Request hash và execution plan không phải run ID hay phiếu chấp thuận.

## Config, identity và job

[`ServingRequest`, `ServingJob`, `result_document`](../../../core/serving_contracts.py)
là validator thực thi của schema; nhận JSON nguyên bản và trả bản sao từ bytes
bất biến. F08 dựng config phía server, không nhận config/owner/resource path
hoặc credential từ body người dùng.

Config đóng gồm `version`, `registry_version`, `runner_version`,
`provider_version`, `source_sha256`, `calendar_sha256`, `support_sha256`,
`credential_scope_sha256`, `resources`, `prompt_versions`. Mỗi resource gồm
`version` và SHA256 đầy đủ. Bắt buộc prices/news/calendar cộng mọi resource
của dependency closure: chọn MT cần facts/context/student; chọn Bayesian cần
bank/regime. Prompt versions bao phủ cả năm upstream role và từng variant
trong topo plan. Source hash nhận diện manifest code/runtime của release,
support hash nhận diện manifest mã/ngày/availability đã kiểm. Hash resource
không thay cho kiểm PIT/fit dates. Không dùng nguồn U09 frozen để tạo live
forecast chỉ bằng lookup response.

Server bind hash snapshot hoặc manifest snapshot của cả cohort **trước Decision**.
Snapshot chỉ chứa forecast inputs/PIT; outcome lấy sau forecast barrier.
Job có run UUID riêng, owner scope hash, config hash, identity hash, cache hash,
requested IDs và execution plan. Identity gồm toàn request/model/options,
config/prompt/resource/provider/source/calendar/support versions, snapshot hash,
method profiles và hợp đồng kinh tế cố định. Cache hash thêm owner scope;
không dùng hash native để trả kết quả common hay khác ngôn ngữ/model/repeat.
Credential scope là digest của tham chiếu opaque do server cấp, không hash trực
tiếp API key và không chứa key. F08 giữ secret trong kho server riêng, snapshot
theo job; browser/export/checkpoint public không nhận raw credential.

Hai job cùng nội dung có thể cùng identity nhưng UUID khác nhau. Resume phải
nạp đúng run/owner/identity/checkpoint cũ, không gọi create để đổi UUID rồi
chạy lại slot. Owner/hash không thay authentication; mọi endpoint job sau này
phải kiểm quyền owner. Idempotency/retry/checkpoint/storage thuộc F08.

## Result và trạng thái lỗi

Envelope giữ identity/run/config/snapshot/support, requested IDs, execution plan,
`executed_ids`, `state`, `progress`, `rows`, `error`, `metric_units`.
Progress tách `points_total`, `points_complete`, `decision_slots_total`,
`decision_slots_complete`, `api_attempts`. Tổng slot tính cả dependency × repeat;
rows chỉ chứa slot đã có kết quả hợp lệ, không tạo CASH cho slot lỗi/chưa xong.
Một dependency chỉ có một slot mỗi point/repeat. Point complete khi đủ mọi
slot trong topo plan. Completed chỉ khi coverage đầy đủ và không có lỗi.

Mỗi row đóng gồm point_id/symbol/as_of_date/repeat, requested_id/executed_id,
raw_prediction/final_prediction/final_action, fallback_reason/bypass_reason,
support, net_return_pct và metric_reason. Prediction LONG/SHORT; action LONG/CASH.
Executed ID phải là chính phương pháp hoặc thuộc chuỗi fallback registry;
fallback/bypass cần lý do. Raw có thể null khi không gọi LLM theo policy.
Support gồm `manifest_sha256` khớp config và status
`supported`/`declared_fallback`; không nhận free-form context có thể chứa secret.
Các lý do do adapter chuẩn hóa, không đưa raw exception vào row.

Net return của hành động có đơn vị `PERCENT_PER_CYCLE`, không phải daily NAV,
label lợi nhuận thị trường hay tổng portfolio; CASH có lợi nhuận giao dịch bằng 0.
Metric chưa xác định giữ null và lý do `PENDING_EXIT`/`NOT_EVALUATED`/
`MISSING_OUTCOME`; analyze/compare luôn chưa có outcome. Backtest chỉ nhận kết
quả kinh tế từ oracle hiện hành sau barrier, không tính công thức mới trong UI.
Hợp đồng vẫn Open(t+1)→Close(t+3), fee .25%+slippage .10% mỗi chiều, SHORT giữ cash.
Result validator kiểm envelope; không chứng nhận tính đúng của số oracle,
availability hay causal gate bằng cấu trúc JSON.

| State | Ý nghĩa và bước sau do runner F08 thực hiện |
| --- | --- |
| `queued` | Chưa thực thi; sau preflight có thể running, stopped hoặc failed |
| `running` | Đang chạy; có thể stop_requested, partial, completed, failed hoặc unknown |
| `stop_requested` | Chờ ranh giới an toàn; giữ checkpoint rồi stopped/partial |
| `stopped` | Dừng chủ động, giữ slot đã xong; resume đúng identity khi được yêu cầu |
| `partial` | Coverage chưa đủ; hiển thị phần có kết quả, không rank final |
| `completed` | Đủ point và slot, không lỗi; outcome coverage vẫn phải trình bày riêng |
| `failed` | Lỗi có code, giữ mọi slot đã hoàn tất |
| `unknown` | Attempt chưa rõ kết quả; đối soát journal trước khi resume, không retry mù |

Error job đóng gồm `code`, thông báo an toàn `message`, `retryable`. Codes:
`RESOURCE_UNAVAILABLE`, `SUPPORT_MISMATCH`, `PROVIDER_FAILURE`, `QUOTA_EXCEEDED`,
`UNKNOWN_ATTEMPT`, `INVALID_MODEL_OUTPUT`, `INTEGRITY_FAILURE`, `INTERNAL_ERROR`.
Failed/unknown phải có error; unknown bắt buộc UNKNOWN_ATTEMPT, retryable=false.
Backoff/retry qua wrapper, UNKNOWN reconciliation và state transitions thực
thi do F08 quản lý; F06 chỉ validate envelope, không giả lập state machine.

Model text luôn là dữ liệu không tin cậy: F09 render text/escape, không chèn HTML.
F07/F10 chống path traversal/CSV formula tại reader/export mới. Không quảng bá
đã hoàn tất các bề mặt chưa triển khai đó bằng test schema của F06.

## Historical replay

`web_interface.py` thêm đăng ký blueprint nên source pin historical của file này
sẽ không còn khớp HEAD mới. Registry/contract/method/evaluator nghiên cứu và
template cũ không đổi. Dùng [checkout/overlay theo F01](final_evidence_map.md)
khi verifier yêu cầu nguồn U09; không bỏ guard hay cập nhật expected pin.
Snapshot/release U09 và hai PDF F05 vẫn nguyên byte. Native causal vẫn FAIL,
whole-system NOT_CERTIFIED; contract serving không nâng kết luận khoa học.
