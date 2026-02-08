---
id: pt-i7hx
status: closed
deps: [pt-1qk7]
links: [pt-1qk7, pt-4hyo]
created: 2026-02-08T18:18:50Z
type: task
priority: 2
assignee: legout
external-ref: plan-implement-auto-followups
tags: [tf, backlog, plan, component:agents, component:cli, component:docs, component:workflow]
---
# Define followups.md format + align /tf-followups to always write it

## Task
Update `/tf-followups` prompt/spec so it always writes a `followups.md` artifact with a consistent structure (including “none needed” cases).

## Context
The new scan command relies on `followups.md` as the idempotency marker. For correctness, `/tf-followups` should always produce it when it runs.

## Acceptance Criteria
- [ ] Update `.pi/prompts/tf-followups.md` and `prompts/tf-followups.md` to specify a stable `followups.md` template.
- [ ] Explicitly document behavior when `review.md` is missing or contains no Warnings/Suggestions (“No follow-ups needed”).
- [ ] Ensure template includes origin ticket id + review path and lists created follow-up ticket IDs.

## Constraints
- Keep ticket creation semantics unchanged (still `tk create ... --tags tf,followup --priority 3`).

## References
- Plan: plan-implement-auto-followups



## Notes

**2026-02-08T22:46:04Z**

--note ## Implementation Complete

Updated both prompt files with stable followups.md template:
- .pi/prompts/tf-followups.md
- prompts/tf-followups.md

### Changes
- Added structured followups.md template with origin ticket ID, review path, and created ticket listings
- Documented 'No Follow-ups Needed' behavior for missing review.md or empty Warnings/Suggestions
- Template includes table format for consistency with existing followups.md files

### Commit
623c5802782d3b351bd62417a5042b8a227a80f9
