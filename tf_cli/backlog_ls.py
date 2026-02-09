"""Compatibility shim for deprecated tf_cli.backlog_ls module.

DEPRECATED: Use 'tf.backlog_ls' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.backlog_ls import *  # noqa: F401,F403
