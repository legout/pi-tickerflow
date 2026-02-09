"""Compatibility shim for deprecated tf_cli.seed_cli module.

DEPRECATED: Use 'tf.seed_cli' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.seed_cli import *  # noqa: F401,F403
