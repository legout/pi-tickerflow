# Review (Spec Audit): pt-li6a

## Overall Assessment
The implementation provides the basic `/tf-followups-scan` command structure with dry-run default and `--apply` flag support. However, there are significant gaps between the implementation and the spec requirements, including missing prompt registration, incomplete flag support, and deviations from the eligibility heuristic and output format.

## Critical (must fix)
- `.tf/config/settings.json` - **Missing prompt registration**: The plan explicitly requires "Register the prompt in `.tf/config/settings.json` under `prompts` (meta-model: `planning`)." The `tf-followups-scan` prompt is NOT registered in the settings.json prompts section, which means Pi won't recognize the command.

## Major (should fix)
- `.pi/prompts/tf-followups-scan.md:32-36` - **Wrong eligibility heuristic**: The spec requires detecting "implemented/closed" tickets using the heuristic `close-summary.md` exists. The implementation instead checks for `review.md` exists. These are different signals - a ticket can have a review without being closed/implemented.
- `.pi/prompts/tf-followups-scan.md` - **Missing `--json` flag**: The spec requires `--json` for structured output (CI/automation friendly). The implementation only supports `--apply`.
- `.pi/prompts/tf-followups-scan.md` - **Missing `--stop-on-error` flag**: The spec requires this flag for strict mode when `tk create` fails. The implementation does not address partial failure handling.

## Minor (nice to fix)
- `.pi/prompts/tf-followups-scan.md:44-53` - **Missing `close-summary.md` handling**: The spec says tickets with `close-summary.md` should be processed but if missing `followups.md`, should write a note. Implementation only processes based on `review.md`.
- `.pi/prompts/tf-followups-scan.md:72-75` - **Simplified "none needed" message**: The spec requires "No warnings or suggestions found in review." but implementation uses "No follow-ups needed" - slightly different semantics.
- `.pi/prompts/tf-followups-scan.md` - **No atomic write requirement**: The spec requires atomic writes (temp file + rename) for `followups.md` to prevent partial files on crash. Not mentioned in implementation.
- `.pi/prompts/tf-followups-scan.md:76-80` - **Output summary mismatch**: The spec shows summary format with table structure including "Scanned/Eligible/Processed/Skipped" but the implementation's summary format differs slightly (shows sub-items under Processed differently).

## Warnings (follow-up ticket)
- **No `followups.md` artifact format compliance**: The spec defines a specific format with "Created Tickets" and "Skipped Items" sections, timestamps, and source references. The implementation description is vague about the actual file content format.
- **No dedup mechanism for tickets**: The spec mentions avoiding duplicate follow-up tickets but MVP implementation relies only on `followups.md` presence without stronger dedup (e.g., source review hash).

## Suggestions (follow-up ticket)
- Add `--batch-size` flag for rate limiting with large repos (mentioned in plan open questions)
- Consider implementing the `--implemented-heuristic` flag to allow different signals (close-summary|implementation+review|tk-status) as mentioned in risks section

## Positive Notes
- Both `.pi/prompts/tf-followups-scan.md` and `prompts/tf-followups-scan.md` files are created as required
- Dry-run default behavior is correctly implemented
- `--apply` flag works as specified
- Uses `workflow.knowledgeDir` from settings.json
- Safe/idempotent behavior: skips directories with existing `followups.md`
- Per-ticket actions and summary statistics are printed
- Ticket description template follows the spec format

## Summary Statistics
- Critical: 1
- Major: 3
- Minor: 4
- Warnings: 2
- Suggestions: 2

## Spec Coverage
- Spec/plan sources consulted: 
  - Ticket pt-li6a (acceptance criteria)
  - Plan: plan-implement-auto-followups/plan.md (comprehensive spec)
  - Existing /tf-followups.md prompt (for reuse patterns)
- Missing specs: none (plan covers all requirements)
