# Implementation: pt-psvv

## Summary
Added dry-run output enhancements and optional reclassify report artifact for the `tf priority-reclassify` command.

## Changes Made

### 1. Added `--json` flag for JSON output
- Modified `print_results()` function to support JSON output format
- JSON output includes:
  - `mode`: "dry-run" or "apply"
  - `tickets`: Array of ticket objects with id, title, current, proposed, bucket, reason, confidence, would_change
  - `summary`: Counts of total, would_change, unknown, unchanged

### 2. Made report file optional with `--report` flag
- Changed `write_audit_trail()` to only run when `--report` is specified
- Report file path: `.tf/knowledge/priority-reclassify-{timestamp}.md`
- Without `--report`, only stdout output is produced (table or JSON)

### 3. Updated tests
- Added `TestJsonOutput` class with tests for JSON format and mode
- Added `TestReportFlag` class with tests for optional report generation
- Updated help output test to include new flags

## Files Changed
- `tf_cli/priority_reclassify_new.py` - Added --json and --report flags, updated print_results()
- `tests/test_priority_reclassify.py` - Added tests for new functionality

## Key Decisions
1. JSON output goes to stdout (for piping to other tools)
2. Report file is now opt-in (--report) rather than always written
3. Human-readable table remains the default output format
4. Both --json and --report can be used together (JSON to stdout, report to file)

## Tests Run
```bash
python -m pytest tests/test_priority_reclassify.py -v
# 30 tests passed
```

## Verification
```bash
# JSON output
python -m tf_cli.priority_reclassify_new --ids pt-psvv --json

# Table output (default)
python -m tf_cli.priority_reclassify_new --ids pt-psvv

# With report file
python -m tf_cli.priority_reclassify_new --ids pt-psvv --report
```

## Acceptance Criteria
- [x] Human-readable table printed (id, title, current, proposed, reason)
- [x] Optional `--json` output for scripting
- [x] Optional report file written under `.tf/knowledge/` (path documented)
- [x] Report must not contain secrets; only ticket metadata
