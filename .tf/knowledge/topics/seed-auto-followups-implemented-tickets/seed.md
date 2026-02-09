# Seed: Auto-create follow-ups for implemented tickets

## Vision

Ensure that every implemented ticket has its review feedback (warnings/suggestions) turned into explicit follow-up tickets (or an explicit “no follow-ups needed” record), so nothing gets lost after implementation.

## Core Concept

Introduce a command that:

1. Scans `.tf/knowledge/tickets/*` for tickets that are considered “implemented/closed”.
2. For each such ticket, checks whether `followups.md` exists.
3. If missing, invokes `/tf-followups` (or shared library logic used by that command) to create follow-up tickets from the ticket’s `review.md`.
4. Writes `followups.md` into the ticket directory (even if no follow-ups were created).

## Key Features

1. **Implemented-ticket scanner**
   - Fast traversal of `.tf/knowledge/tickets/`
   - Clear definition of “implemented ticket” (e.g., `close-summary.md` exists)

2. **Idempotent follow-up generation**
   - Skip tickets that already have `followups.md`
   - Avoid creating duplicate follow-up tickets if the command is re-run

3. **Integrate with existing follow-up flow**
   - Prefer reusing `/tf-followups` implementation (shared function/module)
   - Optionally extend `/tf-followups` to support a “scan mode” rather than introducing a separate command

## Open Questions

- What is the canonical signal for “implemented/closed” in `.tf/knowledge/tickets/{id}/`?
  - `close-summary.md` present?
  - `chain-summary.md` present?
  - ticket status in `tk`?
- Should “scan mode” create follow-ups only when `review.md` exists, or also create an explicit `followups.md` stating why it was skipped?
- Should the command default to a dry-run with a summary, requiring `--apply` to create tickets?
