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

## 4. Quy ước bổ sung sổ nguồn

Tiếp tục bổ sung ánh xạ luận điểm/ô bảng, ghi chú kiểm nguồn gốc và danh mục
hình/bảng vào sổ này khi viết. Chưa tạo bibliography mới hoặc bản thảo sáu
chương. Trạng thái nằm duy nhất tại [checklist trong kế hoạch](plan.md#21-một-nguồn-trạng-thái-công-việc);
lịch sử kiểm tra gộp lưu tại README tuần.
