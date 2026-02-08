---
id: pt-9sx3
status: closed
deps: [pt-bb97]
links: [pt-3rza, pt-l8za]
created: 2026-02-08T17:59:15Z
type: task
priority: 2
assignee: legout
external-ref: plan-ticketflow-kanban-tui
tags: [tf, backlog, plan, component:cli, component:docs, component:workflow]
---
# Build Textual UI MVP: board + ticket detail + manual refresh

## Task
Implement the MVP Textual UI layout: board/list navigation + read-only ticket detail panel + manual refresh.

## Context
Use the loaders + classification logic to populate the UI. MVP is keyboard-first and must exit cleanly.

## Acceptance Criteria
- [ ] Board shows Ready/Blocked/In Progress/Closed columns
- [ ] Selecting a ticket shows a read-only detail panel
- [ ] `r` triggers reload of data from disk
- [ ] App exits cleanly without breaking terminal state

## Constraints
- Keep interactions minimal; no ticket edits/moves in MVP

## References
- Plan: plan-ticketflow-kanban-tui



## Notes

**2026-02-08T18:36:10Z**

Implemented Textual UI MVP with Kanban board.

Changes:
- Added TicketBoard widget with 4 columns (Ready/Blocked/In Progress/Closed)
- Ticket selection shows read-only detail panel with full metadata
- 'r' key triggers reload of data from disk (context-aware per tab)
- Clean integration with existing BoardClassifier and TicketLoader

Fixes applied:
- Removed unused DataTable import
- Fixed misleading 'press o to open' text
- Improved BoardView type annotation

Commit: d69ae89
Tests: 79 passed (board_classifier, ticket_loader)
