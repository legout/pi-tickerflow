# Review (Second Opinion): pt-ussr

## Overall Assessment
The implementation correctly displays ready/blocked counts (R:<n> B:<n>) and done/total progress in Ralph's output. The QueueStateSnapshot class provides proper formatting for both TTY progress display and log output. All 74 existing tests pass, confirming the implementation meets acceptance criteria. However, I identified minor code quality issues and missing test coverage for the queue state integration.

## Critical (must fix)
No issues found

## Major (should fix)
No major issues identified.

## Minor (nice to fix)
- `tf/ralph.py:1424-1430` - In `ralph_start()`, `str(queue_state.total)` is passed to `start_ticket()` but the parameter type is already `Union[int, str]`. The explicit `str()` conversion is unnecessary and adds slight cognitive overhead. Consider passing `queue_state.total` directly.

- `tf/ralph/queue_state.py:1` - Module-level docstring says "Follows semantics defined in pt-m54d specification" but there's no reference link or doc comment explaining where to find pt-m54d. Consider adding a comment with the ticket reference or removing the internal ticket reference from user-facing code.

- `tests/test_progress_display.py` - Missing test coverage for `queue_state` parameter in `start_ticket()` and `complete_ticket()`. The existing tests don't verify that queue state is properly formatted in the output when provided. Consider adding tests like:
  ```python
  def test_complete_ticket_with_queue_state(self):
      output = StringIO()
      display = ProgressDisplay(output=output, is_tty=False)
      from tf.ralph.queue_state import QueueStateSnapshot
      queue_state = QueueStateSnapshot(ready=3, blocked=2, running=1, done=1, total=7)
      display.complete_ticket("abc-123", "COMPLETE", 0, queue_state=queue_state)
      result = output.getvalue()
      assert "R:3 B:2" in result
      assert "done 1/7" in result
  ```

## Warnings (follow-up ticket)
- `tf/ralph.py:1430-1435` - Queue state is computed twice per ticket (once at start, once at completion). While not expensive for typical workloads (O(|pending| + |running| + |completed|)), this could be optimized by passing the same snapshot and marking it as "after completion". Consider a follow-up ticket to optimize if profiling shows this matters.

- `tf/logger.py:157-170` - The `log_ticket_start()` and `log_ticket_complete()` methods check `if queue_state is not None` twice each - once to add to extra dict, once for message formatting. Consider refactoring to a helper method to reduce duplication:
  ```python
  def _add_queue_state(extra, msg, queue_state):
      if queue_state:
          extra["queue_state"] = str(queue_state)
          return f"{msg} [{queue_state.to_log_format()}]"
      return msg
  ```

## Suggestions (follow-up ticket)
- Consider adding dedicated queue state tests in `tests/test_queue_state.py` to validate the QueueStateSnapshot dataclass, including:
  - `__post_init__` validation raises ValueError on invariant violation
  - `__str__()` and `to_log_format()` produce correct output
  - `get_queue_state()` correctly computes blocked vs ready from dep_graph
  - Edge cases: empty sets, all blocked, all ready, single ticket

- The TTY progress line format could include the done count in the "Processing" message for better visibility. Currently it only shows on completion.

## Positive Notes
- Clean separation of concerns: `QueueStateSnapshot` handles formatting, `ProgressDisplay` handles UI output, `RalphLogger` handles structured logging
- Proper use of immutable dataclass with validation (`frozen=True`, `__post_init__`)
- TTY/non-TTY modes are correctly distinguished with appropriate control character usage
- Queue state is recomputed after each ticket completion ensuring counts stay accurate as dependencies resolve
- All 74 existing tests pass without modification, demonstrating backwards compatibility
- Logger redaction helper prevents sensitive data leaks in log output
- The implementation correctly follows the codebase pattern of using `Optional["QueueStateSnapshot"]` type hints with forward references

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 3
- Warnings: 2
- Suggestions: 2
