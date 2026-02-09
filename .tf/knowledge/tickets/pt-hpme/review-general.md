# Review: pt-hpme

## Overall Assessment
The implementation successfully creates a canonical `tf` package with `tf_cli` as a compatibility shim. The shim design is clean, deprecation warnings are properly opt-in, and backward compatibility is maintained. However, there are some inconsistencies in version reading logic and missing error handling edge cases that should be addressed.

## Critical (must fix)
- `tf/__init__.py:14-22` - The `_read_version()` function is significantly simpler than the original `tf_cli/version.py` implementation and may not work correctly in all installation scenarios. The original had: (1) repo root resolution, (2) git tag fallback, and (3) multiple VERSION file search paths. The new implementation only looks at `pkg_dir.parent / "VERSION"` which assumes VERSION is always at package root. This could break for edge cases like development installs, nested packages, or different installation modes.
- `tf/__init__.py:17-18` - Returns `"0.0.0-dev"` as fallback, but the original implementation returns `"unknown"`. This inconsistency could cause version comparison logic to fail if code expects one behavior and gets the other. The fallback values should be consistent between implementations during the transition period.

## Major (should fix)
- `tf_cli/__init__.py:26` - References `docs/deprecation-policy.md` in the warning message, but the path shown to users doesn't specify that this is relative to the repo root. Users running from installed packages may not know where to find this file. Consider using an absolute reference (URL) or showing a more user-friendly message like "Run `tf help deprecation` for details" or adding a dedicated deprecation help command.
- `tf_cli/cli.py:8` - The docstring says "This module is maintained for backward compatibility" but doesn't clearly indicate that `tf_cli` will be removed in 0.5.0. The deprecation message is good, but the module-level docstring could be more explicit about the removal timeline.
- `tf_cli/cli.py:30-36` - Re-exports many internal functions (`install_main`, `install_local_package`, `read_root_file`, `render_uvx_shim`, `resolve_repo_root`) that are implementation details of the CLI shim. These should not be part of the public API. The shim should only export `main` and `can_import_tf` (and the compat alias `can_import_tf_cli`). Exposing internals couples external code to implementation details.

## Minor (nice to fix)
- `tf/__init__.py:9` - Exception handling is too broad (`except Exception`). This masks specific errors (permission denied, encoding issues, etc.) making debugging harder. Consider catching specific exceptions like `OSError`, `FileNotFoundError`, `PermissionError`.
- `tf_cli/__init__.py:15-16` - The deprecation warning check happens at module import time. While the opt-in prevents spam, the check itself runs on every import. Consider making it a lazy check in `__getattr__` for a slight performance optimization (though this is minor and the current approach is simpler).
- `tf_cli/__main__.py:17` - The deprecation warning uses `stacklevel=2` but for module execution (`python -m tf_cli`), this might not point to the correct caller. Consider using `stacklevel=3` or testing the warning output to ensure it points to user code.

## Warnings (follow-up ticket)
- `tf_cli/__init__.py:13-20` - The ticket_factory imports are re-exported from `tf_cli.ticket_factory`. According to the implementation notes, these should be moved to `tf/` in pt-tupn. After pt-tupn completes, update the shim to re-export from `tf.ticket_factory` instead.
- `tf/cli.py:272-367` - The command handlers are imported from `tf_cli` modules (e.g., `from tf_cli import setup`, `from tf_cli import login`). This is intentional per the implementation notes, but after pt-tupn, these imports should be changed to `from tf import setup`, `from tf import login`, etc. Add a tracking note for pt-tupn.
- `tests/test_cli_version.py` - The test file still imports from `tf_cli.cli` and `tf_cli.version`. These tests should be updated in pt-m06z to import from `tf` instead. Currently they test the shim rather than the canonical implementation.

## Suggestions (follow-up ticket)
- Consider adding a `tf deprecation-info` command that prints the full deprecation policy and migration guide. This would be more discoverable than pointing to a markdown file that users may not know how to locate.
- The shim re-exports in `tf_cli/cli.py` could be simplified using `__all__` and `__getattr__` to avoid listing every function explicitly. For example:
  ```python
  __all__ = ["main", "can_import_tf", "can_import_tf_cli"]
  def __getattr__(name):
      if name in __all__:
          return getattr(tf.cli, name)
      raise AttributeError(...)
  ```
  This would automatically handle any new exports from `tf.cli` without updating the shim.

## Positive Notes
- The shim design is clean - no duplicated logic, just thin re-exports from the canonical `tf` package.
- The opt-in deprecation warning via `TF_CLI_DEPRECATION_WARN=1` is well-implemented and avoids CI noise.
- Both `python -m tf` and `python -m tf_cli` work correctly for module execution.
- The backward compatibility alias `can_import_tf_cli = can_import_tf` in `tf_cli/cli.py` is thoughtful.
- Lazy imports in `tf/cli.py` command handlers successfully avoid circular import issues.
- The pyproject.toml entry point `tf = "tf.cli:main"` correctly points to the canonical implementation.
- Type hints are used consistently throughout the codebase.
- The `__main__.py` modules are clean and correctly delegate to `main()`.

## Summary Statistics
- Critical: 2
- Major: 3
- Minor: 3
- Warnings: 3
- Suggestions: 2
