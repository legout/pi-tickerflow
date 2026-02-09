# Research: pt-4qvw

## Status
Research enabled but minimal - straightforward implementation of configuration knobs.

## Rationale
This ticket is about defining configuration surface for Ralph timeout and restart behavior. The implementation requires:

1. Adding `attemptTimeoutMs` and `maxRestarts` to DEFAULTS in `tf_cli/ralph.py`
2. Updating the `usage()` help text to document these options
3. Adding env var override support (RALPH_ATTEMPT_TIMEOUT_MS, RALPH_MAX_RESTARTS)
4. Implementing timeout and restart logic in `run_ticket()` and `ralph_run()` functions

## Context Reviewed
- `tf_cli/ralph.py` - Main Ralph implementation with DEFAULTS, usage(), run_ticket(), ralph_run()
- Existing config loading mechanism via `load_config()`
- Existing env var pattern (RALPH_LOG_LEVEL, RALPH_VERBOSE, etc.)
- Ticket acceptance criteria

## Implementation Plan
1. Add config keys to DEFAULTS with conservative defaults
2. Update usage() help text
3. Add env var resolution for new configs
4. Implement timeout using subprocess timeout parameter
5. Implement restart logic with retry counter
6. Update ralph_run() to use the new logic

## Sources
- `tf_cli/ralph.py` - Source code
- `.pi/ralph/config.json` - Example config file
