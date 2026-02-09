# Implementation: pt-qu8a

## Summary
Changed the progress display total for `tf ralph start --progress` to reflect the number of ready tickets computed once at loop start, instead of using `max_iterations` (default 50).

## Files Changed
- `tf_cli/ralph.py` - Modified the serial loop to compute ready tickets count once at start

## Key Changes

### 1. Added Union import for type hints
```python
from typing import Any, Dict, List, Optional, TextIO, Tuple, Union
```

### 2. Updated ProgressDisplay to accept int or str for total
- Changed `self.total` type from `int` to `Union[int, str]`
- Changed `start_ticket` parameter `total_tickets` from `int` to `Union[int, str]`
- This allows displaying "?" when ticket listing fails

### 3. Compute ready tickets once at loop start
In `ralph_start()`, before the while loop:
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

### 4. Use pre-computed count in progress display
Inside the loop, when updating progress:
```python
if progress_display:
    # Use pre-computed ready tickets count for progress display
    # If listing failed, show '?' as placeholder instead of default 50
    if ready_tickets_count is not None:
        total_display = str(ready_tickets_count)
    else:
        total_display = "?"
    progress_display.start_ticket(ticket, iteration, total_display)
```

## Acceptance Criteria Verification

- [x] Progress display total is derived from `len(list_ready_tickets(...))` computed once at loop start
- [x] If ticket listing fails, progress shows "?" as placeholder total (avoid showing 50)
- [x] No behavior change when `--progress` is not used (progress_display is None, code skipped)

## Tests Run
- `tests/test_progress_display.py` - 22 tests passed
- `tests/test_ralph_state.py` - passed
- `tests/test_ralph_pi_invocation.py` - passed
- `tests/test_ralph_logging.py` - passed
- `tests/test_ralph_session_dir.py` - passed

## Behavior

### Before
Progress showed `[1/50]`, `[2/50]`, etc. (using max_iterations as total)

### After  
Progress shows `[1/5]`, `[2/5]`, etc. (using actual ready tickets count computed once)

If ticket listing fails, shows `[1/?]` instead of defaulting to 50.
