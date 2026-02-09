# MVP Scope: Fix Ralph AGENTS.md

## In Scope

1. **Fix conditional write in `update_state()`**
   - Remove `agents_path.exists()` check
   - Create file with default template if missing
   - Ensure lessons are appended correctly

2. **Default template for AGENTS.md**
   ```markdown
   # Ralph Lessons Learned

   ## Patterns

   ## Gotchas
   ```

3. **Testing**
   - Verify file is created on first lesson
   - Verify lessons are appended correctly
   - Verify multiple tickets accumulate lessons

## Out of Scope (Future)

1. Reading AGENTS.md during re-anchoring (documented but never implemented)
2. Pruning old lessons when count exceeds `lessonsMaxCount`
3. Backfilling lessons from existing close-summary.md files

## Success Criteria

- [ ] After processing a ticket with lessons learned, `.tf/ralph/AGENTS.md` exists
- [ ] The file contains the lesson content from the ticket
- [ ] Multiple tickets accumulate lessons in the file
- [ ] No errors when processing tickets without lessons
