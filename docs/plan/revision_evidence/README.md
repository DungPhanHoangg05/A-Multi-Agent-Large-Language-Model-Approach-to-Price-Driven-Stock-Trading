# Kho bằng chứng revision lịch sử

74 thư mục không còn được ứng dụng hay bản thảo hiện hành đọc đã được đưa
khỏi `outputs/revision/`. Kho này giữ nguyên byte bằng chứng đã đóng băng;
không phải gói nguồn bài báo. Nguồn hiện hành ở [paper/](../../../paper/README.md),
PDF ở [outputs/paper/](../../../outputs/paper/README.md).

`index.json` ánh xạ đường dẫn gốc tới SHA-256, kích thước và các mảnh dữ liệu
được khử trùng lặp. `part-*.zip` chứa dữ liệu được theo dõi bằng Git;
`local-*.zip` giữ các asset cục bộ vốn đã được ignore, tiếp tục không đưa lên Git.
Các gói ZIP nguồn/PDF cũ, raw, manifest và receipt bên trong đều giữ nguyên byte.
Không có ZIP bài báo hiện hành được tạo mới.

Bản staging trong `tmp/artifact_cleanup/retired_revision/` đã được xóa sau khi
kiểm SHA-256 từng tệp với kho. Có thể khôi phục bằng CLI dưới đây.

## Cách tra và khôi phục

Chạy từ gốc repo:

```powershell
py -3.13 -X utf8 scripts/revision_evidence.py list
py -3.13 -X utf8 scripts/revision_evidence.py verify author_metadata_v1
py -3.13 -X utf8 scripts/revision_evidence.py restore author_metadata_v1 --destination tmp/revision-restore
```

Lệnh cuối dựng lại `tmp/revision-restore/outputs/revision/author_metadata_v1/`.
Bỏ `--destination` chỉ khi cần khôi phục đúng đường dẫn gốc cho audit lịch sử.
CLI kiểm hash phần lưu trữ, từng mảnh và toàn tệp; từ chối ghi đè tệp khác byte.
Không tự giải nén khi khởi động ứng dụng hoặc chạy test.

Một audit cũ có thể cần nhiều release cha: tra đường dẫn trong manifest/runbook,
khôi phục các release đó và dùng đúng snapshot code/runtime mà receipt đã khóa.
Việc đổi cấu trúc thư mục không cấp lại chứng nhận gate cho source mới.
Lệnh `verify` không chỉ định tên kiểm toàn kho và cần cả các phần `local-*`;
checkout Git mới chỉ có phần tracked. CLI sẽ báo lỗi nếu thiếu phần cần đọc.
Snapshot Markdown trước khi cập nhật liên kết nằm dưới khóa `snapshots/` trong
chỉ mục; các đường dẫn bên trong bằng chứng cũ được giữ nguyên để tái lập.

## Chỉ mục thư mục đã lưu trữ

Các liên kết tới release cũ dẫn đến dòng tương ứng dưới đây. Dùng tên ở cột
đầu với CLI để kiểm hoặc khôi phục đúng thư mục.

| Release lịch sử | Mục đích | Số tệp | MiB gốc |
| --- | --- | ---: | ---: |
| <a id="account_annualisation_v1"></a>`account_annualisation_v1` | Đối soát tài khoản, chi phí và khớp lệnh | 7 | 0.30 |
| <a id="alpha_contract_v1"></a>`alpha_contract_v1` | Kiểm định nhân tố, chỉ báo và đối chứng định lượng | 5 | 0.06 |
| <a id="alpha_registry_v1"></a>`alpha_registry_v1` | Kiểm định nhân tố, chỉ báo và đối chứng định lượng | 3 | 0.36 |
| <a id="alpha_selection_v1"></a>`alpha_selection_v1` | Kiểm định nhân tố, chỉ báo và đối chứng định lượng | 5 | 12.52 |
| <a id="author_metadata_v1"></a>`author_metadata_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 3 | 6.31 |
| <a id="author_preserved_v1"></a>`author_preserved_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 34 | 29.52 |
| <a id="chart_convention_v1"></a>`chart_convention_v1` | Quy ước biểu đồ và thực nghiệm biểu đồ lịch sử | 11 | 0.53 |
| <a id="chart_manuscript_v1"></a>`chart_manuscript_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 16.91 |
| <a id="chart_r1_run_v1"></a>`chart_r1_run_v1` | Quy ước biểu đồ và thực nghiệm biểu đồ lịch sử | 2122 | 58.86 |
| <a id="chart_r4_bank_v1"></a>`chart_r4_bank_v1` | Quy ước biểu đồ và thực nghiệm biểu đồ lịch sử | 1 | 0.53 |
| <a id="chart_r4_run_v1"></a>`chart_r4_run_v1` | Quy ước biểu đồ và thực nghiệm biểu đồ lịch sử | 35 | 0.11 |
| <a id="chart_resume_audit_v1"></a>`chart_resume_audit_v1` | Quy ước biểu đồ và thực nghiệm biểu đồ lịch sử | 5 | 0.94 |
| <a id="clean_replay_v1"></a>`clean_replay_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 7 | 13.12 |
| <a id="dependent_statistics_v1"></a>`dependent_statistics_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 14 | 0.14 |
| <a id="execution_evidence_v1"></a>`execution_evidence_v1` | Đối soát tài khoản, chi phí và khớp lệnh | 5 | 0.12 |
| <a id="execution_final_v1"></a>`execution_final_v1` | Đối soát tài khoản, chi phí và khớp lệnh | 8 | 4.26 |
| <a id="execution_sensitivity_v1"></a>`execution_sensitivity_v1` | Đối soát tài khoản, chi phí và khớp lệnh | 8 | 4.03 |
| <a id="final_contracts_v1"></a>`final_contracts_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 7 | 3.98 |
| <a id="final_cost_integrity_v1"></a>`final_cost_integrity_v1` | Đối soát tài khoản, chi phí và khớp lệnh | 14 | 1.64 |
| <a id="final_pdf_v1"></a>`final_pdf_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 31 | 24.87 |
| <a id="final_regression_v1"></a>`final_regression_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 6 | 1.00 |
| <a id="final_repeats_v1"></a>`final_repeats_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 19 | 0.73 |
| <a id="final_temporal_v1"></a>`final_temporal_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 20 | 0.68 |
| <a id="fusion_prompt_audit_v1"></a>`fusion_prompt_audit_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 2 | 1.08 |
| <a id="indicator_alpha_manuscript_v1"></a>`indicator_alpha_manuscript_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 16.40 |
| <a id="indicator_alpha_rules_v1"></a>`indicator_alpha_rules_v1` | Kiểm định nhân tố, chỉ báo và đối chứng định lượng | 4 | 0.02 |
| <a id="legacy_lineage_v1"></a>`legacy_lineage_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 11 | 3.98 |
| <a id="manuscript_blueprint_v1"></a>`manuscript_blueprint_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 5 | 0.17 |
| <a id="manuscript_content_v1"></a>`manuscript_content_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 4 | 8.00 |
| <a id="manuscript_figures_v1"></a>`manuscript_figures_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 4 | 8.17 |
| <a id="manuscript_layout_references_v1"></a>`manuscript_layout_references_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 8.23 |
| <a id="manuscript_rewrite_v1"></a>`manuscript_rewrite_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 26 | 14.33 |
| <a id="manuscript_standalone_v1"></a>`manuscript_standalone_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 8.10 |
| <a id="manuscript_unified_final_v1"></a>`manuscript_unified_final_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 11 | 9.03 |
| <a id="numeric_controls_design_v1"></a>`numeric_controls_design_v1` | Kiểm định nhân tố, chỉ báo và đối chứng định lượng | 3 | 0.40 |
| <a id="numeric_controls_v1"></a>`numeric_controls_v1` | Kiểm định nhân tố, chỉ báo và đối chứng định lượng | 80 | 11.32 |
| <a id="quantagent_attribution_v1"></a>`quantagent_attribution_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 5 | 1.26 |
| <a id="r1_72h_bank_v2"></a>`r1_72h_bank_v2` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 3277 | 109.75 |
| <a id="r1_72h_run_v2"></a>`r1_72h_run_v2` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 3354 | 68.50 |
| <a id="r1_common_bank_v1"></a>`r1_common_bank_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 3042 | 121.50 |
| <a id="r1_common_bank_v2"></a>`r1_common_bank_v2` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 3043 | 121.50 |
| <a id="r1_common_bank_v3"></a>`r1_common_bank_v3` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 3042 | 121.10 |
| <a id="r1_common_numeric_v2"></a>`r1_common_numeric_v2` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 222 | 5.65 |
| <a id="r1_common_numeric_v3"></a>`r1_common_numeric_v3` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 222 | 5.65 |
| <a id="r1_common_run_v1"></a>`r1_common_run_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 7 | 0.18 |
| <a id="r1_common_run_v2"></a>`r1_common_run_v2` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 185 | 7.15 |
| <a id="r1_common_run_v3"></a>`r1_common_run_v3` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 6 | 0.08 |
| <a id="r1_legacy"></a>`r1_legacy` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 5 | 0.17 |
| <a id="r1_manuscript_v1"></a>`r1_manuscript_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 5 | 12.69 |
| <a id="r1_manuscript_v2"></a>`r1_manuscript_v2` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 9 | 25.18 |
| <a id="r1_numeric_v1"></a>`r1_numeric_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 88 | 1.14 |
| <a id="r1_prices_v1"></a>`r1_prices_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 10 | 0.60 |
| <a id="r2_manuscript_v1"></a>`r2_manuscript_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 19.01 |
| <a id="r2_panel_v1"></a>`r2_panel_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 16 | 0.33 |
| <a id="r3_manuscript_v1"></a>`r3_manuscript_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 19.07 |
| <a id="r3_repeats_v1"></a>`r3_repeats_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 17 | 1.36 |
| <a id="r4_audit_v1"></a>`r4_audit_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 10 | 0.48 |
| <a id="r4_final_v1"></a>`r4_final_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 12 | 0.33 |
| <a id="r4_manuscript_v1"></a>`r4_manuscript_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 19.13 |
| <a id="r4_manuscript_v2"></a>`r4_manuscript_v2` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 19.16 |
| <a id="r4_value_bank_v1"></a>`r4_value_bank_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 1 | 0.60 |
| <a id="r4_value_run_v1"></a>`r4_value_run_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 1099 | 4.06 |
| <a id="reference_audit_v1"></a>`reference_audit_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 9 | 0.23 |
| <a id="reproducibility_v1"></a>`reproducibility_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 10 | 435.35 |
| <a id="reviewer_crosswalk_v1"></a>`reviewer_crosswalk_v1` | Phản hồi và đối chiếu reviewer lịch sử | 9 | 0.35 |
| <a id="reviewer_response_v1"></a>`reviewer_response_v1` | Phản hồi và đối chiếu reviewer lịch sử | 10 | 110.85 |
| <a id="revision_minimal_final_v1"></a>`revision_minimal_final_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 19 | 3.74 |
| <a id="revision_minimal_v1"></a>`revision_minimal_v1` | Dữ liệu, lần chạy và phân tích thực nghiệm lịch sử | 762 | 6.00 |
| <a id="sentiment_contract_v1"></a>`sentiment_contract_v1` | Kiểm kê, độ phủ và hợp đồng dữ liệu tin tức | 4 | 0.77 |
| <a id="sentiment_coverage_v1"></a>`sentiment_coverage_v1` | Kiểm kê, độ phủ và hợp đồng dữ liệu tin tức | 3 | 0.89 |
| <a id="sentiment_inventory_v1"></a>`sentiment_inventory_v1` | Kiểm kê, độ phủ và hợp đồng dữ liệu tin tức | 3 | 0.34 |
| <a id="structure_preserved_v1"></a>`structure_preserved_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 33 | 28.45 |
| <a id="target_contract_v1"></a>`target_contract_v1` | Audit, provenance hoặc kiểm tra tái lập lịch sử | 8 | 0.44 |
| <a id="target_manuscript_v1"></a>`target_manuscript_v1` | Bản thảo, hình/bảng hoặc kiểm tra tài liệu tham khảo cũ | 6 | 19.12 |
