"""Compatibility shim for deprecated tf_cli.track module.

DEPRECATED: Use 'tf.track' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.track import *  # noqa: F401,F403
