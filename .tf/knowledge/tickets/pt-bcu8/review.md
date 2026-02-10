# Review: pt-bcu8

## Critical (must fix)
- `tf/utils.py:79` - Parameter order mismatch with specification: the ticket requires `(base_ms, increment_ms, iteration_index, max_ms?)` but the implementation uses `(base_ms, iteration_index, increment_ms, max_ms)`. This breaks API contract consistency and will confuse callers expecting the documented signature.

## Major (should fix)
- `tf/utils.py:79` - No input validation for negative values. Negative `base_ms`, `iteration_index`, `increment_ms`, or `max_ms` would produce nonsensical timeout values (e.g., negative timeouts). Add validation to ensure all time-related parameters are non-negative.
- `tf/utils.py:79` - No protection against `max_ms < base_ms`: If caller accidentally passes `max_ms` smaller than `base_ms`, the cap silently reduces timeout below the intended minimum, violating the "at least base timeout" semantic expectation.

## Minor (nice to fix)
- `tf/utils.py:8` - Inconsistent type annotation style. Uses `Optional[Path]` (old style) alongside `int | None` (Python 3.10+ union style). Consider standardizing on the newer union syntax throughout the module.
- `tf/utils.py:63` - Function lacks `__all__` export declaration. Adding `calculate_timeout_backoff` and `DEFAULT_TIMEOUT_INCREMENT_MS` to the module's `__all__` list would improve API discoverability.
- `tf/utils.py:79` - `iteration_index` naming could be clearer as `iteration` or `attempt` since "index" implies array indexing semantics that may not apply here.

## Warnings (follow-up ticket)
- `tf/utils.py:91` - Potential performance concern with unbounded iteration growth. While Python handles large integers, extremely large `iteration_index` values (e.g., from a runaway loop) could cause memory issues. Consider documenting maximum expected iteration count or adding a sanity check.

## Suggestions (follow-up ticket)
- `tf/utils.py:79` - Consider adding validation that raises `ValueError` with descriptive messages for invalid inputs rather than silently accepting negative values.
- `tf/utils.py:72` - Consider adding a brief comment explaining why 150000ms (2.5 minutes) was chosen as the default.

## Summary Statistics
- Critical: 1
- Major: 2
- Minor: 3
- Warnings: 1
- Suggestions: 2

## Reviewer Sources
- reviewer-general: Major (negative validation, tests), Minor (type style, __all__)
- reviewer-spec-audit: No issues (spec compliant except parameter order)
- reviewer-second-opinion: Critical (parameter order), Major (negative validation, max < base), Minor (naming)
