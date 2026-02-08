---
id: pt-c2b0
status: closed
deps: [pt-hfqc]
links: [pt-hfqc, pt-j485]
created: 2026-02-08T19:32:06Z
type: task
priority: 2
assignee: legout
external-ref: seed-add-ralph-loop-timeout-restarts
tags: [tf, backlog, component:api, component:tests, component:workflow]
---
# Add tests for timeout + restart behavior in tf ralph

## Task
Add unit tests for timeout termination + bounded restart behavior.

## Context
We need confidence that timeouts trigger retries and that the loop fails cleanly after max restarts.

## Acceptance Criteria
- [ ] Tests cover: timeout detected, retry happens, stops at maxRestarts
- [ ] Tests cover: subprocess termination path (mocked) and cleanup/warn behavior
- [ ] Tests do not invoke real `pi`

## Constraints
- Prefer mocking subprocess APIs and timeouts

## References
- Seed: seed-add-ralph-loop-timeout-restarts


