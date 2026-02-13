# Review: pt-lw9p

## Critical (must fix)
- No issues found

## Major (should fix)
- `tf/frontmatter.py:45` - The fallback for missing meta-models returns `{"model": name, "thinking": "medium"}` which uses the **agent name** (`name`) instead of the **meta-model key** (`meta_key`). This contradicts the accompanying comment and would produce an unexpected model ID if an agent's mapping value differs from its name.
- `.tf/knowledge/tickets/pt-lw9p/design-fixer-model-selection.md:153-157` - The document states that when the meta-model is missing, the base model becomes `None`, but earlier in the same doc it states fallback is literal `"fixer"`.
- `tests/test_sync.py` - Missing test coverage for fallback path that the new design doc highlights.

## Minor (nice to fix)
- None

## Warnings (follow-up ticket)
- No issues found

## Suggestions (follow-up ticket)
- Add configuration validation (e.g., during `tf sync` or `tf init`) to warn when an agent's `agents.<name>` mapping points to a non-existent `metaModels` key.

## Summary Statistics
- Critical: 0
- Major: 3
- Minor: 0
- Warnings: 0
- Suggestions: 1
