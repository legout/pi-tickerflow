# Review: ptw-ykvx

## Overall Assessment
Well-structured integration test suite with comprehensive coverage of version check CLI functionality. The 14 tests cover the main user-facing paths through `run_doctor()`, including all CLI flags (`--fix`, `--dry-run`, `--project`) and various manifest types. Tests are properly isolated using pytest fixtures and mocked dependencies.

## Critical (must fix)
No issues found

## Major (should fix)
- `tests/test_doctor_version_integration.py:19` - Unused imports: `check_extension` and `load_workflow_config` are imported but never used in the test file. These should be removed to keep imports clean.

## Minor (nice to fix)
- `tests/test_doctor_version_integration.py:15` - `pytestmark` placement: The module-level pytestmark is placed before local imports (lines 17-19). While functionally correct, this is unconventional. Typically pytestmark goes after all imports for better readability.
- `tests/test_doctor_version_integration.py:275-296` - The end-to-end test `test_run_doctor_finds_real_tk_and_pi` has misleading logic: it checks for tk/pi existence but runs the full test regardless. The comment says "Only run if tk and pi are available" but there's no actual skip condition. Consider using `@pytest.mark.skipif(shutil.which("tk") is None, reason="tk not installed")` or similar to properly conditionally skip.
- `tests/test_doctor_version_integration.py:292` - Vague assertion: The test asserts `result in [0, 1]` which allows any outcome. This provides minimal validation. Consider asserting specific expected behavior based on whether tk/pi are actually present.

## Warnings (follow-up ticket)
- `tests/test_doctor_version_integration.py:189-218` - Git dependency in test: `test_run_doctor_with_git_tag_matching` requires git to be installed. While marked as integration test, there's no graceful skip if git is unavailable. The subprocess calls use `check=True` which will raise `CalledProcessError` if git commands fail. Consider wrapping in try/except and calling `pytest.skip("git not available")` if git init fails.

## Suggestions (follow-up ticket)
- Consider adding a test case for when `--fix` and `--dry-run` are both specified (edge case in CLI flag interaction)
- Consider adding a test for invalid `--project` path (non-existent directory)
- Consider adding test coverage for the case when `run_doctor` raises SystemExit in mocked scenarios to verify error handling paths

## Positive Notes
- Excellent use of pytest fixtures (`tmp_path`, `mock_dependencies`, `capsys`) for clean test isolation
- Good test naming following the `test_<scenario>_<expected_behavior>` convention
- Proper use of markers (`pytest.mark.integration`, `pytest.mark.e2e`) which are registered in pyproject.toml
- Mock dependencies fixture effectively isolates the version check testing from external tool dependencies
- Tests verify both return codes AND output messages, ensuring complete behavior validation
- The two-tier approach (mocked integration tests + real e2e tests) provides both speed and realism
- Clean separation between TestRunDoctorVersionIntegration (12 mocked tests) and TestRunDoctorEndToEnd (2 real tests)

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 3
- Warnings: 1
- Suggestions: 3
