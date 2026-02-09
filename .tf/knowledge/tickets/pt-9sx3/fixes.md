# Fixes: pt-9sx3

## Summary
Applied fixes for 3 minor issues identified during review.

## Fixes Applied

### 1. Removed unused import
**File:** `tf_cli/ui.py:411`  
**Change:** Removed `DataTable` from imports since it's not used in the implementation.

```python
# Before
from textual.widgets import (
    Static, Header, Footer, ListView, ListItem, Label,
    TabbedContent, TabPane, Input, Markdown, DataTable
)

# After
from textual.widgets import (
    Static, Header, Footer, ListView, ListItem, Label,
    TabbedContent, TabPane, Input, Markdown
)
```

### 2. Fixed misleading UI text
**File:** `tf_cli/ui.py:603`  
**Change:** Removed reference to unimplemented 'o' keybinding.

```python
# Before
if len(ticket.body) > 500:
    body += "\n\n[i](truncated... press 'o' to open full ticket)[/i]"

# After
if len(ticket.body) > 500:
    body += "\n\n[i](truncated...)[/i]"
```

### 3. Improved type annotation
**File:** `tf_cli/ui.py:538` and import at top  
**Change:** Added `BoardView` to imports and used it for type annotation.

```python
# Added to imports
from tf_cli.board_classifier import BoardClassifier, BoardColumn, ClassifiedTicket, BoardView

# Changed type annotation
# Before
board_view: reactive[Optional[object]] = reactive(None)

# After
board_view: reactive[Optional[BoardView]] = reactive(None)
```

## Verification
- Syntax check: ✓ Passed
- Import check: ✓ Passed  
- Unit tests: ✓ 79 passed

## Files Changed
- `tf_cli/ui.py` - 3 minor fixes applied
