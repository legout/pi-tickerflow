# Review: pt-xu9u (Attempt 3)

## Critical (must fix)
- `tf/retry_state.py:224-288` - **Sequencing bug in resolve_escalation()**: Uses `get_attempt_number()` which returns `len(attempts)`, but should use the NEXT attempt number for blocked retries. If called before `start_attempt`, attempt 2's escalation is resolved as attempt 1, so fixer never escalates. **FIXED** - Added `next_attempt_number` parameter and logic to calculate next attempt number.

## Major (should fix)
- `tf/retry_state.py:183-211` - **start_attempt() doesn't resume in-progress**: Unconditionally appends new attempt without checking if last attempt is in_progress. Creates duplicate attempts when run crashes/restarts. **FIXED** - Added check for in-progress status and resume logic.
- `skills/tf-workflow/SKILL.md:78-82` - **Agent name mapping documentation**: Uses camelCase in escalation config but hyphenated in agents map. **Already documented** in SKILL.md with explicit mapping note.

## Minor (nice to fix)
- `skills/tf-workflow/SKILL.md:152-161` - Base model resolution note lacks example code. **Documented** - The mapping is explained in the text.
- `tf/retry_state.py:151-155` - `get_attempt_number()` returns 0 for new tickets vs 1-indexed in docs. **By design** - Returns 0 when no attempts, caller adds 1 for next attempt.

## Warnings (follow-up ticket)
- `skills/tf-workflow/SKILL.md:412-420` - No escalation for reviewer-general or reviewer-spec-audit. Only fixer, reviewer-second-opinion, and worker are in escalation curve.
- `skills/tf-workflow/SKILL.md:501-510` - Ralph integration doesn't check in-progress status when picking up tickets.

## Suggestions (follow-up ticket)
- Add `attemptId` UUID for easier log correlation
- Add `reason` field for SKIPPED status
- Document behavior when retry-state.json exists but for different ticket ID
- Add metrics for escalation effectiveness

## Positive Notes
- Opt-in default (`enabled: false`) is correct for backward compatibility
- Detection algorithms have sensible fallback from close-summary to review.md
- Atomic write pattern for retry-state.json shows good defensive coding
- Separation of `attemptNumber` (1-indexed) from `retryCount` (0-indexed) is clear

## Summary Statistics
- Critical: 1 (FIXED)
- Major: 2 (FIXED)
- Minor: 2 (ACCEPTED)
- Warnings: 2
- Suggestions: 4

## Reviewers
- reviewer-general
- reviewer-spec-audit  
- reviewer-second-opinion
