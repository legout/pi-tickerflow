# Review (Spec Audit): pt-9i1l

## Overall Assessment
The Follow-ups Scan procedure has been added to the SKILL.md and follows the general structure. However, there are discrepancies between the implementation documentation and the approved plan (plan-implement-auto-followups), particularly around the "implemented ticket" heuristic and missing documentation for expected artifact format and certain flags.

## Critical (must fix)
- `.pi/skills/tf-planning/SKILL.md:613-691` - **Mismatched "implemented ticket" heuristic**: The procedure defines the heuristic as requiring both `implementation.md` AND `review.md`, but the approved plan specifies the MVP heuristic as `close-summary.md` exists. This is a spec violation that could cause the scan to miss tickets that were closed via a different workflow.

## Major (should fix)
- `.pi/skills/tf-planning/SKILL.md:613-691` - **Missing `followups.md` artifact format**: The plan specifies a detailed format for `followups.md` including timestamp, source reference, created tickets list, and skipped items list. The procedure mentions creating this file but does not document the required format, leading to inconsistent implementations.
- `.pi/skills/tf-planning/SKILL.md:621-626` - **Missing `--json` flag**: The plan requires a `--json` flag for structured output (CI/automation friendly), but this is not documented in the procedure.
- `.pi/skills/tf-planning/SKILL.md:621-626` - **Missing `--stop-on-error` flag**: The plan specifies this flag for strict mode behavior when `tk create` fails, but it's not documented.
- `.pi/skills/tf-planning/SKILL.md:647-655` - **Missing idempotency documentation**: The plan specifies that tickets with existing `followups.md` should be skipped. The procedure mentions dry-run is default but doesn't document the idempotency check based on artifact presence.

## Minor (nice to fix)
- `.pi/skills/tf-planning/SKILL.md:680-691` - **Incomplete output format example**: The `scan-followups.md` example shows a table format but doesn't include the "Skipped Items" section which the plan requires for tickets where `review.md` is missing or no follow-ups were needed.

## Warnings (follow-up ticket)
- `.pi/skills/tf-planning/SKILL.md:613-691` - **Atomic writes not documented**: The plan specifies atomic writes (temp + rename) for `followups.md`, but this implementation detail is not mentioned in the procedure. Should be added as implementation guidance.
- `.pi/skills/tf-planning/SKILL.md:619` - **Heuristic extensibility**: The plan notes a future flag `--implemented-heuristic` for different detection methods, but this is not mentioned in the procedure as a planned extension.

## Suggestions (follow-up ticket)
- Consider adding a note that the heuristic may be configurable in future versions to support different workflow styles (e.g., tickets closed without `close-summary.md`).
- Consider documenting that empty reviews should produce `followups.md` with "No warnings or suggestions found in review" rather than being skipped entirely.

## Positive Notes
- The procedure correctly references `workflow.knowledgeDir` from settings.json as required by the ticket acceptance criteria
- The flags section is well-structured with clear descriptions of `--dry-run`, `--apply`, `--since`, `--ticket`, and `--limit`
- The safety defaults (dry-run by default, explicit opt-in required) are properly documented
- The relationship to Follow-up Creation is clearly explained as complementary
- The existing Follow-up Creation procedure was left intact as required

## Summary Statistics
- Critical: 1
- Major: 4
- Minor: 1
- Warnings: 2
- Suggestions: 2

## Spec Coverage
- Spec/plan sources consulted: 
  - Ticket pt-9i1l (implementation requirements)
  - Plan: plan-implement-auto-followups (.tf/knowledge/topics/plan-implement-auto-followups/plan.md)
  - Implementation: .tf/knowledge/tickets/pt-9i1l/implementation.md
  - Result: .pi/skills/tf-planning/SKILL.md
- Missing specs: none
