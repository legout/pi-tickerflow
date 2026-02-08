---
id: pt-hstd
status: closed
deps: [pt-4qvw]
links: [pt-4qvw, pt-hfqc]
created: 2026-02-08T19:32:05Z
type: task
priority: 2
assignee: legout
external-ref: seed-add-ralph-loop-timeout-restarts
tags: [tf, backlog, component:api, component:cli, component:config, component:workflow]
---
# Implement subprocess timeout + safe termination for pi run

## Task
Add timeout handling around the `pi -p "..."` subprocess execution so a stuck ticket attempt can be terminated reliably.

## Context
`tf_cli/ralph.py:run_ticket()` currently uses `subprocess.run(args, ...)`. We need a watchdog timeout and safe cleanup (no zombies).

## Acceptance Criteria
- [ ] When timeout is configured, the `pi` subprocess is terminated after the timeout (terminate/kill as needed)
- [ ] Return code / error reason indicates timeout distinctly (for retry logic)
- [ ] Output capture modes remain correct (`--pi-output=file/discard/inherit`, `--capture-json`)

## Constraints
- Must not leave zombie processes (always wait after kill)

## References
- Seed: seed-add-ralph-loop-timeout-restarts



## Notes

**2026-02-08T19:56:30Z**

--note ## Implementation Complete

**Summary:** Implemented subprocess timeout handling with safe termination for Ralph's `pi run` subprocess.

**Changes:**
- Added `_run_with_timeout()` helper in `tf_cli/ralph.py`
- Implements graceful termination (SIGTERM) followed by force kill (SIGKILL) if needed
- Always reaps child processes to prevent zombies
- Returns -1 distinctly for timeout (used by restart logic in pt-hfqc)
- Preserves all output capture modes: inherit, file, discard, JSON capture

**Testing:**
- Normal execution: PASS
- Timeout detection: PASS  
- No zombie processes: PASS

**Commit:** a2010d8

**Review:** 0 critical, 0 major, 1 minor (logging enhancement suggestion) 2
