# Implementation: pt-yx8a

## Summary
Defined the timestamp format and placement specification for Ralph `--progress` output. This ticket produces a decision document that unblocks the implementation work in pt-d68t.

## Decision Record

### Timestamp Format
**Decision**: Local time in `HH:MM:SS` (24-hour format)

**Rationale**:
- Compact and readable
- Sufficient precision for Ralph progress tracking (seconds-level)
- No date needed for typical same-day Ralph runs
- Local time is more intuitive than UTC for users watching progress
- Aligns with MVP constraint of minimal config surface

### Placement
**Decision**: Prefix before the `[i/total]` counter

**Format**: `HH:MM:SS [i/total] message`

**Examples**:
```
14:32:05 [1/5] Processing pt-abc123...
14:32:05 [1/5] ✓ pt-abc123 complete
14:35:22 [2/5] Processing pt-def456...
14:35:22 [2/5] ✓ pt-def456 complete
```

**Rationale**:
- Timestamp is metadata that should prefix the operational content
- Follows standard logging conventions (timestamp first)
- Easy to scan visually for time correlation

### Application Scope
**Decision**: Apply timestamps to both start AND completion lines

**Rationale**:
- Provides complete temporal context for each step
- Users can calculate elapsed time per ticket by comparing timestamps
- Consistent output format for all progress lines
- No configuration needed (MVP constraint)

### TTY vs Non-TTY Behavior
**Decision**: Same timestamp format for both output modes

| Mode | Behavior |
|------|----------|
| TTY | Timestamp appears with in-place updates (carriage return) |
| Non-TTY | Timestamp appears on completion lines only |

**Rationale**:
- No additional complexity needed
- Existing control character logic in `_draw()` handles mode differences
- Non-TTY mode intentionally suppresses intermediate progress to avoid log spam

## Implementation Guidance for pt-d68t

### Code Changes Required

1. **Modify `ProgressDisplay._draw()` method** in `tf_cli/ralph.py`:
   - Import `datetime` if not already available
   - Generate timestamp at the start of `_draw()`
   - Prefix timestamp to the text before output

2. **Suggested implementation**:
```python
def _draw(self, text: str, final: bool = False) -> None:
    """Draw progress line with timestamp prefix."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    full_text = f"{timestamp} {text}"
    
    if self.is_tty:
        clear_seq = "\x1b[2K\r"
        self.output.write(f"{clear_seq}{full_text}")
        if final:
            self.output.write("\n")
        self.output.flush()
    else:
        if final:
            self.output.write(f"{full_text}\n")
            self.output.flush()
```

3. **Update tests** in `tests/test_progress_display.py`:
   - Update assertions to expect timestamp prefix
   - Verify timestamp format matches `HH:MM:SS` pattern
   - Ensure TTY and non-TTY tests both account for timestamps

### Acceptance Criteria for pt-d68t
- [ ] Progress output includes timestamp in `HH:MM:SS` format
- [ ] Timestamp appears before `[i/total]` counter
- [ ] Both start and completion lines include timestamps
- [ ] TTY mode works correctly with in-place updates
- [ ] Non-TTY mode shows timestamps on completion lines
- [ ] Tests updated and passing

## Files Changed
- `.tf/knowledge/tickets/pt-yx8a/research.md` (created)
- `.tf/knowledge/tickets/pt-yx8a/implementation.md` (created)

## Verification
This decision document provides the specification needed to unblock pt-d68t. The implementation ticket can proceed with the code changes outlined above.

## Notes
- No code changes were made in this ticket - it is a specification/decision task
- The blocking relationship to pt-d68t can now be resolved
- This follows the pattern established in pt-7mvl (decision ticket with explicit Decision section)
