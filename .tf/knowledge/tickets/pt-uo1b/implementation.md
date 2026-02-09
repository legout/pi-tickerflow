# Implementation: pt-uo1b

## Summary
Added explicit CI smoke tests for headless import of `tf_cli.ui` module. The tests verify that the module can be imported without errors in non-TTY environments (CI, web-served contexts).

## Files Changed
- `tests/test_ui_smoke.py` - Added `TestUiHeadlessImport` class with 2 tests:
  - `test_ui_module_imports_without_error` - Basic import verification
  - `test_ui_module_imports_in_non_tty_context` - Import in mocked headless environment

## Key Decisions
- Added a dedicated test class `TestUiHeadlessImport` to make the CI smoke test explicit and discoverable
- The tests mock `sys.stdin` and `sys.stdout` to simulate non-TTY environments
- Tests force module re-import to verify import-time behavior in headless context
- No new dependencies added - uses existing `unittest.mock` and `pytest`

## Tests Run
```bash
$ python -m pytest tests/test_ui_smoke.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0
...
tests/test_ui_smoke.py::TestUiHeadlessImport::test_ui_module_imports_without_error PASSED
tests/test_ui_smoke.py::TestUiHeadlessImport::test_ui_module_imports_in_non_tty_context PASSED
...
============================== 16 passed in 0.09s ==============================
```

## Verification
- Verified `import tf_cli.ui` succeeds in non-TTY context
- Verified tests run in existing CI test suite (pytest)
- No additional dependencies required

## Acceptance Criteria
- [x] Add a test that imports `tf_cli.ui` without raising
- [x] Test runs in existing CI test suite
- [x] No additional heavy dependencies added
