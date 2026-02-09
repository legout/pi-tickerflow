# Review (Second Opinion): pt-yeny

## Overall Assessment
The implementation is well-structured and follows established codebase patterns from `TopicIndexLoader`. The lazy loading design is appropriate for the UI performance requirements. Code is clean with good separation of concerns between `Ticket` (data) and `TicketLoader` (operations). Most issues are minor edge cases or consistency improvements.

## Critical (must fix)
No critical issues found.

## Major (should fix)
No major issues found.

## Minor (nice to fix)
- `tf_cli/ticket_loader.py:189` - `count_by_status` returns empty dict when not loaded, but other methods raise `TicketLoadError`. Inconsistent error handling pattern - should raise for consistency with `get_by_id()`, `search()`, etc.
- `tf_cli/ticket_loader.py:164` - `Ticket._body` and `Ticket._body_loaded` fields are redundant. Since `None` is a valid loaded state (file not found), the boolean flag is necessary - but this could be cleaner with a sentinel value pattern or enum to track load states.
- `tf_cli/ticket_loader.py:369` - The `_basic_parse_frontmatter()` method doesn't handle nested list syntax like `[item, [nested]]` or multiline strings. Given this is a fallback parser, this is acceptable but should be documented.
- `tests/test_ticket_loader.py:15-23` - `test_empty_frontmatter()` expects `None` for empty frontmatter (`---\n---\n`), which means such tickets are skipped. This is intentional strict behavior, but consider if empty frontmatter should be treated as valid (empty dict) instead.

## Warnings (follow-up ticket)
- `tf_cli/ticket_loader.py:54-55` - `_body` and `_body_loaded` dataclass fields use `repr=False` which is good for hiding internals, but `file_path: Path` is included in repr and may leak absolute paths in logs. Consider `repr=False` for `file_path` too.
- `tf_cli/ticket_loader.py:306` - `FRONTMATTER_PATTERN` regex `r"^---\s*\n(.*?)\n---\s*\n(.*)$"` doesn't allow whitespace before the opening `---`. Files with indentation or leading spaces on the first line won't match. Unlikely but possible edge case.
- `tf_cli/ticket_loader.py:1` - Module docstring says "This module provides efficient loading of ticket metadata from `.tickets/*.md` files" but the actual directory resolution looks for `.tf` directory to find repo root, then appends `.tickets`. The docstring oversimplifies the resolution logic.

## Suggestions (follow-up ticket)
- `tf_cli/ticket_loader.py:77` - Consider adding `__slots__` to the `Ticket` dataclass for memory efficiency when loading hundreds of tickets. With `@dataclass(slots=True)` (Python 3.10+), memory usage drops significantly for many instances.
- `tf_cli/ticket_loader.py:164` - Add a `refresh()` or `reload()` method to `TicketLoader` to clear cached tickets and reload from disk. Useful for long-running UI processes where tickets may change.
- `tf_cli/ticket_loader.py:28` - Consider exporting `Ticket` and `TicketLoader` in `tf_cli/__init__.py` for cleaner imports: `from tf_cli import TicketLoader` instead of `from tf_cli.ticket_loader import TicketLoader`.
- Consider adding type hints for `frontmatter` dict return values (currently `Optional[dict]` which is equivalent to `Optional[dict[Any, Any]]`). A `TypedDict` for ticket frontmatter fields would improve type safety.

## Positive Notes
- **Clean separation of concerns**: `Ticket` dataclass handles lazy body loading, `TicketLoader` handles file operations. Matches the `Topic`/`TopicIndexLoader` pattern in `ui.py` well.
- **Robust error handling**: Malformed tickets are skipped with warnings rather than crashing the entire load operation. File read errors during lazy loading gracefully return empty body.
- **Good test coverage**: 45 tests covering frontmatter parsing, title extraction, lazy loading, filtering, and error cases.
- **Performance-conscious design**: Eager loading of metadata with lazy body loading is exactly right for the UI use case with ~100s of tickets.
- **Thoughtful fallback**: Basic frontmatter parser when PyYAML unavailable ensures the code works in minimal environments.
- **Consistent API design**: Filter methods (`get_by_status`, `get_by_tag`, `get_by_assignee`) follow same pattern with consistent error handling.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 4
- Warnings: 3
- Suggestions: 4
