# Implementation: pt-a51k

## Summary
Consolidated duplicated frontmatter/model-sync logic from `tf_cli/sync_new.py` and `scripts/tf_config.py` into a single shared module `tf_cli/frontmatter.py`.

## Files Changed

### Created
- `tf_cli/frontmatter.py` - New shared module containing:
  - `resolve_meta_model()` - Model resolution from config
  - `_update_frontmatter()` - Core frontmatter manipulation
  - `update_frontmatter_fields()` - Generic frontmatter updater
  - `update_agent_frontmatter()` - Agent-specific wrapper
  - `update_prompt_frontmatter()` - Prompt-specific wrapper
  - `sync_models_to_files()` - Unified sync orchestration

### Modified
- `tf_cli/sync_new.py` - Refactored to import from `tf_cli.frontmatter`:
  - Removed duplicated `resolve_meta_model()` function
  - Removed duplicated `_update_frontmatter()` function
  - Removed duplicated `update_agent_frontmatter()` function
  - Removed duplicated `update_prompt_frontmatter()` function
  - Simplified `sync_models()` to use `sync_models_to_files()`

- `scripts/tf_config.py` - Refactored to import from `tf_cli.frontmatter`:
  - Removed duplicated `resolve_meta_model()` function (~30 lines)
  - Removed duplicated `update_agent_frontmatter()` function (~28 lines)
  - Removed duplicated `update_prompt_frontmatter()` function (~28 lines)
  - Simplified `sync_models()` to use `sync_models_to_files()` (~20 lines saved)

- `.tf/scripts/tf_config.py` - Updated bundle copy with same changes

## Key Decisions

1. **Single source of truth**: All frontmatter manipulation logic now lives in `tf_cli/frontmatter.py`

2. **Backward compatibility preserved**: 
   - Function signatures remain compatible
   - Default values maintained (`openai-codex/gpt-5.1-codex-mini`, `medium`)
   - Existing tests pass without modification

3. **Improved API design**:
   - Added `update_frontmatter_fields()` for generic field updates
   - Added optional `predicate` parameter for conditional updates
   - Unified `sync_models_to_files()` works with both project-local and global installs

4. **Code reduction**:
   - Removed ~150 lines of duplicated code across files
   - Centralized logic makes future updates easier
   - Reduces risk of drift between implementations

## Tests Run
- `tests/test_sync_new.py` - 15 tests passed
- `tests/test_priority_reclassify.py` - Frontmatter-related tests passed
- `tests/test_kb_rebuild_index.py` - Frontmatter extraction tests passed
- Manual verification of `tf sync` and `scripts/tf_config.py sync-models` commands

## Verification
1. ✅ `python -m tf_cli.sync_new` runs without errors
2. ✅ `python scripts/tf_config.py sync-models` runs without errors
3. ✅ All existing tests pass
4. ✅ No behavioral changes - pure refactoring

## Acceptance Criteria
- [x] Single source of truth for frontmatter update behavior
- [x] Duplicate implementations removed or reduced to wrappers
- [x] tf sync behavior validated by tests
- [x] Config compatibility preserved
