# Success Metrics

- A stuck `/tf` ticket run is aborted automatically after the configured timeout.
- Ralph retries the same ticket implementation attempt up to `max_restarts` and then marks it failed (no infinite loops).
- Logs clearly show:
  - timeout threshold
  - elapsed time
  - attempt number / restart count
  - how the run was terminated
- No orphaned processes or dangling worktrees remain after a timeout/restart.
- Normal (non-stuck) tickets are not materially slowed down.
