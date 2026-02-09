# Review: abc-123

## Critical (must fix)
- `pyproject.toml:62` - Coverage `source` list is `["tf", "tf_cli"]` but doesn't include `"demo"` even though it's declared in `packages`. This means code coverage for the new demo package won't be tracked or reported, breaking the project's quality metrics. *(from reviewer-second-opinion)*

## Major (should fix)
- `demo/__main__.py:14-15` - CLI uses raw `sys.argv` parsing with `" ".join(sys.argv[1:])` instead of `argparse`. This diverges from the project's convention (see `tf/hello.py` which uses `argparse`) and makes the CLI less extensible and harder to test. The function signature should accept `argv: Optional[list[str]] = None` like `tf/hello.py:main()`. *(from reviewer-second-opinion)*

## Minor (nice to fix)
- `demo/__main__.py:17` - Redundant fallback: The CLI does `or "World"` after joining args, but `hello()` already handles empty/whitespace names internally. While harmless, this duplicates logic. *(from reviewer-general)*
- `tests/test_demo_hello.py` - No tests for the `demo/__main__.py` CLI module. The CLI entry point is untested, including the multi-word name joining logic. *(from reviewer-second-opinion)*
- `demo/__main__.py:10` - Missing module-level docstring example showing multi-word name support (e.g., `python -m demo Alice Smith` works). *(from reviewer-second-opinion)*

## Warnings (follow-up ticket)
- `pyproject.toml:66-69` - Coverage `omit` patterns may need review to ensure demo package test files are properly excluded if tests are reorganized. *(from reviewer-second-opinion)*

## Suggestions (follow-up ticket)
- `demo/__main__.py` - Consider using `argparse` for CLI argument parsing if the tool grows in complexity. The current `sys.argv` approach is fine for this simple use case but doesn't scale well. *(from reviewer-general)*
- `demo/hello.py:42` - Consider adding type validation for the `name` parameter (e.g., raise `TypeError` if not a string). *(from reviewer-spec-audit)*
- `tests/test_demo_hello.py:28` - Consider adding a test for CLI invocation via `subprocess` or `click.testing` if CLI testing is desired. *(from reviewer-spec-audit)*
- `demo/__main__.py` - Consider adding argparse support with `--help`, `--version` flags to match the full-featured CLI pattern in `tf/hello.py`. *(from reviewer-second-opinion)*
- `tests/` - Consider organizing tests into `tests/unit/demo/` structure as the project grows. *(from reviewer-second-opinion)*

## Summary Statistics
- Critical: 1
- Major: 1
- Minor: 3
- Warnings: 1
- Suggestions: 5

## Reviewer Sources
- reviewer-general: 0 Critical, 0 Major, 1 Minor, 0 Warnings, 1 Suggestion
- reviewer-spec-audit: 0 Critical, 0 Major, 0 Minor, 0 Warnings, 2 Suggestions
- reviewer-second-opinion: 1 Critical, 1 Major, 2 Minor, 1 Warning, 2 Suggestions
