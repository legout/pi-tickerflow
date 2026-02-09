# Seed: Add timeout + restart handling for Ralph ticket implementation

## Vision

Ralph should not get stuck indefinitely while implementing a ticket via `/tf`. If a ticket run exceeds a configured time budget, Ralph should abort that run and retry (up to a maximum number of restarts), then fail the ticket cleanly with actionable logs.

## Core Concept

Wrap the per-ticket “implementation run” in a watchdog timeout.

- If the run finishes in time → proceed normally.
- If the run exceeds the timeout → terminate the run, record diagnostics, and restart the ticket run (bounded by `max_restarts`).

## Key Features

1. Configurable timeout for a single ticket implementation attempt
2. Configurable maximum restarts (retries) per ticket
3. Clear logging/telemetry when timeouts occur (attempt number, elapsed time, reason)
4. Safe cleanup semantics (don’t leave zombie processes / dangling worktrees)

## Open Questions

- What’s the safest termination mechanism in this codebase (signal, subprocess kill, cancel task)?
- Should timeout apply to the whole ticket (IRF) or only implementation step?
- Where should configuration live (CLI flags, settings.json, env vars), and what are defaults?
- How do we detect “stuck” vs “slow but progressing” (timeout only, or progress heartbeat)?
