# CPP-05 — Const-correctness in read-only APIs

**Type:** Authored reference evaluation.

**Requirement:** A function reads a vector and should not mutate it.

**Candidate pattern reviewed:** Accept a mutable reference and unintentionally modify values while searching.

**Finding:** The signature permits mutation that is not part of the function contract, making accidental changes easier.

**Correction:** Accept `const std::vector<T>&` for read-only access and keep mutation in a separate, explicitly named operation.

**Complexity:** This is an API safety and maintainability concern, not necessarily a runtime defect.

**Expected tests:** Compile-time checks and behavioral tests confirming input remains unchanged.

**Execution status:** Design review. Severity depends on public API guarantees and actual mutation.
