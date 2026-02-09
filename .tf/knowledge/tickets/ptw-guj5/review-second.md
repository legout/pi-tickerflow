# Review (Second Opinion): ptw-guj5

## Overall Assessment
The legacy doctor already includes a version consistency check, but its shell implementation still has gaps compared to the python version. The python helpers and tests (`tests/test_doctor_version.py`) cover manifest parsing, normalization, git tags, and --fix/--dry-run paths thoroughly, yet the bash helper relies on optional dependencies and hides parsing failures, so Python/Rust manifests can be silently ignored when the dependency tree changes.

## Critical (must fix)
- None.

## Major (should fix)
- `scripts/tf_legacy.sh:1468-1514` - `get_pyproject_version` and `get_cargo_version` both try to `import tomllib` and fall back to `import tomli as tomllib`. On Python ≤3.10, tomllib does not exist and tomli is not bundled, so the fallback raises `ModuleNotFoundError`. Because the call is wrapped in `2>/dev/null || true`, the error is swallowed and the version helpers simply return empty. In practice this means that on most standard Linux installations the legacy doctor cannot read pyproject.toml/Cargo.toml, prints “version field missing or invalid,” and cannot construct a canonical version for those languages. That makes version checking ineffective for the very manifests we care about; the helper should either vendor a TOML parser or detect/report the missing dependency so the check keeps working on older Python runtimes.

## Minor (nice to fix)
- None.

## Warnings (follow-up ticket)
- `scripts/tf_legacy.sh` currently has zero automated tests covering the version consistency helpers, while the python implementation is exercised by `tests/test_doctor_version.py`. Any change to the legacy script can therefore drift from the tested behavior without detection. A lightweight shell test or smoke run that mirrors tf_cli/doctor.py would help keep the two implementations in sync.

## Suggestions (follow-up ticket)
- `scripts/tf_legacy.sh:1406-1514` - All manifest helpers invoke `python3 - "$file" <<'PY' …` with `2>/dev/null || true`, so parser failures (missing tomli, invalid TOML, `python3` not installed) are completely silent. That is why the missing tomli dependency is hard to diagnose. Logging stderr when the parser exits non-zero or doing an explicit dependency check would make it much easier for users to understand why their version manifest is being ignored.

## Positive Notes
- `tests/test_doctor_version.py` provides comprehensive unit coverage for the python helpers: manifest detection, normalization, git-tag handling, VERSION file syncing, and fix/dry-run behavior. That thorough coverage gives high confidence in the new version-checking path and provides a solid reference when comparing the legacy bash behavior.

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 0
- Warnings: 1
- Suggestions: 1
