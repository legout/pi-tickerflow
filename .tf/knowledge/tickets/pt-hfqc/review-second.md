# Review (Second Opinion): pt-hfqc

## Overall Assessment
The implementation adds bounded restart logic for timeout handling in serial mode across both `ralph_run` and `ralph_start` functions. While functionally correct, there are inconsistencies between the two implementations that could lead to confusing user experience and maintenance challenges.

## Critical (must fix)
- `tf_cli/ralph.py:1253` - Error message uses `max_attempts` instead of `attempt` variable. Line reads `error_msg = f"Attempt timed out after {max_attempts} attempt(s)..."` but should use `attempt` to be consistent with the actual count. This is misleading when max_restarts=0 (shows "1 attempt(s)" even though only 1 attempt was made).

## Major (should fix)
- `tf_cli/ralph.py:1214-1271` vs `tf_cli/ralph.py:1437-1490` - **Inconsistent restart loop implementations** between `ralph_run()` and `ralph_start()`. The two functions have divergent logic:
  - `ralph_run`: increments `attempt` only on timeout, non-timeout failures exit immediately
  - `ralph_start`: increments `attempt` at start of each loop iteration
  - This creates different user-facing behavior and log outputs for the same feature
  - **Recommendation**: Extract the restart loop into a shared helper function to ensure consistency

- `tf_cli/ralph.py:1221` vs `tf_cli/ralph.py:1446` - **Inconsistent log message formats**:
  - `ralph_run`: `"Restart attempt {attempt}/{max_restarts}"`
  - `ralph_start`: `"Restart attempt {attempt - 1}/{max_restarts} for ticket (timeout: {timeout_ms}ms)"`
  - The timeout value is only logged in one path, making debugging harder for `ralph_run` users

## Minor (nice to fix)
- `tf_cli/ralph.py:1239` - Log message `"Attempt timed out, restarting ({attempt}/{max_restarts})"` is confusing because `attempt` has already been incremented, so it shows "1/2" on first timeout which could be interpreted as "attempt 1 of 2" rather than "restart 1 of 2". Consider using clearer phrasing like `"Restarting (restart {attempt} of {max_restarts})"`.

- `tf_cli/ralph.py:1446` - The condition `if attempt > 1` followed by `attempt - 1` in the log message is confusing. Consider restructuring to log before incrementing, or use a separate restart counter variable.

- `tf_cli/ralph.py:574, 601` - Resolver functions don't validate that returned values are non-negative. Negative `max_restarts` or `timeout_ms` could cause unexpected behavior.

## Warnings (follow-up ticket)
- `tf_cli/ralph.py:1437-1490` - The serial mode restart loop is not covered by automated tests. The test file only validates logging helpers. A follow-up ticket should add integration tests for:
  - Timeout triggering restart
  - Max restarts enforcement
  - Non-timeout failures not triggering restart
  - Dry-run mode only attempting once

- `tf_cli/ralph.py:1393-1394` - The timeout and restart configuration is resolved but not logged at the start of `ralph_start`, making it hard to debug configuration issues. Consider logging resolved config values at INFO level.

## Suggestions (follow-up ticket)
- `tf_cli/ralph.py:1437-1490` - Consider extracting the restart loop into a `run_ticket_with_restarts()` helper function to share logic between `ralph_run` and `ralph_start`. This would reduce code duplication and ensure consistent behavior.

- `tf_cli/ralph.py:1437-1490` - Add a small backoff delay between restart attempts (e.g., 1-5 seconds) to prevent hammering the system in a tight loop when timeouts occur rapidly.

## Positive Notes
- The `-1` return code convention for timeouts is clean and unambiguous
- The graceful process termination with SIGTERM -> SIGKILL fallback in `_run_with_timeout()` is well-implemented
- Environment variable overrides (`RALPH_ATTEMPT_TIMEOUT_MS`, `RALPH_MAX_RESTARTS`) follow good configuration priority patterns
- The dry-run mode correctly bypasses restart logic as expected
- State updates and progress display happen correctly after the restart loop completes (not per-attempt)

## Summary Statistics
- Critical: 1
- Major: 1
- Minor: 3
- Warnings: 2
- Suggestions: 2
