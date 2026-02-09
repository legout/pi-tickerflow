# Review: pt-ljos

## Critical (must fix)

- `tf_cli/logger.py:416` - **Security: Unsanitized command in structured log fields**. The `extra["command"] = command` is set with raw command before sanitization, exposing secrets in structured logs. Fix: Use sanitized command in extra dict.

- `tf_cli/ralph_new.py:821, 950` - **TypeError: Unexpected keyword argument**. `log_error_summary()` called with `iteration=iteration` but method doesn't accept this parameter.

## Major (should fix)

- `tf_cli/logger.py:440-450` - **Incomplete command sanitization patterns**. Patterns only handle space-separated values (`--api-key value`) but not equals-sign formats (`--api-key=value`). Add patterns like `r'(--api-key[=:]\S+)'`.

- `tf_cli/logger.py:450` - **Incomplete JWT pattern**. Pattern `(eyJ[\w-]*\.eyJ[\w-]*)` only captures header.payload; JWTs have 3 parts. Use `(eyJ[\w-]*\.eyJ[\w-]*\.[\w-]*)`.

- `tf_cli/logger.py:407-410` - **Inconsistent log level for loop completion**. `max_iterations_reached` is expected/normal termination but logged at WARN level. Consider using INFO for expected completions.

## Minor (nice to fix)

- `tf_cli/ralph_new.py:795` - **Redundant iteration logging**. `ticket_logger` context already has `iteration`, but `log_ticket_start()` also passes it explicitly.

- `tf_cli/logger.py:354-357` - **Missing iteration in no_ticket logging**. `log_no_ticket_selected()` doesn't accept iteration parameter for consistency.

## Warnings (follow-up ticket)

- `tf_cli/logger.py:440-450` - **Command sanitization maintenance burden**. Hardcoded patterns need ongoing maintenance. Consider making configurable.

- `tf_cli/ralph_new.py:785-791` - **Parallel mode error handling**. When worktree add fails, error is logged but loop continues, potentially leaving system in inconsistent state.

## Suggestions (follow-up ticket)

- Add duration tracking to `log_command_executed()` for performance monitoring
- Add `log_backlog_status()` method for consistent backlog check logging
- Add loop heartbeat logging every N iterations for long-running processes
- Add transaction/correlation ID for distributed log tracing

## Summary Statistics

- Critical: 2
- Major: 3
- Minor: 2
- Warnings: 2
- Suggestions: 4

## Spec Coverage

- ✅ Loop start logged with mode and max_iterations
- ✅ Selected ticket logged
- ✅ Running command logged (sanitized in message, but Critical issue in structured fields)
- ✅ Exit code logged via log_command_executed()
- ✅ Loop completion reason logged (backlog_empty, max_iterations_reached)
- ✅ No ticket selected with sleep duration logged
- ✅ Error summary with artifact path to .tf/knowledge/tickets/<id>/
