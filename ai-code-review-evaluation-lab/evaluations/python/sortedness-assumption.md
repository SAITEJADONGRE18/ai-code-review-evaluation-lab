# PY-07 — Hidden sorted-input assumption

**Type:** Authored reference evaluation.

**Requirement:** A binary-search helper expects sorted input.

**Finding:** If the API does not state the sorted-input precondition, callers may pass unsorted values and receive a misleading `-1` or wrong index.

**Correction:** Document the precondition, validate sortedness when appropriate (O(n) overhead), or use a search method that matches unsorted input requirements.

**Complexity:** Binary search itself is O(log n); checking sortedness first is O(n).

**Expected tests:** Sorted hit/miss, unsorted input, duplicate values, empty input.

**Execution status:** Requirement and API review; the missing precondition is a documentation/contract issue unless sorted input is already guaranteed.
