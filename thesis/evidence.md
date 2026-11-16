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
thiếu: MT-BICL và PFN, tổng **59 nguồn/10 nhóm** tại T04. P5 bổ sung ba nguồn, thành 62 mục discovery; bibliography chỉ nhận 22 nguồn đã kiểm theo §11.1.
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
  có phạm vi ghi tại §4.4, §8.5 hoặc §11.1**. Không có nghĩa đã đọc/kiểm mọi trang, tái lập
  kết quả, kiểm quyền phát hành hoặc xác minh ứng dụng sang thị trường Việt Nam.
- Tại mốc T04: **3 DA_KIEM, 5 DA_DOC, 51 CHUA_DOC**. Cập nhật P5 tại §11.1 ghi 22 nguồn đã kiểm cho bibliography riêng và thêm ba ứng viên; không coi toàn bộ danh sách là đã đọc. A = đọc trước
  khi viết phương pháp/đánh giá liên quan; B = nguồn so sánh/bổ trợ; C = đọc
  tùy mức liên quan. Ưu tiên không phải đánh giá chất lượng nghiên cứu.
- Sau P5, danh sách có **62 mục**: **24 DA_KIEM theo phạm vi** (22 mục của
  bibliography và hai trang TA-Lib tại §8.5.2), **38 CHUA_DOC**. Không có
  mục DA_DOC còn lại sau các lần đối chiếu đã ghi.
- Link trong 38 dòng CHUA_DOC là **đích cần kiểm**, không phải xác nhận đã
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
| `lo2000technical` | [Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation](https://business.columbia.edu/sites/default/files-efs/pubfiles/19268/Lo-Mamaysky_wang_foundations.pdf) — 2000 | A | DA_KIEM (phạm vi §11.1) |
| `grinold1999active` | [Active Portfolio Management](https://www.mheducation.com/highered/mhp/product/active-portfolio-management-quantitative-approach-producing-superior-returns-selecting-superior-returns-controlling-risk.html) — 1999 | B | CHUA_DOC |
| `kakushadze2016formulaic` | [101 Formulaic Alphas](https://arxiv.org/abs/1601.00991v3) — 2016 | A | DA_KIEM (phạm vi §11.1) |
| `jegadeesh1993momentum` | [Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency](https://doi.org/10.1111/j.1540-6261.1993.tb04702.x) — 1993 | B | CHUA_DOC |
| `fama1992crosssection` | [The Cross-Section of Expected Stock Returns](https://doi.org/10.1111/j.1540-6261.1992.tb04398.x) — 1992 | B | CHUA_DOC |
| `hurst2017trend` | [A Century of Evidence on Trend-Following Investing](https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/AQR-JPM-Fall-2017.pdf) — 2017 | B | CHUA_DOC |
| `talib_rsi_docs` | [Relative Strength Index (RSI)](https://ta-lib.github.io/ta-doc/indicator/RSI.htm) — n.d. | A | DA_KIEM (phạm vi §8.5.2) |
| `talib_willr_docs` | [Williams' %R (WILLR)](https://ta-lib.github.io/ta-doc/indicator/WILLR.htm) — n.d. | A | DA_KIEM (phạm vi §8.5.2) |

#### Nhóm 2. LLM và hệ thống đa agent tài chính

Chương 2.2/4.3; nguồn kế thừa kiến trúc và các hệ so sánh; không nhập kết quả của chúng thành kết quả khóa luận.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `xiong2025quantagent` | [QuantAgent: Price-Driven Multi-Agent LLMs for High-Frequency Trading](https://arxiv.org/abs/2509.09995v3) — 2025 | A | DA_KIEM (phạm vi §11.1) |
| `tradingagents2024` | [TradingAgents: Multi-Agents LLM Financial Trading Framework](https://arxiv.org/abs/2412.20138v7) — 2025 (v7; khóa legacy2024) | B | DA_KIEM (phạm vi §11.1) |
| `fatemi2024finvision` | [FinVision: A Multi-Agent Framework for Stock Market Prediction](https://arxiv.org/abs/2411.08899v1) — 2024 | B | DA_KIEM (phạm vi §11.1) |
| `wu2023bloomberggpt` | [BloombergGPT: A Large Language Model for Finance](https://arxiv.org/abs/2303.17564v3) — 2023 | B | CHUA_DOC |
| `yang2023fingpt` | [FinGPT: Open-Source Financial Large Language Models](https://arxiv.org/abs/2306.06031v1) — 2023 | B | CHUA_DOC |
| `xia2026agentictrading` | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337v2) — 2026 | C | CHUA_DOC |
| `deng2017deep` | [Deep Direct Reinforcement Learning for Financial Signal Representation and Trading](https://ieeexplore.ieee.org/abstract/document/7407387) — 2017 | B | CHUA_DOC |

#### Nhóm 3. Thị giác và kiểm hiểu biểu đồ

Chương 2.2/4.3/5.9; phân biệt biểu đồ thông thường, candlestick và limit-order book.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `han2023chartllama` | [ChartLlama: A Multimodal LLM for Chart Understanding and Generation](https://arxiv.org/abs/2311.16483v1) — 2023 | B | DA_KIEM (phạm vi §11.1) |
| `tsantekidis2017lob` | [Forecasting Stock Prices from the Limit Order Book Using Convolutional Neural Networks](https://pure.au.dk/portal/en/publications/forecasting-stock-prices-from-the-limit-order-book-using-convolut/) — 2017 | B | CHUA_DOC |
| `shu2026finchart` | [FinChart-Bench: Benchmarking Financial Chart Comprehension in Vision-Language Models](https://aclanthology.org/2026.acl-long.615/) — 2026 | C | CHUA_DOC |
| `wang2026martingale` | [Martingale Doppelgänger-Eval: An Identification Framework for Auditing Candlestick Understanding in Vision-Language Models](https://arxiv.org/abs/2606.17423v1) — 2026 | C | CHUA_DOC |

#### Nhóm 4. Sentiment tài chính và NLP tiếng Việt

Chương 2.2/3.3/4.3; backbone, classifier, miền dữ liệu và scoring recipe là các đối tượng khác nhau.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `nguyen2023visobert` | [ViSoBERT: A Pre-Trained Language Model for Vietnamese Social Media Text Processing](https://aclanthology.org/2023.emnlp-main.315/) — 2023 | A | DA_KIEM (phạm vi §11.1) |
| `hf5cdsentiment` | [5CD-ViSoBERT for Vietnamese Sentiment Analysis](https://huggingface.co/5CD-AI/Vietnamese-Sentiment-visobert) — n.d. | A | DA_KIEM (phạm vi §11.1) |
| `araci2019finbert` | [FinBERT: Financial Sentiment Analysis with Pre-trained Language Models](https://arxiv.org/abs/1908.10063v1) — 2019 | B | CHUA_DOC |
| `tetlock2007news` | [Giving Content to Investor Sentiment: The Role of Media in the Stock Market](https://business.columbia.edu/sites/default/files-efs/pubfiles/3097/Tetlock_Media_Sentiment_JF.pdf) — 2007 | B | CHUA_DOC |
| `wolf2020transformers` | [Transformers: State-of-the-Art Natural Language Processing](https://aclanthology.org/2020.emnlp-demos.6/) — 2020 | B | CHUA_DOC |

#### Nhóm 5. Regime, HMM và Bayes nền tảng

Chương 2.3/3.4–3.6; lọc so với làm trơn, học tham số, posterior và bất định. Bayesian bootstrap chỉ dùng khi khớp phép tính thực tế.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `rabiner1989hmm` | [A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition](https://web.mit.edu/6.435/www/Rabiner89.pdf) — 1989 | A | DA_KIEM (phạm vi §11.1) |
| `hamilton2005regimes` | [Regime-Switching Models](https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf) — 2005 | A | DA_KIEM (phạm vi §11.1) |
| `dempster1977em` | [Maximum Likelihood from Incomplete Data via the EM Algorithm](https://web.mit.edu/6.435/www/Dempster77.pdf) — 1977 | A | CHUA_DOC |
| `gelman2013bayesian` | [Bayesian Data Analysis](https://sites.stat.columbia.edu/gelman/book/) — 2013 | A | CHUA_DOC |
| `rubin1981bootstrap` | [The Bayesian Bootstrap](https://doi.org/10.1214/aos/1176345338) — 1981 | A | CHUA_DOC |

#### Nhóm 6. ICL, truy xuất và MT-BICL

Chương 2.4–2.5/3.6/4.8; tách few-shot, implicit Bayes, PFN và context đa tác vụ. Hai khóa mới là đề xuất cho bibliography khóa luận.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `xie2022implicitbayes` | [An Explanation of In-context Learning as Implicit Bayesian Inference](https://arxiv.org/abs/2111.02080v6) — 2022 | A | DA_KIEM (phạm vi §11.1) |
| `rubin2022retrieve` | [Learning To Retrieve Prompts for In-Context Learning](https://aclanthology.org/2022.naacl-main.191/) — 2022 | A | DA_KIEM (phạm vi §11.1) |
| `wei2022chain` | [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://proceedings.neurips.cc/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract.html) — 2022 | B | CHUA_DOC |
| `zhu2026multitask` | [Multi-Task Bayesian In-Context Learning](https://arxiv.org/abs/2606.20538v1) — 2026 | A | DA_KIEM (phạm vi §11.1) |
| `muller2022transformers` | [Transformers Can Do Bayesian Inference](https://arxiv.org/abs/2112.10510v7) — 2022 | A | DA_KIEM (phạm vi §11.1) |

#### Nhóm 7. Thiết kế đánh giá, chọn mô hình và phụ thuộc

Chương 2.6/3.7/5.5/5.9; thiên lệch lựa chọn, nhiều so sánh, resampling phụ thuộc và backtest. Có phương pháp trong nguồn không có nghĩa nghiên cứu đã chạy phương pháp đó.

| Khóa trích dẫn | Nguồn gốc/ứng viên và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `varma2006bias` | [Bias in Error Estimation When Using Cross-Validation for Model Selection](https://bmcbioinformatics.biomedcentral.com/counter/pdf/10.1186/1471-2105-7-91.pdf) — 2006 | A | DA_KIEM (phạm vi §11.1) |
| `white2000reality` | [A Reality Check for Data Snooping](https://users.ssc.wisc.edu/~behansen/718/White2000.pdf) — 2000 | A | DA_KIEM (phạm vi §11.1) |
| `harvey2016` | [...and the Cross-Section of Expected Returns](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF) — 2016 | A | CHUA_DOC |
| `bailey2014deflated` | [The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality](https://davidhbailey.com/dhbpapers/deflated-sharpe.pdf) — 2014 | B | CHUA_DOC |
| `holm1979multiple` | [A Simple Sequentially Rejective Multiple Test Procedure](https://sci2s.ugr.es/keel/pdf/specific/articulo/0052_001.pdf) — 1979 | A | DA_KIEM (phạm vi §11.1) |
| `lahiri2003resampling` | [Resampling Methods for Dependent Data](https://www.gbv.de/dms/goettingen/366100181.pdf) — 2003 | A | CHUA_DOC |
| `newey1987hac` | [A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix](https://www.ssc.wisc.edu/~bhansen/718/NeweyWest1987.pdf) — 1987 | B | DA_KIEM (phạm vi §11.1) |
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
| `pedregosa2011sklearn` | [Scikit-learn: Machine Learning in Python](https://jmlr.org/papers/v12/pedregosa11a.html) — 2011 | B | DA_KIEM (phạm vi §11.1) |
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


#### Bổ sung cho P5

Ba nguồn sau được nhận sau danh sách T04; không thay lịch sử 59 ứng viên ban đầu.

| Khóa trích dẫn | Nguồn gốc và năm | Ưu tiên | Trạng thái đọc |
| --- | --- | --- | --- |
| `politis1994stationary` | [The Stationary Bootstrap](https://doi.org/10.1080/01621459.1994.10476870) — 1994 | A | DA_KIEM (phạm vi §11.1) |
| `arnott2019backtesting` | [A Backtesting Protocol in the Era of Machine Learning](https://doi.org/10.3905/jfds.2019.1.064) — 2019 | A | DA_KIEM (phạm vi §11.1) |
| `yresearch2026quantagentcode` | [QuantAgent source comparison snapshot](https://github.com/Y-Research-SBU/QuantHarness/tree/92519f806286192345e940e7ab77496462d662b7) — 2026 | A | DA_KIEM (phạm vi §11.1) |

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
| F09 | **Mean account-return differences against Native and Common.** Giữ hai baseline, năm extension mỗi baseline và band mô tả; trục dùng pp. | Ch. 5.7–5.8 | T43 | ĐÃ_CÓ_VECTOR_RENDER_ĐÃ_XEM | ED07; §10.9 | [Source](assets/figures/F09_return_contrasts.py), SVG/PDF/PNG; rawpins đầu vào và hash đầu ra §10.9 |
| F10 | **Historical-context coverage and final-action changes.** Hiện support, fallback/bypass và mức giữ anchor; không quy thay đổi gộp cho student riêng. | Ch. 5.8 | T44 | ĐÃ_CÓ_VECTOR_RENDER_ĐÃ_XEM | ED07/16/40; §10.10 | [Source](assets/figures/F10_coverage_actions.py), SVG/PDF/PNG; hash §10.10 |
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
| B05 | **Component results and sensitivities.** B05a–g kết quả, B05h–j cohort/strata/12scenario. | Ch.5.6/5.8; App.D | T41/T46 | ĐÃ_CÓ_BẢN_NHÁP_MARKDOWN | §10.7/§10.12 | Mọi ô có nguồn; CSV/LaTeX ởT69 |
| B06 | **Context results, contrasts and sensitivities.** B06a–h đủ8role/2control, repeats, 20contrast, bridge, sensitivity và missingpanel. | Ch.5.7–5.9; App.D | T42/T43/T46/T47 | ĐÃ_CÓ_BẢN_NHÁP_MARKDOWN | §10.8/§10.9/§10.12/§10.13 | Mọi ô có nguồn; CSV/LaTeX ởT69 |
| B07 | **Context, policy, cases and resources.** B07a–h giữ coverage/NA/302of306anchor, rulecases và usage/timing. | Ch.5.8; App.B/D | T44/T45/T46 | ĐÃ_CÓ_BẢN_NHÁP_MARKDOWN | §10.10–§10.12, CT01–CT30 | Mọi ô có nguồn; CSV/LaTeX ởT69 |
| B08 | **Comparison with related research.** B08a tài chính đa agent; B08b context/Bayes/MT; từng hàng/cột có nguồn, giữ các giới hạn PIT/economics/novelty. | [Ch.2.7](chapters/02_related_work.md#27-research-gap-and-position-of-the-thesis) | T53 | ĐÃ_CÓ_BẢN_NHÁP_MARKDOWN | R04/R06/R07/R13–R16 và binding nội bộ; §11.6 | Bảng trong chương; CSV/LaTeX ở T70, chưa dàn trang cuối |
| B09 | **Research questions and remaining evidence.** ĐủRQ1–4, observations, boundedanswers và missingevidence. | Ch.5.9.3/B09; Ch.6.2 tổng hợp | T47/T56 | ĐÃ_CÓ_BẢN_NHÁP_CHƯƠNG5_VÀ6 | CL145–CL187/CL221–CL226; §10.13/§12.3 | Bảng trong§5.9, câu trả lời §6.2; chưa chuyển CSV/LaTeX |

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
  outcome. Ch. 4.3–4.5/T18–T24: inputs, hai view, missing sentiment và hai
  loại lịch sử. Ch. 4.6–4.8/T25–T32: nối v1/C2/A/B, numeric context,
  teacher/student và anchor/policy; giữ hai nguồn regime riêng.
- Ch. 4.9/T33: shared u0 và các nhánh/repeat; Ch. 4.10/T35: mở outcome
  §7.6 sau facts/proposals/actions; Ch. 5.8/T45 phân tích ca trong kết quả rộng hơn.
  B07/F10 có thể dùng EX01, nhưng ví dụ
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
| [01_introduction.md](chapters/01_introduction.md) | §1 metadata; outline §A; CL214–CL220/§12.1–12.2 | Đủ bản nháp §§1.1–1.5: động cơ/bài toán, bốn RQ, phạm vi, attribution và mạch sáu chương; chưa review/dàn trang cuối |
| [02_related_work.md](chapters/02_related_work.md) | §4 discovery register; §11 nguồn/version/claim; §6 B08 | P5/T48–T53 đủ bản nháp§2.1–§2.7/B08a–b, bibliography22nguồn; còn ràsoátliênchương/G3toànbộ vàdàntrangcuối |
| [03_background.md](chapters/03_background.md) | §3 nguồn hợp đồng; §4 tài liệu phương pháp; §5 ký hiệu; §6 F01/F02; §8.4–§8.5 binding nền tảng | Bản nháp §3.1–§3.7; claim đối soát nội bộ ở §8.2; chưa rà soát khoa học/trích dẫn/toàn văn cuối |
| [04_proposed_system.md](chapters/04_proposed_system.md) | §3 source/runtime; §5 tên/ID; §6 danh mục; §7 EX01; §9 nguồn phương pháp | P3 đủ bản nháp §4.1–§4.10, kèm F03/F04/F05/F05a/F06/F07/F08/F11, B03 và A01–A03; G2 tự kiểm nội bộ, UI/F11 vẫn PENDING, chưa rà soát/dàn trang cuối |
| [05_experiments.md](chapters/05_experiments.md) | §3 hai nghiên cứu; §6 bảng/hình; §7 EX01; §10 nguồn/ô/claim | P4/T36–T47 đủ bản nháp§5.1–§5.9, F09/F10/B04/B05/B06/B07/B09; còn App.D, ràsoát/G3toànbộ vàdàntrangcuối, khôngđổi acceptance nghiêncứu/UI |
| [06_conclusion.md](chapters/06_conclusion.md) | Outline §A; Ch.5/B09; CL221–CL230/§12.3–12.4 | Đủ bản nháp §§6.1–6.4: bốn câu trả lời, giới hạn và ưu tiên nghiên cứu riêng; không kết quả mới hoặc review/dàn trang cuối |

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

| CL093 | [Utility/support](chapters/04_proposed_system.md#484-utility) | HOP_DONG_TRIEN_KHAI | BG13/BG11/SYS33; §9.17 | 45 bar, bucket biết, K≥2, ≥5 mỗi dấu; thiếu support trả null/0 draws | Không cân bằng nhãn hoặc fallback teacher khi student lỗi |
| CL094 | [Sampler/mean](chapters/04_proposed_system.md#484-utility) | HOP_DONG_TRIEN_KHAI | BG13; §9.17 | 4096 draw, family posterior/target Beta, bootstrap magnitude theo ID; CRN/linear quantile | p_student không thay theta; giả định pooling magnitude khác PIT |
| CL095 | [EX01 utility](chapters/04_proposed_system.md#484-utility) | DO_DUOC | U08 MT aux.branch.utility; §7.5/§9.17 | 5 gain/9 loss, mean/MC/Q10/Q90/draw hash đúng wire | Không sinh lại draws hoặc gọi interval là coverage đã hiệu chuẩn |
| CL096 | [Policy/trace](chapters/04_proposed_system.md#486-external-policy) | HOP_DONG_TRIEN_KHAI | BG14/BG18/SYS33; §9.17 | facts→same action→strict Q10 delta; invalid/unsupported/error riêng | EX01 KEEP_PROPOSED_SAME, không có veto; component paths khác unified roles |
| CL097 | [F07 và bốn ví dụ](chapters/04_proposed_system.md#486-external-policy) | MINH_HOA | BG14, arithmetic; §9.17 | CASH→LONG Q10U>0; LONG→CASH −Q90U>0, equality reject | Ví dụ giả định có nhãn, không tạo response/kết quả nghiên cứu |

| CL098 | [Projection membership](chapters/04_proposed_system.md#485-context-projection) | HOP_DONG_TRIEN_KHAI | SYS43/BG09; §9.18 | n/w/l/r toàn group, age từ exit; exemplar nearest/latest/ID | Không đổi membership hoặc lấy exemplar làm mẫu số |
| CL099 | [Feature code/interventions](chapters/04_proposed_system.md#485-context-projection) | HOP_DONG_TRIEN_KHAI | SYS43/SYS42; §9.18 | rint(2v), clip±8; Plain/NoU cùng Full mask; No_target tính lại | Tên builder không chứng minh thực nghiệm hoặc unified role |
| CL100 | [EX01 projection](chapters/04_proposed_system.md#485-context-projection) | DO_DUOC | U08 MT aux.branch/projection/request, U06 context; §9.18 | 14 rows/4 exemplar, prefix437/request4586, summary/count/mean/age/code | English translation không là request gốc; query không y/r_net |
| CL101 | [Input/schema/budget](chapters/04_proposed_system.md#485-context-projection) | HOP_DONG_TRIEN_KHAI | BG18/SYS42/SYS18; U08; §9.18 | Six family rows, fact/anchor/projection guards; causal content card | Short content digest khác proof; C2/A/B bypass không có prompt quan sát |

| CL102 | [B03/F08](chapters/04_proposed_system.md#491-eight-roles-on-one-shared-parent) | HOP_DONG_TRIEN_KHAI | SYS44–SYS46/BG18; §9.19 | Eight roles, registry dependencies và fallback, shared u0 | Shared input khác forecast dependency; Fact Anchor là role dependency |
| CL103 | [Order/repeats](chapters/04_proposed_system.md#491-eight-roles-on-one-shared-parent) | HOP_DONG_TRIEN_KHAI | SYS45–SYS46; U08 EX01; §9.19 | ordered_branches(3i+r), topo/rotation/Native insertion; output map mới mỗi repeat | Slot/response/HTTP khác nhau; không làm lại upstream |
| CL104 | [A01–A03](chapters/04_proposed_system.md#492-algorithms-and-outcome-barrier) | MINH_HOA | BG16/BG17/BG18/SYS46/SYS47; §9.19 | PIT context, method/policy và paired evaluation pseudocode | Không source replacement/new run; resource fit offline; exposure cũ không biến mất |
| CL105 | [EX01 barrier](chapters/04_proposed_system.md#492-algorithms-and-outcome-barrier) | DO_DUOC | U08 24 prepare/forecast slots + shared/outcome; §9.19 | All timestamp order, parent digests, same-repeat deps; r0 five replies/three bypass | Không cold replay hoặc nâng Native FAIL/whole-system NOT_CERTIFIED |

| CL106 | [Budget](chapters/04_proposed_system.md#4101-prompt-admission-and-bounded-repair) | HOP_DONG_TRIEN_KHAI | SYS02/SYS18/SYS42/SYS48/SYS52/BG18; §9.20 | cap từng report, prefix600/facts700/anchor80/final<6500 kể cả repair | Ký tự khác token; cap có thể mất nội dung giữa |
| CL107 | [Retry/format](chapters/04_proposed_system.md#4102-one-retry-owner-and-durable-http-evidence) | HOP_DONG_TRIEN_KHAI | SYS48/SYS49/SYS02; §9.20 | One owner, ≤3 HTTP active execution, raw trước parse, schema repair khác semantic | Legacy delay cap60 khác durable max provider waits; không nhân retry |
| CL108 | [Quota epochs](chapters/04_proposed_system.md#4102-one-retry-owner-and-durable-http-evidence) | DO_DUOC | SYS48/SYS53/SYS54; OP01/OP02; §9.20 | Pooled→org/model tại487→provider response tại591 | Không mô tả toàn U08 bằng policy đầu; không suy quota hiện hành |
| CL109 | [Checkpoint/UNKNOWN](chapters/04_proposed_system.md#4103-checkpoint-lifecycle-and-recovery) | HOP_DONG_TRIEN_KHAI | SYS48/SYS50/SYS51/SYS46; §9.20 | Identity/intent/raw/stage hashes; ambiguoussend dừng, NOT_SENT có evidence | Lifecycle interrupted mô tả source, không nhận chạy crash test mới |
| CL110 | [Authorized replacements](chapters/04_proposed_system.md#4103-checkpoint-lifecycle-and-recovery) | DO_DUOC | SYS55–SYS57; OP03/OP04; §9.20 | Two point generations/one exhausted slot, retired12→15 giữ ledger/cost | Ngoại lệ có backup/grant; không reset ngầm hoặc bỏ valid response để chọn action |

| CL111 | [Current application form](chapters/04_proposed_system.md#4104-application-workflow-and-interpretation) | HOP_DONG_TRIEN_KHAI | AP01/AP03/AP13–AP15; §9.21 | Six main versions/1D/one analyze repeat; Original legacy, enhanced capture/preflight/job | Backend modes không là form hiện hành; MT closure3 khác study8 |
| CL112 | [Capture/identity](chapters/04_proposed_system.md#4104-application-workflow-and-interpretation) | HOP_DONG_TRIEN_KHAI | AP04–AP07/AP10/AP11; §9.21 | Timeframe envelope1d có daily_provisional; owner/hash/freshness/PIT, GET đọc capture | Không đồng nhất older daily-closed path; no future prices/false CASH |
| CL113 | [Live resource transfer](chapters/04_proposed_system.md#4104-application-workflow-and-interpretation) | HOP_DONG_TRIEN_KHAI | AP08/AP09; §9.21 | Frozen selector/top5/scaler/HMM/student, labels before2026-07-01; querylive | Transfer không refit/parity vendor; planned weekdays không lịch sàn |
| CL114 | [Presentation/result](chapters/04_proposed_system.md#4104-application-workflow-and-interpretation) | HOP_DONG_TRIEN_KHAI | AP02/AP12–AP15/AP17; §9.21 | Same-job reports/context; bilingual existing invocations/canonicalpolicy/stored switch | Logic-equivalent UI không cùng raw bytes; confidence/RR khác actual P&L |
| CL115 | [EX01 complete walkthrough](chapters/04_proposed_system.md#4105-closing-ex01-after-the-forecasting-barrier) | DO_DUOC | U08 shared/24 forecasts/outcome, TIME01/TIME06; §7/§9.21 | Entry48180/exit48390, gross+.4358655%/net−.2647317%, DOWN; r0 actions | Outcome chỉ sau barrier; cycle không portfolio; không thay ca sai bằng ca thắng |
| CL116 | [Application acceptance](chapters/04_proposed_system.md#4104-application-workflow-and-interpretation) | DO_DUOC | AP16/AP17; §9.21 | OFFLINE_PASS_BROWSER_PENDING/f11false;135Python/24DOM recorded, 403 nguồn khớp | Không chạy lại suite/browser/market/API, không chứng nhận deployment/lợi nhuận |

| CL117 | [Two studies](chapters/05_experiments.md#511-two-response-collections-and-two-questions) | DO_DUOC | ED01–ED03/ED06–ED09; §10.2 | Main102/51 accounts riêng response collection; Full/Base khác Native/Common | Không trộn cohort support với execution/response count |
| CL118 | [Execution accounting](chapters/05_experiments.md#511-two-response-collections-and-two-questions) | DO_DUOC | ED02/ED03 và records/panels; §10.2 | 204+54+135−18=375; reused193/new182/attempt194/errors12 | New là release-relative, không tổng tất cả donor/vision |
| CL119 | [Freezes/exposure](chapters/05_experiments.md#512-what-was-frozen-and-what-acceptance-establishes) | DO_DUOC | ED01/ED04/ED05/ED08/ED09; §10.2 | Component freeze giữa first/last request; U08 seal/accept UTC khác financial dates | Post-inference, served revision null, không preregistered/untouched holdout |
| CL120 | [Acceptance boundary](chapters/05_experiments.md#512-what-was-frozen-and-what-acceptance-establishes) | HOP_DONG_TRIEN_KHAI | ED04/ED07–ED09; §3/§10.2 | PASS scopes, Native FAIL/whole-system NOT_CERTIFIED/UI pending | Không new replay/API hoặc lấy component factorial thay unified ablation |

| CL121 | [Data provenance/exclusion](chapters/05_experiments.md#521-vendor-data-admissible-views-and-exclusions) | DO_DUOC | ED10/ED11/ED13; §10.3 | 9 raw files1681rows, BHN673prefix excluded,102/108cells | Vendor reconstruction khác authenticated snapshot; no synthetic repair |
| CL122 | [Schedule/B04a](chapters/05_experiments.md#522-main-schedule-and-chronological-partitions) | DO_DUOC | ED11/ED13/ED16, U08 shared; §10.3 | 12dates/6folds/102points/51accounts; component train32–318/validation18–21 | Hai endpoints/fold không continuous daily backtest |
| CL123 | [Final context split](chapters/05_experiments.md#522-main-schedule-and-chronological-partitions) | DO_DUOC | ED14/ED15 alpha_support; §10.3 | 51bindings/9selectors,8×123train/BHN85;validation54–60/BHN56 | Amended firewall không xóa prototype/exposure; component splits khác |
| CL124 | [Coverage/B04b](chapters/05_experiments.md#523-coverage-historical-resources-and-missing-sentiment) | DO_DUOC | ED11/ED12/ED15/ED16; §10.3 | UP25/DOWN77;missing79;CORE4bank852;48/54support | Bank count khác query eligibility, numeric tasks khác signal episodes |
| CL125 | [Missingness/transfer](chapters/05_experiments.md#523-coverage-historical-resources-and-missing-sentiment) | DO_DUOC | ED12/ED15/BG16/SYS21; §10.3 | Component verified_articles<3:79; U08 unavailable79;828return differences | Không828label flips, no missing=neutral, không loại fallback để đẹp kết quả |

| CL126 | [B04c/runtime/models](chapters/05_experiments.md#531-runtime-model-identities-and-offline-fitting) | DO_DUOC | ED01/ED17/ED20–ED22/ED07; §10.4 | Python3.13.5, modelaliases, declared0/observed1e-8; outputtoken1024/2048 vs960 | No APIseed/immutable revision; current defaults không thay metadata |
| CL127 | [Fit versus inference](chapters/05_experiments.md#531-runtime-model-identities-and-offline-fitting) | HOP_DONG_TRIEN_KHAI | ED14/ED15/ED22; TR01–TR08 §9.15; §10.4 |9selector fits/51bindings; teacher48tasks/731cycles/student42-3000 reused | Trainingfalse của U06 không nghĩa nevertrained; no LLMfinetune |
| CL128 | [Pairing histories](chapters/05_experiments.md#532-pairing-and-execution-histories) | DO_DUOC | ED19/ED20/ED14/ED22; §10.4 | Component147groups,40order mismatch/9cross-epoch; contextu0/r0–2/topo | Component provider-only override khác U08three-attempt rule; no independent repeats |
| CL129 | [B04d/e slot accounting](chapters/05_experiments.md#533-forecast-response-and-http-accounting) | DO_DUOC | ED03/ED17/ED18/ED08/ED09; §10.4 |375selected;2448slots1290raw1158bypass;1702HTTP=1687active+15retired | HTTP200 khác valid response; upstreamgraph408 không408LLM |
| CL130 | [Telemetry/reserve](chapters/05_experiments.md#533-forecast-response-and-http-accounting) | DO_DUOC | ED08/ED07; §10.4 |4750maxchars,2986930observedtokens,9177UNKNOWNreserve,51accounts/repeat | Tokens khác billing, U09newAPI0 khác U08collection0; no new measurements |

| CL131 | [Component main controls](chapters/05_experiments.md#541-component-main-controls-and-response-interventions) | HOP_DONG_TRIEN_KHAI | ED11/ED20/ES01/ES02; §10.5 | AS/B+7numeric, trainmajority/momentum/logistic/factorvote recipes | Broader numericinputs không bằng toàn LLM reasoning; no new fit |
| CL132 | [Panel interventions](chapters/05_experiments.md#541-component-main-controls-and-response-interventions) | DO_DUOC | ED02/ED05/ED21; §10.5 | Upstream9×3×2, factorial9×3×5, sevencontrasts/donor rankvector | Compact/fullvalue families riêng, interaction không causal synergy |
| CL133 | [23 factor controls](chapters/05_experiments.md#542-separate-factor-selection-and-economic-controls) | DO_DUOC | ED23–ED25/ED27/ES03; §10.5 | fixed/dynamic/noflip/20random,2346actions,51scopes,threshold.1 | Train-only numerical design khác Native selector/LLMablation; keep all seeds |
| CL134 | [Economic controls/scenarios](chapters/05_experiments.md#542-separate-factor-selection-and-economic-controls) | HOP_DONG_TRIEN_KHAI | ED26/ED14, componentfinancial§3.2; §10.5 | CycleLONG/CASH vscontinuoushold price-only;12scenariofixedlabels | Unified excludescontinuous;scenario notcertifiedfills/worstcasebound |
| CL135 | [Context families/bridges](chapters/05_experiments.md#543-context-baseline-families-bridges-and-absent-ablations) | DO_DUOC | ED14/ED07; §10.5 |5extensions×2baselines×2endpoints=20;3bridges;102/3/51support | Fallback retained; Common khácBase; bridgepackage khácisolatedcause |
| CL136 | [Absent ablations](chapters/05_experiments.md#543-context-baseline-families-bridges-and-absent-ablations) | DO_DUOC | ED14/ED07 deferred_panels; §10.5 | Retrieval/prior/MT plannedpanel deferred | Có builder/componentpanel không có unified response; no causalstudent claim |

| CL137 | [Classification definitions](chapters/05_experiments.md#551-classification-support-and-undefined-values) | HOP_DONG_TRIEN_KHAI | ES04/ES06/ES07/ES09; §10.6 | FinalLONG→UP/CASH→DOWN; confusion/Acc/BA/MCC/F1/LONG-rate, NA | Zero-F1 có denominator khác undefined; macroclass khác macrostocks |
| CL138 | [Aggregation/Brier](chapters/05_experiments.md#551-classification-support-and-undefined-values) | HOP_DONG_TRIEN_KHAI | ES04/ES06/ES07/ED07; §10.6 | Component pooled102; contextperrepeat102→mean3; Briersupportedonly/uniqueN | No306independent, no confidence→probability hoặc fill0.5 |
| CL139 | [Net/account estimators](chapters/05_experiments.md#552-net-economics-account-aggregation-and-risk-conventions) | HOP_DONG_TRIEN_KHAI | ES01/ES04–ES06/ED07/ED24/ED30; §10.6 | Multiplicative2sidescost; component51mean; contextmean3repeat/account→mean51; numeric9symbolheadline | Cycle/account/portfolio khác,65entry≠decisionClose/7grossnet flips giữsource |
| CL140 | [NAV/MDD/exposure/turnover](chapters/05_experiments.md#552-net-economics-account-aggregation-and-risk-conventions) | HOP_DONG_TRIEN_KHAI | ES01/ES04/ES06; §10.6 | Initialanchor/EODvscycleMDD;heldvsclose;componentprevNAV/contextinitialturnover | Query-to-exit context khác componententry-to-exit; nofills certification |
| CL141 | [Risk conventions](chapters/05_experiments.md#552-net-economics-account-aggregation-and-risk-conventions) | HOP_DONG_TRIEN_KHAI | ES06/ES07/ES10/ED31; §10.6 | Componentdaily252/popSD/negative-subsetSD; contextcycleunannualized/sampleSD/LPM2 | No sharedSortino denominator; sparsecyclefrequency auditcanNA; noinventannualization |
| CL142 | [Component uncertainty](chapters/05_experiments.md#553-paired-resampling-and-descriptive-uncertainty) | DO_DUOC | ED05/ED25/ED27–ED29/ES07/ES08; §10.6 | Main/panel seed20261102; factorialjoint6986/undefined3014; numericseed0/sign64/Holm23 | Conditionalfinite envelope không context9500rule; no confirmatory symmetry/coverage |
| CL143 | [Context joint band](chapters/05_experiments.md#553-paired-resampling-and-descriptive-uncertainty) | HOP_DONG_TRIEN_KHAI | ES05/ED07; §10.6 | PCG64/seed20261110/L2/10000/20joint, SDddof1/higherquantile/threshold9500 | Wholefamily nullifdegenerate, no dropcolumns/redraw; no calibrated95claim |
| CL144 | [Recorded sensitivity scope](chapters/05_experiments.md#553-paired-resampling-and-descriptive-uncertainty) | DO_DUOC | ED07/ED28/ED29; §10.6 | L1/L3/CORE4/leavefold/leavesymbol; metadata finite counts/indexhash | Fewexposedclusters, no selectnarrowestband or extraindependentcohort |
| CL145 | [Main comparison](chapters/05_experiments.md#561-main-comparison-and-economic-outcomes) | DO_DUOC | ED28/32/33; §10.7 | 102 điểm, 25UP/77DOWN; Full BA52.961%, Base49.714%, chênh+3.247pp; interval[−1.176;8.125]pp | Sáu block exposed; tám interval chính đều chứa0, không xác nhận superiority |
| CL146 | [Confusion/exposure](chapters/05_experiments.md#561-main-comparison-and-economic-outcomes) | DO_DUOC | ED33–35; §10.7 | B05b TP7/FN18 cho cả hai; TN60/55, FP17/22; LONG24/29; exposure lịch khác LONG-rate | Không suy chỉ năm điểm đổi action từ chênh aggregate |
| CL147 | [Economic outcomes](chapters/05_experiments.md#561-main-comparison-and-economic-outcomes) | DO_DUOC | ED33/34; §10.7 | Full−0.797%, Base−0.750%, delta−0.047pp; 51 account means; MDD dương, continuous hold tách riêng | Return âm, fractional reference, không portfolio hoặc chứng nhận fill |
| CL148 | [Stock/block patterns](chapters/05_experiments.md#562-stock-and-temporal-block-patterns) | DO_DUOC | ED35/36; §10.7 | Đủ9mã/6block; VNM và b2025_h1 thiếuUP→BA NA; BHN6điểm/1UP | Các partition chồng nhau; không lọc kết quả xấu hoặc gọi các hàng độc lập |
| CL149 | [Numerical factors](chapters/05_experiments.md#563-separate-numerical-factor-controls) | DO_DUOC | ED24/25; §10.7 | B05d giữ3rule+mean20random, return trung bình9mã; random BA47.738%±5.377pp, tất cả20return âm | Không so mức return với mean51account; không best seed/ensemble hoặc LLM-selector ablation |
| CL150 | [Numeric diagnostics](chapters/05_experiments.md#563-separate-numerical-factor-controls) | DO_DUOC | ED24/25; §10.7 | B05e ba contrast chính trong family23/64signs; zeroHolmreject, intervals chép nguồn | Symmetry/exchangeability chưa xác nhận; không chọn riêng interval loại0 để kết luận |
| CL151 | [Upstream panel](chapters/05_experiments.md#564-upstream-variation-and-alphasentimentplacebo-panel) | DO_DUOC | ED05/37; §10.7 | 9điểm×3execution×2branch=54,18shared; FullBA95.238%/Base90.476%, return+.496%/+.371% | Panel riêng3block, không thay main hoặc tách variance upstream/Decision |
| CL152 | [Factorial outcomes](chapters/05_experiments.md#564-upstream-variation-and-alphasentimentplacebo-panel) | DO_DUOC | ED05/37; §10.7 | 9điểm,8mã,8account/execution; ASBA19.048%<B28.571%<P30.952%; năm branch return âm | Full-value khác compact-alpha; không khẳng định tác dụng thuần alpha/sentiment hoặc placebo causal |
| CL153 | [Seven BA contrasts](chapters/05_experiments.md#564-upstream-variation-and-alphasentimentplacebo-panel) | DO_DUOC | ED29/37; §10.7 | B05g bảy contrast, finite6986/undefined3014, radius27.619pp; cả bảy envelope chứa0 | Joint-finite max-absolute-deviation, không standardized U09 band hoặc calibrated coverage |
| CL154 | [Answer to RQ1](chapters/05_experiments.md#565-bounded-answer-to-rq1) | DAN_XUAT | CL145–CL153; §3 native audit; §10.7 | Full tăng BA nhưng return thấp hơn Base; panel khác support/representation; kết quả adverse giữ nguyên | Native row-wise FAIL/NOT_CERTIFIED/UIpending giữ nguyên; không profitability/causal/generalization claim |

| CL155 | [Context main results](chapters/05_experiments.md#571-overall-results-on-the-complete-cohort) | DO_DUOC | ED07/38; §10.8 | B06a đủ8role+2control, BA mean3repeat, return mean3withinaccount→mean51; return8role đều âm | Không pooled306 hoặc portfolio; CASH0, dailyMDD dương, repeatSD không market uncertainty |
| CL156 | [Context slots/fallback](chapters/05_experiments.md#572-response-coverage-and-retained-fallbacks) | DO_DUOC | ED07/16; §10.8 | B06b 306slot/method, raw+bypass306; nghiên cứu1290raw+1158bypass=2448 | Bypass vẫn ở primary; hai noLLM controls không fallbackCommon |
| CL157 | [All repeats](chapters/05_experiments.md#573-repeat-dispersion-and-secondary-support) | DO_DUOC | ED07/38; §10.8 | B06c đủ30method/repeat, không best run; các return nghiên cứu âm ở cả3repeat | Một upstream/point, baDecisionrepeat không độc lập thị trường |
| CL158 | [Secondary support boundaries](chapters/05_experiments.md#573-repeat-dispersion-and-secondary-support) | DAN_XUAT | ED07/39; §10.8 | Stock/fold/CORE4 thuộc sensitivity, VNM/b2025_h1 BA NA | Không covered-only thay102primary hoặc chọn favorable subset |

| CL159 | [Joint contrast family](chapters/05_experiments.md#574-paired-contrasts-against-both-baselines) | DO_DUOC | ED07; §10.9 | B06d đủ20cell; F09 đủ10returncontrast, pp, cùngscale | Giữ toànfamily20/finite10000; không vẽ equitycurve nốiaccount |
| CL160 | [Baseline-dependent v1 result](chapters/05_experiments.md#574-paired-contrasts-against-both-baselines) | DAN_XUAT | ED07; §10.9 | v1−Common return+.327pp[.067,.586], BA+4.130pp[2.011,6.249]; soNative return−.045/BA−1.749 | Common-based cải thiện không thành vượtNative hoặc cólãi, banddescriptive |
| CL161 | [Adverse contrast outcomes](chapters/05_experiments.md#574-paired-contrasts-against-both-baselines) | DO_DUOC | ED07; §10.9 | MT−Native return−.601pp[−1.090,−.111]; C2/BnativeBAband<0 | Endpoint khác nhau; không chọn riêng family/metric thuận lợi |
| CL162 | [Three bridges](chapters/05_experiments.md#575-descriptive-bridge-to-anchor-and-mt-policy) | DO_DUOC | ED07/16; §10.9 | Common−Native−.372pp/−5.879pp; Anchor−Common−.262/−3.229; MT−Anchor+.033/+.433; same273/273/302of306 | Khôngbridgebandmới hoặc táchcausalstudent/policy |

| CL163 | [Coverage and gates](chapters/05_experiments.md#581-historical-support-and-recorded-context) | DO_DUOC | ED07/16/40; §10.10 | Bank48/OOD54; C2/B READY1, A READY8; insufficient47/40/47; READY không có visible examples | READY khác truy xuất3; reason chồng nhau, primary giữ fallback |
| CL164 | [Recorded age and similarity](chapters/05_experiments.md#581-historical-support-and-recorded-context) | DO_DUOC | ED16/40; §10.10 | v1 có48điểm K3; age median1291.833d/range441.667–2026; similarity median.833/range.5–1 | Tổng hợp trường đã lưu, không retrieval mới; MT age/sim export và regret thiếu giữNA |
| CL165 | [Regime sources](chapters/05_experiments.md#581-historical-support-and-recorded-context) | DO_DUOC | ED40/EX01; §10.10 | v1 active48 regime CONSOLIDATION40/BULL4/CHOPPY4 | Không ánh xạ thành MT HMM regime hoặc hiệu ứng nhân quả regime |
| CL166 | [MT policy counts](chapters/05_experiments.md#582-anchor-relative-revisions-and-probability-outputs) | DO_DUOC | ED07/16; §10.10 | 48feature+60utilitybypass+189same+5reject+4accept=306; final=anchor302 | Flagfalse108bypass không phải108reply sai; eligible66points |
| CL167 | [Direction of utility gate](chapters/05_experiments.md#582-anchor-relative-revisions-and-probability-outputs) | HOP_DONG_TRIEN_KHAI | Chapter4.8.6/BG18; ED16; §10.10 | CASH→LONG Q10U; LONG→CASH −Q90U, strict>0 | Không gọi utility_q10 là deltaquantile cho mọi chiều |
| CL168 | [Probability support](chapters/05_experiments.md#582-anchor-relative-revisions-and-probability-outputs) | DO_DUOC | ED07calibration/ED16; §10.10 | numericBrier.205811/258slot86points, teacher.212024/198slot66points | Support khác không xếp hạng; không LLMconfidencecalibration/studentcausalclaim |

| CL169 | [Case selection](chapters/05_experiments.md#583-traceable-cases-selected-by-the-declared-rule) | DAN_XUAT | §7.7, ED16/40, CT01–CT30; §10.11 | r0,102điểm đủ nguồn; candidates29/47/5/2/52, chọnngày/mãđầu; tieorder công bố | Chỉ nhóm sai dùng outcome; overlap cho phép, không errorrate/causaleffect |
| CL170 | [EX01 support and loss](chapters/05_experiments.md#583-traceable-cases-selected-by-the-declared-rule) | DO_DUOC | EX01/CT; §10.11 | FPT03Jul2023: đủMT/v1 nhưngC2insufficient, rawMTLONG=anchor, gross+.436%→net−.265% | Giữ hai nguồnregime, samebranchkhôngquantiletest; khôngveto giả |
| CL171 | [Accepted losing change](chapters/05_experiments.md#583-traceable-cases-selected-by-the-declared-rule) | DO_DUOC | HVN CT, ED16; §10.11 | HVN01Jul2024: anchorCASH/rawLONG/acceptLONG, Q10delta+.0027822661645950566; net−1.574% | Modelutility không profitguarantee; signalbank khác numericcontext |
| CL172 | [Veto and missed gain](chapters/05_experiments.md#583-traceable-cases-selected-by-the-declared-rule) | DO_DUOC | MWG CT, ED16; §10.11 | MWG20Sep2024: anchorCASH/rawLONG/vetoCASH, Q10delta−.020861640105904133; candidate net+.324% | CASH0 khôngloss; labelerror/missedgain, không policybenefitclaim |
| CL173 | [Native error](chapters/05_experiments.md#583-traceable-cases-selected-by-the-declared-rule) | DO_DUOC | CMG CT, ED16; §10.11 | CMG03Jul2023: NativeSHORT→CASH, candidate net+.171%/UP | Packet là auditview, không Nativeinput tương đươngMT; không actualshort |

| CL174 | [Context sensitivity family](chapters/05_experiments.md#584-sensitivity-to-support-and-dependence-assumptions) | DO_DUOC | ED07; §10.12 | B06f/g đủ5extension×2baseline×return/BA; L1/L3/CORE4 saved20cell/finite10000, LOFO6/LOSO9ranges | Không tạo draw hoặc chọn bandhẹp, range khôngCI |
| CL175 | [Baseline and support sensitivity](chapters/05_experiments.md#584-sensitivity-to-support-and-dependence-assumptions) | DAN_XUAT | ED07; §10.12 | v1−CommonL1return[−.019,.672]khác L2[.067,.586]; CORE4v1−Native+.350[−.024,.725] | Zero-exclusion khôngrobusttoblocklength; subset48/24khácprimary102/51 |
| CL176 | [Component cohorts and dependence](chapters/05_experiments.md#584-sensitivity-to-support-and-dependence-assumptions) | DO_DUOC | ED28/34/35/41/42; §10.12 | Common8 96/48account, recent9 54/27account; returnorderingđổi; LOO BA+.820..4.918pp, CBB/HAC intervals chứa0 | HACaccuracy khácBA, khôngconfirmatory hoặcfinancialgain |
| CL177 | [Component strata](chapters/05_experiments.md#584-sensitivity-to-support-and-dependence-assumptions) | DO_DUOC | ED45/47; §10.12 | Trend35/33/34, volatility33/69, liquidity80/22; B05i giữ adversegroup | Proxy/thresholdpostinference, khácHMMregime; không strategychọnstrata |
| CL178 | [Twelve economic scenarios](chapters/05_experiments.md#585-recorded-economic-execution-scenarios) | DO_DUOC | ED26/43/44; §10.12 | B05j12scenario×AS/B51account, fixedprediction/labels; Base delayedpending1, uncertifiedfills0 | Assumptions không broker/venuequote; nofill không worstcasebound hoặcqueryforesight |
| CL179 | [Recorded resource scopes](chapters/05_experiments.md#586-recorded-resource-use-and-unavailable-costs) | DO_DUOC | ED18/07/46; §10.12 | Component194new/455sourceattempts; context1702HTTP, observed2986930tokens/UNKNOWNreserve9177 | Không cộng thành bill375outputs, reservekhácusage, missingkhác0billed |
| CL180 | [Latency and missing costs](chapters/05_experiments.md#586-recorded-resource-use-and-unavailable-costs) | DAN_XUAT | ED46 và HTTPmembers; §10.12 | 1700timed/2untimed, sum4056.744s/median1.715/range.554–31.819; loại503carry | Timestamp durations khácwallclock/perrolematchedlatency, không monetarybill |

| CL181 | [Unperformed interventions](chapters/05_experiments.md#591-interventions-without-a-completed-matched-result) | DAN_XUAT | ED07deferred/ED05/37; §10.13 | B06h retrieval/prior/MT/no-prior/no-utility/no-target/statistics/student và execution gaps | Builder/offlinetest/separatecomponent không matchedhostedresult |
| CL182 | [Native temporal validity](chapters/05_experiments.md#592-limits-on-causal-statistical-and-external-validity) | DO_DUOC | ED15/07; §10.13 | Native row-wiseFAIL/wholeNOT_CERTIFIED_HISTORICAL_EXPLORATORY | Outerquerycutoff và Commonalpha không chứngnhận toàninheritedpath |
| CL183 | [Bank/query provenance](chapters/05_experiments.md#592-limits-on-causal-statistical-and-external-validity) | DO_DUOC | ED15provider_support.bank_audit; §10.13 | 828/852numericalreturndiff, max.04298848884252138pp, rawsignaljournalsunavailable | Không828changedlabels hoặc tựrelabel; membershiphash không authenticity |
| CL184 | [Sampling and external validity](chapters/05_experiments.md#592-limits-on-causal-statistical-and-external-validity) | DAN_XUAT | ED15qualitylimits/ED04/ED26/ED44; §10.13 | Exposedfolds, unknownservedrevision, purposive9stocks, news/content/corporateaction/venuefill giới hạn | Khôngprospectiveholdout, authenticatedmarketcapacity hoặc liveprofitability |
| CL185 | [Dependence and confounding](chapters/05_experiments.md#592-limits-on-causal-statistical-and-external-validity) | DAN_XUAT | CL126–CL144/CL174–177; §10.13 | Sixclusters, oneupstream/contextpoint, promptprofile/ordermismatches40/epochs9, L1band sensitivity | Khôngcalibratedcoverage/power hoặc pooledstudy/causaleffect |
| CL186 | [Acceptance scope](chapters/05_experiments.md#592-limits-on-causal-statistical-and-external-validity) | DO_DUOC | ED08/15/07; snapshotcoldreceipt§3.4; §10.13 | U08pins718/maxprompt4750/maxattempt3/suite_rerunFalse; historicalcoldreplay/0inference | Không gatechạymới, futurehostedidenticalresponse hoặc đóng F11/UI/externalreview |
| CL187 | [RQ synthesis](chapters/05_experiments.md#593-supported-answers-to-the-research-questions) | DAN_XUAT | CL145–CL186; §10.13 | B09 đủRQ1–4 vớiobservation/answer/remainingevidence | P4đủbảnnháp, khôngG3toànbộ/T48–58 hoặcnghiêncứu/phảnbiệnngoàiđãxong |

| CL188 | [Bibliography và phạm vi nguồn](references.bib) | NGUON_HOC_THUAT | R01–R22; §11.1 | 22 mục có metadata/version/đoạn hỗ trợ, tách discovery register và bibliography | Không 62 nguồn đều đã đọc; không suy paper method thành hiệu quả hệ thống hoặc nguồn chưa đọc thành citation hợp lệ |

| CL189 | [Technical analysis as empirical hypothesis](chapters/02_related_work.md#21-technical-analysis-and-quantitative-stock-prediction) | NGUON_HOC_THUAT | R01/lo2000technical; §11.1–§11.2 | Pattern recognition và conditional return distributions là hướng kiểm tra thực nghiệm | Không suy mọi indicator/market adaptation sinh lời |
| CL190 | [Formula operators and adaptation](chapters/02_related_work.md#21-technical-analysis-and-quantitative-stock-prediction) | NGUON_HOC_THUAT | R02/kakushadze2016formulaic AppendixA; CL043–CL047 | Cross-sectional rank/group neutralization khác temporal operators; single-asset và typical-price proxy là thích nghi | Không gọi registry hiện tại tương đương nguyên xi101alpha hoặc VWAP thật |
| CL191 | [Quantitative controls](chapters/02_related_work.md#21-technical-analysis-and-quantitative-stock-prediction) | DAN_XUAT | R03/pedregosa2011sklearn; CL131–CL136 | Thư viện cung cấp môi trường; recipe/controls của nghiên cứu lấy từ artifacts | Không gán hyperparameter hay hiệu quả study cho paper thư viện |
| CL192 | [Selection versus independent assessment](chapters/02_related_work.md#21-technical-analysis-and-quantitative-stock-prediction) | NGUON_HOC_THUAT | R17/varma2006bias; CL149–CL150 | Optimized CV score có thể lạc quan; numerical factor rules khác LLM-selector ablation | Không áp kết quả microarray thành theorem về mọi time-series split |

| CL193 | [QuantAgent method attribution](chapters/02_related_work.md#22-llms-vlms-and-multi-agent-financial-systems) | NGUON_HOC_THUAT | R04/xiong2025quantagent §3–4; §11.3 | Price-derived specialists, Risk và Decision tách vai trò; benchmark1h/4h | Không chuyển HFT/title hoặc kết quả gốc sang study dailyLONG/CASH |
| CL194 | [Code inheritance and integration](chapters/02_related_work.md#22-llms-vlms-and-multi-agent-financial-systems) | HOP_DONG_TRIEN_KHAI | R05/yresearch2026quantagentcode, THIRD_PARTY_NOTICES, CL025–CL050 | Pin92519f8 là comparison; agent/tools/graph/UI kế thừa, alpha/news/context/policy/evaluator bổ sung | Adopted commit unknown; không nhận VLM/đaagent là mới hoặc blanketlicense |
| CL195 | [TradingAgents and FinVision](chapters/02_related_work.md#22-llms-vlms-and-multi-agent-financial-systems) | NGUON_HOC_THUAT | R06–R07; §11.3 | Team/debate/structured communication và news/chart/reflection là cơ chế liên quan | Không head-to-head cùng dữ liệu/economics; reflection khác Bayesian posterior |
| CL196 | [Visual understanding boundary](chapters/02_related_work.md#22-llms-vlms-and-multi-agent-financial-systems) | NGUON_HOC_THUAT | R08/han2023chartllama §3/4.2 | Chart understanding có data/tasks/evaluation riêng | Không dùng ChartLlama weights hoặc coi chartQA là finance/trading validation |
| CL197 | [Vietnamese sentiment resources](chapters/02_related_work.md#22-llms-vlms-and-multi-agent-financial-systems) | NGUON_HOC_THUAT | R09/R10; CL048–CL050 | ViSoBERT backbone khác classifier5CD/3label, financial-domain validity chưa có | Không dùng card score thành accuracy/calibration/PIT certificate |

| CL198 | [Regime-switching model](chapters/02_related_work.md#23-market-regime-detection) | NGUON_HOC_THUAT | R11/R12; §11.4 | Latent transitions/emissions và kinh tế thay đổi theo state; fitting khác inference | Không xác nhận state tài chính thật hay strategy sinh lời |
| CL199 | [Regime information set and implementation](chapters/02_related_work.md#23-market-regime-detection) | DAN_XUAT | Rabiner§III, CL061–CL063/CL165/CL177 | Forward/backward thông tin khác, frozen resource/prefix và regime nguồn riêng cần định danh | Endpoint cutoff không tự sửa mọi row-wise feature hoặc NativeFAIL |
| CL200 | [Implicit Bayes assumptions](chapters/02_related_work.md#24-in-context-learning-and-bayesian-historical-context) | NGUON_HOC_THUAT | R13/xie2022implicitbayes §2–§4 | Mixture-of-HMMs/latent concept giải thích ICL trong setting có giả định | HMM sinh văn bản khác HMM VN-Index; không arbitraryprompt Bayes certificate |
| CL201 | [Learned retrieval and implemented priors](chapters/02_related_work.md#24-in-context-learning-and-bayesian-historical-context) | NGUON_HOC_THUAT | R14/rubin2022retrieve; CL064–CL075 | Learned dense prompt retrieval khác heuristic; v1 empirical rates/C2Beta/structured tasks khác cơ chế | B_semantic không mặc nhiên là dense retriever, no posterior từ tên hoặc fewshot |
| CL202 | [PFN objective](chapters/02_related_work.md#25-multi-task-bayesian-icl-and-studentteacher-methods) | NGUON_HOC_THUAT | R15/muller2022transformers §3–§4 | Dataset sampled from prior, prior-data NLL, amortized predictive mapping | Không gán PFN guarantees cho LLM bất kỳ hoặc weights thesis |
| CL203 | [MT-BICL source method](chapters/02_related_work.md#25-multi-task-bayesian-icl-and-studentteacher-methods) | NGUON_HOC_THUAT | R16/zhu2026multitask §4/5.1/AppC | Prior datasets/target observations/query tách task; paperobjective target likelihood và synthetic8layer8head | Không đồng nhất nhiềuexamples thành MT hoặc sourcepaper thành stocktradingevidence |
| CL204 | [Actual teacher/student and policy differences](chapters/02_related_work.md#25-multi-task-bayesian-icl-and-studentteacher-methods) | HOP_DONG_TRIEN_KHAI | CL078–CL101; §4.8 và §11.4 | LocalBeta16teacher/counts, syntheticsoftquerydistillation, features independent syntheticlabels, student2block4head, hostedproposal/policy tách | Replica label không exactreplication; syntheticagreement không calibration/causalstudentbenefit |

| CL205 | [Backtesting and selection](chapters/02_related_work.md#26-evaluation-of-trading-systems-using-llms) | NGUON_HOC_THUAT | R17/R18/R22; §11.5 | Development/selection/assessment, implementation shortfall và data reuse cần phân biệt | Không nói đã chạy White Reality Check/nestedCV hoặc có deploymentprofitability |
| CL206 | [Temporal, paired and ablation contracts](chapters/02_related_work.md#26-evaluation-of-trading-systems-using-llms) | HOP_DONG_TRIEN_KHAI | CL021–CL024/CL126–CL144 | Label maturity/holdinginterval, shared upstream và matched interventions là hợp đồng cụ thể | Pairing không tách causal effect khi projection/information cùng đổi; repeat không newmarketdata |
| CL207 | [Dependence methods and assumptions](chapters/02_related_work.md#26-evaluation-of-trading-systems-using-llms) | NGUON_HOC_THUAT | R19/R21; §11.5 | Stationary bootstrap randomlength và HAC có giả định; fixedcircular/fold của thesis khác | Không chuyển asymptotic motivation thành nominalcoverage sáu exposedfolds |
| CL208 | [Multiplicity and valid tests](chapters/02_related_work.md#26-evaluation-of-trading-systems-using-llms) | NGUON_HOC_THUAT | R20/Holm pp65–67; CL142–CL144/CL150 | Sequential adjustment cần validindividualtests; giữ family đầy đủ và undefined rules | Holm không sửa symmetry/exchangeability chưa kiểm hoặc xác nhận exploratory |
| CL209 | [Reproducibility versus confirmation](chapters/02_related_work.md#26-evaluation-of-trading-systems-using-llms) | DAN_XUAT | R22, CL179–CL186; §11.5 | Source/input/prompt/reply/checkpoint/offlinereplay khác freshhostedinference/prospective/livefills | Không suy authenticity, wholecausal hoặcprofit từhash/fluentexplanation/replay |

| CL210 | [Financial-agent comparison](chapters/02_related_work.md#27-research-gap-and-position-of-the-thesis) | DAN_XUAT | B08a/R04/R06/R07, Chapters4–5; §11.6 | Inputs, roles/history, temporal protocol/economics được so theo đúngversion/đoạn | Không xếp hạng khácstudy, authorstatement khác independentPIT/venueaudit |
| CL211 | [Context/inference comparison](chapters/02_related_work.md#27-research-gap-and-position-of-the-thesis) | DAN_XUAT | B08b/R13–R16 và CL064–CL101; §11.6 | Contextunit/prior/learner/domain tách implicitBayes/retrieval/PFN/MT và localpath | Không synonymfewshot=MT, không coi validationdomain của paper là tradingevidence |
| CL212 | [Bounded contribution](chapters/02_related_work.md#27-research-gap-and-position-of-the-thesis) | DAN_XUAT | CL025–CL028/CL064–CL101/CL145–CL187; §11.6 | Source-bound integration, context/fallback, teacher/student, policy và pairedaccounting | Không globalfirst/noveltheorem/firstvisualmultiagent hoặc returnadvantage |
| CL213 | [Remaining research gap](chapters/02_related_work.md#27-research-gap-and-position-of-the-thesis) | DAN_XUAT | CL155–CL187/CL198–CL209; §11.6 | Baseline/readiness dependent, MTmostlyanchor, eightnegative means, NativeFAIL vàmissingmatchedablations | Gap về reliablevalue chưa được giải quyết bằng implementation; G3/T54–58 vẫn còn |

| CL214 | [Motivation](chapters/01_introduction.md#11-context-and-motivation) | DAN_XUAT | R01/R02/R04/R16/R22, §11.1; §§2.1–2.7 | Price/chart/news roles, completed context and distinct multi-task/multi-agent meanings motivate a controlled question | No assumed return advantage, new foundational invention or market-rule claim |
| CL215 | [Decision problem](chapters/01_introduction.md#12-problem-statement) | DAN_XUAT | CL025–CL034/CL104–CL117; §§3.1–3.2/4.7–4.10 | Available input, mature history, proposal/fallback/action and shared economic labels match existing method | Intended cutoff is not Native row-wise causal certification; SHORT means CASH |
| CL216 | [Input/output schematic and evaluation](chapters/01_introduction.md#12-problem-statement) | DAN_XUAT | F01/F02/F03/F07, CL112–CL117; §12.1 | Inline English Mermaid separates forecasting from future-price evaluation | No new empirical figure/data, independent observation, portfolio or live-fill claim |

| CL217 | [RQ objectives and evidence map](chapters/01_introduction.md#13-objectives-and-research-questions) | DAN_XUAT | Outline §A.2; B09/CL187; §12.2 | Four questions copied verbatim, compared on distinct study/control/support identities | Audit RQ4 is not a performance contrast; no assumed advantage |
| CL218 | [Challenges and scope](chapters/01_introduction.md#14-challenges-and-boundaries) | DAN_XUAT | CL181–CL186; §§5.1/5.9 | Nonstationarity, coverage, exposed dependence, provenance, hosted scope and UI limits retained | 2448 slots are not independent observations; Native FAIL/NOT_CERTIFIED/UI PENDING |
| CL219 | [Contribution attribution](chapters/01_introduction.md#15-contributions-and-thesis-organization) | DAN_XUAT | Outline §A.4; CL198–CL213; Chapters4–5; §12.2 | Four contribution types bind implementation to evidence and inherited foundations | No foundational invention, MT-specific isolated gain or prospective advantage |
| CL220 | [Six-chapter argument](chapters/01_introduction.md#15-contributions-and-thesis-organization) | DAN_XUAT | Outline §A.5; six chapter sources; §12.2 | Questions lead through literature/concepts/method to two studies and bounded answers | Unperformed work is future work, not a completed intervention |

| CL221 | [Approach summary](chapters/06_conclusion.md#61-summary-of-the-approach) | DAN_XUAT | Chapters2–4; CL214–CL220; §12.3 | Current evidence, completed history, regimes, numeric MT and final policy reconnect to common accounting | Implementation/inherited foundation does not prove effectiveness or causality |
| CL222 | [Answer RQ1](chapters/06_conclusion.md#621-rq1-combined-information-and-controls) | DAN_XUAT | B05a–b/CL145–CL154; §5.6; §12.3 | BA +3.247 pp with descriptive interval crossing zero, return −0.047 pp, controls/panels retained | No generalized information/selector gain or profitability |
| CL223 | [Answer RQ2](chapters/06_conclusion.md#622-rq2-historical-context-and-conditional-evidence) | DAN_XUAT | ED07/B06a–d, CL155–CL161/CL174; §§5.7/5.8.4; §12.3 | v1 versus Common +0.327 pp but versus Native −0.045 pp; L1 band crosses zero, C2/B sparse, all eight negative means | No isolated regime causal effect, confirmatory superiority or favorable subset substitution |
| CL224 | [Answer RQ3](chapters/06_conclusion.md#623-rq3-factual-anchoring-mt-inference-and-utility) | DAN_XUAT | ED07/B06e, CL162–CL168/CL181; §§5.7.5/5.8.2; §12.3 | 302/306 same final actions; 108+189+5+4 decomposition, four accepted slots/three points, +0.033 pp bridge | No separate student/context/utility attribution or new bridge band |
| CL225 | [Answer RQ4](chapters/06_conclusion.md#624-rq4-temporal-economic-and-operational-evidence) | DAN_XUAT | CL119–CL120/CL179–CL187; source-scoped receipts; §12.3 | Specific economic/paired/operational contracts coexist with unresolved temporal/provenance/execution/UI limits | Native FAIL, whole-system NOT_CERTIFIED_HISTORICAL_EXPLORATORY, UI/F11 PENDING unchanged |
| CL226 | [Contribution synthesis](chapters/06_conclusion.md#62-answers-and-contributions) | DAN_XUAT | §1.5/outline §A.4; CL219/CL221–CL225; §12.3 | Four contribution types survive at the same mechanism/evidence strength as introduction | No new result, theory, trading advantage or external acceptance |

| CL227 | [Validity limitations](chapters/06_conclusion.md#63-limitations) | DAN_XUAT | CL174–CL186; §5.9.2; §12.4 | Row-wise failure, source provenance, small dependent exposed support and hosted uncertainty preserved | 828/852 return differences are not changed labels; hashes do not authenticate original signals |
| CL228 | [Mechanism and deployment limits](chapters/06_conclusion.md#63-limitations) | DAN_XUAT | CL155–CL173/CL178/CL181/CL186; §§5.8–5.9; §12.4 | Coverage/fallback and combined interventions limit attribution; daily bars/scenarios/UI do not certify live deployment | No isolated student/utility benefit, guaranteed worst-case bounds or portfolio/live-fill certification |
| CL229 | [Priorities: causality, coverage, attribution](chapters/06_conclusion.md#64-future-work) | DAN_XUAT | B06h/B09; CL181–CL187/CL227–CL228; §12.4 | Separately versioned repairs then authenticated context and registered matched interventions address missing evidence | Proposed checks/experiments are not run; frozen historical failure/results not overwritten |
| CL230 | [Priorities: unexposed evaluation and deployment](chapters/06_conclusion.md#64-future-work) | DAN_XUAT | CL174–CL187/CL227–CL228; §12.4 | Fixed unexposed protocol, dependence-aware precision and venue/portfolio/UI validation have distinct evidence requirements | Future UI acceptance alone cannot establish prospective execution/profitability |

| CL231 | [Cross-chapter argument](chapters/01_introduction.md#13-objectives-and-research-questions) | DAN_XUAT | Outline §A; §§1.1–1.5/2.7/3.2/3.6–3.7/4.1/4.5–4.10/5.1/5.6–5.9/6.1–6.4; §12.5 | Same title direction, four verbatim RQs, four contribution types, action/label/context meanings and study boundaries form one traceable chain | Editorial consistency is not independent scientific review, causal certification or final typesetting |
| CL232 | [G3 internal self-review scope](plan.md#7-các-mốc-rà-soát) | DAN_XUAT | T36–T58 outputs, CL117–CL231; §12.5 | Results/literature/RQs/conclusions align within existing sources; future studies remain proposed and historical failures retained | No external acceptance, whole-system runtime rerun, deployment certification or finished thesis claim |

| CL233 | [Abstract: problem and approach](frontmatter.md#abstract) | DAN_XUAT | §§1.1–1.5/4.1/4.5–4.9/6.1; CL214–CL221; §13.1 | Source-bound agent/context/MT/policy synthesis, proposal differs from final action | No new foundational invention or assumed benefit |
| CL234 | [Abstract: design](frontmatter.md#abstract) | DAN_XUAT | §§5.1–5.5; CL117–CL144/CL218; §13.1 | 102 points, nine stocks, six exposed blocks/folds, 51 accounts; context eight roles/three repeats/2448 dependent slots | Two response collections/estimators distinct; account mean is not a shared-capital portfolio |
| CL235 | [Abstract: principal results](frontmatter.md#abstract) | DAN_XUAT | B05a–b/B06a–e/B07c/B09; CL222–CL224; §13.1 | Full−Base BA +3.247 pp/return −0.047 pp; v1−Common +0.327 pp but v1−Native −0.045 pp; 302/306 MT/anchor actions agree; all eight means negative | Descriptive, support/baseline/dependence qualified; no isolated student/utility effect |
| CL236 | [Abstract limits and keywords](frontmatter.md#abstract) | DAN_XUAT | §§1.4/5.9/6.2–6.4; CL225–CL230; §13.1 | Causal failure and provenance/execution/application limits retained; seven indexing terms describe the research subject | No prospective profitability, whole-system causal certificate or application acceptance |

| CL237 | [Front-matter identity](frontmatter.md#cover-metadata) | DAN_XUAT | User brief/reply and evidence §1; frontmatter/covers at e6e1e1a4; §13.2 | Institution/title/author/23020346/major/supervisor/place-year unchanged; covers retain existing layout | No new submission date, program code, signature, approval or official prescribed wording |
| CL238 | [Acknowledgements and declaration draft](frontmatter.md#declaration) | DAN_XUAT | User-provided supervisor and subsequent wording confirmation; manuscript/source attribution and actual drafting process; §§1/13.2–13.3 | Minimal thanks and declaration wording confirmed by author; attribution/scope/editorial AI assistance retained; signature/date pending | Text is not a signed or institution-approved declaration; no sole-authorship, never-submitted, funding or endorsement assertion |
| CL239 | [Abbreviations](frontmatter.md#list-of-abbreviations) | DAN_XUAT | Outline Front matter; evidence §5; Chapters2–5 terminology; §13.2 | 42 abbreviations/metric labels expanded consistently with body, including required 12 terms | Named methods/IDs are not silently redefined as general algorithms or certified properties |
| CL240 | [Notation](frontmatter.md#list-of-symbols) | DAN_XUAT | Evidence §5.3; §§3.1–3.7/4.5–4.8/5.5; §13.2 | 26 controlled-notation rows with units; local symbol overloads and teacher/component roles explicit | Examples/tasks/support, percent/pp, probability/confidence/utility remain distinct |
| CL241 | [Reading conventions](frontmatter.md#reading-conventions) | DAN_XUAT | Evidence §5.1–5.5; §§1.2/3.2/3.7/4.9/5.1/5.5/5.9; §13.2 | Study/profile names, proposal/action/target, missingness and validity scopes align with six chapters | No portfolio, short sale, row-wise causal certificate, input authenticity or live/UI acceptance claim |

| CL242 | [A.1 shared identity/schema](archive/p8-source.zip) | DAN_XUAT | Frozen unified_contracts/BG16–18/SYS44–47; EX01 shared member; §13.4 | Whitelist/forbidden fields, point/provenance/version and exact identity projection | Causal version string is not a whole-system causal certificate |
| CL243 | [A.2 historical schemas/example](archive/p8-source.zip) | DAN_XUAT | Frozen historical-task-record:1, memory member FPT:2022-04-07, MT contracts; §13.4 | CORE4 enum, required field groups and complete stored episode; numerical tasks distinct | JSON schema alone does not enforce maturity/economics or nine-stock coverage |
| CL244 | [A.3 timeline/label](archive/p8-source.zip) | DAN_XUAT | CL001–CL007/CL021–CL024/CL115; canonical oracle/EX01 dates; §13.4 | Cutoff/availability/maturity/barrier, t+1/t+3, per-leg costs and fraction/percent label meanings | No law/live-fill/portfolio claim or query outcome in shared input |
| CL245 | [A.4 absence and failure](archive/p8-source.zip) | DAN_XUAT | CL029–CL031/CL104–CL114; §§3.7/4.2/4.9; §13.4 | Unavailable/undefined/zero, fallback/bypass/technical failure and primitive finite JSON remain distinct | Local contract checks preserve Native FAIL/NOT_CERTIFIED |

| CL246 | [B.1 request families/identities](archive/p8-source.zip) | DAN_XUAT | EX01 r0 Common/v1/anchor/MT prepare/forecast members; §13.5 | Original UUIDs, request hashes and exact one-message character counts bind four examples | Translations/redactions are not original wire bytes or new calls |
| CL247 | [B.2/B.3 translated instructions and BRPP](archive/p8-source.zip) | DAN_XUAT | EX01 v1 message substring and frozen anchored builder; §13.5 | Counts, examples, original BRPP length and English presentation legend/instructions preserve source meaning | Translation length does not establish budget; legacy settlement wording is not verified law |
| CL248 | [B.4 schema and reply projection](archive/p8-source.zip) | DAN_XUAT | Frozen TradeDecisionOutput/utility_icl_reply_v3; EX01 MT reply cc6bf729-784a-458a-8e40-07398fac513f; §13.5 | Base seven fields, extended fact/context fields and exact machine-field projection; categorical confidence and prose translation labeled | No calibrated confidence, full-schema claim for a projection or measured C3 ablation |
| CL249 | [B.5 budgets/repair](archive/p8-source.zip) | DAN_XUAT | CL106–CL110/CL179–CL180; frozen cap/repair and U08 wire audit; §13.5 | Report/prefix/fact/anchor/final caps separated from observed prompt lengths and transport attempts | Character limits are not tokens; no new measured hosted behavior |

| CL250 | [C.1/C.2 runtime and signals](archive/p8-source.zip) | DAN_XUAT | B04c/ED runtime; SYS03/BG02–03; §§3.3/4.3; §13.6 | Study-specific aliases/options/caps; five indicator settings, Native/Common/factor-control distinctions | Not current-provider guidance, full Alpha101 replication or matched selector ablation |
| CL251 | [C.3/C.4 regimes and priors](archive/p8-source.zip) | DAN_XUAT | BG04–07/RG01–02; §§4.5–4.7; §13.6 | Actual 2022/2020 resources, HMM fit/quality settings, C2/A/B counts/shrinkage/selection/readiness | Generic fit bounds do not override artifacts; no calibrated regime/query probability |
| CL252 | [C.5 context and model recipe](archive/p8-source.zip) | DAN_XUAT | BG08–12/TR01–TR08; §§4.8.2–4.8.3; §13.6 | Frozen feature/task/teacher/student recipe, 271873 parameters, three training seeds but selected seed42/step3000 | Not 69-token pilot or ensemble; 2021 selection uses labels, no new training |
| CL253 | [C.6 utility and policy](archive/p8-source.zip) | DAN_XUAT | BG13–14/SYS33; §§4.8.4–4.8.6; §13.6 | Support, 4096 draws, Exp magnitude weights, teacher sign and strict anchor-relative quantile tests | Not student-probability substitution, repeat-independent market evidence or profit guarantee |

| CL254 | [D.1/D.2 component extensions](archive/p8-source.zip) | DAN_XUAT | final_baselines pinned classification.csv cohort=all_102 AS/B; archived panels.by_execution; §13.7 | 30 stock/block rows and 21 nine-unit panel execution rows preserve source support/confusions | Separate small panels are not 102-point ablations or independent market samples |
| CL255 | [D.3/D.4 stock/fold grids](archive/p8-source.zip) | DAN_XUAT | U09 classification_by_group.csv and accounts.csv; method/group/repeat keys; §13.7 | 90 stock and 60 fold rows; three-repeat class metrics and account-first aggregation; NA retained | Financial weighted reconciliation does not authorize weighted group BA or portfolio claims |
| CL256 | [D.5 repeat results](archive/p8-source.zip) | DAN_XUAT | U09 classification_by_repeat.csv/per_repeat.csv all30 rows; §13.7 | TP/FN/TN/FP, BA/MCC, return and unannualized risk ratios copied, global means reconcile | No independent-upstream or interchangeable component-risk convention claim |
| CL257 | [D.6 complete sensitivity](archive/p8-source.zip) | DAN_XUAT | ED07 contrasts/sensitivity exact identity order; §13.7 | All20 L1/L2/L3/CORE4 cells and 300 saved omission point values retained | Descriptive, support-changing, no new interval or favorable selection |
| CL258 | [D.7 execution extension](archive/p8-source.zip) | DAN_XUAT | ED43 scenario_summary.csv all12 scenarios AS/B; §13.7 | 24 display rows of120 archived scenario-method rows; denominators and within-method reference delta explicit | No certified fills, best/worst-case guarantees or changed canonical predictions/labels |

| CL259 | [E.1 verification scope](archive/p8-source.zip) | DAN_XUAT | Archived final_contracts target/indicator/report, U08/U09 receipts and frozen contracts; §13.8 | Local economic/PIT/paired/prompt/recovery checks have distinct support and validity limits | Audit PASS is not whole-system causality or deployment certification |
| CL260 | [E.2 retained Native failures](archive/p8-source.zip) | DAN_XUAT | alpha_contract_v1 leakage/summary/cases/manifest; exact paths/hashes §13.8 | Recorded prefix-extension vectors and bfill/global-volume flags coexist with outer-cutoff PASS | Synthetic stored outputs, not rerun audits or proof of outer-test future access |
| CL261 | [E.3 provenance/adverse cases](archive/p8-source.zip) | DAN_XUAT | ED15 bank_audit/quality limits, EX01, CL182–CL186; §13.8 | 828/852 return differences, missing journals/news provenance and negative/bypassed cases retained | Not 828 changed labels or a repaired causal study |
| CL262 | [E.4/E.5 receipts and missing acceptance](archive/p8-source.zip) | DAN_XUAT | ED08 prior_checks/ED09, U09 cold record, AP16/AP17; §13.8 | Historical reused test groups, 15 cold artifacts and pending browser scope explicitly separated | No new suite/replay, full gate rerun, missing ablation or UI/financial acceptance claim |

| CL263 | [F.1 inputs/resources](archive/p8-source.zip) | DAN_XUAT | §3.2–3.4/RG/TR/U08/U09 pins and source gate; §13.9 | Actual package sizes/hashes, archives/resource/checkpoint identities and separate source commits | Current source, restored paths and immutable hosted weights are not conflated |
| CL264 | [F.2/F.3 offline commands](archive/p8-source.zip) | DAN_XUAT | Inspected CLI parsers/revision archive/analysis runtime; source CSV columns; §13.9 | Real positional release/destination semantics, stdlib member read, U06 hydration and historical U09 cold verify | Commands not run; cold statistical regeneration differs from byte reading, hosted calls or new training |
| CL265 | [F.4 prerequisites](archive/p8-source.zip) | DAN_XUAT | B04c/recorded runtime107 packages, TR01 inference CPU and local asset prerequisites; §13.9 | Resource levels and platform/cached dependencies named without new minimum runtime/GPU/bill assumptions | No current vendor availability, universal platform reproducibility or unmeasured cost guarantee |
| CL266 | [F.5 application workflow](archive/p8-source.zip) | DAN_XUAT | AP01–AP17/§4.10.4/current web and fixture entrypoints; §13.9 | Mock loopback fixture differs from actual Realtime1D capture/job/dependencies/provisional data/views | UI remains pending; no fixture-to-live financial or browser certification |

| CL267 | [LaTeX foundation](latex/README.md) | DAN_XUAT | Frontmatter/cover brief; existing covers.tex; LuaLaTeX/Biber build logs; §14.1 | Clean report/A4/12pt framework, local assets/bibliography, Roman/Arabic numbering hooks and source-only build command | Observed sample conventions are not official rules; no new runtime or submission acceptance |

| CL268 | [Methods in LaTeX](latex/chapters/04_proposed_system.tex) | DAN_XUAT | Markdown Chapters3–4 at e4e31daf, 10 existing vector figure assets, migration math/table QA and PDF build; §14.2 | 84 headings, 29 tables/139 data rows, 28 display equations and three pseudocode algorithms transferred | Typesetting edits preserve operands/values; partial-build cross-references to later chapters are resolved at integration |

| CL269 | [Results in LaTeX](latex/chapters/05_experiments.tex) | DAN_XUAT | Source-checked Chapter5 at e4e31daf; F09/F10 PDF assets; migration row/numeric/math QA; §14.3 | 43 headings, 37 tables/254 data rows, 8 display equations and 2 vector plots transferred | Same recorded endpoints, pp/% units, NA/support and adverse findings; no recomputation |

| CL270 | [Front matter and literature](latex/frontmatter/content.tex) | DAN_XUAT | Confirmed frontmatter and Chapters1/2/6, bibliography22 entries; Biber log; §14.4 | Acknowledgements/declaration/abstract/7 keywords,42 abbreviations/26 notation rows, three chapters and auto lists/citations transferred | Declaration unsigned; editorial status notes excluded without inventing official approval; sources attributed |

| CL271 | [Appendices in LaTeX](archive/p8-source.zip) | DAN_XUAT | Appendices A–F at e4e31daf; full migration row/numeric/math QA; PDF build; §14.5 | Six appendices,32 tables/479 data rows,5 display equations,stored JSON/prompt/command examples and cross-references transferred | Same support and original UUID/values; long code wraps without new execution or translated-wire claim |

| CL272 | [Integrated LaTeX source](latex/main.tex); [cutover map](latex/source-map.json); [PDF](release/thesis.pdf) | DAN_XUAT | 13 archival Markdown files at e4e31daf; strict dependency/hash check; isolated LuaLaTeX/Biber build; migration and PDF QA; §14.6 | Six chapters and six appendices appear once; 259-page P8 draft; LaTeX became the source of record at 2026-11-16T13:14:55+07:00 | Technical integration only; P9/P10, official institutional requirements and UI acceptance remain open; historical FAIL/NOT_CERTIFIED are retained |

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
| SYS43 | `core/mt_bicl_context.py` | `cf61434f719b43fb908711fd17972fe33ef6db3c3031df2f69671980f0e38c1e` | Live đồng nhất byte |
| SYS44 | `core/variant_registry.py` | `30067f05c3b59c8fc3a44bdc3cd55f9adeb3796b21ee2b39c129355781938ae8` | Live đồng nhất byte |
| SYS45 | `core/unified_protocol.py` | `5ae2bf413afc257c49c441517e828337e9cc7a41fdf0d9974cf9d29b9a302109` | Live đồng nhất byte |
| SYS46 | `core/unified_live/execution.py` | `2bc419ccada9b67810201a78b462a9b93c85d57f13a3d43bd4c8957ccc66272c` | Live đồng nhất byte |
| SYS47 | `core/unified_experiment.py` | `a4f2e2859ba4a32a3c6961cfd9c430f5d4b7594e4226d4872e94f18a6b450cd0` | Live đồng nhất byte |
| SYS48 | `core/unified_execution_transport.py` | `ec170ced17bdfc8595ac0df3aea3f1384f9b1372ccf22850db5eded02120faf2` | Live đồng nhất byte |
| SYS49 | `core/research_invocation.py` | `0f49ca85d0c17ae8d65f8cf78bd469bc612af992d47e1814871fc477c860d18e` | Live đồng nhất byte |
| SYS50 | `core/unified_execution.py` | `e3e415d1af3a0bb4a9caddf49bbb629fd69a57f9cf623923ad64409591663708` | Live đồng nhất byte |
| SYS51 | `core/historical_evaluation_journal.py` | `9791555e200032532ff22f0a51ae7c9e4fae643b178c58dcc4f08ffdbd206f17` | Live đồng nhất byte |
| SYS52 | `core/mt_bicl_prompt_limits.py` | `588d801af508201bf5ee93f390516aed2ac06a30a09057487ebaba2da55f0003` | Live đồng nhất byte |
| SYS53 | `core/unified_model_quota/policy.py` | `f81b6e7eb4416ca2bda83ef7765b506a3a2d19cb4f21dfe21e36735a9cfb03ad` | Live đồng nhất byte |
| SYS54 | `core/unified_provider_quota/policy.py` | `8a6ac44b255b65ec38a3a68249c1b0fe2a5743e962d135fa714777e65dd9a80c` | Live đồng nhất byte |
| SYS55 | `core/unified_point_restart/wire.py` | `2510bedc81e662940777e1860a00c6ab819ebd33433e0deab58fd4b2e2c1cf6f` | Live đồng nhất byte |
| SYS56 | `core/unified_point_restart/runtime.py` | `9ec9e84a3526107c19efbc304334a4c0a0907e01ff22900f99845889f4d78c1e` | Live đồng nhất byte |
| SYS57 | `core/unified_slot_restart/runtime.py` | `0ae30e3d4ce97f6e3f28cd9805c928531dc546a067b4c20106529638fca89b83` | Live đồng nhất byte |
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

### 9.17. Utility, policy và trace hành động

T31; CL093–CL097 dùng BG11/BG13/BG14/BG18/SYS33 đã khóa.
Wire U08 EX01 MT có K3/m3, 5 gain/9 loss, 4096 draw; source
TEACHER_SIGN_BAYESIAN_BOOTSTRAP_MAGNITUDE. Mean/MC/Q10/Q90 chép đúng §7.5
và wire; MC mean = −0.006077377243185831. Draw hash
`d48fa67a94dd615f360d57051dfd47e4cdbcb2f2f25a52ae64010006ef755a0e` là giá trị
đã lưu, không tái tạo draw để viết. EX01 raw/anchor/final LONG,
KEEP_PROPOSED_SAME, delta quantile null; không diễn giải mean âm thành veto.
Bốn hàng giả định kiểm arithmetic và dấu strict, không gọi policy/LLM.
F07 một trang 180×183 mm, render/xem PNG 2000px, kiểm font/bbox/log/hash.
Không thay code/schema/runtime/input; không chạy compileall/unit/E2E/leakage,
API, sampling, model forward hoặc đánh giá lại nghiên cứu.

Hash sản phẩm F07_action_policy (source chuẩn hóa LF; PDF/PNG nguyên byte):

- `F07_action_policy.tex`: `dac92bcdc0ba13b632aeb79fea6c38c0727c7bbcf2c6a4a6551d0f656cc0ac65`.
- `F07_action_policy.pdf`: `db6db61add3d79c6f7fcfeafdea29fe49dfcf2b5b6ac55911146b01a8105af39`.
- `F07_action_policy.png`: `863c361205bd7c8beef9495550f52da78afb643bc3a0cd4bc0a4ae9e11f5d358`.

### 9.18. Projection, schema và prompt đã lưu

T32; CL098–CL101. SYS43 là core/mt_bicl_context.py frozen; BG09/SYS42/SYS18/BG18 giữ đúng builder. U06 provider EX01 raw hash 64e5…07c7 (§9.14) nối full membership 9ed7…fcb4 với U08 MT. Kiểm số học summary 5/4/2/3, wins4/0/0/1, exemplar/rank/age và mean utility từ 5 gain/9 loss; không gọi project_context hoặc sampler. Prefix gốc 437 ký tự nằm nguyên trong request4586; các request Native/Common/v1/Anchor có 3699/4186/4556/3916 ký tự, C2/A/B null. Source card c2cf28588843ea3ee339bccec6e08f445495863de839d6fe727a5e9459a220c0 khớp trace/request; proof giữ riêng. Bản dịch tiếng Anh phục vụ trình bày, không nhận độ dài/hash của bản gốc. Kiểm nguồn, số liệu, 84 đặc tả, liên kết/footnote/diff; không sửa runtime, chạy suite/API/forward hoặc đánh giá mới.

### 9.19. Tám vai trò, DAG và thuật toán ghép cặp

T33; CL102–CL105. SYS44 registry/SYS45 order/SYS46 hosted runner/SYS47 evaluation đều khớp frozen/live theo bảng §9.1. B03 hoàn thiện ở Markdown; F08 tách shared-input relation với dependency giữa output. A01–A03 là pseudocode có nguồn, không chạy mới. Kiểm EX01 24 slot prepare/forecast, ba repeat, parent shared e6c16…a103, dependency Common/Anchor đúng output digest cùng repeat; mọi stage hoàn tất trước outcome bắt đầu 2026-11-10T06:56:01.840159Z. Request ID không trùng giữa các reply; r0 có năm response và ba bypass. Barrier không xóa donor exposure; Native FAIL/whole-system NOT_CERTIFIED giữ nguyên. F08 một trang180×155mm, PNG2000px, font/bbox/log/hash kiểm PASS. Không runtime/code/input changes, suite, cold replay, model hoặc API.

Hash sản phẩm F08_variant_dag (source chuẩn hóa LF; PDF/PNG nguyên byte):

- `F08_variant_dag.tex`: `702c693829cdfd547ad40db565a6ee4e1446c096b54af75a1ff563d57e1741f2`.
- `F08_variant_dag.pdf`: `90741562af5cb5c24dd5e51e178448f636cf15278ddc2d4170ff0009c0a79517`.
- `F08_variant_dag.png`: `0be37326955cc6b2e9f7bfd3d75cc5844384bad81d5591571276204e4bd946af`.

### 9.20. Ngân sách, retry, stage/HTTP checkpoint và amendment

T34; CL106–CL110. SYS48–SYS57 khớp snapshot/live theo §9.1; SYS02 frozen phân biệt bản live trình bày. Chỉ đọc source/records, không chạy transport hoặc recovery. Kiểm số học cooldown: provider wait1200 không bị cắt theo cap exponential900, còn wrapper legacy cap60; mô tả rõ hai đường. EX01 năm response r0 nối raw HTTP200, đúng stage attempt UUID/body/hash; không gửi request mới. Ordinary resume giữ active execution cap3, UNKNOWN không resend. Nguồn U08 thực tế có amendment quota/restart, không suy mọi HTTP dùng policy đầu. Các binding sau là member U08 (outer hash §3.4), đã kiểm manifest/envelope; OP03 có12 retired, OP04 có15, không sinh reset mới.

| Binding | Member U08 | SHA-256 nguyên byte | Phạm vi |
| --- | --- | --- | --- |
| OP01 | `docs/plan/week12/unified_model_quota_runtime.json` | `9a94c795df76ae2e74687d36555d4dd063026a102c38620a6b201b961c9e66d1` | org/model từ sequence487 |
| OP02 | `docs/plan/week12/unified_provider_quota_runtime.json` | `6ee886350077e972588af39396b9a55dbdfbd2ae1bd327d53328f076c96e28c2` | provider response từ sequence591 |
| OP03 | `docs/plan/week12/unified_point_restart_runtime.json` | `550cdc887077131c8208993d0d9f800c7ebc15db66a76fff1b13d0c1bbda093c` | VCB-2026-04-01 và VJC-2025-12-19 generation1 |
| OP04 | `docs/plan/week12/unified_slot_restart_runtime.json` | `00d6cdca4526d0f1685a0261b374a662cef15e329f4e8f05e4176f5c07b5852e` | VCB-2026-09-23 r2 MT slot, retired map15 |

Kiểm hash/source/84 đặc tả/links/footnotes/diff PASS; không compileall/unit/E2E/leakage vì không đổi runtime, code, schema hoặc dữ liệu. Không cold replay, tái thu hoặc nâng gate lịch sử.

### 9.21. Ứng dụng hiện hành, EX01 hoàn chỉnh và tự kiểm G2

T35; CL111–CL116. Nguồn ứng dụng sau snapshot nghiên cứu được giữ **riêng**:
AP01–AP17 dưới đây là byte checkout hiện hành, đối chiếu Git `c432fef2`
(nội dung source chuẩn hóa LF khớp blob). Không gán chúng vào snapshot
nghiên cứu hoặc đổi expected hash cũ. Code/app/receipt không sửa trong T31–T35.
Đã đọc contract phần form hiện hành và source dispatch thực: form 1D dùng
timeframe envelope/capture, có daily_provisional; endpoint daily-closed cũ
khác đường này. Không bỏ chi tiết đó để kể ứng dụng như luôn có nến đóng.

| Binding | File hiện hành | Byte | SHA-256 checkout | Nguồn trong QA ứng dụng |
| --- | --- | ---: | --- | --- |
| AP01 | `docs/plan/week12/variant_serving_contract.md` | 46710 | `81e74eba95001603609297fe3e17369afdc63a26296f69fe6e4e9ec620a70548` | Đọc và pin riêng, không nhận là QA source |
| AP02 | `web_interface.py` | 37164 | `240972a503099144993c77aa3fd9a97826655b0d3b781c1c1500eb66b02566d6` | Khớp QA |
| AP03 | `core/serving_registry.py` | 4985 | `21746b6717da86de7b22b066429fc784574495f96547af4680929aabb4c6c230` | Khớp QA |
| AP04 | `core/serving_live/service.py` | 8129 | `b117b100465a208efe027190155ec0b3b31a3bc60c9a99cbf6c36970bc24837a` | Khớp QA |
| AP05 | `core/serving_live/snapshots.py` | 8918 | `0ccfe21a40e18a5b9e2c02fdd6f4503c939c2c55ffe1e166d86e42bbb68fc7ac` | Khớp QA |
| AP06 | `core/serving_live/timeframes.py` | 8556 | `16aa0058308bcac38d09dc870cc64007fa5c705d999ca0aa8f16d179136f37e3` | Khớp QA |
| AP07 | `core/serving_live/timeframe_provider.py` | 2026 | `3415bf105adc677867ce03f73f61434ef13c015d5d6324b65903620fcb098b73` | Khớp QA |
| AP08 | `core/serving_live/provider.py` | 7036 | `4c4588c658bdf4d62223f39735799a480f10662f6ecd63a5d1798e200b7b42f2` | Khớp QA |
| AP09 | `core/serving_live/context.py` | 2680 | `5a8c370cc101df0ae6db037b482782ca1e45884cb3b0b36d277fcbbd59ab9d3e` | Khớp QA |
| AP10 | `core/serving_runtime/service.py` | 14630 | `505a1fe9bd697372a5550367b5e82a60df8c4462d670c0fb79846bd18d7d7686` | Khớp QA |
| AP11 | `core/serving_runtime/runner.py` | 13143 | `0c8b1f3e99f383ec61b2ac1f5c665941123308593da457ec29c69cf1a1ab31b6` | Khớp QA |
| AP12 | `core/ui_presentation/live.py` | 2027 | `51c6a7407b8533faff15ceb3c410fb9ea8cc3c9064816869d33e710d48ea793c` | Khớp QA |
| AP13 | `static/js/analysis/form.js` | 3080 | `7fcda3d851c96465e9464a309a7f850bbd5f8bd046cbd692f3db70937bb4bbe2` | Khớp QA |
| AP14 | `static/js/analysis/timeframe.js` | 1683 | `b2ce603fcb767c4b7799d528fdf5fe2342e6f9798fb8681e63febb223f483efc` | Khớp QA |
| AP15 | `templates/analysis/form.html` | 499 | `68ae0b1f0affa200d5ad1b6848a42d7746ff30a610802100352a04386d910ebf` | Khớp QA |
| AP16 | `docs/plan/week12/serving_integration_acceptance.json` | 2503 | `1fc3a65af3a8301a9c884dd19e1f2cbb3510ad5e584a760bf0e737a68971c5be` | Đọc và pin riêng, không nhận là QA source |
| AP17 | `docs/plan/week12/serving_bilingual_checks.zip` | 73374 | `69f0a279932b91973aebfe89350b8ae8a5a637eaffb7435019636fed1cda8914` | Đọc và pin riêng, không nhận là QA source |

AP16 là serving_integration_acceptance_v10, status
OFFLINE_PASS_BROWSER_PENDING, f11_complete=false, desktop/mobile NOT_RUN.
AP17 có 13 member được kiểm hash/bytes với manifest và receipt. 403 source
bindings hiện hành khớp QA; 135 Python/24 DOM là kết quả **đã lưu**, không
chạy lại. Đọc python_reuse.json để giữ nguồn kế thừa/delta DOM; không nhận là
mọi suite đã chạy lại sau sửa DOM. Receipt/QA ghi market_calls=0 và
hosted_llm_calls=0 trong gate đó. Không mở browser, app, capture hoặc model
trong task viết; trạng thái F11/F12 và gate khoa học giữ nguyên.

EX01 outcome lấy riêng sau barrier24 đã kiểm §9.19: decision03/07, entry04/07,
exit06/07/2023; VND48180→48390; gross+.4358655044%, net−.2647317124%, DOWN.
Kiểm oracle số học theo TIME01, bốn yếu tố phí/slippage, source identity
TIME06 và bảng tám raw/final/reason r0. Không đọc outcome vào context/request,
không chạy lại tài khoản hoặc chọn ca thắng. F11 schematic một trang180×185mm,
đã render/xem PNG2000px; không screenshot giả hoặc browser acceptance mới.

**G2 — tự kiểm nội bộ phạm vi viết P2/P3**, không phải bốn gate runtime,
giảng viên phê duyệt hay hoàn tất T74. Chương3/4 không còn block chưa viết;
các câu hỏi đọc hiểu ở plan §3.3 được nối như sau:

| Câu hỏi đọc hiểu | Nơi giải thích | Giới hạn cần giữ |
| --- | --- | --- |
| SHORT/CASH và giá vào/thoát | Ch.3 §3.2; Ch.4 §4.2/§4.10.5 | Không bán khống; giá tương lai chỉ mở sau forecast |
| Agent nhìn gì, deterministic/offline/hosted | Ch.4 §4.1/§4.2/§4.3 và F03 | Role khác số call |
| Pattern khác Trend | Ch.4 §4.3.2/§4.3.3 và F04 | Format/heuristic không chứng minh prose đúng |
| Alpha/sentiment/confidence | Ch.3 §3.3; Ch.4 §4.3.4/§4.3.5 | Missing khác neutral; confidence không calibrated p |
| Native/Common khác Base | Ch.4 §4.4 và B03 | Bridge nhiều thay đổi, không single-cause ablation |
| Episode/regime/similarity/support/K | Ch.4 §4.5–§4.7, F05/F05a | Strict maturity, population khác examples |
| Prior/target/query MT | Ch.4 §4.8.2 và F06 | Query không nhãn; frozen fold pool/reserved IDs |
| Teacher/student/resources | Ch.4 §4.8.3 | Seed42/step3000 có nguồn; no query optimizer update |
| p cao nhưng utility âm | Ch.3 §3.6; Ch.4 §4.8.4 | Teacher sign + bootstrap magnitude; p_student riêng |
| Anchor/veto | Ch.4 §4.8.1/§4.8.6, F07 | Strict Q10/Q90, equality reject; enum khác prose |
| Tám role ít hơn tám reply | Ch.4 §4.9.1, F08 | Dependency cùng repeat/bypass không fake request |
| Account và barrier outcome | Ch.4 §4.9.2 A03/§4.10.5 | Cycle khác account; paired khác independent n |
| Đã kiểm gì, causal vẫn thiếu | Ch.4 §4.9.2/§4.10.4; sổ §3 | Native FAIL, whole-system NOT_CERTIFIED, UI PENDING |

P3 hoàn tất **bản nháp** T16–T35: F07/F08/F11, B03 tám role, A01–A03 và
walkthrough có outcome. Không nhận toàn luận văn/citation/LaTeX hoặc phản biện
ngoài đã xong. T36 trở đi chưa đánh dấu; bảng LaTeX, phụ lục và rà soát cuối
tiếp tục theo plan. Chỉ kiểm nguồn/hash/số học/link/footnote/spec/diff và bố
cục hình. Không compileall/unit/E2E/leakage vì không đổi runtime/code/schema/
input, không chạy lại acceptance, replay, fit/forward/sampling/API.

Hash sản phẩm F11_application_flow (source chuẩn hóa LF; PDF/PNG nguyên byte):

- `F11_application_flow.tex`: `c6da57e7b215605f8ceb4254c97bf961c6da5ac68c767c037e0708144bb0de0e`.
- `F11_application_flow.pdf`: `a6a53ed05199d14f4d224d80e79d8a8d575162e706527ff95deb380f849446af`.
- `F11_application_flow.png`: `27bbef8c7762bd232a9f307492d97b7a23000ecacc735040aabe7448a7cf0b9b`.

## 10. Nguồn thiết kế thực nghiệm

### 10.1. Binding artifact và source đã khóa

ED là dữ liệu/receipt nguyên byte; ES là source frozen. Revision đọc qua index/chunk đã kiểm (§3.2); U08/U09 và snapshot dùng outer/member pin tại §3.4. Không chạy code trong ZIP, không tái phân tích hoặc gọi model.

| Binding | Nơi lưu | Member/đường dẫn gốc | SHA-256 nguyên byte |
| --- | --- | --- | --- |
| ED01 | revision | `outputs/revision/revision_minimal_final_v1/manifest.json` | `5ccb426ab41088a7ff3956e229802a3a8e8c23a9980db93be602c9499d9279f1` |
| ED02 | revision | `outputs/revision/revision_minimal_final_v1/summary.json` | `46782716a0770c9589056fbcf499b60f738c7243647e9a378f91e01656c04299` |
| ED03 | revision | `outputs/revision/revision_minimal_final_v1/completion.json` | `6ddc1ae726bdf6a35b59d685cb2e76090a06ffbb27ec3d1507ab129234c7cfb6` |
| ED04 | revision | `outputs/revision/final_temporal_v1/contamination.json` | `4f0b8c2c3008dabf5e2b44354e960c75f21be9d4514a7bbca58ee9906a89207e` |
| ED05 | revision | `outputs/revision/final_repeats_v1/protocol.json` | `282ca8743076b1bd48266160a78b8fe0a74f2301f2d133c018a4554df7e87357` |
| ED06 | U09 | `outputs/unified_integration/u09_analysis_r1/receipt.json` | `b1b73325718f7343c8c9457f35a31d5a391335f2b28d1e4c55792abc19ccbc2b` |
| ED07 | U09 | `outputs/unified_integration/u09_analysis_r1/results.json` | `3136ab9bdeab377196236e1a01402646257ec3beb251877702dbc86e1e67e31f` |
| ED08 | U08 | `acceptance/u08_acceptance.json` | `b7271af5ea56b07ea5616465f974101c3a69935546e8e69ef8443996e7b1b50e` |
| ED09 | U08 | `outputs/unified_integration/u08_research_r1/receipt.json` | `2e0ec8bf9a7c57cac8621597e1b88220ca72499dec2dfad5c8306c1a8eb2dd49` |
| ED10 | revision | `outputs/revision/revision_minimal_final_v1/price_quality.json` | `610e03c180adf5221a9a52b997cac10e03a43d1a9d61fac2fff6c4c1c304ea86` |
| ED11 | revision | `outputs/revision/revision_minimal_final_v1/main_predictions.json` | `1e9e0bd1803e1f243734dc79c7ad4834d823f2b042c1daca2cada9e11ffe6840` |
| ED12 | revision | `outputs/revision/revision_minimal_final_v1/lineage.json` | `11ff03d51dfdd72e2f908f3cbe387f1e7863b8cbb0697f783878913eb6421626` |
| ED13 | revision | `outputs/revision/final_temporal_v1/folds.csv` | `3cafd3eea9d752b8a65aba6774b422c98616c78177f66a13898b2861db8121ba` |
| ED14 | snapshot-data | `docs/plan/week12/unified_comparison_protocol_v2.json` | `b783a0d50cd03d418fdc439ee93eba76edcd1a60be063deaecf3e8259c8bb34a` |
| ED15 | snapshot-data | `docs/plan/week12/unified_comparison_manifest_v2.json` | `dff00745cb55d8e92570fd7a331e69971f241d06ca77815d0382006c67e8b30e` |
| ED16 | U09 | `outputs/unified_integration/u09_analysis_r1/predictions.csv` | `d7d5f9b90d009f3da31de64df067ae9ac4ff72ccd395debf6c7f8ff08aa1da32` |
| ED17 | revision | `outputs/revision/revision_minimal_final_v1/attempts.json` | `5323ea436d2f6fd3f023de2e16bf7fddecc1e5d172c8ec6fed8cc372126d50a9` |
| ED18 | revision | `outputs/revision/revision_minimal_final_v1/costs.json` | `d6a682ac947c959f2d4f96ef25fc478afdc2611fe3cb5ad2a2e87589ed6b77bd` |
| ED19 | revision | `outputs/revision/revision_minimal_final_v1/pairing.json` | `aa6eb54cfb0c7931876a1ede1cfabaddc9ace2eeace340acb806c56a96c03c0b` |
| ED20 | revision | `outputs/revision/chart_r1_run_v1/run_manifest.json` | `487d92694d96dace807471e7c83cd30fda4d312335b14759f262998fc8e5b086` |
| ED21 | revision | `outputs/revision/r4_value_bank_v1/manifest.json` | `6ea80ee64283fe68b15c61e5ccbc0ca30d394e4d8544f7a41946e3b90a1deca4` |
| ED22 | U08 | `docs/plan/week12/unified_live_runtime.json` | `2a4661d43ffde54a991cb58858c4420241645ddb1feca59f00ec875fdbdde083` |
| ED23 | revision | `outputs/revision/numeric_controls_v1/run.json` | `372b9c02a145d2fb1dc356170f589a32a819d5b71c0ce5c35ce6c7261052529c` |
| ED24 | revision | `outputs/revision/numeric_controls_v1/summary.json` | `d7a9217e9c61edb8a88de1e6f87098b0bf6729ae2232afee63065fb1d8c5c85d` |
| ED25 | revision | `outputs/revision/numeric_controls_v1/inference.json` | `2f5eb5db8fe0fb2fb6de298c6361b6d4c892be9fbcf51672a4224bb66dd504f8` |
| ED26 | revision | `outputs/revision/execution_final_v1/policy.json` | `c020b42211a2afc6672d8bd570b7eabbe6cdc2d1477c97855cefd23cdf894a0c` |
| ED27 | snapshot-data | `revision/numeric_controls_protocol.json` | `9615814a62e0a0aa72dfda99c3c55d45c4abaaa5e2a8362591e1cb2cb6343eaf` |
| ES01 | snapshot | `core/revision_baselines.py` | `b6c0e05d62154c31a6fec387b68d6c6f875b1125a4115046d2e978de1b2ed6c5` |
| ES02 | snapshot | `core/revision72_analysis.py` | `6586c5e9d78988e408cf55672fce30cdcff2d7475bf9059eb9b2f54edb69eec8` |
| ES03 | snapshot | `core/revision_numeric_design.py` | `ee2f36416efbda4c5237c55a882f7da3f836db66da7cd9135cbdeccbc1b8131e` |
| ED28 | revision | `outputs/revision/final_temporal_v1/primary_dependence.json` | `e3486057da26a875f621cd3062bb74c256900a7f2401f37a947d842d27b043fc` |
| ED29 | revision | `outputs/revision/final_repeats_v1/ba_family.json` | `05c22e2c93c35dc3aa357080ee480368dd9d7befd3cf604a2ce8c65f859423bd` |
| ED30 | revision | `outputs/revision/final_contracts_v1/targets.json` | `244e60604a0924ee884afa364dbeed298ccf1c19c9ef080d151ee36bbb7574ab` |
| ED31 | revision | `outputs/revision/final_contracts_v1/report.json` | `d70a70952ffbf32e3a2f7e995b95eff4a672efbb6dbce50f2dbb8d0e5b9c75bf` |
| ES04 | snapshot | `core/unified_analysis/analysis.py` | `e805460aa47b8d36f563d936b0e52322968f65485537c16fdd94525955179a85` |
| ES05 | snapshot | `core/unified_analysis/statistics.py` | `4446fa0a77fce1a74a38d94918ae64c1c379c9a6a997b60a8d5df40dfff85b12` |
| ES06 | snapshot | `core/free_pilot_statistics.py` | `097cf88e3068126c1f668da3022109649aeaff4f8e22a2a319639a9fa9bcd7fb` |
| ES07 | snapshot | `core/revision_clean_metrics.py` | `f7aaa809cf2d1422f60b1210f7546e0503eea2dab6721f33cacbffeea6f60f75` |
| ES08 | snapshot | `core/revision_numeric_statistics.py` | `22d4a54e23d26fdd3c2985c942c5403a804c3969aa471e72827657bdb47b61e7` |
| ES09 | snapshot | `utils/statistical_tests.py` | `5d1096fbf63d9428efc9f6b13ed611fc2324e4ed1281e3c61f1cc9246e54b314` |
| ES10 | snapshot | `utils/account_risk.py` | `487a50fe28397130a93a92c3f2cd79b5184e5cc1a546b9b21ea7ab7a976cd829` |
| ED32 | root-export | `outputs/revision/final_baselines_v1/manifest.json` | `0a20fbe49049dd61fae2eb8bf3289f65039395e6bcac6745b851a5a00d804226` |
| ED33 | root-export | `outputs/revision/final_baselines_v1/main_comparison.csv` | `06742e2b876f3bb0e38191cb74f98e9d43f7ed5847b50e4a29e8b210c4056e6c` |
| ED34 | root-export | `outputs/revision/final_baselines_v1/financial.csv` | `ddc84b3e5a44c20c0d8825e61dc139dbfb7aef03c38e1b7cb7d37d429f070ae0` |
| ED35 | root-export | `outputs/revision/final_baselines_v1/classification.csv` | `5fdce7ee034756102a76f9aba8e3f8f4c60e563b16e1426aacca2271a4d26643` |
| ED36 | root-export | `outputs/revision/final_baselines_v1/macro.csv` | `0d9b2e38a49a20509b680d666cd22c75ded41f238d5997facb7cb359a986f6a7` |
| ED37 | revision | `outputs/revision/final_repeats_v1/panels.json` | `814f47d11502c2dfb3c30a64f0ef0a14dd6dff39e965bd5fc5e36f8b8c9f5fab` |
| ED38 | U09 | `outputs/unified_integration/u09_analysis_r1/per_repeat.csv` | `71f54c70b71672d3e8b2d2e4bdb56281e932f1764dfa24d0bd79c15c9a1f236e` |
| ED39 | U09 | `outputs/unified_integration/u09_analysis_r1/classification_by_group.csv` | `cd0c12b3363c7466ec9e167ffdacb3daf05db6e6fae125f94e2e08413c449cbb` |
| ED40 | U09 | `outputs/unified_integration/u09_analysis_r1/prior_traces.json` | `dff668d4841a1ff9e36bb13ae4e09f8a54e612f264cf1b9cedb94281824dea3e` |
| ED41 | revision | `outputs/revision/final_temporal_v1/block_sensitivity.json` | `4233ce33073c343acf8df8a0fff1b346ccbaa7e32648c6b77980d51d5d5fa822` |
| ED42 | revision | `outputs/revision/final_temporal_v1/panel_hac.json` | `9ad67cf77df631e11f71ddc6e3874a495812963e91201565ec5f8764dd4b287b` |
| ED43 | revision | `outputs/revision/execution_final_v1/scenario_summary.csv` | `89cf353e5499aa5e14d3f3322224ff7288ac5754b1d906f715fd7a88bb36aa92` |
| ED44 | revision | `outputs/revision/execution_final_v1/report.json` | `0faec26af37be228ff1863926c778ff6910d4aff39d3c476ef6123a60112882c` |
| ED45 | revision | `outputs/revision/final_temporal_v1/stratified_metrics.json` | `313a17af07e951d228ce01081510f36b83c4e19ae85041a69505f653df28fefd` |
| ED46 | U08 | `outputs/unified_integration/u08_research_r1/wire.json` | `f7a5894f2576211c03dfd190428679bcdf1e5ee7be8d5909bbca4e27efa9eb6c` |
| ED47 | revision | `outputs/revision/final_temporal_v1/protocol.json` | `7f8f3cead7d95a00c3967c43e60b3332430a4fc54e630bd0929807c56bae2449` |
<!-- experiment-data-end -->

### 10.2. Phạm vi hai nghiên cứu và mốc khóa

T36; CL117–CL120, ED01–ED09. Đã đọc74 artifact/source chọn lọc bằng EvidenceArchive.read và consumer U09 chỉ đọc; không analyze, restore ghi đè, cold replay hoặc thực thi code ZIP. Index/chunk/member/outer/envelope/receipt khớp pin §3; reader U09 kiểm15 artifact với acceptance. Component records375 job_id duy nhất, main204/upstream36 mới tính trong release/factorial135; nominal upstream54 có18 reuse main. Reused193/new182/194 attempts/12errors không là tất cả historical calls. Context raw1290+bypass1158=2448;102points/51accounts/sixfolds/12dates không biến thành2448 độc lập. ED04 first-request2026-11-02→queuefreeze2026-11-03→last2026-11-04, prospectivefalse/servedrevisionnull. U08 seal2026-11-12T03:10:18.266468Z/accept03:17:37.298613UTC; source/hash không chứng minh unseen holdout. Kiểm số đếm/timestamps/84 đặc tả/footnote/links/diff; không chạy suite do docs-only, không đổi runtime/input hoặc gate khoa học.

### 10.3. Dữ liệu, lịch, phân vùng và độ phủ

T37; CL121–CL125, ED10–ED16. Table B04a/b nằm trong §5.2 Markdown, chưa tạo CSV/TeX dàn trang. Kiểm main prediction theo symbol/date khớp102 U08shared; labels25/77, BHN6/others12, accounts51, dates12/folds6. Component lineage<3verified_articles=79 và U08flag unavailable79 đọc từ hai nguồn riêng. Price-quality9×1681rawrows; BHNinvalid2022-09-13, suffix bắt đầu14/09, excluded673. Componentfolds51purgePASS/train32–318/validation18–21; finalcontext8train123/BHN85, validation54–60/BHN56,51bindings/9fits, không gán split mới cho donor cũ. U06 bank coverage211/213/215/213 tổng852, maxexit2022-12-30; chênh828 với ngưỡng1e-8percentagepoints, max.04298848884252138pp là giá trị return, không labelcount. ED14/15 raw snapshot khớp source pin; immutable source/system gate giữ nguyên. Chỉ kiểm tài liệu/hash/counts/links/84specs, không fit/compute label/pipeline/API/suite.

### 10.4. Cấu hình thực dùng và đơn vị thực thi

T38; CL126–CL130, ED17–ED22. Component attempt metadata649records:455frozen-source (240upstream/215Decision),194newDecision; success433/182/error22/12. Toàn SDKtemp1e-8, visionqwen3.8-27b1024 và Decisiongpt-oss-20b2048, APIseednull; protocol khai0. ED20provider-only bỏ internalcap/deadline, không áp U08cap3 cho toàn component. Pairing147groups/40order mismatch/9cross-epoch. U08config token960/960, observedwiretemp1e-8, SDKretry0; runtime analysis107packages/Python3.13.5. ED08receipt counts1702all/1687active/15retired, status2001505/429194/5031/UNKNOWN2; active2001495/429191/5031. Graph408/render204/shared102 khác số modelcalls. Slots2448/raw1290/bypass1158 và51account/repeat giữ đúng đơn vị. Tokens2986930/reserveUNKNOWN9177/maxchars4750 chép receipt, không billing estimate; U09API0 chỉ analysis. Kiểm metadata/counts/84spec/link/footnote/diff, không runtime suite, model, fit, newtelemetry hoặc replay.

### 10.5. Đối chứng, panel và can thiệp có/không có bằng chứng

T39; CL131–CL136, ED23–ED27/ES01–ES03. Mainprediction9variants gồmAS/B+7numeric; giữrecipe/provenance frozen, không refit. ES01logisticvalidationgrids/median/scale/refit vàfactorvote; ES03fixedfive IDs/currentcustom, noflipkhôngrerank, threshold.1/strictmeanvote. Numericrun23strategies×102=2346,51scopes/20random; eligible_train_range=[85,85] là số eligiblefactor, không85trainrows. Factorial9units/3exec/5variants và7contrasts riêng compactpromptmain/upstream. ED26scenario12, labels/predictionsfixed; continuoushold_price_only componentfinancial khác cycleLONG và unifiedprotocol excludescontinuous. ED07/14 xác nhận20maincontrastcells và3bridges, support102/3/51 giữfallback; deferredretrieval/prior/MTpanel không tạo thêmresponse. Chỉ source/hash/IDs/count/math/links/84spec/diff, không numericalreplay, fit, API hoặc suite.

### 10.6. Metric, aggregation và resampling theo từng nguồn

T40; CL137–CL144, ED28–ED31/ES04–ES10. Đọc sourcefrozen, runtime/source không đổi. Metric ví dụCASH trên25UP/77DOWN kiểmAcc77/102/BA.5/MCCnull/F1UP0; missing-class toy giữnull. CycleSharpe/SortinoLPM2 trên ba return giả định kiểm ddof1/RMS, không tính lại performance thật. Targetaudit7grossnetflip/65entry≠Close chépED30, không relabel. Primarycomponent51accounts/contextmean3repeatwithinaccount→mean51 khác numericfactorheadline9symbolaccounts. NAV initialanchor/EODvscycle và held/close/turnover denominator táchđúngsource. Componentriskdaily252/popSD/negative-subsetSD khác contextcycleunannualized/sampleSD/LPM2; sparsecyclegate không được suy252. Componentmain/panel seed20261102, factorialjointfinite6986/undefined3014 khác U09threshold9500; numericfamily23/64signassignments/seed0/10000draws. U09joint20/L2/PCG64seed20261110/10000finite/nozeroSD, indexhash09374ae6e221b701c9b2b88241135fd70a701e611e752a8b8ec5bf82b669b9a7, lấymetadatađãlưu; không redraw/bootstrap/risk/accountreplay. Brier chỉsupportednumeric, không LLMconfidencecalibration. Giữ undefined/rationale và descriptive-only/NativeFAIL/NOT_CERTIFIED/UIpending. Kiểm ED/ESrawhash/counts/math/84spec/link/footnote/diff; docs-only không compileall/unit/E2E/leakage hoặc acceptance/replay/API/fit. §5.1–§5.5 đủ bản nháp thiết kế, §5.6–§5.9 chưa viết/P4 chưa xong; bảngLaTeX/phảnbiệncuối vẫn giai đoạn sau.

### 10.7. Kết quả thành phần và ánh xạ từng ô B05

T41; CL145–CL154. Bản nháp [§5.6](chapters/05_experiments.md#56-component-study-results) giữ bảy bảng Markdown B05a–g, chưa xuất CSV/LaTeX; dàn trang bảng ở T69. Nguồn ED32–ED37 được ghim tại §10.1. Manifest ED32 khóa đủ 11 export; từng file đã đối chiếu SHA-256. Sáu member revision dùng trực tiếp (ED05/24/25/28/29/37) đọc lại qua `EvidenceArchive`, kiểm index/part/chunk/member và so nguyên byte với bản đọc dùng cho định dạng. Không chạy code trong ZIP, không gọi model, fit, replay tài khoản hay sinh bootstrap.

| Đích / phạm vi ô | Locator của nguồn đã khóa | Đơn vị, phép dẫn xuất và support |
| --- | --- | --- |
| B05a, chín hàng phương pháp có classification; tên, Acc/BA/MCC/F1/LONG và return | ED33, khóa `cohort=all_102`, `dimension=pooled`, `group=all`, `variant` lần lượt AS/B/constant_down_cash/train_majority/constant_up_cycles/momentum_20/logistic_price/logistic_matched_market_inputs/factor_only_vote; cột `label,accuracy,balanced_accuracy,mcc,macro_f1,long_rate,mean_account_net_return_pct` | Acc/BA/LONG nhân100; MCC/F1 giữ fraction, NA giữ nguyên; return đã là%; `n_valid=102`, `support_up=25`, `support_down=77`, `n_accounts=51` mọi hàng |
| B05a, toàn bộ cột MDD và hàng Continuous hold | ED34, khóa `cohort=all_102` và cùng `variant`; MDD=`mean_account_drawdown_pct`; hàng cuối `variant=continuous_hold_price_only`, return=`mean_account_net_return_pct` | MDD/return đã là%; mean51 tài khoản. Continuous hold có `classification_units=0` nên toàn bộ năm ô classification/LONG là NA, không suy nhãn; mean MDD dương |
| B05b, toàn bộ ô | ED33 AS/B: `tp,fn,tn,fp,predicted_long,predicted_short`; ED34 AS/B: `mean_account_held_session_fraction,mean_account_close_exposure` | Count nguyên, predicted_short thể hiện CASH; hai fraction exposure nhân100, mean51 account; không đồng nhất exposure với LONG-rate |
| B05c, đủ9mã và6block; mọi ô | ED35, khóa `all_102`, `dimension=symbol` hoặc `block`, `group` đúng tên hàng, `variant=AS/B`; `n_valid,support_up,support_down,balanced_accuracy` | BA nhân100; ba count support của AS khớp B; BA NA tại VNM/b2025_h1 giữ nguyên. ED36 `all_102`, metric BA, `n_planned/n_defined` giải thích macrostock8/9, không lấy macro thay pooled |
| B05d, ba hàng đầu | ED24 `headline`, `strategy=fixed_custom5/dynamic_train_top5/dynamic_train_top5_no_flip`; `pooled.accuracy/balanced_accuracy/mcc/long_rate`, `mean_symbol_return_pct` | Acc/BA/LONG nhân100, MCC giữ fraction; return đã là%, mean9mã khác mean51account; mỗi strategy102điểm/25UP/77DOWN |
| B05d, hàng Random; đoạn dispersion/range | ED24 `random_family`, các metric tương ứng, `mean/sd/min/max`, `n_planned/n_defined=20` | Mean của20trial metrics, không ensemble; SD BA nhân100 thànhpp, returnSD giữpp; tất cả20return âm vì saved max<0 |
| B05e, đủ ba contrast, mọi ô | ED25 `contrasts`, khóa `dynamic_vs_fixed`, `dynamic_vs_random_mean`, `dynamic_vs_no_flip`; `balanced_accuracy_difference,bootstrap_percentile_95,p_exact_two_sided,p_holm_family_23`; metadata `family_size=23,sign_assignments=64`; ED24 `holm_rejections=0` | BA và hai đầu interval nhân100 thànhpp; p giữ fraction, hiển thị5decimals cho exact p và3cho Holm. Tất cả23contrast giữ trong adjustment, không chỉ ba hàng hiển thị |
| B05f, đủ bảy hàng/hai panel, mọi ô | ED37 `upstream/factorial.summaries.<branch>.<metric>.mean/sd`; metric `balanced_accuracy,mcc,long_rate,mean_account_net_return_pct`; support từ `n_units_per_execution,n_executions,n_accounts_per_variant_execution,support_per_execution,n_dates,n_symbols,blocks` | BA/LONG mean&SD nhân100; MCC giữ fraction; return mean&SD đã là%/pp. Mean±sampleSD qua3execution, `n_defined=3` mọi ô; upstream9account, factorial8account/execution; cùng9điểm/2UP/7DOWN nhưng khác panel |
| B05g, bảy contrast, mọi ô | ED37 factorial summary BA mean cho từng branch; ED29 `descriptive_envelopes.<contrast>` | AS−B/A−B/AS−S/S−B/AS−A/AS−P; interaction=AS−A−S+B. Trừ số chưa làm tròn rồi nhân100, không tạo resample; hai đầu envelope chép ED29×100 |
| Main và upstream interval/counts trong văn bản | ED28 `cohorts.all_102.intervals` (AS−B và đủ8contrast); ED37 `upstream.statistics.contrasts.AS-B.balanced_accuracy` và `mean_pairwise_disagreement.AS/B`; ED29 joint counts/radius | Main AS−B finite10000/undefined0; upstream/factorial BA finite6986/undefined3014, hiển thịpp; disagreement×100; main/18shared theo ED03/05 và phạm vi §5.1 |
| Các chênh lệch và diễn giải còn lại | CL145–CL153; đúng các ô chưa làm tròn ở trên; ED35 cho đếm nhóm tốt/xấu/tie | Full−Base BA+3.247pp, Acc+4.902pp, return−0.047pp; UP recall=7/25×100=28.000%. Năm mã BA cao hơn/hai thấp hơn/một tie/một NA; ba block cao hơn/hai tie/một NA; không tính thêm performance |

Quy ước hiển thị: ba chữ số thập phân, exact p năm chữ số, không làm tròn trung gian; dấu âm, NA, percent/pp và thứ tự mean đều giữ đúng nguồn. Mỗi hàng/cột chung locator được liệt kê đầy đủ, không dùng dẫn nguồn chung chung cho bảng. Kiểm khớp toàn văn bảy bảng với các ô đã định dạng từ nguồn, hỗ trợ count/NA, 84 dòng đặc tả nguyên trạng, links/anchors/footnotes và diff. Chỉ sửa sáu file Markdown; không cần compileall, unit, E2E hay leakage suite theo AGENTS §1.2. Native causal FAIL, NOT_CERTIFIED và UI/F11 PENDING không đổi. T42–T47/P4 còn việc; chưa phản biện ngoài hay dàn trang cuối.

### 10.8. Kết quả ngữ cảnh B06a–c

T42; CL155–CL158. Đọc lại U08/U09, snapshot và acceptance bằng consumer read-only `core/manuscript_u09/sources.load`, kiểm outer pins, từng member, 15 artifact/receipt và support, không gọi hàm phân tích hoặc replay. ED07 `results.json` là nguồn cho B06a/b: mười hàng theo `summary[].method` (Native=`original_fix`, Common=`original_common`), các cột lần lượt `accuracy×100,balanced_accuracy_pct,mcc,macro_f1,mean_account_return_pct,repeat_return_sd_ddof1,mean_daily_mdd_pct`; B06b dùng `n_points,n_forecasts,long_forecasts,raw_decision_responses,bypass_forecasts`. B06c lấy `per_repeat` tại khóa `(method,repeat=0/1/2)`, cột `mean_account_return_pct,balanced_accuracy_pct`, khớp export ED38. ED39 giữ đủ grouped classification; VNM/b2025_h1 thiếu UP nên BA NA. Tất cả ô hiển thị3decimals, fraction chỉ nhân100 ở accuracy; BA/return đã là% nên không nhân lại. Count nguyên, MCC controlnull→NA. Mean51account, mean3repeat và repeatSDddof1 giữ nguồn; không gộp306slot làm306điểm. Bypass/noLLM denominator khác nhau về ý nghĩa được nêu ngay caption. Bảng Markdown chưa xuất CSV/LaTeX (T69). Chỉ sửa tài liệu; không compileall/unit/E2E/leakage hoặc chạy lại API/fit/bootstrap.

### 10.9. Contrast, bridge và F09

T43; CL159–CL162. B06d: ED07 `contrasts`, khóa `(baseline,method,endpoint)` đầy đủ20cell; cột `effect_pp,band95_low_pp,band95_high_pp` đã làpp, không nhân100. Mỗi hàng bảng ghép đúng hai endpoint cùng baseline/method. B06e: ED07 `bridge`, ba khóa `(original_common,original_fix)/(Fact_Anchor,original_common)/(MT_BICL,Fact_Anchor)`, các cột `return_difference_pp,BA_difference_pp,same_action_forecasts,n_forecasts`. Ba chữ số thập phân, không làm tròn trung gian hoặc thêm bridge band. F09 vẽ đủ10returncontrast từ cùng nguồn, đọc ZIP/member theo rawpins trong source; cùngxscale[-1.22,.72], zeroline, CI không tái lấy mẫu. 20cell liên kết đúng jointfamily, không familyriêng cho hình. Source Python chỉ phục vụ hình, đã biên dịch đúngfile; PDF render bằng Poppler và xem PNG, nhãn/trục/band không cắt/chồng. Không compileall/unit/E2E/leakage hoặc bootstrap/API/fit. Hash sản phẩm hình:

Hash source Python dưới đây dùng nội dung chuẩn hóa LF như blob Git; PDF/SVG/PNG băm nguyên byte. Checkout Windows có thể đổi LF thành CRLF mà không đổi nội dung source; không dùng raw hash của bản CRLF thay cho pin LF.

- `thesis/assets/figures/F09_return_contrasts.py`: `2a7b1fa2a983ad5835a358c3496d97fa5361bbedbf971d86b1a15f7fe62e6bc4`.
- `thesis/assets/figures/F09_return_contrasts.pdf`: `fc216e18a06ddd3878f62d1d314ec2f740f8999bdacde02f721cd0a77c789efc`.
- `thesis/assets/figures/F09_return_contrasts.svg`: `5639b47b8f659deccb6a4470ef58420d4c270a4649e53eed5aefe1925832f00e`.
- `thesis/assets/figures/F09_return_contrasts.png`: `f192f4cf5bf89e4eea412c471aad133a3700ca7a45151e4a652759a1da9e2a0d`.

### 10.10. Độ phủ, descriptor và can thiệp policy

T44; CL163–CL168, ED07/16/40. B07a lọc ED16 repeat0, nối ED40 qua `trace_sha256`; `trace_reason=NO_SAME_SYMBOL_FROZEN_BANK_OOD` tách54điểm. Trên48điểm cóbank, `request.trace.status`, `visible_k` và `reason_codes` xác nhận READY1/8/1, insufficient47/40/47, visible_k0; reason LOW_POPULATION_SUPPORT40/QUERY_FEATURE_UNAVAILABLE10 đếm có chồng, không cộng thành102. V1 `retrieval.metadata.current_regime` đếm40/4/4 trên48active; không thay MT HMM. B07b age/sim median/min/max của ED16 `prior_mean_age_days/prior_mean_similarity` trên48v1point r0, kiểm bằng nhau qua3repeat; đây là tổng hợp trường đã lưu, không retrieval/bootstrap hoặc performance mới. MT `effective_K`3×86/0×16, numericprob86, teacher66; age/sim và prior_regret exportrỗng giữNA. B07c ED07 `policy_reasons` năm mục đầy đủ48/60/189/5/4, khớp từng ED16 `reason`; 302final=anchor. Brier chép `calibration` với đủslot/unique-point support, không so trên supportkhác. F10 đọc summary từ U09pin, raw/bypass chia3 để đếmpoint; kiểm các repeat có cùngmask, policy dùng slot306. Script mới đã biên dịch đúngfile; Poppler renderPDF và xemPNG rõ, không cắt/chồng. Không chạy policy, fit, API, replay hoặc suite runtime. Hash sản phẩm F10:

Hash source Python dùng nội dung chuẩn hóa LF như blob Git; PDF/SVG/PNG băm nguyên byte, cùng quy ước F09 tại §10.9.

- `thesis/assets/figures/F10_coverage_actions.py`: `377edf2825c632e5efa85ad109b8d17e7ad022848b22f2744699f307f9ce073b`.
- `thesis/assets/figures/F10_coverage_actions.pdf`: `5982a4696c317097780bc35bc01a6c3209511f27d6e5bafd6681b2906bcd17d7`.
- `thesis/assets/figures/F10_coverage_actions.svg`: `ad3cfd5afa55eba381f5bb8c2330a5702e037c17d4b04be31b5838e1d8ad06c8`.
- `thesis/assets/figures/F10_coverage_actions.png`: `f263b153da1db2fdb665d86739cd9dfe9de646908f177e9050a0511eaf3e61f0`.

### 10.11. Quy tắc và nguồn nhóm ca T45

T45; CL169–CL173. Giữ §7.7, không đặt rule sau khi chọn ca đẹp: repeat0, nguồn đầy đủ trước, sort(date,symbol). Toàn102điểm/816forecast r0 có shared/prepare/forecast/outcome; rawmember đối chiếu manifest trong U08 outerpin §3, envelope và outputdigest. Kiểm outcome.started_at sau completed_at của cả24forecast/point, không chỉ nhánh minh họa. Nhóm đủcontext: MT eligible và v1 khôngbypass→29; thiếu: bất kỳC2/A/B gateINSUFFICIENT_EVIDENCE vàbypass→47, tieC2,A,B; bấtđồngMT rawmapped≠anchor→5; vetoMT reasonREJECT_NONPOSITIVE_Q10_DELTA_U vàrawmapped≠final→2; sai: bất kỳ8role LONG/DOWN hoặcCASH/UP→52, tiemethodorder B06a. Chọnđầu mỗi nhóm cho FPT/FPT/HVN/MWG/CMG, không đổi r0. Chỉ nhóm sai dùnglabel cóchủđích, không suyaccuracy từ mẫu này.

B07d là count/ID/predicate; B07e lấy `prepare/forecast/<id>/u0/r0/Fact_Anchor.output.aux.packet.numeric/assertions`, unit nghìnVND, prefix45, sentiment từ shared. PacketCMG chỉ là auditview, không Nativeinput. B07f lấy ED16 raw/anchor/final và policyforecast, giữ NA khi bypass; fullreason/requestID bảng dưới. B07g lấy outcome.output.target và dates[1]/dates[3], VND, gross/net fraction×100, labelgiữnguyên; không relabel hoặc accountreplay. Longcycle thấtbại khác CASHmissedgain; hai CASHcase realized0 theo contract. FPT MT K3/m3 vàC2 population19/conditional1 liên kết EX01 §7.4–§7.6; regimekhácnguồn khônggộp.

Mọi basename dưới thuộc `outputs/unified_integration/u08_research_r1/slots/` trong U08ZIP đã pin. CT là locator nguồn tại sổ chung, không tạo receipt riêng. Mỗi hàng chỉ băm rawmember; outputdigest và contextmembership không thay thế rawhash.

| Binding | Logical slot | Member basename | SHA-256 raw member |
| --- | --- | --- | --- |
| `CT01` | `forecast/CMG-2023-07-03/u0/r0/Fact_Anchor` | `2f56c53019a165e530b49e0f0c88a650d842debcf3270c2ffdcc0963ec6f342b.json` | `f585f448d86aa593301f8c6a8535f5a92ab80a1a733fc091dfca4cca2bc5fefb` |
| `CT02` | `forecast/CMG-2023-07-03/u0/r0/original_fix` | `f1ea2a568b54540be5f64d06cbc0d5a37074a73cb3618b8339444eb4db07c73b.json` | `0097369bceaa448ad108631c4ddb0fd004cf7928abcf82cb354f32f234204f1a` |
| `CT03` | `forecast/FPT-2023-07-03/u0/r0/C2` | `d33c4a932ddfe9a5365fe271c5b176488aff85a5cb59bb01db5cf8693becf693.json` | `104be95520b47e7bd2ad6071002d5e039b1ec3c2f3264a20636f85faacedf00a` |
| `CT04` | `forecast/FPT-2023-07-03/u0/r0/Fact_Anchor` | `3fc8ef7e65fb8ae2cacb89fa3ce5bce94e98ef48a894e65cc74a48924b1b3b61.json` | `c9ebdeb3c900f5633234e7915b8f8129f5e0d919dc8115f9725da5de42109c44` |
| `CT05` | `forecast/FPT-2023-07-03/u0/r0/MT_BICL` | `58d6247d4cdd587aade0b220539c197053b921d48fde462bd1e4725ee56919ad.json` | `1a490828b1596a0b605da6371f2fd4bc6f95876ce590765582441828076e6fb0` |
| `CT06` | `forecast/FPT-2023-07-03/u0/r0/bayesian_v1` | `f875086c494f4b35ab84f1e1df38e0fd152df7f00cbc53e4ba615fcbd2551509.json` | `366b32095f0f5f022bc9852034c28bde87521eae720449b722061b130083d0f3` |
| `CT07` | `forecast/FPT-2023-07-03/u0/r0/original_common` | `64423caca8a47ecfcb81e2d2d7c9a9d6c6618facc1ef45e84c1e327d5f13fbe2.json` | `203a51ac6c6f79ea429b565b067f39f8283b46d10b002ab1a9fec5a9d90037da` |
| `CT08` | `forecast/HVN-2024-07-01/u0/r0/Fact_Anchor` | `5529ea4025966f7bf36443e2c4c32e322ef5b5a309464585945928c5dafad3f7.json` | `8bb7ff3c3f1031b8febb3ea2656924cc8aa004de6e31acffb979cb66965afd27` |
| `CT09` | `forecast/HVN-2024-07-01/u0/r0/MT_BICL` | `c8c71c657cf74869b599b410bcbdb6dbf7a6d1d6c10dc1419832ca6a3eedaf22.json` | `4a7d29b6805d968cf9a8b7afed66930e3046953686e4f83d6738ea66825f5b04` |
| `CT10` | `forecast/MWG-2024-09-20/u0/r0/Fact_Anchor` | `2e633ea731688ed0063cc805f4a850a04c3115fe2db3b828edb8c825d38bf05d.json` | `2a23fcfeb31b5f802f63cc61bfc00af13b87de2a89b7eb66f10d4e53ac940a8b` |
| `CT11` | `forecast/MWG-2024-09-20/u0/r0/MT_BICL` | `ea1bfdaaeb4d92aac3ce4307ff4fdfa4a26ffd7a487cf30b3f7a429ebf111c6f.json` | `cb8cba18703d4628cf57dbbbb45becf17710934b5ba94b0e1923b84c7976b906` |
| `CT12` | `outcome/CMG-2023-07-03` | `ca988293ec4fb389ad474ab0801dfeae295d0b7fc2471cc1e68f9c25f987682f.json` | `cd7045cf5964a4bfb393f21b0540c33a76e0b9e4f7f014cab2ee19b23dd996ac` |
| `CT13` | `outcome/FPT-2023-07-03` | `44ee5a008ff1b2964ddf676f02420fe9ed5a3f9aadb87e8a5bc789af23822605.json` | `ccc7cd71bc2877ea821b372b68427c9bf2d76636c944e4c66539dea4dd839866` |
| `CT14` | `outcome/HVN-2024-07-01` | `436c55af493bff35c023ee42b6f319a3a03971282a5c2cd12b128054cf00e827.json` | `a4600ff7a09cb4bf9743237d933648cffcc88e4f551c999658445e4072e5a161` |
| `CT15` | `outcome/MWG-2024-09-20` | `06dd15ab154bdf46ba6c03d14f28664554c503c143d7d402d4a3f29855d13b58.json` | `b0fb8fa988a8bc88636fec3b9d4af5258b37ce90a9f3284e2a546d87f8f57118` |
| `CT16` | `prepare/forecast/CMG-2023-07-03/u0/r0/Fact_Anchor` | `709f1f7a0393e8f2457d3ec17ecc8e6ae119bdddda5b811b9b230aa994d1f165.json` | `c475baae656171560ac9cde55a41674dafe4c2ed1a0bae63a57790a43522df5e` |
| `CT17` | `prepare/forecast/CMG-2023-07-03/u0/r0/original_fix` | `4e8cb9d5467eaef8497df63ce982d909a4a53dc468044f4e3961122f4ed3e15f.json` | `7ac1a7a49958fec08808545b4f2e26eaee88c636a229426f913caadff1a25cab` |
| `CT18` | `prepare/forecast/FPT-2023-07-03/u0/r0/C2` | `01e15b9af24cc5221d7c0a52aea7d0d75f57dfb27bf9399bc44d0d4f7f3f2111.json` | `3be9c1af7b82643958fbcb71e4bc5a2abd0f458ad94fea5e931815c304d179d2` |
| `CT19` | `prepare/forecast/FPT-2023-07-03/u0/r0/Fact_Anchor` | `6c8a29ac75aeb061c98d24cf6bcd99b9a90300b8fb06d71d787e028a2ff95266.json` | `baa0a9cb15eb9c121254cdf57d76c00dd1d6ada39a603279547f42489845ae4f` |
| `CT20` | `prepare/forecast/FPT-2023-07-03/u0/r0/MT_BICL` | `08ff81cfe2d64902d2f366e3668e9fdd3e87e8c6bc08c9d3288fc87feeee96aa.json` | `613707509fb6e579cf4f534a86a5040d13142d5b5a254c0b57da272dc69fd1e3` |
| `CT21` | `prepare/forecast/FPT-2023-07-03/u0/r0/bayesian_v1` | `738d6fb060b83cc5e47bd90ba1270e0f23f2a145731e49b41c0d621c724f5e22.json` | `6cb5f8473fb07138da22b84274be792453d5cd4e551f4e9a70cfada5dda1b202` |
| `CT22` | `prepare/forecast/FPT-2023-07-03/u0/r0/original_common` | `e32175e16f4bc276326e727e178368a385cac23dc5b26bcacc92d39a7c3adaf5.json` | `253af331cdaf7ee2b9435b5faf52bd6fa1ed372ad41f2bd128a071bc8484241b` |
| `CT23` | `prepare/forecast/HVN-2024-07-01/u0/r0/Fact_Anchor` | `45d938cae699a0d4b1884c0a7a70518017fbbbae556bdff03e45fef0a95bb71b.json` | `ec2fb64306c327795af77d6ef5e98fa56d05a757fbe94f9b8f5d2943d540c627` |
| `CT24` | `prepare/forecast/HVN-2024-07-01/u0/r0/MT_BICL` | `1b542349cfdd4274bd0bd8164e8b74022b70576f0c8cbc0d2cc9f53ef9d8ad88.json` | `faf10f90334f163bac733da4722a6aef738741e2ba8f7b007ed613c2395fa087` |
| `CT25` | `prepare/forecast/MWG-2024-09-20/u0/r0/Fact_Anchor` | `863134e8d4f1be77db19ff6d00d0f5e474e7d296d177e1a2c12e9b3f79f25e29.json` | `cae093c1f5abf112181b495900978556b7f2230b2d3d5203596507d371e127fa` |
| `CT26` | `prepare/forecast/MWG-2024-09-20/u0/r0/MT_BICL` | `4a55c8701b576f691c2d9c897fa4255fc5c928e18224b7e0361cb5630c6cc2da.json` | `475824088486aaffcc554655392808be110de88b7ea2c986e60cad26587eea07` |
| `CT27` | `shared/CMG-2023-07-03` | `bb5386de16154e9c9c4f5c97bfc5bebea7c1100a52c83a522e78b133c3565552.json` | `5d1deb264c9d73edcac4b93b66d28017b7c8ee2f83acdda8dd5dd4e1d2d404fa` |
| `CT28` | `shared/FPT-2023-07-03` | `7ace396801b8666a24f23ed0aef3466aa073db80185db93ceab24d48741a9ec3.json` | `42296f5e9e1c8b5ba25730a19adf0cd8445d251486116029bc2191e3f57e79cc` |
| `CT29` | `shared/HVN-2024-07-01` | `8d955df4cc7f6de4697c3d94b9856f1fa230ab1e65cf07a82358588f5c5643fb.json` | `6103bce1f0f20ca901122bd9d67e790d7b80789586af88ad5908a824678444b8` |
| `CT30` | `shared/MWG-2024-09-20` | `3ec26085d0deba6658532f7a00eb7616ecae86c5a27211a934fc2381322dfb20.json` | `627cc4f5f14c744faca5362d2f4783c89ec4e72cc863b6d22ee6d4bc894a2b5d` |

| Point | Role | Source request ID | Saved Q10(delta U), fraction |
| --- | --- | --- | --- |
| FPT-2023-07-03 | MT-BICL | `cc6bf729-784a-458a-8e40-07398fac513f` | NA |
| FPT-2023-07-03 | C2 | `NA (bypass)` | NA |
| HVN-2024-07-01 | MT-BICL | `ecf988b6-57a5-4601-98f8-ee7e9c64fe73` | 0.0027822661645950566 |
| MWG-2024-09-20 | MT-BICL | `80f57fde-498b-4fd3-975d-25ebc5973822` | -0.020861640105904133 |
| CMG-2023-07-03 | Native | `1493f745-e2fa-49bf-b0db-c7eb474ef9f1` | NA |

Kiểm từng ô facts/actions/outcomes, unit×100/×1000 khi trình bày, request/shared/policy/barrier, nguồnselection/support, links/footnotes/spec/diff. Docs-only không compileall/unit/E2E/leakage; không API/fit/replay/bootstrap. Không chọnoutcome cho nhóm đủ/thiếu/disagree/veto, không thêm giả lập để thay ca thật.

### 10.12. Sensitivity, thực thi và tài nguyên đã ghi

T46; CL174–CL180. B06f/g dùng ED07 `sensitivity`, cùng index20cột như `contrasts`: endpoint return/BA, baselineNative/Common và đủ5extension. L1/L3 `ci95[i]`, CORE4 `point[i]/ci95[i]` đãpp; LOFO/LOSO lấy min/max của6/9savedvector đúngindex, khôngCI/khôngredraw. CORE4points48/accounts24; L1/L3primary102/51. Mọi20cell/sensitivityfinite10000, không chỉ giữ vài contrast tốt. Các support và estimator giữ §5.5.

B05h ED35 pooled AS/B theo3cohort, ED34 n_accounts/return; n96/48account và54/27account không thayprimary102/51. ED28 `leave_one_block_out.AS_B_BA_delta` min/max×100 thànhpp. ED41 chọnall_102/AS-B/BA, lengths1/2/3 vàsavedpercentile; ED42 đủ6panel-HAC rows accuracy, lags0/1/2 trên96/54 cohorts, không nhầm vớiBA. B05i ED45 all_102/AS/B, khóa(dimension,stratum), cột n_units/metrics.balanced_accuracy×100. ED47 giữ SMA60±.02/trailing20/trainmedian vàpostinferencevol/liquidity; không suy HMM switching performance. Fullwidth summaries/higherdiagnostics vẫn có nguồn để mở App.D/T64, không chạy mới.

B05j ED43 đủ12scenario trong ED26 policy, AS/B n_accounts51, cột `mean_account_net_return_pct,blocked_attempts,pending_cash_accounts,residual_stock_accounts`. Returnđã%, countnguyên, cả120rows/10variants giữsource. ED44 zero certifiedfills vàevent/account audit; labels/predictionskhôngđổi. Các giảđịnhfee/slip/lot100/cap1%/advance15%/ACT365 đọc ED26, không tuyên bố pháp luật/quote hiện hành hoặc nofill bounds.

B07h ED18 `new/frozen_source` giữ attempts/successes/errors/prompt/completion/latency_seconds_sum; ledger ngoài375selectedoutputs được ghi rõ. Context ED07telemetry matched ED46wire `rows`1702, không lấy503carry. Mỗi HTTPmember tại `outputs/unified_integration/u08_research_r1/http/<id>.json` khớp rawmanifest và envelope.sha256 trong wire. Status1505/194/1/2; tổngobserved_tokens2986930, UNKNOWNreserve9177 khôngusage. Chỉ1700cặp completed_at/started_at hữu hạn: trừ timestamp để lấy duration, sum4056.744243621826s, median1.7145425081253052s, min.5543968677520752/max31.819045066833496; hai UNKNOWNuntimed giữmissing. Đây là thống kê trực tiếp trường đãlưu, không benchmark latency mới. Money/perrolebilledusage/wallclockmatched khôngcó, giữNA trongdiễngiải.

Đối soát toàn bộ ô/identity/unit/denominator, nguyênhash archive/source, links/footnotes/84spec/diff. Docs-only không compileall/unit/E2E/leakage, không execution/accountreplay, statisticalbootstrap, API hoặcfit. Các sốmin/max/median chỉ tổng hợp số đãlưu, không tínhlại estimatorperformance. T47 còn tổnghợpgiớihạn; không nâng trạngthái NativeFAIL/NOT_CERTIFIED/UIpending.

### 10.13. Giới hạn, ablation và trả lời RQ

T47; CL181–CL187. B06h đối chiếu ED07 `deferred_panels`: retrieval random/recent/similarity/bayesian, priorstats/examples/no_regime, MT Plain_revision/No_utility/No_target/Stats_only/Utility_only không có matchedhostedslots. No-prior/student separation mô tả câu hỏi chưa có kết quả, không bịa IDvariant đã chạy. Componentalpha/sentiment/placebo có panel nhỏ nhưng không thay matchedunified/main102. B09 tổng hợp đúngRQ outline, các bảng B05/B06/B07 và§5.8; mỗi observation nối CL145–180, không lấy số mới hoặc chọn riêng familytốt.

Audit source ED15 rawpin: `native_rowwise_causal_gate=FAIL`, `whole_system_causal_gate=NOT_CERTIFIED_HISTORICAL_EXPLORATORY`; `provider_support.bank_audit.records=852`, `donor_label_difference.count_above_1e_8=828`, `max_abs_percentage_points=.04298848884252138`, `raw_signal_journals_available=false`. Không diễn giải thành828nhãnđổi, khôngauthenticity từhash. ED15qualitylimits giữ NEWS_CONTENT_PIT_NOT_CERTIFIED/BANK_QUERY_SOURCE_TRANSFER/vendorlimits. ED04first/queuefreeze/lastrequest giữ historicalexposure; ED22SDK/modeloptions không suy immutableweights. ED08 `source_pins_verified=718`, `max_decision_prompt_characters_including_repair=4750`, `max_http_attempts_per_execution=3`, `suite_rerun=false`, `new_inference_requests=0`; scopeU08 khôngáp sangcomponentprovider-onlyoverride. U09coldreceipt §3.4 chỉofflinebyteidenticalreplay/0newAPI, phiên viết chỉ kiểmpin/receipt, không chạy lại replay. UI/F11 PENDING/F12chưađóng, không phảnbiệnngoài/nghiệmthunộp.

Tự kiểm P4: đủ§5.1–§5.9, nguồn hai collection vàscope/mean/account/repeat/bands/missing/fallback táchđúng; đủF09/F10source/vector/render đãxem, B04/B05/B06/B07/B09 cólocator. Đối soát84spec/checkedT01–T47, CLliêntục, footnotes/links/units/sourcehash/diff. Bảng cònMarkdown, App.D/T64 vàCSV/LaTeX/T69 chưa triểnkhai. Không đánhG3hoàntất vìT48–T58còntổngquan/introduction/conclusion; P4đủbảnnháp không đồngnghĩa khóa luận/nguồncuối/acceptance hoànthành. Khôngthayruntime/test/config/schema/input/sourcearchive; không compileall/unit/E2E/leakage/fit/API/bootstrap/executionreplay. Hai script mới phục vụhình được biên dịchriêng tạiT43/T44.

## 11. Nguồn tổng quan tài liệu và định vị

### 11.1. Phạm vi đọc, metadata và luận điểm được hỗ trợ

Ngày **16/11/2026**, T48: tạo [thesis/references.bib](references.bib) gồm **22 nguồn** được đối chiếu metadata và đoạn hỗ trợ dưới đây. Đây là tập được nhận vào bibliography cho phần viết, không phải toàn bộ ứng viên đều đã đọc. Nguồn học thuật dùng bản tác giả/arXiv có version hoặc proceedings/journal gốc; các mirror đại học chứa bản bài báo gốc, không dùng bình luận thứ cấp thay nội dung. Chỉ các phần ghi ở cột locator đã được dùng để kiểm phát biểu; không tuyên bố kiểm toàn bộ proof/thực nghiệm/quyền phát hành. PDF scan Holm pp65–67, Newey–West p703 và Politis–Romano p1303 được xem ảnh trực tiếp; tải thành công không tự thành trạng thái đã đọc. Các bản tải để đọc nằm ở tmp, không phân phối toàn văn trong Git.

Khóa `tradingagents2024` giữ ổn định nhưng edition được trích là v7 năm2025; `muller2022transformers` dùng năm venue ICLR2022, ghi rõ văn bản kiểm là arXivv7 sửa năm2024. MT-BICL trích preprintv1; không suy final pagination từ footer/comment ICML. Hamilton dùng manuscript18May2005, không trộn metadata edition Palgrave khác. ViSoBERT dùng tên trên PDF (Quoc-Nam Nguyen, Thang Chau Phan, Duc-Vu Nguyen, Kiet Van Nguyen); ACL export dùng dạng rút gọn. TradingAgents PDF/abs xác nhận Xiao/Sun/Luo/Wang; tên Einstein/Tesla/Newton/Rus trong HTML thử nghiệm là nội dung template, không đưa vào bibliography. DOI chỉ điền khi đã có định danh xác thực; không tạo DOI cho Holm/White từ phỏng đoán. Trang catalogue hoặc OpenReview challenge không được ghi là đã đọc toàn văn tại đó.

Nguồn phần mềm QuantAgent trích riêng paper: commit92519f8 là mốc đối chiếu, ngày08May2026, không phải adopted commit đã biết. README root và THIRD_PARTY_NOTICES giữ nguyên; không áp license cho additions/datasets/weights chỉ từ MIT của upstream. Model card 5CD pin cả README và config, không tải/chạy weights. Key/metadata/locator/scope/limit dưới đây là ánh xạ luận điểm–trích dẫn; cite dùng `[@key]`, chuyển sang LaTeX ở giai đoạn sau.

| ID / khóa | Nguồn gốc đã kiểm | Edition/version | Đoạn hỗ trợ | Phát biểu được hỗ trợ (English) | Giới hạn |
| --- | --- | --- | --- | --- | --- |
| R01 / `lo2000technical` | [Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation](<https://business.columbia.edu/sites/default/files-efs/pubfiles/19268/Lo-Mamaysky_wang_foundations.pdf>) | 2000 | Trang bìa, abstract, Introduction và mô tả nhận dạng pattern tự động; NBER Working Paper 7613, March 2000. | Technical patterns can be defined algorithmically and studied through conditional return distributions. | Không chuyển phát hiện thống kê ở mẫu Mỹ thành lợi nhuận hay bằng chứng Việt Nam. |
| R02 / `kakushadze2016formulaic` | [101 Formulaic Alphas](<https://arxiv.org/abs/1601.00991v3>) | 1601.00991v3 | §2–§3 và Appendix A, nhất là rank/correlation/indneutralize và ts operators; record arXiv v3 có journal reference. | Formulaic alphas distinguish cross-sectional operators from temporal operators. | Bản một mã là phép thích nghi; không đồng nhất proxy VWAP hay temporal rank với công thức gốc. |
| R03 / `pedregosa2011sklearn` | [Scikit-learn: Machine Learning in Python](<https://jmlr.org/papers/v12/pedregosa11a.html>) | 2011 | PDF trang 1–3: author list, abstract, §1–§3; publication record JMLR12/2825–2830. | Scikit-learn provides a common implementation environment for supervised learning controls. | Paper thư viện không xác định hyperparameter/version của thí nghiệm đã khóa. |
| R04 / `xiong2025quantagent` | [QuantAgent: Price-Driven Multi-Agent LLMs for High-Frequency Trading](<https://arxiv.org/abs/2509.09995v3>) | 2509.09995v3 | PDF §3/§3.1.1–§3.1.3, Fig.2–3, §4: price-only, chart roles, Risk/Decision và benchmark1h/4h. | QuantAgent supplies the price-driven specialist-agent foundation; its reported task differs from daily LONG/CASH evaluation. | Không lấy title HFT làm mô tả tốc độ hệ hiện tại, không nhận vai trò thị giác/đa agent là mới. |
| R05 / `yresearch2026quantagentcode` | [QuantAgent source repository: comparison snapshot](<https://github.com/Y-Research-SBU/QuantHarness/tree/92519f806286192345e940e7ab77496462d662b7>) | 92519f806286192345e940e7ab77496462d662b7 | Git object commit92519f8, README/agent/tool paths; THIRD_PARTY_NOTICES và LICENSES/QuantAgent-MIT.txt; raw README tải đúng pin. | Agent, chart-tool and orchestration code is adapted from the upstream comparison snapshot. | Mốc đối chiếu khác commit thật đã tiếp nhận; rename QuantHarness không thay paper v3. |
| R06 / `tradingagents2024` | [TradingAgents: Multi-Agents LLM Financial Trading Framework](<https://arxiv.org/abs/2412.20138v7>) | 2412.20138v7 | PDF title page, §3–§4, §5.1: teams/debate/communication và simulation; arXiv abs author/version. | TradingAgents organizes financial analysis, debate, trading and risk management through specialized teams. | HTML thử nghiệm có tên template; dùng bốn tác giả của PDF/abs. Không nhập returns của bài vào bảng thesis. |
| R07 / `fatemi2024finvision` | [FinVision: A Multi-Agent Framework for Stock Market Prediction](<https://arxiv.org/abs/2411.08899v1>) | 2411.08899v1 | PDF §3.1–§3.4, §4.1–§4.2: news, charts, textual/visual reflection, BUY/SELL/HOLD và evaluation. | FinVision combines news, chart analysis and reflection before a trading recommendation. | Reflection không tự là Bayesian posterior hay task-aware student; simulation khác hợp đồng thesis. |
| R08 / `han2023chartllama` | [ChartLlama: A Multimodal LLM for Chart Understanding and Generation](<https://arxiv.org/abs/2311.16483v1>) | 2311.16483v1 | Abstract, §3 data/instruction construction, §4.2 benchmark/tasks; arXiv v1. | Chart understanding can be studied as its own data, instruction and evaluation problem. | Không coi chart benchmark là kiểm định candlestick trading; thesis không dùng ChartLlama weights. |
| R09 / `nguyen2023visobert` | [ViSoBERT: A Pre-Trained Language Model for Vietnamese Social Media Text Processing](<https://aclanthology.org/2023.emnlp-main.315/>) | 2023 | PDF trang5191/§3–§4 corpus/tasks; ACL venue/pages/DOI; tên đầy đủ theo PDF, không mở rộng từ suy đoán. | ViSoBERT is a Vietnamese social-media backbone, distinct from the downstream 5CD sentiment classifier. | Không chuyển social-media task scores thành độ chính xác tin tài chính của Sentiment Agent. |
| R10 / `hf5cdsentiment` | [Vietnamese-Sentiment-visobert: Model Card and Configuration](<https://huggingface.co/5CD-AI/Vietnamese-Sentiment-visobert/blob/d7738b85200272f10ba8b048d80236c8c582b581/README.md>) | d7738b85200272f10ba8b048d80236c8c582b581 | README Dataset/Evaluation và config.id2label đúng revision d7738b8; không tải/chạy weights. | The pinned classifier supplies three sentiment labels from a separate fine-tuning resource. | Card không chứng nhận financial-domain calibration, news availability hoặc quyền toàn hệ. |
| R11 / `rabiner1989hmm` | [A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition](<https://web.mit.edu/6.435/www/Rabiner89.pdf>) | 1989 | §II/§III.A–C: state/transition/emissions, forward/backward, decoding và model reestimation; title/page metadata. | HMMs separate latent state transitions, observation likelihoods and inference or fitting problems. | Nguồn speech HMM không xác nhận số state, tên regime hoặc tác dụng giao dịch của VN-Index model. |
| R12 / `hamilton2005regimes` | [Regime-Switching Models](<https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf>) | 2005 | Manuscript18May2005, phần mô hình/transition/filtering và maximum-likelihood recursion, eqs.1–10. | Economic regimes can be modeled as latent states with state-dependent time-series behavior. | Dùng đúng manuscript2005, không gán metadata edition sách chưa đối chiếu; không chứng minh state tài chính thật. |
| R13 / `xie2022implicitbayes` | [An Explanation of In-context Learning as Implicit Bayesian Inference](<https://arxiv.org/abs/2111.02080v6>) | 2111.02080v6 | §2 assumptions, §3.1–§3.3 statement/interpretation, §4 GINC; không khẳng định đã kiểm lại toàn bộ proof. | An implicit-Bayes account is established under a mixture-of-HMMs pretraining setting with explicit assumptions. | Không dùng theorem này để chứng nhận arbitrary LLM prompt, finance HMM hoặc calibration. |
| R14 / `rubin2022retrieve` | [Learning To Retrieve Prompts for In-Context Learning](<https://aclanthology.org/2022.naacl-main.191/>) | 2022 | PDF abstract/§2–§3 retriever training và §4 semantic-parsing setup; ACL metadata. | Example retrieval can itself be learned using language-model-based supervision. | Không gọi B_semantic trong repo là dense retriever của Rubin; không suy hiệu quả trong tài chính. |
| R15 / `muller2022transformers` | [Transformers Can Do Bayesian Inference](<https://arxiv.org/abs/2112.10510v7>) | 2112.10510v7 | Title page/§3 Algorithm1 prior-data NLL/§4 architecture; record arXivv7 đối chiếu nămvenue2022 và revision2024. | PFNs amortize predictive inference by training on datasets sampled from a chosen prior. | Không đồng nhất PFN với generic LLM hoặc coi PFN này là checkpoint tài chính của thesis. |
| R16 / `zhu2026multitask` | [Multi-Task Bayesian In-Context Learning](<https://arxiv.org/abs/2606.20538v1>) | 2606.20538v1 | §4 representation/objective, §5.1 synthetic setup, §5.5 ERA5 và AppendixC GPT2 config. | Prior datasets and target observations are represented separately to adapt hierarchical predictive inference across priors. | Nguồn ý tưởng MT-BICL, không nguồn cho stock-return guarantee; paperconfig8/8 khác student2/4 nội bộ. |
| R17 / `varma2006bias` | [Bias in Error Estimation When Using Cross-Validation for Model Selection](<https://link.springer.com/article/10.1186/1471-2105-7-91>) | 2006 | Abstract, Background, Results/Discussion, Conclusion; publisher DOI và PDF8trang. | Using the same cross-validation score for tuning and evaluation can produce optimistic error estimates. | Microarray experiments không chứng minh nested random CV hợp lệ cho mọi time series; thesis không chạy lại nestedCV. |
| R18 / `white2000reality` | [A Reality Check for Data Snooping](<https://users.ssc.wisc.edu/~behansen/718/White2000.pdf>) | 2000 | Abstract/§1 và phần bootstrap testing setup; PDF journal copy pp1097–1126. | Specification search requires accounting for data reuse when evaluating predictive superiority. | Không gọi band mô tả hiện có là đã chạy White Reality Check hoặc có adjusted confirmation. |
| R19 / `politis1994stationary` | [The Stationary Bootstrap](<https://users.ssc.wisc.edu/~bhansen/718/Politis%20Romano.pdf>) | 1994 | Scan xem trực tiếp p1303: abstract/§1/đầu§2; publisher DOI/Crossref cho metadata. | Dependent-data resampling uses blocks under stationarity and weak-dependence assumptions; stationary bootstrap has random block lengths. | Chỉ đọc phần nêu trên, không claim proof được kiểm; fixed-length circular blocks của thesis khác stationary bootstrap. |
| R20 / `holm1979multiple` | [A Simple Sequentially Rejective Multiple Test Procedure](<https://sci2s.ugr.es/keel/pdf/specific/articulo/0052_001.pdf>) | 1979 | Scan xem trực tiếp pp65–67: §1–§2/Scheme1/Theorem1 và proof bằng Boole. | The sequential Bonferroni procedure controls family-wise error when the individual tests satisfy their validity requirements. | Holm không sửa p-values sinh từ symmetry/exchangeability chưa xác nhận; không tự xác nhận family23 của thesis. |
| R21 / `newey1987hac` | [A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix](<https://www.ssc.wisc.edu/~bhansen/718/NeweyWest1987.pdf>) | 1987 | Scan xem trực tiếp p703/eqs.1–4: covariance/regularity motivation; Crossref DOI metadata. | HAC covariance estimation addresses heteroskedasticity and autocorrelation under regularity conditions. | Không claim đã đọc toàn theorem/proof hoặc finite-sample calibration cho6exposedfolds. |
| R22 / `arnott2019backtesting` | [A Backtesting Protocol in the Era of Machine Learning](<https://people.duke.edu/~charvey/Research/Published_Papers/SSRN-id3275654.pdf>) | 2019 | Author version abstract/protocol categories, implementation shortfall và structural changes; Crossref journal record2019. | Financial research protocols should address selection, implementation costs and nonstationarity before deployment claims. | Đây là căn cứ thiết kế/giới hạn, không phải chứng nhận prospective hay receipt lịch sử của hệ này. |

Hash bản đọc để truy vết, không thay version/metadata và không chứng nhận nội dung nguồn:

| Khóa | Dạng bản đọc | Byte | SHA-256 nguyên byte |
| --- | --- | --- | --- |
| `lo2000technical` | PDF | 676351 | `df3cb4ceddc3e23dd4833f0871bd556c19fa661027ed03facce00f6a72ccdb74` |
| `kakushadze2016formulaic` | PDF | 244416 | `1f9c21afe32dcb3ee77b31548acdaea00451fbfa1c0ee10c907867bcc736fce9` |
| `pedregosa2011sklearn` | PDF | 42310 | `1c338a6b3c6c1dcafda3990a8098b8b50dd6c77616361396fb75f6822c6e0778` |
| `xiong2025quantagent` | PDF | 4767772 | `05652d9dd2887c86bf470fdb424c49e5bb12ca1e839510968eb43fb6a4b55760` |
| `yresearch2026quantagentcode` | pinned README | 12109 | `e5732eef7ee52ad96b8d70629632f3067616175d76e5a8b05520f87086df70d2` |
| `tradingagents2024` | PDF | 1903362 | `431d0c39365b4c46b43162371fa15b3dcf8d142b377d642b3e5925dc81f3487b` |
| `fatemi2024finvision` | PDF | 770109 | `8483714696f009ffecd5e818ce2b8937e88be03343476bb23344b4f38b080921` |
| `han2023chartllama` | PDF | 2627897 | `a3d947e6ba338d2de546f49ddb5ad4da45a3137b27dab1459dfac24d64790a37` |
| `nguyen2023visobert` | PDF | 521767 | `72a802681a6f4a83fb909a4779c67e8700a20ad6acd0e4048ea91776b33b08a1` |
| `hf5cdsentiment` | pinned README | 14326 | `2ce2dbf61f24751136f7af2080f88efe5dd823389e9873206e8f59ea662333cc` |
| `rabiner1989hmm` | PDF | 2754043 | `d5cb7e282741d6ace368bab6260acc5eb5a4decbc6b984a7f0f1a73c9c22517c` |
| `hamilton2005regimes` | PDF | 158535 | `447e3fa98699bddfa1bc5692c2949ae0a8c3ed6406eb44b189dcf40a5d826721` |
| `xie2022implicitbayes` | PDF | 1240973 | `ad9be01798fcf4fdc66ff3630f7a6f1cc157c04d51d0821d7798e028cb175c4b` |
| `rubin2022retrieve` | PDF | 1115072 | `0b88f05530aa4e233a1560ea96844c068d6a56d5938b0cf0a7e8b64ccfdfc2a1` |
| `muller2022transformers` | PDF | 1271614 | `9736e7789e7f4b7dd7401b6017602be87410eb15c1b11f94065d88ba7fec5a9b` |
| `zhu2026multitask` | PDF | 7576663 | `35e78229b2a7c89507f218901114baeb2385e2bcf566ec6166e0ef83f4080e0f` |
| `varma2006bias` | PDF | 243814 | `573198025179f340870428087dd3a980a5c2cbdab890ace3d155e0cf8fcd6e1b` |
| `white2000reality` | PDF | 259584 | `675eb3226dee3af4dfa8089410f9bbf0a2798c7b58985c8334c42fb4983a9743` |
| `politis1994stationary` | PDF | 1984053 | `269f5437920af4861360d4e1a74a77f3aa6a3d3f070cd52a9f0e8502822a5c35` |
| `holm1979multiple` | PDF | 533148 | `eb4b0014bcb5e8d371092035c31a873b2ee55bdcdcbbc4a7ff7b508d9787884c` |
| `newey1987hac` | PDF | 539596 | `64cca3ea37246ab27f8d5a537cd101a2adb9d1463091b29c23f1127eff5fd192` |
| `arnott2019backtesting` | PDF | 291336 | `2ebced0662e2ced12d8ab28297e1f7a97bda597d350ca86b774f5de7a3ba4144` |

Config5CD cùng revision d7738b8 có id2label0/1/2=NEG/POS/NEU; bản đọc rawconfig SHA-256 `04499fbdf5bb3ff5c93abf63c845670387485fdd16e9472847f1168a5dda102b`. Metadata Crossref đối chiếu Lo journal record (nhưng bibliography dùng NBER7613), Newey–West, Politis–Romano, Varma–Simon và Arnott et al.; nội dung nghiên cứu vẫn lấy bài gốc, không lấy Crossref làm bằng chứng phương pháp. Arnott/Harvey/Markowitz dùng bản tác giả29Oct2018, gắn record journal2019 được kiểm; DOI/volume/pages giữ đúng record.

Kiểm BibTeX bằng parser BibTeX thực trong thư mục tạm, keys duy nhất/cân bằng và metadata bắt buộc; không tạo PDF toàn văn. Không chép `paper/references.bib` hoặc bibliography mẫu. T48 không sửa Chương3–5, runtime hoặc artifact thực nghiệm; không compileall/unit/E2E/leakage suite, không fit/API LLM/replay. Các kết luận mạnh hơn locator cần đọc và đối chiếu thêm, không suy từ trạng thái DA_KIEM.

### 11.2. Phân tích kỹ thuật, alpha và đối chứng

T49; CL189–CL192, R01–R03/R17. §2.1 phân biệt feature/report/action và chứng cứ ngoài mẫu; attribution Alpha101 dựa AppendixA, phần thích nghi dựa CL043–CL047/SYS/BG đã khóa. Lo et al. là nguồn empirical pattern testing, không chứng minh strategy Việt Nam. Paper scikit-learn chỉ nhận diện software environment; recipe logistic/factor controls vẫn theo Chương5. Varma–Simon hỗ trợ cảnh báo selection bias, không biến nested random CV thành nghiệm thu temporal protocol. So sánh phương pháp thay vì liệt kê công thức; không thêm số kết quả, citations chưa đọc hoặc tài liệu runtime mới. Kiểm keys/locators, placeholder còn lại, footnote/link/84spec/diff; chỉ tài liệu nên không compileall/unit/E2E/leakage hoặc study replay.

### 11.3. LLM/VLM đa agent và attribution

T50; CL193–CL197, R04–R10. §2.2 xác định QuantAgent là arXiv2509.09995v3; paper§3.1.3 có RiskAgent và DecisionAgent riêng dù abstract nêu bốn specialists. Input/charts/benchmarks và chính sách stop-loss/take-profit của paper không thay oracle LONG/CASH daily của thesis. Source pin92519f8 đối chiếu README đã tải và Git object/local notices, không đổi source hiện hành hoặc bịa adopted commit. TradingAgents v7§3–5.1 dùng để so organization/communication; FinVision v1§3 dùng để so reflection/multimodality. Không xếp hạng returns giữa các paper hoặc ghi họ không có PIT chỉ vì chưa audit độc lập. ChartLlama là nguồn cho chart-task distinction, không nguồn của modelvision đã chạy. ViSoBERT/5CD giữ riêng backbone/classifier/domain/pin; không suy financialaccuracy từ task scores. Kiểm citation/locator/keys, 84spec/footnote/link/diff; các chương khác và runtime giữ nguyên, không suite/compileall/inference/fit.

### 11.4. Regime, ICL và MT-BICL

T51; CL198–CL204, R11–R16. §§2.3–2.5 trình bày HMM/Markov-switching như mô hình latent-state, khác threshold strata và nguồn regime cụ thể trong thesis. Rabiner forward/backward và Hamilton filtering chỉ ra vì sao phải giữ thông tin/fitting cutoff; không dùng lý thuyết để ghi Native causal PASS. Xie: mixture-HMM pretraining/latent concept/giả định distinguishability, không chứng minh mọi LLMfinance Bayes. Rubin: LM-supervised dense retrieval trong semantic parsing, không bằng tên B_semantic của repo. PFN Algorithm1/prior-data NLL khác generic prompt; MTpaper§4 tách prior datasets/target/query và target-task likelihood. AppendixC sourcepaper synthetic8layers/8heads khác local2blocks/4heads.

Điểm triển khai đối chiếu Chương4.8/CL078–CL101: teacher16Beta components dùng label counts, student distill teacher probability ởQ; feature vectors độc lập latent/label tổng hợp. Input/membership/projection/teacher/student/hostedLM/policy giữ vai trò riêng; không đổi checkpoint hoặc fit. Sourcepaper regression/ERA5 không cung cấp stockprofitability. Kiểm câu/citation/locator, không import learner/retriever/model để viết; key/footnote/link/spec/diff PASS. Hai section §2.6–§2.7 còn placeholder để viết tại T52–T53.

### 11.5. Backtest, phụ thuộc và tái lập

T52; CL205–CL209, R17–R22 và hợp đồng nội bộ. §2.6 dùng Arnott/Harvey/Markowitz cho research-protocol/implementation-cost rationale, White cho data snooping/specification search, Varma–Simon cho optimistic error after tuning. Không gán purging theo holdinginterval của repo thành thuật toán đã chứng minh bởi bài microarray, và không nói đã chạy White Reality Check. Politis–Romano p1303 nêu stationarybootstrap với randomgeometriclength và weakstationarity; fixedcircular/wholefold đang lưu khác cách dựng đó. Newey–West p703 chỉ được dùng cho HAC motivation/regularity, không claim đã kiểm toànproof hoặc coverage6folds. Holm pp65–67/Scheme1/Theorem1 yêu cầu valid tests, không tự sửa underlying sign-exchangeability. Phần pairing/ablation và source/input/checkpoint/replay dùng binding nội bộ Chương3–5, giữ NativeFAIL và các giới hạn lịch sử. Kiểm citation/key/locator/footnote/link/spec/diff; docs-only không compileall/unit/E2E/leakage/bootstrap/API LLM/fit/replay.

### 11.6. B08 và định vị đóng góp

T53; CL210–CL213. B08a từng hàng/cột: QuantAgentR04§3–§4 cho inputs/charts/Indicator–Pattern–Trend–Risk/Decision, 1h/4h/futurebars và directional contract; TradingAgentsR06§3–§5.1 cho teams/debate/structured communication, UStech/backtest/actions và author-stated availability; FinVisionR07§3.1–§4.2 cho news/chart/reflection/dates/BUY-SELL-HOLD/size. Các trường temporal/economic chỉ mô tả nội dung đọc, không đánh PASS/FAIL cho paper khác hoặc suy không có guard từ sự vắng mặt trong đoạn đọc. Rowthesis theo CL025–CL028/CL064–CL101 và Chương5, giữ oracle/cost/account và NativeFAIL/NOT_CERTIFIED.

B08b từng hàng: XieR13§2–§4 cho latentconcept/mixture-HMM/GINC; RubinR14§3–§4 cho LM-supervised dense retrieval/semanticparsing; PFNR15§3–§4/Algorithm1 cho prior-dataNLL và predictiveapproximation; MTR16§4/§5.1/§5.5 cho taskboundaries/priorprefix/hierarchicalobjective và regression/ERA5. Rowthesis dùng numerical/hosted/policy tách biệt, teacher/student khác originalrecipe và giới hạn hiệu quả từ Chương5. Không đánh mọi ô theo cùng một financialbenchmark khi nguồn không có. Cả hai panel B08 nằm trong Markdown, CSV/LaTeX và rà soát kích thước bảng ở T70/T74 sau; chưa tạo bảng LaTeX hoặc PDF toàn văn.

Khoảng trống được định vị cho tích hợp và phép đo đã triển khai, không surveyexhaustive/globalpriority. Kết quả không bị viết lại để khớp narrative: tám returnngữcảnh âm, v1 phụ thuộc baseline/support, MTgiữanchor, NativeFAIL, provenance và missingablations còn nguyên. Kiểm từngcâu/ô/citation/key/locator so nguồn và các chương đã khóa; 84spec giữnguyên, không code/runtime/test/config/schema/input/model/receipt đổi. P5 đủ bản nhápChương2/bibliography, chưaG3toànbộ doT54–T58 chưaviết, chưaphảnbiệnngoài hoặc dàntrangcuối. Docs-only không compileall/unit/E2E/leakage/fit/API LLM/replay.

## 12. Mở đầu, kết luận và đối soát lập luận

### 12.1. Động cơ và bài toán

T54 viết §§1.1–1.2 cho người đọc kỹ thuật chung. CL214–CL216 nối nguồn gốc R01/R02/R04/R16/R22 đã đọc tại §11.1 với hợp đồng §§3.1–3.2/4.7–4.10 và hai nghiên cứu Chương 5. Chỉ dùng các luận điểm/phiên bản đã kiểm, bibliography giữ nguyên 22 mục. Sơ đồ Mermaid inline là sơ đồ bài toán dẫn xuất từ F01/F02/F03/F07, không thêm ID vào danh mục 23 hình/bảng/thuật toán, không phải dữ liệu hoặc hình thực nghiệm mới. Đầu vào tương lai chỉ nối tới evaluator sau forecast barrier; fallback và lỗi kỹ thuật tách biệt. Giữ 3 phiên, hai chiều phí/slippage, candidate-LONG UP/DOWN khác CASH, intended PIT khác Native causal FAIL. Chưa dàn trang sơ đồ; việc chuyển LaTeX và kiểm hiển thị cuối thuộc P8/P9.

Đối soát câu/nguồn, RQ theo outline, liên kết/anchor, footnote, citation-key, 84 đặc tả bất biến và diff theo phạm vi. Chỉ tài liệu nên không chạy compileall/unit/E2E/leakage; không fit/API LLM/replay/bootstrap hoặc sửa input/receipt.

### 12.2. Câu hỏi, phạm vi và đóng góp

T55 viết §§1.3–1.5/CL217–CL220. Bốn câu hỏi lấy nguyên văn outline §A.2; bảng overview chỉ là bản đồ câu hỏi–phép so–bằng chứng, không thêm kết quả hoặc ID hình/bảng. RQ1 giữ Base và controls/panels riêng; RQ2 giữ hai đối chứng Native/Common, readiness và fallback; RQ3 là combined bridge, chưa tách student/target/utility; RQ4 là đối soát hợp đồng. Bốn loại đóng góp khớp outline §A.4, mỗi loại có vị trí triển khai, nguồn kế thừa và kết quả/giới hạn. Đối soát đúng mục chương và source, không suy lý thuyết mới hoặc hoàn thành ablation còn thiếu. §1.4 giữ chín cổ phiếu/sáu fold đã lộ, một upstream mỗi điểm, 2448 slots có phụ thuộc, các trạng thái FAIL/NOT_CERTIFIED/PENDING.

Chương 1 đủ bản nháp, chưa phản biện ngoài/dàn trang cuối. QA source/citation/RQ/links/spec/diff; runtime và bibliography không đổi, không suite hoặc nghiên cứu mới.

### 12.3. Tóm tắt phương pháp và câu trả lời

T56 viết §§6.1–6.2/CL221–CL226, trả lời nguyên văn bốn RQ theo §1.3/outline §A.2, nối B09 trong §5.9.3. Mỗi số đối chiếu lại B05a–b/B06a–e và §5.8.2; giữ phần trăm khác pp, account means khác portfolio, hai nghiên cứu/estimators riêng, family20 contrasts và L1 khác primary. B09 giờ có tổng hợp trả lời tại Chương 6, không sao thêm bảng kết quả hoặc dựng band mới.

Đọc lại nguyên byte U09 ZIP SHA256 `e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9`, ED07 `3136ab9bdeab377196236e1a01402646257ec3beb251877702dbc86e1e67e31f`, revision index `cc4400dadc585b6b0dd5dd3a012f1f510a994347b9395cdbbcc721cc9f2b9599` và baseline manifest `0a20fbe49049dd61fae2eb8bf3289f65039395e6bcac6745b851a5a00d804226`. Hai member component summary/main_cohorts đọc từ archive bằng EvidenceArchive khớp byte với nguồn P4, hashes lần lượt `46782716a0770c9589056fbcf499b60f738c7243647e9a378f91e01656c04299` và `68eafd80dfa067b31d9f6cfdafdb536f82109d9bc8c8244b374bde6b4007e5d6`. Đây là kiểm nguồn đọc-only, không phải chạy lại analysis hoặc suite. So số/nguồn, câu trả lời/boundaries, attribution, citation/footnote/link/84 spec/diff PASS; chưa viết §§6.3–6.4, chưa review ngoài/dàn trang cuối.

### 12.4. Hạn chế và ưu tiên nghiên cứu tiếp theo

T57 viết §§6.3–6.4/CL227–CL230. Giới hạn nối trực tiếp §§5.8–5.9: Native row-wise FAIL, nguồn bank/query/news và raw journals thiếu; 828/852 là khác return chứ không phải nhãn đổi; sáu fold đã lộ và repeats cùng upstream; thiếu support/matched ablations; daily bars/scenarios không xác thực fills/portfolio; UI chưa nghiệm thu. Không thêm kết quả hoặc diễn giải all-clear từ hash/receipt.

Thứ tự ưu tiên là diễn giải đề xuất: (1) causal/provenance trước bằng nghiên cứu version riêng, (2) coverage/chart/news validation, (3) registered matched retrieval/prior/MT/student/utility ablations, (4) protocol đóng băng và giai đoạn chưa lộ với precision theo phụ thuộc, (5) execution/portfolio/UI theo đúng phạm vi. Mỗi bước nói bằng chứng cần thêm, không coi là task đã chạy hoặc cho phép sửa archive hiện tại. Chương 6 đủ bản nháp, chưa tự kiểm toàn mạch T58, review ngoài hay typesetting. Kiểm nguồn/câu/đơn vị/link/footnote/84 spec/diff; chỉ tài liệu nên không suite/fit/API/replay/bootstrap.

### 12.5. Đối soát toàn mạch và tự kiểm G3

T58 đọc nối câu hỏi/mục tiêu §§1.1–1.5 → định vị §2.7 → hợp đồng/khái niệm §§3.1–3.2/3.6–3.7 → luồng/policy/điều phối §§4.1/4.5–4.10 → thiết kế, kết quả và B09 §§5.1–5.9 → trả lời/giới hạn/ưu tiên §§6.1–6.4. Tự kiểm tập trung mạch lập luận và truy vết, không thay cho rà khoa học/ngôn ngữ toàn văn hoặc đánh giá ngoài. CL231–CL232 ghi phạm vi.

| Điểm kiểm | Chuỗi đối chiếu | Kết quả và chỉnh sửa |
| --- | --- | --- |
| Tên đề tài và attribution | Frontmatter/outline §A; §§1.1/1.5/2.7/4.8/6.1–6.2 | Cùng hướng nghiên cứu, không hàm ý gain; multi-agent khác multi-task, HMM/Beta/QuantAgent/Alpha101/student-source có attribution; không đổi bìa/metadata |
| RQ và đóng góp | Outline §A.2/§A.4 → §1.3/§1.5 → B09 → §6.2 | Bốn câu hỏi nguyên văn và bốn loại đóng góp cùng mức bằng chứng; kiểm đúng số mục trong overview và contribution map |
| Kinh tế và terminology | §§1.2/3.2/4.9/5.5/6.1 | LONG/SHORT proposal khác LONG/CASH action, UP/DOWN là candidate-LONG; ba phiên, hai chiều phí/slippage, không portfolio; rút phần định nghĩa lặp ở §6.1 về tham chiếu §3.2 |
| Temporal boundary | §§1.2/3.7/4.2/4.5/4.9/5.9/6.3 | Ngày xuất bản và protocol availability đều cần ≤ cutoff, exit lịch sử < cutoff; làm rõ §1.2 theo §3.7, outer cutoff không phủ nhận Native FAIL |
| RQ1 và hai nghiên cứu | §§1.3/4.4/5.1/5.6/6.2.1 | Không trộn Base với Native/Common hoặc response/estimator; +3.247 pp BA, interval qua 0, −0.047 pp return và logistic/CASH controls giữ nguyên |
| RQ2/context support | §§4.5–4.7/5.7/5.8.1/5.8.4/6.2.2 | Hai baseline, family20, fallback trong primary, C2/B chỉ ba replies, L1/Common band qua 0 và cả tám means âm; không chọn subset hoặc suy regime causal gain |
| RQ3/policy | §§3.6/4.8/5.7.5/5.8.2/6.2.3 | 108+189+5+4=306, 302 giữ anchor, bốn accepted slots/ba unique points; +0.033 pp bridge không tách student/target/utility; matched ablations vẫn thiếu |
| RQ4 và tương lai | §§4.9–4.10/5.8–5.9/6.2.4/6.3–6.4 | Receipt theo scope; Native FAIL/NOT_CERTIFIED/UI PENDING không đổi; 828/852 return khác không thành changed labels; repairs/ablations/tiền cứu/portfolio/UI chưa chạy |
| Chuyển đoạn và định nghĩa | §§1.3/3.3/3.6/3.7/5.1/5.9/6.1 | Thay future-draft wording bằng chỉ dẫn mục đã có, nối Ch.3→4→5 và B09→Ch.6, rút diễn giải lặp sau bảng RQ; không đổi phương pháp/kết quả |

**G3 — tự kiểm nội bộ đạt trong phạm vi T36–T58:** các kết quả, tổng quan, RQ, đóng góp và kết luận khớp với nguồn đã có; các nhận định vượt nguồn đã được loại trừ/thu hẹp, việc nghiên cứu mới tách riêng là tương lai. Đây không phải phản biện/duyệt của giảng viên hoặc hội đồng, không là bốn gate runtime chạy lại, và không đổi trạng thái Native FAIL/whole-system NOT_CERTIFIED/UI F11 PENDING. P6 đủ bản nháp và đối soát mạch, chưa hoàn thiện khóa luận/P7–P10.

QA cuối: 84 dòng đặc tả giữ nguyên; checklist T01–T58, T59 trở đi chưa đánh dấu; bốn RQ đối chiếu nguyên văn, title metadata/covers giữ nguyên; citation keys/bibliography, footnote và local links/anchors hợp lệ. Bảng/công thức/JSON/pseudocode/số liệu nguồn Chương 2–5 bất biến; chỉ chuyển đoạn văn ở Chương 3/5. Hash U09/member/revision/baseline kiểm tại §12.3, không sửa archive/receipts/models/inputs/code/runtime. Tài liệu thuần túy nên không compileall/unit/E2E/leakage suite, không fit/API LLM/resampling/replay. Hình và Mermaid chưa được dàn trang/kiểm trong PDF toàn văn, thuộc P8/P9.

**Số kiểm P6 cuối:** 84 đặc tả bất biến; CL001–CL232 liên tục; 117 footnote/6 chương; 777 liên kết local và 401 anchor hợp lệ; 22 bibliography entries giữ nguyên. Bốn RQ nguyên văn và title/covers metadata khớp; số tóm tắt v1/bridge/policy/BA đối chiếu nguồn đã khóa. Chỉ 9 file Markdown được sửa; Chương 2/4, mọi bảng/math/code block Chương 2–5 và toàn bộ code/runtime/asset/receipt giữ nguyên. Không chạy suite theo phạm vi tài liệu.

## 13. Phần đầu và phụ lục

### 13.1. Abstract và keywords

T59 viết abstract tiếng Anh và bảy keywords trong `frontmatter.md`; CL233–CL236 ánh xạ tới các chương đã hoàn tất. Chưa có giới hạn từ chính thức; độ dài hiện tại là lựa chọn biên tập, không gán thành quy định trường. Abstract tự đứng được, không citation/footnote/task ID, nêu bài toán → phương pháp → hai thiết kế/đơn vị → kết quả chính → giới hạn/đóng góp. Không đổi phần bìa hoặc metadata đã xác nhận, không thêm kết quả hoặc trích dẫn nguồn mới.

Đối soát số tóm tắt với §§5.6–5.9/B09 và §§6.1–6.4, giữ pp khác %, paired repeats có phụ thuộc, Full/Base khác Native/Common, account means khác portfolio; +3.247 BA không thành return gain, v1 phụ thuộc baseline, MT mostly-anchor và cả tám mean âm. Kiểm lại nguyên byte U09 ZIP/ED07 theo hash §12.3 và giữ nguyên sáu chương/bibliography; không tính lại thống kê hoặc chạy nghiên cứu. Native FAIL/whole-system NOT_CERTIFIED/UI F11 PENDING không đổi. QA word count/keywords, liên kết/anchor, metadata, 84 đặc tả và diff; chỉ tài liệu nên không suite/compileall/API/fit/bootstrap/replay. Phần đầu chưa là bản nộp/đã ký hoặc dàn trang cuối.

### 13.2. Bìa, lời cảm ơn, cam đoan và danh mục

T60 giữ nguyên toàn bộ ba section metadata/bìa ngoài/bìa trong so với e6e1e1a4; tác giả Phan Hoang Dung, mã 23020346 và người hướng dẫn Dr. Tran Hong Viet đúng hồ sơ §1. Không sửa LaTeX/logo/PDF nên không biên dịch/render lại bìa; vị trí Supervisor đã căn giữa giữ nguyên. Bổ sung 42 chữ viết tắt/metric labels, 26 dòng ký hiệu và reading conventions theo glossary §5 và các chương. Không thay định nghĩa hoặc biến ID B_semantic thành embedding retrieval. List of Contents/Figures/Tables sẽ sinh từ LaTeX ở P8, không bịa danh mục/số trang trong Markdown.

Ở bản nháp ban đầu, lời cảm ơn dùng câu tối giản chỉ nêu người hướng dẫn đã xác nhận; câu hỏi cá nhân hóa đã gửi, chưa tự thêm người/tài trợ/đóng góp cụ thể. Cam đoan là văn bản gốc đề xuất để tác giả xem: ghi nguồn và phần kế thừa, giữ kết quả bất lợi/giới hạn, phân biệt tương lai với thực nghiệm đã chạy và minh bạch AI hỗ trợ soạn/biên tập thực tế của bản thảo. Không chép lời cam đoan mẫu, không viết khẳng định độc lập hoàn toàn/chưa từng nộp/chưa xuất bản hoặc nhận phê duyệt không có nguồn. Chữ ký và ngày ký để trống có nhãn rõ; chưa ghi tác giả đã xác nhận nội dung hoặc trường đã chấp thuận. Quy định chính thức vẫn chưa được cung cấp theo phản hồi trước, không hỏi lại như thể đã có quy định.

CL237–CL241 ánh xạ thông tin và danh mục. Đối soát ký hiệu/đơn vị, metadata/cover identity, acronym expansions/cross-section definitions, local links và 84 đặc tả; chỉ 6 file Markdown quản lý/phần đầu được sửa, sáu chương/bibliography/code/runtime/assets/receipts nguyên vẹn. Không suite/compileall/API/fit/bootstrap/replay; đây là QA tài liệu. Tại thời điểm soạn ban đầu, phần cá nhân/cam đoan chờ xác nhận theo tiêu chí T60; xác nhận tiếp theo được ghi tại §13.3. Không coi bản nháp là văn bản đã ký/đã nộp.

**QA T59–T60 trước khi tác giả xác nhận câu chữ:** abstract 329 từ/7 keywords; 42 abbreviations và 26 symbol rows khớp glossary (đủ 12 thuật ngữ yêu cầu); 84 đặc tả bất biến, CL001–CL241 liên tục, 680 liên kết local/390 anchor trong 6 file kiểm. Sáu chương, glossary nguồn, bibliography 22 mục, metadata/bìa/LaTeX/logo/PDF và toàn bộ code/runtime/model/archive/receipt không đổi. SHA256 U09 ZIP/ED07/revision index/component summary đã đối soát theo §12.3; không chạy lại analysis/suite. QA nội dung và diff PASS; T59 DONE, T60 REVIEW phần câu chữ cam đoan tác giả, không coi bản chưa ký là văn bản đã xác nhận hoặc bản nộp cuối. Quy định chính thức vẫn chưa được cung cấp; danh mục trang và visual QA thuộc P8/P9.

### 13.3. Xác nhận câu chữ cá nhân và hoàn tất T60

Trong phản hồi tiếp theo, tác giả trả lời trực tiếp hai câu hỏi: **“Dùng lời cảm ơn tối giản như trên”** và **“Giữ câu chữ bản nháp hiện tại”** đối với Declaration đã trình bày. Đây là nguồn xác nhận câu chữ trong phạm vi T60. Giữ nguyên toàn bộ lời cảm ơn/cam đoan đã soạn, gồm thông tin về hỗ trợ AI soạn/biên tập và trách nhiệm kiểm tra bản cuối; chỉ đổi nhãn trạng thái từ chờ xem sang tác giả đã xác nhận. CL238 bổ sung nguồn phản hồi và locator này, không thêm luận điểm khoa học.

T60 chuyển REVIEW → DONE; T59–T60 hoàn tất bản nháp phần đầu. Xác nhận câu chữ không phải chữ ký, ngày ký, duyệt biểu mẫu của trường hoặc trạng thái nộp: các trường ký/ngày vẫn để tác giả điền, quy định chính thức vẫn chưa được cung cấp như hồ sơ §1. Không yêu cầu xác nhận lại thông tin đã được tác giả chốt.

QA theo thay đổi: so nguyên nội dung Acknowledgements/Declaration (bỏ nhãn blockquote) với bản trước phản hồi, metadata/bìa/abstract/keywords/42 abbreviations/26 symbol rows và sáu chương giữ nguyên; đối soát 84 đặc tả, checklist T01–T60, liên kết/anchor và diff. Chỉ sửa trạng thái/nguồn xác nhận trong 6 file Markdown nên không chạy compileall/unit/E2E/leakage, không kiểm lại hash hay chạy analysis/replay/fit/API đã không đổi. Nguồn kiểm T59–T60 tại §13.1–13.2 tiếp tục có đúng phạm vi cũ; code/runtime/models/assets/archives/receipts không đổi.

### 13.4. Phụ lục A: hợp đồng dữ liệu và thời gian

T61 viết `appendices/A_contracts.md`/CL242–CL245, nối tham chiếu từ §4.2. Dùng source frozen và schema `urn:kltn:historical-task-record:1`; CORE4 enum bốn mã không bị suy thành coverage chín mã. Hai JSON gồm projection identity shared EX01 và nguyên record FPT:2022-04-07 từ bank snapshot; parse và so equality với dữ liệu nguồn. `shared_snapshot_causal_v1`, point id và content hash giữ đúng wire, không là causal certificate. Query outcome/entry-exit dates thuộc evaluation, không cho vào sealed payload.

Đầu lượt appendix đã đọc lại U08/U09 bằng reader chỉ đọc: kiểm outer pins, member/envelope/receipt, 15 artifact cold-replay identities và 56 stage EX01 khớp nguồn. Source commit lịch sử `384725a66fec074700963fac67c358b28b842092`; archive/member pins vẫn tại §3.4/§12.3. Nguồn schema/contracts/model trích tạm đều kiểm member hash của snapshot đã pin. Không chạy cold replay hoặc inference; đây là kiểm danh tính/đọc record. Appendix tables A1 và các bảng hỗ trợ không thêm ID vào danh mục 23 asset chính; LaTeX/numbering sau.

QA: JSON hợp lệ, source equality, ngày/nhãn/đơn vị/giới hạn khớp Chương 3/4, links/anchors/footnote/84 spec/diff; thân bài chỉ thêm cross-reference, bảng/công thức/kết quả cũ không sửa. Không suite/compileall/API/fit/bootstrap/replay theo phạm vi tài liệu. Appendix E sẽ viết ở bước tương ứng; tham chiếu tên bằng prose trong A chưa tạo liên kết tới file chưa tồn tại.

### 13.5. Phụ lục B: prompt và response

T62 viết `appendices/B_prompts.md`/CL246–CL249, nối §4.10.1. Đọc EX01 prepare/forecast r0, giữ UUID Common e9cd5100-0f68-4677-8ca5-84a08e41386c, v1 4ccd3bbe-9004-468f-a5dd-8859a2c53c97, anchor f7c7664b-69c7-4bef-a075-26c2d9c0d6e2, MT cc6bf729-784a-458a-8e40-07398fac513f. One-user-message lengths 4186/4556/3916/4586, BRPP substring 369 ký tự không gồm report separator. Đây là đo chuỗi đã lưu, không token/billing hoặc maximum của toàn study. Digest từng request theo source record giữ trong bảng.

Mọi trích natural language đều là English presentation translation, không đổi archive hoặc nhận prompt Anh đã chạy. Giữ metric denominators, example codes/returns và nhãn legacy T→T+2 ở ghi chú, không hợp thức hóa luật thị trường. Response JSON là projection machine fields thật, không giả full schema; confidence Cao được giải thích bằng bản dịch High, không thành probability. C3 prior_use builder không bị gán cho schema thống nhất đã đánh giá. Không in header, API key, env, account ID; raw request UUID phải giữ để truy vết.

QA: so machine JSON với reply, bốn UUID/hash/length với source, BRPP numerical lines với chuỗi gốc, schema fields/enums với frozen schema; English excerpts và caveats so source. Kiểm local links/footnote/JSON/84spec/diff, thân bài chỉ thêm cross-reference. Không API/fit/bootstrap/replay/suite; bảo toàn EX01 LONG thua và policy KEEP_PROPOSED_SAME.

### 13.6. Phụ lục C: công thức và cấu hình đã khóa

T63 viết `appendices/C_configuration.md`/CL250–CL253, nối §5.3.1. Mỗi nhóm số có source ID trong cột và locator chương/sổ: runtime B04c tách component/context, indicator/Native/Common, hai query HMM và episode-prefix khác nhau, v1/C2/A/B, bốn features/scalers/task membership, teacher/student recipe/selection và utility. Không lấy generic class train bounds, default token cap hay packing pilot thay resource đã chạy.

Đối chiếu TR02 bằng pin TR01.protocol SHA256 `11146a55e347be77b4a942c67d0acc9dba8646fa1d5a0b4817e5ffb504214857`; file không nằm trong source_members snapshot nên đọc đúng file đã khóa theo manifest pin, không giả nó là snapshot member. Selection file đọc theo TR01.receipts pin TR05. Nguồn RG01/RG02/TR01/TR03 và code đã trích đều kiểm byte/member tại đầu lượt. Kiểm 271873 parameters, PAIRED37, model seeds, recipe và seed42/step3000 theo manifest/protocol; công thức so với frozen source và §§3.3/4.3/4.5–4.8. Không chạy fit, load weights, forward, bootstrap utility hoặc hosted inference.

QA số/tham số theo đúng profile/resource, công thức/units, local link/footnote/84spec/diff; thân bài chỉ thêm tham chiếu, bảng/công thức cũ bất biến. Các table Appendix C thuộc phần bổ trợ, không thay số/thông điệp 23 asset chính. Không suite/compileall/replay do chỉ viết tài liệu.

### 13.7. Phụ lục D: bảng mở rộng và đối soát số

T64 viết `appendices/D_results.md`/CL254–CL258 và nối §§5.6/5.7. D1 lấy classification.csv cohort all_102, hai method AS/B, dimension symbol/block: 30 dòng; D2 giữ đủ21 execution rows trong upstream/factorial có9unit/3execution. Hai panel không gộp thành102points. Baseline manifest11 outputs kiểm hash theo pin tại §12.3; panels và execution CSV so nguyên byte với EvidenceArchive/index đã khóa.

D3/D4 lấy U09 classification_by_group.csv (450 dòng) và accounts.csv (1.530 dòng), xuất đủ 9 mã × 10 phương pháp = 90 dòng và 6 fold × 10 phương pháp = 60 dòng. BA là trung bình ba giá trị theo repeat đã lưu, kèm số repeat có định nghĩa; các nhóm có 0 hoặc 3 giá trị BA hợp lệ, giữ NA khi không xác định. Return/MDD được bình quân ba repeat trong từng tài khoản (symbol, fold), sau đó bình quân đều các tài khoản; không dựng lại ledger. D5 giữ đủ 30 dòng phương pháp/repeat từ hai CSV nguồn, gồm confusion, NA và tỷ số rủi ro chưa annualize. Kiểm theo từng phương pháp: tổng tài khoản là 51; return nhóm có trọng số tài khoản khớp summary trong sai số 1e−12; tổng support là 102 điểm, 25 UP/77 DOWN và tổng confusion khớp từng repeat. Trung bình BA/return theo repeat khớp summary. Không dùng trọng số tài khoản để cộng group BA.

D6 giữ đủ 20 định danh contrast; point arrays L1/L3 khớp effect gốc, band L2 lấy từ contrast; CORE4 có riêng 48 điểm/24 tài khoản. D7a/b giữ đủ 6/9 lượt loại fold/mã × 20 ô = 300 giá trị điểm, không biến min/max thành CI hoặc chọn bỏ cột. D8 giữ cả AS/B ở 12 kịch bản, tổng 24 dòng hiển thị trong 120 dòng nguồn; delta so với reference của chính phương pháp khác Full−Base. Giữ nguyên predictions, các trạng thái blocked/residual/pending và giới hạn không có fill được xác thực.

Đây là định dạng và tổng hợp mô tả số đã lưu, không gọi model, fit, bootstrap mới, sinh utility draws hoặc replay kinh tế. QA khóa dòng/ô nguồn, đơn vị, support, confusion, thứ tự tổng hợp, NA, liên kết, footnote, 84 đặc tả và diff đều PASS. Bảng/công thức/số liệu thân bài không đổi; chỉ thêm tham chiếu. Bảng D1–D8 là bảng phụ lục; landscape/longtable và chia trang thuộc P8/P9, chưa nghiệm thu PDF.

### 13.8. Phụ lục E: audit và phản ví dụ giữ lại

T65 viết `appendices/E_verification.md`/CL259–CL262, nối §5.9.2. Đọc alpha_contract_v1 qua EvidenceArchive; contract report/targets/indicators so byte với nguồn đã dùng P4. Nội dung tập trung requirement→evidence→scope, outer-cutoff PASS khác row-wise FAIL, PASS_DETECTION/CONTRACT_AUDIT không là causal PASS. Vectors ba normalizer lấy trực tiếp leakage.json và round6, không chạy synthetic audit mới.

| Đường dẫn qua revision index | SHA-256 nguyên byte |
| --- | --- |
| outputs/revision/alpha_contract_v1/cases.json | `16d8f3de8f7f70f7674c6d0a0606ce046e62ead61714056d17e7659c744ac7cd` |
| outputs/revision/alpha_contract_v1/leakage.json | `eafedda293364545792c760066bd9ed4406fe6fad33d84484fcb16f392f0d8f6` |
| outputs/revision/alpha_contract_v1/summary.json | `83079d9ea2f453af801a10d6e45861871343739d37621f2ea88ea024bad56c4c` |
| outputs/revision/alpha_contract_v1/manifest.json | `6c29b42c4704145fc956923e99f39445e3172ae2699f6e3c216aa289c4fef541` |

U08 acceptance/receipt đã kiểm member hash trong archive được pin. Các nhóm prior_checks ghi 69/61/41/44/40 test với rerun=false, không cộng thành số test độc lập hay toàn suite. Giữ source commit 69935d..., 718 source pins, prompt tối đa 4.750 ký tự và tối đa 3 HTTP attempts đúng phạm vi U08. Cold record U09 ghi 15 artifact, 0 API mới và training=false; không replay lại. AP16 khớp pin `1fc3a65af3a8301a9c884dd19e1f2cbb3510ad5e584a760bf0e737a68971c5be`. Các số 135 Python/24 DOM/23 compiled/2 JavaScript là kiểm tra đã được receipt ghi nhận; không nhận đã chạy lại hoặc desktop/mobile PASS.

Giữ 828/852 là khác biệt giá trị return, không phải số nhãn đổi; nguồn raw journals còn thiếu, Native FAIL, whole-system NOT_CERTIFIED và UI/F11 chưa hoàn tất. Giữ EX01 LONG thua và các ablation chưa chạy. Kiểm từng số, vector, trạng thái, nguồn, đơn vị, liên kết, footnote, đặc tả và diff; không chạy compileall/unit/E2E/leakage, inference, fit, bootstrap hoặc replay. Bốn gate là tiêu chí kiểm theo phạm vi, không phải tuyên bố toàn hệ PASS. Appendix F cung cấp lệnh tái lập offline riêng.

### 13.9. Phụ lục F: tái lập offline và ứng dụng

T66 viết `appendices/F_reproduction.md`/CL263–CL266, nối §§4.10.4/5.1.2. Đường dẫn, outer pins và số byte lấy từ input_bindings đã kiểm; asset/model/index/baseline bổ sung theo §3.4/TR. Tách các mức tài nguyên: đọc bằng thư viện chuẩn, cold replay thống kê, inference/replay số học, HTTP fixture và live provider. Không coi Git checkout tự cung cấp asset ngoài Git hoặc đảm bảo trọng số hosted bất biến.

Kiểm tĩnh parser và implementation: revision_evidence dùng tên release dạng positional, destination là thư mục gốc giữ outputs/revision/...; U06 restore/verify khác replay-numeric. U09 verify gọi calculate trong thư mục tạm, tái tạo artifact thống kê/resampling rồi so byte, không chỉ đọc hash; không client, key hoặc training. Các lệnh replay yêu cầu checkout lịch sử tách biệt và đúng bindings; không chạy freeze/analyze hoặc ghi đè receipt cũ. Snippet PowerShell dùng thư viện chuẩn, kiểm hash outer/member rồi đọc đúng 10 dòng summary và các cột nguồn. Lệnh fixture serve_serving_review với port 5051, duration 300, seed khớp parser; chỉ loopback, cookie riêng và namespace tạm. Entry point web_interface.py là luồng khác, có thể gọi provider khi yêu cầu phân tích. Không chạy replay, khởi động server hoặc gọi API để viết tài liệu.

Luồng ứng dụng khớp §4.10.4: Realtime 1D chọn một version/mã; capture timeframe có thể daily_provisional, khác backend chỉ dùng phiên hoàn tất. Giữ 600 quan sát daily context, preflight/job một repeat; ba stage phụ thuộc của MT không phải tám vai trò × ba repeat. Stored VI/EN views không dịch hoặc gọi LLM khi đổi ngôn ngữ. UI/F11 chưa hoàn tất, desktop/mobile NOT_RUN. Các quy tắc thực thi vẫn được trình bày là giả định nghiên cứu hoặc policy khả dụng dữ liệu, không khẳng định luật hiện hành.

QA đường dẫn/cờ lệnh, cú pháp Python tĩnh, danh tính asset đã pin, tài nguyên bắt buộc, luồng ứng dụng so với source, liên kết, footnote, đặc tả và diff. P7/T59–T66 đủ bản nháp phần đầu và sáu phụ lục; T67–T84 còn việc. G4 yêu cầu T59–T72 nên chưa hoàn tất; chưa có LaTeX/PDF toàn văn hoặc nghiệm thu ngoài. Không chạy suite/compileall, huấn luyện, forward, bootstrap hay replay vì chỉ sửa tài liệu.

**QA cuối T61–T66:** 84 đặc tả bất biến; checklist T01–T66, CL001–CL266 liên tục; sáu phụ lục tiếng Anh với 32 bảng/479 dòng dữ liệu, ba ví dụ JSON khớp nguồn và bốn cặp UUID/hash/độ dài request. Appendix D có 315 dòng bảng mở rộng, giữ đủ 300 giá trị omission, support/confusion/aggregation và NA đã đối soát. Kiểm 841 liên kết local/452 anchor; tám đoạn tham chiếu thêm vào Chương 4/5. Toàn bộ nội dung cũ của sáu chương, gồm bảng/công thức/kết quả, được giữ nguyên ngoài tám đoạn này; phần đầu đã xác nhận, bibliography, bìa/assets và code/runtime/config/input/model/archive/receipt không đổi. Chỉ 13 file Markdown được sửa/thêm. Kiểm hình dạng bảng, cặp ngoặc công thức và cú pháp snippet/parser tĩnh PASS; các lệnh tái lập không được thực thi. Không chạy suite theo AGENTS §1.2 vì thuần tài liệu. P7 đủ bản nháp; G4 chưa hoàn tất, chưa dàn trang/kiểm PDF toàn văn hoặc duyệt ngoài.


## 14. Dàn trang LaTeX và chuyển nguồn chính


### 14.1. Khung LaTeX sạch đã biên dịch

T67 dựng main/preamble/build guide trong thesis/latex, không dùng macro/chủ đề/danh tính mẫu. Hai bìa dùng nguồn đã chốt nguyên nội dung; render hai trang kiểm trực quan, Supervisor căn giữa và không tràn. LuaHBTeX 1.24.0 (MiKTeX 25.12), Latin Modern, report12pt/A4, lề 2,5cm ngang/3cm trên dưới, giãn1,5; bibliography numeric theo thứ tự hiện tại, chưa là chuẩn trường.

Đã bổ sung package thiếu theo lỗi build; build tắt auto-installer/shell-escape, dùng Biber trên bản sao bcf/bib tại thư mục tạm để tránh lỗi Perl với đường dẫn Unicode Windows. Python build.py chỉ compile chính file thay đổi và chạy đúng build tài liệu; không unit/E2E/leakage nghiên cứu. LuaLaTeX/Biber thành công, PDF khung2trang; warning MiKTeX chưa kiểm cập nhật và locale Perl không đổi kết quả. Tại mốc này mới khung; thân bài đang chuyển, chưa G4 hoặc bản nộp.


### 14.2. Chương 3–4 đã chuyển LaTeX và gắn sơ đồ

T68 chuyển 84 heading, 29 bảng/139 dòng, 28 display equations, ba thuật toán và 10 hình vector nguồn sẵn có. Tên/đơn vị/mẫu số được giữ; tự sinh số chương/section/table/figure, ID nguồn như F01/B03 vẫn dùng để đối chiếu. Công thức BA/MCC tách hai dòng để đọc được, không đổi biểu thức; escape ký tự phần trăm trong công thức, xử lý path/hash dài bằng điểm ngắt hợp lệ. TikZ source và PDF đi cùng trong cây thesis.

Đối soát tất cả token số theo từng hàng bảng và toàn bộ display equations với Markdown PASS; equations chỉ khác layout/escape. Build LuaLaTeX/Biber thành công, PDF ghép tạm88trang gồm hai bìa/Chương3–4, render kiểm phương pháp/hình/bảng/BA-MCC/thuật toán. Còn cảnh báo ngắt trang longtable/footnote không gây mất nội dung và hbox nhỏ dưới1pt; sẽ rà lại trên bản ghép cuối, không ghi là PDF đã hoàn tất. Liên kết tới chương/phụ lục chưa chuyển chờ T69–T71. Không sửa Markdown đã khóa, input hoặc code nghiên cứu; không chạy runtime suite/API/fit/replay.


### 14.3. Chương 5 và bảng/đồ thị đã chuyển LaTeX

T69 chuyển đủ 43 heading, 37 bảng/254 dòng, tám display equations và hai đồ thị F09/F10 vector; giữ source notes/footnotes, NA, hai studies/estimators và family20 contrasts. Mỗi hàng đối chiếu toàn bộ token số với AST bản Markdown đã khóa, display equations khớp sau bỏ layout/escape. Bảng rộng dùng landscape/longtable với header lặp; các caption/list entry sinh tự động còn ID B05/B06/F09 giữ để truy vết.

Build bản ghép Chương3–5 thành công bằng LuaLaTeX/Biber, không source/citation error; liên kết đến phần chưa chuyển còn xử lý lúc ghép. Đã render bản kết quả để kiểm bảng/đồ thị; các cảnh báo độ rộng/ngắt trang còn được sửa trên bản ghép T72, không nghiệm thu trực quan cuối tại bước này. Không chạy lại analysis/bootstrap/LLM hoặc suite nghiên cứu. Công cụ build có tùy chọn số lượt và bỏ Biber chỉ khi bibliography không đổi; build đầy đủ cuối vẫn dùng Biber và nhiều lượt ổn định.


### 14.4. Chương 1/2/6, phần đầu và bibliography đã nối

T70 chuyển ba chương còn lại, phần đầu đã xác nhận,42 abbreviations/26 symbol rows, bibliography22 mục, danh mục nội dung/hình/bảng tự sinh. Bìa chỉ xuất hiện hai trang theo nguồn covers, không chép lại bảng metadata/outer/inner từ Markdown; nhãn quản lý Draft/Writing aids không vào PDF. Lời cảm ơn/cam đoan giữ câu chữ tác giả, nhãn unsigned và trường ký/ngày còn trống. Sơ đồ Mermaid bài toán chuyển TikZ có thể sửa, giữ hướng future prices chỉ tới evaluation.

Đối soát ba bảng/13 dòng của Chương1/2 và phần ký hiệu với nguồn; citation keys nối Biber, style numeric/sorting none theo lựa chọn biên tập. Biber không có key thiếu; hai warning legacy month March/year n.d. giữ metadata gốc và không ảnh hưởng thứ tự numeric. LuaLaTeX ghép đủ6chương/phầnđầu; render/kiểm bản ghép tiếp ở T71–T72. Markdown/bibliography gốc chưa sửa; không suy luật hoặc chứng nhận mới. Không suite/API/fit/replay nghiên cứu.


### 14.5. Sáu phụ lục đã chuyển LaTeX và nối tham chiếu

T71 chuyển đủ Appendix A–F,32 bảng/479 dòng dữ liệu, năm display equations, các JSON/schema/prompt/command examples. Tất cả token số trong hàng bảng và biểu thức display khớp nguồn Markdown; không bỏ NA, scenario/omission hoặc các kết quả âm. Longtable lặp header, các bảng D nhiều cột dùng landscape; Verbatim tự ngắt chuỗi dài, không thực thi lệnh mẫu. Các link từ thân bài và giữa phụ lục chuyển thành hyperref nội bộ, không có undefined reference/citation hay glyph thiếu trong build mới nhất.

LuaLaTeX/Biber ghép toàn bộ, bản tạm258trang; render bảng AppendixD, schema/prompt/command và vùng nhiều footnote để tiếp tục QA. Cảnh báo longtable/độ rộng nhỏ được xem xét ở T72; chưa là rà khoa học/ngôn ngữ/PDF cuối P9. Chưa đổi nguồn chính thức trước khi tích hợp T72; Markdown gốc/bibliography/asset/receipt nghiên cứu giữ nguyên, không API/fit/bootstrap/replay/suite.


### 14.6. Toàn văn đã ghép và chuyển nguồn chính sang LaTeX

T72 ghép đủ hai bìa, phần đầu, sáu chương, bibliography và sáu phụ lục; PDF P8 có 259 trang. Chuyển nguồn lúc 2026-11-16T13:14:55+07:00 (Asia/Saigon), ghi trong README và source-map.json: nội dung tiếp theo sửa trong LaTeX; 13 bản Markdown nội dung giữ làm bản lưu trữ, không duy trì hai nguồn đang sửa. Kế hoạch/sổ bằng chứng vẫn cập nhật bằng Markdown. G4 chưa nghiệm thu yêu cầu chính thức; P9/P10 và UI acceptance còn mở.

**Kiểm tra theo phạm vi:** bản sao chỉ có LaTeX, assets và bibliography build LuaLaTeX/Biber thành công, không có Markdown/Pandoc/thư mục mẫu và không đọc input ở bản repository gốc. `check.py --strict-cutover-targets` PASS: hash 13 bản lưu trữ và nguồn LaTeX tại mốc chuyển khớp, 31 dependency cục bộ tồn tại, mỗi chương/phụ lục ghép đúng một lần. Biên dịch Python riêng `tools/build.py` và `tools/check.py` PASS. Đối chiếu 101 bảng/885 dòng dữ liệu và 41 biểu thức display với Markdown PASS về số dòng/token số/biểu thức sau bỏ layout; hai bảng danh mục phần đầu có thêm 68 dòng (42 chữ viết tắt, 26 ký hiệu). PDF có 13 hình và 22 mục bibliography; citation/reference/glyph thiếu bằng 0, overfull box bằng 0, 423 link nội bộ hợp lệ, kiểm bounds/crop không có vi phạm. Đã render toàn bộ, xem contact sheets và kiểm riêng các trang bìa, công thức, bảng rộng, schema/prompt và vùng footnote; sau lần chỉnh ngắt footnote cuối đã xem lại các trang thay đổi.

**Cảnh báo/giới hạn:** build cuối còn 22 ghi chú nội bộ longtable về glue splitting, underfull boxes và hai warning metadata bibliography gốc (`month=March`, `year=n.d.`); không gọi là build không warning. Đã kiểm render/bounds vùng liên quan; P9 tiếp tục rà khoảng trắng, độ gọn và trình bày. Số trang vượt dự toán ban đầu, chưa có giới hạn chính thức để nghiệm thu; không bỏ bằng chứng để ép số trang. Hạn nộp, chuẩn trích dẫn/bố cục và biểu mẫu bắt buộc chưa được cung cấp; cam đoan đã xác nhận câu chữ nhưng chưa ký. Không chạy suite nghiên cứu hoặc fit/API/bootstrap/replay vì chỉ chuyển tài liệu và công cụ build tài liệu; không đổi runtime, hợp đồng kinh tế, input, model, archive, receipt hay kết quả Native FAIL/NOT_CERTIFIED/UI PENDING.

PDF `release/thesis.pdf` có SHA-256 `eeff3f0b09996d031a296fafc97f9042b711134d05628a5ab6c6264b55ef9826`, khớp đầu ra build tách biệt. Đây là bản P8 để rà soát tiếp, chưa là bản đã duyệt, ký hoặc nộp.


## 15. Rút gọn và đối soát P9

### T73a. Khóa mốc và ánh xạ biên tập theo ngân sách 66 trang

Mốc trước biên tập: commit `38437142` (kế hoạch mới), nội dung/PDF P8 tại `d025facb`; PDF 259 trang có SHA-256 `eeff3f0b09996d031a296fafc97f9042b711134d05628a5ab6c6264b55ef9826`. Có thể đối chiếu nguyên byte bằng `git show d025facb:thesis/release/thesis.pdf` và nguồn cùng commit. Không ghi đè lịch sử hoặc receipt nghiên cứu. Ngân sách hiện hành: phần đầu 10, Chương 1–6 lần lượt 3/5/7/20/15/3, references 3, tổng mục tiêu 66 trang trong khoảng 60–70; 12 pt/giãn 1,5/lề giữ nguyên. Các bảng chi tiết/hash/prompt dài nằm ngoài bản nộp, phần giải thích phương pháp phải tự đủ.

#### Ánh xạ trước/sau đã khóa trước khi biên tập

Mỗi hàng dưới bao phủ section cũ cùng toàn bộ subsection, công thức, bảng, hình và ví dụ thuộc section đó. Nhãn `tab:*`/`fig:*` liệt kê hết đối tượng có caption của bản P8; bảng chi tiết không được chọn vẫn truy vết nguyên byte ở Git `d025facb`. Đây là quyết định biên tập, không phải sửa kết quả. Số mục mới có thể đổi theo LaTeX, tên đích là ràng buộc nội dung.

| Nguồn P8 | Quyết định và nơi đến | Đối tượng cũ nằm trong nhóm |
| --- | --- | --- |
| `latex/chapters/01_introduction.tex` §1 Context and motivation | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 1, Context and motivation | Không có caption riêng |
| `latex/chapters/01_introduction.tex` §2 Problem statement | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 1, Problem statement | `fig:problem` |
| `latex/chapters/01_introduction.tex` §3 Objectives and research questions | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 1, Objectives and research questions | `tab:01_introduction:1` |
| `latex/chapters/01_introduction.tex` §4 Challenges and boundaries | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 1, Challenges and boundaries | Không có caption riêng |
| `latex/chapters/01_introduction.tex` §5 Contributions and thesis organization | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 1, Contributions and thesis organization | Không có caption riêng |
| `latex/chapters/02_related_work.tex` §1 Technical analysis and quantitative stock prediction | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 2, Technical analysis and quantitative stock prediction | Không có caption riêng |
| `latex/chapters/02_related_work.tex` §2 LLMs, VLMs and multi-agent financial systems | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 2, LLMs, VLMs and multi-agent financial systems | Không có caption riêng |
| `latex/chapters/02_related_work.tex` §3 Market regime detection | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 2, Market regime detection | Không có caption riêng |
| `latex/chapters/02_related_work.tex` §4 In-context learning and Bayesian historical context | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 2, In-context learning and Bayesian historical context | Không có caption riêng |
| `latex/chapters/02_related_work.tex` §5 Multi-task Bayesian ICL and student--teacher methods | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 2, Multi-task Bayesian ICL and student--teacher methods | Không có caption riêng |
| `latex/chapters/02_related_work.tex` §6 Evaluation of trading systems using LLMs | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 2, Evaluation of trading systems using LLMs | Không có caption riêng |
| `latex/chapters/02_related_work.tex` §7 Research gap and position of the thesis | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 2, Research gap and position of the thesis | `tab:02_related_work:1`, `tab:02_related_work:2` |
| `latex/chapters/03_background.tex` §1 Observations and time indexing | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 3, Observations and time indexing | `tab:03_background:1`, `fig:F01` |
| `latex/chapters/03_background.tex` §2 Economic contract and prediction target | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 3, Economic contract and prediction target | `tab:03_background:2` |
| `latex/chapters/03_background.tex` §3 Technical, alpha and sentiment signals | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 3, Technical, alpha and sentiment signals | `tab:03_background:3` |
| `latex/chapters/03_background.tex` §4 Hidden Markov models for market regimes | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 3, Hidden Markov models for market regimes | Không có caption riêng |
| `latex/chapters/03_background.tex` §5 Bayesian summaries of historical evidence | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 3, Bayesian summaries of historical evidence | Không có caption riêng |
| `latex/chapters/03_background.tex` §6 Multi-task context and utility | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 3, Multi-task context and utility | `tab:03_background:4` |
| `latex/chapters/03_background.tex` §7 Temporal validity and evaluation principles | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 3, Temporal validity and evaluation principles | `tab:03_background:5`, `fig:F02` |
| `latex/chapters/04_proposed_system.tex` §1 System overview and one-decision walkthrough | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, System overview and one-decision walkthrough; ưu tiên hình tổng quan/MT/policy | `fig:F03` |
| `latex/chapters/04_proposed_system.tex` §2 Input preparation and shared state | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, Input preparation and shared state | `tab:04_proposed_system:1` |
| `latex/chapters/04_proposed_system.tex` §3 The base multi-agent pipeline | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, The base multi-agent pipeline | `tab:04_proposed_system:2`, `fig:F04`, `tab:04_proposed_system:3`, `tab:04_proposed_system:4`, `tab:04_proposed_system:5` |
| `latex/chapters/04_proposed_system.tex` §4 Native and Common foundations | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, Native and Common foundations | `tab:04_proposed_system:6` |
| `latex/chapters/04_proposed_system.tex` §5 Historical memory and market regimes | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, Historical memory and market regimes; ưu tiên hình tổng quan/MT/policy | `tab:04_proposed_system:7`, `tab:04_proposed_system:8`, `tab:04_proposed_system:9`, `fig:F05a` |
| `latex/chapters/04_proposed_system.tex` §6 Bayesian Prior v1 | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, Bayesian Prior v1 | `tab:04_proposed_system:10`, `fig:F05` |
| `latex/chapters/04_proposed_system.tex` §7 Conditional and alternative priors | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, Conditional and alternative priors | `tab:04_proposed_system:11`, `tab:04_proposed_system:12`, `tab:04_proposed_system:13` |
| `latex/chapters/04_proposed_system.tex` §8 MT-BICL and action revision | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, MT-BICL and action revision; ưu tiên hình tổng quan/MT/policy | `tab:04_proposed_system:14`, `tab:04_proposed_system:15`, `tab:04_proposed_system:16`, `fig:F06`, `tab:04_proposed_system:17`, `tab:04_proposed_system:18`, `tab:04_proposed_system:19`, `fig:F07`, `tab:04_proposed_system:20` |
| `latex/chapters/04_proposed_system.tex` §9 Variant orchestration and complete algorithms | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, Variant orchestration and complete algorithms | `tab:04_proposed_system:21`, `fig:F08` |
| `latex/chapters/04_proposed_system.tex` §10 Prompt limits, recovery and application | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 4, Prompt limits, recovery and application | `tab:04_proposed_system:22`, `tab:04_proposed_system:23`, `fig:F11`, `tab:04_proposed_system:24` |
| `latex/chapters/05_experiments.tex` §1 Studies and evidence scope | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Studies and evidence scope; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:1` |
| `latex/chapters/05_experiments.tex` §2 Data and evaluation support | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Data and evaluation support; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:2`, `tab:05_experiments:3` |
| `latex/chapters/05_experiments.tex` §3 Configuration and paired protocol | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Configuration and paired protocol; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:4`, `tab:05_experiments:5`, `tab:05_experiments:6` |
| `latex/chapters/05_experiments.tex` §4 Comparators and interventions | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Comparators and interventions; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:7`, `tab:05_experiments:8` |
| `latex/chapters/05_experiments.tex` §5 Metrics and statistical analysis | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Metrics and statistical analysis; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:9`, `tab:05_experiments:10` |
| `latex/chapters/05_experiments.tex` §6 Component-study results | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Component-study results; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:11`, `tab:05_experiments:12`, `tab:05_experiments:13`, `tab:05_experiments:14`, `tab:05_experiments:15`, `tab:05_experiments:16`, `tab:05_experiments:17` |
| `latex/chapters/05_experiments.tex` §7 Historical-context results | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Historical-context results; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:18`, `tab:05_experiments:19`, `tab:05_experiments:20`, `tab:05_experiments:21`, `fig:F09`, `tab:05_experiments:22` |
| `latex/chapters/05_experiments.tex` §8 Mechanisms, case studies and robustness | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Mechanisms, case studies and robustness; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:23`, `tab:05_experiments:24`, `fig:F10`, `tab:05_experiments:25`, `tab:05_experiments:26`, `tab:05_experiments:27`, `tab:05_experiments:28`, `tab:05_experiments:29`, `tab:05_experiments:30`, `tab:05_experiments:31`, `tab:05_experiments:32`, `tab:05_experiments:33`, `tab:05_experiments:34`, `tab:05_experiments:35` |
| `latex/chapters/05_experiments.tex` §9 Unperformed ablations and threats to validity | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 5, Unperformed ablations and threats to validity; giữ cả adverse/control/NA; chi tiết stock/fold/repeat chuyển nguồn lưu trữ | `tab:05_experiments:36`, `tab:05_experiments:37` |
| `latex/chapters/06_conclusion.tex` §1 Summary of the approach | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 6, Summary of the approach | Không có caption riêng |
| `latex/chapters/06_conclusion.tex` §2 Answers and contributions | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 6, Answers and contributions | Không có caption riêng |
| `latex/chapters/06_conclusion.tex` §3 Limitations | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 6, Limitations | Không có caption riêng |
| `latex/chapters/06_conclusion.tex` §4 Future work | Giữ lõi, gộp diễn giải/bỏ chi tiết quản lý → Chương 6, Future work | Không có caption riêng |
| `latex/appendices/A_contracts.tex` §1 Identity, working state and sealed input | Chuyển nội dung thiết yếu → Chương 3 timing/labels/PIT; Chương 4 input/absence; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:A_contracts:1` |
| `latex/appendices/A_contracts.tex` §2 A completed historical episode | Chuyển nội dung thiết yếu → Chương 3 timing/labels/PIT; Chương 4 input/absence; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:A_contracts:2` |
| `latex/appendices/A_contracts.tex` §3 Time mapping and economic labels | Chuyển nội dung thiết yếu → Chương 3 timing/labels/PIT; Chương 4 input/absence; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:A_contracts:3` |
| `latex/appendices/A_contracts.tex` §4 Missingness, failure and serialization | Chuyển nội dung thiết yếu → Chương 3 timing/labels/PIT; Chương 4 input/absence; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:A_contracts:4` |
| `latex/appendices/B_prompts.tex` §1 Families, provenance and redaction | Chuyển nội dung thiết yếu → Chương 4 request/facts/validation/fallback; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:B_prompts:1`, `tab:B_prompts:2` |
| `latex/appendices/B_prompts.tex` §2 Representative decision instructions | Chuyển nội dung thiết yếu → Chương 4 request/facts/validation/fallback; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | Không có caption riêng |
| `latex/appendices/B_prompts.tex` §3 BRPP and anchored context | Chuyển nội dung thiết yếu → Chương 4 request/facts/validation/fallback; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | Không có caption riêng |
| `latex/appendices/B_prompts.tex` §4 Reply schemas and recorded example | Chuyển nội dung thiết yếu → Chương 4 request/facts/validation/fallback; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:B_prompts:3` |
| `latex/appendices/B_prompts.tex` §5 Budgets, repair and interpretation | Chuyển nội dung thiết yếu → Chương 4 request/facts/validation/fallback; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:B_prompts:4` |
| `latex/appendices/C_configuration.tex` §1 Runtime and hosted requests | Chuyển nội dung thiết yếu → Chương 4 thuật toán; Chương 5 cấu hình thực dùng; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:C_configuration:1` |
| `latex/appendices/C_configuration.tex` §2 Indicators and alpha transformations | Chuyển nội dung thiết yếu → Chương 4 thuật toán; Chương 5 cấu hình thực dùng; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:C_configuration:2` |
| `latex/appendices/C_configuration.tex` §3 HMMs and distinct frozen regime resources | Chuyển nội dung thiết yếu → Chương 4 thuật toán; Chương 5 cấu hình thực dùng; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:C_configuration:3`, `tab:C_configuration:4` |
| `latex/appendices/C_configuration.tex` §4 Retrieval, conditional rates and readiness | Chuyển nội dung thiết yếu → Chương 4 thuật toán; Chương 5 cấu hình thực dùng; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:C_configuration:5` |
| `latex/appendices/C_configuration.tex` §5 Numerical context, teacher and student | Chuyển nội dung thiết yếu → Chương 4 thuật toán; Chương 5 cấu hình thực dùng; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:C_configuration:6`, `tab:C_configuration:7`, `tab:C_configuration:8` |
| `latex/appendices/C_configuration.tex` §6 Utility and final action policy | Chuyển nội dung thiết yếu → Chương 4 thuật toán; Chương 5 cấu hình thực dùng; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:C_configuration:9` |
| `latex/appendices/D_results.tex` §1 Component classification by stock and block | Chuyển nội dung thiết yếu → Chương 5 hai bảng chính, family20 và sensitivity; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:D_results:1` |
| `latex/appendices/D_results.tex` §2 Separate upstream and factorial executions | Chuyển nội dung thiết yếu → Chương 5 hai bảng chính, family20 và sensitivity; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:D_results:2` |
| `latex/appendices/D_results.tex` §3 Historical context by stock | Chuyển nội dung thiết yếu → Chương 5 hai bảng chính, family20 và sensitivity; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:D_results:3` |
| `latex/appendices/D_results.tex` §4 Historical context by fold | Chuyển nội dung thiết yếu → Chương 5 hai bảng chính, family20 và sensitivity; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:D_results:4` |
| `latex/appendices/D_results.tex` §5 Historical context by Decision repeat | Chuyển nội dung thiết yếu → Chương 5 hai bảng chính, family20 và sensitivity; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:D_results:5` |
| `latex/appendices/D_results.tex` §6 Complete contrast sensitivity family | Chuyển nội dung thiết yếu → Chương 5 hai bảng chính, family20 và sensitivity; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:D_results:6`, `tab:D_results:7`, `tab:D_results:8` |
| `latex/appendices/D_results.tex` §7 Component execution-scenario extension | Chuyển nội dung thiết yếu → Chương 5 hai bảng chính, family20 và sensitivity; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:D_results:9` |
| `latex/appendices/E_verification.tex` §1 Evidence matrix and status meanings | Chuyển nội dung thiết yếu → Chương 5 audit/FAIL/NOT_CERTIFIED; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:E_verification:1` |
| `latex/appendices/E_verification.tex` §2 Retained Native row-wise counterexamples | Chuyển nội dung thiết yếu → Chương 5 audit/FAIL/NOT_CERTIFIED; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:E_verification:2` |
| `latex/appendices/E_verification.tex` §3 Provenance and unfavorable records retained | Chuyển nội dung thiết yếu → Chương 5 audit/FAIL/NOT_CERTIFIED; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | Không có caption riêng |
| `latex/appendices/E_verification.tex` §4 Receipt-bound checks and what was not rerun | Chuyển nội dung thiết yếu → Chương 5 audit/FAIL/NOT_CERTIFIED; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:E_verification:3` |
| `latex/appendices/E_verification.tex` §5 Application and missing experimental acceptance | Chuyển nội dung thiết yếu → Chương 5 audit/FAIL/NOT_CERTIFIED; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | Không có caption riêng |
| `latex/appendices/F_reproduction.tex` §1 Inputs, source and model identities | Chuyển nội dung thiết yếu → Chương 4 recovery/UI; Chương 5 tái lập; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:F_reproduction:1`, `tab:F_reproduction:2` |
| `latex/appendices/F_reproduction.tex` §2 Read-only inspection and scoped archive restoration | Chuyển nội dung thiết yếu → Chương 4 recovery/UI; Chương 5 tái lập; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | Không có caption riêng |
| `latex/appendices/F_reproduction.tex` §3 Historical offline replay requires the matching checkout | Chuyển nội dung thiết yếu → Chương 4 recovery/UI; Chương 5 tái lập; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | Không có caption riêng |
| `latex/appendices/F_reproduction.tex` §4 Resource levels and practical limits | Chuyển nội dung thiết yếu → Chương 4 recovery/UI; Chương 5 tái lập; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | `tab:F_reproduction:3` |
| `latex/appendices/F_reproduction.tex` §5 Offline preview versus current live workflow | Chuyển nội dung thiết yếu → Chương 4 recovery/UI; Chương 5 tái lập; bỏ dump/bảng lặp khỏi PDF, lưu nguồn lịch sử | Không có caption riêng |

**Hình:** giữ F03 (toàn hệ), F06 (task/training), F07 (policy); giữ F01 timeline và F04 hai chart nếu giúp phân biệt thông tin; rút F02 indicator, F05a regime, F05 retrieval và F08 DAG thành công thức/bảng/giả mã; gộp F11 application vào vận hành và giữ trạng thái UI PENDING. Bỏ sơ đồ bài toán lặp ở Chương 1; F09/F10 chuyển thành bảng hẹp/diễn giải đủ số và mẫu số. Assets gốc không bị sửa/xóa.

**Bảng:** Chương 1 dùng bốn RQ trong văn bản; hai bảng related-work gộp một bảng định vị. Chương 3 chỉ giữ định nghĩa/timeline và ví dụ cần đọc. 24 bảng Chương 4 gộp contract, variants và cấu hình số cần thiết; các nội dung còn lại chuyển thành công thức/đoạn văn/ví dụ chung. Chương 5 giữ riêng bảng component và context; family20 chia theo baseline với hai endpoint đầy đủ, giữ support/policy, case bất lợi và audit. Bỏ inventory/UUID/log và bảng detail lặp khỏi PDF; nguồn, hash, nguyên giá trị và tập đầy đủ tiếp tục ở sổ bằng chứng/Git/artifact gốc. Phụ lục không được đổi tên để chèn trở lại.

T73a chỉ đổi tài liệu quản lý, chưa sửa LaTeX/PDF. Đã kiểm mốc/hash, toàn bộ section/caption có ánh xạ; không chạy suite nghiên cứu vì runtime/bằng chứng thực nghiệm giữ nguyên.

### T73b. Rút Chương 1–2 còn 3 và 4 trang

Giữ nguyên văn RQ1–RQ4, phạm vi/đóng góp có attribution và các giới hạn Native FAIL/NOT_CERTIFIED/UI PENDING. Related work tổng hợp theo vấn đề, một bảng định vị thay hai ma trận dài; đủ 22 citation keys trong build. LuaLaTeX/Biber ba lượt PASS, không undefined citation/reference hoặc overfull box; đã render/xem bảy trang hai chương. Không dùng các bảng bị bỏ để thay đổi kết quả hoặc nhận là đã rà cuối T74–T80.

### T73c. Rút nền tảng và hợp đồng Chương 3 còn 6 trang

Giữ timing e=t+1, net-return oracle/phí hai chiều, zero=DOWN/SHORT=CASH, tín hiệu, HMM, Beta disjoint, task/teacher/student, utility và PIT/paired. Cấu hình chi tiết nằm ở Chương 4–5; không đổi công thức hoặc giả định. Build riêng Chương 3 ba lượt PASS (6 trang nội dung + 1 references); đã xem render sáu trang. Lần build đầu phát hiện tên file timeline sai và đã sửa đúng asset F01_trade_timeline.pdf trước build PASS. Rà kích thước nhãn hình tiếp tục T73l.

### T73d. Rút tổng quan, hợp đồng và agent foundations Chương 4

Phần 4.1–4.4 còn 5 trang nội dung trong build riêng (thêm 1 trang bibliography). Giữ F03, bảng input/output, phân biệt tính số/LLM/offline, Pattern khác Trend, Alpha/Sentiment và Native/Common khác Full/Base; giữ ca FPT và mâu thuẫn chart/confidence. Build ba lượt PASS; đã render/xem 5 trang nội dung, không đổi runtime hay gọi mô hình. Hình sẽ được kiểm cỡ nhãn toàn văn ở T73l.

### T73e. Rút memory, regime và các prior nhưng giữ điều kiện hỗ trợ

Phần 4.1–4.7 hiện 9 trang nội dung trong build riêng, gồm khoảng 4 trang memory/prior. Giữ bank852/CORE4, strict maturity, nguồn regime end2022/end2020 riêng, fallback/UNKNOWN, công thức similarity/recency và disjoint shrinkage/readiness; không gọi v1 là Beta posterior hoặc B_semantic là embedding. Ca FPT giữ population19 khác K3, bypass C2/A/B. Build ba lượt PASS, không overfull; đã xem trang mới/công thức/bảng. Nguồn/hash/nhãn nghiên cứu không đổi.

### T73f. Rút facts, task inference, teacher/student và policy MT

Phần MT còn khoảng 5 trang; Chương 4 đến 4.8 có 14 trang trong build ghép Chương 3–4. Giữ full task membership, canonical labels/scalers, teacher count likelihood/mixture16, paired37/271873params, synthetic query-soft-target loss, selection seed42-step3000 và utility teacher-sign draws4096. Giữ invalid-anchor/strict quantiles, support và ca FPT không veto. Build đầu theo một chương thiếu nhãn eq:utility ở Chương 3; đã kiểm lại với đúng dependency Chương 3 và sửa chuỗi số quá dài thành số làm tròn có nhãn, policy giữ full precision. Build ba lượt PASS, không overfull/undefined; đã xem các trang MT mới, hình ưu tiên chỉnh nhãn ở T73l.

### T73g. Gộp điều phối, recovery, ứng dụng và khép ví dụ FPT

Chương 4 còn 17 trang trước lượt bố cục T73l. Một giả mã tổng quát thay ba đoạn lặp; giữ upstream một lần/deep-copy, same-repeat dependencies, outcome barrier, distill/cap, prompt<6500/BRPP<=600, retry budget/UNKNOWN/checkpoint và live/provisional/UI PENDING. EX01 giữ LONG lỗ -0.2647317124% sau phí và ba bypass, không biến thành ca thắng/veto. Nội dung A/B/C/F thiết yếu đã có trong chương. Build Chương 3–4 ba lượt PASS; không overfull/undefined, đã xem các trang thay đổi; không chạy recovery hay gọi API.

### T73h. Rút thiết kế, cấu hình và metrics Chương 5 còn 4 trang

Giữ 102points/51accounts/25UP77DOWN/sáu fold/ba Decision repeats và 2448 slots khác quan sát độc lập; cohort/partition/selector/resource và runtime đúng từng nghiên cứu. Giữ estimators theo thứ tự tổng hợp, NA, risk conventions và family20/bootstrap admission; bảng schedule dọc. Build riêng phần thiết kế với dependency Chương 3 ba lượt PASS, bốn trang nội dung đã render/xem, không overfull/undefined. Chỉ đọc kết quả lưu, không fit/replay/API hoặc bootstrap.

### T73i. Rút kết quả/thảo luận, giữ đủ family và kết quả bất lợi

Chương 5 hiện 12 trang, hai bảng kết quả chính riêng, đủ 10method/control rows mỗi bảng và family20 qua hai bảng baseline hẹp. 56 dòng bảng được chiếu nguyên chuỗi ô từ nguồn P8; assets/tables/concise_results.source.json giữ ánh xạ/cột/hash bản Markdown gốc. Giữ numerical controls/factorial seven-BA family, NA, scope/SD, support/bypass, 302/306 anchor agreement, accepted-loss/veto-missed-UP/Native-wrong cases, L1 crossing zero, Native FAIL/NOT_CERTIFIED và ablation chưa làm. Đã đối chiếu/sửa đơn vị exposure sang %, giữ percentile Full–Base BA; build với Chương 3 ba lượt PASS, không overfull/undefined và đã render/xem các trang kết quả. Không sinh bootstrap hoặc nghiên cứu mới.

### T73j. Rút phần đầu còn 10 trang và kết luận còn 2 trang

Giữ nguyên byte nội dung lời cảm ơn/cam đoan đã xác nhận và nguồn bìa; không thêm chữ ký. Abstract rút theo các kết quả còn giữ; glossary/notation gộp một trang, TOC/list tự sinh; Chương 6 trả lời đủ bốn RQ, không kết quả mới. Bản sao preview không phụ lục build ba lượt PASS, phần đầu10/Chương6 hai trang, tổng57 trang trước chỉnh hình/cỡ nhãn T73l; chưa nhận đạt60–70 hoặc T78–T79. Đã render/xem phần đầu và hai trang kết luận.

### T73k. Bỏ phụ lục khỏi bản nộp, giữ nguyên nguồn lịch sử ngoài build

Đã kiểm/lưu 32 member vào archive/p8-source.zip:13 Markdown, nguồn LaTeX P8 và source-map cũ. Hai thư mục phụ lục và 12 file nguồn đã xóa sau đối soát nguyên byte; main.tex không còn appendix/input phụ lục. Hash mốc T72 và hai mảng nguồn lịch sử giữ nguyên, source-map bổ sung locator/raw hash; check.py đọc archive và kiểm được 56 dòng bảng/family20. Chỉ đổi điều hướng hai bản Markdown Chương4–5, nguyên bản trước đổi link còn trong ZIP; link quản lý trỏ archive. Build thực không phụ lục PASS, PDF57trang không Appendix/TOC treo. Compile riêng check.py và strict historical checks PASS; không chạy suite nghiên cứu. Archive ngoài cây LaTeX, không cần để build/gói bản nộp.

### T73l. Hoàn thiện bản 60 trang dọc, bảng đọc được và hình phương pháp

PDF biên tập có **60 trang vật lý**: phần đầu10, Chương1–6 là3/4/6/19/13/2, references3; trong khoảng60–70, không ép từng chương đúng số dự toán. Toàn bộ A4 portrait, rotation=0; không appendix trong nguồn/PDF/TOC/bookmark. Giữ 12pt/giãn1,5/lề2,5cm ngang/3cm trên dưới;17 bảng chính dùng small11pt, năm hình với timeline/F03/MT/policy TikZ có nhãn10pt. Cặp bitmap Pattern/Trend nguyên byte, chú giải đặt ngoài ảnh bằng chữ đọc được. Không landscape/sidewaystable/rotatebox/resizebox hoặc ép mỗi bảng một trang. Các trang hình riêng do float tự sắp để giữ nhãn, không chèn ngắt trang để lấp ngân sách.

Bổ sung lại bảng ưu tiên Indicator, định nghĩa downside denominator và đủ12 execution scenarios vì cần để hiểu heuristic/risk và giữ cả adverse/control; đây là nội dung chọn từ nguồn đã có, không nghiên cứu mới. Ánh xạ bảng hiện68 dòng nguyên ô, đủ20 contrast cells; checker đối chiếu archive/source và bản hiện tại PASS, đối chứng âm đổi một ô trên bản sao bị từ chối.

Build sạch bốn lượt LuaLaTeX+Biber trong cây chỉ có LaTeX/assets/bib PASS, .fls không đọc checkout gốc, không cần Markdown/archive/mẫu/phụ lục. Render toàn60 trang, xem từng contact page và các trang chi tiết, xem lại các trang đổi sau sửa; raster của bản sạch khớp60/60 trang đã kiểm. Không overfull, glyph thiếu, undefined reference/citation hoặc glue-splitting note;129 link nội bộ hợp lệ, không crop/bounds violation hoặc trang trắng. Còn underfull và hai warning bibliography gốc, không tuyên bố zero-warning. Hash lịch sử P8 giữ nguyên; source-map khóa hash LaTeX hiện tại riêng và PDF SHA-256 `704a149251e44ac6a0cb89b3db45288072802a6be9f3185a16af7b8f6be73118`.

Đã compile riêng check.py và kiểm diff/đặc tả. Không chạy compileall/unit/E2E/leakage nghiên cứu vì runtime/bằng chứng không đổi. Đây là QA biên tập T73, chưa thay các lượt rà cuối T74–T80, phản biện ngoài hoặc nghiệm thu/nộp.
