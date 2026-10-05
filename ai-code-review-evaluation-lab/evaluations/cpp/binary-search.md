# Evaluation: Binary Search — Empty Input and Bounds

> Authored reference evaluation, not a claim about a specific model output.

## Requirement
Given a sorted vector and a target, return the target's index or `-1` if it is absent.

## Candidate implementation
```cpp
int binarySearch(const std::vector<int>& values, int target) {
    int left = 0;
    int right = static_cast<int>(values.size());
    while (left <= right) {
        int mid = (left + right) / 2;
        if (values[mid] == target) return mid;
        if (values[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

## Finding
- **High — Out-of-bounds access.** `right` is initialized to `values.size()`, but the final valid index is `size() - 1`. On empty input the first iteration attempts to access `values[0]`; for other inputs the search can also read past the end.

## Corrected implementation
```cpp
#include <vector>

int binarySearch(const std::vector<int>& values, int target) {
    int left = 0;
    int right = static_cast<int>(values.size()) - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (values[mid] == target) return mid;
        if (values[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

## Complexity
O(log n) time and O(1) auxiliary space. This implementation assumes the vector length fits in `int`; a production version can use an unsigned or size-aware index strategy carefully.

## Test matrix
- Empty vector → `-1`
- `[1, 3, 5, 7]`, target `5` → index `2`
- `[1, 3, 5, 7]`, target `2` → `-1`
- Single-element vector containing target → `0`
- Single-element vector without target → `-1`

Compile with warnings and sanitizers where available; record actual command and output before claiming execution.
