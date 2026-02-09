"""Compatibility shim for deprecated tf_cli.ui module.

DEPRECATED: Use 'tf.ui' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.ui import *  # noqa: F401,F403
