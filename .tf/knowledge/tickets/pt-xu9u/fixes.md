# Fixes: pt-xu9u (Attempt 3)

## Summary
Fixed Critical and Major issues identified in Attempt 3 review of the retry_state.py implementation.

## Critical Fix

### 1. resolve_escalation() Sequencing Bug (CRITICAL → FIXED)
**Issue**: `resolve_escalation()` used `get_attempt_number()` which returns `len(attempts)` (completed attempts), but for blocked retries we need the NEXT attempt number to determine correct escalation.

**Impact**: Attempt 2's escalation was resolved as if it were attempt 1, so the fixer never escalated on the first retry. The escalation curve never started.

**Fix**: 
- Added `next_attempt_number: int | None = None` parameter to `resolve_escalation()`
- If explicit number provided, use it; otherwise calculate as `get_attempt_number() + 1`
- This ensures blocked retries get the correct escalation level for their next attempt

**Code Change** (`tf/retry_state.py`):
```python
def resolve_escalation(
    self,
    escalation_config: dict[str, Any],
    base_models: dict[str, str],
    next_attempt_number: int | None = None,  # NEW PARAMETER
) -> EscalatedModels:
    # ...
    if next_attempt_number is not None:
        attempt = next_attempt_number
    else:
        attempt = self.get_attempt_number() + 1  # Calculate next attempt
```

## Major Fixes

### 2. start_attempt() In-Progress Resume (MAJOR → FIXED)
**Issue**: `start_attempt()` unconditionally appended a new attempt without checking if the last attempt was still "in_progress". Created duplicate attempts when a run crashed and restarted.

**Impact**: Aborted executions consumed retry counts and triggered premature escalation.

**Fix**:
- Added check for existing in-progress attempt before creating new one
- If last attempt status is "in_progress", resume it instead of creating duplicate
- Update trigger, quality_gate, and escalation if provided during resume

**Code Change** (`tf/retry_state.py`):
```python
def start_attempt(self, ...):
    # Check if we should resume an in-progress attempt
    if self._data["attempts"]:
        last_attempt = self._data["attempts"][-1]
        if last_attempt.get("status") == "in_progress":
            # Resume existing attempt
            if trigger:
                last_attempt["trigger"] = trigger
            if quality_gate:
                last_attempt["qualityGate"] = quality_gate
            if escalation:
                last_attempt["escalation"] = escalation
            self._data["lastAttemptAt"] = now
            return last_attempt["attemptNumber"]
    
    # ... create new attempt if no in-progress found
```

### 3. SKILL.md Documentation (MAJOR → ACCEPTED)
**Issue**: Reviewers noted camelCase vs hyphenated agent names could cause confusion.

**Status**: Already documented in SKILL.md with explicit mapping note. The documentation clearly states:
- `reviewerSecondOpinion` (escalation config) → `agents.reviewer-second-opinion` (agents map)
- `fixer` → `agents.fixer`
- `worker` → `agents.worker`

No code changes needed - documentation is correct.

## Files Modified
- `tf/retry_state.py` - Fixed resolve_escalation() and start_attempt()

## Verification
- [x] resolve_escalation() now calculates next attempt number correctly
- [x] start_attempt() resumes in-progress attempts instead of duplicating
- [x] Escalation curve works: Attempt 2 escalates fixer, Attempt 3+ escalates fixer + reviewer-second-opinion
- [x] No duplicate attempts created on crash restart

## Status
All Critical and Major issues from Attempt 3 review have been fixed.
