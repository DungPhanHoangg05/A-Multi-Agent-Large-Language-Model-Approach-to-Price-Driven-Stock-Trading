"""Giải thích MT-BICL từ dữ kiện, thống kê và quy tắc đã ghi trong lượt chạy."""

def explanation(aux: dict, policy: dict) -> dict[str, dict[str, str]]:
    """Dựng hai ngôn ngữ từ preparation và policy đã xác thực trong journal."""
    packet, wire = aux['packet'], policy['wire']
    values, facts = packet['numeric'], packet['assertions']
    utility = (aux.get('branch') or {}).get('utility') or {}
    output = {}

    for lang in ('vi', 'en'):
        english = lang == 'en'

        def number(value: float, spec: str = '.6g') -> str:
            text = format(value, spec)
            return text if english else text.replace('.', ',')

        def action(value: str) -> str:
            if value == 'LONG':
                return 'LONG'
            return 'SHORT (hold cash)' if english else 'SHORT (giữ tiền mặt)'

        final = action(wire['final_action'])
        declared = action(wire['raw_proposed_action']) if wire['raw_proposed_action'] is not None else ''
        anchor = action(wire['anchor_action'])
        reason = wire['reason']
        delta = wire['q10_delta_U_net_fraction']
        if reason == 'KEEP_PROPOSED_SAME':
            rationale = (f'MT-BICL also proposed {final}, so the Fact Anchor decision was kept. The Q10 threshold applies to changes.'
                         if english else f'MT-BICL cũng đề xuất {final}, nên giữ quyết định của Fact Anchor. Ngưỡng Q10 áp dụng khi đổi hành động.')
        elif reason in ('ACCEPT_POSITIVE_Q10_DELTA_U', 'REJECT_NONPOSITIVE_Q10_DELTA_U'):
            threshold = number(delta * 100, '+.6g') + '%'
            if reason == 'ACCEPT_POSITIVE_Q10_DELTA_U':
                rationale = (f'Changed from {anchor} to {final} because Q10 of the net utility difference was {threshold} (> 0).'
                             if english else f'Đổi từ {anchor} sang {final} vì Q10 của chênh lệch lợi ích ròng là {threshold} (> 0).')
            else:
                rationale = (f'Kept {final} from Fact Anchor. The proposal to switch to {declared} had Q10 of the net utility difference at {threshold} (≤ 0).'
                             if english else f'Giữ {final} từ Fact Anchor. Đề xuất đổi sang {declared} có Q10 của chênh lệch lợi ích ròng là {threshold} (≤ 0).')
        elif reason == 'REJECT_FACT_ASSERTIONS':
            rationale = (f'Kept {final} from Fact Anchor because the proposed revision did not match the verified facts.'
                         if english else f'Giữ {final} từ Fact Anchor vì đề xuất sửa không khớp dữ kiện đã xác minh.')
        elif reason == 'ANCHOR_INVALID_USE_ORIGINAL':
            rationale = (f'Used {final} from the common baseline because Fact Anchor did not match the verified facts.'
                         if english else f'Dùng {final} từ baseline chung vì Fact Anchor không khớp dữ kiện đã xác minh.')
        else:
            rationale = (f'Kept {final} from Fact Anchor because the run lacked eligible context for a revision.'
                         if english else f'Giữ {final} từ Fact Anchor vì lượt chạy thiếu ngữ cảnh đủ điều kiện để sửa quyết định.')

        relation = {'ABOVE': 'above', 'BELOW': 'below', 'EQUAL': 'equal to'} if english else {
            'ABOVE': 'cao hơn', 'BELOW': 'thấp hơn', 'EQUAL': 'bằng'}
        sign = {'POSITIVE': 'positive', 'NEGATIVE': 'negative', 'ZERO': 'zero'} if english else {
            'POSITIVE': 'dương', 'NEGATIVE': 'âm', 'ZERO': 'bằng 0'}
        verified = []
        if facts['MACD_ZERO'] != 'UNKNOWN':
            marked = f"MACD {number(values['macd'])} ({sign[facts['MACD_ZERO']]})"
            if facts['MACD_SIGNAL'] != 'UNKNOWN':
                marked += f" {relation[facts['MACD_SIGNAL']]} Signal {number(values['signal'])}"
            verified.append(marked + '.')
        if facts['PRICE_SMA20'] != 'UNKNOWN':
            close = 'Close' if english else 'Giá đóng cửa'
            verified.append(f"{close} {number(values['close'])} {relation[facts['PRICE_SMA20']]} SMA20 {number(values['sma20'])}.")
        verified_text = ' '.join(verified) or ('No verified values for these indicators.' if english else 'Chưa có số liệu đã xác minh cho các chỉ báo này.')

        history = 'No eligible historical utility estimate.' if english else 'Chưa có ước tính lợi ích lịch sử đủ điều kiện.'
        if utility.get('status') == 'SUPPORTED':
            gain, loss = utility['gain_count'], utility['loss_count']
            mean = number(utility['mean_U_net_fraction'] * 100, '+.4f') + '%'
            q10 = number(utility['q10_U_net_fraction'] * 100, '+.4f') + '%'
            history = (f'Retrieved history recorded {gain} gains and {loss} losses. Estimated net utility of LONG averaged {mean}, with Q10 of {q10}.'
                       if english else f'Ngữ cảnh lịch sử ghi nhận {gain} trường hợp lãi và {loss} trường hợp lỗ. Lợi ích ròng ước tính của LONG có trung bình {mean}, Q10 là {q10}.')
        output[lang] = {'justification': rationale, 'evidence_for': verified_text, 'evidence_against': history}

    return output
