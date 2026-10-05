# PY-03 — Binary search bounds

**Type:** Authored reference evaluation.

**Requirement:** Find a target in a sorted list; return `-1` when absent.

**Candidate defect:** Setting an inclusive right index to `len(values)` permits an out-of-range access. Empty input can fail immediately.

**Correction:** Initialize `right = len(values) - 1`; calculate midpoint as `left + (right - left) // 2`.

**Complexity:** O(log n) time, O(1) auxiliary space.

**Expected tests:** Empty list, one-element hit/miss, middle hit, absent value below and above range.

**Execution status:** Corrected Python implementation is covered by the reference runner. The unsafe candidate is not executed on empty input in-process because it may raise an exception; its defect is established by the index invariant.
