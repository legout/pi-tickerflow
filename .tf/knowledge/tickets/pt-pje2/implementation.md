# Implementation: pt-pje2

## Summary
Added CLI parsing and help text for progress and Pi-output suppression flags to `tf ralph run` and `tf ralph start` commands.

## Files Changed

### 1. `tf_cli/ralph.py`
**Changes:**
- Updated `usage()` function to document new flags:
  - `--progress`, `--progressbar` - Enable progress indicator (serial mode only)
  - `--pi-output MODE` - Control pi subprocess output (inherit/file/discard)
  - `--pi-output-file PATH` - Override default log file path

- Updated `parse_run_args()` to parse new flags:
  - Now returns 8 values including `progress`, `pi_output`, `pi_output_file`
  - Supports both `--progress` and `--progressbar` aliases
  - Supports both `--key value` and `--key=value` syntax

- Updated `parse_start_args()` to parse same flags:
  - Added `progress`, `pi_output`, `pi_output_file` to options dict

- Added `_validate_pi_output()` helper function to validate pi_output values

- Updated `ralph_run()` to:
  - Handle new return values from parse_run_args
  - Validate pi_output value (must be inherit/file/discard)

- Updated `ralph_start()` to:
  - Handle new options from parse_start_args
  - Validate pi_output value
  - Validate that `--progress` is not used with `--parallel > 1`

### 2. `tests/test_json_capture.py`
**Changes:**
- Updated existing tests to handle new return values from `parse_run_args()`
- Added `TestParseProgressFlags` test class with 14 new tests covering:
  - `--progress` and `--progressbar` flag parsing for both run and start
  - `--pi-output` value parsing (inherit/file/discard)
  - `--pi-output-file` path parsing (both syntaxes)
  - Default values when flags not provided
  - Combined flag usage

## Key Decisions

1. **Default behavior unchanged**: All new flags are opt-in; existing behavior is preserved when flags are not used.

2. **Validation included**: 
   - Invalid `--pi-output` values result in error message and exit code 1
   - `--progress` with parallel mode is rejected (per MVP scope guard in plan)

3. **Help text updated**: The `usage()` function documents all new flags with descriptions.

4. **Syntax flexibility**: Both `--key value` and `--key=value` forms are supported for consistency with existing flags.

## Tests Run

```bash
# All existing tests pass
$ python -m pytest tests/ -v
702 passed

# New progress flag tests
$ python -m pytest tests/test_json_capture.py::TestParseProgressFlags -v
14 passed
```

## Verification

- `tf ralph --help` displays new flags in help text
- Invalid `--pi-output=invalid` produces error
- `--progress --parallel 2` produces error in `ralph start`
- Flags are correctly parsed and returned to calling functions

## Notes

This ticket only implements CLI parsing and validation. The actual output routing and progress rendering will be implemented in follow-up tickets:
- pt-zloh: Implement pi subprocess output routing (inherit/file/discard)
- pt-pnli: Implement serial progress display for tf ralph (per-ticket)
