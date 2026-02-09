# Review (Spec Audit): pt-yeny

## Overall Assessment
The implementation successfully meets all acceptance criteria from the ticket. The ticket loader parses YAML frontmatter correctly, extracts markdown titles, supports lazy body loading, and handles malformed tickets gracefully without crashing.

## Critical (must fix)
None - all acceptance criteria are met.

## Major (should fix)
None.

## Minor (nice to fix)
- `tf_cli/ticket_loader.py:1` - Module could use a `__all__` export list for cleaner public API

## Warnings (follow-up ticket)
- `tf_cli/ticket_loader.py:45` - `Ticket` dataclass stores file_path but not directory path; if tickets are moved after loading, lazy body loading will fail. Consider if this is a concern for the UI use case.

## Suggestions (follow-up ticket)
- `tests/test_ticket_loader.py:1` - Add integration test that loads actual tickets from `.tickets/` directory
- `tf_cli/ticket_loader.py:150` - Consider adding a `reload()` method to refresh ticket metadata without recreating the loader

## Positive Notes
- All acceptance criteria correctly implemented:
  - ✓ Parses YAML frontmatter fields (id, status, deps, tags, assignee, external-ref)
  - ✓ Extracts markdown title (first # heading)
  - ✓ Supports lazy loading of body content
  - ✓ Malformed tickets skipped with warnings (no crash)
- ✓ No per-ticket `tk show` subprocess calls (direct file reading)
- ✓ Clean separation of concerns with Ticket and TicketLoader classes
- ✓ Comprehensive test coverage (45 tests)
- ✓ Follows existing TopicIndexLoader pattern from ui.py

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 1
- Suggestions: 2

## Spec Coverage
- Spec/plan sources consulted: `tk show pt-yeny`
- Missing specs: none - all requirements from ticket are covered
