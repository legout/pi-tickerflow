# Review: pt-7sv0

## Overall Assessment
The implementation successfully creates a shared utility module (`tf_cli/utils.py`) and refactors five CLI modules to eliminate code duplication. The code is well-structured, thoroughly tested (17 tests), and maintains backward compatibility. All 156 existing tests pass, confirming no regressions.

## Critical (must fix)
No issues found

## Major (should fix)
No issues found

## Minor (nice to fix)
- `tf_cli/utils.py:1` - Consider adding `__all__` export list to explicitly define the public API:
  ```python
  __all__ = ["read_json", "find_project_root", "merge"]
  ```

## Warnings (follow-up ticket)
- `tf_cli/utils.py:23` - The `read_json()` function silently returns `{}` for any exception (invalid JSON, permission errors, etc.). This is documented behavior but could mask configuration errors. Consider logging warnings for non-missing-file errors in a future enhancement.

## Suggestions (follow-up ticket)
- `tf_cli/utils.py:62` - The `merge()` function could support additional types (lists, sets) for more comprehensive deep merging if needed in the future.
- `scripts/tf_config.py:11` and `.tf/scripts/tf_config.py:11` - Both scripts use `sys.path.insert()` for importing from `tf_cli`. Consider making `tf_cli` a proper installable package to avoid path manipulation.

## Positive Notes
- **Clean abstraction**: The three utility functions (`read_json`, `find_project_root`, `merge`) are well-designed with clear responsibilities and good type annotations.
- **Comprehensive tests**: The 17 test cases in `tests/test_utils.py` cover happy paths, edge cases, and error conditions. Tests for immutability (`test_does_not_mutate_input`) are particularly good.
- **Backward compatibility**: The unified `find_project_root()` checks for both `.tf` and `.pi` directories, being the most permissive of previous implementations.
- **Consistent refactoring**: All five CLI modules (`sync_new`, `doctor_new`, `backlog_ls_new`, `next_new`, `priority_reclassify_new`) and both `tf_config.py` scripts were properly updated with correct imports.
- **Documentation**: Functions have clear docstrings with Args/Returns sections.
- **Real-world test case**: `test_real_world_config_merge()` validates the merge function against actual config structures.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 1
- Suggestions: 2
