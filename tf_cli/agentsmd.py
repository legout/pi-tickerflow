"""Compatibility shim for deprecated tf_cli.agentsmd module.

DEPRECATED: Use 'tf.agentsmd' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.agentsmd import *  # noqa: F401,F403
