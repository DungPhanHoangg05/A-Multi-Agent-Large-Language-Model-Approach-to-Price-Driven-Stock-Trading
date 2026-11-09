# W12 — Xác nhận độc lập và bàn giao

[Kế hoạch tổng](../plan.md) · [Tiến độ W11](../week11/README.md) ·
[Kế hoạch đánh giá](../week11/historical_reevaluation_plan.md)

Hệ thống giữ Original, Bayesian Prior v1, Bayesian Prior v2/C2,
Bayesian Prior A/B và MT-BICL. Giai đoạn hiện hành đánh giá lại trên
dữ liệu historical đã exposed; chưa có release xác nhận forward.

## Hợp nhất hệ gốc fix và các mở rộng develop

Ngày 09/11/2026: đã lập [kế hoạch hợp nhất](fix_develop_integration_plan.md)
từ hai tip `fix:9efd23f4` và `develop:21f7ee67`. Lấy hành vi fix làm nền,
develop tiếp tục là nhánh tích hợp; phân biệt native baseline, common baseline
và các mở rộng để không gán thay đổi prompt/dữ liệu thành hiệu quả phương pháp.
U02 đã ghép nguồn và U03 đạt parity offline trong worktree riêng; develop vẫn
giữ mốc trước tích hợp. Native chạy mới dùng `original_fix_serving_v1`, có guard
budget được version riêng; parity chỉ trên miền input hợp lệ đã kiểm.
Chưa mở đợt inference mới.

- [x] Phân tích hai nhánh, mô phỏng merge, đối soát 25 tham chiếu file/hash H08/H09 và lập kế hoạch.
- [x] U01 — Khóa inventory nguồn, evidence và callers trước triển khai.
- [x] U02 — Hợp nhất nguồn và bảo toàn contracts fix trên nhánh tích hợp.
- [x] U03 — Kiểm chứng tương đương original_fix trên miền hợp lệ và version delta serving.
- [ ] U04 — Registry, runner, evaluator và CLI/UI thống nhất.
- [ ] U05 — Profile nhân quả chung và bridge với native nếu nghiên cứu causal.
- [ ] U06 — Khóa giao thức so sánh, cohort, thống kê và ngân sách.
- [ ] U07 — Kiểm paired/PIT/recovery theo phạm vi.
- [ ] U08 — Smoke và thu thực nghiệm theo release mới.
- [ ] U09 — Phân tích paired và cold replay.
- [ ] U10 — Cập nhật bài báo từ bằng chứng và bàn giao.

### Checklist chi tiết U03

U03 tiếp tục trên `feat/fix-develop-unification` theo §4.1 của kế hoạch vì nền
U02 chưa đủ gate để vào develop. Mốc đầu vào:
`9eeb201e9133d08ee857eff3abbcffe49291e2af`; oracle fix vẫn là
`9efd23f4157e0d3ab8069fccab7dccf03439a714`.

- [x] U03.1 — Đối soát nhánh sạch/mốc nguồn và giữ ref archive U02 trước khi sửa.
- [x] U03.2 — Phương pháp `original_fix` có profile chạy mới `original_fix_serving_v1`, giữ native distill/cap và chặn quá budget; đường nghiên cứu hiện hành có tên riêng, native không nhận prior/MT.
- [x] U03.3 — Golden request cuối VI/EN, bốn ablation, schema/options, parse/repair và chặn prompt quá budget trước model.
- [x] U03.4 — Hai tiến trình sạch đối chiếu graph/reports/ảnh/factors/sentiment, PIT 600 bars, call counts và ledger kinh tế.
- [x] U03.5 — Replay archive có đủ nguồn: xác minh parent/request/response/hash và báo đúng support, không gán provenance mới.
- [x] U03.6 — Entrypoints CLI/UI cũ giữ hợp đồng dữ liệu/options/default native và lỗi rõ ràng.
- [x] U03.7 — Compile/test caller/PIT/paired/recovery đúng vùng đổi, đối soát gate U02 còn áp dụng và delta mới.
- [x] U03.8 — Cold replay không mạng, khóa source/runtime/golden/log, kiểm diff/links rồi commit trên nhánh tích hợp.
- [ ] Bàn giao nền vào develop — còn cần các kiểm tra U07 liên quan; chưa mở inference hoặc nhận causal gate.

### Kết quả và giới hạn U03

Hoàn tất ngày **09/11/2026** trên `feat/fix-develop-unification`; ref
`refs/archive/fix-develop-u03/integration` giữ mốc U02 trước thay đổi.

Phương pháp native có ID `original_fix`; profile chạy mới là
`original_fix_serving_v1`. CLI/live/backtest mặc định dùng profile này, giữ
native distill/cap, schema và options. Tổng prompt từ **6.500 ký tự** bị chặn
trước Decision inference, không tự cắt lại. Trong **34 golden cases** (VI/EN,
live/backtest, B/A/S/AS, report ngắn/dài và parse/repair), **26 case hợp lệ khớp
đúng request cuối/schema/options/parse**; **8 case live report dài** chỉ thuộc
legacy replay vì donor gửi quá budget. Đây là delta serving có version, không
nhận parity vô điều kiện trên mọi input. `integrated_default_v1` giữ cap nghiên
cứu develop; đường `compile_report_decision` chọn nó tường minh. Tên profile
không biết, prior bật/prefix chèn ngoài hoặc prior hook đi vào native bị từ chối;
native không chạy MT hoặc mở memory bank/student.

Hai tiến trình Python `-I` nạp hai cây nguồn riêng: donor lấy blob thô qua
`git cat-file` (tránh chuyển LF/CRLF), cây tích hợp dùng nguồn hiện hành. Kiểm
hash mọi module dự án đã nạp và từ chối import lẫn cây. Fixture graph chạy engine,
LangGraph, renderer, selector 85 alpha và sentiment thật; chỉ thay transport/
response bằng double xác định, dùng SDK Groq thật để serialize request/schema.
Đối chiếu VI/EN khớp toàn bộ reports, ảnh PNG/pixel, inputs, request, parse,
targets và ledger; chỉ bỏ clock/latency vận hành. Mỗi điểm có prefix **600 bars**,
**8 tin hợp lệ** (future/undated bị loại), một lượt Indicator→Pattern→Trend→Alpha
và hai Decision dùng chung upstream. Poison ba nến outcome không đổi forecast
inputs/ảnh/factors/reports/request nhưng làm đổi target.

Replay phase `main` của `revision_minimal_v1` giữ đủ **204/204 slot B/AS**,
**102 điểm/chín mã**, **204 request IDs**, **204 ảnh dựng lại đúng bytes** và
**102 ledger = 51 tài khoản mã/fold × hai variant**. Mỗi input phải khớp Git
donor trong inventory U01, rồi kiểm parent/shared state, raw request/response,
checkpoint và digest. Hai cây tái tạo cùng prompt, schema, model, effective
temperature/max_tokens, normalized action, target và toàn bộ ledger. Replay này
**conditional trên reports upstream và numeric assets lưu trữ**, không tái sinh
response hosted, không nghiệm thu panel/repeats khác hoặc các trường packet cũ
không được log. Không đổi support/cohort hoặc nhãn `Original_common` của pilot.

CLI consumer bốn ablation/account và Flask test client đã đối chiếu trang
backtest VI/EN, JSON status và 404. Test riêng kiểm default native, refresh và
lỗi profile trước khi tạo client; không khởi động server/live job hoặc gọi nhà
cung cấp market/model. Oracle vô hiệu hóa auto-load `.env`; chính sách credential
tường minh của launcher hiện hành được giữ, không nhận import side effect cũ là
đã khôi phục. Mọi lượt U03 chặn mạng ngoài máy: **0 hosted call, 0 huấn luyện**.

### Kiểm thử U03 và cách kiểm lại

Đã compile đúng **13 file Python mới/đổi**; **183/183 test case duy nhất trong
22 module PASS**, không fail/error/skip:

| Log trong gói QA | PASS | Phạm vi |
| --- | --- | --- |
| `parity.log` | 12 | Golden SDK, native guard/profile, oracle bytes, archive tamper, future poison và caller chart |
| `graphs.log` | 78 | Token budget, paired, Prior graph/prompt, MT Decision và alpha/sentiment cutoff |
| `entrypoints.log` | 35 | Ablation/sweep, JSON UI, target/account risk |
| `recovery.log` | 49 | Prior integration/PIT, checkpoint, locks và durable stage recovery |
| `locks.log` | 9 | Research input lock và leakage |

Hai hàm `compute_round_trip_net_return`, `_validate_account_costs` giữ nguyên
AST so với donor và U02. Đối soát lại **21.383 artifact đóng băng** và đủ
**21.948 đường dẫn U01**: PASS; ngoại lệ workflow đã nghỉ giữ nguyên như U02.
**143/150 source bindings U02** còn nguyên byte; bảy binding đổi được liệt kê
trong `previous_gate_delta.json`. Các file U03 mới/đổi ngoài tập cũ có bindings
mới; đã kiểm lại đúng caller chịu ảnh hưởng và **107 package/Python 3.13.5**.
Không ghi 239 test U02 là đã chạy lại; gate cũ chỉ giữ phạm vi snapshot cũ,
không cấp gate cho hành vi mới. Không chạy full suite/E2E/toàn leakage suite.

Gói [golden, cold output, log và source/runtime bindings](original_fix_parity_checks.zip):
**570.504 byte**, SHA256
`9890f5d6865e83535e63a49611ce3049c4b3aab3cf727338312d17deb3ee7648`.
Tiến trình cold consumer mới đã PASS **22/22 thành viên**, **482 source bindings**,
runtime và toàn bộ archive inputs được khóa. Diff whitespace và **48 liên kết/
anchor local** trong bốn tài liệu hiện hành đã kiểm PASS. Consumer chỉ kiểm bytes/input/
source/runtime và so lại kết quả đã lưu, không tạo client hoặc chạy graph mới:

```powershell
py -3.13 -I -X utf8 scripts/verify_original_fix_parity.py --verify docs/plan/week12/original_fix_parity_checks.zip
```

Khi cần chạy lại parity graph/archive do đổi nguồn tương ứng, dùng output mới
(lệnh chạy vài phút; không ghi đè archive cũ):

```powershell
py -3.13 -I -X utf8 scripts/verify_original_fix_parity.py --output outputs/unified_integration/original_fix_parity_review
```

Harness `run_scoped_checks.py` trong gói chạy lại từng nhóm từ repo root, ví dụ
`py -3.13 -X utf8 <thư_mục_giải_nén>/run_scoped_checks.py graphs <log_mới>`.
Giữ giới hạn **`native_rowwise_causal_gate=FAIL`**: outer cutoff PASS không
chứng nhận row-wise causality/Zero-Leakage toàn hệ. U03 không mở nghiên cứu mới,
không nhận superiority; U04–U10 và bàn giao nền vào develop vẫn theo các gate
riêng trong kế hoạch.

### Checklist chi tiết U02

Trạng thái ở đây là nguồn theo dõi duy nhất; kế hoạch hợp nhất dẫn tới mục này.
Nhánh `feat/fix-develop-unification`, worktree
`C:/Users/Legion/codex-worktrees/stock-unification`, base develop
`2424dbc5fce87083ded678936d715a64f4fa6a82`, donor fix
`9efd23f4157e0d3ab8069fccab7dccf03439a714`.
Delta U01→U02 chỉ có hai commit tài liệu U01, runtime không đổi.

- [x] U02.1 — Fetch/pull fast-forward, worktree sạch, đối soát mốc U01 và tạo nhánh tích hợp riêng.
- [x] U02.2 — Merge đúng donor bằng `--no-commit --no-ff`; xử lý bốn conflict quản trị, giữ chỉ dẫn AGENTS hiện hành.
- [x] U02.3 — Ghép engine theo caller: target/cost/risk fix và hooks Prior/checkpoint develop; không đổi oracle kinh tế.
- [x] U02.4 — Schema Prior v2 và canonical projection cho Prior/MT; schema v1 và record legacy không tự nâng cấp.
- [x] U02.5 — Renderer/legend fix cùng `write_artifacts`; prompt màu VI/EN, strict mode và retry hooks develop được giữ.
- [x] U02.6 — Khóa dependencies/runtime tích hợp, kiểm version/requirements trên môi trường hiện hành.
- [x] U02.7 — Đối soát toàn bộ đường dẫn và byte evidence/paper/revision/data/schema U01; giữ nguồn Git pin và archive.
- [x] U02.8 — Compile đúng Python mới/đổi; test kinh tế, callers, graph/prompt, leakage và recovery trong phạm vi PASS.
- [x] U02.9 — Kiểm diff/links, ghi số test/log/hash và giới hạn; tạo merge commit trên nhánh tích hợp.
- [ ] Bàn giao nền vào develop — chỉ sau U03 và các kiểm tra U07 liên quan, không suy từ việc U02 đã PASS.

### Kết quả và giới hạn U02

Hoàn tất ngày **09/11/2026** trong worktree tích hợp riêng. Đã tạo local refs
`refs/archive/fix-develop-u02/{develop,fix}` giữ đúng hai parent nguồn nêu trên.

Nguồn runtime hiện có một engine root, giữ contracts target/cost/risk của fix
cùng hooks Prior/checkpoint của develop. AST của `compute_round_trip_net_return`
và `_validate_account_costs` giống cả hai nguồn khóa. `target_fields` và validator
đã gọi lại oracle kinh tế thay vì giữ công thức net riêng. Risk giữ convention
fix: SD population, downside SD trên tập âm; thiếu tần suất hoặc mẫu số suy biến
cho `null`, không nhân mặc định `sqrt(252)` cho cycle returns.

Prior/MT tạo canonical target từ frame sau phase forecast và chiếu metadata đã
kiểm vào `TestPoint`; dữ liệu legacy không có provenance vẫn giữ trạng thái
legacy. Prior summary lấy tần suất từ bar indices đã xác thực, không đoán từ
ngày lịch. [Schema checkpoint v2](prior_research_checkpoint_v2.schema.json) có
ID/version riêng, nhận canonical metadata và risk/null; schema v1 ở W4 nguyên
byte và loader vẫn đọc được v1. Identity mới pin thêm schema/helpers/runtime
lock, nên không resume run cũ bằng code mới hoặc sửa receipt cũ để vượt guard.

Renderer giữ handles/màu fix và tùy chọn `write_artifacts` develop. Test ảnh cho
thấy bật/tắt file phụ trả cùng bytes; messages Trend VI/EN khớp donor trên fixture.
Auditor chart lịch sử vẫn từ chối AST tích hợp có retry hooks khác nguồn cũ;
test lịch sử chạy trên đúng source donor, không nới guard để gọi mã mới là bản
cũ. Golden payload Decision và parity graph/archive được nghiệm thu riêng ở
kết quả U03 phía trên.

Đã hợp nhất attributes/ignore của hai nhánh, giữ AGENTS hiện hành và viết root
README tiếng Anh về kiến trúc/cài đặt/vận hành, gồm attribution QuantAgent.
Python **3.13.5** và **107 package** có version/specifier/Requires-Python hợp lệ
trên môi trường Windows hiện hành; [lock runtime](../../../requirements-unified.lock.txt)
ghi đúng versions đã kiểm, bao gồm CUDA build của Torch. Thêm dependencies trực
tiếp `pydantic`, `jsonschema`, `referencing`; Gunicorn chỉ áp dụng Unix. Chưa cài
thử một môi trường mới hoặc nghiệm thu lock Unix/CPU; Docker/deploy cần lock
theo nền tảng riêng trước khi phát hành.

`scripts/verify_unified_evidence.py` đã đối soát **21.383 artifact đóng băng**
bằng index mode/OID và byte length/SHA256 checkout. Đủ **21.948 đường dẫn U01**
được đối chiếu: **21.947 giữ trong cây**, một đường dẫn đã ngừng dùng có lý do:
`.github/workflows/deploy.yml` được develop thay bằng Oracle VM ở
`9d30f85227111bf5ec43b7dd580c0fecb1221754`. Nguồn workflow cũ vẫn truy nguyên
đúng hash từ fix; không bật lại GitHub Pages deployment. Ngoại lệ này chỉ áp dụng
đúng đường dẫn cấu hình đó, không cho phép bỏ evidence hoặc runtime source khác.

Checkout Windows ban đầu có **63 file chỉ khác LF/CRLF**; đã chứng minh delta
chỉ là newline, khôi phục đúng blob U01 và thêm `-text` cho data/schema/evidence.
Không đổi giá trị dữ liệu hoặc sửa nội dung receipt. Quy tắc whitespace riêng
cho evidence/paper giữ nguyên byte log/third-party files và EOF nguồn fix; không
dọn whitespace bằng cách sửa artifacts. Inventory U01, paper/revision, schemas
cũ và mọi evidence được kiểm đều nguyên byte Git; local ignored assets vẫn ở
workspace gốc và chưa được coi là đã khôi phục trong worktree tích hợp.

### Kiểm thử U02 và cách kiểm lại

Đã compile đúng **142 file Python mới/đổi**, không compileall toàn codebase.
Kiểm **239 test case duy nhất**, **245 lượt thực thi** trong **26 module**:
mọi lượt PASS, không fail/error/skip. Sáu ca `test_unified_contract_integration`
được dùng ở cả nhóm economics và locks để đối soát lần thay đổi cuối.

| Nhóm/log | Số lượt PASS | Phạm vi được chọn |
| --- | --- | --- |
| `economics.log` | 81 | Account P&L/risk, target, canonical Prior/MT, evidence tamper, ablation/sweep, JSON UI, chart VI/EN và attribution |
| `callers.log` | 82 | Prior integration/leakage, checkpoint/leakage, durable stage recovery, MT analysis/leakage và pilot statistics |
| `graphs.log` | 67 | Paired upstream, token budget, Prior graph/prompt, MT Decision và alpha/sentiment cutoff leakage |
| `locks.log` | 15 | Research input lock/leakage, schema/helpers/runtime pins và sáu ca nối contracts mới |

Các nhóm bao phủ đúng engine/schema/renderer/helpers và caller thay đổi; không
chạy full unit suite/E2E hoặc toàn bộ leakage suite. Harness chặn socket ra ngoài
máy; cho loopback phục vụ `asyncio.socketpair` trên Windows. Không API/huấn luyện,
không nhận gate toàn hệ thống hoặc chứng nhận native alpha causal từ các test này.

[Gói log và source/runtime bindings](fix_develop_unification_checks.zip):
**31.333 byte**, SHA256
`d3b7753d4db4c8f9e52daef788e3317f524587ab94d1d6cd5f36d9faf91ac952`.
Gói có log bốn nhóm, IDs test/module, danh sách compile, kết quả đối soát
evidence, source hashes, versions package, manifest hash từng thành viên và
harness tái lập. Đây là bằng chứng U02 mới; không thay gate/receipt lịch sử.
Đã kiểm hash **12/12 thành viên gói**, **150 source bindings** và **44 liên kết/
anchor local** trong tài liệu hiện hành: PASS; diff whitespace không lỗi.

Tại worktree tích hợp, có thể kiểm evidence bằng:

```powershell
py -3.13 -X utf8 scripts/verify_unified_evidence.py
```

Để chạy lại một nhóm khi có thay đổi tương ứng, giải nén log ra thư mục tạm mới
rồi dùng harness từ repo root (thay `economics` bằng `callers`, `graphs` hoặc `locks`):

```powershell
Expand-Archive -LiteralPath docs/plan/week12/fix_develop_unification_checks.zip -DestinationPath "$env:TEMP/u02-checks"
py -3.13 -X utf8 "$env:TEMP/u02-checks/run_scoped_checks.py" economics "$env:TEMP/u02-economics.log"
```

U02 chỉ được commit trên `feat/fix-develop-unification`; chưa merge nền vào
develop. U03 được nghiệm thu riêng phía trên; phần U07 bị ảnh hưởng tiếp tục
trên nhánh tích hợp cho đến khi đủ điều kiện §4.1 của kế hoạch. Chưa cấp release
inference mới và không khôi phục H07 full1020 đã hủy.

Task lập kế hoạch chỉ đổi Markdown: kiểm diff, links và bằng chứng nguồn;
không chạy compileall/unit/E2E/leakage theo AGENTS §1.2. Các kết quả pilot
được viện dẫn đúng phạm vi, không coi là nghiệm thu runtime hợp nhất.

## U01 — Inventory nguồn và bằng chứng đã khóa

Hoàn tất ngày **09/11/2026** trên nhánh `docs/fix-develop-source-audit`.
Đầu ra máy đọc là [inventory đầy đủ](fix_develop_source_inventory.zip),
**2.877.720 byte**, SHA256
`9f05fd92493ca74bbafe9ffb2a7412f99f84aa391d3e3ecaa7aaab8404fb3775`.
Gói chỉ chứa chỉ mục/hash và bộ sinh audit; không sao chép dữ liệu thị trường,
responses, model weights hay credential. Quyết định ownership dưới đây là
hướng dẫn tích hợp cho U02, chưa phải thay đổi runtime.

### Mốc nguồn và delta so với kế hoạch

| Nguồn | Commit khóa | Tree |
| --- | --- | --- |
| `fix_frozen`, cũng là `fix`/`origin/fix` sau fetch | `9efd23f4157e0d3ab8069fccab7dccf03439a714` | `f7c8e48de6c110e73ea84b218cf6011323ac71bd` |
| `develop` trước U01 | `3eb3c765946e7fd393abf54d91b3f204d86ee981` | `90207267bf47cdccecfe5c99c7d29e1e8453322a` |
| `origin/develop` sau fetch | `aaf855d3cf908e5735ddf097b150e9767a3e4cb1` | Tra theo commit trong Git |
| Tổ tiên chung | `69800f27a6f84887db624e08acf7d4553f44d5c4` | Tra theo commit trong Git |

Worktree sạch trước task; `git pull --ff-only origin develop` không có thay đổi.
So với mốc `21f7ee67` trong kế hoạch, develop thêm đúng commit tài liệu
`3eb3c765`: sửa `docs/plan/plan.md`, README này và thêm kế hoạch hợp nhất.
Code/test/config/runtime không đổi. Develop tại mốc U01 đi trước remote **37 commit**,
remote không có commit riêng; `fix...develop` có **63/287 commit riêng**.
Live/backtest hiện hành vẫn dùng package root trên develop; `fix_frozen` là
nguồn tham chiếu, chưa có port `original_fix` được nghiệm thu.

Đã tạo local refs `refs/archive/fix-develop-u01/{fix,develop,origin-develop}`
trỏ lần lượt đến ba nguồn ở bảng. Các refs này chỉ ở máy local; clone khác
cần giữ các commit đã ghi và có thể dựng lại refs, không coi ZIP inventory là
bản sao Git hay gói khôi phục dữ liệu. Không reset/force-push hoặc merge fix.

### Phạm vi và cách đọc inventory

| Thành viên ZIP | Nội dung |
| --- | --- |
| `inventory.json` | Toàn bộ **21.948 đường dẫn hợp**: role/category, ownership đề xuất, quan hệ hai nhánh; từng phiên bản có Git mode/type/blob OID, byte length và SHA256 |
| `imports.json`, `definitions.json`, `calls.json` | Imports, định nghĩa và call sites có snapshot/file/dòng/scope; giữ tên gọi và tên qua import alias để tra caller |
| `hardcodes.json` | **4.806 dòng ứng viên** đường dẫn/commit/environment/dynamic loading trong Python và các file text cấu hình, UI, tài liệu, bài báo; không lưu giá trị credential |
| `receipt_bindings.json`, `donor_sources.json` | Đối soát binding local trong JSON kế hoạch và 21 source archive donor với Git fix |
| `handoff_members.json` | Hash/kích thước toàn bộ 2.457 thành viên mà manifest H09 khóa |
| `summary.json` | Mốc nguồn, thống kê, provenance của mismatch, Python/package versions quan sát được và giới hạn audit |
| `manifest.json`, `build_source_audit.py` | Hash/byte length các thành viên còn lại và bộ sinh chỉ đọc, dùng thư viện chuẩn |

Fix có **21.367 file**, develop có **687 file**. Có **81 đường dẫn cùng byte/mode**,
**25 khác nhau**, **21.261 chỉ ở fix** và **581 chỉ ở develop**.
Đã đọc/băm **20.838 blob duy nhất** bằng `git cat-file`, đồng thời đối soát Git
blob SHA1 từ đúng byte; SHA256 trong inventory là byte Git, không mặc định là
byte checkout sau chuyển LF/CRLF. Không có gitlink trong hai cây này.

AST đọc đủ **184 file Python ở fix + 343 ở develop**, không lỗi parse;
thu **8.916 import entries**, **5.830 definitions**, **65.857 call sites**.
Các con số bao gồm test và Python lưu trong evidence; `category` cùng `path`
phân biệt chúng với runtime root. Static import/call chỉ là ứng viên, không
chứng minh đã chạy, call count thực tế hoặc type của `self`/factory. Imports
không resolve local được ghi `external_or_unresolved`; không tự coi tất cả là
dependency bên thứ ba. Dynamic dispatch, `exec`, import whitelist và đường dẫn
ghép ở runtime cần kiểm lại ở U02/U03. Binding JSON chỉ thu bộ ba tường minh
`path`/`bytes`/`sha256`; không tuyên bố đã resolve mọi chuỗi hoặc mọi schema receipt.

### Ownership và callers cần giữ khi port

| Vùng | Chủ sở hữu hành vi và caller/hợp đồng cần kiểm |
| --- | --- |
| `core/backtest_engine.py`, `utils/target_contract.py`, `utils/account_risk.py` | Giữ contracts fix về target, costs, frequency/null và account ledger; chèn hooks Prior/checkpoint từ develop theo caller. `TestPoint` được tạo bởi engine, `core/run_robustness.py`, `scripts/run_ablation_matrix.py`, thêm `core/prior_backtest.py:summarize_points` và `core/mt_bicl_accounting.py:account` ở develop. Hai caller mới chưa cấp canonical indices/metadata, không nâng record legacy thành canonical bằng giá trị giả. |
| Label và metrics của mở rộng | Giữ `compute_round_trip_net_return` làm oracle. Callers trực tiếp gồm Bayesian memory, historical outcomes/data, prior evaluation, MT accounting/analysis, free-pilot statistics và research metrics; tra toàn bộ trong `calls.json`. `target_fields`/validator của fix hiện tính lại công thức: U02 phải đối soát với oracle, không coi đây là hàm độc lập được phép đổi kinh tế. Prior summary dùng metrics engine trực tiếp; MT bỏ ratios mặc định rồi dùng `cycle_risk`; pilot có `cycle_ratios` riêng. Không quy lỗi annualisation của engine cho mọi báo cáo MT/pilot. |
| `utils/static_util.py`, `utils/color_style.py`, `agents/trend_agent.py` | Giữ legend/handles/màu của fix, nối `write_artifacts` của develop. Consumers gồm graph toolkit/live, engine qua graph, historical `GraphProvider`, chart audits và tests fix; phải kiểm cả ảnh/prompt và hai ngôn ngữ. |
| `agents/decision_agent.py`, `agents/agent_state.py`, `utils/graph_setup.py` | Giữ profile gốc fix cho parity; giữ validators/prior hooks, schema prior, distill/cap, budget guard và retry scope develop. Callers gồm `SetGraph`, `utils/trading_graph.py`, `core/decision_prior.py`, `core/mt_bicl_prompt.py`, Prior runners và historical clients/audit. Common instruction được thêm ngay cả prefix rỗng; prior OFF chưa chứng minh native parity. |
| `agents/alpha_agent.py`, `sentiment_agent.py`, `indicator_agent.py`, `pattern_agent.py` | Giữ reports native để replay và strict research mode/retry develop theo profile. Graph lịch sử dựng lại năm dòng alpha nên cần projection có version. Sentiment develop bỏ import-time dotenv; live lấy key qua UI/config/environment (`web_interface.py`, `utils/trading_graph.py`), không tự nạp lại bí mật lúc import. |
| `core/realtime_loader.py`, `core/run_robustness.py`, `utils/statistical_tests.py` | Khác hai tip dù không phải mọi file đều conflict văn bản. Giữ target/frequency plumbing fix trong sweep/load checkpoint và ablation; kiểm caller engine, CLI, UI/export và undefined metrics. |
| Bayesian/Prior/MT và `historical_evaluation_*`, `free_pilot_*` | Develop sở hữu mở rộng, gates, journal/transport/recovery. Chỉ có một engine chung; module import từ `core/backtest_engine.py` có **33 caller files ngoài tests** ở develop. Không thay bằng toàn bộ engine một phía hoặc xóa code pin để làm verifier mới chạy qua. |
| `core/revision_*.py`, `core/revision72_*.py`, scripts/tests fix | Port **28 + 5 module**, **49 script chỉ có ở fix**, **43 test chỉ có ở fix**; phân biệt offline audit/consumer với runner có thể gọi API. Giữ source pins và negative evidence. Không chạy runner trong task audit. |
| `paper/`, `revision/`, outputs và lineage source | Giữ **50 file paper**, **28 file revision** cùng tác giả và nguồn sinh bảng. Fix có **21.100 file outputs**, trong đó **21.052 không có ở develop**; develop có 166 file outputs, 48 file cùng byte với fix. Python trong `outputs/revision/.../historical_sources/` là archive, không đưa vào import path runtime. |
| `.gitattributes`, `.gitignore`, `AGENTS.md`, root `README.md`, dependencies/deploy/UI | Hợp nhất quy tắc giữ byte evidence và bảo mật của hai nhánh; AGENTS theo chỉ đạo hiện hành, root README tiếng Anh. `requirements.txt` khác: develop pin HMM/sklearn/vnstock/vnai và thêm httpx/tiktoken; fix có `revision/requirements-r1.txt` cho nguồn cũ. Runtime hợp nhất cần lock riêng U02; package versions quan sát không phải chứng nhận tái lập môi trường fix. Docker/compose/deploy/templates giữ trong inventory để kiểm entrypoints, không nhận parity chỉ vì cùng byte. |

Danh sách đầy đủ **25 đường dẫn khác nhau** nằm trong `inventory.json` với
`relation=different`, gồm 4 file quản trị, 7 file agents, 3 core, requirements,
1 script, 5 tests và 4 utils. Mô phỏng lại
`git -c merge.renames=false merge-tree --write-tree --name-only develop fix`
trả exit **1 do bốn conflict dự kiến**: `.gitattributes`, `.gitignore`, `AGENTS.md`,
`README.md`; tree mô phỏng `2257334d1549b9380da5b1e682d90b3874009f9d`.
Trend/engine/static renderer tự ghép văn bản vẫn cần các checks U02/U03.
Lệnh không sửa index/worktree và không phải nghiệm thu hành vi.

### Đường dẫn cố định và ranh giới archive/runtime

| Resolver/consumer | Ràng buộc cần giữ |
| --- | --- |
| `historical_evaluation_protocol.py`, `historical_asset_readiness.py`, `historical_evaluation_graph.py` | Donor `9efd23f4`; archive ở `outputs/historical_reevaluation/inputs/fix/`; graph lấy `utils/static_util.py` bằng `git show` rồi compile nhưng import agents từ develop. Đây là adapter lai; giữ donor commit/object và 21 blob archive, không nhận là `original_fix`. |
| `historical_evaluation_scope.py:AlgorithmScope` | Whitelist `PORTS`, pin H03 trong `docs/plan/week11/historical_evaluation_protocol.json`, fallback Git `ae5dbc6d`. Nạp byte local vào namespace riêng rồi điều chỉnh bindings; thay module sau U02 có thể làm verifier cũ từ chối. Replay cũ cần source/environment đã khóa, adapter mới có namespace/version riêng. |
| `core/free_pilot_assets.py`, runtime/analysis, `scripts/package_free_pilot.py` | Giữ `docs/plan/week11/free_pilot_*.json`, namespace `outputs/historical_reevaluation/free_pilot_r1`, H04 regimes, H06 smoke, quota history và replica `full_r1` inputs/model. Nhiều asset là ignored local; Git inventory không đủ khôi phục. H09 ZIP là gói pilot riêng và chứa sparse Git objects cho consumer, không phải full history. |
| `core/prior_backtest.py`, Prior/MT schemas/loaders | Paths schema/QA/protocol/model trong docs và data được nhận diện trong `hardcodes.json`; không dời chúng cùng lúc với port contracts. Giữ JSON fixtures và entrypoints cũ cho consumer; code đã đổi dùng output namespace mới. |
| Fix revision/paper consumers | Giữ `outputs/revision/**`, `revision/*.json`, `paper/generated/`, các `original_sources.zip` và lineage blobs. `fix:scripts/build_revision_manuscript.py` fallback paper source theo member/hash; `core/revision_reproducibility.py` còn đọc manifest/archive và weights. Không chỉ giữ PDF hoặc di chuyển archive mà chưa có resolver/test consumer. |
| Grant/lượt đã hủy | H07 full1020 vẫn CANCELLED; run_r1/managed_r1 không được phục hồi hoặc suy quyền từ protocol/grids còn trên đĩa. Không tái dùng output namespace cũ cho code mới, không sửa receipt frozen để đổi provenance. |

### Đối soát bằng chứng và sáu binding lịch sử

Đã kiểm **896 binding tường minh** trong JSON `docs/plan/` ở snapshot develop:
**890 khớp local**, **6 khác byte/hash**, không có binding thiếu file trong phạm vi
này. Sáu khác biệt là ba đường dẫn lặp qua receipts cũ, không phải sáu file hỏng:

| File được receipt cũ dẫn tới | Receipt có binding cũ | Snapshot khớp hash cũ |
| --- | --- | --- |
| `core/historical_evaluation_audit.py` | `historical_evaluation_freeze.json`, `historical_evaluation_runtime_pre_schema_title.json` | `295c89a0f150ce968439a303e120408000ba29f4` |
| `core/historical_evaluation_clients.py` | Hai receipt như trên | `cb9cf9c004e159ffa682ecfc2ff40573ec0db307` |
| `docs/plan/week11/historical_evaluation_runtime.json` | `historical_evaluation_freeze.json`, `historical_evaluation_validation.json` | `295c89a0f150ce968439a303e120408000ba29f4` |

Ba file đổi tại `698f18ccb03d3d5ff748179ee0b3cc898827080d`.
Đã đọc diff và [amendment transport W11](../week11/historical_evaluation_transport_amendment.json):
SDK thêm title `UtilityICLReply`, clients/audit áp schema adapter, runtime v2→v3.
Byte runtime v2 được giữ ở
[bản trước schema title](../week11/historical_evaluation_runtime_pre_schema_title.json).
Các binding của amendment và nguồn hiện hành nằm trong 890 binding khớp.
Inventory giữ cả expected/actual hashes và Git provenance; không sửa receipts
cũ, không ghi 896/896 PASS, không dùng H05/freeze cũ chứng nhận runtime mới.

H08 **18/18**, H09 **7/7** binding khớp; donor archive **21/21** khớp
SHA256 với blob fix. H09 ZIP giữ **45.782.060 byte**, SHA256
`656be564c58cc78e141b1a8879196bec33ed08776f9196dc4efc6810ae210771`;
manifest SHA256
`275c62808cbed0a0663b510d244de065018cb48069042157c6dc7012e4b85c22`;
đã đọc/kiểm byte length và SHA256 **2.457/2.457 thành viên** được manifest khóa.
Đây là đối soát bytes, không chạy lại restore/cold consumer hoặc nhận gate mới.
Native alpha vẫn có `native_rowwise_causal_gate=FAIL`; PASS detection/outer
cutoff không được chuyển thành chứng nhận Zero-Leakage toàn hệ.

### Kiểm tra bàn giao và cách tái lập

U01 chỉ thêm inventory tài liệu và cập nhật Markdown; không đổi code/test/
schema/config/data đầu vào hay runtime. Đã kiểm **11/11 thành viên ZIP** (10
thành viên theo manifest và chính manifest), path/mode/OID/size của **21.948
đường dẫn** với hai cây Git, delta nguồn, refs, diff whitespace và **35 liên kết/
anchor local**: PASS. Không chạy compileall/unit/E2E/leakage theo AGENTS §1.2;
AST parse phục vụ inventory không thay các gate runtime. Không inference,
huấn luyện, gọi API thị trường/LLM hoặc sửa bằng chứng cũ.

Có thể mở JSON trực tiếp trong ZIP để lọc theo `snapshot`, `path`, `callee`,
`category`, `relation`. Để sinh lại trên đúng repo có Git history và các asset
local đã nêu, giải nén ra thư mục tạm mới rồi chạy:

```powershell
Expand-Archive -LiteralPath docs/plan/week12/fix_develop_source_inventory.zip -DestinationPath "$env:TEMP/u01-source-audit"
py -3.13 -X utf8 "$env:TEMP/u01-source-audit/build_source_audit.py" "$PWD" "$env:TEMP/u01-inventory-rebuilt.zip"
```

Bộ sinh neo hai commit bằng hash, không dùng HEAD mới để thay mốc U01.
Package versions và binding local là quan sát của máy chạy; nếu môi trường/
asset đổi, so từng thành viên và báo delta, không ghi đè inventory đã khóa.
U01 đủ điều kiện chuyển sang U02; U02/U03 và checks U07 liên quan vẫn phải
PASS trên nhánh tích hợp nền trước khi merge phần mã nguồn đó vào develop.

## Điều kiện mở xác nhận

- Hoàn tất registry/common support và cold analysis trong W11.
- Khóa candidate bằng rule được đăng ký trước, giữ toàn bộ kết quả âm.
- Audit exposure, source/model/options, point-in-time và execution data.
- Khóa cohort tương lai sau freeze, đơn vị cluster, power/precision,
  protocol và N trước response đầu.
- Báo risk/exposure, chi phí, missing support và khả năng khớp lệnh.

Repeats không tăng N thị trường và kết quả historical không cấp
bằng chứng prospective. Bàn giao giữ source/runtime/data/model hashes,
raw requests/responses, checkpoints, labels và report tái lập.
