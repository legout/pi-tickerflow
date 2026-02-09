# Review: pt-4qvw

## Critical (must fix)
- None

## Major (should fix)
- None

## Minor (nice to fix)
- **Missing timeout in parallel mode**: The timeout/restart logic was only added to `ralph_run()` (serial mode). The parallel mode in `ralph_start()` uses subprocess.Popen without timeout handling. Consider documenting this limitation or implementing parallel mode timeout in a follow-up ticket.

## Warnings (follow-up ticket)
- Consider adding tests specifically for the timeout and restart functionality to ensure they work as expected under various edge cases (timeout=0, max_restarts=0, timeout expiration, etc.)

## Suggestions (follow-up ticket)
- Add a `--timeout` CLI flag to `tf ralph run` for per-run override, similar to other tools
- Consider logging the timeout value at DEBUG level in run_ticket even when not timing out, for debugging purposes

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 1
- Suggestions: 2

## Review Notes
The implementation correctly addresses all acceptance criteria:
1. ✅ Config keys defined (`attemptTimeoutMs` and `maxRestarts`) in DEFAULTS
2. ✅ Environment variable overrides supported and documented (RALPH_ATTEMPT_TIMEOUT_MS, RALPH_MAX_RESTARTS)
3. ✅ `tf ralph --help` mentions the new settings and their defaults

The code is well-structured, follows existing patterns, and all 889 existing tests pass.
