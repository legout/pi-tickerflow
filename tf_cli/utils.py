"""Compatibility shim for deprecated tf_cli.utils module.

DEPRECATED: Use 'tf.utils' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.utils import *  # noqa: F401,F403
