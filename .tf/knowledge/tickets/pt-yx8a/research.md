# Research: pt-yx8a

## Ticket Context
Define timestamp format and placement for Ralph `--progress` output.

## Current Implementation Analysis

### ProgressDisplay Class Location
- File: `tf_cli/ralph.py` (lines 34-83)
- Class: `ProgressDisplay`

### Current Output Format
```python
# start_ticket() outputs:
"[{iteration + 1}/{total_tickets}] Processing {ticket_id}..."
# Example: "[1/5] Processing pt-abc123..."

# complete_ticket() outputs:
"[{iteration + 1}/{self.total}] {msg}"
# Example: "[1/5] ✓ pt-abc123 complete"
```

### TTY vs Non-TTY Behavior
- **TTY mode**: Uses `\x1b[2K\r` (clear line + carriage return) for in-place updates
- **Non-TTY mode**: Plain text with newlines, no control characters
- Both modes use the same text format, only the control characters differ

### Key Constraints from Seed
1. Minimal config surface for MVP (hardcode sensible format)
2. Safe for TTY (in-place) and non-TTY (newline) output
3. No changes when `--progress` is not enabled

## Decision Requirements

### 1. Timestamp Format
**MVP Recommendation**: Local `HH:MM:SS` (24-hour format)
- Rationale: Easy to read, compact, universally understood
- No date component needed for same-day Ralph runs
- Local time is more intuitive for users than UTC

### 2. Placement
**Decision**: Prefix before `[i/total]` counter
- Format: `HH:MM:SS [i/total] ...`
- Example: `14:32:05 [1/5] Processing pt-abc123...`

### 3. Application Scope
**Decision**: Apply to both start and completion lines
- Start: `14:32:05 [1/5] Processing pt-abc123...`
- Complete: `14:32:05 [1/5] ✓ pt-abc123 complete`
- This provides full temporal context for each step

### 4. TTY vs Non-TTY
**Decision**: Same timestamp format for both modes
- TTY: Timestamps appear with in-place updates
- Non-TTY: Timestamps appear on completion lines only
- No special handling needed - the existing control character logic remains

## Implementation Notes for pt-d68t

The implementing ticket (pt-d68t) will need to:

1. Add timestamp generation to `ProgressDisplay._draw()` method
2. Use `datetime.now()` for local time
3. Format as `%H:%M:%S`
4. Prefix the timestamp before the existing message
5. Ensure timestamp is included in both start and complete outputs

Example implementation approach:
```python
def _draw(self, text: str, final: bool = False) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    full_text = f"{timestamp} {text}"
    # ... rest of existing logic using full_text instead of text
```

## References
- Seed: `seed-add-timestamps-to-the-progressbar-when-r`
- Blocking: pt-d68t (implementation ticket)
