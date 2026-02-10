# Review: pt-w3ie

## Overall Assessment
The timeout backoff implementation is generally well-structured with proper integration into both `ralph_run()` and `ralph_start()`. The code correctly handles backwards compatibility and follows existing patterns. However, there are several edge cases around configuration validation and error handling that could cause unexpected behavior or crashes in production.

## Critical (must fix)
- `tf/ralph.py:1158-1175` - `calculate_effective_timeout()` calls `calculate_timeout_backoff()` which raises `ValueError` if `max_ms < base_ms`. This exception is unhandled and will crash Ralph mid-execution when misconfigured. The error will propagate up and terminate the loop without proper cleanup (lock file won't be released, progress.md state stays "RUNNING").

## Major (should fix)
- `tf/ralph.py:1029-1043` - `resolve_timeout_backoff_*` functions don't validate that returned values are non-negative. Negative `increment_ms` or `max_ms` will pass through and only fail at calculation time with a potentially confusing error message. Add validation to fail fast at config load time.

- `tf/ralph.py:1158-1175` - When `backoff_enabled=True` and `base_timeout_ms=0` (no timeout), the function returns 0 immediately. This is correct behavior but silently ignores the backoff configuration. Consider logging a warning that backoff is ineffective without a base timeout.

- `tf/ralph.py:1614-1622` vs `tf/ralph.py:1237-1250` - Inconsistent logging: `ralph_start()` logs "retrying..." on timeout but `ralph_run()` logs "restarting...". Minor inconsistency but affects log parsing/monitoring.

## Minor (nice to fix)
- `tf/ralph.py:1614` - Error message says "retrying..." but the loop variable is `attempt`, not `attempt-1`, which could confuse users about which attempt number is being retried. The message shows the attempt number that just failed, not the one being started.

- `tf/ralph.py:1158-1175` - The `calculate_effective_timeout()` function is a thin wrapper around `calculate_timeout_backoff()`. The abstraction doesn't add significant value but does add parameter forwarding overhead. Consider whether this indirection is necessary or if callers should use `calculate_timeout_backoff()` directly.

- `tf/ralph/__init__.py:20-25` - Dynamic module loading via `importlib.util.spec_from_file_location()` is fragile. If the file structure changes, this will break silently. Consider a more explicit import strategy or at least add error handling with a descriptive message.

## Warnings (follow-up ticket)
- `tf/ralph.py:1541-1548` - When parallel mode falls back to serial due to timeout settings, the backoff configuration is applied but the user isn't warned specifically about backoff being active. If a user expects parallel behavior, they might not notice the fallback and wonder why timeouts are increasing.

- `tf/ralph.py:1600-1606` - The dry-run mode logs config but doesn't show what the effective timeouts would be for each attempt. Users can't preview the backoff progression without actually running.

## Suggestions (follow-up ticket)
- Consider adding a `timeoutBackoffStrategy` config option to support non-linear backoff (exponential, etc.) in the future. The current implementation hardcodes linear backoff.

- Add metrics/telemetry on how often backoff triggers (attempt counts per ticket). This would help tune increment/max values based on actual usage patterns.

- Consider capping `max_attempts` to prevent runaway loops if someone configures extremely high `maxRestarts` with small `increment_ms` - the loop could run for hours with ever-increasing timeouts.

## Positive Notes
- Backwards compatibility is well handled - default behavior unchanged with `timeoutBackoffEnabled: false`.
- Proper separation between calculation logic (`tf/utils.py`) and application logic (`tf/ralph.py`).
- Good documentation in `usage()` text explaining all three new config options.
- Consistent 0-indexed internal calculation with 1-indexed user-facing messages.
- Parallel mode correctly falls back to serial when timeout/restart settings are active.
- Both `ralph_run()` and `ralph_start()` use the same `calculate_effective_timeout()` function ensuring consistent behavior.

## Summary Statistics
- Critical: 1
- Major: 3
- Minor: 3
- Warnings: 2
- Suggestions: 3
