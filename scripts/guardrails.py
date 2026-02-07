#!/usr/bin/env python3
"""
Repository guardrails to prevent committing oversized files and forbidden paths.

This script checks:
1. File sizes against a configurable maximum threshold
2. Paths against a list of forbidden patterns (build/runtime artifacts)

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Set

# Default configuration
DEFAULT_MAX_SIZE_MB = 5
DEFAULT_MAX_SIZE_BYTES = DEFAULT_MAX_SIZE_MB * 1024 * 1024

# Forbidden paths patterns (directories and files that shouldn't be committed)
DEFAULT_FORBIDDEN_PATTERNS = [
    # Python virtual environments
    r"\.venv(/|$)",
    r"^venv(/|$)",
    r"^env(/|$)",
    r"^\.env(/|$)",
    # Python cache and build artifacts
    r"__pycache__(/|$)",
    r"\.pytest_cache(/|$)",
    r"\.mypy_cache(/|$)",
    r"\.tox(/|$)",
    r"\.egg-info(/|$)",
    r"^\.eggs(/|$)",
    # Build directories
    r"^build(/|$)",
    r"^dist(/|$)",
    r"^target(/|$)",  # Rust
    r"^out(/|$)",
    r"^output(/|$)",
    # Node.js
    r"node_modules(/|$)",
    r"\.next(/|$)",
    r"\.nuxt(/|$)",
    # Coverage and test artifacts
    r"\.coverage($|\.)",
    r"^htmlcov(/|$)",
    r"^coverage(/|$)",
    # IDE and editor files
    r"\.idea(/|$)",
    r"\.vscode(/|$)",
    # OS files
    r"\.DS_Store$",
    r"Thumbs\.db$",
    # Logs
    r"\.log$",
]


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Check repository for oversized files and forbidden paths."
    )
    parser.add_argument(
        "--max-size-mb",
        type=int,
        default=DEFAULT_MAX_SIZE_MB,
        help=f"Maximum allowed file size in MB (default: {DEFAULT_MAX_SIZE_MB})",
    )
    parser.add_argument(
        "--staged-only",
        action="store_true",
        help="Only check staged files (for pre-commit hook)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only output on failure",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Specific paths to check (default: entire repo)",
    )
    return parser.parse_args()


def get_staged_files() -> List[str]:
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [f for f in result.stdout.strip().split("\n") if f]
    except subprocess.CalledProcessError:
        return []


def get_all_files(paths: List[str]) -> List[str]:
    """Get all files in the repository, respecting .gitignore."""
    try:
        if paths:
            # Use git check-ignore to filter out ignored files
            files = []
            for path in paths:
                if os.path.isfile(path):
                    files.append(path)
                elif os.path.isdir(path):
                    for root, _, filenames in os.walk(path):
                        for filename in filenames:
                            filepath = os.path.join(root, filename)
                            # Check if file is ignored by git
                            try:
                                result = subprocess.run(
                                    ["git", "check-ignore", "-q", filepath],
                                    capture_output=True,
                                )
                                if result.returncode != 0:  # Not ignored
                                    files.append(filepath)
                            except (subprocess.CalledProcessError, FileNotFoundError):
                                # If git check-ignore fails, include the file
                                files.append(filepath)
            return files
        else:
            # Use git ls-files to respect .gitignore
            result = subprocess.run(
                ["git", "ls-files"],
                capture_output=True,
                text=True,
                check=True,
            )
            return [f for f in result.stdout.strip().split("\n") if f]
    except subprocess.CalledProcessError:
        return []


def check_file_size(filepath: str, max_size_bytes: int) -> Tuple[bool, int]:
    """Check if a file exceeds the size limit.

    Returns:
        Tuple of (is_ok, actual_size)
    """
    try:
        size = os.path.getsize(filepath)
        return size <= max_size_bytes, size
    except (OSError, IOError):
        return True, 0


def check_forbidden_path(filepath: str, patterns: List[str]) -> Tuple[bool, str]:
    """Check if a path matches any forbidden pattern.

    Returns:
        Tuple of (is_ok, matched_pattern)
    """
    for pattern in patterns:
        if re.search(pattern, filepath):
            return False, pattern
    return True, ""


def format_size(size_bytes: int) -> str:
    """Format byte size as human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}MB"


def main() -> int:
    """Main entry point."""
    args = parse_args()

    max_size_bytes = args.max_size_mb * 1024 * 1024

    # Get files to check
    if args.staged_only:
        files = get_staged_files()
    else:
        files = get_all_files(args.paths)

    if not files:
        if not args.quiet:
            print("No files to check.")
        return 0

    # Track violations
    oversized_files: List[Tuple[str, int]] = []
    forbidden_paths: List[Tuple[str, str]] = []

    # Check each file
    for filepath in files:
        if not os.path.exists(filepath):
            continue

        # Check size
        is_ok, size = check_file_size(filepath, max_size_bytes)
        if not is_ok:
            oversized_files.append((filepath, size))

        # Check forbidden path
        is_ok, pattern = check_forbidden_path(filepath, DEFAULT_FORBIDDEN_PATTERNS)
        if not is_ok:
            forbidden_paths.append((filepath, pattern))

    # Report results
    has_violations = bool(oversized_files or forbidden_paths)

    if has_violations or not args.quiet:
        print("=" * 60)
        print("REPOSITORY GUARDRAILS CHECK")
        print("=" * 60)
        print()

    if oversized_files:
        print(f"❌ OVERSIZED FILES (max {args.max_size_mb}MB):")
        for filepath, size in sorted(oversized_files, key=lambda x: -x[1]):
            print(f"   {filepath} ({format_size(size)})")
        print()

    if forbidden_paths:
        print("❌ FORBIDDEN PATHS:")
        for filepath, pattern in sorted(forbidden_paths):
            print(f"   {filepath} (matched: {pattern})")
        print()

    if not has_violations:
        if not args.quiet:
            print(f"✅ All checks passed ({len(files)} files checked)")
            print(f"   - Max file size: {args.max_size_mb}MB")
            print(f"   - Forbidden patterns: {len(DEFAULT_FORBIDDEN_PATTERNS)}")
        return 0
    else:
        print("=" * 60)
        print("GUARDRAILS FAILED")
        print("=" * 60)
        print()
        print("Please fix the above issues before committing.")
        print()
        print("To bypass in exceptional cases (use with caution):")
        print("   git commit --no-verify")
        return 1


if __name__ == "__main__":
    sys.exit(main())
