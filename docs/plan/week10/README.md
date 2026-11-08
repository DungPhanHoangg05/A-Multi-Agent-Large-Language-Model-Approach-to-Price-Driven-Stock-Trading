# MT-BICL — Thành phần phương pháp hiện hành

[Kế hoạch tổng](../plan.md) · [Tiến độ](../week11/README.md) ·
[Kế hoạch đánh giá](../week11/historical_reevaluation_plan.md)

MT-BICL là một phương pháp gồm student/teacher, context có điều kiện,
facts, posterior utility và policy sửa quyết định nền.

## Các thành phần được giữ

| Module | Trách nhiệm |
| --- | --- |
| core/mt_bicl_bank, scaler, stream, regimes, tasks | Giá, labels engine, feature/scaler và membership PIT |
| core/mt_bicl_inputs, teacher, reference | Input D/C/x, Beta–Bernoulli hierarchy và oracle độc lập |
| core/mt_bicl_student, distillation, adapter | Student causal và frozen-weight inference |
| core/mt_bicl_features, contracts, context | Facts/bucket, schema, context và projection |
| core/mt_bicl_prompt, decision, policy, utility | Prompt gốc/anchored, API wrapper, utility và veto |
| core/mt_bicl_accounting, reporting, analysis | Accounts, decomposition và metrics |

Model package pin candidate tensor và teacher pi bằng byte hash.
Adapter kiểm hash, schema và tensor fingerprint; query outcome bị từ chối.
Asset thiếu/sai dừng trước prediction, không có teacher fallback.

Utility dùng4096 draws và common random streams đã giữ ổn định.
Chỉ context đủ support mới sinh proposal. Fact_Anchor resolve a0 từ
Original/facts; final policy giữ riêng raw proposal, facts guard và utility veto.
No_target bỏ C rồi recompute p và utility theo membership mới.

## Cấu hình và vận hành

Cấu hình dữ liệu/phương pháp tại
[mt_bicl_protocol.json](../week11/mt_bicl_protocol.json),
[schema](../week11/mt_bicl.schema.json),
[model manifest](../week11/mt_bicl_model.json).
Namespace runtime là `outputs/bayesian_benchmark/mt_bicl/`.

```powershell
py -3.13 -X utf8 scripts/verify_mt_bicl_protocol.py
py -3.13 -X utf8 scripts/prepare_historical_assets.py
py -3.13 -X utf8 scripts/prepare_historical_assets.py --verify
```

Protocol hiện SPEC_ONLY. H03–H06 phải hoàn tất adapter/release cho lưới
đánh giá mới trước API. Model gốc không tìm thấy; chỉ đạo mới08/11 dùng
[quy trình replica đầy đủ](../week11/historical_reevaluation_plan.md#h02--chuẩn-bị-dữ-liệu-và-model):
ba seed17/42/73,5.000 step/seed, đủ60 checkpoint rồi mới chọn model.
Người dùng đã chạy đủ ba seed; selection chọn seed42/step3000 và test
`MODEL_GATE_PASS`; cold replay đủ60 checkpoint `CPU_REPLAY_MATCH`, H02 hoàn tất
với [manifest replica](../week11/mt_bicl_replica_full_r1_model.json). Manifest
gốc vẫn giữ như bằng chứng lịch sử. VNINDEX2026 đã có snapshot bổ sung;
H03–H06 vẫn cần bind gói model mới và release lượt đánh giá chung.

## Kết quả đã lưu

Development60 điểm ghi MT-BICL NOT_NOMINATED, D so Original−5,313090 đpt,
accuracy45% so Original65%, mean ΔMDD+5,774045 đpt.
Kết quả lịch sử này không thay cho đánh giá lại trên lưới mới.
