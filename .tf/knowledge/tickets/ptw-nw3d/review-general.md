# Review: ptw-nw3d

## Overall Assessment
The implementation provides a clean, well-documented version retrieval module with comprehensive fallback handling for different installation modes. The code follows Python conventions with good type hints and docstrings. However, there are some significant issues with module-level initialization and fallback behavior that could lead to incorrect version detection in edge cases.

## Critical (must fix)
- `tf_cli/version.py:89` - Module-level `__version__ = get_version()` evaluates at import time and caches the result. If the VERSION file is not found during import (e.g., in a containerized environment or before repo root is properly set up), "unknown" will be permanently cached even if VERSION becomes available later. This also means tests that mock `get_version()` after import won't affect the cached `__version__` value.

## Major (should fix)
- `tf_cli/version.py:82-85` - The CWD fallback checks for VERSION in the current working directory, which can return incorrect version when running `tf` from a different project directory that has its own VERSION file. This is not just an "edge case" but a likely source of bugs when users run `tf` from within other ticketflow-based projects. Consider removing this fallback or making it opt-in with an environment variable.
- `tf_cli/version.py:22` - Docstring comment in `_resolve_repo_root()` says "even when run from a different ticketflow-based project directory" which is misleading. The function actually searches upward from the module's file location (`__file__`), not from cwd. While the current behavior is correct (it should find the actual ticketflow repo, not the cwd project), the comment suggests it handles cwd-based detection which it doesn't.

## Minor (nice to fix)
- `tf_cli/_version.py:4` - The deprecation notice is only in the docstring comment. Consider adding a runtime deprecation warning using `warnings.warn(DeprecationWarning, stacklevel=2)` to help users migrate to `tf_cli.version`.
- `tests/test_version.py` - Missing test coverage for the cwd fallback path in `get_version()`. Given this is a problematic code path, it should have explicit tests to document the expected behavior.
- `tf_cli/version.py:42-49` - The `_read_version_file()` function accepts any file content without validation. Consider adding basic validation to ensure the version string looks like a version (e.g., using a regex pattern like `^\d+\.\d+\.\d+.*`).

## Warnings (follow-up ticket)
- `tf_cli/version.py:71-76` - The fallback logic uses `Path(__file__).resolve().parent.parent` for pip/uvx installs, which assumes a specific package structure. If the package structure changes (e.g., moving version.py to a subdirectory), this will break. Consider using `importlib.resources` or pkgutil for more robust package-relative path resolution.

## Suggestions (follow-up ticket)
- Consider making `get_version()` cache-aware with a `force_reload` parameter for testing scenarios
- The fallback chain could benefit from logging/debug output to help diagnose version detection issues in production
- Consider adding a `tf doctor version` subcommand that tests all fallback paths and reports which one succeeded

## Positive Notes
- Excellent documentation with clear docstrings explaining the fallback order and supported installation modes
- Good use of type hints (`Optional[Path]`, `Optional[str]`) throughout
- Proper error handling in `_read_version_file()` with OSError catching
- Backward compatibility module (`_version.py`) is a nice touch for smooth migration
- Tests are comprehensive for the happy paths and repo root detection
- The module is well-structured with separate helper functions (`_resolve_repo_root`, `_read_version_file`)
- CLI integration is clean with early `--version` flag handling in `cli.py:418-420`

## Summary Statistics
- Critical: 1
- Major: 2
- Minor: 3
- Warnings: 1
- Suggestions: 3
