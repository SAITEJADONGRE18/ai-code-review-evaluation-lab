# Evaluation: Palindrome Checker — Input Normalization

> **Status:** Demonstration case. This is an authored teaching example, not a claim about a particular AI model.

## Task

Implement `is_palindrome(text)` that:
1. Ignores letter case.
2. Ignores non-alphanumeric characters.
3. Returns `True` for an empty normalized string.
4. Returns a Boolean.

## Candidate implementation

```python
def is_palindrome(text):
    text = text.lower()
    return text == text[::-1]
```

## Review findings

### Finding 1 — Medium: Does not ignore punctuation or spaces

**Evidence:** `is_palindrome("A man, a plan, a canal: Panama!")` returns `False` in the candidate implementation because spaces and punctuation remain in the string.

**Impact:** The candidate violates the stated normalization requirement for common natural-language inputs.

**Recommendation:** Normalize the input by retaining only alphanumeric characters before comparing the string with its reverse.

### Finding 2 — Low: No type contract

**Evidence:** The function assumes the input is a string but does not document or enforce that assumption.

**Impact:** Non-string input may raise an attribute error. Whether that is a defect depends on the interface contract.

**Recommendation:** Add a type hint and decide whether invalid types should raise `TypeError` or be handled by the caller.

## Corrected implementation

```python
def is_palindrome(text: str) -> bool:
    normalized = "".join(char.lower() for char in text if char.isalnum())
    return normalized == normalized[::-1]
```

This implementation filters non-alphanumeric characters, lowercases retained characters, and compares the normalized string to its reverse. Its time complexity is **O(n)** and auxiliary space is **O(n)** for the normalized string, where `n` is the input length.

## Suggested test matrix

| Input | Expected | Reason |
|---|---|---|
| `"level"` | `True` | Basic palindrome |
| `"Level"` | `True` | Case normalization |
| `"hello"` | `False` | Non-palindrome |
| `"A man, a plan, a canal: Panama!"` | `True` | Spaces and punctuation |
| `""` | `True` | Empty normalized input |
| `"!!!"` | `True` | Normalizes to empty |
| `"abca"` | `False` | Near-palindrome |

## Reproducible test code

```python
def test_is_palindrome():
    assert is_palindrome("level") is True
    assert is_palindrome("Level") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("A man, a plan, a canal: Panama!") is True
    assert is_palindrome("") is True
    assert is_palindrome("!!!") is True
    assert is_palindrome("abca") is False
```

## Rubric notes

Scores should be assigned only after running the exact candidate against the test matrix. Do not copy example scores into a real model comparison without performing the tests.
