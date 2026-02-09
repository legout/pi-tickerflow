# Review: ptw-n2s4

## Critical (must fix)
No issues found.

## Major (should fix)
- `scripts/sync-version.sh:12` - VERSION file read lacks validation. If VERSION is missing, empty, or contains invalid semver, the script fails with cryptic npm errors. Add validation:
  ```bash
  if [[ ! -f "${REPO_ROOT}/VERSION" ]]; then
      echo "Error: VERSION file not found" >&2
      exit 1
  fi
  VERSION=$(cat "${REPO_ROOT}/VERSION" | tr -d '[:space:]')
  if [[ -z "$VERSION" ]]; then
      echo "Error: VERSION file is empty" >&2
      exit 1
  fi
  if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
      echo "Error: VERSION file contains invalid semver: $VERSION" >&2
      exit 1
  fi
  ```

## Minor (nice to fix)
- `scripts/sync-version.sh:19` - npm version output includes 'v' prefix which may confuse users. Consider suppressing with `> /dev/null` or documenting this is expected npm behavior.
- `scripts/sync-version.sh:18` - The `cd` changes working directory but script relies on subshell behavior. Using `(cd "${REPO_ROOT}" && npm version ...)` would make scope clearer.
- `package.json:3` - Version is hardcoded rather than dynamically derived. While acceptable for MVP per VERSIONING.md, this creates drift risk. The sync script mitigates this.
- `scripts/sync-version.sh` - Consider capturing npm output for cleaner script output.

## Warnings (follow-up ticket)
- `scripts/sync-version.sh` - No test coverage for the sync script. Consider adding tests for VERSION reading, missing npm handling, and invalid version content.
- `VERSIONING.md` - Manual sync procedure is documented but not enforced. Consider pre-commit hook for auto-sync.
- `package.json` - npm version rewrites package.json with its own formatting rules, potentially causing unnecessary diffs across npm versions.
- Missing `CHANGELOG.md` - The seed vision specified maintaining a changelog (not strictly in ticket AC).

## Suggestions (follow-up ticket)
- `scripts/sync-version.sh` - Add `--check` or `--dry-run` mode for CI validation without making changes.
- `VERSIONING.md` - Consider documenting prerelease version patterns (e.g., `1.0.0-beta.1`).
- `VERSIONING.md` - Add validation step to release checklist to verify version consistency across all files.
- `package.json` - Consider adding `version:bump` script combining VERSION update and sync.
- `pyproject.toml` - Consider adding `[project.urls]` section with repository/documentation links.
- `tf_cli/version.py` - Consider caching version at build time or using `functools.lru_cache` on `get_version()`.
- Create `CHANGELOG.md` with initial entry for v0.1.0 per seed vision.

## Summary Statistics
- Critical: 0
- Major: 1
- Minor: 4
- Warnings: 4
- Suggestions: 7

## Reviewers
- reviewer-general: No critical/major issues, 2 minor, 2 warnings, 2 suggestions
- reviewer-spec-audit: No critical/major issues, 1 minor, 2 warnings, 3 suggestions
- reviewer-second-opinion: No critical issues, 1 major, 2 minor, 1 warning, 2 suggestions
