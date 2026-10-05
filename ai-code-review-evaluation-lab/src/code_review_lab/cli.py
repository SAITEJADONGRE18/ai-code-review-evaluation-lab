"""Command-line interface for validation, scoring, and comparison."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from code_review_lab.compare import compare_evaluations
from code_review_lab.scoring import EvaluationValidationError, calculate_score, validate_evaluation


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise EvaluationValidationError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvaluationValidationError(
            f"Invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    except OSError as exc:
        raise EvaluationValidationError(f"Could not read {path}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="code-review-lab",
        description="Validate and score structured code-review evaluation records.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "score"):
        command_parser = subparsers.add_parser(command, help=f"{command.title()} an evaluation JSON file")
        command_parser.add_argument("path", type=Path, help="Path to the evaluation JSON file")
    compare_parser = subparsers.add_parser("compare", help="Compare two records for the same task")
    compare_parser.add_argument("first", type=Path)
    compare_parser.add_argument("second", type=Path)
    args = parser.parse_args(argv)

    try:
        if args.command == "compare":
            result = compare_evaluations(load_json(args.first), load_json(args.second))
            print(json.dumps(result, indent=2))
            return 0
        record = load_json(args.path)
        validate_evaluation(record)
        result = calculate_score(record)
    except (EvaluationValidationError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.command == "validate":
        print(f"VALID: {result['evaluation_id']} — {result['title']}")
        print(f"Weighted score: {result['score_out_of_100']}/100")
        print("Dimension scores:")
        for dimension, score in result["dimension_scores_out_of_100"].items():
            print(f"  - {dimension.replace('_', ' ').title()}: {score}/100")
    else:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
