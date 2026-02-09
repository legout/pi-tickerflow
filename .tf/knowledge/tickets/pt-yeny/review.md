# Review: pt-yeny

## Critical (must fix)
- `tf_cli/ticket_loader.py:46` - **Windows line ending bug**. The frontmatter regex uses `\n` which won't match `\r\n` (CRLF). Tickets created on Windows will fail to parse silently. Fix: Use `\r?\n` in FRONTMATTER_PATTERN. (found by: reviewer-second-opinion)

## Major (should fix)
- `tf_cli/ticket_loader.py:243-268` - `_basic_parse_frontmatter()` numeric parsing bug: `value.isdigit()` returns `False` for negative integers and fails on floats. Should handle or document numeric type limitations. (found by: reviewer-general)
- `tf_cli/ticket_loader.py:101-102` - `body` property reloads from disk on every access if `_body` is empty string (falsy). Empty body is valid. Fix: check `if not self._body_loaded:` only. (found by: reviewer-general)
- `tf_cli/ticket_loader.py:177-182` - ID/filename mismatch risk: if frontmatter ID differs from filename, `_by_id` dictionary will have unexpected key. Consider adding validation warning. (found by: reviewer-second-opinion)
- `tf_cli/ticket_loader.py:220-225` - YAML parse failures silently skip tickets instead of attempting basic parser fallback. Consider trying basic parser as recovery. (found by: reviewer-second-opinion)

## Minor (nice to fix)
- `tf_cli/ticket_loader.py:1` - Missing `__all__` export list for explicit public API. (reviewer-general, reviewer-spec-audit)
- `tf_cli/ticket_loader.py:283` - `count_by_status` returns `{}` when not loaded, but other methods raise `TicketLoadError`. Inconsistent error handling. (reviewer-general)
- `tf_cli/ticket_loader.py:259` - `value.strip().strip('"\'')` removes quotes from inside strings too (e.g., `"say "hello"` becomes `say hello`). (reviewer-general)
- `tf_cli/ticket_loader.py:310-316` - Inefficient search algorithm with multiple `lower()` calls per query. Consider caching lowercase versions. (reviewer-second-opinion)
- `tf_cli/ticket_loader.py:177` - Double file read: initial load reads for frontmatter, then `ticket.body` reads again. Consider tradeoffs. (reviewer-second-opinion)
- `tests/test_ticket_loader.py:30` - Empty frontmatter test documents incorrect behavior - `---\n---\n` is valid empty YAML. (reviewer-general)

## Warnings (follow-up ticket)
- `tf_cli/ticket_loader.py:144` - No maximum file size check when reading ticket files. Malicious/corrupted files could cause memory issues. (reviewer-general)
- `tf_cli/ticket_loader.py:226-233` - No validation that ticket IDs are unique across files. Duplicate IDs silently overwrite in `_by_id`. (reviewer-general)
- `tf_cli/ticket_loader.py:1` - No integration with existing UI. Module is standalone, not used by `ui.py`. (reviewer-second-opinion)
- `tf_cli/ticket_loader.py:136-150` - Missing dependency graph methods (`get_blocked_by()`, `get_blocking()`, cycle detection). (reviewer-second-opinion)

## Suggestions (follow-up ticket)
- `tf_cli/ticket_loader.py:284-289` - Use `collections.Counter` for cleaner `count_by_status` implementation. (reviewer-general)
- `tf_cli/ticket_loader.py:245-268` - Consider TOML-like parser or `python-frontmatter` library instead of custom basic parser. (reviewer-general, reviewer-second-opinion)
- `tf_cli/ticket_loader.py:1` - Add module-level docstring with usage example. (reviewer-general)
- `tf_cli/ticket_loader.py:310` - Search could optionally include body content. (reviewer-second-opinion)
- `tf_cli/ticket_loader.py:80-85` - Add ticket validation layer for required fields and format checking. (reviewer-second-opinion)

## Positive Notes
- Excellent pattern consistency with `TopicIndexLoader` in ui.py. (reviewer-general)
- Comprehensive test coverage with 45 tests. (all reviewers)
- Clean separation of concerns between `Ticket` and `TicketLoader`. (reviewer-second-opinion)
- Thoughtful lazy loading design appropriate for UI use case. (reviewer-general)
- Graceful handling of malformed tickets and PyYAML fallback. (reviewer-second-opinion)
- Good type hints and docstrings throughout. (all reviewers)
- All acceptance criteria from ticket are met. (reviewer-spec-audit)

## Summary Statistics
- Critical: 1
- Major: 4
- Minor: 6
- Warnings: 4
- Suggestions: 5
