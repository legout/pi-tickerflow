# Research: pt-ctov

## Status
Research enabled. Using existing project knowledge - no additional external research required.

## Context Reviewed
- `tk show pt-ctov` - Documentation task for P0-P4 rubric and `/tf-priority-reclassify`
- `tk show pt-gn5z` - Linked design/implementation ticket (closed)
- `prompts/tf-priority-reclassify.md` - Existing Pi prompt
- `tf_cli/priority_reclassify_new.py` - Python CLI implementation
- `.tf/knowledge/topics/priority-rubric.md` - Canonical rubric definition
- `README.md` - Main project documentation
- `docs/commands.md` - Command reference

## Key Findings

### P0-P4 Priority Rubric

| Label | Numeric | Name | Description |
|-------|---------|------|-------------|
| P0 | 0 | **Critical** | System down, data loss, security breach, blocking all work |
| P1 | 1 | **High** | Major feature, significant bug affecting users, performance degradation |
| P2 | 2 | **Normal** | Standard product features, routine enhancements (default) |
| P3 | 3 | **Low** | Engineering quality, dev workflow improvements, tech debt |
| P4 | 4 | **Minimal** | Code cosmetics, refactors, docs polish, test typing |

### Command Implementation
- **Dry-run by default** - Requires `--apply` for changes
- **Multiple selection modes** - `--ids`, `--ready`, `--status`, `--tag`
- **Safety flags** - `--max-changes`, `--yes`, `--force`
- **Audit trail** - Written to `.tf/knowledge/priority-reclassify-{timestamp}.md`
- **JSON output** - For scripting integration

## Sources
- `.tf/knowledge/topics/priority-rubric.md`
- `tf_cli/priority_reclassify_new.py`
- `prompts/tf-priority-reclassify.md`
