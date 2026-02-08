---
id: pt-2s2s
status: closed
deps: []
links: [pt-ut88]
created: 2026-02-08T18:41:27Z
type: task
priority: 2
assignee: legout
external-ref: seed-move-ralph-session-away-from-tf-ralph-us
tags: [tf, backlog, component:agents, component:api, component:config, component:docs, component:workflow]
---
# Define Pi standard session directory for tf ralph

## Task
Identify Pi’s canonical session directory and add a small helper to compute the default path for `tf ralph` sessions.

## Context
Pi auto-saves sessions under `~/.pi/agent/sessions/` organized by working directory. `tf ralph` currently writes session JSONL to `.tf/ralph/sessions` and passes those paths to `pi --session`.

## Acceptance Criteria
- [ ] Default session dir is defined in code (with a clear doc comment)
- [ ] Implementation uses `Path.home()` + `~/.pi/agent/sessions` (or whatever Pi docs confirm)
- [ ] Add an override mechanism (env var or config) without breaking existing config

## Constraints
- Keep this change self-contained (no behavioral change yet; just helper + docs)

## References
- Seed: seed-move-ralph-session-away-from-tf-ralph-us



## Notes

**2026-02-08T19:38:59Z**

Implemented Pi standard session directory helper.

Changes:
- Added PI_STANDARD_SESSION_DIR constant (~/.pi/agent/sessions)
- Added get_pi_session_dir() helper function
- Added get_default_session_dir() helper for path selection
- Enhanced resolve_session_dir() with env var override (RALPH_SESSION_DIR)
- Support 'pi-standard' config value for sessionDir

Commit: 81f3374

Review: 0 Critical, 0 Major, 0 Minor issues. 2 suggestions for follow-up.
