# Implementation: pt-bb97

## Summary

Implemented Ready/Blocked board classification logic and comprehensive unit tests for the Ticketflow Kanban TUI.

## Files Changed

- `tf_cli/board_classifier.py` - New module implementing board classification logic
- `tests/test_board_classifier.py` - Comprehensive unit tests for classification

## Implementation Details

### Board Classification Rules (from plan-ticketflow-kanban-tui)

The classification logic follows the documented MVP rules:

- **Closed**: `status == "closed"` (regardless of dependencies)
- **In Progress**: `status == "in_progress"` AND all dependencies are closed
- **Blocked**: `status in {open, in_progress}` AND any dependency is not closed
- **Ready**: `status == "open"` AND all dependencies are closed

Key insight: A ticket with `in_progress` status that has unmet dependencies is classified as **Blocked**, not In Progress. This ensures work doesn't start on tickets whose prerequisites aren't complete.

### Components Implemented

1. **BoardColumn Enum**: Defines the four board columns (`ready`, `blocked`, `in_progress`, `closed`)

2. **ClassifiedTicket**: Wrapper around Ticket that adds:
   - `column`: The assigned board column
   - `blocking_deps`: List of dependency IDs blocking this ticket
   - Helper methods: `is_ready()`, `is_blocked()`, `is_in_progress()`, `is_closed()`

3. **BoardClassifier**: Core classification engine
   - `classify_all()`: Load and classify all tickets from disk
   - `_classify_tickets()`: Classify a list of Ticket objects
   - Dependency graph resolution with cycle handling
   - Case-insensitive status matching

4. **BoardView**: Immutable snapshot of board state
   - `get_by_column()`: Get tickets in a specific column
   - `get_by_id()`: Lookup specific ticket
   - `counts`: Summary statistics
   - `filter_by_tag()`, `filter_by_assignee()`, `search()`: Filtering operations
   - Sorting by priority (desc) then ID (asc) within columns

5. **Convenience Functions**:
   - `classify_tickets()`: One-shot classification from Ticket list
   - `format_board_summary()`: Human-readable board summary

### Test Coverage

31 tests covering:

- **Classification Rules** (8 tests): Each rule with various inputs
- **Dependency Graph Scenarios** (4 tests): Linear chains, diamonds, parallel tasks, complex graphs
- **BoardView Operations** (9 tests): Query, filtering, search functionality
- **Sorting** (1 test): Priority and ID ordering
- **ClassifiedTicket Properties** (2 tests): Property delegation and helpers
- **BoardClassifier** (2 tests): Initialization with loader and explicit path
- **Case Insensitive Status** (1 test): Upper/lower/mixed case handling
- **Edge Cases** (4 tests): Empty lists, unknown status, self-referential and circular deps

## Key Decisions

1. **Classification Independence**: Logic is independent of UI rendering as required by constraints. The `BoardClassifier` operates purely on ticket data without Textual dependencies.

2. **Dependency Handling**: Missing dependencies (not found in ticket list) are treated as blocking. This is a conservative approach that prevents assuming work can proceed on tickets with unresolved external dependencies.

3. **Sorting**: Within each column, tickets are sorted by priority (highest first) then ID (alphabetical). This puts high-priority work at the top while maintaining stable ordering.

4. **Immutability**: `BoardView` is an immutable snapshot. Filter/search operations return new views rather than modifying the original.

5. **Lazy Loading Compatibility**: Works with the existing `TicketLoader` lazy body loading. Classification only needs frontmatter data.

## Verification

All tests pass:
```
31 passed in tests/test_board_classifier.py
889 passed in full test suite
```

## Integration Notes

The `BoardClassifier` is designed to be used by the TUI in `tf_cli/ui.py`:

```python
from tf_cli.board_classifier import BoardClassifier, BoardColumn

classifier = BoardClassifier()
board = classifier.classify_all()

# Get tickets for each column
ready_tickets = board.get_by_column(BoardColumn.READY)
blocked_tickets = board.get_by_column(BoardColumn.BLOCKED)
```

Future integration could include:
- Real-time board refresh (manual 'r' key already supported in TUI)
- Drag-and-drop support (when mutations are implemented)
- Column counts in the UI header
