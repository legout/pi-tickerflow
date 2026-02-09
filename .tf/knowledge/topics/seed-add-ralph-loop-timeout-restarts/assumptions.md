# Assumptions

- The Ralph loop has a clear “per-ticket attempt” boundary where we can apply a timeout.
- Ticket implementation attempts are restartable (or at least safe to re-run) given existing worktree handling.
- Termination of a run can be performed reliably (e.g., by killing a subprocess or cancelling an async task).
- The system can surface failures in a user-visible way (TUI/log output + ticket status).
