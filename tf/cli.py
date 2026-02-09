"""CLI entrypoint for tf command.

This module provides the main entrypoint for the `tf` console script.
It imports from tf_cli.cli for backward compatibility during the migration.
"""
from __future__ import annotations

# Import main from tf_cli for backward compatibility
# This allows gradual migration of code from tf_cli to tf
from tf_cli.cli import main

__all__ = ["main"]
