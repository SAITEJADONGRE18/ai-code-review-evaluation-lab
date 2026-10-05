# JS-03 — Async error handling

**Type:** Authored reference evaluation.

**Requirement:** Report failures from an asynchronous operation to the caller.

**Candidate pattern reviewed:** Start a promise-returning operation without returning or awaiting it, then return success immediately.

**Finding — High in request/transaction flows:** The caller cannot reliably observe completion or failure; errors may become unhandled rejections.

**Correction:** Return the promise or `await` it within a `try/catch`, and define how errors propagate.

**Complexity:** Not meaningful without a specific workload; focus on control flow and error propagation.

**Expected tests:** Resolved promise, rejected promise, thrown synchronous error, caller awaiting completion.

**Execution status:** Pattern-level review. Use a concrete function and runtime tests before asserting observed behavior.
