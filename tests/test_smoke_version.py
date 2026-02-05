#!/usr/bin/env python3
"""Smoke test for `tf --version`.

This module contains quick smoke tests to verify basic CLI functionality.
"""

from __future__ import annotations

import re
import subprocess
import sys

import pytest


def run_tf_version() -> tuple[int, str]:
    """Run `tf --version` and return (exit_code, stdout)."""
    try:
        result = subprocess.run(
            ["tf", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode, result.stdout.strip()
    except FileNotFoundError:
        print("ERROR: 'tf' command not found in PATH", file=sys.stderr)
        return -1, ""
    except subprocess.TimeoutExpired:
        print("ERROR: 'tf --version' timed out after 30s", file=sys.stderr)
        return -1, ""


def is_valid_semver(version: str) -> bool:
    """Check if version matches basic SemVer format.
    
    Supports:
    - 0.1.0
    - 1.2.3
    - 1.2.3-alpha.1
    - 1.2.3+build.123
    - 1.2.3-alpha.1+build.123
    """
    # Basic SemVer pattern: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
    pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$'
    return bool(re.match(pattern, version))


@pytest.mark.smoke
def test_tf_version_exit_code() -> None:
    """Smoke test: tf --version should exit with code 0."""
    exit_code, _ = run_tf_version()
    assert exit_code == 0, f"Expected exit code 0, got {exit_code}"


@pytest.mark.smoke
def test_tf_version_output_non_empty() -> None:
    """Smoke test: tf --version should produce non-empty output."""
    _, output = run_tf_version()
    assert output, "Output should be non-empty"


@pytest.mark.smoke
def test_tf_version_valid_semver() -> None:
    """Smoke test: tf --version output should match SemVer format."""
    _, output = run_tf_version()
    assert is_valid_semver(output), f"Output '{output}' does not match SemVer format"
