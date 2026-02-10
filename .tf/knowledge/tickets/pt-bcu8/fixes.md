# Fixes: pt-bcu8

## Summary
Applied all Critical and Major fixes identified in review. The implementation now matches the specification with proper parameter order and comprehensive input validation.

## Fixes by Severity

### Critical (must fix)
- [x] `tf/utils.py:79` - **Parameter order corrected**: Changed function signature from `(base_ms, iteration_index, increment_ms, max_ms)` to `(base_ms, increment_ms, iteration_index, max_ms)` to match the ticket specification. This ensures API contract consistency.

### Major (should fix)
- [x] `tf/utils.py:79` - **Input validation added**: Added validation to ensure all time-related parameters are non-negative:
  - `base_ms < 0` → raises `ValueError`
  - `increment_ms < 0` → raises `ValueError`
  - `iteration_index < 0` → raises `ValueError`
  
- [x] `tf/utils.py:79` - **Max cap validation added**: Added check to ensure `max_ms >= base_ms`. If caller passes `max_ms` smaller than `base_ms`, raises `ValueError` to prevent silently reducing timeout below the intended minimum.

### Minor (nice to fix)
- [ ] `tf/utils.py:8` - Type annotation style consistency (deferred - module-wide change)
- [ ] `tf/utils.py:63` - `__all__` export declaration (deferred - API design decision)
- [ ] `tf/utils.py:79` - `iteration_index` naming (deferred - current name is acceptable)

### Warnings (follow-up)
- [ ] `tf/utils.py:91` - Unbounded iteration growth documentation (deferred to follow-up ticket)

### Suggestions (follow-up)
- [ ] `tf/utils.py:79` - Descriptive error messages (implemented as part of Major fixes)
- [ ] `tf/utils.py:72` - Comment explaining default value (deferred)

## Summary Statistics
- **Critical**: 1 fixed
- **Major**: 2 fixed
- **Minor**: 0 fixed (3 deferred)
- **Warnings**: 0 fixed (1 deferred)
- **Suggestions**: 0 fixed (2 deferred, though descriptive errors were implemented)

## Verification
- Python syntax validation: `python -m py_compile tf/utils.py` - PASSED
- Functional tests: All test cases passed
  - Basic backoff calculation
  - Cap behavior
  - Negative value validation
  - Max < base validation
