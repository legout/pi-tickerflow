# Review: pt-hpme

## Critical (must fix)
- `tf/__init__.py:14-22` - The `_read_version()` function is significantly simpler than the original `tf_cli/version.py` implementation and may not work correctly in all installation scenarios. The original had: (1) repo root resolution, (2) git tag fallback, and (3) multiple VERSION file search paths.
- `tf/__init__.py:17-18` - Returns `"0.0.0-dev"` as fallback, but the original implementation returns `"unknown"`. This inconsistency could cause version comparison logic to fail.

## Major (should fix)
- `tf_cli/__init__.py:26` - References `docs/deprecation-policy.md` in the warning message, but the path shown to users doesn't specify that this is relative to the repo root. Users running from installed packages may not know where to find this file.
- `tf_cli/cli.py:8` - The docstring says "This module is maintained for backward compatibility" but doesn't clearly indicate that `tf_cli` will be removed in 0.5.0.
- `tf_cli/cli.py:30-36` - Re-exports many internal functions (`install_main`, `install_local_package`, `read_root_file`, `render_uvx_shim`, `resolve_repo_root`) that are implementation details of the CLI shim. These should not be part of the public API.
- `tf_cli/__init__.py:6-19` - Missing smoke test for shim compatibility. The implementation verification section in implementation.md claims tests exist but `tests/test_smoke_version.py` only tests `tf --version`, not `python -m tf_cli --version` or `import tf_cli`.
- `implementation.md:62-70` - Verification claims tests that don't exist. The verification section shows test commands for tf_cli shim behavior but these are not automated tests in the test suite.

## Minor (nice to fix)
- `tf/__init__.py:9` - Exception handling is too broad (`except Exception`). This masks specific errors (permission denied, encoding issues, etc.) making debugging harder.
- `tf_cli/__init__.py:3-6` - The module docstring is verbose with deprecation notice. While accurate, the deprecation message is repeated in the code comments, warnings, and docstring.
- `tf_cli/cli.py:6-19` - Inconsistent warning message format. The warning says "tf_cli.cli is deprecated" but the message text doesn't include the removal version (0.5.0) like the tf_cli/__init__.py warning does.

## Warnings (follow-up ticket)
- `tf_cli/__init__.py:35-42` - The ticket_factory imports are re-exported from `tf_cli.ticket_factory`. According to the implementation notes, these should be moved to `tf/` in pt-tupn.
- `tf/cli.py:272-367` - The command handlers are imported from `tf_cli` modules. This is intentional per the implementation notes, but after pt-tupn, these imports should be changed to `from tf import setup`, etc.
- `tests/test_cli_version.py` - The test file still imports from `tf_cli.cli` and `tf_cli.version`. These tests should be updated in pt-m06z to import from `tf` instead.

## Suggestions (follow-up ticket)
- Consider adding a `tf deprecation-info` command that prints the full deprecation policy and migration guide.
- The shim re-exports in `tf_cli/cli.py` could be simplified using `__all__` and `__getattr__` to avoid listing every function explicitly.
- Consider adding a test that verifies no deprecation warnings are emitted by default (TF_CLI_DEPRECATION_WARN unset) to prevent regression.

## Summary Statistics
- Critical: 2
- Major: 5
- Minor: 3
- Warnings: 3
- Suggestions: 3
