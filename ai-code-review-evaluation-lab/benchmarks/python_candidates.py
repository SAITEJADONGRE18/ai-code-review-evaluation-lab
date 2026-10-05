"""Runnable Python examples used by the lab's reference evaluations."""


def palindrome_candidate(text):
    # Candidate: fails the requirement to ignore punctuation and whitespace.
    text = text.lower()
    return text == text[::-1]


def palindrome_corrected(text: str) -> bool:
    normalized = "".join(char.lower() for char in text if char.isalnum())
    return normalized == normalized[::-1]


def two_sum_candidate(nums, target):
    # Candidate: can reuse the same index.
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return None


def two_sum_corrected(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    raise ValueError("No two-sum solution exists")


def binary_search_candidate(values, target):
    # Candidate: uses an inclusive right bound incorrectly.
    left, right = 0, len(values)
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def binary_search_corrected(values: list[int], target: int) -> int:
    left, right = 0, len(values) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
