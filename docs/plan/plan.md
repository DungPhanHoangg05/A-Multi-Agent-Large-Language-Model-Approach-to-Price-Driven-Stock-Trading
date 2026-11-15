# Kế hoạch nghiên cứu và triển khai KLTN

Đề tài Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent
LLM Stock Trading in the Vietnamese Stock Market.

## Trạng thái hiện hành

**Viết khóa luận, cập nhật ngày 15/11/2026:** thư mục làm việc là `thesis/`.
[Dàn bài tiếng Anh](../../thesis/outline.md) và [kế hoạch chi tiết bằng tiếng Việt](../../thesis/plan.md)
bao phủ từ chuẩn bị đến bàn giao PDF/nguồn cuối qua 84 task. Phần phương pháp
phải giải thích toàn hệ thống cho giảng viên lần đầu tiếp cận.
[Checklist viết khóa luận](../../thesis/plan.md#21-một-nguồn-trạng-thái-công-việc) là nơi duy nhất
cập nhật trạng thái ngay trong kế hoạch theo yêu cầu tác giả. Hồ sơ yêu cầu,
phạm vi nghiên cứu và [kiểm kê hai nghiên cứu](../../thesis/evidence.md#3-kiểm-kê-nguồn-hiện-tại-và-hai-nghiên-cứu-đã-khóa)
đã có; [danh sách đọc](../../thesis/evidence.md#4-danh-sách-đọc-nguồn-gốc-và-quy-ước-khóa-trích-dẫn)
phân nhóm nguồn gốc, trạng thái đọc/kiểm và quy ước khóa trích dẫn.
[Thuật ngữ và ký hiệu](../../thesis/evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt)
thống nhất tên phương pháp, cấp episode/task/query và đơn vị.
[Danh mục hình/bảng/thuật toán](../../thesis/evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn)
giữ 23 ID có task, vị trí, loại nguồn và provenance; sản phẩm sẽ tạo tại task
phụ trách. [Ví dụ xuyên suốt EX01](../../thesis/evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết)
chọn FPT tại cutoff 03/07/2023 theo quy tắc không dùng outcome, nối nguồn
đầu vào/lịch sử/proposal/policy và tách kết quả sau cutoff.
[Khung sáu chương](../../thesis/evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm)
đã có tiêu đề/placeholder tiếng Anh và quy ước dùng sổ bằng chứng chung.
P2 đã có [bản nháp Chương 3 §3.1–§3.7](../../thesis/chapters/03_background.md),
từ quan sát/kinh tế đến tín hiệu, HMM, Bayes, MT/utility và PIT/đánh giá,
kèm F01/F02 có source. Chưa rà soát toàn văn cuối hoặc tạo kết quả thực
nghiệm mới. **P3 đã đủ bản nháp [Chương 4 §4.1–§4.10](../../thesis/chapters/04_proposed_system.md)**:
từ tổng quan/hợp đồng/các agent và Native/Common tới lịch sử/regime, bốn prior,
MT/teacher–student, facts/utility/policy, projection, tám vai trò/ba thuật toán,
ngân sách/phục hồi và ứng dụng. F03/F04/F05/F05a/F06/F07/F08/F11 có nguồn;
EX01 kết thúc bằng outcome sau barrier, giữ net loss và giới hạn causal.
G2 được tự kiểm nội bộ tại sổ bằng chứng; chưa phản biện ngoài/dàn trang cuối.
UI/F11 vẫn PENDING; T36 trở đi và các chương còn lại giữ trạng thái hiện có.
Bản xem hai
trang bìa có Supervisor căn giữa. Hạn nộp và quy định
trích dẫn/bố cục chính thức chưa được cung cấp. **Trao đổi với người dùng,
kế hoạch, checklist và hướng dẫn quản lý bằng tiếng Việt; toàn bộ nội dung
khóa luận bằng tiếng Anh.** Việc sửa tài liệu này không đổi F11/F12 hoặc phạm vi
nghiệm thu nghiên cứu lịch sử.

Ngày **14/11/2026**, đã nhận khung KLTN và lập [dàn bài Markdown độc lập](../../thesis/outline.md)
trong `thesis/`: sáu chương, câu hỏi nghiên cứu, phụ lục và ánh xạ mã nguồn/bằng chứng.
Chỉ tham chiếu bố cục mẫu; nội dung xây dựng theo hệ hiện tại. [Ghi nhận phạm vi](week12/README.md#khởi-tạo-dàn-bài-khóa-luận)
tách việc viết KLTN khỏi nghiệm thu UI và thực nghiệm; chưa tạo LaTeX/PDF mới.

Nguồn `paper/` đã được [làm rõ đóng góp và rà liên kết](week12/README.md#làm-rõ-đóng-góp-và-rà-liên-kết-bài-báo):
highlights/abstract mới, bảng indicator, bỏ hình lịch đánh giá cũ; hai PDF vẫn
44 trang/43 references, 42 đích truy cập đã xác nhận và một trang nhà xuất bản
còn yêu cầu xác minh trình duyệt, chi tiết trong báo cáo liên kết hiện hành.

Nguồn bài báo ngày 13/11/2026 đã được [biên tập thành bản độc lập](week12/README.md#biên-tập-bài-báo-độc-lập):
bỏ mã task/giọng phản hồi, caption một câu, toàn bộ bảng/hình `[htb]`, cả hai PDF
44 trang và 43 references; nguồn ở `paper/`, PDF hiện hành ở [outputs/paper](../../outputs/paper/README.md).
Cấu trúc thư mục và cách khôi phục kết quả cũ được ghi tại [checklist dọn dẹp](week12/README.md#sắp-xếp-nguồn-bài-báo-và-kết-quả).
Số liệu, công thức và bằng chứng thực nghiệm giữ nguyên.

Ngày 13/11/2026 đã sửa bố cục và bổ sung references cho nguồn `paper/`:
cả hai PDF 50 trang, 43 tài liệu được dẫn; reference [6] có URL thay thế đã kiểm.
[Checklist và gói bố cục trước](week12/README.md#điều-chỉnh-bố-cục-và-tài-liệu-tham-khảo-của-bài-báo)
ghi phạm vi tài liệu, đối soát số liệu và PDF/ZIP Overleaf mới; bản F05 cùng
crosswalk của nó giữ nguyên làm bằng chứng lịch sử.

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
F06 ngày 13/11/2026 đã chốt [contract serving riêng](week12/variant_serving_contract.md),
sáu lựa chọn chính/hai nâng cao, preflight và job/config/result identity; 33 test
đúng phạm vi PASS. F07 đã nối reader U09 đã verify với experiments, so sánh
nhiều bản/baseline, chi tiết và export; 46 Python + 6 DOM PASS. UI tách
template/CSS/JS; browser trực quan chờ F11 do host/approval bị chặn. F08 đã có
provider/runner riêng, resource **188 binding/chín mã/58 phiên 01/07–23/09/2026**,
API job owner/preflight/stop/resume, quota/retry/UNKNOWN và paired DAG; **105 test
đúng phạm vi + compile18 PASS**, chỉ HTTP fixture, chưa smoke hosted mới.
F09 đã nối form/kết quả với serving: sáu bản chính/hai dependency, preflight,
so sánh cùng snapshot, raw/final/CASH, context và hai projection Alpha;
**108 Python + 18 DOM, compile5/JS7 PASS**. Template/CSS/JS đã tách file,
giữ đường realtime legacy riêng; UI VI/EN, báo cáo serving vẫn chỉ VI.
Browser desktop/mobile chưa kiểm vì host không khả dụng, giữ trong F11.
F10 đã nối backtest mới và danh mục owner vào experiments, cùng evaluator
account/classification U09, daily NAV/cycle returns, filter/contrast cùng
support và JSON/CSV; Full/No-Alpha legacy có adapter riêng. **156 Python +
31 DOM, compile13/JS7 PASS**, chỉ HTTP fixture; browser visual chờ F11.
**F11 đang làm**: đã nhận develop `4de6d1aa`, sửa prompt Original realtime và
snapshot VNINDEX. Theo yêu cầu mới nhất, form phân tích chạy realtime,
**bỏ hẳn mục Analysis source**, duy nhất **1D**, chọn một trong
sáu bản rồi Phân tích. Đã xóa lựa chọn as-of/daily riêng, so sánh, repeats và
cấu hình serving khỏi form. Original giữ pipeline hiện tại; bản nâng cấp dùng
cùng overlay từng agent rồi mở cùng bố cục kết quả, thêm phần BICL thực tế.
Tiến trình từ checkpoint, decision/policy/context giữ nguyên; không tính lại
hoặc bịa kết quả khi lỗi/UNKNOWN. [Runbook hiện hành](week12/variant_serving_contract.md#form-phân-tích-hiện-hành--realtime-1d).
[Receipt hiện hành](week12/serving_integration_acceptance.json) và
[QA song ngữ hiện hành](week12/serving_bilingual_checks.zip): **135 Python + 24 DOM, compile23/JS2 PASS**.
Đã sửa BICL đứng trước Decision cuối; khôi phục báo cáo Alpha Agent đầy đủ,
hiển thị common Alpha riêng đúng nguồn Decision, format Indicator theo HTML
Original tham chiếu. Tin hiển thị cùng snapshot/cutoff, thiếu metadata là NA.
Sáu layout dùng chung VI/EN và sáng/tối; đổi ngôn ngữ giữ query/job/filter và
cookie. Theo yêu cầu ngày14/11/2026, profile live mới
`live_bilingual_presentation_v1` tạo VI/EN trong cùng invocation Pattern/Trend/
Decision; Indicator/Alpha số học dùng mẫu song ngữ từ kết quả đã tính, không
chạy lại selector. Policy/snapshot canonical vẫn VI; sidecar trình bày riêng,
không sửa artifact nghiên cứu. Hai bản HTML được nhúng sẵn; đổi VI/EN ngay
tại chỗ, không reload/fetch/POST, không gọi dịch hoặc chờ quota Groq. Route
dịch đã ngừng đăng ký. Bản ghi cũ đọc cache hoàn tất đúng owner không cần key;
nếu chưa có tiếng còn lại thì cần phân tích lại một lần. Lượt phân tích đầu
vẫn dùng model và có thể tăng output token, không tăng số call để đổi tiếng.
Theme nhớ lựa chọn hoặc theo hệ điều hành. Các lần sửa dịch trước,21/21 phần
được rà riêng và raw/journal của incident giữ nguyên ở checklist/QA lịch sử.
Các QA cũ giữ nguyên byte làm lịch sử; không chạy toàn suite/cold study hoặc
gọi model/thị trường thật trong lượt sửa UI. Browser host vẫn không khả dụng;
Theo chỉ đạo mới của người dùng ngày14/11/2026, hợp nhất nhánh
`feat/precomputed-bilingual-results` vào `develop`, giữ **UI/F11: PENDING**.
Merge nguồn không phải nghiệm thu browser hoặc hoàn tất F11.
**F12 chưa bắt đầu**, paper/PDF/U09 giữ nguyên. Khung KLTN đã được tiếp nhận;
dàn bài và định hướng viết nằm tại [thesis](../../thesis/README.md).

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
