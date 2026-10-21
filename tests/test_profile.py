import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1]/'scripts/generate_profile.py'
SPEC = importlib.util.spec_from_file_location('generate_profile', SCRIPT)
profile = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(profile)


class ContributionTests(unittest.TestCase):
    def test_pairs_dates_and_tooltips_independently_of_html_order(self):
        parser = profile.CalendarParser()
        parser.feed('''<td id="b" data-date="2026-10-20" data-level="4"></td>
            <td data-level="0" data-date="2026-10-19" id="a"></td>
            <td data-level="1" data-date="2026-10-21" id="c"></td>
            <tool-tip for="a">No contributions on October 19th.</tool-tip>
            <tool-tip for="b">1,234 contributions on October 20th.</tool-tip>
            <tool-tip for="c">1 contribution on October 21st.</tool-tip>''')
        days = parser.days()
        profile.validate_days(days)
        self.assertEqual([d['count'] for d in days], [0, 1234, 1])
        self.assertEqual(profile.metrics(days), (1235, 2, 2))

    def test_missing_count_is_an_error_instead_of_zero(self):
        parser = profile.CalendarParser()
        parser.feed('<td id="a" data-date="2026-10-21" data-level="2"></td>')
        with self.assertRaises(ValueError):
            parser.days()

    def test_rejects_empty_gapped_duplicate_or_inconsistent_data(self):
        a = {'date': '2026-10-19', 'level': 0, 'count': 0}
        for days in [[], [a, a], [a, dict(a, date='2026-10-21')],
                     [dict(a, count=1)], [dict(a, count=-1)]]:
            with self.subTest(days=days), self.assertRaises(ValueError):
                profile.validate_days(days)

    def test_streak_stops_at_zero_and_counts_days_not_contributions(self):
        days = [{'count': n} for n in [2, 4, 0, 1, 2, 3, 0, 8]]
        self.assertEqual(profile.metrics(days), (20, 6, 3))

    def test_user_text_is_escaped_and_every_theme_is_valid_svg(self):
        data = {'name': 'Shyam & <friends>', 'username': 'ishyamprasath', 'projects': []}
        snapshot = {'username': 'ishyamprasath', 'updated': '2026-10-21',
                    'days': [{'date': '2026-10-21', 'count': 1, 'level': 1}]}
        for colors in profile.THEMES.values():
            for svg in [profile.hero(data, colors), profile.hero(data, colors, mobile=True),
                        profile.projects(data, colors), profile.toolkit(data, colors), profile.activity(snapshot, colors)]:
                root = ET.fromstring(svg)
                self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
                self.assertNotIn('<script', svg)
                self.assertNotIn('<foreignObject', svg)
        self.assertIn('Shyam &amp; &lt;friends&gt;', profile.hero(data, profile.THEMES['dark']))


if __name__ == '__main__':
    unittest.main()
