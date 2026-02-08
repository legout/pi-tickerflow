---
id: pt-4dji
status: closed
deps: [pt-whcy]
links: [pt-whcy]
created: 2026-02-08T18:41:27Z
type: task
priority: 2
assignee: legout
external-ref: seed-move-ralph-session-away-from-tf-ralph-us
tags: [tf, backlog, component:config, component:docs, component:workflow]
---
# Update tf ralph help text + docs for new session location

## Task
Update `tf ralph --help` and any relevant docs to reflect the new default session location and overrides.

## Context
Users need to know where sessions are written (especially when debugging).

## Acceptance Criteria
- [ ] Help text documents default Pi session dir path
- [ ] Help text documents override knobs (config + env var if added)
- [ ] Mention legacy `.tf/ralph/sessions` behavior and warning

## Constraints
- Keep wording precise; avoid guessing paths if platform-specific

## References
- Seed: seed-move-ralph-session-away-from-tf-ralph-us



## Notes

**2026-02-08T23:05:55Z**

Updated tf ralph --help and documentation to reflect new session location.

Changes:
- Help text now documents default Pi session directory (~/.pi/agent/sessions)
- Config override (sessionDir) documented
- Environment variable RALPH_FORCE_LEGACY_SESSIONS documented
- Legacy behavior and warning explained
- docs/ralph.md and docs/configuration.md updated with Session Storage sections

Commit: fb39be1
