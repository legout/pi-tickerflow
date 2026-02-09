"""Compatibility shim for deprecated tf_cli.component_classifier module.

DEPRECATED: Use 'tf.component_classifier' instead. This shim will be removed in version 0.5.0.
"""
from __future__ import annotations

from tf.component_classifier import *  # noqa: F401,F403
