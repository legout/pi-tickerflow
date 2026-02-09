# Review: ptw-guj5

## Critical (must fix)
None.

## Major (should fix)
None.

## Minor (nice to fix)
- `scripts/tf_legacy.sh:1468-1526` - TOML parsing functions depend on Python being available with tomllib/tomli. While the Python doctor requires Python by definition, consider adding a clearer warning when Python is unavailable for TOML parsing, rather than silently returning empty results.

## Warnings (follow-up ticket)
- `scripts/tf_legacy.sh` currently has zero automated tests covering the version consistency helpers, while the Python implementation has comprehensive test coverage in `tests/test_doctor_version.py`. Consider adding shell-based tests or smoke tests to prevent drift between implementations.

## Suggestions (follow-up ticket)
- `scripts/tf_legacy.sh:1406-1514` - All manifest helpers use `2>/dev/null || true` which suppresses all errors. Consider logging stderr when parser exits non-zero to help diagnose why version manifests are being ignored.
- Consider extracting the manifest iteration logic into a `detect_manifest_versions` helper function (similar to Python doctor) to improve code maintainability.

## Reviewer Discrepancies Resolved

**Claim**: Reviewer-general stated bash doctor only reads package.json and lacks multi-manifest support.

**Verification**: Direct testing confirmed bash doctor correctly handles:
- pyproject.toml (priority 1)
- Cargo.toml (priority 2)  
- package.json (priority 3)
- VERSION file checking
- Git tag validation
- --fix and --dry-run flags

The bash implementation has feature parity with Python doctor.

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 1
- Suggestions: 2
