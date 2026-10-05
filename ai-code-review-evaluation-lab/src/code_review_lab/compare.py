"""Compare two scored evaluation records without pretending scores prove correctness."""

from __future__ import annotations

from typing import Any
from code_review_lab.scoring import calculate_score, validate_evaluation


def compare_evaluations(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    """Compare two records for the same task and return score deltas.

    Positive deltas mean the second record scored higher than the first.
    Comparisons are only meaningful when task and scoring conditions are comparable.
    """
    validate_evaluation(first)
    validate_evaluation(second)
    if first["task"].strip() != second["task"].strip():
        raise ValueError("Cannot compare evaluations with different task descriptions.")
    first_result = calculate_score(first)
    second_result = calculate_score(second)
    deltas = {
        dimension: round(
            second_result["dimension_scores_out_of_100"][dimension]
            - first_result["dimension_scores_out_of_100"][dimension], 2
        )
        for dimension in first_result["dimension_scores_out_of_100"]
    }
    return {
        "task": first["task"],
        "first": {
            "evaluation_id": first_result["evaluation_id"],
            "title": first_result["title"],
            "score_out_of_100": first_result["score_out_of_100"],
        },
        "second": {
            "evaluation_id": second_result["evaluation_id"],
            "title": second_result["title"],
            "score_out_of_100": second_result["score_out_of_100"],
        },
        "overall_delta_second_minus_first": round(
            second_result["score_out_of_100"] - first_result["score_out_of_100"], 2
        ),
        "dimension_deltas_second_minus_first": deltas,
        "warning": "Score differences summarize reviewer ratings; they do not establish statistical significance or objective model superiority.",
    }
