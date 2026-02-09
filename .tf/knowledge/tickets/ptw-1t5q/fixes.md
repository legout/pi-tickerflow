# Fixes: ptw-1t5q

## Summary
Fixed the `normalize_version()` function to use precise single-character prefix removal instead of `lstrip("vV")`.

## Issues Fixed

### Critical: lstrip strips all leading v/V characters
**Location:** `tf_cli/doctor_new.py:201-209`
**Problem:** `str.lstrip("vV")` strips ALL leading 'v' or 'V' characters, not just a single prefix. This could cause incorrect comparisons.
**Fix:** Changed to use `version.lower().startswith('v')` check followed by `version[1:]` slice for precise single-character prefix removal.

**Before:**
```python
def normalize_version(version: str) -> str:
    ...
    return version.lstrip("vV")
```

**After:**
```python
def normalize_version(version: str) -> str:
    ...
    if version.lower().startswith('v'):
        return version[1:]
    return version
```

### Major: Docstring incorrectly claims "lowercase" return
**Location:** `tf_cli/doctor_new.py:208`
**Problem:** Docstring claimed return value is "lowercase" but function doesn't call `.lower()`.
**Fix:** Removed "(lowercase" from the docstring Returns description.

## Verification
All edge cases tested and pass:
- `v0.1.0` → `0.1.0` ✓
- `V0.1.0` → `0.1.0` ✓
- `0.1.0` → `0.1.0` ✓
- `vv1.0.0` → `v1.0.0` (only strips first v) ✓
- `version1.0` → `ersion1.0` (only strips first char if v/V) ✓
- `v1.0.0-alpha` → `1.0.0-alpha` ✓

Version consistency check with VERSION file still works correctly.
