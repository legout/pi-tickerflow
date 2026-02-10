# Review: pt-ussr

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf/ralph/queue_state.py:107-108` - The `get_queue_state_from_scheduler()` function accepts a `dep_resolver` callable but never validates that the returned sets are non-empty before adding to `dep_graph`. While the current code handles this correctly (empty sets mean not blocked), adding a comment or filtering would improve clarity. *(reviewer-general)*

- `tf/ralph.py:1537` - The `start_ticket()` call passes `str(queue_state.total)` as the third positional argument. Explicitly using the keyword argument `total_tickets=str(queue_state.total)` would be clearer and more maintainable. *(reviewer-second-opinion)*

- `tests/test_progress_display.py` and `tests/test_logger.py` - No tests verify that `queue_state` parameter is actually passed and rendered in output. The existing tests mock `ProgressDisplay` but don't verify the `queue_state` parameter. *(reviewer-second-opinion)*

## Warnings (follow-up ticket)
- `tf/ralph.py:1478-1510` - The queue state computation in `ralph_start()` recomputes `list_ready_tickets()` and `list_blocked_tickets()` after each ticket completion. While the implementation.md claims this is "in-memory scheduler state", the actual implementation calls external `tk` commands which could be slow for large backlogs. Consider caching these results within the iteration. *(reviewer-general)*

- **Missing unit tests for queue_state.py**: The plan explicitly requires "Unit tests for `queue_state.py` helper (ready/blocked/running/done invariants)" but no dedicated test file exists. This is acknowledged in the ticket's linked work (pt-ri6k: "Add tests for queue-state counts + progress/log formatting"). *(reviewer-spec-audit)*

- `tf/ralph.py:1523-1533` - The `list_blocked_tickets()` function depends on `tk blocked` command. If this command is unavailable or returns different output formats, the queue state computation could be incorrect. Consider adding validation or fallback behavior. *(reviewer-second-opinion)*

## Suggestions (follow-up ticket)
- `tf/ralph/queue_state.py` - No dedicated unit tests exist for the `QueueStateSnapshot` class or `get_queue_state()` function. While these are implicitly tested through integration tests, dedicated unit tests would improve maintainability and document edge cases (e.g., empty queues, validation failures). *(reviewer-general)*

- `tf/logger.py:173-174` - The `log_ticket_start()` method formats queue state differently than `ProgressDisplay` - logger uses `[R:X B:Y done:D/T]` while display uses `R:X B:Y (done D/T)`. Consider standardizing the format for consistency. *(reviewer-general)*

- `tf/ralph/queue_state.py` - Consider adding unit tests specifically for `QueueStateSnapshot` and `get_queue_state()` to document expected behavior and prevent regressions. The class has validation logic in `__post_init__` that should be tested. *(reviewer-second-opinion)*

- `tf/ralph.py:1527-1546` and `tf/ralph.py:1603-1629` - The queue state computation is duplicated in both the start and complete sections. Consider extracting a helper function like `_compute_queue_state()` to reduce duplication and improve maintainability. *(reviewer-second-opinion)*

## Positive Notes
- The `QueueStateSnapshot` dataclass uses `frozen=True` for immutability and includes comprehensive `__post_init__` validation that catches invariant violations early.
- TTY mode correctly uses `\x1b[2K\r` for clearing lines without flickering, while non-TTY mode produces clean output without control characters.
- The progress display properly shows timestamps in `HH:MM:SS` format as specified.
- Queue state is correctly passed to both `ProgressDisplay` and `RalphLogger`, ensuring consistent information across UI and logs.
- The implementation correctly handles the distinction between `__str__()` (for display: `R:3 B:2 (done 1/6)`) and `to_log_format()` (for logs: `R:3 B:2 done:1/6`).
- All 74 existing tests pass, confirming backward compatibility is maintained.
- Queue state is recomputed after each ticket completion, ensuring counts accurately reflect dependency resolution as tickets complete.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 3
- Warnings: 3
- Suggestions: 4

## Reviewers
- reviewer-general
- reviewer-spec-audit
- reviewer-second-opinion
