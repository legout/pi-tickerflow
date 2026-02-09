# Fixes: ptw-nw3d

## Summary
Fixed Critical and Major issues identified in code review.

## Fixed Issues

### Critical (1 fixed)
- `tf_cli/version.py:89` - Module-level `__version__` caching issue
  - **Solution**: Replaced module-level `__version__ = get_version()` with `__getattr__` lazy loading
  - This prevents caching "unknown" at import time and allows proper test mocking

### Major (2 fixed, 1 deferred)
- `tf_cli/version.py:82-85` - Removed problematic CWD fallback
  - **Solution**: Removed the current working directory fallback that could return wrong version
  - Updated docstring to reflect new 2-step fallback (repo root → package root → unknown)
  
- `tests/test_version.py:51` - Missing assertion in test
  - **Solution**: Added `assert result == "2.0.0"` to `test_falls_back_to_module_parent`

- `README.md` - SemVer documentation (deferred)
  - **Reason**: Requires manual documentation update outside scope of code fixes

### Minor (1 fixed)
- `tf_cli/version.py:68` - Clarified comment about VERSION file location
  - **Solution**: Changed "relative to this module" to "at package root (parent of tf_cli/)"

## Tests
All 11 tests in test_version.py pass after fixes.

## Verification
```python
from tf_cli.version import get_version, __version__
print(get_version())   # Output: 0.1.0
print(__version__)     # Output: 0.1.0
```
