# Evaluation Methodology

## Principles
1. **Requirements before review:** define expected behavior before examining a solution.
2. **Evidence over confidence:** tie every defect claim to a reproducible input, output, code path, or test.
3. **Comparable conditions:** A/B candidates should use the same task, constraints, runtime, and test suite.
4. **Explicit uncertainty:** record untested behavior and assumptions.
5. **Provenance:** distinguish measured model outputs from authored examples.
6. **Safety:** execute untrusted code only in a disposable, restricted environment.

## Review sequence
1. Freeze the task and acceptance criteria.
2. Preserve candidate output unchanged.
3. Inspect control flow, input assumptions, error handling, security concerns, and algorithmic behavior.
4. Create tests: typical, boundary, invalid, adversarial, and regression cases as appropriate.
5. Execute tests in a recorded environment.
6. Reproduce and classify findings by impact.
7. Implement and test a correction.
8. Analyze time/space complexity under stated assumptions.
9. Score each dimension using the rubric.
10. Ask a second reviewer to inspect a sample of records when possible.

## Severity
- **Critical:** likely catastrophic security, integrity, or availability impact in the intended context.
- **High:** major requirement failure or serious defect in common/important cases.
- **Medium:** meaningful failure in a subset of cases or substantial reliability issue.
- **Low:** limited impact defect.
- **Info:** suggestion without a demonstrated defect.

Severity is contextual. Explain the impact rather than relying on the label alone.

## Rubric
Each dimension is rated 0–5 and weighted:
- Correctness: 35%
- Edge cases: 20%
- Testing: 20%
- Complexity: 15%
- Code quality: 10%

Weighted score = sum((rating / 5) × dimension weight × 100). Scores support structured discussion; they are not ground truth. Before using them as a benchmark, calibrate reviewers, measure agreement, and document uncertainty.

## Reporting rules
- Never report a test as passed unless it was run and passed.
- Mark unexecuted cases `not_run`.
- Do not compare raw scores from different tasks as if they were directly comparable.
- Do not infer general model superiority from a small convenience sample.
- Do not publish confidential data or secrets.
