# Research: pt-ihfv

## Status
Research complete. No external research needed - this is an internal refactoring task.

## Rationale
The ticket is about removing the `--session` parameter forwarding from Ralph CLI's `pi` command invocation. This is an architectural change to let Pi handle session management implicitly rather than having Ralph manually forward session paths.

## Context Reviewed

### Code Locations Found
1. **`tf_cli/ralph.py:run_ticket()` (lines ~480-620)**
   - Constructs `session_flag` from `session_path` parameter
   - Adds `--session {session_path}` to pi args when session_path is set

2. **`tf_cli/ralph.py:ralph_start()` serial mode (lines ~1550-1600)**
   - Builds `session_path` from `session_dir` and `session_per_ticket` config
   - Passes `session_path` to `run_ticket()`

3. **`tf_cli/ralph.py:ralph_start()` parallel mode (lines ~1680-1750)**
   - Creates session path per ticket: `session_dir / f"{ticket}.jsonl"`
   - Adds `--session` to subprocess.Popen args

4. **`tf_cli/ralph.py:ralph_run()` (lines ~1200-1280)**
   - Similar session path construction as ralph_start
   - Passes to `run_ticket()`

5. **Dry-run logging (lines ~1640-1650)**
   - Logs `session_note` showing what `--session` would be used

### Session Management Context
- Ralph stores session artifacts in Pi's standard session directory (`~/.pi/agent/sessions/`)
- Legacy directory `.tf/ralph/sessions` exists for backward compat
- Session isolation is primarily achieved through:
  - Git worktrees (parallel mode) - each ticket gets its own worktree
  - Knowledge directories - ticket artifacts go to `.tf/knowledge/tickets/{ticket}/`
  - The `--session` flag was forwarding session files for Pi's JSONL logging

### Test Coverage
- `tests/test_ralph_pi_invocation.py` - Regression tests that verify NO `--session` is passed
- Tests currently EXPECT to fail until this ticket is implemented

## Implementation Plan
1. Remove `session_path` parameter from `run_ticket()` function
2. Remove session_flag construction and args appending in `run_ticket()`
3. Remove `session_path` calculation and passing in `ralph_run()`
4. Remove `session_path` calculation and passing in `ralph_start()` serial mode
5. Remove `session_path` calculation and passing in `ralph_start()` parallel mode
6. Remove `session_note` from dry-run logging
7. Update dry-run log messages to not include session info
8. Keep `session_dir` resolution for potential future use (artifact organization)

## Sources
- `tf_cli/ralph.py` - main implementation file
- `tests/test_ralph_pi_invocation.py` - regression tests
- Ticket: pt-ihfv (current ticket)
