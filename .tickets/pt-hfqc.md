---
id: pt-hfqc
status: closed
deps: [pt-hstd]
links: [pt-hstd, pt-c2b0]
created: 2026-02-08T19:32:06Z
type: task
priority: 2
assignee: legout
external-ref: seed-add-ralph-loop-timeout-restarts
tags: [tf, backlog, component:api, component:workflow]
---
# Add bounded restart loop for timed-out ticket attempts (serial mode)

## Task
Implement bounded retry for a ticket when a timeout occurs in serial `tf ralph start` execution.

## Context
On timeout: abort the attempt, log attempt number + elapsed time, and retry the same ticket up to `maxRestarts`, then fail it cleanly.

## Acceptance Criteria
- [ ] Timeout triggers a retry of the same ticket attempt (no advancing to next ticket)
- [ ] Retry is bounded by `maxRestarts` and then marks ticket FAILED with actionable message
- [ ] Logs clearly include attempt number and timeout threshold

## Constraints
- MVP applies to serial mode; parallel behavior must remain functional (may disable retries with a warning)

## References
- Seed: seed-add-ralph-loop-timeout-restarts



## Notes

**2026-02-08T20:03:12Z**


## Implementation Complete

Added bounded restart loop for timed-out ticket attempts in serial <code>tf ralph start</code> execution.

### Changes
- Modified <code>tf_cli/ralph.py</code> serial mode to wrap <code>run_ticket()</code> in a bounded restart loop
- Timeout detection via <code>rc == -1</code> return code
- Attempt tracking with clear logging (attempt number, timeout threshold)
- Bounded by <code>maxRestarts</code> config (default: 0)

### Behavior
- With max_restarts=0 (default): Ticket runs once, on timeout => immediate FAILED
- With max_restarts=N: Up to N+1 attempts, then FAILED with actionable message

### Verification
- All 47 tests in test_ralph_logging.py pass
- Syntax validation passed
- Code review: 0 critical, 0 major, 0 minor issues

### Commit
ad81bfe pt-hfqc: Add bounded restart loop for timed-out ticket attempts in serial mode

