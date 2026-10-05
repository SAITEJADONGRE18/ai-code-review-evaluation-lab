# JS-04 — Unexpected input mutation

**Type:** Authored reference evaluation.

**Requirement:** Transform a collection without modifying the caller's original array, if immutability is part of the contract.

**Candidate pattern reviewed:** Call `array.sort()` directly on an input array.

**Finding:** `sort()` mutates the original array. This can cause surprising side effects for other consumers of the same reference.

**Correction:** Copy before sorting (`[...array].sort(compareFn)`) when a non-mutating result is required. Always provide a comparator for numeric ordering.

**Complexity:** Copy is O(n) space; sorting complexity depends on the runtime implementation and should not be overclaimed.

**Expected tests:** Verify sorted result and verify original input remains unchanged.

**Execution status:** Language behavior review; run against the intended runtime for the project record.
