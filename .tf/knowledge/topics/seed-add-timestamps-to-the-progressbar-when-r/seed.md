# Seed: Add timestamps to the progressbar when running the Ralph loop

## Vision

When Ralph runs with `--progress`, users should be able to see *when* each progress update happened.
This makes long runs easier to debug (e.g., which ticket stalled, how long each step took) and improves overall observability.

## Core Concept

Enhance the progress display emitted by `tf ralph start --progress` (and any related progress modes) to include a timestamp prefix (e.g. `23:14:05 [3/12] Processing pt-...`).
Keep behavior safe for both TTY and non-TTY output.

## Key Features

1. Timestamp prefix added to progress updates (configurable format if needed).
2. Works in TTY (in-place updates) and non-TTY (newline output) without corrupting logs.
3. Does not change output when `--progress` is not enabled.
4. Tests to prevent regressions in output formatting.

## Open Questions

- Timestamp format: `HH:MM:SS`, ISO-8601, or relative elapsed time?
- Should we include timestamps only on “final” lines (ticket completed) or also during “processing” updates?
- Any interaction with `--pi-output` / output routing that could duplicate timestamps?
