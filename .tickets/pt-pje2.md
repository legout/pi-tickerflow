---
id: pt-pje2
status: closed
deps: []
links: [pt-zloh]
created: 2026-02-08T17:30:39Z
type: task
priority: 2
assignee: legout
external-ref: plan-add-progressbar-to-tk-ralph
tags: [tf, backlog, plan, component:api, component:cli, component:config, component:docs, component:workflow]
---
# Define + parse tf ralph progress / pi-output flags

## Task
Add CLI parsing + help text for progress and Pi-output suppression in `tf ralph run` and `tf ralph start`. Do not implement rendering yet.

## Context
`tf ralph` already supports `--quiet/--verbose/--debug` and `--capture-json`, but does not have a progress UI or a way to redirect normal `pi` output.

## Acceptance Criteria
- [ ] `tf ralph --help` documents new flags: `--progress/--progressbar`, `--pi-output`, `--pi-output-file`
- [ ] `parse_run_args()` and `parse_start_args()` accept the new flags and plumb them into execution
- [ ] Basic validation exists for invalid combinations (e.g., unknown `--pi-output` values)

## Constraints
- Keep default behavior unchanged unless new flags are used

## References
- Plan: plan-add-progressbar-to-tk-ralph



## Notes

**2026-02-08T17:37:17Z**

Implemented CLI parsing and help text for progress and Pi-output suppression flags.

Changes:
- Added --progress/--progressbar flag (serial mode only)
- Added --pi-output={inherit,file,discard} flag
- Added --pi-output-file <path> flag  
- Updated help text with new Progress and Pi Output sections
- Added validation for invalid combinations

Tests: 716 passed (14 new)
Commit: c4e5ec0
