# Implementation: pt-zloh

## Summary
Implemented `--pi-output` handling for `tf ralph` by adding output routing logic to the `run_ticket()` function. The feature allows redirecting pi subprocess stdout/stderr to a file, discarding it, or inheriting the terminal (default).

## Files Changed
- `tf_cli/ralph.py` - Added pi_output and pi_output_file parameters to `run_ticket()`, updated `ralph_run()` and `ralph_start()` to pass these parameters
- `tests/test_pi_output.py` - New comprehensive test suite for the feature

## Key Changes

### 1. `run_ticket()` function (lines 203-307)
Added two new parameters:
- `pi_output: str = "inherit"` - Output mode: "inherit", "file", or "discard"
- `pi_output_file: Optional[str] = None` - Custom log file path for file mode

Implemented output routing logic:
- **inherit** (default): Passes output to terminal (previous behavior)
- **file**: Writes stdout/stderr to `.tf/ralph/logs/<ticket>.log` or custom path
- **discard**: Redirects output to `os.devnull`

On failure with file mode, prints exit code and log path for debugging.

### 2. `ralph_run()` function (lines 966-1026)
- Extracts `pi_output` and `pi_output_file` from parsed args
- Passes them to `run_ticket()`
- Sets up `logs_dir` for both JSON capture AND pi output file mode

### 3. `ralph_start()` function (lines 1029+)
- Extracts `pi_output` and `pi_output_file` from options
- Passes them to `run_ticket()` in serial loop
- Sets up `logs_dir` for both JSON capture AND pi output file mode

## Acceptance Criteria
- [x] `--pi-output=inherit` preserves current behavior
- [x] `--pi-output=file` writes output to `.tf/ralph/logs/<ticket>.log` (or `--pi-output-file`)
- [x] `--pi-output=discard` suppresses output
- [x] On failure, print exit code + the log path when file capture is enabled

## Tests Run
```bash
$ python3 -m pytest tests/test_pi_output.py -v
27 passed

$ python3 -m pytest tests/test_json_capture.py tests/test_pi_output.py tests/test_ralph_logging.py -v
105 passed
```

## Verification
Test the feature manually:
```bash
# Test inherit mode (default)
tf ralph run --pi-output=inherit TICKET-123

# Test file mode
tf ralph run --pi-output=file TICKET-123
# Output goes to .tf/ralph/logs/TICKET-123.log

# Test file mode with custom path
tf ralph run --pi-output=file --pi-output-file=/tmp/pi.log TICKET-123

# Test discard mode
tf ralph run --pi-output=discard TICKET-123
```
