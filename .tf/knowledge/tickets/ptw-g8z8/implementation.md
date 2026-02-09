# Implementation: ptw-g8z8

## Summary
Added error handling for VERSION file read errors in the doctor command's `get_version_file_version()` function. Previously, the function silently returned None on any exception, which meant file permission errors or encoding issues would go unnoticed.

## Files Changed
- `tf_cli/doctor_new.py` - Updated `get_version_file_version()` to catch specific exceptions and print warnings:
  - `PermissionError` - warns when file exists but cannot be read due to permissions
  - `UnicodeDecodeError` - warns when file has encoding issues
  - `OSError` - warns on other OS-level read errors
  - Generic `Exception` - catch-all with warning for any other errors
- `tests/test_doctor_version.py` - Added tests for new error handling behavior

## Key Decisions
- Used specific exception types for better error messages and debugging
- Printed warnings to stdout using `[warn]` prefix for consistency with other doctor output
- Preserved backward compatibility by still returning None on errors (just with warnings now)

## Tests Run
- `pytest tests/test_doctor_version.py::TestGetVersionFileVersion -v` - 7/7 passed

## Verification
The function now properly warns users when:
1. VERSION file exists but has permission issues
2. VERSION file has encoding problems (not UTF-8)
3. Other OS-level errors prevent reading the file
