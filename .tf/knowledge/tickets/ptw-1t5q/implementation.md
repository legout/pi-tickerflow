# Implementation: ptw-1t5q

## Summary
Added version normalization for VERSION file comparison in doctor_new.py. The `v` or `V` prefix is now stripped when comparing versions between VERSION file and package.json.

## Files Changed
- `tf_cli/doctor_new.py` - Added `normalize_version()` function and updated `check_version_consistency()` to use normalized versions for comparison

## Key Decisions
- Used `str.lstrip("vV")` to strip both lowercase and uppercase V prefixes
- Only normalized for comparison - the original version strings are still displayed in messages for clarity
- This follows common semantic versioning conventions where tags often include "v" prefix (e.g., git tags like "v1.0.0") while package.json typically stores bare versions

## Tests Run
Tested three scenarios:
1. VERSION file with "v" prefix: `v0.1.0` → matches `0.1.0` in package.json ✓
2. VERSION file without prefix: `0.1.0` → matches `0.1.0` in package.json ✓  
3. VERSION file with uppercase "V": `V0.1.0` → matches `0.1.0` in package.json ✓
4. Actual mismatch: `v1.0.0` vs `0.1.0` → correctly shows warning ✓

## Verification
Run the doctor to verify version consistency check works:
```bash
python3 -c "from tf_cli.doctor_new import check_version_consistency, find_project_root; check_version_consistency(find_project_root())"
```
