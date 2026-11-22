# Đối chiếu bài báo và khóa luận FIN15

Từ gốc checkout có Python 3.13.5 và môi trường của dự án, chạy hai lệnh sau. Các bước dùng dữ liệu đi kèm và chạy ngoại tuyến.

```powershell
py -3.13 -X utf8 scripts/project_finalize_manuscript_tables.py --audit --check
py -3.13 -X utf8 scripts/thesis_docs/check.py --strict-cutover-targets --strict-current-targets
```

| Nội dung cần đối chiếu | Bằng chứng và phép kiểm |
| --- | --- |
| Our system so với QuantAgent | [Gói nghiên cứu thành phần](component_audit.zip) chứa 102 prompt compact đã gửi, bảng kiểm prompt, dự báo và kết quả phụ thuộc thời gian. Lệnh audit kiểm mẫu ghép cặp, trạng thái sentiment và ma trận phân loại với [bảng baseline](../outputs/revision/final_baselines_v1/main_comparison.csv). |
| Các biến thể BICL lịch sử | [Kết quả U09](unified_analysis_results.zip) chứa dự báo, tài khoản và thống kê. [Bảng bổ trợ](../outputs/revision/u09_manuscript_assets_v1/artifacts/) ghi nguồn từng ô. Chạy `py -3.13 scripts/thesis_docs/figures.py` để vẽ lại hai hình trong khóa luận. |
| BICL follow-up | [Gói FIN12](fin12_audit.zip) chứa receipt và bốn tệp kết quả được audit đọc. Lệnh trên kiểm hash, lưới dự báo, nhãn, lệnh trong sổ tài khoản và số fallback, rồi đối chiếu [bản chiếu FIN15](manuscript_evidence.json) với bảng LaTeX của cả hai bản thảo. |
| PDF bàn giao | [Source map](../scripts/thesis_docs/source-map.json) ghi SHA-256, số trang và commit nguồn ở mục `fin15_outputs`. [Hướng dẫn bài báo](../paper/README.md) và [hướng dẫn khóa luận](../docs/thesis_build.md) có lệnh biên dịch. |

Để kiểm hash của ba PDF trong PowerShell, chạy từ gốc checkout.

```powershell
$fin15 = (Get-Content -Raw scripts/thesis_docs/source-map.json | ConvertFrom-Json).fin15_outputs
foreach ($pdf in @($fin15.pdf, $fin15.paper_pdfs.paper, $fin15.paper_pdfs.paper_submit)) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $pdf.path).Hash -ne $pdf.sha256) { throw $pdf.path }
}
```

## Chạy hệ thống và tái lập lịch sử

Ứng dụng web cài [gói tài nguyên phục vụ phân tích](../resources/serving_inputs.zip) khi khởi động. Với CLI hoặc test trực tiếp, dùng `py -3.13 scripts/install_study_resources.py`. Các manifest lịch sử đã khóa cả tên đường dẫn. Bộ cài kiểm SHA-256 và đặt đúng các đầu vào máy đọc vào `docs/plan/` và `outputs/unified_integration/`. Git bỏ qua các bản cài này. Để kiểm xuất xứ từng tệp ở commit trước khi dọn, đối chiếu 26 đầu vào trong `docs/plan/` theo đường dẫn cùng tên và 75 đầu vào U06 với các thành viên của `docs/plan/week12/unified_comparison_assets_v2.zip`.

Khi cần tái chạy công cụ thu thập, nghiệm thu hoặc dựng lại release U09 với toàn bộ journal và snapshot tại thời điểm nghiên cứu, mở một worktree từ bản Git có đầy đủ lịch sử. Chọn commit của bản thảo hoặc commit chụp repo ngay trước khi tách kế hoạch.

```powershell
git worktree add --detach ../fin15-source 6bc661987ea80ce6c7fe44c2e094016f4a45afb9
git worktree add --detach ../fin15-before-cleanup a034c8bb39f77fb47c9387937c590b762e7711f6
```

Các lượt thu có gọi nhà cung cấp còn phụ thuộc thông tin xác thực và journal gốc của tác giả. Gói FIN12 phân phối các đầu ra dẫn xuất mà người đọc cần để kiểm số liệu. Kết quả và giới hạn khoa học được ghi trong [paper](../outputs/paper/main-fin15.pdf) và [khóa luận](../outputs/thesis/thesis-fin15.pdf).
