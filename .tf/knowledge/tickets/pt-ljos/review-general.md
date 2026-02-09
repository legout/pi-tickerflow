# Review: pt-ljos

## Overall Assessment
The implementation adds well-structured lifecycle logging methods to the Ralph logger with good security considerations for command sanitization. The code follows existing patterns and integrates cleanly with the serial loop. However, there are critical security and runtime issues that must be fixed before deployment.

## Critical (must fix)

- `tf_cli/logger.py:425-435` - **Security: Unsanitized command in structured log fields**. The `log_command_executed()` method sets `extra["command"] = command` (raw command) at line 425, but only sanitizes the command for the human-readable message at line 435. The structured log output (key=value pairs from `extra`) will still contain the unsanitized command with potential secrets. The `extra` dict should contain the sanitized version: `extra["command"] = sanitized` instead.

- `tf_cli/ralph_new.py:821` - **TypeError: Unexpected keyword argument**. The call to `logger.log_error_summary(ticket, error_msg, artifact_path=artifact_path, iteration=iteration)` passes `iteration=iteration` but `log_error_summary()` signature (lines 344-350 in logger.py) does not accept an `iteration` parameter. This will raise `TypeError: log_error_summary() got an unexpected keyword argument 'iteration'` at runtime.

- `tf_cli/ralph_new.py:950` - **Same TypeError issue**. The parallel mode section also passes `iteration=iteration` to `log_error_summary()` which doesn't accept it.

## Major (should fix)

- `tf_cli/logger.py:440-450` - **Incomplete command sanitization patterns**. The regex patterns only handle space-separated values (`--api-key \S+`) but don't handle equals-sign formats like `--api-key=value` or `--api-key="value with spaces"`. Add patterns like `r'(--api-key[=:]\S+)'` to cover these common formats.

- `tf_cli/logger.py:450` - **JWT pattern incomplete**. The JWT regex `r'(eyJ[\w-]*\.eyJ[\w-]*)'` only captures header.payload but JWTs have 3 parts (header.payload.signature). The pattern should be `r'(eyJ[\w-]*\.eyJ[\w-]*\.[\w-]*)'` to capture all three parts.

## Minor (nice to fix)

- `tf_cli/logger.py:407-410` - **Inconsistent log level for loop completion**. `log_loop_complete()` uses `LogLevel.WARN` for non-backlog_empty reasons, but `max_iterations_reached` is an expected/normal termination condition (configured by user). Consider using INFO for both cases or distinguishing between "expected" completion reasons vs "unexpected" ones.

- `tf_cli/logger.py:425` - **Code clarity**. The `extra` dictionary is built with the raw command but then the sanitized version is used only for the message. Consider building `extra` with the sanitized command directly to make the intent clear and avoid future security regressions.

- `tf_cli/ralph_new.py:795` - **Missing iteration in ticket_logger context**. When `ticket_logger` is created with `logger.with_context(ticket=ticket, iteration=iteration)`, the iteration is added to context, but then `log_ticket_start()` also explicitly passes `iteration=iteration`. This is redundant - the context already contains it.

## Warnings (follow-up ticket)

- `tf_cli/logger.py:440-450` - **Command sanitization maintenance burden**. The hardcoded list of secret patterns will need ongoing maintenance as new secret types are encountered. Consider a follow-up ticket to make patterns configurable or load from a config file.

- `tf_cli/ralph_new.py` - **Parallel mode uses different artifact path format**. In parallel mode, `artifact_path` uses `worktree_path / ".tf/knowledge" / "tickets" / ticket` while serial mode uses the resolved `knowledge_dir`. While this is technically correct for worktree isolation, consider documenting this behavior for operators debugging parallel runs.

## Suggestions (follow-up ticket)

- `tf_cli/logger.py` - **Add duration tracking to `log_command_executed()`**. Include elapsed time for command execution to help identify slow tickets.

- `tf_cli/logger.py` - **Add `log_backlog_status()` method** for consistent logging of backlog checks (currently only logged implicitly via `log_no_ticket_selected`).

- `tf_cli/ralph_new.py` - **Add loop heartbeat logging** every N iterations to help detect stuck loops in long-running processes.

## Positive Notes

- Clean structured logging format with key=value pairs that are easily parseable
- Good security awareness with `_sanitize_command()` helper and redaction of common secret patterns
- Consistent use of event types (`loop_start`, `loop_complete`, `no_ticket`, `command_executed`) for log aggregation
- Proper log level selection based on exit code in `log_command_executed()` (INFO for success, ERROR for failure)
- Artifact path included in error summaries provides actionable debugging information
- Both serial and parallel modes updated consistently for feature parity

## Summary Statistics

- Critical: 3
- Major: 2
- Minor: 3
- Warnings: 2
- Suggestions: 3
