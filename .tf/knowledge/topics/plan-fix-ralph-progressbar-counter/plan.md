---
id: plan-fix-ralph-progressbar-counter
status: consulted
last_updated: 2026-02-08
---

# Plan: Fix `tf ralph --progress` counter total

## Summary

Fix the `tf ralph --progress` indicator so the total shown in the counter (e.g. `[1/50]`) reflects the **actual ticket backlog size** (open/ready tickets), not the default `maxIterations` value (50).

Nice-to-have: refresh/recompute the total during the run so the counter stays sensible if tickets are added/removed in the background.

## Inputs / Related Topics

- Root Seed: [seed-fix-progressbar-counter-currently-it-sho](topics/seed-fix-progressbar-counter-currently-it-sho/seed.md)
- Session: seed-fix-progressbar-counter-currently-it-sho@2026-02-08T18-46-14Z
- Related Spikes:
  - (none yet)

## Requirements

- In `tf ralph start --progress` (serial mode), compute the progress total from the **current backlog**:
  - Prefer: `total = len(list_ready_tickets(ticket_list_query(ticket_query)))` at start.
  - If ticket listing fails, fall back to a clearly-labeled unknown/approximate total (avoid misleading `50`).
- The displayed counter must not regress existing behavior when `--progress` is not used.
- Keep output stable in TTY and safe in non-TTY (no control chars).

## Constraints

- Must stay lightweight (no expensive per-iteration work).
- Must remain compatible with current ticket selection flow (`ticket_query`, `completion_check`).
- Keep progress serial-only (parallel progress remains out of scope).

## Assumptions

- `tf_cli/ralph.py` already has access to:
  - `ticket_query` (select 1 ticket)
  - a derived list query via `ticket_list_query()`
  - `list_ready_tickets()` helper
- Current progress implementation has a single place where the total is chosen.

## Risks & Gaps

- "Total" semantics: `tk ready` is dependency-resolved; counting only ready tickets may undercount work if many are blocked.
  - MVP decision: total = ready-tickets snapshot (matches what Ralph can actually pick next).
  - Optional enhancement: also compute `blocked` and show `ready+blocked` as total open.
- Backlog changes during run: recomputing total each iteration could be noisy/slow.

## Work Plan (phases / tickets)

1. **Locate total calculation and replace fixed default**
   - Change progress renderer/manager to accept an initial `total_tickets` derived from list query.

2. **Compute snapshot total at loop start**
   - For `ralph_start`: compute `ready = list_ready_tickets(list_query)` once before the loop.
   - Set progress total to `len(ready)` (min 1 if unknown, or render `?`).

3. **(Optional) Periodic total refresh**
   - Recompute total every N iterations or on manual refresh key (if any), not every ticket.

4. **Tests**
   - Unit tests for total derivation with mocked `run_shell` / `list_ready_tickets`.
   - Ensure no `50` appears unless user explicitly set `--max-iterations 50` and we label it as iterations.

## Acceptance Criteria

- [ ] With 2 ready tickets, `tf ralph start --progress` shows `[0/2]` (or equivalent) at start.
- [ ] Counter increments per completed ticket and reaches total when backlog is empty.
- [ ] If ticket listing fails, output uses `?` or a message, not a misleading default.
- [ ] Tests cover the snapshot total logic.

## Open Questions

- Should total be **ready only** or **all open (ready+blocked)**? (MVP proposes ready only)
- Should we display both numbers: `ready/total_open`?

---

## Consultant Notes (Metis)

- 2026-02-08: This plan intentionally keeps dynamic updates optional; snapshot-at-start fixes the main UX bug.
- 2026-02-08: **Gap identified**: The plan should explicitly state that the "50" comes from `DEFAULTS["maxIterations"] = 50` in `tf_cli/ralph.py`, which is used as the progress total when no explicit total is provided.
- 2026-02-08: **Clarification needed**: Distinguish between `ralph run` (single ticket, total=1) and `ralph start` (loop mode, total=ready count). The fix primarily affects `ralph_start()`.
- 2026-02-08: **Implementation hint**: The progress renderer likely receives `max_iterations` from the config; change this to receive `total_tickets` computed from `len(list_ready_tickets(...))` before the loop starts.
- 2026-02-08: **Risk**: `list_ready_tickets()` calls `tk ready` via subprocess - confirm this is acceptably fast for typical backlogs (<100 tickets) or consider caching.
- 2026-02-08: **Suggested MVP simplification**: For `ralph run` (single ticket), total should be `1`. For `ralph start`, compute once at loop start and don't recompute (ignore background changes) to keep scope minimal.

## Reviewer Notes (Momus)

- 2026-02-08: PENDING
