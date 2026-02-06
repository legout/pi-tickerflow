# Review: pt-7cri

## Critical (must fix)
- None

## Major (should fix)
1. **Tests needed for new verbosity controls** (reviewer-general)
   - `tf_cli/ralph_new.py:287-807` - The new verbosity controls (argument parsing in `parse_run_args`/`parse_start_args`, the `resolve_log_level` utility, and the addition of the level flag to `workflow_flags`) are untested. Need tests for CLI flag combinations, environment-variable shortcuts, and propagation of the flag into the workflow invocation.

2. **CLI output doesn't respect log level** (reviewer-spec-audit) 
   - `tf_cli/ralph_new.py:197-218, 849-994` - The resolved `LogLevel` is never consulted when printing dry-run notices, `pi -p…` invocations, completion/loop-status lines, or warnings. The spec requires verbosity modes to gate which lifecycle events are shown. Note: This may be addressed in pt-rvpi when the logger helper is implemented.

## Minor (nice to fix)
- ✅ **FIXED**: `tf_cli/ralph_new.py:65-88` - The `usage()` text referenced `tf new ralph run/start` instead of `tf ralph run/start`. Updated to show the correct command.

## Warnings (follow-up ticket)
- None

## Suggestions (follow-up ticket)
- Add validation for `RALPH_LOG_LEVEL` env var to warn on invalid values
- Consider supporting `--log-level=<level>` as an alternative to individual flags

## Summary Statistics
- Critical: 0
- Major: 2
- Minor: 0 (1 fixed)
- Warnings: 0
- Suggestions: 2

## Reviewer Notes

### Verification Against Ralph Logging Spec (pt-l6yb)

| Spec Requirement | Implementation Status |
|------------------|----------------------|
| `--verbose` flag | ✅ Implemented in both `run` and `start` commands |
| `--debug` flag | ✅ Implemented (mapped to DEBUG level) |
| `--quiet` flag | ✅ Implemented |
| `RALPH_LOG_LEVEL` env var | ✅ Supported with quiet/normal/verbose/debug values |
| `RALPH_VERBOSE=1` env var | ✅ Supported |
| `RALPH_DEBUG=1` env var | ✅ Supported |
| `RALPH_QUIET=1` env var | ✅ Supported |
| Config file support (`logLevel`) | ✅ Supported in `.tf/ralph/config.json` |
| Priority: CLI > env > config | ✅ Correctly implemented in `resolve_log_level()` |
| Flags passed to workflow | ✅ Appended to workflow_flags via `log_level_to_flag()` |
| CLI output filtered by level | ⚠️ Not yet implemented (deferred to pt-rvpi logger helper) |

### Code Quality Assessment
- **Type Safety**: Uses `LogLevel` enum with proper type hints
- **Error Handling**: Graceful fallback to NORMAL for invalid env var values
- **Documentation**: Help text clearly documents all options
- **Backward Compatibility**: All flags are optional, no breaking changes
- **Test Coverage**: All 399 existing tests pass; new functionality needs tests (see Major #1)

### Acceptance Criteria Verification
- ✅ `tf ralph start` accepts verbosity flags
- ✅ `tf ralph run` accepts verbosity flags
- ✅ Flags documented in `--help`
- ✅ Env var override supported
- ✅ Verbosity passed through to logging helper (via workflow flags)
- ✅ No breaking changes
