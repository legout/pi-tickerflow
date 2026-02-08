---
id: pt-pnli
status: closed
deps: [pt-zloh]
links: [pt-zloh, pt-uisf]
created: 2026-02-08T17:30:39Z
type: task
priority: 2
assignee: legout
external-ref: plan-add-progressbar-to-tk-ralph
tags: [tf, backlog, plan, component:workflow]
---
# Implement serial progress display for tf ralph (per-ticket)

## Task
Add a conservative, stdlib-only per-ticket progress display for `tf ralph` in serial mode.

## Context
The UI should update at ticket boundaries (start/complete/fail) and must not emit control characters in non-TTY contexts.

## Acceptance Criteria
- [ ] `tf ralph start --progress` renders a stable progress line to stderr in TTY
- [ ] In non-TTY, progress output is plain text (no control chars)
- [ ] `--progress` forces `--pi-output=file` in TTY (unless `discard`), or warns+overrides
- [ ] `--progress` is rejected for parallel mode in MVP with a clear message

## Constraints
- MVP is serial-only (no multi-process progress UI)

## References
- Plan: plan-add-progressbar-to-tk-ralph



## Notes

**2026-02-08T17:44:36Z**

Implemented serial progress display for tf ralph start --progress.

Changes:
- Added ProgressDisplay class (stdlib-only, TTY-aware)
- Progress updates at ticket boundaries (start/complete/fail)
- TTY mode: uses escape sequences for stable progress line
- Non-TTY mode: plain text output (no control chars)
- --progress in TTY forces --pi-output=file to prevent corruption
- --progress rejected for parallel mode

Commit: 3f239a6
Tests: All 74 existing tests pass
