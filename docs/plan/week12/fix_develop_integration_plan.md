# Kế hoạch hợp nhất hệ gốc fix và các mở rộng develop

[Kế hoạch tổng](../plan.md) · [Checklist W12](README.md) · [Đánh giá lịch sử W11](../week11/historical_reevaluation_plan.md)

Ngày khảo sát **09/11/2026**. **U01–U07 hoàn tất và nền đã vào develop. U08 smoke Free/cold verify PASS, research đang thu theo grant riêng với 102 điểm/ba repeat, còn chờ đủ cohort và cold seal. Whole-system causal chưa được chứng nhận**.
Mục tiêu: một hệ thống có hệ gốc truy nguyên được về `fix`, các phương pháp mở rộng từ `develop`, một giao thức đánh giá chung và các bảng bài báo tái lập được từ bằng chứng.

## 1. Kết luận kiến trúc và phạm vi

**Lấy hành vi và hợp đồng khoa học của `fix` làm nền; tiếp tục dùng `develop` làm nhánh tích hợp Git.** Hai lựa chọn này không mâu thuẫn. Không lấy `develop` ghi đè hệ gốc, không tạo hai bản engine độc lập rồi so sánh các báo cáo tổng hợp khác cohort.

Giữ ba lớp nhận diện:

1. `fix_frozen`: nguồn và bằng chứng cũ, chỉ phục vụ kiểm chứng/replay; không sửa byte hoặc gán provenance mới.
2. `original_fix`: đường chạy gốc đã tích hợp, không prior/MT; phải đạt kiểm chứng tương đương với `fix` trên fixture và archive có đủ nguồn. Lời gọi hosted mới không được hứa hẹn trả đúng response lịch sử.
3. `original_common` và các mở rộng: một cấu hình nghiên cứu chung, công khai các thay đổi về report, prompt, giới hạn đầu ra và schema so với `original_fix`. Tên `Original_common` của pilot cũ giữ nguyên trong archive, không đổi nhãn thành `original_fix`.

Tài liệu này khóa thiết kế hợp nhất. U01 đã hoàn tất audit nguồn/bằng chứng tại [README W12](README.md#u01--inventory-nguồn-và-bằng-chứng-đã-khóa); U02 đã ghép nguồn tại nhánh riêng theo [checklist chi tiết](README.md#checklist-chi-tiết-u02). [U03 đã PASS parity offline](README.md#kết-quả-và-giới-hạn-u03) với profile `original_fix_serving_v1`, công khai guard budget và miền legacy-only. [U07 đã nghiệm thu paired/recovery offline](README.md#kết-quả-và-giới-hạn-u07), đủ điều kiện đưa nền phần mềm vào develop. U08 đã PASS smoke Free/cold verify và khởi chạy research theo grant mới, không huấn luyện hoặc sửa kết quả bài báo; U06 giữ nguyên metadata/receipt cũ. Không khôi phục đợt 1.020 điểm đã hủy.

## 2. Bằng chứng khảo sát hai nhánh

### 2.1. Mốc Git khóa cho phân tích

| Đối tượng | Commit |
| --- | --- |
| `fix` và `origin/fix` | `9efd23f4157e0d3ab8069fccab7dccf03439a714` |
| `develop` local trước task | `21f7ee6700ec478ba3e226d54cce2ef261901c62` |
| `origin/develop` sau fetch | `aaf855d3cf908e5735ddf097b150e9767a3e4cb1` |
| Tổ tiên chung | `69800f27a6f84887db624e08acf7d4553f44d5c4` |

`develop` local đi trước remote 36 commit, không có commit remote riêng; cần giữ đủ phần pilot local khi tích hợp. `fix...develop` có **63/286 commit riêng**. Từ tổ tiên chung, `fix` đổi 21.275 đường dẫn và `develop` đổi 598; chỉ bảy đường dẫn cùng đổi. Số file lớn chủ yếu là bằng chứng: 21.052 đường dẫn `outputs/` có ở `fix` nhưng không có tại tip `develop`. Đây là so sánh cây hiện tại, không mặc định các file này từng bị develop xóa.

Mô phỏng `git -c merge.renames=false merge-tree --write-tree --name-only develop fix` không đổi index/worktree/branch. Kết quả có bốn xung đột: `.gitattributes`, `.gitignore`, `AGENTS.md`, `README.md`. Ba file `agents/trend_agent.py`, `core/backtest_engine.py`, `utils/static_util.py` tự ghép được về văn bản. **Tự ghép không chứng nhận tương thích hành vi.** Mô phỏng này chưa phải kiểm thử runtime hay merge thật.

### 2.2. Khác biệt quyết định cách tích hợp

| Thành phần | Bằng chứng đã đọc | Quyết định tích hợp |
| --- | --- | --- |
| P&L | AST của `compute_round_trip_net_return` giống nhau ở hai tip | Giữ một hàm chuẩn; mọi label/account/memory phải gọi hoặc đối soát đúng hàm này |
| Nhãn và records | `fix` có `utils/target_contract.py`, canonical fields, `require_prompt_costs`, `validate_target_record`; develop tip chưa có các phần này | Giữ hợp đồng fix và mở rộng schema prior theo cách tương thích; kiểm caller tạo `TestPoint` và bộ đọc legacy |
| Risk metrics | `fix` có `utils/account_risk.py`, annualisation theo tần suất xác thực và null; engine develop còn nhân `sqrt(252)` trên cycle returns | Giữ sửa đổi fix; kiểm cả engine, prior metrics, MT và UI. Không suy ra pilot H08 mắc cùng lỗi: pilot có statistics riêng |
| Định nghĩa Sortino | Risk helper fix giữ SD population của tập return âm; pilot dùng LPM2 và sample SD cho Sharpe | Version rõ tên/định nghĩa; bảng mới dùng một convention, không đặt hai số khác định nghĩa vào cùng cột |
| Biểu đồ | Fix gắn legend bằng handles thật; develop có `write_artifacts` và wording màu support khác | Giữ fix renderer/legend, thêm tùy chọn ghi file; kiểm tiếng Việt/Anh và màu/line thực tế cùng prompt |
| Decision | Bốn hàm builder prompt cơ sở và `TradeDecisionOutput` có AST giống nhau; distill/cap, wrapper và factory khác | So request cuối sau distill/cap/schema, không chỉ so builder hoặc action |
| Common prompt | `core/mt_bicl_prompt.py` thêm `COMMON_INSTRUCTION` cả khi prefix rỗng | `prior OFF` chưa có nghĩa là `fix` nguyên gốc; bắt buộc bridge và tên phiên bản riêng |
| Alpha/sentiment | Develop thêm strict research mode, wrapper, bỏ nạp `.env` lúc import; graph lịch sử dựng lại năm dòng alpha | Giữ strict mode cho nghiên cứu, kiểm entrypoint live nạp credential; bảo toàn report gốc trong replay và report đủ năm dòng cho common |
| PIT alpha | `fix:core/revision_alpha_contract.py` ghi `native_rowwise_causal_gate=FAIL`, nhưng có outer-cutoff probe riêng | Không diễn giải test phát hiện lỗi PASS thành Zero-Leakage toàn hệ; xử lý phiên bản phương pháp ở mục 5 |
| Adapter lịch sử | `historical_evaluation_protocol.py` đã pin đúng donor fix; graph lấy renderer bằng `git show`, đồng thời import agents từ develop | Tái sử dụng audit, journal, assets; không gọi adapter lai này là bằng chứng đã tích hợp nguyên gốc |
| Dependencies | Develop thêm HMM/sklearn/httpx/tiktoken, pin vnstock/vnai; fix có dependency audit riêng | Khóa môi trường hợp nhất Python 3.13.5; kiểm source pin của receipts cũ trong môi trường đóng băng riêng |
| Bài báo | `paper/`, `revision/`, 28 module `core/revision_*` + 5 module `core/revision72_*`, 43 test và 49 script có ở fix nhưng không ở develop tip | Giữ nguồn tác giả, pipeline sinh bảng và kiểm chứng; không bỏ bằng chứng âm hoặc ghi đè bài cũ bằng pilot |

### 2.3. Kết quả hiện có được phép dùng tới đâu

Đã đọc [receipt H08](../week11/free_pilot_h08_analysis.json), [receipt H09](../week11/free_pilot_h09_handoff.json) và report pilot trên đĩa; đối soát **18 tham chiếu H08 + 7 tham chiếu H09**, tất cả khớp byte length/SHA256. Đây là kiểm file mà receipt dẫn tới, không chạy lại cold consumer hay toàn bộ nghiên cứu.

- Pilot: 48 điểm = bốn mã × 12 ngày, một realization, một repeat; 336 forecast slots gồm sáu primary và Fact_Anchor. **Slots không đồng nghĩa 336 API calls mới** vì có fallback/bypass; bảng primary có 288 predictions.
- Mean return tám tài khoản mã/năm: Original_common −3,690521%; A_tp_pool −2,550858% (chênh +1,139663 điểm phần trăm); MT_BICL −4,414181% (chênh −0,723660 điểm phần trăm). Mọi band chênh return chứa 0; chưa có bằng chứng superiority.
- C2/B_semantic fallback Original 33/48 điểm; A_tp_pool 25/48. MT có action cuối trùng Fact_Anchor ở 48/48 điểm. Đây là lý do cần báo coverage và đóng góp từng tầng, không chỉ xếp hạng cuối.
- Tham chiếu Full fix: 102 điểm, chín mã, 51 tài khoản; mean return khoảng −0,797%, BA khoảng 52,961%. Khác support, prompt và options; **không lấy return bảng fix trừ return pilot để kết luận cải thiện**.
- Bridge pilot là OFF. H07 đầy đủ 1.020 điểm là CANCELLED; kinh tế vẫn `PENDING_EXECUTION_DATA`, chất lượng `VENDOR_SERIES_LIMITED`.
- Bank Bayesian 852 và query donor có provenance khác nhau; MT dùng context numeric riêng. So sánh phương pháp hiện tại bao gồm khác biệt nguồn thông tin này.

## 3. Hệ thống đích

```text
CLI / Web / tác vụ phân tích offline
                 |
     ExperimentSpec + VariantRegistry
                 |
     Dữ liệu PIT + nhãn ở kho riêng
                 |
     Upstream gốc fix, một lần / điểm / realization
                 |
          SharedSnapshot bất biến
                 |
        các bản deepcopy có hash parent
          /             |                 \
 original_fix     original_common     common + prior / MT
          \             |                 /
       ForecastRecord / PolicyRecord / AttemptLedger
                 |
     Evaluator chung + account ledger + thống kê paired
                 |
      CSV/JSON/TeX sinh tự động + evidence manifest
```

Tên interface ở sơ đồ là thiết kế đề xuất, chưa phải API tồn tại. Tận dụng `historical_evaluation_*`, `free_pilot_*`, `prior_*`, `mt_bicl_*` và bộ revision hiện có; chỉ thêm lớp hợp đồng/adapter tối thiểu, không viết lại các engine song song.

- `ExperimentSpec`: protocol/schema version, cohort IDs và calendar, snapshot/commit/runtime/model/prompt hashes, variants, repeats, seed, costs, order, estimand, quy tắc thiếu dữ liệu và namespace output.
- `SharedSnapshot`: reports thô, ảnh, factor values/masks, sentiment availability, cutoff, hashes. Tạo hai projection native/common có provenance; mọi phương pháp common nhận cùng projection. Không chứa future labels hoặc entry/exit thực hiện.
- `VariantRegistry`: ID ổn định, base profile, bật/tắt alpha/sentiment/prior, retrieval mode, phiên bản prompt/schema, dependencies, fallback, student/model hash. Fact_Anchor là dependency và control cho phân tích đóng góp MT, không phải một replication mới.
- `ForecastRecord`: action raw, parse/repair/fallback, request/response hash, ID điểm/repeat/realization. `PolicyRecord` lưu action sau veto cùng nguyên nhân; không gộp raw LLM và final policy.
- `OutcomeRecord` riêng, canonical `net_cycle_v1` hoặc schema kế thừa có version: query/entry/exit indices, prices, gross/net labels, fee/slippage, nguồn. Chỉ nối vào evaluator sau khi forecasts bắt buộc đã durable.
- Một `RunBook`/ledger làm chủ resume. Tránh retry lồng nhiều tầng, tính quota trên mọi attempt, lưu intent trước HTTP. Trạng thái UNKNOWN phải đối soát, không tự gọi lại rồi chọn response thuận lợi.
- UI mặc định hiển thị `original_fix`; menu cho phép mở rộng đã nghiệm thu. Mọi bảng/export hiện rõ version, support, unit, kinh tế, trạng thái dữ liệu. Kiểm JSON native types và `null` ở metric không xác định.
- Các runner cũ thành compatibility entrypoints hoặc consumer của archive. Không dùng output namespace cũ cho code đã đổi và không xóa source pin mà verifier cần.

## 4. Chiến lược Git và bảo toàn bằng chứng

### 4.1. Tích hợp có kiểm soát

1. Đảm bảo worktree sạch; fetch rồi kiểm lại ba commit nguồn. Nếu nguồn thay đổi, bổ sung delta audit trước khi áp dụng kế hoạch.
2. Tạo `feat/fix-develop-unification` từ develop đã cập nhật fast-forward; ưu tiên worktree riêng. Ghi mốc develop/fix vào manifest và tạo local archive refs khi triển khai. Không reset hoặc force-push hai nhánh.
3. Merge **commit fix đã khóa** vào nhánh tính năng bằng `--no-commit --no-ff`. Không dùng blanket `-X ours`, `-X theirs`, hay chọn toàn file engine theo một phía.
4. Xử lý `.gitattributes` để giữ binary/evidence nguyên byte; `.gitignore` giữ cả mô hình, archive và quy tắc bí mật; `AGENTS.md` theo chỉ dẫn người dùng hiện hành; root README tiếng Anh mô tả hệ thống, không chứa tiến độ.
5. Giữ contracts kinh tế/metrics/chart của fix; tích hợp hooks prior, journaling, guards develop theo caller. Bổ sung compatibility cho artifact và schema cũ thay vì sửa chúng tại chỗ.
6. Chỉ tạo merge commit trên nhánh tính năng sau khi checks áp dụng PASS. U02–U03 và các checks U07 bị ảnh hưởng phải đạt trước khi đưa phần tích hợp nền vào develop; giữ công việc phụ thuộc trên nhánh tính năng cho đến lúc đó. Những task tiếp theo tạo nhánh mới từ develop sau khi phần nền đã nghiệm thu, tách commit theo nội dung kỹ thuật; không viết commit phát triển trực tiếp trên develop.
7. Giữ nhánh fix và lịch sử cho đến khi parity, replay và manuscript lineage hoàn tất. Một hệ thống vận hành chung không đòi hỏi xóa lịch sử Git.

Rollback bằng revert commit tích hợp trên nhánh sửa riêng, giữ outputs thử nghiệm ở namespace riêng; không reset lịch sử dùng chung. Nếu dừng trước commit, dùng `git merge --abort` trong worktree tích hợp và kiểm trạng thái. Không tự dọn/xóa dữ liệu lớn.

### 4.2. Quy tắc với artifact

Không merge bằng cách nạp toàn bộ JSON cũ vào memory dùng cho nghiên cứu mới. Phân loại: source runtime, schema/fixtures đang đọc, evidence frozen, generated manuscript, file tạm. Chỉ đóng gói bằng chứng dư thừa nguyên byte theo AGENTS sau khi có inventory và resolver tương thích; không đổi đường dẫn hardcode/hash cùng lúc với port runtime nếu chưa có test consumer.

Không kế thừa gate cũ cho code đã đổi. Receipt cũ tiếp tục chứng nhận đúng snapshot cũ. Release mới lưu mapping nguồn cũ → phiên bản tích hợp → test/replay mới; kiểm bằng tiến trình mới và chế độ không mạng.

## 5. Bảo toàn hệ gốc và xử lý hạn chế nhân quả

### 5.1. Kiểm chứng tương đương hệ gốc

Trên input có đủ provenance và cùng runtime, đối chiếu `fix_frozen` với `original_fix`: chuẩn hóa OHLCV, 600 bars alpha, sentiment/date policy, ảnh/pixel/legend, thứ tự graph, reports, request cuối, model/options/schema, parse/repair, target fields, action mapping và ledger kinh tế. Golden fixtures dùng responses đóng băng hoặc deterministic doubles, không gọi LLM để kiểm parity.

Tách lỗi số học/schema khỏi biến động hosted. AST giống nhau hoặc action trùng chưa đủ: phải so payload, input và call counts. Native prompt vượt 6.500 ký tự phải fail trước API; không âm thầm cắt rồi gọi là parity. Nếu profile cũ không đáp ứng guard, chỉ replay archive ở chế độ legacy, đặt version mới cho profile chạy mới và mô tả delta.

### 5.2. Hạn chế alpha và thông tin lịch sử

Outer cutoff và row-wise causality là hai tiêu chí riêng. Audit fix đã chỉ ra dữ liệu sau một dòng nhưng vẫn trong prefix quyết định có thể làm thay đổi giá trị quá khứ qua normalizer, bfill hoặc nhánh volume. Điều này chưa tự chứng minh dùng dữ liệu sau query cutoff, nhưng chặn khẳng định walk-forward/Zero-Leakage toàn bộ native selector.

- Giữ native fix để tái lập nghiên cứu cũ; đưa hạn chế vào metadata/report, không nâng nhãn thành causal PASS.
- Trước nghiên cứu mới có mục tiêu kiểm chứng nhân quả, thêm `causal_common_v1`: preprocessing fit trên train/prefix, selection/orientation chỉ dùng labels trưởng thành, purge các horizon giao nhau, validation để chọn cấu hình, test khóa. Kiểm bằng future poisoning và prefix extension tại từng dòng có liên quan.
- Áp dụng cùng profile causal cho baseline và mọi mở rộng trong family mới; giữ bridge native → causal trên cùng dữ liệu. Không trộn sửa alpha vào riêng Bayesian/MT rồi quy chênh lệch cho prior.
- Nếu chưa hoàn thành profile causal, chỉ phát hành so sánh historical exploratory conditional, ghi gate chưa đạt. Bảo toàn code native không đồng nghĩa cho phép công bố Zero-Leakage.
- Tin date-only cần policy availability đã khóa, loại undated; model/sentiment checkpoint phải pin. Metadata ngày không chứng nhận nội dung tin thật sự đã có tại thời điểm đó.
- HMM/scaler chỉ fit trên lịch sử hợp lệ, không smooth với tương lai; memory yêu cầu `exit_date < query`. Context prequential chỉ nhận nhãn trưởng thành sau khi forecasts bắt buộc đã lưu; strict holdout frozen là chế độ khác và không trộn hai chế độ.

## 6. Thiết kế so sánh phục vụ bài báo

### 6.1. Hai câu hỏi, hai family

| Family | Baseline và so sánh | Kết luận được phép |
| --- | --- | --- |
| Hiệu quả hệ thống | `original_fix` so với năm hệ mở rộng đã khóa, cùng cohort, labels, model serving profile và shared raw upstream | Chênh lệch của gói hệ thống; bao gồm thay đổi report/prompt/context/policy đã khai báo |
| Đóng góp phương pháp | `original_common` so với v1, C2, A_tp_pool, B_semantic, MT_BICL dưới cùng common profile | Hiệu quả có điều kiện trên reports/common prompt; riêng MT vẫn là gói anchor + student + utility + policy |
| Bridge | `original_fix` → `original_common`, và native → causal nếu có | Định lượng ảnh hưởng chuẩn hóa/sửa nền; không gán cho Bayesian hoặc student |

Đây là thiết kế mới. Các bảng pilot48 giữ nguyên protocol cũ. Nếu profile phục vụ mới phải đổi model/options so với fix, ghi tên `original_fix_serving_v1` hoặc version tương đương; đó là port phương pháp, không phải tái tạo response lịch sử.

Giữ năm mở rộng primary hiện có, không chọn lại chỉ những phương pháp đẹp trên pilot. Gộp rõ họ Bayesian v2 có C2 đại diện, A/B là hai nhánh, MT có dependencies. Fallback hợp lệ là một phần thuật toán và phải báo; bản schema lỗi/unknown không được biến thành CASH hoặc xem như fallback đã định trước.

### 6.2. Controls và ablations

- Không LLM: CASH, always-LONG theo từng cycle trả phí đầy đủ; price-only continuous hold nếu có dữ liệu phù hợp, tên riêng với cycle LONG. Các baseline numeric train-only từ fix chỉ dùng sau kiểm target/support/causal adapters.
- Retrieval: random/recent/similarity/bayesian dưới cùng bank, K, projection, schema và budget để đo thêm giá trị regime. Nếu khác bank hoặc historical model, mô tả là so gói dữ liệu/phương pháp.
- Prior: stats-only/examples-only và bỏ regime theo registry đã khóa; theo dõi gate active, effective K, fallback, age, similarity, regret và coverage.
- MT: Original_common → Fact_Anchor → MT_BICL; Plain_revision, No_utility, No_target, Stats_only, Utility_only ở panel đã định trước. Báo raw proposal, veto và final action riêng. Bằng chứng pilot action MT trùng anchor không hỗ trợ nhận student tạo ra toàn bộ chênh lệch.
- Alpha/sentiment: giữ B/A/S/AS và placebo của revision như family riêng. Nếu chạy mới, cùng năm factor rows/masks, schema và budget; không diễn giải numeric selector controls thành LLM selector ablation.

### 6.3. Cohort và tách dữ liệu

1. Giữ pilot48 như bằng chứng thăm dò cũ. Dùng làm regression/support audit, không làm final test chưa từng thấy.
2. Giai đoạn historical mới đề xuất dùng **102 anchor units có nguồn từ fix** làm cohort tham chiếu mở rộng, chỉ sau khi kiểm đủ support của mọi phương pháp. Khóa `CORE4` subset và phạm vi chín mã/BHN có suffix hợp lệ như secondary trước inference. Không tự gán 102 thành số điểm usable hoặc mặc định bằng 1.020.
3. Nếu thiếu support của một phương pháp, báo planned/eligible/complete/failed theo cùng IDs; công bố flow loại trừ có lý do từ input, không từ returns. Paired family dùng mask chung đã định trước và sensitivity thiếu dữ liệu; tài khoản thiếu action không được compound như thể ngày đó không tồn tại.
4. Train, validation, checkpoint selection và exposed historical có ledger riêng. Seed42/step3000 đã chọn ở study cũ là asset đóng băng, không chọn lại bằng kết quả cohort mới. Kiểm label horizon chứ không chỉ ngày bắt đầu khi purge split/memory.
5. Nghiên cứu xác nhận cần khoảng tương lai sau freeze thực sự, universe/PIT membership, power hoặc precision target và N khóa trước outcome. Không có dữ liệu chưa xem thì giữ nhãn exploratory; tăng repeats không tạo thêm N thị trường.

### 6.4. Pairing, repeats và chi phí

Một upstream/điểm/realization, deepcopy sang mọi nhánh. Alpha/sentiment/full preparation chạy một lần khi inputs giống nhau; native/common projection được dựng từ cùng raw state. Decision repeats dùng requests mới trên shared upstream đã khóa, không lấy cache response làm repeat độc lập. Nếu đo variance upstream, dùng realization riêng và mọi nhánh cùng nhận realization đó.

Đề xuất ba Decision repeats cho nghiên cứu mở rộng nếu quota đủ; đây là tham số dự kiến, chỉ khóa sau preflight. Counterbalance các nhánh độc lập, giữ DAG Original → Fact_Anchor → MT; log order/time/org/epoch thực tế và công khai hạn chế không thể counterbalance hoàn toàn. Không vote/best-repeat, không chuyển model/key ngầm, không chọn kết quả theo latency.

Ngân sách tính trước bằng số slot thực sự và dependency: N × R × (hai baseline + năm extension + Fact_Anchor) = **8NR Decision slots** cho dual-baseline design; nếu N=102, R=3 thì 2.448 slots trước controls, smoke và retry. Nếu upstream dùng hai vision calls/realization, chi phí vision mới tối đa dự kiến 2NU trước reuse/retry; phải xác minh call graph thực tế, không coi công thức là cam kết quota. Fallback/bypass có thể giảm calls nhưng không giảm số forecasts phải audit. Chưa cấp quyền tự chạy theo con số này; giữ cấu hình paid API OFF cho đến release được chốt theo yêu cầu tiếp theo.

Không nối 48 response cũ với các baseline mới thành một cohort hosted đồng thời mà bỏ qua epoch/model khác nhau. Archive reuse chỉ khi identity đầy đủ khớp và protocol cho phép; so sánh conditional replay phải ghi đúng tên.

### 6.5. Metrics và suy luận

Hợp đồng kinh tế cố định: LONG mua `Open(t+1)`, bán `Close(t+3)` theo lịch phiên; SHORT giữ tiền mặt. Với `fee=0.0025`, `slippage=0.001` mỗi chiều, hàm chuẩn tính `r_net = (exit_close/entry_open) * (1-fee)*(1-slippage) / ((1+fee)*(1+slippage)) - 1`. Nhãn UP khi `r_net>0`, còn lại DOWN; không thay bằng Close-to-Close, không dùng TP/SL mô tả để đổi horizon. Kiểm giá nghìn VND chuyển sang VND đúng một lần; nghiên cứu stress chi phí có version riêng và không đổi nhãn primary đã khóa.

- Primary đề xuất: chênh mean independent account net return, units là điểm phần trăm; báo rõ reset theo symbol/fold hoặc symbol/year, không trộn hai hệ. Tài khoản LONG all-in fractional, SHORT=CASH, 50 triệu VND ban đầu theo protocol. Không gọi trung bình account là portfolio return.
- BA là endpoint phân loại chính trong family phân loại riêng; kèm confusion, UP/DOWN support, accuracy, MCC, F1 mỗi lớp, macro-F1, LONG rate. Mẫu số không xác định cho null/NA, không bù 0.
- Kinh tế: daily MTM MDD và cycle-end MDD riêng, exposure, turnover, phí/slippage, số giao dịch, cash giữa query. Phân biệt forecast return ứng viên LONG và strategy return sau action/veto/no-fill.
- Không annualize cycle thưa bằng sqrt(252). Daily ratios cần daily NAV đầy đủ và convention khóa; cycle Sharpe/Sortino ghi công thức, ddof, downside và tần suất. Replay số cũ bằng convention cũ, bảng mới bằng convention chung.
- Resampling theo ngày/block chung qua mọi mã/phương pháp/repeat; không bootstrap từng symbol-date như mẫu độc lập. Rebuild account theo lịch/tái lấy block đã khai báo. Cùng draw indices cho contrasts paired.
- Khóa multiplicity cho tất cả contrasts/endpoint dùng để nhận superiority. Hai family cùng baseline khác nhau không cho phép chọn family có kết quả đẹp; dùng family chính xác nhận duy nhất hoặc điều chỉnh chung nếu kết luận trên cả hai. Historical ít block chỉ báo sensitivity, không khẳng định coverage/power từ số bootstrap draws.
- Báo effect size, uncertainty, số cluster, undefined draws, per-repeat dispersion và leave-one-block/symbol-out. McNemar/Wilcoxon iid không làm bằng chứng chính nếu còn phụ thuộc thời gian/xuyên mã. Không chọn subgroup sau khi nhìn hiệu ứng.
- Student/teacher numeric probability có thể đánh giá calibration trên đúng target; categorical confidence LLM không tự đổi thành xác suất để tính Brier/ECE.

## 7. Trình tự triển khai và điều kiện hoàn thành

Checklist trạng thái duy nhất ở [README W12](README.md). Các mục dưới là hợp đồng công việc, không phải receipt đã PASS.

U02 được chia thành U02.1–U02.9 tại [checklist chi tiết](README.md#checklist-chi-tiết-u02):
khóa nguồn/nhánh → giải quyết merge quản trị → engine contracts → schema/callers
→ chart/prompt → dependency lock → byte evidence → kiểm thử đúng phạm vi → commit/bàn giao.
Mỗi mục chỉ đánh dấu khi đầu ra tương ứng đã được kiểm; gate đưa nền vào develop
được theo dõi riêng sau U03 và phần U07 bị ảnh hưởng.

U03 có [checklist riêng](README.md#checklist-chi-tiết-u03) cho profile native,
golden requests, graph/ảnh/PIT, archive, CLI/UI và cold replay. Oracle chỉ nạp
nguồn Git donor trong tiến trình cách ly; cap native không được âm thầm đổi
để vượt guard, và mọi support archive thiếu phải được báo trước khi nghiệm thu.

U04 đã có [checklist và kết quả](README.md#kết-quả-và-giới-hạn-u04) cho registry,
snapshots/records, lazy adapters, RunBook/evaluator và CLI/UI offline. Native,
sáu phương pháp nghiên cứu và Fact_Anchor dùng chung evaluator; replay CLI
conditional trên prepared assets, không nhận là thu hosted hoặc chạy lại student/
retrieval. Provider/cohort/protocol/transport cho release mới vẫn phải qua U06–U08.

U05 đã có [profile và bridge riêng](README.md#kết-quả-và-giới-hạn-u05): đủ 85
handler PIT, orientation train, selection validation đã purge và test lock;
Spec v2 áp dụng cùng projection cho mọi common method, giữ native request.
Native row-wise vẫn FAIL; alpha PIT local không thay gate HMM/retrieval/news/
student/providers và protocol U06/U07. Không sửa bằng chứng frozen hoặc nhận
hiệu ứng hosted/superiority từ fixture bridge.

| Mục | Nhánh đề xuất / công việc | Đầu ra và điều kiện thoát |
| --- | --- | --- |
| U01 | `docs/fix-develop-source-audit`: inventory nguồn/evidence/imports/callers, khóa nguồn trước code | Mapping ownership và hashes đầy đủ; phân biệt source đang chạy và archive, nhận diện path hardcode |
| U02 | `feat/fix-develop-unification`: merge fix vào nhánh từ develop, xử lý contracts/schema/renderer/dependencies | Một cây nguồn; không mất evidence; economic/target/risk/chart tests đúng phạm vi PASS |
| U03 | `test/original-fix-parity`: golden request, deterministic graph, archive replay và CLI/UI cũ | Original port đạt parity theo nguồn có provenance; mọi delta chủ động có version, chưa gọi hosted |
| U04 | `refactor/variant-experiment-contract`: registry, snapshots, records, runner và UI/export chung | Sáu phiên bản nghiên cứu + native baseline/dependency dùng cùng evaluator; prior OFF không mở bank/model vô ích |
| U05 | `fix/causal-common-profile`: audit/sửa preprocessing/selector theo train-only nếu làm study causal | Prefix/future poison và purged selection PASS; bridge native/causal rõ, frozen artifacts nguyên byte |
| U06 | `docs/unified-comparison-protocol`: khóa cohort/estimand/controls/repeats/multiplicity/quota/exposure | Offline preflight và manifest hoàn chỉnh; đủ nguồn, không còn lựa chọn sau khi nhìn outcome |
| U07 | `test/unified-paired-recovery`: kiểm đường chạy chung và failure injection | Một upstream; query label không vào state; resume/UNKNOWN/schema repair đúng; verify offline không tạo client |
| U08 | `feat/unified-comparison-run`: smoke mới rồi thu theo release protocol mới | Raw attempts/responses, order/usage/checkpoints/labels đủ; không hồi sinh full1020; báo coverage/thất bại |
| U09 | `feat/unified-comparison-analysis`: tính bảng từ forecast/ledger đã seal | Hai family và bridge đúng support; new-process offline replay khớp; kết quả âm/undefined giữ nguyên |
| U10 | `docs/manuscript-unified-system`: cập nhật nguồn paper của fix và bàn giao | Mỗi số truy về CSV/JSON/code/protocol; LaTeX build và render QA; claims đúng scope, archive tái lập |

Thứ tự phụ thuộc: U01 → U02 → U03 → U04; U05 trước release có tuyên bố causal. U06 chuẩn bị từ U01 nhưng chỉ khóa sau U03–U05 theo scope. U07 → U08 → U09 → U10. Chưa ước lượng ngày hoàn thành inference khi chưa audit quota và support. Ưu tiên xong parity/runner trước khi trả chi phí nghiên cứu mới.

U06 v1 giữ [preflight BLOCKED](README.md#kết-quả-và-giới-hạn-u06) nguyên byte.
Theo yêu cầu hoàn thiện, [amendment v2](README.md#kết-quả-nghiệm-thu-u06-v2)
khóa split/selector trước anchor đầu từng mã, giữ102 test anchor và ngưỡng U05,
51 binding/chín fit frozen, đủ provider controls102 điểm và quota attestation
hiện tại. U06 đã PASS146 test và cold restore/replay102/102 trên nguồn đã khóa.
Prototype expanding có exposure được ghi rõ, không dùng vào study cuối.
Input-eligible và collection-eligible là hai gate riêng: U07 đã PASS116 test,
cold replay102 điểm/2.448 slot, scope chín mã/paired/recovery và dispatcher org
với HTTP mock. U08 còn cần transport live, quota headers/smoke/
grant mới. Không thu nhỏ cohort, sửa receipt cũ hoặc kế thừa quyền inference.

### Kiểm thử theo phạm vi

| Vùng thay đổi | Bộ kiểm hiện có cần chọn và phần cần bổ sung |
| --- | --- |
| Engine/target/risk | `test_account_risk` và `test_target_contract` từ fix; `test_account_pnl`, `test_prior_backtest_integration`, `test_free_pilot_statistics`; bổ sung kiểm lịch phiên, canonical schema giữa legacy/prior/MT và no-trade/undefined |
| Graph/chart/prompt | `test_chart_convention` từ fix; `test_backtest_token_budget`, `test_paired_protocol`, `test_prior_graph_integration`, `test_prior_prompt_contract`, `test_mt_bicl_decision`; golden final payload, cả hai ngôn ngữ, 5 factor rows, len<6500 và prefix≤600 |
| PIT/retrieval/alpha | Leakage suites đúng đường đổi: alpha contract/selection, sentiment, regime, historical memory, prior context/paired, MT tasks/features/adapter, historical adapter và free pilot; test query-y firewall và matured labels |
| Retry/checkpoint | Prior checkpoint/stage recovery, research invocation/input lock, historical journal/transport, free pilot recovery/manager; stop/resume tại intent, success-before-save, parse repair và unknown |
| Statistics/evidence | Revision dependent statistics/reproducibility, free pilot analysis/statistics/package, historical evaluation statistics; paired masks, account/reset conventions, multiplicity, archive byte preservation |
| CLI/UI | Entry points gốc và thống nhất, `test_web_json_serialization`, fixture không mạng và lựa chọn variant; lỗi vẫn hiện rõ, không default CASH |

Tên module cần đối chiếu với inventory sau U02; test mới đặt tên riêng, không ghi thành đã tồn tại. Chỉ compile file Python thay đổi; chạy các caller/integration và leakage liên quan. Không tự chạy toàn suite/E2E. Gate cũ chỉ viện dẫn sau đối soát đúng source/runtime/receipt; thay code nào kiểm lại vùng đó.

## 8. Cập nhật bài báo và tiêu chí bàn giao

Giữ title/tác giả/cấu trúc từ `fix:paper/` trừ khi người dùng yêu cầu đổi. Cập nhật phương pháp và kết quả theo code đã nghiệm thu, không đưa kế hoạch thành kết quả.

1. **Architecture/Methods:** hệ gốc fix, bảng variants, common projection, regime/memory/MT và gate/fallback; phương trình net target, mapping SHORT=CASH và scope L=3.
2. **Experimental setup:** bảng dataset/splits/exposure/cohort, native/common/causal profiles, model/options/repeats/order, common support, tiền đề chi phí, dependency calls và compute budget.
3. **Results:** bảng hệ thống so với fix; bảng conditional common; bridge; ablation/controls; risk/exposure/failure/coverage. Các bảng revision cũ và pilot giữ scope rõ, không pool như độc lập.
4. **Discussion/Limitations:** alpha native causality, bank/query provenance, news availability, hosted contamination, ít calendar clusters, exposure/routing và vendor execution assumptions. Nếu không có cải thiện, giữ kết luận không có bằng chứng cải thiện.
5. **Supplement/Reproducibility:** registry/config, ID lists, raw request provenance, data/model/source/runtime hashes, CSV/JSON, script sinh TeX/figures, lệnh offline và evidence manifest; quyền công bố dữ liệu tách khỏi khả năng replay nội bộ.

Không gõ tay số headline. Tái dùng bộ `scripts/build_revision_manuscript.py` và pipeline sinh bảng sau audit; mỗi cell có nguồn và version. Nếu sửa schema bảng, thêm kiểm tra rounding/unit/denominator, không chỉnh prediction archive. Render PDF và kiểm bảng, công thức, caption, reference; không cần sửa PDF trong task lập kế hoạch này.

Hệ thống chỉ được gọi **hợp nhất hoàn chỉnh** khi native parity, registry chung, economics/PIT/paired/recovery gates trong scope, thống kê chung, CLI/UI và cold replay đều đạt. Bài báo chỉ được cập nhật kết quả mới sau U09. Tích hợp phần mềm thành công, lợi thế thống kê và khả năng giao dịch thực là ba tiêu chí khác nhau.

## 9. Kiểm tra của task lập kế hoạch

Đã khảo sát nguồn/AST hai tip, đọc phương pháp và bản thảo fix, kiểm receipts pilot, fetch/pull fast-forward, mô phỏng merge ngoài worktree và tạo nhánh tài liệu từ develop. Chỉ sửa Markdown dưới `docs/plan/`; không sửa code/test/schema/config/data/paper, không gọi API và không huấn luyện.

Kiểm bàn giao: diff whitespace, liên kết Markdown local, số liệu/commit và file hashes được viện dẫn. Không chạy compileall/unit/E2E/leakage vì task thuần phân tích/tài liệu theo AGENTS §1.2; không nhận gate runtime mới. Commit/merge tài liệu theo Conventional Commits là độc lập với việc merge mã nguồn fix vào develop.
