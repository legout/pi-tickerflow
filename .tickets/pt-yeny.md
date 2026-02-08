---
id: pt-yeny
status: closed
deps: [pt-cc9t]
links: [pt-cc9t, pt-3rza]
created: 2026-02-08T17:59:15Z
type: task
priority: 2
assignee: legout
external-ref: plan-ticketflow-kanban-tui
tags: [tf, backlog, plan, component:config, component:docs, component:workflow]
---
# Implement ticket loader (frontmatter + lazy body)

## Task
Implement a loader that reads `.tickets/*.md` and returns ticket metadata for the UI.

## Context
Startup should be fast for ~100s of tickets. Load frontmatter + title eagerly, and load full body only when a ticket is opened.

## Acceptance Criteria
- [ ] Loader parses YAML frontmatter fields used by the UI (id, status, deps, tags, assignee, external-ref)
- [ ] Loader extracts the markdown title and supports lazy loading of the remaining body
- [ ] Malformed tickets are skipped with a warning (no crash)

## Constraints
- No per-ticket `tk show` subprocess calls

## References
- Plan: plan-ticketflow-kanban-tui



## Notes

**2026-02-08T18:24:41Z**

## Implementation Complete

Implemented ticket loader module with frontmatter parsing and lazy body loading.

### Changes
- Created tf_cli/ticket_loader.py with Ticket and TicketLoader classes
- Supports YAML frontmatter parsing with basic fallback parser
- Lazy body loading for UI performance
- Handles malformed tickets gracefully (warnings, no crash)
- 48 comprehensive tests

### Review
- 3 reviewers: general, spec-audit, second-opinion
- 1 Critical issue fixed: Windows line ending support
- 3 Major issues fixed: numeric parsing, YAML fallback, body loading

### Commit
```
96f02e5 pt-yeny: Implement ticket loader (frontmatter + lazy body)
```
