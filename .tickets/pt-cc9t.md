---
id: pt-cc9t
status: closed
deps: []
links: [pt-bb97, pt-yeny]
created: 2026-02-08T17:59:15Z
type: task
priority: 2
assignee: legout
external-ref: plan-ticketflow-kanban-tui
tags: [tf, backlog, plan, component:cli, component:workflow]
---
# Add `tf ui` command + Textual app skeleton

## Task
Add a new `tf ui` CLI subcommand that launches a minimal full-screen TUI (skeleton only).

## Context
We want a Kanban-style TUI for Ticketflow. MVP is read-only and will be implemented in Python (Textual).

## Acceptance Criteria
- [ ] `tf ui` is routed from `tf_cli/cli.py` to a new module (e.g., `tf_cli/ui.py`)
- [ ] Running `tf ui` in a TTY opens a minimal Textual app (placeholder screen)
- [ ] Running `tf ui` without a TTY exits with a clear message

## Constraints
- Keep behavior of existing commands unchanged

## References
- Plan: plan-ticketflow-kanban-tui



## Notes

**2026-02-08T18:11:08Z**

--note ## Implementation Complete

Added `tf ui` CLI subcommand with Textual TUI skeleton.

### Changes
- Created `tf_cli/ui.py` with minimal Textual app
- Added `ui` command routing in `tf_cli/cli.py`
- TTY detection: exits with clear message if not in interactive terminal
- Graceful degradation: handles missing Textual dependency

### Review
- 3 reviewers: general, spec-audit, second-opinion
- 1 Major issue fixed: type annotation consistency (Optional[list[str]])
- All Critical/Major issues resolved

### Commit
```
8855af9 pt-cc9t: Add tf ui command + Textual app skeleton
```
