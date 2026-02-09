"""Compatibility shim for deprecated tf_cli.tags_suggest module.

DEPRECATED: Use 'tf.tags_suggest' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.tags_suggest import *  # noqa: F401,F403
