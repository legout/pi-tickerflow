# Review: pt-9yjn

## Overall Assessment
The `run_ticket_dispatch()` implementation provides a functional dispatch launcher for Ralph tickets. However, there are several edge cases around resource management, worktree lifecycle, and process handling that present latent risks. The current implementation correctly defers completion tracking to pt-7jzy but may have introduced gaps in the worktree cleanup contract.

## Critical (must fix)
- `tf/ralph.py:815-817` - File handle leak: when `pi_output == "file"`, the opened file handle for stdout is never explicitly closed. If many tickets are dispatched in a loop, this could exhaust file descriptors. The file object should be wrapped in a context manager or explicitly closed after process launch.
- `tf/ralph.py:818-820` - Missing devnull close: when `pi_output == "discard"`, the devnull file handle is also leaked. While less critical than regular files, this still accumulates open FDs.
- `tf/ralph.py:2188-2206` - Worktree cleanup bypass: In dispatch mode on failure, the worktree is cleaned up (good). However, on success, the worktree is NOT merged or cleaned up - it's left dangling. The comment says "Completion detection is handled by pt-7jzy" but there's no mechanism for pt-7jzy to later merge the worktree. This may leave git worktrees in limbo and lose work.

## Major (should fix)
- `tf/ralph.py:749` - Short UUID collision risk: Using only 8 characters of UUID (32 bits of entropy) for session IDs. With Ralph's parallel processing, collision probability becomes non-trivial. Recommend full UUID or at least 12-16 characters.
- `tf/ralph.py:807` - `start_new_session=True` creates a new process group, but there's no corresponding cleanup mechanism shown. If Pi crashes or is killed, the child processes may persist as orphans. Document this behavior or ensure pt-7jzy handles orphan reaping.
- `tf/ralph.py:823-831` - No validation that `proc.pid` is actually running. The process could fail immediately after Popen returns (e.g., pi binary crashes on startup). Consider a brief `time.sleep(0.1)` + `proc.poll()` check to catch immediate failures.

## Minor (nice to fix)
- `tf/ralph.py:793-797` - The `--auto` flag injection modifies the command string by simple substring check. If flags contains `"--auto"` as part of another flag (unlikely but possible), this would fail. Use split-based parsing for robustness.
- `tf/ralph.py:704-842` - Missing type hint on return: function declares `-> DispatchResult` but doesn't import `DispatchResult` at the top level (it's defined after). While Python handles forward references, explicit import or moving the dataclass earlier would be cleaner.
- `tf/ralph.py:741` - The `build_cmd()` helper is used but not shown in the review context. Ensure it properly escapes the ticket ID to prevent shell injection if ticket IDs ever contain special characters.

## Warnings (follow-up ticket)
- `tf/ralph.py:815` - File handle ownership transfer to subprocess is platform-dependent. On Windows, the file handle may not be properly inherited. If Ralph is intended to support Windows, this needs testing.
- `tf/ralph.py:2199` - State tracking gap: When dispatch succeeds, state is set to "DISPATCHED" but there's no transition to "COMPLETE". This creates a new terminal state that downstream tools may not recognize. Ensure the state machine documentation is updated.

## Suggestions (follow-up ticket)
- Consider adding a `cleanup_callback` mechanism so pt-7jzy can merge worktrees after completion without duplicating worktree management logic.
- Add a `dispatch_info.json` file in the worktree directory containing session_id, pid, and start time for external monitoring tools.
- The timeout_ms parameter is accepted but not used in dispatch mode. Consider logging a warning that timeouts are deferred to pt-7jzy to avoid confusion.

## Positive Notes
- Clean separation of concerns between launch (pt-9yjn) and completion tracking (pt-7jzy) is architecturally sound
- `DispatchResult` dataclass provides a clear contract for success/failure handling
- Dry-run mode is properly implemented with informative output
- Good error handling for missing pi binary and invalid tickets

## Summary Statistics
- Critical: 3
- Major: 3
- Minor: 3
- Warnings: 2
- Suggestions: 3
