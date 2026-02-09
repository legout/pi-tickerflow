# Fixes: pt-0nqq

## Summary
Fixed all Critical and Major issues identified in the review.

## Critical Fixes Applied

1. **Network timeout added** (`asset_planner.py`)
   - `_download()` and `_download_bytes()` now use `timeout=30` parameter
   - Prevents indefinite hangs on slow/unresponsive servers

2. **Exception chaining preserved** (`asset_planner.py`)
   - `load_manifest()` now uses `raise ... from exc` to preserve traceback

3. **SystemExit replaced with RuntimeError** (`asset_planner.py`)
   - `install_bundle()` now raises `RuntimeError` instead of `SystemExit(1)`
   - Allows programmatic use and lets CLI layer handle exit decisions

4. **Duplicate import fixed** (`project_bundle.py`)
   - Removed duplicate `AssetPlan` import in `compute_bundle_plan()`

5. **Error handling improved** (`init_new.py`)
   - Now catches `RuntimeError` from `install_bundle()` instead of `SystemExit`
   - Provides cleaner error message

6. **Duplicate constant fixed** (`update_new.py`)
   - Now imports `DEFAULT_RAW_REPO_URL` directly from `asset_planner`

## Major Fixes Applied

1. **Extracted chmod helper** (`asset_planner.py`)
   - Added `_make_executable(path: Path)` helper function
   - Replaced duplicate chmod try/except blocks in `execute_plan()`

2. **Error handling verified** (`update_new.py`)
   - Already returns early when `check_for_updates()` returns errors
   - No changes needed - code already correct

## Not Fixed (Minor/Design Decisions)

The following issues were not fixed as they require design decisions or are minor:

- **Global fallback in update**: The `~/.pi/agent` fallback is preserved for backward compatibility
- **README documentation**: Out of scope for this implementation ticket
- **Bare exception handling**: `_read_text()` still uses bare exception - acceptable for this utility function
- **Memory handling for large files**: Streaming would add complexity; current implementation is acceptable for expected file sizes

## Files Modified During Fix Phase
- `tf_cli/asset_planner.py` - Timeout, exception chaining, RuntimeError, chmod helper
- `tf_cli/project_bundle.py` - Fixed duplicate import
- `tf_cli/init_new.py` - Updated error handling for RuntimeError
- `tf_cli/update_new.py` - Fixed duplicate constant import

## Verification
All 75 tests pass after fixes.
