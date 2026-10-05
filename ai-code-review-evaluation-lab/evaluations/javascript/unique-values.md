# JS-02 — Stable unique values

**Type:** Authored reference evaluation.

**Requirement:** Return unique primitive values in first-occurrence order.

**Candidate pattern reviewed:** `values.filter((value, index) => values.indexOf(value) === index)`.

**Finding:** Usually correct for this requirement, but can be O(n²) because `indexOf` scans the array for every element.

**Correction:** `[...new Set(values)]` preserves insertion order for unique values.

**Complexity:** Set-based approach is expected O(n) time and O(n) space.

**Expected tests:** Empty array, unique values, repeated values, order preservation, `NaN` behavior if relevant.

**Execution status:** Functions are included in the JavaScript reference file. Benchmark performance only with repeatable, warmed-up runs and disclose environment details.
