# Implementation: pt-ut88

## Summary
Add comprehensive unit tests for `tf ralph` sessionDir resolution and legacy warning behavior. The tests cover the `resolve_session_dir()` function in `tf_cli/ralph.py`.

## Files Changed
- `tests/test_ralph_session_dir.py` - New test file covering sessionDir resolution

## Test Coverage

### 1. Default Path Selection
- `test_default_session_dir_is_pi_standard` - Verifies default is `~/.pi/agent/sessions`
- `test_default_path_expands_tilde` - Verifies tilde expansion works correctly
- `test_default_path_creates_directory` - Verifies directory is created if it doesn't exist

### 2. Config Override Semantics
- `test_config_override_absolute_path` - Absolute paths in config are used as-is
- `test_config_override_relative_path` - Relative paths are resolved relative to project root
- `test_config_override_with_tilde` - Tilde expansion in config paths
- `test_config_disabled_with_empty_string` - Empty string disables sessions
- `test_config_disabled_with_false` - Boolean false disables sessions
- `test_config_disabled_with_none` - Null value disables sessions

### 3. Legacy Detection and Warning
- `test_legacy_warning_emitted_when_legacy_exists` - Warning shown when legacy dir exists
- `test_legacy_warning_not_emitted_when_user_explicitly_sets_sessiondir` - No warning if user configured sessionDir
- `test_legacy_warning_emitted_only_once` - Warn-once behavior (global flag)
- `test_legacy_warning_not_emitted_when_legacy_empty` - No warning if legacy dir is empty
- `test_legacy_warning_not_emitted_when_no_legacy` - No warning if legacy dir doesn't exist
- `test_force_legacy_env_var_uses_legacy_path` - RALPH_FORCE_LEGACY_SESSIONS forces legacy path

## Key Implementation Details

The tests use:
- `tmp_path` fixture for isolated test directories
- `unittest.mock` for mocking logger and environment variables
- Module-level cache reset to ensure warn-once tests are isolated
- Direct function testing (no actual Pi invocation)

## Tests Run
```bash
pytest tests/test_ralph_session_dir.py -v
```

## Verification
All tests pass with the current implementation of `resolve_session_dir()` in `tf_cli/ralph.py`.
