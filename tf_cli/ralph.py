"""Compatibility shim for deprecated tf_cli.ralph module.

DEPRECATED: Use 'tf.ralph' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.ralph import *  # noqa: F401,F403
