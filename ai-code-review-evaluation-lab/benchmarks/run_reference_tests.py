"""Run deterministic tests for corrected Python reference implementations."""
from python_candidates import (
    palindrome_corrected,
    two_sum_corrected,
    binary_search_corrected,
)


def run():
    checks = [
        ("palindrome basic", lambda: palindrome_corrected("Level") is True),
        ("palindrome punctuation", lambda: palindrome_corrected("A man, a plan, a canal: Panama!") is True),
        ("palindrome empty normalized", lambda: palindrome_corrected("!!!") is True),
        ("palindrome negative", lambda: palindrome_corrected("hello") is False),
        ("two sum basic", lambda: sorted(two_sum_corrected([2, 7, 11, 15], 9)) == [0, 1]),
        ("two sum duplicates", lambda: two_sum_corrected([3, 3], 6) == [0, 1]),
        ("two sum negatives", lambda: sorted(two_sum_corrected([-1, 4, 2], 1)) == [0, 2]),
        ("two sum no solution raises", lambda: raises_value_error()),
        ("binary search hit", lambda: binary_search_corrected([1, 3, 5, 7], 5) == 2),
        ("binary search miss", lambda: binary_search_corrected([1, 3, 5, 7], 2) == -1),
        ("binary search empty", lambda: binary_search_corrected([], 5) == -1),
        ("binary search single hit", lambda: binary_search_corrected([4], 4) == 0),
        ("binary search single miss", lambda: binary_search_corrected([4], 2) == -1),
    ]
    failed = []
    for name, check in checks:
        try:
            passed = bool(check())
        except Exception as exc:
            passed = False
            print(f"ERROR: {name}: {type(exc).__name__}: {exc}")
        print(f"{'PASS' if passed else 'FAIL'}: {name}")
        if not passed:
            failed.append(name)
    print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed")
    return 1 if failed else 0


def raises_value_error():
    try:
        two_sum_corrected([1], 10)
    except ValueError:
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(run())
