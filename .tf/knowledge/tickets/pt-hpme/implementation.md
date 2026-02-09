# Implementation: pt-hpme

## Summary
Implemented tf_cli compatibility shims with opt-in deprecation warnings. The tf package is now canonical for the CLI dispatcher, and tf_cli is a compatibility shim with optional deprecation warnings.

## Files Changed

### tf/__init__.py
- Made canonical with local version reading (no import from tf_cli)
- Defines `__version__`, `get_version()`
- Note: ticket_factory exports will be added in pt-tupn when modules migrate

### tf/cli.py
- Full CLI dispatcher implementation moved from tf_cli/cli.py
- Entry point for `tf` console script (`tf = "tf.cli:main"` in pyproject.toml)
- Imports command handlers from tf_cli modules (to be migrated in pt-tupn)

### tf/__main__.py
- Unchanged (already imported from tf.cli)

### tf_cli/__init__.py
- Shim with optional deprecation warning
- Re-exports from tf_cli modules (implementation still there during transition)
- Warning only emits when `TF_CLI_DEPRECATION_WARN=1`

### tf_cli/cli.py
- Shim re-exporting from `tf.cli` with optional deprecation warning
- Maintains backward compat with `can_import_tf_cli` alias

### tf_cli/__main__.py
- New file enabling `python -m tf_cli`
- Shim with deprecation warning, delegates to tf.cli

## Key Decisions

1. **Warning Policy**: Opt-in via `TF_CLI_DEPRECATION_WARN=1` as per pt-mu0s decision
2. **No duplicated logic**: All shims are thin re-exports
3. **Circular import avoidance**: tf/__init__.py doesn't import from tf_cli to avoid cycles
4. **Backward compatibility**: `can_import_tf_cli` alias preserved in tf_cli/cli.py
5. **Module execution**: Both `python -m tf` and `python -m tf_cli` work

## Acceptance Criteria Status

- [x] `import tf_cli` and key `tf_cli.*` imports still work
- [x] Shims are thin (no duplicated logic)
- [x] Deprecation warning policy matches strategy (opt-in, default off)
- [x] No warning spam in default test runs

## Verification

```bash
# Test tf works
python -m tf --version  # 0.3.0
python -m tf --help

# Test tf_cli shim works
python -m tf_cli --version  # 0.3.0
python -c "import tf_cli; print(tf_cli.__version__)"

# Test deprecation warnings (opt-in)
TF_CLI_DEPRECATION_WARN=1 python -c "import tf_cli" 2>&1
# Shows: DeprecationWarning: tf_cli is deprecated...

# Test without warnings (default)
python -c "import tf_cli"  # No warning
```

## Post-Review Fixes

After review, the following critical and major issues were addressed:

### Critical
1. **Version reading logic**: Replaced simple `_read_version()` with full implementation matching original `tf_cli/version.py`, including repo root resolution, git tag fallback, and multiple search paths.
2. **Fallback version**: Changed from `"0.0.0-dev"` to `"unknown"` for consistency.

### Major
3. **Warning messages**: Updated all deprecation warnings to use full GitHub URL instead of local path reference.
4. **Docstrings**: Updated to explicitly state compatibility through 0.4.x and removal in 0.5.0.
5. **Public API**: Removed internal function re-exports from `tf_cli/cli.py` (now only exports `main`, `can_import_tf`, `can_import_tf_cli`).

### Minor
6. **Exception handling**: Changed from broad `except Exception` to specific `OSError` catching.

See `fixes.md` for complete details.

## Notes on Migration Path

The full migration plan is:
1. **pt-hpme (this ticket)**: Create tf/ canonical package and tf_cli/ shim ✓
2. **pt-tupn**: Move CLI modules from tf_cli/ to tf/
3. **pt-m06z**: Update tests to use tf namespace + add shim tests
4. **pt-7li0**: Update docs
5. **0.5.0**: Remove tf_cli/ shim

Currently tf/cli.py imports command handlers from tf_cli modules. In pt-tupn, these will be moved to tf/ and tf_cli/cli.py will simply re-export from tf.cli.
