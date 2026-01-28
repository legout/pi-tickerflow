---
description: Sync implement-review-fix-close workflow config into agent files (models, defaults).
---

# IRFC Sync

Apply the workflow configuration from:
- `.pi/workflows/implement-review-fix-close/config.json` (project)
- `~/.pi/agent/workflows/implement-review-fix-close/config.json` (global)

If both exist, merge them with project settings taking precedence.

## What to sync

### 1) Agent models
Update the `model:` field in these agent files when a model is provided in `models`:

- `implementer` → `agents/implementer.md`
- `reviewer-general` → `agents/reviewer-general.md`
- `reviewer-spec-audit` → `agents/reviewer-spec-audit.md`
- `reviewer-second-opinion` → `agents/reviewer-second-opinion.md`
- `review-merge` → `agents/review-merge.md`
- `fixer` → `agents/fixer.md`
- `closer` → `agents/closer.md`
- `researcher` → `agents/researcher.md`
- `researcher-fetch` → `agents/researcher-fetch.md`

If a model is missing for an agent, leave its `model:` unchanged.

### 2) Prompt template notes
No code changes required here, but confirm `/implement-review-fix-close` already reflects config options.

## Output

After syncing, report:
- Which agent models were updated (old → new)
- Which agents were left unchanged
- Any missing config sections
