"""Compatibility shim for deprecated tf_cli.session_store module.

DEPRECATED: Use 'tf.session_store' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.session_store import *  # noqa: F401,F403
