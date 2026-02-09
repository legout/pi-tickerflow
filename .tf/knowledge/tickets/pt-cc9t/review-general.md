# Review: pt-cc9t

## Overall Assessment
Clean implementation of a minimal Textual TUI skeleton with good error handling for TTY detection and optional dependency management. The code follows most project patterns but has minor inconsistencies in type annotations.

## Critical (must fix)
No issues found

## Major (should fix)
- `tf_cli/ui.py:13` - Type annotation uses `list[str] | None` which is inconsistent with the rest of the codebase. All other modules use `Optional[list[str]]` for the `main(argv=...)` signature. While `from __future__ import annotations` makes this technically work, consistency in a shared codebase is important for readability.

## Minor (nice to fix)
- `pyproject.toml` - Textual is not declared as an optional dependency. Since the TUI feature is optional (with graceful import failure handling), consider adding:
  ```toml
  [project.optional-dependencies]
  ui = ["textual>=0.41.0"]
  ```
  This allows users to install with `pip install pi-tk-workflow[ui]`.

- `tf_cli/ui.py:27-30` - The try/except for ImportError is good, but the error message could be more helpful by mentioning the optional dependency pattern:
  ```python
  print("Error: Textual is required for the TUI. Install with: pip install pi-tk-workflow[ui]", file=sys.stderr)
  ```

## Warnings (follow-up ticket)
- No unit tests for the `ui` module. Consider adding tests for:
  - TTY detection logic (can mock `sys.stdin.isatty()`)
  - Import error handling (can mock failed import)
  - Basic app instantiation test

## Suggestions (follow-up ticket)
- Consider adding a `--no-tty` flag to bypass TTY check for testing or CI environments
- Add CSS theming that matches the project's color scheme
- Future enhancement: Add mouse support configuration

## Positive Notes
- Good use of deferred import for optional dependency (Textual imported inside function)
- Clear TTY detection with helpful error message
- Proper `raise SystemExit(main())` pattern in `__main__` block
- Good module docstring explaining purpose
- Minimal skeleton approach is appropriate for this ticket scope
- Help text in `cli.py` properly includes the new command

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 2
- Warnings: 1
- Suggestions: 3
