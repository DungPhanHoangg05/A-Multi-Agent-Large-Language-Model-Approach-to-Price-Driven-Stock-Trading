# Nguồn bài báo

Bài báo so sánh **Our system với QuantAgent** để kiểm tra tác dụng
của alpha OHLCV và sentiment tin tiếng Việt. **BICL v1–v5** là
nghiên cứu mở rộng. Lần đánh giá bổ sung có bảng riêng vì nguồn, dự báo và
mẫu số khác lần đánh giá lịch sử. [Tên hệ thống và ID](../README.md#methods-and-profiles)

Mở `main.tex` bằng pdfLaTeX; `main_submit.tex` là bản có dòng và trang phục vụ nộp bài.
Khi đưa lên Overleaf, tải toàn bộ nội dung thư mục này và chọn đúng main document.
Tệp lớp, kiểu bibliography và dữ liệu tài liệu tham khảo đã nằm trong thư mục.

```text
paper/
  main.tex, main_submit.tex   Điểm vào biên dịch
  layout.tex                 Thiết lập bố cục dùng chung
  references.bib             Tài liệu tham khảo
  content/                   Các phần nội dung và phụ lục
    tables/component/        Bảng nghiên cứu thành phần
    tables/historical_context/ Bảng nghiên cứu ngữ cảnh lịch sử
  figures/                   Hình và sơ đồ được bài báo sử dụng
```

Biên dịch tại thư mục này:

```powershell
pdflatex -halt-on-error main.tex
bibtex main
pdflatex -halt-on-error main.tex
pdflatex -halt-on-error main.tex
```

Đổi `main` thành `main_submit` để biên dịch bản nộp.
PDF hiện hành gồm [bản đầy đủ](../outputs/paper/main-fin15.pdf) và
[bản nộp](../outputs/paper/main-submit-fin15.pdf). Nguồn tự đủ để biên dịch.
[PDF và manifest của bản trước](../outputs/paper/README.md) giữ vai trò bằng chứng lịch sử.

## Nguồn và tái lập

Nguồn PDF ngày **21/11/2026** được khóa tại commit
`314757d6b89bd06167abb6503fc2c7357fc14f3c`.
[Hash SHA-256 và số trang của PDF bàn giao](../scripts/thesis_docs/source-map.json).

| Nghiên cứu | Profile và nguồn bảng |
| --- | --- |
| Thành phần | Main compact `AS` và `B`, với logistic-price và CASH cùng 102 điểm. [Bảng baseline đã khóa](../outputs/revision/final_baselines_v1/main_comparison.csv). |
| BICL lịch sử | Our system dùng alpha native, Common dùng alpha causal và khóa truy xuất dùng nhóm tín hiệu đã ghi. [Bảng và hình lịch sử](../outputs/revision/u09_manuscript_assets_v1/artifacts/). |
| BICL follow-up | `FIN11_RESEARCH_V1`, profile `finalize_serving_v1` với alpha causal dùng chung và khóa truy xuất `ohlcv_retrieval_keys_v1`. [Bản chiếu từ receipt FIN12](../docs/plan/week12/manuscript_evidence.json). |

Từ gốc checkout, tái tạo bảng chính, bảng follow-up và dữ liệu hình khóa
luận, rồi biên dịch PDF bằng các lệnh phía trên:

```powershell
py -3.13 -X utf8 scripts/project_finalize_manuscript_tables.py
py -3.13 -X utf8 scripts/project_finalize_manuscript_tables.py --check
```

Để đối chiếu trực tiếp prompt thực gửi, kết quả lịch sử của FPT và từng
dự báo follow-up, chạy thêm
`py -3.13 -X utf8 scripts/project_finalize_manuscript_tables.py --audit --check`.
Chế độ này cần các phần ZIP `local-*` của kho nghiên cứu được cấp quyền,
`outputs/unified_integration/u09_analysis_r1/` và
`outputs/finalize/fin12_v1/` cùng receipt. [Tra và khôi phục kho bằng chứng](../docs/plan/revision_evidence/README.md).
