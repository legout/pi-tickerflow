---
id: pt-cj59
status: closed
deps: [pt-2s2s]
links: [pt-ut88, pt-whcy]
created: 2026-02-08T18:41:27Z
type: task
priority: 2
assignee: legout
external-ref: seed-move-ralph-session-away-from-tf-ralph-us
tags: [tf, backlog, component:api, component:cli, component:config, component:workflow]
---
# Change tf ralph default sessionDir to Pi sessions directory

## Task
Update `tf ralph` so that, by default, the session JSONL files passed to `pi --session` are stored in Pi’s standard session directory rather than `.tf/ralph/sessions`.

## Context
`tf_cli/ralph.py` has `DEFAULTS["sessionDir"] = ".tf/ralph/sessions"` and `resolve_session_dir()` resolves it relative to the project root. We want a new default aligned with Pi.

## Acceptance Criteria
- [ ] Default `sessionDir` updated to Pi standard dir (absolute path)
- [ ] Existing configs that set `sessionDir` keep working (relative paths still relative to project root)
- [ ] `tf ralph run/start` continues to create per-ticket session files as before

## Constraints
- No change to JSONL session format

## References
- Seed: seed-move-ralph-session-away-from-tf-ralph-us



## Notes

**2026-02-08T19:47:45Z**

Changed default sessionDir from .tf/ralph/sessions to ~/.pi/agent/sessions (Pi's standard session directory).

Changes:
- Updated DEFAULTS['sessionDir'] in tf_cli/ralph.py

Backward compatibility preserved:
- Existing configs with custom sessionDir still work
- Relative paths still resolve relative to project root
- Absolute paths work as expected

Commit: 3774b1e
