# Implementation: ptw-u01e

## Summary
Extended version check to support git tags as third version source, and added package.json version verification for release validation.

## Files Changed
- `tf_cli/version.py` - Added git tag version support and package.json verification
- `tests/test_version.py` - Added comprehensive tests for new functionality

## Key Changes

### 1. Git Tag Version Support (`_get_git_tag_version`)
- New function to retrieve version from git tags
- Attempts exact tag match first (`git describe --tags --exact-match`)
- Falls back to latest tag (`git describe --tags --abbrev=0`)
- Strips 'v' prefix from tags (e.g., "v1.0.0" → "1.0.0")
- Gracefully handles missing git, no tags, and subprocess errors

### 2. Package.json Verification (`verify_package_json_version`)
- New function for release validation
- Compares package.json version with git tag version
- Returns structured result dictionary:
  - `ok`: bool - whether verification passed
  - `package_version`: str|None - version from package.json
  - `git_version`: str|None - version from git tag
  - `error`: str|None - error message if failed

### 3. Updated Version Fallback Order
The `get_version()` function now uses this fallback order:
1. VERSION file in repo root (for development)
2. VERSION file at package root (for pip/uvx installs)
3. **Git tag** (new - for git checkouts without VERSION file)
4. "unknown"

### 4. Public API
Updated `__all__` to export:
- `get_version`
- `verify_package_json_version` (new)
- `__version__`

## Tests Added
- `TestGetGitTagVersion` (6 tests) - Git tag parsing and edge cases
- `TestVerifyPackageJsonVersion` (7 tests) - Package.json verification scenarios
- `TestGetVersionWithGitTagFallback` (3 tests) - Fallback behavior
- `TestPublicAPI` (2 tests) - API exports verification

Total: 18 new tests, all passing (29 total in test_version.py)

## Key Decisions
- Used subprocess instead of GitPython to avoid new dependencies
- Git tag is third fallback, not first, to maintain backward compatibility
- 'v' prefix stripping is consistent with common git tag conventions
- Structured return dictionary for verification allows programmatic handling
- All subprocess errors are caught and return None gracefully

## Tests Run
```bash
pytest tests/test_version.py -v  # 29 passed
pytest tests/test_smoke_version.py tests/test_cli_version.py -v  # 12 passed
```

## Verification
- Existing version functionality remains unchanged
- Git tag fallback works when VERSION file is missing
- Package.json verification correctly identifies mismatches
- All edge cases handled (no git, no tags, invalid JSON, etc.)
