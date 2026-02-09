# Success Metrics

## Primary

- Lessons learned are persisted to `.tf/ralph/AGENTS.md` after ticket completion
- File is created automatically when first lesson is extracted
- No manual intervention required to enable lessons learned feature

## Secondary

- Lessons from multiple tickets accumulate correctly
- File format matches SKILL.md specification
- No regression in existing Ralph functionality

## Validation

```bash
# After fix, this should show lessons content
cat .tf/ralph/AGENTS.md

# Should contain:
# - Default header with "Ralph Lessons Learned"
# - ## Patterns section
# - ## Gotchas section  
# - ## Lesson from {ticket-id} entries
```
