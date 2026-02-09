# Implementation: pt-qayw

## Summary
Added `ticket_title` context field to RalphLogger so verbose logs include the ticket title alongside the ID. This makes Ralph runs easier to understand and debug when viewing logs.

## Changes Made

### 1. `tf_cli/logger.py`
- Added `ticket_title` parameter to `create_logger()` factory function
- Added `ticket_title` parameter to `log_ticket_start()` method
- Added `ticket_title` parameter to `log_ticket_complete()` method
- Added `ticket_title` parameter to `log_command_executed()` method
- Added `ticket_title` parameter to `log_error_summary()` method
- Added `ticket_title` parameter to `log_worktree_operation()` method

When `ticket_title` is provided, it is included in the log output context fields. When not provided, it is gracefully omitted (no "<unknown>" placeholder).

### 2. `tf_cli/ralph.py`
- Added `extract_ticket_titles()` helper function to fetch titles for multiple tickets efficiently
- Updated `ralph_run()` to fetch ticket title and pass to logger context and log methods
- Updated `ralph_start()` serial mode to fetch and pass ticket title for each ticket
- Updated `ralph_start()` parallel mode to:
  - Fetch titles for all selected tickets in batch
  - Pass ticket_title to worktree operation logs
  - Pass ticket_title to command execution logs
  - Pass ticket_title to error summary logs
  - Pass ticket_title to ticket completion logs

## Key Design Decisions

1. **Graceful fallback**: When title is unavailable, the field is simply omitted from logs rather than showing "<unknown>" or similar placeholder. This keeps logs clean.

2. **Caching**: The `extract_ticket_title()` function is called once per ticket and the result is passed through the logging context. This avoids repeated subprocess calls.

3. **Consistent API**: All ticket-related log methods now accept an optional `ticket_title` parameter, making the API consistent across the codebase.

4. **Non-verbose output unchanged**: When log level is INFO or higher, the output format remains the same - only the context fields change. The title appears alongside other context fields.

## Example Output

```
2026-02-07T16:54:48Z | INFO | mode=serial | ticket=pt-qayw | ticket_title="Add ticket_title context field to RalphLogger" | Starting ticket processing: pt-qayw
```

## Tests
- All existing tests pass (41 in test_logger.py, 38 in test_ralph_logging.py)
- Manual verification confirms ticket_title appears in verbose logs when provided
- Manual verification confirms ticket_title is omitted when not provided
