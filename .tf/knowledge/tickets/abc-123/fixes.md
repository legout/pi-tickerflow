# Fixes: abc-123

## Summary
Applied fixes for 1 Major and 2 Minor issues identified in review.

## Fixes Applied

### Major (Fixed)
- `demo/hello.py:35` - Added None handling to prevent `AttributeError`
  - Changed: `if not name.strip():` → `if name is None or not name.strip():`
  - This prevents runtime crash when None is passed to the function

### Minor (Fixed)
- `demo/hello.py:30-31` - Updated docstring to document edge case behavior
  - Added: "Empty strings and whitespace-only strings fall back to 'World'."
  - This clarifies the fallback behavior in the Args section

### Minor (Skipped)
- Whitespace handling ambiguity - Intentionally preserving original behavior
  - The current behavior (preserving internal whitespace) is acceptable for demo purposes
  - Can be addressed in follow-up if needed

## Tests
All 4 existing tests pass after fixes:
- test_hello_default ✅
- test_hello_custom_name ✅
- test_hello_empty_string ✅
- test_hello_whitespace_only ✅

## Files Changed
- `demo/hello.py` - Fixed None handling and updated docstring
