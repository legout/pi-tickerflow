# Review: pt-mej4

## Critical (must fix)
No issues found.

## Major (should fix)
- `tests/test_agentsmd.py:77-90` - The `test_creates_agentsmd` test validates file creation but should verify the complete AGENTS.md template structure including "Quick Commands" section and other expected sections to ensure the template generation logic is fully tested.
- `tests/test_login.py:154-170` - The `test_main_uses_env_vars` test patches `login_module.os.environ.get` but the actual source code uses `os.environ.get` directly after `import os`. Consider patching `os.environ` directly or use `monkeypatch` for more reliable environment variable mocking.
- `tests/test_seed_cli.py:174` - The test assertion `args[0][0] == "my-seed"` relies on implementation detail of mock call args. Consider using `mock_sessions.assert_called_once_with("my-seed", ANY)` for clarity.

## Minor (nice to fix)
- `tests/test_agentsmd.py:1` - Unused import `shutil` at module level (it's accessed via `agentsmd_module.shutil` in tests).
- `tests/test_agentsmd.py:163` - `test_warns_on_large_file` asserts `result == 1` but the source code treats large files as errors, not warnings. Rename test to `test_fails_on_large_file` for accuracy.
- `tests/test_login.py:135` - Test `test_main_uses_env_vars` patches `os.environ.get` directly instead of using `mock.patch.dict(os.environ, {...})` which is the safer pattern.
- `tests/test_setup.py:12` - The import alias `tf_setup_module` avoids pytest collection conflict but a comment explaining this would be helpful.
- `tests/test_setup.py:47` - Test `test_skips_when_pi_not_found` patches `sys.stderr.write` but doesn't verify the error message content.
- `tests/test_tags_suggest.py:56` - `test_suggest_handles_ticket_error` catches generic `RuntimeError` but doesn't verify the error message content.
- `.tf/knowledge/tickets/pt-mej4/implementation.md:1` - Document the staged coverage roadmap more explicitly (the acceptance criteria asks for "Coverage threshold roadmap agreed and applied incrementally").

## Warnings (follow-up ticket)
- `pyproject.toml` - Consider adding `pytest-cov` as an explicit dev dependency since the pytest addopts now requires it.
- `pyproject.toml` - The coverage threshold jump from 25% to 35% may cause CI failures on other branches that haven't synced. Document in release notes.
- `tests/test_login.py:1-220` - No test verifies the actual file permission setting (0o600) works correctly on Unix systems without silently skipping.
- `tests/test_agentsmd.py:1-281` - Missing test coverage for `detect_package_manager` handling of `pipenv`, `pip`, `yarn`, `bun`, and `bundle` package managers.

## Suggestions (follow-up ticket)
- Consider adding `--cov-branch` to pytest addopts to enforce branch coverage alongside line coverage.
- Add a conftest.py with shared fixtures for common mocking patterns to reduce duplication.
- Consider adding parameterized tests for similar test cases (e.g., yes/no prompt tests could use `@pytest.mark.parametrize`).
- `.github/workflows/ci.yml` - Consider adding an explicit coverage report step to make the "updated quality bar" more visible to contributors.
- Add integration tests that verify actual file I/O without mocking for critical paths.

## Summary Statistics
- Critical: 0
- Major: 3
- Minor: 8
- Warnings: 4
- Suggestions: 5

## Reviewer Sources
- review-general.md: General code review
- review-spec.md: Specification compliance audit
- review-second.md: Second opinion review
