# PY-04 — Valid parentheses and stack discipline

**Type:** Authored reference evaluation.

**Requirement:** Determine whether `()`, `[]`, and `{}` are properly nested and matched.

**Candidate pattern reviewed:** Count opening and closing symbols independently.

**Defect:** Equal counts do not establish correct order. Input `")("` has one opening and one closing parenthesis but is invalid.

**Correction:** Use a stack; push opening symbols, and require each closing symbol to match the most recent opening symbol. Reject unexpected characters if the specification restricts the alphabet.

**Complexity:** O(n) time and O(n) worst-case space.

**Expected tests:** `"()"` valid; `"([]{})"` valid; `")("` invalid; `"([)]"` invalid; empty string valid if allowed.

**Execution status:** Specification-based review. Add an executable implementation and run tests before claiming measured outcomes.
