# Model evaluation protocol

## Purpose

Measure how consistently code-review systems identify known defects in a fixed set of 22 small code-review tasks across Python, JavaScript, and C++. The benchmark includes explicit contracts and hand-authored gold tags.

## Important provenance note

The scenarios and gold tags are authored for this portfolio project. They are not taken from a commercial evaluation suite. No provider/model scores should be reported until actual outputs from that named model/version have been collected and scored.

## Fair comparison procedure

1. Use the same benchmark cases, system instructions, output schema, and generation settings for each model.
2. Use a fresh conversation for each model. Do not give the model the gold tags or expected findings.
3. Ask each model to review all 22 cases (or split into fixed batches if context limits require it).
4. Preserve the raw response, provider, exact model/version, date, prompt, temperature, token limit, and whether tools were enabled.
5. Convert each response to `benchmarks/submission-template.json` format. For each finding, include a tag, severity, evidence, impact, and suggested fix. Tags should be chosen from the gold tags only when the finding genuinely matches; record unmatched valid findings with a descriptive new tag for human adjudication.
6. Run the evaluator and report micro precision, recall, F1, severity agreement, and coverage.
7. Manually adjudicate synonyms, false positives, evidence quality, and fixes before publishing any ranking. The automated tag score is a screening metric, not a complete semantic judgement.
8. Do not compare incomplete submissions as if they covered the same cases. Compare like-for-like case coverage.

## Standard review prompt

Use this same prompt for every model. Insert the case objects from `benchmarks/model-prompts.json` (which intentionally excludes gold tags).

> You are a careful senior software engineer reviewing code. For each case, assess the code only against the stated task contract. Identify concrete correctness, edge-case, safety, complexity, or maintainability issues. Do not invent defects that contradict explicit preconditions. Return valid JSON only, using this schema:
>
> `{"case_id":"...","findings":[{"tag":"short_snake_case","severity":"critical|high|medium|low|info","evidence":"specific code evidence","impact":"concrete consequence","fix":"actionable correction"}]}`
>
> Include only actionable findings. If you find no issue, return an empty findings array. Treat each case independently. Do not assume hidden requirements beyond the task statement.

## Run the evaluator

From the repository root:

```bash
python benchmarks/evaluate_submissions.py   --submissions path/to/actual-model-submissions.json   --out reports/model-evaluation-results.json
```

`--submissions` must be a JSON array of submission objects, one per model, following `benchmarks/submission-template.json`.

## Interpreting results

- **Precision:** proportion of predicted tags that match the gold tags.
- **Recall:** proportion of gold tags that were found.
- **F1:** harmonic mean of precision and recall.
- **Severity agreement:** proportion of matched tags whose severity exactly matches the gold label.
- **Coverage:** fraction of the 22 cases included in the submission.

A higher score does not by itself prove a model is better for all code review. Gold tags are finite, some issues require nuanced interpretation, and this benchmark has not undergone external validation or inter-rater calibration.
