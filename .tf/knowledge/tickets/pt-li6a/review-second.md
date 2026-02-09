# Review (Second Opinion): pt-li6a

## Overall Assessment
The implementation creates two prompt files for `/tf-followups-scan` with good structure and clear documentation. However, there are critical issues with missing configuration, inconsistent model references, and a non-existent procedure reference that would prevent the command from functioning properly.

## Critical (must fix)
- `.pi/prompts/tf-followups-scan.md:3` - Uses `model: tf-followups-scan` but this meta-model is **not registered** in `.tf/config/settings.json` under the `prompts` section. This will cause model resolution to fail when the command is invoked.
- `.pi/prompts/tf-followups-scan.md:33` - References "Follow the **TF Planning Skill** 'Follow-up Scan' procedure" but this procedure **does not exist** in `.pi/skills/tf-planning/SKILL.md`. Only "Follow-up Creation" exists. The skill needs to be updated with the new procedure, or the prompt needs to inline the procedure steps.

## Major (should fix)
- `prompts/tf-followups-scan.md:3` - Root-level copy uses `model: openai-codex/gpt-5.2` directly instead of `model: tf-followups-scan`. This is inconsistent with the `.pi/prompts/` version and bypasses the meta-model system. Both copies should use the same meta-model reference for maintainability.
- `prompts/tf-followups-scan.md:2` - Root-level copy missing the `[tf-planning +codex-mini]` annotation in the description that exists in the `.pi/prompts/` version, making the two files inconsistently formatted.

## Minor (nice to fix)
- `.pi/prompts/tf-followups-scan.md:46` - The output summary format shows `Marked as "none needed": {N}` but the dry-run message says "Would mark {ticket-id} as processed (no follow-ups needed)". The terminology is inconsistent ("none needed" vs "processed"). Consider aligning these for clarity.
- `.pi/prompts/tf-followups-scan.md:50` - Summary output shows `Skipped: {N} tickets (already have followups.md)` but the skip rules in section 4 don't actually count skipped tickets separately - they just skip them. Need to track skipped count during scan.

## Warnings (follow-up ticket)
- `.pi/prompts/tf-followups-scan.md:1` - The prompt references `skill: tf-planning` but implements a new "Follow-up Scan" procedure that doesn't exist in the skill. Consider whether this should be:
  1. Added to the tf-planning skill (preferred)
  2. Made a standalone skill if it's complex enough
  3. Inlined in the prompt if it's simple enough

## Suggestions (follow-up ticket)
- Consider adding a `--limit` or `--max` flag to prevent accidentally creating too many tickets in a single run when there are many reviews with warnings/suggestions.
- Consider adding a `--filter` option to only process specific severity levels (e.g., only Warnings but not Suggestions).
- The prompt could benefit from error handling guidance (e.g., what to do if `tk create` fails for one item but succeeds for others).

## Positive Notes
- Dry-run by default is the correct safe default - prevents accidental ticket spam
- Idempotent skip logic for existing `followups.md` is well-designed
- Clear separation of dry-run vs apply mode behavior with explicit labeling (`[DRY-RUN]`)
- Good ticket description template provided with clear metadata (origin file, line number, severity)
- Consistent with existing `/tf-followups` command structure and naming conventions
- Follows established YAML frontmatter pattern with description, model, thinking, and skill fields
- Examples section is clear and shows both dry-run and apply usage

## Summary Statistics
- Critical: 2
- Major: 2
- Minor: 2
- Warnings: 1
- Suggestions: 3
