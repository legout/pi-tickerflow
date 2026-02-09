# Review: ptw-azum

## Overall Assessment
The component classifier implementation is well-structured, thoroughly tested, and follows project conventions. It provides a clean API with sensible defaults and good extensibility. All acceptance criteria are met.

## Critical (must fix)
- No critical issues found.

## Major (should fix)
- No major issues found.

## Minor (nice to fix)
- `tf_cli/component_classifier.py:190-191` - The `suggest_tags_for_ticket()` function uses subprocess to call `tk show`. Consider documenting the expected `tk` CLI format or adding a fallback if the format changes.
- `tf_cli/component_classifier.py:98` - The `min_confidence` parameter is accepted but unused. Either implement confidence scoring or remove the parameter to avoid confusion.

## Warnings (follow-up ticket)
- `tf_cli/component_classifier.py:77` - `json` module is imported inside a function for regex matching. Consider moving to top-level for consistency, though this is a minor style issue.
- The classifier doesn't handle stemming or word variations (e.g., "testing" vs "test" both match, but "document" vs "documentation" might not depending on keyword list). This is acceptable for MVP but could be enhanced.

## Suggestions (follow-up ticket)
- Consider adding support for loading custom keyword mappings from a config file (e.g., `.tf/config/component-keywords.json`).
- Could add a confidence threshold that requires multiple keyword matches before assigning a tag.
- Consider caching ticket fetches when processing multiple tickets in batch.

## Positive Notes
- Excellent test coverage with 24 tests covering normal cases, edge cases, and error conditions.
- Clean separation of concerns: core logic in `component_classifier.py`, CLI in `tags_suggest_new.py`.
- Good documentation with docstrings, type hints, and generated markdown docs.
- Follows existing project patterns for CLI structure.
- The `ClassificationResult` dataclass is well-designed with boolean coercion support.
- Keyword merging logic (custom + defaults) is intuitive and well-tested.
- CLI commands follow consistent patterns with `--json` and `--rationale` flags.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 2
- Warnings: 2
- Suggestions: 3
