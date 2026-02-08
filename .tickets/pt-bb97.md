---
id: pt-bb97
status: closed
deps: [pt-yeny, pt-3rza]
links: [pt-cc9t]
created: 2026-02-08T17:59:15Z
type: task
priority: 2
assignee: legout
external-ref: plan-ticketflow-kanban-tui
tags: [tf, backlog, plan, component:docs, component:tests, component:workflow]
---
# Implement Ready/Blocked board classification + tests

## Task
Implement the MVP rule for mapping tickets into Ready/Blocked/In Progress/Closed and add unit tests.

## Context
We want Ready/Blocked to be derived locally from ticket deps (not via `tk ready`).

## Acceptance Criteria
- [ ] Classification matches the documented rule in the plan
- [ ] Unit tests cover a small dependency graph (blocked->ready after dep closes)
- [ ] Closed/In Progress mapping is correct

## Constraints
- Keep classification logic independent of UI rendering

## References
- Plan: plan-ticketflow-kanban-tui



## Notes

**2026-02-08T18:31:42Z**

--note ## Implementation Complete

Implemented Ready/Blocked board classification logic for the Kanban TUI.

### Changes
- **tf_cli/board_classifier.py** - New module with classification logic
- **tests/test_board_classifier.py** - 31 comprehensive unit tests

### Classification Rules Implemented
- **Closed**: status == "closed" (regardless of dependencies)
- **In Progress**: status == "in_progress" and all deps closed
- **Blocked**: status in {open, in_progress} and any dep not closed  
- **Ready**: status == "open" and all deps closed

### Review Summary
- 3 reviewers: No Critical or Major issues
- 5 Minor fixes applied:
  1. Fixed docstring to match implementation
  2. Added defensive status handling
  3. Removed unused _loaded attribute
  4. Optimized classify_tickets() function
  5. Cleaned up test comments

### Test Results
31 passed in test_board_classifier.py
889 passed in full test suite

Commit: 43144d5
