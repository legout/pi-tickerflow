# Review (Spec Audit): pt-hfqc

## Overall Assessment
The implementation successfully meets all acceptance criteria for the bounded restart loop feature in serial mode. The restart logic properly tracks attempt numbers, enforces the max_restarts limit, and provides clear logging with timeout thresholds. The parallel mode constraint is satisfied (remains functional), though it lacks explicit warning when restarts are attempted in parallel.

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf_cli/ralph.py:~1543` - Parallel mode does not implement timeout restart logic. While the constraint states "MVP applies to serial mode; parallel behavior must remain functional (may disable retries with a warning)", there's no warning logged when `max_restarts > 0` and `use_parallel > 1`. Consider adding a warning log when parallel mode is used with max_restarts > 0 to inform users that restarts are disabled in parallel mode.

## Warnings (follow-up ticket)
- `tf_cli/ralph.py` - No tests for the new timeout restart logic in serial mode. Ticket pt-c2b0 is already in the backlog for adding these tests, but this is a gap that should be addressed before the feature is considered production-ready.

## Suggestions (follow-up ticket)
- `tf_cli/ralph.py:1423-1474` - Consider adding a small delay between restart attempts (e.g., exponential backoff) to avoid hammering a potentially stuck system immediately. This is mentioned as "out of scope for MVP" in the success metrics document, but could improve robustness in production.
- `tf_cli/ralph.py` - Consider persisting the attempt count to the ticket state so that Ralph can resume retries after a crash/restart rather than starting over from attempt 1.

## Positive Notes
- The bounded restart loop correctly implements 1-based attempt counting with clear user-facing messages
- Timeout detection via `rc == -1` is properly implemented per the spec
- The `max_restarts` enforcement correctly calculates `max_attempts = max_restarts + 1` (initial attempt + restarts)
- Dry-run mode correctly skips restarts (only one attempt)
- Non-timeout failures exit the restart loop immediately, matching the expected behavior
- Logging includes both attempt number and timeout threshold as required
- The failure message "Ticket failed after {attempt} attempt(s) due to timeout (threshold: {timeout_ms}ms)" is actionable and clear
- The implementation follows the same pattern as the existing `ralph_run()` function for consistency

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 1
- Suggestions: 2

## Spec Coverage
- Spec/plan sources consulted:
  - Ticket pt-hfqc (requirements)
  - `.tf/knowledge/topics/seed-add-ralph-loop-timeout-restarts/mvp-scope.md`
  - `.tf/knowledge/topics/seed-add-ralph-loop-timeout-restarts/constraints.md`
  - `.tf/knowledge/topics/seed-add-ralph-loop-timeout-restarts/backlog.md`
  - `.tf/knowledge/topics/seed-add-ralph-loop-timeout-restarts/success-metrics.md`
  - `.tf/knowledge/topics/seed-add-ralph-loop-timeout-restarts/seed.md`
  - Ticket pt-hstd implementation (timeout mechanism dependency)
  - Ticket pt-4qvw implementation (config surface dependency)
- Missing specs: none
