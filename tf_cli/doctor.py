"""Compatibility shim for deprecated tf_cli.doctor module.

DEPRECATED: Use 'tf.doctor' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.doctor import *  # noqa: F401,F403
