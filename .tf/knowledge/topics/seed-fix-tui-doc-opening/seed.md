# Seed: Fix TUI document opening keys (o, 1, 2, 3, 4)

## Problem Statement
In the `tf ui` TUI, pressing `o`, `1`, `2`, `3`, or `4` to open topic documents (overview, sources, plan, backlog) does not work. Nothing happens when these keys are pressed.

## Root Cause Analysis (from debugging)

Two issues were identified:

### Issue 1: Action Methods in Wrong Class
The key bindings are defined in `TicketflowApp` class:
```python
class TicketflowApp(App):
    BINDINGS = [
        Binding("o", "open_doc", "Open Doc"),
        Binding("1", "open_overview", "Overview"),
        Binding("2", "open_sources", "Sources"),
        Binding("3", "open_plan", "Plan"),
        Binding("4", "open_backlog", "Backlog"),
    ]
```

However, the action methods (`action_open_doc`, `action_open_overview`, etc.) are defined in the `TopicBrowser` class (lines ~545-572 in `tf_cli/ui.py`), not in `TicketflowApp`.

**In Textual**, when a key is pressed, the framework looks for `action_{name}` methods on the class where the binding is defined. Since `TicketflowApp` only has `action_refresh` and lacks the document-opening action methods, the key presses are silently ignored.

### Issue 2: Missing Terminal Suspend
Even if the actions were in the correct class, the `_open_doc` method uses `os.system(cmd)` directly:

```python
exit_code = os.system(cmd)
```

This runs while Textual has the terminal in raw/cooked mode. External pagers like `less` or editors like `vim` need the terminal in normal mode. Without suspending the Textual app first, the pager would receive garbled input or appear unresponsive.

**The fix** requires using Textual's suspend mechanism:
```python
with self.app.suspend():
    os.system(cmd)
```

This temporarily restores terminal control to the shell, runs the command, then returns control to Textual.

## Proposed Solution

1. **Move or delegate action methods**: Either:
   - Move `action_open_doc`, `action_open_overview`, `action_open_sources`, `action_open_plan`, `action_open_backlog` from `TopicBrowser` to `TicketflowApp`, OR
   - Keep them in `TopicBrowser` but add delegating methods in `TicketflowApp` that call the `TopicBrowser` methods

2. **Add terminal suspend**: Wrap the `os.system()` call in `_open_doc` method with `self.app.suspend()` context manager

3. **Consider active tab context**: The keys should probably only work when the Topics tab is active, not when Tickets tab is active

## Files to Modify
- `tf_cli/ui.py` - Main TUI implementation

## Open Questions
- Should the document-opening keys be disabled when the Tickets tab is active?
- Should there be visual feedback (notification) when trying to open a doc but no topic is selected?
