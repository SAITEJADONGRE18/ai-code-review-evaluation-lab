// Reference C++ examples. Compile with:
// g++ -std=c++17 -Wall -Wextra -Wpedantic -fsanitize=address,undefined cpp_candidates.cpp -o cpp_candidates
#include <iostream>
#include <vector>

// Candidate: right is one past the final valid index, creating out-of-bounds risk.
int binarySearchCandidate(const std::vector<int>& values, int target) {
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

int binarySearchCorrected(const std::vector<int>& values, int target) {
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

int main() {
    const std::vector<int> values{1, 3, 5, 7};
    if (binarySearchCorrected(values, 5) != 2) return 1;
    if (binarySearchCorrected(values, 2) != -1) return 2;
    if (binarySearchCorrected({}, 5) != -1) return 3;
    std::cout << "C++ corrected binary-search smoke tests passed\n";
    return 0;
}
