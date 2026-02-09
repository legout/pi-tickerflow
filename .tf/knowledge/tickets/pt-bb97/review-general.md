# Review: pt-bb97

## Overall Assessment
Well-structured implementation with comprehensive test coverage (31 tests). The board classification logic correctly implements the Ready/Blocked/In Progress/Closed rules with proper dependency handling. Code follows existing patterns in the codebase with good documentation and type hints. Minor documentation inconsistency in the module docstring should be corrected.

## Critical (must fix)
No critical issues found.

## Major (should fix)
No major issues found.

## Minor (nice to fix)
- `tf_cli/board_classifier.py:8-11` - Module docstring incorrectly states "Ready: status in {open, in_progress}" but the actual implementation only puts "open" tickets in Ready column. In Progress tickets go to IN_PROGRESS column. Update docstring to match implementation: "Ready: status == 'open' and all dependencies are closed".
- `tests/test_board_classifier.py:142-143` - Confusing comment with crossed-out thinking ("t-1 has no deps but is open, so ready? No - t-1 has no deps") should be cleaned up to just explain the test clearly.
- `tf_cli/board_classifier.py:157` - If `ticket.status` is ever None, `.lower()` will raise AttributeError. While Ticket dataclass types it as `str`, defensive handling (e.g., `status = (ticket.status or "").lower()`) would be more robust.

## Warnings (follow-up ticket)
- `tf_cli/board_classifier.py:329-335` - The `classify_tickets()` convenience function always creates a new `TicketLoader()` with default path, ignoring any custom path that might have been used to load the input tickets. If the caller loaded tickets from a non-standard location, the classifier's `TicketLoader` won't match. Consider removing the loader parameter or documenting this limitation.

## Suggestions (follow-up ticket)
- `tf_cli/board_classifier.py:205-207` - Consider adding stable sort or tie-breaker for tickets with same priority and ID prefix (e.g., add title as secondary sort) to ensure consistent ordering across classifications.
- `tf_cli/board_classifier.py:282-285` - Consider caching filtered views or adding a `memoize` parameter to avoid recomputing expensive filters on large boards.
- Consider adding a method to get blocking dependency *objects* (not just IDs) for richer UI display (showing titles of blocking tickets).

## Positive Notes
- Excellent separation of concerns between `BoardClassifier` (loading/classification) and `BoardView` (immutable queries/filters)
- Comprehensive test coverage (31 tests) with good organization into logical test classes
- Proper handling of edge cases: circular dependencies, self-referential deps, missing dependencies treated as blocking
- Clean property delegation in `ClassifiedTicket` provides ergonomic API while maintaining separation
- Case-insensitive status handling is practical and well-tested
- Sorting by priority (desc) then ID provides intuitive board ordering
- `get_by_column()` returns a copy, preserving immutability guarantees
- Search function covers ID, title, and tags - good UX thinking

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 3
- Warnings: 1
- Suggestions: 3
