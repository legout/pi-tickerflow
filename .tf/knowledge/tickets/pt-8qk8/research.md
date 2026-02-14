# Research: pt-8qk8

## Status
Research completed. Implementation context gathered from existing codebase and design documents.

## Rationale
Research enabled by config (`workflow.enableResearcher: true`). This ticket implements core reliability features for the Ralph background dispatch system.

## Context Reviewed

### 1. Ticket Details (`tk show pt-8qk8`)
- **Task**: Implement orphaned session recovery and TTL cleanup
- **Type**: Task
- **Dependencies**: pt-699h (parallel dispatch scheduling)
- **Links**: pt-699h, pt-uu03

**Acceptance Criteria**:
- [ ] Startup scans and marks orphaned sessions from prior runs
- [ ] Orphaned sessions are killed/cleaned before new scheduling starts  
- [ ] Finished session metadata is retained for a limited TTL then pruned

### 2. Design Documents

**Plan: plan-ralph-background-interactive-shell** (`plan.md`)
- Recovery decision (Section: Decisions/Resolved Questions #3):
  > "On Ralph startup, detect orphaned sessions for this run, mark stale ones, and kill/cleanup before scheduling new tickets."
- Finished session retention (Section: Decisions/Resolved Questions #4):
  > "Keep completed session metadata/log pointers briefly for debugging (TTL), then auto-cleanup."

**Spike: spike-interactive-shell-execution** (`spike.md`)
- Identified orphaned sessions as a risk: "Ralph restart may leave orphaned background sessions"
- Recommended recovery on startup before scheduling

**Seed: seed-add-ralph-loop-background-interactive** (`backlog.md`)
- pt-8qk8 is ticket #6 in the backlog chain
- Depends on pt-699h (parallel dispatch scheduling)
- Blocks pt-uu03 (manual validation)

### 3. Existing Implementation

**File: `tf/ralph/session_recovery.py`**
The module already exists with complete implementation:

| Function | Purpose |
|----------|---------|
| `detect_orphaned_sessions()` | Finds sessions with status "running" where PID is not alive or owned by current process |
| `cleanup_orphaned_session()` | Terminates process, cleans worktree, updates status to "orphaned" |
| `cleanup_all_orphaned_sessions()` | Main entry point for orphaned session recovery |
| `prune_expired_sessions()` | Removes sessions in terminal states (completed/failed/orphaned) older than TTL |
| `run_startup_recovery()` | Combined recovery: orphaned cleanup + TTL pruning |

**State Persistence**:
- File: `.tf/ralph/dispatch-sessions.json`
- Schema: `SessionStateFile` with version, sessions list, last_updated
- TTL default: 7 days (604800000 ms)

**Integration Point**:
- Already imported in `tf/ralph.py` (line ~41):
  ```python
  from tf.ralph.session_recovery import (
      DEFAULT_SESSION_TTL_MS,
      DispatchSessionState,
      register_dispatch_session,
      remove_dispatch_session,
      run_startup_recovery,
      update_dispatch_session_status,
  )
  ```

### 4. Related Code

**Completion monitoring** (`tf/ralph_completion.py`):
- `graceful_terminate_dispatch()` - Used by cleanup to kill orphaned processes
- `poll_dispatch_status()` - Checks if PID is still running

## Key Implementation Notes

1. **Idempotency**: Recovery must be safe across repeated starts. The implementation:
   - Detects orphaned sessions by checking PID status
   - Updates session status after cleanup to prevent double-processing
   - Uses file-based state that survives process restarts

2. **Worktree cleanup**: Orphaned session cleanup removes git worktrees to prevent disk leaks

3. **TTL handling**: Sessions in terminal states are pruned based on `completed_at` timestamp

4. **Integration requirement**: `run_startup_recovery()` should be called at Ralph startup before scheduling begins

## Sources

1. `/home/volker/coding/pi-ticketflow/.tickets/pt-8qk8.md` - Ticket specification
2. `/home/volker/coding/pi-ticketflow/.tf/knowledge/topics/plan-ralph-background-interactive-shell/plan.md` - Approved plan
3. `/home/volker/coding/pi-ticketflow/.tf/knowledge/topics/spike-interactive-shell-execution/spike.md` - Technical spike
4. `/home/volker/coding/pi-ticketflow/.tf/knowledge/topics/seed-add-ralph-loop-background-interactive/backlog.md` - Backlog context
5. `/home/volker/coding/pi-ticketflow/tf/ralph/session_recovery.py` - Existing implementation
6. `/home/volker/coding/pi-ticketflow/tf/ralph.py` - Integration context

## Research Conclusion

The `session_recovery.py` module already implements all required functionality for this ticket:
- ✅ Orphaned session detection and cleanup
- ✅ TTL-based pruning  
- ✅ Startup recovery procedure
- ✅ State persistence

**Remaining work**: Verify integration point in `ralph.py` startup sequence and ensure `run_startup_recovery()` is called before scheduling loop begins.
