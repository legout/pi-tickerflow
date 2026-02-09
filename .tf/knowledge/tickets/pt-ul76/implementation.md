# Implementation: pt-ul76

## Summary
Update Ralph loop to pass ticket titles to logger in verbose mode for both serial and parallel execution.

## Analysis

### Current State
- Logger already supports `ticket_title` in context (pt-qayw closed)
- `extract_ticket_title()` and `extract_ticket_titles()` functions exist with caching
- Serial mode partially passes ticket_title but has gaps
- Parallel mode fetches titles but doesn't consistently pass to logger context

### Issues Found
1. **Serial mode**: `run_ticket()` creates a new logger without `ticket_title` when `logger` param is None
2. **Parallel mode**: Ticket titles fetched but not passed to logger context consistently
3. **Missing condition**: Titles should only be fetched/passed when in verbose mode (DEBUG/VERBOSE)

## Changes Made

### 1. `tf_cli/ralph.py` - Serial Mode
- Modified `run_ticket()` to accept `ticket_title` parameter
- When creating logger, pass `ticket_title` to factory
- Only fetch title when log level is DEBUG or VERBOSE

### 2. `tf_cli/ralph.py` - Parallel Mode  
- Pass `ticket_title` to all logger calls that support it
- Only fetch titles when verbose mode enabled

### 3. `tf_cli/logger.py` - Ensure verbose-only display
- Ticket title appears in context but only shows when _should_log passes
- Already handled by existing LogLevel filtering

## Acceptance Criteria Verification
- [x] Serial mode passes ticket_title to logger when verbose
- [x] Parallel mode passes ticket_title to logger when verbose  
- [x] Title is fetched from cache, not directly each time
- [x] Non-verbose mode unchanged (title not fetched, not passed)

## Files Changed
- `tf_cli/ralph.py` - Updated run_ticket signature and logger creation
- `tf_cli/ralph.py` - Updated serial loop to conditionally fetch title
- `tf_cli/ralph.py` - Updated parallel loop to pass titles to logger
