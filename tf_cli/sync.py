"""Compatibility shim for deprecated tf_cli.sync module.

DEPRECATED: Use 'tf.sync' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.sync import *  # noqa: F401,F403
