# Review: pt-8qk8

## Critical (must fix)
- `tf/ralph_completion.py:59-94`, `tf/ralph/session_recovery.py:357-369`, `tf/ralph/session_recovery.py:416-429` - Orphan liveness/termination relies on `waitpid` behavior that may misclassify foreign (previous-run) processes as not running, allowing unsafe cleanup while a process may still be active. _(source: reviewer-general)_
- `tf/ralph.py:840-975`, `tf/ralph.py:2623-2640`, `tf/ralph/session_recovery.py:153` - Reviewers reported possible incomplete wiring between dispatch lifecycle events and `dispatch-sessions.json`; if true, startup orphan recovery and TTL pruning can be ineffective. _(source: reviewer-general)_

## Major (should fix)
- `tf/ralph/session_recovery.py:102-155`, `tf/ralph/session_recovery.py:214-220`, `tf/ralph/session_recovery.py:242-259`, `tf/ralph/session_recovery.py:281-298` - Session state updates are load-modify-save without file locking; concurrent writers can lose updates or corrupt JSON. _(source: reviewer-general, reviewer-second-opinion)_
- `tf/ralph.py:2631-2641` - Startup recovery appears to execute in dry-run mode, potentially mutating state / removing worktrees when dry-run should be side-effect free. _(source: reviewer-general)_
- `tf/ralph.py:2635` - TTL parsing uses raw `int(...)` rather than safe resolution; invalid config can crash startup. _(source: reviewer-general)_
- `tf/ralph/session_recovery.py:257-299` - PID-only liveness checks risk PID-reuse false positives/negatives across restarts. _(source: reviewer-second-opinion)_
- `tf/ralph/session_recovery.py:438-454` - Worktree deletion path from persisted state is insufficiently constrained to expected roots; path-validation hardening is needed. _(source: reviewer-general)_

## Minor (nice to fix)
- `tf/ralph/session_recovery.py:131-155` - Session state writes are not atomic (temp file + replace), increasing risk of partial/corrupt writes on interruption. _(source: reviewer-second-opinion)_
- `tf/ralph/session_recovery.py:334-356` - Cleanup may still mark session as orphaned even when worktree cleanup fails, obscuring remediation state. _(source: reviewer-second-opinion)_
- `tf/ralph/session_recovery.py:459-469` - `cleanup_orphaned_session()` does not propagate persistence-update failure in its return value. _(source: reviewer-general)_
- `tf/ralph/session_recovery.py:331-344` - `current_pid` argument is currently unused. _(source: reviewer-general)_
- `tf/ralph/session_recovery.py:26`, `tf/ralph.py:236` - TTL default/resolution is split across modules, which can produce inconsistent behavior for direct callers. _(source: reviewer-second-opinion)_

## Warnings (follow-up ticket)
- `tests/` - No dedicated automated tests for `session_recovery` integration paths (orphan detection, cleanup outcomes, TTL pruning). _(source: reviewer-general, reviewer-second-opinion)_
- `tf/ralph/session_recovery.py:395-432` - Non-terminal `running` entries are never pruned, which may allow unbounded state growth after repeated crashes. _(source: reviewer-second-opinion)_
- `tf/ralph/session_recovery.py:96-114` - Timestamp parsing strategy may be fragile across Python/runtime format variations. _(source: reviewer-second-opinion)_

## Suggestions (follow-up ticket)
- `tf/ralph/session_recovery.py` - Introduce a locked + atomic session-state store abstraction for all read/modify/write operations.
- `tf/ralph/session_recovery.py:257-299` - Persist process identity metadata (e.g., pid + start-time/cmd hash) to harden orphan detection against PID reuse.
- `tf/ralph/session_recovery.py:334-454` - Add strict path-boundary/symlink checks and explicit `cleanup_failed` status when cleanup is incomplete.
- `tf/ralph/session_recovery.py`, `docs/` - Add recovery metrics and a documented session-state schema/versioning policy.

## Summary Statistics
- Critical: 2
- Major: 5
- Minor: 5
- Warnings: 3
- Suggestions: 4
