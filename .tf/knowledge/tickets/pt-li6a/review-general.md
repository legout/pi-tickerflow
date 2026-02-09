# Review: pt-li6a

## Overall Assessment
The implementation creates a well-structured prompt for `/tf-followups-scan` that follows established patterns from other TF prompts. The dry-run by default, idempotent behavior, and comprehensive output format are all solid design choices. However, there are critical issues with model configuration that must be fixed.

## Critical (must fix)
- `.pi/prompts/tf-followups-scan.md:3` - Uses undefined meta-model key `model: tf-followups-scan`. There is no `tf-followups-scan` entry in `.tf/config/settings.json` → `metaModels`, so Pi cannot resolve this to an actual model. Should match `prompts/tf-followups-scan.md` which correctly uses `model: openai-codex/gpt-5.2`.

## Major (should fix)
- `.pi/prompts/tf-followups-scan.md` - References "Follow-up Scan" procedure in the TF Planning Skill, but SKILL.md only defines "Procedure: Follow-up Creation" (lines ~800-820). The "Follow-up Scan" procedure should be added to the skill file, or the prompt should reference an existing procedure.

## Minor (nice to fix)
- `.pi/prompts/tf-followups-scan.md` - Description in frontmatter references `+codex-mini` suffix: `[tf-planning +codex-mini]`, but the model specification uses `gpt-5.2`, not a codex-mini variant. This is inconsistent with similar prompts like `tf-followups.md` which uses consistent naming.
- Both prompt files - Consider using the meta-model key approach consistently. `settings.json` has `prompts.tf-followups-scan` undefined, but could be added to use a shared model configuration instead of hardcoding the model in two places.

## Warnings (follow-up ticket)
- None

## Suggestions (follow-up ticket)
- Consider adding the "Follow-up Scan" procedure to the TF Planning Skill documentation for completeness. The procedure is well-documented in the prompt itself but should be in the canonical skill reference.
- Consider adding a `metaModels.followups-scan` entry to `settings.json` to allow centralized model configuration, similar to other prompt types.

## Positive Notes
- Excellent dry-run default behavior with clear `--apply` flag semantics
- Idempotent design correctly skips directories with existing `followups.md`
- Comprehensive output summary format with clear statistics
- Safe config-aware approach reading `workflow.knowledgeDir` from settings
- Clear ticket description template with proper origin tracking
- Both `.pi/prompts/` and `prompts/` versions created consistently
- Follows established frontmatter pattern (description, model, thinking, skill)

## Summary Statistics
- Critical: 1
- Major: 1
- Minor: 2
- Warnings: 0
- Suggestions: 2
