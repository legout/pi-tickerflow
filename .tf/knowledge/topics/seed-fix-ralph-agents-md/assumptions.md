# Assumptions

1. **close-summary.md contains lessons**: The existing `extract_lesson_block()` function correctly parses lessons from ticket close summaries

2. **Single fix location**: The bug is isolated to the `update_state()` function around line 940 of `ralph.py`

3. **No config changes needed**: The `lessonsMaxCount` config option exists but pruning is out of scope

4. **Default template acceptable**: The template from SKILL.md (`## Patterns`, `## Gotchas`) is sufficient

5. **File permissions**: The Ralph process has write permissions to `.tf/ralph/` directory

6. **Atomic writes not required**: Simple write operations are sufficient (no need for temp file + rename for this fix)
