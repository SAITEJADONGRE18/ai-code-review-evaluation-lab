# PY-05 — Duplicate detection

**Type:** Authored reference evaluation.

**Requirement:** Return whether a collection contains a repeated value.

**Candidate pattern reviewed:** Compare every pair of elements.

**Finding:** The pairwise approach can be correct but costs O(n²) time. It may be acceptable for tiny fixed inputs; it is a performance issue rather than a correctness bug.

**Correction:** Use a set and stop when an item has already been seen.

**Complexity:** Expected O(n) time and O(n) space for hashable values.

**Expected tests:** Empty list, one item, all unique values, duplicate at beginning/end, negative integers.

**Execution status:** Design review; distinguish algorithmic trade-offs from defects. Do not classify slower code as incorrect unless a performance requirement is violated.
