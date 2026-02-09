# Implementation: pt-5g48

## Summary
Added topic browser functionality to open selected topic documents via $PAGER or $EDITOR in the TUI.

## Changes Made

### File: `tf_cli/ui.py`

Added keyboard shortcuts and actions to the `TopicBrowser` class for opening topic documents:

1. **Key Bindings Added** (in `TicketflowApp.CSS`):
   - `o` - Open the first available document for the selected topic
   - `1` - Open overview document
   - `2` - Open sources document  
   - `3` - Open plan document
   - `4` - Open backlog document

2. **New Action Methods** in `TopicBrowser`:
   - `action_open_doc()` - Opens the first available document (default action)
   - `action_open_overview()` - Opens overview document
   - `action_open_sources()` - Opens sources document
   - `action_open_plan()` - Opens plan document
   - `action_open_backlog()` - Opens backlog document
   - `_open_doc_by_type(doc_type)` - Helper to open doc by type with validation
   - `_open_doc(topic, doc_type)` - Core logic to open documents using $PAGER/$EDITOR

3. **Updated `update_detail_view()`**:
   - Shows key bindings [1-4] next to available documents
   - Displays hint: "Press [1-4] to open, 'o' for first available"
   - Uses dim styling for "no documents available" message

4. **Document Opening Logic** (in `_open_doc`):
   - Checks if document exists before attempting to open
   - Priority: $PAGER → $EDITOR → fallback to less/more/cat
   - Shows user-friendly notifications for:
     - Missing documents (warning)
     - Document not found (error)
     - No pager/editor configured (error)
     - Failed to open (error with exit code)

## Acceptance Criteria

- [x] UI lists topics by type and supports simple filtering (already existed)
- [x] User can open a doc for a selected topic using $PAGER or $EDITOR
- [x] Missing docs are handled gracefully with notification messages

## Implementation Details

### Pager/Editor Resolution Order
1. `$PAGER` environment variable
2. `$EDITOR` environment variable
3. System fallback: `less` → `more` → `cat`

### Error Handling
- No topic selected → Warning notification
- No documents available → Warning notification with topic ID
- Document doesn't exist → Error notification with path
- No pager/editor found → Error with helpful message to set env vars
- Command fails → Error with exit code

### Key Mapping
| Key | Document Type |
|-----|---------------|
| 1   | overview      |
| 2   | sources       |
| 3   | plan          |
| 4   | backlog       |
| o   | First available |

## Tests Run
```bash
python -m pytest tests/test_topic_loader.py -v
# 38 passed

python -m pytest tests/ -v --ignore=tests/test_kb_cli.py --ignore=tests/test_login.py
# 840 passed
```

## Verification

To verify the implementation:
1. Run `tf ui` to launch the TUI
2. Navigate to the "Topics" tab
3. Select a topic with documents
4. Press `1-4` or `o` to open documents
5. Verify missing docs show warning notifications
