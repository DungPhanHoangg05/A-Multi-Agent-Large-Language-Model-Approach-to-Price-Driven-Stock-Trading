"""Nhãn backtest/compare VI-EN, không đổi ngôn ngữ hoặc metric của nguồn."""
from __future__ import annotations


def messages(language: str) -> dict[str,str]:
    """Tái dùng nhãn phân tích, thêm ý nghĩa account/filter/legacy rõ ràng."""
    from utils.analysis_ui import messages as common
    result = common(language)
    labels = {
        'title':('Backtest nhiều phiên bản','Multi-version backtest'),
        'new_backtest':('Backtest mới · exploratory','New backtest · exploratory'),
        'paper_evidence':('Bằng chứng bài báo','Paper evidence'),
        'legacy_backtest':('Full / No-Alpha cũ','Legacy Full / No-Alpha'),
        'legacy_full':('Full · legacy','Full · legacy'),'legacy_no_alpha':('Base No-Alpha · legacy','Base No-Alpha · legacy'),
        'legacy_scope':('Số liệu nguồn cũ chưa được chứng nhận lại; No-Alpha không phải baseline common. Không ghép với run mới.','Recorded legacy values are not recertified; No-Alpha is not common. Do not pair with a new run.'),
        'symbols':('Mã trong cùng cửa sổ','Symbols in the same window'),
        'start_date':('Từ ngày query','First query date'),'end_date':('Đến ngày query','Last query date'),
        'run':('Chạy backtest','Run backtest'),'settings':('Cấu hình backtest','Backtest settings'),
        'domain_note':('1d/VI, tối đa 30 point/job; lấy mỗi ba phiên, không chồng vòng vốn. Không dùng dữ liệu mới nhất.','Daily/VI, up to 30 points/job, every third session with non-overlapping cycles. Latest data is unavailable.'),
        'select_methods':('Chọn ít nhất một phiên bản','Select at least one version'),
        'models':('Model/options đã mở','Released models/options'),
        'key_settings':('Cấu hình API key tại trang phân tích','Configure the API key on the analysis page'),
        'results':('Kết quả backtest','Backtest results'),'filters':('Bộ lọc cùng support','Common support filters'),
        'all':('Tất cả','All'),'apply':('Áp dụng','Apply'),'baseline':('Mốc so sánh','Comparison baseline'),
        'none':('Không có / chưa chạy baseline','None / baseline not executed'),
        'filter_note':('Filter tính lại metric trên cùng subset của job; không giữ band U09 cho run/subset mới.','Filters recompute metrics on a common subset of this job; U09 intervals are not reused.'),
        'accounts_note':('Mỗi mã/repeat là tài khoản độc lập 50 triệu VND; số trung bình không phải portfolio. Daily NAV và return chu kỳ tách riêng.','Each symbol/repeat is an independent VND 50 million account. The average is not a portfolio. Daily NAV and cycle returns are separate.'),
        'summary':('Metrics theo phiên bản','Metrics by version'),'method':('Phiên bản','Version'),
        'returns':('Return tài khoản (%)','Account return (%)'),'accuracy':('Accuracy (%)','Accuracy (%)'),
        'balanced_accuracy':('BA (%)','BA (%)'),'mcc':('MCC','MCC'),'f1':('Macro F1','Macro F1'),
        'long_rate':('LONG (%)','LONG (%)'),'daily_mdd':('Daily MDD (%)','Daily MDD (%)'),
        'cycle_mdd':('Cycle-end MDD (%)','Cycle-end MDD (%)'),'fee':('Phí (VND)','Fees (VND)'),
        'slippage':('Trượt giá (VND)','Slippage (VND)'),'turnover':('Turnover (VND)','Turnover (VND)'),
        'fallback':('Fallback / bypass','Fallback / bypass'),'coverage':('Coverage','Coverage'),
        'no_metrics':('Chưa đủ common support/outcome để tính summary hoặc đường NAV; không xếp hạng partial.','Common support/outcomes are incomplete. Summary and NAV are withheld; partial results are not ranked.'),
        'empty_support':('Subset không có point.','The subset contains no points.'),
        'contrasts':('Chênh lệch ghép cặp cùng job','Paired differences within this job'),
        'contrast_note':('Point estimate cùng support, không có CI/p-value mới; native/common khác profile có chủ đích.','Point estimates on common support, without new CIs or p-values. Native/common intentionally use different profiles.'),
        'delta_return':('Chênh return (điểm %)','Return difference (pp)'),
        'delta_ba':('Chênh BA (điểm %)','BA difference (pp)'),
        'daily_nav':('Daily NAV theo tài khoản (VND)','Daily NAV by account (VND)'),
        'chart_account':('Tài khoản biểu đồ','Chart account'),'cycle_returns':('Return chu kỳ theo point (%)','Cycle returns by point (%)'),
        'predictions':('Quyết định và outcome từng point','Decisions and outcomes by point'),
        'outcome':('Nhãn kinh tế','Economic label'),'cycle_return':('Return chu kỳ (%)','Cycle return (%)'),
        'export':('Xuất cùng bộ lọc','Export current filters'),'json':('JSON và provenance','JSON and provenance'),
        'csv_summary':('CSV summary','CSV summary'),'csv_predictions':('CSV quyết định','CSV decisions'),
        'csv_daily':('CSV daily NAV','CSV daily NAV'),'csv_cycles':('CSV chu kỳ','CSV cycles'),
        'csv_accounts':('CSV tài khoản','CSV accounts'),'csv_contrasts':('CSV chênh lệch','CSV differences'),
        'catalog':('Xem trong trang thực nghiệm','View in experiments'),
        'saved':('Kết quả Full/Base đã lưu','Saved Full/Base results'),
    }
    index = int(language == 'en'); result.update({key:pair[index] for key,pair in labels.items()})
    return result
