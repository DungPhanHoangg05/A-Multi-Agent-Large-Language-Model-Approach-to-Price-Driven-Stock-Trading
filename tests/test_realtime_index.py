"""Tái hiện lỗi VNINDEX thật: Open ngoài Low/High không thuộc hợp đồng lịch/Close của HMM."""
from unittest.mock import patch
import unittest

import pandas as pd

from core.realtime_index import clean_index,fetch_index_history,index_document,index_frame
from core.realtime_loader import _clean_realtime_frame


class RealtimeIndexTests(unittest.TestCase):
    def raw(self) -> pd.DataFrame:
        """Bốn dòng lỗi OHLC công khai từ VCI ngày13/11/2026; giữ nguyên giá nguồn."""
        return pd.DataFrame({'time':['2019-06-24','2019-06-25','2019-06-26','2021-08-23'],
            'open':[949.48,949.48,949.48,1329.43],'high':[967.11,963.23,962.70,1326.07],
            'low':[962.63,960.06,958.49,1298.86],'close':[962.85,960.13,959.13,1298.86],
            'volume':[113476250,120760130,119422620,761345100]})

    def test_original_incident_rows_pass_close_contract_without_repairing_prices(self) -> None:
        raw = self.raw(); saved = raw.copy(deep=True)
        with self.assertRaises(ValueError): _clean_realtime_frame(raw,'FPT')
        actual = clean_index(raw)
        self.assertEqual(actual.columns.tolist(),['Datetime','Close'])
        self.assertEqual(actual.Close.tolist(),raw.close.tolist())
        pd.testing.assert_frame_equal(raw,saved)
        self.assertEqual(index_document(actual)['Close'],raw.close.tolist())
        pd.testing.assert_frame_equal(index_frame(index_document(actual)),actual)

    def test_index_fallback_checks_close_and_never_uses_bad_close_as_valid(self) -> None:
        raw = self.raw(); bad = raw.copy(); bad.loc[0,'close'] = float('nan')
        with patch('core.realtime_loader._fetch_from_vnstock',side_effect=[bad,raw]) as fetch:
            actual,error = fetch_index_history('1d',lookback_days=3600,tail=3000)
        self.assertFalse(error); self.assertEqual(len(actual),4)
        self.assertEqual([call.args[-1] for call in fetch.call_args_list],['VCI','KBS'])
        with patch('core.realtime_loader._fetch_from_vnstock',return_value=bad):
            actual,error = fetch_index_history()
        self.assertTrue(actual.empty); self.assertTrue(error)

    def test_missing_duplicate_negative_infinite_or_intraday_daily_dates_raise(self) -> None:
        raw = self.raw()
        for value in (float('nan'),float('inf'),0.,-1.):
            changed = raw.copy(); changed.loc[0,'close'] = value
            with self.assertRaises(ValueError): clean_index(changed)
        changed = raw.copy(); changed.loc[0,'time'] = '2019-06-24 09:00:00'
        with self.assertRaises(ValueError): clean_index(changed)
        self.assertEqual(len(clean_index(changed,daily=False)),4)
        changed = raw.copy(); changed.loc[1,'time'] = changed.loc[0,'time']
        with self.assertRaises(ValueError): clean_index(changed)
        with self.assertRaises(ValueError): clean_index(raw.drop(columns='close'))
