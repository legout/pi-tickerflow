# Implementation: pt-tpwl

## Summary
Fix `tf_cli/ralph.py:update_state()` to create `.tf/ralph/AGENTS.md` when it doesn't exist, instead of silently discarding lessons learned.

## Changes Made

### File: `tf_cli/ralph.py`

Modified the `update_state()` function to:
1. Check if a lesson block exists in the close-summary.md
2. If lessons exist and AGENTS.md doesn't exist, create it with a minimal template
3. Then append the lesson to the file

The key change is replacing:
```python
if lesson_block and agents_path.exists():
```

With:
```python
if lesson_block:
    if not agents_path.exists():
        # Create minimal template
        agents_path.write_text("...", encoding="utf-8")
    # Append lesson
    ...
```

## Template Used
```markdown
# Ralph Lessons Learned

## Patterns

## Gotchas
```

## Verification
- When a ticket close-summary contains a "Lessons Learned" section and AGENTS.md doesn't exist, the file is created
- Lessons are appended under `## Lesson from <ticket> (<timestamp>)`
- If no lesson block exists, AGENTS.md is not created or modified
