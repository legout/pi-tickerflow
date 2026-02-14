# Implementation: pt-8qk8

## Summary
Implemented the session lifecycle tracking for dispatch sessions to enable orphaned session recovery and TTL-based cleanup. The key fix was wiring the session registration and status update calls into the dispatch launch and completion paths.

## Retry Context
- Attempt: 1
- Escalated Models: fixer=base, reviewer-second=base, worker=base

## Files Changed

### `tf/ralph.py`
- **Added `ralph_dir` parameter** to `run_ticket_dispatch()` function signature (line 820)
- **Session registration on launch** (lines 968-979): After successful dispatch launch, register the session in `dispatch-sessions.json` with status "running"
- **Updated parallel dispatch calls** to pass `ralph_dir` parameter (lines 2382 and 3051)
- **Session status updates on completion** in parallel mode:
  - Missing PID case (line 3075): Update to "failed"
  - Timeout case (line 3093): Update to "failed"
  - Dispatch failed case (line 3107): Update to "failed" with return code
  - Worktree merge failed case (line 3123): Update to "failed"
  - Success case (line 3128): Update to "completed"

### `tf/ralph/session_recovery.py`
- **Fixed syntax error** in worktree cleanup validation (line 448): Changed incorrect `elif` to `else` + nested `if` for proper try/except/else structure

## Key Decisions

1. **Added ralph_dir parameter**: Rather than importing ralph_dir globally or using a global state, passing it as a parameter keeps the function signature explicit and testable.

2. **Parallel mode focus**: The session status updates were added primarily to the parallel dispatch completion paths since that's where multiple dispatches are tracked simultaneously. Serial mode dispatch returns immediately after launch with status "DISPATCHED".

3. **Path validation fix**: Fixed a pre-existing syntax error in the worktree cleanup validation that would have caused runtime failures.

## Tests Run
- `python -m py_compile tf/ralph.py` - Syntax check passed
- `python -m py_compile tf/ralph/session_recovery.py` - Syntax check passed
- `python -c "from tf.ralph import run_ticket_dispatch"` - Import verification passed
- `python -m pytest tests/test_ralph_session*.py` - 20/21 passed (1 pre-existing failure)

## Verification
The implementation can be verified by:
1. Running `tf ralph start` and observing session registration in `.tf/ralph/dispatch-sessions.json`
2. Starting Ralph with a previously orphaned session (status="running" but PID not alive)
3. Observing cleanup logs showing orphaned session detection and removal
4. After 7 days (default TTL), verify expired sessions are pruned from the state file
