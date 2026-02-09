# Research: pt-3rza

## Status
Research enabled but minimal external research was performed. Implementation is straightforward based on existing codebase patterns.

## Context Reviewed
- `tk show pt-3rza` - Ticket requirements
- `.tf/knowledge/index.json` structure - Topics with id, title, keywords, and optional paths
- `tf_cli/kb_helpers.py` - Existing KB helper functions including `get_topic_type()` and `get_topic_docs()`
- `tf_cli/ui.py` - Existing Textual TUI skeleton
- Plan: `plan-ticketflow-kanban-tui` - Requirements for topic browser UI

## Key Findings
1. `index.json` has a `topics` array with objects containing:
   - `id`: Topic ID (e.g., "seed-add-versioning")
   - `title`: Human-readable title
   - `keywords`: Array of search terms
   - Optional paths: `overview`, `sources`, `plan`, `backlog`

2. Topic types are derived from ID prefix:
   - `seed-*` → seed
   - `plan-*` → plan
   - `spike-*` → spike
   - `baseline-*` → baseline

3. `kb_helpers.py` already has `get_topic_type()` and `get_topic_docs()` functions that can be reused.

4. Topic docs are stored in `topics/{topic_id}/{doctype}.md`

## Sources
- Local codebase inspection
