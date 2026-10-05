# Evaluation: Two Sum — Return Indices

> Authored reference evaluation. This is not attributed to a specific AI model.

## Requirement
Given a list of integers and a target, return indices of two distinct elements whose values sum to the target. Assume exactly one solution exists.

## Candidate implementation
```python
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

## Findings
- **Medium — Can reuse the same element.** For `nums = [3]`, `target = 6`, it returns `[0, 0]`, violating the distinct-index requirement. It can also return the same index when a single value doubles to the target.
- **Low — Unnecessary work.** It checks ordered pairs, including duplicate pairs, giving O(n²) time.

## Corrected implementation
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    raise ValueError("No two-sum solution exists")
```

## Complexity
Expected O(n) time and O(n) auxiliary space using a hash map.

## Tests to run
| Input | Expected |
|---|---|
| `[2, 7, 11, 15]`, target `9` | indices `[0, 1]` in either order |
| `[3, 3]`, target `6` | `[0, 1]` |
| `[-1, 4, 2]`, target `1` | `[0, 2]` |
| `[3]`, target `6` | raises `ValueError` |

## Evidence policy
Run the tests against the exact candidate and corrected implementations before marking results as observed. The table above gives expected outcomes, not claimed execution results.
