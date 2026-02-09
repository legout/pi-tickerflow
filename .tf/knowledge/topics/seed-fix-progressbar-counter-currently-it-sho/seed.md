# Seed: Fix tf ralph progress counter to use open ticket count

## Vision

When running `tf ralph ... --progress`, the progress display should be meaningful. Right now it shows a fixed total (e.g. `[1/50]`) based on the default max-iterations rather than the number of tickets actually pending.

## Core Concept

Compute the progress total from the current ticket backlog (number of open/ready tickets), not from `maxIterations` (default 50). Optionally refresh the total during the run (nice-to-have).

## Key Features

1. **Correct total**: show `[done/total]` where `total` is derived from the actual open/ready tickets.
2. **Stable behavior**: do not regress non-progress mode or parallel mode restrictions.
3. **(Optional) Dynamic total**: if tickets are added while Ralph is running, update the total on refresh/iteration (not required for MVP).

## Open Questions

- Should `total` be derived from `tk ready`, `tk blocked`, or all open tickets (`tk list --status=open`)?
- In `start` mode, should `total` be a snapshot at start or recomputed each iteration?
- How should we display “unknown total” when the ticket query can’t be listed reliably?
