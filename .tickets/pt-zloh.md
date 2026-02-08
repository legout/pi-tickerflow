---
id: pt-zloh
status: closed
deps: [pt-pje2]
links: [pt-pje2, pt-pnli]
created: 2026-02-08T17:30:39Z
type: task
priority: 2
assignee: legout
external-ref: plan-add-progressbar-to-tk-ralph
tags: [tf, backlog, plan, component:api, component:cli, component:config, component:workflow]
---
# Implement pi subprocess output routing (inherit/file/discard)

## Task
Implement `--pi-output` handling for `tf ralph` by redirecting the `pi` subprocess stdout/stderr as requested.

## Context
`run_ticket()` currently calls `subprocess.run(args)` which inherits the terminal. Progress display requires redirecting output away from the terminal to avoid corrupting the progress line.

## Acceptance Criteria
- [ ] `--pi-output=inherit` preserves current behavior
- [ ] `--pi-output=file` writes output to `.tf/ralph/logs/<ticket>.log` (or `--pi-output-file`)
- [ ] `--pi-output=discard` suppresses output
- [ ] On failure, print exit code + the log path when file capture is enabled

## Constraints
- Avoid changing JSON capture behavior (`--capture-json`) except to keep it compatible

## References
- Plan: plan-add-progressbar-to-tk-ralph



## Notes

**2026-02-08T17:41:57Z**

Implemented --pi-output handling for tf ralph.

Changes:
- run_ticket() now accepts pi_output ('inherit'/'file'/'discard') and pi_output_file parameters
- File mode writes pi subprocess output to .tf/ralph/logs/<ticket>.log (or custom path)
- Discard mode redirects output to /dev/null
- On failure with file mode, prints exit code and log path

Commit: 31cb1cb

All acceptance criteria met. 743 tests passing (including 27 new tests for this feature).
