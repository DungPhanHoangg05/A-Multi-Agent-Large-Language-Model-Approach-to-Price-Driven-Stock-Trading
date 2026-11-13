# W12 — Xác nhận độc lập và bàn giao

[Kế hoạch tổng](../plan.md) · [Tiến độ W11](../week11/README.md) ·
[Kế hoạch đánh giá](../week11/historical_reevaluation_plan.md)

Hệ thống giữ Original, Bayesian Prior v1, Bayesian Prior v2/C2,
Bayesian Prior A/B và MT-BICL. Giai đoạn hiện hành đánh giá lại trên
dữ liệu historical đã exposed; chưa có release xác nhận forward.

## Đầu mối làm việc duy nhất trên develop

Ngày **12/11/2026**, theo yêu cầu người dùng, mọi công việc hệ thống, thực nghiệm,
bài báo và reviewer chuyển sang cùng luồng **nhánh tác vụ từ develop → kiểm tra
theo phạm vi → merge develop**. [Hướng dẫn làm việc](develop_workflow.md) là đầu
mối vận hành; không còn luồng phát triển riêng trên fix. Các tên `original_fix`,
donor commit và source pin tiếp tục là định danh phương pháp/bằng chứng.

- [x] Kiểm ancestry: `fix:9efd23f4` đã nằm trong `develop:4bc61086`; không có commit riêng của fix chưa được tích hợp.
- [x] Kiểm đủ cây fix: chỉ workflow GitHub Pages đã nghỉ là không có ở cây hiện hành; không bật lại deployment cũ.
- [x] Nguồn bài báo 50 file và revision 28 file đã có trên develop, cùng blob với fix; giữ nguyên raw/release/receipt lịch sử.
- [x] Chuyển đầu mối root plan sang kế hoạch chung; hướng dẫn code, bài báo, reviewer và bằng chứng cùng trên develop.
- [x] Kiểm diff/liên kết và đối soát evidence/source pins cho phạm vi tài liệu; không gọi API, refit hoặc sửa kết quả.

Đã kiểm **29 liên kết mới/thay đổi**, giữ đủ **729 source bindings U09**.
Rà checkout phát hiện **48 artifact lịch sử chỉ lệch CRLF/LF** so với inventory
U01; đã sao lưu bản checkout vào ZIP tạm rồi khôi phục đúng byte Git đã khóa,
kiểm cả OID/SHA256/length, không đổi giá trị dữ liệu hoặc expected hash. Các file
này không thuộc source pins U09 hoặc asset bindings U06 hiện hành. Bản sao trước
khôi phục: `%LOCALAPPDATA%/Temp/develop_checkout_newlines_d828a84970564413b1417138b1e2503e.zip`.
Verifier U01/U02 sau khôi phục **PASS 21.383 artifact**, đối soát **21.948 đường
dẫn**: giữ 21.947 đường dẫn, một workflow đã nghỉ có nguồn Git xác thực.

Đợt này chỉ sửa tài liệu quản lý và thêm hướng dẫn vận hành. Không chạy
compileall/unit/E2E/leakage theo AGENTS §1.2 vì code, runtime, schema, input,
paper và các kết quả đã khóa không đổi. Gate U03/U08/U09 giữ đúng phạm vi cũ;
việc tập trung công việc không nâng causal/reviewer acceptance hay đánh dấu U10
hoàn thành. Các bản README/plan cũ trong revision là tài liệu lịch sử khóa byte;
trạng thái hiện tại và công việc tiếp theo chỉ cập nhật tại kế hoạch chung/W12.

## Biên tập bài báo độc lập

Ngày **13/11/2026**, biên tập tiếp nguồn `paper/` theo yêu cầu bỏ mã task và
giọng trả lời phản biện, giữ các giới hạn và kết quả khoa học:

- [x] Viết lại abstract, introduction, related work, limitations, conclusion,
  availability và phụ lục thành bài độc lập; bỏ U08/U09, task/receipt/acceptance,
  đường dẫn quản lý dự án và nội dung mô tả quá trình sửa bài khỏi PDF.
- [x] Dùng hai tên nghiên cứu `component study` và `historical-context study`;
  đổi C2/A/B thành Conditional/Trend--pattern/Explicit counts, giải thích trong
  Methods và thống nhất bảng/sơ đồ/biểu đồ; nhóm Covered/Other được định nghĩa
  theo bốn mã có bank và năm mã còn lại, không nhầm với ngành ngân hàng.
- [x] Cả **21 bảng, 7 hình và 1 thuật toán** dùng đúng `[htb]`, không còn wrapper
  ghi đè; **29 caption và 21 ghi chú bảng** đều một câu, caption không quá 25 từ,
  ghi chú không quá 40 từ. Chi tiết phương pháp cần thiết nằm trong thân bài/phụ lục.
- [x] Giữ nguyên ô số của **32 panel bảng**, **27 khối equation/align** và byte
  của **hai file macro**; biểu đồ vector chỉ vẽ lại các điểm/cận đã có trong bảng
  để đổi nhãn, không chạy lại thống kê hoặc inference. Tên tác giả và tài trợ giữ nguyên.
- [x] Build mới hai cây độc lập, tám lệnh cuối
  `pdflatex → bibtex → pdflatex → pdflatex` exit 0; cả hai PDF **44 trang**,
  **43 references**, đủ 29 locators. Poppler render **88 trang**; xem toàn bộ
  contact sheet và đọc riêng sơ đồ, biểu đồ cùng bảng đổi nhãn. Không Overfull,
  undefined reference/citation, Type3, chữ ngoài trang hoặc mã nội bộ bị cấm.
  Mỗi bản có năm Underfull notice; BibTeX còn notice bài ICLR điện tử không có số trang.

[PDF đầy đủ](../../../outputs/revision/manuscript_standalone_v1/main.pdf),
[PDF submit](../../../outputs/revision/manuscript_standalone_v1/main_submit.pdf),
[ZIP Overleaf](../../../outputs/revision/manuscript_standalone_v1/overleaf.zip),
[manifest](../../../outputs/revision/manuscript_standalone_v1/manifest.json)
và [locators mới](../../../outputs/revision/manuscript_standalone_v1/pdf_anchors.json)
thuộc phiên bản này; [QA đóng gói](manuscript_standalone_checks.zip) lưu log,
ảnh render, kiểm tự động và công cụ biên tập/kiểm tra. Các gói nguồn/PDF/receipt
cũ giữ nguyên; tên phương pháp hiển thị được ánh xạ trong manifest tới danh tính
thực nghiệm cũ để truy nguyên, không đổi tên runtime hoặc raw records.
Đợt này chỉ sửa tài liệu: không chạy unit/E2E/leakage/compileall theo AGENTS §1.2
vì code, runtime, schema và dữ liệu nghiên cứu không đổi; không nâng trạng thái
đóng phản biện hoặc chứng nhận nhân quả/khả năng giao dịch.

## Điều chỉnh bố cục và tài liệu tham khảo của bài báo

Ngày **13/11/2026**, theo yêu cầu sửa bản hiện hành tại `paper/`:

- [x] Đổi vị trí bảng/hình sang `[!htb]` linh hoạt; bỏ ép `[H]` và ngắt trang
  cứng ở phụ lục F, bỏ ngắt trang references riêng của bản submit. Giữ rào chắn
  ở nơi đổi số phụ lục. Trang chỉ chứa float được căn đầu, không giãn khoảng giữa
  các bảng; hai bảng bốn panel dùng lưới 2×2, không thu nhỏ phông bảng.
- [x] Bổ sung citation thực tế cho indicator/chart, IC, Sharpe/Sortino,
  walk-forward, BA/MCC, HAC, Holm, dependent bootstrap, HMM, teacher Bayes/EM,
  Bayesian bootstrap và các công cụ được sử dụng. Danh mục được dẫn tăng từ
  **21 lên 43 nguồn**, không dùng `nocite{*}` để tăng số lượng.
- [x] Reference **[6] Tsantekidis et al.** giữ đúng bài/DOI, đủ sáu tác giả;
  thay URL IEEE `/metrics` lỗi bằng bản ghi Đại học Aarhus đã kiểm HTTP **200**.
  Bật ngắt URL ở dấu gạch nối để các địa chỉ dài không tràn lề.
- [x] Build mới hai cây độc lập bằng `pdflatex → bibtex → pdflatex → pdflatex`,
  tám lệnh exit 0; cả hai bản **50 trang**. Poppler render đủ **100 trang**;
  xem toàn bộ bố cục qua contact sheet và xem riêng bảng lưới, trang references,
  phụ lục của bản submit. Không Overfull, undefined reference/citation, chữ ngoài
  trang hoặc Type3. Mỗi bản còn tám Underfull notice; BibTeX giữ một notice
  thiếu số trang của bài ICLR điện tử Xie et al., không tự tạo số trang giả.
- [x] Đối soát 64 nguồn trước sửa với source ZIP F05; giữ nguyên **32 panel
  tabular, 27 khối equation/align, 22 asset hình/sơ đồ** và hai bộ macro số liệu.
  Các kết quả, raw, receipt, source ZIP và PDF lịch sử không bị ghi đè.

[Bản đầy đủ](../../../outputs/revision/manuscript_layout_references_v1/main.pdf),
[bản submit](../../../outputs/revision/manuscript_layout_references_v1/main_submit.pdf)
và [ZIP nguồn Overleaf](../../../outputs/revision/manuscript_layout_references_v1/overleaf.zip)
thuộc [manifest mới](../../../outputs/revision/manuscript_layout_references_v1/manifest.json).
[QA đóng gói](manuscript_layout_references_checks.zip) lưu nguồn công cụ kiểm,
log, aux/bibliography, kết quả đối soát và PNG. Source ZIP F05 và crosswalk
reviewer F05 vẫn là bằng chứng lịch sử; vị trí trang mới nằm trong
[pdf anchors](../../../outputs/revision/manuscript_layout_references_v1/pdf_anchors.json),
không nhận các số trang F05 là vị trí hiện tại. Bản này chỉ sửa tài liệu và
trình bày, không chạy unit/E2E/leakage/compileall theo AGENTS §1.2 vì không đổi
code, runtime, schema hoặc dữ liệu nghiên cứu. Không chạy lại inference,
scoring hay thống kê và không nâng trạng thái đóng các phản biện khoa học.

## Công việc cuối cho bài báo và giao diện

[Kế hoạch cuối](final_paper_ui_plan.md) được lập ngày **12/11/2026** sau audit
nguồn `develop:d16630e9`. Checklist này và cột checklist tại mục 6 của plan
được cập nhật đồng bộ trong cùng commit; kết quả kiểm tra ghi tại đây. F01–F05
cụ thể hóa U10, F06–F12 là yêu cầu nâng ứng dụng sau đó. Giữ nguyên các section
chính và A–F của bài, đưa mô tả/kết quả mở rộng chính vào thân bài và chi tiết
vào appendix. Giữ Flask và bốn trang trong `templates/`; backend dùng registry/
adapter chung để lựa chọn thực sự chạy đúng phiên bản, không chỉ đổi nhãn UI.

**Bước tiếp theo: F11**, nghiệm thu tích hợp và kiểm trình duyệt đúng phạm vi.
F00–F05 và U10 hoàn tất trong phạm vi bàn giao bản thảo nội bộ; F06 đã chốt
contract ứng dụng; F07 có viewer U09 offline, F08 có provider/runner/API job
as-of; F09 đã nối form/kết quả, chọn/chạy sáu bản và so sánh cùng snapshot.
F10 đã nối backtest nhiều bản và trang thực nghiệm, filter/evaluator/export
cùng support; adapter Full/No-Alpha riêng. F11–F12 chưa bắt đầu.
**0/18 comment được chứng nhận đóng**;
không suy quyền công bố/nộp bài.
Đợt bổ sung cột checklist trước F01 ngày 12/11/2026 chỉ đổi plan và README;
kiểm diff, liên kết và trạng thái khớp nhau, không chạy suite hoặc API theo
AGENTS §1.2 vì không đổi code/runtime/input hay bằng chứng.

- [x] F00 — Audit paper/reviewer, bảng/hình, registry/runner/API/templates; lập kế hoạch cuối, chưa triển khai code hoặc sửa bản thảo.
- [x] F01 — Chốt mapping hai study, snapshot 810 nguồn nguyên byte; historical restore và cold replay U09 PASS.
- [x] F02 — Generator và release U09 riêng: 26 artifact/798 ô có provenance, 16 test và cold render nguyên byte PASS.
- [x] F03 — Cập nhật tám section và appendix A–F; giữ metadata/cấu trúc, build hai PDF 50 trang và kiểm trực quan đủ 100 trang PASS.
- [x] F04 — Cập nhật bốn sơ đồ/caption, figure hai baseline và vị trí bảng; hai PDF 51/50 trang, kiểm đủ 101 trang PASS.
- [x] F05 — Đồng bộ 87 yêu cầu/matrix/response, chốt numbering/locators, hai PDF 51/50 trang và release nội bộ; U10 hoàn tất, 0/18 comment được chứng nhận đóng.
- [x] F06 — Contract/registry/config serving v1 riêng, sáu lựa chọn chính/hai nâng cao, API metadata/preflight, job/result identity và 33 test đúng phạm vi PASS.
- [x] F07 — Reader U09 kiểm hash/receipt, viewer nhiều bản/hai baseline, plot/export và legacy; 46 Python + 6 DOM PASS, browser trực quan chờ F11 do host/approval.
- [x] F08 — Resource188/chín mã/58 phiên 1d/VI, sáu bản qua runner paired chung, owner/config isolation, retry/quota/UNKNOWN/stop/resume; 105 test/compile18 PASS, HTTP fixture, chưa smoke hosted mới.
- [x] F09 — Form/kết quả chọn/chạy sáu bản qua serving, paired snapshot, preflight, raw/final/CASH/coverage/context; UI VI/EN, CSS mobile; 108 Python + 18 DOM, compile5/JS7 PASS, browser visual chờ F11.
- [x] F10 — Backtest/experiments nhiều bản, evaluator U09 và daily NAV/cycle returns, filter/common support, progress/stop/resume/JSON/CSV; Full/No-Alpha riêng. 156 Python + 31 DOM, compile13/JS7 PASS; browser visual chờ F11.
- [ ] F11 — Kiểm thử tích hợp/leakage/caller đúng phạm vi và kiểm trình duyệt; smoke live có phạm vi nếu cần.
- [ ] F12 — Release ứng dụng, assets/runbook và bàn giao trên develop; không tự deploy/submit.

Tại mốc audit F00, paper/revision cùng blob fix và bài chưa chứa U09; F03 đã
bổ sung nội dung U09 vào bản thảo hiện hành, giữ nguyên snapshot lịch sử. Web analyze
chưa dispatch variant, backtest chặn bản khác native, `/experiments` chỉ nhận
`identity.json` + `result.json` nên chưa thấy U09 (`results.json`). Cả bốn template,
registry và web entrypoint thuộc nguồn đã khóa: sửa UI cần release mới và giữ
đường tái lập historical. U09 không chứng minh mở rộng vượt native, native
row-wise causal vẫn FAIL, whole-system NOT_CERTIFIED; reviewer không được tự
đánh dấu đóng khi mới bổ sung trình bày.

Kiểm tra đợt plan: **729/729 source bindings U09 khớp byte/hash**, SHA256 hai
gói U08/U09 khớp receipt, paper50/revision28 không đổi so fix. Chỉ sửa Markdown
kế hoạch/checklist; kiểm diff và **101 liên kết/anchor local** trong ba tài liệu
PASS. Không chạy compileall/unit/
E2E/leakage hoặc cold analysis lại theo AGENTS §1.2 vì code, runtime, inputs,
schema và evidence không đổi. Kết quả PASS cũ chỉ được viện dẫn, không ghi là
đã chạy lại. **0 API mới, 0 lượt chạy full, 0 refit** trong audit này.

### F01 — Nguồn và historical replay

Hoàn tất ngày **12/11/2026**, nhánh `docs/final-evidence-map`, từ develop
`384725a66fec074700963fac67c358b28b842092`. [Mapping và lệnh restore](final_evidence_map.md)
tách study gốc Full/Base, numeric controls và hai panel chín đơn vị khỏi
study U08/U09 một upstream/ba Decision repeat; xác định nguồn cho từng nhóm
bảng/hình/macros và nền bản thảo `author_preserved_v1`. Không trộn response,
N hoặc phương pháp thống kê giữa hai study.

[Snapshot nguồn](final_evidence_snapshot.zip): **93.154.448 byte**, SHA256
`80fed8c9a1c265098a394bfc40f13d7f0266c1e05abdb142fba01d873cb8b8b5`.
ZIP giữ 810 file nguồn cùng manifest, gồm đủ 729 pin U09, paper50/revision28
và cây app/cấu hình; các tập giao nhau. Có cả file ignored mà pin yêu cầu.
Proof `evidence/f01_restore_smoke.json` và full `evidence/u09_cold_verify.json`
được lưu trong ZIP này, không tạo receipt rời lặp lại kết quả.

- [x] Hash/length của 810 nguồn khớp snapshot ở cả cây hiện hành và historical checkout biệt lập tại commit trên; 50 file paper khớp nguyên byte `author_preserved_v1/sources.zip`.
- [x] Restore đúng 286 asset ignored từ gói U06 v2 và 16 file U09 từ gói đã seal (15 artifact + receipt); giữ namespace/`results.json`, không ghi đè bằng kết quả phân tích mới.
- [x] Consumer gói U09 PASS: 24 member, 729 source pin, 102 điểm và 2.448 forecast slot; Python3.13.5/107 package đúng manifest được cold consumer đối soát.
- [x] **Đã chạy mới** cold replay trong tiến trình `-I` trên checkout historical: `PASS_U09_COLD_REPLAY`, cả 15 artifact nguyên byte; mạng ngoài và sáu constructor key/client/provider bị chặn.
- [x] **Đã chạy mới** verifier U01 trên cả hai checkout: 21.383 artifact, 21.948 đường dẫn được giải trình (21.947 giữ, một workflow đã nghỉ); 20 gói W12 và 30 archive cũ không đổi SHA256/length.
- [x] Kiểm bàn giao: ZIP 814 member không trùng/hỏng, đủ source/proof đúng hash; 134 liên kết/anchor local trong năm tài liệu PASS, checklist F01/F02 đồng bộ.

F01 chỉ bổ sung tài liệu vận hành và snapshot/proof. Không sửa code, test,
runtime, schema, inputs, paper, template hoặc expected hashes/receipt cũ;
không cần resolver mới. Không chạy unit/E2E/leakage suite hoặc compileall
theo AGENTS §1.2; smoke restore/hash/cold analysis ở trên bao phủ đúng yêu cầu
F01. **0 API mới, 0 full inference, 0 training/refit**. Gate U03/U08/U09 giữ
phạm vi cũ; native row-wise causal **FAIL**, whole-system **NOT_CERTIFIED**.
Kết thúc F01, F02 chưa bắt đầu; U10 vẫn chờ F02–F05.

### F02 — Generator và artifact bài báo U09

Hoàn tất ngày **12/11/2026**, nhánh `feat/manuscript-unified-results`, từ develop
`5d1b31b2`; commit generator **`3ac6a28a`**. [Generator](../../../core/manuscript_u09)
đọc trực tiếp các ZIP U09/U08 đã pin và acceptance, đối soát member/receipt/
identity, viện dẫn source gate lịch sử F01. Không chạy lại evaluator,
bootstrap, provider hoặc refit. Consumer historical U09 và generator Full/Base
cũ giữ nguyên; verifier artifact trình bày này không chứng nhận code serving mới.

[Manifest release](../../../outputs/revision/u09_manuscript_assets_v1/manifest.json)
khóa input, chín file nguồn/test/attributes, runtime render/font và từng output.
**26 artifact**, trong đó **14 file** được cài vào
[`paper/generated/u09/`](../../../paper/generated/u09); nội dung section và hai
entrypoint LaTeX chưa đổi. Release gồm:

- Bảng scope, so sánh chính đủ mười vai trò/control, class-aware metrics, economics, ba Decision repeat, đủ 20 contrast và ba dependency bridge.
- Bảng CORE4/OOD5 có raw/bypass và effective K được ghi; giữ NA khi K thiếu. Ghi đúng 79/102 điểm thiếu sentiment; không đổi missing thành neutral.
- L1/L2/L3 cho cả return và BA; CORE4 riêng; companions nguyên byte theo symbol/fold/repeat/account và toàn bộ leave-one-out/sensitivity đã khóa.
- **109 macro** prefix `Unified` trong `summary_numbers.tex`, namespace dành riêng U09; macro Full/Base cũ không đổi. Return/BA là %, contrasts là đpt, phí/slippage hiển thị kVND; scale/rounding được ghi riêng.
- Figure SVG/PNG tiếng Anh cho hai baseline từ đúng mười return contrasts, giữ nguyên figure nguồn U09. **798 ô số** trong `numeric_cells.json` nối literal/pointer/package/member tới output, đơn vị, scale và giá trị render; support đếm từ shared/prediction frozen có lineage riêng.

[QA/log đúng phạm vi](unified_manuscript_checks.zip): **5.226 byte**, SHA256
`b1b00e3d26e724f2d164286196f4cc5b6f68d5053f797162c9c1c3ac5fe84b6c`.
Gói bảy member giữ log test, compile, build/cold verify, preservation và source/
runtime bindings; không tạo thêm receipt rời.

- [x] **16 test trực tiếp PASS**, không skip/error: nguồn/schema, hai baseline/family, đủ support, đơn vị/null, lineage, macro hợp lệ/tách namespace, không ghi đè, phát hiện source/output/install/thừa file bị sửa và render xác định.
- [x] Compile đúng **sáu file Python mới**, không compileall toàn codebase.
- [x] CLI `-I` ở tiến trình mới: **`PASS_U09_MANUSCRIPT_COLD_REPLAY`**, khớp nguyên byte cả 26 artifact, gồm SVG/PNG; network bị chặn.
- [x] Kiểm trực quan figure hai panel: nhãn, đơn vị, point/band đầy đủ, không cắt/tràn; ảnh preview khớp byte release. Build/render toàn bộ hai bản thảo và QA layout cuối thuộc F03–F05.
- [x] Đối soát F01 sau sinh: **810 nguồn** (gồm paper50/revision28 và 729 pin U09), **20 gói W12 + 30 archive cũ** nguyên byte. Chỉ thêm namespace mới, không sửa công thức kinh tế hoặc dữ liệu đã seal.
- [x] Kiểm bàn giao: bảy member QA đúng hash, chín binding source khớp Git commit generator, 114 liên kết/anchor local trong bốn tài liệu PASS; checklist F02/F03 đồng bộ.

Kiểm lại release đã có, không ghi đè:

```powershell
py -3.13 -I -X utf8 scripts/manuscript_u09/run.py verify
```

`build` chỉ dùng một lần khi release và `paper/generated/u09` chưa tồn tại;
`--artifact-only --release outputs/revision/u09_manuscript_assets_<tên-mới>`
cho phép tạo bản riêng không cài vào paper. F03 sẽ dùng
`\input{generated/u09/summary_numbers.tex}` và các bảng theo mapping, chưa thực
hiện trong F02. Không chạy lại `tests/unified_analysis/test_analysis.py`,
`tests/test_revision_manuscript.py`, E2E hoặc leakage suite vì nguồn/caller/
contracts cũ không đổi; 16 test mới và cold CLI bao phủ đường export mới theo
AGENTS §1.2. **0 API mới, 0 inference/refit/ước lượng lại metrics**. Native
row-wise causal vẫn **FAIL**, whole-system **NOT_CERTIFIED**; U10 chờ F03–F05.

### F03 — Nội dung bản thảo hai nghiên cứu

Hoàn tất ngày **12/11/2026**, nhánh `docs/manuscript-extensions`, từ develop
`4c091408`; commit nguồn **`a9912c5c`**. Cập nhật đúng mapping §3 của kế hoạch:
phần mở rộng ở thân bài, chi tiết prompt/schema/config/teacher/utility và kết
quả đầy đủ tại A–F. Hai nghiên cứu giữ response, N, seed và thống kê riêng.
Native/Common được phân biệt; v1 cải thiện so Common nhưng chưa chứng minh
vượt Native, mọi vai trò research có mean return âm. Báo raw/final, bypass,
CORE4/OOD5, thiếu sentiment và bridge chưa thay được ablation còn thiếu.

[Manifest bản thảo nội dung](../../../outputs/revision/manuscript_content_v1/manifest.json)
khóa **64 file nguồn**, input, runtime build và PDF; trạng thái
`CONTENT_READY_FOR_F04_NOT_FINAL_PUBLICATION_RELEASE`. [Source archive](../../../outputs/revision/manuscript_content_v1/sources.zip)
giữ nguyên byte 64 nguồn cùng manifest. Đây là mốc nội dung cho F04, chưa phải
release xuất bản F05 hoặc hoàn tất U10.

- [x] **14 file paper thay đổi, 50 file giữ nguyên**; giữ title/tác giả/ORCID/affiliation/CRediT/funding/keywords, tám section và tên/thứ tự subsection/A–F. Appendix D và acknowledgments không đổi; 24 khối equation/align gốc giữ nội dung sau chuẩn hóa LF, thêm hai khối cho snapshot/utility.
- [x] Abstract hai bản giống nhau, **203 từ**; năm highlights đều ≤85 ký tự. **29 macro U09 được dùng** có định nghĩa, label/ref/cite key hợp lệ; không tính lại số trong LaTeX. Bảng gốc, macros Full/Base và 14 file generated U09 nguyên byte.
- [x] Đọc ba nguồn nghiên cứu chính trước khi thêm citation: [Xie et al., ICLR 2022](https://arxiv.org/abs/2111.02080v6), [Rubin et al., NAACL 2022](https://aclanthology.org/2022.naacl-main.191/), [Hamilton, author draft 18/05/2005](https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf). Giữ 40 mục BibTeX cũ, thêm ba mục đúng phiên bản; audit URL/hash/phạm vi hỗ trợ lưu trong QA. Không nhận lý thuyết Bayesian là bảo đảm cho LLM tài chính.
- [x] **Build mới cả hai entrypoint** trong hai cây tạm biệt lập: `pdflatex → bibtex → pdflatex → pdflatex`, đủ tám lệnh exit 0. [Bản đầy đủ](../../../outputs/revision/manuscript_content_v1/main.pdf) **50 trang**; [bản submit](../../../outputs/revision/manuscript_content_v1/main_submit.pdf) **50 trang**. Poppler render đủ **100 trang** và kiểm trực quan từng trang; không tràn khung, thiếu glyph, Type3, chữ ngoài trang, undefined ref/citation hoặc LaTeX warning. Mỗi bản còn **bảy Underfull spacing notice**, đã xem và không gây cắt/mất chữ.
- [x] Đối soát **26 artifact F02, chín binding nguồn generator, input và 20 gói W12 + 30 archive cũ** nguyên byte/hash. Không đổi code/test/schema/runtime/input nghiên cứu; không chạy compileall/unit/E2E/leakage theo AGENTS §1.2 vì chỉ đổi tài liệu/LaTeX. Build/render/hash là kiểm mới, không nhận đã chạy lại gate runtime cũ.
- [x] QA **123 member**, gồm 100 PNG từng trang, tám command log, hai log LaTeX cuối, source/content/ref/render/visual checks và manifest; source ZIP 65 member. Kiểm hash mọi member, 64 nguồn khớp commit, **120 liên kết/anchor local** trong bốn tài liệu và checklist đồng bộ PASS.

[Gói QA F03](manuscript_content_checks.zip): **17.791.977 byte**, SHA256
`1eab72eb5591c98dd9a906a229328f23fd7b248f64738c41dc86cf5672809170`.
Manifest release SHA256
`3de4994c93c76a810351a8101ff612b8b7736c4cc9c2bf27ea71ea5beb2ecb31`.
Không phân phối lại PDF nguồn nghiên cứu bên ngoài trong QA; chỉ lưu audit.

**0 LLM/market API mới, 0 inference, 0 training/refit hoặc ước lượng lại số liệu**.
Các sơ đồ cũ được ghi rõ là đường native; F04 còn cập nhật sơ đồ/caption/figure
và layout cuối. F05 còn đối soát 87 tiểu mục reviewer, chốt locators và release;
không tự đóng reviewer. Native row-wise causal vẫn **FAIL**, whole-system
**NOT_CERTIFIED**. U10 chờ F04–F05; không push, deploy hoặc submit.

### F04 — Sơ đồ, caption và layout bản thảo

Hoàn tất ngày **12/11/2026**, nhánh `docs/manuscript-figures`, từ develop
`9439e54e`; commit nguồn **`da8d1db2`**. Cập nhật bốn sơ đồ TikZ hiện có,
giữ năm vai trò và khung tám section/A–F:

- Pipeline chung: I/P/T một lần theo trình tự, immutable parent, deep-copy, hai projection native/common, dependency và raw → policy → final action → ledger.
- Alpha: tách native diagnostics khỏi causal-common frozen selector và đường sentiment; giữ native causal FAIL và không vẽ sentiment thành factor-score input.
- Decision: dependency cùng repeat, prior bypass về Common, fact assertions, MT về anchor khi thiếu support và veto Q10ΔU; lỗi kỹ thuật giữ retry/checkpoint.
- Walk-forward: bank exit trước cutoff, resource/fits đóng băng, loại toàn bộ evaluation IDs khỏi context, ba Decision repeat chung upstream, outcome barrier và Open(t+1)→Close(t+3).

Algorithm 1 đã được cập nhật ở F03; F04 đối chiếu lại với bốn sơ đồ, giữ nguyên
byte thuật toán và công thức. Caption lịch nói rõ cùng calendar nhưng khác
responses. PNG lịch khớp 12 ngày/102 điểm/sáu ô BHN được dùng; cặp chart CMG và
provenance gốc được giữ. Figure 7 dùng **nguyên PNG F02**, hiển thị hai panel
phóng lớn xếp dọc bằng viewport LaTeX; giữ đủ nhãn, trục, point/band, hai scale
và mọi kết quả âm. Caption ghi đơn vị đpt, joint family 20 contrasts và giới
hạn band mô tả. Không tính lại metrics hoặc sinh lại figure dữ liệu.

Chỉ đổi placement cục bộ bên ngoài hai bảng generated scope/comparison:
bảng phạm vi ở trước sơ đồ walk-forward, bảng so sánh trước figure kết quả,
tránh trôi sang phần khác. Không đổi byte bất kỳ bảng/macros đã khóa.

[Manifest bản thảo sơ đồ](../../../outputs/revision/manuscript_figures_v1/manifest.json)
khóa nguồn, input, runtime, PDF và locators của build này; trạng thái
`FIGURES_READY_FOR_F05_NOT_FINAL_PUBLICATION_RELEASE`.
[Source archive](../../../outputs/revision/manuscript_figures_v1/sources.zip)
giữ **64 nguồn + manifest**, không ghi đè bản nội dung F03.

- [x] **Bảy file paper thay đổi, 57 file nguyên byte**; metadata/hai entrypoint, abstract/highlights, appendix, references và đủ **27 khối equation/align** giữ nguyên. Algorithm 1 không đổi.
- [x] Build mới hai cây biệt lập, đủ tám lệnh `pdflatex → bibtex → pdflatex → pdflatex` exit 0. [Bản đầy đủ](../../../outputs/revision/manuscript_figures_v1/main.pdf) **51 trang**, [bản submit](../../../outputs/revision/manuscript_figures_v1/main_submit.pdf) **50 trang**; render Poppler và kiểm trực quan đủ **101 trang**.
- [x] Mỗi PDF có **bảy figure, 21 table và một algorithm**; đối soát **29 locators** với caption trên trang vật lý. Kiểm hình học **38 khung TikZ mỗi bản**: không chồng khung hoặc chữ vượt node. Không Overfull, undefined ref/cite, thiếu glyph, Type3, chữ ngoài trang hoặc LaTeX warning. Mỗi PDF giữ **bảy Underfull spacing notice**, đã xem và không mất nội dung.
- [x] Đối soát **26 artifact F02**, nguồn generator/input, release/QA F03, **50 archive/gói lịch sử** và **732 binding snapshot ngoài paper/revision** nguyên byte/hash. Không sửa source pins/receipt hoặc kết quả đã seal.
- [x] Gói QA **130 member**, gồm **101 PNG**, tám command log, log/aux của hai bản, source/render/visual/geometry/calendar checks, locators, công cụ kiểm và manifest. Source ZIP 65 member; 64 nguồn khớp Git commit. Kiểm mọi member, **126 liên kết/anchor local** trong bốn tài liệu, diff và checklist đồng bộ PASS.

[QA F04](manuscript_figures_checks.zip): **18.332.010 byte**, SHA256
`247e13f0c0ddc7fd82b3f8955de4bf5edd86aa66c65a04fe4f52ffc10bb07961`.
Manifest release SHA256
`048c7a2e88e58a476878e0347c68be75baac78590dba0fd17c80db47c2d75ee1`.
Trình tự dựng và phiên bản công cụ nằm trong `build_commands.json` và
`build_runtime.json` của QA; nguồn PDF lấy từ source ZIP nêu trên.

F04 chỉ sửa LaTeX/tài liệu, không đổi code/test/schema/runtime/input nghiên
cứu; không chạy compileall/unit/E2E/leakage theo AGENTS §1.2. Build/render,
hình học và hash là kiểm mới, không nhận chạy lại gate nghiên cứu cũ.
**0 LLM/market API mới, 0 inference/training/refit hoặc ước lượng lại metrics**.
F05 còn đối soát 87 tiểu mục reviewer, xác nhận locators ở bản cuối và đóng
gói release xuất bản; **U10 chưa hoàn tất**. Native row-wise causal vẫn
**FAIL**, whole-system **NOT_CERTIFIED**; không push, deploy hoặc submit.

### F05 — Reviewer, locators và bàn giao bản thảo cuối

Hoàn tất ngày **13/11/2026**, nhánh `docs/manuscript-final-release`, từ develop
`22ceec41`; commit nguồn khóa cuối **`08d02162`**. **U10 hoàn tất theo phạm vi F01–F05:**
bản thảo khớp bằng chứng và đủ gói bàn giao nội bộ. Không đồng nghĩa reviewer
đã chấp thuận, causal gate toàn hệ PASS hoặc có quyền public/submit.

[Response hiện hành](../../../revision/response_to_reviewers.md),
[matrix hiện hành](../../../revision/reviewer_matrix.csv) và
[crosswalk khóa phiên bản](../../../outputs/revision/manuscript_unified_final_v1/response_map.json)
cùng đủ **87 yêu cầu/18 comment**. Matrix 43 dòng cũ có trạng thái/locators từ
các lượt khác đã được thay bằng 87 mã yêu cầu; nguyên byte bốn tài liệu reviewer
trước F05 được giữ trong QA. Mỗi yêu cầu có giải trình, trạng thái riêng,
bằng chứng/hash, source anchor/dòng hiện tại, PDF/hash/trang vật lý và phần
còn thiếu. Không gắn locator author vào bản submit khi block không được render.

| Trạng thái theo từng yêu cầu | Số mục | Ý nghĩa |
| --- | ---: | --- |
| `documented_with_limits` | 43 | Có giải trình/bằng chứng trong phạm vi nêu rõ; không phải reviewer acceptance |
| `partial_missing_scientific_evidence` | 22 | Còn thiếu thực nghiệm/validation khoa học |
| `unresolved_historical_identity` | 14 | Chưa xác minh được nguồn/định danh lịch sử |
| `pending_rights_or_author_route` | 5 | Còn thiếu quyền, liên hệ hoặc route/hồ sơ tác giả |
| `partial_editorial_request` | 3 | Yêu cầu biên tập còn một phần, giữ title/khung theo chỉ dẫn |

**0/18 comment được chứng nhận đóng.** Giữ rõ native causal FAIL, whole-system
NOT_CERTIFIED, thiếu financial-news/PIT/human-visual/prospective/factorial
validation, unknown legacy duplicates/references, PID/quyền và route/contact.
Đã cập nhật đầu mối revision README/runbook để không còn lấy nhãn R1–R4 cũ làm
nghiệm thu hiện tại. Mọi gói/receipt lịch sử giữ nguyên.

[Manifest cuối](../../../outputs/revision/manuscript_unified_final_v1/manifest.json)
khóa **68 nguồn** (64 paper + bốn tài liệu reviewer), **74 input bindings** và
từng output; trạng thái `FINAL_LOCAL_MANUSCRIPT_HANDOFF_U10_COMPLETE`.
[Source ZIP](../../../outputs/revision/manuscript_unified_final_v1/sources.zip)
có **69 member** kể cả manifest. [Companions](../../../outputs/revision/manuscript_unified_final_v1/scientific_companions.zip)
giữ **40 artifact nguyên byte + manifest**: 14 S1–S4 của study gốc và 26 artifact
F02/U09 trong hai namespace riêng. S1 classification có 144 dòng tổng cộng,
trong đó đúng 81 dòng theo mã; giữ cả pooled/block. Không gộp các study hoặc
chạy lại analysis để tạo gói. [Runbook](../../../revision/archive_runbook.md)
phân biệt current handoff với historical checkout/overlay.

- [x] Build mới hai cây MiKTeX biệt lập, đủ tám lệnh exit 0. [Bản đầy đủ](../../../outputs/revision/manuscript_unified_final_v1/main.pdf) **51 trang**, [bản submit](../../../outputs/revision/manuscript_unified_final_v1/main_submit.pdf) **50 trang**, gồm highlights. Ngày hiển thị manuscript giữ **12/11/2026** theo F04; ngày release/response là **13/11/2026**.
- [x] Poppler render đủ **101 trang**; 99 PNG khớp nguyên byte các trang đã kiểm trực quan ở F04, hai trang availability thay đổi đã xem trực tiếp. **Bảy figure/21 table/một algorithm và 29 locators mỗi PDF**; 38 node TikZ/bản không chồng khung hoặc chữ vượt node. Không Overfull, undefined ref/cite, thiếu glyph, Type3, chữ ngoài trang hoặc LaTeX warning. **Tám Underfull spacing notice mỗi PDF** được xem và không mất nội dung.
- [x] Reference ledger khóa **43 BibTeX entries/21 cited keys**, số/trang/bbox reference thực tế ở cả hai PDF. Deng giữ uncited; các historical [14]/[21]/[22]/[23] vẫn chưa định danh, không ánh xạ bằng numbering hiện hành. Audit ba nguồn primary F03 được viện dẫn đúng phiên bản, không nhận tra cứu mới.
- [x] Chỉ availability đổi trong paper; **63/64 nguồn paper** nguyên byte, đủ **27 equation/align**, metadata/title/authors/ORCID/CRediT/funding, abstract/highlights, bảng/hình/macros không đổi. **798 ô số F02, 26 artifact**, 732 binding snapshot ngoài paper/revision và **50 gói/archive lịch sử** khớp. Source/evidence/anchor/hash của đủ 87 yêu cầu và 64 nguồn evidence gốc đã đối soát.
- [x] Gói QA **145 member**, gồm 101 PNG, tám command log, log/aux/bibliography/runtime, source/reviewer/numbering/geometry/companion/visual checks và bốn tài liệu trước F05. Kiểm mọi member, source ZIP/companion ZIP, nguồn khớp commit, **700 liên kết/anchor local** trong chín tài liệu, diff và checklist đồng bộ PASS.

[QA cuối](manuscript_final_checks.zip): **18.428.304 byte**, SHA256
`f0505aa9ed800d8562ef3af1c88496d4ca3ebd62160b9163485ca1805d2583e0`.
Manifest release SHA256
`8e5ce2a4ca6f3a52945047cb8e1e1e99e8c00dfcd959a6fc6cdadcd701013de9`.
[Rights](../../../outputs/revision/manuscript_unified_final_v1/rights.json)
giữ `public_release_authorized=false`, `pid=null`, `editorial_acceptance_certified=false`.

F05 chỉ đổi LaTeX/tài liệu và metadata đối soát reviewer; không đổi code/test,
schema chạy, runtime hoặc input nghiên cứu. Theo AGENTS §1.2 không chạy lại
compileall/unit/E2E/leakage; kiểm hash nguồn/runtime/receipt bảo toàn phạm vi
các gate cũ, không nâng native/whole-system causal. Build/render/hash/locators
là kiểm mới. **0 API LLM/thị trường, 0 inference/scoring/fit/bootstrap mới**;
không push, upload, publish, liên hệ bên ngoài, submit hoặc deploy.
Tại thời điểm kết thúc F05, F06–F12 ứng dụng chưa bắt đầu.

### F06 — UX, capability và contract serving

Hoàn tất ngày **13/11/2026**, nhánh `feat/variant-serving-contract` từ develop
`cb2df984`. [Contract ứng dụng](variant_serving_contract.md) chốt sáu lựa chọn
chính và hai vai trò nâng cao, native mặc định, ba khả năng đọc/phân tích/
backtest cùng mode compare và các luồng bốn màn hình theo plan §4. Mỗi lựa
chọn giữ canonical ID, dependency/fallback/profile của phương pháp hiện hữu.

- [x] Thêm registry `variant_serving_registry_v1`, contract `variant_serving_v1` và config `serving_config_v1`; registry/schema nghiên cứu cũ nguyên byte.
- [x] `GET /api/serving/v1/registry` chỉ metadata; `POST /api/serving/v1/preflight` kiểm body đóng và trả request hash/topo plan/blocker, không tạo job hoặc inference.
- [x] Phân biệt artifact lịch sử và inference mới; miền ứng viên 1d/VI, chưa công bố mã/ngày live. Preflight báo runner/support/resources thiếu; EN chưa nghiệm thu có blocker riêng. Không mở hàng loạt bằng `hosted_release` của research cũ.
- [x] Request snapshot đủ sáu agent model/provider/options, mã/ngày/ngôn ngữ/repeat/variant; config server khóa source/provider/calendar/support/resource/prompt versions. Job bất biến có UUID/owner/config/snapshot/identity/cache hashes; cache gồm owner scope, không chứa API key.
- [x] Result envelope kiểm raw/final, LONG/SHORT→LONG/CASH, fallback đúng chuỗi, dependency/repeat coverage, units, null/NA reason; partial/failed/UNKNOWN giữ slot đã xong, UNKNOWN không retry mù. Chưa có state machine hoặc start/resume/stop/export mới ở F06.
- [x] **33 test PASS**: 15 `test_variant_serving.py`, 15 `test_unified_experiment.py`, 3 `test_web_json_serialization.py`. Bao phủ validation/security boundary mới, identity/isolation, coverage/error và caller web/CLI/evaluator cũ. `py_compile` đúng **5 file Python** thay đổi PASS, runtime **3.13.5**.
- [x] Đối soát **20 gói W12 + 30 archive lịch sử**, **11 file release F05 + 68 nguồn manuscript** nguyên byte. **728/729** source pins U09 còn khớp HEAD; chỉ `web_interface.py` thêm hai dòng đăng ký blueprint. Snapshot F01 vẫn phục hồi đủ **729/729** pin; không sửa expected hash hoặc receipt.

QA gọn **10 member** gồm log test, integrity/link checks (**142 liên kết/anchor
local và checklist đồng bộ PASS**), command/source hashes và script đối soát
tại [variant_serving_checks.zip](variant_serving_checks.zip).
Chỉ chọn test contract và caller bị ảnh hưởng theo AGENTS §1.2; không chạy
full unit/E2E/compileall hoặc cold replay study. Không đổi đường dữ liệu/PIT/
retrieval nên không chạy lại leakage suite; test shared/future-poison và
forecast barrier có trong hồi quy experiment đã PASS. Native row-wise causal
vẫn FAIL, whole-system NOT_CERTIFIED; không nâng gate khoa học từ test serving.
**0 API LLM/thị trường, 0 refit**, bốn template và hành vi endpoint native cũ
giữ nguyên. F07 triển khai reader U09; F08 mới grant runner/provider, F09/F10
mới nối các màn hình chạy. Tại mốc F06, F07–F12 chưa hoàn tất; không push/deploy/submit.

### F07 — Viewer U09 và so sánh offline

Hoàn tất phạm vi triển khai/kiểm chức năng ngày **13/11/2026**, nhánh
`feat/research-results-viewer` từ develop `a5e30ab0`. `/experiments` mặc định
**U09 · Research102**, phân biệt bằng chứng bài báo và replay legacy. Giữ
endpoint/schema/evaluator legacy, không đổi `no_alpha` thành common hoặc ghép
run khác nhau thành paired contrast. Legacy vẫn kiểm source/runtime cũ;
run có pin khác HEAD cần checkout historical như F01.

- [x] `core/research_results.py` kiểm SHA256 gói U09, inventory/member/receipt và identity `results.json`. Không import Python từ ZIP, không gọi cold evaluator/provider/LLM; cache theo bytes, không tin mtime. Support companion F02 có hash riêng, giữ missing sentiment **79/102**.
- [x] API `/api/research-results/runs`, `/<run_id>`, `/export`, `/artifacts/<name>` có whitelist run/table/artifact, filter/phân trang đóng, lỗi an toàn. PNG nguyên byte; JSON/CSV projection có units/support/provenance, CSV chặn formula chuỗi, giữ số âm.
- [x] So sánh tám vai trò/hai control nâng cao: return/BA/accuracy/MCC/F1/LONG/MDD/phí/slippage/turnover/bypass, policy tooltip, bridge, metrics từng repeat. Plot dùng đúng effect/band đã khóa; không tạo family/bootstrap hay suy superiority.
- [x] Mã/fold chỉ lọc chi tiết; repeat còn chọn metrics từng repeat đã seal. Summary/band luôn đủ **102 điểm, 51 tài khoản, ba repeat**. Không nhận date/cohort filter tùy ý rồi giữ band toàn study. Bốn bảng predictions/accounts/cycles/daily NAV có phân trang; BHN/fold thiếu giữ rỗng, không padding CASH.
- [x] Export lấy mọi hàng chi tiết khớp, không chỉ trang đang xem. Phân biệt `r_net` nhãn thị trường và `strategy_return`/P&L; NAV EOD từng account không cộng thành portfolio, null/NA có lý do và zero giữ zero.
- [x] UI VI/EN tách **template chính + ba partial, CSS riêng + bốn module JS**; giữ điều hướng và bảng phương pháp/profile/dependency. DOM chỉ ghi text. Abort/response guard chống response cũ đè lựa chọn mới; error/empty xóa dữ liệu/link export cũ.
- [x] **46 Python + 6 DOM/JavaScript PASS**, không skip: 13 viewer mới, 15 serving contract, 15 unified experiment, 3 web JSON. DOM kiểm số/NA, chart/export, nội dung không tin cậy, legacy, empty/error và đổi filter nhanh. Compile đúng **9 Python**, syntax **4 JS** PASS; Python **3.13.5**, Node **v24.18.0**. HTTP local app thật trả 200 U09/HTML EN/static JS đúng MIME, không coi là browser visual PASS.
- [x] **20 gói W12 + 30 archive lịch sử**, **11 file release F05 + 68 nguồn manuscript** giữ nguyên byte. HEAD khớp **726/729** source pin U09; ba file đổi có chủ đích: `templates/experiments.html`, `utils/experiment_web.py`, `web_interface.py`. Snapshot F01 khôi phục đủ **729/729**, không sửa receipt/expected pin.

Lượt đầu CLI export trả exit2 trong lúc runtime source đang được sửa giữa
replay/verify/export và có guard khóa hash; stderr lượt đầu không được lưu.
Chẩn đoán riêng và toàn nhóm khi source ổn định đã PASS, giữ guard/hash.
Receipt F06 tiếp tục là lịch sử; source serving đã đổi
được kiểm lại trong F07. [QA viewer](research_viewer_checks.zip), **13 member**,
giữ log, source hashes, integrity và **144 liên kết/checklist PASS**, cùng
giới hạn kiểm trực quan. Chạy lại
đúng phạm vi bằng unittest discover với từng pattern
`test_research_results_viewer.py`, `test_variant_serving.py`,
`test_unified_experiment.py`, `test_web_json_serialization.py`; DOM:
`node --test tests/js/research_viewer.test.mjs`.

**Browser trực quan chưa kiểm:** browser access host không khả dụng; automatic
approval review từ chối Edge: “Computer Use was not approved to use Microsoft
Edge”, không nêu thêm lý do. Desktop/mobile/keyboard/layout giữ trong gate F11.
F07 chỉ đọc outcome đã seal, không đổi inference/PIT/retrieval/kinh tế; theo
AGENTS §1.2 không chạy full unit/E2E/compileall/leakage hoặc cold replay study.
Hồi quy unified có forecast barrier/future-poison; native causal vẫn FAIL,
whole-system NOT_CERTIFIED. **0 API LLM/thị trường, 0 refit**; F08–F12 chưa
hoàn tất, không push/deploy/submit. Server QA local đã dừng.

### F08 — Provider as-of và runner bền vững

Hoàn tất ngày **13/11/2026**, nhánh `feat/variant-serving-runner` từ develop
`5fd45e2b`. [Contract và lệnh vận hành](variant_serving_contract.md#chạy-serving-as-of-từ-f08)
công bố backend riêng cho cả sáu bản chính/hai dependency, không đổi grant
U08 hoặc verifier/receipt lịch sử. **Chỉ hỗ trợ 1d/VI trên chín mã, 58 phiên
01/07–23/09/2026**, tối đa 30 point/job, repeat1–3; backtest mỗi ba phiên để
không chồng vòng vốn. Latest/intraday/EN chưa được release; UI mới chờ F09/F10.

- [x] [Resource manifest](serving_resources_v1.json) `serving_asof_q3_2026_v1`, **188 binding**, SHA256 `ec0cb010361533716604b5ea2155ea6303358aa68c30bca16ffa0151e64e704c`; giữ weights/scaler/HMM/bank frozen. `prepare_serving_resources.py --restore-assets --verify` khôi phục đúng byte asset U06 thiếu, không ghi đè khác hash; lệnh đã PASS.
- [x] Provider riêng dựng snapshot as-of, ảnh theo run/point, I→P→T/Alpha/sentiment một lần/point và deep-copy. Tái dùng adapter/prompt/retrieval/policy hiện hữu, không lookup response U09. Context freeze trước 01/07, không nhập query vào memory; news từ dated corpus có missingness, không coi thiếu/hỏng nguồn là fallback thành công.
- [x] Native giữ projection gốc; common dùng causal alpha/selector đã khóa. Không fit HMM/student/bank mới; kiểm selector có replay train/validation cũ, native Alpha giữ hành vi tính/selection vốn có trên prefix. Gate native vẫn FAIL, whole-system NOT_CERTIFIED.
- [x] API `/api/serving/v1/defaults`, preflight thực và jobs start/status/stop/resume; owner cookie ký/HttpOnly/SameSite, JSON cùng origin, key chỉ ở server. Mỗi job snapshot model/options/key scope/source/runtime/resource; config toàn cục đổi không làm hotswap job đang chạy, resume sai credential/owner bị từ chối.
- [x] Journal/intent/raw atomic/fsync, quota SQLite chung mọi serving job/key/model, headroom/reset headers, backoff/retry-after và attempt cap ba lần/slot qua restart. UNKNOWN giữ reserve, không retry mù hoặc đổi thành CASH; raw complete được replay cùng UUID. Stop theo generation không bị resume cũ xóa; checkpoint giữ slot đã xong.
- [x] Outcome provider tự kiểm barrier đủ slot/dependency/repeat và chỉ mở ở backtest; oracle chung dùng VND đổi đúng một lần, SHORT giữ CASH/P&L0. Analyze/compare để P&L null/NOT_EVALUATED. Status GET read-only không tạo model/client; raw/checksum bị sửa bị từ chối.
- [x] Đối soát **522 cửa sổ mã/ngày** (chín mã × 58 phiên): ngày query và ba phiên thực thi khớp calendar chung, **0 lệch lịch**; không dùng payoff để chọn query.
- [x] **105 test PASS**, không skip, gồm **26 mới** (17 runtime/quota, 4 API, 5 resource/provider) và **79 hồi quy**: serving15, unified15, webJSON3, recovery17, leakage **8+6+4**, tokenbudget11. Actual provider/adapter chạy query mới **MWG 02/07/2026**, đủ tám slot và **MT có raw khi eligible**, toàn HTTP fixture; OOD/BHN fallback và stop giữa vision node/resume không gọi Pattern lần hai đều PASS. Hai owner/job khác key/model không lẫn config.
- [x] Compile đúng **18 Python** thay đổi PASS, Python **3.13.5**. Giữ nguyên **20 gói W12 + 30 archive lịch sử**, **11 file release F05 + 68 nguồn manuscript**. HEAD khớp **725/729** pin U09: ba đường UI/entrypoint đã version hóa và `scripts/.gitattributes` thêm quy tắc LF cho installer mới; F01 phục hồi đủ729. Các template không đổi trong F08.

[QA runner](serving_runner_checks.zip) gồm 22 member, giữ test/runtime/source/resource/log,
integrity và checklist/**148 liên kết**. Sửa fixture OOD thiếu nhãn tín hiệu rồi chạy
lại đủ file resource PASS; lỗi đóng SQLite trên Windows đã sửa và kiểm qua
cleanup/restart. Theo AGENTS §1.2 chọn đúng caller/recovery/leakage/token paths,
không chạy full unit/E2E/compileall hoặc cold replay study. **0 LLM hosted,
0 market API mới, 0 training HMM/student/bank**; chưa smoke hosted mới hay
chứng nhận causal/live fills. F09–F12 tiếp tục, không push/deploy/submit.

### F09 — Form phân tích và kết quả chọn phiên bản

Hoàn tất phạm vi chức năng/offline ngày **13/11/2026**, nhánh
`feat/variant-analysis-ui` từ develop `943b7b61`. `/` và `/demo` mặc định
**as-of/Hệ gốc**, so sánh mặc định Hệ gốc + Bayesian v1. Nguồn realtime legacy
được chọn riêng, chỉ chạy Hệ gốc; không gửi lựa chọn mở rộng tới endpoint cũ.
Miền serving giữ nguyên F08: chín mã, 58 phiên, 1d/VI. Giao diện VI/EN tách
khỏi ngôn ngữ báo cáo; yêu cầu báo cáo EN bị preflight chặn rõ ràng.

- [x] Sáu lựa chọn chính, hai đối chứng nâng cao, ngày/mã, repeat và model/options từ server defaults; cấu hình nâng cao thu gọn, không đưa hash vào form chính. Preflight analyze/compare độc lập; đổi input/key hủy grant, response cũ không bật lại nút. POST start gửi bản request đã kiểm, không retry tự động khi chưa xác nhận được job.
- [x] `/output?serving_run=<UUID>` chỉ render shell, API owner đọc checkpoint; reload không gọi model. Poll/progress phân biệt point/slot/API attempt, có stop/resume; UNKNOWN không tự gửi lại hoặc cho resume trong UI. Lỗi đọc/sai owner xóa card/ảnh cũ; job partial giữ slot đã hoàn tất và đánh dấu slot còn thiếu, không suy CASH hoặc xếp hạng.
- [x] Sáu bản được chọn hiện cạnh nhau; dependency tự chạy nằm trong phần nâng cao. Card tách raw prediction/final prediction/LONG-CASH/effective ID/fallback-bypass; analyze/compare giữ P&L null/NOT_EVALUATED. Biểu đồ Close, ảnh Pattern/Trend và I/P/T/sentiment lấy cùng snapshot; **Alpha native và common hiển thị riêng**, không gọi giá mới. Context/trace/aux đọc từ prepare durable, không chạy retrieval/Decision lại qua GET.
- [x] Model/report/context dùng text DOM, ảnh chỉ nhận PNG base64; không chèn HTML từ output serving. ID URL phải UUID, bootstrap JSON/URL được escape; không lấy ảnh/sessionStorage legacy cho serving. Confidence giữ raw trong chi tiết, không biến thành xác suất đã hiệu chuẩn.
- [x] Tách `demo_new.html` còn khoảng 300 dòng và `output.html` thành dispatcher; partial trong `templates/analysis/`, CSS/JS trong `static/css/analysis/` và `static/js/analysis/`. CSS legacy hai trang giữ nguyên nội dung; JS output chỉ đổi bootstrap sang JSON. Handler Python native/realtime/backtest giữ nguyên AST, chỉ thêm context render và nhánh output serving. Realtime trì hoãn tải danh sách đến khi chọn nguồn, giữ kiểm trạng thái năm phút; dừng đổi nguồn khi legacy đang chạy.
- [x] **108 Python PASS**: bảy test page/API mới + 101 hồi quy (serving26, contract15, unified15, webJSON3, reader13, native parity11, leakage8+6+4). **18 DOM PASS**: 12 mới + sáu viewer U09. Có ca API thật/provider thật cho **MWG 02/07/2026**, đủ tám slot/cả sáu yêu cầu, MT eligible có raw; toàn HTTP fixture. Kiểm stale preflight/poll, double click, lỗi POST mơ hồ, wrong-owner, context, NA, UNKNOWN và legacy dispatcher.
- [x] Biên dịch đúng **năm Python** và kiểm syntax **bảy JS** thay đổi PASS. Gói QA giữ lỗi kiểm thử đầu tiên (timeout join quá ngắn và assertion nhầm metadata legacy) cùng kết quả chạy lại PASS; không sửa runtime để né test.
- [x] Đối soát **20 gói W12 + 30 archive lịch sử**, **11 output F05 + 68 nguồn manuscript**, resource manifest và QA F08 nguyên byte. Worktree khớp **723/729** pin U09: sáu đường version hóa gồm bốn đường đã đổi đến F08 và hai template mới; F01 vẫn phục hồi đủ729. Không ký lại receipt hoặc nâng native causal FAIL/whole-system NOT_CERTIFIED.

[QA giao diện](analysis_ui_checks.zip) gồm **26 member**, giữ nguồn/runtime/test/log/syntax/integrity
và kiểm **149 liên kết**/checklist. Theo AGENTS §1.2 chỉ chạy các caller UI/result/native,
serving và leakage liên quan; không chạy full unit/E2E/compileall/cold study.
**0 hosted LLM, 0 API thị trường, 0 training HMM/student/bank mới**; native Alpha
giữ hành vi tính/selection cũ. CSS có layout mobile, focus và vùng đọc cuộn,
nhưng **chưa kiểm trực quan desktop/mobile**: công cụ báo
`The browser access host is unavailable`, không có browser trong inventory;
không đánh dấu browser PASS, giữ gate này tại F11. F10–F12 tiếp tục;
không push/deploy/submit.

### F10 — Backtest nhiều bản và so sánh cùng support

Hoàn tất phạm vi chức năng/offline ngày **13/11/2026**, nhánh
`feat/variant-backtest-ui` từ develop `6666f48c`. `/backtest` mặc định serving
as-of; `/backtest?source=legacy` giữ form/Full-No-Alpha cũ. Template đã tách
partial/CSS/JS theo chức năng, không tiếp tục đưa thêm logic vào file lớn.
Miền F08 giữ chín mã/58 phiên 1d/VI, ≤30 point/job, repeat1–3 và step ba phiên.

- [x] Form nhiều mã/cửa sổ/IDs/model options và preflight có số point/slot/trần API attempts. Body start đúng bản request đã kiểm; đổi input hủy grant/response cũ, không POST lại mù khi mất phản hồi. UI VI/EN, report vẫn chỉ VI; key giữ phía server.
- [x] API mới `GET /api/serving/v1/jobs` catalog owner; `jobs/<UUID>/evaluation` và `/export` đọc checkpoint/resource đã bound, không tạo model/provider. Outcome cần đủ forecast/dependency/repeat; source evaluator/runtime hoặc resource đổi thì từ chối. UUID raw response dùng lại qua slot/repeat bị chặn cả khi envelope đã được tính lại checksum.
- [x] Evaluator tái dùng **`core.free_pilot_statistics.account` và `core.unified_analysis.analysis.classified`** của U09, đối chiếu outcome với `outcome_from_frame`/oracle nguồn VND. Daily NAV EOD/MDD và return/cycle-end MDD tách riêng, fee/slippage/turnover đúng helper; không annualize. Mỗi mã/repeat là account 50 triệu độc lập, mean không phải portfolio; classification mean theo repeat, không coi repeat là mẫu độc lập mới.
- [x] Partial/UNKNOWN chỉ hiện forecast đã xong và coverage; giữ null, không tạo CASH cho slot thiếu. Summary/account/NAV/contrast chỉ mở khi **toàn job đủ outcome/common support**; subset rỗng không dựng metric. Filter mã/query-date/repeat tính lại account/classification trên cùng subset; baseline native/common phải thực sự có trong plan. Contrast chỉ là point estimate cùng job, không sinh CI/p-value mới hoặc ghép hai run.
- [x] `/experiments` giữ **U09 mặc định**; thêm “Backtest mới” của owner và “Full/No-Alpha cũ” từ `backtest_result/`. Run/kind được kiểm riêng, filter/poll cũ bị hủy khi đổi run; lỗi catalog mới không làm mất viewer U09. Plot chỉ một mã/repeat cùng lúc, không cộng NAV nhiều account. Có stop/resume, counts point/slot/API, partial và error rõ ràng.
- [x] Adapter legacy dùng `legacy_full`/`legacy_no_alpha`, **không đổi No-Alpha thành `original_common`**. Số nguồn ghi nhãn `LEGACY_DECLARED_NOT_RECERTIFIED`; thiếu là null, lỗi dù raw SHORT vẫn không thành CASH. CSS/JS cũ giữ nội dung (JS chỉ đổi JSON bootstrap); handler native/realtime/backtest Python giữ nguyên AST, chỉ bổ sung context render. Không đọc Python từ archive lên web import path.
- [x] JSON/CSV cùng evaluator/filter/provenance/units, export summary/predictions/accounts/daily NAV/cycles/contrasts; owner và query được kiểm server, attachment/nosniff/no-store. CSV chặn công thức, số âm numeric và zero giữ nghĩa; DOM chỉ ghi text, ID/path/bootstrap được kiểm/escape; không export field key tùy ý trong file legacy.
- [x] **156 Python PASS**, gồm **18 test mới** (9 evaluator, 9 API/page), 108 hồi quy F09, 10 scalar-oracle pilot statistics và 20 unified-analysis. Có 18 test leakage, 11 native parity, owner/cookie, stop/resume/UNKNOWN, source/runtime/raw tamper/duplicate UUID, filter/NA/economics và CSV. Ca **MWG 02/07/2026** chạy cả sáu bản qua API/provider/resource thật, tám forecast slot, sáu account được chọn/24 daily NAV row, MT eligible có raw; toàn HTTP fixture.
- [x] **31 DOM PASS** (13 mới + 12 analysis + 6 U09), compile **13 Python**, syntax **7 JS** thay đổi PASS. Fixture CLI ban đầu thiếu root trong `sys.path` đã sửa và chạy lại; không chỉnh runtime để né test. Không chạy full unit/E2E/compileall/cold study theo AGENTS §1.2.
- [x] **20 gói W12 + 30 archive lịch sử**, **11 output F05 + 68 nguồn manuscript**, resource manifest/QA F08 và QA F09 giữ nguyên byte. Worktree khớp **722/729** pin U09: bảy đường đã version hóa, thêm `templates/backtest.html` so với F09; F01 phục hồi đủ729. Native causal vẫn FAIL, whole-system NOT_CERTIFIED.

[QA backtest](backtest_ui_checks.zip) gồm **29 member**, giữ source/runtime/test/log/syntax/integrity,
checklist và **150 liên kết**. **0 hosted LLM, 0 market API, 0 training HMM/student/bank
mới**; native Alpha giữ hành vi tính/selection cũ. Chưa smoke hosted mới.
Browser tiếp tục báo `The browser access host is unavailable`, inventory không
có browser; **chưa kiểm trực quan desktop/mobile**, giữ gate này tại F11.
F11–F12 tiếp tục; không push/deploy/submit.

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
replay đã PASS trong phạm vi U06. U08 đã thu đủ 102 điểm/2.448 forecast/102 labels
và cold seal PASS ngày 12/11/2026; gói research đã được nghiệm thu nguyên byte.
U09 đã PASS phân tích paired/cold replay nguyên byte; U10 đã hoàn tất bàn giao
bản thảo nội bộ qua F01–F05 ngày 13/11/2026; không phải nghiệm thu khoa học/editor.

- [x] Phân tích hai nhánh, mô phỏng merge, đối soát 25 tham chiếu file/hash H08/H09 và lập kế hoạch.
- [x] U01 — Khóa inventory nguồn, evidence và callers trước triển khai.
- [x] U02 — Hợp nhất nguồn và bảo toàn contracts fix trên nhánh tích hợp.
- [x] U03 — Kiểm chứng tương đương original_fix trên miền hợp lệ và version delta serving.
- [x] U04 — Registry, runner, evaluator và CLI/UI offline thống nhất.
- [x] U05 — Profile alpha nhân quả chung và bridge với native; gate toàn hệ còn chờ U06/U07.
- [x] U06 — Amendment v2 đủ nguồn offline, quota có bằng chứng, scoped tests và cold replay102/102 PASS; inference/release vẫn OFF.
- [x] U07 — Paired/PIT/recovery offline PASS116 test, cold replay102 điểm/2.448 forecast slot; không mở inference.
- [x] U08 — Smoke và research đã seal đủ 102 điểm/2.448 forecast/102 labels; nghiệm thu và gói evidence PASS.
- [x] U09 — Phân tích paired102 điểm/ba repeat, hai family/20 contrast và bridge; cold replay15 artifact, oracle1.530 account và gói evidence PASS.
- [x] U10 — F01–F05 hoàn tất: bản thảo/response/87-row matrix/locators/source/companions/QA nội bộ khớp bằng chứng; quyền/PID, nghiên cứu còn thiếu và reviewer acceptance vẫn riêng.

### Checklist chi tiết U09

Ngày 12/11/2026, triển khai trên `feat/unified-comparison-analysis` từ develop
`2ead2bc9`; source phân tích khóa tại `ae90d995`. Chỉ đọc research U08 đã seal,
không gọi LLM, refit student/HMM, đổi economics/PIT hoặc sửa primary sau outcome.

- [x] U09.1 — Đối soát gói U08, receipt active, protocol v2, 718 pin nguồn/286 assets/Python3.13.5 và107 package; giữ đủ102 điểm/ba repeat.
- [x] U09.2 — Consumer từ archive đã seal, kiểm đúng 2.448 slot/UUID/shared và nhãn; 51 account mã/fold, BHN chỉ ba fold sau.
- [x] U09.3 — Hạch toán daily NAV/cycle ledger, hai family/20 endpoint-contrast, ba bridge, CASH/ALWAYS_LONG và toàn sensitivity đã khóa.
- [x] U09.4 — PASS25 test trực tiếp/caller, compile8 file Python mới; thêm4 test label/firewall liên quan PASS.
- [x] U09.5 — Phân tích đủ tám vai trò và hai control, mean repeat trong account rồi mean51 account; giữ âm/null/fallback và toàn bộ cost ledger.
- [x] U09.6 — Cold replay tiến trình mới khớp nguyên byte15 artifact; oracle engine/scalar BA đối soát1.530 account PASS; giữ8.035 file journal U08 nguyên byte.
- [x] U09.7 — Receipt/gói kết quả/QA/hash/consumer PASS, cập nhật checklist, commit/merge vào develop; bàn giao dữ liệu cho U10.

### Kết quả và giới hạn U09

[Nghiệm thu U09](unified_analysis_acceptance.json),
[runtime](unified_analysis_runtime.json), [checks](unified_analysis_checks.json),
[gói kết quả](unified_analysis_results.zip) và [QA](unified_analysis_checks.zip)
khóa lineage vào đúng dataset active U08. Namespace kết quả là
`outputs/unified_integration/u09_analysis_r1`, chứa JSON/CSV/report và PNG/SVG.
Bổ sung 11 pin mới, tổng729 nguồn; không sửa718 pin hoặc gói research U08.

| Vai trò/control | Mean account return % | BA % | LONG /306 | Bypass /306 |
| --- | ---: | ---: | ---: | ---: |
| original_fix | -0.652699 | 51.844156 | 69 | 0 |
| original_common | -1.024794 | 45.965368 | 88 | 0 |
| bayesian_v1 | -0.698188 | 50.095238 | 73 | 162 |
| C2 | -1.030117 | 45.748918 | 89 | 303 |
| A_tp_pool | -1.019471 | 46.181818 | 87 | 282 |
| B_semantic | -1.030117 | 45.748918 | 89 | 303 |
| MT_BICL | -1.253483 | 43.168831 | 105 | 108 |
| Fact_Anchor | -1.286449 | 42.735931 | 107 | 0 |
| CASH_EVERY_CYCLE | 0.000000 | 50.000000 | 0 | 306 |
| ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS | -2.999738 | 50.000000 | 306 | 306 |

Return là bình quân đều51 account mã/fold, mỗi account bình quân ba repeat;
không nối fold hoặc compound qua repeat, không gọi mean account là portfolio.
Tám vai trò và ALWAYS_LONG đều có mean net return âm; CASH là0. Đây là
cycle controls cùng102 query, không phải continuous buy-and-hold.

Primary dùng10.000 circular fold block L2, PCG64 seed20261110, cùng indices
cho hai endpoint ×10 contrast. Cả10.000 draw joint finite; không redraw.
Band95% dùng SD ddof1 trên joint finite và higher quantile của max
|draw−estimate|/SD, chung20 chiều. Index SHA256
`09374ae6e221b701c9b2b88241135fd70a701e611e752a8b8ec5bf82b669b9a7`.

| Return contrast | Effect đpt | Band95% mô tả đpt |
| --- | ---: | --- |
| bayesian_v1 − original_fix | -0.045489 | [-0.362311; 0.271332] |
| C2 − original_fix | -0.377419 | [-0.865902; 0.111065] |
| A_tp_pool − original_fix | -0.366772 | [-0.867016; 0.133472] |
| B_semantic − original_fix | -0.377419 | [-0.865902; 0.111065] |
| MT_BICL − original_fix | -0.600784 | [-1.090421; -0.111147] |
| bayesian_v1 − original_common | +0.326606 | [0.067130; 0.586081] |
| C2 − original_common | -0.005323 | [-0.015970; 0.005323] |
| A_tp_pool − original_common | +0.005323 | [-0.005323; 0.015970] |
| B_semantic − original_common | -0.005323 | [-0.015970; 0.005323] |
| MT_BICL − original_common | -0.228689 | [-0.575839; 0.118462] |

Bayesian v1 cải thiện so common trong band mô tả: D return +0,326606đpt và
D BA +4.129870đpt [2.010663; 6.249077]. So native, D return
−0,045489đpt có band chứa0. MT có D return −0,600784đpt so native và
−0,228689đpt so common; giữ nguyên các kết quả bất lợi. Sáu cluster lịch đã
exposed chỉ hỗ trợ sensitivity, không p-value xác nhận, coverage/power hoặc
khẳng định superiority/live profitability. Không chọn family có kết quả đẹp.

Bridge mô tả native→common làm return thay đổi −0,372095đpt; common→anchor
−0,261655đpt; anchor→MT +0,032967đpt. MT trùng action anchor302/306 forecast,
chỉ bốn action khác; không quy toàn bộ chênh baseline cho student. C2/B_semantic
chỉ có3 raw Decision mỗi nhánh, A_tp_pool24, v1 144, MT198. Kết quả primary
bao gồm fallback đúng protocol, không coi mọi slot là một LLM call mới.

`results.json` giữ L1/L3, leave-one-fold-out, leave-one-symbol-out và CORE4
48 điểm/24 account đã khóa. `per_repeat.csv` giữ dispersion và cycle ratios;
confusion/F1/MCC/BA theo repeat và mã/fold nằm ở các CSV classification.
`accounts.csv`, `cycles.csv`, `daily_nav.csv` giữ toàn1.530 account, phí/slippage,
fractional shares, EOD MTM MDD, cycle-end MDD và cash giữa query. Sharpe dùng
SD sample ddof1, Sortino dùng RMS phần âm toàn cycle/MAR0; annualized=null.
Null/zero denominator và draw thiếu class được kiểm bằng unit test, không ép0.

Raw proposal, numeric veto, final action, trace hash và support nằm ở predictions;
prior_traces.json giữ trace dedup. K/age/similarity xuất khi đã ghi; regret không
có trong frozen trace cho null kèm lý do. Brier chỉ mô tả numeric student/teacher
đúng target trên eligible support; không gán probability cho confidence LLM/fallback.
Các panel retrieval/prior/MT ablation deferred vẫn chưa thực thi.

Cold consumer chạy trong tiến trình mới với mạng ngoài và sáu constructor
key/client/SDK/provider bị chặn: `PASS_U09_COLD_REPLAY`, khớp nguyên byte cả
15 artifact. Kiểm riêng bằng `compute_account_metrics` frozen và BA scalar
trên1.530 account/tám vai trò/hai control khớp trong tolerance1e−10đpt return
và1e−12đpt BA. Không gọi evaluator U04 như một replay đầy đủ ABI metadata;
chỉ đối soát kinh tế/phân loại bằng engine và phép đếm độc lập. Figure PNG đã
được xem kiểm nhãn/band, không clipping.

Đã PASS25 test mới/caller (20 ca U09,5 ca accounting/metrics) và4 ca firewall
U08 liên quan; compile riêng8 file Python mới. Test phủ oracle scalar, reset
account/repeat, padding BHN, paired indices, cả20 chiều, higher quantile, missing
class/zero SD/minimum9500, checksum/grid/raw reuse, VND một lần và null JSON.
Không chạy full suite/compileall/E2E vì chỉ thêm consumer/statistics offline;
PIT/retrieval/kernel frozen được giữ hash, không mở đường thu hoặc huấn luyện mới.

Gói kết quả có24 thành viên/1,383,945 byte, SHA256
`e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9`.
Gói QA có17 thành viên/18,302 byte, SHA256
`8cb5adcf002a228c6b4a1ac9162526c9d0372f6be247a26cab43a727868a4dde`.
Consumer thư viện chuẩn đã kiểm đủ member/hash và729 nguồn local. Gói giữ
15 artifact/receipt gốc, runtime/checks, cold proof/cross-check/firewall và
manifest; source Git, gói U08,286 assets và107 package là dependency ngoài gói.
Acceptance JSON là gate cold cuối; receipt execution giữ nguyên mốc
`cold_replay=PENDING` trước khi verifier riêng chạy, không ghi đè lịch sử.

Chỉ0 API mới,0 training/refit. Giữ nguyên native row-wise causal FAIL,
whole-system causal NOT_CERTIFIED và giới hạn nguồn/exposure U06. U09 hoàn tất;
U10 đã cập nhật nguồn bài báo và chốt build/render/QA ở F05 ngày 13/11/2026;
không thay kết quả nghiên cứu hoặc nâng gate causal/reviewer.

Kiểm lại toàn bộ phân tích, không gọi LLM:

```powershell
py -3.13 -I -X utf8 scripts/unified_analysis/run.py verify
```

Khôi phục các bảng đã sinh từ gói (giữ nguyên namespace) và kiểm manifest:

```powershell
py -3.13 -I -m zipfile -e docs/plan/week12/unified_analysis_results.zip "$env:TEMP/u09-results"
py -3.13 -I -X utf8 "$env:TEMP/u09-results/evidence/verify_u09_package.py" docs/plan/week12/unified_analysis_results.zip --root "$PWD"
```

`analyze` chỉ dùng cho checkout chưa có namespace U09; có receipt thì dùng
`verify`, không overwrite results để chọn lại kết quả.

### Checklist chi tiết U08

Triển khai trên `feat/unified-comparison-run`, từ develop `ea90605b`.
Grant kỹ thuật cho lượt mới đã neo Git theo protocol khóa, chỉ Free/0 USD.
Theo đính chính của người dùng ngày 10/11/2026, người dùng tự khởi chạy research
bằng lệnh được bàn giao. Collector đã tự khởi chạy trước khi bàn giao lệnh và đã
dừng có checkpoint lúc 14:02. Người dùng đã chạy tiếp và thu đủ research;
nghiệm thu hoàn tất ngày 12/11/2026, xem [kết quả U08](#nghiệm-thu-u08).

- [x] U08.1 — Đối soát develop/plan, tạo branch; năm GET catalog mới đều thấy hai model active,0 inference.
- [x] U08.2 — Thêm transport live/release riêng, giữ DAG, UUID, quota/carry và cap3/retry+repair.
- [x] U08.3 — PASS69 test/8 module, compile11 file; QA14 source mới và672 nguồn U07 giữ nguyên; neo runtime/preflight/grant smoke riêng vào Git.
- [x] U08.4 — Smoke BHN-2025-10-01, một repeat/đúng org4:8 slot,6 HTTP200,12.793 token;0 query payoff, cold verify PASS.
- [x] U08.5 — Grant research mới sau smoke đã neo Git. Collector có lock/checkpoint/heartbeat đã chạy và dừng an toàn, sẵn sàng để người dùng resume thủ công.
- [x] U08.5a — Amendment quota theo `(org, model)` đã PASS 61 test, compile 5 file và cold verify 32 điểm hoàn chỉnh. Prefix 487 HTTP và 2.390 file checkpoint giữ nguyên byte, bàn giao entrypoint resume mới.
- [x] U08.5b — Admission provider bỏ lịch local, PASS 41 test/compile 5 file, cold verify 38 điểm và đối soát 2.878 file checkpoint nguyên byte. Bàn giao lệnh resume mới, 0 HTTP mới trong lượt sửa.
- [x] U08.5c — Reset hai điểm lỗi theo yêu cầu người dùng, sao lưu 44 checkpoint và giữ ledger; PASS 44 test/compile 6 file, cold verify 67 điểm hoàn chỉnh, bàn giao lệnh mới.
- [x] U08.5d — Reset riêng MT_BICL/VCB-2026-09-23/repeat3 đã hết attempt; giữ 2.437 forecast và 1.693 HTTP, PASS 40 test/compile 4 file và cold verify 100 điểm.
- [x] U08.6 — Đủ102 shared,2.448 forecast,102 canonical labels; receipt PASS_U08_RESEARCH, raw/usage/order/coverage và cold replay đã đối soát.
- [x] U08.7 — Nghiệm thu nguồn/runtime/receipt PASS, giữ 8.035 file journal nguyên byte, đóng gói/hash/consumer PASS; cập nhật checklist, commit/merge tài liệu, bàn giao U09.

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

### Nghiệm thu U08

Ngày 12/11/2026, research do người dùng chạy đã seal lúc **10:10:18 giờ Việt Nam**,
receipt `PASS_U08_RESEARCH`. Đã thu đủ **102 điểm, chín mã, 51 symbol/fold,
ba repeat, một realization**, 102 shared snapshot, 408 graph nodes, 204 render,
2.448 prepare, **2.448 forecast** và **102 canonical labels**. Mỗi repeat có
816 forecast; mỗi vai trò có đủ 306 forecast. Smoke vẫn tách riêng, không nhập
response smoke vào study. Student/HMM và các prepared assets U06 giữ frozen.

| Vai trò | Forecast | Raw Decision được dùng | Bypass theo thuật toán |
| --- | ---: | ---: | ---: |
| original_fix | 306 | 306 | 0 |
| original_common | 306 | 306 | 0 |
| Fact_Anchor | 306 | 306 | 0 |
| bayesian_v1 | 306 | 144 | 162 |
| C2 | 306 | 3 | 303 |
| A_tp_pool | 306 | 24 | 282 |
| B_semantic | 306 | 3 | 303 |
| MT_BICL | 306 | 198 | 108 |
| Tổng | 2.448 | 1.290 | 1.158 |

Bypass có record/policy hợp lệ theo registry, không thay lỗi transport/schema
thành CASH. U09 phải báo coverage/fallback cùng kết quả thay vì coi 2.448 slot
là 2.448 lời gọi LLM. Ledger research giữ **1.702 HTTP attempts**: 1.505 HTTP200,
194 HTTP429, một HTTP503 và hai UNKNOWN. Tập active có 1.687 attempts; **15 raw
đã nghỉ** sau hai amendment reset vẫn nguyên byte, gồm cả hai UNKNOWN cũ;
không có UNKNOWN active. Cả hai backup giữ quyết định thay kết quả, không suy
UNKNOWN thành NOT_SENT. Cap vẫn 7.956 cho toàn ledger, tối đa ba HTTP mỗi UUID
execution. Usage quan sát trong raw là 2.986.930 token; hai UNKNOWN giữ reserve
9.177 token riêng. Đây là usage của research, chưa cộng carry lịch sử/smoke.
Quyền chỉ Free/0 USD; không suy usage thiếu thành số token thực hoặc chi phí trả phí.

Đối soát mới dùng cold consumer ở tiến trình riêng, chặn mạng ngoài và sáu
constructor key/client/SDK/provider: `PASS_U08_ACCEPTANCE`, **0 inference mới**.
Đã tái lập toàn bộ metadata/raw/policy, shared/parents, thứ tự/DAG, barrier đủ
24 forecast trước label, nhãn T+2.5 từ oracle canonical và từng policy quota
qua các mốc amendment. **718 source bindings**, Python3.13.5/107 package cùng
assets/data/model frozen khớp; 8.035 file journal được kiểm nguyên byte trước
và sau nghiệm thu. Prompt Decision lớn nhất kể cả repair là 4.750 ký tự.
Receipt, quota receipt, status và log cold seal của collector đồng nhất.

Lượt này chỉ cập nhật tài liệu và đóng gói bằng chứng có sẵn. Theo AGENTS §1.2,
không chạy lại compileall/unit/E2E/leakage suite. Viện dẫn đúng checks đã PASS
và được đối soát hash nguồn: U08 ban đầu 69 test/11 file compile; amendment
model 61/5, provider 41/5, point reset 44/6, slot reset 40/4. Đây là các gate
đúng phạm vi của từng snapshot, không cộng thành một full suite mới hoặc nâng
các gate causal cũ. Cold consumer/kiểm archive đã thực thi mới trong lượt này.

[Gói research đã seal](unified_live_research.zip) giữ **8.064 thành viên /
78.438.700 byte**, SHA256
`5936bc971bebf1b139a34b93f154ad8e54d0a0e37fdaa6ac4673295f8b60a11c`.
Trong đó có 8.035 file journal/205.506.904 byte nguyên bản, toàn bộ raw kể cả
raw đã nghỉ, diagnostics, receipt/status/log, hai backup, protocol/runtime/
checks/grants, 718 source bindings, inventory và script/log nghiệm thu.
Manifest liệt kê hash từng thành viên; consumer thư viện chuẩn đã đọc và kiểm
đủ 8.064 thành viên cùng 718 nguồn local, `PASS_U08_EVIDENCE_PACKAGE`.
Các lock/owner/recovery/launcher tạm không thuộc evidence dataset. Source Git,
assets U06 và các QA ZIP cha vẫn là dependency ngoài gói, được consumer nghiệm
thu đối soát; gói không chứa credential hoặc tự nhận là bản cài đặt độc lập.

U09 dùng dataset active theo `receipt.json`/`quota_receipt.json` trong namespace
`outputs/unified_integration/u08_research_r1`, được giữ trong gói ở cùng đường dẫn.

- `records_sha256`: `c5c9d18fc8175b9067d2d08df9925a6c6c80d83f70acd613e95874fa80ac414c`.
- `outcomes_sha256`: `39ee19354355f1264a92e37f3cd10a649ab42d79bb9e7c30056043149774dc44`.
- `wire_sha256`: `f7a5894f2576211c03dfd190428679bcdf1e5ee7be8d5909bbca4e27efa9eb6c`.
- Runtime slot reset: `24ec38a6fdb2c040384abd2f15de49af2cf823c42120b8e87ca29e6c59244f47`.

U08 hoàn tất thu thập và nghiệm thu phần mềm/evidence. U09 đã có phân tích
paired tại mục phía trên; tại mốc U08, U10 chưa cập nhật bài báo. Trạng thái
hiện hành là F05/U10 đã bàn giao nội bộ ngày 13/11/2026. Historical exposure,
news availability và các giới hạn nguồn ở U06 giữ nguyên; native row-wise causal
vẫn **FAIL**, whole-system causal **NOT_CERTIFIED**. Repeats không tăng N thị trường.
Nhật ký amendment bên dưới ghi đúng trạng thái tại từng mốc trước khi seal.

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

#### Admission theo phản hồi provider

Ngày 11/11/2026, người dùng yêu cầu bỏ lịch chờ local để gửi được request khi
provider còn quota. Policy `provider_response_v1` cho gửi ngay, chỉ defer khi
response lỗi thực của đúng org/model yêu cầu Retry-After hoặc exponential
backoff. Bộ đếm RPM/RPD/TPM/TPD và header remaining của response thành công cũ
được giữ làm telemetry. Budget từng request, phase cap 7.956, trần ba attempt
gồm retry/repair và rào UNKNOWN tiếp tục được kiểm trong đường gọi U08.

Collector đã dừng an toàn trước sửa, prefix gồm 591 HTTP (590 HTTP200, 1 HTTP503),
43 shared, 968 forecast và 38 canonical labels. Amendment áp dụng từ sequence591,
tức HTTP attempt thứ592. Cold verifier kiểm policy org/model cũ trên đoạn487–590
và policy provider từ591, cùng identity/UUID của journal research hiện có.
Các thời điểm chờ local cũ trong status được xóa khi chuẩn bị bàn giao.

[Runtime provider](unified_provider_quota_runtime.json),
[grant thủ công](unified_provider_quota_release.json),
[scoped checks](unified_provider_quota_checks.json) và
[gói QA](unified_provider_quota_checks.zip) quản lý amendment này.
Telemetry `WAITING_QUOTA`/`waiting_models` ghi lý do
`PROVIDER_RETRY_AFTER_OR_BACKOFF`, mã HTTP gần nhất và thời điểm retry.

Nghiệm thu tại source commit `8c4f45cb` có 41 test, gồm 29 ca mới hoặc chạy bằng
transport mới và 12 ca prefix/label firewall liên quan, 0 failure/error/skip.
Compile riêng 5 file Python mới. Phạm vi gồm bỏ bốn gate bộ đếm local, header
remaining cũ, cooldown thực theo org/model, 429 qua restart, retry/repair/cap,
UNKNOWN, raw reuse, paired/barrier, mixed-policy replay và manager lock khi seal.
Tám pin source mới nối tiếp 694 pin nguồn đã khóa của các giai đoạn trước.

Cold audit mới chặn mạng ngoài và sáu constructor key/client/SDK/provider,
kết quả `PASS_PROVIDER_QUOTA_COLD_HANDOFF`, tái lập 38 điểm/912 forecast thuộc
những điểm này và 38 canonical labels. Cả 2.878 file identity/wire/raw/slot được
đối soát nguyên byte. Journal có thêm 56 forecast ở các điểm dở, tổng 968.
Probe offline 8.000 token ở đủ 10 bucket nhận READY, 0 HTTP mới. Study còn
`PARTIAL_U08`, chờ thu đủ và seal. Gói QA có 7 thành viên/225.090 byte, SHA256
`7d281df5b154bccc6e30f235a4cfed97f18ecfe781f396b04227cb40140aa3fa`.

### Reset hai điểm lỗi theo yêu cầu người dùng

Ngày 11/11/2026, người dùng xác nhận Groq Console có HTTP200 khớp hai request
mà journal local đang ghi UNKNOWN, rồi yêu cầu xóa điểm lỗi để tự chạy lại.
Đã sao lưu và xóa toàn bộ 44 checkpoint của `VCB-2026-04-01` và
`VJC-2025-12-19`, khóa generation mới bằng `provider_response_point_restart_v1`.
Các kết quả mới thay toàn điểm, giữ upstream dùng chung cho đủ 24 forecast
trong generation mới; 15 forecast dở trước reset được giữ trong backup.

- [x] Hai điểm reset được chỉ định trước khi chạy lại, mọi checkpoint được sao lưu nguyên byte trước xóa.
- [x] Giữ 67 điểm hoàn chỉnh và 4.916 file identity/wire/raw/slot còn lại nguyên byte.
- [x] Giữ toàn bộ 1.087 HTTP attempts, gồm 12 raw của generation đã nghỉ và hai UNKNOWN cũ; chi phí vẫn cộng vào phase cap 7.956.
- [x] PASS 44 test, compile riêng 6 file Python; cold handoff offline PASS, 0 HTTP mới.
- [x] Neo runtime/grant/backup/checks vào Git và bàn giao entrypoint mới để người dùng tự chạy.

[Backup checkpoint](unified_point_restart_backup.zip) có 57 thành viên/740.003 byte,
SHA256 `5b61f99f7f44340e3545d56b22fecb23b1428a291b2dd46e44b13e8d9515249e`.
[Runtime reset](unified_point_restart_runtime.json),
[grant thủ công](unified_point_restart_release.json),
[scoped checks](unified_point_restart_checks.json) và
[gói QA](unified_point_restart_checks.zip) khóa danh sách điểm, từng raw đã nghỉ,
prefix còn lại và quyền manual/Free/0 USD. Gói QA có 9 thành viên/382.452 byte,
SHA256 `ead409a839c09f15b18cbdcc59e225bf3a1df93c0ec2bb9cfdc00af6d5ec41c1`.

Nghiệm thu source `2369e6f0` bao phủ reset sau HTTP timeout, UUID mới, replay/raw,
retry/repair/cap qua restart, backup hỏng, checkpoint bị sửa, đường dẫn ngoài
namespace, purge bị ngắt, bảo vệ điểm hoàn chỉnh/prefix, paired/barrier, manager
lock và label/leakage firewall liên quan. Chín pin source mới nối tiếp 702 pin
nguồn cũ giữ nguyên hash; runtime/package versions cũ giữ nguyên. Chỉ kiểm thử
đường chạy bị ảnh hưởng, không chạy full suite, full compileall hoặc E2E.

Cold consumer chặn mạng ngoài và sáu constructor key/client/SDK/provider,
nhận `PASS_EXPLICIT_POINT_RESTART_COLD_HANDOFF`: tái lập 67 điểm hoàn chỉnh/
1.608 forecast và 67 canonical labels. Trạng thái active có 70 shared,
1.632/2.448 forecast và 67/102 labels. Ledger có 1.075 HTTP active và 12 HTTP
đã nghỉ; cả 1.087 vẫn có raw gốc. Probe admission offline cho đủ 10 bucket
nhận READY; quota thực tiếp tục được xác định qua phản hồi provider khi người
dùng chạy. UNKNOWN mới vẫn dừng để đối soát; cooldown 429/5xx và trần ba
attempt mỗi execution vẫn hiệu lực. Diagnostic mới lưu status/request ID,
response hoặc loại ngoại lệ sát HTTP transport, loại bỏ header credential
và nội dung thông báo ngoại lệ khỏi log.

U08.6 còn chờ đủ cohort và cold seal. U09 phải dùng receipt/dataset active của
entrypoint mới; raw đã nghỉ được giữ để kiểm toán chi phí và quyết định reset.

### Reset riêng forecast hết attempt

Ngày 12/11/2026, người dùng yêu cầu bỏ lượt lỗi để chạy nốt. Đã sao lưu rồi xóa
riêng checkpoint `forecast/VCB-2026-09-23/u0/r2/MT_BICL`; shared upstream,
prepare và các forecast khác giữ nguyên. Execution cũ có ba HTTP theo thứ tự
429 do TPM, 200 có `evidence_against` rỗng và 429 khi schema repair.
Không chọn lại response hợp lệ hoặc xem payoff của điểm chưa hoàn chỉnh.

- [x] Sao lưu một checkpoint và ba raw gốc trước xóa; giữ 7.992 file còn lại nguyên byte.
- [x] Giữ 102 shared, 2.437 forecast, 100 điểm/labels hoàn chỉnh và toàn bộ 1.693 HTTP.
- [x] UUID execution mới chỉ áp dụng slot đã chỉ định; 15 raw đã nghỉ gồm 12 raw của lần reset trước và ba raw lần này vẫn tính vào cap 7.956.
- [x] PASS 40 test, compile riêng 4 file Python; cold handoff offline PASS, 0 request mới tới provider.
- [x] Neo runtime/grant/backup/checks vào Git; người dùng tự chạy bằng CLI bên dưới.

[Runtime slot](unified_slot_restart_runtime.json),
[grant thủ công](unified_slot_restart_release.json),
[scoped checks](unified_slot_restart_checks.json),
[backup](unified_slot_restart_backup.zip) và [gói QA](unified_slot_restart_checks.zip)
quản lý amendment `provider_response_slot_restart_v1` tại source `5177da6b`.
Backup có 5 thành viên/22.750 byte, SHA256
`09bec6ca8621e8f82802960527ab6e772ce901af8e01b19bdf773b9d45d2d7a9`.
Gói QA có 9 thành viên/601.311 byte, SHA256
`f2aee4c3b11ac718fbefdaa09400c11a91b7b2b823f3b5fe2fec90b4db1d098e`.
Bảy pin mới nối tiếp 711 nguồn cũ giữ nguyên hash. Các test kiểm reset sau
429/schema lỗi/429, giữ upstream/prepare/các slot khác, UUID mới, replay,
retry/repair/cap, từ chối bỏ response hợp lệ, backup/checkpoint bị sửa,
manager lock, barrier nhãn và leakage firewall liên quan. Chỉ chạy checks đúng
phạm vi, không chạy full suite, full compileall hoặc E2E. Cold verifier chặn
mạng và sáu constructor key/client/SDK/provider, tái lập 100 điểm hoàn chỉnh/
2.400 forecast cùng 100 labels; 37 forecast còn lại thuộc hai điểm dở.
Study còn thiếu 11 forecast và hai labels, chưa seal hoặc hoàn tất U08.6.
Quota thực vẫn theo response provider; trần ba HTTP áp dụng riêng execution mới.

Research đã hoàn tất; collector hiện không chạy. Đọc trạng thái hoặc đối soát
lại receipt đã seal bằng các lệnh offline sau từ thư mục gốc repo:

```powershell
py -3.13 -I -X utf8 scripts/unified_slot_restart/run.py status
py -3.13 -I -X utf8 scripts/unified_slot_restart/run.py verify --seal
```

Để kiểm gói độc lập, giải nén vào thư mục tạm rồi chạy consumer có trong gói:

```powershell
py -3.13 -I -m zipfile -e docs/plan/week12/unified_live_research.zip "$env:TEMP/u08-research-evidence"
py -3.13 -I -X utf8 "$env:TEMP/u08-research-evidence/acceptance/verify_u08_package.py" docs/plan/week12/unified_live_research.zip --root "$PWD"
```

Không nhập các file trong backup vào tập forecast active của U09. Đọc manifest
và receipt active để giữ đúng quyết định reset đã khóa và tính đủ chi phí HTTP.

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
