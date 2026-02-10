"""Shared CLI utility module for root resolution and JSON helpers.

This module provides common utility functions used across multiple CLI modules
to avoid code duplication.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


# Default increment for timeout backoff calculation (milliseconds)
DEFAULT_TIMEOUT_INCREMENT_MS = 150000


def read_json(path: Path) -> Dict[str, Any]:
    """Read and parse a JSON file.
    
    Args:
        path: Path to the JSON file.
        
    Returns:
        The parsed JSON content as a dictionary. Returns an empty dict
        if the file doesn't exist or cannot be parsed.
    """
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def find_project_root(start: Optional[Path] = None) -> Optional[Path]:
    """Find the project root by looking for .tf or .pi directory.
    
    Searches upward from the starting directory (or current working directory)
    for a directory containing either a .tf or .pi subdirectory.
    
    Args:
        start: The directory to start searching from. Defaults to current working directory.
        
    Returns:
        The Path to the project root, or None if not found.
    """
    cwd = start or Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".tf").is_dir() or (parent / ".pi").is_dir():
            return parent
    return None


def merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries.
    
    Recursively merges dictionary b into dictionary a. For nested dictionaries,
    values from b are merged into a. For non-dict values, b's values overwrite a's.
    
    Args:
        a: The base dictionary.
        b: The dictionary to merge into a.
        
    Returns:
        A new dictionary containing the merged result.
    """
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = v
    return out


def calculate_timeout_backoff(
    base_ms: int,
    increment_ms: int,
    iteration_index: int,
    max_ms: int | None = None,
) -> int:
    """Calculate effective timeout per iteration using linear backoff.

    Computes timeout as: effective = base_ms + iteration_index * increment_ms

    When max_ms is provided, the result is capped at that value to prevent
    runaway execution times.

    Args:
        base_ms: Base timeout in milliseconds. Must be non-negative.
        increment_ms: Additional timeout per iteration in milliseconds.
                     Must be non-negative.
        iteration_index: Zero-based iteration index (0 = first iteration).
                        Must be non-negative.
        max_ms: Optional maximum cap in milliseconds. If None, no cap is applied.
                If provided, must be >= base_ms.

    Returns:
        Effective timeout in milliseconds for the given iteration.

    Raises:
        ValueError: If any parameter is negative, or if max_ms < base_ms.

    Examples:
        >>> calculate_timeout_backoff(60000, DEFAULT_TIMEOUT_INCREMENT_MS, 0)
        60000
        >>> calculate_timeout_backoff(60000, DEFAULT_TIMEOUT_INCREMENT_MS, 1)
        210000
        >>> calculate_timeout_backoff(60000, DEFAULT_TIMEOUT_INCREMENT_MS, 2, max_ms=300000)
        300000
    """
    if base_ms < 0:
        raise ValueError(f"base_ms must be non-negative, got {base_ms}")
    if increment_ms < 0:
        raise ValueError(f"increment_ms must be non-negative, got {increment_ms}")
    if iteration_index < 0:
        raise ValueError(f"iteration_index must be non-negative, got {iteration_index}")
    if max_ms is not None and max_ms < base_ms:
        raise ValueError(
            f"max_ms ({max_ms}) must be >= base_ms ({base_ms})"
        )

    effective = base_ms + iteration_index * increment_ms
    if max_ms is not None:
        effective = min(effective, max_ms)
    return effective
