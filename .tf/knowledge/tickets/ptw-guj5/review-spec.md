# Review (Spec Audit): ptw-guj5

## Overall Assessment
The implementation successfully adds version checking to the legacy bash doctor, achieving feature parity with the Python doctor implementation. All major requirements from the ticket are addressed: multi-manifest version checking (pyproject.toml, Cargo.toml, package.json), git tag validation, VERSION file sync with --fix/--dry-run support, and proper version normalization.

## Critical (must fix)
No issues found

## Major (should fix)
No issues found

## Minor (nice to fix)
- `scripts/tf_legacy.sh:1123-1169` - Error handling for VERSION file reading is less granular than Python doctor. The Python version explicitly handles PermissionError, UnicodeDecodeError, and OSError with specific warning messages, while the bash version uses generic `|| true` suppression. Consider adding explicit error messages for common failure cases.

## Warnings (follow-up ticket)
- `scripts/tf_legacy.sh:1041-1085` - The TOML parsing functions (`get_pyproject_version`, `get_cargo_version`) depend on Python being available. If Python is not installed, these functions fail silently. While this is consistent with the Python doctor (which requires Python by definition), the bash doctor could potentially provide a clearer warning when Python is unavailable for TOML parsing.

## Suggestions (follow-up ticket)
- `scripts/tf_legacy.sh:1171-1182` - Consider adding a `detect_manifest_versions` helper function (like the Python doctor has) to consolidate manifest detection logic and make the code more maintainable. Currently the manifest iteration logic is embedded directly in `check_version_consistency`.
- Consider adding test coverage for the bash version checking functions, similar to the Python doctor's test suite (`tests/test_doctor_version.py`).

## Positive Notes
- Version checking functions correctly mirror Python doctor behavior
- Proper manifest priority order implemented: pyproject.toml > Cargo.toml > package.json
- Version normalization (v/V prefix stripping) implemented consistently
- Git tag checking with `git describe --tags --exact-match` works correctly
- --fix and --dry-run flags are properly passed through and handled
- VERSION file sync correctly adds trailing newline (matches Python behavior)
- Multi-manifest version mismatch detection warns but doesn't fail (correct behavior)
- `scripts/tf_legacy.sh` was properly added to `config/install-manifest.txt`
- Script syntax validated and execution verified

## Summary Statistics
- Critical: 0
- Major: 0
- Minor: 1
- Warnings: 1
- Suggestions: 2

## Spec Coverage
- Spec/plan sources consulted: 
  - Ticket description: "Add version checking to legacy bash doctor implementation"
  - Implementation notes in ticket
  - Python doctor reference: `tf_cli/doctor.py`
- Missing specs: none
