# Fixes: abc-123

## Summary
Fixed 1 Major issue and 2 Minor issues identified in code review.

## Issues Fixed

### Major (1)
- `demo/hello.py` - **Type hint consistency**: Kept `name: str` type hint and removed unreachable None check. The type signature correctly indicates only string input is accepted, and the `.strip()` check handles empty/whitespace strings appropriately.

### Minor (2)
- `tests/test_demo_hello.py` - **Added missing CLI tests**: Added `test_cli_default` and `test_cli_with_name` to test the `demo/__main__.py` entry point directly.
- `tests/test_demo_hello.py` - **Expanded whitespace coverage**: Added `test_hello_whitespace_various` to test tabs (`\t`) and newlines (`\n`) in addition to spaces.

## Changes Made
1. `demo/hello.py` - Simplified logic to return early for empty/whitespace strings
2. `tests/test_demo_hello.py` - Added imports for `sys`, `patch`, and `main`; added 3 new test functions

## Test Results
```
7 passed in 0.07s
- test_hello_default
- test_hello_custom_name
- test_hello_empty_string
- test_hello_whitespace_only
- test_hello_whitespace_various (NEW)
- test_cli_default (NEW)
- test_cli_with_name (NEW)
```

## Remaining Issues
- Minor: `demo/__init__.py` - `__version__` not added (cosmetic, skipped)
- Warning: CLI integration tests via subprocess (deferred)
- Suggestions: Parametrized tests, docstring updates, type modernization (deferred)
