# Implementation: ptw-guj5

## Summary
Add version checking to legacy bash doctor implementation

## Status
**COMPLETED** - Version checking was already implemented in `scripts/tf_legacy.sh`

## Findings

Upon investigation, the version checking functionality was already present in the legacy bash doctor implementation. The bash script includes complete feature parity with the Python `doctor.py` implementation.

## Implementation Details

### Functions Present in tf_legacy.sh

1. **`get_package_version()`** - Reads version from package.json using Python helper
2. **`get_pyproject_version()`** - Reads version from pyproject.toml [project] section
3. **`get_cargo_version()`** - Reads version from Cargo.toml [package] section
4. **`get_version_file_version()`** - Reads version from VERSION file
5. **`get_git_tag_version()`** - Gets version from current git tag
6. **`normalize_version()`** - Strips v/V prefix from versions for comparison
7. **`sync_version_file()`** - Creates/updates VERSION file to match canonical version
8. **`check_version_consistency()`** - Main function that checks all version sources

### Features Supported

- Multi-language manifest support (pyproject.toml, Cargo.toml, package.json)
- Priority order: pyproject.toml > Cargo.toml > package.json
- VERSION file consistency checking
- Git tag validation (warns on mismatch)
- Cross-manifest version mismatch warnings
- `--fix` flag to auto-update VERSION file
- `--dry-run` flag to preview changes
- v/V prefix normalization for comparison

### Integration

The `doctor()` function calls `check_version_consistency` at the end of its execution:

```bash
# Version consistency check
echo "Version consistency:"
local project_root
project_root="$(dirname "$TF_BASE")"
if ! check_version_consistency "$project_root" "$fix" "$dry_run"; then
  failed=1
fi
```

## Verification

Tested the bash doctor:

```bash
$ bash scripts/tf_legacy.sh doctor
Ticketflow doctor
[ok] tk
[ok] pi
...
Version consistency:
[info] pyproject.toml: version field missing or invalid
[ok] package.json version: 0.1.0
[ok] VERSION file matches package.json: 0.1.0
```

The version checking is working correctly.

## Files Involved

- `scripts/tf_legacy.sh` - Contains the bash implementation (lines ~1088-1289)
- `tf_cli/doctor.py` - Python implementation (reference)
- `tests/test_doctor_version.py` - Tests for Python implementation (all pass)

## Conclusion

No code changes were required. The legacy bash doctor already includes complete version checking functionality that matches the Python implementation feature-for-feature.
