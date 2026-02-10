# Review: pt-w3ie

## Overall Assessment
The timeout backoff implementation is well-structured and correctly integrated into both `ralph_run()` and `ralph_start()` restart loops. The feature is opt-in (disabled by default) preserving backwards compatibility. The code correctly delegates to the existing `calculate_timeout_backoff()` utility and handles edge cases properly (disabled backoff, zero timeout, max cap).

## Critical (must fix)
No issues found

## Major (should fix)
- `tf/ralph.py:168-172` - Documentation-comment formula mismatch: The comment says `effective = attemptTimeoutMs + attempt_index * timeoutBackoffIncrementMs` but the actual formula in `calculate_effective_timeout()` passes `iteration_index=attempt_index` to `calculate_timeout_backoff()`. The documentation comment at line 106 also says "iteration" instead of "attempt". While the code is correct, the terminology inconsistency between "attempt" and "iteration" in docs vs code may confuse maintainers.

## Minor (nice to fix)
- `tf/ralph.py:1830` - Logging shows 0-indexed attempt numbers: When logging restart attempts, it displays "Restart attempt 0/N" for the first restart. Users may expect 1-indexed messaging ("Restart attempt 1/N"). This is cosmetic but may cause confusion when correlating logs with config settings.
- `tf/ralph.py:1609-1620` - Code duplication: The timeout backoff resolution (resolve_timeout_backoff_enabled, resolve_timeout_backoff_increment_ms, resolve_timeout_backoff_max_ms) is called in both `ralph_run()` and `ralph_start()`. Consider extracting to a helper function `resolve_timeout_backoff_config(config)` that returns a dataclass/namedtuple to reduce duplication and ensure consistency.

## Warnings (follow-up ticket)
- `tf/ralph.py:1756-1761` - Parallel mode warning completeness: The warning message mentions "Timeout ({base_timeout_ms}ms) and restart ({max_restarts}) settings are not supported" but doesn't mention that backoff settings are also disabled. Consider updating the warning to include backoff configuration for clarity.

## Suggestions (follow-up ticket)
- Consider adding metrics/logging for backoff effectiveness: Track how often backoff prevents timeouts on subsequent attempts. This could help users tune their `timeoutBackoffIncrementMs` settings empirically.
- Consider exponential backoff option: Currently only linear backoff is supported. A future enhancement could add `timeoutBackoffType: "linear" | "exponential"` for different use cases.

## Positive Notes
- Clean separation of concerns with `calculate_effective_timeout()` delegating to the existing utility function
- Proper handling of edge cases: backoff disabled, zero base timeout, no cap (max_ms=0)
- Consistent integration in both `ralph_run()` and `ralph_start()` with identical backoff semantics
- Good backwards compatibility - default behavior unchanged when feature disabled
- Config resolution follows established patterns (env vars > config > defaults)
- Tests pass (34 utils tests, 11 ralph state tests)

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 2
- Warnings: 1
- Suggestions: 2
