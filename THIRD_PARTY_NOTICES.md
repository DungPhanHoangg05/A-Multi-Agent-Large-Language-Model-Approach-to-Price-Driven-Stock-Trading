# Nguồn phần mềm và thông báo của bên thứ ba

## QuantAgent

Hệ thống được đánh giá trong bài báo kế thừa các agent Indicator, Pattern, Trend và Decision, quy trình điều phối LangGraph và công cụ phân tích biểu đồ từ QuantAgent của Y-Research @SBU. [Kho mã upstream hiện mang tên QuantHarness](https://github.com/Y-Research-SBU/QuantHarness) · [Bài báo QuantAgent, arXiv:2509.09995v3](https://arxiv.org/abs/2509.09995v3)

**Copyright (c) 2025 Y-Research @SBU.** Mã có nguồn gốc từ QuantAgent được phân phối theo MIT License. Khi phân phối bản sao hoặc phần đáng kể của mã đó, cần giữ thông báo bản quyền và thông báo cấp phép. Tệp giấy phép trong kho lưu nguyên văn cả hai thông báo và điều khoản miễn trừ bảo hành. [Bản MIT trong kho](LICENSES/QuantAgent-MIT.txt) · [Bản MIT upstream](https://github.com/Y-Research-SBU/QuantHarness/blob/92519f806286192345e940e7ab77496462d662b7/LICENSE)

Hồ sơ đối chiếu ghi nguồn theo tệp và hàm, gồm các agent, mã điều phối và công cụ biểu đồ. [Hồ sơ đối chiếu QuantAgent](https://github.com/DungPhanHoangg05/A-Multi-Agent-Large-Language-Model-Approach-to-Price-Driven-Stock-Trading-in-the-Vietnamese-Stock-Ma/blob/0b19e9fc4b285be63bc452068ec6ab261206744d/docs/plan/revision_evidence/README.md#quantagent_attribution_v1)

## Tệp bên thứ ba phục vụ bài báo

| Tệp | Nguồn và điều khoản |
| --- | --- |
| [paper/elsarticle.cls](paper/elsarticle.cls) | Elsevier Ltd, © 2007–2020. Bản 3.3 ghi LaTeX Project Public License (LPPL) 1.2 hoặc mới hơn trong đầu tệp. [Gói Elsarticle](https://ctan.org/pkg/elsarticle) |
| [paper/elsarticle-num.bst](paper/elsarticle-num.bst) | Elsevier Ltd, © 2007–2024. Bản 2.1 ghi LPPL 1.3 hoặc mới hơn trong đầu tệp. [Gói Elsarticle](https://ctan.org/pkg/elsarticle) |
| [alpha101_1601.00991v3.pdf](evidence/alpha101_1601.00991v3.pdf) | Bản tham chiếu *101 Formulaic Alphas* của Zura Kakushadze, cũng là nguồn cho các công thức alpha được điều chỉnh trong dự án. Bản arXiv v3 ghi giấy phép phân phối không độc quyền cấp cho arXiv. Quyền phân phối lại PDF trong kho này chưa được ghi nhận. [Bài báo](https://arxiv.org/abs/1601.00991v3) · [Điều khoản arXiv](https://arxiv.org/licenses/nonexclusive-distrib/1.0/) |

## Mô hình và dữ liệu dùng trong đánh giá

- Bộ chấm sentiment sử dụng `5CD-AI/Vietnamese-Sentiment-visobert` cho tin tiếng Việt. Model card và danh sách tệp tại revision dùng trong nghiên cứu chưa công bố giấy phép riêng cho trọng số của bản đó. [Model card dùng trong nghiên cứu](https://huggingface.co/5CD-AI/Vietnamese-Sentiment-visobert/blob/d7738b85200272f10ba8b048d80236c8c582b581/README.md)
- Dữ liệu thị trường, tin CafeF và mô hình dùng qua dịch vụ bên ngoài tuân theo điều khoản của từng nguồn. [Nguồn dữ liệu và bằng chứng đánh giá](evidence/README.md)
