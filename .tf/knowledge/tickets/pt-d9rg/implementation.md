# Implementation: pt-d9rg

## Summary
Wrapped the `os.system()` call in the `_open_doc` method with `self.app.suspend()` context manager to properly suspend the Textual TUI before launching external pagers and editors.

## Files Changed
- `tf_cli/ui.py` - Modified `_open_doc()` method (around line 628-638)

## Key Changes

### Before:
```python
# Run the command
exit_code = os.system(cmd)
```

### After:
```python
# Run the command with terminal suspend for external pagers/editors
try:
    with self.app.suspend():
        exit_code = os.system(cmd)
except Exception as e:
    self.notify(f"Failed to suspend terminal: {e}", severity="error")
    return
```

## Key Decisions
1. **Used try/except block**: Added error handling around the suspend context manager to gracefully handle any suspend failures
2. **Early return on error**: If suspend fails, the method returns early without attempting to access `exit_code` (which would be undefined)
3. **Preserved existing notification flow**: Success/error notifications remain the same for document opening results

## Testing Notes
- Syntax validated with `python -c "import ui"`
- The change requires manual testing with `$PAGER` or `$EDITOR` environment variables set
- Test scenarios: less, more, vim, or any custom pager/editor

## Acceptance Criteria Status
- [x] Wrap the os.system() call with `with self.app.suspend():`
- [x] Add graceful error handling if suspend fails
- [ ] Test document opening with less pager (manual)
- [ ] Test document opening with vim editor (manual)
- [ ] Verify TUI resumes correctly after closing pager/editor (manual)
