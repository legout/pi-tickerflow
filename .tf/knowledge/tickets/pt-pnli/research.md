# Research: pt-pnli

## Status
Research enabled. No additional external research was performed - implementation is straightforward using Python stdlib.

## Context Reviewed
- `tk show pt-pnli` - Ticket requirements
- `tf_cli/ralph.py` - Main ralph implementation
- `tf_cli/logger.py` - Logging system
- `tf_cli/cli.py` - CLI entry point

## Key Requirements
1. Add `--progress` flag to `tf ralph start`
2. Per-ticket progress display in serial mode
3. Updates at ticket boundaries (start/complete/fail)
4. No control characters in non-TTY contexts
5. `--progress` forces `--pi-output=file` in TTY (unless `discard`), or warns+overrides
6. `--progress` rejected for parallel mode

## Implementation Plan
1. Create `ProgressDisplay` class in ralph.py (stdlib only)
2. Detect TTY using `sys.stderr.isatty()`
3. In TTY mode: use `\r` + clear line escape sequences for stable progress line
4. In non-TTY mode: plain text output, no control characters
5. Hook into ticket start/complete/fail events in the serial loop
6. Enforce `--pi-output=file` when `--progress` is used in TTY mode

## Files to Modify
- `tf_cli/ralph.py` - Add ProgressDisplay class and integrate into ralph_start
