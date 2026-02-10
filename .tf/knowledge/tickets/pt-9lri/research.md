# Research: pt-9lri

## Status
Research enabled but minimal - implementation is straightforward based on existing code.

## Context Reviewed
- `tk show pt-9lri` - Unit tests for timeout backoff calculation
- `tk show pt-bcu8` - Implementation ticket (closed) with `calculate_timeout_backoff()` in tf/utils.py
- `/home/volker/coding/pi-ticketflow/tf/utils.py` - Contains the function to test
- `/home/volker/coding/pi-ticketflow/tests/test_utils.py` - Existing test patterns

## Implementation Details from pt-bcu8

Function signature:
```python
def calculate_timeout_backoff(
    base_ms: int,
    increment_ms: int,
    iteration_index: int,
    max_ms: int | None = None,
) -> int:
```

Formula: `effective = base_ms + iteration_index * increment_ms`
- Capped at `max_ms` when provided
- Default increment: 150000 ms (DEFAULT_TIMEOUT_INCREMENT_MS)
- Input validation for negative values

## Acceptance Criteria Mapping
1. Tests cover iteration_index=0 and iteration_index=1 semantics ✓
2. Tests cover cap behavior (max_timeout_ms) ✓
3. Tests cover non-default increment override ✓

## Sources
- tf/utils.py (implementation)
- tests/test_utils.py (test patterns)
