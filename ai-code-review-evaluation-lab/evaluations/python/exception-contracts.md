# PY-06 — Explicit exception contract

**Type:** Authored reference evaluation.

**Requirement:** A function that cannot satisfy its contract must report failure predictably.

**Candidate pattern reviewed:** Return `None` for a missing result even though callers expect a list of indices.

**Finding:** An ambiguous sentinel can cause downstream type errors and hide the reason no result exists.

**Correction:** Either document and type a sentinel return (`list[int] | None`) or raise a specific exception. The correct choice depends on the API contract.

**Complexity:** Depends on the underlying algorithm; do not score complexity without reviewing it.

**Expected tests:** Normal result, no-result case, invalid input, caller handling the failure.

**Execution status:** Contract review. This is not automatically a bug unless the stated API requires a different behavior.
