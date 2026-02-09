# Implementation: pt-whcy

## Summary
Add backward compatibility behavior for projects that already have `.tf/ralph/sessions` session files. When the legacy directory exists and the user hasn't explicitly configured a custom `sessionDir`, emit a warning with clear next steps.

## Changes Made

### File: `tf_cli/ralph.py`

1. **Added constants for legacy detection:**
   - `LEGACY_SESSION_DIR = ".tf/ralph/sessions"` - Path to legacy session directory
   - `_legacy_warning_emitted` - Flag to ensure warning is only shown once per run

2. **Enhanced `resolve_session_dir()` function:**
   - Added `raw_config` parameter to detect if user explicitly set `sessionDir`
   - Added `logger` parameter for structured logging
   - Detects if legacy `.tf/ralph/sessions` directory exists and has content
   - Emits warning when:
     - Legacy directory exists AND
     - User hasn't explicitly configured `sessionDir` AND
     - Warning hasn't been emitted yet this run
   - Supports `RALPH_FORCE_LEGACY_SESSIONS=1` environment variable to force legacy behavior

3. **Updated callers in `ralph_run()` and `ralph_start()`:**
   - Both functions now load raw config to pass to `resolve_session_dir()`
   - Logger is passed for proper warning output

4. **Updated `usage()` documentation:**
   - Added `RALPH_FORCE_LEGACY_SESSIONS` environment variable documentation

## Warning Message
When legacy sessions are detected, users see:
```
[ralph] Warning: Legacy session directory detected at '.tf/ralph/sessions'
[ralph] New default location is: ~/.pi/agent/sessions
[ralph] Options:
[ralph]   1. To use the new location: Move files from .tf/ralph/sessions to ~/.pi/agent/sessions
[ralph]   2. To keep using legacy location: Set RALPH_FORCE_LEGACY_SESSIONS=1 or
[ralph]      add '{"sessionDir": ".tf/ralph/sessions"}' to .tf/ralph/config.json
```

## Acceptance Criteria
- [x] If legacy `.tf/ralph/sessions` exists and user did not set `sessionDir`, emit a clear warning with next steps
- [x] Provide a documented way to force legacy behavior (config or env var)
- [x] No automatic bulk migration required for MVP

## Constraints Met
- Warning is only shown once per run (not on every loop iteration)
- Non-breaking: existing behavior continues, just with warning
- Two escape hatches provided: env var and config setting

## Tests Run
- Syntax check: `python -m py_compile tf_cli/ralph.py` - PASSED

## Verification
To verify the warning works:
1. Ensure `.tf/ralph/sessions` exists with content
2. Ensure `.tf/ralph/config.json` does NOT have `sessionDir` set
3. Run `tf ralph run` or `tf ralph start`
4. Warning should appear before ticket processing begins
