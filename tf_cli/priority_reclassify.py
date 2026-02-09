"""Compatibility shim for deprecated tf_cli.priority_reclassify module.

DEPRECATED: Use 'tf.priority_reclassify' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.priority_reclassify import *  # noqa: F401,F403
