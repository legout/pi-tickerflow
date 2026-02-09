# Implementation: pt-4qvw

## Summary
Implemented Ralph timeout + restart configuration surface as specified in the ticket. Added `attemptTimeoutMs` and `maxRestarts` configuration options with environment variable overrides.

## Files Changed
- `tf_cli/ralph.py` - Added:
  - New config defaults `attemptTimeoutMs` (600000ms = 10min) and `maxRestarts` (0)
  - Environment variable support: `RALPH_ATTEMPT_TIMEOUT_MS`, `RALPH_MAX_RESTARTS`
  - Updated `usage()` help text with configuration documentation
  - `resolve_attempt_timeout_ms()` and `resolve_max_restarts()` functions
  - Timeout support in `run_ticket()` with subprocess timeout handling
  - Restart loop logic in `ralph_run()` for timeout recovery

## Key Decisions
- **Conservative defaults**: 10 minute timeout (600000ms) and 0 restarts by default to avoid false positives
- **Environment variable priority**: Env vars override config file settings for these values
- **Timeout return code**: Used -1 to indicate timeout specifically, allowing restart logic to distinguish from regular failures
- **Restart only on timeout**: Non-timeout failures don't trigger restarts to avoid infinite loops on actual errors
- **Milliseconds for timeout**: Used milliseconds to match existing config conventions (sleepBetweenTickets, etc.)

## Configuration
Users can configure via:

1. **Config file** (`.tf/ralph/config.json`):
   ```json
   {
     "attemptTimeoutMs": 600000,
     "maxRestarts": 0
   }
   ```

2. **Environment variables**:
   ```bash
   export RALPH_ATTEMPT_TIMEOUT_MS=300000  # 5 minutes
   export RALPH_MAX_RESTARTS=2
   ```

## Tests Run
- `python -m pytest tests/ -v` - All 889 tests passed
- Syntax check passed: `python -m py_compile tf_cli/ralph.py`
- Help text verified: `python -m tf_cli ralph --help`

## Verification
The new settings appear in `tf ralph --help`:
```
Configuration (in .tf/ralph/config.json):
  attemptTimeoutMs      Per-ticket attempt timeout in milliseconds (default: 600000 = 10 min)
                        Set to 0 to disable timeout.
  maxRestarts           Maximum restarts per ticket on timeout/failure (default: 0)
                        Set to N to allow up to N restarts before marking as failed.

Configuration Environment Variables:
  RALPH_ATTEMPT_TIMEOUT_MS  Override attemptTimeoutMs (in milliseconds)
  RALPH_MAX_RESTARTS        Override maxRestarts (integer)
```
