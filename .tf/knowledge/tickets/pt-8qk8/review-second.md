# Second Opinion Review: pt-8qk8

**Ticket:** Implement orphaned session recovery and TTL cleanup  
**Review Type:** Verification (implementation already exists)  
**Review Date:** 2026-02-14  
**Reviewers:** Second-opinion agent

---

## Executive Summary

This is a **verification review** for an implementation that was discovered to already exist in the codebase. The session recovery functionality (`tf/ralph/session_recovery.py`) is well-architected and integrated correctly into Ralph's startup sequence. However, several non-obvious issues were identified through second-opinion analysis, ranging from race conditions to error handling gaps.

The implementation is **functionally correct for normal operation** but has edge cases that could lead to resource leaks, stale data, or difficult-to-debug issues in production.

---

## Critical Issues

*No critical issues found that would cause immediate system failure or data loss.*

---

## Major Issues

### 1. Race Condition in Session State File Access

**Location:** `tf/ralph/session_recovery.py:102-128` (`load_session_state`), `tf/ralph/session_recovery.py:131-155` (`save_session_state`)

**Issue:** The session state file (`dispatch-sessions.json`) is read and written without file locking. In parallel mode, multiple Ralph instances could:
- Corrupt the JSON file with interleaved writes
- Lose session state updates when two processes read-modify-write simultaneously
- Create duplicate entries for the same session

**Evidence:**
```python
# Line 102-128 - No locking on read
def load_session_state(ralph_dir: Path, logger: Optional[RalphLogger] = None) -> SessionStateFile:
    state_path = get_session_state_path(ralph_dir)
    if not state_path.exists():
        return SessionStateFile()
    data = json.loads(state_path.read_text(encoding="utf-8"))  # No lock!
    ...

# Line 131-155 - No locking on write  
def save_session_state(ralph_dir: Path, state: SessionStateFile, ...) -> bool:
    state_path = get_session_state_path(ralph_dir)
    state_path.write_text(json.dumps(state.to_dict(), indent=2))  # No lock!
```

**Impact:** In parallel mode with multiple workers, session state corruption could lead to:
- Undetected orphaned sessions (lost cleanup)
- Phantom sessions (duplicate entries)
- Unparseable JSON crashing Ralph on startup

**Recommendation:** Implement file locking using `fcntl` (Unix) or `portalocker` (cross-platform) around all read-modify-write operations.

---

### 2. PID Reuse Vulnerability in Orphan Detection

**Location:** `tf/ralph/session_recovery.py:257-299` (`detect_orphaned_sessions`)

**Issue:** The orphan detection relies solely on PID existence via `poll_dispatch_status()`. If a PID is reused by a different process between Ralph restarts, the detection logic will incorrectly identify the session as "still running" and skip cleanup.

**Evidence:**
```python
# Line 272-279
if session.pid:
    is_running, _ = poll_dispatch_status(session.pid)
    if is_running:
        # Process is still running but we don't own it
        # (it was started by a previous Ralph instance)
        logger.info(f"Found orphaned running session: {session.session_id}")
        orphaned.append(session)  # Could be a completely different process!
```

**Impact:** Orphaned sessions with reused PIDs will:
- Never be cleaned up
- Leave worktrees dangling
- Accumulate over time

**Recommendation:** Store additional process metadata (start time, process name, command line hash) in the session state and validate it before declaring a session orphaned.

---

## Minor Issues

### 3. Missing Atomic Write for Session State

**Location:** `tf/ralph/session_recovery.py:131-155` (`save_session_state`)

**Issue:** The session state file is written directly, not atomically. A crash during write could leave a partially-written JSON file.

**Evidence:**
```python
# Line 147-148
state_path.write_text(
    json.dumps(state.to_dict(), indent=2),
    encoding="utf-8"
)
```

**Note:** `test_session_store.py` shows atomic write patterns using temp files that could be adapted.

**Recommendation:** Write to a temp file and rename atomically.

---

### 4. Worktree Cleanup Failure Handling Gap

**Location:** `tf/ralph/session_recovery.py:334-350` (`cleanup_orphaned_session`)

**Issue:** If both `git worktree remove` and `shutil.rmtree` fail, the error is logged but the session is still marked as "orphaned" (line 356), potentially leaving stale worktree paths in the session state.

**Evidence:**
```python
# Line 345-350
if remove_result.returncode != 0:
    import shutil
    try:
        shutil.rmtree(worktree_path, ignore_errors=True)
    except Exception as e:
        log.warning(f"Failed to remove worktree directory: {e}")
# Execution continues - status updated to "orphaned" regardless
```

**Recommendation:** Track worktree cleanup success and include in the return value; consider not updating status if worktree cleanup fails (or use a different status like "cleanup_failed").

---

### 5. Inconsistent TTL Configuration Location

**Location:** `tf/ralph/session_recovery.py:26` vs `tf/ralph.py:236`

**Issue:** The default TTL is defined in `session_recovery.py` (as `DEFAULT_SESSION_TTL_MS`) but the config key `sessionTtlMs` is only used in `ralph.py`. The session_recovery module uses the default but never checks config for overrides when called independently.

**Evidence:**
```python
# tf/ralph/session_recovery.py:26
DEFAULT_SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000  # Local definition

# tf/ralph.py:2635-2636 - Config only used here
ttl_ms = int(config.get("sessionTtlMs", DEFAULT_SESSION_TTL_MS))
orphaned_cleaned, expired_pruned = run_startup_recovery(..., ttl_ms=ttl_ms)
```

**Impact:** If `prune_expired_sessions()` is called directly (not through `run_startup_recovery()`), it won't respect config overrides.

**Recommendation:** Move config resolution into `prune_expired_sessions()` or document that direct callers must handle config.

---

## Warnings

### 6. No Tests for Session Recovery Module

**Location:** Entire `tf/ralph/session_recovery.py` module

**Issue:** There are no unit tests for the session recovery module. `tests/test_session_store.py` tests a different module (`tf/session_store.py`).

**Impact:** Changes to session recovery logic have no automated regression protection.

**Evidence:**
```bash
$ find tests -name "*.py" | xargs grep -l "session_recovery" || echo "No test files found"
No test files found
```

**Recommendation:** Create `tests/test_session_recovery.py` with tests for:
- Orphan detection with mocked PIDs
- TTL pruning with time manipulation
- Concurrent access scenarios
- State file corruption recovery

---

### 7. Unbounded Session State Growth

**Location:** `tf/ralph/session_recovery.py:395-432` (`prune_expired_sessions`)

**Issue:** Sessions in "running" status are never pruned. If Ralph crashes repeatedly without proper cleanup, the session state file could grow unbounded with zombie "running" entries.

**Evidence:**
```python
# Line 413-415
# Keep non-terminal sessions
if session.status not in terminal_states:
    retained_sessions.append(session)
    continue
```

The `terminal_states` set is `{"completed", "failed", "orphaned"}` - "running" is never pruned.

**Recommendation:** Consider a "stale running" threshold (e.g., sessions marked "running" for >30 days) to prevent unbounded growth.

---

### 8. Timezone Handling Ambiguity

**Location:** `tf/ralph/session_recovery.py:96-114` (`_parse_timestamp`)

**Issue:** The timestamp parsing handles "Z" suffix but relies on `fromisoformat()` which has different behaviors across Python versions for timezone-aware strings.

**Evidence:**
```python
# Line 108-112
if ts.endswith("Z"):
    ts = ts[:-1] + "+00:00"
dt = datetime.fromisoformat(ts)
return dt.timestamp()
```

**Warning:** In Python < 3.11, `fromisoformat()` doesn't support all ISO 8601 formats. This could cause issues with timestamps from external sources.

**Recommendation:** Use `datetime.strptime()` with explicit format or require Python 3.11+.

---

## Suggestions

### 9. Add Session Recovery Metrics

**Location:** `tf/ralph/session_recovery.py:447-471` (`run_startup_recovery`)

**Suggestion:** The current logging only captures counts. Add metrics for:
- Time taken for recovery operations
- Age distribution of pruned sessions
- Worktree cleanup success/failure rates

**Benefit:** Operational visibility for tuning TTL values and identifying cleanup issues.

---

### 10. Configurable Orphan Detection Window

**Location:** `tf/ralph/session_recovery.py:257-299` (`detect_orphaned_sessions`)

**Suggestion:** Currently all "running" sessions are candidates for orphan detection. Add a "grace period" config option (e.g., `orphanGracePeriodMs`) to ignore recently-started sessions, preventing false positives during fast Ralph restarts.

---

### 11. Session State Backup Before Cleanup

**Location:** `tf/ralph/session_recovery.py:447-471` (`run_startup_recovery`)

**Suggestion:** Before modifying the session state file during recovery, create a timestamped backup. This allows manual recovery if a bug causes incorrect session deletion.

**Implementation:**
```python
# Before cleanup
backup_path = state_path.with_suffix(f".json.backup.{int(time.time())}")
shutil.copy2(state_path, backup_path)
# Limit to last N backups
```

---

### 12. Document Session State Schema

**Suggestion:** The session state schema version (`SESSION_STATE_VERSION = 1`) is defined but there's no documentation of:
- The full schema structure
- Migration path for version bumps
- Backward compatibility guarantees

**Recommendation:** Create `docs/session-state-schema.md` documenting the JSON structure and versioning policy.

---

## Code Quality Observations

### Positive
- Clean separation of concerns between detection, cleanup, and pruning
- Good use of type hints and dataclasses
- Comprehensive docstrings
- Proper use of logger context for debugging

### Areas for Improvement
- `cleanup_orphaned_session()` is 50+ lines and handles multiple concerns (process termination, worktree cleanup, state update)
- Magic numbers scattered (5000ms kill wait, 2.0s SIGKILL wait) - could be constants
- `shutil` and `subprocess` imports inside functions (lines 344, 347) - better at module level

---

## Verification Checklist

| Criterion | Status | Notes |
|-----------|--------|-------|
| Startup scans for orphaned sessions | ✅ | `run_startup_recovery()` called at ralph.py:2636 |
| Orphaned sessions cleaned before scheduling | ✅ | Called before `iteration = 0`, before while loop |
| Finished sessions retained for TTL | ✅ | `prune_expired_sessions()` uses `completed_at` timestamp |
| Configurable TTL | ✅ | `sessionTtlMs` config with 7-day default |
| State file versioning | ✅ | `SESSION_STATE_VERSION = 1` defined |
| Unit test coverage | ❌ | No tests for session_recovery module |
| Race condition handling | ⚠️ | No file locking on state file |
| PID reuse protection | ❌ | No additional metadata for validation |

---

## Conclusion

The implementation is **architecturally sound** and **functionally complete** for normal operation. The identified issues are primarily edge cases and operational concerns:

1. **Race conditions** in parallel mode need addressing before high-concurrency deployments
2. **PID reuse** is a low-probability but persistent risk
3. **Test coverage** should be added before any refactoring

**Overall Assessment:** The implementation meets acceptance criteria but should be hardened for production reliability, particularly around concurrent access scenarios.

---

## Files Reviewed

1. `tf/ralph/session_recovery.py` (complete)
2. `tf/ralph.py` (lines 2630-2650, integration point)
3. `tf/ralph/__init__.py` (module exports)
4. `tf/ralph_completion.py` (termination functions)
5. `tests/test_session_store.py` (related test patterns)
6. `.tf/knowledge/tickets/pt-8qk8/implementation.md` (verification context)
