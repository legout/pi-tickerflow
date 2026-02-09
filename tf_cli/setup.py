"""Compatibility shim for deprecated tf_cli.setup module.

DEPRECATED: Use 'tf.setup' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.setup import *  # noqa: F401,F403
