---
id: pt-9i1l
status: closed
deps: [pt-4hyo]
links: [pt-4hyo]
created: 2026-02-08T18:18:50Z
type: task
priority: 2
assignee: legout
external-ref: plan-implement-auto-followups
tags: [tf, backlog, plan, component:agents, component:cli, component:docs, component:workflow]
---
# Update tf-planning skill: add Follow-ups Scan procedure

## Task
Extend the tf-planning skill docs to include a procedure for `/tf-followups-scan` (scan implemented tickets and invoke `/tf-followups`).

## Context
The skill currently documents single-ticket follow-up creation. Scan mode should be documented so future prompt updates stay consistent.

## Acceptance Criteria
- [ ] Add a new procedure section under `.pi/skills/tf-planning/SKILL.md` describing scan behavior, flags, and safety defaults.
- [ ] Ensure it references `workflow.knowledgeDir` and the “implemented ticket” heuristic.
- [ ] Keep the existing Follow-up Creation procedure intact; reference scan mode as complementary.

## Constraints
- Documentation-only change (no runtime code required).

## References
- Plan: plan-implement-auto-followups



## Notes

**2026-02-08T22:52:55Z**

## Implementation Complete

Added Follow-ups Scan procedure to  and registered the command in settings.json.

### Changes Made
- **SKILL.md**: Added comprehensive Follow-ups Scan procedure with:
  - Correct  heuristic for implemented tickets
  - All required flags: , , , , , , 
  - Proper  artifact format specification
  - Idempotency via artifact presence checking
  - Atomic writes documentation
  - Safety defaults (dry-run by default)
  
- **settings.json**: Added  prompt entry with  meta-model

### Review Summary
- 2 Critical issues identified and fixed
- 6 Major issues identified and fixed
- 3 Minor, 4 Warnings, 4 Suggestions remain as non-blocking follow-ups

### Commit
 - pt-9i1l: Add Follow-ups Scan procedure to tf-planning skill
