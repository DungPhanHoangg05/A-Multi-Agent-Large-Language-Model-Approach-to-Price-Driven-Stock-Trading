"""Ngôn ngữ/cookie/theme nhất quán trên mọi trang; bản dịch không chạy qua GET."""
from html.parser import HTMLParser
import importlib
from urllib.parse import urlsplit,parse_qs
import unittest
from unittest.mock import patch


class Links(HTMLParser):
    def __init__(self,raw: str) -> None:
        super().__init__(); self.links=[]; self.feed(raw)
    def handle_starttag(self,tag: str,attrs: list) -> None:
        value=dict(attrs)
        if tag=='a' and value.get('lang') in ('vi','en'): self.links.append(value['href'])


class Preferences(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]): cls.web=importlib.import_module('web_interface')

    def test_all_pages_share_language_theme_controls_and_keep_query_identity(self) -> None:
        client=self.web.app.test_client()
        urls=['/demo','/output','/backtest','/backtest?source=legacy','/experiments?kind=paper_evidence',
              '/output?serving_run=12345678-1234-4234-8234-123456789abc&serving_source=live']
        for language in ('vi','en'):
            for url in urls:
                query=url+('&' if '?' in url else '?')+'lang='+language
                response=client.get(query); self.assertEqual(response.status_code,200)
                raw=response.get_data(as_text=True)
                self.assertIn('id="theme-toggle"',raw); self.assertIn('css/site_theme.css',raw)
                self.assertIn('js/site_preferences.js',raw); self.assertIn('<html lang="'+language+'"',raw)
                self.assertIn('qa_lang='+language,';'.join(response.headers.getlist('Set-Cookie')))
                original=parse_qs(urlsplit(url).query)
                for link in Links(raw).links:
                    values=parse_qs(urlsplit(link).query)
                    for key,value in original.items(): self.assertEqual(values[key],value)
        self.assertIn('<html lang="en"',client.get('/demo').get_data(as_text=True))
        raw=client.get('/demo?lang=en').get_data(as_text=True)
        self.assertNotIn('id="analysis-source"',raw)

    def test_native_report_language_is_bound_and_not_inferred_from_later_cookie(self) -> None:
        analyzer=object.__new__(self.web.WebTradingAnalyzer)
        value=analyzer.extract_analysis_results({'success':True,'asset_name':'FPT','timeframe':'1d','data_length':45,
            'final_state':{'final_trade_decision':'{"decision":"SHORT"}'}},'en')
        self.assertEqual(value['report_language'],'en')

    def test_saved_native_vietnamese_timeframe_is_localized_only_for_display(self) -> None:
        results={'timeframe':'1 Ngày','asset_name':'FPT','final_decision':{'decision':'SHORT','confidence':'Cao'},
            'report_language':'vi','technical_indicators':'Giá trị 1.23'}
        with self.web.app.test_request_context('/output?lang=en'):
            from flask import render_template
            raw=render_template('analysis/legacy_output.html',results=results,T=self.web.catalogue('en'),LANG='en',
                A=importlib.import_module('utils.analysis_ui').messages('en'))
        self.assertIn('1 Day',raw); self.assertNotIn('1 Ngày',raw)
        self.assertIn('High',raw); self.assertIn('data-source-language="vi"',raw)
        self.assertEqual(results['timeframe'],'1 Ngày'); self.assertEqual(results['final_decision']['confidence'],'Cao')

    def test_serving_report_loads_one_versioned_locale_module_without_hidden_pending_content(self) -> None:
        results={'serving_analysis':True,'asset_name':'FPT','final_decision':{'decision':'SHORT'},
            'report_language':'vi','alpha_analysis':'Alpha source','pattern_analysis':'Pattern source','trend_analysis':'Trend source'}
        with self.web.app.test_request_context('/output?lang=en'):
            from flask import render_template
            raw=render_template('analysis/legacy_output.html',results=results,T=self.web.catalogue('en'),LANG='en',
                A=importlib.import_module('utils.analysis_ui').messages('en'))
        self.assertEqual(raw.count('js/display_locale.js?v=reports-v3'),1)
        self.assertNotIn('js/analysis/daily_output.js',raw)
        self.assertIn('css/site_theme.css?v=reports-v3',raw)
        from pathlib import Path
        css=(Path(__file__).resolve().parents[2]/'static/css/site_theme.css').read_text(encoding='utf-8')
        self.assertNotIn('visibility:hidden',css)
