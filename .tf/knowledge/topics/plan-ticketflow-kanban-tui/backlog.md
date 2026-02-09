# Backlog: plan-ticketflow-kanban-tui

| ID | Title | Score | Est. Hours | Depends On | Links |
|----|-------|-------|------------|------------|-------|
| pt-bb97 | Implement Ready/Blocked board classification + tests | 4 | 1-2 | pt-yeny,pt-3rza | pt-cc9t |
| pt-cc9t | Add `tf ui` command + Textual app skeleton | 3 | 1-2 | - | pt-bb97,pt-yeny |
| pt-yeny | Implement ticket loader (frontmatter + lazy body) | 3 | 1-2 | pt-cc9t | pt-cc9t,pt-3rza |
| pt-3rza | Implement knowledge topic index loader for UI | 3 | 1-2 | pt-cc9t | pt-yeny,pt-9sx3 |
| pt-9sx3 | Build Textual UI MVP: board + ticket detail + manual refresh | 3 | 1-2 | pt-bb97 | pt-3rza,pt-l8za |
| pt-l8za | Docs + smoke tests for `tf ui` | 1 | 1-2 | pt-sbvo,pt-5g48 | pt-9sx3,pt-sbvo |
| pt-sbvo | Add ticket search + filters in TUI | 0 | 1-2 | pt-9sx3 | pt-l8za,pt-5g48 |
| pt-5g48 | Add topic browser + open docs via $PAGER/$EDITOR | 0 | 1-2 | pt-9sx3 | pt-sbvo |