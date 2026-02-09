"""Compatibility shim for deprecated tf_cli.logger module.

DEPRECATED: Use 'tf.logger' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.logger import *  # noqa: F401,F403
