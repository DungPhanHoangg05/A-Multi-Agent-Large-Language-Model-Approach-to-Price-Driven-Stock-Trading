# Kế hoạch nghiên cứu và triển khai KLTN

Đề tài Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent
LLM Stock Trading in the Vietnamese Stock Market.

## Trạng thái hiện hành

**Từ 12/11/2026, `develop` là nhánh tích hợp duy nhất cho toàn bộ công việc:**
hệ gốc, Bayesian/MT-BICL, thực nghiệm, bài báo và phản hồi reviewer.
Task mới tách nhánh từ develop rồi merge trở lại theo AGENTS; `fix` chỉ giữ vai
trò nguồn lịch sử. [Hướng dẫn làm việc chung](week12/develop_workflow.md) xác định
nguồn bài báo, evidence, lệnh kiểm offline và ranh giới tài liệu cũ.
[Checklist W12](week12/README.md#đầu-mối-làm-việc-duy-nhất-trên-develop) là nơi
theo dõi F06–F12 và các yêu cầu khoa học/editorial còn thiếu sau U10; root `plan.md` là lịch sử.

**Kế hoạch thực hiện phần còn lại:** [bài báo và giao diện chọn phiên bản](week12/final_paper_ui_plan.md),
audit ngày 12/11/2026 tại `develop:d16630e9`. Giữ tám section chính và appendix
A–F của bài; đưa phương pháp/kết quả mở rộng chính vào thân bài, chi tiết vào
appendix. F01–F05 cụ thể hóa U10; F06–F12 nâng ứng dụng Flask hiện tại để chọn,
chạy và so sánh phiên bản. [Checklist cuối](week12/README.md#công-việc-cuối-cho-bài-báo-và-giao-diện)
là nơi cập nhật tiến độ. F00–F05 và U10 đã hoàn tất phạm vi bàn giao nội bộ: [mapping và historical restore](week12/final_evidence_map.md)
giữ snapshot 810 nguồn, restore 286 asset và cold replay nguyên byte 15 artifact
U09; [release F02](week12/README.md#f02--generator-và-artifact-bài-báo-u09) có
26 artifact/798 ô có provenance, 16 test và cold render nguyên byte PASS.
[F03](week12/README.md#f03--nội-dung-bản-thảo-hai-nghiên-cứu) đã bổ sung
nội dung tám section/A–F, giữ metadata/cấu trúc và build hai PDF 50 trang,
kiểm trực quan đủ 100 trang PASS. [F04](week12/README.md#f04--sơ-đồ-caption-và-layout-bản-thảo)
đã cập nhật bốn sơ đồ/caption, figure hai baseline và vị trí bảng; hai PDF
51/50 trang, kiểm đủ 101 trang PASS. [F05](week12/README.md#f05--reviewer-locators-và-bàn-giao-bản-thảo-cuối)
ngày 13/11/2026 đã đồng bộ đủ 87 yêu cầu/matrix/response, chốt PDF, source,
companions, locators và manifest; **0/18 comment được chứng nhận đóng**.
Bước tiếp theo là F06 UX/capability/API contract; F06–F12 chưa bắt đầu,
UI chưa đổi và không gọi LLM/market API để hoàn thiện bài từ U09.

U06 hoàn tất offline với amendment v2, 102 anchor/ba repeat, 51 selector binding
và student/HMM frozen; U07 đã nghiệm thu paired/recovery offline và nền đã vào
develop. **U08 hoàn tất ngày 12/11/2026**: receipt `PASS_U08_RESEARCH`, đủ
**102 điểm/chín mã, 2.448 forecast, 102 canonical labels**. Cold consumer mới
và gói research đã PASS, giữ 8.035 file journal nguyên byte và đối soát 718
source bindings/runtime đã khóa, 0 inference mới trong lượt nghiệm thu.

[Nghiệm thu và bàn giao U08](week12/README.md#nghiệm-thu-u08) ghi coverage,
raw/usage, reset, nguồn/hash và lệnh kiểm gói. Ledger giữ 1.702 HTTP attempts,
trong đó 15 raw đã nghỉ vẫn tính chi phí và được lưu; không có UNKNOWN active.
[Gói research đã seal](week12/unified_live_research.zip) là đầu vào U09.
**U09 hoàn tất ngày 12/11/2026**: [kết quả và giới hạn](week12/README.md#kết-quả-và-giới-hạn-u09),
[gói bảng/figure](week12/unified_analysis_results.zip) và
[receipt](week12/unified_analysis_acceptance.json) đã PASS. Cold replay15 artifact
nguyên byte,29 test đúng phạm vi, compile8 file; oracle độc lập1.530 account khớp.
Return mean account: native−0,652699%, common−1,024794%, v1−0,698188%,
MT−1,253483%; mọi vai trò research âm. V1 cải thiện so common trong band mô tả,
chưa có bằng chứng vượt native; chỉ sensitivity trên sáu fold đã exposed.
U10 đã xong F01–F05 trong phạm vi bản thảo/bằng chứng nội bộ; reviewer/editor
acceptance, quyền/PID và các nghiên cứu còn thiếu không được suy là hoàn tất. Native row-wise causal vẫn FAIL,
whole-system causal NOT_CERTIFIED;0 API mới hoặc refit trong U09.

Yêu cầu mới: [hợp nhất fix làm hệ gốc và develop làm các mở rộng](week12/fix_develop_integration_plan.md).
Đã hoàn tất phân tích và kế hoạch; [checklist W12](week12/README.md) quản lý U01–U10.
U01 đã khóa inventory/hash hai cây nguồn, imports/callers và bằng chứng;
[kết quả audit](week12/README.md#u01--inventory-nguồn-và-bằng-chứng-đã-khóa) ghi rõ delta nguồn và binding lịch sử.
U02 đã ghép nguồn và PASS kiểm thử đúng phạm vi trên nhánh/worktree riêng;
[checklist chi tiết](week12/README.md#checklist-chi-tiết-u02)
theo dõi contracts/schema/chart, dependencies, evidence và kiểm thử.
U03 đã PASS parity offline trên miền native hợp lệ, replay đủ 204 slot B/AS;
[checklist U03](week12/README.md#checklist-chi-tiết-u03) ghi profile
`original_fix_serving_v1`, delta budget, log và giới hạn nhân quả.
U04 đã có registry tám vai trò, snapshot/records, runner/evaluator và CLI/UI
offline dùng chung; [checklist U04](week12/README.md#checklist-chi-tiết-u04)
ghi 128 test, cold fixture và giới hạn prepared-asset replay.
U05 đã thêm `causal_common_v1`, selector train/validation đã purge và bridge
native/common; [checklist U05](week12/README.md#checklist-chi-tiết-u05) ghi 151 test
và cold replay. Gate này chỉ cho alpha PIT, không nâng native hoặc toàn hệ
thành Zero-Leakage. U07 nghiệm thu phần mềm offline, không nâng gate native/
whole-system causal. Research U08 đã seal với smoke tách biệt; U09 dùng receipt/dataset active
để phân tích paired, giữ nguyên raw đã nghỉ làm bằng chứng chi phí/reset. Trạng thái pilot bên dưới
là bằng chứng giữ nguyên, không phải nghiệm thu hệ thống hợp nhất.

Hệ thống giữ Original và bốn nhóm cải tiến.

| Phiên bản | Vai trò |
| --- | --- |
| Bayesian Prior v1 | Regime retrieval và historical examples |
| Bayesian Prior v2, đại diện C2 | Conditional statistics và readiness |
| Bayesian Prior cải tiến A/B | A_tp_pool và B_semantic |
| MT-BICL | Bucket context, student/teacher, facts, utility và revision policy |

[Kế hoạch hiện hành](week11/historical_reevaluation_plan.md#h07--pilot-ghép-cặp48-điểm-bằng-api-free)
là FREE_PAIRED_PILOT_48 để phục vụ buổi trình bày trong hai ngày. Sáu primary
gồm Original_common, bayesian_v1, C2, A_tp_pool, B_semantic, MT_BICL; giữ
Fact_Anchor dependency. CORE4 ×12 cutoff chung2023–2024 =48 điểm, một repeat,
336 Decision nominal và0–96 vision mới tùy archive hợp lệ; smoke9 lượt riêng.
Bridge fix mặc định OFF, nếu khóa ON trước inference thì thêm48 Decision.
Chỉ Groq Free, chi tiêu0 USD; preflight phải xác minh ngân sách48 giờ.

[Checklist W11](week11/README.md#checklist-đánh-giá-lại) quản lý H01–H09.
H01–H06 của thiết kế cũ đã nghiệm thu dữ liệu, replica đủ ba seed/60 checkpoint,
chọn seed42/step3000, MODEL_GATE_PASS/CPU_REPLAY_MATCH;492 HMM prefix,
84 test offline và55 smoke execution. Các asset/receipt đã hoàn tất được giữ.
Pilot cần audit bank852/reuse upstream, khóa protocol/input/runtime riêng và
kiểm lại phần thay đổi trước release; H03–H06 cũ không tự cấp gate pilot.

Ngày09/11/2026, người dùng hủy H07 đầy đủ34.806 call. Supervisor/child đã
dừng, run_r1/managed_r1 đã xóa; grant thu đầy đủ REVOKED, api=false.
Trước khi xóa có186 node upstream complete và0 forecast grid. Chỉ giữ riêng
ledger tối thiểu103 request/264.449 token đã tính hoặc reserve để cộng quota
còn hiệu lực vào lượt mới. Smoke H06 và model/donor/HMM giữ nguyên.

Pilot đã nghiệm thu P01–P05:48 shared,336 forecast,48 nhãn và cold PASS;
[receipt H07](week11/free_pilot_h07_acceptance.json) khóa evidence trước phân tích.
H08 đã chạy offline và cold consumer PASS; [receipt H08](week11/free_pilot_h08_analysis.json).
Return bình quân tám account: Original−3,690521%; A_tp_pool−2,550858%,
D+1,139663 đpt với band95%[−0,680467;2,959792]; MT−4,414181%, D−0,723660 đpt.
Cả sáu return âm; mọi band D return chứa0, chưa đủ bằng chứng vượt Original.
H09 đã đóng gói và phục hồi cold PASS; trạng thái PILOT_COMPLETE, phạm vi48 điểm.
[Bàn giao và lệnh tái lập](week11/README.md#h09--bàn-giao-pilot48)
cùng [receipt gói bằng chứng](week11/free_pilot_h09_handoff.json) quản lý SHA256.
Không đánh dấu toàn hệ thống hoặc full matrix DONE từ pilot này.
Bayesian dùng bank signal đóng băng2020–2022; MT giữ numeric context của
phương pháp. Query chung dùng donor fix; bank/query khác provenance phải
được audit và báo như giới hạn chuyển giao. Kết luận là historical exploratory
có điều kiện trên shared reports; một repeat không đo variance giữa các lần LLM.
H07 đầy đủ1.020 điểm vẫn CANCELLED. Execution acceptance giữ
PENDING_EXECUTION_DATA và giới hạn vendor series.

## Những phần đã triển khai

- Hệ gốc Indicator/Alpha/Sentiment/Pattern/Trend/Decision cùng backtest.
- Memory Bank và Bayesian Prior có historical signals, provenance, PIT,
  retrieval, feature index, split readiness và BRPP.
- C2, A_tp_pool, B_semantic, các content-mode ablation và retrieval controls.
- MT-BICL có teacher Beta–Bernoulli, student causal, task/scaler/regime,
  bucket context, fact packet, posterior utility4096 draws và policy veto.
- Readiness donor archive, grid, label bridge và kiểm input trước inference.

## Hợp đồng nghiên cứu

LONG vào Open(t+1), ra Close(t+3); SHORT giữ CASH. Phí0,25% và slippage0,10%
cả hai chiều. Nhãn lịch sử dùng compute_round_trip_net_return.
Nến query≤t, tin available≤t và mọi observation phải exit<t.
Upstream một lần/unit/realization, deep-copy tới mọi nhánh.
BRPP≤600 ký tự với K=3, prompt<6.500, API qua retry/checkpoint đã audit.

Model/recipe/prompt/options và IDs được khóa trước inference. Không chọn
winner theo subgroup thuận lợi, không vote/best repeat hoặc đổi model/key
ngầm. Kết quả historical đã exposed mang scope exploratory.
Xác nhận forward có protocol/power/release riêng.

## Tài liệu theo giai đoạn

- [W1](week1/README.md), [W2](week2/README.md), [W3](week3/README.md),
  [W4](week4/README.md), [W5](week5/README.md) quản lý dữ liệu và Bayesian Prior.
- [W6](week6/README.md), [W7](week7/README.md), [W8](week8/README.md),
  [W9](week9/README.md) quản lý cải tiến, development và holdout.
- [W10](week10/README.md) mô tả MT-BICL hiện hành.
- [W11](week11/README.md) quản lý tiến độ áp dụng lại trên dữ liệu chung.
- [W12](week12/README.md) quản lý điều kiện xác nhận và bàn giao.

Mỗi task thực hiện trên nhánh riêng từ develop, kiểm theo phạm vi,
Conventional Commit và hợp nhất sau khi các kiểm tra áp dụng PASS.
