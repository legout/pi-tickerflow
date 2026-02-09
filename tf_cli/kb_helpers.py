"""Compatibility shim for deprecated tf_cli.kb_helpers module.

DEPRECATED: Use 'tf.kb_helpers' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.kb_helpers import *  # noqa: F401,F403
