# Research: pt-zloh

## Status
Research complete. The feature requires implementing `--pi-output` handling in `run_ticket()` function.

## Context Reviewed

### Current State
- `tf_cli/ralph.py` has `run_ticket()` function at line 203
- The function already parses `--pi-output` and `--pi-output-file` flags in `parse_run_args()` and `parse_start_args()`
- However, `run_ticket()` doesn't accept or use these parameters - it only handles `capture_json`

### Required Changes
1. Add `pi_output` and `pi_output_file` parameters to `run_ticket()`
2. Pass these through all call sites:
   - `ralph_run()` → `run_ticket()`
   - `ralph_start()` serial loop → `run_ticket()`
   - Parallel mode uses `subprocess.Popen` (different handling)
3. Implement output routing logic:
   - `inherit`: current behavior (subprocess.run without capture)
   - `file`: redirect stdout/stderr to log file
   - `discard`: redirect to DEVNULL
4. On failure with file capture: print exit code + log path

### Acceptance Criteria Mapping
- [x] `--pi-output=inherit` preserves current behavior
- [ ] `--pi-output=file` writes output to `.tf/ralph/logs/<ticket>.log` (or `--pi-output-file`)
- [ ] `--pi-output=discard` suppresses output
- [ ] On failure, print exit code + the log path when file capture is enabled

## Implementation Plan
1. Modify `run_ticket()` signature and body
2. Update `ralph_run()` to pass pi_output params
3. Update `ralph_start()` serial loop to pass pi_output params
4. Add test coverage

## Sources
- `tf_cli/ralph.py` - main implementation file
- `tests/test_json_capture.py` - test patterns for similar features