# Implementation: pt-9lri

## Summary
Added comprehensive unit tests for the `calculate_timeout_backoff` function in `tf/utils.py`, covering iteration indexing semantics, cap behavior, and non-default increment overrides.

## Retry Context
- Attempt: 1
- Escalated Models: fixer=base, reviewer-second=base, worker=base

## Files Changed
- `tests/test_utils.py` - Consolidated duplicate test classes and added comprehensive tests for `calculate_timeout_backoff`

## Key Changes

### Test Coverage Added

The tests cover all acceptance criteria from the ticket:

1. **Iteration Index Semantics** (Zero-based indexing):
   - `iteration_index=0` returns base timeout (no increment)
   - `iteration_index=1` adds exactly one increment
   - `iteration_index=2` adds two increments

2. **Cap Behavior** (`max_timeout_ms`):
   - Cap applied when effective timeout exceeds max
   - Cap not applied when effective is below max
   - Edge case: effective exactly equals max
   - Edge case: max equals base (always capped)
   - No cap when max_ms is None

3. **Non-Default Increment Override**:
   - Custom increment values work correctly
   - Zero increment produces constant timeout
   - Large iteration indices handled correctly

4. **Input Validation**:
   - Negative base_ms raises ValueError
   - Negative increment_ms raises ValueError
   - Negative iteration_index raises ValueError
   - max_ms < base_ms raises ValueError
   - Zero base timeout is valid

### Code Quality Improvements

- Removed duplicate `TestCalculateTimeoutBackoff` class (was present twice in the file)
- Organized tests with clear section comments
- Added comprehensive docstrings explaining test purpose
- All 34 tests in the file pass

## Tests Run

```bash
$ python -m pytest tests/test_utils.py::TestCalculateTimeoutBackoff -v
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-0.13.1
collected 17 items

tests/test_utils.py::TestCalculateTimeoutBackoff::test_iteration_index_zero_returns_base PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_iteration_index_one_adds_single_increment PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_iteration_index_two_adds_two_increments PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_cap_applied_when_effective_exceeds_max PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_cap_not_applied_when_effective_below_max PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_cap_exactly_at_max PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_cap_with_max_equal_to_base PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_no_cap_when_max_ms_is_none PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_non_default_increment_override PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_zero_increment_constant_timeout PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_large_iteration_index PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_zero_base_timeout_is_valid PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_negative_base_ms_raises PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_negative_increment_ms_raises PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_negative_iteration_index_raises PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_max_ms_less_than_base_raises PASSED
tests/test_utils.py::TestCalculateTimeoutBackoff::test_default_increment_constant_value PASSED

============================== 17 passed in 0.04s ==============================
```

Full test suite also passes:
```bash
$ python -m pytest tests/test_utils.py -v
============================== 34 passed in 0.06s ==============================
```

## Verification

Run the following to verify:

```bash
python -m pytest tests/test_utils.py::TestCalculateTimeoutBackoff -v
```

All tests are fast and hermetic:
- No I/O operations (except tmp_path fixtures in other test classes)
- No external dependencies
- Pure function testing with deterministic inputs/outputs
