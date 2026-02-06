# Review (Spec Audit): pt-ljos

## Overall Assessment
The implementation covers most lifecycle logging requirements for the serial Ralph loop including loop start/end, ticket selection, command execution results, and error summaries with artifact pointers. However, there are security and spec compliance issues regarding command sanitization that need addressing.

## Critical (must fix)
- `tf_cli/logger.py:416` - The `command` field in the `extra` dict passed to `_log()` contains the raw unsanitized command. While the human-readable message uses `sanitized`, the structured context (key=value pairs) still contains the raw command with potential secrets. This violates the spec requirement "running command (sanitized)" for structured logs and creates a security risk. The `extra` dict should use `sanitized` instead of `command`, or the redaction logic should be enhanced to sanitize command values.

## Major (should fix)
- `tf_cli/logger.py:429-445` - The `_sanitize_command()` regex patterns use `\S+` which only matches non-whitespace characters. This fails to redact values that contain spaces (e.g., `--api-key "key with spaces"`). Pattern should use more robust matching like `[^\s\-'"]+` or handle quoted values.
- `tf_cli/ralph_new.py:905-906` - The error summary logs `artifact_path` but this path may not exist if the ticket hasn't been processed through the full workflow yet. Consider verifying path existence or logging a more helpful pointer message.

## Minor (nice to fix)
- `tf_cli/ralph_new.py:871` - The iteration count is logged at the start of the loop body but the ticket is selected afterwards. If ticket selection fails and loops back, the same iteration number appears in multiple "no_ticket" log lines, which could be confusing for debugging.
- `tf_cli/logger.py:394` - `log_command_executed()` logs after command execution, but the spec mentions "running command" which implies logging at start. Consider adding a `log_command_start()` method for verbose/debug mode to log before execution.

## Warnings (follow-up ticket)
- `tf_cli/ralph_new.py:835-836` - The `ticket_logger` includes `iteration` in context, but `log_ticket_start()` also accepts `iteration` as a parameter, causing duplicate iteration fields in logs (one from context, one from explicit param). Not a functional issue but adds noise to structured logs.

## Suggestions (follow-up ticket)
- Consider adding a `log_decision()` call when a ticket is selected to log *why* it was chosen (deps satisfied, ready state, etc.) per the seed spec's "Decision logging" feature request.
- The seed spec mentions "phase transitions (re-anchor → research → implement → review → fix → close)" but these are not logged. Consider extending `log_phase_transition()` usage in the workflow integration.

## Positive Notes
- `log_loop_start()` correctly includes mode, max_iterations, and parallel_workers context
- `log_no_ticket_selected()` satisfies the requirement to log sleep duration and reason when no ticket is available
- `log_error_summary()` includes artifact_path pointing to `.tf/knowledge/tickets/<id>/` as required
- Exit codes are properly logged via `log_command_executed()` with appropriate log levels (INFO for success, ERROR for failure)
- Loop completion reasons are logged for both `backlog_empty` and `max_iterations_reached` scenarios
- The implementation distinguishes serial vs parallel mode consistently in all log methods

## Summary Statistics
- Critical: 1
- Major: 2
- Minor: 2
- Warnings: 1
- Suggestions: 2

## Spec Coverage
- Spec/plan sources consulted: 
  - Ticket acceptance criteria (pt-ljos)
  - Seed spec: `.tf/knowledge/topics/seed-add-more-logging-to-ralph-loop/seed.md`
  - Implementation: `.tf/knowledge/tickets/pt-ljos/implementation.md`
- Missing specs: None (blocking ticket pt-rvpi implementation.md was not found but the logger helper is present in code)
