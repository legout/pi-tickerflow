# Review: pt-ussr

## Overall Assessment
The implementation for updating Ralph progress display with ready/blocked counts is complete and functional. The code correctly integrates `QueueStateSnapshot` into both the `ProgressDisplay` class for TTY/non-TTY output and the `RalphLogger` for structured logging. All acceptance criteria are met, and existing tests pass.

## Critical (must fix)
No issues found

## Major (should fix)
No issues found

## Minor (nice to fix)
- `tf/ralph/queue_state.py` - No unit tests exist for this module. While the code is straightforward, adding tests for `QueueStateSnapshot` validation, `get_queue_state()` edge cases, and format methods would improve maintainability.

## Warnings (follow-up ticket)
- `tests/test_progress_display.py` - Tests don't verify queue_state formatting in progress output. The test file only tests basic TTY/non-TTY behavior without the `R:<n> B:<n>` format.
- `tests/test_logger.py` - Tests for `log_ticket_start()` and `log_ticket_complete()` don't verify queue_state is correctly formatted in log output.

## Suggestions (follow-up ticket)
- `tf/ralph.py:1525-1537` - Consider caching `list_ready_tickets()` and `list_blocked_tickets()` results to avoid duplicate shell calls when computing queue state at ticket start and completion.
- `tf/ralph/queue_state.py:90-104` - The `get_queue_state_from_scheduler()` convenience function exists but is not used anywhere. Consider removing if not needed, or document when to use it vs `get_queue_state()`.

## Positive Notes
- Clean separation of concerns: `QueueStateSnapshot` handles formatting, `ProgressDisplay` handles UI, `RalphLogger` handles logging
- Good type hints throughout with proper `Optional` annotations
- Immutable dataclass with invariant validation ensures data integrity
- Both TTY (`\x1b[2K\r` for clear line) and non-TTY (plain text) modes properly implemented
- Backward compatible: queue_state parameter is optional in all public methods
- Queue state is recomputed after each ticket completion to reflect updated counts
- Logger uses separate format (`to_log_format()`) optimized for log parsing vs display

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 2
- Suggestions: 2
