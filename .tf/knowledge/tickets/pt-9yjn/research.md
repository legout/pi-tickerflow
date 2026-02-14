# Research: pt-9yjn

## Status
Research completed

## Rationale
Research is needed to understand:
1. The current Ralph `run_ticket()` implementation
2. How `interactive_shell` dispatch mode works
3. The existing worktree lifecycle implementation (completed in pt-0v53)
4. The contract between this ticket and pt-7jzy (completion handling)

## Context Reviewed

### Ticket Details (pt-9yjn)
**Task**: Implement a dispatch-based ticket runner that launches `pi /tf <ticket> --auto` in background sessions.

**Acceptance Criteria**:
- [ ] New runner launches one interactive_shell dispatch session per ticket
- [ ] Session ID and ticket ID are captured together for tracking
- [ ] Runner returns structured result for success/failure handling

**Blocking**: pt-7jzy (Handle dispatch completion and graceful session termination)
**Blocked by**: pt-0v53 (Add per-ticket worktree lifecycle for dispatch runs) - **CLOSED**

### Current Implementation (tf/ralph.py)

The existing `run_ticket()` function (lines 462-629) currently:
- Uses subprocess (`pi -p`) for both dispatch and subprocess backends
- Has a TODO comment at line 486: `# TODO(pt-9yjn): Implement actual dispatch execution via interactive_shell tool`
- Worktree lifecycle functions are already implemented:
  - `create_worktree_for_ticket()` (lines 1056-1100)
  - `merge_and_close_worktree()` (lines 1103-1172)
  - `cleanup_worktree()` (lines 1175-1215)

The `ralph_run()` function (lines 1736-1830) already:
- Creates worktrees when `execution_backend == "dispatch"`
- Calls `run_ticket()` with the worktree as `cwd`
- Handles merge on success, cleanup on failure

### interactive_shell Dispatch Mode

From the interactive-shell skill:

```typescript
// Dispatch (Fire-and-Forget) - NON-BLOCKING, NO POLLING
interactive_shell({
  command: 'pi "Fix all TypeScript errors in src/"',
  mode: "dispatch",
  reason: "Fixing TS errors"
})
// Returns: { sessionId: "calm-reef", mode: "dispatch" }
// → Do other work. When session completes, receive notification via triggerTurn.
```

Key characteristics:
- **Non-blocking**: Returns immediately with sessionId
- **Notification-based**: Agent is notified on completion via `triggerTurn`
- **Background capable**: Can use `background: true` for headless execution
- **Auto-exit**: Defaults `autoExitOnQuiet: true` for single-task delegation

### Contract with pt-7jzy

Ticket pt-7jzy handles:
- Completion detection from dispatch/session state
- Idle session handling with graceful EOF (`Ctrl+D`) before forced kill
- Timeout and forced termination reporting

This means pt-9yjn should:
1. **Launch** the dispatch session
2. **Capture** session ID with ticket ID
3. **Return** a structured result that pt-7jzy can use for tracking

The actual completion detection, timeout handling, and session cleanup will be implemented in pt-7jzy.

### Plan Reference

From `plan-ralph-background-interactive-shell/plan.md`:

**Phase 1: Foundation (MVP)** includes:
1. Create new function `run_ticket_dispatch()` in `tf/ralph.py`
2. Use `interactive_shell` dispatch mode with `pi /tf <ticket> --auto`
3. Each dispatch gets its own Pi session (fresh context guaranteed)
4. Handle completion notification from dispatch

## Implementation Notes

### Function Signature
The new `run_ticket_dispatch()` function should:
- Accept similar parameters to `run_ticket()` but return a structured result
- Return object should include: `session_id`, `ticket_id`, `status` (pending/launched)
- Not block waiting for completion (that's pt-7jzy's job)

### Integration Point
In `ralph_run()`, instead of calling `run_ticket()` directly when backend is dispatch:
```python
if execution_backend == "dispatch":
    result = run_ticket_dispatch(...)
    # Store session_id for tracking (pt-7jzy will use this)
else:
    rc = run_ticket(...)
```

### Worktree Context
The worktree is already created before ticket execution in `ralph_run()`:
- `worktree_cwd` is passed to `run_ticket()` as the `cwd` parameter
- Same pattern should apply to `run_ticket_dispatch()`

## Sources

1. `tk show pt-9yjn` - Ticket specification
2. `tk show pt-0v53` - Closed worktree lifecycle ticket (with notes)
3. `tk show pt-7jzy` - Blocking completion handling ticket
4. `tf/ralph.py` - Current implementation with TODO marker
5. `.pi/agent/skills/interactive-shell/SKILL.md` - Dispatch mode documentation
6. `.tf/knowledge/topics/plan-ralph-background-interactive-shell/plan.md` - Implementation plan
7. `.tf/knowledge/topics/spike-interactive-shell-execution/spike.md` - Research on completion detection
8. `.tf/knowledge/topics/seed-add-ralph-loop-background-interactive/seed.md` - Original vision
