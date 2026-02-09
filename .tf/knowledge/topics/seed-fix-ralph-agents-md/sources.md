# Sources

## Primary Source

- `tf_cli/ralph.py` - Main Ralph implementation file containing the bug

## Related Documentation

- `.pi/skills/ralph/SKILL.md` - Ralph skill specification documenting expected behavior

## Key Code Locations

- `update_state()` function (line ~857-942) - Contains the bug
- `extract_lesson_block()` function (line ~817-830) - Extracts lessons from close-summary.md
- `ensure_progress()` function (line ~815-832) - Reference for file creation pattern

## Test Files

- `tests/test_next.py` - May contain related tests
- `tests/test_agentsmd.py` - Specific to AGENTS.md functionality

## Related Topics

- `.tf/knowledge/topics/plan-add-progressbar-to-tk-ralph/` - Recent Ralph enhancement work
