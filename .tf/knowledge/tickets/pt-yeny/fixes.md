# Fixes: pt-yeny

## Issues Fixed

### Critical (1)
1. **Windows line ending bug in FRONTMATTER_PATTERN**
   - File: `tf_cli/ticket_loader.py:49`
   - Fix: Changed regex from `\n` to `\r?\n` to support both Unix (LF) and Windows (CRLF) line endings
   - Before: `r"^---\s*\n(.*?)\n---\s*\n(.*)$"`
   - After: `r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$"`

### Major (3)
2. **Basic parser numeric handling (negative integers and floats)**
   - File: `tf_cli/ticket_loader.py:252-268`
   - Fix: Replaced `value.isdigit()` with try/except for int/float parsing
   - Before: Only handled positive integers via `isdigit()`
   - After: Handles negative integers, floats, and falls back to string

3. **YAML parse failures now fallback to basic parser**
   - File: `tf_cli/ticket_loader.py:220-225`
   - Fix: Instead of returning None on YAML error, now attempts basic parser
   - Before: `logger.warning(...); return None`
   - After: `logger.warning(...); return self._basic_parse_frontmatter(...)`

4. **Body reload bug verification**
   - File: `tf_cli/ticket_loader.py:98`
   - Status: Already correct - check uses `if not self._body_loaded:` only
   - The review concern was unfounded - the code was already correct

### Additional Improvements
5. **Added tests for new functionality**
   - File: `tests/test_ticket_loader.py:51-65`
   - Added `test_parse_negative_integer` and `test_parse_float_field` tests
   - Added `test_windows_line_endings` test for frontmatter pattern
   - Total tests: 45 → 48

## Tests After Fixes
```bash
pytest tests/test_ticket_loader.py -v
```
Result: 48 tests passed (added 3 new tests for fixed functionality)

## Files Modified
- `tf_cli/ticket_loader.py` - Critical and major fixes applied
- `tests/test_ticket_loader.py` - Added tests for new functionality

## Outstanding Issues (Follow-up)
The following issues were identified but not fixed in this pass (suitable for follow-up tickets):
- ID/filename mismatch validation warning
- Missing `__all__` export list
- `count_by_status` inconsistent error handling
- No maximum file size check
- No duplicate ID validation
- No integration with ui.py yet
