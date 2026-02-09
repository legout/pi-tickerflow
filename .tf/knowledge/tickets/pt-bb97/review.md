# Review: pt-bb97

## Overall Assessment

Well-structured implementation with comprehensive test coverage (31 tests). The board classification logic correctly implements the Ready/Blocked/In Progress/Closed rules with proper dependency handling. Code follows existing patterns in the codebase with good documentation and type hints.

All three reviewers agree: No Critical or Major issues. The implementation fully complies with the plan requirements and is ready to merge after minor fixes.

## Critical (must fix)

No critical issues found.

## Major (should fix)

No major issues found.

## Minor (nice to fix)

1. **tf_cli/board_classifier.py:8-11** - Module docstring incorrectly states "Ready: status in {open, in_progress}" but actual implementation only puts "open" tickets in Ready column. Update docstring to match implementation.

2. **tf_cli/board_classifier.py:157** - Defensive handling if `ticket.status` is None would be more robust. Suggest: `status = (ticket.status or "").lower()`

3. **tf_cli/board_classifier.py:329-335** - `classify_tickets()` convenience function creates unused `TicketLoader()`. Refactor to avoid unnecessary instantiation.

4. **tf_cli/board_classifier.py:88-93** - `_loaded` attribute is set but never used. Remove dead code or add guards to prevent stale data access.

5. **tests/test_board_classifier.py:142-143** - Confusing crossed-out comment should be cleaned up for clarity.

## Warnings (follow-up ticket)

1. **tf_cli/board_classifier.py:122-124** - Unknown status defaults to Ready without explicit spec documentation.

2. **tf_cli/board_classifier.py:329-335** - `classify_tickets()` function always creates `TicketLoader()` with default path, ignoring custom paths used to load input tickets.

3. **tf_cli/board_classifier.py:1** - Consider adding `__all__` export list for explicit public API definition (codebase-wide pattern).

## Suggestions (follow-up ticket)

1. **tf_cli/board_classifier.py:205-207** - Consider stable sort tie-breaker for same priority/ID.

2. **tf_cli/board_classifier.py:282-285** - Consider caching for expensive filters on large boards.

3. **tf_cli/board_classifier.py:139-140** - Consider adding optional cycle detection/logging for circular dependencies.

4. Add method to get blocking dependency *objects* (not just IDs) for richer UI display.

5. Add explicit test for "closing the last dependency moves ticket from Blocked to Ready" scenario.

## Positive Notes (All Reviewers)

- **Excellent separation of concerns**: `BoardClassifier` (loading/classification), `BoardView` (immutable queries), `ClassifiedTicket` (wrapper)
- **Comprehensive test coverage**: 31 tests covering classification rules, dependency graphs, edge cases
- **Clean implementation**: Follows existing patterns, good docstrings, type hints
- **Proper edge case handling**: Circular dependencies, self-referential deps, missing deps
- **Case-insensitive status handling**: Practical and well-tested
- **Immutability by design**: Returns copies, prevents accidental mutation
- **Spec compliance**: All four board column rules correctly implemented per plan

## Summary Statistics

- Critical: 0
- Major: 0
- Minor: 5
- Warnings: 3
- Suggestions: 5

## Sources

- review-general.md
- review-spec.md  
- review-second.md
