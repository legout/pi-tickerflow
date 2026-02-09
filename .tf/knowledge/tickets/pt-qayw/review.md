# Review: pt-qayw

## Critical (must fix)
(no critical issues found)

## Major (should fix)
- `tf_cli/ralph.py:extract_ticket_title()` returns the ticket ID as fallback when title extraction fails. This causes `ticket_title` to always be populated, potentially duplicating the `ticket` field in logs. The implementation description claims "When not provided, it is gracefully omitted" but the function never returns None or empty string. Consider returning empty string or None when extraction fails so the graceful omission actually works.

## Minor (nice to fix)
1. `tf_cli/ralph.py:extract_ticket_titles()` comment says "If a title cannot be fetched, the ticket_id is used as fallback" but the actual `extract_ticket_title()` function already does this fallback. The comment is slightly misleading.

2. `tf_cli/ralph.py:extract_ticket_title()` parsing logic may fail - the title line `# Title` typically appears BEFORE the frontmatter in the ticket format, not after.

3. `tf_cli/logger.py` - Values with spaces are wrapped in double quotes, but internal quotes are not escaped. A ticket title like `Fix "broken" parser` would produce malformed output.

## Warnings (follow-up ticket)
- No tests were added for the new `ticket_title` functionality. The implementation mentions "All existing tests pass" but new code paths have no test coverage.
- `tf_cli/ralph.py` - `extract_ticket_title()` makes a subprocess call per ticket. Consider caching results in a persistent cache for large backlogs (note: separate ticket pt-70hy covers caching).

## Suggestions (follow-up ticket)
- Consider adding a dedicated `ticket_title` formatter that truncates very long titles (e.g., >100 chars) to keep log lines readable.
- Add a helper to validate the ticket title parsing logic against actual ticket file format.

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 3
- Warnings: 2
- Suggestions: 2

## Reviewer Sources
- reviewer-general: Full review with API consistency focus
- reviewer-spec-audit: Spec compliance audit
- reviewer-second-opinion: Code quality and pattern review
