"""Compatibility shim for deprecated tf_cli.update module.

DEPRECATED: Use 'tf.update' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.update import *  # noqa: F401,F403
