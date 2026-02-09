---
id: plan-implement-auto-followups
status: approved
last_updated: 2026-02-08
---

# Plan: Implement auto followups

## Summary

Add a CLI command that scans **implemented tickets** under `.tf/knowledge/tickets/` and (re)uses the existing `/tf-followups` logic to generate follow-up tickets for any ticket directory missing a `followups.md` artifact.

The goal is to make follow-up generation **systematic and idempotent**: every implemented ticket should end up with `followups.md`, even if the result is "no follow-ups needed".

## Inputs / Related Topics

- Root Seed: [seed-auto-followups-implemented-tickets](topics/seed-auto-followups-implemented-tickets/seed.md)
- Session: seed-auto-followups-implemented-tickets@2026-02-08T18-06-38Z
- Related Spikes:
  - (none yet)

## Requirements

### Functional

- Provide a command that:
  - Iterates `.tf/knowledge/tickets/*/`.
  - Detects "implemented/closed" tickets (MVP heuristic: `close-summary.md` exists).
  - For each implemented ticket **without** `followups.md`:
    - Run follow-up creation against the ticket's `review.md`.
    - Write `followups.md` into the ticket directory, recording what happened.

### Integration with `/tf-followups`

- Prefer **reusing** the existing `/tf-followups` parsing + ticket creation logic.
- If needed, refactor `/tf-followups` so its core behavior is available as a function (e.g., `generate_followups(ticket_id|review_path, ...)`) that both:
  - `/tf-followups <ticket-id>` and
  - the new "scan implemented tickets" command
  can call.

### Idempotency / de-dup

- The scan command must be safe to re-run:
  - Skip ticket dirs that already contain `followups.md`.
  - Avoid creating duplicate follow-up tickets for the same review content.
    - MVP: treat the presence of `followups.md` as the primary "already processed" marker.

### Command Interface

- Add a new Pi prompt command: **`/tf-followups-scan`**.
- Usage:
  ```
  /tf-followups-scan [--apply] [--dry-run] [--json] [--stop-on-error]
  ```
- Default mode is **dry-run** (no side effects). `--apply` performs changes.
- Implementation model:
  - The scan command should iterate ticket dirs and, for each eligible ticket missing `followups.md`, invoke the same logic as `/tf-followups <ticket-id>`.
  - If refactoring is needed, update `/tf-followups` to share its core logic with scan mode.

### UX

- Print a short summary:
  - total ticket dirs scanned
  - how many were considered implemented
  - how many were missing `followups.md`
  - how many follow-up tickets were created
  - how many were skipped (and why)
- **Output format**: human-readable table by default; optional `--json` for structured output (CI/automation friendly).
- **Dry-run**: `--dry-run` shows what would happen without creating tickets or writing files.

### `followups.md` Artifact Format

Each processed ticket directory gets a `followups.md` with:
```markdown
# Follow-ups: {ticket-id}

Generated: ISO-8601 timestamp
Source: {ticket-dir}/review.md

## Created Tickets

- TKT-XXX: {title}
- ...

## Skipped Items

- Reason: {explanation}
```
If no follow-ups needed: "No warnings or suggestions found in review."
If no review.md: "Skipped: no review.md present."

## Constraints

- Knowledge-dir must respect `workflow.knowledgeDir` (default `.tf/knowledge`).
- Must not modify existing ticket artifacts except writing missing `followups.md`.
- Conservative definition of implemented/closed for MVP (prefer false negatives to false positives).
- **Error handling**: handle permission errors gracefully (log skip, don't crash).
- **Atomic writes**: `followups.md` must be written atomically (temp + rename) to prevent partial files on crash.

## Assumptions

- Implemented tickets have a stable artifact signal (MVP: `close-summary.md`).
- Review feedback to parse lives at `{ticket-dir}/review.md`.
- `tk` is available to create follow-up tickets.

## Risks & Gaps

- **Definition drift**: "implemented" may not always correlate with `close-summary.md`.
  - Mitigation: allow a flag later (e.g., `--implemented-heuristic close-summary|implementation+review|tk-status`).
- **Missing review.md**: some implemented tickets may not have a review artifact.
  - Mitigation: still write `followups.md` with a note ("skipped: no review.md").
- **Duplicate followups** if followups were created manually without `followups.md`.
  - Mitigation: MVP relies on artifact presence; later can add a stronger dedup marker inside `followups.md` (e.g., source review hash).
- **Orphaned follow-up tickets**: If `tk create` succeeds but writing `followups.md` fails (crash/power loss), re-running creates duplicates.
  - Mitigation (MVP): write `followups.md` atomically (temp file + rename); accept small window of inconsistency. Later: add transaction log or idempotency key to ticket metadata.
- **Partial batch failures**: If `tk create` fails for one ticket, should the scan continue or abort?
  - Mitigation: default to continue with error logging; add `--stop-on-error` flag for strict mode.

## Work Plan (phases / tickets)

1. **Assess current `/tf-followups` implementation**
   - Identify what can be reused as-is vs what needs refactoring for library use.

2. **Refactor `/tf-followups` into reusable core** (if needed)
   - Extract parsing of Warnings/Suggestions + ticket creation into a helper.
   - Ensure the existing command behavior remains unchanged.

3. **Implement scan command**
   - Add new prompt entrypoint: `.pi/prompts/tf-followups-scan.md` (and `prompts/tf-followups-scan.md` if this repo maintains both copies).
   - Register the prompt in `.tf/config/settings.json` under `prompts` (meta-model: `planning`).
   - Locate implemented tickets.
   - For each missing `followups.md`, run follow-up generation (reuse `/tf-followups` logic) and write artifact.

4. **Add safety + reporting**
   - Optional `--dry-run` (recommended).
   - Clear per-ticket output in verbose mode.

5. **Add tests**
   - Unit tests for "implemented ticket" detection.
   - Unit tests for scan skip conditions and artifact writing.

## Acceptance Criteria

- [ ] A command `/tf-followups-scan` exists to scan `.tf/knowledge/tickets/` for implemented tickets missing `followups.md` (default dry-run; `--apply` performs changes).
- [ ] For each such ticket, follow-up generation runs (or records why it cannot run) and writes `followups.md`.
- [ ] Re-running the command makes no changes when all implemented tickets have `followups.md`.
- [ ] `/tf-followups` remains usable standalone and shares the same core logic.
- [ ] Empty reviews (no Warnings/Suggestions) produce `followups.md` with "none needed" record, not error.
- [ ] Partial failures (e.g., one `tk create` fails) are logged but don't abort the entire scan.
- [ ] `--dry-run` produces accurate preview without side effects.

## Decisions

- Implement as a new command: **`/tf-followups-scan`** (keeps `/tf-followups` focused on single-ticket operation).
- Default to **dry-run**; require `--apply` to create tickets and write `followups.md`.

## Open Questions (remaining)

- Do we need `--batch-size` / rate limiting for large repos (100s–1000s of implemented tickets)? If yes, default batch size and behavior (stop vs continue).

---

## Consultant Notes (Metis)

- 2026-02-08: Drafted initial plan from the active seed; no spikes attached yet. Consider adding a small spike to inspect the current `/tf-followups` code paths and dedup behavior before implementation.
- **2026-02-08**: Gap detection pass:
  - **Added**: `followups.md` artifact format specification (previously undefined).
  - **Added**: Empty review handling requirement (write "none needed" record).
  - **Added**: Partial failure handling (continue by default, `--stop-on-error` option).
  - **Added**: Orphaned ticket risk with atomic write mitigation.
  - **Added**: Output format clarification (human table + optional `--json`).
  - **Added**: Explicit recommendations for Open Questions (new command, dry-run default).
  - **Flagged**: Still need to specify `--batch-size` or rate limiting if large ticket volumes expected.

## Reviewer Notes (Momus)

- 2026-02-08: PASS
  - Blockers:
    - none
  - Required changes:
    - none
  - Notes:
    - The command interface and dry-run/apply semantics are now explicit.
    - Remaining open question (`--batch-size` / rate limiting) is non-blocking for MVP; can be added if scan time becomes an issue.
