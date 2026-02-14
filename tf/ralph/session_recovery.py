"""Session recovery and TTL cleanup for Ralph dispatch sessions.

This module provides:
1. Orphaned session detection and cleanup on Ralph startup
2. TTL-based pruning of finished session metadata

The session state is persisted to .tf/ralph/dispatch-sessions.json for recovery
across Ralph restarts.
"""

from __future__ import annotations

import fcntl
import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from tf.logger import LogLevel, RalphLogger, create_logger


# Default TTL for finished session metadata (7 days in milliseconds)
DEFAULT_SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000

# Session state file version for future compatibility
SESSION_STATE_VERSION = 1


@dataclass
class DispatchSessionState:
    """State for a single dispatch session.

    Attributes:
        session_id: Unique session identifier
        ticket_id: Ticket being processed
        pid: Process ID of the dispatch process
        started_at: ISO timestamp when session started
        worktree_path: Path to the worktree for this session
        status: Current status (running, completed, orphaned, failed)
        completed_at: ISO timestamp when session completed (if applicable)
        return_code: Exit code if completed
    """
    session_id: str
    ticket_id: str
    pid: Optional[int]
    started_at: str
    worktree_path: Optional[str] = None
    status: str = "running"
    completed_at: Optional[str] = None
    return_code: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "ticket_id": self.ticket_id,
            "pid": self.pid,
            "started_at": self.started_at,
            "worktree_path": self.worktree_path,
            "status": self.status,
            "completed_at": self.completed_at,
            "return_code": self.return_code,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DispatchSessionState":
        """Create from dictionary (JSON deserialization)."""
        return cls(
            session_id=data.get("session_id", ""),
            ticket_id=data.get("ticket_id", ""),
            pid=data.get("pid"),
            started_at=data.get("started_at", ""),
            worktree_path=data.get("worktree_path"),
            status=data.get("status", "running"),
            completed_at=data.get("completed_at"),
            return_code=data.get("return_code"),
        )


@dataclass
class SessionStateFile:
    """Container for the session state file.

    Attributes:
        version: Schema version for compatibility
        sessions: List of session states
        last_updated: ISO timestamp of last update
    """
    version: int = SESSION_STATE_VERSION
    sessions: List[DispatchSessionState] = field(default_factory=list)
    last_updated: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "sessions": [s.to_dict() for s in self.sessions],
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionStateFile":
        """Create from dictionary (JSON deserialization)."""
        sessions = [
            DispatchSessionState.from_dict(s)
            for s in data.get("sessions", [])
        ]
        return cls(
            version=data.get("version", SESSION_STATE_VERSION),
            sessions=sessions,
            last_updated=data.get("last_updated", ""),
        )


def _utc_now() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_timestamp(ts: str) -> Optional[float]:
    """Parse ISO timestamp to Unix epoch seconds.

    Args:
        ts: ISO timestamp string

    Returns:
        Unix epoch seconds, or None if parsing fails
    """
    if not ts:
        return None
    try:
        # Handle both formats: with and without timezone
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        dt = datetime.fromisoformat(ts)
        return dt.timestamp()
    except (ValueError, TypeError):
        return None


def get_session_state_path(ralph_dir: Path) -> Path:
    """Get the path to the session state file.

    Args:
        ralph_dir: Ralph directory path (.tf/ralph)

    Returns:
        Path to dispatch-sessions.json
    """
    return ralph_dir / "dispatch-sessions.json"


def load_session_state(ralph_dir: Path, logger: Optional[RalphLogger] = None) -> SessionStateFile:
    """Load session state from file.

    Creates an empty state file if it doesn't exist.

    Args:
        ralph_dir: Ralph directory path
        logger: Optional logger

    Returns:
        SessionStateFile with loaded or empty state
    """
    state_path = get_session_state_path(ralph_dir)

    if not state_path.exists():
        return SessionStateFile()

    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        state = SessionStateFile.from_dict(data)

        # Validate version
        if state.version > SESSION_STATE_VERSION:
            if logger:
                logger.warning(
                    f"Session state file version {state.version} is newer than "
                    f"supported version {SESSION_STATE_VERSION}. Some data may be lost."
                )

        return state
    except json.JSONDecodeError as e:
        if logger:
            logger.warning(f"Failed to parse session state file: {e}. Starting fresh.")
        return SessionStateFile()
    except Exception as e:
        if logger:
            logger.warning(f"Failed to load session state file: {e}. Starting fresh.")
        return SessionStateFile()


def _with_lock(file_obj, exclusive: bool = True) -> None:
    """Acquire a file lock on the given file object.

    Uses fcntl for Unix systems. This is a blocking lock.

    Args:
        file_obj: Open file object
        exclusive: If True, acquire exclusive (write) lock; else shared (read) lock
    """
    lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
    fcntl.flock(file_obj.fileno(), lock_type)


def _release_lock(file_obj) -> None:
    """Release file lock on the given file object.

    Args:
        file_obj: Open file object with a lock
    """
    fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)


def save_session_state(
    ralph_dir: Path,
    state: SessionStateFile,
    logger: Optional[RalphLogger] = None,
) -> bool:
    """Save session state to file with atomic write and file locking.

    Uses write-to-temp-then-rename for atomicity and fcntl for file locking
    to prevent concurrent writer corruption.

    Args:
        ralph_dir: Ralph directory path
        state: Session state to save
        logger: Optional logger

    Returns:
        True if save succeeded
    """
    state_path = get_session_state_path(ralph_dir)

    try:
        state.last_updated = _utc_now()
        state_path.parent.mkdir(parents=True, exist_ok=True)

        # Use a lock file to prevent concurrent writes
        lock_path = state_path.with_suffix(".lock")

        # Write to temp file, then rename atomically
        temp_path = state_path.with_suffix(".tmp")

        with open(lock_path, "w") as lock_file:
            _with_lock(lock_file, exclusive=True)
            try:
                # Write to temp file
                temp_path.write_text(
                    json.dumps(state.to_dict(), indent=2),
                    encoding="utf-8"
                )
                # Atomic rename
                temp_path.rename(state_path)
            finally:
                _release_lock(lock_file)

        # Clean up temp file if it still exists (e.g., after failed rename)
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass

        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed to save session state file: {e}")
        return False


def register_dispatch_session(
    ralph_dir: Path,
    session: DispatchSessionState,
    logger: Optional[RalphLogger] = None,
) -> bool:
    """Register a new dispatch session in the state file.

    Args:
        ralph_dir: Ralph directory path
        session: Session state to register
        logger: Optional logger

    Returns:
        True if registration succeeded
    """
    state = load_session_state(ralph_dir, logger)

    # Check for duplicate session_id
    existing_ids = {s.session_id for s in state.sessions}
    if session.session_id in existing_ids:
        if logger:
            logger.warning(
                f"Session {session.session_id} already exists in state file, updating"
            )
        # Update existing session
        state.sessions = [
            session if s.session_id == session.session_id else s
            for s in state.sessions
        ]
    else:
        state.sessions.append(session)

    return save_session_state(ralph_dir, state, logger)


def update_dispatch_session_status(
    ralph_dir: Path,
    session_id: str,
    status: str,
    return_code: Optional[int] = None,
    logger: Optional[RalphLogger] = None,
) -> bool:
    """Update the status of a dispatch session.

    Args:
        ralph_dir: Ralph directory path
        session_id: Session ID to update
        status: New status (completed, failed, orphaned)
        return_code: Optional exit code
        logger: Optional logger

    Returns:
        True if update succeeded
    """
    state = load_session_state(ralph_dir, logger)

    found = False
    for session in state.sessions:
        if session.session_id == session_id:
            session.status = status
            session.completed_at = _utc_now()
            if return_code is not None:
                session.return_code = return_code
            found = True
            break

    if not found:
        if logger:
            logger.warning(f"Session {session_id} not found in state file for update")
        return False

    return save_session_state(ralph_dir, state, logger)


def remove_dispatch_session(
    ralph_dir: Path,
    session_id: str,
    logger: Optional[RalphLogger] = None,
) -> bool:
    """Remove a dispatch session from the state file.

    Args:
        ralph_dir: Ralph directory path
        session_id: Session ID to remove
        logger: Optional logger

    Returns:
        True if removal succeeded
    """
    state = load_session_state(ralph_dir, logger)

    original_count = len(state.sessions)
    state.sessions = [s for s in state.sessions if s.session_id != session_id]

    if len(state.sessions) == original_count:
        if logger:
            logger.debug(f"Session {session_id} not found in state file for removal")
        return True  # Not found is still a success

    return save_session_state(ralph_dir, state, logger)


def _is_process_alive(pid: int) -> bool:
    """Check if a process is alive using os.kill(pid, 0).

    This works for ANY process, not just our children (unlike waitpid).
    It's safe for checking orphaned sessions from previous Ralph runs.

    Args:
        pid: Process ID to check

    Returns:
        True if process exists and is running, False otherwise
    """
    try:
        os.kill(pid, 0)  # Signal 0 = check existence without sending signal
        return True
    except ProcessLookupError:
        # Process does not exist
        return False
    except PermissionError:
        # Process exists but we don't have permission to signal it
        # This means it's alive (and owned by another user)
        return True
    except OSError:
        # Any other OS error (e.g., invalid PID)
        return False


def detect_orphaned_sessions(
    ralph_dir: Path,
    logger: Optional[RalphLogger] = None,
) -> List[DispatchSessionState]:
    """Detect orphaned sessions from previous Ralph runs.

    An orphaned session is one that:
    - Has status "running"
    - Was started by a different process (not current Ralph instance)
    - The process is either not running or not our child

    Note: We use os.kill(pid, 0) instead of waitpid() because orphaned
    sessions were started by a previous Ralph instance and are NOT our
    child processes. waitpid() would raise ChildProcessError for non-children.

    Args:
        ralph_dir: Ralph directory path
        logger: Optional logger

    Returns:
        List of orphaned session states
    """
    state = load_session_state(ralph_dir, logger)
    orphaned: List[DispatchSessionState] = []

    for session in state.sessions:
        # Only consider sessions marked as running
        if session.status != "running":
            continue

        # Check if the process is still alive
        if session.pid:
            # Use os.kill(pid, 0) instead of poll_dispatch_status() because
            # orphaned sessions are NOT our children - waitpid won't work
            is_running = _is_process_alive(session.pid)

            if is_running:
                # Process is still running but we don't own it
                # (it was started by a previous Ralph instance)
                if logger:
                    logger.info(
                        f"Found orphaned running session: {session.session_id} "
                        f"(ticket: {session.ticket_id}, pid: {session.pid})"
                    )
                orphaned.append(session)
            else:
                # Process is dead but session is still marked as running
                # This is also orphaned (stale state)
                if logger:
                    logger.info(
                        f"Found stale session (process dead): {session.session_id} "
                        f"(ticket: {session.ticket_id})"
                    )
                orphaned.append(session)
        else:
            # No PID - session is incomplete/orphaned
            if logger:
                logger.info(
                    f"Found session without PID: {session.session_id} "
                    f"(ticket: {session.ticket_id})"
                )
            orphaned.append(session)

    return orphaned


def cleanup_orphaned_session(
    ralph_dir: Path,
    session: DispatchSessionState,
    repo_root: Path,
    logger: Optional[RalphLogger] = None,
) -> bool:
    """Clean up a single orphaned session.

    This includes:
    1. Terminating the process if still running
    2. Cleaning up the worktree if it exists
    3. Updating session status to "orphaned" in state file

    Args:
        ralph_dir: Ralph directory path
        session: Session to clean up
        repo_root: Repository root path (for worktree cleanup)
        logger: Optional logger

    Returns:
        True if cleanup fully succeeded (process terminated, worktree cleaned, status updated)
    """
    import shutil
    import signal
    import subprocess

    log = logger or create_logger(level=LogLevel.NORMAL)
    worktree_cleaned = True  # Track worktree cleanup success

    # Step 1: Terminate process if still running
    # Use _is_process_alive() because orphaned processes are NOT our children
    if session.pid:
        if _is_process_alive(session.pid):
            log.info(
                f"Terminating orphaned session process: pid={session.pid}, "
                f"session={session.session_id}"
            )
            try:
                # Try graceful termination first (SIGTERM)
                os.kill(session.pid, signal.SIGTERM)
                # Wait for graceful shutdown
                time.sleep(0.5)

                # Check if still running
                if _is_process_alive(session.pid):
                    # Force kill
                    os.kill(session.pid, signal.SIGKILL)
                    log.info(f"Orphaned session process force-killed: pid={session.pid}")
                else:
                    log.info(f"Orphaned session process terminated gracefully: pid={session.pid}")
            except ProcessLookupError:
                log.info(f"Orphaned session process already exited: pid={session.pid}")
            except PermissionError:
                log.warning(
                    f"Permission denied terminating orphaned session process: pid={session.pid}"
                )
            except OSError as e:
                log.warning(f"Failed to terminate orphaned session process: {e}")

    # Step 2: Clean up worktree if it exists
    # Security: Validate worktree_path is under repo_root before deletion
    if session.worktree_path:
        worktree_path = Path(session.worktree_path).resolve()
        safe_repo_root = repo_root.resolve()

        # Validate path is under repo_root (prevent path traversal attacks)
        try:
            worktree_path.relative_to(safe_repo_root)
        except ValueError:
            log.warning(
                f"Worktree path {worktree_path} is outside repo root {safe_repo_root}, "
                f"skipping cleanup for safety"
            )
            worktree_cleaned = False
        else:
            # Path validation passed, proceed with cleanup
            if worktree_path.exists():
                log.info(
                    f"Cleaning up orphaned session worktree: {worktree_path}"
                )
                # Try git worktree remove first
                remove_result = subprocess.run(
                    ["git", "-C", str(repo_root), "worktree", "remove", "-f", str(worktree_path)],
                    capture_output=True,
                )
                if remove_result.returncode != 0:
                    # Fallback to direct removal
                    try:
                        shutil.rmtree(worktree_path, ignore_errors=True)
                    except Exception as e:
                        log.warning(f"Failed to remove worktree directory: {e}")
                        worktree_cleaned = False

                # Verify cleanup succeeded
                if worktree_path.exists():
                    log.warning(f"Worktree path still exists after cleanup: {worktree_path}")
                    worktree_cleaned = False

    # Step 3: Update session status
    status_updated = update_dispatch_session_status(
        ralph_dir=ralph_dir,
        session_id=session.session_id,
        status="orphaned",
        logger=log,
    )

    if status_updated and worktree_cleaned:
        log.info(
            f"Orphaned session cleaned up: {session.session_id} (ticket: {session.ticket_id})"
        )
        return True
    elif not status_updated:
        log.warning(
            f"Orphaned session cleanup partially failed (status update failed): "
            f"{session.session_id} (ticket: {session.ticket_id})"
        )
        return False
    else:
        log.warning(
            f"Orphaned session cleanup partially failed (worktree cleanup failed): "
            f"{session.session_id} (ticket: {session.ticket_id})"
        )
        return False


def cleanup_all_orphaned_sessions(
    ralph_dir: Path,
    repo_root: Path,
    logger: Optional[RalphLogger] = None,
) -> int:
    """Detect and clean up all orphaned sessions.

    This is the main entry point for orphaned session recovery.
    Should be called at Ralph startup before starting new scheduling.

    Args:
        ralph_dir: Ralph directory path
        repo_root: Repository root path
        logger: Optional logger

    Returns:
        Number of orphaned sessions cleaned up
    """
    log = logger or create_logger(level=LogLevel.NORMAL)

    orphaned = detect_orphaned_sessions(ralph_dir, logger=log)

    if not orphaned:
        log.debug("No orphaned sessions detected")
        return 0

    log.info(f"Detected {len(orphaned)} orphaned session(s), cleaning up...")

    cleaned = 0
    for session in orphaned:
        try:
            if cleanup_orphaned_session(ralph_dir, session, repo_root, log):
                cleaned += 1
        except Exception as e:
            log.error(
                f"Failed to clean up orphaned session {session.session_id}: {e}"
            )

    log.info(f"Cleaned up {cleaned}/{len(orphaned)} orphaned session(s)")
    return cleaned


def prune_expired_sessions(
    ralph_dir: Path,
    ttl_ms: int = DEFAULT_SESSION_TTL_MS,
    logger: Optional[RalphLogger] = None,
) -> int:
    """Prune finished session metadata older than TTL.

    This removes sessions with status in (completed, failed, orphaned)
    that were completed more than ttl_ms ago.

    Args:
        ralph_dir: Ralph directory path
        ttl_ms: Retention TTL in milliseconds (0 = no pruning)
        logger: Optional logger

    Returns:
        Number of sessions pruned
    """
    if ttl_ms <= 0:
        return 0

    log = logger or create_logger(level=LogLevel.NORMAL)

    state = load_session_state(ralph_dir, log)
    now = time.time()
    ttl_sec = ttl_ms / 1000.0

    # Terminal states that can be pruned
    terminal_states = {"completed", "failed", "orphaned"}

    original_count = len(state.sessions)
    pruned_sessions: List[DispatchSessionState] = []
    retained_sessions: List[DispatchSessionState] = []

    for session in state.sessions:
        # Keep non-terminal sessions
        if session.status not in terminal_states:
            retained_sessions.append(session)
            continue

        # Check if session is within TTL
        if session.completed_at:
            completed_ts = _parse_timestamp(session.completed_at)
            if completed_ts:
                age_sec = now - completed_ts
                if age_sec > ttl_sec:
                    pruned_sessions.append(session)
                    continue

        # Keep session if within TTL or no timestamp
        retained_sessions.append(session)

    if not pruned_sessions:
        return 0

    # Update state with only retained sessions
    state.sessions = retained_sessions
    save_session_state(ralph_dir, state, log)

    log.info(
        f"Pruned {len(pruned_sessions)} expired session(s) "
        f"(older than {ttl_ms}ms)"
    )

    return len(pruned_sessions)


def run_startup_recovery(
    ralph_dir: Path,
    repo_root: Path,
    ttl_ms: int = DEFAULT_SESSION_TTL_MS,
    logger: Optional[RalphLogger] = None,
) -> tuple[int, int]:
    """Run full startup recovery: orphaned session cleanup + TTL pruning.

    This should be called at Ralph startup before starting new scheduling.

    Args:
        ralph_dir: Ralph directory path
        repo_root: Repository root path
        ttl_ms: Retention TTL in milliseconds (0 = no TTL pruning)
        logger: Optional logger

    Returns:
        Tuple of (orphaned_cleaned, expired_pruned)
    """
    log = logger or create_logger(level=LogLevel.NORMAL)

    log.info("Running session recovery...")

    # Step 1: Clean up orphaned sessions
    orphaned_cleaned = cleanup_all_orphaned_sessions(ralph_dir, repo_root, log)

    # Step 2: Prune expired sessions
    expired_pruned = prune_expired_sessions(ralph_dir, ttl_ms, log)

    if orphaned_cleaned > 0 or expired_pruned > 0:
        log.info(
            f"Session recovery complete: "
            f"{orphaned_cleaned} orphaned cleaned, {expired_pruned} expired pruned"
        )
    else:
        log.debug("Session recovery complete: no cleanup needed")

    return orphaned_cleaned, expired_pruned
