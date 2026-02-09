# Review: pt-uo1b

## Critical (must fix)
No critical issues found.

## Major (should fix)
- `tests/test_ui_smoke.py:178-181` - The module cache deletion only removes `tf_cli.ui` but not its submodules. If `tf_cli.ui` imports submodules (like `tf_cli.ticket_loader`, `tf_cli.board_classifier`), those remain cached with their original TTY state. This means the test may not actually re-import in a truly "fresh" non-TTY context. **Suggestion**: Clear all `tf_cli.*` modules from `sys.modules` to ensure a complete fresh import.

- `tests/test_ui_smoke.py:171` - The test assumes the module hasn't been imported yet, but `test_ui_module_imports_without_error` imports it first. Python's import caching means the second test may not trigger a truly fresh import even after `del sys.modules["tf_cli.ui"]`. **Suggestion**: Use subprocess for true isolation or clear all related modules.

## Minor (nice to fix)
- `tests/test_ui_smoke.py:88-96` - The `test_ui_module_imports_in_non_tty_context` test has a flaw in its module re-import logic. After deleting `tf_cli.ui` from `sys.modules`, the parent `tf_cli` module still holds a reference to the original `ui` module. **Suggestion**: Also delete `tf_cli.ui` from the parent module: `delattr(sys.modules['tf_cli'], 'ui')` if present.

- `tests/test_ui_smoke.py:165-181` - The two test methods have overlapping concerns. `test_ui_module_imports_without_error` is essentially a subset of `test_ui_module_imports_in_non_tty_context`. Consider consolidating or making the distinction clearer.

- `tests/test_ui_smoke.py:158` - The docstring could explain *why* this is critical (Textual/TUI libraries often fail on import in headless environments due to terminal detection).

## Warnings (follow-up ticket)
- `tf_cli/ui.py:1` - The UI module imports Textual and other heavy dependencies at module level. If the import-time TTY check becomes more restrictive in the future, these smoke tests won't catch it until runtime. Consider a follow-up ticket to add import-time safety checks or lazy loading for TTY-dependent libraries.

## Suggestions (follow-up ticket)
- Consider adding a test that verifies the TTY warning message is actually written when running in non-TTY mode.
- Add a test that mocks `textual` import failure to verify graceful degradation.
- Consider a test that verifies import also works when `tf_cli` itself hasn't been previously imported (true cold-start scenario).

## Positive Notes
- The test class `TestUiHeadlessImport` is well-documented with a clear docstring explaining the purpose
- Tests use appropriate mocking from `unittest.mock` without adding new dependencies
- Tests integrate cleanly with existing pytest infrastructure
- No additional heavy dependencies were added as required by the acceptance criteria
- Implementation fully satisfies all acceptance criteria from the ticket

## Summary Statistics
- Critical: 0
- Major: 2
- Minor: 3
- Warnings: 1
- Suggestions: 3
