import json
import unittest
from pathlib import Path
from src.grader import calculate, GradingError

ROOT = Path(__file__).resolve().parents[1]


class TestGrader(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / 'examples/example-reviewed-report.json').read_text())
        self.rubric = json.loads((ROOT / 'rubrics/core-25.json').read_text())

    def test_scores_draft(self):
        result = calculate(self.report, self.rubric)
        self.assertEqual(result['earned'], 19)
        self.assertEqual(result['percentage'], 76.0)
        self.assertFalse(result['release_authorized'])

    def test_rejects_over_maximum(self):
        self.report['criteria_scores'][0]['points'] = 6
        with self.assertRaises(GradingError):
            calculate(self.report, self.rubric)

    def test_rejects_duplicate_criteria(self):
        self.report['criteria_scores'][1]['criterion_id'] = 'workflow_design'
        with self.assertRaises(GradingError):
            calculate(self.report, self.rubric)

    def test_rejects_unapproved_release(self):
        self.report['status'] = 'released'
        self.report['released_at'] = '2026-11-19T11:00:00Z'
        with self.assertRaises(GradingError):
            calculate(self.report, self.rubric)

    def test_approved_report(self):
        self.report.update(status='approved', approved_by='instructor-123', approved_at='2026-11-19T11:00:00Z')
        self.assertTrue(calculate(self.report, self.rubric)['release_authorized'])


if __name__ == '__main__':
    unittest.main()
