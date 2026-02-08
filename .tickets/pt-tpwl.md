---
id: pt-tpwl
status: closed
deps: []
links: [pt-im9d]
created: 2026-02-08T23:04:18Z
type: task
priority: 2
assignee: legout
external-ref: seed-fix-ralph-agents-md
tags: [tf, backlog, component:cli, component:config, component:docs, component:workflow]
---
# Fix Ralph to create .tf/ralph/AGENTS.md when saving lessons

## Task
Fix `tf_cli/ralph.py:update_state()` so lessons learned are persisted even when `.tf/ralph/AGENTS.md` does not yet exist.

## Context
Ralph extracts a Lessons Learned block from `close-summary.md` via `extract_lesson_block()`. However, `update_state()` only appends lessons when `agents_path.exists()` is true, and there is no code path that creates the file. This causes lessons to be silently discarded and prevents re-anchoring from ever having lessons.

## Acceptance Criteria
- [ ] When a ticket close-summary contains a "Lessons Learned" section, running `update_state()` creates `.tf/ralph/AGENTS.md` if missing
- [ ] New file starts with a minimal template:
  ```markdown
  # Ralph Lessons Learned

  ## Patterns

  ## Gotchas
  ```
- [ ] Lesson is appended under a header like `## Lesson from <ticket> (<timestamp>)`
- [ ] If no lesson block exists, do not create or modify AGENTS.md

## Constraints
- Minimal change; no new dependencies
- Use UTF-8 reads/writes consistent with codebase

## References
- Seed: seed-fix-ralph-agents-md
- File: `tf_cli/ralph.py` (update_state + extract_lesson_block)



## Notes

**2026-02-08T23:10:02Z**

Implemented fix for Ralph lessons learned persistence.

Changes:
- Modified update_state() in tf_cli/ralph.py to create .tf/ralph/AGENTS.md with minimal template when it doesn't exist
- Lessons are now appended even when the file is missing (previously silently discarded)

Commit: fce49aa

Review: 0 critical, 0 major, 3 minor issues (pre-existing patterns)
All acceptance criteria met.
