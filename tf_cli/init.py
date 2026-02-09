"""Compatibility shim for deprecated tf_cli.init module.

DEPRECATED: Use 'tf.init' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.init import *  # noqa: F401,F403
