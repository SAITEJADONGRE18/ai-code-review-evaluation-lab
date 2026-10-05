# Evaluation: Reverse a String — Unicode Scope

> Authored reference evaluation, not a claim about a specific model output.

## Requirement
Return the input string with its Unicode code points reversed. This requirement does not promise grapheme-cluster preservation.

## Candidate implementation
```javascript
function reverseString(text) {
  return text.split("").reverse().join("");
}
```

## Finding
- **Medium — Splits UTF-16 code units, not Unicode code points.** Some characters represented by surrogate pairs can be split and corrupted. Combining marks and multi-code-point emoji may also display unexpectedly even if code points are reversed correctly.

## Corrected implementation
```javascript
function reverseString(text) {
  return Array.from(text).reverse().join("");
}
```

`Array.from` iterates Unicode code points, avoiding surrogate-pair splitting. It does not preserve grapheme clusters (for example, an emoji plus skin-tone modifier or a base letter plus combining mark). If user-perceived characters must remain intact, use `Intl.Segmenter` where supported.

## Complexity
O(n) time and O(n) space, where n is the number of code points produced by iteration.

## Test matrix
- `"hello"` → `"olleh"`
- `""` → `""`
- `"A😀B"` → `"B😀A"`
- `"e\u0301"` → code-point reversal produces combining mark before `e`; grapheme-aware reversal should preserve the visible accented character as one unit.

Run in the intended Node.js/browser runtime and document Unicode assumptions.
