# Review (Second Opinion): pt-uo1b

## Overall Assessment
The implementation adds appropriate CI smoke tests for headless import of the `tf_cli.ui` module. The tests are well-structured, follow existing conventions, and correctly verify the module can be imported without errors. However, there are some edge cases in the module re-import logic that could lead to false positives in certain scenarios.

## Critical (must fix)
No critical issues found.

## Major (should fix)
- `tests/test_ui_smoke.py:178-181` - The module cache deletion only removes `tf_cli.ui` but not its submodules. If `tf_cli.ui` imports submodules (like `tf_cli.ticket_loader`, `tf_cli.board_classifier`), those remain cached with their original TTY state. This means the test may not actually re-import in a truly "fresh" non-TTY context.
  
  **Why it's an issue**: If the UI module or its dependencies perform TTY checks at import time and cache that state, the test might pass even though a real headless import would fail. The test should clear all `tf_cli.*` modules from `sys.modules` to ensure a complete fresh import.

- `tests/test_ui_smoke.py:171` - The test assumes the module hasn't been imported yet in the test process, but `test_ui_module_imports_without_error` (line 162) imports it first. Python's import caching means the second test may not actually trigger a fresh import even after `del sys.modules["tf_cli.ui"]`.

  **Why it's an issue**: In pytest, tests run in order within a class, so the first test imports the module, and the second test's "fresh" import isn't truly fresh. This creates a dependency on test execution order that could mask real issues.

## Minor (nice to fix)
- `tests/test_ui_smoke.py:165-181` - The two test methods have overlapping concerns. `test_ui_module_imports_without_error` is essentially a subset of `test_ui_module_imports_in_non_tty_context`. Consider consolidating or making the distinction clearer (e.g., one tests basic import, the other tests import with explicit TTY mocking).

- `tests/test_ui_smoke.py:158` - The docstring says "These tests verify the module doesn't crash on import" but doesn't explain *why* this is critical (Textual/TUI libraries often fail on import in headless environments due to terminal detection).

## Warnings (follow-up ticket)
- `tf_cli/ui.py:1` - The UI module imports Textual and other heavy dependencies at module level. If the import-time TTY check (lines 320-324) becomes more restrictive in the future, these smoke tests won't catch it until runtime. Consider a follow-up ticket to add import-time safety checks or lazy loading for TTY-dependent libraries.

## Suggestions (follow-up ticket)
- `tests/test_ui_smoke.py` - Consider adding a test that verifies the TTY warning message is actually written when running in non-TTY mode. The existing tests verify import succeeds, but don't verify the warning behavior at lines 320-324 in `ui.py`.

- `tests/test_ui_smoke.py` - Add a test that mocks `textual` import failure to verify graceful degradation (the module should import even if Textual isn't installed, even though `main()` will fail later).

## Positive Notes
- Tests are well-organized with clear class-level docstrings explaining the purpose
- Good use of existing test infrastructure (pytest fixtures, unittest.mock)
- Follows existing file patterns and naming conventions (class names like `TestUiHeadlessImport` match the file's style)
- Proper use of `monkeypatch` fixture instead of manual patch context managers
- Tests verify both basic import and non-TTY context scenarios
- All 16 tests in the file pass, including the 2 new smoke tests

## Summary Statistics
- Critical: 0
- Major: 2
- Minor: 2
- Warnings: 1
- Suggestions: 2
