# Fixes: pt-9yjn

## Summary
Fixed critical and major issues in the `run_ticket_dispatch()` function including pipe buffer deadlock, file descriptor leaks, worktree lifecycle tracking, and improved command validation.

## Fixes by Severity

### Critical (must fix)
- [x] `tf/ralph.py:811-834` - **Pipe buffer deadlock**: Changed `stdout=PIPE` to `subprocess.DEVNULL` for "inherit" mode to avoid blocking on full pipe buffer. The parent process never consumes the pipe output, which can cause deadlock for high-output tasks.
- [x] `tf/ralph.py:807-812` - **FD leaks**: Added explicit file handle closure after subprocess launch. File handles opened for `pi_output="file"` and `pi_output="discard"` modes are now closed in the parent process after successful process spawn.
- [x] `tf/ralph.py:2188-2220` - **Worktree lifecycle**: Added dispatch tracking file (`dispatch/{ticket}.json`) that registers worktree path, session ID, PID, and repo root for deferred cleanup by pt-7jzy. This ensures worktrees aren't stranded after dispatch launch.
- [x] `tf/ralph.py:740-742` - **Docstring clarity**: Updated docstring to clarify the architectural decision to use subprocess.Popen instead of direct interactive_shell tool invocation. Python code cannot directly invoke Pi tools, so subprocess launch achieves equivalent isolation.

### Major (should fix)
- [x] `tf/ralph.py:708-713,779,795` - **capture_json not applied**: Added `--mode json` flag to command when `capture_json=True`. Previously the parameter was accepted but never used in the actual command.
- [x] `tf/ralph.py:749-765` - **Session ID collision risk**: Changed from truncated 8-character UUID to full UUID for session IDs to reduce collision risk in high-throughput scenarios.
- [x] `tf/ralph.py:823-831` - **Post-launch health check**: Added immediate `poll()` after process launch to catch startup failures. Process that dies immediately now returns a failed status instead of appearing successful.

### Minor (nice to fix)
- [x] `tf/ralph.py:715-719,793-795` - **Documentation alignment**: Updated docstring to accurately describe subprocess-based implementation rather than interactive_shell tool.
- [x] `tf/ralph.py:492-498` - **Command validation**: Added regex validation in `build_cmd()` to ensure ticket IDs only contain safe characters (alphanumeric, hyphens, underscores) to prevent command injection.

### Warnings (follow-up)
- [ ] `tf/ralph.py:713,813-833` - `timeout_ms` unused in dispatch launch path (deferred to pt-7jzy)
- [ ] `tf/ralph.py:2199` - `DISPATCHED` lifecycle state needs explicit state machine handling (deferred to pt-7jzy)
- [ ] `tf/ralph.py:815` - Cross-platform handle inheritance (Windows) unverified (deferred)

### Suggestions (follow-up)
- [ ] `tests/test_json_capture.py`, `tests/test_pi_output.py` - Add dedicated tests for `run_ticket_dispatch()`
- [ ] `tf/ralph.py` - Add explicit dispatch tracking artifact mechanism

## Summary Statistics
- **Critical**: 4
- **Major**: 3
- **Minor**: 2
- **Warnings**: 0 (deferred)
- **Suggestions**: 0 (deferred)

## Verification
- Syntax check: `python3 -m py_compile tf/ralph.py` - PASSED
- Unit tests: `python3 -m pytest tests/test_ralph_logging.py tests/test_ralph_state.py` - PASSED
- Functional tests:
  - `build_cmd()` validates ticket IDs
  - `DispatchResult` has required fields
  - `run_ticket_dispatch` has `capture_json` parameter
