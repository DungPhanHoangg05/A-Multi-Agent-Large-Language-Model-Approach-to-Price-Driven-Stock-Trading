# Nguồn bài báo và khôi phục historical trước F02

[Checklist và kết quả F01](README.md#f01--nguồn-và-historical-replay) ·
[Kế hoạch cuối](final_paper_ui_plan.md#5-bảo-toàn-bằng-chứng-khi-sửa-paper-và-ui)

## Mốc nguồn và phạm vi snapshot

Mốc trước sửa bài/ứng dụng là commit
`384725a66fec074700963fac67c358b28b842092` trên develop; donor gốc là
`9efd23f4157e0d3ab8069fccab7dccf03439a714`. Nhánh triển khai F01 là
`docs/final-evidence-map`. Các tên study dưới đây chỉ dùng để phân biệt nguồn
trong mapping biên tập, không đổi ID trong journal hoặc registry.

[Snapshot](final_evidence_snapshot.zip) giữ **810 file nguồn nguyên byte**:
hợp của 729 source pin U09, 50 file `paper/`, 28 file `revision/` và 228 file
ứng dụng/cấu hình được Git theo dõi. Các tập có giao nhau; không cộng chúng
thành số file mới. Phạm vi ứng dụng gồm `agents/`, `core/`, `utils/`,
`data_manager/`, `web_interface.py`, sáu file `templates/` (bốn trang và hai
logo), cấu hình và dependency/runtime. Snapshot gồm cả các nguồn ignored mà
pin yêu cầu, như candidate student và handoff pilot48; không chỉ lưu Git blob
rồi giả định checkout có đủ file. Giữ LF/CRLF đúng SHA256/length đã khóa.

`snapshot_manifest.json` trong ZIP ghi commit, binding của từng file nguồn,
20 gói evidence W12 và 30 ZIP lịch sử trong `outputs/revision/`. Các gói lịch
sử đó được giữ tại vị trí cũ/Git commit trên, không được sinh lại hoặc ghi đè.
SHA256 ngoài của snapshot và kết quả smoke nằm trong README W12; proof nằm
trong `evidence/` của chính ZIP. Snapshot không phải release bài báo F05 hoặc
ứng dụng F12, không mở lại quyền inference của các grant được lưu lịch sử.

## Mapping hai nghiên cứu tới bài báo

| Study / bằng chứng | Nguồn đã khóa | Đích dùng ở F02–F05 và giới hạn |
| --- | --- | --- |
| `legacy_fix_revision`: main Full/Base và controls | `outputs/revision/final_baselines_v1/{classification,per_class,macro,financial,accounts,main_comparison}.csv`; các binding trong `manifest.json` cùng thư mục | Giữ `t02_classification.tex`, `t03_accounts.tex`, companion S1 và macro Full/Base. Main 102 điểm, 25 UP/77 DOWN, 51 account, 204 Decision B/AS. B bỏ cả alpha/sentiment; không phải `original_common`. |
| Study gốc: scope và repeats | `paper/content/tables/component/scope.tex`; `outputs/revision/final_repeats_v1/{protocol.json,repeat_summary.csv,contrasts.csv,disagreement.csv,lineage.csv}` | Giữ `t01_scope.tex`, `t04_repeats.tex` và companion S2. Hai panel riêng, mỗi panel chín đơn vị, ba execution: upstream B/AS và factorial B/A/S/AS/P. Có reuse main r0 ở upstream; 375 Decision duy nhất theo scope cũ, không cộng các panel thành N độc lập. |
| Study gốc: temporal/numeric/execution | `outputs/revision/final_temporal_v1/{primary_dependence.json,stratified_metrics.json,block_sensitivity.csv,panel_hac.csv}`; `numeric_controls_v1/{summary.json,random_dispersion.json,inference.json}`; `execution_final_v1/scenario_summary.csv` | Giữ `t05_temporal.tex`, `t06_numeric.tex`, appendix F và S3/S4. Numeric controls không phải retrieval ablation; stress scenarios cũ không áp sang variant mới. |
| Study gốc: lineage bảng, hình, headline | `outputs/revision/manuscript_rewrite_v1/{generation.json,numeric_cells.json,headline_values.json,manifest.json,original_sources.zip,sources.zip}`; `scripts/build_revision_manuscript.py` tại commit snapshot | Generator lịch sử ghi đường dẫn, identity, đơn vị/scale, literal và ô render. Giữ namespace `summary_numbers.tex`; không thay macro Full/Base bằng U09, không chạy generator để overwrite release. |
| Bản thảo/tác giả/reviewer hiện hành | `paper/`, `revision/` trong snapshot; `outputs/revision/author_preserved_v1/{manifest.json,sources.zip,main.pdf,main_submit.pdf,formula_comparison.json}` | Nền F03/F04: tám section, A–F, title/tác giả/công thức hiện hành. Đây là bản giữ cấu trúc/tác giả sau các release trước; không chọn `final_pdf_v1` chỉ vì tên có chữ final. Reviewer cập nhật riêng ở F05, không tự đóng comment. |
| Các bản thảo cũ và QA lịch sử | `outputs/revision/{final_pdf_v1,structure_preserved_v1,author_preserved_v1}/`; `revision/manuscript_original.zip` | Giữ từng source ZIP/PDF/receipt đúng release. `original_sources.zip` là nguồn trước lượt sửa tương ứng, không phải bản paper hiện hành. QA/render lịch sử chỉ áp cho PDF của release đó; F01 không build hoặc QA lại PDF. |
| `unified_u08_u09_r1`: response và input | `unified_live_research.zip`, `unified_comparison_protocol_v2.json`, `unified_comparison_manifest_v2.json`; acceptance U08 trong ZIP | U08 có 102 điểm, một upstream realization, ba Decision repeat, tám vai trò; 2.448 forecast slot gồm bypass. Dùng đúng active dataset/receipt, giữ retired raw cho cost/reset; không dùng pilot48 hoặc lượt đã hủy làm kết quả mới. |
| Study mở rộng: kết quả chính | `unified_analysis_results.zip`: `outputs/unified_integration/u09_analysis_r1/{results.json,summary.csv,contrasts.csv,bridge.csv,report.md}`; `unified_analysis_acceptance.json` | F02 sinh namespace U09 riêng: mười hàng (tám vai trò, CASH, ALWAYS_LONG theo chu kỳ đủ phí), hai baseline, 20 contrast và ba bridge. Methods/Setup/Results đọc cùng identity; mean account qua repeat rồi qua 51 account, không phải portfolio. |
| Study mở rộng: support, policy và sensitivity | Cùng namespace U09: `predictions.csv`, `prior_traces.json`, `classification_by_group.csv`, `classification_by_repeat.csv`, `per_repeat.csv`, `accounts.csv`, `cycles.csv`, `daily_nav.csv`; sensitivity trong `results.json` | Thân bài báo coverage/fallback/missing sentiment; appendix F giữ chi tiết symbol/fold/repeat/L1/L3/leave-one-out/CORE4. Giữ null/NA, không chọn subgroup hoặc repeat tốt nhất. |
| Study mở rộng: figure và macro mới | Cùng namespace U09: `return_contrasts.svg`, `return_contrasts.png`, `summary.csv`, `results.json` | F02 tạo bảng/macros prefix riêng; F04 dùng figure hai baseline từ cùng dữ liệu đã verify. Band chỉ mô tả trên sáu fold đã exposed; không nhận calibrated significance hoặc superiority/profitability. |

Cùng lịch 102 điểm không tạo pairing giữa hai study: response, protocol và
provenance khác nhau. Không ghép predictions, cộng N, áp bootstrap/seed U09
ngược lên bảng gốc, hoặc diễn giải ba Decision repeat thành ba full execution.
F02 phải nối từng artifact đầu vào/hash → field/đơn vị → bảng/hình/macro mới
trong release riêng. Mapping chốt tại F01; artifact F02 và kết quả kiểm tra
được ghi tại [README W12](README.md#f02--generator-và-artifact-bài-báo-u09).

## Khôi phục và smoke offline trong checkout riêng

Yêu cầu Git còn giữ commit snapshot và donor/ancestry; Python **3.13.5** cùng
**107 package đúng version** trong manifest U06 v2. `requirements.txt` không
thay cho runtime lock này. Verifier U09 sẽ dừng khi lệch nguồn/runtime; không
sửa expected hash hoặc refreeze receipt để ép PASS. Chỉ dùng `restore` và
`verify` bên dưới, không dùng `assets`, `freeze`, `analyze`, `collect` hoặc
`replay-numeric` (lệnh cuối có refit offline, không cần cho F01).

Chạy từ root repository; chọn thư mục tạm mới, đủ chỗ cho checkout đầy đủ.
Kiểm SHA256 snapshot theo README W12 **trước khi giải nén**. Những lệnh này
chỉ overlay snapshot vào checkout lịch sử đã tách biệt, không phải cây đang
sửa paper/UI. Sau mỗi lệnh native, dừng nếu `$LASTEXITCODE -ne 0`.

```powershell
$sourceRoot = (Get-Location).Path
$snapshot = Join-Path $sourceRoot 'docs/plan/week12/final_evidence_snapshot.zip'
$snapshotSha = '80fed8c9a1c265098a394bfc40f13d7f0266c1e05abdb142fba01d873cb8b8b5'
if ((Get-FileHash -LiteralPath $snapshot -Algorithm SHA256).Hash -ne $snapshotSha) { throw 'Snapshot khác SHA256 đã khóa' }
$historicalRoot = Join-Path $env:TEMP ('final-evidence-' + [guid]::NewGuid().ToString('N'))
git -c core.autocrlf=false worktree add --detach $historicalRoot 384725a66fec074700963fac67c358b28b842092
if ($LASTEXITCODE -ne 0) { throw 'Không tạo được checkout historical' }
py -3.13 -I -m zipfile -e $snapshot $historicalRoot
if ($LASTEXITCODE -ne 0) { throw 'Không giải nén được snapshot' }
Push-Location -LiteralPath $historicalRoot
```

Đối soát đủ 810 nguồn sau overlay (không chuẩn hóa newline):

```powershell
@'
import hashlib, json
from pathlib import Path
root = Path.cwd()
manifest = json.loads((root / 'snapshot_manifest.json').read_bytes())
for name, expected in manifest['source_members'].items():
    raw = (root / name).read_bytes()
    assert len(raw) == expected['bytes'], name
    assert hashlib.sha256(raw).hexdigest() == expected['sha256'], name
print({'source_files_verified': len(manifest['source_members'])})
'@ | py -3.13 -I -X utf8 -
if ($LASTEXITCODE -ne 0) { throw 'Nguồn historical khác snapshot' }
```

Restore **286 asset** ignored từ ZIP U06 đã khóa. Đây là dữ liệu/model/query
đóng băng, không gọi provider hoặc huấn luyện. Sau đó restore **16 file** U09
(15 artifact và receipt) từ gói đã nghiệm thu vào namespace vốn chưa tồn tại:

```powershell
py -3.13 -I -X utf8 scripts/prepare_unified_comparison_v2.py restore
if ($LASTEXITCODE -ne 0) { throw 'Không restore được asset U06' }
py -3.13 -I -m zipfile -e docs/plan/week12/unified_analysis_results.zip tmp/u09-results
if ($LASTEXITCODE -ne 0) { throw 'Không giải nén được kết quả U09' }
py -3.13 -I -X utf8 tmp/u09-results/evidence/verify_u09_package.py docs/plan/week12/unified_analysis_results.zip --root .
if ($LASTEXITCODE -ne 0) { throw 'Gói U09 khác binding đã khóa' }
if (Test-Path -LiteralPath outputs/unified_integration/u09_analysis_r1) { throw 'Cần checkout mới, không overwrite U09' }
Copy-Item -LiteralPath tmp/u09-results/outputs/unified_integration/u09_analysis_r1 -Destination outputs/unified_integration/u09_analysis_r1 -Recurse -ErrorAction Stop
py -3.13 -I -X utf8 scripts/unified_analysis/run.py verify
if ($LASTEXITCODE -ne 0) { throw 'Cold replay U09 không PASS' }
py -3.13 -I -X utf8 scripts/verify_unified_evidence.py
if ($LASTEXITCODE -ne 0) { throw 'Inventory U01 không khớp checkout historical' }
Pop-Location
```

`PASS_U09_COLD_REPLAY` phải khớp nguyên byte **15 artifact**, 102 điểm và
2.448 slot, **0 API mới/0 training**. CLI đã chặn external network và sáu
constructor key/client/provider; chỉ tái lập phân tích từ raw đã seal. Gói
U08 được consumer đọc trực tiếp, không cần bung 8.035 file journal ra cây làm
việc. Không import Python trong ZIP vào Flask; F07 sẽ đọc output đã verify,
không chạy lại toàn phân tích trên mỗi HTTP GET.

Snapshot + checkout + ZIP assets U06 bao phủ đường U09 nói trên. Các private
bundle/model sidecar ở `outputs/revision/reproducibility*/model_weights.zip`
và `reviewer_response_v1/private_bundle.zip` không cần cho smoke này, không
được ngầm coi là có trong clone hoặc được phép công bố. Không nhận việc
restore U09 là đã tái tạo hosted outputs, refit mọi model, hoặc PASS lại bốn
gate toàn hệ. Native row-wise causal vẫn **FAIL**, whole-system vẫn
**NOT_CERTIFIED**; U10 chỉ xong khi F05 hoàn tất.

Giữ worktree historical để tra cứu, hoặc tự dọn bằng `git worktree remove`
sau khi đã lưu output cần thiết và kiểm đúng đường dẫn. Không xóa cưỡng bức
worktree đang dùng; không chuyển task phát triển mới sang nhánh donor `fix`.
