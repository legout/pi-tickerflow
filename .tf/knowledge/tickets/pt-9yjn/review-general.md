# Review: pt-9yjn

## Overall Assessment
The new `run_ticket_dispatch()` structure is a good step toward explicit dispatch lifecycle handling, and the `DispatchResult` contract is clear and easy to consume. However, the current launcher has a critical process I/O bug and a few major integration/behavior gaps that can cause hangs and inconsistent backend behavior. These should be addressed before relying on dispatch mode in production.

## Critical (must fix)
- `tf/ralph.py:799-824` - `stdout` defaults to `subprocess.PIPE` for dispatched processes, but the parent never reads that pipe. Once output exceeds pipe buffer capacity, the child process can block indefinitely, causing dispatched tickets to hang and never complete.

## Major (should fix)
- `tf/ralph.py:804-809` - File handles opened for `pi_output == "file"` and `pi_output == "discard"` are never closed in the parent process (both success and exception paths), creating descriptor leaks during long runs.
- `tf/ralph.py:2565-2606` (with `tf/ralph.py:584-588`) - `ralph_start` still routes dispatch backend through `run_ticket()` (which does not actually dispatch), so backend behavior is inconsistent between run paths and session tracking is skipped in this flow.
- `tf/ralph.py:708-713`, `tf/ralph.py:779`, `tf/ralph.py:795` - `capture_json` is accepted but not implemented in dispatch execution (`--mode json` is never applied), creating silent behavior drift from non-dispatch execution.

## Minor (nice to fix)
- `tf/ralph.py:715-719` and `tf/ralph.py:793-795` - Docstring/comments say this uses `interactive_shell` dispatch mode, but implementation launches `pi` via `subprocess.Popen`; this mismatch increases maintenance risk.
- `tf/ralph.py:765` - Session IDs are truncated to 8 chars from UUID; collision risk is low but non-zero for high-volume/long-lived tracking.

## Warnings (follow-up ticket)
- `tf/ralph.py:713`, `tf/ralph.py:813-833` - `timeout_ms` is currently unused in dispatch path, so launched processes have no timeout enforcement here.
- `tf/ralph.py:2155-2225` - Dispatch mode creates per-ticket worktrees and returns immediately after launch; merge/cleanup is deferred. If follow-up completion tracking fails, stale worktrees/processes may accumulate.

## Suggestions (follow-up ticket)
- `tests/test_json_capture.py:122`, `tests/test_pi_output.py:137` - Add dedicated tests for `run_ticket_dispatch()`; current coverage focuses on `run_ticket()` and does not exercise dispatch runner semantics.
- `tf/ralph.py:700-843` - Add behavioral tests for dispatch output routing (`inherit/file/discard`), pipe safety under high output, and file descriptor closure on both success/failure paths.

## Positive Notes
- `tf/ralph.py:690-697` introduces a clean structured result (`DispatchResult`) that is straightforward for callers to consume.
- `tf/ralph.py:741-756` includes solid early validation (ticket, `pi` availability, prompt presence) before launch.
- `tf/ralph.py:817-824` correctly uses `start_new_session=True`, which is a good foundation for future lifecycle/termination control.

## Summary Statistics
- Critical: 1
- Major: 3
- Minor: 2
- Warnings: 2
- Suggestions: 2
