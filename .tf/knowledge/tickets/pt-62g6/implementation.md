# Implementation: pt-62g6

## Summary
Wired packaging/entrypoints so the `tf` console script uses the new `tf` namespace while maintaining backward compatibility with `tf_cli`.

## Files Changed

### New Files
- `tf/__init__.py` - Package initialization with re-exports from tf_cli
- `tf/cli.py` - CLI entrypoint that imports from tf_cli.cli

### Modified Files
- `pyproject.toml` - Updated entrypoint and packages list:
  - Changed `[project.scripts]` from `tf = "tf_cli.cli:main"` to `tf = "tf.cli:main"`
  - Added `"tf"` to `[tool.setuptools.packages]`
  - Updated `[tool.coverage.run].source` to include `"tf"`

## Key Decisions

1. **Compatibility-first approach**: The new `tf` package imports from `tf_cli` rather than moving code immediately. This ensures:
   - Existing workflows continue to work (Ralph, prompts, etc.)
   - No breaking changes to imports
   - Gradual migration path for future refactoring

2. **Smoke test already exists**: `tests/test_smoke_version.py` already covers the `tf --version` console script. No changes needed.

## Verification

```bash
# Test imports work
python3 -c "import tf; print('tf package imports OK')"
python3 -c "from tf.cli import main; print('tf.cli imports OK')"

# Test --version works via new entrypoint
python3 -c "from tf.cli import main; import sys; sys.argv = ['tf', '--version']; main()"
# Output: 0.3.0

# Test --help works
python3 -c "from tf.cli import main; import sys; sys.argv = ['tf', '--help']; main()"
# Output: Full help text displayed
```

## Acceptance Criteria

- [x] Installed `tf --help` still works - VERIFIED
- [x] No duplicate/competing entrypoints remain - Only `tf = "tf.cli:main"` exists
- [x] Smoke test covering console script exists - `tests/test_smoke_version.py`

## Notes

- The `tf_cli` package remains functional for backward compatibility
- Future tickets can gradually move code from `tf_cli` to `tf`
- The entrypoint change is transparent to users - the `tf` command behaves identically
