---
name: tf-tickets
description: Ticket maintenance workflows (component tag suggestions, dependency sync, dedup suggestions).
---

# TF Tickets Skill

Guidance for maintaining ticket metadata in `.tickets/` using `tk`.

## Common Setup

- Use `tk query` to get all tickets as JSON.
- Prefer filtering by status: `open` and `in_progress` unless user requests otherwise.
- Avoid destructive changes by default; only apply when `--apply`/`--link` flags are provided.

## Procedure: Suggest Component Tags

Goal: add `component:*` tags to enable safe parallel scheduling.

1. Collect tickets:
   - `tk query` → filter to open/in_progress (or user-specified status).
2. For each ticket:
   - Extract existing tags.
   - If any tag starts with `component:`, skip.
   - Otherwise, infer 1–2 component tags from:
     - Title keywords (delta/iceberg/parquet/checkpoint/kafka/serialization/storage/cli/tests/docs)
     - Parent ticket title
     - External ref / seed topic names
3. Output a table:
   - Ticket ID
   - Title
   - Current tags
   - Suggested component tags
   - Rationale
4. If `--apply`:
   - Append suggested `component:*` tags to the YAML `tags:` list.
   - Preserve existing tags and ordering.
   - Use direct file edits in `.tickets/<id>.md`.

## Procedure: Sync Dependencies

Goal: ensure parent relationships are reflected in `deps`.

1. Collect tickets + status via `tk query`.
2. For each open/in_progress ticket:
   - If `parent` is set and not in `deps`, propose adding.
   - Do **not** remove existing deps automatically.
   - Report missing or unknown deps.
3. If `--apply`:
   - For each missing parent dep, run: `tk dep <id> <parent>`.

## Procedure: Deduplicate Tickets

Goal: surface likely duplicates (no auto close).

1. Collect open/in_progress tickets via `tk query`.
2. Compare by:
   - Same parent
   - High keyword overlap in title
   - Similar description snippets
3. Output candidate clusters with rationale.
4. If `--link`:
   - Run `tk link <id> <duplicate-id>` for each suggested pair.
   - Do **not** close or merge tickets automatically.
