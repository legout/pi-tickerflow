"""Compatibility shim for deprecated tf_cli.ticket_factory module.

DEPRECATED: Use 'tf.ticket_factory' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.ticket_factory import *  # noqa: F401,F403
