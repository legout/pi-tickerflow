# Review: pt-xu9u

## Overall Assessment
The retry-aware escalation implementation is functionally complete with all Critical and Major issues addressed. The documentation covers the happy path well, but there are edge cases around state corruption recovery, timestamp fidelity, and silent configuration drift that could lead to unexpected behavior in production. These issues are subtle and only surface under failure conditions or long-running deployments.

## Critical (must fix)
No issues found

## Major (should fix)
- `skills/tf-workflow/SKILL.md:137-149` - **Timestamp precision bug in attempt ordering**: The `start_attempt` procedure uses string timestamps for `startedAt`/`completedAt` (ISO 8601 format). When attempts are created rapidly (within the same second), lexical sorting of these timestamps may not match chronological order if timezones or millisecond precision vary. This could cause `attemptNumber` resolution to pick the wrong "latest" attempt when resuming. Impact: Wrong escalation level applied, potentially skipping escalation on retry or escalating prematurely.

- `skills/tf-workflow/SKILL.md:149` + `retry-state.json` - **Silent state truncation on write failures**: The atomic write procedure uses `os.replace()` which is atomic on POSIX but not guaranteed on all filesystems (e.g., some network filesystems). If the workflow crashes between writing the temp file and the rename, or if the filesystem buffers the write, subsequent runs may see partially written or stale state. Impact: Retry count resets unexpectedly, causing infinite retry loops or premature max-retries enforcement.

- `skills/tf-workflow/SKILL.md:137-149` - **In-progress detection ambiguity**: The procedure says to check if "last attempt was in_progress" but doesn't define how to detect this state. The retry-state schema has no explicit `status: in_progress` - only `blocked` or `closed` are defined. The current logic would need to infer "in_progress" from `completedAt` being null/undefined, but this isn't documented as a valid schema state. Impact: Unclear behavior when resuming interrupted attempts; may create duplicate attempts or fail to resume correctly.

## Minor (nice to fix)
- `skills/tf-workflow/SKILL.md:78-82` - **Agent name mapping inconsistency**: The docs use `reviewerSecondOpinion` in escalation config but `reviewer-second-opinion` in agents map. While the note explains the mapping, this creates a trap where users might copy the escalation key name into the agents map and wonder why resolution fails. Consider adding validation that warns when escalation model keys don't resolve.

- `skills/tf-workflow/SKILL.md:105-112` - **Detection regex fragility**: The `detect_blocked_from_review` fallback uses regex pattern `r'\n-\s'` to check for bullet items, but review sections may use numbered lists (`1. `) or other formats. This could cause false negatives when reviews use alternative list styles.

- `settings.json:89-96` - **Default escalation models are all null**: While documented as "use base model", having all escalation models default to null means enabling escalation (setting `enabled: true`) without also configuring specific models results in no actual escalation occurring. Users may think they've enabled escalation when they haven't. Consider logging a warning when escalation is enabled but all model overrides are null.

## Warnings (follow-up ticket)
- `skills/tf-workflow/SKILL.md:412-420` - **No escalation for reviewer-general or reviewer-spec-audit**: The escalation curve only covers fixer, reviewer-second-opinion, and worker. If review quality from the primary reviewers is the bottleneck, there's no mechanism to escalate them. Document this limitation or consider adding these roles to the escalation matrix.

- `skills/tf-workflow/SKILL.md:301-310` - **Model switching failures not escalated**: If `switch_model` fails during an escalated attempt, the workflow continues with the current model (per Error Handling section). This effectively loses the escalation benefit without recording that the escalation model was unavailable. Consider tracking switch failures in retry-state for debugging.

- `skills/tf-workflow/SKILL.md:501-510` - **Ralph integration doesn't check in-progress status**: The Ralph skip conditions check `status: blocked` and `retryCount >= maxRetries`, but don't check for `in_progress` attempts. If Ralph picks up a ticket that has an in-progress attempt from a crashed worker, it may create parallel attempts on the same ticket.

## Suggestions (follow-up ticket)
- Add a `attemptId` UUID to each attempt entry for easier correlation across logs and artifacts
- Consider adding a `reason` field when status is SKIPPED (max retries exceeded vs manually skipped)
- Document expected behavior when retry-state.json exists but is for a different ticket ID (corruption/manual move)
- Add metrics/logging for escalation effectiveness (how often does escalation help resolve blocked tickets?)

## Positive Notes
- The opt-in default (`enabled: false`) is the right choice for backward compatibility
- The agent name mapping note prevents a common configuration error
- Detection algorithm has sensible fallback from close-summary to review.md
- Atomic write pattern for retry-state.json shows good defensive coding
- The separation of `attemptNumber` (1-indexed for humans) from `retryCount` (0-indexed for logic) is clear and consistent

## Summary Statistics
- Critical: 0
- Major: 3
- Minor: 3
- Warnings: 3
- Suggestions: 4
