# MVP Scope

## In Scope

- Add a timeout for a single ticket implementation attempt.
- Add a `max_restarts` (max retries) setting.
- Implement restart logic (timeout → abort attempt → retry until limit).
- Ensure cleanup (process termination + worktree/session cleanup as appropriate).
- Add minimal tests (unit/integration) for timeout/retry paths.

## Out of Scope (for MVP)

- Adaptive timeouts based on ticket type or historical runtime.
- Heartbeat/progress-based “stuck” detection.
- Distributed/remote execution supervision.
- Sophisticated backoff strategies beyond a simple bounded retry.
