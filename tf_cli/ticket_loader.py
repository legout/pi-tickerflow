"""Compatibility shim for deprecated tf_cli.ticket_loader module.

DEPRECATED: Use 'tf.ticket_loader' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.ticket_loader import *  # noqa: F401,F403
