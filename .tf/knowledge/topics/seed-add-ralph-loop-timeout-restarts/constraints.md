# Constraints

- Must be bounded: restarting must stop after `max_restarts`.
- Must avoid leaving zombie processes or corrupted state.
- Must not break existing Ralph parallelism/worktree behavior.
- Timeouts and retries must be observable (logs + status reporting).
- Defaults should be conservative (avoid false-positive timeouts).
