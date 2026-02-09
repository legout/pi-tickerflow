# Implementation: pt-yeny

## Summary
Implemented a ticket loader module (`tf_cli/ticket_loader.py`) that reads `.tickets/*.md` files and returns ticket metadata for the UI. The loader supports lazy loading of full ticket body content to keep startup fast when dealing with hundreds of tickets.

## Files Changed
- `tf_cli/ticket_loader.py` (new) - Core ticket loader implementation
- `tests/test_ticket_loader.py` (new) - Comprehensive test suite with 45 tests

## Implementation Details

### Ticket Data Class
- `Ticket` dataclass with fields: id, status, title, file_path, deps, tags, assignee, external_ref, priority, ticket_type, created, links
- Lazy body loading via `@property body` that reads from disk only when accessed
- `get_summary()` method for display formatting

### TicketLoader Class
- `load_all()` - Loads all tickets from `.tickets/*.md` (metadata only, fast)
- `get_by_id()` - Retrieve ticket by ID
- `get_by_status()` - Filter by status (open/closed/etc)
- `get_by_tag()` - Filter by tag
- `get_by_assignee()` - Filter by assignee
- `search()` - Case-insensitive search across ID, title, and tags
- `count_by_status` - Property for status distribution

### Frontmatter Parsing
- Primary: PyYAML (`yaml.safe_load()`) when available
- Fallback: Basic parser for simple key: value and key: [list] formats
- Handles: strings, integers, booleans, lists, empty values

### Error Handling
- Malformed tickets are skipped with warning logs (no crash)
- Missing tickets directory raises `TicketLoadError`
- File read errors during lazy loading return empty body

### Performance
- Eager loading: frontmatter + title only (fast for ~100s of tickets)
- Lazy loading: full body only read when `.body` property accessed
- No subprocess calls to `tk show` per ticket

## Key Decisions
1. **Separate Ticket and TicketLoader classes** - Clean separation of concerns, matches Topic/TopicLoader pattern in ui.py
2. **Dataclass for Ticket** - Immutable-ish, auto-generated methods, type hints
3. **Regex-based frontmatter extraction** - Fast, no dependencies required
4. **YAML with basic fallback** - Robust parsing when PyYAML available, still works without it
5. **Lazy body loading** - Essential for UI performance with many tickets

## Tests Run
```bash
pytest tests/test_ticket_loader.py -v
```
Result: 45 tests passed

Coverage:
- Frontmatter pattern matching
- Title extraction
- Ticket creation and lazy loading
- TicketLoader operations (load, filter, search)
- Basic frontmatter parser fallback
- Formatting utilities
- Error handling (missing files, malformed tickets)

## Verification
1. Import test: `from tf_cli.ticket_loader import TicketLoader` - ✓
2. Unit tests: All 45 pass - ✓
3. Integration with existing codebase: Follows patterns from TopicIndexLoader - ✓

## Usage Example
```python
from tf_cli.ticket_loader import TicketLoader

loader = TicketLoader()
tickets = loader.load_all()

for ticket in tickets:
    print(f"[{ticket.status}] {ticket.id}: {ticket.title}")
    # Body loaded only when accessed:
    if "urgent" in ticket.body:
        print("URGENT!")
```
