# CPP-02 — Removing duplicates from a sorted vector

**Type:** Authored reference evaluation.

**Requirement:** Given a sorted vector, remove duplicates in place and return the new logical length.

**Candidate pattern reviewed:** Build a second vector and copy unique values back.

**Finding:** It can be correct, but uses O(n) additional space when the requirement asks for in-place mutation.

**Correction:** Use a write index: preserve the first item, then copy each value different from the last kept value into the next output slot.

**Complexity:** O(n) time and O(1) auxiliary space.

**Expected tests:** Empty vector, one item, all equal values, all distinct values, multiple repeated runs.

**Execution status:** Algorithmic review; record compiler and actual test output when implementing a runnable case.
