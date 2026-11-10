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
U02 đã ghép nguồn và U03 đạt parity offline trong worktree riêng; U07 nghiệm thu
paired/recovery để đưa nền vào develop. Native chạy mới dùng `original_fix_serving_v1`, có guard
budget được version riêng; parity chỉ trên miền input hợp lệ đã kiểm.
U04 đã thêm registry/runner/evaluator và CLI/UI offline chung. U05 có profile
alpha causal và bridge riêng, không nâng gate native hoặc toàn hệ. U06 có
amendment v2 giữ 102 anchor, đủ assets/PIT và quota offline; nghiệm thu và cold
replay đã PASS trong phạm vi U06. Smoke U08 đã cold verify PASS. Research đã
dừng có checkpoint để người dùng tự chạy tiếp bằng lệnh, giữ 102 điểm/ba repeat.
U08 còn chờ đủ cohort và cold seal.

- [x] Phân tích hai nhánh, mô phỏng merge, đối soát 25 tham chiếu file/hash H08/H09 và lập kế hoạch.
- [x] U01 — Khóa inventory nguồn, evidence và callers trước triển khai.
- [x] U02 — Hợp nhất nguồn và bảo toàn contracts fix trên nhánh tích hợp.
- [x] U03 — Kiểm chứng tương đương original_fix trên miền hợp lệ và version delta serving.
- [x] U04 — Registry, runner, evaluator và CLI/UI offline thống nhất.
- [x] U05 — Profile alpha nhân quả chung và bridge với native; gate toàn hệ còn chờ U06/U07.
- [x] U06 — Amendment v2 đủ nguồn offline, quota có bằng chứng, scoped tests và cold replay102/102 PASS; inference/release vẫn OFF.
- [x] U07 — Paired/PIT/recovery offline PASS116 test, cold replay102 điểm/2.448 forecast slot; không mở inference.
- [ ] U08 — Smoke và thu thực nghiệm theo release mới.
- [ ] U09 — Phân tích paired và cold replay.
- [ ] U10 — Cập nhật bài báo từ bằng chứng và bàn giao.

### Checklist chi tiết U08

Triển khai trên `feat/unified-comparison-run`, từ develop `ea90605b`.
Grant kỹ thuật cho lượt mới đã neo Git theo protocol khóa, chỉ Free/0 USD.
Theo đính chính của người dùng ngày 10/11/2026, người dùng tự khởi chạy research
bằng lệnh được bàn giao. Collector đã tự khởi chạy trước khi bàn giao lệnh và đã
dừng có checkpoint lúc 14:02. U08 còn chờ đủ cohort và nghiệm thu.

- [x] U08.1 — Đối soát develop/plan, tạo branch; năm GET catalog mới đều thấy hai model active,0 inference.
- [x] U08.2 — Thêm transport live/release riêng, giữ DAG, UUID, quota/carry và cap3/retry+repair.
- [x] U08.3 — PASS69 test/8 module, compile11 file; QA14 source mới và672 nguồn U07 giữ nguyên; neo runtime/preflight/grant smoke riêng vào Git.
- [x] U08.4 — Smoke BHN-2025-10-01, một repeat/đúng org4:8 slot,6 HTTP200,12.793 token;0 query payoff, cold verify PASS.
- [x] U08.5 — Grant research mới sau smoke đã neo Git. Collector có lock/checkpoint/heartbeat đã chạy và dừng an toàn, sẵn sàng để người dùng resume thủ công.
- [x] U08.5a — Amendment quota theo `(org, model)` đã PASS 61 test, compile 5 file và cold verify 32 điểm hoàn chỉnh. Prefix 487 HTTP và 2.390 file checkpoint giữ nguyên byte, bàn giao entrypoint resume mới.
- [ ] U08.6 — Đủ102 shared,2.448 forecast,102 canonical labels; seal raw/usage/order/coverage và cold replay.
- [ ] U08.7 — Đối soát receipt/evidence, cập nhật checklist, commit/merge theo phạm vi; U09 phân tích sau seal.

Trạng thái live được đọc qua `scripts/unified_live/run.py status --phase SMOKE`
hoặc `--phase RESEARCH`. `verify` không khởi tạo client/key/provider. Outcome
research chỉ đọc sau đủ24 slot durable; smoke không tính payoff. Mọi UNKNOWN
giữ reserve và dừng để đối soát, không tự gửi lại hoặc đổi lỗi thành CASH.

[Runtime U08](unified_live_runtime.json), [preflight](unified_live_preflight.json),
[QA](unified_live_checks.json)/[log gói](unified_live_checks.zip) và
[grant smoke](unified_live_smoke_release.json) là các artifact mới, không sửa
receipt cũ. Năm GET catalog mới thành công, hai model active; org IDs không được
provider trả về nên vẫn ghi nguồn xác nhận độc lập/Free từ người dùng. Carry
giữ497 request/1.140.404 token, không reset hoặc tự giả định đã hết cửa sổ.
Header thực sẽ được kiểm ngay trên response đầu của từng org và trước admission
tiếp theo. Token/attempt/planned cohort không bị giảm theo kết quả smoke.
Transport HTTPX cũng đã được GET catalog kiểm TLS trên đúng org của điểm smoke
(một GET bổ sung,0 inference); không sửa receipt năm GET đã khóa trong preflight.
Smoke live đã nhận raw vision200 và quota header RPD1.000/TPM8.000 như attestation;
collector giữ reserve và nhường đúng cửa sổ quota, không chọn key/model khác.

Các69 test gồm23 test U08,23 recovery/firewall U07,15 runner/caller và8 provider
leakage. Chỉ compile11 file mới; không chạy full suite/E2E vì kernel cũ giữ byte
và các thay đổi nằm ở release, transport, runner và oracle gate mới.

Smoke đã **PASS_U08_SMOKE**, hai vision và bốn Decision thực, không repair hoặc
transport retry; bốn bypass theo registry vẫn có record đầy đủ. `outcome` của
smoke chỉ là marker barrier; counter `labels_complete` ở phase này không phải
nhãn thị trường. Cold verify trong tiến trình/cây nguồn tạm có686 source pin và
U07 ZIP phụ thuộc, không key/client/SDK/provider constructors hoặc mạng, đã PASS.
[Gói smoke](unified_live_smoke.zip) giữ raw, images, slot, runtime/grant/receipt
và proof replay nguyên byte; [grant research](unified_live_research_release.json)
neo đúng digest receipt smoke, không mang response smoke vào study.
Gói smoke có46 thành viên/543.113 byte, SHA256
`f3f09d19937cc6ff975bd84820506d3af3f636d2accbd6b9c29a408eb12a2676`.
Source smoke/runtime không đổi sau các response; research chỉ bổ sung grant
và mang thêm chi phí6 smoke request/12.793 token vào carry, không reuse forecasts.

Research khởi chạy lúc 13:14 ngày 10/11/2026, giờ Việt Nam, PID25328 tại
`outputs/unified_integration/u08_research_r1`. Vòng đầu đã nhận HTTP200 từ đủ
năm org, mỗi response có header RPD1.000/TPM8.000. Provider chưa trả org ID.
Ledger research giữ đúng 503 carry request/1.153.197 token, gồm lịch sử và smoke.
Mã nguồn, QA, runtime và hai grant đã vào develop tại merge `e898e2ad`.
Collector đã dừng lúc 14:02 ngày 10/11/2026 theo yêu cầu người dùng tự khởi chạy
research. Trạng thái `STOPPED_BY_OPERATOR`, tiến trình PID25328 đã thoát.
Journal giữ 9 shared, 152 forecast, 5 canonical labels và 98 HTTP attempt
(97 HTTP200, 1 HTTP503), mọi attempt có trạng thái xác định. `stop.request` giữ
trạng thái dừng đến khi người dùng chạy lệnh resume bên dưới.
Lượt bàn giao thủ công tại commit `6c50b0ff` chỉ sửa ba tài liệu kế hoạch, kiểm
diff/liên kết và hash nguồn/bằng chứng, viện dẫn69 test/11 file compile đã PASS.
Tiến độ trong `status.json` là checkpoint gần nhất. Raw HTTP có thể đi trước
checkpoint khi một tick đang chạy. Chỉ receipt research PASS mới xác nhận thu đủ.

#### Amendment quota theo model

Người dùng yêu cầu tách quota theo model ngày 10/11/2026. Bản gộp bảo thủ cũ
cộng Qwen và GPT-OSS vào chung 200.000 token/24 giờ mỗi org, dẫn đến chờ ở
32 điểm dù từng model còn ngân sách. Policy mới `per_org_model_v1` tính riêng
RPM30/RPD1.000/TPM8.000/TPD200.000 cho từng cặp org/model, kể cả header reset,
retry-after và reserve UNKNOWN. Tổng trần HTTP của phase là 7.956 attempt.

Amendment nối từ sequence487, tức HTTP attempt thứ488, trong cùng journal.
Prefix trước sửa gồm 487 HTTP (486 HTTP200, 1 HTTP503), 36 shared, 802 forecast và
32 canonical labels. Runtime/grant riêng neo prefix raw, carry, run identity và
mọi slot complete để kiểm khi resume. Nghiệm thu cuối có `receipt.json` cho
execution và `quota_receipt.json` cho amendment. Telemetry mới có trạng thái
`WAITING_QUOTA` và `waiting_models` ghi model, reserve, thời điểm mở lại.

[Runtime amendment](unified_model_quota_runtime.json),
[grant thủ công](unified_model_quota_release.json),
[scoped checks](unified_model_quota_checks.json) và
[gói QA](unified_model_quota_checks.zip) quản lý policy mới. Lệnh dưới dùng
entrypoint amendment để tiếp tục cùng checkpoint.

Nghiệm thu amendment tại source commit `1770b743` có 61 test, gồm 34 ca mới hoặc
chạy bằng transport mới và 27 ca caller/recovery/leakage liên quan, 0 failure/error/skip.
Compile riêng 5 file Python mới. Các ca phủ bốn loại hạn mức, header/reset,
retry/repair/UNKNOWN, trần attempt chung, mixed-policy resume, paired/barrier
và manager lock giữ đến hết cold seal. Tám pin source mới nối tiếp 686 pin nguồn
U07/U08 đã đối soát. Phạm vi kiểm tra tập trung vào các đường bị ảnh hưởng.

Cold audit trong tiến trình mới đã chặn mạng ngoài và sáu constructor key/client/
SDK/provider, kết quả `PASS_MODEL_QUOTA_COLD_HANDOFF`, 0 HTTP mới. Đã tái lập
32 điểm hoàn chỉnh/768 forecast thuộc những điểm này và 32 nhãn canonical,
đối soát cả 2.390 file identity/wire/raw/slot nguyên byte. Journal có thêm 34
forecast ở các điểm đang dở, tổng 802. Probe offline 8.000 token nhận READY ở đủ
10 bucket org/model tại thời điểm kiểm tra. Study còn `PARTIAL_U08`.
Gói QA có 7 thành viên/189.185 byte, SHA256
`0c1851ba45665808f03b04760c91e155f3e60e9bb3a5b69e1220805f347242ab`.

Người dùng khởi chạy hoặc resume từ thư mục gốc repo bằng PowerShell.

```powershell
py -3.13 -I -X utf8 scripts/unified_model_quota/run.py status
Remove-Item -LiteralPath 'outputs/unified_integration/u08_research_r1/stop.request' -ErrorAction SilentlyContinue
py -3.13 -I -X utf8 scripts/unified_model_quota/run.py collect
```

Sau khi thu đủ, collector tự cold verify và seal. Có thể đối soát lại bằng lệnh sau.

```powershell
py -3.13 -I -X utf8 scripts/unified_model_quota/run.py verify --seal
```

Collector có OS lock và heartbeat ở `outputs/unified_integration/u08_research_r1/status.json`.
Lệnh collect thứ hai không được mở worker trùng. Chờ quota giữ timestamp/usage,
không reset UUID hoặc mở lại full1020. UNKNOWN/cap3 hoặc source thay đổi làm
dừng có checkpoint để đối soát. Chỉ khi đủ102 điểm và cold seal PASS mới đánh dấu
U08.6 hoàn tất; trạng thái khởi chạy chưa phải nghiệm thu thu đủ hoặc superiority.

### Checklist chi tiết U07

Tiếp tục trên `feat/fix-develop-unification` theo §4.1, từ commit U06
`ec1ca7ec8a7789a2d18f1cccce328aeccb92ac73`; ref
`refs/archive/fix-develop-u07/integration` giữ nguyên mốc. Chỉ mock HTTP,
không kế thừa release cũ hoặc mở inference. Checklist đang triển khai:

- [x] U07.1 — Đối soát phạm vi paired/PIT/recovery và khóa mốc nguồn U06.
- [x] U07.2 — Dispatcher năm org cố định, counterbalance đúng DAG, quota gộp hai model và carry.
- [x] U07.3 — Durable intent/raw, UNKNOWN fail-closed, replay cùng UUID, retry/repair chung trần3.
- [x] U07.4 — Graph/renderer thật, một upstream cho24 forecast/điểm; test scope chín mã và firewall nhãn.
- [x] U07.5 — Fault injection, thoát tiến trình sau raw fsync, resume cùng UUID và verify không tạo client; kiểm parents/raw policy.
- [x] U07.6 — Kiểm thử/compile đúng vùng, cold replay102 điểm, gói QA/hash và cập nhật checklist.
- [x] U07.7 — Commit và đưa nền đã nghiệm thu vào develop theo §4.1; inference/release vẫn OFF.
- [x] U07.8 — Hậu kiểm checkout Windows, khôi phục LF/CRLF đúng hash và test helper độc lập; không sửa gói QA đã khóa.

### Kết quả và giới hạn U07

`core/unified_execution.py` điều phối năm hàng đợi cooperative, gán org bằng
`1 + global_point_index % 5`, giữ toàn bộ repeat của một điểm trên cùng org.
Thứ tự nhánh dùng `ordered_branches(3 * point_index + repeat)` đã khóa ở U06;
Original_common → Fact_Anchor → MT và các parent fallback được giữ nguyên.
`StudyProviders` chạy Indicator/Pattern/Trend/Alpha và renderer donor, tạo một
shared snapshot rồi deepcopy sang tám vai trò. Context, selector, bank, HMM và
student vẫn dùng hợp đồng frozen U06; không nhập nhãn102 query vào memory.

`DurableCalls` chỉ nhận `MockHTTP`, không có constructor live, key hoặc quyền
kế thừa grant cũ. Intent/reserve được fsync trước sender, raw response được fsync
trước parse; forecast chỉ complete sau khi kiểm lại raw/policy/parent. UNKNOWN
giữ reserve, không tự gửi lại; đối soát NOT_SENT cần đúng UUID và bằng chứng,
vẫn trừ attempt cũ. Raw200 được replay cùng UUID khi mất checkpoint, kể cả qua
tiến trình mới. Lỗi429/5xx dùng backoff và retry-after; schema repair chỉ thêm
chỉ dẫn định dạng cố định, giữ nguyên reply cũ và cùng trần ba HTTP/slot qua
mọi lần resume. Lỗi không được đổi thành CASH. Một org chờ quota nhường lượt
cho org khác; CLI control dừng nếu có UNKNOWN cần đối soát, giữ mọi shard durable.

Quota gộp cả hai model theo org, giữ carry đã dedup497 request/1.140.404 token,
không reset bằng namespace/model/key. Header giảm limit, remaining/reset và
usage vượt reserve đều được kiểm. Đồng hồ ảo chỉ phục vụ kiểm lịch offline;
không đo latency hoặc cam kết thời gian hoàn thành hosted. Barrier outcome chỉ
mở sau đủ24 forecast durable/điểm; U07 lưu marker
`WITHHELD_CONTROL_NO_QUERY_PAYOFF`, không tính nhãn hay P&L cohort.

Đã PASS **116 test / 13 module**, không lỗi hoặc skip:23 test paired/recovery
và firewall mới,77 hồi quy caller/journal/prompt/paired,16 leakage alpha/provider
liên quan. Đã biên dịch riêng sáu file Python mới. Không chạy full unit suite,
full compileall hoặc E2E vì không đổi các kernel cũ; đối soát hash U06 và
21.383 frozen artifacts là kiểm bảo toàn bằng chứng, không gọi là chạy lại
các gate lịch sử.

Nghiệm thu toàn cohort giữ nguyên **102 điểm, chín mã, 51 symbol/fold, ba repeat,
một realization**:102 shared snapshot,408 node graph complete,204 raw vision,
**2.448 forecast slot complete**, **1.302 raw Decision** và1.146 bypass theo
registry. Toàn bộ1.506 HTTP attempts là `MockHTTP`,0 request đến provider,
0 query payoff,0 huấn luyện student/HMM. Repeats có UUID request mới; không lấy
response của repeat khác làm mẫu mới. Hai vision body của điểm đầu khớp nguyên
ABI probe SDK U06 trên cùng ảnh thật. Cold restore/replay ở tiến trình và cây
nguồn tạm độc lập đã PASS với client/SDK/provider constructors và socket bị chặn.
Verifier kiểm lại request/schema/model/options, ảnh, raw-policy, shared/parent,
shard/epoch, thứ tự thực và thời điểm barrier; không mở lại numeric providers.
Proof số/context/student/retrieval U06 chỉ được viện dẫn sau khi băm660/660
source bindings nguyên byte. Đây không phải lần chạy lại numeric replay U06.

[Gói QA U07](unified_execution_checks.zip) chứa journal/raw nguyên byte, logs,
116 test IDs, compile sáu file,672 source bindings, runtime107 package/Python3.13.5,
consumer và log cold replay. Ba file attributes chỉ khóa LF cho sáu file Python
mới và chính các attributes; giữ nguyên quy tắc audit cũ. Không sửa manifest,
ZIP, grants hoặc receipt U06/W11. Source U07 mới có identity riêng; verifier
nguyên cây U06 chạy trên snapshot `ec1ca7ec`, không nhận source mới là receipt cũ.

Gói có **7.241 thành viên / 71.926.900 byte**, SHA256
`c77da519973da453bd0581951421528d9567704a6b8ec17f39a9653cbf3a8d21`.

Khôi phục từ checkout có đủ các nguồn/artifact gốc đã pin:

```powershell
py -3.13 -I -X utf8 scripts/restore_unified_checkout.py --write
py -3.13 -I -X utf8 scripts/prepare_unified_comparison_v2.py restore
py -3.13 -I -m zipfile -e docs/plan/week12/unified_execution_checks.zip "$env:TEMP/u07-checks"
py -3.13 -I -X utf8 "$env:TEMP/u07-checks/verify_package.py" "$PWD" docs/plan/week12/unified_execution_checks.zip --restore
py -3.13 -I -X utf8 scripts/check_unified_execution.py verify --namespace outputs/unified_integration/u07_acceptance_r1
```

Consumer chỉ restore file thiếu trong đúng namespace, không overwrite byte khác.
Helper checkout mặc định chỉ kiểm, `--write` chỉ chọn LF hoặc CRLF nếu đúng
byte/hash đã khóa trong gói QA; từ chối mọi khác biệt nội dung thực sự và không
stage Git. Hậu kiểm merge Windows đã gặp57 file đổi newline; đã khôi phục và
đối soát đủ672/672 hash tại worktree gốc. Helper có **3 test bổ sung PASS** và
compile riêng hai file; không chạy lại116 test hoặc numeric replay vì các nguồn
nghiên cứu đã khóa giữ nguyên byte. Gói QA116 test ở trên giữ nguyên SHA; helper
và tests mới được neo trong commit Git riêng, không gán vào receipt U07 cũ.
Lệnh `control --namespace outputs/unified_integration/u07_<tên_mới>` chạy lại QA
mock102 điểm trên graph/renderer thật; `--fixture-images` hoặc `--limit` chỉ dành
probe có khai báo, không thay nghiệm thu toàn cohort. Verify không ghi journal.

U07 hoàn tất **phần mềm và kiểm soát offline**, không cấp collection release.
Native row-wise vẫn **FAIL**, whole-system causal **NOT_CERTIFIED**; metadata
ngày tin không chứng nhận nội dung PIT, dữ liệu historical vẫn exposed và
bank/query vẫn có giới hạn nguồn đã công bố ở U06. U08 còn phải tích hợp transport
live sau grant mới, đối soát quota/carry/header/thay đổi serving và smoke riêng;
không lấy control forecasts làm kết quả nghiên cứu hoặc trộn smoke vào repeats.

### Checklist chi tiết U06

Tiếp tục trên nhánh tích hợp từ U05
`c0a4993fbd3214d32f0580109ad4ecfefd246fcb`; ref
`refs/archive/fix-develop-u06/integration` giữ mốc trước task. U06 không kế thừa
grant full1020 đã REVOKED hoặc grant pilot48 đã hoàn tất.

- [x] U06.1 — Khóa hai family, năm mở rộng, hai baseline, Fact_Anchor và bridge; không chọn lại phương pháp theo pilot.
- [x] U06.2 — Đối soát 102 anchor/51 scope bằng đúng 21 blob donor, calendar/index/suffix BHN; khóa CORE4 và ledger exposure.
- [x] U06.3 — Khóa estimand/account reset, ba repeats/một realization, outcome barrier, strict frozen memory và thứ tự có dependency.
- [x] U06.4 — Khóa controls, panel deferred tường minh, 20 endpoint/contrast đồng thời, block/bootstrap/undefined và sensitivity trước inference mới.
- [x] U06.5 — Tính slot/attempt cap; khôi phục nguyên byte quota/handoff có sẵn, dedup carry, không suy quota/giá/thời gian hiện tại từ lịch sử.
- [x] U06.6 — CLI/manifest offline, source/runtime/model hashes, test chống đổi thiết kế/cohort/quyền/manifest và cold verify.
- [x] U06.7 — Amendment v2 giữ 102 test anchor, min60/min30 và horizon; train từ index319, validation180 phiên trước anchor đầu từng mã; 51 binding tới chín selector frozen xuyên fold.
- [x] U06.8 — Đủ 102 projection và provider controls tám vai trò; context MT frozen theo fold, chặn tất cả102 ID trước oracle; bank/source/schema compatibility có provenance riêng.
- [x] U06.9 — Năm catalog GET và xác nhận hiện tại của người dùng về năm org Free; khóa payload SDK, carry-over và hai scenario quota, không giảm N/repeats hoặc mở inference.
- [x] U06.10 — Compile/test đúng vùng, cold restore/replay nguồn số và request/policy, hash/evidence/links; commit trên nhánh tích hợp, không merge develop trước U07.

### Kết quả nghiệm thu U06 v2

Theo yêu cầu hoàn thiện U06, [protocol v2](unified_comparison_protocol_v2.json)
thay thế điều kiện nguồn của v1 trước bất kỳ response hosted mới nào. Cohort,
hai family, năm extension, ba repeats, một realization, economics, controls
deferred và thống kê của v1 giữ nguyên. [Manifest v2](unified_comparison_manifest_v2.json)
phân biệt **input-eligible 102** và **collection-eligible 0**: đủ nguồn offline
không cấp grant inference, không thay các kiểm tra U07 hoặc release mới U08.

**Split cuối:** với mỗi mã, dùng anchor đầu tiên làm ranh test cho tất cả fold;
train từ bar319 tới `first_anchor_index−187`, validation từ `−183` tới `−4`
với cadence3. Embargo bảo đảm mọi nhãn train/validation đóng trước ranh kế tiếp.
Min60 train, min30 validation, min5 LONG, năm factor và ba threshold U05 giữ
nguyên. Chín fit riêng theo mã được replay/khóa cho **51 scope**, đủ **102 query**;
train có **85–123 cycle**, validation common **54–60 cycle**. Các fold sau dùng
nguyên selector đầu mã; không dùng nhãn anchor cũ để refit.

Prototype ban đầu mở rộng train theo từng fold đã tính nhãn của anchor thuộc
fold trước trong history. Prototype này **không được dùng trong assets cuối**;
amendment ghi rõ exposure, không gọi nghiên cứu là fresh holdout hoặc khẳng định
chưa từng tính payoff trong cả phiên làm việc. Các file prototype local giữ riêng;
gói nghiệm thu chỉ chứa selector frozen trước anchor đầu từng mã. Không chọn
cohort/ngưỡng/thiết kế dựa vào payoff test hoặc lợi nhuận phương pháp.

**Provider:** namespace riêng mở đúng ID/schema chín mã, tái dùng byte thuật toán
đã pin và không sửa `sys.modules`/globals của hệ gốc. HMM/scaler/student/teacher
frozen; chỉ forward CPU, không optimizer/refit HMM hoặc huấn luyện student.
Context numeric đóng băng trước query đầu mỗi fold và giữ cùng view cho anchor
cuối fold. Cả102 ID cohort bị reserve **trước** khi oracle có thể tính nhãn,
kể cả ID thuộc fold cũ; query chỉ cung cấp feature/facts tại cutoff.

Bank852 vẫn CORE4/raw execution; OOD5 fallback `original_common` có reason,
không tạo episode giả hoặc đổi nhãn. Kiểm tương thích phát hiện schema và
CSV/events trong QA cũ khóa checkout **CRLF** trong khi Git lưu **LF**. Byte
CRLF đúng hash được phục hồi vào namespace mới, qua đầy đủ validator/schema/
oracle gốc; file nguồn, manifest và QA cũ giữ nguyên. Nhãn raw/donor vẫn khác
**828/852**, chênh lớn nhất **0,042988489 điểm phần trăm**; không relabel bank
để làm mất khác biệt provenance. Gate H03 cũ từ chối serving tree mới đúng
thiết kế; không dùng nó làm gate cây mới hoặc bỏ pin để ép PASS.

Control không LLM đã dựng đủ tám request/policy role tại **102 điểm**, nguồn
numeric thật, Indicator/Alpha chạy thật; Pattern/Trend và reply có marker control.
Native request trước/sau bridge khớp. Đây là kiểm ABI/prompt, **không** phải
forecast hay kết quả kinh tế mới. MT có support **66/102** điểm; **36** giữ
fallback theo nguyên nhân (20 thiếu magnitude support,16 feature unavailable).
Probe prior fallback lần lượt v1 **54**, C2 **99**, A **94**, B **99**; ngoài OOD
bắt buộc, gate prior còn phụ thuộc reports control nên không nhận là tỷ lệ active
của hosted run tương lai. News kiểm policy next-day/undated và mask từng điểm;
**79/102** unavailable giữ missing, không thay bằng neutral. Metadata ngày vẫn
không chứng nhận content PIT, execution fills hoặc contamination hosted model.

**Quota:** người dùng xác nhận ngày **10/11/2026** năm org độc lập, Free, mỗi
model RPM30/RPD1000/TPM8000/TPD200000, không tách ITPM/OTPM. Năm **GET catalog**
xác nhận cả hai model active; không POST/inference. Endpoint không trả org ID,
nên grade là **user attestation + authenticated catalog**, không nhận provider
đã xác minh org IDs. [Nguồn hạn mức chính thức](https://console.groq.com/docs/rate-limits)
và [catalog model](https://console.groq.com/docs/models) được đối chiếu cùng ngày.
Không ghi key hoặc tạo credential/quyền mới; receipt chỉ giữ tham chiếu/HMAC.

Trong controls, prompt lớn nhất **3.835 ký tự**, reserve body SDK lớn nhất
**3.422 token**; khóa planning
Decision reserve **4.500**, hai vision body trên ảnh thật **5.471 / 5.110**.
Trần admission mỗi request **8.000 token**, prompt<6.500 ký tự, BRPP≤600;
vượt trần phải dừng, không hạ cap ngầm. Budget vẫn **2.448 Decision slots +
204 vision +10 smoke =2.662 nominal**, tối đa **7.986 attempts** gồm repair.
Carry497 request/1.140.404 token giữ nguyên, dedup theo org/UUID; không reset
quota khi đổi namespace.

Lịch planning khóa năm queue org độc lập, point giữ cùng org ở mọi branch/repeat,
DAG nội điểm tuần tự; ưu tiên point theo lịch, thứ tự hoàn tất xuyên org có thể
khác nhau vì memory frozen không nhập nhãn test. Bảo thủ gộp cả hai model vào
cùng RPM/RPD/TPM/TPD mỗi org. Với giả định latency **5 giây/request** (scenario,
không phải phép đo hosted mới), nominal reserve **12.141.843 token**, khoảng
**298,64 giờ**; scenario mọi attempt dùng trọn8.000 reserve là **63.888.000 token**,
khoảng **1.594,28 giờ**. Đây là mô phỏng quota có điều kiện, không bảo đảm thời
gian hoàn thành; không có deadline48h hoặc tự giảm mẫu. Usage bên ngoài, headers
thực và model availability phải đối soát lại trước/tại U08. Chi tiêu khóa **0 USD**.

[Gói assets v2](unified_comparison_assets_v2.zip) giữ **287 thành viên**,
**25.448.065 byte**, SHA256
`d5c4f1bc31c1a95d9e685a9cc13d1f86ce2d3cc0105b9023561fd5f567e2d8c4`.
Gói có nguồn numeric/preparations/control và compatibility, không có model
weights hoặc raw response hosted mới. Model/H09/nguồn gốc dùng bindings hiện hữu;
CLI restore chỉ nhận namespace/hash đã khóa và từ chối overwrite byte khác.

```powershell
py -3.13 -I -X utf8 scripts/prepare_unified_comparison_v2.py restore
py -3.13 -I -X utf8 scripts/prepare_unified_comparison_v2.py verify
py -3.13 -I -X utf8 scripts/prepare_unified_comparison_v2.py replay-numeric
```

`verify` mặc định chỉ hash/tái dựng preflight thuần, không đọc credential,
import model hoặc tạo client. `replay-numeric` tái fit selector trước test,
kiểm102 alpha/native bridge, context/student/utility, retrieval và tám prompt/
policy control từ nguồn đã pin trong tiến trình mới, không tạo HTTP client.

Đã compile **chín Python mới/đổi**, PASS **146 case duy nhất / 14 module**,
không fail/error/skip trong bốn log nghiệm thu cuối:

| Nhóm | PASS | Phạm vi |
| --- | --- | --- |
| protocol | 31 | V1 candidate trên cây hiện hành, protocol/nguồn v2, split/export→CausalSources, quota pooling, metadata GET-only, không key/client trong verify |
| causal | 25 | Đủ85 formula/prefix/poison, selector/bridge U05, source9-symbol/future events, reserve chặn oracle có positive control, H03 refusal và LF/CRLF compatibility |
| providers | 75 | Regime prefix, Bayesian/price-index/similarity PIT, MT tasks/features/student/Decision và fallback/source proofs |
| unified | 15 | Runner/evaluator/UNKNOWN/resume, immutable shared, paired/raw-policy, CLI/UI và lazy OFF |

Module `test_historical_adapter_leakage` vẫn neo H03 và từ chối source serving
mới ở setup, không được tính là suite PASS cho cây này. Probe bị từ chối được
giữ nguyên trong QA; test mới xác nhận verifier cũ vẫn fail-closed, còn provider
mới được kiểm bằng source/PIT và cold consumer riêng. Không sửa verifier/receipt
H03, không che bằng skip hoặc xóa test cũ. Không chạy full unit/E2E/toàn leakage
suite; chỉ các đường split, providers và hợp đồng caller ở bảng trên bị ảnh hưởng.

Cold restore sang thư mục tạm mới đã kiểm **286 asset + manifest ZIP**, nguồn
và runtime. Tiến trình `-I` mới tái tạo **102/102** điểm, chín fit selector và
toàn native numeric/sentiment, alpha bridge, HMM/scaler/context/student/utility,
retrieval, request và policy ABI. Không chỉ tin preparations đã ký; provider
thật dựng lại trace/request và so bytes/numeric với producer. Gate cuối khóa
manifest payload SHA256
`973504c09932bd70d8fb8369ca9b6dfc757eeee79ab8eb57d0cefd31968e4548`,
**660 source bindings**, **107 package/Python3.13.5**. **551/554** binding U06 v1
giữ nguyên; ba thay đổi là `.gitattributes`, root README và test V1 dùng candidate
hiện hành thay vì giả receipt frozen chứng nhận mọi cây mới. Model/runtime/math
cũ không đổi; v1/H03 receipts tiếp tục giữ scope nguồn cũ.

Đối soát **21.383 frozen artifact / 21.948 đường dẫn U01** PASS; không sửa giá,
paper, revision, receipt hoặc archive lịch sử. [QA v2](unified_comparison_checks_v2.zip)
giữ log/IDs, cold receipts, compile/source bindings và prototype bị loại nguyên
byte trong `not_admitted_prototype/`; consumer không nhập chúng vào study.
Gói **480.508 byte / 171 thành viên**, SHA256
`0891a3934ab256a170b42b3681b65fc8b7ce2fbacdc11df2a18bda212005b7ce`.
Consumer mới đã PASS hash/nguồn/runtime, viện dẫn đúng cold numeric đã khóa.
Thêm `--numeric` để chạy lại toàn bộ forward/selector replay, không API:

```powershell
Expand-Archive -LiteralPath docs/plan/week12/unified_comparison_checks_v2.zip -DestinationPath "$env:TEMP/u06-v2-checks"
py -3.13 -I -X utf8 "$env:TEMP/u06-v2-checks/verify_package.py" "$PWD" docs/plan/week12/unified_comparison_checks_v2.zip
```

U06 **COMPLETE_OFFLINE_INPUTS_READY**; native row-wise vẫn **FAIL**, whole-system
causal **NOT_CERTIFIED**, execution release **PENDING_U07_U08**. Không nhận
hosted effect hoặc superiority từ controls. Chưa merge nền vào develop.

### Kết quả và giới hạn U06

Phần dưới giữ kết quả **v1** tại commit `1c19513d`, trước amendment ở trên.
Trạng thái BLOCKED và gói QA v1 chứng nhận snapshot đó, không phải trạng thái v2
hoặc gate của cây nguồn hiện hành; giữ nguyên byte cả ba artifact máy v1.

[Protocol v1](unified_comparison_protocol.json) khóa thiết kế
`unified_anchor102_historical_v1`; [manifest máy](unified_comparison_manifest.json)
ghi **`DESIGN_LOCKED_RELEASE_BLOCKED`**. PASS kiểm manifest nghĩa là tái dựng
được audit, **không** phải đủ support hoặc được phép gọi API. Vì điều kiện
thoát “đủ nguồn” của kế hoạch chưa đạt, checkbox U06 tổng vẫn để mở.

Cohort dự kiến là đúng **102 endpoint anchor**, **51 symbol/fold account**,
**12 cutoff**, chín mã; CORE4 **48 điểm** là subset secondary cố định. BHN
chỉ có sáu anchor ở ba fold cuối, raw index lệch suffix **673**. Tất cả anchor
đã thuộc nghiên cứu fix; **16/102** trùng selected pilot48. Không coi phần còn
lại là holdout chưa xem, không nối response pilot vào lượt mới, không khôi phục
full1020. Selection chỉ dùng lịch/ID; thêm hoặc đảo outcome trong metadata không
thay cohort. Calendar có nguồn đủ **102/102**; **collection eligible 0**, complete
mới 0, failed mới 0, not started 102. Số 0 eligible là chưa được gate chấp nhận,
không phải kết luận không còn dữ liệu thị trường.

Audit split phát hiện **cả 51 fold** có trần validation **18–21 cycle**, thấp hơn
`causal_common_v1.min_validation=30`; phân bố lần lượt 9/16/18/8 fold với
18/19/20/21 cycle. Một fold BHN còn chỉ có **32 train cycle**, dưới mức 60.
Đây là trần từ lịch cycle đã purge, chưa giả định factor có support đủ. Không fit
selector trên thị trường, không giảm ngưỡng U05 hoặc âm thầm mở rộng validation.
Do đó chưa thể gắn 51 selector hợp lệ vào Spec v2 cho cohort này. Amendment
phải có lý do, version, nguồn và quy tắc lịch trước response mới; lịch sử vẫn
exposed/exploratory dù sau này giải quyết được numeric support.

Hai family giữ đủ năm contrast extension-minus-baseline: method dùng
`original_common`, system dùng `original_fix`. Bridge native/common và ladder
Original_common → Fact_Anchor → MT báo riêng, không gán mọi chênh lệch cho
student. Primary là chênh mean net return của **51 account độc lập**, reset
50 triệu VND theo symbol/fold/method/realization/repeat, lấy mean ba repeat
trong account rồi mean đều các account; không gọi là portfolio return. BA tính
mỗi repeat trên 102 điểm rồi mean; repeats không tăng N thị trường. Kinh tế,
oracle, LONG/CASH, horizon, phí/slippage và null metric giữ nguyên.

Khóa **ba Decision repeats**, **một upstream realization**, chung raw parent,
projection causal cho common và native nguyên vẹn. Xoay sáu ưu tiên tail common
theo DAG rồi chèn native lần lượt ở tám vị trí; manifest lưu đủ **306 order**.
Native ở mỗi vị trí 38 hoặc 39 lần; common/anchor vẫn bị dependency ràng buộc,
không nhận cân bằng hoàn toàn. Runner offline U04 hiện chưa áp dụng lịch hosted
này: gate U07/U08 phải kiểm thứ tự thực, org/epoch/time và retry; manifest không
đổi runtime âm thầm.

Controls CASH và always-LONG cùng cycle/cost/support, chỉ mở outcome sau barrier.
Continuous hold bị loại khỏi v1 do chưa có execution acceptance; không đồng nhất
với cycle LONG. Random/recent/similarity/bayesian, prior/MT ablations và B/A/S/AS
được liệt kê rõ nhưng **deferred**, có **0 hosted slot** trong v1; không được
nhận kết luận đóng góp regime/utility từ panel chưa chạy. Mở panel cần version
và ngân sách riêng trước response của panel đó.

Thống kê khóa chung **20 endpoint/contrast**: mười contrast ở hai family ×
return và BA. Bootstrap di chuyển chung tất cả mã/ngày/method/repeat theo sáu
fold có thứ tự, circular block length 2, **10.000 draw PCG64/seed20261110**;
rebuild account của mỗi fold-copy từ 50 triệu, không compound xuyên fold.
Dùng centered max standardized deviation cho band đồng thời 95%; tối thiểu
9.500 draw joint-finite, thiếu hoặc SD=0 thì band null kèm lý do, không redraw.
Block 1/3, leave-one-fold/symbol-out và CORE4 là sensitivity cố định. Chỉ là
historical sensitivity với ít cluster đã exposed; không có confirmatory
p-value, power/superiority hoặc chọn family/subgroup sau outcome. U09 mới
triển khai tính toán từ forecast sealed; U06 không xuất kết quả lợi nhuận mới.

Ngân sách khóa **2.448 Decision forecast slots**, tối đa **204 vision executions**,
**10 smoke executions** ở epoch riêng: **2.662 nominal HTTP upper bound**,
**7.986 attempts** nếu ba attempt/execution (repair và transport chung cap).
Fallback có thể giảm call nhưng không xóa forecast slot. Không thu history mới,
không reuse Decision archive, không tự giảm N/repeats hoặc đổi model/key.
Token reserve, thời gian và USD hiện là null: chưa đo payload mới hoặc xác minh
hạn mức/org/model hiện hành; không dùng giá/quota W11 như dữ liệu hiện tại.

Đã tìm asset ignored ở worktree gốc và sao chép **nguyên byte 15 ledger quota +
H09 ZIP** sang worktree tích hợp; không sửa nguồn. Dedup theo org/request UUID
giữ **497 request**, **1.140.404 token đã tính/reserve**, không giả định hết cửa
sổ quota theo đồng hồ. H06/lượt hủy/pilot trùng carry không bị đếm hai lần;
history này chưa chứng nhận quota còn dùng được. H09 giữ SHA256 cũ
`656be564c58cc78e141b1a8879196bec33ed08776f9196dc4efc6810ae210771`.
Student/teacher full_r1, HMM prefix và bank852 được kiểm byte/hash, không load
weights, không fit lại; bank vẫn khác provenance query và chỉ có CORE4, không
gắn nhãn bank causal hoặc giả hỗ trợ OOD5. Nguồn raw news có ngày không chứng
nhận content PIT; providers/context/scaler/news và availability còn phải gate.

CLI chỉ có `build` và `verify`, chặn mạng ngoài máy và không tạo client. Thiết kế
có hash pin trong code; envelope đã tự băm lại nhưng đổi cohort, repeat, quyền
API hoặc multiplicity vẫn bị từ chối. Verify tái dựng toàn bộ manifest, còn build
chỉ tạo file mới; không overwrite bản sealed. Tái lập từ repo root có đủ local
asset đã hash:

```powershell
py -3.13 -I -X utf8 scripts/prepare_unified_comparison.py verify
```

Đã compile **ba file Python mới**, PASS **16 test / một module**
`test_unified_protocol`, không fail/error/skip trong log nghiệm thu. Nhóm này
kiểm đúng CLI và compiler offline mới: immutable design, ID/calendar/purge,
outcome-poison selection, source/donor mismatch, quota carry, DAG/order,
manifest tự băm lại, overwrite guard và tiến trình cách ly không import
torch/Groq/httpx/retriever/HMM/alpha runtime. Không đổi caller/đường chạy dữ
liệu hiện hữu nên không chạy lại full unit/E2E/toàn leakage suite hoặc 151 test
U05. Đối soát **495/497 bindings U05** nguyên byte; hai thay đổi chỉ là
`.gitattributes` và root README. **107 package/Python 3.13.5** giữ nguyên.
Đã đối soát lại **21.383 frozen artifact / 21.948 đường dẫn U01**: PASS.

Manifest khóa **554 source bindings**, protocol semantic SHA256
`2d12701324e04f40c5513ca9f1541b9008546b38e9c02c44cd9dee8169548283`,
manifest payload SHA256
`81d7ebacd7baedb557187fd04461b54420ec64baeada4693fc5ab4440f07bdd6`.
[Gói QA nhỏ](unified_comparison_checks.zip) gồm năm thành viên: log test,
cold verify, validation, consumer và manifest hash; **4.697 byte**, SHA256
`814ed01046fcd77dc6a25ae1604df46fc6660158d92102bdb7994ec3994f3562`.
Consumer `-I` mới đã PASS byte/hash gói và tái dựng đúng audit/manifest; trạng
thái release vẫn BLOCKED. Gói không chứa lại thị trường, weights hoặc H09 ZIP;
cần asset local đã hash. Diff whitespace và **61 liên kết/anchor local** trong bốn tài liệu hiện hành PASS.

```powershell
Expand-Archive -LiteralPath docs/plan/week12/unified_comparison_checks.zip -DestinationPath "$env:TEMP/u06-checks"
py -3.13 -I -X utf8 "$env:TEMP/u06-checks/verify_package.py" "$PWD" docs/plan/week12/unified_comparison_checks.zip
```

Nguồn runtime U05 giữ nguyên;
native row-wise vẫn **FAIL**, whole-system causal vẫn **PENDING_U06_U07**,
API/paid API/training đều **false**, chưa merge nền vào develop.

### Checklist chi tiết U05

Tiếp tục trên nhánh tích hợp từ U04
`45ab87a132463dd2bada2bb0d7d9dbbee13dd193`; ref
`refs/archive/fix-develop-u05/integration` giữ mốc đầu vào. Không thay code
native hoặc nâng `native_rowwise_causal_gate=FAIL` thành PASS.

- [x] U05.1 — Audit nguồn noncausal: normalizer, bfill, volume toàn cửa sổ và sáu cửa sổ phụ thuộc `len(d)`.
- [x] U05.2 — `causal_common_v1` riêng cho 85 handler, rolling/expanding PIT, warm-up/missing mask rõ; nguồn native nguyên byte.
- [x] U05.3 — Orientation trên train; top5/threshold trên validation common support, purge theo exit thực và chu kỳ LONG/CASH không chồng lấn; test không vào fit.
- [x] U05.4 — Artifact nguồn/runtime/lịch/costs; replay fit trước load, freeze ID/sign/threshold khi predict, không reset origin hoặc fallback native.
- [x] U05.5 — Spec/snapshot/forecast v2 tường minh; một raw parent, native giữ request cũ, cả family common dùng cùng causal projection.
- [x] U05.6 — CLI fit/verify/predict/bridge offline, model/price hashes và giới hạn gate alpha riêng với toàn hệ.
- [x] U05.7 — Prefix extension/future poison đủ 85 handler, purge/orientation, bridge tám vai trò và hồi quy đúng vùng PASS.
- [x] U05.8 — Cold replay/QA, đối soát frozen evidence/gate cũ, diff/links và commit nhánh tích hợp.
- [x] Bàn giao nền phần mềm vào develop — U06/U07 đã nghiệm thu offline theo phạm vi, xem checklist U07.
- [ ] Release causal toàn hệ — U05/U07 không tự chứng nhận Zero-Leakage; giữ giới hạn news, nguồn và exposure.

### Kết quả và giới hạn U05

`causal_common_v1` dùng đủ **85 công thức native** trong namespace riêng, không
monkeypatch hoặc sửa byte `core/alpha_compare.py`, selector/agent native hay
engine kinh tế. Thay riêng toán tử: không bfill, chuẩn hóa expanding theo từng
prefix, volume observed-only không proxy và sáu cửa sổ cố định thay `len(d)`.
Warm-up **300 bars**, normalizer tối thiểu **20 quan sát**; missing/undefined
có mask, thiếu support phải dừng, không zero-fill hoặc fallback native. Đây vẫn
là các công thức single-stock adaptation hiện hữu, không nhận là tái lập đầy đủ
WorldQuant cross-sectional/industry/VWAP gốc.

Selector học orientation bằng train Spearman; chọn top5/threshold trên validation
**common support**, dùng cycle LONG/CASH thực và phí hai chiều. Nhãn gọi chính
`compute_round_trip_net_return` qua ufunc; không thêm công thức net khác. Train
exit phải **< validation start**, validation exit **< test start**; grid cách ba
phiên không chồng cycle. Threshold candidates `.05/.10/.20`, support tối thiểu
60 train/30 validation và 5 LONG được khóa trong artifact. Artifact giữ toàn
validation search, selected IDs/sign/threshold, source/runtime/lịch/giá/costs.
Giá test không vào fit, kể cả khi poison thành NaN. Load tái lập train/validation
một lần; predict chỉ tính feature PIT, không chọn lại, không reset origin hoặc
đổi selected ID khi missing.

Normalization giữ **history origin cố định** trên toàn prefix hợp lệ; khác với
native dùng cửa sổ 600 nến. Bridge vẫn dùng cùng file giá và raw upstream 600
nến: native request nguyên vẹn, cả sáu phương pháp common và Fact_Anchor nhận
cùng năm factor/report causal. Selector dùng anchored history để tính feature;
đây là delta profile được công khai, không gán cho riêng prior/MT. Spec
`unified_experiment_v2` khóa `input_profile` và `causal_sources` mỗi mã/fold
(selector + giá đều ở `source_hashes`). Snapshot/forecast/result v2 và CSV giữ
profile, projection/native-parent hashes; v1 không nhận causal snapshot ngầm.

Regression bổ sung đã phát hiện opaque hash provenance toàn file có thể đổi
source-card MT dù chỉ giá sau cutoff thay đổi. V2 nay chỉ dùng digest **request,
facts card và nội dung reply PIT** cho token trong prompt; policy proof, raw
source hashes và dependency ledger vẫn giữ đầy đủ bên ngoài prompt. V1/archives
không đổi. Poison cả future prices và provenance response không đổi request
ở bất kỳ nhánh nào; outcome và hash nguồn thay đổi đúng như kỳ vọng.

Đã compile **10 file Python mới/đổi**, PASS **151 case duy nhất / 19 module**,
không fail/error/skip trong các log nghiệm thu cuối:

| Log trong gói QA | PASS | Phạm vi |
| --- | --- | --- |
| `causal.log` | 17 | Oracle toán tử/kinh tế, 85 raw handlers trước warm-up, prefix extension, future/validation poison, purge/freeze, cache, v2, tám request và CLI |
| `unified.log` | 15 | Hồi quy v1 registry/snapshot/runner/UNKNOWN/resume/ledger/CLI/UI và lazy OFF |
| `contracts.log` | 41 | Account/target, classification helper, JSON UI và RunBook |
| `data.log` | 42 | Prior/quality-gate leakage và MT Decision/adapter/features |
| `native.log` | 36 | Native golden/token/paired, outer-cutoff và các counterexample native row-wise |

Prefix extension kiểm đủ 85 output ở các boundary 380/600/900; raw handlers
được so cả trước warm-up. Future OHLCV/missing-volume không sửa quá khứ;
validation poison không đổi orientation train; test poison không đổi artifact.
Native counterexamples vẫn **`native_rowwise_causal_gate=FAIL`**, không bị đổi nhãn
thành PASS bởi test detection hoặc local alpha gate.

Cold fixture **synthetic** có **133 cycle train**, **59 cycle validation common**,
purge một cycle tại mỗi boundary và freeze threshold `.20`. Native agent/selector
thật chạy đúng một lần trên cùng giá: top5 giao **2/5**, Jaccard **0,25** với causal
tại một cutoff (600 nến native so với 1.297 nến anchored causal). Đây chỉ là
numeric/input bridge, không đo hiệu ứng hosted hoặc lợi nhuận thị trường.
CLI fit/verify/predict/bridge/replay/export chạy ở tiến trình `-I` mới: artifact,
projection, native request và policy/ledger **8/8 slot, 8 account** khớp; 5 response
offline/3 fallback, prompt lớn nhất **2.859 ký tự**. Không API, không nạp student
weights hoặc fit/cập nhật model thị trường; numeric selector được fit trên fixture.

Đối soát lại **21.383 artifact frozen** và đủ **21.948 đường dẫn U01**: PASS.
**484/491 source bindings U04** nguyên byte; bảy file đổi được ghi trong
`previous_gate_delta.json`, file U05 mới có bindings riêng. **107 package và
Python 3.13.5** giữ nguyên; không cài mới môi trường. Receipt U04 giữ scope
snapshot cũ; các nhóm U05 ở bảng trên là kết quả kiểm lại, không phải nghiệm thu toàn hệ.
Không full suite/E2E/toàn leakage suite; chỉ các nhóm trên cho vùng thay đổi.

[Gói QA, selector, bridge và fixture journal](causal_common_profile_checks.zip):
**347.774 byte**, SHA256
`dbb07fa015c62833ef383088eb504a69b7cdebbcee9e9596aa219b279307a08d`.
Manifest khóa **68 thành viên**, **497 source bindings**, runtime, log/IDs,
compile list và toàn bộ fixture/journal. Consumer mới đã PASS hash/source/runtime,
restore sang thư mục mới rồi tái fit đúng selector, projection/bridge/ledger và
native numeric; không tạo SDK/HTTP client, bank hoặc student. Diff whitespace và
**56 liên kết/anchor** trong bốn tài liệu hiện hành PASS. Tái lập từ repo root:

```powershell
Expand-Archive -LiteralPath docs/plan/week12/causal_common_profile_checks.zip -DestinationPath "$env:TEMP/u05-checks"
py -3.13 -I -X utf8 "$env:TEMP/u05-checks/verify_package.py" docs/plan/week12/causal_common_profile_checks.zip "$env:TEMP/u05-cold-restore"
```

[Hướng dẫn profile/CLI](../../../README.md#causal-alpha-profile) mô tả schema
lịch, nguồn và bridge. Harness trong ZIP chạy riêng `causal`, `unified`,
`contracts`, `data`, `native` khi vùng tương ứng đổi. Local alpha PIT PASS không
chứng nhận availability tin, PIT universe, HMM/scaler, retrieval/student,
vendor/execution data hoặc contamination của hosted model. **Whole-system
causal gate còn PENDING_U06_U07**; chưa mở release inference, cohort mới,
superiority hoặc merge nền vào develop.

### Checklist chi tiết U04

Tiếp tục trên `feat/fix-develop-unification` từ U03
`84d9307a91ae7ff12c0cd321964cddff8a4349a9` theo §4.1; ref
`refs/archive/fix-develop-u04/integration` giữ mốc đầu vào. Không sửa engine
kinh tế, native factory, archive hoặc các runner lịch sử để nhận identity mới.

- [x] U04.1 — Đối soát nhánh sạch, mốc U03 và callers; giữ nền ngoài develop.
- [x] U04.2 — Registry tám vai trò, DAG dependencies, ExperimentSpec khóa version/cohort/order/model/options/source/resource/runtime/calendar/costs.
- [x] U04.3 — SharedSnapshot bất biến, bản sao riêng cho consumer, projection từ graph/PIT 600 bars và rào query-y đệ quy.
- [x] U04.4 — Adapter gọi primitive native/common/prior/facts/MT hiện hữu; lazy bank/context/student, tách raw proposal với fallback/veto/final policy.
- [x] U04.5 — Một RunBook/OS lock, shared một lần mỗi realization, checkpoint/resume, UNKNOWN và outcome barrier đủ mọi repeat/variant.
- [x] U04.6 — Evaluator chung canonical target, common support fail-closed, ledger reset mã/fold/realization/repeat, classification/undefined/unit rõ.
- [x] U04.7 — CLI registry/spec/replay/verify/export và UI cùng IDs/evaluator; mặc định native, hosted extensions chưa được mở.
- [x] U04.8 — Compile/test đúng vùng, active retrieval/PIT, OFF không mở tài nguyên, nối ContextBank và đối soát evidence/gate cũ.
- [x] U04.9 — Cold replay/consumer mới, khóa source/runtime/log/fixture, diff/links và commit nhánh tích hợp.
- [x] Bàn giao nền vào develop — gate U07 đã PASS offline; U04 không tự cấp release inference hoặc causal gate.

### Kết quả và giới hạn U04

Hoàn tất **09/11/2026** trên nhánh tích hợp. Registry `unified_variant_registry_v1`
có `original_fix`, `original_common`, `bayesian_v1`, `C2`, `A_tp_pool`, `B_semantic`,
`MT_BICL` và dependency/control `Fact_Anchor`. Native vẫn dùng profile U03;
`Original_common` chỉ là alias archive được công khai, không đổi nhãn pilot.
Spec khóa DAG/order, cohort, serving config, source/resource hashes, runtime,
calendar fingerprint, repeats/realizations, seed **42**, kinh tế và missing policy.
Calendar/cohort admission, counterbalance và protocol nghiên cứu mới vẫn thuộc U06.

`SharedSnapshot` seal bytes bất biến, chặn query-y đệ quy và availability sau
cutoff; consumer nhận bản sao riêng. `snapshot_from_graph` giữ raw reports,
ảnh, factors/sentiment và kiểm prefix đúng **600 bars** trước projection.
Adapter tái dùng native factory, common renderer, request của bank và fact/MT
policy hiện hữu. Bank, context/student được tạo khi nhánh tương ứng cần;
native/common OFF và Fact_Anchor riêng không mở student. Callback
`runner.forecasts_done` nối vào ContextBank để khóa nhãn selected query.
Family common hiện theo hợp đồng **VI/1d** đã có; native live VI/EN cũ giữ nguyên.

Runner dùng một RunBook/OS lock, một shared mỗi điểm/realization và deepcopy
sang mọi repeat/variant. Checkpoint shared/preparation/forecast/outcome có
parent hashes; UNKNOWN không tự gọi lại. Outcome chỉ được nối sau mọi forecast
bắt buộc của điểm đã durable. Raw JSON/proposal và hash nguồn được giữ riêng
với fallback/veto/final policy; schema lỗi không thành CASH. Evaluator tái dùng
`target_fields` và `compute_account_metrics`, không thêm công thức P&L khác;
ledger reset theo **mã/fold/realization/repeat**, common support fail-closed.
Classification tách từng realization/repeat, giữ confusion/BA/MCC/F1/null;
không coi repeats hoặc Fact_Anchor là thêm N thị trường độc lập.

CLI có registry/spec/replay/verify/export; UI **`/experiments`** đọc cùng IDs,
evaluator và JSON/CSV. Mặc định chọn native; request chọn extension ở endpoint
backtest cũ bị chặn trước engine/credential. Trang backtest cũ và các runner/
archive lịch sử được giữ cho hợp đồng cũ, không gán identity U04 cho chúng.
[Hướng dẫn vận hành và adapter](../../../README.md#unified-experiments) mô tả
resource factories và cấu trúc bundle. CLI chỉ replay **prepared assets có hash**:
dựng lại prompt/schema/policy/ledger, không chạy lại retrieval, không nạp student
weights và không tái sinh hosted response. Mọi subcommand CLI chặn mạng ngoài
máy. Caller của adapter phải cung cấp đúng provider/assets đã xác minh; việc
nghiệm thu provider/cohort/transport cho thu mới còn ở U06–U08.

Đã compile **9 file Python mới/đổi** và PASS **128 test case duy nhất / 15 module**,
không fail/error/skip:

| Log trong gói QA | PASS | Phạm vi |
| --- | --- | --- |
| `unified.log` | 15 | Tám vai trò, active retrieval thật trên fixture đã kiểm, lazy OFF, immutable/PIT/query-y, raw/policy/bypass, reset/CASH/null, UNKNOWN/resume, CLI/UI |
| `contracts.log` | 41 | Target/account risk, classification pilot helper, JSON UI và RunBook/reconcile |
| `data.log` | 42 | Improvement prior/leakage, quality gate leakage, MT Decision, adapter/features leakage |
| `native.log` | 30 | Native golden/guard/poison, token budget và paired protocol |

Cold fixture tổng hợp chạy CLI replay, rồi tiến trình `-I` khác verify/export:
**8/8 slot**, **8 account**, **8 classification groups**, **5 response offline**
và **3 fallback**, prompt lớn nhất **2.644 ký tự**, policy/ledger khớp hoàn toàn.
Đây là **fixture hợp đồng synthetic**, không phải tám forecast thị trường mới,
không dùng frozen student weights hoặc fit/cập nhật model nghiên cứu. Kiểm
active prior dùng retriever/index/selector/renderer thật trên bank fixture có
nhãn engine; không nhận fixture fallback là bằng chứng active retrieval.

Đối soát lại **21.383 artifact đóng băng**, đủ **21.948 đường dẫn U01**: PASS.
**479/482 source bindings U03** giữ nguyên; ba file đổi là `.gitattributes`,
root `README.md`, `web_interface.py`; nguồn native/economic/renderer cũ không đổi.
**107 package/Python 3.13.5** vẫn khớp. Gate U03 giữ đúng snapshot/phạm vi cũ;
không ghi là đã chạy lại cả 183 test hoặc replay archive 204 slot. U04 chỉ chạy
các nhóm trên, không full suite/E2E/toàn leakage suite. Hạn chế
**`native_rowwise_causal_gate=FAIL`** vẫn được giữ trong registry/kết quả/UI.

[Gói QA và fixture journal](unified_experiment_checks.zip): **126.040 byte**,
SHA256 `dc004fc209206378133fd073560145d045e124f00dc3c28f160becce46ba161f`.
Manifest khóa **46 thành viên**, **491 source bindings**, runtime, test IDs/logs,
compile list, delta gate cũ và toàn bộ journal fixture. Consumer mới đã kiểm
PASS hash/source/runtime, restore sang thư mục tạm mới và tái tính đúng hoàn
toàn prompt/policy/ledger; không khởi tạo
SDK/HTTP client, bank hoặc student. Diff whitespace và **52 liên kết/anchor**
trong bốn tài liệu hiện hành đã kiểm PASS. Có thể chạy lại từ repo root:

```powershell
Expand-Archive -LiteralPath docs/plan/week12/unified_experiment_checks.zip -DestinationPath "$env:TEMP/u04-checks"
py -3.13 -I -X utf8 "$env:TEMP/u04-checks/verify_package.py" docs/plan/week12/unified_experiment_checks.zip "$env:TEMP/u04-cold-restore"
```

Harness `run_scoped_checks.py` trong gói chạy riêng `unified`, `contracts`,
`data` hoặc `native` khi vùng tương ứng đổi. Không API/thu cohort mới, không
khôi phục H07 bị hủy, không nhận causal/superiority hoặc release inference từ U04.

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
- [x] Bàn giao nền vào develop — kiểm tra U07 liên quan đã PASS; chưa mở inference hoặc nhận causal gate.

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
- [x] Bàn giao nền vào develop — sau U03 và các kiểm tra U07 liên quan, không suy riêng từ U02.

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
