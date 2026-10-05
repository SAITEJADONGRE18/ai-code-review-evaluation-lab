# PY-02 — Two Sum requires distinct indices

**Type:** Authored reference evaluation.

**Requirement:** Return two distinct indices whose values sum to the target.

**Candidate defect:** A nested loop starting `j` at zero can pair an element with itself. Example: `[3]`, target `6` can return `[0, 0]`.

**Correction:** Scan once and store previously seen values and their indices. Raise `ValueError` if no pair exists.

**Complexity:** Corrected approach is expected O(n) time and O(n) extra space.

**Expected tests:** `[2,7,11,15]`, target `9`; `[3,3]`, target `6`; negative values; no-solution case; one-element input.

**Execution status:** Corrected behavior is tested in the reference runner. This is a reproducible teaching example, not a measured model result.
