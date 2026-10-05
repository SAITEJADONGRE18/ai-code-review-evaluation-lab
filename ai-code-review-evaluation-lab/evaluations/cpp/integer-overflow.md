# CPP-03 — Integer overflow in midpoint and arithmetic

**Type:** Authored reference evaluation.

**Requirement:** Compute the midpoint of valid integer bounds safely.

**Candidate pattern reviewed:** `int mid = (left + right) / 2`.

**Finding:** If `left + right` exceeds the maximum representable signed `int`, signed overflow is undefined behavior in C++.

**Correction:** For non-negative ordered bounds, use `left + (right - left) / 2`; still ensure the chosen type can represent the indices. Use wider types when the domain requires them.

**Complexity:** O(1) per midpoint calculation.

**Expected tests:** Bounds near the maximum representable index in a synthetic arithmetic unit test; sanitizer-enabled build.

**Execution status:** Language-semantics review; do not claim a runtime overflow was observed unless the exact test was run.
