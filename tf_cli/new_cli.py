"""Compatibility shim for deprecated tf_cli.new_cli module.

DEPRECATED: Use 'tf.new_cli' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.new_cli import *  # noqa: F401,F403
