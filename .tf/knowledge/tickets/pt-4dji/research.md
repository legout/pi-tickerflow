# Research: pt-4dji

## Task Summary
Update `tf ralph --help` and relevant docs to reflect the new default session location and overrides.

## Current Implementation Analysis

### Session Directory Resolution (tf_cli/ralph.py)

**Default Location:**
- Code: `DEFAULTS["sessionDir"] = "~/.pi/agent/sessions"` (line 96)
- This is Pi's standard session directory

**Legacy Location:**
- Code: `LEGACY_SESSION_DIR = ".tf/ralph/sessions"` (line 111)
- Still detected for backward compatibility

**Resolution Logic (resolve_session_dir function, lines 633-694):**
1. Check if user explicitly set `sessionDir` in config
2. Check if legacy `.tf/ralph/sessions` exists
3. If legacy exists and user hasn't explicitly configured, emit warning
4. Use user's config value, or default to `~/.pi/agent/sessions`

**Override Mechanisms:**
1. **Config file**: `.tf/ralph/config.json` → `sessionDir` key
2. **Environment variable**: `RALPH_FORCE_LEGACY_SESSIONS=1` forces legacy location

### Current Help Text (tf_cli/ralph.py lines 117-168)

Already documents:
- `RALPH_FORCE_LEGACY_SESSIONS` environment variable

Missing:
- Default Pi session directory path (`~/.pi/agent/sessions`)
- Config override via `sessionDir` in `.tf/ralph/config.json`
- Clear explanation of legacy detection behavior

### Current Documentation

**docs/ralph.md:**
- Still shows `"sessionDir": ".tf/ralph/sessions"` as default (line 83)
- Needs update to reflect new default location

**docs/configuration.md:**
- Ralph section doesn't mention sessionDir at all (lines 264-285)
- Should document the config option and environment variable

## Files to Update

1. **tf_cli/ralph.py** - Update `usage()` function help text
2. **docs/ralph.md** - Update configuration table and example
3. **docs/configuration.md** - Add sessionDir to Ralph config section

## Acceptance Criteria Mapping

| Criterion | Implementation Location |
|-----------|------------------------|
| Help text documents default Pi session dir path | tf_cli/ralph.py usage() |
| Help text documents override knobs (config + env var) | tf_cli/ralph.py usage() |
| Mention legacy `.tf/ralph/sessions` behavior and warning | tf_cli/ralph.py usage() |
| Update docs/ralph.md | Configuration table |
| Update docs/configuration.md | Ralph config section |
