# Versioning and Releases

This document describes the versioning policy, release process, and version management for the Ticketflow project.

## Semantic Versioning Policy

We follow [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html):

| Version Component | When to Bump | Examples |
|-------------------|--------------|----------|
| **MAJOR** (`X.0.0`) | Breaking changes that require user action | Removing CLI commands, changing config file format, incompatible API changes |
| **MINOR** (`0.X.0`) | New features, backward compatible | Adding new commands, new workflow features, new agent types |
| **PATCH** (`0.0.X`) | Bug fixes, docs improvements | Fixing typos, bug fixes, performance improvements, dependency updates |

### Decision Matrix

- **MAJOR**: Will existing user configs/workflows break? → Bump major
- **MINOR**: Is this a new capability users will want? → Bump minor
- **PATCH**: Does this fix something that's broken? → Bump patch

## Release Checklist

Before releasing a new version, complete all these steps:

- [ ] **1. Update version in `VERSION` file**
  ```bash
  echo "0.2.0" > VERSION
  ```

- [ ] **2. Update `CHANGELOG.md`**
  - Move items from `[Unreleased]` to new version section
  - Add release date (YYYY-MM-DD format)
  - Update comparison links at the bottom

- [ ] **3. Sync `package.json` version** (for documentation consistency)
  ```bash
  npm version $(cat VERSION) --no-git-tag-version --allow-same-version
  ```

- [ ] **4. Run tests**
  ```bash
  pytest
  ```

- [ ] **5. Commit version changes**
  ```bash
  git add VERSION package.json CHANGELOG.md
  git commit -m "Release v$(cat VERSION)"
  ```

- [ ] **6. Create git tag**
  ```bash
  git tag -a "v$(cat VERSION)" -m "Release version $(cat VERSION)"
  ```

- [ ] **7. Push to remote**
  ```bash
  git push origin main
  git push origin "v$(cat VERSION)"
  ```

## Canonical Version Source

The single source of truth for the project version is:

```
VERSION
```

This plain text file contains only the version string (e.g., `0.1.0`).

### How Version is Used

| Location | How Version is Read |
|----------|---------------------|
| **Python Package** (`pyproject.toml`) | `dynamic = ["version"]` with `version = {file = "VERSION"}` |
| **Python Code** | `from tf_cli import __version__` reads at runtime |
| **Node.js** (`package.json`) | Manually synced (package is private, for docs only) |

## Quick Commands

```bash
# View current version
cat VERSION

# Bump version (example: 0.1.0 → 0.2.0)
echo "0.2.0" > VERSION

# Create release commit and tag
./scripts/release.sh  # Or run the checklist above manually
```
