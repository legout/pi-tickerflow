# Implementation: ptw-n2s4

## Summary
Established VERSION file as the canonical version source of truth and created a sync mechanism for package.json. The project already had most of the infrastructure in place; this implementation added the missing sync script and updated documentation.

## Files Changed

### New Files
- `scripts/sync-version.sh` - Bash script to sync version from VERSION file to package.json
  - Reads VERSION file from repo root
  - Uses `npm version` to update package.json
  - Handles case where npm is not installed

### Modified Files
- `package.json` - Added `version:sync` npm script
  - Added `"version:sync": "./scripts/sync-version.sh"` to scripts section
  - Reformatted by npm (added newlines between keys)

- `VERSIONING.md` - Updated references to sync script
  - Changed release checklist step 3 to use `./scripts/sync-version.sh`
  - Updated Quick Commands section to show proper bump workflow

## Key Decisions

1. **Kept VERSION as canonical source** - It was already documented and pyproject.toml already reads from it dynamically
2. **Created sync script instead of dynamic reading** - package.json cannot dynamically read from external files, so a sync script is the lightweight solution
3. **Used npm version command** - This ensures package.json is properly formatted and version is validated

## Verification

```bash
# Verify sync script works
./scripts/sync-version.sh
# Output: Syncing version: 0.1.0
#         v0.1.0
#         ✓ package.json updated
#         Version sync complete: 0.1.0

# Verify all files consistent
cat VERSION                    # 0.1.0
npm run version:sync           # syncs package.json
grep '"version"' package.json  # "version": "0.1.0"
```

## Notes

- pyproject.toml already used dynamic version loading from VERSION file
- tf_cli/version.py already provides runtime version access
- No breaking changes - all existing workflows continue to work
