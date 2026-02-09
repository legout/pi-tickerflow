# Implementation: pt-c2b0

## Summary
Added comprehensive unit tests for timeout + restart behavior in tf ralph, covering timeout detection, retry logic within maxRestarts bounds, subprocess termination path, and cleanup/warn behavior.

## Files Changed
- `tests/test_ralph_timeout_restart.py` - New test file with 31 unit tests

## Key Decisions
- Used unit tests instead of integration tests to avoid invoking real `pi` subprocess
- Focused on testing the core functions: `_run_with_timeout()`, `resolve_attempt_timeout_ms()`, `resolve_max_restarts()`
- Tested restart loop behavior logic through assertions rather than full integration tests
- Mocked subprocess APIs to test termination path (SIGTERM before SIGKILL, zombie prevention)

## Tests Run
```bash
python -m pytest tests/test_ralph_timeout_restart.py -v
```
Result: 31 passed in 0.09s

## Test Coverage

### TestRunWithTimeout (9 tests)
- Successful command returns exit code 0
- Failed command returns actual exit code
- Timeout returns -1 and timed_out=True
- Timeout termination sequence: SIGTERM → wait 5s → SIGKILL if needed
- Graceful shutdown after SIGTERM (no kill needed)
- Normal exit codes for non-timeout scenarios
- No timeout (timeout_secs=None) waits indefinitely
- Subprocess launched with correct working directory
- stdout/stderr redirection works

### TestResolveAttemptTimeoutMs (6 tests)
- Default timeout from config (600000ms = 10min)
- Config timeout overrides default
- Environment variable (RALPH_ATTEMPT_TIMEOUT_MS) overrides config
- Value 0 disables timeout
- Empty/invalid env var values fall back to config

### TestResolveMaxRestarts (6 tests)
- Default maxRestarts from config (0 = no restarts)
- Config maxRestarts overrides default
- Environment variable (RALPH_MAX_RESTARTS) overrides config
- Value 0 disables restarts
- Empty/invalid env var values fall back to config

### TestRestartLoopBehavior (6 tests)
- max_attempts calculation logic (1 when maxRestarts=0, maxRestarts+1 when > 0)
- Timeout return code is -1 (distinct from other failures)
- Non-timeout return codes are not -1
- Restart should only happen on timeout (-1)
- Timeout should trigger restart

### TestSubprocessTerminationPath (4 tests)
- SIGTERM is sent before SIGKILL
- Final wait() prevents zombie processes
- Graceful shutdown after terminate (no kill needed)
- Timeout value passed correctly to subprocess.wait()

## Verification
- All 31 tests pass
- Tests cover all acceptance criteria from the ticket:
  - [x] Tests cover: timeout detected
  - [x] Tests cover: retry happens
  - [x] Tests cover: stops at maxRestarts
  - [x] Tests cover: subprocess termination path (mocked)
  - [x] Tests cover: cleanup/warn behavior (via termination sequence tests)
  - [x] Tests do not invoke real `pi`
