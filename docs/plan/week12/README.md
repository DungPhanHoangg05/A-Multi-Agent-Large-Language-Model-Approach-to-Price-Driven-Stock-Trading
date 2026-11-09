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
Chưa merge mã nguồn hoặc mở đợt inference mới.

- [x] Phân tích hai nhánh, mô phỏng merge, đối soát 25 tham chiếu file/hash H08/H09 và lập kế hoạch.
- [x] U01 — Khóa inventory nguồn, evidence và callers trước triển khai.
- [ ] U02 — Hợp nhất nguồn và bảo toàn contracts fix.
- [ ] U03 — Kiểm chứng tương đương original_fix.
- [ ] U04 — Registry, runner, evaluator và CLI/UI thống nhất.
- [ ] U05 — Profile nhân quả chung và bridge với native nếu nghiên cứu causal.
- [ ] U06 — Khóa giao thức so sánh, cohort, thống kê và ngân sách.
- [ ] U07 — Kiểm paired/PIT/recovery theo phạm vi.
- [ ] U08 — Smoke và thu thực nghiệm theo release mới.
- [ ] U09 — Phân tích paired và cold replay.
- [ ] U10 — Cập nhật bài báo từ bằng chứng và bàn giao.

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
Code/test/config/runtime không đổi. Develop hiện đi trước remote **37 commit**,
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
