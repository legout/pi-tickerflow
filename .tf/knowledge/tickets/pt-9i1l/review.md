# Review: pt-9i1l

## Critical (must fix)

1. **`.pi/skills/tf-planning/SKILL.md:613-691`** - **Mismatched "implemented ticket" heuristic**: The procedure defines the heuristic as requiring both `implementation.md` AND `review.md`, but the approved plan (plan-implement-auto-followups) specifies the MVP heuristic as `close-summary.md` exists. This is a spec violation that could cause the scan to miss tickets closed via a different workflow. *(from reviewer-spec-audit)*

2. **`.pi/skills/tf-planning/SKILL.md`** - **Command naming mismatch**: The procedure documents command `/tf-followups-scan` but `settings.json` only defines `tf-followups` (no `-scan` variant). This is a mismatch: either settings.json needs a new `tf-followups-scan` prompt entry, or the procedure should use `/tf-followups --scan` as the command interface. *(from reviewer-second-opinion)*

## Major (should fix)

3. **`.pi/skills/tf-planning/SKILL.md`** - **Missing `followups.md` artifact format**: The plan specifies a detailed format for `followups.md` including timestamp, source reference, created tickets list, and skipped items list. The procedure mentions creating this file but doesn't document the required format. *(from reviewer-spec-audit)*

4. **`.pi/skills/tf-planning/SKILL.md`** - **Missing `--json` flag**: The plan requires a `--json` flag for structured output (CI/automation friendly), but this is not documented. *(from reviewer-spec-audit)*

5. **`.pi/skills/tf-planning/SKILL.md`** - **Missing `--stop-on-error` flag**: The plan specifies this flag for strict mode behavior when `tk create` fails. *(from reviewer-spec-audit)*

6. **`.pi/skills/tf-planning/SKILL.md`** - **Missing idempotency documentation**: The plan specifies that tickets with existing `followups.md` should be skipped. The procedure mentions dry-run is default but doesn't document the idempotency check based on artifact presence. *(from reviewer-spec-audit)*

7. **`.pi/skills/tf-planning/SKILL.md`** - **`--since` flag frontmatter issue**: The flag checks `implementation.md` frontmatter, but there's no standard frontmatter format defined for `implementation.md` files in the knowledge base structure. This could lead to inconsistent behavior when filtering by date. *(from reviewer-second-opinion)*

8. **`.pi/skills/tf-planning/SKILL.md`** - **`scan-followups.md` location issue**: The output file is written to `{ticketsDir}/scan-followups.md` (root), which could cause concurrent scan overwrites and mixes scan results with individual ticket directories. Consider using a dated filename or subdirectory. *(from reviewer-second-opinion)*

## Minor (nice to fix)

9. **`.pi/skills/tf-planning/SKILL.md`** - **Incomplete output format example**: The `scan-followups.md` example doesn't include the "Skipped Items" section which the plan requires. *(from reviewer-spec-audit)*

10. **`.pi/skills/tf-planning/SKILL.md`** - **Default limit not explicit in steps**: The default `--limit` of 10 is in flags but step 3 doesn't explicitly state the default. *(from reviewer-second-opinion)*

11. **`.pi/skills/tf-planning/SKILL.md`** - **Command reference consistency**: The "Relationship" section uses `/tf-followups` but examples use `/tf-followups-scan`. Ensure consistency once naming is resolved. *(from reviewer-second-opinion)*

## Warnings (follow-up ticket)

12. **Atomic writes not documented**: The plan specifies atomic writes (temp + rename) for `followups.md`, not mentioned in procedure. *(from reviewer-spec-audit)*

13. **Heuristic extensibility**: The plan notes a future `--implemented-heuristic` flag, not mentioned as planned extension. *(from reviewer-spec-audit)*

14. **Title normalization undefined**: Claims idempotency via "de-dupe by title" but doesn't specify normalization rules (case, whitespace, punctuation). *(from reviewer-second-opinion)*

15. **Review format assumption**: The heuristic for detecting Warnings/Suggestions assumes specific markdown structure. If review formats vary, scan may miss follow-ups. *(from reviewer-second-opinion)*

## Suggestions (follow-up ticket)

16. Consider adding a note that the heuristic may be configurable in future versions.

17. Consider documenting that empty reviews should produce `followups.md` with "No warnings or suggestions found" rather than being skipped.

18. Consider adding a `--output <path>` flag for custom scan result locations.

19. Consider adding an integration test example verifying scan works end-to-end.

## Summary Statistics
- Critical: 2
- Major: 6
- Minor: 3
- Warnings: 4
- Suggestions: 4

## Reviewers
- reviewer-general: PASS (no issues)
- reviewer-spec-audit: Issues found (1 critical, 4 major)
- reviewer-second-opinion: Issues found (1 critical, 2 major)
