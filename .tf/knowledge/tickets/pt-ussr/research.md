# Research: pt-ussr

## Status
Research enabled. No additional external research was performed - using existing codebase and project documentation.

## Context Reviewed

### Ticket Requirements
- Update Ralph progress indicator to show ready/blocked counts (R:<n> B:<n>) and done/total
- Display format: `R:3 B:2 (done 1/6)` in TTY, readable format in non-TTY
- In non-TTY mode, output remains readable (no animated control characters)
- Counts update when deps resolve (blocked → ready)

### Existing Code

#### Queue State Module (tf/ralph/queue_state.py)
Already exists with:
- `QueueStateSnapshot` dataclass with ready/blocked/running/done/total
- `get_queue_state()` function to compute from scheduler state
- `__str__()` method formats as `R:3 B:2 (done 1/6)`
- `to_log_format()` method for log lines

#### ProgressDisplay Class (tf/ralph.py)
Current behavior:
- Shows `[x/y] Processing {ticket}...` format
- TTY mode: uses carriage return + clear line (`\x1b[2K\r`)
- Non-TTY mode: plain text, no control characters
- Tracks `completed`, `failed`, `total` internally

#### Logger (tf/logger.py)
- `log_ticket_start()` - logs when ticket processing starts
- `log_ticket_complete()` - logs when ticket completes
- Need to add queue state to these messages

#### Ralph Loop (ralph_start function)
- Serial mode: processes tickets one at a time
- Needs to track pending/running/completed sets
- Progress display is initialized if `--progress` flag is used

## Implementation Plan

1. **Update ProgressDisplay class**:
   - Add queue_state parameter to start_ticket() and complete_ticket()
   - Update _draw() to include R/B counts in the format
   - Keep TTY vs non-TTY handling

2. **Update logger methods**:
   - Add queue_state parameter to log_ticket_start() and log_ticket_complete()
   - Include queue state in log output

3. **Update Ralph loop**:
   - Track pending, running, completed ticket sets
   - Compute queue state using queue_state module
   - Pass queue state to progress display and logger

## References
- Plan: plan-ready-blocked-counts-ralph
- Seed: seed-show-ready-and-blocked-ticket-count
- Related tickets: pt-g6be (logging), pt-ri6k (tests)
