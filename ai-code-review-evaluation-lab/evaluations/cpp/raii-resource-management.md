# CPP-04 — Resource cleanup and RAII

**Type:** Authored reference evaluation.

**Requirement:** Ensure a resource is released on normal return and exceptional paths.

**Candidate pattern reviewed:** Acquire a raw resource, then manually release it at the end of the function.

**Finding — Context-dependent:** Early returns or exceptions may bypass cleanup, leaking the resource.

**Correction:** Prefer RAII: standard library containers, `std::unique_ptr`, `std::lock_guard`, or a dedicated scope-bound owner depending on the resource.

**Complexity:** Not applicable as an algorithmic complexity claim; discuss resource lifecycle and exception safety.

**Expected tests:** Normal path, early return, exception path, repeated calls, and resource ownership transfer.

**Execution status:** Design review. State the resource and ownership contract before assigning severity.
