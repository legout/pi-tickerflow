# Implementation: pt-pnli

## Summary
Implemented serial progress display for `tf ralph start` with conservative, stdlib-only approach.

## Files Changed
- `tf_cli/ralph.py` - Added ProgressDisplay class and integrated into serial loop

## Key Decisions
1. **ProgressDisplay class** - Uses stdlib only, no external dependencies
2. **TTY detection** - Uses `sys.stderr.isatty()` to detect terminal vs pipe/redirection
3. **TTY mode** - Uses `\x1b[2K\r` escape sequences to clear line and return to start for stable progress line
4. **Non-TTY mode** - Plain text output, no control characters, only final status on completion
5. **pi-output enforcement** - When `--progress` is used in TTY mode with `--pi-output=inherit`, automatically switches to `--pi-output=file` to prevent progress bar corruption from subprocess output

## Implementation Details

### ProgressDisplay Class
- `start_ticket(ticket_id, iteration, total)` - Shows `[n/total] Processing {ticket}...`
- `complete_ticket(ticket_id, status, iteration)` - Shows `[n/total] ✓ {ticket} complete` or `✗ {ticket} failed`
- `_draw(text, final)` - Handles TTY vs non-TTY rendering

### Integration Points
- Progress display initialized at start of serial loop when `--progress` flag is set
- `start_ticket()` called when ticket begins processing
- `complete_ticket()` called on both success and failure paths
- Enforces `--pi-output=file` when `--progress` is used in TTY mode (unless already set to `discard`)

## Acceptance Criteria Status
- [x] `tf ralph start --progress` renders a stable progress line to stderr in TTY
- [x] In non-TTY, progress output is plain text (no control chars)
- [x] `--progress` forces `--pi-output=file` in TTY (unless `discard`), or warns+overrides
- [x] `--progress` is rejected for parallel mode in MVP with a clear message

## Tests Run
- `python -m py_compile tf_cli/ralph.py` - Syntax check passed
- `python -m pytest tests/test_ralph_logging.py -v` - All 47 tests passed
- `python -m pytest tests/test_pi_output.py -v` - All 27 tests passed

## Verification
To verify the implementation works:
1. In a TTY: `tf ralph start --progress --max-iterations 1 --dry-run` - Should show progress line with escape sequences
2. In non-TTY: `tf ralph start --progress --max-iterations 1 --dry-run 2>&1 | cat` - Should show plain text output
3. Parallel rejection: `tf ralph start --progress --parallel 2` - Should error with clear message
