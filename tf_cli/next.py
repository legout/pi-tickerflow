"""Compatibility shim for deprecated tf_cli.next module.

DEPRECATED: Use 'tf.next' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.next import *  # noqa: F401,F403
