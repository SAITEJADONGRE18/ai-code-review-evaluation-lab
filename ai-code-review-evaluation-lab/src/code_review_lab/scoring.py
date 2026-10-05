"""Schema validation and transparent weighted scoring for review records."""

from __future__ import annotations

from typing import Any

DIMENSION_WEIGHTS: dict[str, float] = {
    "correctness": 0.35,
    "edge_cases": 0.20,
    "testing": 0.20,
    "complexity": 0.15,
    "code_quality": 0.10,
}

ALLOWED_SEVERITIES = {"critical", "high", "medium", "low", "info"}


class EvaluationValidationError(ValueError):
    """Raised when an evaluation record does not match the expected schema."""


def validate_evaluation(data: Any) -> dict[str, Any]:
    """Validate the required fields and return the original record.

    The function intentionally validates structure, not the truth of review claims.
    """
    if not isinstance(data, dict):
        raise EvaluationValidationError("The evaluation must be a JSON object.")

    required = {"evaluation_id", "title", "language", "metadata", "task", "scores", "findings", "tests", "summary"}
    missing = sorted(required - data.keys())
    if missing:
        raise EvaluationValidationError(f"Missing required top-level field(s): {', '.join(missing)}")

    for field in ("evaluation_id", "title", "language", "task", "summary"):
        if not isinstance(data[field], str) or not data[field].strip():
            raise EvaluationValidationError(f"'{field}' must be a non-empty string.")

    if not isinstance(data["metadata"], dict):
        raise EvaluationValidationError("'metadata' must be an object.")
    if not isinstance(data["scores"], dict):
        raise EvaluationValidationError("'scores' must be an object.")

    missing_scores = sorted(set(DIMENSION_WEIGHTS) - data["scores"].keys())
    extra_scores = sorted(data["scores"].keys() - set(DIMENSION_WEIGHTS))
    if missing_scores:
        raise EvaluationValidationError(f"Missing score dimension(s): {', '.join(missing_scores)}")
    if extra_scores:
        raise EvaluationValidationError(f"Unknown score dimension(s): {', '.join(extra_scores)}")

    for dimension, score in data["scores"].items():
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 5:
            raise EvaluationValidationError(f"Score '{dimension}' must be a number from 0 to 5.")

    if not isinstance(data["findings"], list):
        raise EvaluationValidationError("'findings' must be a list.")
    for index, finding in enumerate(data["findings"]):
        if not isinstance(finding, dict):
            raise EvaluationValidationError(f"Finding at index {index} must be an object.")
        for field in ("severity", "title", "evidence", "recommendation"):
            if not isinstance(finding.get(field), str) or not finding[field].strip():
                raise EvaluationValidationError(
                    f"Finding at index {index} requires a non-empty '{field}' string."
                )
        if finding["severity"].lower() not in ALLOWED_SEVERITIES:
            allowed = ", ".join(sorted(ALLOWED_SEVERITIES))
            raise EvaluationValidationError(
                f"Finding at index {index} has unknown severity '{finding['severity']}'. Allowed: {allowed}"
            )

    if not isinstance(data["tests"], list):
        raise EvaluationValidationError("'tests' must be a list.")
    for index, test in enumerate(data["tests"]):
        if not isinstance(test, dict):
            raise EvaluationValidationError(f"Test at index {index} must be an object.")
        for field in ("name", "input", "expected", "observed", "status"):
            if field not in test:
                raise EvaluationValidationError(f"Test at index {index} is missing '{field}'.")
        if test["status"] not in {"pass", "fail", "not_run"}:
            raise EvaluationValidationError(
                f"Test at index {index} status must be 'pass', 'fail', or 'not_run'."
            )

    return data


def calculate_score(data: dict[str, Any]) -> dict[str, Any]:
    """Return a weighted score out of 100 and the normalized dimension scores."""
    validate_evaluation(data)
    dimension_scores = {
        name: round((float(data["scores"][name]) / 5.0) * 100, 2)
        for name in DIMENSION_WEIGHTS
    }
    total = sum(dimension_scores[name] * weight for name, weight in DIMENSION_WEIGHTS.items())
    return {
        "evaluation_id": data["evaluation_id"],
        "title": data["title"],
        "score_out_of_100": round(total, 2),
        "dimension_scores_out_of_100": dimension_scores,
        "weights": DIMENSION_WEIGHTS.copy(),
        "interpretation": (
            "Structured reviewer aid only; read findings and test evidence before drawing conclusions."
        ),
    }
