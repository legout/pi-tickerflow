# Research: pt-c2b0

## Status
Research enabled. Minimal research performed.

## Rationale
This ticket is about adding unit tests for the timeout + restart behavior that was recently added to `tf ralph`. The functionality is already implemented in `tf_cli/ralph.py` and needs test coverage.

## Context Reviewed
- `tk show pt-c2b0` - Ticket requirements
- `tf_cli/ralph.py` - Implementation of timeout and restart logic
  - `_run_with_timeout()` function (lines ~275-330)
  - `resolve_attempt_timeout_ms()` and `resolve_max_restarts()` functions (lines ~572-621)
  - Serial mode restart loop (lines ~1435-1480)
  - `run_ticket()` function (lines ~342-455)
- `tests/test_ralph_logging.py` - Existing test patterns for ralph functionality

## Key Implementation Details

### Timeout Detection
- `_run_with_timeout()` returns a tuple `(return_code, timed_out)`
- On timeout, returns `(-1, True)` to signal timeout to caller
- Timeout occurs when `subprocess.wait()` raises `TimeoutExpired`

### Restart Logic (Serial Mode)
- Configured via `attemptTimeoutMs` (default: 600000ms = 10min) and `maxRestarts` (default: 0)
- Environment variables: `RALPH_ATTEMPT_TIMEOUT_MS` and `RALPH_MAX_RESTARTS`
- Restart loop only happens for timeout failures (return code -1)
- Non-timeout failures (other exit codes) do not trigger restarts
- Max attempts = `maxRestarts + 1` if `maxRestarts > 0`, else 1

### Subprocess Termination Path
1. Try graceful termination (SIGTERM)
2. Wait 5 seconds for graceful shutdown
3. Force kill (SIGKILL) if still running
4. Reap process with final `wait()` to prevent zombies

### Logging Behavior
- `ticket_logger.warn()` for timeout restart warnings
- `ticket_logger.error()` when max restarts exceeded
- Logs include attempt count and timeout duration

## Sources
- `tf_cli/ralph.py` - Implementation code
- `tests/test_ralph_logging.py` - Existing test patterns
