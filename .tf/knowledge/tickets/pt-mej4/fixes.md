# Fixes: pt-mej4

## Issues Fixed

### Major Issues (3)

1. **test_agentsmd.py:116** - Enhanced `test_creates_agentsmd` to verify complete AGENTS.md template structure:
   - Added assertions for "## Quick Commands" section
   - Added assertions for uv commands (run, test)
   - Added assertions for "## Conventions" and "## Notes" sections
   - Added assertion for package manager documentation

2. **test_login.py:203** - Fixed environment variable mocking to use proper pattern:
   - Changed from `@patch.object(login_module.os.environ, "get", ...)` to `@patch("os.environ.get", ...)`
   - This ensures the patch works correctly since login.py imports `os` and uses `os.environ.get`
   - Applied same fix to `test_main_skips_config_when_no_keys`

3. **test_seed_cli.py:228** - Improved test clarity using `assert_called_once_with`:
   - Changed from manual `args[0][0]` inspection to `mock_sessions.assert_called_once_with("my-seed", ANY)`
   - Added explicit `isinstance` check for Path in knowledge_dir test
   - Added `from unittest.mock import ANY` import

## Tests Re-run
```bash
python -m pytest tests/ --cov=tf_cli --cov-report=term
```
Result: 693 passed, 59.4% coverage

## Remaining Issues

### Minor (8)
- Unused import cleanup, test naming improvements, and documentation comments

### Warnings (4)
- Follow-up: Add pytest-cov as explicit dev dependency
- Follow-up: Document coverage threshold change in release notes
- Follow-up: Improve file permission testing on Unix
- Follow-up: Add tests for remaining package managers (pipenv, pip, yarn, bun, bundle)

### Suggestions (5)
- Add branch coverage enforcement
- Create shared fixtures in conftest.py
- Use parameterized tests for similar cases
- Add coverage report step to CI
- Add integration tests for critical paths
