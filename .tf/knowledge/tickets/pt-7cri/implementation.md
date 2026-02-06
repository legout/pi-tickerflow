# Implementation: pt-7cri

## Summary
Added verbosity control mechanism to Ralph CLI (`tf ralph start` and `tf ralph run`) with CLI flags and environment variable support.

## Files Changed
- `tf_cli/ralph_new.py` - Added LogLevel enum, argument parsing for --verbose/--debug/--quiet flags, env var support, and integration with workflow flags

## Key Decisions

### LogLevel Enum
Created a `LogLevel` enum with four levels (QUIET, NORMAL, VERBOSE, DEBUG) that maps to the specification in the logging spec (pt-l6yb). This provides type safety and clear semantics.

### Priority Order
Following best practices, the resolution priority is:
1. CLI flags (highest priority - explicit user intent)
2. Environment variables (RALPH_LOG_LEVEL, RALPH_VERBOSE, RALPH_DEBUG, RALPH_QUIET)
3. Config file (`logLevel` setting in `.tf/ralph/config.json`)
4. Default (NORMAL)

### Flag Passing Strategy
The log level is passed through to the workflow by appending the appropriate flag (`--verbose`, `--debug`, or `--quiet`) to the workflow flags. This ensures the verbosity setting propagates through to the actual ticket processing.

### Environment Variable Design
Multiple env vars are supported for convenience:
- `RALPH_LOG_LEVEL` - Direct level setting (quiet/normal/verbose/debug)
- `RALPH_VERBOSE=1` - Shortcut for verbose mode
- `RALPH_DEBUG=1` - Shortcut for debug mode  
- `RALPH_QUIET=1` - Shortcut for quiet mode

## Tests Run
- All 399 existing tests pass
- Manual verification of `--help` output confirms new flags are documented

## Verification
```bash
# Test help shows new flags
python -m tf_cli.ralph_new --help

# Expected output includes:
#   --verbose         Enable verbose output (INFO + DEBUG events)
#   --debug           Alias for --verbose (maximum detail)
#   --quiet           Minimal output (errors only)
```

## Acceptance Criteria Status
- [x] `tf ralph start` accepts verbosity flags (--verbose, --debug, --quiet)
- [x] `tf ralph run` accepts verbosity flags (--verbose, --debug, --quiet)
- [x] Flags documented in --help
- [x] Env var override supported (RALPH_LOG_LEVEL, RALPH_VERBOSE, RALPH_DEBUG, RALPH_QUIET)
- [x] Verbosity passed through to workflow flags
- [x] Config file support (logLevel setting)
- [x] No breaking changes (flags are optional)
