"""Demonstrate known defects in authored candidate examples and corrected behavior.

These are controlled teaching examples, not outputs attributed to an external AI model.
"""
import unittest

from python_candidates import (
    palindrome_candidate, palindrome_corrected,
    two_sum_candidate, two_sum_corrected,
    binary_search_candidate, binary_search_corrected,
)


class CandidateBehaviorTests(unittest.TestCase):
    def test_palindrome_candidate_misses_punctuation_normalization(self):
        self.assertFalse(palindrome_candidate("A man, a plan, a canal: Panama"))
        self.assertTrue(palindrome_corrected("A man, a plan, a canal: Panama"))

    def test_two_sum_candidate_can_reuse_same_index(self):
        self.assertEqual(two_sum_candidate([3], 6), [0, 0])
        with self.assertRaises(ValueError):
            two_sum_corrected([3], 6)

    def test_two_sum_corrected_uses_distinct_indices(self):
        result = two_sum_corrected([3, 3], 6)
        self.assertEqual(result, [0, 1])
        self.assertNotEqual(result[0], result[1])

    def test_binary_search_candidate_can_index_past_end(self):
        with self.assertRaises(IndexError):
            binary_search_candidate([1, 3, 5], 99)
        self.assertEqual(binary_search_corrected([1, 3, 5], 99), -1)

    def test_binary_search_corrected_empty_and_boundaries(self):
        self.assertEqual(binary_search_corrected([], 1), -1)
        self.assertEqual(binary_search_corrected([1, 3, 5], 1), 0)
        self.assertEqual(binary_search_corrected([1, 3, 5], 5), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
