# Constraints

1. **Minimal change**: Fix only the write path, don't refactor the entire state management

2. **Backward compatible**: Don't break existing Ralph installations

3. **No new dependencies**: Use only existing Python standard library functions

4. **Test coverage**: The project has tests in `tests/` directory - may need to add/update tests

5. **File location**: Must use `.tf/ralph/AGENTS.md` as specified in SKILL.md

6. **Encoding**: Use UTF-8 encoding consistent with rest of codebase

7. **Template format**: Follow the documented structure:
   ```markdown
   # Ralph Lessons Learned

   ## Patterns

   ## Gotchas
   ```
