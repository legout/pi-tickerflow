# Review: pt-a51k

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)

1. **`tf_cli/frontmatter.py:118-166`** - `update_agent_frontmatter()` and `update_prompt_frontmatter()` are nearly identical (only variable names differ). Consider unifying into a single internal helper that both call, or document why the duplication is intentional for API clarity. *(from reviewer-general)*

2. **`tf_cli/frontmatter.py:36-37`** - When returning a meta-model directly (name is a key in metaModels), the function returns the raw dict without validating it contains 'model' and 'thinking' keys. While callers use `.get()` with defaults, inconsistent meta-model definitions could cause confusing behavior. Consider validating the returned dict has expected keys or document that meta-models MUST include both fields. *(from reviewer-second-opinion)*

3. **`tf_cli/frontmatter.py:82`** - The `_update_frontmatter()` function silently returns unchanged content if no frontmatter block is found (no regex match). For a sync operation, this could mask files that should have been updated but weren't due to malformed frontmatter. Consider adding a warning or returning an indicator when no frontmatter is found. *(from reviewer-second-opinion)*

## Warnings (follow-up ticket)

1. **`tf_cli/frontmatter.py:62`** - The regex pattern `^(---\s*\n)` uses `^` anchor which with `re.DOTALL` only matches start of string, but doesn't handle Windows line endings (`\r\n`). If this codebase needs to support Windows contributors, consider making the pattern handle both line ending styles with `\r?\n`. *(from reviewer-second-opinion)*

## Suggestions (follow-up ticket)

1. **`tf_cli/frontmatter.py:68-81`** - The `_update_frontmatter()` function uses regex for frontmatter parsing. Consider adding a simple YAML parser fallback or validation for edge cases like nested YAML structures in frontmatter, though the current implementation handles the simple key-value case correctly. *(from reviewer-general)*

2. **Testing** - Consider adding dedicated unit tests for `tf_cli/frontmatter.py` to test edge cases (e.g., malformed frontmatter, missing fields, predicate functionality). *(from reviewer-spec-audit)*

3. **Worktree cleanup** - Consider deprecating/removing the duplicate implementations in `.tf/ralph/worktrees/pt-gzqg/` once that ticket completes, to avoid confusion. *(from reviewer-spec-audit)*

4. **`tf_cli/frontmatter.py:48`** - Consider adding a `validate_frontmatter()` helper that checks frontmatter has required fields before sync. This could provide better error messages when agent/prompt files have malformed frontmatter. *(from reviewer-second-opinion)*

5. **`tf_cli/frontmatter.py:215-225`** - The `sync_models_to_files()` function could benefit from returning files that were skipped (no changes needed) separately from files that were updated, for more detailed reporting. Currently the caller can't distinguish between "already up to date" and "doesn't exist". *(from reviewer-second-opinion)*

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 3
- Warnings: 1
- Suggestions: 5

## Reviewers
- reviewer-general
- reviewer-spec-audit
- reviewer-second-opinion
