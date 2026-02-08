# Research: pt-hfqc - Add bounded restart loop for timed-out ticket attempts

## Ticket Summary
Implement bounded retry for a ticket when a timeout occurs in serial `tf ralph start` execution.

## Key Findings

### Current State
1. **Timeout mechanism exists**: `_run_with_timeout()` function handles subprocess timeout with safe termination (SIGTERM → SIGKILL)
2. **Config options exist**: `attemptTimeoutMs` (default: 600000ms = 10min) and `maxRestarts` (default: 0) are already in DEFAULTS
3. **Single-ticket restart loop exists**: `ralph_run()` has restart logic for `tf ralph run <ticket>`
4. **Serial mode in ralph_start lacks restarts**: The main loop in `ralph_start()` calls `run_ticket()` once without restart logic

### Code Locations

**`ralph.py` key sections:**
- Lines 316-355: `_run_with_timeout()` - handles timeout with safe process termination
- Lines 534-542: `resolve_attempt_timeout_ms()` - resolves timeout from env/config
- Lines 556-568: `resolve_max_restarts()` - resolves max restarts from env/config
- Lines 884-940: `ralph_run()` - single ticket with restart loop (reference implementation)
- Lines 1077-1088: Serial mode in `ralph_start()` - calls `run_ticket()` without restart loop

### Implementation Requirements

1. **Serial mode restart loop**: Wrap the `run_ticket()` call in a restart loop similar to `ralph_run()`
2. **Attempt tracking**: Track attempt number, log clear messages with attempt count
3. **Timeout detection**: `run_ticket()` returns `-1` on timeout (already implemented)
4. **Max restarts enforcement**: Use `resolve_max_restarts(config)` to get limit
5. **Failure on max reached**: After `max_restarts` attempts, mark ticket FAILED with actionable message
6. **Parallel mode**: Should remain functional (per constraints, may warn if restarts attempted)

### Testing Considerations
- Ticket pt-c2b0 is the dependent ticket for adding tests
- Current tests in `tests/test_ralph_logging.py` may need updates for new log patterns

## Acceptance Criteria Mapping

| Criterion | Implementation Location | Notes |
|-----------|------------------------|-------|
| Timeout triggers retry | Serial mode loop in `ralph_start()` | Check `rc == -1` |
| Bounded by `maxRestarts` | Use `resolve_max_restarts()` + attempt counter | Already implemented in `ralph_run()` |
| Clear logging | Use `ticket_logger` with context | Include attempt number, timeout threshold |
| Actionable failure message | On max restarts exceeded | Log ticket FAILED with timeout details |
