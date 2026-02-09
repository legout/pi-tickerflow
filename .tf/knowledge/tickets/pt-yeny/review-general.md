# Review: pt-yeny

## Overall Assessment
Well-implemented ticket loader module following existing codebase patterns (mirrors `TopicIndexLoader` from `ui.py`). Clean separation of concerns with `Ticket` dataclass and `TicketLoader` class. Comprehensive test suite with 45 tests covering core functionality. Good use of lazy loading for performance and graceful error handling.

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf_cli/ticket_loader.py:151` - `_load_body()` re-parses frontmatter that was already parsed during `load_all()`. Consider passing parsed body offset to avoid redundant regex matching.
- `tf_cli/ticket_loader.py:203` - `_basic_parse_frontmatter()` lacks return type annotation (should be `-> dict[str, Any]`).
- `tf_cli/ticket_loader.py:289` - `count_by_status` returns empty dict when not loaded, but other methods raise `TicketLoadError`. Consider consistent behavior (either always raise or always return empty).

## Warnings (follow-up ticket)
- `tests/test_ticket_loader.py` - Test coverage gap: No tests exercise the YAML parsing path (when PyYAML is available). All frontmatter parsing tests use `_basic_parse_frontmatter()` directly. Consider mocking `HAS_YAML` or testing both paths.
- `tf_cli/ticket_loader.py:100` - `FRONTMATTER_PATTERN` doesn't match empty frontmatter (`---\n---\n`). This is acknowledged in tests but may surprise users with empty frontmatter tickets.
- `tf_cli/ticket_loader.py:45` - Ticket ID defaults to `file_path.stem` when frontmatter lacks `id` field, but no validation ensures this matches expected ID format. Could cause inconsistencies.

## Suggestions (follow-up ticket)
- `tf_cli/ticket_loader.py:164-177` - Consider adding a `reload()` method to refresh tickets without creating new loader instance (useful for long-running UI).
- `tf_cli/ticket_loader.py:288-296` - Consider caching `count_by_status` result or computing it during `load_all()` to avoid O(n) scan on each access.
- `tf_cli/ticket_loader.py:131` - Consider adding file modification time tracking to enable selective reloading of changed tickets only.

## Positive Notes
- Clean dataclass design with `field(default_factory=list)` for mutable defaults - correct pattern.
- Excellent docstrings following Google style with Args/Returns/Raises sections.
- Good use of `Optional[str]` type hints throughout.
- Smart lazy loading implementation with `_body_loaded` flag to prevent redundant disk reads.
- Graceful degradation when PyYAML not available - basic parser handles common cases.
- Comprehensive error handling with custom `TicketLoadError` exception.
- Test fixtures are well-structured with `tmp_tickets_dir` providing realistic test data.
- Pattern consistency with existing `TopicIndexLoader` (same method names, similar structure) makes codebase cohesive.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 3
- Warnings: 3
- Suggestions: 3
