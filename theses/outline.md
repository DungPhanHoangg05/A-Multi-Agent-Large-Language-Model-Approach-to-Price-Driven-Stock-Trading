# Dàn bài khóa luận tốt nghiệp

## A. Định hướng đề tài

**Tên tiếng Việt đề xuất:** Học trong ngữ cảnh Bayes đa tác vụ có xét trạng thái thị trường cho hệ thống giao dịch cổ phiếu đa tác tử sử dụng mô hình ngôn ngữ lớn tại Việt Nam.

**Tên tiếng Anh theo định hướng dự án:** Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market.

**Trục lập luận:** xuất phát từ hệ thống phân tích giá đa agent, xây dựng ngữ cảnh lịch sử hợp lệ theo thời điểm và trạng thái thị trường, đưa ngữ cảnh vào Decision Agent bằng các cơ chế prior và MT-BICL, rồi đánh giá ảnh hưởng lên dự báo và hành động LONG/CASH trong cùng hợp đồng kinh tế.

Tên đề tài mô tả hướng nghiên cứu, không hàm ý các phương pháp đã chứng minh vượt trội. Cần giải thích riêng “đa tác vụ” trong MT-BICL và “đa agent” trong kiến trúc; không dùng hai khái niệm thay thế nhau.

### A.1. Mục tiêu và phạm vi

- Mô tả chính xác hệ thống đã xây dựng: đầu vào giá/tin, các báo cáo agent, bộ nhớ lịch sử, nhận diện regime, truy xuất prior, student/teacher, policy và bộ đánh giá.
- Đánh giá giá trị bổ sung của ngữ cảnh lịch sử trên cùng dữ liệu, cùng upstream và cùng quy tắc giao dịch, bao gồm cả trường hợp thiếu support hoặc kết quả bất lợi.
- Phân biệt ba lớp đóng góp: thích nghi/tích hợp hệ gốc; thiết kế các cơ chế ngữ cảnh và policy; xây dựng quy trình đánh giá, truy vết và tái lập.
- Tập trung vào dữ liệu ngày và nghiên cứu lịch sử đã lưu. Giao diện realtime là phần minh họa phần mềm; chưa phải bằng chứng lợi nhuận ngoài thực tế hoặc kết quả kiểm định tiền cứu.
- Kế thừa QuantAgent phải được ghi nguồn. Không trình bày các agent, HMM, Alpha101, Beta–Bernoulli hay kiến trúc student được kế thừa như thuật toán hoàn toàn mới do khóa luận phát minh.

### A.2. Câu hỏi nghiên cứu

| Mã | Câu hỏi | Cách trả lời trong khóa luận |
| --- | --- | --- |
| RQ1 | Hệ đa agent kết hợp giá, alpha và sentiment có hành vi dự báo/giao dịch như thế nào so với các đối chứng? | Nghiên cứu thành phần: Full/Base, đối chứng số và các panel thành phần đã thực hiện; báo cả chất lượng phân loại và kết quả tài khoản. |
| RQ2 | Ngữ cảnh lịch sử có xét regime và thống kê điều kiện làm thay đổi kết quả thế nào trên cùng upstream? | So Bayesian v1, C2, A_tp_pool, B_semantic với Common và Native; phân tích support, fallback, độ tuổi và phạm vi ngân hàng lịch sử. |
| RQ3 | Chuỗi Fact Anchor → MT-BICL và policy utility tác động thế nào tới quyết định cuối? | Phân rã Common → Fact Anchor → MT-BICL; đối chiếu raw proposal, veto và final action. Chỉ kết luận riêng về student nếu có ablation phù hợp. |
| RQ4 | Những ràng buộc thời gian, kinh tế và vận hành nào có thể kiểm chứng, và giới hạn nào còn tồn tại? | Audit PIT/row-wise causality, nhãn và P&L, ghép cặp, ngân sách prompt, checkpoint, cold replay; phân biệt từng gate với chứng nhận toàn hệ. |

### A.3. Quy tắc sử dụng bằng chứng

1. **Mã đã có không đồng nghĩa thí nghiệm đã chạy.** Mỗi bảng kết quả phải có cohort, protocol, nguồn artifact và trạng thái nghiệm thu tương ứng.
2. **Đánh giá lịch sử mang tính thăm dò.** Các fold đã được quan sát không trở thành holdout chưa sử dụng chỉ bằng cách đổi tên.
3. **Không gộp hai nghiên cứu.** Nghiên cứu thành phần và nghiên cứu ngữ cảnh lịch sử có responses, support và quy ước thống kê riêng.
4. **Không đồng nhất cutoff với nhân quả toàn hệ.** Native row-wise causal còn `FAIL`; whole-system causal còn `NOT_CERTIFIED`. Causal-common chỉ có phạm vi kiểm chứng riêng.
5. **Giữ kết quả âm và fallback.** Không loại các điểm thiếu prior khỏi bảng chính để tạo lợi thế; phân tích trên tập có support phải ghi rõ là phân tích phụ.

## B. Khung tổ chức kế thừa từ mẫu

| Vị trí | Cấu trúc tham chiếu | Nội dung của khóa luận mới |
| --- | --- | --- |
| Phần đầu | Hai trang bìa; Abstract; Acknowledgements; Declaration; mục lục; danh mục hình; từ viết tắt | Điền metadata của khóa luận mới sau khi xác nhận; thêm danh mục bảng và bảng ký hiệu vì có nhiều đại lượng/phương pháp. |
| Chương 1 | Introduction | Bối cảnh, bài toán, mục tiêu, câu hỏi, đóng góp và phạm vi. |
| Chương 2 | Related Works | Nghiên cứu giao dịch định lượng, LLM đa agent, regime, ICL/Bayesian ICL và phương pháp đánh giá. |
| Chương 3 | Theoretical Background | Các khái niệm, ký hiệu, hợp đồng kinh tế, HMM, Bayes, MT-BICL và đánh giá cần dùng. |
| Chương 4 | Chương phương pháp đề xuất | Kiến trúc hiện thực, ngữ cảnh lịch sử, các biến thể prior, MT-BICL và vận hành. |
| Chương 5 | Experiments and Results | Thiết kế thực nghiệm, hai nhóm kết quả, phân tích cơ chế và giới hạn suy luận. |
| Chương 6 | Conclusions and Future Works | Trả lời câu hỏi nghiên cứu, đóng góp đạt được, hạn chế, hướng phát triển. |
| Phần cuối | References | Tài liệu tham khảo riêng của đề tài; bổ sung phụ lục thuật toán, hợp đồng, bảng mở rộng và tái lập. |

Mẫu dùng A4, cỡ chữ 12pt, giãn dòng 1,5; phần đầu đánh số La Mã, nội dung chính đánh số Ả Rập, mục lục hiện đến cấp mục. Đây là tham chiếu từ nguồn mẫu, chưa thay thế quy định trình bày chính thức. Không sao chép các macro, định lý hay tài liệu tham khảo chuyên biệt của đề tài mẫu.

**Dung lượng dự kiến:** khoảng 65–81 trang nội dung sáu chương, chưa tính phần đầu, tài liệu tham khảo và phụ lục. Đây là phân bổ biên soạn để cân đối phương pháp/thực nghiệm, không phải ràng buộc số trang.

## C. Mục lục rút gọn

1. **Mở đầu — Introduction**
2. **Tổng quan nghiên cứu liên quan — Related Work**
3. **Cơ sở lý thuyết và mô hình bài toán — Theoretical Background and Problem Formulation**
4. **Hệ thống đa agent với ngữ cảnh Bayes theo trạng thái thị trường — Regime-Aware Bayesian Context for Multi-Agent Trading**
5. **Thực nghiệm và thảo luận — Experiments and Discussion**
6. **Kết luận và hướng phát triển — Conclusions and Future Work**

Tài liệu tham khảo; Phụ lục A–F.

## D. Dàn bài chi tiết

### Phần đầu khóa luận

- **Bìa ngoài và bìa trong:** cơ sở đào tạo, tên đề tài, sinh viên, mã sinh viên, ngành, người hướng dẫn, địa điểm/năm; thông tin chưa có để trống ở giai đoạn dàn bài.
- **Tóm tắt / Abstract:** bài toán → cách tiếp cận → thiết kế đánh giá → kết quả chính có giới hạn → đóng góp. Viết sau Chương 5; tránh tuyên bố có lợi nhuận hoặc vượt trội khi bằng chứng không hỗ trợ.
- **Lời cảm ơn; lời cam đoan:** soạn mới theo thông tin thực tế và yêu cầu của đơn vị.
- **Mục lục; danh mục hình; danh mục bảng.**
- **Danh mục từ viết tắt và ký hiệu:** LLM, VLM, ICL, BICL, MT-BICL, HMM, PIT, OHLCV, BRPP, BA, MCC, NAV; phân biệt prior, posterior, confidence, utility, return và support.

### Chương 1. Mở đầu

**Mục đích:** đặt bài toán và xác định điều khóa luận sẽ kiểm chứng. **Dung lượng:** 5–7 trang.

#### 1.1. Bối cảnh và động cơ nghiên cứu

- Dữ liệu giá, mẫu biểu đồ, chỉ báo và tin tức cung cấp các loại tín hiệu khác nhau cho hỗ trợ quyết định cổ phiếu.
- LLM/VLM có thể diễn giải báo cáo và biểu đồ nhưng cần kiểm soát tính nhất quán, dữ liệu sẵn có tại thời điểm quyết định và chi phí vận hành.
- Động cơ bổ sung các tình huống lịch sử theo trạng thái thị trường khi các agent bất đồng hoặc mẫu lịch sử ít.
- Đặc thù của mô phỏng cổ phiếu Việt Nam: hành động long-only, độ trễ vào/thoát và phí hai chiều; trình bày như hợp đồng nghiên cứu, không khái quát thành mọi cơ chế giao dịch thực tế.

#### 1.2. Phát biểu bài toán

- Đầu vào tại ngày quyết định `t`: lịch sử OHLCV, thông tin regime, sentiment đủ điều kiện thời gian, các episode lịch sử đã kết thúc.
- Đầu ra dự báo LONG/SHORT, hành động thực thi LONG/CASH và báo cáo có thể truy vết.
- Hai đích đánh giá khác nhau: đúng nhãn lợi nhuận ròng và kết quả tài khoản sau chi phí.

#### 1.3. Mục tiêu và câu hỏi nghiên cứu

- Trình bày RQ1–RQ4 cùng các đối chứng tương ứng.
- Xác định rõ giả thuyết cần kiểm chứng; không viết trước kết luận “regime” hoặc “multi-task” luôn cải thiện kết quả.

#### 1.4. Thách thức và phạm vi

- Thị trường không dừng, mẫu nhỏ/phụ thuộc thời gian, thiếu tin, thiếu ngân hàng lịch sử cho một số mã.
- Rò rỉ thời gian ở query và trong các hàng lịch sử; khác nguồn giữa bank/query; khác biệt native/common.
- Ngẫu nhiên LLM, giới hạn prompt/API, fallback và policy làm thay đổi hành động.
- Phạm vi dữ liệu ngày, tập mã/ngày đã chọn; không đồng nhất với giao dịch tần suất cao hay danh mục thực chiến.

#### 1.5. Đóng góp và bố cục

- Nêu đóng góp hiện thực có thể kiểm tra qua module/artifact.
- Nêu kết quả thực nghiệm theo mức bằng chứng; kết quả âm vẫn là phát hiện cần báo cáo.
- Tóm tắt quan hệ Chương 2 → 3 → 4 → 5 → 6.

**Hình/bảng dự kiến:** một hình bài toán đầu vào–đầu ra; một bảng câu hỏi–phương pháp–bằng chứng.

### Chương 2. Tổng quan nghiên cứu liên quan

**Mục đích:** đặt hệ thống vào các hướng nghiên cứu, chỉ ra phần kế thừa và khoảng trống. **Dung lượng:** 8–10 trang.

#### 2.1. Phân tích kỹ thuật và mô hình định lượng cho dự báo cổ phiếu

- Chỉ báo giá/khối lượng, alpha factors và các đối chứng thống kê/máy học.
- Alpha101 và giới hạn khi chuyển công thức chéo tài sản sang chuỗi đơn tài sản.
- Sự khác nhau giữa tín hiệu xếp hạng trong mẫu và hiệu quả giao dịch ngoài mẫu.

#### 2.2. LLM, VLM và hệ đa agent trong tài chính

- Phân công vai trò, biểu diễn trạng thái chung và tổng hợp bằng chứng giá/tin.
- QuantAgent như nguồn kiến trúc kế thừa; xác định phần dùng lại, phần sửa và phần bổ sung của dự án.
- Giới hạn đọc biểu đồ, độ tin cậy của lời giải thích và độ biến thiên đầu ra.

#### 2.3. Nhận diện trạng thái thị trường

- HMM và cách mô hình hóa trạng thái ẩn; các hướng dựa trên xu hướng/biến động.
- Nhận diện bằng dữ liệu chỉ tới cutoff, đóng băng fit, rủi ro dùng smoothing có dữ liệu tương lai.
- Regime như biến điều kiện của truy xuất, không tự nó là tín hiệu mua/bán được bảo đảm.

#### 2.4. In-context learning, truy xuất ví dụ và Bayesian ICL

- Few-shot ICL, retrieval, lựa chọn ví dụ và phân biệt với cập nhật trọng số LLM.
- Thống kê Bayes như cách biểu diễn bằng chứng hữu hạn; prior/posterior và giới hạn diễn giải.
- Truy xuất ví dụ, cung cấp thống kê và học đa tác vụ là các cơ chế khác nhau cần tách khi đánh giá.

#### 2.5. Multi-task Bayesian ICL và student–teacher

- Prior tasks, target-task observations, phân bố tác vụ và suy luận cho query.
- Vai trò teacher, student và quá trình huấn luyện/đóng băng tài nguyên trước đánh giá.
- Chỉ rõ quan hệ giữa phương pháp tham khảo và bản triển khai của dự án; không gọi mọi prompt có nhiều ví dụ là MT-BICL.

#### 2.6. Đánh giá hệ thống giao dịch có LLM

- Walk-forward, purge nhãn giao cắt phân vùng, backtest có chi phí, so sánh ghép cặp.
- Ablation, đối chứng số, kiểm định trên dữ liệu phụ thuộc và khả năng tái lập.
- Phân biệt đánh giá thăm dò lịch sử với nghiên cứu tiền cứu chưa tiếp xúc kết quả.

#### 2.7. Khoảng trống và vị trí của đề tài

- Tổng hợp bảng: loại đầu vào, kiến trúc, ngữ cảnh lịch sử, regime, PIT, hợp đồng kinh tế và đối chứng.
- Xác định vấn đề đề tài trực tiếp xử lý và vấn đề vẫn chưa chứng minh được.

**Bằng chứng cần chuẩn bị:** đọc nguồn gốc của các công trình trước khi điền bảng so sánh; có thể dùng thư mục bài báo hiện tại làm đầu mối tìm nguồn, không sao chép kết luận từ tên trích dẫn. Lượt lập dàn bài chưa thực hiện một tổng quan tài liệu mới.

### Chương 3. Cơ sở lý thuyết và mô hình bài toán

**Mục đích:** thống nhất định nghĩa/công thức để Chương 4 mô tả được thuật toán và Chương 5 đánh giá đúng. **Dung lượng:** 10–12 trang.

#### 3.1. Chuỗi dữ liệu và quy ước thời gian

- OHLCV theo phiên quan sát, cutoff `t`, cửa sổ biểu đồ và lịch sử tính factor.
- Ánh xạ sang chỉ số engine: cửa sổ `[e-W,e)`, `t=e-1`, vào lệnh `e`, thoát `e-1+L`; cấu hình nghiên cứu `L=3`.
- Phân biệt ngày lịch và phiên giao dịch, dữ liệu thiếu và warm-up.

#### 3.2. Hợp đồng kinh tế và nhãn dự báo

- LONG: mua `Open(t+1)`, bán `Close(t+3)`; SHORT được ánh xạ thành CASH, không bán khống.
- Với phí `f=0,0025` và slippage `s=0,001` mỗi chiều, giữ đúng công thức của `compute_round_trip_net_return`:

\[
r^{net}_t=\frac{C_{t+3}}{O_{t+1}}
\frac{(1-s)(1-f)}{(1+s)(1+f)}-1.
\]

- Nhãn UP khi `r_net > 0`, DOWN khi `r_net <= 0`; trường hợp bằng 0 phải được quy định rõ.
- Nhãn candidate-LONG khác lợi nhuận tài khoản khi chọn CASH. Khoản chi phí xấp xỉ 0,70% không thay thế công thức nhân hai chiều.
- Hợp đồng này áp dụng cho query và nhãn lịch sử; sai khác của bằng chứng cũ phải được báo như giới hạn provenance, không âm thầm sửa số liệu.

#### 3.3. Tín hiệu kỹ thuật, alpha và sentiment

- Nguyên lý năm chỉ báo của Indicator: MACD, RSI, Stochastic, Williams %R và ROC.
- Alpha, chuẩn hóa, định hướng theo IC và lựa chọn factor; phân biệt quy tắc native với causal-common.
- Sentiment như nguồn ngữ cảnh riêng; điểm số, độ phủ, ngày công bố và quy ước thiếu dữ liệu.
- Vote/confidence của agent không mặc nhiên là xác suất được hiệu chuẩn.

#### 3.4. HMM cho trạng thái thị trường

- Trạng thái ẩn, phân bố quan sát, ma trận chuyển, fit và suy luận trạng thái ở cuối prefix.
- Đặc trưng VN-Index hiện có: log-return, volatility 20 phiên và khoảng cách tới MA20/50/200.
- Gán ý nghĩa trạng thái, chất lượng fit và fallback; scaler/model phải được khóa đúng thời điểm.

#### 3.5. Thống kê Bayes cho ngữ cảnh lịch sử

- Beta–Bernoulli, counts, posterior mean và credible interval.
- Thống kê có điều kiện và shrinkage từ background rời nhau; không đếm lặp cùng cycle.
- Phân biệt cỡ mẫu thống kê với số ví dụ `K` đưa vào prompt.
- Khoảng Beta plug-in mô tả tỷ lệ lịch sử có điều kiện; không tự trở thành khoảng dự báo lợi nhuận query.

#### 3.6. Học trong ngữ cảnh đa tác vụ và utility

- Phân biệt prior tasks, target context đã có nhãn trưởng thành và query chưa biết nhãn.
- Teacher Beta–Bernoulli, student số học, đặc trưng/scaler và context theo bucket.
- `P(y=1)` khác kỳ vọng lợi nhuận; utility cần thông tin về cả xác suất và độ lớn lời/lỗ.
- Fact anchor, đề xuất sửa quyết định và điều kiện chấp nhận theo phân bố chênh lệch utility.

#### 3.7. Point-in-time và nguyên tắc đánh giá

- Giá có ngày `<= t`; tin có thời điểm khả dụng hợp lệ; tin không ngày bị loại. Trình bày thêm quy ước khả dụng bảo thủ của từng protocol.
- Episode được dùng chỉ khi `exit_date < t`; loại các evaluation ID đã dành riêng khỏi context theo protocol đã khóa.
- Purge train/validation/test; phân biệt fit hợp lệ, cutoff bên ngoài và tính nhân quả từng hàng.
- Ghép cặp trên upstream cố định; repeats của Decision không làm tăng số quan sát thị trường độc lập.
- Accuracy, BA, MCC; account return, NAV/drawdown, exposure; định nghĩa mẫu số và NA khi không xác định.

**Hình/bảng dự kiến:** timeline quyết định–vào–thoát; sơ đồ phân vùng thời gian; bảng ký hiệu; minh họa posterior bằng ví dụ tính tay được ghi rõ là minh họa, không phải dữ liệu thực nghiệm.

### Chương 4. Hệ thống đa agent với ngữ cảnh Bayes theo trạng thái thị trường

**Mục đích:** mô tả cách các thành phần được hiện thực và phối hợp. **Dung lượng:** 18–22 trang.

#### 4.1. Kiến trúc tổng thể và hợp đồng dữ liệu

- Các tầng: nguồn dữ liệu → snapshot PIT → báo cáo agent → nhánh phương pháp → Decision/policy → checkpoint → evaluator/giao diện.
- State có kiểu, định danh point/repeat/variant, source hashes và JSON serialization.
- Tách luồng forecast khỏi outcome/label; không đưa dữ liệu đánh giá vào request.

#### 4.2. Hệ đa agent cơ sở

- **4.2.1. Indicator:** tính chỉ báo và tổng hợp vote; mô tả hành vi xác định của backtest.
- **4.2.2. Pattern và Trend:** hai ảnh đầu vào, mô tả mẫu nến và hỗ trợ/kháng cự, kiểm tính nhất quán; không xem kiểm hình học là chứng nhận VLM hiểu ảnh đúng.
- **4.2.3. Alpha và sentiment:** factor registry/selection và ngữ cảnh tin; giải thích vị trí Sentiment trong đường Alpha, tránh đồng nhất số module với số LLM call.
- **4.2.4. Decision:** distill/cap báo cáo, schema đầu ra và ánh xạ dự báo sang hành động.
- **4.2.5. Native và Common:** giữ native làm nguồn so sánh, causal-common thay projection alpha và họ prompt; bridge này thay đổi hơn một yếu tố.

#### 4.3. Bộ nhớ lịch sử và nhận diện regime

- Schema episode: mã, cutoff, ngày vào/thoát, tín hiệu agent, regime, outcome và provenance.
- Sinh nhãn theo engine chung; kiểm dữ liệu, ngày đáo hạn và version của bank.
- HMM/scaler trên VN-Index, regime prefix và cơ chế suy luận đúng thời điểm.
- Phân biệt signal bank của Bayesian với numeric task context của MT-BICL; không mô tả thành một ngân hàng đồng nhất nếu nguồn khác nhau.

#### 4.4. Bayesian Prior v1

- Lọc PIT trước khi đọc outcomes để thống kê/truy xuất; phạm vi cùng mã và thông tin regime/tín hiệu.
- Chọn tối đa `K=3` ví dụ; trình bày metric, tie-break và điều kiện thiếu support theo code/protocol được dùng.
- Sinh Bayesian Regime Prior Prefix (BRPP), chèn trước các báo cáo đã rút gọn.
- Truy vết membership/example IDs; fallback tái dùng Common cùng repeat khi không đủ điều kiện.

#### 4.5. Prior có điều kiện và các biến thể

- **C2 / Bayesian Prior v2:** matching tín hiệu, thống kê Beta có shrinkage, kiểm readiness riêng cho thống kê và ví dụ.
- **A_tp_pool:** nới nhóm thống kê theo Trend/Pattern; phân tích đánh đổi giữa support và mức tương đồng.
- **B_semantic:** diễn đạt counts, intervals và định danh ví dụ rõ hơn trên support tương ứng; không suy từ tên `semantic` rằng có embedding/vector search.
- Bảng so sánh điều kiện lọc, thống kê, ví dụ, prompt và fallback của bốn prior.

#### 4.6. MT-BICL và cơ chế sửa quyết định

- **4.6.1. Fact packet và Fact Anchor:** facts PIT, kiểm assertions, phụ thuộc vào Common và quy tắc khi anchor không hợp lệ.
- **4.6.2. Tạo tác vụ:** bucket theo facts, prior tasks/target observations, vector đặc trưng, scaler và cutoff của từng observation.
- **4.6.3. Teacher và student:** nguồn target huấn luyện, recipe, seed/checkpoint, tách fit khỏi inference; mô tả kiến trúc thực dùng theo module/lock, không suy từ tên thuật toán.
- **4.6.4. Posterior utility:** cách lấy mẫu, gain/loss support, mean/quantiles và các trường hợp không đủ bằng chứng.
- **4.6.5. Projection vào prompt:** summary toàn membership, ví dụ đại diện, prefix và schema phản hồi.
- **4.6.6. Policy ngoài LLM:** giữ anchor nếu không eligible hoặc facts sai; khi đề xuất khác anchor, chỉ đổi nếu `Q10(ΔU)>0` theo policy. Với CASH→LONG dùng `Q10(U)`; LONG→CASH dùng `-Q90(U)`.
- **4.6.7. Truy vết:** lưu riêng raw proposal, anchor action, bypass/veto reason và final action; tách hiệu ứng student khỏi hiệu ứng policy.

#### 4.7. Registry và thực thi ghép cặp

| Vai trò trong nghiên cứu hợp nhất | ID mã nguồn | Phụ thuộc/fallback chính |
| --- | --- | --- |
| Native | `original_fix` | Projection và prompt native. |
| Common | `original_common` | Causal-common alpha và prompt chung. |
| Bayesian prior | `bayesian_v1` | Common; bank + regime. |
| Conditional prior | `C2` | Common; thống kê và readiness có điều kiện. |
| Trend–pattern prior | `A_tp_pool` | Common; nhóm thống kê Trend/Pattern. |
| Explicit-count prior | `B_semantic` | Common; diễn đạt bằng chứng tường minh. |
| Fact anchor | `Fact_Anchor` | Common; facts và assertions. |
| MT-BICL | `MT_BICL` | Common + Fact Anchor; numeric context/student/utility. |

- Một upstream cho mỗi point/realization; deep-copy snapshot tới các nhánh, không gọi lại vision riêng để so đối chứng.
- Thực thi theo thứ tự phụ thuộc trong mỗi repeat; lưu nguồn của việc tái dùng quyết định.
- Registry tám vai trò nghiên cứu khác số lựa chọn hiển thị trên UI và khác số call API thực phát sinh.

#### 4.8. Ngân sách prompt và độ bền vận hành

- Giữ `_distill_report`, `_cap_report`; BRPP không quá 600 ký tự với `K=3`, prompt Decision dưới 6.500 ký tự. Ký tự và token là hai đơn vị khác nhau.
- API qua `_invoke_with_retry` theo đường chạy được audit; exponential backoff, retry-after, schema repair và ghi nhận attempt.
- Checkpoint theo point/stage, resume và xử lý UNKNOWN; lỗi kỹ thuật không được âm thầm biến thành dự báo CASH hợp lệ.
- Đóng băng model/options, nguồn dữ liệu, weights và receipts; replay số liệu lưu khác tái lập một lần hosted inference mới.

#### 4.9. Ứng dụng minh họa và thuật toán tổng hợp

- Flask: phân tích realtime 1D, chọn phiên bản, tiến trình agent, báo cáo BICL và Decision cuối; xem backtest/so sánh/export.
- Presentation VI/EN được tách khỏi kết quả canonical; đổi ngôn ngữ không được làm đổi quyết định.
- Minh họa một luồng end-to-end và giả mã của ba thuật toán: tạo episode/PIT context; chuẩn bị prior/MT và áp policy; chạy paired forecast rồi mới nối labels/evaluate.
- Ảnh giao diện chỉ thêm khi đã chụp/kiểm trên phiên bản xác định; browser acceptance đang chờ ở mốc khảo sát, không ghi là đã nghiệm thu UI hoàn chỉnh.

**Hình/bảng dự kiến:** kiến trúc tổng; DAG tám vai trò; cấu trúc episode; luồng retrieval; student–teacher/context; cây policy; bảng khác biệt biến thể; ba thuật toán và 1–2 màn hình minh họa.

### Chương 5. Thực nghiệm và thảo luận

**Mục đích:** trả lời RQ1–RQ4 bằng bằng chứng có thể truy vết. **Dung lượng:** 20–24 trang.

#### 5.1. Mục tiêu, các nghiên cứu và mức bằng chứng

- Tách nghiên cứu thành phần của hệ gốc với nghiên cứu ngữ cảnh lịch sử trên hệ hợp nhất.
- Công bố mốc freeze, protocol, các kết quả đã tiếp xúc trước khi chốt lịch và giới hạn thăm dò.
- Phân biệt artifact đã nghiệm thu, khả năng hiện thực và thí nghiệm cần bổ sung.

#### 5.2. Dữ liệu và phạm vi đánh giá

- Chín mã FPT, CMG, VCB, MBB, MWG, VNM, BHN, HVN, VJC; OHLCV, VN-Index, sentiment và provenance riêng.
- Sáu block thời gian, 12 ngày được chọn, 102 điểm hợp lệ và 51 tài khoản mã–fold; công bố các loại trừ, warm-up và các cảnh báo dữ liệu.
- Bank prior 852 ví dụ trên bốn mã FPT/MWG/VCB/VNM; nêu phần không có bank và chính sách tương ứng.
- Trong nghiên cứu ngữ cảnh, sentiment thiếu tại 79/102 điểm; missingness là thuộc tính đầu vào, không mặc định là sentiment trung tính đã quan sát.
- Bảng timeline tách train/validation/test, cửa sổ biểu đồ 45 nến và prefix dài phục vụ alpha; không gọi 12 ngày chọn là backtest liên tục nhiều năm.

#### 5.3. Thiết lập tái lập và protocol ghép cặp

- Python, dependencies, model aliases/options và fingerprint theo khóa của **lượt nghiên cứu**, không lấy cấu hình live hôm nay thay cho cấu hình đã chạy.
- Query IDs, source/data/model hashes, ngân sách prompt, thứ tự nhánh, retry/checkpoint và quy tắc reserve evaluation IDs.
- Nghiên cứu ngữ cảnh: một upstream/điểm, ba Decision repeats, tám vai trò; `102 × 3 × 8 = 2.448` forecast slots. Đây không phải 2.448 quan sát thị trường độc lập hoặc 2.448 HTTP calls.
- Dùng receipt để tách active raw responses, bypass và attempts đã nghỉ; không cộng số liệu hai nghiên cứu thành một cohort mới.

#### 5.4. Đối chứng và thiết kế so sánh

- **Nghiên cứu thành phần:** Full/Base và các đối chứng đã lưu như CASH, always-LONG, train-majority, momentum, logistic-price, logistic-matched, factor-vote; mô tả chính xác support của từng bảng.
- **Nghiên cứu ngữ cảnh:** năm phương pháp mở rộng so với Native và so với Common; thêm bridge Common–Native, Fact Anchor–Common, MT–Fact Anchor và hai đối chứng kinh tế.
- Base bỏ alpha và sentiment; Common giữ hai phần này dưới profile khác. Không dùng Base và Common thay thế nhau.
- Always-LONG theo từng chu kỳ khác continuous hold; continuous hold là đối chứng tài khoản riêng.
- Các panel factor/sentiment/placebo và upstream repeats đã có được báo với support riêng, không coi là full ablation MT-BICL.

#### 5.5. Chỉ số và thống kê

- Phân loại: BA, MCC, accuracy, precision/recall hai lớp, confusion matrix và tỷ lệ LONG; giữ mẫu số/NA.
- Kinh tế: mean account return, tổng chi phí, turnover, exposure, NAV và drawdown; phân biệt bình quân tài khoản với một danh mục gộp vốn.
- Nghiên cứu ngữ cảnh: tính return qua repeats trong từng account rồi bình quân accounts; BA tính trên 102 điểm mỗi repeat rồi bình quân.
- Chỉ trình bày Sharpe/Sortino cùng đúng tần suất và mẫu số của từng nghiên cứu; không annualize lịch thưa/không đều bằng công thức không phù hợp.
- Giữ bootstrap theo block/fold và cấu trúc paired; giải thích hai họ contrast, bands đồng thời, leave-one-fold/symbol-out và sensitivity.
- Với sáu fold đã exposed, gọi khoảng hiện có là **band mô tả/sensitivity**, không kết luận ý nghĩa thống kê xác nhận hay power đã bảo đảm.

#### 5.6. Kết quả nghiên cứu thành phần

- Hiệu quả Full/Base và đối chứng số trên tập chính.
- Phân tích theo mã/block, mức exposure và độ lệch giữa accuracy với lợi nhuận.
- Factorial alpha/sentiment/placebo và biến thiên upstream trên các panel nhỏ đã có.
- Thảo luận yếu tố gây nhiễu: thay đổi nội dung/độ dài prompt, định dạng factor và native row-wise causality.
- Trả lời RQ1 trong phạm vi các panel, không suy thành đánh giá đầy đủ mọi thành phần hệ mở rộng.

#### 5.7. Kết quả nghiên cứu ngữ cảnh lịch sử

- Bảng tám vai trò và hai đối chứng kinh tế: BA/return, support, calls mới, fallback và độ phân tán repeats.
- Hai họ chênh lệch: so Native để đánh giá thay đổi hệ thống, so Common để đánh giá phần ngữ cảnh trên nền chung.
- Đối chiếu kết quả theo fold, mã và nhóm có bank như phân tích độ nhạy.
- **Mốc định hướng đọc bằng chứng hiện có, không phải kết quả mới:** mean account return của Native khoảng −0,653%, Common −1,025%, Bayesian v1 −0,698%, MT-BICL −1,253%; cả tám vai trò nghiên cứu có mean return âm. Bayesian v1 tốt hơn Common trong band mô tả đã lưu, chưa chứng minh vượt Native. Khi viết bảng chính, lấy đầy đủ độ chính xác từ artifact và ghi đúng đơn vị.
- Trả lời RQ2 bằng cả kết quả chính và support thực dùng; không quy lợi thế cho riêng regime khi chưa có đối chứng tắt regime thích hợp.

#### 5.8. Phân tích cơ chế, trường hợp điển hình và độ bền

- Readiness riêng của thống kê/ví dụ; số lượng, độ tuổi, regime, similarity và fallback theo nhánh.
- Common → Fact Anchor → MT: phân biệt thay đổi raw proposal, giữ anchor và veto. Bằng chứng hiện có ghi MT trùng final action với anchor ở 302/306 slots.
- C2/B_semantic mỗi nhánh chỉ có ba raw Decision mới, A_tp_pool có 24; lý giải vai trò của fallback trước khi bình luận “phương pháp không khác baseline”.
- Chọn case minh họa theo quy tắc công bố: prior được dùng, thiếu support, agent bất đồng, utility chặn thay đổi và quyết định sai. Không chỉ chọn giao dịch thắng.
- Chi phí/latency/token/attempts và giới hạn trường usage thiếu; robustness chi phí, thanh khoản/khớp lệnh và giả định settlement theo các artifact đã có.
- Tách minh họa UI khỏi kiểm chứng cơ chế tài chính; trả lời RQ3 và phần vận hành của RQ4.

#### 5.9. Ablation chưa thực hiện và giới hạn suy luận

- Ghi rõ các đối chứng retrieval-only, statistics-only, no-prior, no-target, no-utility và tách student/policy là hướng cần bổ sung khi chưa có kết quả trong nghiên cứu hợp nhất.
- Một số module đã hỗ trợ ablation không cấp quyền điền số liệu hoặc kết luận tác động nhân quả của từng thành phần.
- Các hạn chế phải thảo luận: native row-wise causal FAIL; xác thực lịch sử tin/giá còn thiếu; bank/query khác provenance; ngân hàng phủ hẹp; ít block độc lập; dữ liệu lịch sử đã exposed; training contamination của hosted model chưa loại trừ.
- Mẫu mã được chọn có chủ đích, chưa xác minh đầy đủ membership niêm yết/hủy niêm yết; fill/khối lượng/lô/lịch giao dịch và corporate actions có giới hạn.
- Báo cáo audit hiện có về sai khác tính return bank/query ở 828/852 records; không đổi thành số nhãn sai hoặc tự sửa bằng chứng cũ trong bản thảo.
- Kết thúc bằng bảng RQ → kết quả quan sát → điều có thể kết luận → điều còn thiếu.

**Bảng/hình tối thiểu:** dữ liệu/phân vùng; thiết lập và support; kết quả thành phần; kết quả ngữ cảnh; contrast bands; bridge/policy; coverage/fallback; case có truy vết; chi phí và audit. Không tạo equity curve liên tục bằng cách nối các tài khoản độc lập hoặc lấp khoảng không giao dịch sai quy tắc.

### Chương 6. Kết luận và hướng phát triển

**Mục đích:** chốt điều đã làm và điều bằng chứng thực sự cho phép nói. **Dung lượng:** 4–6 trang.

#### 6.1. Tổng kết bài toán và cách tiếp cận

- Tóm tắt kiến trúc đa agent, ngữ cảnh regime/Bayesian, MT-BICL và evaluator thống nhất.
- Nhắc lại ranh giới đóng góp tự phát triển và thành phần kế thừa.

#### 6.2. Trả lời câu hỏi nghiên cứu và đóng góp đạt được

- Trả lời riêng RQ1–RQ4, dẫn về bảng/figure tương ứng ở Chương 5.
- Phân biệt kết quả kỹ thuật tái lập được với kết luận khoa học còn giới hạn.
- Không diễn đạt “đã nâng hiệu quả” như kết luận chung khi kết quả phụ thuộc baseline, support và policy.

#### 6.3. Hạn chế

- Tóm tắt các hạn chế ảnh hưởng trực tiếp tới kết luận: dữ liệu, nhân quả, cỡ mẫu, attribution, LLM và thực thi giao dịch.
- Nêu trạng thái chưa chứng nhận toàn hệ và UI acceptance còn chờ nếu vẫn đúng ở thời điểm hoàn thiện bản thảo.

#### 6.4. Hướng phát triển

- Sửa và kiểm chứng row-wise causality native; đồng nhất nguồn và kiểm provenance nhãn lịch sử.
- Mở rộng/kiểm chứng bank, sentiment và phạm vi mã/ngày; bổ sung nhãn miền tài chính và đối chứng hiểu biểu đồ.
- Chạy ablation tách retrieval, statistics, prior/target tasks, student và utility với protocol đăng ký trước.
- Thiết kế tiền cứu trên dữ liệu chưa tiếp xúc, tính precision/power phù hợp và tái sinh upstream để đo biến thiên toàn hệ.
- Mô phỏng thực thi sát hơn với dữ liệu venue/lô/thanh khoản và cạnh tranh vốn danh mục; hoàn thiện nghiệm thu giao diện.

### Tài liệu tham khảo

- Lập danh mục mới theo các nhóm ở Chương 2 và những phương pháp thực dùng ở Chương 3–5.
- Ưu tiên bài báo gốc, tài liệu chính thức của thư viện/phương pháp và nguồn dữ liệu; kiểm tác giả, năm, DOI/URL trước khi đưa vào bản thảo.
- Dẫn nguồn QuantAgent, Alpha101, HMM, Bayesian/MT-BICL và các phương pháp thống kê đúng phần kế thừa. Code/receipt nội bộ phục vụ provenance, không thay thế nguồn học thuật của thuật toán.
- Các quy định thị trường nếu đưa vào bản chính phải được đối chiếu nguồn phù hợp thời điểm nghiên cứu; không suy luật hiện hành từ một giả định trong backtest.

### Phụ lục đề xuất

| Phụ lục | Nội dung |
| --- | --- |
| A. Đặc tả dữ liệu và thời gian | Schema episode/state, point IDs, bảng ký hiệu, mapping cutoff/entry/exit, dữ liệu thiếu và nhãn kinh tế. |
| B. Prompt và đầu ra | Prompt từng họ phương pháp, BRPP, schema, ví dụ request/response đã bỏ bí mật và bảng ngân sách. |
| C. Thuật toán và cấu hình | Chi tiết factor/chỉ báo, HMM, retrieval, conditional statistics, MT student/teacher, utility và bảng hyperparameter theo lock. |
| D. Bảng kết quả mở rộng | Theo mã/fold/repeat, confusion, sensitivity và support; giữ riêng từng nghiên cứu. |
| E. Kiểm thử và audit | Kiểm PIT, paired, economics, token/retry/checkpoint, phản ví dụ native; phạm vi gate và liên kết receipts. |
| F. Tái lập và ứng dụng | Source/runtime/data/model hashes, lệnh offline, artifact manifest, điều kiện tài nguyên và hướng dẫn UI minh họa. |

## E. Ánh xạ dàn bài sang nguồn hiện có

Đây là chỉ mục phục vụ viết, không phải danh sách tài liệu tham khảo học thuật cuối cùng. Đường dẫn trỏ về mã hiện hành; khi trích kết quả phải dùng đúng source/runtime đã khóa của nghiên cứu tương ứng.

| Phần viết | Nguồn để đối chiếu | Điều cần xác minh khi viết |
| --- | --- | --- |
| Khung trình bày | [main.tex mẫu](../Latex/main.tex), [preamble mẫu](../Latex/preamble.tex), [PDF mẫu](../23020332_Tran_Xuan_Bao.pdf) | Chỉ dùng cấu trúc/hình thức; metadata và nội dung được viết mới. |
| Định hướng, phạm vi | [plan hiện hành](../docs/plan/plan.md), [README tích hợp](../docs/plan/week12/README.md) | Tách trạng thái hiện tại với receipt lịch sử và phần còn chờ. |
| Agent cơ sở | [graph_setup](../utils/graph_setup.py), [state](../agents/agent_state.py), [Indicator](../agents/indicator_agent.py), [Pattern](../agents/pattern_agent.py), [Trend](../agents/trend_agent.py), [Alpha](../agents/alpha_agent.py), [Sentiment](../agents/sentiment_agent.py), [Decision](../agents/decision_agent.py) | Đúng profile live/backtest, vai trò xác định/LLM và prompt thực dùng. |
| Kinh tế và nhãn | [backtest engine](../core/backtest_engine.py), [target contract](../utils/target_contract.py), [MT accounting](../core/mt_bicl_accounting.py) | Một công thức return chuẩn; indices, costs, ledger và frequency. |
| Regime, bank, retrieval | [regime detector](../core/regime_detector.py), [Bayesian memory](../core/bayesian_memory.py), [retriever](../core/bayesian_retriever.py), [historical outcomes](../core/historical_outcomes.py) | Cutoff của fit/query/episode, schema và provenance. |
| Prior có điều kiện | [conditional statistics](../core/prior_conditional_statistics.py), [example selection](../core/prior_example_selection.py), [quality gate](../core/prior_quality_gate.py), [improvement prior](../core/improvement_prior.py) | P/C/background, readiness riêng, fallback và khác biệt A/B. |
| MT-BICL | [tasks](../core/mt_bicl_tasks.py), [teacher](../core/mt_bicl_teacher.py), [student](../core/mt_bicl_student.py), [replica student](../core/mt_bicl_replica_student.py), [context](../core/mt_bicl_context.py), [utility](../core/mt_bicl_utility.py), [policy](../core/mt_bicl_policy.py) | Bản student/checkpoint thực chạy, target context và điều kiện đổi action. |
| Registry, bridge, paired | [registry](../core/variant_registry.py), [causal bridge](../core/causal_bridge.py), [method adapters](../core/unified_methods.py), [protocol](../core/unified_protocol.py) | Native khác Common; snapshot chung và phụ thuộc từng repeat. |
| Thiết kế, kết quả thành phần | [experimental setup](../paper/content/experimental_setup.tex), [bảng thành phần](../paper/content/tables/component/), [results](../paper/content/results.tex) | Phân biệt main/upstream/factorial panels và protocol riêng. |
| Kết quả ngữ cảnh hợp nhất | [bảng ngữ cảnh](../paper/content/tables/historical_context/), [receipt phân tích](../docs/plan/week12/unified_analysis_acceptance.json), [gói kết quả](../docs/plan/week12/unified_analysis_results.zip), [consumer](../core/unified_analysis/analysis.py) | Đơn vị sample/account/repeat, contrasts, fallback và bands mô tả. |
| Phạm vi, phục hồi bằng chứng | [evidence map](../docs/plan/week12/final_evidence_map.md), [nguồn bảng bài báo](../core/manuscript_u09/sources.py), [limitations hiện có](../paper/content/limitations.tex) | Mỗi số liệu có nguồn; không dùng cây live thay source frozen. |
| Giao diện | [web entrypoint](../web_interface.py), [serving contract](../docs/plan/week12/variant_serving_contract.md), [live service](../core/serving_live/service.py), [research viewer](../utils/research_view.py) | UI realtime 1D và kết quả lưu; chỉ tuyên bố nghiệm thu đúng trạng thái. |
| Các hợp đồng cần viện dẫn | [paired tests](../tests/test_paired_protocol.py), [retrieval leakage](../tests/test_bayesian_retriever_leakage.py), [regime leakage](../tests/test_regime_leakage.py), [prompt budget](../tests/test_backtest_token_budget.py), [MT tasks leakage](../tests/test_mt_bicl_tasks_leakage.py) | Sự hiện diện của test không thay kết quả thực thi trên một source/runtime cụ thể. |

## F. Trình tự phát triển thành bản thảo

1. Chốt tên đề tài/ngôn ngữ bản nộp và metadata bìa; duyệt RQ1–RQ4, phạm vi sáu chương.
2. Viết Chương 3–4 trước để khóa ký hiệu, hợp đồng, kiến trúc và tên phương pháp; kiểm từng mô tả với code/profile thực dùng.
3. Dựng Chương 5 từ bảng/receipt đã khóa, có chỉ mục provenance; ghi phần chưa thực hiện đúng trạng thái, không chạy thêm thí nghiệm chỉ để lấp dàn bài.
4. Viết Chương 2 từ nguồn học thuật đã đọc/kiểm; hoàn thiện Chương 1 theo đóng góp thực có.
5. Viết Chương 6 và Abstract sau cùng; đối soát mọi kết luận với RQ và bảng bằng chứng.
6. Chuyển nội dung đã duyệt sang cây LaTeX riêng trong `theses/`, dùng phần trình bày cần thiết từ mẫu; kiểm mục lục, tham chiếu, công thức, bảng/hình và PDF sau khi biên dịch.

Không đưa mã task, checklist theo tuần hoặc lịch sử sửa lỗi vào thân khóa luận. Chúng chỉ làm đầu mối truy vết trong giai đoạn viết; tiến độ dự án tiếp tục quản lý tại `docs/plan/`.
