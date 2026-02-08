---
id: pt-li6a
status: closed
deps: []
links: [pt-1qk7]
created: 2026-02-08T18:18:50Z
type: task
priority: 2
assignee: legout
external-ref: plan-implement-auto-followups
tags: [tf, backlog, plan, component:agents, component:cli, component:config, component:docs, component:workflow]
---
# Setup /tf-followups-scan prompt entrypoint (dry-run default)

## Task
Add new Pi prompt command `/tf-followups-scan` that scans implemented ticket artifact dirs and runs follow-up creation for those missing `followups.md`.

## Context
We already have `/tf-followups <review-path-or-ticket-id>`. We need a scan command to ensure every implemented ticket has a `followups.md` record (created or “none needed”).

## Acceptance Criteria
- [ ] Create `.pi/prompts/tf-followups-scan.md` (and `prompts/tf-followups-scan.md` if required) describing usage + flags.
- [ ] Default behavior is **dry-run** (no `tk create`, no file writes); `--apply` performs changes.
- [ ] Scan uses `workflow.knowledgeDir` and iterates `{knowledgeDir}/tickets/*`.
- [ ] Prints per-ticket actions + final summary (scanned/eligible/processed/created/skipped).

## Constraints
- Keep safe/idempotent: skip ticket dirs that already have `followups.md`.

## References
- Plan: plan-implement-auto-followups



## Notes

**2026-02-08T22:42:46Z**

## Implementation Complete

Created  prompt that scans ticket artifact directories for missing  files.

### Files Created/Modified
-  - Main prompt file (root level)
-  - Project-local copy
-  - Added prompt registration

### Features
- Dry-run by default (no changes without --apply)
- Scans  for directories with  but missing 
- Creates follow-up tickets for Warnings/Suggestions from review.md
- Idempotent: skips directories with existing followups.md
- Comprehensive summary output

### Review Summary
- Critical: 3/3 fixed (model reference, prompt registration, procedure reference)
- Major: 5/6 fixed (consistency, eligibility heuristic)
- Deferred: --json and --stop-on-error flags (enhancement)

Commit: 0cb9a33
