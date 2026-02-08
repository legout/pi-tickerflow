---
id: pt-uisf
status: closed
deps: [pt-pnli]
links: [pt-pnli]
created: 2026-02-08T17:30:39Z
type: task
priority: 2
assignee: legout
external-ref: plan-add-progressbar-to-tk-ralph
tags: [tf, backlog, plan, component:api, component:cli, component:config, component:tests, component:workflow]
---
# Test tf ralph progress + pi-output suppression

## Task
Add unit tests covering new flag parsing and output routing behavior for `tf ralph`.

## Context
There are existing tests for `--capture-json` and Ralph logging that can be extended for these new flags.

## Acceptance Criteria
- [ ] Tests cover parsing of `--progress`, `--pi-output`, `--pi-output-file` for run/start
- [ ] Tests cover output routing modes (inherit/file/discard) without running `pi`
- [ ] Tests cover non-TTY progress behavior (no control characters)

## Constraints
- Prefer mocking `subprocess.run` rather than invoking external commands

## References
- Plan: plan-add-progressbar-to-tk-ralph



## Notes

**2026-02-08T17:49:41Z**

Implementation complete. Added 30 new tests covering:
- ProgressDisplay class (22 tests): non-TTY behavior with no control characters, TTY mode, counters
- Output routing without subprocess (8 tests): inherit/file/discard modes

Commit: 5e9b4a2
All 87 related tests pass.
