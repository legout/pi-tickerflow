"""Compatibility shim for deprecated tf_cli.hello module.

DEPRECATED: Use 'tf.hello' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.hello import *  # noqa: F401,F403
