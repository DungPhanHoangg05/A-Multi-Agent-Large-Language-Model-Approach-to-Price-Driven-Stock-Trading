# Làm việc chung trên develop: hệ thống, bài báo và reviewer

[Kế hoạch tổng](../plan.md) · [Checklist hiện hành](README.md#đầu-mối-làm-việc-duy-nhất-trên-develop)

## Một luồng phát triển

`develop` là nhánh tích hợp duy nhất. Mọi task code, dữ liệu nghiên cứu, phân tích,
nguồn LaTeX hoặc phản hồi reviewer đều bắt đầu từ develop và quay lại develop
sau kiểm tra đúng phạm vi. Không tạo công việc mới từ nhánh `fix`; không cần
chuyển về fix để tìm bài báo hoặc chạy các công cụ revision.

```powershell
git switch develop
git pull --ff-only origin develop
git switch -c docs/manuscript-unified-results
```

Tên nhánh trên là ví dụ cho task bài báo; dùng `feat/`, `fix/`, `test/`,
`refactor/` hoặc `docs/` phù hợp công việc. Commit Conventional Commits trên
nhánh tác vụ, kiểm diff/test áp dụng, rồi merge về develop theo AGENTS.md.
Không commit phát triển trực tiếp trên develop/main. Push remote, deployment,
submission và public archive là các thao tác riêng, không phát sinh từ việc
chuyển đầu mối công việc.

Giữ nhánh fix ở commit `9efd23f4157e0d3ab8069fccab7dccf03439a714` làm mốc
lịch sử. Commit này đã là tổ tiên của develop; `git show <commit>:<path>` và
source archive vẫn dùng được ngay khi đang ở develop. Không đổi tên
`original_fix`, `original_fix_serving_v1`, đường dẫn donor hoặc hash chỉ để bỏ
chữ fix: chúng xác định phương pháp và bằng chứng, không phải nơi phải làm việc.

## Nguồn làm việc và bằng chứng

| Nội dung | Nơi làm việc trên develop | Cách sử dụng |
| --- | --- | --- |
| Hệ thống và các phiên bản | `agents/`, `core/`, `utils/`, `data_manager/`, `scripts/`, `tests/` | Sửa theo task; giữ hợp đồng kinh tế/PIT/paired/token/recovery |
| Bài báo | [paper/main.tex](../../../paper/main.tex), [main_submit.tex](../../../paper/main_submit.tex), [các sections](../../../paper/sections), [references.bib](../../../paper/references.bib) | Nguồn tác giả hiện hành; sửa tại đây theo U10, giữ tên tác giả/title/cấu trúc đã được chốt |
| Bảng và hình | [paper/generated](../../../paper/generated), [paper/figs](../../../paper/figs) | Sinh từ release được xác định; không nhập tay số headline hoặc trộn cohort |
| Phản hồi reviewer | [response_to_reviewers.md](../../../revision/response_to_reviewers.md), [reviewer_matrix.csv](../../../revision/reviewer_matrix.csv) | Cập nhật trên nhánh tác vụ từ develop; mỗi yêu cầu dẫn đúng evidence, version và vị trí bản thảo |
| Quy ước bài báo cũ | [manuscript_blueprint.md](../../../revision/manuscript_blueprint.md), [author_metadata.md](../../../revision/author_metadata.md), [target_contract.md](../../../revision/target_contract.md) | Đọc quy ước khoa học/tác giả; các chỉ dẫn branch/tiến độ cũ được thay bằng hướng dẫn hiện hành này |
| Bằng chứng fix | [outputs/revision](../../../outputs/revision), [revision](../../../revision) | Giữ releases/raw/schema/source archives đã đóng băng, không chạy lại generator để ghi đè |
| Bằng chứng so sánh hợp nhất | [research U08](unified_live_research.zip), [analysis U09](unified_analysis_results.zip), [acceptance](unified_analysis_acceptance.json) | U08/U09 là nguồn kết quả mới, tách khỏi pilot48 và main fix cũ |
| Tiến độ | [docs/plan/plan.md](../plan.md), [README W12](README.md) | Đầu mối duy nhất cho công việc mới; tiếp tục tuần sau trong cùng cây docs/plan |
| Lịch sử kế hoạch phản biện | [root plan.md](../../../plan.md), [revision/README.md](../../../revision/README.md) | Tham chiếu lịch sử; không khôi phục luồng tách riêng trên fix hoặc quyền chạy cũ |

Toàn bộ đường dẫn trong bảng nằm trong checkout develop. `.github/workflows/deploy.yml`
của fix đã ngừng dùng khi chuyển deployment sang Oracle VM; không khôi phục
workflow tự xuất toàn repository lên GitHub Pages. Nội dung cũ vẫn truy nguyên
được từ commit donor.

## Tiếp tục bài báo và xử lý reviewer

U10 là công việc tiếp theo, theo [kế hoạch hợp nhất](fix_develop_integration_plan.md#8-cập-nhật-bài-báo-và-tiêu-chí-bàn-giao).
Không coi việc chuyển branch là đã cập nhật bài báo hoặc đáp ứng reviewer.

1. Lấy bản thảo hiện có trên develop làm nền, giữ quy ước tác giả. Đối chiếu
   từng yêu cầu reviewer với response/matrix và bằng chứng đã có; trạng thái cũ
   không tự áp dụng cho nghiên cứu mới.
2. Cập nhật Methods/Experimental setup theo tám vai trò, native/common,
   profile causal, cohort 102 điểm, ba Decision repeat và một upstream realization.
3. Sinh bảng mới từ U09: hai family, bridge, support/fallback, economics và
   sensitivity. Báo riêng study fix, pilot48 và U08/U09; không trộn predictions
   hoặc nhận 2.448 forecast slots là 2.448 calls độc lập.
4. Cập nhật giới hạn và trả lời reviewer đúng evidence. Native causal FAIL,
   whole-system NOT_CERTIFIED, ít temporal clusters và các ablation deferred
   vẫn phải hiển thị. Không nhận superiority chỉ vì cải thiện so common.
5. Đóng băng nguồn trước/sau sửa bài, tạo release mới với manifest liên kết
   nguồn CSV/JSON, rồi build/render kiểm PDF và cập nhật vị trí response.
   Giữ toàn bộ releases cũ nguyên byte; bàn giao theo checklist W12.

`scripts/build_revision_manuscript.py` là generator có hợp đồng release lịch
sử, không phải lệnh một bước để cập nhật U09 vào bài. Chế độ build có thể ghi
`paper/`; phải đọc scope và chọn namespace mới trước khi dùng. Không chạy
finalizer cũ để ép bản thảo mới khớp receipt cũ.

## Kiểm chứng và khôi phục trên develop

Khi nguồn chưa đổi, có thể kiểm đối soát hiện hành bằng các lệnh offline:

```powershell
py -3.13 -X utf8 scripts/verify_unified_evidence.py
py -3.13 -I -X utf8 scripts/unified_analysis/run.py verify
```

Lệnh thứ nhất kiểm cây/evidence đã khóa U01/U02; lệnh thứ hai kiểm source,
runtime, assets và tái lập 15 artifact U09 trong thư mục tạm, không inference.
Khi U10 chủ động sửa paper/revision, verifier U01 không còn là gate của nguồn
bản thảo mới: dùng snapshot/source ZIP lịch sử và release mới có provenance,
không sửa hash expected hoặc tắt guard để nhận PASS. Những receipt có pin
README/code/runtime cũng chỉ chứng nhận đúng phiên bản của chúng.

Một checkout Git không tự cung cấp mọi asset ignored như model weights,
giá hoặc quota ledger. Trên workspace này giữ các asset hiện có; khi chuyển
máy, dùng runbook/gói handoff và đối soát source/runtime/data hashes. Không
tạo lại dữ liệu hay gọi API vì thiếu file mà chưa kiểm archive và nguồn đã khóa.

F01 đã chốt [mapping hai study và lệnh historical restore](final_evidence_map.md),
[snapshot nguyên byte](final_evidence_snapshot.zip) và
[kết quả smoke/hash](README.md#f01--nguồn-và-historical-replay).
Khi paper/UI thay đổi, dùng checkout biệt lập tại commit snapshot và overlay
đúng nguồn đã khóa để chạy verifier lịch sử; không đưa code ZIP vào import
path Flask hoặc sửa receipt cũ để nhận bản thảo/ứng dụng mới.

Các chỉ dẫn lịch sử ở root plan/revision mô tả đợt trước. Hướng dẫn branch và
tiến độ hiện hành tại đây được ưu tiên cho công việc mới; các protocol khoa học,
quyền gọi API, điều kiện công bố và raw evidence của từng release vẫn giữ scope
riêng. Tập trung công việc về develop không mở lại run đã hủy hoặc quyền submit.
