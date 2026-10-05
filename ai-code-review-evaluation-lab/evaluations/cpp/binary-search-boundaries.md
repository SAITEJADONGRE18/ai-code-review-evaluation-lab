# CPP-01 — Binary search out-of-bounds risk

**Type:** Authored reference evaluation.

**Requirement:** Return an index for a target in a sorted vector, otherwise `-1`.

**Finding — High:** Candidate uses `right = values.size()` with an inclusive condition, so it can index one element beyond the vector. Empty vectors are a direct boundary case.

**Correction:** Use `right = static_cast<int>(values.size()) - 1`, an inclusive range, and a safe midpoint expression. For production code, consider `std::size_t`/iterator-based approaches and vector sizes beyond `int` range.

**Complexity:** O(log n) time, O(1) auxiliary space.

**Execution:** `benchmarks/cpp_candidates.cpp` contains corrected smoke tests. Compile with C++17 and sanitizers if a compiler is available. Do not execute the unsafe candidate against boundary cases outside an isolated test process.
