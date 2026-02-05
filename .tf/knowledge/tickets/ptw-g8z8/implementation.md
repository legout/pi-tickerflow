# Implementation: ptw-g8z8

## Summary
Added error handling for VERSION file read errors in the doctor command's `get_version_file_version()` function. Previously, the function silently returned `None` on any exception, hiding file permission errors or encoding issues.

## Files Changed
- `tf_cli/doctor_new.py` - Updated `get_version_file_version()` to print warnings for specific error types
- `tests/test_doctor_version.py` - Added tests for warning behavior on PermissionError and UnicodeDecodeError

## Changes Made

### tf_cli/doctor_new.py
Modified `get_version_file_version()` to catch specific exceptions and print warnings:

- **PermissionError**: Prints `[warn] VERSION file exists but cannot be read: {message}`
- **UnicodeDecodeError**: Prints `[warn] VERSION file has encoding issues: {message}`
- **OSError**: Prints `[warn] VERSION file exists but cannot be read: {message}`
- **Generic Exception**: Prints `[warn] VERSION file exists but cannot be read: {message}`

The function still returns `None` on all error conditions (maintaining backward compatibility), but now users are informed when the VERSION file exists but can't be read due to permissions or encoding issues.

### tests/test_doctor_version.py
Added two new test cases:

1. `test_prints_warning_on_permission_error` - Verifies warning is printed when file cannot be read due to permissions
2. `test_prints_warning_on_encoding_error` - Verifies warning is printed when file has encoding issues

## Test Results
All 40 tests pass:
- 8 tests for `get_package_version`
- 7 tests for `get_version_file_version` (including 2 new warning tests)
- 9 tests for `normalize_version`
- 7 tests for `sync_version_file`
- 9 tests for `check_version_consistency`

## Verification
```bash
uv run python -m pytest tests/test_doctor_version.py -v
```
