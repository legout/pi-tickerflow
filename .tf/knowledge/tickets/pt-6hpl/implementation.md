# Implementation: pt-6hpl

## Summary
Added `datastar-py` dependency to Ticketflow and pinned to a compatible version with Datastar JS v1.0.0-RC.7.

## Files Changed
- `pyproject.toml` - Added `datastar-py>=0.7.0,<0.8.0` to dependencies with rationale comment
- `tf_cli/web_ui.py` - Added module docstring note explaining the version pin rationale

## Key Decisions
1. **Version 0.7.0 selected**: While 0.8.0 is the latest, it requires Python >=3.10. Ticketflow supports >=3.9, so 0.7.0 was chosen as the latest compatible version.
2. **Upper bound <0.8.0**: Prevents accidental upgrade to 0.8.0 which would break Python 3.9 compatibility.
3. **Compatibility verified**: Both 0.7.0 and 0.8.0 are compatible with Datastar JS v1.0.0-RC.7 per PyPI documentation examples.

## Version Rationale Note
Added to both pyproject.toml comment and web_ui.py docstring:
- datastar-py provides SSE response helpers for Sanic
- Pinned to match Datastar JS v1.0.0-RC.7 (loaded from CDN in templates)
- 0.7.0 chosen for Python 3.9 compatibility

## Tests Run
- Import check: `python -c "import datastar_py"` ✓
- Package installed via uv: `uv add "datastar-py>=0.7.0,<0.8.0"` ✓

## Verification
1. Run `python -c "import datastar_py"` - should succeed without error
2. Check `pyproject.toml` shows `datastar-py>=0.7.0,<0.8.0` in dependencies
3. Check `tf_cli/web_ui.py` module docstring explains the version pin
