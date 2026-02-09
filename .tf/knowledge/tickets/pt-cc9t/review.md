# Review: pt-cc9t

## Critical (must fix)
No issues found.

## Major (should fix)
- `tf_cli/ui.py:13` - Type annotation uses `list[str] | None` which is inconsistent with the rest of the codebase. All other modules use `Optional[list[str]]` for the `main(argv=...)` signature. (from reviewer-general)

## Minor (nice to fix)
- `pyproject.toml` - Textual is not declared as an optional dependency. Consider adding:
  ```toml
  [project.optional-dependencies]
  ui = ["textual>=0.41.0"]
  ```
  (from reviewer-general)

- `tf_cli/ui.py:27-30` - The error message could mention the optional dependency pattern. (from reviewer-general)

- `tf_cli/ui.py:28-34` - The `TicketflowApp` class is defined inside the `main()` function, which prevents proper type annotations. Consider defining at module level. (from reviewer-second-opinion)

- `tf_cli/ui.py:32` - CSS uses `border: solid green` which may not render well on all terminals. Consider `border: solid $primary`. (from reviewer-second-opinion)

## Warnings (follow-up ticket)
- `tf_cli/ui.py` - No unit tests for the ui module. Consider adding tests for TTY detection and import error handling. (from reviewer-general, reviewer-second-opinion)

## Suggestions (follow-up ticket)
- Consider adding `--demo` or `--mock` flag with sample tickets (from reviewer-second-opinion)
- Add CSS theming matching project color scheme (from reviewer-general)
- Consider `--no-tty` flag for testing (from reviewer-general)

## Positive Notes
- Good use of deferred import for optional dependency (from all reviewers)
- Clear TTY detection with helpful error message (from all reviewers)
- Follows existing project patterns for command routing (from reviewer-spec-audit)
- Minimal skeleton approach is appropriate for ticket scope (from reviewer-general)

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 4
- Warnings: 1
- Suggestions: 3
