"""Compatibility shim for deprecated tf_cli.login module.

DEPRECATED: Use 'tf.login' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.login import *  # noqa: F401,F403
