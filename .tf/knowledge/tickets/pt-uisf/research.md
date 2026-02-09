# Research: pt-uisf

## Status
Research enabled. No additional external research was performed.

## Rationale
- This is a straightforward unit test implementation task
- The existing codebase provides clear patterns to follow
- ticket `pt-pnli` (parent/linked ticket) already implemented the feature, so implementation patterns are available in the codebase

## Context Reviewed
- `tk show pt-uisf` - Ticket description and acceptance criteria
- `tests/test_pi_output.py` - Existing tests for --pi-output flags
- `tests/test_json_capture.py` - Existing tests for --capture-json and --progress flags
- `tf_cli/ralph.py` - Implementation of ProgressDisplay class and output routing

## Existing Test Coverage Analysis

### Already Covered (test_json_capture.py):
- `--progress` flag parsing for run/start
- `--pi-output` flag parsing (inherit/file/discard)
- `--pi-output-file` flag parsing
- Combined flag parsing

### Already Covered (test_pi_output.py):
- `_validate_pi_output()` function
- `parse_run_args()` pi_output parsing
- `parse_start_args()` pi_output parsing
- `run_ticket()` with different pi_output modes
- Dry run output notes

### Missing Coverage (identified):
1. **Non-TTY progress behavior** - No tests for ProgressDisplay class's non-TTY mode
2. **Output routing without subprocess** - Need tests that verify output routing decisions without actually calling subprocess.run

## Sources
- `/home/volker/coding/pi-ticketflow/tf_cli/ralph.py` lines 32-76 (ProgressDisplay class)
- `/home/volker/coding/pi-ticketflow/tests/test_pi_output.py`
- `/home/volker/coding/pi-ticketflow/tests/test_json_capture.py`
