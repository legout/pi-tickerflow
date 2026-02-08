# Review: pt-hfqc

## Overall Assessment
The implementation correctly adds bounded retry logic for ticket attempts when timeouts occur in serial `tf ralph start` execution. The code is well-structured, follows existing patterns in the codebase, and handles edge cases appropriately. All 47 logging tests pass and syntax validation succeeds.

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf_cli/ralph.py:1427` - The conditional `if max_restarts > 0` is unnecessary since `max_restarts + 1` works correctly for all values including 0. The expression could be simplified to `max_restarts + 1` for cleaner code, though the current implementation is functionally correct.

## Warnings (follow-up ticket)
No warnings - the implementation scope is well-contained.

## Suggestions (follow-up ticket)
- `tf_cli/ralph.py:1423-1474` - Consider adding unit tests specifically for the restart loop logic (mocking `run_ticket` to return -1 and verifying the retry behavior). This would help prevent regressions in this critical path.
- `tf_cli/ralph.py` - Consider adding brief documentation about timeout/restart behavior to the user-facing help text in `usage()` function, mentioning the `RALPH_ATTEMPT_TIMEOUT_MS` and `RALPH_MAX_RESTARTS` environment variables.

## Positive Notes
- Clean implementation of timeout detection using `-1` return code from `run_ticket()` (line 474)
- Correct attempt counting with 1-based user-facing messages ("attempt 1 of 3")
- Proper dry-run handling that exits after first attempt
- Good separation of concerns with helper functions `resolve_attempt_timeout_ms()` and `resolve_max_restarts()`
- Comprehensive logging includes attempt numbers and timeout thresholds as required
- Correct behavior: non-timeout failures exit the restart loop immediately without unnecessary retries
- Environment variable overrides (`RALPH_ATTEMPT_TIMEOUT_MS`, `RALPH_MAX_RESTARTS`) provide flexibility without config file changes
- The `_run_with_timeout()` function properly handles process termination (SIGTERM, then SIGKILL after 5s) and prevents zombie processes

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 0
- Suggestions: 2
