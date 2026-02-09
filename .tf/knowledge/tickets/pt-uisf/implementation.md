# Implementation: pt-uisf

## Summary
Added comprehensive unit tests for `tf ralph` progress display and pi-output flag behavior, covering non-TTY progress behavior and output routing modes without invoking external `pi` commands.

## Files Changed
- `tests/test_progress_display.py` - **NEW FILE** - 22 tests for ProgressDisplay class
- `tests/test_pi_output.py` - **MODIFIED** - Added 8 new tests for output routing

## Test Coverage Added

### 1. ProgressDisplay Tests (test_progress_display.py - 22 tests)

**TestProgressDisplayInit (4 tests):**
- `test_default_tty_detection` - Verifies TTY detection from output stream
- `test_explicit_tty_true` - Tests explicit is_tty=True
- `test_explicit_tty_false` - Tests explicit is_tty=False
- `test_initial_state` - Verifies initial counter and state values

**TestProgressDisplayNonTTY (6 tests):**
- `test_start_ticket_no_output` - Non-TTY: intermediate progress suppressed
- `test_complete_ticket_success_newline` - Non-TTY: plain text with newline, no control chars
- `test_complete_ticket_failure_newline` - Non-TTY: failure output with newline
- `test_complete_unknown_status` - Non-TTY: unknown status handling
- `test_no_control_characters_in_non_tty` - **Key AC test** - Verifies no escape sequences, CR, or bell chars
- `test_completed_counter_increments` - Counter tracking verification
- `test_failed_counter_increments` - Failed counter tracking

**TestProgressDisplayTTY (3 tests):**
- `test_start_ticket_clears_line` - TTY: escape sequence usage
- `test_complete_ticket_adds_newline` - TTY: newline handling
- `test_tty_intermediate_no_newline` - TTY: intermediate update format

**TestProgressDisplayCounters (4 tests):**
- `test_counters_accumulate` - Counter accumulation across tickets
- `test_current_ticket_cleared_on_complete` - State cleanup
- `test_iteration_number_in_output` - 1-indexed iteration display
- `test_iteration_number_mid_sequence` - Mid-sequence iteration display

**TestProgressDisplayIntegration (2 tests):**
- `test_full_ticket_sequence` - End-to-end ticket sequence
- `test_multiple_starts_no_output` - Multiple starts without completes

**TestProgressDisplayWithRealStream (2 tests):**
- `test_with_stderr_mock` - Stream handling
- `test_flush_is_called` - Output flushing verification

### 2. Output Routing Tests (test_pi_output.py - 8 new tests)

**TestOutputRoutingWithoutSubprocess (8 tests):**
- `test_inherit_mode_routing_decision` - Verifies inherit mode passes through stdout/stderr
- `test_file_mode_routing_decision` - Verifies file mode redirects to file handle
- `test_discard_mode_routing_decision` - Verifies discard mode redirects to devnull
- `test_file_mode_with_custom_path_decision` - Custom path routing verification
- `test_dry_run_shows_routing_decision_inherit` - Dry run inherit message
- `test_dry_run_shows_routing_decision_file` - Dry run file message
- `test_dry_run_shows_routing_decision_discard` - Dry run discard message

## Acceptance Criteria Coverage

| Criteria | Status | Test Location |
|----------|--------|---------------|
| Tests cover parsing of `--progress`, `--pi-output`, `--pi-output-file` for run/start | ✅ | test_json_capture.py (already existed) |
| Tests cover output routing modes (inherit/file/discard) without running `pi` | ✅ | test_pi_output.py::TestOutputRoutingWithoutSubprocess |
| Tests cover non-TTY progress behavior (no control characters) | ✅ | test_progress_display.py::TestProgressDisplayNonTTY |

## Key Decisions

1. **Used mocking for subprocess.run** - As specified in constraints, all subprocess calls are mocked rather than invoking external commands.

2. **Created separate test file for ProgressDisplay** - The ProgressDisplay class has substantial behavior worth its own test file rather than adding to existing files.

3. **Tested both TTY and non-TTY modes** - While the AC focuses on non-TTY behavior, testing both ensures the implementation is correct and documents expected behavior.

4. **Focused on observable behavior** - Tests verify actual output (no control chars, proper newlines) rather than just internal state.

## Tests Run

```bash
$ python -m pytest tests/test_progress_display.py tests/test_pi_output.py tests/test_json_capture.py -v

87 passed in 0.18s
```

All new and existing tests pass.

## Verification

To verify the implementation:
```bash
cd /home/volker/coding/pi-ticketflow
python -m pytest tests/test_progress_display.py tests/test_pi_output.py tests/test_json_capture.py -v
```
