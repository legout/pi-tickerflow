# Fixes: pt-bb97

## Summary

All 5 minor issues from the review have been addressed. No Critical or Major issues were found.

## Changes Made

### 1. Fixed Module Docstring (tf_cli/board_classifier.py:8-11)

**Issue**: Docstring incorrectly stated "Ready: status in {open, in_progress}" but actual implementation only puts "open" tickets in Ready column.

**Fix**: Updated docstring to accurately reflect the classification rules:
```python
# Before:
- Ready: status in {open, in_progress} and all dependencies are closed

# After:
- Ready: status == "open" and all dependencies are closed
```

Also clarified that Closed status is applied "regardless of dependencies".

### 2. Defensive Status Handling (tf_cli/board_classifier.py:170)

**Issue**: If `ticket.status` is None, `.lower()` would raise AttributeError.

**Fix**: Added defensive handling:
```python
# Before:
status = ticket.status.lower()

# After:
status = (ticket.status or "").lower()
```

### 3. Removed Unused _loaded Attribute (tf_cli/board_classifier.py:115, 157)

**Issue**: `_loaded` attribute was set but never checked or used (dead code).

**Fix**: Removed the unused attribute initialization and assignment:
```python
# Removed from __init__:
self._loaded = False

# Removed from _classify_tickets:
self._loaded = True
```

### 4. Fixed classify_tickets() Wasteful Instantiation (tf_cli/board_classifier.py:356-373)

**Issue**: `classify_tickets()` convenience function created unused `TicketLoader()`.

**Fix**: Use `__new__` to create classifier without calling `__init__`:
```python
# Before:
classifier = BoardClassifier(loader=TicketLoader())
return classifier._classify_tickets(tickets)

# After:
classifier = BoardClassifier.__new__(BoardClassifier)
return classifier._classify_tickets(tickets)
```

### 5. Cleaned Up Confusing Comment (tests/test_board_classifier.py:175-176)

**Issue**: Comment contained crossed-out thinking that was confusing.

**Fix**: Replaced with clear explanation:
```python
# Before:
# All blocked (t-1 has no deps but is open, so ready? No - t-1 has no deps)
# Actually t-1 has no deps, so it should be READY

# After:
# t-1 is READY (no deps, open status), t-2 and t-3 are BLOCKED by upstream deps
```

## Verification

All tests pass after fixes:
```
31 passed in tests/test_board_classifier.py
889 passed in full test suite
```

## Warnings Not Addressed

The following warnings were intentionally not addressed as they require broader design decisions or are codebase-wide patterns:

1. **Unknown status defaults to Ready** - Conservative default behavior; changing would require spec update
2. **classify_tickets() ignores custom paths** - Documented limitation of convenience function
3. **Consider adding __all__ export list** - Codebase-wide pattern to address separately

## Suggestions for Future Work

These suggestions were noted but not implemented as they are enhancements rather than fixes:

- Add stable sort tie-breaker for same priority/ID
- Consider caching for expensive filters on large boards  
- Add optional cycle detection/logging for circular dependencies
- Add method to get blocking dependency objects (not just IDs)
- Add explicit test for "closing the last dependency moves ticket from Blocked to Ready"
