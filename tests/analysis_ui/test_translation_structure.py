"""Hồi quy đúng report HTTP200 bỏ bốn dòng; không nới guard số hoặc gọi forecast."""
import json
from pathlib import Path
import unittest

from core.display_translation import TranslationError, validate_translation


class TranslationStructure(unittest.TestCase):
    def test_truncated_translation_is_rejected(self) -> None:
        fixture=json.loads((Path(__file__).parent/'locale_regression.json').read_bytes())
        with self.assertRaises(TranslationError): validate_translation(fixture['source'],fixture['truncated_translation'],'en')
        validate_translation(fixture['source'], fixture['expected_translation'], 'en')
