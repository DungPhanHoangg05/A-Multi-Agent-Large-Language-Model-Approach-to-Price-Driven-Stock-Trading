# Kế hoạch nghiên cứu và triển khai KLTN

Đề tài Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent
LLM Stock Trading in the Vietnamese Stock Market.

## Trạng thái hiện hành08/11/2026

Hệ thống giữ Original và bốn nhóm cải tiến.

| Phiên bản | Vai trò |
| --- | --- |
| Bayesian Prior v1 | Regime retrieval và historical examples |
| Bayesian Prior v2, đại diện C2 | Conditional statistics và readiness |
| Bayesian Prior cải tiến A/B | A_tp_pool và B_semantic |
| MT-BICL | Bucket context, student/teacher, facts, utility và revision policy |

[Kế hoạch đánh giá lại](week11/historical_reevaluation_plan.md) dùng dữ
liệu donor fix, primary6 nhánh, CORE4 gồm480 unit và lưới mở rộng1.020 unit/
120 ngày. Fact_Anchor là dependency MT-BICL. H03 đã chốt H=2.358,
budget nominal34.806 calls với3 Decision repeats, chưa gồm retry/smoke/unknown.

[Checklist W11](week11/README.md#checklist-đánh-giá-lại) quản lý H01–H09.
H01 hoàn tất; H02 đã bổ sung VNINDEX tới30/09/2026, audit raw/quyền9 mã,
bank train731 cycle/48 task và CLI replica. Theo chỉ đạo mới08/11,
train `MT_BICL_replica_full_r1` theo [checklist H02](week11/historical_reevaluation_plan.md#h02--chuẩn-bị-dữ-liệu-và-model):
đủ ba seed17/42/73 ×5.000 step, đánh giá60 checkpoint, chọn bằng dữ liệu2021,
test sau selection seal; giữ oracle/cold replay và hash riêng. Train-only
không cần chờ VNINDEX2026. Người dùng đã hoàn tất fit/pilot/train, chọn
seed42/step3000; test `MODEL_GATE_PASS`, cold replay60 checkpoint
`CPU_REPLAY_MATCH`. H02 hoàn tất, gói [model replica](week11/mt_bicl_replica_full_r1_model.json)
đã được neo Git. H03 đã khóa [protocol đánh giá](week11/historical_evaluation_protocol.json),
lịch/schema và dự toán offline. H04 đã hoàn tất adapter9 mã, runner paired,
checkpoint/run/resume/verify và kiểm triển khai offline. Tiếp theo H05;
H05–H09 chưa hoàn tất, quota trực tiếp và smoke thuộc H06. Cần người dùng
chạy `scripts/run_historical_evaluation.py prepare-regimes` để chuẩn bị492
HMM prefix lịch sử bằng CPU trước thu thập; không train lại teacher/student.
Đã sửa guard fit/load prefix sau2022 tại adapter riêng; hiện có51/492 prefix
được kiểm hash, chạy lại cùng lệnh để tiếp tục441 prefix còn thiếu.
Chưa release lưới mới; execution data vẫn có giới hạn vendor series.

## Những phần đã triển khai

- Hệ gốc Indicator/Alpha/Sentiment/Pattern/Trend/Decision cùng backtest.
- Memory Bank và Bayesian Prior có historical signals, provenance, PIT,
  retrieval, feature index, split readiness và BRPP.
- C2, A_tp_pool, B_semantic, các content-mode ablation và retrieval controls.
- MT-BICL có teacher Beta–Bernoulli, student causal, task/scaler/regime,
  bucket context, fact packet, posterior utility4096 draws và policy veto.
- Readiness donor archive, grid, label bridge và kiểm input trước inference.

## Hợp đồng nghiên cứu

LONG vào Open(t+1), ra Close(t+3); SHORT giữ CASH. Phí0,25% và slippage0,10%
cả hai chiều. Nhãn lịch sử dùng compute_round_trip_net_return.
Nến query≤t, tin available≤t và mọi observation phải exit<t.
Upstream một lần/unit/realization, deep-copy tới mọi nhánh.
BRPP≤600 ký tự với K=3, prompt<6.500, API qua retry/checkpoint đã audit.

Model/recipe/prompt/options và IDs được khóa trước inference. Không chọn
winner theo subgroup thuận lợi, không vote/best repeat hoặc đổi model/key
ngầm. Kết quả historical đã exposed mang scope exploratory.
Xác nhận forward có protocol/power/release riêng.

## Tài liệu theo giai đoạn

- [W1](week1/README.md), [W2](week2/README.md), [W3](week3/README.md),
  [W4](week4/README.md), [W5](week5/README.md) quản lý dữ liệu và Bayesian Prior.
- [W6](week6/README.md), [W7](week7/README.md), [W8](week8/README.md),
  [W9](week9/README.md) quản lý cải tiến, development và holdout.
- [W10](week10/README.md) mô tả MT-BICL hiện hành.
- [W11](week11/README.md) quản lý tiến độ áp dụng lại trên dữ liệu chung.
- [W12](week12/README.md) quản lý điều kiện xác nhận và bàn giao.

Mỗi task thực hiện trên nhánh riêng từ develop, kiểm theo phạm vi,
Conventional Commit và hợp nhất sau khi các kiểm tra áp dụng PASS.
