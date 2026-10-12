"""Validate the delivered five-day/two-person scenario against its constraints."""
from datetime import date, timedelta
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ChengduScenarioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenario = json.loads((ROOT / 'examples/chengdu-5days.json').read_text())
        cls.markdown = (ROOT / 'examples/chengdu-5days-zh.md').read_text()

    def test_dates_party_size_and_only_one_intense_day(self):
        data = self.scenario
        self.assertEqual(data['party_size'], 2)
        days = data['activities']
        self.assertEqual(len(days), 5)
        expected = [(date(2026, 10, 19) + timedelta(days=i)).isoformat() for i in range(5)]
        self.assertEqual([a['date'] for a in days], expected)
        self.assertEqual(data['weather_dates'], expected)
        self.assertEqual(sum(a['intense'] for a in days), 1)
        for day in days:
            self.assertIn(day['date'], self.markdown)
            if '成都博物馆' in day['venues']:
                self.assertNotEqual(date.fromisoformat(day['date']).weekday(), data['museum_closed_weekday'])

    def test_budget_arithmetic_and_five_day_meal_allowance(self):
        data = self.scenario
        subtotal = sum(item['amount'] for item in data['costs'])
        self.assertEqual(subtotal, data['subtotal'])
        self.assertEqual(round(subtotal * data['contingency_rate'], 2), data['contingency'])
        self.assertEqual(subtotal + data['contingency'], data['total'])
        self.assertEqual(data['total'] / data['party_size'], data['per_person'])
        self.assertEqual(data['budget'] - data['total'], data['headroom'])
        self.assertLessEqual(data['total'], data['budget'])
        meals = data['meals']
        self.assertEqual(len(meals), 15)
        for day in range(1, 6):
            self.assertEqual({m['meal'] for m in meals if m['day'] == day}, {'早餐', '午餐', '晚餐'})
        # Explicitly budget 30 CNY per person in addition to meal estimates for snacks/water.
        meal_total = (sum(m['per_person_estimate'] for m in meals) + 30) * data['party_size']
        food = next(c['amount'] for c in data['costs'] if c['name'].startswith('餐饮'))
        self.assertEqual(meal_total, food)
        self.assertIn('CNY4279', self.markdown)
        self.assertIn('CNY3916', self.markdown)

    def test_unbooked_and_estimated_information_is_disclosed(self):
        self.assertTrue(self.scenario['prices_are_estimates'])
        self.assertIn('不包含出发城市往返成都的大交通', self.markdown)
        self.assertIn('未预订', self.markdown)
        self.assertIn('人工编排内容没有冒充脚本直接生成的文本', self.markdown)
        self.assertIn('无需换汇', self.markdown)


if __name__ == '__main__':
    unittest.main()
