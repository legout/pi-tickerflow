# Review: pt-ussr

## Overall Assessment
The implementation for updating Ralph progress display with ready/blocked counts is functionally complete and well-structured. The QueueStateSnapshot class provides immutable queue state with proper validation, and both TTY and non-TTY output modes are correctly handled. All 63 relevant tests pass.

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf/ralph/queue_state.py:107-108` - The `get_queue_state_from_scheduler()` function accepts a `dep_resolver` callable but never validates that the returned sets are non-empty before adding to `dep_graph`. While the current code handles this correctly (empty sets mean not blocked), adding a comment or filtering would improve clarity.

## Warnings (follow-up ticket)
- `tf/ralph.py:1478-1510` - The queue state computation in `ralph_start()` recomputes `list_ready_tickets()` and `list_blocked_tickets()` after each ticket completion. While the implementation.md claims this is "in-memory scheduler state", the actual implementation calls external `tk` commands which could be slow for large backlogs. Consider caching these results within the iteration.

## Suggestions (follow-up ticket)
- `tf/ralph/queue_state.py` - No dedicated unit tests exist for the `QueueStateSnapshot` class or `get_queue_state()` function. While these are implicitly tested through integration tests, dedicated unit tests would improve maintainability and document edge cases (e.g., empty queues, validation failures).
- `tf/logger.py:173-174` - The `log_ticket_start()` method formats queue state differently than `ProgressDisplay` - logger uses `[R:X B:Y done:D/T]` while display uses `R:X B:Y (done D/T)`. Consider standardizing the format for consistency.

## Positive Notes
- The `QueueStateSnapshot` dataclass uses `frozen=True` for immutability and includes comprehensive `__post_init__` validation that catches invariant violations early.
- TTY mode correctly uses `\x1b[2K\r` for clearing lines without flickering, while non-TTY mode produces clean output without control characters.
- The progress display properly shows timestamps in `HH:MM:SS` format as specified.
- Queue state is correctly passed to both `ProgressDisplay` and `RalphLogger`, ensuring consistent information across UI and logs.
- The implementation correctly handles the distinction between `__str__()` (for display: `R:3 B:2 (done 1/6)`) and `to_log_format()` (for logs: `R:3 B:2 done:1/6`).
- All existing tests pass, confirming backward compatibility is maintained.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 1
- Suggestions: 2
