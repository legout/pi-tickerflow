---
id: pt-sbvo
status: closed
deps: [pt-9sx3]
links: [pt-l8za, pt-5g48]
created: 2026-02-08T17:59:15Z
type: task
priority: 2
assignee: legout
external-ref: plan-ticketflow-kanban-tui
tags: [tf, backlog, plan, component:api, component:workflow]
---
# Add ticket search + filters in TUI

## Task
Add substring search and basic filters (status/tags/assignee/external-ref) to the TUI.

## Context
MVP needs fast discovery. Keep it simple (substring search, basic filter inputs).

## Acceptance Criteria
- [ ] Search filters the visible ticket list/board by substring (title at minimum)
- [ ] Filters exist for status, tags, assignee, external-ref
- [ ] Clearing search/filters restores the full set

## Constraints
- No indexing engine for MVP

## References
- Plan: plan-ticketflow-kanban-tui



## Notes

**2026-02-08T22:55:54Z**

Implementation complete.

Changes:
- Added search input for substring matching (title + body)
- Added filter inputs for status, tags, assignee, external-ref
- Added Clear button to reset all filters
- Filters combine with AND logic
- No indexing engine used (simple in-memory filtering)

Commit: 038cd8f

Review: 0 Critical, 0 Major, 0 Minor issues
