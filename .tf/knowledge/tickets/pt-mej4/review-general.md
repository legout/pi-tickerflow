# Review: pt-mej4

## Overall Assessment
Excellent test coverage implementation that raises the coverage gate from 25% to 35% while adding 114 comprehensive new tests across 5 previously uncovered user-facing modules. The tests are well-structured, use proper mocking patterns, and follow pytest best practices. All 693 tests pass with coverage at 59.4%, well above the new threshold.

## Critical (must fix)
No issues found

## Major (should fix)
- `tests/test_seed_cli.py:174` - The test assertion `args[0][0] == "my-seed"` relies on implementation detail of mock call args. Consider using `mock_sessions.assert_called_once_with("my-seed", ANY)` for clarity and to avoid fragility if argument order changes.

## Minor (nice to fix)
- `tests/test_agentsmd.py:1` - Unused import `shutil` at module level (it's accessed via `agentsmd_module.shutil` in tests, so the direct import can be removed)
- `tests/test_login.py:135` - Test `test_main_uses_env_vars` patches `os.environ.get` directly instead of using `mock.patch.dict(os.environ, {...})` which is the safer pattern for environment variable mocking
- `tests/test_setup.py:47` - Test `test_skips_when_pi_not_found` patches `sys.stderr.write` but doesn't verify the error message content, missing opportunity to assert on the "pi not found in PATH" message

## Warnings (follow-up ticket)
- `pyproject.toml` - The coverage threshold jump from 25% to 35% is reasonable but may cause CI failures on other branches that haven't synced. Consider documenting this change in release notes or coordinating with team.

## Suggestions (follow-up ticket)
- Consider adding parameterized tests for similar test cases (e.g., `test_default_yes_returns_true_on_empty` and `test_default_no_returns_false_on_empty` could be combined with `@pytest.mark.parametrize`)
- `tests/test_agentsmd.py` - Could benefit from a test for `status_agentsmd` that verifies the content preview functionality with files > 20 lines
- Consider adding integration tests that verify actual file I/O without mocking for critical paths like `configure_web_search` and `configure_mcp`

## Positive Notes
- Excellent use of `tmp_path` fixture for filesystem isolation in all new tests
- Proper use of `capsys` fixture for stdout/stderr capture instead of manual patching
- Good coverage of error handling paths (invalid JSON, permission errors, missing files)
- Tests verify actual behavior, not just that functions were called (e.g., checking file permissions, JSON content)
- Well-organized test classes that group related functionality
- The 10-point threshold increase (25% → 35%) demonstrates thoughtful incremental improvement rather than overly aggressive jumps

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 3
- Warnings: 1
- Suggestions: 3
