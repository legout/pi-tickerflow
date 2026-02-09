# Fixes: pt-uisf

## Issues Fixed

### Minor Issue - Logic Fix in Test Assertion

**File:** `tests/test_pi_output.py:639`
**Issue:** The assertion used OR when it should use AND to properly verify that neither phrase appears in the output.

**Before:**
```python
assert "output to" not in call_args.lower() or "discarded" not in call_args.lower()
```

**After:**
```python
assert "output to" not in call_args.lower() and "discarded" not in call_args.lower()
```

**Explanation:** The original assertion with OR would pass if EITHER condition was true, which means it would pass if "output to" was present but "discarded" was not. The correct logic requires BOTH to be absent, hence AND.

## Tests Re-run

After fix:
```bash
$ python -m pytest tests/test_pi_output.py::TestOutputRoutingWithoutSubprocess::test_dry_run_shows_routing_decision_inherit -v

1 passed in 0.09s
```

All 87 tests in the related test files continue to pass.
