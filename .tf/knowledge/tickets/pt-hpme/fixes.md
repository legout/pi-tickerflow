# Fixes: pt-hpme

## Summary
Fixed critical and major issues identified in the review process. All critical issues resolved, major issues addressed where applicable.

## Critical Fixes

### 1. Fixed version reading logic in `tf/__init__.py`
**Issue**: The `_read_version()` function was significantly simpler than the original `tf_cli/version.py` implementation.

**Fix**: Replaced simple implementation with full version resolution logic matching the original:
- Added `_resolve_repo_root()` to find repository root by looking for `.tf` directory and `VERSION` file markers
- Added `_read_version_file()` for safe version file reading with proper encoding
- Added `_get_git_tag_version()` for git tag fallback with subprocess calls
- Proper fallback chain: repo root VERSION → package root VERSION → git tag → "unknown"

**Files changed**: `tf/__init__.py`

### 2. Fixed fallback version inconsistency
**Issue**: Returned `"0.0.0-dev"` instead of `"unknown"` when version cannot be determined.

**Fix**: Changed fallback return value to `"unknown"` to match original `tf_cli/version.py` behavior.

**Files changed**: `tf/__init__.py`

## Major Fixes

### 3. Fixed warning message in `tf_cli/__init__.py`
**Issue**: Warning message referenced local path `docs/deprecation-policy.md` which users may not find.

**Fix**: Updated warning to use full GitHub URL:
```
See https://github.com/legout/pi-ticketflow/blob/main/docs/deprecation-policy.md
```

**Files changed**: `tf_cli/__init__.py`

### 4. Updated docstring in `tf_cli/cli.py`
**Issue**: Module docstring didn't clearly indicate removal timeline.

**Fix**: Updated docstring to explicitly state:
- "through version 0.4.x" for compatibility period
- Direct reference to removal in "version 0.5.0"

**Files changed**: `tf_cli/cli.py`

### 5. Removed internal function re-exports from `tf_cli/cli.py`
**Issue**: Re-exported internal functions (`install_main`, `install_local_package`, `read_root_file`, `render_uvx_shim`, `resolve_repo_root`, `DEFAULT_UVX_SOURCE`) that are implementation details.

**Fix**: Reduced exports to only public API:
- `main`
- `can_import_tf`
- `can_import_tf_cli` (backward compat alias)

Removed internal functions from `__all__` and imports.

**Files changed**: `tf_cli/cli.py`

### 6. Fixed warning message in `tf_cli/cli.py`
**Issue**: Warning message format was inconsistent (didn't include removal version).

**Fix**: Updated warning to include "This shim will be removed in version 0.5.0" and full GitHub URL.

**Files changed**: `tf_cli/cli.py`

### 7. Fixed warning message in `tf_cli/__main__.py`
**Issue**: Warning message referenced local path instead of URL.

**Fix**: Updated to use full GitHub URL for deprecation policy.

**Files changed**: `tf_cli/__main__.py`

### 8. Simplified docstring in `tf_cli/__init__.py`
**Issue**: Verbose docstring with repeated deprecation notice.

**Fix**: Consolidated to concise single-line deprecation notice.

**Files changed**: `tf_cli/__init__.py`

## Minor Fixes (Partial)

### 9. Improved exception handling in `tf/__init__.py`
**Issue**: Used broad `except Exception` which masks specific errors.

**Fix**: Changed to specific `OSError` catching in `_read_version_file()` and specific `subprocess.SubprocessError`, `FileNotFoundError`, `OSError` in `_get_git_tag_version()`.

**Files changed**: `tf/__init__.py`

## Not Addressed (Deferred)

### Missing smoke tests for tf_cli shim
The review identified that `tests/test_smoke_version.py` only tests `tf --version`, not `python -m tf_cli --version`. However, this is explicitly deferred to **pt-m06z** which is tasked with "add at least one test that imports tf_cli (shim) successfully". Adding tests in pt-hpme would create unnecessary duplication.

### Test file still imports from tf_cli
`tests/test_cli_version.py` imports from `tf_cli.cli` and `tf_cli.version`. This is intentional during the migration period and will be updated in **pt-m06z**.

## Verification

After fixes, verified:
- `python -c "import tf; print(tf.__version__)"` → `0.3.0` ✓
- `python -c "import tf_cli; print(tf_cli.__version__)"` → `0.3.0` ✓
- `TF_CLI_DEPRECATION_WARN=1 python -c "import tf_cli"` → Shows warning ✓
- `python -c "import tf_cli"` → No warning (default) ✓
- `python -m tf --version` → `0.3.0` ✓
- `python -m tf_cli --version` → `0.3.0` ✓

## Files Changed Summary

| File | Changes |
|------|---------|
| `tf/__init__.py` | Complete rewrite of version reading logic to match original tf_cli/version.py |
| `tf_cli/__init__.py` | Simplified docstring, updated warning message with URL |
| `tf_cli/cli.py` | Reduced exports to public API only, updated docstring and warning |
| `tf_cli/__main__.py` | Updated warning message with URL |
