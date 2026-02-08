---
id: pt-l8za
status: closed
deps: [pt-sbvo, pt-5g48]
links: [pt-9sx3, pt-sbvo]
created: 2026-02-08T17:59:15Z
type: task
priority: 2
assignee: legout
external-ref: plan-ticketflow-kanban-tui
tags: [tf, backlog, plan, component:cli, component:docs, component:tests, component:workflow]
---
# Docs + smoke tests for `tf ui`

## Task
Add user-facing docs/help and basic tests for parsing + board classification + CLI wiring.

## Context
We need a stable MVP with minimal regressions. Textual rendering can be lightly smoke-tested; logic should be unit-tested.

## Acceptance Criteria
- [ ] `tf --help` includes `ui` command help (or `tf ui --help` works)
- [ ] Tests exist for ticket parsing + classification + topic index loading
- [ ] CI/local test run passes

## Constraints
- Prefer unit tests over brittle screenshot-like UI tests

## References
- Plan: plan-ticketflow-kanban-tui



## Notes

**2026-02-08T22:59:05Z**

## Completed: Docs + Smoke Tests for tf ui

### Changes Made
- **tf_cli/cli.py**: Updated help text with proper  command documentation including:
  - Added  to usage line
  - Added comprehensive  section with descriptions
  - Documented  as "Launch the interactive Kanban TUI"
  
- **tests/test_ui_smoke.py**: Added 14 smoke tests covering:
  - CLI help documentation verification
  - CLI wiring/integration tests
  - Error handling (TTY requirement)
  - Module import verification
  - Topic utility function tests
  - Component instantiation tests

### Test Results
- All 14 new smoke tests pass
- Full test suite: 131 tests pass
- Existing tests verified: ticket parsing (39), board classification (28), topic index loading (27)

### Acceptance Criteria
✅ Ticketflow CLI

Usage:
  tf --version | -v | -V
  tf install [--global] [--force-local]
  tf setup
  tf login
  tf init [--project <path>]
  tf sync [--project <path>]
  tf doctor [--project <path>] [--fix]
  tf update
  tf next
  tf backlog-ls [topic-id-or-path]
  tf track <path>
  tf priority-reclassify [--apply] [--ids ...] [--ready] [--status ...] [--tag ...]
  tf ralph <subcommand> ...
  tf agentsmd <subcommand> ...
  tf seed ...
  tf kb ...
  tf ui

Commands:
  install           Install the Ticketflow CLI shim
  setup             Run interactive setup wizard
  login             Authenticate with ticket storage service
  init              Initialize a project for Ticketflow
  sync              Sync tickets with external service
  doctor            Diagnose and fix common issues
  update            Update the CLI to latest version
  next              Show next recommended ticket to work on
  backlog-ls        List tickets in backlog by topic
  track             Track file changes for a ticket
  priority-reclassify  Reclassify ticket priorities
  ralph             Ralph loop management commands
  agentsmd          AGENTS.md management commands
  seed              Create seed topics from ideas
  kb                Knowledge base management commands
  ui                Launch the interactive Kanban TUI

Run 'tf <command> --help' for more information on a command.

(You can also use: tf new <command> ... for the old subcommand namespace.) includes  command help
✅ Tests exist for ticket parsing + classification + topic index loading
✅ CI/local test run passes

**Commit**: 3313f83
