# Implementation: pt-buwk

## Summary
Add a regression test that asserts the generated `pi` invocation for `tf ralph start/run` does not include `--session`.

## Context
This change is easy to regress because it's a small flag in a subprocess call. A test should lock in the desired command construction. The test is being added BEFORE the actual removal (pt-ihfv) to follow TDD principles.

## Files Changed
- `tests/test_ralph_pi_invocation.py` - New test file with smoke/regression tests for pi command construction

## Key Decisions
- Created a focused test file specifically for pi invocation args
- Tests use mocking to avoid requiring actual pi execution
- Tests cover both `ralph_run` and `ralph_start` code paths
- Tests verify the absence of `--session` in constructed arguments

## Tests Run
- `pytest tests/test_ralph_pi_invocation.py -v` - New tests added

## Verification
- Test will initially FAIL (expected since pt-ihfv hasn't removed `--session` yet)
- Once pt-ihfv is implemented, the test will PASS
