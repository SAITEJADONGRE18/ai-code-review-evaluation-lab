import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmarks"))
from evaluate_submissions import score_submission


class BenchmarkEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.gold = {
            "version": "test",
            "cases": [
                {"id": "T1", "title": "Example", "gold_findings": [
                    {"tag": "bug_a", "severity": "high"},
                    {"tag": "bug_b", "severity": "low"},
                ]},
                {"id": "T2", "title": "No bug", "gold_findings": []},
            ],
        }

    def test_perfect_tag_match(self):
        result = score_submission(self.gold, {
            "model_name": "test-model",
            "cases": [{"case_id": "T1", "findings": [
                {"tag": "bug_a", "severity": "high"},
                {"tag": "bug_b", "severity": "low"},
            ]}],
        })
        self.assertEqual(result["micro"]["precision"], 1.0)
        self.assertEqual(result["micro"]["recall"], 1.0)
        self.assertEqual(result["micro"]["f1"], 1.0)
        self.assertEqual(result["micro"]["severity_agreement_on_matched_tags"], 1.0)

    def test_false_positive_and_false_negative(self):
        result = score_submission(self.gold, {
            "model_name": "test-model",
            "cases": [{"case_id": "T1", "findings": [
                {"tag": "bug_a", "severity": "medium"},
                {"tag": "invented_bug", "severity": "high"},
            ]}],
        })
        self.assertEqual(result["micro"]["true_positives"], 1)
        self.assertEqual(result["micro"]["false_positives"], 1)
        self.assertEqual(result["micro"]["false_negatives"], 1)
        self.assertEqual(result["micro"]["severity_agreement_on_matched_tags"], 0.0)

    def test_duplicate_case_rejected(self):
        with self.assertRaises(ValueError):
            score_submission(self.gold, {"cases": [
                {"case_id": "T1", "findings": []},
                {"case_id": "T1", "findings": []},
            ]})

    def test_unknown_case_rejected(self):
        with self.assertRaises(ValueError):
            score_submission(self.gold, {"cases": [{"case_id": "NOPE", "findings": []}]})

if __name__ == "__main__":
    unittest.main()
