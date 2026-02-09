# Review: pt-buwk

## Critical (must fix)
- None

## Major (should fix)
- None

## Minor (nice to fix)
- None

## Warnings (follow-up ticket)
- None

## Suggestions (follow-up ticket)
- Consider adding a test that verifies the behavior when `sessionPerTicket=false` (loop-level sessions)
- Could add a parallel mode test to verify `--session` is not passed in parallel execution paths

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 0
- Warnings: 0
- Suggestions: 2

## Review Notes
Test file created successfully with 3 test cases:
1. `test_ralph_run_pi_invocation_no_session_with_session_dir` - Verifies `ralph run` doesn't include `--session`
2. `test_ralph_start_pi_invocation_no_session_with_session_dir` - Verifies `ralph start` doesn't include `--session`
3. `test_pi_command_starts_with_pi_dash_p` - Verifies basic command structure

The first test currently FAILS as expected (the code still adds `--session`). This is correct behavior for a regression test written before the fix (pt-ihfv).

The tests properly mock subprocess calls to avoid requiring actual pi execution, meeting the acceptance criteria of being stable and not requiring Pi to run.
