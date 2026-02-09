# Research: pt-ooda

## Status
Research completed. No external research needed - this is an internal testing ticket.

## Context Reviewed

### Ticket Analysis
- **Type**: Manual testing task
- **Scope**: Verify document opening feature with various pagers/editors
- **Blocking**: pt-d9rg (terminal suspend implementation)

### Code Review

#### Current Implementation Location
File: `tf_cli/ui.py` (TopicBrowser class, ~lines 540-610)

Key findings:
1. `_open_doc` method exists in `TopicBrowser` class
2. Uses `os.system(cmd)` directly WITHOUT `self.app.suspend()`
3. Action methods (`action_open_doc`, etc.) are in `TopicBrowser`, not `TicketflowApp`

#### Current Flow
```python
def _open_doc(self, topic: Topic, doc_type: str) -> None:
    # ... validation ...
    
    # Determine command to use
    pager = os.environ.get("PAGER", "").strip()
    editor = os.environ.get("EDITOR", "").strip()
    
    cmd = None
    if pager:
        cmd = f'{pager} "{full_path}"'
    elif editor:
        cmd = f'{editor} "{full_path}"'
    else:
        # Fallback to common pagers
        for fallback in ["less", "more", "cat"]:
            ...
    
    # Run the command - ISSUE: No terminal suspend!
    exit_code = os.system(cmd)
```

#### Environment Variables Used
- `$PAGER` - Preferred pager (less, more, etc.)
- `$EDITOR` - Preferred editor (vim, nano, etc.)
- Fallback chain: less → more → cat

### Test Scenarios Required

Based on acceptance criteria:
1. **PAGER tests**: less, more, fallback (none set)
2. **EDITOR tests**: vim, nano
3. **Error cases**: missing document, no topic selected
4. **TUI restoration**: verify interface after each test

### Dependencies
- pt-d9rg: Must add terminal suspend before meaningful testing
- Current state: Document opening will likely fail or behave incorrectly without suspend fix

## Sources
- `tf_cli/ui.py` - Lines 540-610
- `tk show pt-ooda`
- `tk show pt-d9rg`
- `.tf/knowledge/topics/seed-fix-tui-doc-opening/seed.md`
