"""Hồi quy đúng report HTTP200 bỏ bốn dòng; không nới guard số hoặc gọi forecast."""
import json
from pathlib import Path
import unittest

from core.display_translation import ReportPlan,TranslationError,validate_translation,MARKER,NUMBERS


class TranslationStructure(unittest.TestCase):
    def test_real_truncation_is_rejected_and_every_numbered_rule_has_required_segment(self) -> None:
        fixture=json.loads((Path(__file__).parent/'locale_regression.json').read_bytes())
        with self.assertRaises(TranslationError): validate_translation(fixture['source'],fixture['truncated_translation'],'en')
        plan=ReportPlan(fixture['source'])
        rules=[(key,segment) for key,segment in plan.segments.items() if any(word in segment.source for word in ('Sử dụng ĐÚNG','KHÔNG tự đếm','KHÔNG dùng số liệu','Mỗi section'))]
        self.assertEqual(len(rules),4)
        # Tất cả đoạn là thuộc tính bắt buộc; số thứ tự nằm ở skeleton do server giữ.
        translated={key:'Translated rule '+' '.join(MARKER.findall(segment.masked)) for key,segment in plan.segments.items()}
        value=plan.render(translated,'en')
        for number in range(1,5): self.assertIn('\n'+str(number)+'. Translated rule',value)
        self.assertEqual(NUMBERS.findall(fixture['source']),NUMBERS.findall(value))
        translated.pop(rules[-1][0])
        with self.assertRaises(TranslationError): plan.render(translated,'en')

    def test_code_formula_numeric_data_and_markdown_skeleton_are_immutable(self) -> None:
        source='## Giá trị\n\n| Giá trị | WQ57_VwapArgmax |\n|---|---|\n| **-2.8411** | `rank(C,5)` |\n\n1. Giá trị +0.55% SHORT\n```python\nrank(C,5)\n```\n'
        plan=ReportPlan(source)
        translated={key:segment.masked.replace('Giá trị','Value') for key,segment in plan.segments.items()}
        value=plan.render(translated,'en')
        self.assertEqual(value,source.replace('Giá trị','Value'))
        for key,segment in plan.segments.items():
            if MARKER.search(segment.masked):
                broken={**translated,key:MARKER.sub('',translated[key],count=1)}
                with self.assertRaises(TranslationError): plan.render(broken,'en')
                break

    def test_long_lines_split_between_words_and_preserve_whitespace(self) -> None:
        source=('VeryLongWord '*300)+'\n  \n'
        plan=ReportPlan(source)
        self.assertEqual(plan.render({key:value.masked for key,value in plan.segments.items()},'en'),source)
        self.assertTrue(all('VeryLongWord' in value.masked for value in plan.segments.values()))
