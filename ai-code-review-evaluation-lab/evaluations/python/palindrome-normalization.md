# PY-01 — Palindrome normalization

**Type:** Authored reference evaluation; not attributed to a model.

**Requirement:** Ignore case and non-alphanumeric characters when checking palindromes.

**Candidate defect:** `text.lower() == text.lower()[::-1]` retains punctuation and spaces. For `"A man, a plan, a canal: Panama!"`, the candidate returns false even though normalized text is a palindrome.

**Correction:** Filter alphanumeric characters, lowercase, then compare with the reverse. See `benchmarks/python_candidates.py`.

**Complexity:** O(n) time and O(n) auxiliary space.

**Expected tests:** `"Level" → True`; `"hello" → False`; `"A man, a plan, a canal: Panama!" → True`; `"!!!" → True` under the documented empty-normalized-string policy.

**Execution status:** The corrected function is covered by the test runner `benchmarks/run_reference_tests.py`. Candidate behavior is assessed against explicit cases; do not generalize this authored example to any particular AI model.
