# MVP Scope

## In Scope

- Add a command (new or an extension to `/tf-followups`) that:
  - Iterates `.tf/knowledge/tickets/*`
  - Identifies implemented/closed tickets via a simple heuristic (MVP: `close-summary.md` exists)
  - For each implemented ticket missing `followups.md`, runs the follow-up creation logic against `{ticket-dir}/review.md` (if present)
  - Writes `{ticket-dir}/followups.md` with a summary of created follow-up tickets, or a note that none were needed / review missing

## Out of Scope (for MVP)

- Deep integration with `tk` status queries to determine “implemented”
- Parallel processing / concurrency
- Rich filtering UI (e.g., component filters)
- Auto-dedup across *different* tickets (dedup within one ticket is required)
