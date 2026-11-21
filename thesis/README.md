# Khóa luận tốt nghiệp

Để đưa lên Overleaf, nén **nội dung của thư mục này** sao cho `main.tex`
nằm ngay ở gốc ZIP, cùng cấp với `references.bib`, `latex/` và `assets/`.
Chọn `main.tex` làm **Main document** và chọn **pdfLaTeX** hoặc **XeLaTeX**.
Bibliography dùng Biber. `covers-preview.tex` là điểm vào riêng để xem hai bìa.

[Hướng dẫn biên dịch cục bộ](../docs/plan/thesis/build.md) ·
[Kế hoạch khóa luận](../docs/plan/thesis/plan.md) ·
[PDF hiện hành](../outputs/thesis/thesis-fin15.pdf)

## Nguồn và tái lập

Nguồn bàn giao tại commit `6bc661987ea80ce6c7fe44c2e094016f4a45afb9`.
Nghiên cứu chính dùng profile `finalize_serving_v1` của lần chạy
`FIN11_RESEARCH_V1` và kết quả follow-up đã đối soát với receipt FIN12.
[Bản chiếu có hash nguồn](../docs/plan/week12/manuscript_evidence.json) ·
[Hash SHA-256 của PDF bàn giao](../scripts/thesis_docs/source-map.json).

Chạy từ gốc checkout:

```powershell
py -3.13 -X utf8 scripts/project_finalize_manuscript_tables.py
py -3.13 -X utf8 scripts/project_finalize_manuscript_tables.py --check
py -3.13 -X utf8 scripts/thesis_docs/build.py --engine pdflatex
```

Dùng `--engine xelatex` cho bản dựng XeLaTeX. Checkout có đủ nguồn
LaTeX, bảng và hình để build. Chế độ `--audit --check` cần kho prompt
và dự báo cục bộ. [Profile từng nghiên cứu và các nguồn cần khôi phục](../paper/README.md#nguồn-và-tái-lập).

## Trang cam đoan

Trang *Declaration* trình bày tên **Phan Hoang Dung** dưới mục *Student*.
Nội dung nằm trong [nguồn phần đầu khóa luận](latex/frontmatter/content.tex).
