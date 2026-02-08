---
id: pt-1qk7
status: closed
deps: [pt-li6a]
links: [pt-li6a, pt-i7hx]
created: 2026-02-08T18:18:50Z
type: task
priority: 2
assignee: legout
external-ref: plan-implement-auto-followups
tags: [tf, backlog, plan, component:agents, component:api, component:cli, component:config, component:docs, component:workflow]
---
# Configure prompt registry: add tf-followups-scan to settings + manifest

## Task
Register the new `/tf-followups-scan` prompt in workflow config so model routing works consistently.

## Context
Prompts are mapped to meta-models in `.tf/config/settings.json` and included in the install manifest used by sync/install tooling.

## Acceptance Criteria
- [ ] Add `"tf-followups-scan": "planning"` to `.tf/config/settings.json` under `prompts`.
- [ ] Ensure prompt file is included in `config/install-manifest.txt` (and any other prompt sync list).
- [ ] Run formatting on edited JSON/MD files if required by repo tooling.

## Constraints
- No behavior changes to existing prompts besides adding the new entry.

## References
- Plan: plan-implement-auto-followups



## Notes

**2026-02-08T22:43:47Z**

Implemented: Added prompts/tf-followups-scan.md to config/install-manifest.txt. The settings.json registry entry was already present. Commit: 8874f59
