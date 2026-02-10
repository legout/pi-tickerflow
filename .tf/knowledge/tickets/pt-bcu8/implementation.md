# Implementation: pt-bcu8

## Summary
Implemented a timeout backoff calculation helper function in `tf/utils.py` that calculates effective timeout per iteration using linear backoff with optional maximum cap.

## Retry Context
- Attempt: 1
- Escalated Models: fixer=base, reviewer-second=base, worker=base

## Files Changed
- `tf/utils.py` - Added `calculate_timeout_backoff()` function and `DEFAULT_TIMEOUT_INCREMENT_MS` constant

## Key Decisions
- Placed the helper in `tf/utils.py` alongside other utility functions (`read_json`, `find_project_root`, `merge`)
- Used the default increment of 150000 ms as specified in the ticket constraints
- Made `max_ms` parameter optional (None = no cap) for flexibility
- Used `int | None` type annotation for the optional max parameter (Python 3.10+ union syntax)
- Followed the exact formula: `effective = base_ms + iteration_index * increment_ms`
- Included comprehensive docstring with examples demonstrating the backoff behavior

## Implementation Details

### Function Signature
```python
def calculate_timeout_backoff(
    base_ms: int,
    iteration_index: int,
    increment_ms: int = DEFAULT_TIMEOUT_INCREMENT_MS,  # 150000
    max_ms: int | None = None,
) -> int:
```

### Cap Behavior
- When `max_ms` is provided, the result is capped using `min(effective, max_ms)`
- When `max_ms` is None, no cap is applied (unbounded growth)

### Examples from Docstring
- `calculate_timeout_backoff(60000, 0)` → 60000 (base only, first iteration)
- `calculate_timeout_backoff(60000, 1)` → 210000 (base + 1 increment)
- `calculate_timeout_backoff(60000, 2, max_ms=300000)` → 300000 (capped)

## Tests Run
- Python syntax validation: `python -m py_compile tf/utils.py` - PASSED

## Verification
1. Import verification:
   ```python
   from tf.utils import calculate_timeout_backoff, DEFAULT_TIMEOUT_INCREMENT_MS
   ```

2. Basic functionality:
   ```python
   assert calculate_timeout_backoff(60000, 0) == 60000
   assert calculate_timeout_backoff(60000, 1) == 210000
   assert calculate_timeout_backoff(60000, 2, max_ms=250000) == 250000
   ```

## Acceptance Criteria Status
- [x] Helper accepts (base_ms, increment_ms, iteration_index, max_ms?)
- [x] Cap behavior is implemented (min() cap when max_ms provided)
- [x] Units are consistent (ms) and naming is clear
