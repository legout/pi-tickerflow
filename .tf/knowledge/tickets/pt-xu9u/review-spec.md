# Review: pt-xu9u (Spec Audit)

## Overall Assessment
The retry-aware escalation feature has been implemented with comprehensive documentation in SKILL.md and a working Python module (tf/retry_state.py). All four acceptance criteria are addressed, but there are two critical sequencing bugs in the retry_state.py implementation that cause the escalation curve to behave incorrectly: attempt number resolution happens before the new attempt is recorded, and in-progress attempts are not resumed but always create new entries.

## Critical (must fix)
- `tf/retry_state.py:224-288` - `resolve_escalation()` uses `self.get_attempt_number()` which returns `len(attempts)`, but the SKILL.md procedure (Load Retry State, step 3-4) calculates `attemptNumber = len(attempts) + 1` for blocked retries. If `resolve_escalation` is called before `start_attempt`, attempt 2's escalation is resolved as if it were attempt 1, so the fixer never escalates on the first retry. **Impact**: The escalation curve never starts; all retries use base models. **Fix**: Either call `start_attempt` before `resolve_escalation`, or make `resolve_escalation` accept an explicit `next_attempt_number` parameter.

## Major (should fix)
- `tf/retry_state.py:183-211` - `start_attempt()` unconditionally appends a new attempt entry without checking if `attempts[-1]['status'] == 'in_progress'`. The SKILL.md (Load Retry State, step 3) explicitly requires resuming in-progress attempts, but the implementation creates duplicate attempts when a run crashes and restarts. **Impact**: Aborted executions consume retry counts and trigger premature escalation. **Fix**: Check last attempt status in `start_attempt` and either update the existing entry or return its number instead of appending.
- `tf/retry_state.py:151-155` - `get_attempt_number()` returns 0 for new tickets (no attempts), but the SKILL.md uses 1-indexed attempt numbers throughout. While the SKILL.md handles this by setting `attemptNumber = 1` for fresh tickets, the inconsistency between the Python API and documented behavior could cause integration bugs. **Impact**: Potential off-by-one errors in workflow integration. **Fix**: Document this behavior clearly or make `get_attempt_number()` return 1 for uninitialized state.

## Minor (nice to fix)
- `skills/tf-workflow/SKILL.md:152-161` - The base model resolution note explains hyphenated vs camelCase mapping, but doesn't explicitly show the lookup code. A brief example would help implementers.

## Warnings (follow-up ticket)
- None.

## Suggestions (follow-up ticket)
- Consider adding a `get_next_attempt_number()` method to RetryState that returns `len(attempts) + 1`, making the intent explicit for callers.

## Positive Notes
- `skills/tf-workflow/SKILL.md:163-211` - Detection algorithms are thoroughly documented with regex patterns, making implementation straightforward.
- `.tf/config/settings.json:126-155` - Escalation configuration is properly integrated with `enabled: false` default, satisfying the "no behavior change when disabled" constraint.
- `tf/retry_state.py:298-345` - `detect_blocked_from_close_summary()` and `detect_blocked_from_review()` faithfully implement the documented detection algorithms.
- `tf/retry_state.py:41-82` - Retry state schema uses TypedDict for type safety and includes comprehensive docstrings.

## Summary Statistics
- Critical: 1
- Major: 2
- Minor: 1
- Warnings: 0
- Suggestions: 1

## Acceptance Criteria Verification

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Retry attempt loaded from retry state before running phases | ✅ Met | `skills/tf-workflow/SKILL.md:119-161` Load Retry State sub-procedure |
| Attempt 2 escalates fixer model (if configured) | ⚠️ Partially Met | Documented in SKILL.md table, but `resolve_escalation()` bug prevents correct resolution |
| Attempt 3+ escalates fixer + reviewer-second-opinion (+ worker) | ⚠️ Partially Met | Same issue as above - sequencing bug affects all escalation levels |
| Retry attempt number and escalated roles/models recorded in artifacts/logs | ✅ Met | `retry-state.json` schema includes attempt history and escalation; `implementation.md` template includes retry context |

## Constraint Verification
- **No behavior change when escalation disabled**: ✅ Verified - Default `enabled: false` in settings.json; SKILL.md checks `workflow.escalation.enabled` before applying escalation logic.
