"""Compatibility shim for deprecated tf_cli.kb_cli module.

DEPRECATED: Use 'tf.kb_cli' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.kb_cli import *  # noqa: F401,F403
