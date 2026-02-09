# Review: pt-0nqq

## Overall Assessment
The implementation successfully converges asset installation/update logic into a single canonical `asset_planner.py` module. The code is well-structured with clear separation of concerns, good use of dataclasses, and comprehensive test coverage (60 tests passing for the modified modules). The design maintains backward compatibility through the thin wrapper approach. However, there are several critical issues around error handling, timeout configuration, and security considerations that should be addressed.

## Critical (must fix)
- `tf_cli/asset_planner.py:187-190` - `_download()` and `_download_bytes()` use `urllib.request.urlopen()` without timeout parameters. Network operations can hang indefinitely if servers are slow or unresponsive. Add `timeout=30` (or configurable) to both functions.
- `tf_cli/asset_planner.py:194-196` - `_download_bytes()` reads entire response into memory with `resp.read()`. For large files, this could exhaust memory. Implement streaming or add size limits.
- `tf_cli/asset_planner.py:507-514` - `install_bundle()` raises `SystemExit(1)` on errors after printing error details. This is unexpected behavior for a library-style function - it should raise an exception instead, letting the CLI layer decide whether to exit. Currently prevents programmatic use.
- `tf_cli/asset_planner.py:117-121` - `_read_text()` catches all exceptions with bare `except Exception:` and returns empty string. This masks important errors like permission denied, encoding issues, or I/O errors. Should be more specific or log warnings.
- `tf_cli/asset_planner.py:455-458` - In `plan_installation()` with `force=True`, files are marked for update without actually fetching new content first. Later in `execute_plan()`, if `plan.new_content` is None, it re-downloads the file. This means force operations may fail silently if the source becomes unavailable between planning and execution.

## Major (should fix)
- `tf_cli/update_new.py:50-60` - `resolve_target_base()` returns `~/.pi/agent` as a fallback global path. This is inconsistent with other commands (init_new.py, sync_new.py) which have clearly defined project-local behavior. The update command should either: (a) require explicit project specification, or (b) clearly document that it falls back to global installation.
- `tf_cli/update_new.py:124-126` - When `check_for_updates()` returns errors, they are printed to stderr but the function continues. The code then proceeds to update even though there were manifest loading errors. Should return early if errors exist before prompting user.
- `tf_cli/asset_planner.py:425-437` - In `plan_installation()` with `check_updates=True`, if both `plan.entry.local_path` and `plan.entry.source_url` are None (shouldn't happen but defensive coding), the code sets `new_content = current_content`, treating files as identical. This should raise an explicit error.
- `tf_cli/asset_planner.py:458-470` - Duplicate chmod error handling code in `execute_plan()`. The try/except block for `chmod` is identical in both the install and update sections. Extract to helper `_make_executable(path: Path) -> None` to reduce duplication.
- `tf_cli/init_new.py:42-46` - In `init_project()`, when `install_bundle()` fails, the generic error message "Failed to install bundle" doesn't help users troubleshoot. Include the exception message: `print(f"ERROR: Failed to install bundle: {exc}", file=sys.stderr)`

## Minor (nice to fix)
- `tf_cli/asset_planner.py:505` - `install_bundle()` returns `(total_changed, skipped_count)` where total_changed = installed + updated. However, the docstring says "(installed_count, skipped_count)" which is misleading. Rename return values or clarify docstring.
- `tf_cli/update_new.py:30` - `DEFAULT_RAW_REPO_URL` is redefined from `asset_planner` instead of importing it: `from .asset_planner import DEFAULT_RAW_REPO_URL`. This creates a second copy of the constant rather than maintaining single source of truth.
- `tf_cli/asset_planner.py:321-324` - In `create_asset_plan()`, the redundant `local_src.exists()` check after already verifying `if local_src` (which checks truthiness). Path objects are truthy, so the exists check adds no value.
- `tf_cli/sync_new.py:94` - `project_bundle.install_bundle()` is called without any error handling. If the manifest is empty or loading fails, the `SystemExit` will propagate up and exit the program. Consider catching and re-raising with more context.
- `tf_cli/project_bundle.py:50` - Duplicate import in `compute_bundle_plan()`: `AssetPlan` is imported twice in the same line. Clean up the import statement.

## Warnings (follow-up ticket)
- `tf_cli/asset_planner.py:120` - `find_repo_root()` silently catches all exceptions when reading `.tf/cli-root` marker files. If there are permission issues or corrupted files, debugging becomes very difficult. Consider logging warnings in debug/verbose mode.
- `tf_cli/asset_planner.py:223` - `raw_base_from_source()` URL parsing assumes well-formed GitHub URLs. Malformed inputs like "github.com/owner" or "github.com/owner/repo/extra/something" could cause index errors or incorrect behavior.
- `tf_cli/asset_planner.py:179-182` - `resolve_raw_base()` falls back to `DEFAULT_RAW_REPO_URL` if `raw_base_from_source()` returns None. However, if `TF_UVX_FROM` environment variable is set to an invalid URL, the user's intent is silently ignored. Could log a warning when falling back.
- `tf_cli/asset_planner.py:518` - In `update_assets()`, the `select` parameter filters the manifest to only update specific files. However, this happens after `load_manifest()` is called. For large manifests, consider optimizing to only fetch selected files when a filter is provided.

## Suggestions (follow-up ticket)
- Add a `--dry-run` flag to `tf update` command that shows what would be changed without actually modifying files. This is already supported in `execute_plan()` but not exposed to users.
- Consider using a dedicated HTTP client library like `httpx` or `requests` instead of `urllib.request` for better timeout handling, retry logic, and connection pooling.
- Add progress indicators for bulk operations (e.g., "Installing 15 files... 3/15 complete").
- Implement caching for downloaded assets to avoid re-downloading unchanged files across multiple operations.
- Add configuration options in settings.json for timeout values, retry policies, and download size limits.
- Add unit tests for error paths that aren't covered: network failures, permission errors, malformed URLs, and concurrent access issues.
- Consider adding a `--verbose` flag that logs detailed information about what's being checked, skipped, or updated.
- Document the behavior of the `--global` flag across all commands. Currently some commands reject it while others silently use global fallbacks.
- Add type hints for private functions (starting with `_`) to improve IDE autocomplete and documentation generation.
- Consider implementing a content hash-based comparison instead of full byte comparison for large files to improve performance.

## Positive Notes
- Excellent architectural decision to create a single canonical `asset_planner.py` module, eliminating duplication between init, sync, and update commands.
- Clean use of Python dataclasses (`AssetEntry`, `AssetPlan`, `PlanResult`, `ExecutionResult`) makes the data model clear and type-safe.
- Backward compatibility is well maintained through the thin wrapper in `project_bundle.py`, allowing gradual migration.
- The `dry_run` parameter in `execute_plan()` enables safe testing and preview functionality.
- Comprehensive test coverage with 60 tests specifically for the new asset_planner module and updated commands.
- Good separation of planning (what to do) and execution (actually doing it), which enables better testing and dry-run support.
- The `classify_asset()` function provides a centralized, extensible way to determine where different asset types should be installed.
- Consistent use of `__future__ import annotations` for forward compatibility with Python 3.10+.
- Clear docstrings with parameter descriptions and return value documentation.
- The `AssetAction` enum makes the state machine for file operations explicit and readable.

## Summary Statistics
- Critical: 5
- Major: 5
- Minor: 5
- Warnings: 4
- Suggestions: 13
