---
id: pt-3rza
status: closed
deps: [pt-cc9t]
links: [pt-yeny, pt-9sx3]
created: 2026-02-08T17:59:15Z
type: task
priority: 2
assignee: legout
external-ref: plan-ticketflow-kanban-tui
tags: [tf, backlog, plan, component:api, component:config, component:docs, component:workflow]
---
# Implement knowledge topic index loader for UI

## Task
Load `.tf/knowledge/index.json` and expose a list of topics by type (seed/spike/plan/baseline) for the UI.

## Context
The UI should allow browsing knowledge topics and opening their docs quickly.

## Acceptance Criteria
- [ ] Topics can be listed and filtered by type
- [ ] For a topic, resolve doc paths (overview/sources/plan/backlog) when present
- [ ] Missing/invalid index.json yields a friendly UI message

## Constraints
- Filesystem-only; no network

## References
- Plan: plan-ticketflow-kanban-tui



## Notes

**2026-02-08T18:14:52Z**

--note-file -
