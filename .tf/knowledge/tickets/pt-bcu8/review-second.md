# Review: pt-bcu8

## Overall Assessment
The implementation correctly calculates linear timeout backoff with optional capping. However, there is a subtle but significant deviation from the ticket specification regarding parameter order, and several edge cases around input validation that could cause unexpected behavior in production.

## Critical (must fix)
- `tf/utils.py:79` - Parameter order mismatch with specification: the ticket requires `(base_ms, increment_ms, iteration_index, max_ms?)` but the implementation uses `(base_ms, iteration_index, increment_ms, max_ms)`. This breaks API contract consistency and will confuse callers expecting the documented signature.

## Major (should fix)
- `tf/utils.py:79` - No input validation for negative values: `iteration_index=-1` produces timeout less than base (mathematically valid but semantically wrong), and negative `base_ms` or `increment_ms` produce nonsensical negative timeouts. Consider adding assertions or validation.
- `tf/utils.py:79` - No protection against `max_ms < base_ms`: If caller accidentally passes `max_ms` smaller than `base_ms`, the cap silently reduces timeout below the intended minimum, violating the "at least base timeout" semantic expectation.

## Minor (nice to fix)
- `tf/utils.py:1` - Inconsistent type annotation style: module uses `Optional[Path]` (line 22) but new code uses `int | None` (Python 3.10+ union syntax). While functional, mixing styles reduces maintainability.
- `tf/utils.py:101` - Missing type hints in docstring examples: the docstring shows numeric literals but doesn't indicate expected types, which could confuse users about whether ms parameters accept floats.
- `tf/utils.py:79` - `iteration_index` naming could be clearer as `iteration` or `attempt` since "index" implies array indexing semantics that may not apply here.

## Warnings (follow-up ticket)
- `tf/utils.py:101` - No explicit overflow consideration: while Python handles arbitrarily large integers, extremely large `iteration_index` values (e.g., from a runaway loop) could cause memory/performance issues when calculating `iteration_index * increment_ms`. The calling code should have iteration limits.

## Suggestions (follow-up ticket)
- `tf/utils.py:79` - Consider adding a `@functools.lru_cache` decorator if the same calculations are repeated frequently with identical parameters, though this depends on actual usage patterns.
- `tf/utils.py:79` - Consider returning a dataclass or namedtuple with `.effective`, `.capped` fields to give callers visibility into whether capping occurred (useful for debugging/metrics).

## Positive Notes
- Clean, readable implementation with excellent docstring including working examples
- Good placement in `tf/utils.py` alongside related utilities
- Sensible default constant with clear naming convention
- Proper use of `min()` for capping - concise and Pythonic
- Type annotations present for all parameters and return value

## Summary Statistics
- Critical: 1
- Major: 2
- Minor: 3
- Warnings: 1
- Suggestions: 2
