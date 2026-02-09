# Review (Second Opinion): pt-0nqq

## Overall Assessment
The implementation successfully converges asset install/update flow into a canonical `asset_planner.py` module with good test coverage. The code is well-structured and follows separation of concerns. However, there are several critical issues around network operations without timeouts, memory handling for large files, and some error handling concerns that should be addressed.

## Critical (must fix)
- `tf_cli/asset_planner.py:257-266` - `_download()` and `_download_bytes()` use `urllib.request.urlopen()` without timeout. Network operations can hang indefinitely if the server is slow or unresponsive. Add `timeout` parameter (e.g., `urllib.request.urlopen(url, timeout=30)`).
- `tf_cli/asset_planner.py:268` - `_download_bytes()` reads entire file into memory with `resp.read()`. Large files could cause memory exhaustion. Consider streaming or adding size limits.
- `tf_cli/asset_planner.py:279` - `load_manifest()` catches bare `Exception` and wraps in `RuntimeError`. The traceback is lost in the re-raising, making debugging harder. Use `raise ... from exc` to preserve the chain.
- `project_bundle.py:50` - Duplicate import statement: `from .asset_planner import AssetPlan, classify_asset, AssetPlan`. `AssetPlan` is imported twice, causing confusion and potential issues.

## Major (should fix)
- `tf_cli/asset_planner.py:425` - In `plan_installation()`, when both `plan.entry.local_path` and `plan.entry.source_url` are `None`, it falls back to `new_content = current_content`. This silently treats files as identical with no source to compare. Should return an error or handle this case explicitly.
- `tf_cli/asset_planner.py:458-470` - Duplicate chmod error handling code in `execute_plan()`. The try/except block for setting executable permissions is identical in both the install and update sections. Extract to a helper function to reduce duplication.
- `tf_cli/update_new.py:124-126` - When `check_for_updates()` returns errors, they are printed but the function continues. The error list is then ignored. Check if errors exist before proceeding with update flow.
- `tf_cli/update_new.py:50-60` - `resolve_target_base()` falls back to `~/.pi/agent` when no project is found. This appears to be a legacy global path. Since the implementation is now project-local, this fallback may lead to incorrect behavior if used unexpectedly.

## Minor (nice to fix)
- `tf_cli/asset_planner.py:321-324` - In `create_asset_plan()`, the code checks `if local_src and local_src.exists()` to determine the source. However, `local_src` was already filtered by the condition above. The `local_src.exists()` check is redundant but harmless.
- `tf_cli/asset_planner.py:505` - `install_bundle()` returns `(total_changed, skipped_count)` where total_changed = installed + updated. The docstring says `(installed_count, skipped_count)` and the code comment refers to "total changes". This naming inconsistency could confuse callers.
- `tf_cli/sync_new.py:94` - `project_bundle.install_bundle()` is called without handling potential failures (like empty manifest). If it raises `RuntimeError`, it will propagate up and show a generic error without context.
- `tf_cli/update_new.py:30` - `DEFAULT_RAW_REPO_URL` is redefined from `asset_planner` instead of just importing it. Use `from .asset_planner import DEFAULT_RAW_REPO_URL` to maintain single source of truth.
- `tf_cli/sync_new.py:26` - Inconsistent error handling pattern: `update_agent_frontmatter()` and `update_prompt_frontmatter()` re-raise exceptions that sync_models() catches and adds to errors list. Other modules raise SystemExit directly. Consider standardizing error handling.

## Warnings (follow-up ticket)
- `tf_cli/asset_planner.py:120` - `find_repo_root()` catches all exceptions when reading `.tf/cli-root` files. If there's a permissions issue or file corruption, it will fail silently. Log warnings in development mode.
- `tf_cli/asset_planner.py:223` - `raw_base_from_source()` has limited URL parsing. It assumes GitHub URLs but doesn't validate that the split results in exactly 2 parts for owner/repo. Malformed URLs like "github.com/owner/repo/extra" could cause issues.
- `tf_cli/update_new.py:45` - The fallback to `Path.home() / ".pi/agent"` assumes this directory exists. If it doesn't, the update command will fail later when trying to read/write assets. Document this in the help text or verify early.
- `tf_cli/asset_planner.py:518` - In `update_assets()`, new file installations are suppressed (`to_install=[]`). If a manifest adds new files, `update` won't install them. Users must run `init` first. Document this behavior or add an `--include-new` flag.

## Suggestions (follow-up ticket)
- Consider using `requests` or `httpx` instead of `urllib.request` for better timeout handling, retry logic, and connection pooling.
- Add progress indicators for large downloads (e.g., when downloading multiple assets).
- Implement a `--dry-run` option for `tf update` to show what would be changed without applying changes.
- Add type hints for private functions (those starting with `_`) for better IDE support and documentation.
- Consider adding a configuration file option to override default timeouts and retry policies.
- Extract the chmod logic into a reusable helper function: `_make_executable(path: Path) -> None`.
- Add unit tests for error paths (network failures, permission errors, malformed URLs).
- Consider using `pathlib.Path.read_text()` and `write_text()` consistently instead of mixing with bytes operations where possible.

## Positive Notes
- Clean separation of concerns with `asset_planner.py` as the canonical implementation and `project_bundle.py` as a thin compatibility wrapper.
- Comprehensive test coverage in `tests/test_asset_planner.py` with 541 tests passing.
- Good use of dataclasses (`AssetEntry`, `AssetPlan`, `PlanResult`, `ExecutionResult`) for clear data modeling.
- Backward compatibility maintained through the `project_bundle.py` wrapper layer.
- Consistent use of `__future__ import annotations` for forward compatibility.
- Clear function documentation with docstrings explaining purpose, arguments, and return values.
- Dry-run support in `execute_plan()` for safe testing without side effects.

## Summary Statistics
- Critical: 4
- Major: 4
- Minor: 5
- Warnings: 4
- Suggestions: 8
