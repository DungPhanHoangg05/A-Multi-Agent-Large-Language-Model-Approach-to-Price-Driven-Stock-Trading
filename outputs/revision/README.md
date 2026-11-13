# Bằng chứng đang được sử dụng

Thư mục này chỉ giữ hai bộ dữ liệu còn có consumer hiện hành:

| Thư mục | Mục đích |
| --- | --- |
| `u09_manuscript_assets_v1/` | `core/research_results.py` đọc `artifacts/support.json` đã khóa hash để hiển thị kết quả nghiên cứu. Giữ nguyên release đầy đủ và manifest. |
| `final_baselines_v1/` | `core/free_pilot_analysis.py` đọc `main_comparison.csv` làm đối chứng lịch sử. Giữ nguyên dữ liệu và manifest. |

Tệp `r1_source_inventory.json` là chỉ mục kiểm kê nguồn được các script baseline
lịch sử tham chiếu, được giữ nguyên để đối soát; đây không phải kết quả bài báo mới.

Nguồn bài báo ở [paper/](../../paper/README.md), PDF hiện hành ở
[outputs/paper/](../paper/README.md). Các release cũ đã chuyển vào
[kho bằng chứng có chỉ mục](../../docs/plan/revision_evidence/README.md).
Chỉ khôi phục release lịch sử khi cần chạy đúng audit cũ; không cần khôi phục
để biên dịch bài báo hoặc mở màn hình kết quả nghiên cứu.
