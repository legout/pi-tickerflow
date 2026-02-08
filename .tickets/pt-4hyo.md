---
id: pt-4hyo
status: closed
deps: [pt-i7hx]
links: [pt-i7hx, pt-9i1l]
created: 2026-02-08T18:18:50Z
type: task
priority: 2
assignee: legout
external-ref: plan-implement-auto-followups
tags: [tf, backlog, plan, component:agents, component:docs, component:tests, component:workflow]
---
# Test + document /tf-followups-scan (dry-run + apply) with sample tickets

## Task
Add lightweight docs and a manual smoke-test checklist for `/tf-followups-scan`.

## Context
Since this is a prompt-driven workflow, a practical verification checklist and examples reduce regressions.

## Acceptance Criteria
- [ ] Update `docs/commands.md` (or equivalent) to include `/tf-followups-scan` usage and examples.
- [ ] Add a short manual test recipe: create a dummy implemented ticket dir with/without `review.md`, run dry-run then apply, verify `followups.md`.
- [ ] Ensure docs mention idempotency (second run should do nothing for processed tickets).

## Constraints
- No brittle end-to-end automation required for MVP; keep it as docs + checklist.

## References
- Plan: plan-implement-auto-followups



## Notes

**2026-02-08T22:49:23Z**

## Implementation Complete

**Changes:**
- Updated docs/commands.md with /tf-followups-scan command reference (syntax, arguments, examples, idempotency note)
- Created docs/tf-followups-scan-manual-test.md with 6 comprehensive test cases covering dry-run, apply, idempotency, and edge cases

**Commit:** 720195a0b3e28c291e9941f9402c374a35d8d01e

**Review:**
- Critical: 0
- Major: 0
- Minor: 0
- Suggestions: 3 (follow-up material)
