# Assumptions

- The `--session` argument currently forwarded to `pi` is not strictly required for correctness, or its behavior can be replaced by a deterministic default.
- Ralph already has enough context (ticket id / run directory / knowledge dir) to identify the correct working state without Pi session plumbing.
- Removing `--session` will not silently merge unrelated runs (or we can enforce isolation another way).
