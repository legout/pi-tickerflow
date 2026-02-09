# MVP Scope

## In Scope (MVP)

- Add a CLI flag (name TBD) to enable a progress display for `tk ralph`.
- Render progress only when running in a TTY.
- Add a mode to suppress verbose logging / Pi tool output on screen while progress is enabled.
- Ensure errors still print immediately.

## Out of Scope (for MVP)

- Full-screen TUI dashboard.
- Persisted historical run metrics.
- Highly granular per-tool progress; start with per-ticket (or per-phase) progress.
