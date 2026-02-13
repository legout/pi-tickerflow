# Fixes: pt-lw9p

## Summary
Fixed code bugs and documentation inconsistencies identified in code review.

## Fixes by Severity

### Critical (must fix)
- [x] No critical issues found

### Major (should fix)
- [x] `tf/frontmatter.py:45` - Fixed bug where fallback used `name` (agent name) instead of `meta_key` (meta-model key). This would cause incorrect model resolution when agent name differs from meta-model key (e.g., `agents.fixer="custom-fixer"` would fallback to model "fixer" instead of "custom-fixer").
- [x] `tf/frontmatter.py:52` - Same fix applied to prompts fallback.
- [x] `.tf/knowledge/tickets/pt-lw9p/design-fixer-model-selection.md:153-157` - Fixed contradiction in "Base Model Resolution for Escalation" section. Now correctly states that when meta-model is missing, the base model becomes the meta-model key itself (literal model ID), not `None`.

### Minor (nice to fix)
- [x] `tests/test_sync.py` - Added comprehensive test coverage for fallback behavior:
  - `test_fallback_when_meta_model_missing` - Documents actual fallback behavior
  - `test_fallback_uses_meta_key_not_agent_name` - Tests the bug that was fixed
  - `test_resolves_via_prompts_map` - Prompt resolution coverage
  - `test_prompt_fallback_when_meta_model_missing` - Prompt fallback coverage

### Warnings (follow-up)
- [ ] No issues fixed (deferred)

### Suggestions (follow-up)
- [ ] Consider adding config validation during `tf sync` to warn when agent mappings point to non-existent meta-models (noted for future improvement).

## Summary Statistics
- **Critical**: 0
- **Major**: 3 (all fixed)
- **Minor**: 1 (test coverage added)
- **Warnings**: 0
- **Suggestions**: 0

## Files Changed
- `tf/frontmatter.py` - Fixed fallback bug to use `meta_key` instead of `name`
- `tests/test_sync.py` - Added 4 new test cases for fallback behavior
- `.tf/knowledge/tickets/pt-lw9p/design-fixer-model-selection.md` - Fixed contradiction in escalation section

## Verification
- All 6 tests in `TestResolveMetaModel` pass
- Code behavior now matches documented behavior
