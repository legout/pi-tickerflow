# Review (Second Opinion): pt-ussr

## Overall Assessment
The implementation for updating Ralph progress display with ready/blocked counts is complete and functional. The `QueueStateSnapshot` class properly formats output as `R:<n> B:<n> (done x/y)` for TTY displays and `R:<n> B:<n> done:x/y` for log output. All 74 existing tests pass, confirming no regressions.

## Critical (must fix)
No issues found.

## Major (should fix)
No issues found.

## Minor (nice to fix)
- `tf/ralph.py:1537` - The `start_ticket()` call passes `str(queue_state.total)` as the third positional argument, but `start_ticket()` signature shows `total_tickets` comes after `iteration`. While this works due to the actual call structure, explicitly using the keyword argument `total_tickets=str(queue_state.total)` would be clearer and more maintainable.

- `tests/test_progress_display.py` and `tests/test_logger.py` - No tests verify that `queue_state` parameter is actually passed and rendered in output. The existing tests mock `ProgressDisplay` but don't verify the `queue_state` parameter. Consider adding tests like:
  ```python
  def test_progress_display_with_queue_state():
      display = ProgressDisplay(output=output, is_tty=False)
      queue_state = QueueStateSnapshot(ready=3, blocked=2, running=1, done=1, total=7)
      display.complete_ticket("T-1", "COMPLETE", 0, queue_state=queue_state)
      assert "R:3 B:2" in output.getvalue()
  ```

## Warnings (follow-up ticket)
- `tf/ralph.py:1523-1533` - The `list_blocked_tickets()` function depends on `tk blocked` command. If this command is unavailable or returns different output formats, the queue state computation could be incorrect. Consider adding validation or fallback behavior. This is a defensive coding concern rather than an immediate bug.

## Suggestions (follow-up ticket)
- `tf/ralph/queue_state.py` - Consider adding unit tests specifically for `QueueStateSnapshot` and `get_queue_state()` to document expected behavior and prevent regressions. The class has validation logic in `__post_init__` that should be tested (e.g., invariant violation detection).

- `tf/ralph.py:1527-1546` and `tf/ralph.py:1603-1629` - The queue state computation is duplicated in both the start and complete sections. Consider extracting a helper function like `_compute_queue_state()` to reduce duplication and improve maintainability.

## Positive Notes
- The `QueueStateSnapshot` dataclass is well-designed with immutable frozen=True and proper invariant validation in `__post_init__`.
- TTY mode correctly uses `\x1b[2K\r` escape sequences for clean in-place updates without leaving artifacts.
- Non-TTY mode properly avoids control characters, producing clean log output with newlines only.
- The implementation is fully backwards compatible - `queue_state` is optional everywhere, preserving existing behavior when not provided.
- Queue state is recomputed after each ticket completion (lines 1603-1617), ensuring counts accurately reflect dependency resolution as tickets complete.
- Both `__str__()` and `to_log_format()` methods provide appropriate formatting for their contexts (TTY display vs structured logging).

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 2
- Warnings: 1
- Suggestions: 2
