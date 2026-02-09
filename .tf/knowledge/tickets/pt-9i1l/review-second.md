# Review (Second Opinion): pt-9i1l

## Overall Assessment
The implementation adds a well-structured "Follow-ups Scan" procedure to the tf-planning skill documentation. The procedure follows existing conventions, has good safety defaults with dry-run by default, and clearly documents its relationship to single-ticket follow-up creation. However, there's a critical command naming mismatch between the documented `/tf-followups-scan` and the actual configured command in settings.json.

## Critical (must fix)
- `.pi/skills/tf-planning/SKILL.md:845` - The procedure documents command `/tf-followups-scan` but `settings.json` only defines `tf-followups` (line 66). This is a mismatch: either the settings.json needs a new `tf-followups-scan` prompt entry, or the procedure should use `/tf-followups --scan` as the command interface. Without this alignment, the documented command won't work.

## Major (should fix)
- `.pi/skills/tf-planning/SKILL.md:880` - The `--since` flag checks `implementation.md` frontmatter, but there's no standard frontmatter format defined for `implementation.md` files in the knowledge base structure (lines 1139-1150). The document shows various artifact types but doesn't specify frontmatter for implementation.md. This could lead to inconsistent behavior when filtering by date.

- `.pi/skills/tf-planning/SKILL.md:890` - The output file `scan-followups.md` is written to `{ticketsDir}/scan-followups.md` (the tickets directory root), which could cause issues: (1) concurrent scans could overwrite each other, (2) there's no timestamp or session ID in the filename for historical tracking, (3) it mixes scan results with individual ticket directories. Consider using a dated filename or subdirectory.

## Minor (nice to fix)
- `.pi/skills/tf-planning/SKILL.md:856` - The default `--limit` of 10 is documented in the flags description but not enforced in the steps. Step 3 mentions "Stop after N tickets" but doesn't explicitly state the default value of 10. Consider adding "(default: 10)" to the step description for clarity.

- `.pi/skills/tf-planning/SKILL.md:934-935` - The "Relationship to Follow-up Creation" section uses `/tf-followups` (single-ticket mode) but the procedure title and examples use `/tf-followups-scan`. If the command naming issue is fixed, ensure both references are consistent.

## Warnings (follow-up ticket)
- `.pi/skills/tf-planning/SKILL.md:915` - Claims idempotency via "de-dupe by title" but doesn't specify how title normalization works (case sensitivity, whitespace handling, punctuation). This could lead to duplicate tickets if normalization rules differ between implementations.

- `.pi/skills/tf-planning/SKILL.md:875` - The heuristic for detecting Warnings/Suggestions sections assumes a specific markdown structure. If review formats vary (e.g., different heading levels, section names), the scan may miss follow-ups. Consider documenting the expected review.md structure more explicitly.

## Suggestions (follow-up ticket)
- `.pi/skills/tf-planning/SKILL.md:889` - Consider adding a `--output <path>` flag to allow custom scan result locations instead of hardcoding `scan-followups.md`. This would enable better CI/CD integration and historical tracking.

- `.pi/skills/tf-planning/SKILL.md` - Consider adding an integration test example that verifies the scan procedure works end-to-end with sample ticket artifacts. This would catch issues like the command naming mismatch in the future.

## Positive Notes
- Excellent safety defaults with dry-run by default and explicit `--apply` opt-in (lines 847, 884, 911-913)
- Clear "implemented ticket" heuristic with both `implementation.md` and `review.md` required (line 872)
- Well-structured procedure following the existing Purpose/Input/Flags/Steps format
- Good example usage section with multiple scenarios (lines 919-930)
- Clear documentation of relationship between scan mode and single-ticket mode (lines 933-936)
- Proper placement immediately after "Follow-up Creation" procedure shows good document organization

## Summary Statistics
- Critical: 1
- Major: 2
- Minor: 2
- Warnings: 2
- Suggestions: 2
