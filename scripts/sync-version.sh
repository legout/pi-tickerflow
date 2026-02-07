#!/bin/bash
# Sync version from VERSION file to all package metadata files
# Usage: ./scripts/sync-version.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Validate VERSION file exists
if [[ ! -f "${REPO_ROOT}/VERSION" ]]; then
    echo "Error: VERSION file not found at ${REPO_ROOT}/VERSION" >&2
    exit 1
fi

# Read and validate VERSION content
VERSION=$(cat "${REPO_ROOT}/VERSION" | tr -d '[:space:]')
if [[ -z "$VERSION" ]]; then
    echo "Error: VERSION file is empty" >&2
    exit 1
fi

# Validate semver format (MAJOR.MINOR.PATCH)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
    echo "Error: VERSION file contains invalid semver: $VERSION" >&2
    exit 1
fi

echo "Syncing version: ${VERSION}"

# Update package.json (Node.js metadata)
# Using npm version to properly update package.json
if command -v npm &> /dev/null; then
    (cd "${REPO_ROOT}" && npm version "${VERSION}" --no-git-tag-version --allow-same-version > /dev/null)
    echo "✓ package.json updated"
else
    echo "⚠ npm not found, skipping package.json sync"
fi

echo "Version sync complete: ${VERSION}"
