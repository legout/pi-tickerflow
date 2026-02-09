# Implementation: pt-g42s

## Summary
Successfully removed the legacy shell runtime path (`scripts/tf_legacy.sh`) per the deprecation policy. Updated CLI fallback wiring and documentation.

## Files Changed

### Removed
- `scripts/tf_legacy.sh` - 4,365 lines of legacy bash CLI implementation

### Modified
- `tf_cli/cli.py` - Removed `find_legacy_script()`, `run_legacy()` functions and `legacy` command handler
- `docs/deprecation-policy.md` - Updated status to "Removed", marked milestones complete

## Key Decisions

1. **Direct removal vs quarantine**: Chose direct removal per policy since:
   - Python CLI has full feature parity
   - No active code paths were invoking the legacy script
   - Git history provides rollback capability

2. **CLI fallback removal**: Removed the `tf legacy <args>` command path entirely rather than leaving a stub error message, as the deprecation policy timeline has elapsed.

3. **install.sh unchanged**: Current version of `install.sh` already had no legacy references - it only installs the Python CLI.

## Rollback Notes

If restoration is needed:
```bash
# Restore from git history
git checkout <commit-before-removal> -- scripts/tf_legacy.sh

# Restore CLI fallback (manual edit required)
# - Re-add find_legacy_script() and run_legacy() to tf_cli/cli.py
# - Re-add 'legacy' command handler
```

## Tests Run

- Python syntax check: `python -m py_compile tf_cli/cli.py` - PASSED
- Shell syntax check: `bash -n install.sh` - PASSED
- Verified legacy script no longer exists: `ls scripts/tf_legacy.sh` - NOT FOUND (expected)

## Verification

1. Legacy script removed: ✓
2. CLI fallback updated: ✓
3. Documentation updated: ✓
4. Quality checks passed: ✓
