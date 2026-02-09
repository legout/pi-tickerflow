# Seed: Add a progress bar to `tk ralph` (optional) + suppress Pi output

## Vision

`tk ralph` should be pleasant to run interactively: users should be able to tell “how far along” the run is at a glance, without scrolling through verbose logs.

## Core Concept

Introduce an optional progress display for `tk ralph` that summarizes overall progress (e.g., tickets completed / total, current phase/step), and optionally suppresses existing detailed logging / Pi output.

## Key Features

1. **Progress bar mode**: show a single-line, continuously updating progress indicator while Ralph processes tickets.
2. **Optional replacement for current logging**: when enabled, reduce console noise (keep only progress + key milestones / errors).
3. **Suppress Pi output**: provide a way to hide Pi tool output in the terminal (while still retaining it for debugging).

## Open Questions

- What is the correct CLI surface?
  - `tk ralph --progress` / `--progressbar`
  - `tk ralph --quiet` (implies progress?)
  - `tk ralph --pi-output=none|stderr|file:<path>`
- What is the unit of progress?
  - tickets, steps within a ticket (IRF phases), or both?
- How should this behave in non-TTY contexts (CI, piping)?
- Do we need to preserve structured logs for later inspection (e.g., a JSONL file) when console output is suppressed?
