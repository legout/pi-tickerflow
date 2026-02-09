# Research: pt-g42s - Remove legacy shell runtime path

## Status
Research completed. Legacy script identified and all references mapped.

## Rationale
Per the deprecation policy, `scripts/tf_legacy.sh` should be removed or isolated. The Python CLI modules are now fully functional and supersede the legacy bash implementation.

## Context Reviewed

### 1. Legacy Script Location
- **Path**: `scripts/tf_legacy.sh`
- **Size**: ~4,266 lines of bash
- **Purpose**: Original monolithic CLI implementation (ralph, agentsmd, seed, track, next, backlog-ls, login, sync, update, doctor)

### 2. Current State
- Python CLI modules in `tf_cli/` are fully functional
- `tf_cli/cli.py` has `legacy` command that calls `run_legacy()` → executes `tf_legacy.sh`
- `find_legacy_script()` searches multiple locations:
  - `$TF_LEGACY_SCRIPT` env var
  - `.tf/scripts/tf_legacy.sh` (local)
  - `~/.tf/scripts/tf_legacy.sh` (global)
  - `scripts/tf_legacy.sh` (repo)

### 3. Files Referencing tf_legacy.sh

#### Must Update (in-repo):
1. `tf_cli/cli.py` - Remove `find_legacy_script()`, `run_legacy()`, and `legacy` command
2. `install.sh` - Remove legacy CLI download/copy logic (lines ~22-35, ~182-198)
3. `docs/deprecation-policy.md` - Update status to "Removed"

#### May Reference (worktrees - out of scope):
- `.tf/ralph/worktrees/*/install.sh` - Historical copies
- `.tf/ralph/worktrees/*/tf_cli/cli.py` - Historical copies

### 4. Deprecation Policy Timeline
- **Deprecated**: 2026-02-07
- **Removal Date**: 2026-04-01
- **Status**: Ready for removal per policy

### 5. Rollback Plan
- Legacy script can be restored from git history if needed
- Document rollback steps in implementation notes

## Implementation Plan
1. Remove `scripts/tf_legacy.sh`
2. Update `tf_cli/cli.py` - Remove legacy fallback
3. Update `install.sh` - Remove legacy CLI installation
4. Update `docs/deprecation-policy.md` - Mark as removed
5. Document rollback procedure

## Sources
- `tk show pt-g42s`
- `scripts/tf_legacy.sh` (content analysis)
- `tf_cli/cli.py` (fallback logic)
- `install.sh` (installation logic)
- `docs/deprecation-policy.md` (policy compliance)
