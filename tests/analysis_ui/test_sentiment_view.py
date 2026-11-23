"""Đọc đúng tin snapshot/PIT cho UI, không dựng neutral hoặc counts giả khi thiếu metadata."""
from copy import deepcopy
import unittest

from core.historical_evaluation_data import FrozenNews
from utils.analysis_sentiment_view import sentiment_view


class SentimentView(unittest.TestCase):
    def rows(self) -> list[dict]:
        return [{'date_parsed':'2026-11-10','numeric_score':value,'scorer':'lexicon','label':label,'title':'Tin '+label}
                for value,label in ((.8,'positive'),(.6,'positive'),(-.2,'negative'))]

    def test_recorded_weighted_score_preserved_distribution_and_backend_are_actual(self) -> None:
        articles=self.rows(); source,_=FrozenNews({'FPT':articles}).get_sentiment_at('FPT','2026-11-13')
        original=deepcopy(source); view=sentiment_view(source,articles,'FPT','2026-11-13')
        self.assertEqual(source,original); self.assertEqual(view['main_sentiment']['avg_score'],source['main_sentiment']['avg_score'])
        self.assertEqual(view['main_sentiment']['label'],'positive')
        self.assertEqual(view['main_sentiment']['positive'],2); self.assertEqual(view['main_sentiment']['negative'],1)
        self.assertEqual(view['model_used'],'lexicon'); self.assertFalse(view['relative_available'])

    def test_future_undated_stale_and_not_yet_available_news_never_enter_display(self) -> None:
        articles=self.rows()+[{'date_parsed':None},
            {'date_parsed':'2026-01-01'},{'date_parsed':'2026-11-13'}]
        source,_=FrozenNews({'FPT':articles}).get_sentiment_at('FPT','2026-11-13')
        view=sentiment_view(source,articles,'FPT','2026-11-13')
        self.assertEqual(len(view['scored_articles']),3)
        self.assertTrue(all(row['date_parsed']=='2026-11-10' for row in view['scored_articles']))
        with self.assertRaises(ValueError): sentiment_view(source,articles+[{'date_parsed':'2026-11-14'}],'FPT','2026-11-13')

    def test_missing_labels_not_zero_counts_or_fake_neutral_and_mismatched_snapshot_fails(self) -> None:
        articles=self.rows()
        for row in articles: row.pop('label')
        source,_=FrozenNews({'FPT':articles}).get_sentiment_at('FPT','2026-11-13')
        view=sentiment_view(source,articles,'FPT','2026-11-13')
        self.assertFalse(view['distribution_available']); self.assertNotIn('positive',view['main_sentiment'])
        source['main_sentiment']['avg_score']=.99
        with self.assertRaises(ValueError): sentiment_view(source,articles,'FPT','2026-11-13')
        self.assertEqual(sentiment_view({},None,'FPT','2026-11-13'),{})
