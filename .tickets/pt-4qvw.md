---
id: pt-4qvw
status: closed
deps: []
links: [pt-hstd]
created: 2026-02-08T19:32:05Z
type: task
priority: 2
assignee: legout
external-ref: seed-add-ralph-loop-timeout-restarts
tags: [tf, backlog, component:api, component:config, component:docs, component:workflow]
---
# Define Ralph timeout + restart configuration surface

## Task
Define and implement configuration knobs for per-ticket attempt timeout and max restarts for `tf ralph`.

## Context
We want to abort stuck `/tf` runs after a time budget and retry, bounded by `max_restarts`.

## Acceptance Criteria
- [ ] Config keys are defined (e.g., `attemptTimeoutMs` and `maxRestarts`) in `.tf/ralph/config.json` defaults
- [ ] Optional env var overrides are supported (documented) OR explicitly deferred
- [ ] `tf ralph --help` mentions the new settings and their defaults

## Constraints
- Defaults must be conservative to avoid false positives

## References
- Seed: seed-add-ralph-loop-timeout-restarts



## Notes

**2026-02-08T19:44:42Z**

Implemented Ralph timeout + restart configuration.\n\nChanges:\n- Added attemptTimeoutMs (default: 600000ms = 10min) and maxRestarts (default: 0) config options\n- Added env var overrides: RALPH_ATTEMPT_TIMEOUT_MS, RALPH_MAX_RESTARTS\n- Updated tf ralph --help with new settings\n- Implemented subprocess timeout handling and restart loop logic\n\nCommit: ff38216\nAll 889 tests pass.
