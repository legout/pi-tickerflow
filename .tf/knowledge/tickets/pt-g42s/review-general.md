# Review: pt-g42s

## Overall Assessment
The implementation successfully removes the legacy shell runtime (`scripts/tf_legacy.sh`) and all associated fallback logic. Code changes are correct and thorough, with proper cleanup of imports, functions, and command handlers. The tests pass and the implementation follows the deprecation policy. However, the implementation documentation is incomplete - it doesn't list all files that were modified.

## Critical (must fix)
None - The core implementation is correct and all legacy references have been properly removed.

## Major (should fix)
- `implementation.md` - Documentation is incomplete. The files_changed.txt lists only 3 files but the actual changes include:
  - `install.sh` - Modified to remove legacy CLI installation logic (removing `ensure_global_config()` function and legacy script download/copy)
  - `config/install-manifest.txt` - Modified to remove `scripts/tf_legacy.sh`, `bin/tf`, and `config/install-manifest.txt` entries, and to update header comments
  - The research.md explicitly mentioned `install.sh` should be updated, but the implementation.md doesn't document this change
  - This incomplete documentation makes it harder to understand the full scope of changes and could confuse future maintainers

## Minor (nice to fix)
- `docs/deprecation-policy.md:84` - Minor discrepancy in line count: says "4,078 lines of bash code" but the actual file had 4,365 lines (implementation.md correctly states 4,365)
- `implementation.md` - Could be improved by listing all removal criteria that were checked (not just the completed checkbox)

## Warnings (follow-up ticket)
None

## Suggestions (follow-up ticket)
- Consider adding a git commit hook or pre-commit check to prevent re-introduction of legacy script references
- The `install.sh` help text marks `--project` as DEPRECATED - this should be tracked for actual removal in a future ticket per the deprecation policy timeline (mentioned in policy for removal on 2026-03-01)
- The `config/install-manifest.txt` header comments were improved to clarify routing - this enhancement should be documented separately as it's not strictly part of legacy removal

## Positive Notes
- Clean removal of unused imports (`urllib.request`) along with functions that used them
- Help text properly updated to remove "Legacy:\n  tf legacy <args...>" from CLI usage
- Test `test_skips_legacy_script` in `test_asset_planner.py` still passes, confirming proper behavior
- Rollback notes in implementation.md are clear and practical
- The `install.sh` changes properly mark `--project` as deprecated with clear guidance to use global install + `tf init`
- Python syntax and shell syntax checks both passed as documented
- No orphaned environment variable references (`TF_LEGACY_SCRIPT` was only in research docs, not actual code)

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 1
- Warnings: 0
- Suggestions: 3
