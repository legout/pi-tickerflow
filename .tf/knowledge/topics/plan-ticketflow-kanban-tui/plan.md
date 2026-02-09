---
id: plan-ticketflow-kanban-tui
status: approved
last_updated: 2026-02-08
---

# Plan: Ticketflow Kanban-style TUI (Python)

## Summary

Implement a Kanban-style TUI for **pi-ticketflow** that lets users browse tickets and knowledge-base topics with fast search/filtering, and drill into details without leaving the terminal.

MVP goal: **read-only productivity UI** (board + lists + details + search). Ticket mutations (move/edit) are explicitly out of scope for MVP to keep risk low.

## Inputs / Related Topics

- Root Seed: [seed-kanban-style-tui-for-tf](topics/seed-kanban-style-tui-for-tf/seed.md)
- Session: seed-kanban-style-tui-for-tf@2026-02-08T17-45-37Z
- Related Spikes:
  - [spike-kanban-style-tui-in-python](topics/spike-kanban-style-tui-in-python/spike.md)

## Requirements

### CLI / Packaging

- Add a new CLI entrypoint: **`tf ui`** (MVP choice; add alias `tf kanban` later if desired).
- Implement as a Python module under `tf_cli/` and dispatch from `tf_cli/cli.py`.
- Add a TUI dependency (default choice: **Textual**).

### Data Model

- Tickets:
  - Load from `.tickets/*.md`.
  - Parse YAML frontmatter + markdown body.
  - For performance: load **frontmatter + title** eagerly; load full body text lazily when the ticket is opened.
- Topics:
  - Load from `.tf/knowledge/index.json`.
  - Support listing by type (seed/spike/plan/baseline).

### Board Columns (MVP)

- Column derivation (local computation; no `tk show`):
  - **Closed**: `status: closed`
  - **In Progress**: `status: in_progress`
  - **Blocked**: `status in {open,in_progress}` and any dependency is not `closed`
  - **Ready**: `status in {open,in_progress}` and all dependencies are `closed`
- Notes:
  - This is intended to match the spirit of `tk ready` / `tk blocked` without spawning subprocesses.
  - If later needed, add an optional `--use-tk-ready` mode.

### UI Features (MVP)

- Full-screen TUI with:
  - Board view (Ready / Blocked / In Progress / Closed)
  - Ticket list navigation
  - Ticket detail panel (read-only): title, selected frontmatter fields, body sections, deps/links
  - Topic browser view: list topics and open relevant docs
- Search + filtering:
  - Substring search across ticket title + body (title-only search is acceptable as a fallback)
  - Filters: status, tags, assignee, external-ref

### Terminal Behavior

- Keyboard-first navigation.
- Clean exit (terminal state restored even on exceptions).
- Resize-safe.
- Output rules:
  - UI is interactive only when attached to a TTY.
  - In non-TTY contexts, `tf ui` should exit with a clear message.

## Constraints

- MVP is read-only: no ticket edits, no moves, no dependency modifications.
- Must work offline (filesystem only).
- Avoid O(n) subprocess calls at startup (e.g., no per-ticket `tk show`).
- Acceptable performance for ~100s of tickets:
  - initial load should feel instant (<1–2s)
  - search/filter should not noticeably lag (simple substring is fine)

## Assumptions

- Tickets are stored in `.tickets/` as markdown with YAML frontmatter.
- Knowledge base is under `.tf/knowledge/` and `index.json` is present.
- Python 3.9+ is acceptable (Textual requirement).

## Risks & Gaps

- **Framework dependency**: Textual is productive but adds dependency surface area.
  - Mitigation: keep UI logic isolated; leave a seam for swapping rendering later.
- **Status mapping drift**: Local Ready/Blocked computation might diverge from `tk` behavior.
  - Mitigation: document the rule and add tests with fixture tickets.
- **Search scope creep**: incremental search + advanced filters can explode complexity.
  - Mitigation: MVP uses substring search + a small set of filters; no indexing engine.
- **Markdown rendering**: inline markdown rendering can be complex.
  - Mitigation: MVP shows plain text; topic docs open in `$PAGER`/`$EDITOR`.

## Work Plan (phases / tickets)

1. **Framework + CLI wiring**
   - Add `tf ui` dispatch in `tf_cli/cli.py`
   - Add new module skeleton (e.g., `tf_cli/ui.py`)
   - Add Textual dependency + a minimal “hello app”

2. **Parsing layer**
   - Ticket parser: frontmatter + title + body (lazy load body)
   - Topic index loader: index.json -> topic list by type

3. **Board computation**
   - Implement Ready/Blocked/In Progress/Closed classification
   - Add unit tests with sample ticket graphs

4. **UI MVP**
   - Board/list layout + selection model
   - Ticket detail panel
   - Manual refresh (`r`)

5. **Search + filters**
   - Search input (substring)
   - Filter toggles/inputs for status/tags/assignee/external-ref

6. **Topic browser**
   - List topics and open docs via `$PAGER` / `$EDITOR`

7. **Docs + smoke tests**
   - Keybindings/help screen
   - Minimal tests for parsing/filtering + a CLI smoke test

## Acceptance Criteria

- [ ] `tf ui` launches a TUI in a terminal (TTY required).
- [ ] The UI shows tickets split into Ready/Blocked/In Progress/Closed using the documented dependency rule.
- [ ] User can navigate tickets and open a read-only detail panel.
- [ ] User can search by substring and filter by status/tag/assignee/external-ref.
- [ ] User can browse knowledge topics and open a topic doc via `$PAGER`/`$EDITOR`.
- [ ] On crash/exit, terminal state is restored (no broken prompt).

## Open Questions

- Should `tf kanban` be an alias in MVP or later?
- Do we want title-only search as the MVP baseline (fastest), with body search added later?

---

## Consultant Notes (Metis)

- 2026-02-08: This plan assumes Textual as the primary framework; if dependency footprint is a concern, consider a prompt_toolkit fallback for a simpler list/detail UI.
- 2026-02-08: Added missing spike reference `spike-kanban-style-tui-in-python` to Related Spikes.
- 2026-02-08: Clarified MVP scope reductions:
  - Manual refresh (`r` key) instead of file watchers
  - Open topic docs in `$EDITOR`/`less` instead of inline markdown rendering
  - Load ticket metadata eagerly but defer full body until opened
  - Target Python 3.9+ (Textual requirement)
- 2026-02-08: Risk mitigation: "filter chips" and "incremental search" can be simplified to a basic search input for MVP.

## Reviewer Notes (Momus)

- 2026-02-08: PASS
  - Blockers:
    - none
  - Required changes:
    - none
  - Notes:
    - Plan now makes explicit MVP choices (command name, status mapping rule, no mutations) and is ready for backlog generation.
