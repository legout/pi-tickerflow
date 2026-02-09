# Review: ptw-ykvx

## Critical (must fix)
- (none)

## Major (should fix)
- `tests/test_doctor_version_integration.py:17-19` - **Unused imports**: `check_extension` and `load_workflow_config` are imported but never used directly in test functions (only mocked). Remove these to clarify that tests exercise `run_doctor()` as a black box.
  - Reported by: reviewer-general, reviewer-second-opinion

## Minor (nice to fix)
- `tests/test_doctor_version_integration.py:69-75` - **Unused fixture return value**: The `mock_dependencies` fixture yields a dictionary of mock objects that are never used by test functions. Consider either using the returned mocks for explicit verification, or change the fixture to not yield anything.
  - Reported by: reviewer-second-opinion

- `tests/test_doctor_version_integration.py:275-296` - **Overly permissive e2e test**: `test_run_doctor_finds_real_tk_and_pi` asserts `result in [0, 1]` which passes regardless of whether tk/pi are installed. The test provides minimal validation when dependencies are missing.
  - Reported by: reviewer-general, reviewer-spec-audit, reviewer-second-opinion

- `tests/test_doctor_version_integration.py:15` - **pytestmark placement**: The module-level pytestmark is placed before local imports (lines 17-19). While functionally correct, this is unconventional. Typically pytestmark goes after all imports for better readability.
  - Reported by: reviewer-general

## Warnings (follow-up ticket)
- `tests/test_doctor_version_integration.py:189-218` - **Git dependency without graceful skip**: `test_run_doctor_with_git_tag_matching` requires git and uses `check=True` on subprocess calls. If git is unavailable, the test will raise `CalledProcessError` rather than skipping gracefully. Consider wrapping in try/except and calling `pytest.skip("git not available")`.
  - Reported by: reviewer-general

- `tests/test_doctor_version_integration.py:1` - **Documentation inconsistency**: The module docstring says "14 integration tests" but `implementation.md` has a typo listing test #12 twice. Minor documentation issue.
  - Reported by: reviewer-second-opinion

## Suggestions (follow-up ticket)
- Consider adding a test case for when `--fix` and `--dry-run` are both specified (edge case in CLI flag interaction)
- Consider adding a test for invalid `--project` path (non-existent directory)
- Consider adding test coverage for error conditions in version file I/O (permission errors, encoding issues)
- Consider extracting common assertion patterns into a helper fixture to reduce duplication

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 4
- Warnings: 2
- Suggestions: 4

## Reviewers
- reviewer-general (gpt-5.1-codex-mini)
- reviewer-spec-audit (gpt-5.3-codex)
- reviewer-second-opinion (gemini-3-flash)
