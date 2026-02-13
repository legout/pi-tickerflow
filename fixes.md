Done! I've completed the fix task for abc-123:

**Summary:**
- **Critical: 0** - No fixes needed
- **Major: 0** - No fixes needed (the one listed was noting correct implementation)
- **Minor: 5** - All addressed

**Changes made:**
1. `demo/hello.py` - Updated docstring to accurately describe whitespace collapsing behavior and added note about CLI TypeError behavior
2. `tests/test_demo_hello.py` - Added new test `test_hello_internal_whitespace_normalized()` that explicitly pins the internal whitespace normalization behavior

**Tests:** All 13 tests pass (was 12, now 13 with the new test)

The fixes are written to `/home/volker/coding/pi-ticketflow/fixes.md` with follow-up ticket recommendations for the Warnings and Suggestions.