# Implementation: pt-cj59

## Summary
Changed `tf ralph` default session directory from `.tf/ralph/sessions` to Pi's standard session directory (`~/.pi/agent/sessions`).

## Files Changed
- `tf_cli/ralph.py` - Updated `DEFAULTS["sessionDir"]` from `.tf/ralph/sessions` to `~/.pi/agent/sessions`

## Key Decisions
- Used `~/.pi/agent/sessions` as the new default to align with Pi's standard session storage location
- The existing `resolve_session_dir()` function already handles both absolute and relative paths correctly:
  - Absolute paths (like the new default) are used as-is
  - Relative paths from existing configs are still resolved relative to project root (backward compatibility)
- No changes needed to `resolve_session_dir()` since it already handles the logic correctly

## Backward Compatibility
- Existing configs that explicitly set `sessionDir` will continue to work
- Custom relative paths are still resolved relative to project root
- Only the default changes when no `sessionDir` is configured

## Tests Run
- `python -m pytest tests/test_pi_output.py -v` - 34 passed
- `python -m pytest tests/ -k "ralph" -v` - 65 passed

## Verification
The change ensures that:
1. New installations use Pi's standard session directory
2. Existing configs with custom `sessionDir` continue to work
3. Per-ticket session files continue to be created as before
