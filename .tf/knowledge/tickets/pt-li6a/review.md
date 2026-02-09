# Review: pt-li6a

## Critical (must fix)

1. **`.pi/prompts/tf-followups-scan.md:3` - Undefined meta-model key**
   - Uses `model: tf-followups-scan` but this meta-model is NOT registered in `.tf/config/settings.json` → `metaModels`
   - Pi cannot resolve this to an actual model
   - Fix: Register in settings.json prompts section OR use concrete model like `openai-codex/gpt-5.2`

2. **`.tf/config/settings.json` - Missing prompt registration**
   - The prompt `tf-followups-scan` is not registered in the `prompts` section
   - Pi won't recognize the `/tf-followups-scan` command
   - Fix: Add `"tf-followups-scan": "planning"` to settings.json prompts section

3. **Non-existent procedure reference**
   - References "Follow the **TF Planning Skill** 'Follow-up Scan' procedure"
   - This procedure does NOT exist in `.pi/skills/tf-planning/SKILL.md`
   - Only "Follow-up Creation" procedure exists
   - Fix: Add the procedure to the skill OR inline the steps in the prompt

## Major (should fix)

4. **Inconsistent model references between prompt files**
   - `.pi/prompts/tf-followups-scan.md` uses `model: tf-followups-scan` (meta-model)
   - `prompts/tf-followups-scan.md` uses `model: openai-codex/gpt-5.2` (concrete)
   - Both should use the same approach for maintainability

5. **Wrong eligibility heuristic**
   - Implementation checks for `review.md` existence
   - Spec requires detecting "implemented/closed" tickets using `close-summary.md` existence
   - These are different signals - a ticket can have a review without being closed/implemented

6. **Missing flags from spec**
   - `--json` flag for structured output (CI/automation friendly) not implemented
   - `--stop-on-error` flag for strict mode when `tk create` fails not implemented

## Minor (nice to fix)

7. **Inconsistent description format**
   - Root-level copy missing `[tf-planning +codex-mini]` annotation in description
   - Both files should have consistent frontmatter formatting

8. **Terminology inconsistency in output**
   - Summary shows `Marked as "none needed": {N}` but dry-run message says "Would mark {ticket-id} as processed (no follow-ups needed)"
   - Align terminology for clarity

9. **Summary tracking issue**
   - Summary output shows `Skipped: {N} tickets` but skip rules don't track skipped count separately

## Warnings (follow-up ticket)

10. **`followups.md` artifact format compliance**
    - Spec defines specific format with "Created Tickets" and "Skipped Items" sections, timestamps, source references
    - Implementation description is vague about actual file content format

11. **No dedup mechanism for tickets**
    - MVP relies only on `followups.md` presence without stronger dedup (e.g., source review hash)

## Suggestions (follow-up ticket)

12. Add `--limit` or `--max` flag to prevent accidentally creating too many tickets
13. Add `--filter` option to only process specific severity levels
14. Add error handling guidance for partial `tk create` failures
15. Consider adding `metaModels.followups-scan` entry for centralized model configuration

## Positive Notes

- Excellent dry-run default behavior with clear `--apply` flag semantics
- Idempotent design correctly skips directories with existing `followups.md`
- Comprehensive output summary format with clear statistics
- Safe config-aware approach reading `workflow.knowledgeDir` from settings
- Clear ticket description template with proper origin tracking
- Both `.pi/prompts/` and `prompts/` versions created consistently
- Follows established frontmatter pattern
- Clear separation of dry-run vs apply mode behavior

## Summary Statistics
- Critical: 3
- Major: 3
- Minor: 3
- Warnings: 2
- Suggestions: 4

## Source Reviewers
- reviewer-general: Critical (1), Major (1), Minor (2)
- reviewer-spec-audit: Critical (1), Major (3), Minor (4), Warnings (2), Suggestions (2)
- reviewer-second-opinion: Critical (2), Major (2), Minor (2), Warnings (1), Suggestions (3)
