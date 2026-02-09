# Implementation: pt-0nqq

## Summary
Converged asset install/update flow onto one canonical planner implementation (`asset_planner.py`). All three commands (init, sync, update) now use the same underlying asset flow logic.

## Files Changed

### New Files
- `tf_cli/asset_planner.py` - Canonical asset planner with unified implementation for:
  - Manifest parsing and planning
  - Asset download and installation
  - Local vs remote source resolution
  - Bundle entry classification and routing

### Modified Files
- `tf_cli/project_bundle.py` - Refactored to use `asset_planner` as thin wrapper
- `tf_cli/init_new.py` - Updated to use `asset_planner.install_bundle()`
- `tf_cli/update_new.py` - Completely refactored to use `asset_planner` for all asset decisions
- `tf_cli/sync_new.py` - No changes needed (already uses `project_bundle.install_bundle()`)

### Updated Tests
- `tests/test_init_new.py` - Updated mocks to use `asset_planner`
- `tests/test_update_new.py` - Rewritten for new implementation using `asset_planner`
- `tests/test_asset_planner.py` - New comprehensive test suite for the canonical planner

## Key Decisions

1. **Single Planner Design**: Created `asset_planner.py` as the single source of truth for all asset operations:
   - `plan_installation()` - Plans what to install/update/skip
   - `execute_plan()` - Executes the planned operations
   - `install_bundle()` - High-level wrapper for init/sync
   - `check_for_updates()` - For update command
   - `update_assets()` - Apply updates

2. **Backward Compatibility**: `project_bundle.py` remains as a thin wrapper to maintain compatibility with existing code

3. **User-Facing Contract**: All command-line interfaces remain unchanged (init, sync, update work the same way)

## Testing
- All 541 tests pass
- New test suite covers:
  - Manifest parsing
  - Asset classification
  - Installation planning
  - Plan execution (including dry-run)
  - Update detection
  - Bundle installation
  - Error handling

## Verification
To verify the implementation works:
```bash
# Test init (installs bundle)
tf init --project /tmp/test-project

# Test sync (ensures bundle + syncs models)
tf sync --project /tmp/test-project

# Test update (checks for and applies updates)
tf update --project /tmp/test-project
```
