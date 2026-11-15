# Sổ nguồn và đối chiếu bằng chứng khóa luận

## 1. Thông tin tác giả và yêu cầu trình bày

Thông tin được ghi nhận ngày **14/11/2026** từ yêu cầu và phản hồi trực tiếp
của tác giả trong phiên làm việc này. Bảng dưới phân biệt yêu cầu tác giả đã
chốt với quy định chính thức chưa được cung cấp. Nội dung bìa tiếng Anh nằm
tại [frontmatter.md](frontmatter.md); hồ sơ này dùng để quản lý nguồn.

| Trường | Giá trị | Nguồn và phạm vi xác nhận |
| --- | --- | --- |
| Cơ sở đào tạo | VIETNAM NATIONAL UNIVERSITY, HANOI; UNIVERSITY OF ENGINEERING AND TECHNOLOGY | Hai trang đầu PDF mẫu; tác giả yêu cầu giữ nguyên cơ sở đào tạo. |
| Tác giả | Phan Hoang Dung | Tác giả cung cấp trực tiếp; bìa dùng PHAN HOANG DUNG theo kiểu chữ hoa của mẫu. |
| Mã sinh viên | 23020346 | Tác giả bổ sung trực tiếp; không dùng mã 23020332 trong tên file mẫu. Mẫu không in mã sinh viên trên hai bìa nên bản xem bìa cũng không thêm trường này. |
| Tên đề tài | Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market | Tác giả cung cấp trực tiếp; tên chuẩn khớp [dàn bài](outline.md#a-research-direction). |
| Người hướng dẫn | Dr. Tran Hong Viet | Tác giả cung cấp trực tiếp; thay toàn bộ người hướng dẫn của mẫu. |
| Ngành trên bìa | Artificial Intelligence | Giữ theo mẫu theo yêu cầu chỉ thay tên, đề tài và người hướng dẫn; chưa có hồ sơ ngành/chương trình chính thức riêng. |
| Loại tài liệu | BACHELOR'S GRADUATION THESIS | Giữ theo hai bìa mẫu. |
| Địa điểm/năm trên bìa | HA NOI - 2026 | Giữ theo mẫu theo yêu cầu tác giả; không suy ra hạn nộp hay ngày bảo vệ. |
| Logo | Logo UET gốc, chỉ ở bìa ngoài | Sao chép nguyên byte từ `Latex/images/UET_logo.jpg` vào [tài nguyên khóa luận](assets/figures/UET_logo.jpg). Bìa trong mẫu không có logo. Quyền phát hành lại ngoài phạm vi khóa luận chưa được xác minh. |
| Mẫu trình bày đã chọn | Hai trang đầu [23020332_Tran_Xuan_Bao.pdf](../23020332_Tran_Xuan_Bao.pdf) | Yêu cầu trình bày của tác giả, không phải chứng cứ trường đã phê duyệt toàn bộ mẫu. |
| Hạn nộp/ngày bảo vệ | Chưa xác định | Tác giả xác nhận tạm thời chưa có hạn nộp; không tự đặt ngày. |
| Quy định trích dẫn chính thức | Chưa được cung cấp | Tác giả xác nhận tạm thời chưa có; numeric theo thứ tự xuất hiện chỉ là gợi ý từ `biblatex` trong mẫu, chưa chốt thành quy định. |
| Quy định bố cục chính thức | Chưa được cung cấp | Tác giả xác nhận tạm thời chưa có; A4, cỡ thân bài 12 pt, giãn dòng 1,5, lề và đánh số trang là quan sát từ nguồn mẫu. |
| Biểu mẫu bắt buộc, lời cam đoan, chữ ký, phê duyệt | Chưa xác định | Chưa nhận văn bản chính thức hoặc phê duyệt; không sao chép lời cam đoan/chữ ký của tác giả mẫu. |

### Đối chiếu hai trang bìa

- Giữ A4, Latin Modern, hai dòng tên trường, khung đôi và vị trí logo/tác giả
  theo mẫu; logo rộng `0.25\textwidth`. Khung ngoài cách trái 2 cm, trên
  1,5 cm, phải 1,5 cm, dưới 2 cm; khung trong lùi 0,15 cm.
- Bìa ngoài có logo, bìa trong có Supervisor; cả hai không có số trang.
- Theo đính chính tiếp theo ngày 14/11/2026, toàn dòng Supervisor được căn
  giữa theo trục trang; bỏ độ thụt trái của nguồn bìa mẫu.
- Đề tài mới dài hơn đề tài mẫu, nên giữ cỡ `\Large` và chia thành năm dòng
  nhất quán trên hai bìa. Bìa trong giảm khoảng trắng quanh tiêu đề để giữ
  khoảng tách với loại khóa luận/ngành/người hướng dẫn. Đây là điều chỉnh
  dàn dòng cho nội dung mới, không phải tuyên bố đồng nhất từng pixel.
- [Nguồn bìa độc lập](latex/frontmatter/covers.tex) và
  [trình biên dịch bản xem](latex/covers-preview.tex) chỉ phục vụ kiểm yêu cầu
  bìa đã cung cấp sớm; chưa thay thế khung LaTeX toàn văn hay hoàn tất phần đầu.
  [Bản PDF xem bìa](release/covers-preview.pdf) không phải bản khóa luận hoàn chỉnh.
- Markdown vẫn là nguồn nội dung chính. Khi đổi metadata tại
  `frontmatter.md`, phải đồng bộ bản trình bày LaTeX và biên dịch/kiểm lại PDF;
  chưa có chuyển đổi nguồn bản nộp sang LaTeX.

Thông tin còn thiếu chỉ chặn phần hoàn thiện phụ thuộc nó: mã chương trình
chính thức nếu khác ngành trên mẫu, biểu mẫu/câu chữ bắt buộc, kiểu trích dẫn,
giới hạn số trang, quy cách đóng/nộp và hạn nộp. Có thể tiếp tục viết nội dung
kỹ thuật. Hồ sơ yêu cầu đầy đủ theo nghĩa mỗi trường đã có nguồn hoặc ghi rõ
chưa xác định; không có nghĩa các yêu cầu nộp đã được trường xác nhận.

## 2. Phạm vi nghiên cứu và ranh giới luận điểm

[Dàn bài §A](outline.md#a-research-direction) là nơi giữ tên đề tài, RQ1–RQ4,
đóng góp và phạm vi sáu chương đã rà. Không sao chép thêm một bảng trạng thái
ở đây. Đối chiếu dùng cây nguồn
`develop:896353b3e07dc3d7fbae328fb647fd3dd738c15c` làm mốc khảo sát; các file
live dưới đây chỉ xác nhận thành phần đang tồn tại. Kết quả nghiên cứu phải
dùng nguồn/runtime được khóa trong receipt tương ứng, không lấy HEAD live
thay thế.

### Nguồn đối chiếu cho câu hỏi và giới hạn

| ID nguồn | Nguồn | Vai trò trong lần rà này | Giới hạn |
| --- | --- | --- | --- |
| S01 | [Thiết kế thực nghiệm](../paper/content/experimental_setup.tex), [support thành phần](../paper/content/tables/component/scope.tex) | RQ1: Full/Base, đối chứng số, panel upstream/factorial, đơn vị và sự khác biệt hai nghiên cứu. | Bản thảo/bảng dẫn tới bằng chứng; kiểm kê nhóm nguồn ở mục 3; truy vết từng ô khi dựng bảng khóa luận. |
| S02 | [Kết quả](../paper/content/results.tex), [bảng support ngữ cảnh](../paper/content/tables/historical_context/support.tex) | RQ2: hai họ so sánh với Common/Native, fallback và độ phủ. | Không suy kết quả dùng prior thường xuyên từ tên phương pháp; luôn giữ support và trường hợp fallback. |
| S03 | [Registry](../core/variant_registry.py), [policy](../core/mt_bicl_policy.py), [bridge](../paper/content/tables/historical_context/bridge.tex) | RQ3: tám vai trò, phụ thuộc Common/Fact Anchor/MT-BICL, proposal/final action và điều kiện utility. | Mã live là nguồn giải thích; bridge là mô tả các can thiệp gộp, không cô lập student. |
| S04 | [Receipt phân tích U09](../docs/plan/week12/unified_analysis_acceptance.json), [gói kết quả](../docs/plan/week12/unified_analysis_results.zip) | RQ4: định danh nghiên cứu, 102 điểm/2.448 slot, cold replay 15 artifact và phạm vi audit được ghi nhận. Hash ZIP hiện tại khớp `payload.results_package.sha256`. | Chỉ kiểm hash gói/đọc receipt trong lần này; không chạy lại replay hoặc gate runtime, không tự chứng nhận toàn hệ. |
| S05 | [Hạn chế](../paper/content/limitations.tex), [trạng thái tích hợp](../docs/plan/plan.md) | Giữ các kết luận âm, nhân quả, provenance, ablation chưa chạy và UI chưa nghiệm thu. | F11 vẫn PENDING; trạng thái tài liệu không đóng nghiệm thu ứng dụng. |

Các điểm chặn cách diễn giải đã đối chiếu:

1. Full/Base là so sánh trong nghiên cứu thành phần. Native/Common là cầu
   nối profile trong nghiên cứu ngữ cảnh, thay cả biểu diễn Alpha và chỉ dẫn;
   **Base không phải Common**. Không gộp response hai nghiên cứu thành một mẫu.
2. Nghiên cứu ngữ cảnh có 102 điểm, ba repeat và tám vai trò: 2.448 slot.
   Repeat của Decision giữ nguyên một realization upstream; không tăng số
   quan sát thị trường hoặc đo toàn bộ biến thiên đa agent.
3. C2 và B_semantic chỉ có ba raw Decision mỗi phương pháp; A_tp_pool có 24.
   MT-BICL trùng Fact Anchor ở 302/306 hành động cuối. Những số này được dùng
   để giới hạn câu hỏi quy thuộc cơ chế, không thay cho phân tích kết quả.
4. Mọi return trung bình của tám vai trò nghiên cứu đều âm. Lợi thế Bayesian
   v1 so với Common trong band mô tả không chứng minh vượt Native hay sinh lời.
5. Native row-wise causal vẫn `FAIL`; whole-system causal vẫn
   `NOT_CERTIFIED`. Kiểm cutoff bên ngoài không khắc phục nhân quả từng hàng.
   Khác biệt return bank/query 828/852 bản ghi không phải số nhãn đã đổi.
6. Retrieval-only, statistics-only, no-prior, no-target, no-utility và tách
   student/policy chưa có kết quả trong nghiên cứu ngữ cảnh thống nhất.
   Không dùng panel factorial thành phần để nhận thay các ablation này.

### Định danh nguồn đã dùng trong lần rà

SHA-256 dưới đây là hash toàn file tại thời điểm khảo sát. Đây là danh sách
nguồn tối thiểu cho metadata và phạm vi của lượt T01–T02; kiểm kê hai nghiên
cứu được bổ sung tại mục 3. Nguồn mẫu gốc đang nằm ngoài Git; logo cần thiết đã được đưa vào
cây `thesis/` để bản xem không cần đọc `Latex/` khi biên dịch.

| Đường dẫn | SHA-256 |
| --- | --- |
| `23020332_Tran_Xuan_Bao.pdf` | `885413c427959b34e7ed5370fe516d9a4364499bfc8f7589517522d875138b15` |
| `Latex/chapters/00_covers.tex` | `86a51194673f34c242415b6620caeadf229828a070261e5bcf03916c8722fb78` |
| `Latex/preamble.tex` | `6d16f909215eb82924d91cb8cbdeefcfbbb4d24f30648b4534c66f9b136aaf48` |
| `thesis/assets/figures/UET_logo.jpg` | `d71ffc8c4e8d40e1497d54c1fb25621bcd8ef8c0ad0cb73ee0c356980be66229` |
| `core/variant_registry.py` | `30067f05c3b59c8fc3a44bdc3cd55f9adeb3796b21ee2b39c129355781938ae8` |
| `core/mt_bicl_policy.py` | `301525c36c150e21f09a1971101d53d5927cf38c1d2921017c477441e097b488` |
| `paper/content/experimental_setup.tex` | `a6328ee5892106e9e98a2ee40aac81ca8ec7bafa6b35dcc321a87c59a6df1ccc` |
| `paper/content/results.tex` | `c7b61e835ba4b41d4605b65b5531af21444f01cd226260cc42951a073b6380cd` |
| `paper/content/limitations.tex` | `5a88b722c31bdfdaaefe0718e983379e6a7857a728532c7838dfba874044afe4` |
| `docs/plan/week12/unified_analysis_acceptance.json` | `6b435c21c89000775be1f1e1d043b6b3429a0729f37efc16f4bd03be92355456` |
| `docs/plan/week12/unified_analysis_results.zip` | `e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9` |

## 3. Kiểm kê nguồn hiện tại và hai nghiên cứu đã khóa

Kiểm kê ngày **14/11/2026**, từ cây nguồn
`b9ce7ce34989a83cb95ae625daf936da7bc11966`. Chỉ đọc artifact, kiểm hash và
đếm support đã lưu; không sinh lại dự báo, nhãn, metrics hoặc bootstrap.
Đường dẫn `outputs/revision/...` trong kho có thể là **đường dẫn gốc đã
đóng gói**, không phải thư mục hiện còn trên đĩa.

### 3.1. Các lớp phiên bản và cách truy cập

| Lớp nguồn | Định danh và nơi đọc | Cách dùng |
| --- | --- | --- |
| Mã triển khai hiện tại | Commit khảo sát ở trên; các module trong [dàn bài §D](outline.md#d-implementation-and-evidence-map). | Giải thích hệ thống hiện tại và lớp UI; không thay hash nguồn đã khóa trong receipt. |
| Snapshot nghiên cứu chung | [final_evidence_snapshot.zip](../docs/plan/week12/final_evidence_snapshot.zip), commit `384725a66fec074700963fac67c358b28b842092`, donor `9efd23f4157e0d3ab8069fccab7dccf03439a714`. | Đã đối soát 810 member nguồn với `snapshot_manifest.json`; bản nguồn đúng byte để truy xuất nghiên cứu. |
| Nghiên cứu thành phần | `legacy_fix_revision`; run signature `904b838a466290d9c8aa73245a6285e813b4f7c90d280355d3b2847ed9933fab`; `revision_minimal_final_v1` và các release trong mục 3.2. | Nguồn chính là dữ liệu/manifest đã khóa; không chọn bản có tên “final” chỉ theo tên. |
| Thu thập ngữ cảnh lịch sử | `unified_u08_u09_r1`; U08 source commit `69935d71b469d0a34ef8959ca598e1cee791f7ac`, `unified_live_research.zip`. | Giữ active slots, raw/journal, retired attempts và acceptance của lượt hoàn tất. Pilot48/lượt hủy không thay cho dataset này. |
| Phân tích ngữ cảnh lịch sử | U09 source commit `ae90d995a27f8d7820d88a7181a64f55b92b43d9`; `unified_analysis_results.zip` cùng acceptance. | 15 artifact phân tích và `receipt.json`; đọc kết quả đã lưu, không tái ước lượng. |
| Bản trình bày bài báo hiện tại | [paper/](../paper/README.md), [outputs/paper/manifest.json](../outputs/paper/manifest.json). | Đã đối chiếu 49 file nguồn và hai PDF với manifest. Bảng/hình đã biên tập là đường dẫn tìm nguồn; không thay dữ liệu nghiên cứu. |
| Artifact trung gian trình bày U09 | `outputs/revision/u09_manuscript_assets_v1/manifest.json` và `artifacts/`. | Đã kiểm 26 output theo manifest, gồm supplement và numeric lineage; không ghi đè bằng bộ sinh mới. |

**Xác nhận phạm vi cùng snapshot nghiên cứu:** theo tác giả ngày 14/11/2026,
Indicator, Decision và graph giữ kết quả/logic nghiên cứu, chỉ bổ sung đường
trình bày UI. Đối chiếu diff xác nhận Indicator thêm capture, graph bọc client
trình bày; các wrapper chuyển tiếp lời gọi gốc khi capture tắt. Decision giữ
trần prompt ở `is_backtest=True`; phần thay đổi điều kiện áp dụng cho realtime.
Vì vậy, trong phạm vi khóa luận này, ba module được coi **tương đương với
snapshot về đường nghiên cứu/backtest**, không tách thành nghiên cứu mới và
không mở lại nghiệm thu. Hai hash trong bảng chỉ nhận diện file đóng băng và
lớp UI hiện tại, không hàm ý kết quả thực nghiệm đã thay đổi.

| Module | SHA-256 nguồn trong snapshot | SHA-256 file hiện tại có lớp UI |
| --- | --- | --- |
| `agents/indicator_agent.py` | `470fa5d1f4350180a23bfe40564cd6c02e00b8939cd2d90cad775776f74ee57b` | `a42f3e46772253d6eb209ac6624a2473ccb94569b58616822eeb0a3162900a21` |
| `agents/decision_agent.py` | `a7ed07e310652cfc0de1b1d15ec2bad1a03eeebd6be6a4144b5146c52df118a9` | `4e43ca18ccc396b54204065d629f7edcc643823d5a0d46415cd516036f273601` |
| `utils/graph_setup.py` | `61bc18bad7bf83a96ee2a862589fba20d5e5b398124132a8fb815d0771c13acf` | `9bc12d7484279de565494a016fe6d0a9f80567a1833d23f6af89aaf67254247b` |

Trong 16 module chính đã đối chiếu, 13 file còn lại đồng nhất byte:
Pattern, Trend, Alpha, Sentiment, backtest engine, registry, BayesianRetriever,
MT policy, hai student implementation, MT tasks, unified methods và protocol.
Nhận định tương đương ở trên là xác nhận tác giả cộng kiểm đường mã liên quan,
không phải một lượt gọi mô hình hoặc kiểm thử thực nghiệm mới. Profile UI
realtime song ngữ vẫn được mô tả riêng khi viết phần ứng dụng.

### 3.2. Nguồn nghiên cứu thành phần

`outputs/revision/final_baselines_v1/` còn ở cây làm việc; 11 output đều khớp
manifest. Các nhóm dưới đã chuyển vào [kho revision](../docs/plan/revision_evidence/README.md).
[index.json](../docs/plan/revision_evidence/index.json) ánh xạ đường dẫn gốc
đến chunks và SHA-256; reader kiểm phần ZIP, từng chunk và toàn file trước
khi trả nội dung. Đã kiểm đủ **179 file thuộc bảy nhóm**, tất cả là
`local_only=false`, không cần model weights riêng tư để đọc các kết quả này.

Tên nhóm ở bảng được đặt sau tiền tố `outputs/revision/`. Hash là **toàn
file `manifest.json`**, khác digest semantic có thể nằm bên trong JSON.

| Nhóm | File đã kiểm | Nội dung/support | SHA-256 manifest |
| --- | --- | --- | --- |
| `final_repeats_v1` | 19 | Hai panel chín đơn vị; protocol, ba execution, contrasts và donors. | `4faad32ced5d2569d12106dd776fe1e69c8dcf8340ac9b93df392e0db9f2e4df` |
| `final_temporal_v1` | 20 | 102 điểm chính và các sensitivity cohort chồng lấn; phân tầng, regime và phụ thuộc. | `72590009b448ef4de1fc93b1bd4cd2cb9fa0b0d71a780a3cb5ab70c01e77a1db` |
| `numeric_controls_v1` | 80 | 23 chiến lược × 102 điểm = 2.346 dự báo số; 51 fit scope; 20 trial random-five. | `0ed26b01cde685a443950cb2d0ede21b931e5b81ce292c33e77c2eb373e23ec8` |
| `execution_final_v1` | 8 | 12 kịch bản kinh tế; nhãn và dự báo gốc giữ nguyên. | `428968dedcad93691eb37137fecd5e656e83d16c704287afb9c9a72e0e21327e` |
| `manuscript_rewrite_v1` | 26 | Generation, numeric_cells, headline và các ZIP nguồn bản thảo lịch sử. | `fb73df6e8a28d3d69a73fcb70eec1e9ce2025e87374add60bde007ebb49b0440` |
| `final_contracts_v1` | 7 | Targets, chỉ báo và quy ước rủi ro đã chốt. | `24bc892b572c0c09e49abd076276ce3bf4f248de4def4337936e6804500b1e9b` |
| `revision_minimal_final_v1` | 19 | Main/panel records, predictions, nhãn, pairing, chi phí và lineage. | `5ccb426ab41088a7ff3956e229802a3a8e8c23a9980db93be602c9499d9279f1` |

| Kết quả định lượng dự kiến | Artifact nguồn có thể đọc | Support và giới hạn |
| --- | --- | --- |
| Full/Base, numerical baselines, confusion, pooled/macro và tài khoản | `final_baselines_v1/{classification,per_class,macro,financial,accounts,main_comparison}.csv`; `revision_minimal_final_v1/{main_predictions,records,summary}.json`. | Main 102 điểm, 25 UP/77 DOWN, chín mã/12 ngày/sáu block, 51 tài khoản và 204 Decision Full/Base. Các đối chứng số dùng cùng main support nhưng không thêm quan sát thị trường. |
| Biến thiên upstream và factorial/placebo | `final_repeats_v1/{protocol,panels,ba_family}.json`, `{repeat_summary,contrasts,disagreement,lineage,donors,pairing}.csv`. | Hai panel riêng, mỗi panel chín đơn vị, ba execution; upstream chín mã/ba ngày, factorial tám mã/bốn ngày. 204+54+135−18 = 375 Decision duy nhất, không cộng support của các panel thành N độc lập. |
| Phụ thuộc thời gian và phân tầng | `final_temporal_v1/{primary_dependence,stratified_metrics,block_sensitivity,panel_hac}.json` cùng CSV. | Main 102; common-eight 96; recent-nine 54, các cohort chồng lấn. Seed bootstrap thành phần `20261102`, 10.000 draw; post-inference/descriptive. |
| Đối chứng lựa chọn factor và độ phân tán random-five | `numeric_controls_v1/{run,summary,test_predictions,random_dispersion,inference}.json`, `resampling.npz`. | 23 chiến lược, 2.346 test predictions trên cùng 102 điểm; 20 trial random-five. Không phải ablation selector của pipeline LLM. |
| Kịch bản chi phí/thanh toán/khớp lệnh | `execution_final_v1/{policy,report}.json`, `{scenario_summary,account_results}.csv`, `daily_ledger.csv.gz`. | 12 kịch bản; dự báo/nhãn cố định. Không phải mô phỏng đã chứng nhận venue hoặc cận worst-case toán học. |
| Targets, chỉ báo, risk và provenance của số đã trình bày | `final_contracts_v1/{targets,indicators,report}.json`; `manuscript_rewrite_v1/{generation,numeric_cells,headline_values}.json`. | Có đường truy vết literal/đơn vị/nguồn cho bảng cũ. Khi dựng bảng khóa luận phải nối từng ô đến dữ liệu này; chưa coi bảng luận văn đã hoàn tất. |
| Chi phí gọi, retry, sentiment và lineage thành phần | `revision_minimal_final_v1/{attempts,costs,lineage,numeric_provenance,price_quality}.json`; records/pairing cùng nhóm. | Chỉ báo trường đã ghi; latency/usage thiếu không tự điền. Báo cáo không thay việc xác thực lịch sử tin hoặc đánh giá sentiment trên tập nhãn độc lập. |

Đọc trực tiếp bằng `EvidenceArchive.read(đường_dẫn_gốc)`; không chạy Python
được đóng gói trong ZIP. Nếu cần khôi phục để dựng bảng, dùng
`scripts/revision_evidence.py restore <nhóm> --destination <thư_mục_mới>`;
không ghi đè nguồn lịch sử. Bốn phần đã kiểm hash khi đọc các nhóm trên:

| Phần trong `docs/plan/revision_evidence/` | SHA-256 |
| --- | --- |
| `part-003.zip` | `c04a7ea966af44cd408c0c5e9b6d21bd8428dfbc43afcf755ddcc23fa97866a2` |
| `part-004.zip` | `8e6fde14ad92dad2cffb5ee5c4b90c50051b47e49c5453a72694af5325388d1a` |
| `part-005.zip` | `0fa9c21c602a5c2d9bdf09927c06bcaa32dac68506a376148efcabec998c967e` |
| `part-013.zip` | `2fc7f4fe68cf2045e64e63b0033472dfb15a17246060ade9f6ffd7cc3fbe41ad` |

### 3.3. Nguồn nghiên cứu ngữ cảnh lịch sử

Đã đọc qua consumer chỉ đọc `core/manuscript_u09/sources.py`: kiểm pin ngoài,
manifest/member U08/U09, envelope receipt và 15 artifact với acceptance, rồi
kiểm support/identity đã lưu. **Không chạy `analyze`, cold replay, refit hoặc
inference.** Gói U08 có 8.035 journal file và 8.064 member cả manifest;
U09 có 24 member, trong đó 15 artifact phân tích cộng một receipt ở namespace
`outputs/unified_integration/u09_analysis_r1/`.

Support: **102 điểm/chín mã/12 ngày/sáu fold/51 tài khoản**, một upstream
realization mỗi điểm, ba Decision repeat, tám vai trò = **2.448 forecast slot**.
BHN có sáu điểm, mỗi mã còn lại 12. Có 79/102 điểm thiếu sentiment. Kiểm đếm
từ bản ghi cho 1.290 raw Decision response và 1.158 slot bypass; các slot
bypass giữ trong kết quả chính, không phải lỗi bị loại. Số HTTP attempt và
retired raw phải đọc ledger U08 riêng, không đồng nhất với 1.290 response.

| Vai trò | Raw Decision response | Slot bypass trên 306 |
| --- | --- | --- |
| `original_fix` | 306 | 0 |
| `original_common` | 306 | 0 |
| `bayesian_v1` | 144 | 162 |
| `C2` | 3 | 303 |
| `A_tp_pool` | 24 | 282 |
| `B_semantic` | 3 | 303 |
| `MT_BICL` | 198 | 108 |
| `Fact_Anchor` | 306 | 0 |

| Kết quả định lượng dự kiến | Member sau tiền tố namespace U09 | Quy ước cần giữ |
| --- | --- | --- |
| Mười hàng phương pháp/đối chứng và các chỉ số chính | `results.json`, `summary.csv`, `classification_by_repeat.csv`. | Tám vai trò cộng CASH/Always-LONG; return trung bình qua repeat trong tài khoản rồi qua 51 tài khoản; BA tính mỗi repeat rồi trung bình. Không ghép thành portfolio. |
| Hai họ contrast, ba bridge và band | `contrasts.csv`, `bridge.csv`, `results.json/primary_joint_family`. | 20 contrast return/BA; 10.000 draw, seed `20261110`, block length 2. Khác giao thức thành phần; band mô tả trên sáu fold đã exposed. |
| Support, fallback, membership, ví dụ và policy | `predictions.csv`, `prior_traces.json`, `results.json/coverage`; summary/policy reasons. | Signal bank phủ FPT/MWG/VCB/VNM, khác context tác vụ số. MT trùng anchor ở 302/306 hành động cuối; raw proposal khác final action. Tuổi/similarity chỉ báo khi trace thực sự ghi. |
| Phân tầng theo mã/fold/repeat và sensitivity | `classification_by_group.csv`, `per_repeat.csv`, `results.json/sensitivity`. | L1/L3, leave-one-fold/symbol-out, CORE4 là sensitivity/secondary; không chọn subset/repeat đẹp nhất. |
| Kinh tế, chi phí, turnover, exposure và drawdown | `accounts.csv`, `cycles.csv`, `daily_nav.csv`, `results.json`. | Cash/action theo hợp đồng chuẩn, không annualize lịch rời rạc sai cách, giữ NA và mẫu số. |
| Kiểm toán và tài nguyên vận hành | `receipt.json`, `results.json/telemetry`; các member `evidence/u09_*.json`; U08 `acceptance/` và journal slots/attempts/raw. | Receipt ghi PASS lịch sử, không ghi là đã chạy lại. Native row-wise causal FAIL; whole-system NOT_CERTIFIED; UI/F11 vẫn PENDING. |

### 3.4. Runtime, model và định danh gói

- Thành phần: `revision_minimal_final_v1/manifest.json/runtime` ghi Python
  **3.13.5**, numpy 2.1.2, pandas 2.3.3, scipy 1.16.1, scikit-learn 1.7.2,
  TA-Lib 0.6.8, groq 0.37.1, langchain-core 1.2.17, langchain-groq 1.1.2 và
  pydantic 2.11.7. `reproducibility_v1/runtime.json` giữ runtime frozen T04/T07
  và quan sát lúc đóng gói; đây là mã task lịch sử của nghiên cứu thành phần,
  không phải task cùng số trong kế hoạch viết. Không dùng môi trường hiện
  tại suy ngược runtime.
- Ngữ cảnh: U06 manifest v2 khóa Python **3.13.5/107 package**; U08 live
  runtime khóa model aliases/options, source bindings và call policy; U09
  analysis runtime khóa các nguồn phân tích. Phiên này dùng Python 3.13.5
  để đọc nhưng không tuyên bố đã đối soát lại toàn bộ 107 package.
- Đã kiểm toàn bộ **286 asset** trong `unified_comparison_assets_v2.zip`
  theo `assets_manifest.json`, gồm prices, providers, compatibility và 51
  selector binding. Asset preparation là input/control, không phải forecast
  hosted. Không khởi tạo provider hoặc nạp model để kiểm kê.
- Ba resource sau có ngay trong snapshot nguồn, đã kiểm byte. Tiền tố là
  `outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/`; checkpoint student
  được nghiên cứu sử dụng là seed 42/step 3000 theo
  `docs/plan/week11/mt_bicl_replica_full_r1_model.json` trong snapshot,
  không lấy checkpoint mới trong cây live thay thế.

| Resource trong snapshot | Byte | SHA-256 |
| --- | --- | --- |
| `inputs/regime_models.json` | 17,700 | `5df0307a70b3df177a43faba8be04a72c00dabcb422c0b1c66a4b76cd84e724d` |
| `model/candidate.pt` | 1,098,944 | `a6f0d294b6f731bfc630fe58631b921ec2f0877338745a84e9459ec6a248e702` |
| `model/teacher.json` | 37,674 | `c0a39f327bacd8636fd7edff2f19b30799581bd144ac28176a7cd97fe9dbc335` |

| File/gói trên đĩa | Byte | SHA-256 toàn file |
| --- | --- | --- |
| `docs/plan/week12/unified_analysis_results.zip` | 1,383,945 | `e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9` |
| `docs/plan/week12/unified_live_research.zip` | 78,438,700 | `5936bc971bebf1b139a34b93f154ad8e54d0a0e37fdaa6ac4673295f8b60a11c` |
| `docs/plan/week12/final_evidence_snapshot.zip` | 93,154,448 | `80fed8c9a1c265098a394bfc40f13d7f0266c1e05abdb142fba01d873cb8b8b5` |
| `docs/plan/week12/unified_analysis_acceptance.json` | 5,064 | `6b435c21c89000775be1f1e1d043b6b3429a0729f37efc16f4bd03be92355456` |
| `docs/plan/week12/unified_comparison_assets_v2.zip` | 25,448,065 | `d5c4f1bc31c1a95d9e685a9cc13d1f86ce2d3cc0105b9023561fd5f567e2d8c4` |
| `docs/plan/week12/unified_comparison_manifest_v2.json` | 363,594 | `dff00745cb55d8e92570fd7a331e69971f241d06ca77815d0382006c67e8b30e` |
| `docs/plan/week12/unified_comparison_protocol_v2.json` | 14,563 | `b783a0d50cd03d418fdc439ee93eba76edcd1a60be063deaecf3e8259c8bb34a` |
| `docs/plan/week12/unified_analysis_runtime.json` | 3,189 | `e9638253bdf42449e6e716a48332f9fe2057443c0a774d27117b002a87c64806` |
| `docs/plan/week12/unified_live_runtime.json` | 27,845 | `2a4661d43ffde54a991cb58858c4420241645ddb1feca59f00ec875fdbdde083` |
| `outputs/revision/u09_manuscript_assets_v1/manifest.json` | 12,119 | `9633dc6de3cc036b76f503713e3bf959581d93729ef8c420e4267a26aa0ebd7b` |
| `docs/plan/revision_evidence/index.json` | 7,661,428 | `cc4400dadc585b6b0dd5dd3a012f1f510a994347b9395cdbbcc721cc9f2b9599` |
| `outputs/revision/final_baselines_v1/manifest.json` | 4,268 | `0a20fbe49049dd61fae2eb8bf3289f65039395e6bcac6745b851a5a00d804226` |
| `outputs/paper/manifest.json` | 9,888 | `ca7aa5ca0240d8d21fff21cdf251f9fd3bc7e396c39168064c6ef6206c3c4256` |

Các artifact quan trọng bên trong archive vẫn có hash riêng dưới đây.
`U09/` là namespace trong ZIP kết quả, các đường dẫn thành phần là đường dẫn
gốc qua index; toàn bộ member còn lại có binding trong manifest đã kiểm.

| Artifact | SHA-256 |
| --- | --- |
| `outputs/revision/manuscript_rewrite_v1/numeric_cells.json` | `859b534d1530072ae02251b329130572028e36a32b2b259ed5091d2d97a28cf5` |
| `outputs/revision/revision_minimal_final_v1/main_predictions.json` | `1e9e0bd1803e1f243734dc79c7ad4834d823f2b042c1daca2cada9e11ffe6840` |
| `outputs/revision/reproducibility_v1/runtime.json` | `2dd8a8a01eec23f3cd3d31760bd5c1dabcd3bc44becefda03a60b32b88c7ecd4` |
| `U09/predictions.csv` | `d7d5f9b90d009f3da31de64df067ae9ac4ff72ccd395debf6c7f8ff08aa1da32` |
| `U09/prior_traces.json` | `dff668d4841a1ff9e36bb13ae4e09f8a54e612f264cf1b9cedb94281824dea3e` |
| `U09/results.json` | `3136ab9bdeab377196236e1a01402646257ec3beb251877702dbc86e1e67e31f` |
| `U09/summary.csv` | `1173fb0e92a062137dc4a8d5b99c461723b4182c724fd0313e9c2a13ccec1d07` |

### 3.5. Thông tin thiếu và giới hạn khả dụng

| Phần còn thiếu/chưa xác minh | Cách xử lý khi viết |
| --- | --- |
| Retrieval-only, statistics-only, no-prior, no-target, no-utility và tách student/policy | Chưa có kết quả trong nghiên cứu ngữ cảnh thống nhất; chỉ mô tả khả năng/đề xuất, không tạo bảng kết quả giả. Panel factorial thành phần không thay thế. |
| Kết luận tiền cứu hoặc lợi nhuận thực thi ngoài thị trường | Chưa có; mọi mean return vai trò nghiên cứu đều âm. Không biến chênh lệch với Common thành vượt Native hoặc có lãi. |
| Ground truth tài chính cho sentiment/chart và lịch sử khả dụng của dữ liệu/tin | Chưa xác thực độc lập. Giữ thiếu sentiment, hạn chế grounding, corporate actions/membership và dữ liệu query/bank có provenance khác nhau. |
| Lỗi nhân quả từng hàng native và khác biệt return bank/query | Giữ FAIL/NOT_CERTIFIED và audit 828/852 return khác số; không viết thành 828 nhãn đổi, không sửa bằng chứng đóng băng. |
| Model weights/private bundle thành phần | Index ghi `reproducibility_v1/model_weights.zip` 390.297.384 byte và `reviewer_response_v1/private_bundle.zip` 114.784.275 byte, đều `local_only=true`. Các phần local có ở máy nhưng chưa đọc/kiểm toàn payload trong T03; clone Git không bảo đảm có. Không cần chúng để đọc metrics đã khóa hoặc U09; không hứa tái sinh scorer hay quyền phát hành. |
| Wheelhouse/interpreter và hosted revision bất biến | Chưa có gói môi trường tự đủ; immutable hosted revision trong protocol thành phần là null. Hash dữ liệu/nguồn không bảo đảm gọi model lại cho response giống byte. |
| Độ trễ/usage/tuổi ví dụ không được ghi ở một số bản ghi | Để NA hoặc thu hẹp thống kê, không suy thời gian từ thứ tự file hay tự gán tuổi/similarity. |
| Nghiệm thu ứng dụng, quyền dữ liệu/model và phê duyệt bên ngoài | UI/F11 vẫn PENDING, F12 chưa bắt đầu; quyền/PID/phản biện/nộp trường chưa được suy là hoàn tất. |

Inventory này đủ xác định nguồn có thể đọc cho các nhóm kết quả dự kiến ở
Chương 5/Phụ lục D–F và chỉ rõ các nhóm không có bằng chứng. Truy vết từng ô,
kiểm citation nguồn gốc, chọn tình huống và dựng bảng/hình vẫn thuộc các bước
viết tương ứng; lần kiểm kê không hoàn tất các chương hoặc mở rộng nghiệm thu.

## 4. Danh sách đọc nguồn gốc và quy ước khóa trích dẫn

Lập ngày **14/11/2026**, từ commit khảo sát
`e081f0c74db199018cbe8156017cb62f44410d80`. Danh sách này phục vụ chuẩn bị
đọc và kiểm nguồn; không phải bản Related Work hay bibliography đã chốt.
Đã phân nhóm **57 ứng viên hiện có** và bổ sung **hai nguồn nền tảng** còn
thiếu: MT-BICL và PFN, tổng **59 nguồn/10 nhóm**, mỗi nguồn có một khóa.
Không nhập bibliography chủ đề khác từ `Latex/references.bib` của mẫu.

### 4.1. Nguồn đầu vào và ý nghĩa trạng thái

- [paper/references.bib](../paper/references.bib) có 57 khóa duy nhất, 25
  trường DOI và 54 trường URL. SHA-256 nguyên file:
  `9912c4fa3e2acfe5c661d69b57b6e4fa11e8ea85c89cf4ad750ff87cf1494dbc`.
  Đây là nguồn **ứng viên**, không phải 57 nguồn đã đọc hoặc được chấp nhận.
- [Báo cáo truy cập references cũ](../outputs/paper/reference_links.json),
  SHA-256 `fb5d56c32c7ce1ccac09d63c9354f012626723bddb632582e0e3fd354f7806eb`,
  chỉ ghi kết quả lần kiểm bài báo trước. Không chuyển HTTP PASS cũ thành
  xác minh nội dung mới hoặc bằng chứng đã đọc toàn văn trong khóa luận.
- **CHUA_DOC:** mới lấy metadata/đường dẫn từ ứng viên, chưa đọc nội dung
  trong lượt này; cả metadata và phát biểu dự kiến còn phải kiểm nguồn gốc.
- **DA_DOC:** đã đọc phần chỉ rõ ở §4.4, thường là abstract; chưa đủ để dùng
  mọi công thức, so sánh hoặc chi tiết triển khai của toàn tài liệu.
- **DA_KIEM:** đã đối chiếu metadata/phiên bản và đoạn nguồn hỗ trợ **nhận định
  có phạm vi ghi tại §4.4**. Không có nghĩa đã đọc/kiểm mọi trang, tái lập
  kết quả, kiểm quyền phát hành hoặc xác minh ứng dụng sang thị trường Việt Nam.
- Trạng thái hiện tại: **3 DA_KIEM, 5 DA_DOC, 51 CHUA_DOC**. A = đọc trước
  khi viết phương pháp/đánh giá liên quan; B = nguồn so sánh/bổ trợ; C = đọc
  tùy mức liên quan. Ưu tiên không phải đánh giá chất lượng nghiên cứu.
- Link trong 51 dòng CHUA_DOC là **đích cần kiểm**, không phải xác nhận đã
  truy cập được. Nguồn có DOI dùng DOI để xác thực định danh; bản tác giả,
  arXiv, proceedings, trang nhà xuất bản hoặc tài liệu/model card chính thức
  được ưu tiên. HTTP 200, catalogue hoặc mục lục không chứng minh có toàn văn.

### 4.2. Quy ước khóa và điều kiện đưa vào bản thảo

1. Khóa mới dùng ASCII `firstauthorYYYYkeyword`, ví dụ `zhu2026multitask`,
   `muller2022transformers`; khóa hiện có được giữ ổn định, gồm ngoại lệ
   legacy như `tradingagents2024`, `hf5cdsentiment`, `talib_rsi_docs`.
   Trùng tác giả/năm/chủ đề thì thêm từ khóa phân biệt hoặc hậu tố `a`, `b`
   được ghi rõ; không để hai khóa cho cùng một tác phẩm chỉ do khác URL.
2. Khóa, năm xuất bản và phiên bản là ba trường khác nhau. Không suy năm từ
   khóa hoặc số arXiv: Xie dùng venue 2022 dù preprint đầu 2021; PFN dùng
   khóa năm ICLR 2022, bản arXiv đọc là v7 năm 2024. Khi có proceedings chính
   thức, chọn nhất quán edition được trích và ghi version nếu đọc preprint.
3. Tại bước kiểm bibliography, đối chiếu tên/thứ tự tác giả, tiêu đề,
   venue, năm, tập/số/trang, DOI/ISBN, URL và ngày truy cập; kiểm publication
   record thay vì tin BibTeX cũ. Không tự tạo DOI, ngày xuất bản hoặc tuyên bố
   đã peer review chỉ từ số arXiv hay comment tác giả.
4. Với arXiv, lưu ID kèm `vN` đúng bản đã đọc; không âm thầm thay latest.
   Sách lưu edition, phần/chương/trang thực đọc. Tài liệu phần mềm/model card
   lưu tổ chức, URL, version/commit và `urldate`; không bịa năm cho nguồn không
   ghi ngày. Các field metadata giữ tiếng Anh và đúng schema BibTeX.
5. Khi soạn Markdown có thể dùng `[@key]`; lúc chuyển LaTeX dùng `\cite{key}`.
   Trước khi đưa một citation vào bản thảo phải có bản ghi gồm: khóa, nguồn/
   version, đoạn/mục/trang hỗ trợ, phát biểu dự kiến bằng tiếng Anh, giới hạn
   và ngày kiểm. Một citation không được mở rộng sang nhận định chưa đọc.
   Các ghi chú ở đây bằng tiếng Việt là quản lý nguồn, không phải thân khóa luận.
6. Trích phương pháp gốc cho nguồn gốc học thuật; trích code/license và commit
   riêng khi nói dùng lại triển khai. Receipt/hash nội bộ chứng minh provenance
   thực nghiệm; không thay trích dẫn khoa học. Không xem lời tự nhận vượt trội
   trong abstract là kết luận độc lập hoặc bằng chứng hệ này sinh lời.
7. Chỉ dựng `thesis/references.bib` từ các nguồn đã kiểm cho phát biểu cụ thể ở
   bước đọc/viết tương ứng; chưa tạo file này trong T04. Không copy cả 57 mục
   rồi coi bibliography đã hoàn thành. Kiểu numeric/order ở mẫu vẫn chỉ là gợi
   ý; quy định trích dẫn chính thức của trường chưa được cung cấp.

### 4.3. Danh sách theo chủ đề

Tiêu đề/năm ở dòng CHUA_DOC là metadata ứng viên, còn có thể sửa sau đối
chiếu. Không lấy số lượng mục ở đây làm số tài liệu cuối cùng được trích.

#### Nhóm 1. Phân tích kỹ thuật, giá và alpha

Chương 2.1/3.3/4.3; phân biệt công thức gốc với phép thích nghi một mã.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `appel2005technical` | [Technical Analysis: Power Tools for Active Investors](https://www.informit.com/store/technical-analysis-power-tools-for-active-investors-9780131479029) — 2005 | A | CHUA_DOC |
| `murphy1999technical` | [Technical Analysis of the Financial Markets](https://www.penguinrandomhouse.com/books/350647/technical-analysis-of-the-financial-markets-by-john-j-murphy/) — 1999 | A | CHUA_DOC |
| `lane1984stochastic` | [Lane's Stochastics](https://store.traders.com/-v02-c03-lane-pdf.html) — 1984 | B | CHUA_DOC |
| `lo2000technical` | [Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation](https://business.columbia.edu/sites/default/files-efs/pubfiles/19268/Lo-Mamaysky_wang_foundations.pdf) — 2000 | A | CHUA_DOC |
| `grinold1999active` | [Active Portfolio Management](https://www.mheducation.com/highered/mhp/product/active-portfolio-management-quantitative-approach-producing-superior-returns-selecting-superior-returns-controlling-risk.html) — 1999 | B | CHUA_DOC |
| `kakushadze2016formulaic` | [101 Formulaic Alphas](https://arxiv.org/abs/1601.00991v3) — 2016 | A | DA_DOC (phạm vi §4.4) |
| `jegadeesh1993momentum` | [Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency](https://doi.org/10.1111/j.1540-6261.1993.tb04702.x) — 1993 | B | CHUA_DOC |
| `fama1992crosssection` | [The Cross-Section of Expected Stock Returns](https://doi.org/10.1111/j.1540-6261.1992.tb04398.x) — 1992 | B | CHUA_DOC |
| `hurst2017trend` | [A Century of Evidence on Trend-Following Investing](https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/AQR-JPM-Fall-2017.pdf) — 2017 | B | CHUA_DOC |
| `talib_rsi_docs` | [Relative Strength Index (RSI)](https://ta-lib.github.io/ta-doc/indicator/RSI.htm) — n.d. | A | DA_KIEM (phạm vi §8.5.2) |
| `talib_willr_docs` | [Williams' %R (WILLR)](https://ta-lib.github.io/ta-doc/indicator/WILLR.htm) — n.d. | A | DA_KIEM (phạm vi §8.5.2) |

#### Nhóm 2. LLM và hệ thống đa agent tài chính

Chương 2.2/4.3; nguồn kế thừa kiến trúc và các hệ so sánh; không nhập kết quả của chúng thành kết quả khóa luận.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `xiong2025quantagent` | [QuantAgent: Price-Driven Multi-Agent LLMs for High-Frequency Trading](https://arxiv.org/abs/2509.09995v3) — 2025 | A | DA_KIEM (phạm vi §4.4) |
| `tradingagents2024` | [TradingAgents: Multi-Agents LLM Financial Trading Framework](https://arxiv.org/abs/2412.20138v7) — 2024 | B | CHUA_DOC |
| `fatemi2024finvision` | [FinVision: A Multi-Agent Framework for Stock Market Prediction](https://arxiv.org/abs/2411.08899v1) — 2024 | B | CHUA_DOC |
| `wu2023bloomberggpt` | [BloombergGPT: A Large Language Model for Finance](https://arxiv.org/abs/2303.17564v3) — 2023 | B | CHUA_DOC |
| `yang2023fingpt` | [FinGPT: Open-Source Financial Large Language Models](https://arxiv.org/abs/2306.06031v1) — 2023 | B | CHUA_DOC |
| `xia2026agentictrading` | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337v2) — 2026 | C | CHUA_DOC |
| `deng2017deep` | [Deep Direct Reinforcement Learning for Financial Signal Representation and Trading](https://ieeexplore.ieee.org/abstract/document/7407387) — 2017 | B | CHUA_DOC |

#### Nhóm 3. Thị giác và kiểm hiểu biểu đồ

Chương 2.2/4.3/5.9; phân biệt biểu đồ thông thường, candlestick và limit-order book.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `han2023chartllama` | [ChartLlama: A Multimodal LLM for Chart Understanding and Generation](https://arxiv.org/abs/2311.16483v1) — 2023 | B | CHUA_DOC |
| `tsantekidis2017lob` | [Forecasting Stock Prices from the Limit Order Book Using Convolutional Neural Networks](https://pure.au.dk/portal/en/publications/forecasting-stock-prices-from-the-limit-order-book-using-convolut/) — 2017 | B | CHUA_DOC |
| `shu2026finchart` | [FinChart-Bench: Benchmarking Financial Chart Comprehension in Vision-Language Models](https://aclanthology.org/2026.acl-long.615/) — 2026 | C | CHUA_DOC |
| `wang2026martingale` | [Martingale Doppelgänger-Eval: An Identification Framework for Auditing Candlestick Understanding in Vision-Language Models](https://arxiv.org/abs/2606.17423v1) — 2026 | C | CHUA_DOC |

#### Nhóm 4. Sentiment tài chính và NLP tiếng Việt

Chương 2.2/3.3/4.3; backbone, classifier, miền dữ liệu và scoring recipe là các đối tượng khác nhau.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `nguyen2023visobert` | [ViSoBERT: A Pre-Trained Language Model for Vietnamese Social Media Text Processing](https://aclanthology.org/2023.emnlp-main.315/) — 2023 | A | DA_DOC (phạm vi §4.4) |
| `hf5cdsentiment` | [5CD-ViSoBERT for Vietnamese Sentiment Analysis](https://huggingface.co/5CD-AI/Vietnamese-Sentiment-visobert) — n.d. | A | DA_KIEM (phạm vi §4.4) |
| `araci2019finbert` | [FinBERT: Financial Sentiment Analysis with Pre-trained Language Models](https://arxiv.org/abs/1908.10063v1) — 2019 | B | CHUA_DOC |
| `tetlock2007news` | [Giving Content to Investor Sentiment: The Role of Media in the Stock Market](https://business.columbia.edu/sites/default/files-efs/pubfiles/3097/Tetlock_Media_Sentiment_JF.pdf) — 2007 | B | CHUA_DOC |
| `wolf2020transformers` | [Transformers: State-of-the-Art Natural Language Processing](https://aclanthology.org/2020.emnlp-demos.6/) — 2020 | B | CHUA_DOC |

#### Nhóm 5. Regime, HMM và Bayes nền tảng

Chương 2.3/3.4–3.6; lọc so với làm trơn, học tham số, posterior và bất định. Bayesian bootstrap chỉ dùng khi khớp phép tính thực tế.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `rabiner1989hmm` | [A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition](https://web.mit.edu/6.435/www/Rabiner89.pdf) — 1989 | A | DA_KIEM (forward/backward §III.A–B; §8.5.3) |
| `hamilton2005regimes` | [Regime-Switching Models](https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf) — 2005 | A | DA_DOC (định nghĩa state/transition; §8.5.3) |
| `dempster1977em` | [Maximum Likelihood from Incomplete Data via the EM Algorithm](https://web.mit.edu/6.435/www/Dempster77.pdf) — 1977 | A | CHUA_DOC |
| `gelman2013bayesian` | [Bayesian Data Analysis](https://sites.stat.columbia.edu/gelman/book/) — 2013 | A | CHUA_DOC |
| `rubin1981bootstrap` | [The Bayesian Bootstrap](https://doi.org/10.1214/aos/1176345338) — 1981 | A | CHUA_DOC |

#### Nhóm 6. ICL, truy xuất và MT-BICL

Chương 2.4–2.5/3.6/4.8; tách few-shot, implicit Bayes, PFN và context đa tác vụ. Hai khóa mới là đề xuất cho bibliography khóa luận.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `xie2022implicitbayes` | [An Explanation of In-context Learning as Implicit Bayesian Inference](https://arxiv.org/abs/2111.02080v6) — 2022 | A | DA_DOC (phạm vi §4.4) |
| `rubin2022retrieve` | [Learning To Retrieve Prompts for In-Context Learning](https://aclanthology.org/2022.naacl-main.191/) — 2022 | A | DA_DOC (phạm vi §4.4) |
| `wei2022chain` | [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://proceedings.neurips.cc/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract.html) — 2022 | B | CHUA_DOC |
| `zhu2026multitask` | [Multi-Task Bayesian In-Context Learning](https://arxiv.org/abs/2606.20538v1) — 2026 | A | DA_KIEM (phạm vi §4.4) |
| `muller2022transformers` | [Transformers Can Do Bayesian Inference](https://arxiv.org/abs/2112.10510v7) — 2022 | A | DA_DOC (phạm vi §4.4) |

#### Nhóm 7. Thiết kế đánh giá, chọn mô hình và phụ thuộc

Chương 2.6/3.7/5.5/5.9; thiên lệch lựa chọn, nhiều so sánh, resampling phụ thuộc và backtest. Có phương pháp trong nguồn không có nghĩa nghiên cứu đã chạy phương pháp đó.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `varma2006bias` | [Bias in Error Estimation When Using Cross-Validation for Model Selection](https://bmcbioinformatics.biomedcentral.com/counter/pdf/10.1186/1471-2105-7-91.pdf) — 2006 | A | CHUA_DOC |
| `white2000reality` | [A Reality Check for Data Snooping](https://users.ssc.wisc.edu/~behansen/718/White2000.pdf) — 2000 | A | CHUA_DOC |
| `harvey2016` | [...and the Cross-Section of Expected Returns](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF) — 2016 | A | CHUA_DOC |
| `bailey2014deflated` | [The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality](https://davidhbailey.com/dhbpapers/deflated-sharpe.pdf) — 2014 | B | CHUA_DOC |
| `holm1979multiple` | [A Simple Sequentially Rejective Multiple Test Procedure](https://sci2s.ugr.es/keel/pdf/specific/articulo/0052_001.pdf) — 1979 | A | CHUA_DOC |
| `lahiri2003resampling` | [Resampling Methods for Dependent Data](https://www.gbv.de/dms/goettingen/366100181.pdf) — 2003 | A | CHUA_DOC |
| `newey1987hac` | [A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix](https://www.ssc.wisc.edu/~bhansen/718/NeweyWest1987.pdf) — 1987 | B | CHUA_DOC |
| `pardo2008evaluation` | [The Evaluation and Optimization of Trading Strategies](https://www.wiley.com/en-us/-p-9780470128015) — 2008 | B | CHUA_DOC |

#### Nhóm 8. Chỉ số phân loại và rủi ro tài khoản

Chương 3.7/5.5; đối chiếu định nghĩa, mẫu số, tần suất và NA với evaluator đã khóa.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `brodersen2010balanced` | [The Balanced Accuracy and Its Posterior Distribution](https://www.ong-home.my/papers/brodersen10post-balacc.pdf) — 2010 | A | CHUA_DOC |
| `chicco2020mcc` | [The Advantages of the Matthews Correlation Coefficient (MCC) over F1 Score and Accuracy in Binary Classification Evaluation](https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-019-6413-7.pdf) — 2020 | A | CHUA_DOC |
| `sharpe1966mutual` | [Mutual Fund Performance](https://web.stanford.edu/~wfsharpe/art/mfp.pdf) — 1966 | A | CHUA_DOC |
| `sortino1994downside` | [Performance Measurement in a Downside Risk Framework](https://www.pm-research.com/content/iijinvest/3/3/59) — 1994 | A | CHUA_DOC |

#### Nhóm 9. Phần mềm, dữ liệu và model card

Chương 4/5.3/Phụ lục C/F; tài liệu chính thức cần đi kèm version/commit của nghiên cứu, không thay lock bằng mặc định online.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `pedregosa2011sklearn` | [Scikit-learn: Machine Learning in Python](https://jmlr.org/papers/v12/pedregosa11a.html) — 2011 | B | CHUA_DOC |
| `langgraph_docs` | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — n.d. | B | CHUA_DOC |
| `mplfinance_docs` | [mplfinance: Financial Markets Data Visualization Using Matplotlib](https://github.com/matplotlib/mplfinance) — n.d. | B | CHUA_DOC |
| `vnstock_docs` | [Vnstock Documentation](https://vnstocks.com/docs) — n.d. | B | CHUA_DOC |
| `openai2025gptoss` | [gpt-oss-120b & gpt-oss-20b Model Card](https://arxiv.org/abs/2508.10925v1) — 2025 | B | CHUA_DOC |

#### Nhóm 10. Bối cảnh Việt Nam và benchmark dự báo tương lai

Chương 1/2.6/5.9/6; thông báo thanh toán là nguồn lịch sử cần kiểm ngày áp dụng; prediction markets khác cổ phiếu cơ sở.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `vo2016herdvietnam` | [Herd Behavior in Emerging Equity Markets: Evidence from Vietnam](https://digital.lib.ueh.edu.vn/handle/UEH/56589) — 2016 | C | CHUA_DOC |
| `vsd2022settlement` | [Settlement schedule announcement (19 August 2022)](https://vsdc.vn/vi/ad/152750) — 2022 | A | CHUA_DOC |
| `arora2026predictionmarketbench` | [PredictionMarketBench: A SWE-bench-Style Framework for Backtesting Trading Agents on Prediction Markets](https://arxiv.org/abs/2602.00133v1) — 2026 | C | CHUA_DOC |
| `zeng2025futurexadvancedlivebenchmark` | [FutureX: An Advanced Live Benchmark for LLM Agents in Future Prediction](https://arxiv.org/abs/2508.11987v3) — 2025 | C | CHUA_DOC |
| `zhang2026predictionarena` | [Prediction Arena: Benchmarking AI Models on Real-World Prediction Markets](https://arxiv.org/abs/2604.07355v1) — 2026 | C | CHUA_DOC |

### 4.4. Ghi chú đọc và xác minh trong lượt này

Mọi ngày kiểm dưới đây là **14/11/2026**; phạm vi đọc được nêu tường minh.

- **`zhu2026multitask` — DA_KIEM:** kiểm tên Zhu/Oermann/Cho, năm 2026 và
  ID v1 trên [arXiv](https://arxiv.org/abs/2606.20538v1); đọc
  [§4](https://arxiv.org/html/2606.20538v1#S4), §5.1 và Appendix C.
  Phần được hỗ trợ: đưa các dataset của tác vụ trước vào context để điều
  chỉnh prior khi dự báo tác vụ đích. Giới hạn: đây là nguồn cho ý tưởng,
  không chứng minh hiệu quả giao dịch; phải đối chiếu riêng student, teacher,
  target và utility của hệ thống với recipe nội bộ khi viết phương pháp.
  [Repo tác giả](https://github.com/martianmartina/multi-task-bayesian-icl/)
  được paper liên kết, đã xem README; chưa audit hoặc khẳng định mã hiện tại
  là bản sao repo đó.
- **`xiong2025quantagent` — DA_KIEM:** kiểm tác giả/năm và bản v3 trên
  [arXiv](https://arxiv.org/abs/2509.09995v3); đọc
  [§3.1–§3.1.3](https://arxiv.org/html/2509.09995v3#S3.SS1), phần đầu §4.
  Dùng cho nguồn gốc các vai trò và loại đầu vào biểu đồ/chỉ báo. Paper phân
  biệt RiskAgent và DecisionAgent; không viết rằng mọi tên/vai trò/logic của
  hệ gốc trùng pipeline hiện tại. Bài gốc xét 1h/4h, khác nghiên cứu daily
  LONG/CASH. Bản v4 đã tồn tại nhưng lần này vẫn giữ v3 đã đọc; không tự đổi
  version để sửa lịch sử kế thừa.
- **`hf5cdsentiment` — DA_KIEM:** đọc model card, Dataset/Evaluation và
  `id2label` ở revision đã khóa
  `d7738b85200272f10ba8b048d80236c8c582b581`:
  [README](https://huggingface.co/5CD-AI/Vietnamese-Sentiment-visobert/blob/d7738b85200272f10ba8b048d80236c8c582b581/README.md),
  [config](https://huggingface.co/5CD-AI/Vietnamese-Sentiment-visobert/blob/d7738b85200272f10ba8b048d80236c8c582b581/config.json).
  Xác nhận nhãn 0/1/2 tương ứng NEG/POS/NEU và nguồn classifier riêng của
  5CD-AI. Card mô tả dữ liệu xã hội/review, không cung cấp kiểm định riêng
  cho tin tài chính trong nghiên cứu này; không lấy điểm card làm độ chính
  xác của Sentiment Agent. Chưa tải/chạy model hoặc kiểm lại weights.
- **`muller2022transformers` — DA_DOC:** đọc abstract và metadata trên
  [arXiv v7](https://arxiv.org/abs/2112.10510v7); dùng để mở đường đọc PFN,
  không thay MT-BICL bằng PFN/TabPFN. Trang OpenReview forum yêu cầu browser
  verification trong lượt này; chưa đọc bản conference ở đó, chưa đánh dấu
  toàn văn đã kiểm.
- **`xie2022implicitbayes` — DA_DOC:** đọc abstract/metadata
  [v6](https://arxiv.org/abs/2111.02080v6). Tài liệu xét mô hình sinh hỗn hợp
  HMM và dữ liệu synthetic GINC; chưa đọc chứng minh. Không dùng để chứng
  nhận mọi LLM/prompt hoặc regime HMM tài chính thực hiện Bayesian inference.
- **`kakushadze2016formulaic` — DA_DOC:** đọc abstract và record
  [v3](https://arxiv.org/abs/1601.00991v3), có journal reference Wilmott 2016.
  Chưa đối chiếu từng công thức/operator; không coi việc liệt kê 101 alpha
  là bằng chứng các phép thích nghi một mã trong repo tương đương toán học.
- **`nguyen2023visobert` — DA_DOC:** đọc abstract, thông tin venue/DOI và
  export trên [ACL](https://aclanthology.org/2023.emnlp-main.315/).
  Nguồn mô tả backbone/social-media tasks, không phải chính classifier 5CD-AI
  và không xác minh sentiment tài chính. Tên tác giả trong export dùng dạng
  Nam Nguyen/Thang Phan/Duc-Vu Nguyen/Kiet Nguyen, khác cách ghi mở rộng trong
  bibliography cũ; cần đối chiếu PDF authoritative trước chuẩn hóa, chưa tự
  sửa bibliography bài báo.
- **`rubin2022retrieve` — DA_DOC:** đọc abstract, metadata và DOI trên
  [ACL](https://aclanthology.org/2022.naacl-main.191/). Công trình học dense
  retriever cho các tác vụ semantic parsing; chỉ tạo liên hệ để đọc sâu,
  không chứng minh `B_semantic` trong hệ này dùng embedding retrieval.

### 4.5. Các việc còn phải kiểm khi đọc sâu

| Vấn đề | Cách xử lý ở các task viết/kiểm nguồn sau |
| --- | --- |
| Nguồn học thuật MT-BICL/PFN thiếu trong bibliography cũ | Giữ hai khóa đề xuất ở đây; lấy metadata từ nguồn gốc trước khi điền BibTeX. Không trình bày MT-BICL là phát minh riêng của khóa luận. |
| Paper MT-BICL và student nội bộ khác cấu hình | Appendix C của paper synthetic dùng 8 layer/8 head, hidden 128/FF 512; recipe nội bộ khóa 2 layer/4 head, hidden 128/FF 256. “Replica” trong tên artifact nội bộ không tự chứng minh tái lập nguyên xi paper. Khi viết §4.8, đối chiếu recipe/lock, không thay checkpoint hoặc mở lại nghiên cứu. |
| Commit recipe nội bộ và repo tác giả là hai đối tượng | `docs/plan/week11/mt_bicl_replica_full_r1.json` neo recipe tại commit repo này `00b24679f63d491c15cda6be0bc9a2c412651f93`. Đây không phải mặc nhiên là Git pin của repo tác giả. Hash protocol giữ `11146a55e347be77b4a942c67d0acc9dba8646fa1d5a0b4817e5ffb504214857`. |
| Khóa legacy, năm đầu đăng và năm revision không trùng | Giữ khóa để tránh gãy liên kết; đối chiếu edition/year/venue khi tạo bibliography mới, đặc biệt TradingAgents. Không ghi năm chỉ theo tên khóa. |
| Báo cáo link lịch sử, catalogue và sách preview | Không suy toàn văn đã đọc. Sách cần edition/chương/trang hỗ trợ; link challenge hoặc chỉ mục lục phải giữ trạng thái truy cập chưa đủ. |
| Nguồn thị trường Việt Nam và T+2 | Thông báo VSD 2022 chưa đọc trong lượt này; cần kiểm ngày hiệu lực và phạm vi trước khi viết nhận định về quy định. Hợp đồng mô phỏng của hệ thống vẫn lấy từ engine/evidence, không suy là pháp luật hiện hành. |
| Bảng so sánh nghiên cứu và citation cuối cùng | Chưa hoàn tất T48–T53; chỉ trích những nhận định đã có đoạn nguồn phù hợp. Các nguồn CHUA_DOC và paper mới năm 2026 chưa được dùng để tuyên bố khoảng trống hay vượt trội. |

## 5. Thuật ngữ tiếng Anh, ký hiệu và quy ước diễn đạt

Chốt quy ước viết ngày **14/11/2026**, từ commit
`d2cf431aa9312add8870e06690e6e4776f624a0d`. Các định nghĩa tiếng Anh trong
bảng dùng làm từ vựng thống nhất cho bản thảo; phần quản lý/đối chiếu nguồn
vẫn bằng tiếng Việt. Ký hiệu là quy ước trình bày, không đổi tên field JSON,
ID phương pháp, schema, nhãn hoặc bằng chứng đã khóa. Chưa tạo danh mục
viết tắt hoàn chỉnh của phần đầu hay viết thay các mục lý thuyết.

### 5.1. Tên phương pháp và ánh xạ ID

Đối chiếu [registry](../core/variant_registry.py),
[cấu hình thành phần](../utils/graph_setup.py) và
[phụ thuộc/policy thống nhất](../core/unified_methods.py). Không lấy từ
“baseline”, “original” hoặc “Full” đứng riêng để suy ra ID/profile.

| Canonical manuscript name | Implementation or archive name | Meaning and scope in the thesis |
| --- | --- | --- |
| Full | Component study: `full`, `AS` | The price-based pipeline with alpha factors and sentiment enabled in the recorded component comparison. Its responses belong to the component study. |
| Base | Component study: `baseline`, `B`; legacy “No-Alpha” output label | The component control with both alpha-factor and sentiment report sections disabled. The legacy label does not mean a factor-only intervention. |
| Native | `original_fix` | The native alpha representation and native Decision profile in the historical-context study. It is not an alias for the component study's saved Full responses. |
| Common | `original_common`; explicit archive alias `Original_common` | The foundation retaining alpha and sentiment under the causal-common alpha representation and common Decision instructions. It is not Base. |
| Bayesian Prior v1 | `bayesian_v1` | The Common-based method using matured signal-bank history and market-regime context; unsupported cases reuse Common from the same repeat. |
| Conditional Prior | `C2` | Conditional historical statistics with disjoint-background shrinkage and separate readiness conditions for statistics and examples. |
| Trend-Pattern Prior | `A_tp_pool` | The alternative using relaxed Trend/Pattern matching for historical evidence. Its larger candidate pool is not automatically stronger evidence. |
| Explicit-Count Prior | `B_semantic` | The alternative exposing historical counts, intervals and example identities. “Semantic” in the ID does not establish embedding-based retrieval. |
| Fact Anchor | `Fact_Anchor` | The Common-dependent factual anchoring step. Its resolved action is the reference for MT revision; this step has no numerical utility veto. |
| MT-BICL | `MT_BICL` | Multi-task Bayesian in-context learning: the method combining a frozen numerical student, task context and utility-gated revision relative to Fact Anchor. It is one evaluated method, not a synonym for every Bayesian prior. |
| CASH control | `CASH_EVERY_CYCLE` | A registered rule that retains cash at every scheduled cycle; it has no new LLM response. |
| Always-LONG cycles | `ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS` | A registered rule that enters and closes each scheduled LONG cycle and pays both trading legs. |
| Continuous hold | Component economic comparator | A position held across the specified account window. Its gap exposure and costs differ from Always-LONG cycles. |

**Quy tắc phạm vi:** Full/Base và Native/Common thuộc hai nghiên cứu riêng;
không gộp raw response, support hoặc protocol thống kê. Native/Common thay cả
biểu diễn Alpha và chỉ dẫn; chênh lệch giữa chúng không cô lập riêng tác động
Alpha. MT-BICL là multi-task; pipeline nhiều vai trò là multi-agent — hai
khái niệm này không thay thế nhau.

Tên `Full` trong `prepare_variants(...)["contexts"]["Full"]` lại chỉ context
MT đủ prior/target observations, không phải Full của nghiên cứu thành phần.
Trong unified policy, reason `FALLBACK_ORIGINAL` tái dùng `original_common`,
không chuyển sang Native. Các tên legacy “Original” phải được giải theo
protocol/ID của đúng nghiên cứu, không tự gộp thành một alias chung.

### 5.2. Từ vựng cốt lõi cho bản thảo

| English term | Definition for the manuscript |
| --- | --- |
| Large language model (LLM) | The language model invoked for the specified report or Decision role. A named agent can instead be deterministic; an agent count is not an LLM-call count. |
| Vision-language model (VLM) | A model receiving chart images with textual instructions. Producing a fluent report does not by itself validate visual grounding. |
| In-context learning (ICL) | Prediction conditioned on information supplied in the current context, without updating model parameters during that inference. |
| Bayesian in-context learning (BICL) | In-context prediction interpreted or constructed through an explicitly stated Bayesian model. Few examples in a prompt alone do not establish a validated Bayesian inference mechanism. |
| Hidden Markov model (HMM) | The latent-state model used for market-regime estimation. Fitting, prefix inference and any fallback must retain their declared temporal boundaries. |
| Point-in-time (PIT) | Availability of inputs and admissible historical outcomes relative to the specified decision cutoff. Outer-cutoff isolation and row-wise causality are distinct requirements. |
| OHLCV | Open, High, Low, Close and Volume of the declared observed bar. Price basis, vendor units and availability remain part of the input contract. |
| Bayesian Regime Prior Prefix (BRPP) | The bounded prompt block presenting the applicable historical context. Its presentation budget does not define the full statistical population or imply that all prior methods use identical evidence. |
| Market observation / test point | One eligible stock and decision-cutoff pair. The market observation is distinct from its method-specific forecasts and repeated Decisions. |
| Observed trading session / bar | One ordered daily vendor observation used by the protocol. A bar index is not a calendar-day offset or an authenticated exchange calendar. |
| Decision cutoff / as-of date | The time boundary defining the admissible information for a query. Prices and eligible dated news cannot extend beyond it; historical outcome membership requires a strictly earlier exit. |
| Candidate LONG cycle | The hypothetical entry-to-exit cycle used to define the net target for every observation, including observations on which the method ultimately retains CASH. |
| Matured historical episode | A historical cycle whose exit precedes the query cutoff and whose recorded features, label and return may therefore be considered under the applicable eligibility rules. Maturity alone does not certify every provenance or row-wise-causality requirement. |
| Signal memory bank | The frozen collection of cycle-level historical records used by the signal-based Bayesian priors. A record called a “historical task” in this bank is not necessarily a multi-observation MT task. |
| MT task | A group of numerical observations associated with one stock and a calendar-block identity in the implemented MT construction. It is not an agent or an individual forecast. |
| Prior task | A selected earlier MT task contributing matured observations to the prior-task context. Task boundaries are retained rather than replacing all tasks by one pooled count. |
| Target task | The MT task containing the current query. Its historical observations and its unlabeled query have different information roles. |
| Target observations | Matured observations selected from the target task before the query; they exclude the query's own label and return. |
| Query | The current input to be predicted, with features and permitted metadata but no observed outcome supplied to inference. Scheduled entry/exit dates do not make their future prices available. |
| MT context episode | The complete inference object containing the query, prior tasks, target observations, scaler and provenance. This container is distinct from one historical trading episode. |
| Numerical task context | The MT membership and features used by the numerical student/teacher and utility computation. It is not interchangeable with the signal memory bank or with a few rendered examples. |
| Market regime | A market-state assignment inferred under the specified model, feature prefix and fit cutoff. A regime name is not a trading action or a guarantee of future return. |
| Support | The number of admissible observations relevant to a specified statistic or decision condition. The statistic, population and denominator must be named. |
| Coverage / readiness | Coverage reports how often a specified resource or condition is available; readiness is the method's rule for whether evidence can be used. Neither term means predictive accuracy. |
| Displayed example | A record projected into the prompt for presentation. Displayed examples can be a small subset of the observations used in numerical summaries. |
| Numerical student | The frozen learned predictor producing a numerical estimate of the positive net label from the permitted MT input. It is distinct from the hosted Decision LLM. |
| Bayesian teacher | The numerical hierarchical Beta-Bernoulli reference model supplying predictive quantities and posterior uncertainty under its specified assumptions. “Teacher” does not mean an additional hosted LLM call. |
| Predictive probability | A numerical estimate of the probability that the candidate LONG net return is strictly positive. An estimate in [0,1] is not automatically calibrated out of sample. |
| Reported confidence | A model's reported confidence field. In `TradeDecisionOutput`, `confidence` is a string; it is not automatically the student's probability, a posterior probability or an input to utility. |
| Posterior utility | A model-based estimate of the net return of LONG relative to CASH, incorporating sign probability and gain/loss magnitudes. It is expressed as a net-return fraction, not as confidence. |
| Factual assertion validity | Agreement with the required recorded assertion IDs and enum values. Passing this check does not verify every statement in free-text reasoning. |
| Raw proposal | The LONG/SHORT direction returned by a new Decision response before the external action policy; it can be absent when no new response is required. |
| Anchor action | The resolved Fact Anchor LONG/CASH action used as the reference for MT revision. An invalid anchor response resolves through its recorded Common dependency. |
| Final action | The LONG/CASH action selected after factual, eligibility and utility conditions. Evaluation follows this action rather than assuming every raw proposal was accepted. |
| Fallback / policy bypass | A specified reuse or retention of a dependency/anchor action when evidence conditions are not met. A technical failure or missing required response is not silently converted into a valid CASH decision. |
| Shared upstream realization | The immutable Indicator/Pattern/Trend evidence and associated shared inputs produced once for a test point and copied to comparison branches. |
| Decision repeat | A repeated Decision execution conditional on the same upstream realization. It does not add a new market date or an independently regenerated complete pipeline. |
| Forecast slot / raw response / HTTP attempt | A slot is a scheduled method-point-repeat output; a raw response is an actual recorded model response; an HTTP attempt is one transport attempt, including retries. These counts are not interchangeable. |
| Paired contrast | A difference evaluated on common eligible observations and the protocol's shared dependencies. Pairing within one study does not pair independently collected responses across studies. |
| Stock-fold account | A separately capitalized stock/fold simulation. An average across these accounts is not one capital-constrained multi-stock portfolio. |
| Historical credible interval | A posterior interval for a specified historical rate, conditional on the model and fitted/plug-in hyperprior. It is not a return-prediction interval or proof of query calibration. |
| Descriptive comparison band | The recorded resampling envelope for an effect or contrast family. With exposed folds and limited dependent support, it is not described as prospective confirmation or guaranteed calibrated coverage. |
| Missing / undefined / zero | Missing or undefined quantities remain NA/null with a reason; a genuine numerical zero remains zero. These states must not be silently interchanged. |

### 5.3. Ký hiệu và đơn vị

Các ký hiệu toán dưới đây là tên trình bày cho cùng đối tượng; tên field gốc
giữ nguyên. Dùng chỉ số riêng cho tác vụ, quan sát và repeat; không dùng
`K`, `N`, “return” hoặc “confidence” đứng riêng khi có nhiều mẫu số/đơn vị.

| Symbol | Meaning | Unit / wire correspondence |
| --- | --- | --- |
| $t$, $e=t+1$, $L$ | Decision-bar index, exclusive window end/entry index, and holding horizon in observed bars. | $L=3$ for the study; entry at $e$, exit at $e+L-1=t+3$. |
| $W$, $[e-W,e)$ | Chart-window length and the corresponding half-open input window. | Observed bars; separate from the longer factor-computation history. |
| $O_{t+1}$, $C_{t+3}$ | Entry Open and exit Close of the candidate LONG cycle. | Prices on the same declared basis/unit; unavailable to the query inference. |
| $f$, $s$ | Brokerage fee and slippage on each trading leg. | Fractions: $f=0.0025$, $s=0.001$. |
| $r_t^{\mathrm{net}}$ | Net candidate-LONG round-trip return after both legs. | Fraction; `net_return`, context `r_net`. |
| $y_t$ | Positive net label: $\mathbf{1}[r_t^{\mathrm{net}}>0]$. | Binary; `1` corresponds to UP, `0` to DOWN; zero net return is DOWN. |
| $\hat d_{t,v,j}$, $a_{t,v,j}$, $a_0$ | Raw direction, final action, and resolved anchor action for method $v$/repeat $j$. | Raw: LONG/SHORT; actions: LONG/CASH. `SHORT` maps to CASH. |
| $r_{t,v,j}^{\mathrm{strategy}}$ | Realized cycle return under the final action in the all-in LONG/CASH contract. | $\mathbf{1}[a_{t,v,j}=\mathrm{LONG}]r_t^{\mathrm{net}}$; CASH cycle return is zero. |
| $N_{\mathrm{point}}$, $N_{\mathrm{account}}$, $n_{\mathrm{rep}}$ | Counts of market points, separately capitalized stock-fold accounts, and Decision repeats. | Historical-context study: 102, 51 and 3; report other panels with their own supports. |
| $K_{\mathrm{ex}}$ | Number of selected/displayed signal-bank examples. | Records; a request's `k` is an upper limit, not necessarily the realized count. |
| $K_{\mathrm{task}}$, $m$ | Number of selected prior MT tasks and number of target-task observations. | MT episode `K` and `m`; neither is a count of LLM calls or prompt characters. |
| $n_k$, $\mathcal D_k$, $\mathcal C_q$, $\boldsymbol x_q$ | Prior-task observation count, prior-task dataset, target observations, and unlabeled query features. | Membership counts/data; query is excluded from labeled context. |
| $\boldsymbol x_i$, $\boldsymbol z_i$ | Raw numerical feature vector and its standardized form. | Feature-specific units before scaling; dimensionless after scaling. Model clipping/projection is specified separately. |
| $S_t$ | Market-regime state/assignment used at cutoff $t$. | Categorical; kept distinct from standardized-feature symbol $\boldsymbol z$. |
| $n_{c,h}$, $s_{c,h}$, $n_{b,h}$, $s_{b,h}$ | Conditional/background support and success counts for historical metric $h$. | Counts in disjoint metric-specific subsets; not $K_{\mathrm{ex}}$ or global query count. |
| $\tau$, $a_h$, $b_h$ | Shrinkage strength and resulting Beta shape parameters for conditional statistic $h$. | Model parameters; `shrink_strength`, `posterior_alpha`, `posterior_beta`. They are distinct from financial alpha factors. |
| $p_{S,q}$, $p_{T,q}$ | Numerical student estimate and teacher predictive mean for the positive label. | Fractions in [0,1]; `numeric_probability`/branch `probability` versus `teacher_probability`/`posterior_mean_theta`. |
| $\theta_q$, $\boldsymbol\pi$ | Target-task Bernoulli parameter and the frozen teacher's weights over its latent hyperparameter grid. | Model-based probability/weights; distinct from LLM weights and reported confidence. |
| $g_q$, $\ell_q$ | Positive-return magnitude and nonpositive-return loss magnitude used in utility. | Nonnegative net-return fractions; zero returns belong to the nonpositive group. |
| $U_q$, $\Delta U_q$ | Utility of LONG relative to CASH, and utility change relative to the anchor action. | Net-return fraction; $U_q=\theta_q g_q-(1-\theta_q)\ell_q$ for the posterior draws. |
| $Q_\eta(U_q)$ | Quantile of the model-based posterior utility draws. | Net-return fraction; $Q_{0.1}$ and $Q_{0.9}$ map to `q10_U_net_fraction`/`q90_U_net_fraction`. |
| $R_{a,j}$, $\bar R_v$ | Net return of account $a$ in repeat $j$, and the method's equally weighted mean across accounts after repeat averaging. | Define in fractions in equations; `mean_account_return_pct` is already multiplied by 100. |
| $V_{a,d}$, MDD | Account NAV at observation date $d$, and maximum drawdown over the declared NAV path. | NAV in VND; recorded MDD in percent as a nonnegative loss magnitude. Specify daily versus cycle-end path. |
| BA, MCC, IC | Balanced accuracy, Matthews correlation coefficient, and factor Information Coefficient. | BA is a fraction or percent as labeled; MCC and rank IC are dimensionless in [-1,1]. IC is not an account return. |
| $\Delta_R^{\mathrm{pp}}$, $\Delta_{\mathrm{BA}}^{\mathrm{pp}}$ | Differences of mean returns or BA between the named method and named comparator. | Percentage points: multiply a difference of fractions by 100; do not multiply a difference of percent-valued fields again. |
| $\operatorname{age}_i$, $d_i$, $\operatorname{sim}_i$ | Age, numerical distance and retrieval similarity of a specified historical item. | Age in recorded calendar days; distance/similarity use their defined score scales, not probability units. |

Hai lưu ý phải giữ khi dựng bảng/hình:

- `effective_K` trong artifact phân tích lấy `selected_count` của retrieval
  khi có, còn nhánh MT lấy `utility.K`. Vì vậy, phải ghi **examples** hay
  **prior tasks** theo phương pháp; không vẽ một trục “K” như thể cùng đơn vị.
- Support của thống kê lịch sử tính trên population/membership hợp lệ,
  không mặc định bằng số ví dụ đưa vào prompt. Nếu cần ký hiệu $K$ ngắn trong
  một mục, phải định nghĩa rõ là $K_{\mathrm{ex}}$ hay $K_{\mathrm{task}}$ tại đó.

### 5.4. Phân biệt đơn vị và các đại lượng dễ nhầm

| Quantity / presentation rule | Correct reading |
| --- | --- |
| Fraction versus percent | A stored return of `0.012` is `1.2%`; a percent-valued field containing `1.2` is already `1.2%`. Do not multiply by 100 twice. |
| Percent versus percentage points | An illustrative rate change from 50% to 55% is +5 percentage points (`pp`), or +10% relative to 50%. State which difference is reported. |
| Basis point | 1 basis point (`bp`) = 0.01 percentage points = 0.0001 as a fraction. The fee and slippage are 25 bp and 10 bp on each leg. |
| Brokerage/slippage cost | The approximate 0.70% round-trip drag is a shorthand. The canonical multiplicative formula, not a subtraction of exactly 0.007, defines the net label/return. |
| Probability versus reported confidence | `numeric_probability=0.7` is a numerical positive-label estimate. A confidence string such as `HIGH` remains a reported category/text unless a separate validated mapping exists. |
| Probability versus expected return | Illustratively, with probability 0.7, mean gain 1% and mean loss magnitude 4%, expected net return is −0.5%. A high positive-label probability alone does not imply positive utility. |
| Student probability versus utility source | `probability_student` is recorded separately. The implemented utility uses the teacher's sign posterior and Bayesian-bootstrap magnitudes; it does not substitute the student point estimate into every utility draw. |
| Mean utility versus utility quantile | `mean_U_net_fraction` and `MC_mean_U_net_fraction` are the analytical and Monte Carlo means. `q10`/`q90` are uncertainty quantiles, not a 10%/90% probability of trading success. |
| Risk-reward ratio | The generated trade-setup ratio is distinct from realized net return, forecast probability and the external utility veto. It does not override the fixed entry/exit evaluator. |
| Sentiment score versus alpha IC | A signed sentiment aggregate, an alpha factor value and its IC retain their own meanings/scales. A shared range or sign does not make them calibrated probabilities or identical signals. |
| Return versus money P&L | Return is dimensionless; P&L and NAV carry VND units. Vendor price conversion is declared separately and applied once, not inferred from an unlabelled chart. |
| Character budget versus token budget | Prompt characters, tokenizer tokens, requests per minute and tokens per minute are different units. A 600-character prefix bound is not a 600-token allowance. |

Các số ở hai ví dụ tỷ lệ/xác suất trên chỉ **minh họa đơn vị**, không phải
kết quả nghiên cứu hoặc tình huống thực nghiệm đã chọn. Ví dụ tình huống
xuyên suốt và các phép tính lý thuyết đầy đủ vẫn làm ở task tương ứng.

### 5.5. Quy tắc diễn đạt và nguồn đối chiếu

1. Nhãn kinh tế được viết theo đúng hàm chuẩn:

   $$
   r_t^{\mathrm{net}}=\frac{C_{t+3}}{O_{t+1}}
   \frac{(1-s)(1-f)}{(1+s)(1+f)}-1.
   $$

   `UP`/`y=1` nghĩa là return này dương; `DOWN`/`y=0` gồm zero. SHORT giữ CASH,
   không mô tả là lợi nhuận bán khống. $t+1$, $t+3$ là phiên quan sát; tên
   hợp đồng $T+2.5$ không được dùng thay phép đếm phiên hay quy định thị trường.
2. Khi nói “available at the cutoff”, giữ giá/tin hợp lệ không sau cutoff,
   historical membership có `exit_date < as_of_date`, và query không có nhãn.
   Không đổi dấu `<` thành `<=`. Quy tắc global reserved IDs/fold context
   của nghiên cứu vẫn giữ riêng; eligibility không đồng nghĩa đã giải quyết
   mọi hạn chế provenance hoặc nhân quả từng hàng.
3. Khi giải thích MT policy, giữ đúng dấu:
   CASH→LONG đòi $Q_{0.1}(U_q)>0$; LONG→CASH đòi $-Q_{0.9}(U_q)>0$.
   Chỉ mô tả đổi action khi nhánh đủ điều kiện và assertion hợp lệ; giá trị
   bằng zero không vượt ngưỡng. Không dùng confidence để thay kiểm utility.
4. Viết “historical descriptive difference”, “conditional on shared upstream”
   và “model-based estimate” theo đúng loại bằng chứng. Không đổi band mô tả
   thành ý nghĩa thống kê xác nhận, hoặc ghi fallback là một inference mới.
   Support, repeat, response, HTTP attempt và tài khoản luôn có mẫu số riêng.
5. Viết NA khi thiếu hoặc chỉ số không xác định; giữ lý do và số lượng có
   thể tính. Không biến thiếu sentiment thành số trung tính được bịa, MCC/BA
   không xác định thành zero, hay missing response thành một forecast đúng.

Đường đối chiếu triển khai (cùng phạm vi snapshot nghiên cứu đã ghi tại §3):

| Nội dung | Nguồn đã đọc để chốt quy ước |
| --- | --- |
| Net return, horizon và nhãn | [compute_round_trip_net_return](../core/backtest_engine.py), [target_fields/validate_target_record](../utils/target_contract.py). |
| Native/Common/Base và fallback | [registry](../core/variant_registry.py), [ABLATION_CONFIGS](../utils/graph_setup.py), [unified methods](../core/unified_methods.py). |
| Confidence, decision, risk-reward | [TradeDecisionOutput](../agents/decision_agent.py), [action/fact contracts](../core/mt_bicl_contracts.py). |
| IC và thang điểm factor | [compute_metrics/rank_alphas](../core/alpha_compare.py); IC dùng Spearman, không phải return tài khoản. |
| Population, ví dụ, counts và interval | [retriever](../core/bayesian_retriever.py), [conditional_metric](../core/prior_conditional_statistics.py). |
| MT task/query/membership và prompt projection | [validate_episode/TaskBuilder](../core/mt_bicl_tasks.py), [context projection](../core/mt_bicl_context.py). |
| Teacher, utility và action revision | [teacher](../core/mt_bicl_teacher.py), [posterior_utility](../core/mt_bicl_utility.py), [MT policy](../core/mt_bicl_policy.py). |
| Field/đơn vị kết quả và effective_K | [prediction_rows](../core/unified_analysis/analysis.py), [paired estimators](../core/unified_analysis/statistics.py), [classification/account primitives](../core/free_pilot_statistics.py). |

Đây là chuẩn thuật ngữ dùng chung. Bằng chứng nguồn gốc học thuật vẫn theo
§4 và cần đọc/kiểm sâu khi viết; định nghĩa trùng với một field trong code
không thay thế citation học thuật hoặc chứng nhận phương pháp đã hiệu chuẩn.

## 6. Danh mục hình, bảng và thuật toán có nguồn

Lập ngày **14/11/2026**, từ commit khảo sát
`3e7a045d5a94237becef7c3f636fca267abe66d4`, theo danh mục gốc tại
[kế hoạch §6](plan.md#6-danh-mục-hình-bảng-và-thuật-toán-cần-chuẩn-bị).
Giữ **23 ID cha**: F01–F11, A01–A03 và B01–B09; mở riêng các ID đã được
gộp theo khoảng trong kế hoạch. Đây là **danh mục chuẩn bị**, chưa phải xác
nhận hình/bảng/thuật toán đã soạn, đã render hoặc đã được phản biện.

Tên tiếng Anh là working title để dùng khi soạn; thông điệp và ghi chú quản
lý dùng tiếng Việt. ID phục vụ truy vết; số Figure/Table/Algorithm cuối và
cross-reference do LaTeX sinh. `F11` trong danh mục hình khác mốc nghiệm thu
ứng dụng cũng mang tên F11 tại README tuần.

### 6.1. Loại nguồn và nguyên tắc sử dụng

- **ĐO_ĐƯỢC:** đầu vào/quan sát, cấu hình, bản ghi thực thi hoặc ảnh đã lưu
  trực tiếp. “Đo được” không đồng nghĩa dữ liệu đã xác thực độc lập, kết quả
  có ý nghĩa nhân quả hoặc ảnh UI đã nghiệm thu.
- **DẪN_XUẤT:** phép tổng hợp, bảng/đồ thị hoặc đối chiếu từ nguồn có thể truy
  vết. Metrics đã tính trong nghiên cứu vẫn là dẫn xuất khi dựng bảng khóa
  luận; chỉ nhập giá trị đã khóa, không thu/refit/tái ước lượng nghiên cứu.
- **MINH_HỌA:** sơ đồ, timeline và giả mã giải thích hợp đồng/luồng xử lý từ
  code/protocol. Hình đó không phải kết quả đo cơ chế, hiệu quả hay nhân quả.
- Mỗi ID có **một loại nguồn chính**; panel phụ phải ghi loại/nguồn của nó.
  Ví dụ ảnh UI thật nếu bổ sung vào F11 phải ghi version và lượt kiểm riêng,
  không biến sơ đồ workflow thành bằng chứng nghiệm thu.
- Đường xuất trong bảng là **đề xuất tại mốc T06**; sản phẩm F01/F02 tạo sau
  đó được ghi tại §8.4/§8.5.6, không suy các ID khác đã có sản phẩm. Các tiền tố
  `diagrams/`, `figures/`, `tables/` nằm dưới `thesis/assets/`. Nguồn giả mã
  A01–A03 nằm trong bản thảo Chương 4 §4.9 rồi chuyển sang LaTeX; label là
  định danh dự kiến. Chưa tạo các thư mục/file này chỉ để lấp danh mục.

### 6.2. Sổ nguồn dùng cho danh mục

Định danh/hash và cách đọc archive kế thừa mục 3. Các source ID dưới đây chỉ
rút gọn đường dẫn cho bảng, không phải task mới hay nguồn kết quả mới.

| Source ID | Nguồn có thể truy cập | Vai trò và giới hạn |
| --- | --- | --- |
| SRC01 | [Engine](../core/backtest_engine.py), [target contract](../utils/target_contract.py), [thuật ngữ §5](#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt). | Entry/exit, label/P&L, LONG/CASH và đơn vị; công thức/hợp đồng không đổi. |
| SRC02 | [Protocol U06 v2](../docs/plan/week12/unified_comparison_protocol_v2.json), [manifest U06 v2](../docs/plan/week12/unified_comparison_manifest_v2.json); component `final_temporal_v1/primary_dependence.json`, `final_repeats_v1/protocol.json` trong kho revision. | Lịch, split, support và frozen-resource boundaries theo đúng nghiên cứu; không thay vendor sessions bằng lịch sàn chưa xác thực. |
| SRC03 | [Graph](../utils/graph_setup.py), [registry](../core/variant_registry.py), [unified methods](../core/unified_methods.py), [paired protocol](../core/unified_protocol.py). | Luồng, projection, dependency và outcome barrier. Lớp UI của graph vẫn cùng logic snapshot nghiên cứu theo xác nhận tác giả ở §3. |
| SRC04 | [Retriever](../core/bayesian_retriever.py), [conditional statistics](../core/prior_conditional_statistics.py); U09 `prior_traces.json`/`predictions.csv`. | Eligibility, population/counts, matching, selection và prefix/fallback đã ghi; không gộp signal bank với numeric task context. |
| SRC05 | [MT tasks](../core/mt_bicl_tasks.py), [context projection](../core/mt_bicl_context.py), [recipe](../docs/plan/week11/mt_bicl_replica_full_r1.json), [model lock](../docs/plan/week11/mt_bicl_replica_full_r1_model.json); teacher/student/regime resource trong snapshot đã liệt kê ở §3.4. | Prior/target/query, fit/freeze/inference; dùng cấu hình thực tế, không lấy kiến trúc trong paper gốc thay student đã đánh giá. |
| SRC06 | [MT policy](../core/mt_bicl_policy.py), [utility](../core/mt_bicl_utility.py), dependency trong SRC03; U09 trace/bridge/predictions. | Anchor, eligibility, assertion, utility veto, bypass và hành động cuối; lỗi kỹ thuật không thành CASH im lặng. |
| SRC07 | [Baseline còn trên đĩa](../outputs/revision/final_baselines_v1/manifest.json); [index revision](../docs/plan/revision_evidence/index.json) và [reader](../core/revision_evidence_archive.py): các nhóm `revision_minimal_final_v1`, `final_repeats_v1`, `final_temporal_v1`, `numeric_controls_v1`, `execution_final_v1`, `manuscript_rewrite_v1`. | Metrics/panels và cell lineage thành phần. Đường trong index là đường gốc đã đóng gói; xem §6.3 để chọn member, không đọc nhầm một thư mục live trùng tên. |
| SRC08 | [ZIP kết quả U09](../docs/plan/week12/unified_analysis_results.zip), [acceptance](../docs/plan/week12/unified_analysis_acceptance.json); namespace `outputs/unified_integration/u09_analysis_r1/`. | Kết quả ngữ cảnh, contrast, coverage, policy, sensitivity và account. Member/field cụ thể ở §6.3; metrics/bands giữ nguyên. |
| SRC09 | [Manifest trình bày paper](../outputs/paper/manifest.json), [source kiến trúc](../paper/content/system_architecture.tex), [source kết quả](../paper/content/results.tex), [hai ảnh](../paper/figures/), [source đồ thị/bảng F02](../outputs/revision/u09_manuscript_assets_v1/manifest.json). | Bản trình bày giúp đối chiếu, không thay nguồn đo. Cặp PNG khớp snapshot và chart record; lineage chi tiết ở §6.3. |
| SRC10 | [Danh sách nguồn gốc §4](#4-danh-sách-đọc-nguồn-gốc-và-quy-ước-khóa-trích-dẫn), [dàn bài/RQ](outline.md). | Sổ citation và câu hỏi nghiên cứu; các nguồn CHUA_DOC chưa đủ để điền bảng so sánh học thuật cuối. |
| SRC11 | [Serving contract](../docs/plan/week12/variant_serving_contract.md), [entrypoint](../web_interface.py), [live service](../core/serving_live/service.py). | Workflow realtime 1D và cách đọc kết quả; chỉ mô tả chức năng/luồng có nguồn. Ảnh UI trực quan mới vẫn chờ nghiệm thu, không tự đóng F11 ứng dụng. |

### 6.3. Member cần dùng và tình trạng bằng chứng

- **Ảnh F04:** `paper/figures/candlestick.png` và `trendlines.png` khớp nguyên
  byte với `paper/figs/final_pattern.png` và `final_trend.png` trong snapshot.
  Đồng thời, PNG giải mã từ `pattern_image`/`trend_image` trong record gốc
  `outputs/revision/chart_r1_run_v1/shards/org1/charts/CMG_b2023_h2_872.json`
  khớp cả hai file hiện tại. Reader đọc record này qua index đã kiểm hash.
  Caption paper ghi CMG/cutoff 03/07/2023; khi soạn T19 vẫn phải nối
  `asset_hash` tới input/prefix và chú giải cụ thể, không chỉ tin filename.
  Record SHA-256: `51e3a94026314e886a54126dac131513f5c2810ce85ac886cc6cc05c760f47ad`;
  `asset_hash`: `d9a9edb04166ce420c1085cf4504b550bb4cc5f308e895c8417fce94f26a59f0`.
  PNG Pattern SHA-256: `6e3a15ae1ad3bd417312d97b835b3558d4bcf31dc04addbe3c518cf540720f73`;
  PNG Trend SHA-256: `265c73db2caba5a76a61ddae0678f6b27f33bcae0f7c45aeb1e28c0c4b36161d`.
- **B05 thành phần:** CSV tại `final_baselines_v1/` cung cấp classification,
  per-class/macro/account/financial. `final_repeats_v1/{protocol.json,
  repeat_summary.csv,contrasts.csv}` dùng cho panel lặp; `final_temporal_v1/
  primary_dependence.json`, `numeric_controls_v1/summary.json` và
  `execution_final_v1/scenario_summary.csv` giữ từng sensitivity/control.
  `manuscript_rewrite_v1/{generation,numeric_cells}.json` nối ô bảng cũ với
  nguồn. Mọi đường nhóm ở đây có tiền tố gốc `outputs/revision/` qua index.
- **B06/F09 ngữ cảnh:** U09 `summary.csv`/`results.json` là nguồn số;
  `contrasts.csv` có `family,method,baseline,endpoint,effect_pp,
  band95_low_pp,band95_high_pp`. F09 vẽ mười contrast return (năm extension
  cho mỗi baseline); đủ 20 contrast return/BA được giữ ở B06/Phụ lục D.
  Band dùng họ đồng thời 20 contrast return/BA đã khóa; không tính lại một
  họ chỉ gồm mười contrast được vẽ để thay band gốc.
  Không lấy hình một baseline thay cả hai. Member `return_contrasts.svg/png`
  là figure U09 đã lưu; `paper/figures/return_comparisons.pdf` là bản trình
  bày hiện tại để tham khảo, không phải nguồn số độc lập.
- **F10/B07:** U09 `predictions.csv` có `point_id,method,repeat,raw_proposal,
  final_action,reason,bypass,llm_response,anchor_action,effective_K,
  numeric_probability,teacher_probability,utility_q10,utility_q90,trace_sha256`.
  Nối `trace_sha256` với `prior_traces.json`; nối outcome chỉ ở phần đánh giá.
  `bridge.csv` giữ `same_action_forecasts,n_forecasts` và chênh lệch return/BA.
  `effective_K` phải ghi đơn vị examples/prior tasks theo phương pháp. Tại
  mốc T06, T07 chưa chọn tình huống xuyên suốt; lựa chọn sau đó ghi tại
  [EX01](#7-ví-dụ-xuyên-suốt-có-truy-vết), không tự chọn ca thắng để điền B07.
- **B04 và bảng mở rộng:** `results.json` có `coverage,telemetry,input_identity,
  per_repeat,classification_by_group,classification_by_repeat,sensitivity`;
  các CSV `accounts,cycles,daily_nav,per_repeat,classification_by_group,
  classification_by_repeat` giữ support/đơn vị. Phần `sensitivity` có
  `BLOCK_LENGTH_1`, `BLOCK_LENGTH_3`, `CORE4_FIXED_SUBSET`,
  `LEAVE_ONE_FOLD_OUT`, `LEAVE_ONE_SYMBOL_OUT`. Không dựng portfolio bằng
  cách nối các đường vốn tài khoản độc lập.
- **Lineage trình bày:** `outputs/revision/u09_manuscript_assets_v1/artifacts/
  {numeric_cells.json,support.json,points.json}` đã có binding trong manifest;
  source này giúp nối bảng U09 sang ô/đơn vị/ID. Đây là artifact dẫn xuất,
  không làm thay lịch sử nghiên cứu hoặc cho phép chạy generator ghi đè.
- **B08/F11:** B08 có danh sách nguồn, còn phải đọc/kiểm nội dung tại T48–T53.
  F11 có nguồn code/contract cho sơ đồ; ảnh browser và nghiệm thu trực quan
  chưa có trong phạm vi hiện tại. Có thể giải thích workflow không cần ảnh;
  không dùng mockup để giả làm screenshot đã đo hoặc coi T06 hoàn tất là
  nghiệm thu ứng dụng.

### 6.4. Danh mục hình

#### Hình F01–F11

| ID | Tên tiếng Anh / thông điệp | Vị trí | Task phụ trách | Loại nguồn | Nguồn | Nơi soạn/xuất dự kiến |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | **Decision cutoff, entry and exit of a trading cycle.** Thấy gì tại cutoff, vào/thoát khi nào; SHORT giữ CASH. | Ch. 3.1–3.2 | T09, T10 | MINH_HỌA | SRC01 | `diagrams/F01_trade_timeline.tex → .pdf` |
| F02 | **Chronological partitions and historical-label maturity.** Tách fit/selection/test, purge và maturity; không đưa nhãn query vào context. | Ch. 3.7; Ch. 5.2 | T15, T37 | MINH_HỌA | SRC02, SRC05 | `diagrams/F02_temporal_partitions.tex → .pdf` |
| F03 | **System overview from available inputs to evaluated actions.** Tách tính số, hosted inference, fit offline, policy và đánh giá. | Ch. 4.1 | T16 | MINH_HỌA | SRC03, SRC05, SRC06 | `diagrams/F03_system_overview.tex → .pdf` |
| F04 | **Candlestick and support-resistance inputs to Pattern and Trend.** Cho thấy hai đầu vào ảnh khác nhau trên cùng điểm, không đồng nhất ảnh với diễn giải đúng. | Ch. 4.3 | T19 | ĐO_ĐƯỢC | SRC09 (nguồn có sẵn T06); EX01-IP/IT (sản phẩm T19, §9.5) | `figures/F04_pattern.png; F04_trend.png; diagrams/F04_chart_pair.tex` |
| F05 | **Matured historical episodes and Bayesian context retrieval.** Lọc PIT trước matching/statistics; tách population, ví dụ và fallback. F05a giải thích resource regime riêng. | Ch. 4.5–4.7 | T23, T24, T25 | MINH_HỌA | SRC04, SRC08, RG01/RG02 và EX01 (§9.10) | `diagrams/F05_memory_retrieval.tex; F05a_regime_training.tex → .pdf` |
| F06 | **Prior tasks, target observations and frozen MT inference.** Tách task với episode/query; tách huấn luyện teacher/student khỏi inference. | Ch. 4.8 | T28, T29 | MINH_HỌA | SRC05, SRC10 | `diagrams/F06_mt_tasks_training.tex → .pdf` |
| F07 | **Fact Anchor and utility-gated action revision.** Giữ raw proposal, anchor và final action riêng; điều kiện Q10/Q90 nghiêm ngặt. | Ch. 4.8 | T30, T31 | MINH_HỌA | SRC06 | `diagrams/F07_action_policy.tex → .pdf` |
| F08 | **Shared upstream and within-repeat method dependencies.** Một upstream mỗi điểm; Common/anchor dependency dùng đúng repeat, fallback không tạo call giả. | Ch. 4.9 | T33 | MINH_HỌA | SRC03, SRC06 | `diagrams/F08_variant_dag.tex → .pdf` |
| F09 | **Mean account-return differences against Native and Common.** Giữ hai baseline, năm extension mỗi baseline và band mô tả; trục dùng pp. | Ch. 5.7–5.8 | T43 | DẪN_XUẤT | SRC08, SRC09 | `figures/F09_return_contrasts.py → .svg/.pdf` |
| F10 | **Historical-context coverage and final-action changes.** Hiện support, fallback/bypass và mức giữ anchor; không quy thay đổi gộp cho student riêng. | Ch. 5.8 | T44 | DẪN_XUẤT | SRC08 | `figures/F10_coverage_actions.py → .svg/.pdf` |
| F11 | **Application workflow and interpretation of a recorded result.** Theo đầu vào/tiến trình/kết quả, phân biệt raw/final/CASH và bối cảnh thực dùng. | Ch. 4.10; App. F | T35 | MINH_HỌA | SRC11 | `diagrams/F11_application_flow.tex; figures/F11_ui_*.png nếu được kiểm` |

### 6.5. Danh mục thuật toán

Đây là giả mã trình bày cho đường đã triển khai, không phải ba thuật toán
mới đã được chứng minh. Phải nêu input/output, điều kiện PIT, thiếu support,
đường lỗi và điểm lưu bền vững; không cho outcome quay lại đường dự báo.

#### Thuật toán A01–A03

| ID | Tên tiếng Anh / thông điệp | Vị trí | Task phụ trách | Loại nguồn | Nguồn | Nơi soạn/xuất dự kiến |
| --- | --- | --- | --- | --- | --- | --- |
| A01 | **Construct admissible historical context.** Giữ cutoff, reserved IDs, task boundaries và trạng thái thiếu support; query không có nhãn. | Ch. 4.9 | T33 | MINH_HỌA | SRC02, SRC04, SRC05 | `§4.9; label alg:pit-context` |
| A02 | **Run a method and resolve its final action.** Dựng prompt/schema đúng nhánh, lưu raw, xử lý dependency/facts/utility và checkpoint. | Ch. 4.9 | T33 | MINH_HỌA | SRC03, SRC06 | `§4.9; label alg:method-policy` |
| A03 | **Execute paired forecasts and evaluate separate accounts.** Chỉ nối outcome sau forecast bền vững; giữ economics, support và thứ tự tổng hợp đúng nghiên cứu. | Ch. 4.9 | T33 | MINH_HỌA | SRC01, SRC02, SRC03, SRC07, SRC08 | `§4.9; label alg:paired-evaluation` |

### 6.6. Danh mục bảng

B04–B07 có thể tách panel phụ nhưng giữ ID cha và provenance của từng panel;
không cộng support của hai nghiên cứu hoặc nhận panel thành phần thay cho
ablation MT-BICL chưa chạy.

#### Bảng B01–B09

| ID | Tên tiếng Anh / thông điệp | Vị trí | Task phụ trách | Loại nguồn | Nguồn | Nơi soạn/xuất dự kiến |
| --- | --- | --- | --- | --- | --- | --- |
| B01 | **Notation, terminology and units.** Một đối tượng có một nghĩa; K ví dụ khác K task, fraction khác %/pp. | Front matter; Ch. 3 | T05, T60 | DẪN_XUẤT | SRC01, SRC05 | `tables/B01_notation.csv + .tex` |
| B02 | **Component input-output and temporal contracts.** Mỗi thành phần có input/kiểu, cutoff, xử lý, output và bên dùng. | Ch. 4.2–4.4 | T17, T18, T19, T20, T21, T22 | DẪN_XUẤT | SRC01, SRC03, SRC04, SRC05, SRC06 | `tables/B02_component_contracts.csv + .tex` |
| B03 | **Method foundations, context and policy differences.** Native/Common/Base rõ phạm vi; so sánh matching/statistics/examples, dependencies và fallback. | Ch. 4.4, 4.7, 4.9 | T22, T27, T33 | DẪN_XUẤT | SRC03, SRC04, SRC05, SRC06 | `tables/B03_method_comparison.csv + .tex` |
| B04 | **Data, evaluation support and frozen configuration.** Tách cohort/loại trừ, bank, missingness, models, runtime và call/repeat units của hai nghiên cứu. | Ch. 5.2–5.3 | T37, T38 | ĐO_ĐƯỢC | SRC02, SRC05, SRC07, SRC08 | `tables/B04_data_configuration.csv + .tex` |
| B05 | **Component-study results and controls.** Giữ classification/account cùng support, tách main/upstream/factorial/numeric/scenario panels. | Ch. 5.6; App. D | T41 | DẪN_XUẤT | SRC07 | `tables/B05_component_results.csv + .tex` |
| B06 | **Historical-context results and paired comparisons.** Giữ đủ tám vai trò/hai economic controls, 20 contrast, ba bridge và sensitivity đúng nguồn. | Ch. 5.7; App. D | T42 | DẪN_XUẤT | SRC08, SRC09 | `tables/B06_context_results.csv + .tex` |
| B07 | **Traceable contexts, proposals, policies and outcomes.** Chọn tình huống theo rule, nối facts/context/raw/final/outcome; có fallback, veto và quyết định sai. | Ch. 5.8; App. B/D | T44, T45 | DẪN_XUẤT | SRC06, SRC08 | `tables/B07_case_traces.csv + .tex` |
| B08 | **Comparison with related research.** So sánh inputs, architecture, context/regime, PIT, economics và controls từ nguồn đã kiểm. | Ch. 2.7 | T53 | DẪN_XUẤT | SRC10 | `tables/B08_related_research.csv + .tex` |
| B09 | **Research questions, supported answers and remaining uncertainty.** Mỗi RQ nối với quan sát, kết luận có giới hạn và bằng chứng còn thiếu. | Ch. 5.9; Ch. 6.2 | T47, T56 | DẪN_XUẤT | SRC07, SRC08, SRC10 | `tables/B09_rq_answers.csv + .tex` |

### 6.7. Yêu cầu khi tạo sản phẩm ở task phụ trách

1. Trước khi tạo, đọc lại source đúng namespace/hash tại §3; lưu liên kết
   input/member/field → giá trị/đơn vị → figure/table/panel. Nhận định thiếu
   nguồn phải bỏ, thu hẹp hoặc ghi NA; không gọi model/thu dữ liệu/refit để
   làm đẹp danh mục. Những đường xuất dự kiến không được ghi thành file đã có.
2. Nhãn/caption/legend bằng tiếng Anh, giải thích được khi đọc độc lập.
   Caption của ảnh/ca thực ghi stock/cutoff, loại nguồn và ID truy vết phù
   hợp; số minh họa phải có nhãn `Illustrative`. Dịch chú giải hoặc báo cáo
   Việt để trình bày phải ghi rõ là bản dịch, giữ nguyên raw/hash gốc.
3. Sơ đồ nên dùng nguồn vector có thể sửa, đồ thị khoa học dùng công cụ plot
   chuẩn và xuất SVG/PDF. Giữ mã nguồn vẽ/bảng dẫn xuất trong gói sau; không
   biến ảnh raster hoặc đồ thị đo được thành hình AI tái dựng. Cặp PNG F04
   giữ nguyên byte nếu tái sử dụng; chú giải đặt ở caption/layout riêng.
4. Khi dựng F01/F07/A02, giữ entry Open(t+1), exit Close(t+3), phí hai chiều,
   SHORT=CASH và hai dấu strict Q10/Q90. Khi dựng F03/F08/A03, tách upstream
   chung khỏi repeat; fallback/bypass không phải một response mới.
5. F09/B05/B06 phải ghi support và đơn vị %/pp, estimator và loại band của
   đúng nghiên cứu; giữ kết quả âm, NA, bootstrap undefined và fallback trong
   tập chính. Không dùng “significant”, “calibrated” hoặc “profitable” mạnh
   hơn bằng chứng. F10/B07 không suy hiệu quả student riêng khi thiếu ablation.
6. Khi chuyển LaTeX, sinh references/danh mục tự động, kiểm chữ đủ đọc, không
   cắt/chồng bảng/hình và xem bản render ở task tương ứng. T06 chỉ chốt danh
   mục và nguồn, chưa chạy build hoặc kiểm trực quan các sản phẩm tương lai.

## 7. Ví dụ xuyên suốt có truy vết

### 7.1. Danh tính và quy tắc chọn

**EX01 — A historical FPT decision at the 3 July 2023 cutoff.** Dùng
`FPT-2023-07-03`, fold `b2023_h2`, upstream realization `u0`, Decision
repeat `r0` của nghiên cứu historical-context U08/U09 tại §3. Đây là **bản
ghi thực đã lưu**, không phải số giả định, lần chạy mới hoặc trường hợp của
nghiên cứu component. Chất lượng nguồn giữ nguyên
`U08_HOSTED_HISTORICAL_EXPLORATORY`; execution diễn ra ngày 10/11/2026 với
cutoff lịch sử, không phải giao dịch đã thực hiện vào tháng 7/2023.

Quy tắc biên tập `EX01_SELECTION_V1` được đặt ở T07, **sau khi nghiên cứu
đã khóa**, không phải đăng ký trước thực nghiệm:

1. Bắt đầu từ 102 `point_id` trong U09 `predictions.csv`; lấy CORE4
   FPT/MWG/VCB/VNM để có signal memory cùng phạm vi (48 điểm).
2. Giữ điểm có đủ tám dòng phương pháp nghiên cứu tại repeat 0 (48 điểm),
   `MT_BICL.eligible=True` (29 điểm), và `bayesian_v1.bypass=False`
   (vẫn 29 điểm). Bypass của các nhánh khác được giữ nguyên.
3. Sắp tăng theo `(date, symbol)`, chọn điểm đầu tiên; cố định repeat 0,
   không chọn lại repeat cho kết quả đẹp hơn. Kết quả là `FPT-2023-07-03`.
   Việc lọc/xếp hạng chỉ dùng ID, ngày, mã, method, repeat, eligible và bypass;
   không dùng label, return, raw/final action, độ đúng hoặc mức thay đổi policy.
4. Sau khi cố định ID, nối shared/prepare/forecast/outcome và provider theo
   §7.2; kiểm hash và thời gian trước khi diễn giải. Thiếu nguồn phải ghi NA
   hoặc dùng minh họa có nhãn `Illustrative`, không gọi model để bù. EX01
   hiện có đủ nguồn nên không cần một trường hợp giả định thay thế.

Các bộ lọc này chủ động chọn trường hợp có context để giải thích cơ chế;
EX01 không đại diện ngẫu nhiên cho 102 điểm và không dùng để ước lượng hiệu quả.

### 7.2. Chỉ mục nguồn và đường nối

Hash dưới đây là SHA256 đầy đủ. `raw member` băm byte JSON trong ZIP;
`output_sha256` và `membership_sha256` là digest nội dung theo hợp đồng,
không được thay thế cho nhau. Gói ngoài được khóa tại §3; T07 đã kiểm lại
U08, U09, U06 assets v2 và acceptance U09 trước khi đọc nguồn.

| ID | Gói / member / trường được dùng | SHA256 raw member |
| --- | --- | --- |
| EX01-P | [U09](../docs/plan/week12/unified_analysis_results.zip), `outputs/unified_integration/u09_analysis_r1/predictions.csv`; chọn bằng khóa `(point_id, method, repeat)` | `d7d5f9b90d009f3da31de64df067ae9ac4ff72ccd395debf6c7f8ff08aa1da32` |
| EX01-C | [U06 assets v2](../docs/plan/week12/unified_comparison_assets_v2.zip), `outputs/unified_integration/u06_assets_v2/providers/FPT-2023-07-03.json`; `context` và chuẩn bị offline | `64e5d696a50b33a8f7b11cade299511e6c41c4dc458dcfeefff28100b51007c7` |
| EX01-S | [U08](../docs/plan/week12/unified_live_research.zip), slot `shared/FPT-2023-07-03`, file `7ace396801b8666a24f23ed0aef3466aa073db80185db93ceab24d48741a9ec3.json` | `42296f5e9e1c8b5ba25730a19adf0cd8445d251486116029bc2191e3f57e79cc` |
| EX01-O | U08, slot `outcome/FPT-2023-07-03`, file `44ee5a008ff1b2964ddf676f02420fe9ed5a3f9aadb87e8a5bc789af23822605.json`; `output.target` | `ccc7cd71bc2877ea821b372b68427c9bf2d76636c944e4c66539dea4dd839866` |
| EX01-IP | U08, slot `render/FPT-2023-07-03/pattern`, file `6b58a30a0892e8ff6aa4e61d0486edcbe0877d3deb02cbb9cbb62060385cabb6.json` | `3138604be32bcd9bd21970a25f19a8d6e0d278455de87532c9b7be67d35e54a9` |
| EX01-IT | U08, slot `render/FPT-2023-07-03/trend`, file `6b920deb6684e0c6d03260866aa93e3cdbff66eb0e16ed5685caad707afe2c12.json` | `d8c737cbdce366738a7e466c218a36c2955d8674a8262816941bb107dde72733` |

Các file slot U08 đều nằm trong
`outputs/unified_integration/u08_research_r1/slots/`. Đọc envelope `payload`,
rồi `attempts[0].output`; các attempt được dùng đều `complete`. Với forecast,
prepared context nằm tại `payload.inputs.prepared`, còn response/policy tại
`attempts[0].output.forecast` và `.policy`. Bảng sau ánh xạ
`forecast/FPT-2023-07-03/u0/r0/<method>` → file slot → hash byte:

| Method | File slot JSON | SHA256 raw member |
| --- | --- | --- |
| original_fix | `416712d1d7a3ef607c0f2031ef8ded6c9509fe4221bb795d70d6c7de005edb9d.json` | `e27e0e8920e151b23bcd2c0f4d45cad395a2a061082aea859a8d4284172ea7b5` |
| original_common | `64423caca8a47ecfcb81e2d2d7c9a9d6c6618facc1ef45e84c1e327d5f13fbe2.json` | `203a51ac6c6f79ea429b565b067f39f8283b46d10b002ab1a9fec5a9d90037da` |
| bayesian_v1 | `f875086c494f4b35ab84f1e1df38e0fd152df7f00cbc53e4ba615fcbd2551509.json` | `366b32095f0f5f022bc9852034c28bde87521eae720449b722061b130083d0f3` |
| C2 | `d33c4a932ddfe9a5365fe271c5b176488aff85a5cb59bb01db5cf8693becf693.json` | `104be95520b47e7bd2ad6071002d5e039b1ec3c2f3264a20636f85faacedf00a` |
| A_tp_pool | `b199c2067d02f4c41f370f39ae0828abc1fc14a6857e641265bda184f8971e8b.json` | `eb214c58c10e72a7c874ab80a63ea7b5a7bf3877968d74dbda6ab31e54b21a41` |
| B_semantic | `80c295792334b939858325b602e480ec1a847ee6dfb28862c7470b5d9769728e.json` | `a616a82c575600ad311b83b93c3a04c6c14baf510911d56f428cbb3e63a5433a` |
| MT_BICL | `58d6247d4cdd587aade0b220539c197053b921d48fde462bd1e4725ee56919ad.json` | `1a490828b1596a0b605da6371f2fd4bc6f95876ce590765582441828076e6fb0` |
| Fact_Anchor | `3fc8ef7e65fb8ae2cacb89fa3ce5bce94e98ef48a894e65cc74a48924b1b3b61.json` | `c9ebdeb3c900f5633234e7915b8f8129f5e0d919dc8115f9725da5de42109c44` |

Tám forecast cùng `shared_sha256` =
`e6c16c36dd776a804922f466af1c9742bf3ba70015d60929e4112992e269a103`,
khớp output của EX01-S. Các nhánh fallback nối output Common cùng repeat
`964b7aa19d16e01affa47869a62a2ad20bcc8c1a0eb204f4926abc92a9471c41`;
MT còn nối Fact Anchor
`49f6edd2a051b94bee3bc642f9c97f43e781ddd1a0cacf3a595562e3f9882269`.
Không chạy lại upstream cho từng nhánh/repeat. EX01-C là nguồn **offline
preflight**, không phải response thị trường; membership context tính lại
theo JSON compact của `query/scaler/prior/target/advisor` khớp
`9ed7e2a35da59ea5157fb6fe2baacd09671ebf12749943d0882bc98bc98f3cb4`
ở EX01-C và hosted MT `prepared.aux.branch`. Chỉ nối context qua binding này,
không dùng `probe_raw/probe_policy` offline làm kết quả LLM.

### 7.3. Đầu vào ở cutoff và ranh giới thông tin

| Record / availability | Giá trị đọc từ nguồn | Cách dùng khi viết |
| --- | --- | --- |
| Price prefix — EX01-S | 600 nến OHLCV từ 02/02/2021 đến 03/07/2023; mọi ngày ≤ cutoff | Prefix cho đường dữ liệu 600 nến; không đưa các giá entry/exit vào input |
| Chart window — EX01-S/IP/IT | 45 nến cuối, 27/04/2023–03/07/2023 | Candlestick và support–resistance là hai view của cùng cửa sổ |
| Numeric fact packet — hosted MT `prepared.aux.packet` | Close 48.18, SMA20 47.5675, MACD 0.6542675609756259, Signal 0.7043937016476567; `prefix_rows=45`, frame end 03/07/2023 | Đơn vị giá nguồn là nghìn VND; packet ghi MACD_SIGNAL=BELOW, MACD_ZERO=POSITIVE, PRICE_SMA20=ABOVE |
| Upstream reports — EX01-S | Indicator ghi MACD dưới Signal; Pattern dự báo tăng, độ tin cậy thấp; Trend tăng, support 47.8/resistance 49.2 | Đây là báo cáo/đánh giá của agent, không phải nhãn giá tương lai. Khi diễn giải tiếng Anh phải ghi là bản dịch/tóm tắt |
| Sentiment — EX01-S | `is_unavailable=True`, article_count=0, verified_article_count=0, scored_articles rỗng, news_dates rỗng | **Unavailable**, không coi là một quan sát thị trường trung tính. Mã legacy `NEUTRAL` trong signal memory không bổ sung bài báo |
| Alpha profiles — EX01-S và forecast profile | Native giữ payload legacy; Common dùng `causal_alpha.projection`, cutoff 03/07/2023, selector đã khóa | Không gọi hai input profile là giống hệt nhau hoặc dùng một ví dụ để chứng nhận Native PIT |
| Historical context — EX01-C và hosted prepared | Chỉ các observation đã có exit trước 03/07/2023; query không có `y/r_net` | Nhãn lịch sử đã trưởng thành là hợp lệ cho context; nhãn query thuộc §7.6 |

Digest của sáu cột OHLCV 45 nến cuối, JSON UTF-8 sort keys/compact, là
`3fc47186925157588db7b2d9d34a66ef29822087a27acdb39825fd8f0e77c908`;
khớp `inputs.kline_sha256` của cả hai render slot. Ảnh giải mã có hash
`d423db489a59706c4aae32e1f9de49cc63f73eded74f8e6f97c018cd1211200f`
(pattern, 52,655 byte) và
`93744337e0d375c04973332e4dba86c75d55d79398ed4553ad26a8d8593f3734`
(trend, 75,628 byte). Chưa xuất ảnh mới; T19 có thể dùng đúng nguồn EX01 này.
Cặp PNG CMG trong F04/§6 là trường hợp khác, không gắn lại nhãn thành FPT.

### 7.4. Hai loại lịch sử và hai nguồn regime

**Signal prior v1:** hosted `prepared.trace.retrieval` ghi regime
`CONSOLIDATION`, same-symbol eligible_count=211, matched population=19 và
ba example được chọn. Selected scores theo thứ tự là 1.0, 0.75, 0.75.

| Episode ID | As-of → entry → exit | Net return lịch sử (%) |
| --- | --- | --- |
| FPT:2022-04-07 | 07/04 → 08/04 → 13/04/2022 | +0.8800636494421088 |
| FPT:2022-04-18 | 18/04 → 19/04 → 21/04/2022 | −4.533273497129919 |
| FPT:2022-04-13 | 13/04 → 14/04 → 18/04/2022 | −0.43895669480141786 |

Không lấy ba example làm mẫu số thống kê: v1 win_rate_long=9/19;
bull_trap_rate=9/18. C2 ghi population_count=19 dưới min_population_count=20,
conditional_count=1 dưới min_conditional_count=5; C2/A/B đều có gate
`INSUFFICIENT_EVIDENCE`, `LOW_POPULATION_SUPPORT`, `NO_READY_METRICS`.
V1 có example không có nghĩa các gate của C2/A/B phải mở.

**Numeric MT context:** EX01-C có `K=3` prior tasks (11 observation) và
`m=3` target observation, tổng 14 hàng lịch sử; đây không phải ba signal
example ở trên. Mọi ID ở bảng sau có tiền tố `FPT-` trước ngày observation.

| Context group / task ID | Ngày observation được chọn | Exit muộn nhất |
| --- | --- | --- |
| Prior / FPT:block0011 | 2020-10-14, 2020-11-04, 2020-12-03, 2020-12-21, 2020-12-24 | 2020-12-29 |
| Prior / FPT:block0015 | 2021-10-21, 2021-10-26, 2021-11-16, 2021-11-24 | 2021-11-29 |
| Prior / FPT:block0013 | 2021-07-01, 2021-07-09 | 2021-07-14 |
| Target / FPT:block0021 | 2023-06-16, 2023-06-21, 2023-06-26 | 2023-06-29 |

Target exits lần lượt 21/06, 26/06 và 29/06/2023, đều strict < cutoff.
Query `FPT-2023-07-03` thuộc task `FPT:block0021` nhưng **không có nhãn**.
Query có entry_date/exit_date theo lịch horizon; sự hiện diện của các ngày
lịch không cho phép đọc giá tương lai. Các ID context và scaler-fit không
trùng 102 evaluation IDs được dành riêng.

MT query regime là **BULL**, nguồn VNINDEX/HMM với feature_end_date
03/07/2023, model_fit_cutoff/model_training_end_date 31/12/2020, model hash
`cf711a9ce10dd1ebbccbeae048cce5bbd9f10271b9bab67a21e33aff5258541d`.
Scaler frozen_train: fit_count=731, fit_cutoff=31/12/2020,
fit_max_exit_date=29/12/2020. **CONSOLIDATION của v1 và BULL của MT là hai
trường/nguồn regime khác nhau**, không đồng nhất hoặc tự sửa để kể một câu
chuyện nhất quán. Source đã khóa quyết định cách mô tả từng đường chạy.

### 7.5. Proposal, anchor và hành động thực thi

Các ô NA dưới đây là không có raw response vì bypass, không phải dự báo
SHORT/LONG ngầm định. Request ID nối trực tiếp tới response đã lưu ở U08.

| Method | Raw proposal | Final action | Policy reason | Source request ID |
| --- | --- | --- | --- | --- |
| Native / original_fix | SHORT | CASH | RAW_DECISION | `a405af62-8faa-4d8c-bbcb-cee3f7bddb27` |
| Common / original_common | LONG | LONG | RAW_DECISION | `e9cd5100-0f68-4677-8ca5-84a08e41386c` |
| bayesian_v1 | LONG | LONG | RAW_DECISION | `4ccd3bbe-9004-468f-a5dd-8859a2c53c97` |
| C2 | NA | LONG | FALLBACK_ORIGINAL | NA — dùng Common r0 |
| A_tp_pool | NA | LONG | FALLBACK_ORIGINAL | NA — dùng Common r0 |
| B_semantic | NA | LONG | FALLBACK_ORIGINAL | NA — dùng Common r0 |
| MT_BICL | LONG | LONG | KEEP_PROPOSED_SAME | `cc6bf729-784a-458a-8e40-07398fac513f` |
| Fact_Anchor | LONG | LONG | NO_NUMERIC_VETO | `f7c7664b-69c7-4bef-a075-26c2d9c0d6e2` |

Có năm Decision response mới và ba bypass tại repeat này; chỉ có một realization
upstream chung. Hai control đã đăng ký là CASH_EVERY_CYCLE=CASH và
ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS=LONG, không có response LLM.
Native SHORT được ánh xạ thành giữ tiền, không phải bán khống cổ phiếu.

MT ghi student probability `0.38681803029367656`; teacher posterior mean
theta `0.3777360437578734`; utility source
`TEACHER_SIGN_BAYESIAN_BOOTSTRAP_MAGNITUDE`, mean_U_net_fraction
`-0.00597534968574255`, Q10 `-0.01288257428075956`, Q90
`0.0002422913686701239`; 4,096 draws, gain_count=5, loss_count=9.
Đây là các số đã lưu trước khi đọc outcome query, không phải lợi nhuận query
thực hiện hoặc xác suất được chứng minh calibrated. K=3/m=3 có nghĩa như §7.4.

Fact assertions của MT hợp lệ và eligible=True, nhưng raw LONG đã giống
anchor LONG nên policy giữ `KEEP_PROPOSED_SAME`; không có veto trong ca này.
Không suy rằng mean utility âm bắt buộc chuyển CASH: điều kiện đổi hành động
dùng Q10/Q90 theo §5, không dùng dấu của mean; Q90 ở đây vẫn dương.
Validity của ba assertion không chứng minh toàn bộ lập luận văn xuôi đúng.

### 7.6. Outcome chỉ đọc sau quyết định

EX01-O ghi decision date 03/07, entry 04/07, phiên trung gian 05/07,
exit 06/07/2023. Giá đã quy đổi VND: decision_close=48,180,
entry_open=48,180, exit_close=48,390. LONG mua Open(t+1), bán Close(t+3),
phí môi giới 0.25% và slippage 0.10% **mỗi chiều**, label_contract_version
`net_cycle_v1`; label kinh tế theo oracle `compute_round_trip_net_return`.
Không dùng Close-to-Close để thay thế.

- Gross return đã lưu: `0.004358655043586568` = **+0.4358655044%**.
- Net return đã lưu: `-0.00264731712420041` = **−0.2647317124%**;
  label_gross=UP nhưng **label_net=DOWN**.
- Vì vậy LONG của Common/v1/MT/Anchor và các fallback là một quyết định
  sai theo nhãn net ở chu kỳ này; Native CASH không chịu lỗ chu kỳ LONG đó.
  CASH control có payoff chu kỳ 0, Always-LONG nhận net return trên. Không
  biến một payoff chu kỳ thành tổng lợi nhuận tài khoản hoặc kết quả 306 dự báo.

Giá entry/exit, return và label ở mục này không thuộc đầu vào §7.3–§7.5.
EX01 không chứng minh một phương pháp tốt hơn; giữ cả hành động sai và chi
phí làm đổi dấu kết quả, không chọn lại một ca thắng sau khi thấy outcome.

### 7.7. Cách tái sử dụng và quy tắc cho nhóm tình huống sau

- Ch. 4.1/T16: mở EX01 ở cutoff, giải thích mục đích các module; chưa lộ
  outcome. Ch. 4.3–4.5/T19/T20: inputs, hai view, missing sentiment và hai
  loại lịch sử. Ch. 4.6–4.8/T21–T24: nối v1/C2/A/B, numeric context,
  teacher/student và anchor/policy; giữ hai nguồn regime riêng.
- Ch. 4.9/T25: shared u0 và các nhánh/repeat; Ch. 5.8/T45: mở outcome
  §7.6 sau facts/proposals/actions. B07/F10 có thể dùng EX01, nhưng ví dụ
  này không đại diện cho veto hoặc chứng minh cải thiện student riêng.
- Quy tắc biên tập cho T45: xét repeat 0, yêu cầu nguồn/hash đầy đủ rồi
  chọn ca đầu theo `(date, symbol)` trong từng nhóm đã định nghĩa: đủ context
  (MT eligible và v1 không bypass), thiếu support (gate insufficient và
  bypass), bất đồng (raw proposal khác anchor), veto (policy thực sự đổi
  hành động), và sai (LONG với label_net=DOWN hoặc CASH với label_net=UP).
  Công bố predicate thực dùng, mẫu số, ID và nhãn nhóm; cho phép một ca
  thuộc nhiều nhóm. Nhóm sai dùng outcome **có chủ đích để minh họa lỗi**,
  không dùng để ước lượng accuracy. Nhóm không có ca phù hợp ghi không có;
  chỉ dùng minh họa gắn nhãn rõ nếu cần giải thích, không giả có veto đã đo.
- T07 chưa chọn thêm các ca T45, viết các mục chương, tạo hình/bảng hay xây
  UI. Không thay bằng screenshot live để làm chứng cứ dự báo lịch sử. Ba
  module live giữ cùng logic/snapshot nghiên cứu theo xác nhận tại §3;
  hash raw vẫn giữ để truy vết. Native causal audit FAIL, overall
  NOT_CERTIFIED và các giới hạn/F11/F12 tại §3 vẫn nguyên vẹn; các kiểm tra
  thời gian cục bộ EX01 không nâng thành chứng nhận nhân quả toàn hệ thống.

## 8. Khung bản thảo và đối soát luận điểm

### 8.1. Điểm vào sáu chương

Sáu file dưới đây được khởi tạo từ **khung Markdown** tại T08. Chương 3 nay
có bản nháp §3.1–§3.7, chưa qua rà soát toàn văn; các chương khác vẫn có
placeholder. Phạm vi đối soát nội bộ ghi tại §8.2.
Tiêu đề chương/mục giữ theo [dàn bài §C](outline.md#c-detailed-chapter-outline).
Các mục chưa viết có block `Not yet drafted` nêu cụ thể nội dung còn thiếu. Các ghi chú
này là hỗ trợ viết, phải được thay bằng nội dung và kiểm nguồn ở task tương
ứng; không đưa nhãn placeholder vào bản nộp. Không suy hoàn thành các task
viết từ việc đã có file hoặc tiêu đề.

| File bản thảo | Nguồn bắt đầu trong sổ chung | Nội dung cần viết, chưa phải kết quả đã có |
| --- | --- | --- |
| [01_introduction.md](chapters/01_introduction.md) | §1 metadata; §2 và outline §A về RQ/đóng góp; §3 giới hạn | Bối cảnh, bài toán, câu hỏi, giới hạn, đóng góp và mạch sáu chương |
| [02_related_work.md](chapters/02_related_work.md) | §4 reading register/khóa citation; §5 thuật ngữ; §6 B08 | Kiểm nguồn gốc, tổng hợp tài liệu, ghi nhận kế thừa và khoảng trống có căn cứ |
| [03_background.md](chapters/03_background.md) | §3 nguồn hợp đồng; §4 tài liệu phương pháp; §5 ký hiệu; §6 F01/F02; §8.4–§8.5 binding nền tảng | Bản nháp §3.1–§3.7; claim đối soát nội bộ ở §8.2; chưa rà soát khoa học/trích dẫn/toàn văn cuối |
| [04_proposed_system.md](chapters/04_proposed_system.md) | §3 source/runtime; §5 tên/ID; §6 danh mục; §7 EX01; §9 nguồn phương pháp | §4.1–4.7 và Fact Anchor/tác vụ/teacher–student của §4.8 đã có bản nháp, kèm F03/F04/F05/F05a/F06; utility/projection/chính sách sửa action/traceability/điều phối/ứng dụng còn placeholder |
| [05_experiments.md](chapters/05_experiments.md) | §3 hai nghiên cứu; §6 bảng/hình; §7 ca EX01 | Thiết kế, số liệu chính xác, ô bảng có nguồn, phân tích/band/ca sai và giới hạn |
| [06_conclusion.md](chapters/06_conclusion.md) | §2 RQ/đóng góp và giới hạn §3; kết quả Ch. 5 sau khi viết | Trả lời RQ, đóng góp có giới hạn, hạn chế và hướng phát triển; không thêm kết quả mới |

Không tạo sổ nguồn thứ hai, bibliography cuối, file phụ lục rỗng hoặc khung
LaTeX toàn văn trong bước này. `evidence.md` tiếp tục là nơi giữ nguồn,
ghi chú đọc, luận điểm, đơn vị, hình/bảng và vấn đề bằng chứng. Nội dung
chương bằng tiếng Anh; hướng dẫn quản lý trong sổ này bằng tiếng Việt.

### 8.2. Quy ước ánh xạ luận điểm và ô bảng khi viết

Các dòng dưới ánh xạ **luận điểm/ô bảng đã viết trong bản thảo**, hiện thuộc
Chương 3–4 và hình kèm theo. Đây là đối soát nội bộ, chưa phải phản biện bản thảo
hoặc xác nhận nhân quả toàn hệ. Các số đã kiểm ở §3/§7 vẫn là bằng chứng
nguồn; việc chép vào chương phải có ánh xạ cụ thể và kiểm lại cách diễn đạt.
Thêm dòng vào bảng dưới khi một luận điểm, công thức hoặc ô bảng được viết;
chỉ gán ID `CL001`, `CL002`, … khi có nội dung thật, không gán ID giả cho
placeholder. Giữ ID khi sửa cách diễn đạt, không tái dùng cho luận điểm khác.

| Claim ID | Đích bản thảo và nội dung chính xác | Loại bằng chứng | Nguồn, phiên bản, hash và locator | Đơn vị, support và phép dẫn xuất | Phạm vi kiểm, giới hạn và việc còn thiếu |
| --- | --- | --- | --- | --- | --- |
| CL001 | [§3.1.1](chapters/03_background.md#311-daily-observations): trường OHLCV, ngày quan sát và ý nghĩa chỉ số hàng | HOP_DONG_TRIEN_KHAI | TIME03–TIME05 tại §8.4; `price_view`, `snapshot_payload`, `HistoricalData.prefix/state` | Một chuỗi/mã; i=0..N−1 sau khi xác định analysis view; unit/price basis giữ theo nguồn | Đối soát 15/11/2026; đây là định nghĩa dùng trong nghiên cứu, không chứng nhận lịch sàn, unit vendor hoặc thời điểm công bố thực |
| CL002 | [§3.1.2 và bảng event/index](chapters/03_background.md#312-decision-cutoff-and-the-exclusive-window-boundary): [e−W,e), t=e−1, entry=e, exit=e+L−1 | HOP_DONG_TRIEN_KHAI | TIME01 `_prepare_window/_get_actual_direction`; TIME02 `target_fields` | Chỉ số nguyên zero-based trên chuỗi mẹ; L=3 cho daily contract, không phải cộng ba ngày lịch | Đã đối chiếu hai đường nguồn frozen; reset index cửa sổ không đổi cutoff của chuỗi mẹ; không diễn giải thành quy định thanh toán hiện hành |
| CL003 | [§3.1.3](chapters/03_background.md#313-chart-windows-longer-history-and-warm-up): W=45, A=600, điều kiện đủ prefix/horizon và tối thiểu 603 hàng cho một query sớm nhất | DAN_XUAT | TIME01 `ALPHA_HISTORY_CANDLES/required_backtest_rows/build_walk_forward_end_indices`; TIME03 `state` | max(W,A)+L = max(45,600)+3 = 603; ba hàng cuối dùng đánh giá | Kiểm số học và slicing nguồn; không gọi engine/API; không phải ngưỡng hội tụ indicator, số hàng train hoặc bảo đảm mọi feature hợp lệ |
| CL004 | [§3.1.4](chapters/03_background.md#314-missing-and-invalid-records): analysis view, suffix sau OHLC lỗi, thiếu prefix/horizon và UNKNOWN | HOP_DONG_TRIEN_KHAI | TIME04 `price_view`; TIME03 `prefix/state`; TIME01 `_get_actual_direction`; TIME02 `target_fields` | Kiểm ngày/finite/OHLC/volume; thiếu observation không được tự thay bằng nến giả | Chỉ mô tả đường frozen đã đọc; phân biệt helper UNKNOWN với target contract ném lỗi; không nâng thành mô tả tất cả loader hoặc chứng nhận causal |
| CL005 | [§3.1.5](chapters/03_background.md#315-a-dated-example): dates, số nến và chỉ số hàng của EX01 | DAN_XUAT | EX01-S/EX01-O tại §7.2 và TIME06 tại §8.4; `price_prefix.Datetime`, `target.decision_bar_index`, `dates` | 600/45 quan sát; t=872 → e=873; start=e−45=828, exit=e+3−1=875; dates từ nguồn, không cộng ngày lịch | Join point/source hash và kiểm cutoff/prefix; số hàng/các ngày là dữ liệu đã lưu, indices còn lại là số học; chưa đọc giá/return vào input hoặc sinh lại outcome |
| CL006 | [F01](assets/diagrams/F01_trade_timeline.pdf), chèn tại §3.1.5: lịch sử khả dụng, entry/exit và EX01 | MINH_HOA | TIME01–TIME03, EX01-S/O; nguồn TikZ và sản phẩm có hash tại §8.4 | Hình contract; khoảng cách không theo thời gian lịch; không hiển thị giá tương lai | PDF một trang đã build/render/xem 15/11/2026; chưa phải sơ đồ chia tập F02, công thức phí T10 hay kiểm bố cục PDF toàn văn |
| CL007 | [§3.2.1–§3.2.2](chapters/03_background.md#321-a-candidate-long-cycle): công thức hai chiều, nhãn strict >0, SHORT=CASH và payoff theo action | HOP_DONG_TRIEN_KHAI | TIME01/TIME02, hàm oracle/accounts/target_fields; §8.5.1 | Fraction trong công thức, % khi hiển thị; không dùng số làm tròn sinh nhãn | Đối chiếu nguồn frozen; giả định nghiên cứu, không phải quy định sàn hoặc xác nhận giao dịch thật |
| CL008 | [§3.2.3](chapters/03_background.md#323-illustrative-calculation): entry 100, exit 100/103 và biên break-even | MINH_HOA | Oracle TIME01; phép tính tại §8.5.1 | Net −0.6975568073%/+2.2815164885%, hiển thị 6 chữ số; CASH=0 | Đã kiểm bằng hàm oracle trích AST; số giả định có nhãn Illustrative, không phải kết quả nghiên cứu |
| CL009 | [§3.3.1](chapters/03_background.md#331-five-deterministic-indicator-families): công thức/kwargs năm chỉ báo, heuristic khác probability | HOP_DONG_TRIEN_KHAI | Toolkit/Indicator frozen §8.6, TA-Lib official references | MACD12/26/9, RSI14, Stoch14/3/3, WILLR14, ROC10 | Đối chiếu source; current upstream không thay runtime study; không tính lại chỉ báo |
| CL010 | [§3.3.2](chapters/03_background.md#332-alpha-transformations-and-selection): expanding normalization, IC/orientation và selector | HOP_DONG_TRIEN_KHAI | `core/causal_alpha.py` frozen §8.6, Kakushadze2016v3 cho nguồn candidate | Spearman train, ranking validation; sample std expanding | Không gộp native, không suy hiệu quả test hoặc calibrated probability |
| CL011 | [§3.3.3](chapters/03_background.md#333-sentiment-and-missing-information): news score, availability, decay và unavailable | HOP_DONG_TRIEN_KHAI | TIME03 `FrozenNews`, EX01-S | Window90 ngày, minimum3, half-life30; date-only ngày sau | Đọc source/trace đã lưu; legacy NEUTRAL không phải tin quan sát |
| CL012 | [§3.4.1–§3.4.2](chapters/03_background.md#341-latent-states-and-observed-features): HMM, features VN-Index, fitting/scaling/mapping/fallback | HOP_DONG_TRIEN_KHAI | Regime source frozen §8.6; Hamilton/Rabiner và hmmlearn official về khái niệm | 4 Gaussian diag states; log return/std20 ddof1/distances20/50/200 | Không fit; source default training range khác resource cutoff; giữ provenance hai nhánh EX01 |
| CL013 | [§3.4.3](chapters/03_background.md#343-endpoint-inference-and-future-observations): endpoint filtering=smoothing với model cố định và prefix cắt đúng | DAN_XUAT | Rabiner1989 §III.A–B, `classify_regime` frozen | Chỉ posterior hàng cuối, không Viterbi hoặc hồi tố hàng trước từ chuỗi dài | Kiểm source và suy luận từ backward endpoint; không suy fit/model/scaler đã PIT chỉ vì data prefix đúng |
| CL014 | [§3.5.1](chapters/03_background.md#351-counts-and-a-conjugate-update): Beta conjugacy và minh họa 7/10 | MINH_HOA | Beta density/algebra; Stan author case study; SciPy quantiles | Beta2,2→9,5; mean9/14; CrI [.385738,.861421] | Kiểm số học, có nhãn Illustrative; không phải nghiên cứu thị trường |
| CL015 | [§3.5.2](chapters/03_background.md#352-conditional-evidence-with-a-disjoint-background): background plug-in rời C và toy posterior | HOP_DONG_TRIEN_KHAI | Conditional statistics frozen §8.6, ví dụ §8.5.4 | B=11/18,C=3/4,tau4→Beta5.4,2.6 mean.675; CrI [.339435,.928893] | Kiểm AST hàm thuần và quantile; không tích phân uncertainty background; zero-support giữ NA |
| CL016 | [§3.5.3](chapters/03_background.md#353-interval-meaning-readiness-and-example-counts): CrI, support và K riêng | HOP_DONG_TRIEN_KHAI | Prior gate/retriever frozen §8.6 | Population≥20, conditional≥5,width≤.75; example readiness độc lập | Không suy gate giao dịch/CASH từ gate evidence hoặc interval coverage được hiệu chuẩn |
| CL017 | [§3.6.1](chapters/03_background.md#361-prior-tasks-target-observations-and-the-query): multi-task khác multi-agent, task/target/query | HOP_DONG_TRIEN_KHAI | MT bank/tasks/features frozen §8.6; Zhu2026 §4/PFN concept | Block63 reference-calendar observations, không phải elapsed days; K≤3, m≤8 | Kiểm source/membership; không dùng nhãn query hoặc nhập performance paper nguồn |
| CL018 | [§3.6.2](chapters/03_background.md#362-a-frozen-teacher-and-a-learned-student): teacher mixture count, frozen student/distillation và LLM riêng | HOP_DONG_TRIEN_KHAI | MT teacher/replica student frozen §8.6; recipe §3.4 | Prior tasks reweight component, target counts update target Beta; soft CE query mask | Không chạy student/teacher inference hoặc fit; teacher không hồi quy continuous query feature |
| CL019 | [§3.6.3](chapters/03_background.md#363-from-sign-probability-to-net-return-utility): U=theta*g−(1−theta)*loss và toy −.004 | MINH_HOA | Utility source frozen §8.6; phép tính §8.5.5 | p=.8,g=.01,loss=.06 → −.4%; utility source teacher, student log riêng | Kiểm toán học; không chạy 4096 draws hoặc sinh lại utility study |
| CL020 | [§3.6.4](chapters/03_background.md#364-anchor-relative-action-revision): strict Q10 delta utility, anchor/fallback | HOP_DONG_TRIEN_KHAI | MT policy frozen §8.6 | CASH→LONG Q10U>0, LONG→CASH −Q90U>0; equality reject | Kiểm source và dấu; lỗi kỹ thuật không thành bypass; quantile không bảo đảm lợi nhuận |
| CL021 | [§3.7.1](chapters/03_background.md#371-availability-at-a-query-cutoff): PIT/maturity/resource/reserved/query và row-wise causality | HOP_DONG_TRIEN_KHAI | TIME03, alpha/MT/unified provider frozen §8.6; giới hạn §3 | Giá≤d_t,tin availability≤cutoff,cycle exit<d_t; reserved IDs loại toàn cục | Không ghi toàn hệ causal PASS; không dùng outer cutoff sửa giá trị hàng lịch sử |
| CL022 | [§3.7.2](chapters/03_background.md#372-chronological-partitions-and-purging): purge labels tại boundary | HOP_DONG_TRIEN_KHAI | Causal alpha/protocol frozen §8.6; sklearn guide về temporal evaluation | Exit<b cho split trước; exit=b hoặc >b purge, không xóa toàn history giá | Không tự đặt actual fold dates hoặc gọi exposed folds untouched holdout |
| CL023 | [§3.7.3](chapters/03_background.md#373-pairing-and-units-of-evidence): paired immutable parent, repeat/slot/bypass/market support | HOP_DONG_TRIEN_KHAI | Unified providers/methods frozen §8.6, §3 U08/U09 | 102×3×8=2448 slots conditional trên cùng upstream | Không independent market n=2448; không gộp Full/Base với Native/Common hoặc suy isolated MT ablation |
| CL024 | [§3.7.4](chapters/03_background.md#374-metrics-denominators-and-dependence): metrics, NA, account/NAV và frequency | HOP_DONG_TRIEN_KHAI | Free pilot/unified analysis/risk helper frozen §8.6, official BA/MCC/CV docs | BA hai class; MCC zero denominator NA; sample/pop SD và LPM2 khác nhau | Không annualize tùy tiện, pooled portfolio, significance/coverage claims hoặc sửa study convention |
| CL025 | [F02](assets/diagrams/F02_temporal_partitions.pdf), §3.7.2 | MINH_HOA | Source TikZ/hash §8.5.6, CL021–CL022 | Schematic split/purge/maturity, không ngày/độ dài fold thật | Đã build/render/xem một trang; không phải cohort schedule T37 hoặc causal acceptance |
| CL026 | [§4.1.1–§4.1.2](chapters/04_proposed_system.md#411-what-the-system-decides): mục đích, loại xử lý, shared parent và thứ tự thật | HOP_DONG_TRIEN_KHAI | BG02/BG14/BG17/BG18 và source §9.1 | Indicator→Pattern→Trend→joint alpha/news; profile/context sau shared parent | Không gọi mỗi role là một hosted call hoặc shared parent là final prompt giống nhau |
| CL027 | [F03](assets/diagrams/F03_system_overview.pdf), §4.1.2 | MINH_HOA | Source TikZ/hash §9.2; CL026 và offline resources đã khóa | Group theo compute type, không phải strict node sequence hoặc latency chart | Build/render/xem; outcome chỉ vào evaluation; chưa phải DAG/thuật toán chi tiết T33 |
| CL028 | [§4.1.3](chapters/04_proposed_system.md#413-opening-the-fpt-example): mở EX01 bằng input và lịch | DO_DUOC | EX01-S, selection/source §7, TIME01–03 | FPT cutoff03/07/2023,u0/r0; 45/600 bars; chưa lộ realized prices/return | Kiểm saved records, không thu lại dữ liệu hoặc chọn lại ca theo thành tích |
| CL029 | [§4.2.1](chapters/04_proposed_system.md#421-preparing-a-query-without-its-outcome): nguồn giá/index/news và windows | HOP_DONG_TRIEN_KHAI | TIME03/TIME04, BG17, EX01-S | Query exact cutoff; 45/600 bars; event barriers không splice donor series | Không gọi vendor/live thay historical input, không chứng nhận adjustment/units chỉ từ field names |
| CL030 | [B02, §4.2.2](chapters/04_proposed_system.md#422-component-inputoutput-contracts): interface/type/cutoff/output/consumer/failure | HOP_DONG_TRIEN_KHAI | Các source TIME/BG/SYS được dẫn ở §9.3 | 10 interfaces; bảng tóm tắt, schema đầy đủ phụ lục sau | Nội dung bảng đã viết; CSV/TeX dự kiến chưa xuất, không giả artifact đã có |
| CL031 | [§4.2.3](chapters/04_proposed_system.md#423-working-state-versus-a-sealed-shared-snapshot): immutable bytes/copy/whitelist/query-target barrier | HOP_DONG_TRIEN_KHAI | SYS04 SharedSnapshot, SYS05 causal bridge, BG18 | Producer600 rows khác constructor≤600; prior labels cấp qua interface riêng | Validation/hash chỉ integrity; không chứng nhận semantics/causal hoặc final prompts đồng nhất |
| CL032 | [§4.2.4](chapters/04_proposed_system.md#424-identity-and-explicit-absence-in-ex01): semantic shared hash và unavailable | DO_DUOC | EX01-S, tám forecast u0/r0 §7.2 | Shared hash e6c16…103 khác raw member/source/projection/membership | Kiểm nguyên byte/envelope/joins; không có observed neutral news tự tạo |
| CL033 | [§4.3.1](chapters/04_proposed_system.md#431-indicator): priorities, counts/confidence và error-neutral paths | HOP_DONG_TRIEN_KHAI | BG01/BG02 frozen, §9.4 | 5 emitted entries; missing/error khác numeric zero nhưng có thể neutral vote | Không gọi 5 entry là 5 tín hiệu hữu hạn/độc lập hoặc confidence calibrated |
| CL034 | [EX01 Indicator](chapters/04_proposed_system.md#431-indicator): 2 bullish/3 bearish/0 neutral, bearish-medium | DO_DUOC | EX01-S indicator_report | Tóm tắt tiếng Anh của báo cáo Việt nguyên byte | Full report khác fragment LLM thực thấy |
| CL035 | [§4.3.6](chapters/04_proposed_system.md#436-decision): caps, budget, schema và action | HOP_DONG_TRIEN_KHAI | SYS02 frozen helpers/builders/schema | Native900/900/900/1200/600; integrated800/800/800/1100/500; prompt<6500 | Chars khác tokens; schema không xác thực văn xuôi; prior/MT chi tiết T32 |
| CL036 | [EX01 projection](chapters/04_proposed_system.md#436-decision): heading mismatch bỏ count lines | DO_DUOC | EX01-S và Native/Common inputs.prepared.request.messages; SYS02, §9.4 | Raw3661; fragment899/798; prompt3699/4186 characters | Exact substring kiểm trong saved request, không tạo forecast/prompt mới |
| CL037 | [EX01 proposal/action](chapters/04_proposed_system.md#436-decision): Native SHORT/high/RR1.5, Common LONG/high/RR2.5 | DO_DUOC | Raw.reply/policy hai forecast r0 §7.2 | LONG/SHORT khác LONG/CASH; confidence text, RR không phải order | Không nhận “short position” hoặc expected profit trong model prose là hành vi/outcome đã xác thực |
| CL038 | [§4.3.2](chapters/04_proposed_system.md#432-pattern): candlestick rendering, six-field report và local verifier | HOP_DONG_TRIEN_KHAI | Pattern/renderer source §9.1, EX01 render+graph slots | 45 bars; image khác report; text fallback là đường có điều kiện | Không gọi image/format check là pattern validity hoặc future-direction proof |
| CL039 | [EX01 Pattern](chapters/04_proposed_system.md#432-pattern): upward/low và warning; final5 có4 C<O | DO_DUOC | Saved Pattern processed report, shared 45-bar prefix, §9.5 | Dịch tiếng Anh có nhãn; levels47.5/46.5 là report prose | Không suy warning bác bỏ mọi trend dài hạn, không kích hoạt stop-order trong engine |
| CL040 | [§4.3.3](chapters/04_proposed_system.md#433-trend): renderer Close-lines và verifier mean/slope | HOP_DONG_TRIEN_KHAI | Trend/static_util/BG01 frozen, §9.1 | Blue/red Close fits khác high/low fits và model-stated horizontal levels | Verifier không xác thực mọi level/width/prose; high confidence không phải calibrated probability |
| CL041 | [EX01 geometry](chapters/04_proposed_system.md#433-trend): report says widening nhưng Close gap giảm | DAN_XUAT | Frozen fit_trendlines_single/check_trend_line/optimize_slope, Close45 saved; §9.5 | Gap1.8857842646→1.4561850893; slopes .1128526497/.1030890321 | Helper số trích AST, không render lại ảnh, gọi VLM hoặc thay report/metric nghiên cứu |
| CL042 | [F04](assets/diagrams/F04_chart_pair.pdf), source và annotations | DO_DUOC | Hai bitmap EX01-IP/IT nguyên byte; layout hash §9.5 | A1–B2 chú thích mới bên ngoài ảnh; PDF180×250mm một trang | Raw images khác annotation/derived check; không relabel CMG hoặc sinh ảnh AI |
| CL043 | [§4.3.4](chapters/04_proposed_system.md#434-alpha): registry, WQ18 thực thi, Native normalization/IC/ranking/report | HOP_DONG_TRIEN_KHAI | SYS03/SYS10/SYS11 frozen; §9.6; nguồn Alpha101 đọc tại §8.5.2 | 85=5 system-specific+80 adapted; weights mặc định .40/.35/.25; symmetric diagnostic khác CASH | Không đồng nhất template với executable formula, typical-price proxy với VWAP thật, adapted với original hoặc score với probability |
| CL044 | [EX01 Native Alpha](chapters/04_proposed_system.md#434-alpha): năm dòng/value/signal/IC/accuracy/composite và consensus | DO_DUOC | EX01-S alpha_factors/alpha_report; §9.6 | Values4 decimals; metrics là in-sample; 1 bullish/3 bearish/1 neutral | Chép saved fields, không chạy selection lại hoặc suy từ diagnostic tới future profit |
| CL045 | [Native limitations](chapters/04_proposed_system.md#434-alpha): full-window/backfill/global volume/length windows và same-sample selection | HOP_DONG_TRIEN_KHAI | SYS11/SYS12; §9.6 và audit W12 đã khóa | Native row-wise FAIL khác outer-cutoff PASS và PASS_DETECTION | Chỉ đọc source/audit cũ, không chạy lại suite/counterexample hoặc nâng thành Zero-Leakage |
| CL046 | [Common Alpha](chapters/04_proposed_system.md#434-alpha): namespace/operator changes, train orientation/validation ranking/freeze | HOP_DONG_TRIEN_KHAI | BG03; artifact EX01-AS, §9.6 | 300-bar volume mask; normalizer20; support60/30/5; threshold .05/.10/.20; strict split exits | Loader verification có tái lập fit trong implementation; đợt viết này không fit, Alpha scope không chứng nhận toàn hệ |
| CL047 | [EX01 Common Alpha](chapters/04_proposed_system.md#434-alpha): IDs/signs/values/threshold/lịch | DO_DUOC | EX01-AS/AP trong U06 assets v2, projection khớp U08 EX01-S | Threshold.05; origin2020-01-02; fit_end2023-06-30; train/validation theo artifact | Số bản thảo làm tròn6 decimals, raw vẫn giữ; không coi U06 preparation là hosted response hoặc so sánh chỉ đổi prior |
| CL048 | [§4.3.5](chapters/04_proposed_system.md#435-sentiment): live scorer/fallback và component frozen cache | HOP_DONG_TRIEN_KHAI | SYS13/SYS15/SYS16; §9.7 | Arithmetic mean, strict±.10; historical dated90 days/min3; scorer/backend/fallback riêng | Không lấy code model ID làm chứng cứ backend thực dùng hoặc fallback neutral làm market evidence |
| CL049 | [FrozenNews](chapters/04_proposed_system.md#435-sentiment): availability, decay, missingness | HOP_DONG_TRIEN_KHAI | SYS14, FrozenNews.get_sentiment_at; §9.7 | available≥publication-day+1, 90days theo available; exp(-ln2×age/30), min3 | Scorer tag/verified count là contract, không chứng nhận tin đúng/đủ hoặc thời điểm gốc; không gán±.10 của live vào provider này |
| CL050 | [EX01 news/normalizer](chapters/04_proposed_system.md#435-sentiment): unavailable và reliability khác neutral | DO_DUOC | EX01-S, SYS03; §9.7 | Count0, score null, min3 vs reliable8; delta_1d_proxy=z/2 | Không gọi proxy là biến động1ngày thực hoặc tin thành input dynamic factor chỉ từ tên SFA |
| CL051 | [§4.4.1](chapters/04_proposed_system.md#441-native-and-common-in-the-context-study): Native/Common bridge và request | HOP_DONG_TRIEN_KHAI | SYS01/02/05/17/18, BG18; §9.8 | Common thay top-level alpha_report/alpha_factors; preserved raw parent; instruction/caps đổi; empty prefix | Không nhận whole nested payload identical, Native=Base hoặc Common không có Alpha |
| CL052 | [EX01 profile trace](chapters/04_proposed_system.md#443-what-the-bridge-can-establish): envelope bằng nhau, messages khác | DO_DUOC | Hai forecast EX01 Native/Common, §7.2, §9.8 | Tất cả non-message request fields bằng nhau; prompt3699/4186; SHORT/CASH và LONG | Không kết luận riêng thay đổi nào gây response khác, không đọc outcome vào input |
| CL053 | [§4.4.2/B03](chapters/04_proposed_system.md#442-full-and-base-in-the-component-study): Full/Base và hai switch | HOP_DONG_TRIEN_KHAI | SYS01 ABLATION_CONFIGS/compile, TIME01 paired path; §9.8 | Full(true,true), Base(false,false); upstream một lần/deepcopy | Joint bundle khác alpha-only; cấu hình tồn tại không chứng minh panel đã chạy |
| CL054 | [§4.4.3](chapters/04_proposed_system.md#443-what-the-bridge-can-establish): giới hạn can thiệp | DAN_XUAT | Delta field/builder từ CL051–CL053 và identity hai nghiên cứu §3 | B03 foundation portion viết inline Markdown; variant rows tiếp ở các mục sau | Không coi Native/Common là ablation một thành phần hoặc gán lợi ích student riêng |
| CL055 | [§4.5.1](chapters/04_proposed_system.md#451-a-completed-signal-episode): fields/schema/oracle và bull trap | HOP_DONG_TRIEN_KHAI | SYS19, TIME01, EP04 schema; §9.9 | Net_pct=100×oracle; strict>0; T/P bullish và net≤0; exact fields/types/calendar | LOSS_IF_LONG khác CASH loss; không gán label theo báo cáo hoặc hướng Close-to-Close |
| CL056 | [EX01 record/timeline](chapters/04_proposed_system.md#452-temporal-eligibility-and-frozen-membership): 3 record đã lưu và boundary | DO_DUOC | EP01 original bank và U08 v1 trace; §9.9 | Exact JSON FPT:2022-04-07; 3 exit năm2022 < query2023-07-03 | Hai boundary rows có nhãn Illustrative; không giả ID hoặc đọc giá query tương lai |
| CL057 | [Bank provenance](chapters/04_proposed_system.md#452-temporal-eligibility-and-frozen-membership): 852 CORE4 và transfer | DO_DUOC | EP01–EP03, SYS21, BG16; §9.9 | FPT211/MWG213/VCB215/VNM213; max_exit2022-12-30 | Bank raw khác donor query; QA cũ không phải chứng nhận raw signal journal mới; không relabel |
| CL058 | [§4.5.2–4.5.3](chapters/04_proposed_system.md#453-signal-memory-versus-numerical-context-in-ex01): freeze/reserved và hai loại context | HOP_DONG_TRIEN_KHAI | BG16/BG17/BG23, EX01-C/S/hosted v1; §7.4/§9.9 | Signal211→19→3; numeric3tasks/11prior+3target=14rows; reserved102 | Không đồng nhất 3examples với 3tasks, không coi maturity theo từngquery là fold-frozen protocol |
| CL059 | [§4.5.4](chapters/04_proposed_system.md#454-regime-fitting-and-query-time-assignment): fit/features/naming | HOP_DONG_TRIEN_KHAI | BG04/SYS22–24/BG23; §9.10 | 5features,4states, seed42/maxiter500/tol.001/mincov.001; train-only mapping/scaler | Generic2018–2022bounds không thay cutoff artifact; category ID khác latent state |
| CL060 | [Quality fallback](chapters/04_proposed_system.md#454-regime-fitting-and-query-time-assignment): MULTI_FACTOR khác UNKNOWN/error | HOP_DONG_TRIEN_KHAI | BG04 calibration/fallback và SYS23 timeline | Occupancy≥5%, separation, vol ratio1.1, gain criterion; <499price rows UNKNOWN | Không coi existence fallback là EX01 đã fallback; missing artifact dừng, không fit ngầm |
| CL061 | [Frozen inference/F05a](chapters/04_proposed_system.md#454-regime-fitting-and-query-time-assignment): model/scaler resources và endpoint | HOP_DONG_TRIEN_KHAI | RG01/RG02, SYS22/SYS23/BG23/SYS24; §9.10 | Historical episode-prefix khác query2022/MT2020; prefix endpoint khác historical smoothing | Không reassign bank hoặc suy state dưới model mới là state PIT cũ |
| CL062 | [EX01 assignments](chapters/04_proposed_system.md#454-regime-fitting-and-query-time-assignment): CONSOLIDATION vs BULL và fit metadata | DO_DUOC | RG01/RG02/EX01-C/hosted v1; §9.10 | 1251/1052rows end2022 vs752/553rows end2020; HMM/no fallback reasons | Không phân loại lại/fit model để làm hai label giống nhau; rawhash khác semantic parameter fingerprint |
| CL063 | [MT scaler identity/F05a](chapters/04_proposed_system.md#454-regime-fitting-and-query-time-assignment): 4-feature context khác HMM scaler | DO_DUOC | EX01-C.context.scaler, §9.10 | fit731, cutoff2020-12-31, maxexit2020-12-29; full-scaler digest và fit-ID hash | Không lấy731 làm training_rows HMM hoặc nhận hình khái niệm là mới chạy thực nghiệm |
| CL064 | [§4.6.1](chapters/04_proposed_system.md#461-filtering-and-ranking-without-outcome-based-selection): E/P, four-signal score và tie-break | HOP_DONG_TRIEN_KHAI | BG07, BG16, SYS20, §9.11 | Same symbol, exit<cutoff, same regime; .25 per T/P/A/I; score↓/exit↓/ID↑, K≤3 | Sentiment alias hợp lệ nhưng không vào score; seed42 không là RNG trong deterministic mode; kiểm integrity outcome khác dùng outcome để rank |
| CL065 | [§4.6.2](chapters/04_proposed_system.md#462-population-statistics-and-the-displayed-examples): population empirical rates | HOP_DONG_TRIEN_KHAI | BG07._compute_statistics và format; §9.11 | LONGwin trên P; trap trên T∨P; TrendFail/PatternFail mẫu số riêng;0/0NA | Tên Bayesian không biến ratio v1 thành Beta posterior/credible interval hoặc calibrated query probability |
| CL066 | [EX01 selected list/counts](chapters/04_proposed_system.md#462-population-statistics-and-the-displayed-examples): 211→19→3 và scores | DO_DUOC | EP01 original bank + U08 EX01 v1 trace; §9.11 | q=+++-; IDsApr7/18/13, scores1/.75/.75; 9/19,9/18,7/14,9/18 | Kiểm arithmetic từ saved fields sau filter, không chạy forecast/retrieval pipeline mới; examples1win không làm n=3 |
| CL067 | [§4.6.3](chapters/04_proposed_system.md#463-the-bounded-prefix): BRPP có chú giải và prompt delta | DO_DUOC | Exact substring U08 request, BG07 format, SYS18; §9.11 | Original prefix369chars, Common4186→v14556=+370 inclnewline; caps600/<6500 | English translation có nhãn, không giả nó là prompt đã chạy hoặc cắt task để vừa cap |
| CL068 | [§4.6.4](chapters/04_proposed_system.md#464-partial-support-bypass-and-traceability): status/fallback/error khác nhau | HOP_DONG_TRIEN_KHAI | BG07 selection, BG16 wrapper, BG18 prepare/resolve | No-bank same-point/repeat Common reuse; raw/request/response null; reason/bypass riêng | Partial/empty status không tự thành wrapperfallback, không gán C2min20 cho v1, technicalerror không thành CASH |
| CL069 | [FB01/F05](chapters/04_proposed_system.md#464-partial-support-bypass-and-traceability): HVN no-bank trace và hình | DO_DUOC | FB01 v1/Common U08 members, §9.11; source TikZ | HVN2023-07-03,u0/r0,dep digestkhớp, inheritedLONG | Không gọi inheritedaction là forecast mới hoặc suy thiếu prior có evidenceLONG; F05 khái niệm có source |
| CL070 | [§4.7.1](chapters/04_proposed_system.md#471-c2-disjoint-shrinkage-and-separate-readiness): P=C∪B, counts và shrinkage | HOP_DONG_TRIEN_KHAI | BG05/BG07; §9.12 | C exactT/P/A/I, B=P\C; metric masks riêng; strength4, background mean(s+1)/(n+2) | Không double-count C trong background; nC=0 không hiện posterior từ prior đơn thuần, CrI plug-in khác query probability |
| CL071 | [C2 examples](chapters/04_proposed_system.md#471-c2-disjoint-shrinkage-and-separate-readiness): signal/price/age/diversity | HOP_DONG_TRIEN_KHAI | SYS26/SYS27; saved EX01 metadata §9.12 | .5S+.5/(1+RMSdist); decay365; age≤730, base≥.625, gap≥5sessions, K≤3 | Selection filters không cắt statisticalP; không dùng return hoặc random bù ví dụ |
| CL072 | [C2 split gate](chapters/04_proposed_system.md#471-c2-disjoint-shrinkage-and-separate-readiness): stats/examples/view readiness | HOP_DONG_TRIEN_KHAI | BG06, SYS25/BG18; §9.12 | nP≥20, metricnC≥5,width≤.75; examples có query/scaler/list riêng; stats=any ready | Không đồng nhất retrieved/visibleK, không biến missingartifact thành evidencefallback |
| CL073 | [EX01 C2 table](chapters/04_proposed_system.md#471-c2-disjoint-shrinkage-and-separate-readiness): 4 metrics/groups/gate/bypass | DO_DUOC | U08 C2 slot §7.2, EP01; §9.12 | P19/C1/B18; counts9/19=1/1+8/18, etc; posterior table round6; retrieved3/visible0 | Bảng audit không phải prompt đã thấy; LOW_POPULATION và LOW_CONDITIONAL dù widths<.75 |
| CL074 | [§4.7.2](chapters/04_proposed_system.md#472-alternative-conditional-and-presentation-profiles): A đổi condition T/P, B đổi renderer | HOP_DONG_TRIEN_KHAI | SYS25/SYS28/BG06; §9.13 | A same-stock/regime P, C matchTP; ranking4signals giữ; B=C2evidence, wording khác | Pool không cross-stock, semantic không embeddings, C2 cũng đã hiện counts/CrI |
| CL075 | [B03 prior portion](chapters/04_proposed_system.md#472-alternative-conditional-and-presentation-profiles): so sánh bốn prior | DAN_XUAT | BG07/05/06, SYS25–28 và CL064–074 | Matching/statistics/examples/prefix/readiness/Commondependency; basefull_prior khác registered contentmodes | Bảng inline nguồn Markdown; chưa xuất CSV/TeX hoặc hoàn tất orchestrationT33 |
| CL076 | [EX01 A table](chapters/04_proposed_system.md#472-alternative-conditional-and-presentation-profiles): counts P19/C14/B5, posterior | DO_DUOC | U08 Atrace.statistics, EP01; §9.13 | win7/14+2/5; trap/pattern7/14+2/4; trend7/14+0/0; meansround6 | nBcycle5 không là denominator metric; 0/0trendbackground dùng fixedsymmetricprior |
| CL077 | [EX01 C2/A/B contrast](chapters/04_proposed_system.md#472-alternative-conditional-and-presentation-profiles): identical C2/B evidence và bypass | DO_DUOC | U08 ba prepared/request/forecast/policy records; §9.13 | C2/Bbasehash0092…e2a; Abasehash2d11…f5a8; same3IDs; prefix[]/rawnull/depCommon | Không nói B wording đã tới model khi bypass hoặc kế thừaLONG là ba forecast mới |
| CL078 | [§4.8.2](chapters/04_proposed_system.md#482-task-construction): observation/vector/oracle | HOP_DONG_TRIEN_KHAI | SYS29/32, BG08; §9.14 | 21bars, momentum5/20, std20logreturns ddof0, MA20distance; y=net>0 | r_net sidecar không thành coordinate, không đồng nhất std với HMMddof1 |
| CL079 | [MT scaling](chapters/04_proposed_system.md#482-task-construction): raw/z/clip và resource | HOP_DONG_TRIEN_KHAI | SYS31/BG23, EX01-Cscaler; §9.10/9.14 | populationvariance, zeroVarScale1, clip±4; frozen2020/fit731 | Không dùng scalerC2stock/fold hoặc HMM, không refit600bars/query |
| CL080 | [Task membership](chapters/04_proposed_system.md#482-task-construction): same-symbol63sessionblocks và bucket | HOP_DONG_TRIEN_KHAI | BG09/BG10, SYS33; §9.14 | i//63; facts45bars MACD−Signal/Close−SMA20 strictsign,zeroUNKNOWN | MACDNEG là quan hệ Signal, không MACDzero; bucket khác regime, query không nhãn |
| CL081 | [Selection/freeze/F06](chapters/04_proposed_system.md#482-task-construction): task/row ranking và proof | HOP_DONG_TRIEN_KHAI | BG09/BG16/BG17/BG23, SYS33; §9.14 | Regimematchpriority, centroidfullpool, distance/latestexit/ID; K≤3, 2–8rows/prior, m≤8latesttarget | Allhistoryexit<cutoff và foldfreeze/reserved; membershiphashfullobjects, không chỉ displayedIDs |
| CL082 | [EX01 context/table/F06](chapters/04_proposed_system.md#482-task-construction): vectors/taskcounts/dates | DO_DUOC | EX01-C.context và hostedMT membership; §9.14 | eligible30, K3 counts5/4/2+m3=14; index1372/block21; round6vectors | Ba signalexamples khác ba numerictasks; không sinh lại context/model hoặc xemqueryfutureprices |
| CL083 | [§4.8.3](chapters/04_proposed_system.md#483-teacher-and-student): resource/teacher fit/conditioning | HOP_DONG_TRIEN_KHAI | BG11, TR01–03; §9.15 | Grid16 mu×kappa; MAPEMDirichlet2; 48tasks/731cycles;237iters; countlikelihood/noqueryx | Posterior conditioning khác refit; teacher không dùng featurevalues hoặc gộp priorcounts vào θtarget |
| CL084 | [Synthetic training](chapters/04_proposed_system.md#483-teacher-and-student): generator/domains/loss target | HOP_DONG_TRIEN_KHAI | SYS34/SYS38/TR02; §9.15 | K0–3,n2–8,m0–8, pool731vectors independentlatents/labels, fixed5000corpora/500stress | Không gọi source labels là syntheticlabels hoặc teacheragreement là marketcalibration |
| CL085 | [Packing/architecture/loss](chapters/04_proposed_system.md#483-teacher-and-student): paired tokens/causal/query-only | HOP_DONG_TRIEN_KHAI | BG12, SYS37/36/40, TR02 | 6→128,2layers/4heads/FF256/GELU/dropout0/preLN;271873params;37max/EX0119tokens | Teacherq detachedsidecar, queryy/latent/rnet không token; 69packing diagnostic không production |
| CL086 | [Recipe table](chapters/04_proposed_system.md#483-teacher-and-student): optimizer/sampling/checkpoint | DO_DUOC | TR01/02, SYS35/40, training/pilotreceipts; §9.15 | seeds17/42/73×5000steps,batch128,640000episodes/seed;AdamW/schedule/clip1 | Recorded physical128 khác OOMoptions128/64/32; không metricearlystop hoặc fit runtime mới |
| CL087 | [Selection](chapters/04_proposed_system.md#483-teacher-and-student): gates/2021rank/seed42step3000 | DO_DUOC | SYS41, TR01/05–08 and60assessmenthashes; §9.15 | Eligibilitysynthetic/swap/control then2021macroLL/Brier,step,seed; selectedtensorc60a… | Read receipts/hash/rankkhớp, không chạy lại evaluation/gates; 2021selection dùng labels dù optimizersynthetic |
| CL088 | [Frozen inference/EX01](chapters/04_proposed_system.md#483-teacher-and-student): adapter/resources/p | DO_DUOC | SYS36/37, BG23; TR01/03/04, U08MTaux.branch; §9.15 | candidate exporta6f0… khác resumable9414…; CPUeval/nograd; psaved.38681803029367656 | Không loadweights/forward hoặc nâng gate/calibration; p khác utility/LLMconfidence/return |
| CL089 | [§4.8.1](chapters/04_proposed_system.md#481-fact-packet-and-fact-anchor): facts numeric/provenance/assertions | HOP_DONG_TRIEN_KHAI | BG10/SYS33, source45barsEX01; §9.16 | MACD12/26/9/SMA20, rawdiff/strictrelations, bucket và prefixhash | Packet/selfhash không tự chứng minh nguồn; warnings không hardfacts hoặc endpointsign là crossing |
| CL090 | [Fact request/reply](chapters/04_proposed_system.md#481-fact-packet-and-fact-anchor): Common reports/factcard/schema | HOP_DONG_TRIEN_KHAI | SYS42/SYS33/BG18; FA01schema, §9.16 | NoMTprojection/p/U; threeuniqueIDs/enums/contextNOTAPPLICABLE; card≤700,total<6500 | Factcard khác BRPP600; schema khác semanticcorrectness; không implicitutilityveto |
| CL091 | [Anchor validity/failure branch](chapters/04_proposed_system.md#481-fact-packet-and-fact-anchor): resolveda0/Commondependency/proof | HOP_DONG_TRIEN_KHAI | BG14/BG18; §9.16 | Exactassertions+NOTAPPLICABLE; invalid→Common, reason/valid/bypass khác nhau | Illustrative schema-validSHORT/NEGATIVE chưa là rawcase; technicalfailureraise, Commonfallback không được cấp fakefacts |
| CL092 | [EX01 fact table/reply](chapters/04_proposed_system.md#481-fact-packet-and-fact-anchor): packet/numbers/prompt/source/prose | DO_DUOC | U08Fact_Anchor/Common r0 §7.2 và §9.16 | MACD.65426756<Signal.7043937 nhưng>0; Close48.18>SMA47.5675; prompt3916; LONG/RR1.5/NO_NUMERIC_VETO | fact_assertions_validtrue không kiểm “bullish momentum”/“positive zero crossing”; q10null, không gọi là veto |

Quy tắc điền bảng:

1. **Đích:** file + anchor/nhãn ổn định, câu nhận định hoặc table/row/column;
   tham chiếu một vùng chung chung không đủ truy vết một con số. Nhiều ô
   cùng nguồn/quy tắc có thể dùng chung dòng nếu kê rõ toàn bộ phạm vi.
2. **Loại:** dùng `NGUON_HOC_THUAT`, `HOP_DONG_TRIEN_KHAI`, `DO_DUOC`,
   `DAN_XUAT` hoặc `MINH_HOA`. Tên loại thể hiện nguồn của nhận định, không
   thay điều kiện đã kiểm; hình/bảng tiếp tục dùng danh mục §6.
3. **Nguồn:** nối ID §2/§3/§6/§7 hoặc khóa đọc §4, kèm đúng phiên bản/hash
   và vị trí: ZIP/member/field, CSV row keys/column hoặc trang/section của
   tài liệu. Nguồn đã có binding trong sổ chỉ cần dẫn binding đó và locator
   chi tiết; không sao chép archive hoặc lấy HEAD live thay snapshot lịch sử.
4. **Đại lượng:** ghi đơn vị, cohort, mẫu số, repeat, thứ tự tổng hợp, công
   thức/đường dẫn phép dẫn xuất và cách làm tròn khi áp dụng. Giữ fraction,
   %, pp và các nghĩa K riêng; giữ NA và lý do thiếu, không điền 0 để lấp ô.
5. **Kiểm và giới hạn:** ghi đã kiểm gì, nguồn/receipt nào, giới hạn diễn
   giải và phần chưa xác minh. Citation ứng viên chưa đọc, nguồn live giải
   thích hoặc cold replay không tự chứng minh một kết luận thực nghiệm hay
   gate toàn hệ. Minh họa phải có nhãn `Illustrative` trong bản thảo.

Mục này là sổ ánh xạ bằng chứng, không phải checklist task thứ hai. Không
đánh dấu một nhận định đã kiểm chỉ vì có link; mỗi mục viết xong phải đối
chiếu nội dung/đơn vị/phạm vi với nguồn và sửa hoặc thu hẹp nếu thiếu support.

### 8.3. Điều kiện còn thiếu và quy ước cập nhật

| Nhóm còn thiếu | Nơi giữ thông tin gốc | Cách xử lý khi viết |
| --- | --- | --- |
| Yêu cầu nộp và biểu mẫu chính thức | §1 | Ghi chưa được cung cấp; chỉ để chờ phần phụ thuộc, không tự đặt hạn hoặc phê duyệt |
| Nguồn học thuật, metadata và phạm vi trích dẫn | §4 | Tiếp tục đọc/kiểm trước khi đưa nhận định hoặc citation vào chương; bibliography hiện có chỉ là ứng viên |
| Giới hạn dữ liệu, nhân quả, hỗ trợ lịch sử và ablation | §3, §7 | Giữ kết quả âm/fallback và nguồn chưa xác minh; thu hẹp nhận định, không tự chạy nghiên cứu để bù |
| Hình, bảng, thuật toán, ca bổ sung và rà soát bản thảo | §6, §7 và bảng ánh xạ §8.2 | Chưa có sản phẩm hoặc nội dung thì giữ placeholder; task phụ trách tạo/kiểm sau, không coi danh mục là sản phẩm |

Tiếp tục bổ sung ghi chú đọc và nguồn sản phẩm vào phần tương ứng; ánh xạ
luận điểm/ô bảng mới vào §8.2. Mỗi vấn đề mới ghi nguồn, ảnh hưởng tới
luận điểm/chương nào và cách giới hạn nhận định trong khi chưa giải quyết.
Không tự sửa bằng chứng đã đóng băng. Markdown là nguồn nội dung chính
trong giai đoạn viết; việc chuyển nguồn bản nộp sang LaTeX thuộc bước sau.
Trạng thái công việc nằm duy nhất tại
[checklist trong kế hoạch](plan.md#21-một-nguồn-trạng-thái-công-việc);
lịch sử kiểm tra gộp lưu tại README tuần.

### 8.4. Binding cho quan sát và chỉ số thời gian

Đối soát ngày **15/11/2026**, từ develop
`12508f18fc6348fdde53aff264e8e98547f4e316`. TIME01–TIME05 dưới đây khớp
byte với member cùng đường dẫn trong `final_evidence_snapshot.zip`, hash gói
ở §3; đã kiểm `snapshot_manifest.json.source_members` cho cả năm file.
Vì vậy link mã hiện tại ở bảng chỉ là đường đọc thuận tiện; binding tham
chiếu vẫn là source frozen, không đổi phiên bản nghiên cứu.

| Source ID | Đường đọc / member snapshot | SHA256 nguyên byte |
| --- | --- | --- |
| TIME01 | [core/backtest_engine.py](../core/backtest_engine.py) | `6c8f87c9ac7e15fbf67493ccfce06487c22b3a56145a5583f7fa8305d852026b` |
| TIME02 | [utils/target_contract.py](../utils/target_contract.py) | `1b2af4f8c3a031d44334281a63e812a1b1ee6cb52216b02602601c489d10ffb7` |
| TIME03 | [core/historical_evaluation_data.py](../core/historical_evaluation_data.py) | `96cab48918cd53b7408943157759a97477c367e3a4a07b4c98e46ecb7b039857` |
| TIME04 | [core/historical_asset_readiness.py](../core/historical_asset_readiness.py) | `914d9cfa94696f0dec572fac0af0d6ab4ddc1e0160edcd705434b8a27d9579f1` |
| TIME05 | [core/historical_signals.py](../core/historical_signals.py) | `26a35fa6e5421db09f5cbed5f219346e9aa72667b2a759568f0884cdcecdc7c5` |
| TIME06 | EX01-S/EX01-O, slot U08 và raw hash tại §7.2; input `provenance.source_sha256` = outcome `source_sha256` | `1bba0057bf6b4a847b43236bef745a311ef633692202a59138e065d0a9ddca27` (source identity đã ghi, không phải raw slot hash) |

EX01-S giữ 600 ngày từ 02/02/2021 tới 03/07/2023, 45 ngày cuối bắt đầu
27/04/2023. EX01-O có decision_bar_index=872, target_horizon_bars=3, dates
03/07, 04/07, 05/07, 06/07/2023. Đã kiểm raw hash/manifest và envelope hai
slot, cùng point_id/source identity; chỉ đọc trường thời gian/index, không
chạy lại labels/metrics. Chỉ số 828/873/874/875 là dẫn xuất từ index đã lưu,
không đổi chỉ số khi slice 45/600 hàng được reset cục bộ.

**Sản phẩm F01:** nhãn/caption tiếng Anh, nguồn minh họa contract, dates/index
được truy về EX01. Nguồn TikZ standalone giữ được để sửa và chuyển vào LaTeX
sau; PNG chỉ phục vụ xem trong Markdown, PDF là hình vector để dàn trang.

| File đã tạo | SHA256 nguyên byte |
| --- | --- |
| [F01_trade_timeline.tex](assets/diagrams/F01_trade_timeline.tex) | `5d716830ca1c81ecb9a569306ea0260976d3dd8499088b5cfaaa6f33c3ccc9b2` |
| [F01_trade_timeline.pdf](assets/diagrams/F01_trade_timeline.pdf) | `b4fa90e3c743863cf33031e67410133e5e08b9194e2ee1cceb398885b2a414bb` |
| [F01_trade_timeline.png](assets/diagrams/F01_trade_timeline.png) | `b777264fe6dc820de343b6db7e24eee2c3aba047f8bca729fc0c0184cfb780d9` |

Từ root repo, tạo thư mục tạm `tmp/pdfs/thesis-t09`, chạy
`pdflatex --disable-installer --interaction=nonstopmode --halt-on-error --output-directory=tmp/pdfs/thesis-t09 thesis/assets/diagrams/F01_trade_timeline.tex`,
rồi `pdftoppm -scale-to 1800 -singlefile -png tmp/pdfs/thesis-t09/F01_trade_timeline.pdf tmp/pdfs/thesis-t09/F01_preview`.
Chỉ chép PDF/PNG đã kiểm sang `assets/diagrams/`. Toolchain: pdfTeX
3.141592653-2.6-1.40.28, MiKTeX 25.12; một trang 170×112 mm. Đã xem toàn
trang render, không cắt/chồng chữ; log không overfull/underfull hoặc undefined
reference. MiKTeX vẫn nhắc kiểm cập nhật nhưng build exit 0. Metadata PDF có
thể khác giữa các lần build; hash trên khóa sản phẩm đã kiểm, không cam kết
PDF luôn byte-identical. Tại mốc T09, T10 còn viết công thức phí/net label và ví dụ kinh
tế; F01 không thay nội dung đó hoặc việc kiểm toàn văn ở các task dàn trang.

### 8.5. Nguồn và phép tính cho các phần nền tảng tiếp theo

#### 8.5.1. Kinh tế và nhãn

T10, ngày 15/11/2026: TIME01/TIME02 giữ hash §8.4 và byte snapshot; chỉ
trích AST hai hàm `_validate_account_costs` và `compute_round_trip_net_return`
để kiểm số minh họa, không import graph hoặc tạo lại label thực nghiệm.
Entry=100, exit=100 cho r_net=−0.006975568072824623; exit=103 cho
r_net=0.02281516488499058; tỷ lệ tăng giá break-even=0.007024568428076972.
Giá vốn mua=100.35025, thu bán ở exit=103 là 102.6397575. Có cả phí/slippage
hai chiều; nhãn zero đối chiếu trực tiếp điều kiện `net > 0` ở TIME02.
Các số là minh họa độc lập với EX01. F01 không build lại chỉ vì viết công
thức; PDF/PNG giữ nguyên byte. Git checkout Windows chuyển source TikZ sang
CRLF: binding source §8.4 đối chiếu blob Git/LF, không nhầm newline đổi với
đổi hình. Không ghi source working-tree CRLF có cùng raw hash với blob LF.

#### 8.5.2. Tín hiệu giá, alpha và tin

T11, ngày 15/11/2026: đọc toolkit và Indicator, đối chiếu kwargs với công
thức năm họ chỉ báo; đọc normalization/IC/orientation/selection của Common
và `FrozenNews` (TIME03). Binding source bổ sung ở §8.6; không import graph
hoặc sinh lại indicator/alpha/sentiment của nghiên cứu. Kiểm tài liệu TA-Lib
RSI/WILLR theo phạm vi định nghĩa và official source MACD/RSI/STOCH/WILLR/ROC
đã link ở footnote chương, không coi phiên bản upstream hiện tại là runtime
đã khóa. Hai entry TA-Lib ở §4 cập nhật DA_KIEM theo phạm vi; không tuyên bố
đã đọc sách Wilder/Appel/Lane. Alpha101 v3 kiểm lại trang tác giả/metadata,
giữ ghi chú đọc cũ về cross-sectional adaptation, không nhập kết quả paper
gốc thành kết quả hệ thống. Thống kê số nguồn đã đọc tại T04 là lịch sử mốc
T04, không phải tổng trạng thái đọc sau các task này. Bibliography cuối vẫn
thuộc T48; các link primary mới ở footnote có ngày truy cập/phạm vi.

#### 8.5.3. Regime và HMM

T12, 15/11/2026: Rabiner §III.A–B (forward/backward và marginal), Hamilton
phần đầu về state/transition và hmmlearn tutorial về EM/fitting được đọc
theo phạm vi, không tuyên bố đọc toàn bộ hai paper. `classify_regime` đọc
`predict_proba(...)[-1]`, không gọi Viterbi. Source frozen xác nhận features,
mapping/fallback và check training-prefix hash; nguồn EX01 §7 giữ cutoff
2020-12-31 riêng với khoảng train cho phép trong module. Không fit, không
chạy HMM inference hoặc đổi nhãn regime trong record nghiên cứu.

#### 8.5.4. Counts, shrinkage và khoảng

T13, 15/11/2026: đối chiếu `conditional_metric` và split gate; kiểm ví dụ
Beta(9,5) và Beta(5.4,2.6) bằng SciPy `beta.ppf`, đối chiếu counts/mean bằng
hàm thuần trích AST (không import retriever/graph). Tất cả counts ví dụ là
Illustrative, không phân tích lại study. Đọc Stan author case study về Beta
conjugacy và SciPy official về density/quantile. Web không mở được BDA3.pdf
do vượt giới hạn dung lượng; **không** đánh dấu Gelman đã đọc hoặc viện dẫn
nội dung sách chưa truy cập. Giữ ứng viên đó CHUA_DOC, dùng nguồn primary
đã truy cập và phép nhân density trình bày rõ trong chương. Chưa cần chốt
khóa citation mới vào bibliography cuối của T48.

#### 8.5.5. Context đa tác vụ, teacher/student và utility

T14, 15/11/2026: đọc Zhu2026v1 §4 và PFN abstract theo phạm vi khái niệm,
không tái dùng kiến trúc/kết quả paper làm triển khai đã đo. Kiểm frozen
bank/tasks/features/teacher/student/utility/policy, phân biệt 63 reference
calendar observations với 63 ngày lịch; target query không nhãn. Teacher
count-only khác student feature input; utility lấy theta teacher, không
student. Ví dụ .8×.01−.2×.06=−.004 và dấu hai hướng policy đã đối chiếu.
Rubin DOI/ProjectEuclid không mở được nội dung đầy đủ, giữ CHUA_DOC;
không dùng trang Stan bagging làm bằng chứng đã đọc Rubin hoặc coi bagging
posterior là phép weighting trong code. Chương ghi trực tiếp normalized
exponential-weight construction; nguồn gốc học thuật còn kiểm tại T48.
Không torch load/forward, teacher inference, fit, utility sampling hoặc
thêm ablation để bù nội dung.

#### 8.5.6. Tính hợp lệ thời gian và đánh giá

T15, 15/11/2026: đọc source purge/label admission/reserved-ID providers,
paired deep-copy và metrics/ratios; kiểm nguồn frozen qua §8.6. Tách xếp
thời gian feature/fit/query/history, exit strict trước boundary hoặc query,
labels reserved không tái dùng. Diễn giải BA/MCC/CV dựa thêm official sklearn
docs đã đọc đúng mục, không lấy sklearn behavior thay NA policy trong source
study. Không chạy lại classification/accounts/bootstrap. F02 là layout
Illustrative, không tự tạo các ngày chia tập hoặc gọi exposed folds là
untouched holdout. Numerical-context pool frozen trước query đầu fold,
không tự nhập nhãn mới trong fold; query feature vẫn tới cutoff tương ứng.
Ngày/độ dài/cohort thực tế vẫn viết ở T37/Chương 5.

| File F02 | SHA256 byte sản phẩm đã kiểm (source theo blob LF) |
| --- | --- |
| [F02_temporal_partitions.tex](assets/diagrams/F02_temporal_partitions.tex) | `f2dbfdaa2a4a48438b90d8126237b6756913a61638be8307bd1526ed89a1f575` |
| [F02_temporal_partitions.pdf](assets/diagrams/F02_temporal_partitions.pdf) | `0531acba3e263efe0af0cd244315a617bf4bf1dc0326310253f138190713b2e6` |
| [F02_temporal_partitions.png](assets/diagrams/F02_temporal_partitions.png) | `82b8142baebf840e059cc3666847bef5dd3c7389aec6dd9d57d921127be8d029` |

Build tương tự F01, đổi basename thành `F02_temporal_partitions` và thư mục
tạm thành `tmp/pdfs/thesis-t15`. pdfLaTeX một lượt exit0, một trang 170×118 mm,
Poppler render1.800px đã xem toàn trang, không cắt/chồng chữ/Type3 hoặc lỗi
overfull/underfull/undefined. MiKTeX còn nhắc cập nhật; không phải lỗi build.
PNG để xem Markdown, PDF vector để dàn trang, source TikZ để chỉnh sửa; không
build toàn văn. Metadata PDF có thể khác khi rebuild như ghi chú F01.

### 8.6. Binding source nền tảng bổ sung

Nguồn dưới được đọc từ `final_evidence_snapshot.zip` đúng byte/manifest,
hash gói giữ ở §3. Cột hash là **member frozen**, không phải fingerprint
library hoặc hash của mã upstream trên web. Mã live chỉ dùng kiểm thuận
tiện; các khác biệt UI được xác nhận ở §3 không thay nguồn nghiên cứu.

| Source ID | Member snapshot | SHA256 frozen | Phạm vi đối chiếu live |
| --- | --- | --- | --- |
| BG01 | `utils/graph_util.py` | `5a8ea82f3112932d8df7677223a433d331e5a0212c42154e3b4c648a4cb24b6a` | Live đồng nhất byte |
| BG02 | `agents/indicator_agent.py` | `470fa5d1f4350180a23bfe40564cd6c02e00b8939cd2d90cad775776f74ee57b` | Live khác presentation; dùng member frozen, không suy hash live đồng nhất |
| BG03 | `core/causal_alpha.py` | `6f52a344047c0e96139e389807161b7dcccfbb70e6bde13db99e9910dc4e47e6` | Live đồng nhất byte |
| BG04 | `core/regime_detector.py` | `fba35472efafe4d5133db50d8ca24d4c57b5682960de2b8a2320a18bddf3be8b` | Live đồng nhất byte |
| BG05 | `core/prior_conditional_statistics.py` | `7d5fbde8a9639d94026aa1b855e81db40f61d7ce3fb961284dfa21043cc9e534` | Live đồng nhất byte |
| BG06 | `core/prior_quality_gate.py` | `00814586220357ba447ced38f91a8551edd2d0558a516fdaaed91929e48efdd5` | Live đồng nhất byte |
| BG07 | `core/bayesian_retriever.py` | `0c71c4508e89355acb3430faee6c95ceea53e2657d3d696bce17b9ce519b8d98` | Live đồng nhất byte |
| BG08 | `core/mt_bicl_bank.py` | `e537efa9f2049e4de217ee13a0aa28bb6ab100953438de0cb24aae3f26dcdb47` | Live đồng nhất byte |
| BG09 | `core/mt_bicl_tasks.py` | `0e8fdd0ce442ceb567f2650780dc812b9c3686d527be139957733bbeb41f72f1` | Live đồng nhất byte |
| BG10 | `core/mt_bicl_features.py` | `8c3fb1d4d4557bd976af13c79fd12e5025d83432eceb194c172a4c282ea8331e` | Live đồng nhất byte |
| BG11 | `core/mt_bicl_teacher.py` | `423dc73be34113634b473ca391c293c1520b046be2e157a9ad8b2ba22734d151` | Live đồng nhất byte |
| BG12 | `core/mt_bicl_replica_student.py` | `0a7a18066f8874ff1d21417f6e46c3b93782e0c6f4836b6f48a942c8d0616ecb` | Live đồng nhất byte |
| BG13 | `core/mt_bicl_utility.py` | `7678ff30ad5cb8f563628f41e3ba7f42415c035df02d0cab1833da6ccdef87b2` | Live đồng nhất byte |
| BG14 | `core/mt_bicl_policy.py` | `301525c36c150e21f09a1971101d53d5927cf38c1d2921017c477441e097b488` | Live đồng nhất byte |
| BG15 | `core/historical_evaluation_protocol.py` | `9b8233f60554201cf861dc39f7326720f907ef9930fea01ebefa235073df2345` | Live đồng nhất byte |
| BG16 | `core/unified_asset_providers.py` | `dfd88f386e458fa1716095bf2964cc603952086c5abd2bada6a167f36ca70147` | Live đồng nhất byte |
| BG17 | `core/unified_execution_providers.py` | `987563e6a5855a56b817de995682326f5d8d1e39c688176a9a5fb59849997a23` | Live đồng nhất byte |
| BG18 | `core/unified_methods.py` | `db8f320dc64d590fc5348e9faec967e2acd2a097547e3d8478bb685dd8061c87` | Live đồng nhất byte |
| BG19 | `core/free_pilot_statistics.py` | `097cf88e3068126c1f668da3022109649aeaff4f8e22a2a319639a9fa9bcd7fb` | Live đồng nhất byte |
| BG20 | `core/unified_analysis/analysis.py` | `e805460aa47b8d36f563d936b0e52322968f65485537c16fdd94525955179a85` | Live đồng nhất byte |
| BG21 | `core/unified_analysis/statistics.py` | `4446fa0a77fce1a74a38d94918ae64c1c379c9a6a997b60a8d5df40dfff85b12` | Live đồng nhất byte |
| BG22 | `utils/account_risk.py` | `487a50fe28397130a93a92c3f2cd79b5184e5cc1a546b9b21ea7ab7a976cd829` | Live đồng nhất byte |
| BG23 | `core/historical_evaluation_context.py` | `9c9e0e8bce652582ead55a71c1f7faaac534b79aaef02830d99cd541b372ec91` | Live đồng nhất byte |

## 9. Nguồn giải thích hệ thống đề xuất

### 9.1. Binding source bổ sung

Dùng cùng snapshot/source commit tại §3. Các hash dưới là member frozen
đã kiểm với `snapshot_manifest.json`; không lấy UI/live thay nguồn lịch sử.
BG/TIME đã có thì viện dẫn lại. Ba module graph/Indicator/Decision có lớp UI
giữ logic nghiên cứu theo xác nhận người dùng; hash vẫn phân biệt đúng byte.

| Source ID | Member snapshot | SHA256 frozen | Đối chiếu live |
| --- | --- | --- | --- |
| SYS01 | `utils/graph_setup.py` | `61bc18bad7bf83a96ee2a862589fba20d5e5b398124132a8fb815d0771c13acf` | Live có presentation khác; dùng frozen theo phạm vi §3 |
| SYS02 | `agents/decision_agent.py` | `a7ed07e310652cfc0de1b1d15ec2bad1a03eeebd6be6a4144b5146c52df118a9` | Live có presentation khác; dùng frozen theo phạm vi §3 |
| SYS03 | `agents/alpha_agent.py` | `04ee4e42dbe30f8b12dd21181c031888f779eae093597f90facec2f66b863158` | Live đồng nhất byte |
| SYS04 | `core/unified_contracts.py` | `ae1051f1ae0b86f7a4abfb5ed331870d0841d6815df6e67247974f2d100647c1` | Live đồng nhất byte |
| SYS05 | `core/causal_bridge.py` | `0ca009cc8b5d361535a0efc4635977c18b8213307c92be9145c649c7f5fc70ef` | Live đồng nhất byte |
| SYS06 | `agents/agent_state.py` | `0dc8621ab971df9438a5601385f616d2eee495382e12d6a4aca2bb0a54eeff76` | Live đồng nhất byte |
| SYS07 | `agents/pattern_agent.py` | `0b343ad7cd1d8c1e7c3781d22c8b843430c5ce35226088f336fad0cc1b2e7d49` | Live đồng nhất byte |
| SYS08 | `agents/trend_agent.py` | `5b610eec0e78768e5d4bd31b2f61f14660e67345334852643ea42d6126193803` | Live đồng nhất byte |
| SYS09 | `utils/static_util.py` | `d2ff7865be9e08f831e1a254d3c85ae2141c7f1cf26181bbf4d9e0f2708597ca` | Live đồng nhất byte |
| SYS10 | `utils/alpha_selector.py` | `a8fcf575385805debb2a30b00cb946f8ab2a55bad7c94df4fa369b3f76c12323` | Live đồng nhất byte |
| SYS11 | `core/alpha_compare.py` | `b9b0419d93541f49837ab4cabffad13a6771e5aaea74561f1070fe7c2d1166bd` | Live đồng nhất byte |
| SYS12 | `core/revision_alpha_contract.py` | `deb310e091b4fa60e2d1fa4e343f42b5c96ae1a6c483eab53169f56ea1b92b1e` | Live đồng nhất byte |
| SYS13 | `agents/sentiment_agent.py` | `4470e6a6937a9e49ca0c573ea1da75346e449eca7b3b4f84db841a71cd0cf9fc` | Live đồng nhất byte |
| SYS14 | `core/historical_evaluation_data.py` | `96cab48918cd53b7408943157759a97477c367e3a4a07b4c98e46ecb7b039857` | Live đồng nhất byte |
| SYS15 | `data_manager/sentiment_cache.py` | `d2fee68ca6cc7ee1386eeafca408d939dcd91e2ac2ce20cef453bbb0bc82355d` | Live đồng nhất byte |
| SYS16 | `core/historical_signals.py` | `26a35fa6e5421db09f5cbed5f219346e9aa72667b2a759568f0884cdcecdc7c5` | Live đồng nhất byte |
| SYS17 | `core/decision_profiles.py` | `49f3e313734e4cd2117008e004bb25dc925dfcbc327eba2eb360afadfd9ee93f` | Live đồng nhất byte |
| SYS18 | `core/mt_bicl_prompt.py` | `93519b6951a6d5c4df18a420eaf080af33ee9448422dcda3903b7809840c90c2` | Live đồng nhất byte |
| SYS19 | `core/bayesian_memory.py` | `d78482b4b1e014ee1bfa916cddc911ef9573217a0225738bf3ced7d639d201f9` | Live đồng nhất byte |
| SYS20 | `core/historical_evaluation_prior.py` | `89e67d53acad3634d1309584c4d5e16990f59089fa807c18ec7c7e8b997d912a` | Live đồng nhất byte |
| SYS21 | `core/free_pilot_assets.py` | `4b4f8c748ea851dba55fc281938550b0f6eb3e75ace011ed7d22dcead51837d7` | Live đồng nhất byte |
| SYS22 | `core/historical_evaluation_runner.py` | `e2025fcdb2fe069e68a92e1be72d0dea97039479ba38db38164e90b27f9cb11a` | Live đồng nhất byte |
| SYS23 | `core/mt_bicl_regimes.py` | `6d036cb93c0ca3a965e536145fe2074fc2e27064c21cae0c2d7de637fcada704` | Live đồng nhất byte |
| SYS24 | `core/historical_runner.py` | `778099c2d413b81ec6f2803f15d1a8b5ccd769db2b862067ca92d74b457d0ecf` | Live đồng nhất byte |
| SYS25 | `core/improvement_prior.py` | `a6ddb54f2a54c14cdd09c05e4191c3e694df7cf28a76f2e3e8006d18bc6110a7` | Live đồng nhất byte |
| SYS26 | `core/prior_example_selection.py` | `ca59b7df58f25c470d3949b2ef297640790b15df7465bf3244ebb3dedb277eae` | Live đồng nhất byte |
| SYS27 | `core/prior_price_similarity.py` | `0c008b756d60473f03a597fd8e7b91fdd8fb3c107ce8c85672d938bfe2b9e347` | Live đồng nhất byte |
| SYS28 | `core/prior_prompt.py` | `6866493d426ebfe138b9cf5c43a0c16a14e188849dfd01c0d337adb7a93e2bdd` | Live đồng nhất byte |
| SYS29 | `core/pit_price_features.py` | `35e5042a49aa2d1c3854150925389c6c3a79260eecaa99851ae6bea2a43794dc` | Live đồng nhất byte |
| SYS30 | `core/price_feature_index.py` | `2809fc1c6e5ba1253feacfc715a839368aeaf1de5b24a7c968ef639818ff8d4b` | Live đồng nhất byte |
| SYS31 | `core/mt_bicl_scaler.py` | `f960bd8efae36c641cff2cca9e444877f1b44debddeee985cb84d12de615d27e` | Live đồng nhất byte |
| SYS32 | `core/mt_bicl_stream.py` | `d87b67432ea415ef60fb12eb96c8658565ee672de801273512d0ddc53454cd4b` | Live đồng nhất byte |
| SYS33 | `core/mt_bicl_contracts.py` | `cb155d306aacb5ec3172fd9d54da2ee344b47ddb1ceafcc2fd50410f2e6eb432` | Live đồng nhất byte |
| SYS34 | `core/mt_bicl_replica_sampling.py` | `fd5a314ef3cf72e837030d824193450ec5344544d4507f4a8bc25c45b127f5bf` | Live đồng nhất byte |
| SYS35 | `core/mt_bicl_replica_training.py` | `f806849b71669a8e2c4be9b686ddd7b5293a7823d36993dac167d9ecd0044449` | Live đồng nhất byte |
| SYS36 | `core/mt_bicl_adapter.py` | `7b4b217771b9e6445ae1be17d15ca2c50403e197a95e58c61d1f679c669aa98b` | Live đồng nhất byte |
| SYS37 | `core/mt_bicl_student.py` | `fa2a7c783177f8c19fcebecaa320ac92d71c219fccbedb37a641ed658e56a885` | Live đồng nhất byte |
| SYS38 | `core/mt_bicl_inputs.py` | `5a273a32bab9d15e6404c200c8a7d89206d6ebbe9dab4df5eece7e5be7dc7b61` | Live đồng nhất byte |
| SYS39 | `core/mt_bicl_oracle.py` | `01b4202a996765399add9056405266d9805f69daa89a3a29e8d3d45d2d725579` | Live đồng nhất byte |
| SYS40 | `core/mt_bicl_replica_learner.py` | `4fcc849d3c606eb3495de1dff218a0ca83b888ef5ee11fd3b3e1a03c9f5201d0` | Live đồng nhất byte |
| SYS41 | `core/mt_bicl_replica_metrics.py` | `7548b420869f04ccde35e6c3734c77605164e80c44b710c332d36bf94ff65010` | Live đồng nhất byte |
| SYS42 | `core/mt_bicl_decision.py` | `2c02c0c9886a4f556444003d5fe39a2c0165eb3710318b82d9eb4e43e4d4c435` | Live đồng nhất byte |
<!-- system-source-end -->

### 9.2. Tổng quan, EX01 và F03

T16, ngày 15/11/2026: đối chiếu historical provider chạy Indicator → Pattern
→ Trend → full(alpha/news), rồi đóng parent/bind Common projection. Sơ đồ
group theo loại tính toán, không giả các node đều gọi LLM hoặc mọi nhánh
dùng một final prompt. Source lớp UI chỉ tương đương logic đã được người
dùng xác nhận, không đổi byte binding. Mở EX01 ở input, giữ realized
prices/return cho Chương 5. Chưa viết thay nội dung chi tiết T17–T35.

| Sản phẩm F03 | SHA256 (source theo blob LF, PDF/PNG nguyên byte) |
| --- | --- |
| [F03_system_overview.tex](assets/diagrams/F03_system_overview.tex) | `130a57abca720735af1148df87213f107a6c4f52445e22379c4deca5efb48b34` |
| [F03_system_overview.pdf](assets/diagrams/F03_system_overview.pdf) | `6ffb441b584445bf06494558844d8512428d7a6abe88847669ef05571479e11e` |
| [F03_system_overview.png](assets/diagrams/F03_system_overview.png) | `abf0f57e4845899d82fe8a34e51eca2eb556a5fdd958a2296a95a9f9c9274293` |

Build như F01/F02, basename `F03_system_overview`, thư mục tạm
`tmp/pdfs/thesis-t16`. pdfLaTeX/Poppler hiện có; PDF một trang 180×150 mm,
render1.900px và xem toàn trang sau sửa wrap/type labels; không cắt/chồng
chữ/Type3/overfull/underfull/undefined. Không build PDF toàn văn. Source
TikZ có thể sửa, PNG để xem Markdown, PDF vector cho dàn trang sau.

### 9.3. Hợp đồng input và shared snapshot

T17: đối chiếu `HistoricalData`, `price_view`, `SharedSnapshot.create/document`,
`forecast_only/json_bytes`, `snapshot_from_graph` và `decision_payload`.
B02 tại §4.2.2 gồm 10 interface có type/cutoff/output/consumer/failure;
chưa tạo CSV/TeX của đường xuất dự kiến. EX01 shared output hash khớp tám
forecast r0; price/source/raw/projection/membership hash được giữ đúng vai.
Source frozen đã bind ở TIME/BG/SYS, không thay bằng annotation TypedDict
legacy khi runtime check có hợp đồng chặt hơn. Không sửa schema/runtime,
không thu dữ liệu, gọi model, chạy suite hoặc build hình nguyên vẹn.

### 9.4. Indicator và Decision cơ sở

T18: đọc priorities `_classify_signals`, clean/round4, error-neutral và
consensus/confidence; bản report EX01 có2/5 tăng,3/5 giảm,0/5 trung tính,
bearish/medium. Kiểm schema base và helper distillation/caps của SYS02.
Trích AST **chỉ** constants và `_distill_report/_cap_report`, áp trên report
đã lưu rồi tìm exact fragment trong request archive; không gọi prompt
builder/node/LLM hoặc replay nghiên cứu. Raw Indicator=3661 chars; heading
không thuộc `_CONVERGENCE_HEADINGS`; Native fragment899, Common798, cả hai
không giữ count lines2/5–3/5. Prompts archived3699/4186 chars. Đây là giới
hạn thật của representation, không âm thầm sửa source hoặc thay prompt.
Native request ID `a405af62-8faa-4d8c-bbcb-cee3f7bddb27`, Common
`e9cd5100-0f68-4677-8ca5-84a08e41386c`; raw reply/policy khớp §7.5. Không
dùng model prose làm chứng cứ short selling/expected realized profit.

### 9.5. Pattern/Trend, ảnh FPT và giới hạn grounding

T19: copy hai PNG giải mã trực tiếp EX01-IP/IT trong U08, không render lại
chart hoặc sửa bitmap. Hai graph slot chứa processed report được định danh
trong manifest U08 (cùng thư mục `outputs/unified_integration/u08_research_r1/slots/`):

| Slot | Tên member JSON | SHA256 nguyên byte |
| --- | --- | --- |
| `graph/FPT-2023-07-03/pattern` | `0fdfe0d1396815148689043d40432c0f9bcaefeab663ec3a0be3e642a3999b51.json` | `f8729661926b913e0b91c2beaa35e1ac10f4a7b843ca67c3294e23563ca9fb66` |
| `graph/FPT-2023-07-03/trend` | `1ba306f11f9f41211c0d8dc9151e3b92415b78f4bf7a56315772fb00c319f654.json` | `150b33c76c076090ca8ce7aacaa0bb9cffce7e738a66088df813ec384146f797` |

Hai processed report được dịch/tóm tắt tiếng Anh có nhãn, không
gọi là raw response trước repair/verification. Pattern giữ warning/low;
Trend giữ high và widening assertion dù geometry Close-fit không khớp.

Helper số `fit_trendlines_single/check_trend_line/optimize_slope` trích AST
từ BG01, input Close45 của EX01-S. Derived support slope/intercept:
0.11285264971385098 / 43.09714735028615; resistance:
0.1030890320923232 / 44.982931614892124. X=0..44 cho khoảng cách đầu
1.8857842646059737, cuối1.456185089258753. Đây là derivation mới dùng giải
thích geometry, **không** metrics/backtest/vision mới; giữ source/input
locator và không sửa report nghiên cứu. Four bearish candles trong last5
kiểm trực tiếp Open/Close ở dates27/06,28/06,29/06,30/06,03/07.

| File F04 | SHA256 (source blob LF, ảnh/PDF nguyên byte) |
| --- | --- |
| [F04_pattern.png](assets/figures/F04_pattern.png) | `d423db489a59706c4aae32e1f9de49cc63f73eded74f8e6f97c018cd1211200f` |
| [F04_trend.png](assets/figures/F04_trend.png) | `93744337e0d375c04973332e4dba86c75d55d79398ed4553ad26a8d8593f3734` |
| [F04_chart_pair.tex](assets/diagrams/F04_chart_pair.tex) | `50cdc69679accd2bcdcc3660fa9361bebc67cabba54880c0e4accd689b19eb4c` |
| [F04_chart_pair.pdf](assets/diagrams/F04_chart_pair.pdf) | `8cef4378a418adffab6a69cb43a75262228b2e282696d4cc70a89eb0318450a9` |
| [F04_chart_pair.png](assets/diagrams/F04_chart_pair.png) | `aea3f8b1a0550eecba5bf12bdd98958d1cb800a2aaa83aa8269ee6aff9e1e2c9` |

Ảnh CMG ở §6.3/paper là nguồn có sẵn tại T06, vẫn giữ identity cũ; sản phẩm
F04 đã chọn FPT/EX01, không relabel ảnh CMG. A1–B2 là annotation ở ngoài
bitmap trên layout LaTeX mới, không nói chúng là đầu vào VLM lúc nghiên cứu.
PDF180×250mm, một trang sau chỉnh kích thước ảnh; source dùng article chuẩn
để tránh dependency extarticle thiếu. Render2.100px cuối đã xem toàn trang,
không cắt/chồng chữ/Type3 hoặc lỗi log. Build từ root như F03, đổi basename
`F04_chart_pair` và thư mục tạm `tmp/pdfs/thesis-t19`; tài nguyên ảnh nằm
trong thesis/assets. Không gọi AI để vẽ lại ảnh nghiên cứu.

### 9.6. Alpha: ứng viên, chấm điểm Native và selector Common đã khóa

T20: §4.3.4, CL043–CL047. Đọc SYS03/SYS10/SYS11/SYS12 và BG03 từ
snapshot, đối chiếu manifest/source byte; không import pipeline, chạy
selector, tính lại factor, kiểm thử counterexample hoặc fit. AST registry
xác nhận85 ID duy nhất:5 CURRENT và80 WQ adaptations. WQ18 thực thi dùng
`-ts_rank(std5 + close-open + corr10,20)`; template report viết rank rút gọn,
WQ29 có ellipsis. Không nhận các chuỗi display là specification chính xác.
Nguồn Alpha101 giữ metadata/phạm vi đọc §8.5.2, không trích công thức gốc
để giả chúng bằng implementation single-stock.

Native: selection tối đa600 bars đã cutoff; daily lookahead3. Hàm
`build_forward_execution_returns` viết trực tiếp phép tính net cùng phí
.0025/slippage.001 hai chiều, khác việc gọi oracle scalar của Common.
Không đổi nhãn prior tasks hoặc economic engine. Normalize full-window
(sample std cho zscore_tanh), nonfinite→0; `delay` bfill, global volume branch,
cửa sổ phụ thuộc length và selection cùng mẫu giữ giới hạn causal. IC dùng
Spearman, metric orientation trước rounding; alpha agent định hướng bằng
IC đã lưu4 decimals. Rank default norm01(|IC|/accuracy/Sharpe diagnostic),
trọng số.40/.35/.25, không long_acc. Sharpe sign(signal)×net return trên
hàng overlap là diagnostic đối xứng, không execution SHORT hoặc account.
Native query signal dùng strict±.10 trước round value4. Empty dynamic
backtest selection dừng; nonfinite last value vẫn có thể về0 ngay cả strict
mode. Historical alpha không gọi LLM reason. EX01 năm dòng khớp saved
alpha_factors/report, gồm WQ29 negative-IC flip; consensus1/3/1. Không suy
accuracy56.9% hoặc score.8509 là xác suất hay lợi nhuận tương lai.

Gói [U06 assets v2](../docs/plan/week12/unified_comparison_assets_v2.zip)
SHA256 `d5c4f1bc31c1a95d9e685a9cc13d1f86ce2d3cc0105b9023561fd5f567e2d8c4`.
Hai member dưới thư mục `outputs/unified_integration/u06_assets_v2/` được
đối chiếu `assets_manifest.json.members` (bytes/hash), không tái tạo:

| ID | Member tương đối | SHA256 nguyên byte |
| --- | --- | --- |
| EX01-AS | `frozen_selectors/FPT_b2023_h2.json` | `25a580cfb1999a2868ded4007091c993068db7e12c6fe244cccb25ee665e75b8` |
| EX01-AP | `frozen_alpha/FPT-2023-07-03.json` | `f59e4bebb8b2b86f7f2c87f7f5ca262263d96c8be2116111ce2f88d77dae5108` |

AS envelope semantic digest `35c16d6c5d39e22f53b2f769a835ac99d1fd36b04f451308e18800ac7bddfeb4`
khớp AP.selector_sha256; AP.projection_sha256
`024b8f3d633cff6a378d543ef886da00464780d5fffc8b518f2d029d9992315d`
khớp compact sorted JSON (bỏ trường digest). AP nguyên nội dung bằng
EX01-S.payload.causal_alpha.projection từ U08, không lấy preparation U06
làm bằng chứng hosted forecast. Source native/causal/economics trong AS
khớp SYS11/BG03/TIME01; config bằng CONFIG source frozen.

AS giữ history_origin2020-01-02, fit_end2023-06-30; train2021-04-14..2022-09-30,
validation2022-10-06..2023-06-27; test2023-07-03..2026-09-23. Có123 ngày
train-grid và55 ngày validation common support; tập dùng cho IC từng candidate
còn lọc finite, không nhận123 là mọi train_n. Boundary validation_end không
đồng nghĩa ngày cuối common support: ngày cuối được lưu là23/06/2023.
Không tự đổi lịch theo tên b2023_h2 hoặc nhận mỗi query được fit lại.
Đối soát chọn max validation-search score và tie-break từ giá trị đã lưu,
threshold.05, ID/sign đúng năm factor AP; không chạy validation mới.
Các value6 decimals trong bản thảo là round từ AP, signal theo full precision.

Nguồn SYS12 giữ `native_rowwise_causal_gate=FAIL` và `PASS_DETECTION`;
đọc lại source không phải chạy lại audit. Common scoped checks/receipt cũ
không sửa Native hoặc whole-system NOT_CERTIFIED. Không chạy compileall,
unit/E2E/leakage vì đợt này chỉ đổi nội dung tài liệu; F03/F04 giữ hash đã
kiểm khi tạo, không build lại cho T20.

### 9.7. Sentiment: đường live và hai provider lịch sử

T21; CL048–CL050. SYS13–SYS16 đối chiếu member snapshot và byte live.
Live `run_sentiment_for_alpha/_score_text/_lexicon_fallback/_aggregate_sentiment`
có backend/fallback riêng, title/snippet scoring và mean round4, label strict±.10;
không kiểm API hoặc tải model để viết. Cache component dùng
FrozenSentimentSnapshot→SentimentCache.get_at(strict=True,min_articles=3,
window_days=90); date_parsed inclusive≤cutoff, không mượn tin không ngày.
Sparse giữ mã neutral/score0 và reliability false, không phải observed neutral.

Context FrozenNews giữ available≥published.normalize()+1day; cutoff ở
23:59:59, cửa sổ90ngày theo available timestamp, age theo available, decay
half-life30ngày. Score hữu hạn±1, scorer tag visobert/lexicon; dưới3 score
trả avg_score=null, main.article_count=0 nhưng verified_article_count giữ
count thực. Không có list scored_articles hoặc peers để suy z/relative
sentiment từ dữ liệu không hiện hữu; không áp label±.10 của live cho provider.
Normalizer SYS03 compute từ3/main reliable8, proxy delta=z×.5. Threshold
reliability của cache và normalizer khác nhau, không dùng một cờ thay tất cả.

EX01-S đã pin §7: unavailable true, verified_count/article_count0,
avg_score null, list rỗng và normalized reliability false. Full sentiment
report có thông báo thiếu3score; các zero normalized không thay mask.
Chỉ đối soát source/saved output, không tính lại sentiment hoặc nâng gate
nghiên cứu. Đợt thuần tài liệu không chạy suite/runtime/API theo AGENTS§1.2.

### 9.8. Hồ sơ Native/Common và Full/Base

T22; CL051–CL054, B03 phần foundation inline tại §4.4. Chưa xuất CSV/TeX
hoặc hoàn tất bảng các prior ở T27. Source SYS17/SYS18 bổ sung; SYS05/BG18
và TIME01/SYS01/SYS02 dùng binding cũ, không lấy live UI làm nguồn frozen.
Native `original_fix_serving_v1` capture factory invocation; Common canonical
builder dùng integrated caps/COMMON_INSTRUCTION/prefix rỗng. Bridge đổi đúng
hai top-level fields alpha_report/alpha_factors; raw nested provenance còn
Native, không nói toàn JSON chuyển thành Common. Kiểm hai EX01 request:
point/repeat/model/temperature/max_tokens/client_max_retries/client_options/
service_tier/structured bằng nhau; messages khác, prompt3699/4186 chars.
Các số Alpha và raw/action dùng §9.6/§7, không sinh request mới.

Component TIME01 `_run_ablation_variants`: upstream.invoke một lần,
variant_input=deepcopy(upstream_state), config bật/tắt hai cờ; Full bật cả
hai, Base tắt cả hai, không vào Alpha node nếu cả hai false. Alpha-only và
sentiment-only là cấu hình được định nghĩa, actual panel phải nối protocol
§3.2; không dùng sự tồn tại của code để bổ sung run. Native/Common thay
selector/normalization/history/report/instruction/caps cùng lúc; Full/Base
thay bundle. Không suy riêng Alpha, prompt hoặc student causal effect.
Chỉ kiểm source/record/diff/liên kết, không replay hoặc chạy runtime suite.

### 9.9. Episode/bank, schema và timeline hợp lệ

T23; CL055–CL058. SYS19–SYS21 dùng source snapshot; memory schema/oracle,
CORE4 frozen bank và context freeze/reserved đọc riêng, không chạy loader
pipeline. Các file dưới có binding `snapshot_manifest.json.source_members`;
đối chiếu nguyên byte và by-ID với ba tasks trong U08 EX01 v1:

| ID | Member snapshot | SHA256 nguyên byte |
| --- | --- | --- |
| EP01 | `data_manager/regime_memory_store.json` | `09b48c6192a092b562173e8b3b7eceb44025c6e02454093e34214a730a460949` |
| EP02 | `data_manager/regime_memory_store.manifest.json` | `70ea72a41a518fc4e3ab57ebdac99506710733edc41fececbb6d832e39fdfb88` |
| EP03 | `docs/plan/week2/memory_bank_audit.json` | `c6368f7483191d5023cf5c74f305393b119864f2148c66a2fb7b09000f14eb54` |
| EP04 | `docs/plan/week1/historical_task_record.schema.json` | `ad718fa19e424046ece7529cd3dfa44c4506bd551cae096b3ed74f5ed4f0a948` |

EP02/03 bank_sha256 bằng EP01 raw byte hash;852unique ID, counts211/213/215/213,
first_as_of2020-06-01/latestexit2022-12-30. QA legacy schema_sha256 là
`77954798615a5075ccca1c4f7817a33bc58eac1e398ec0460114bc46eca39148`
của biến thể CRLF; source schema EP04 là LF. BG16 kiểm dựng đúng biến thể
CRLF, không sửa schema hoặc lấy LFrawhash thay legacyexpected. Bản ghi
FPT:2022-04-07 và hai record13/18April khớp nguyên nội dung saved retrieval.
Timeline có hai boundary minh họa được gắn nhãn, không là records mới.

Loader memory exact schema/dates/types, duplicate/overlap, event/price và
oracle rồi strict exit<cutoff. Bank852 giữ raw-execution source khác query
donor series; không tính lại nhãn trên donor. Numeric context dùng foldfreeze
trước queryđầu và reserved102 trước label API; K3prior/11rows+3target là
context khác3signal examples. Chỉ source/manifest/record/diff checks, không
chạy lại bank QA, oracle toàn bank, model hoặc benchmark.

### 9.10. Regime: resource/scaler, quality fallback và F05a

T24; CL059–CL063. Source SYS22/SYS23/SYS24, BG04/BG23 và providerBG16/17
được đối soát snapshot; chỉ đọc fit/inference implementation. Hai artifact
dưới có raw hash khớp `snapshot_manifest.json.source_members`:

| ID | Member snapshot | SHA256 nguyên byte |
| --- | --- | --- |
| RG01 | `data_manager/regime_model.json` | `7c1749752d449844cd458b71bb3fe5f276961b794e1bc8d1f1b90d8bddac026e` |
| RG02 | `outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/inputs/regime_models.json` | `5df0307a70b3df177a43faba8be04a72c00dabcb422c0b1c66a4b76cd84e724d` |

RG01 envelope semantic hash
`e8274ad3271f6e35a794a9f931a2aacf66297b923c00e2acde304ef6048b0747`;
payload chứa cả HMM/scaler/metadata, train2018-01-02..2022-12-30,
price1251/features1052, methodHMM/reasons[], iterations41. RG02 entry
2020-12-31 có parameters content hash
`cf711a9ce10dd1ebbccbeae048cce5bbd9f10271b9bab67a21e33aff5258541d`,
train2018-01-02..2020-12-31, price752/features553, methodHMM/reasons[],
iterations29. HMM5-feature StandardScaler nằm trong từng artifact, không
lấy4-feature scaler numericalMT thay. Không refit, gọi predict_proba hoặc
classify lại EX01; tên regime đọc từ trace và EX01-C.

EX01-C đã pin §7.2: regime=CONSOLIDATION; context.query.regime.name=BULL,
modelhash khớp RG02entry2020, feature_end=2023-07-03. Context4-feature scaler
modefrozen_train, fit731/cutoff2020-12-31/maxexit2020-12-29,
fit_ids_sha256 `25893eaad08b599103e7f4f1121c99e237d0eb8b6c008fa3a5e617e141f83f90`.
Digest mới để định danh chính object scaler đã lưu (JSON compact/sortkeys):
`5067ce86a04bc43f34c6c53cb3f7d8f1ceb23cab301b6bde6f313d56ce5dec2c`;
đây không là modelhash hoặc phép fit mới. Membership EX01-C nối hosted MT
bằng binding §7, không coi preparation thành forecast.

F05a là child của danh mục F05, sơ đồ fit/query hai resource và lưu ý scaler
MT riêng. Source TikZ/PDF/PNG tại assets/diagrams, build từ root với pdflatex
như F03, output tạm tmp/pdfs/thesis-t24. PDF1trang180×167mm, PNGmax2000px;
đã render/xem toàn trang sau dời label tránh đường nối, không cắt/chồng chữ,
fontType3 hoặc warning/overfull/underfull/undefined trong log. MiKTeX nhắc
cập nhật nhưng build exit0. Không sửa output regime hoặc receipt nghiên cứu.

| Artifact F05a | SHA256 (source LF, PDF/PNG nguyên byte) |
| --- | --- |
| [Source TikZ](assets/diagrams/F05a_regime_training.tex) | `916c693586d23dbd1ea14994f15001f88854a34f216883dab91eb65d2a48a8ce` |
| [PDF](assets/diagrams/F05a_regime_training.pdf) | `18832b0099f0d7b72894861dbfb0a6998a27dd0b8941f103841944565e5b7f1f` |
| [PNG](assets/diagrams/F05a_regime_training.png) | `717618e7f47b319911cfb75f36bee9e41ff5044938c10c1a3d5a6120e586f74a` |

### 9.11. Bayesian v1: ranking, population, prefix và fallback đã lưu

T25; CL064–CL069. BG07/BG16/BG18/SYS20/SYS18 dùng snapshot. Từ EP01 lọc
sameFPT và exit<2023-07-03 trước, được211; lọcCONSOLIDATION được19.
QueryCommon signals từ saved reports + causal5factor majority + newsnull:
T/P/A/I=+++-; score .25×số trùng4fields. Sắp score↓/exit↓/episode_id↑ cho
Apr7/Apr18/Apr13, scores1/.75/.75, khớp U08 trace metadata và record nguyên
nội dung. Chỉ tính số học trên archive, không import retriever/run benchmark.
Stats trên19: wins9/19, trap9/18, TrendFail7/14, PatternFail9/18; không dùng
top3 làm denominator hoặc gọi các rate này posterior Beta. Chưa có gate
min20 ở v1, không chuyển threshold C2 vào branch này.

Original BRPP là substring từ `[BRPP v1]` tới trước `\n### [1]` trong U08
EX01 v1 request:369Unicode chars,6lines. Bỏ prefix+newline khôi phục chính
xác Common request4186chars từ v1request4556chars. Bản tiếng Anh trong
manuscript ghi rõ translationforpresentation. Format max3tasks, NFC,
prefix≤600; requestguard<6500; overflowraise, không drop/cut examples.
V1T/P/A/I only, legendS=thiếu tin không thêm sentiment vào score. Render
không tự kiểm PIT/provenance thay caller.

FB01 bổ sung chỉ minh họa no-bank fallback, không thay EX01 hoặc chọn nhóm
case T45. Hai member dưới trong U08/slots cùng prefixthưmục §7.2, đã kiểm
manifest/rawhash/envelope/complete-attempt/outputdigest:

| FB01 slot | Tên member JSON | SHA256 nguyên byte |
| --- | --- | --- |
| `forecast/HVN-2023-07-03/u0/r0/original_common` | `8c89c0bdd588379a50a81a98ed5d460b120c26c691a7950b8fcfc39efc5c1c28.json` | `06d91dcc4ce3e939dfe81d449e3d866cd9ff896338a05305acd9f658d3750de3` |
| `forecast/HVN-2023-07-03/u0/r0/bayesian_v1` | `cd2d43b940bdd66156d4784a981804bc9b23322c5612605f74deb6947f776b2b.json` | `02afc84eac423c8ca10e35be824b30bf6f0c3760c8a2cea3bd6b9c8abf2e5ced` |

FB01v1 trace reasonNO_SAME_SYMBOL_FROZEN_BANK_OOD/fallbacktrue, tasks[],
statsnull/prepared.requestnull; forecastraw/requestsha/responsesha null,
policy raw_proposalnull,bypasstrue,reasonFALLBACK_ORIGINAL,finalLONG.
Dependency `original_common` digest
`2a09ec453ec637941229c7457b6bf7630f8c1cb531640e71a8e88f1ec0d2fa06`
khớp complete output Common cùng point/u0/r0; Common requestID
`a24b7410-5e45-490a-9e1a-f9d51d554749`. Không gọi đây là raw v1 forecast.

F05 nguồn TikZ/PDF/PNG minh họa membership→rank/statistics→prefix/bypass.
Build từ root bằng pdflatex như F03, outputtạm tmp/pdfs/thesis-t25;
PDF1trang180×190mm, PNGmax2000px. Đã render/xem toàn trang, không cắt/chồng
chữ/Type3 hoặc lỗi log. Không chạy suite/API/refit/replay vì chỉ sửa tài liệu
và hình giải thích, không thay code/runtime/input.

| Artifact F05 | SHA256 (source LF, PDF/PNG nguyên byte) |
| --- | --- |
| [Source TikZ](assets/diagrams/F05_memory_retrieval.tex) | `59bf81a1006faaa6e4ec69d4d764dfbe5b80d7722bc27defd8b0834b4a938371` |
| [PDF](assets/diagrams/F05_memory_retrieval.pdf) | `717a1d01c2757e7b1f6210db7b9f9dbe245281a6bfdaffad535e06ad743861d4` |
| [PNG](assets/diagrams/F05_memory_retrieval.png) | `3d8dc9b0af0554cb6aa3fe4d2356ff11231031b664110c46493c9129b7bbd41b` |

### 9.12. C2: partition, posterior và gate tách block

T26; CL070–CL073. BG05/BG06/BG07 và SYS25–27 đọc đúng snapshot/rawhash.
EX01 C2 dùng slot/hash tại §7.2, prepared.trace.evidence: P19, C1 duy nhất
FPT:2022-04-07, B18; IDs disjoint/union khớp bankEP01 đã lọc same-symbol/
regime/exit trước cutoff. Metric counts P/C/B tương ứng: win9/19,1/1,8/18;
trap9/18,0/1,9/17; trend7/14,0/1,7/13; pattern9/18,0/1,9/17.
Đối soát mean/prior/posterior và Beta2.5/97.5% bằng số học trên counts saved,
không chạy production stats/retriever. Table6decimals giữ raw fields nguồn.

Settings observed: shrink4; selector.5signal, decay365calendar days, age730,
gap5sessions, minbase.625, requested3. Stats P không áp age/feature/diversity
filters. Quality split nP≥20/nCmetric≥5/width≤.75, statsanymetric; examples
query/scaleravailable+nonemptylist và nP≥20 riêng. EX01 widths .7486954120,
.7444316222,.7458184921,.7444316222 dưới .75 nhưng fail floors19/1.
Selection IDs Apr7/Mar25/Mar4, retrieved3; examples gate false/effective0,
tasks visible[], prefixrỗng; prepared.request/rawC2null, policybypasstrue
reasonFALLBACK_ORIGINAL, finalLONG từ Common cùng point/repeat. Không nói
posterior hoặc ba selected records đã vào hosted prompt C2.

Đợt thuần tài liệu: kiểm source/manifest/record/count/quantile/link/diff,
không compileall/unit/E2E/leakage, refit, model/API hoặc replay nghiên cứu.

### 9.13. A/B và bảng so sánh bốn prior

T27; CL074–CL077, B03 phần prior viết inline ở §4.7.2 nối foundation §4.4;
CSV/TeX và DAG đầy đủ thuộc các task dàn trang/điều phối sau. SYS25/SYS28
phân biệt AconditionTP, Bpresentation; selectorSYS26/27 vẫn4signals+price.
Đọc PROFILES/PREFIXES và basefull_prior, không coi registeredcontentmodes
là panel đã chạy. C2 renderer vốn có counts/CrI; B đổi notation/semantics,
không thêm embedding/modelsearch. Thêm binding SYS29/30 phục vụ giải thích
4-dimensional rawfeatures/scalerindex, không dùng chúng thay scalerMT.

EX01: A.population19/conditional14/background5, counts P/C/B:
win9/19,7/14,2/5; trap9/18,7/14,2/4; trend7/14,7/14,0/0;
pattern9/18,7/14,2/4. Posterior means .4841269841/.5/.5/.5.
C2 và B toàn bộ evidence object bằng nhau, base_evidence_sha256
`0092e7def660273b8dc86e8de3393a91e6dd0d5a75a59fafb882687458332e2a`;
A khác, `2d11cd0e3b7a76150375d3593638cf6cc435902495d507648114bd83a434f5a8`.
SelectionIDs cả ba Apr7/Mar25/Mar4; requestedprefixversionsv3/v3_tp/vsemantic
nhưng actualprefix''/preparedrequestnull; policybypass/FALLBACK_ORIGINAL
finalLONG có dependency đúng Commonr0. Không dựng prefix giả rồi gọi đó là
request nghiên cứu; so sánh base evidence khác so sánh nội dung model đã thấy.

Chỉ kiểm snapshot/hash/group/count/mean/linkedrecord/Markdown, không chạy
suite, production renderer/retriever/API hoặc tính performance mới.

### 9.14. MT task/context và F06

T28; CL078–CL082. BG08/09/10, SYS29/31/32/33 và BG16/17/23 giữ nguồn
snapshot. Features21bars, volatilityddof0; scalerpopulationvariance/clip±4
khác HMM. Task63sessionblocks, same-symbol, bucket45bars trước taskselection;
centroidtừfulladmittedblock, priorregimematchpriority không hardfilter;
closest8prior/last8target. Foldfrozen/historyreserved giữ theo §9.9.

EX01-C member/hash §7.2 đọc qua U06assetsv2 manifest. ContextK3,m3,
eligible30; priorblocks11/15/13 chứa5/4/2rows, targetblock21 chứa3rows.
Queryindex1372/block21, raw/modelvectors round6 trong manuscript từ object
saved; scalerfit731. TargetdatesJun16/21/26 và exitsJun21/26/29;
queryentry/exit chỉ lịch, khôngr_net/y. Fullmembershipdigest
`9ed7e2a35da59ea5157fb6fe2baacd09671ebf12749943d0882bc98bc98f3cb4`
hash query/scaler/prior/target/advisor, nối U08 MT aux.branch đã pin §7.
Mọi selectedID/centroidID có factsbucket cùng query, không đọc labels để rank.

F06sourceTikZ/PDF/PNG giải thích taskcounts và offline/query boundary.
Build từ root bằng pdflatex như F03, outputtạm tmp/pdfs/thesis-t28;
PDF1trang180×185mm/PNGmax2000px đã render/xem và chỉnh điểm nối arrow,
không cắt/chồng chữ/Type3 hoặc warning/overfull/underfull/undefined trong log.
Không gọi feature/context/fit/predict pipeline; chỉ arithmetic từ saved
vectors, membership và source/record checks. Metadata PDF có thể khác khi
rebuild như các hình trước; source binding theo LF, sản phẩm theo raw bytes.

| Artifact F06 | SHA256 (source LF, PDF/PNG nguyên byte) |
| --- | --- |
| [Source TikZ](assets/diagrams/F06_mt_tasks_training.tex) | `bb2e84e3d86e738e0c3243beec7dd88daba55e86743c915c794154d7837f94b2` |
| [PDF](assets/diagrams/F06_mt_tasks_training.pdf) | `b0ceb9356163864de8debd57b4e588c60fc2f020efb9b81c4559935a0de569db` |
| [PNG](assets/diagrams/F06_mt_tasks_training.png) | `30ea056f1794df5790e59a461053583eaa2d647b46014acc9dc6ac3938ba4d2d` |

### 9.15. Teacher/student recipe, checkpoint và inference đã khóa

T29; CL083–CL088. BG11/BG12 và SYS34–41 đối chiếu snapshot byte. Các
artifact training được nối từ TR01 modelmanifest frozen; file receipt local
chỉ dùng sau khớp bytes/hash trong manifest. Không lấy tên full/final làm
định danh hoặc import/khởi tạo model để kiểm. TR01 semantic envelope hash
`0bffee83801e59b257c2fb6bb7bb352a7d9ca2721647824cb2cab3061af8aec3`.

| ID | Nguồn/locator | SHA256 nguyên byte |
| --- | --- | --- |
| TR01 | Snapshot `docs/plan/week11/mt_bicl_replica_full_r1_model.json` | `9937e1bdd0dbe7d9ca1156265cab027ead6dc1318caa542cdba1e81f28c95182` |
| TR02 | `docs/plan/week11/mt_bicl_replica_full_r1.json`, pin TR01.protocol | `11146a55e347be77b4a942c67d0acc9dba8646fa1d5a0b4817e5ffb504214857` |
| TR03 | Snapshot `outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/model/teacher.json` | `c0a39f327bacd8636fd7edff2f19b30799581bd144ac28176a7cd97fe9dbc335` |
| TR04 | Snapshot cùng namespace `model/candidate.pt`, TR01.artifact_trees | `a6f0d294b6f731bfc630fe58631b921ec2f0877338745a84e9459ec6a248e702` |
| TR05 | Cùng namespace `training/selection.json`, TR01.receipts | `ebc0f4e3fa14731f5dfc4ee47e32ee9a0c53e64b07483da20ceae4150d8939a5` |
| TR06 | Cùng namespace `training/state.json`, TR01.receipts | `77954c590e667c6f84604627e49f1b7da6582a4c2e3fa50e69362cbe4961e13e` |
| TR07 | Cùng namespace `training/seed42/checkpoint-03000.pt`, TR01.training.selected_checkpoint | `94145f90c5da6e0c8ab0daec439474b653769c47db09024de61d7f9303fd5932` |
| TR08 | Cùng namespace `training/seed42/checkpoint-03000.assessment.json`, TR05 global candidate report | `d12f01c705f6813f1375a0609f0868a68391e811e6f4883ae7f21b09b203dfc5` |

Đối soát10receipts trong TR01 và hai exportedcomponents nguyên byte, protocol
rawhash và semantic signature `1939d2095b8be52aa0956aa99d33409ea74548e4b56d01f8b76ec1c0e8402f79`.
TR03teacher16pi positive/sum1,48unique tasks/731cycles, converged237iters;
nguồnkhôngxétxvalue ởlikelihood. Simulator mu.2/.4/.6/.8×kappa2/8/32/128,
K0–3,m0–8,n2–8,731trainvectors independentlabelgen. Recipe các stream5000
syntheticvalidation/test có500stress; train640000/seed,5000steps,128batch.
Pilot/state physical128; sourceOOMoptions không phải giátrị đã chạy.

TR06 có60checkpoint/report pointers đủ20steps/seed17/42/73. Kiểm hash của
60assessmentfiles và envelope, chọn theo saved eligible/2021macroLL/Brier/
step/seed-order khớp TR05 và TR01:seed42/step3000. Selectedcheckpoint raw
hashkhớp TR07; exportedcandidate rawhash khác vì không chứa optimizer/RNG.
Tensorfingerprint được receipt ghi
`c60ae9695dde6f308ff30b0f4de7e40539ea5e8353cc7b1e0acb3d57a11f471c`;
không tự tính lại tensorhash bằng loadmodel. Số market2021/validation trong
receipt dùng kiểm selection, không táiước lượng hoặc đưa performance mới
vào Chương4. Các acceptance flags READY_FOR_H03_BINDING/inference_releasedfalse
ở manifest là mốc resource trước U08, không đổi release/gate hiện hành.

Packing source train BG12/runtimeSYS37 cùng kiếntrúcpaired37; counttham số
271873 kiểm bằng kích thước layers/embeddings, không modelinit. EX01tokens
14obs+4markers+1query=19,pos18, maskedquerytail[0,1]; p_student saved
.38681803029367656 tại U08MTaux.branch. F06 giữ nguyên hash đã kiểm T28,
không build lại cho task viết. Không training, syntheticgeneration, predict,
coldreplay, API hoặc suite; chỉ source/hash/receipt/packing/arithmetic checks.

### 9.16. Facts, Fact Anchor và nhánh assertion không hợp lệ

T30; CL089–CL092. BG10/SYS33/SYS42/BG14/BG18 lấy từ snapshot; không chạy hàm
tạo facts, TA-Lib, bộ dựng prompt hoặc LLM. Fact_Anchor của EX01 trong U08
dùng packet, reply, policy/proof tại slot/hash đã ghi ở §7.2.
MACD/Signal/Close/SMA20 và hiệu số được chép đủ độ chính xác; ba assertion là
BELOW/POSITIVE/ABOVE, bucket là MACD_NEG_PRICE_POS.
Hash của prefix PIT gốc (dates/columns/values, 45 bar) là
`83263839c601360faea0017da5362741a1fa5d068903fd0ceafe8cedfec60ba2`;
hash nội dung packet là `c6f7d2919729c53215a263f3e106ea6c33704f6afc50702804527865ce7227ba`.
Thẻ facts định dạng .8g được kiểm bằng chuỗi con trong prompt đã lưu dài
3.916 ký tự; không dựng request mới.

Digest dependency Common là `964b7aa19d16e01affa47869a62a2ad20bcc8c1a0eb204f4926abc92a9471c41`;
digest đối tượng raw của anchor là `25c472eae6d4d3285fc05cd4886ed35cdd20431903211505d24e616aca637220`.
Hash đối tượng proof là `1b4a5846922443657bae8e91d68c7489dfd58ea92688bdce007cb29b14f70049`;
request ID là `f7c7664b-69c7-4bef-a075-26c2d9c0d6e2`.
Assertion hợp lệ, context_reason=NOT_APPLICABLE; raw LONG, confidence=Cao,
R:R=1.5; a0/final=LONG, reason=NO_NUMERIC_VETO, q10=null và bypass=false.
`prepared.aux.anchor` của MT khớp proof/output này và dependency Fact_Anchor
cùng repeat. Không diễn giải p_student thấp thành veto số của anchor.

Giữ giới hạn văn xuôi: reply đã lưu nói “MACD below Signal indicates bullish
momentum” và “positive zero crossing”; hợp đồng enum không kiểm các luận điểm
đó. Packet chỉ xác nhận quan hệ tại điểm cuối, không chứng minh giao cắt.
Phản ví dụ minh họa hợp lệ về schema đổi decision=SHORT/MACD_ZERO=NEGATIVE
được gắn nhãn Illustrative; so sánh sai dẫn đến Common LONG/valid=false.
Không chạy policy/model để tạo response hoặc gọi đó là bản ghi nghiên cứu.

FA01 là schema wire `docs/plan/week11/mt_bicl.schema.json`, 13.541 byte,
raw SHA-256 `0ff8ae6d4c58b33a1672ad45b3a852d650fd32c95fd20da2ae6e33dcf8861dc8`,
khớp snapshot manifest, bản live và SYS33 `SCHEMA_SHA256`. Chỉ schema/enum/proof/source/hash/link checks;
không compileall/unit/E2E/leakage vì không đổi code/runtime/input, không
fit/forward/replay/API. Utility/policy đầy đủ vẫn chờ T31.
