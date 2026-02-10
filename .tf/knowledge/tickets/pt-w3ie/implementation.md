# Implementation: pt-w3ie

## Summary
Wire timeout backoff into the retry/iteration timeout enforcement point.

## Status
**COMPLETE** - The timeout backoff was already fully implemented in the codebase.

## Files Changed
No changes required - implementation was already in place.

## Implementation Details

The timeout backoff feature was found to be already fully implemented:

### 1. Core Calculation (tf/utils.py)
- `calculate_timeout_backoff()` - Computes effective timeout using linear backoff
- Formula: `effective = base_ms + iteration_index * increment_ms`
- Supports optional `max_ms` cap
- Default increment: **150000 ms** (as per spec)

### 2. Configuration Resolution (tf/ralph.py)
- `resolve_timeout_backoff_enabled()` - Checks if backoff is enabled
- `resolve_timeout_backoff_increment_ms()` - Gets increment from config
- `resolve_timeout_backoff_max_ms()` - Gets max cap from config
- Default config values in `DEFAULTS` dict:
  - `timeoutBackoffEnabled: False` (backwards compatible)
  - `timeoutBackoffIncrementMs: 150000`
  - `timeoutBackoffMaxMs: 0` (no cap by default)

### 3. Effective Timeout Calculation (tf/ralph.py)
- `calculate_effective_timeout()` - Wrapper that applies backoff when enabled
- Returns base timeout when backoff disabled or timeout is 0
- Calls `calculate_timeout_backoff()` when enabled

### 4. Enforcement Points (tf/ralph.py)
The effective timeout is wired into both enforcement locations:

#### A. `ralph_run()` function (single ticket execution)
```python
effective_timeout_ms = calculate_effective_timeout(
    base_timeout_ms=base_timeout_ms,
    attempt_index=attempt,  # 0-indexed
    backoff_enabled=backoff_enabled,
    increment_ms=backoff_increment_ms,
    max_ms=backoff_max_ms,
)
# Passed to run_ticket(timeout_ms=effective_timeout_ms)
```

#### B. `ralph_start()` function (serial mode restart loop)
```python
effective_timeout_ms = calculate_effective_timeout(
    base_timeout_ms=base_timeout_ms,
    attempt_index=attempt - 1,  # 0-indexed for first attempt
    backoff_enabled=backoff_enabled,
    increment_ms=backoff_increment_ms,
    max_ms=backoff_max_ms,
)
# Passed to run_ticket(timeout_ms=effective_timeout_ms)
```

### 5. Observability (Logging)
The implementation logs effective timeout at key points:
- Initial timeout when backoff is enabled and differs from base
- Timeout value on each restart attempt
- Timeout value in error messages when attempts time out

### 6. Unit Tests (tests/test_utils.py)
Comprehensive test coverage in `TestCalculateTimeoutBackoff`:
- ✅ Iteration index semantics (0, 1, 2+)
- ✅ Cap behavior (applied when exceeded, not applied when under)
- ✅ Edge cases (cap exactly at max, max equal to base)
- ✅ No cap when max_ms is None
- ✅ Non-default increment override
- ✅ Zero increment (constant timeout)
- ✅ Large iteration index
- ✅ Input validation (negative values raise ValueError)

## Acceptance Criteria Verification

| Criteria | Status | Notes |
|----------|--------|-------|
| Effective timeout computed using iteration index | ✅ | `calculate_effective_timeout()` uses `attempt_index` |
| Applied to enforcement | ✅ | Passed to `run_ticket(timeout_ms=...)` which uses `_run_with_timeout()` |
| Base/increment/max from config | ✅ | Resolved via `resolve_timeout_backoff_*` functions |
| Backwards compatible | ✅ | `timeoutBackoffEnabled: False` by default |

## Configuration Example

To enable timeout backoff, add to `.tf/ralph/config.json`:

```json
{
  "attemptTimeoutMs": 600000,
  "maxRestarts": 2,
  "timeoutBackoffEnabled": true,
  "timeoutBackoffIncrementMs": 150000,
  "timeoutBackoffMaxMs": 900000
}
```

## Behavior Examples

With base=600000ms, increment=150000ms, max=900000ms:

| Attempt | Effective Timeout | Notes |
|---------|------------------|-------|
| 1 (index 0) | 600000 ms | Base timeout |
| 2 (index 1) | 750000 ms | Base + 1×increment |
| 3 (index 2) | 900000 ms | Base + 2×increment, capped |
| 4+ (index 3+) | 900000 ms | Capped at max |

## Retry Context
- Attempt: 1
- Escalated Models: fixer=base, reviewer-second=base, worker=base
