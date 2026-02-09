# Close Summary: pt-6q53

## Status
CLOSED

## Summary
Successfully implemented `tf kb rebuild-index` command to regenerate `index.json` from filesystem.

## Implementation Details

### Changes Made
1. **tf_cli/kb_cli.py**
   - Added `cmd_rebuild_index()` function with dry-run and JSON output support
   - Added `_extract_title_from_frontmatter()` helper for title extraction
   - Updated `usage()` to document the new command
   - Updated `main()` to parse `--dry-run` flag and dispatch command

2. **tests/test_kb_rebuild_index.py** (new file)
   - 14 comprehensive tests covering:
     - Title extraction from frontmatter and headings
     - Dry-run mode with text and JSON output
     - Index creation and stable ordering by ID
     - Metadata preservation from existing index
     - Stale path removal
     - Error handling

### Features
- ✅ Scans `.tf/knowledge/topics/*` directories
- ✅ Produces canonical index entries with stable ordering by topic ID
- ✅ `--dry-run` flag prints changes without writing
- ✅ `--json` flag for programmatic output
- ✅ Atomic writes using `atomic_write_index()` helper
- ✅ Preserves existing metadata (keywords, custom fields)
- ✅ Extracts titles from frontmatter or markdown headings
- ✅ Removes stale file path references

### Test Results
All 295 tests pass:
- 33 tests in test_kb_helpers.py
- 14 new tests in test_kb_rebuild_index.py
- 248 other existing tests

## Commit
`2a8195f` pt-6q53: Implement tf kb rebuild-index (--dry-run)

## Verification
```bash
# Dry-run mode
$ tf kb rebuild-index --dry-run
Dry-run: Would rebuild index at .tf/knowledge/index.json
  Current topics: 7
  New topics: 7
  Unchanged (7): ...

# Actual rebuild
$ tf kb rebuild-index
Rebuilt index: 7 topics

# Validate
$ tf kb validate
Knowledge base validation: PASSED
```
