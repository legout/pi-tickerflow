# MVP Scope

## In Scope

- Compute `total` for the progress counter from actual tickets (snapshot at start).
- Keep the counter accurate for the common case: `tf ralph start --progress` in serial mode.

## Nice-to-have

- Recompute total each iteration (or on manual refresh) to account for tickets added/removed mid-run.

## Out of Scope

- Parallel-mode progress rendering.
