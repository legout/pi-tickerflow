# Seed: Kanban-style TUI (Python) for tickets + topic browsing

## Vision

Working with TF tickets via raw CLI commands is efficient but not always *discoverable*. A Kanban-style terminal UI should provide a quick “dashboard” to:
- see the current ready/blocked tickets
- open a ticket and read its description/notes
- search and filter tickets and knowledge-base topics

## Core Concept

Create a Python TUI (likely Textual-based) that reads from:
- `.tickets/` (tickets)
- `.tf/knowledge/index.json` + `.tf/knowledge/topics/*` (topics)

…and renders an interactive Kanban board + searchable lists.

## Key Features

1. **Kanban board view**
   - Columns: Ready / In Progress / Blocked / Closed (or similar)
   - Keyboard navigation + move actions (optional for MVP)

2. **Ticket detail view**
   - Open a ticket, show markdown sections (Task/Context/AC/Notes)
   - Show deps/links and allow jumping to related tickets

3. **Search + filter**
   - Filter by status, tags, assignee, external-ref
   - Full-text search across ticket title + description

4. **Topic browsing**
   - Show seeds/spikes/plans with links to docs
   - Open plan/backlog docs quickly

5. **Proven inspiration**
   - Use findings from: `spike-kanban-style-tui-in-python`

## Open Questions

- Should this be a new command (`tf ui` / `tf kanban`) or a standalone script?
- Do we allow editing/moving tickets from the UI, or keep it read-only initially?
- What is the best status mapping (TF statuses vs “Ready/Blocked” derived from deps)?
- Should it support Ralph parallel workflows (component tags)?
