# Implementation: pt-hfqc - Add bounded restart loop for timed-out ticket attempts

## Summary
Implemented bounded retry logic for ticket attempts when timeouts occur in serial `tf ralph start` execution. The implementation adds a restart loop around the `run_ticket()` call in serial mode, tracking attempt numbers and enforcing the `max_restarts` limit.

## Files Changed

### `tf_cli/ralph.py`
**Changes in `ralph_start()` function (serial mode section):**

1. **Added timeout/restart config resolution** (lines ~1393-1394):
   - Calls `resolve_attempt_timeout_ms(config)` to get timeout setting
   - Calls `resolve_max_restarts(config)` to get max restarts setting

2. **Added bounded restart loop** (lines ~1423-1474):
   - Wraps `run_ticket()` call in a while loop tracking attempt numbers
   - Attempt counter starts at 1, max is `max_restarts + 1`
   - Logs restart attempts with attempt number and timeout threshold
   - Passes `timeout_ms` to `run_ticket()` (was missing before)

3. **Timeout detection and handling**:
   - Checks for `rc == -1` (timeout return code from `run_ticket()`)
   - If timeout and attempts remain, logs warning and continues loop
   - If timeout and max attempts reached, logs error with actionable message

4. **Non-timeout failures**:
   - Non-timeout failures (rc != 0, rc != -1) exit restart loop immediately
   - This matches the expected behavior from the constraints

5. **Failure messaging**:
   - Timeout failures: "Ticket failed after {attempt} attempt(s) due to timeout (threshold: {timeout_ms}ms)"
   - Regular failures: "pi -p failed (exit {rc})"

## Key Decisions

1. **Attempt counting**: Uses 1-based counting for user-facing messages ("attempt 1 of 3")
2. **Dry-run behavior**: Only one attempt in dry-run mode (no restarts)
3. **Progress display**: Updates happen after the restart loop completes (not per-attempt)
4. **State updates**: Only called after the restart loop completes (success or final failure)

## Behavior

### With max_restarts=0 (default)
- Ticket runs once
- On timeout: immediately marked FAILED with timeout message

### With max_restarts=2
- Ticket runs up to 3 times (initial + 2 restarts)
- On timeout: logs warning, retries if attempts remain
- After 3 timeouts: marked FAILED with actionable timeout message

### Timeout logging
```
# First attempt
[INFO] ticket=abc-123 status=start
# ... timeout occurs
[WARN] Attempt 1 timed out after 600000ms, retrying...
[INFO] Restart attempt 1/2 for ticket (timeout: 600000ms)
[INFO] ticket=abc-123 status=start
# ... timeout occurs again
[WARN] Attempt 2 timed out after 600000ms, retrying...
[INFO] Restart attempt 2/2 for ticket (timeout: 600000ms)
[INFO] ticket=abc-123 status=start
# ... timeout occurs third time
[ERROR] Ticket timed out after 3 attempt(s) (timeout: 600000ms)
[ERROR] ticket=abc-123 status=failed error="Ticket failed after 3 attempt(s) due to timeout (threshold: 600000ms)"
```

## Tests Run
- `tests/test_ralph_logging.py` - 47 tests passed
- Syntax validation passed

## Verification
The implementation meets all acceptance criteria:
- [x] Timeout triggers a retry of the same ticket attempt (no advancing to next ticket)
- [x] Retry is bounded by `maxRestarts` and then marks ticket FAILED with actionable message
- [x] Logs clearly include attempt number and timeout threshold
