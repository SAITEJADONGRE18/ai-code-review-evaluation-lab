"""Unit tests for evaluation validation and weighted scoring."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from code_review_lab.compare import compare_evaluations  # noqa: E402
from code_review_lab.scoring import (  # noqa: E402
    EvaluationValidationError,
    calculate_score,
    validate_evaluation,
)


def sample_record():
    return {
        "evaluation_id": "TEST-001",
        "title": "Sample evaluation",
        "language": "Python",
        "metadata": {"model": "illustrative", "date": "2026-01-01"},
        "task": "Return whether an integer is even.",
        "scores": {
            "correctness": 5,
            "edge_cases": 4,
            "testing": 4,
            "complexity": 5,
            "code_quality": 4,
        },
        "findings": [{
            "severity": "low",
            "title": "Could add a type hint",
            "evidence": "The function signature omits an input type.",
            "recommendation": "Add an int type hint if the interface requires it.",
        }],
        "tests": [{
            "name": "positive even",
            "input": "4",
            "expected": "True",
            "observed": "True",
            "status": "pass",
        }],
        "summary": "Illustrative test record.",
    }


class EvaluationValidationTests(unittest.TestCase):
    def test_valid_record_is_returned(self):
        record = sample_record()
        self.assertIs(validate_evaluation(record), record)

    def test_missing_top_level_field_fails(self):
        record = sample_record()
        del record["task"]
        with self.assertRaisesRegex(EvaluationValidationError, "task"):
            validate_evaluation(record)

    def test_score_above_five_fails(self):
        record = sample_record()
        record["scores"]["correctness"] = 6
        with self.assertRaisesRegex(EvaluationValidationError, "0 to 5"):
            validate_evaluation(record)

    def test_boolean_is_not_accepted_as_numeric_score(self):
        record = sample_record()
        record["scores"]["testing"] = True
        with self.assertRaises(EvaluationValidationError):
            validate_evaluation(record)

    def test_unknown_severity_fails(self):
        record = sample_record()
        record["findings"][0]["severity"] = "catastrophic-ish"
        with self.assertRaisesRegex(EvaluationValidationError, "unknown severity"):
            validate_evaluation(record)

    def test_unknown_score_dimension_fails(self):
        record = sample_record()
        record["scores"]["vibes"] = 5
        with self.assertRaisesRegex(EvaluationValidationError, "Unknown score dimension"):
            validate_evaluation(record)

    def test_weighted_score_is_correct(self):
        result = calculate_score(sample_record())
        self.assertEqual(result["score_out_of_100"], 90.0)
        self.assertEqual(result["dimension_scores_out_of_100"]["correctness"], 100.0)

    def test_all_zero_scores_produce_zero(self):
        record = sample_record()
        record["scores"] = {key: 0 for key in record["scores"]}
        self.assertEqual(calculate_score(record)["score_out_of_100"], 0.0)

    def test_all_five_scores_produce_one_hundred(self):
        record = sample_record()
        record["scores"] = {key: 5 for key in record["scores"]}
        self.assertEqual(calculate_score(record)["score_out_of_100"], 100.0)

    def test_invalid_test_status_fails(self):
        record = sample_record()
        record["tests"][0]["status"] = "maybe"
        with self.assertRaisesRegex(EvaluationValidationError, "status must"):
            validate_evaluation(record)


    def test_compare_same_task(self):
        first = sample_record()
        second = copy.deepcopy(first)
        second["evaluation_id"] = "TEST-002"
        second["title"] = "Alternative sample"
        second["scores"] = {key: 5 for key in second["scores"]}
        result = compare_evaluations(first, second)
        self.assertEqual(result["overall_delta_second_minus_first"], 10.0)

    def test_compare_different_tasks_fails(self):
        first = sample_record()
        second = copy.deepcopy(first)
        second["task"] = "A different task."
        with self.assertRaisesRegex(ValueError, "different task"):
            compare_evaluations(first, second)


if __name__ == "__main__":
    unittest.main()
