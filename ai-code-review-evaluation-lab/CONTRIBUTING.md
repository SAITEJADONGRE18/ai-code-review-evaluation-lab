# Contributing

Thanks for helping improve the lab. Keep evaluations reproducible and evidence-based.

## Before submitting an evaluation

- State the problem and assumptions clearly.
- Preserve the candidate output before editing it.
- Record the language/runtime and exact test commands.
- Include normal, boundary, and failure-oriented tests.
- Link every claimed defect to a reproducible input or other concrete evidence.
- Explain the correction and any remaining limitations.
- Do not publish confidential prompts, customer data, secrets, or restricted model output.

## Style

- Use descriptive filenames such as `python-two-sum.md`.
- Keep one primary task per evaluation file.
- Prefer small, reproducible examples over unsupported generalizations.
- Avoid scoring based on personal preference when no requirement or measurable impact is involved.
- Mark authored examples as illustrative; do not imply they are measured model results.

## Tests

Run:

```bash
python -m unittest discover -s tests -v
```

For scoring changes, add tests for valid records, missing fields, invalid scores, and malformed input.
