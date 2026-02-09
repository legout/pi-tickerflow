"""Compatibility shim for deprecated tf_cli.asset_planner module.

DEPRECATED: Use 'tf.asset_planner' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.asset_planner import *  # noqa: F401,F403
