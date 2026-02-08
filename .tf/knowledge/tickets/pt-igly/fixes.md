# Fixes: pt-igly

## Issues Fixed

### Critical (1)
1. **Wrong tickets directory path** - Changed from `.tf/tickets` to `.tickets/` at project root to match actual project structure.

### Major (3)
1. **Unused import** - Removed `subprocess` import (was not used).
2. **Fragile frontmatter parsing** - Replaced substring matching with proper regex-based parsing using `FRONTMATTER_PATTERN`. Now correctly extracts status and deps fields from YAML frontmatter without false positives from body text.
3. **Incorrect "ready" logic** - Fixed to count tickets as "ready" only when status is "open" AND deps list is empty (has no dependencies).

### Minor improvements
- Changed file I/O to read only first 2KB of files for frontmatter parsing (efficient)
- Added logging instead of silent exception swallowing
- Changed project root detection to use `for parent in [cwd, *cwd.parents]` pattern (consistent with codebase)
- Added `_parse_frontmatter_status()` helper for clean separation

## Verification
```bash
python tf_cli/workflow_status.py
```

**Before fixes:**
- Open: 0, Ready: 0, Closed: 0 (incorrect - wrong directory)

**After fixes:**
- Open: 3, Ready: 1, Closed: 133 (correct)

## Changed Files
- `tf_cli/workflow_status.py` - Applied all fixes
