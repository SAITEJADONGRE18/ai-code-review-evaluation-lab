#!/usr/bin/env python3
"""Evaluate structured code-review findings against authored gold tags.

Expected submission shape:
{
  "model_name": "Provider model/version",
  "run_date_utc": "YYYY-MM-DD",
  "notes": "Prompt/configuration details",
  "cases": [
    {"case_id": "PY-01", "findings": [
      {"tag": "same_index_reuse", "severity": "high", "evidence": "...", "fix": "..."}
    ]}
  ]
}

Only tags are used for the simple precision/recall metric. Severity agreement is
reported separately. This is a transparent baseline evaluator, not a full semantic
judge: synonym mapping and nuanced partial credit require human adjudication.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path


def score_submission(gold: dict, submission: dict) -> dict:
    gold_by_id = {case["id"]: case for case in gold["cases"]}
    seen_ids = set()
    case_rows = []
    total_tp = total_fp = total_fn = severity_matches = severity_compared = 0

    for result in submission.get("cases", []):
        case_id = result.get("case_id")
        if case_id not in gold_by_id:
            raise ValueError(f"Unknown case_id in submission: {case_id}")
        if case_id in seen_ids:
            raise ValueError(f"Duplicate case_id in submission: {case_id}")
        seen_ids.add(case_id)
        gold_findings = {f["tag"]: f for f in gold_by_id[case_id]["gold_findings"]}
        predicted = result.get("findings", [])
        predicted_by_tag = {}
        for finding in predicted:
            tag = finding.get("tag")
            if not isinstance(tag, str) or not tag.strip():
                raise ValueError(f"Every finding for {case_id} needs a non-empty tag")
            if tag in predicted_by_tag:
                raise ValueError(f"Duplicate finding tag '{tag}' for {case_id}")
            predicted_by_tag[tag] = finding

        pred_tags, gold_tags = set(predicted_by_tag), set(gold_findings)
        tp = len(pred_tags & gold_tags)
        fp = len(pred_tags - gold_tags)
        fn = len(gold_tags - pred_tags)
        total_tp += tp
        total_fp += fp
        total_fn += fn
        for tag in pred_tags & gold_tags:
            severity_compared += 1
            if predicted_by_tag[tag].get("severity") == gold_findings[tag]["severity"]:
                severity_matches += 1
        precision = tp / (tp + fp) if tp + fp else (1.0 if not gold_tags else 0.0)
        recall = tp / (tp + fn) if tp + fn else (1.0 if not gold_tags else 0.0)
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        case_rows.append({
            "case_id": case_id,
            "title": gold_by_id[case_id]["title"],
            "true_positives": tp, "false_positives": fp, "false_negatives": fn,
            "precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4),
            "missed_gold_tags": sorted(gold_tags - pred_tags),
            "unsupported_tags": sorted(pred_tags - gold_tags),
        })

    precision = total_tp / (total_tp + total_fp) if total_tp + total_fp else 0.0
    recall = total_tp / (total_tp + total_fn) if total_tp + total_fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "model_name": submission.get("model_name", "UNNAMED"),
        "run_date_utc": submission.get("run_date_utc"),
        "benchmark_version": gold.get("version"),
        "case_count_in_submission": len(case_rows),
        "case_count_in_benchmark": len(gold_by_id),
        "coverage": round(len(case_rows) / len(gold_by_id), 4) if gold_by_id else 0.0,
        "micro": {
            "true_positives": total_tp, "false_positives": total_fp, "false_negatives": total_fn,
            "precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4),
            "severity_agreement_on_matched_tags": round(severity_matches / severity_compared, 4) if severity_compared else None,
        },
        "cases": case_rows,
        "limitations": [
            "Gold tags are human-authored and finite; valid findings with different tags may be counted as false positives.",
            "Scores are not a complete semantic or safety evaluation; manually adjudicate synonyms, evidence quality, and fix quality.",
            "Compare models only when prompts, temperature, token limits, and case coverage are held constant.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, default=Path("benchmarks/gold-benchmark.json"))
    parser.add_argument("--submissions", type=Path, required=True, help="JSON array of model submission objects")
    parser.add_argument("--out", type=Path, default=Path("reports/model-evaluation-results.json"))
    args = parser.parse_args()
    gold = json.loads(args.gold.read_text(encoding="utf-8"))
    submissions = json.loads(args.submissions.read_text(encoding="utf-8"))
    if not isinstance(submissions, list) or not submissions:
        parser.error("--submissions must contain a non-empty JSON array")
    results = [score_submission(gold, item) for item in submissions]
    results.sort(key=lambda r: (r["micro"]["f1"], r["micro"]["precision"], r["micro"]["recall"]), reverse=True)
    report = {
        "report_type": "model_code_review_benchmark",
        "provenance": "Scores are computed from submitted model outputs against the included authored gold tags. No results are inferred or fabricated.",
        "ranking": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    for row in results:
        m = row["micro"]
        print(f'{row["model_name"]}: F1={m["f1"]:.3f} precision={m["precision"]:.3f} recall={m["recall"]:.3f} coverage={row["coverage"]:.1%}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
