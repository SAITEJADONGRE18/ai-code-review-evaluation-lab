# JS-01 — Reversing Unicode strings

**Type:** Authored reference evaluation.

**Requirement:** Reverse Unicode code points.

**Finding — Medium:** `split('').reverse().join('')` splits UTF-16 code units and can corrupt characters represented by surrogate pairs.

**Correction:** `Array.from(text).reverse().join('')` reverses code points. It does not preserve grapheme clusters; for user-perceived characters, use `Intl.Segmenter` where available.

**Complexity:** O(n) time and O(n) space.

**Expected tests:** `"hello"`, empty string, `"A😀B"`, combining marks, emoji modifiers.

**Execution status:** Runnable functions are in `benchmarks/javascript_candidates.js`; use the runner and record Node.js version. Unicode behavior must match the explicitly chosen requirement.
