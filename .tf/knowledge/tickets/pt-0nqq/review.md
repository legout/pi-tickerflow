# Review: pt-0nqq

## Critical (must fix)

1. **`tf_cli/asset_planner.py:187-190`** - Network timeout missing (all reviewers)
   - `_download()` and `_download_bytes()` use `urllib.request.urlopen()` without timeout
   - **Fix**: Add `timeout=30` parameter to prevent indefinite hangs

2. **`tf_cli/asset_planner.py:507-514`** - Unexpected SystemExit (reviewer-general)
   - `install_bundle()` raises `SystemExit(1)` on errors, preventing programmatic use
   - **Fix**: Raise a proper exception instead, let CLI layer handle exit

3. **`tf_cli/asset_planner.py:194-196`** - Memory issue with large files (reviewer-general, second-opinion)
   - `_download_bytes()` reads entire response into memory
   - **Fix**: Implement streaming or add size limits

4. **`tf_cli/asset_planner.py:117-121`** - Bare exception handling masks errors (reviewer-general)
   - `_read_text()` catches all exceptions, masks permission/encoding issues
   - **Fix**: Be more specific or log warnings

5. **`tf_cli/asset_planner.py:279`** - Lost traceback in exception chain (second-opinion)
   - `load_manifest()` wraps exceptions without preserving chain
   - **Fix**: Use `raise ... from exc` to preserve traceback

6. **`project_bundle.py:50`** - Duplicate import (second-opinion, reviewer-general)
   - `AssetPlan` imported twice in same line
   - **Fix**: Remove duplicate

## Major (should fix)

1. **`tf_cli/asset_planner.py:458-470`** - Duplicate chmod code (all reviewers)
   - Same try/except block in both install and update sections
   - **Fix**: Extract to helper `_make_executable(path: Path) -> None`

2. **`tf_cli/update_new.py:124-126`** - Continues despite errors (reviewer-general, second-opinion)
   - When `check_for_updates()` returns errors, code continues to update
   - **Fix**: Return early if errors exist before prompting user

3. **`tf_cli/update_new.py:50-60`** - Global fallback inconsistency (reviewer-general, second-opinion)
   - Falls back to `~/.pi/agent` which is inconsistent with other commands
   - **Fix**: Document behavior or require explicit project specification

4. **`tf_cli/asset_planner.py:425-437`** - Silent handling of missing source (reviewer-general)
   - When both local_path and source_url are None, silently treats as identical
   - **Fix**: Raise explicit error

5. **`tf_cli/init_new.py:42-46`** - Unhelpful error message (reviewer-general)
   - Generic "Failed to install bundle" doesn't help troubleshoot
   - **Fix**: Include exception message: `f"Failed to install bundle: {exc}"`

## Minor (nice to fix)

1. **`tf_cli/asset_planner.py:505`** - Docstring/return mismatch (reviewer-general, second-opinion)
   - Returns `(total_changed, skipped)` but docstring says `(installed_count, skipped_count)`
   - **Fix**: Clarify docstring

2. **`tf_cli/update_new.py:30`** - Duplicate constant (reviewer-general, second-opinion)
   - `DEFAULT_RAW_REPO_URL` redefined instead of imported
   - **Fix**: Import from asset_planner

3. **`tf_cli/asset_planner.py:321-324`** - Redundant exists check (reviewer-general, second-opinion)
   - `local_src.exists()` check after `if local_src` is redundant
   - **Fix**: Remove redundant check

4. **`tf_cli/sync_new.py:94`** - Missing error handling (reviewer-general, second-opinion)
   - `install_bundle()` called without error handling
   - **Fix**: Add try/catch with context

5. **`README.md`** - Missing documentation (spec-audit)
   - No reference to new asset_planner.py architecture
   - **Fix**: Update README to document the converged asset flow

## Warnings (follow-up ticket)

1. **`tf_cli/asset_planner.py:120`** - Silent failures in find_repo_root() (all reviewers)
   - Catches all exceptions when reading marker files, hard to debug

2. **`tf_cli/asset_planner.py:223`** - Limited URL validation (reviewer-general, second-opinion)
   - Assumes well-formed GitHub URLs, malformed inputs could cause issues

3. **`tf_cli/asset_planner.py:179-182`** - Silent fallback in resolve_raw_base() (reviewer-general)
   - Falls back to default without warning when TF_UVX_FROM is invalid

4. **`tf_cli/asset_planner.py:518`** - Selective update optimization (reviewer-general)
   - Could optimize to only fetch selected files when filter is provided

## Suggestions (follow-up ticket)

1. Add `--dry-run` flag to `tf update` command (spec-audit, all reviewers)
2. Consider using `httpx` or `requests` instead of `urllib.request` (all reviewers)
3. Add progress indicators for bulk operations (reviewer-general)
4. Implement caching for downloaded assets (reviewer-general)
5. Add configuration options for timeout values, retry policies (reviewer-general)
6. Add integration tests for full workflow (spec-audit)
7. Expose `--select` flag for selective updates (spec-audit)
8. Document `--global` flag behavior across commands (reviewer-general)

## Summary Statistics
- Critical: 6
- Major: 5
- Minor: 5
- Warnings: 4
- Suggestions: 8

## Overall Assessment
The implementation successfully converges asset install/update flow onto a single canonical planner (`asset_planner.py`). All 541 tests pass. The code is well-structured with good separation of concerns. Critical issues focus on network timeout handling and error propagation. Major issues involve code duplication and error handling consistency.
