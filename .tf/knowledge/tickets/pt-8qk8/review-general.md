# Review: pt-8qk8

## Overall Assessment
The current implementation is **not functionally complete** for the stated ticket goals. The startup hook exists, but the session state it depends on is never populated from the dispatch lifecycle, and the process liveness check cannot reliably handle orphaned processes from previous Ralph runs. As written, this can produce false cleanup success while leaving real orphaned processes alive.

## Critical (must fix)
- `tf/ralph.py:840-975`, `tf/ralph.py:2623-2640`, `tf/ralph/session_recovery.py:153` - Session recovery is wired at startup, but there is no call to `register_dispatch_session()` / `update_dispatch_session_status()` / `remove_dispatch_session()` in the dispatch launch/completion paths. Recovery reads `.tf/ralph/dispatch-sessions.json`, but the runtime writes only `.tf/ralph/dispatch/<ticket>.json` tracking files. Impact: orphan recovery + TTL pruning are effectively no-op for real sessions because the recovery state file is never maintained.
- `tf/ralph_completion.py:59-94`, `tf/ralph/session_recovery.py:357-369`, `tf/ralph/session_recovery.py:416-429` - Orphan detection/termination relies on `poll_dispatch_status()` which uses `os.waitpid(...)`. For processes from a previous Ralph instance (not children of current process), `waitpid` raises `ChildProcessError` and is treated as "not running". Impact: genuinely running orphan processes may not be terminated, while metadata is still marked orphaned and worktree cleanup proceeds, risking live-process/worktree conflicts.

## Major (should fix)
- `tf/ralph.py:2631-2641` - Startup recovery runs even in dry-run mode (`options["dry_run"]` only gates lock/state, not recovery). Impact: `tf ralph start --dry-run` can still kill processes, remove worktrees, and mutate metadata, which violates dry-run expectations.
- `tf/ralph.py:2635` - TTL parsing uses raw `int(config.get(...))` instead of the existing safe resolver (`resolve_session_ttl_ms`). Impact: invalid config values (e.g. non-numeric string) can raise `ValueError` and abort startup.
- `tf/ralph/session_recovery.py:438-454` - `session.worktree_path` from persisted JSON is removed without validating it is under the configured worktree root/repo boundary. Impact: if the state file is corrupted/tampered, cleanup may delete arbitrary paths.

## Minor (nice to fix)
- `tf/ralph/session_recovery.py:331-344` - `current_pid` parameter is documented but never used. Impact: API/behavior mismatch and future confusion.
- `tf/ralph/session_recovery.py:459-469` - `cleanup_orphaned_session()` ignores the return value from `update_dispatch_session_status(...)` and always returns `True`. Impact: cleanup counts/logging can report success despite persistence failure.
- `tf/ralph.py:31-37`, `tf/ralph.py:1203-1217` - Several recovery symbols are imported/defined but currently unused in control flow (`DispatchSessionState`, `register_dispatch_session`, `remove_dispatch_session`, `update_dispatch_session_status`, `resolve_session_ttl_ms`). Impact: dead code signals incomplete integration and reduces maintainability.

## Warnings (follow-up ticket)
- `tests/` (project-wide search) - No dedicated tests were found for `tf/ralph/session_recovery.py` integration paths (registration, startup orphan cleanup, TTL pruning). Impact: regressions in lifecycle wiring and edge-case process handling are likely to slip through.
- `tf/ralph/session_recovery.py:214-220`, `tf/ralph/session_recovery.py:242-259`, `tf/ralph/session_recovery.py:281-298` - Session-state updates are load-modify-save without file locking or atomic replace. Impact: if multiple writers are introduced (or crash during write), state loss/corruption risk increases.

## Suggestions (follow-up ticket)
- `tf/ralph.py:952-975`, `tf/ralph.py:3050-3110`, `tf/ralph/session_recovery.py:227-298` - Wire full lifecycle persistence: register on launch, update on completion/failure/timeout, and remove/archive consistently.
- `tf/ralph_completion.py:59-97`, `tf/ralph/session_recovery.py:357-429` - Split liveness checks by context: use child-aware `waitpid` only for owned processes and `os.kill(pid, 0)`/`/proc` command validation for foreign/orphaned processes.
- `tf/ralph/session_recovery.py:438-454` - Enforce path safety before deletion (must be inside configured worktrees dir; reject symlink escapes) and log hard failures explicitly.

## Positive Notes
- `tf/ralph.py:2632-2640` places recovery at startup before scheduling, which is the correct control-point.
- `tf/ralph/session_recovery.py` has a cleanly separated module design (`detect`, `cleanup`, `prune`, `run_startup_recovery`) that is easy to test once lifecycle wiring is completed.

## Summary Statistics
- Critical: 2
- Major: 3
- Minor: 3
- Warnings: 2
- Suggestions: 3
