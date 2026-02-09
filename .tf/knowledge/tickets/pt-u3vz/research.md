# Research: pt-u3vz

## Status
Research enabled. No additional external research was performed - this is a unit testing task for existing codebase.

## Rationale
- The ticket is about adding unit tests for existing functionality
- The parent ticket pt-qu8a already implemented the fix
- No external dependencies or research needed

## Context Reviewed
- `tk show pt-u3vz` - Ticket requirements
- `tk show pt-qu8a` - Parent ticket implementation details
- `tf_cli/ralph.py` - Source code with progress display logic
- `tests/test_progress_display.py` - Existing progress display tests
- `tests/test_ralph_state.py` - Testing patterns for ralph module

## Key Findings

The fix in pt-qu8a computes `ready_tickets_count` once at loop start:

```python
# Compute ready tickets count once at loop start for accurate progress display
ready_tickets_count: Optional[int] = None
if progress:
    try:
        ready_tickets = list_ready_tickets(ticket_list_query(ticket_query))
        ready_tickets_count = len(ready_tickets) if ready_tickets else None
    except Exception:
        ready_tickets_count = None
```

And uses it in progress display:
```python
if ready_tickets_count is not None:
    total_display = str(ready_tickets_count)
else:
    total_display = "?"
progress_display.start_ticket(ticket, iteration, total_display)
```

## Test Requirements
1. Test that progress total equals actual ready ticket count (not maxIterations/default 50)
2. Test that '?' is shown when ticket listing fails
3. Mock all external calls (no shelling out to pi/tk)

## Sources
- (none - internal codebase only)
