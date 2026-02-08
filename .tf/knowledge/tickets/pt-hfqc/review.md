# Review: pt-hfqc

## Overall Assessment
The implementation correctly adds bounded restart logic for serial mode in `tf ralph start`. The code structure follows existing patterns from `ralph_run()`, properly handles timeout detection (rc == -1), and provides clear logging with attempt numbers and timeout thresholds.

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
No issues found.

## Warnings (follow-up ticket)
- `tf_cli/ralph.py:1600+` - Parallel mode does not implement timeout/restart logic. Consider adding a warning log when `max_restarts > 0` is configured but parallel mode is active, informing users that restarts are only supported in serial mode.

## Suggestions (follow-up ticket)
- `tf_cli/ralph.py` - Consider adding exponential backoff between restart attempts to avoid hammering resources immediately after timeout. This would require a new config option like `restartBackoffMs`.

## Positive Notes
- Clean integration with existing `resolve_attempt_timeout_ms()` and `resolve_max_restarts()` functions
- Proper 1-based attempt counting for user-facing messages
- Correct handling of dry-run mode (single attempt only)
- Timeout threshold is now passed to `run_ticket()` in serial mode (was missing before)
- Clear, actionable error messages when max restarts exceeded: "Ticket failed after N attempt(s) due to timeout (threshold: Xms)"
- Non-timeout failures correctly exit the restart loop immediately without unnecessary retries
- All existing tests pass (47/47 in test_ralph_logging.py)

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 0
- Warnings: 1
- Suggestions: 1

## Spec Coverage
- Spec sources consulted: Ticket pt-hfqc, seed-add-ralph-loop-timeout-restarts topic, ralph.py existing patterns
- Requirements verified:
  - [x] Timeout triggers retry of same ticket attempt
  - [x] Retry bounded by maxRestarts
  - [x] Actionable failure message on max exceeded
  - [x] Logs include attempt number and timeout threshold
